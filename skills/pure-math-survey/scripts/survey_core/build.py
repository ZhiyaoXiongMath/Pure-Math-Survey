"""Actual TeX/BibTeX build and full-page rasterization. Neither is visual review."""
from __future__ import annotations
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
from .common import all_files, atomic_bytes, diagnostic, file_hash, file_inventory, now, read_json, require, result, safe, sha, write_json, writer
from .exports import output_inputs,validate_structure,verify_generated
from .models import load_plan
from .history import archive_current, save_record

def executable(names:list[str])->str:
    for name in names:
        path=shutil.which(name)
        if path:return path
    raise FileNotFoundError('Required external executable not found: '+', '.join(names))

def run_command(command:list[str],cwd:Path,timeout:int=120,env:dict|None=None)->dict:
    proc=subprocess.run(command,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout,env=env)
    return {'command':command,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}

def pdf_pages(path:Path)->int:
    proc=run_command([executable(['pdfinfo']),path.name],path.parent)
    require(proc['returncode']==0,'BUILD_FAILED','pdfinfo could not read actual PDF',path.name)
    m=re.search(r'^Pages:\s+(\d+)',proc['stdout'],re.M)
    require(m,'BUILD_FAILED','PDF has no readable page count',path.name)
    return int(m[1])

def build_output(root:Path,output_id:str)->dict:
    out=safe(root,'outputs/'+output_id);plan=load_plan(out/'plan.json');verify_generated(root,plan)
    # Exact fragments and literal input safety are checked even for drafts.
    structure=validate_structure(root,output_id)
    hard=[e for e in structure['errors'] if e['code']!='MANUSCRIPT_INCOMPLETE']
    require(not hard,'BUILD_FAILED','Structural input errors: '+str(hard),'manuscript/main.tex')
    sources=file_inventory(out,sorted(output_inputs(out)))
    engine=executable(['pdflatex']);bib=executable(['bibtex','bibtex.original','bibtex8'])
    with writer(root):
        archive_current(out, 'legacy-build')
        stage=Path(tempfile.mkdtemp(prefix='.tex-build-',dir=out));compiled=stage/'compiled';compiled.mkdir()
        report={'built_at':now(),'output_id':output_id,'snapshot_id':plan['snapshot_id'],'source_inputs':sources,
                'commands':[],'tools':{},'status':'FAILED','stability_reached':False,'warnings':[]}
        try:
            for row in sources:
                atomic_bytes(safe(stage,row['path']),safe(out,row['path'],True).read_bytes())
            for key,path in [('pdflatex',engine),('bibtex',bib)]:
                version=run_command([path,'--version'],stage)
                report['tools'][key]={'executable':path,'version':version['stdout'].splitlines()[0] if version['stdout'] else version['stderr'].splitlines()[0]}
            env=os.environ.copy();env['openout_any']='p'
            previous=None;bib_done=False
            for turn in range(1,7):
                cmd=[engine,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode','-file-line-error','-recorder','-output-directory=../compiled','main.tex']
                proc=run_command(cmd,stage/'manuscript',env=env);report['commands'].append(proc)
                atomic_bytes(compiled/f'pass-{turn}.txt',(proc['stdout']+proc['stderr']).encode())
                require(proc['returncode']==0,'BUILD_FAILED',f'TeX pass {turn} failed; actual logs retained','build')
                aux=(compiled/'main.aux').read_text(errors='replace')
                if '\\bibdata' in aux and '\\citation' in aux and not bib_done:
                    p=run_command([bib,'main'],compiled,env=env);report['commands'].append(p)
                    require(p['returncode']==0,'BUILD_FAILED','BibTeX failed; inspect build report','build')
                    bib_done=True;previous=None;continue
                digest=sha(b''.join((compiled/('main'+ext)).read_bytes() if (compiled/('main'+ext)).exists() else b'' for ext in ('.aux','.toc','.out','.bbl')))
                if turn>=2 and digest==previous:report['stability_reached']=True;break
                previous=digest
            from build_checks import log_issues,log_warnings
            log=(compiled/'main.log').read_text(errors='replace');issues=log_issues(log)
            if not report['stability_reached']:issues['unstable_auxiliary_files']=['Six passes did not stabilize.']
            report['blocking_log_issues']=issues;report['nonblocking_log_warnings']=log_warnings(log)
            require(not issues,'BUILD_FAILED','Blocking TeX log diagnostics: '+', '.join(issues),'build/main.log')
            pdf=compiled/'main.pdf';require(pdf.is_file() and pdf.read_bytes().startswith(b'%PDF-'),'BUILD_FAILED','Actual PDF missing','build/main.pdf')
            report.update({'status':'BUILT','pdf_sha256':sha(pdf.read_bytes()),'pages':pdf_pages(pdf),'passes':turn})
            require(file_inventory(out,sorted(output_inputs(out)))==sources,'BUILD_INPUT_CHANGED','Inputs changed while compiling; do not accept this build')
        except Exception as e:
            report['failure']=str(e)
            raise
        finally:
            write_json(compiled/'build-report.json',report)
            history_data={'inputs/'+row['path']:safe(stage,row['path'],True).read_bytes() for row in sources if safe(stage,row['path']).is_file()}
            history_data.update({'compiled/'+p:safe(compiled,p,True).read_bytes() for p in all_files(compiled)})
            record=save_record(out,'build',history_data)
            write_json(out/'history/latest-build.json',{'history_id':record['history_id'],'status':report['status'],'new_visual_review':'NOT_PERFORMED'})
            dest=out/'build'
            if dest.exists():shutil.rmtree(dest)
            compiled.rename(dest);shutil.rmtree(stage,ignore_errors=True)
    return result('output.build','BUILT',{'pdf':f'outputs/{output_id}/build/main.pdf','report':f'outputs/{output_id}/build/build-report.json','pages':report['pages'],'tools':report['tools']})

def check_build(out:Path)->tuple[dict,list[dict]]:
    errors=[];path=out/'build/build-report.json'
    if not path.is_file():return {},[diagnostic('BUILD_FAILED','No actual build report','build/build-report.json')]
    b=read_json(path)
    if b.get('status')!='BUILT' or not b.get('stability_reached') or b.get('blocking_log_issues'):
        errors.append(diagnostic('BUILD_FAILED','Build did not pass its actual checks','build/build-report.json'))
    if b.get('source_inputs')!=file_inventory(out,sorted(output_inputs(out))):
        errors.append(diagnostic('BUILD_STALE','Build source files no longer match actual inputs','build/build-report.json'))
    pdf=out/'build/main.pdf'
    if not pdf.is_file() or sha(pdf.read_bytes())!=b.get('pdf_sha256'):
        errors.append(diagnostic('BUILD_STALE','Actual PDF differs from built PDF','build/main.pdf'))
    elif pdf_pages(pdf)!=b.get('pages'):
        errors.append(diagnostic('BUILD_STALE','Actual PDF page count differs from report','build/main.pdf'))
    return b,errors

def render_output(root:Path,output_id:str,dpi:int=120)->dict:
    require(type(dpi) is int and 72<=dpi<=300,'CONTRACT_INVALID','Render DPI must be 72..300')
    out=safe(root,'outputs/'+output_id);b,errors=check_build(out)
    require(not errors,'BUILD_STALE','Rebuild current sources before rendering: '+str(errors))
    with writer(root):
        archive_current(out,'render')
        folder=out/'evidence/pages';folder.parent.mkdir(exist_ok=True)
        stage=Path(tempfile.mkdtemp(prefix='.pages-',dir=folder.parent))
        try:
            cmd=[executable(['pdftoppm']),'-png','-r',str(dpi),'../../build/main.pdf','page']
            # cwd=stage: relative ../../build is out/build.
            proc=run_command(cmd,stage)
            require(proc['returncode']==0,'RENDER_FAILED','pdftoppm failed: '+proc['stderr'])
            imgs=sorted(stage.glob('page-*.png'),key=lambda x:int(x.stem.split('-')[-1]))
            require(len(imgs)==b['pages'],'RENDER_FAILED','Renderer did not produce every page')
            pages=[{'page':i,'path':'evidence/pages/'+p.name,'sha256':sha(p.read_bytes())} for i,p in enumerate(imgs,1)]
            m={'rendered_at':now(),'pdf_path':'build/main.pdf','pdf_sha256':b['pdf_sha256'],'pages':pages,'dpi':dpi,
               'command':cmd,'tool_stdout':proc['stdout'],'tool_stderr':proc['stderr'],
               'status':'RENDERED_NOT_REVIEWED','meaning':'Image generation is not a human visual check.'}
            if folder.exists():shutil.rmtree(folder)
            stage.rename(folder);write_json(out/'evidence/render-manifest.json',m)
            archive_current(out,'render')
        finally:
            if stage.exists():shutil.rmtree(stage)
    return result('output.render','RENDERED_NOT_REVIEWED',{'manifest':f'outputs/{output_id}/evidence/render-manifest.json','pages':len(pages)})

def reading_budget(root:Path,output_id:str)->dict:
    """Only explicit max_pages blocks this separate, actual-PDF reading-budget check."""
    out=safe(root,'outputs/'+output_id);plan=load_plan(out/'plan.json');pages=pdf_pages(safe(out,'build/main.pdf',True));errors=[];warnings=[]
    maximum=plan['limits'].get('max_pages');threshold=plan['limits'].get('page_review_threshold')
    if maximum is not None and pages>maximum:errors.append(diagnostic('MAX_PAGES_EXCEEDED',f'{pages} actual pages exceed explicit maximum {maximum}','build/main.pdf'))
    if threshold is not None and pages>threshold:warnings.append(diagnostic('READING_LENGTH_ADVISORY',f'{pages} actual pages exceed nonblocking editorial suggestion {threshold}; preserve typography and scope','build/main.pdf'))
    return result('output.reading-budget','NEEDS_WORK' if errors else 'CHECKED',{'pages':pages,'profile':plan['profile'],'max_pages':maximum},errors,warnings)
