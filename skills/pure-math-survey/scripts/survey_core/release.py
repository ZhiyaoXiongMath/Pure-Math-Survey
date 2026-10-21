"""Mechanical output packaging: exact inputs, successful build and safe members."""
from __future__ import annotations
from pathlib import Path
import json
import tempfile
import zipfile
from .common import FONT_SUFFIXES,SKILL_ROOT,VERSION,all_files,read_json,diagnostic,require,result,safe,sha,writer
from .models import load_plan, load_project
from .exports import output_inputs,validate_structure
from .build import check_build


def assess_release(root:Path,output_id:str)->dict:
    load_project(root)
    out=safe(root,'outputs/'+output_id);plan=load_plan(out/'plan.json')
    structure=validate_structure(root,output_id)
    built,errors=check_build(out);errors=structure['errors']+errors
    maximum=plan['limits'].get('max_pages')
    if built.get('pages') and maximum is not None and built['pages']>maximum:
        errors.append(diagnostic('MAX_PAGES_EXCEEDED','Actual PDF exceeds explicit max_pages','build/main.pdf'))
    return result('output.package-check','NEEDS_WORK' if errors else 'PACKAGEABLE',
                  {'output_id':output_id,'input_hash':read_json(out/'generated/manifest.json')['input_hash'],
                   'meaning':'Mechanical package checks only; no mathematical or visual certification.'},errors)


def package_output(root:Path,output_id:str,destination:Path)->dict:
    check=assess_release(root,output_id)
    if check['errors']:
        from .common import SurveyError
        raise SurveyError('PACKAGE_NOT_READY','Package blocked; run output validate --stage package for individual findings',exit_code=3)
    require(not destination.exists(),'DESTINATION_EXISTS','Package target exists; use a new path',destination.name)
    out=safe(root,'outputs/'+output_id);paths=set(output_inputs(out))|set(all_files(out,'build'))
    # A package contains the writing materials, not the entire knowledge project or external source archive.
    data={p:safe(out,p,True).read_bytes() for p in sorted(paths)}
    from .plans import validate_plan
    inv=validate_plan(root,load_plan(out/'plan.json'))
    from .sources import original_hashes
    source_hashes=original_hashes(inv)
    for path,b in data.items():
        require(not any(part.casefold() in {'private','.private'} for part in path.split('/'))
                and sha(b) not in source_hashes,'SOURCE_ORIGINAL_NOT_PACKAGED','Original bytes and private paths cannot enter manuscript packages',path)
    data['rebuild.py']=(SKILL_ROOT/'assets/rebuild/rebuild.py').read_bytes()
    data['runtime/build_checks.py']=(SKILL_ROOT/'scripts/build_checks.py').read_bytes()
    data['release-check.json']=(json.dumps(check,ensure_ascii=False,indent=2)+'\n').encode()
    data['README.md']=(f'# {output_id}\n\nFixed Survey output package; inspect plan.json for profile and prepared input hash.\n\n'
                       'Run `python3 -I rebuild.py --output ../rebuilt-output` in this extracted folder. The target must not exist and must lie outside this package.\n'
                       'Python 3.10+, pdfLaTeX, BibTeX (or the recorded fallback), and Poppler are required. No pip packages are needed.\n'
                       'The included PDF was built from the recorded inputs. A new build is reproducibility evidence; neither build certifies mathematics or visual quality.\n'
                       'Knowledge source identities and selected readable materials are included; original source PDFs are not automatically redistributed. '
                       'A nullable raw-source hash is an explicit access limitation, not a PDF byte certificate.\n'
                       'TeX is trusted code. Shell escape is disabled, but this is not a security sandbox for hostile TeX.\n').encode()
    for path in data:require(Path(path).suffix.lower() not in FONT_SUFFIXES,'FONT_NOT_DISTRIBUTABLE','Never distribute font files',path)
    manifest={'schema_version':VERSION,'files':[{'path':p,'sha256':sha(b),'bytes':len(b)} for p,b in sorted(data.items())],
              'input_hash':check['artifacts']['input_hash'],'original_pdf_sha256':sha(data['build/main.pdf'])}
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
    return result('output.package','PACKAGED',{'archive':str(destination),'sha256':sha(destination.read_bytes()),'members':len(data),'input_hash':manifest['input_hash']},warnings=check['warnings'])
