"""Release re-reads evidence and actual artifacts. No historical PASS inheritance."""
from __future__ import annotations
from pathlib import Path
import json
import re
import shutil
import tempfile
import zipfile
from .common import FONT_SUFFIXES,SKILL_ROOT,all_files,diagnostic,file_hash,file_inventory,read_json,require,result,safe,sha,write_json,writer
from .models import load_plan
from .exports import output_inputs,validate_structure
from .readiness import assess_readiness
from .reviews import check_review_bindings,blocking_unchecked,reviews_in
from .build import check_build
from .tex import validate_locations

def semantic_scope_errors(out:Path,plan:dict,consumed_nodes:list[str],review:dict)->list[dict]:
    """Check a candidate in full before selecting it; invalid historical records
    cannot shadow a later, valid reread of the same manuscript bytes."""
    scope=review.get('scope',{}); errors=[]
    required={'whole_manuscript','canonical_use','conditions_quantifiers','selection',
              'attribution','proof_obligations','readability'}
    if scope.get('whole_manuscript') is not True or not required <= set(scope.get('checks',[])):
        errors.append(diagnostic('REVIEW_SCOPE_INSUFFICIENT','An explicit whole-manuscript review with all seven reading checks is required','evidence'))
    missing=set(consumed_nodes)-set(scope.get('node_ids',[]))
    if missing:
        errors.append(diagnostic('REVIEW_SCOPE_INSUFFICIENT','Semantic review omits consumed nodes: '+', '.join(sorted(missing)),'evidence'))
    if scope.get('profile')!=plan['profile']:
        errors.append(diagnostic('REVIEW_SCOPE_INSUFFICIENT','Semantic review must evaluate this actual reading profile','evidence'))
    for obligation in plan['proof_obligations']:
        key=obligation['node_id']
        if set(obligation['required_steps'])-set(scope.get('proof_steps',{}).get(key,[])):
            errors.append(diagnostic('PROOF_OBLIGATION_UNMET','Output semantic review has not checked all promised steps','evidence',key))
        errors.extend(validate_locations(out,scope.get('proof_locations',{}).get(key),node_id=key))
    for key in sorted({s['node_id'] for s in plan['selections'] if s['role']=='principal_answer'}):
        errors.extend(validate_locations(out,scope.get('principal_locations',{}).get(key),node_id=key,canonical=True))
    return errors

def assess_release(root:Path,output_id:str)->dict:
    out=safe(root,'outputs/'+output_id);plan=load_plan(out/'plan.json')
    ready=assess_readiness(root,plan);errors=list(ready['errors']);warnings=list(ready['warnings']);used=[]
    if plan['draft']:errors.append(diagnostic('DRAFT_NOT_RELEASABLE','Internal unverified drafts cannot be packaged as formal output','plan.json'))
    structure=validate_structure(root,output_id);errors+=structure['errors'];warnings+=structure['warnings']
    records=reviews_in(out,'evidence')
    # render-manifest and structure reports are not review records; reviews_in filters them below.
    inputs=output_inputs(out); sem=None;vis=None;sem_errors=[]
    for path,r in records:
        if r['kind']!='output_semantic' or output_id not in r.get('scope',{}).get('output_ids',[]):continue
        candidate_errors=check_review_bindings(out,r,inputs)
        candidate_errors+=semantic_scope_errors(out,plan,ready['artifacts']['consumed_nodes'],r)
        if r['disposition']=='accepted' and not blocking_unchecked(r) and not candidate_errors:
            sem=r;used.append(r['review_id']);break
        sem_errors+=candidate_errors
    if sem is None:
        errors+=sem_errors
        errors.append(diagnostic('OUTPUT_SEMANTIC_REVIEW_PENDING','Read this manuscript against the fixed nodes and promised proof depth; explicitly record reviewer mode','evidence'))
    built,b_errors=check_build(out);errors+=b_errors
    if built.get('status')=='BUILT' and not b_errors:
        pages=built['pages'];limit=plan['limits'].get('max_pages');threshold=plan['limits'].get('page_review_threshold')
        if limit is not None and pages>limit:errors.append(diagnostic('MAX_PAGES_EXCEEDED',f'Actual {pages} pages exceed explicit user limit {limit}','build/main.pdf'))
        if threshold is not None and pages>threshold:warnings.append(diagnostic('READING_LENGTH_ADVISORY',f'Actual {pages} pages exceed editorial suggestion {threshold}; do not shrink typography or remove conditions','build/main.pdf'))
        render_path=out/'evidence/render-manifest.json'
        render=read_json(render_path) if render_path.is_file() else {}
        rows=render.get('pages',[]);expected=list(range(1,pages+1))
        if render.get('pdf_sha256')!=built['pdf_sha256'] or [r.get('page') for r in rows]!=expected:
            errors.append(diagnostic('VISUAL_REVIEW_INCOMPLETE','Need render manifest for the actual entire PDF','evidence/render-manifest.json'))
        else:
            visual_inputs={'build/main.pdf','build/build-report.json','evidence/render-manifest.json'}|{r['path'] for r in rows}
            image_errors=[]
            for row in rows:
                p=safe(out,row['path'])
                if not p.is_file() or file_hash(out,row['path'])!=row.get('sha256'):
                    image_errors.append(diagnostic('REVIEW_STALE','Rendered image bytes have changed',row['path']))
            errors+=image_errors
            vis_stale=[]
            for path,r in records:
                if r['kind']!='visual' or output_id not in r.get('scope',{}).get('output_ids',[]):continue
                stale=check_review_bindings(out,r,visual_inputs)
                scope=r.get('scope',{});observations=scope.get('page_findings',[])
                valid=(scope.get('pdf_sha256')==built['pdf_sha256'] and scope.get('pages')==expected and
                       [x.get('page') for x in observations]==expected and all(isinstance(x.get('observation'),str) and len(x['observation'].strip())>=12 for x in observations))
                if valid and r['disposition']=='accepted' and not blocking_unchecked(r) and not stale and not image_errors:
                    vis=r;used.append(r['review_id']);break
                vis_stale+=stale
            if vis is None:errors+=vis_stale
            if vis is None:errors.append(diagnostic('VISUAL_REVIEW_INCOMPLETE','Actual full-page human observations and PDF/image-bound evidence are required','evidence'))
    if sem is None or sem['reviewer_mode']!='independent_review':
        warnings.append(diagnostic('NO_INDEPENDENT_REVIEW','No scoped independent mathematical reading of this manuscript is claimed. Author reread is not independent review.'))
    return result('output.release','NEEDS_WORK' if errors else 'RELEASABLE',{'output_id':output_id,'snapshot_id':plan['snapshot_id'],
                  'pages':built.get('pages'),'used_output_review_ids':used,'readiness':ready['status']},errors,warnings)

