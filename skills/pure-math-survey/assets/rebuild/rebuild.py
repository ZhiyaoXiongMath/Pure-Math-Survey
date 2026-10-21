#!/usr/bin/env python3
"""Rebuild a byte-verified Survey manuscript package without a skill installation.

Build evidence only; no mathematical certification. TeX inputs must be trusted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from decimal import Decimal
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

def emergency_stretch_argument(value:float|None)->tuple[str,dict]:
    """Same opt-in line-breaking parameter as the installed builder."""
    if value is None:return 'main.tex',{}
    if type(value) not in (int,float) or not math.isfinite(value) or not 0<value<=10:
        raise ValueError('emergency_stretch_em must be finite and in (0, 10]')
    amount=format(Decimal(str(value)),'f')
    if '.' in amount:amount=amount.rstrip('0').rstrip('.')
    argument=(r'\AddToHook{begindocument/end}{\emergencystretch='+amount+
              r'em\typeout{PMS-EMERGENCY-STRETCH-PT: \the\emergencystretch}}\input{main.tex}')
    return argument,{'emergency_stretch_em':value,'application':'begindocument/end',
                     'effective_emergency_stretch_pt':None}


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--emergency-stretch-em',type=float,help='Explicit normal line-breaking adjustment after style loading; default keeps original behavior.');args=ap.parse_args()
    tex_argument,layout=emergency_stretch_argument(args.emergency_stretch_em)
    root=Path(__file__).resolve().parent;dest=args.output.resolve()
    if dest.exists() or root==dest or root in dest.parents:raise ValueError('Use a new destination outside the package')
    m=json.loads((root/'package-manifest.json').read_text(encoding='utf-8'))
    if m.get('schema_version')!='3.0.0' or not isinstance(m.get('input_hash'),str) or not re.fullmatch('[a-f0-9]{64}',m['input_hash']):
        raise ValueError('Unsupported package identity; expected schema 3.0.0 and prepared input hash')
    expected={x['path'] for x in m['files']}|{'package-manifest.json'}
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    if actual!=expected:raise ValueError('Package has missing or extra members')
    for r in m['files']:
        p=PurePosixPath(r['path'])
        if p.is_absolute() or '..' in p.parts or '\\' in r['path'] or ':' in r['path']:raise ValueError('Unsafe member')
        f=root.joinpath(*p.parts)
        if any(x.is_symlink() for x in (f,*f.parents)) or sha(f.read_bytes())!=r['sha256']:raise ValueError('Changed package member: '+str(p))
    sys.path.insert(0,str(root/'runtime'))
    from build_checks import log_issues,log_warnings,layout_measurements
    dest.mkdir(parents=True);build=dest/'build';build.mkdir()
    for folder in ('manuscript','generated'):shutil.copytree(root/folder,dest/folder)
    report={'status':'FAILED','input_hash':m['input_hash'],'commands':[],'layout':layout,'meaning':'Actual build only; mathematics is not certified','source_package_verified':True}
    try:
        engine=tool('pdflatex');bib=tool('bibtex','bibtex.original','bibtex8');previous=None;bibbed=False;stable=False
        for i in range(1,7):
            r=command([engine,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder','-output-directory=../build',*(['-jobname=main'] if layout else []),tex_argument],dest/'manuscript');report['commands'].append(r)
            if r['returncode']:raise RuntimeError('TeX failed')
            aux=(build/'main.aux').read_text(encoding='utf-8',errors='replace')
            if '\\bibdata' in aux and '\\citation' in aux and not bibbed:
                r=command([bib,'main'],build);report['commands'].append(r)
                if r['returncode']:raise RuntimeError('BibTeX failed')
                bibbed=True;previous=None;continue
            digest=sha(b''.join((build/('main'+e)).read_bytes() if (build/('main'+e)).exists() else b'' for e in ('.aux','.toc','.out','.bbl')))
            if previous==digest and i>=2:stable=True;break
            previous=digest
        log=(build/'main.log').read_text(encoding='utf-8',errors='replace');issues=log_issues(log)
        if layout:
            effective=re.search(r'PMS-EMERGENCY-STRETCH-PT:\s*([0-9.]+)pt',log)
            if effective is None:raise RuntimeError('Explicit emergency stretch was not observed in the TeX log')
            layout['effective_emergency_stretch_pt']=float(effective[1])
        report.update(auxiliary_stable=stable,blocking_log_issues=issues,warnings=log_warnings(log))
        if not stable or issues:raise RuntimeError('Unstable or blocking TeX diagnostics: '+str(issues))
        info=command([tool('pdfinfo'),'main.pdf'],build);report['commands'].append(info)
        page=re.search(r'^Pages:\s*(\d+)',info['stdout'],re.M)
        if info['returncode'] or not page:raise RuntimeError('Actual PDF unreadable')
        plan=json.loads((root/'plan.json').read_text(encoding='utf-8'))
        metrics,layout_errors=layout_measurements(log,int(page[1]),plan['limits'].get('max_pages') or 6)
        report.update(main_pages=metrics['main_pages'],total_pages=int(page[1]),layout_measurements=metrics,layout_errors=layout_errors)
        if layout_errors:raise RuntimeError('Layout/page constraints: '+'; '.join(layout_errors))
        report.update({'status':'BUILT','pages':int(page[1]),'pdf_sha256':sha((build/'main.pdf').read_bytes()),'passes':i,
                       'auxiliary_stable':stable,'blocking_log_issues':issues,'warnings':log_warnings(log)})
    except Exception as e:report['failure']=str(e)
    (dest/'rebuild-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return 0 if report['status']=='BUILT' else 4

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,subprocess.SubprocessError) as e:
        print(json.dumps({'status':'FAILED','error':str(e)}));raise SystemExit(4)
