#!/usr/bin/env python3
"""Rebuild a byte-verified Survey manuscript package without a skill installation.

Does not copy historical approval to the new PDF. TeX inputs must be trusted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path,PurePosixPath
import re
import shutil
import subprocess
import sys


def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def command(args:list[str],cwd:Path)->dict:
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    return {'command':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def tool(*names:str)->str:
    for n in names:
        if shutil.which(n):return shutil.which(n)
    raise RuntimeError('External executable missing: '+', '.join(names))

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parent;dest=args.output.resolve()
    if dest.exists() or root==dest or root in dest.parents:raise ValueError('Use a new destination outside the package')
    m=json.loads((root/'package-manifest.json').read_text(encoding='utf-8'))
    expected={x['path'] for x in m['files']}|{'package-manifest.json'}
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    if actual!=expected:raise ValueError('Package has missing or extra members')
    for r in m['files']:
        p=PurePosixPath(r['path'])
        if p.is_absolute() or '..' in p.parts or '\\' in r['path'] or ':' in r['path']:raise ValueError('Unsafe member')
        f=root.joinpath(*p.parts)
        if any(x.is_symlink() for x in (f,*f.parents)) or sha(f.read_bytes())!=r['sha256']:raise ValueError('Changed package member: '+str(p))
    sys.path.insert(0,str(root/'runtime'))
    from build_checks import log_issues,log_warnings
    dest.mkdir(parents=True);build=dest/'build';build.mkdir()
    for folder in ('manuscript','generated'):shutil.copytree(root/folder,dest/folder)
    report={'status':'FAILED','snapshot_id':m['snapshot_id'],'commands':[],'review_status':'NOT_REVIEWED_NEW_BUILD','source_package_verified':True}
    try:
        engine=tool('pdflatex');bib=tool('bibtex','bibtex.original','bibtex8');previous=None;bibbed=False;stable=False
        for i in range(1,7):
            r=command([engine,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder','-output-directory=../build','main.tex'],dest/'manuscript');report['commands'].append(r)
            if r['returncode']:raise RuntimeError('TeX failed')
            aux=(build/'main.aux').read_text(errors='replace')
            if '\\bibdata' in aux and '\\citation' in aux and not bibbed:
                r=command([bib,'main'],build);report['commands'].append(r)
                if r['returncode']:raise RuntimeError('BibTeX failed')
                bibbed=True;previous=None;continue
            digest=sha(b''.join((build/('main'+e)).read_bytes() if (build/('main'+e)).exists() else b'' for e in ('.aux','.toc','.out','.bbl')))
            if previous==digest and i>=2:stable=True;break
            previous=digest
        log=(build/'main.log').read_text(errors='replace');issues=log_issues(log)
        if not stable or issues:raise RuntimeError('Unstable or blocking TeX diagnostics: '+str(issues))
        info=command([tool('pdfinfo'),'main.pdf'],build);report['commands'].append(info)
        page=re.search(r'^Pages:\s*(\d+)',info['stdout'],re.M)
        if info['returncode'] or not page:raise RuntimeError('Actual PDF unreadable')
        report.update({'status':'BUILT','pages':int(page[1]),'pdf_sha256':sha((build/'main.pdf').read_bytes()),'passes':i,
                       'auxiliary_stable':stable,'blocking_log_issues':issues,'warnings':log_warnings(log)})
    except Exception as e:report['failure']=str(e)
    (dest/'rebuild-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return 0 if report['status']=='BUILT' else 4

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,subprocess.SubprocessError) as e:
        print(json.dumps({'status':'FAILED','error':str(e)}));raise SystemExit(4)