def package_output(root:Path,output_id:str,destination:Path)->dict:
    check=assess_release(root,output_id)
    if check['errors']:
        from .common import SurveyError
        code='DRAFT_NOT_RELEASABLE' if any(x['code']=='DRAFT_NOT_RELEASABLE' for x in check['errors']) else 'RELEASE_NOT_READY'
        raise SurveyError(code,'Release blocked; run output validate --stage release for individual findings',exit_code=3)
    require(not destination.exists(),'DESTINATION_EXISTS','Package target exists; use a new path',destination.name)
    out=safe(root,'outputs/'+output_id);paths=set(output_inputs(out))|set(all_files(out,'evidence'))|set(all_files(out,'build'))
    # A package contains the writing materials, not the entire knowledge project or external source archive.
    data={p:safe(out,p,True).read_bytes() for p in sorted(paths)}
    data['rebuild.py']=(SKILL_ROOT/'assets/rebuild/rebuild.py').read_bytes()
    data['runtime/build_checks.py']=(SKILL_ROOT/'scripts/build_checks.py').read_bytes()
    data['release-check.json']=(json.dumps(check,ensure_ascii=False,indent=2)+'\n').encode()
    data['README.md']=(f'# {output_id}\n\nFixed Survey output package; inspect plan.json for profile and snapshot ID.\n\n'
                       'Run `python -I rebuild.py --output ../rebuilt-output` in this extracted folder. The target must not exist and must lie outside this package.\n'
                       'Python 3.10+, pdfLaTeX, BibTeX (or the recorded fallback), and Poppler are required. No pip packages are needed.\n'
                       'The included PDF has the original scoped review. A new build is reproducibility evidence, not a new semantic or visual review.\n'
                       'Knowledge source identities and selected readable materials are included; original source PDFs are not automatically redistributed. '
                       'A nullable raw-source hash is an explicit access limitation, not a PDF byte certificate.\n'
                       'TeX is trusted code. Shell escape is disabled, but this is not a security sandbox for hostile TeX.\n').encode()
    for path in data:require(Path(path).suffix.lower() not in FONT_SUFFIXES,'FONT_NOT_DISTRIBUTABLE','Never distribute font files',path)
    manifest={'files':[{'path':p,'sha256':sha(b),'bytes':len(b)} for p,b in sorted(data.items())],
              'snapshot_id':check['artifacts']['snapshot_id'],'original_reviewed_pdf_sha256':sha(data['build/main.pdf'])}
    data['package-manifest.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    destination.parent.mkdir(parents=True,exist_ok=True)
    with writer(root):
        handle=tempfile.NamedTemporaryFile(prefix='.package-',suffix='.zip',dir=destination.parent,delete=False);temp=Path(handle.name);handle.close()
        try:
            with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
                for path,b in sorted(data.items()):z.writestr(output_id+'/'+path,b)
            with zipfile.ZipFile(temp) as z:
                require(len(z.namelist())==len(data),'PACKAGE_INVALID','Duplicate/missing archive members')
                for path,b in data.items():require(z.read(output_id+'/'+path)==b,'PACKAGE_INVALID','Archive verification failed',path)
            temp.rename(destination)
        finally:temp.unlink(missing_ok=True)
    return result('output.package','PACKAGED',{'archive':str(destination),'sha256':sha(destination.read_bytes()),'members':len(data),'snapshot_id':manifest['snapshot_id']},warnings=check['warnings'])
