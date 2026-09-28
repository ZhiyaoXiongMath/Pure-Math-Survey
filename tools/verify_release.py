#!/usr/bin/env python3
"""Verify install ZIP, then execute it in a fresh no-pip virtual environment.

No host skill installation, source changes or new accepted reviews are made.
"""
from __future__ import annotations
import argparse
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/pure-math-survey/scripts'))
from package_release import verify_archive


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=Path)
    ap.add_argument('--report',type=Path);ap.add_argument('--no-build',action='store_true',help='Explicitly skip external TeX; reported as NOT_EXECUTED.')
    ap.add_argument('--example-root',type=Path,help='Reviewed three-profile matrix-tree project; needed for builds when examples are distributed separately.')
    ap.add_argument('--work-directory',type=Path,help='Parent of a short-lived staging directory; use a shallow path for deeply nested historical Windows artifacts.')
    args=ap.parse_args();report={'status':'RUNNING','checks':[],'archive':args.archive.name,'python':sys.version}
    def check(command:list[str],cwd:Path,env:dict)->dict:
        p=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        row={'command':command,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr};report['checks'].append(row)
        if p.returncode:raise RuntimeError(p.stdout+p.stderr)
        return json.loads(p.stdout)
    try:
        report['archive_verification']=verify_archive(args.archive)
        if args.work_directory:args.work_directory.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='pms-',dir=args.work_directory) as td:
            base=Path(td);dest=base/'unpacked'
            with zipfile.ZipFile(args.archive) as z:z.extractall(dest)
            venv.EnvBuilder(with_pip=False,system_site_packages=False).create(base/'venv')
            exe=base/'venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
            env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
            skill=dest/'pure-math-survey';entry=skill/'scripts/survey.py'
            v=check([str(exe),'-I',str(entry),'--json','--version'],base,env)
            if v['artifacts']['version']!='2.0.2':raise AssertionError('Wrong installed version')
            code="import importlib,json,pkgutil,sys;sys.path.insert(0,"+repr(str(skill/'scripts'))+");import survey_core;mods={m.name:importlib.import_module('survey_core.'+m.name).__file__ for m in pkgutil.iter_modules(survey_core.__path__)};print(json.dumps({'prefix':sys.prefix,'modules':mods}))"
            loaded=check([str(exe),'-I','-c',code],base,env)
            if not loaded['modules'] or any(not Path(f).is_relative_to(skill) for f in loaded['modules'].values()):raise AssertionError('Imported source-tree module instead of installed one')
            assets=check([str(exe),'-I',str(skill/'scripts/validate_assets.py'),'--json'],base,env)
            if set(assets['profile_preparations_executed'])!={'minimal','thematic','lecture'}:raise AssertionError('Not all installed profile resources executed')
            (base/'scope.md').write_text('# Scope\n\nRecord incidence-matrix conventions without requesting any manuscript.\n')
            project=base/'notebook'
            check([str(exe),'-I',str(entry),'--json','init','--output',str(project),'--topic','clean-install','--scope',str(base/'scope.md')],base,env)
            check([str(exe),'-I',str(entry),'--json','kb','validate',str(project)],base,env)
            f=check([str(exe),'-I',str(entry),'--json','kb','freeze',str(project)],base,env)
            check([str(exe),'-I',str(entry),'--json','kb','verify',str(project),'--snapshot',f['artifacts']['snapshot_id']],base,env)
            if list((project/'outputs').glob('*/plan.json')):raise AssertionError('Knowledge initialization generated a manuscript')
            report['clean_environment']={'venv_with_pip':False,'system_site_packages':False,'isolated_python':True,'runtime_modules_imported':len(loaded['modules']),'knowledge_only_outputs':0}
            if not args.no_build:
                example=args.example_root or ROOT/'examples/matrix-tree'
                if not example.is_dir():raise FileNotFoundError('Supply --example-root with the reviewed matrix-tree project, or explicitly use --no-build.')
                copied=base/'relocated-tree';shutil.copytree(example,copied,ignore=shutil.ignore_patterns('__pycache__','.cache'))
                report['installed_profile_builds']=[]
                for profile,expected_pages in [('minimal',2),('lecture',3),('thematic',2)]:
                    oid='trees-'+profile
                    rel=check([str(exe),'-I',str(entry),'--json','output','validate',str(copied),'--output',oid,'--stage','release'],base,env)
                    if rel['status']!='RELEASABLE':raise AssertionError('Relocated reviewed output no longer validates')
                    built=check([str(exe),'-I',str(entry),'--json','output','build',str(copied),'--output',oid],base,env)
                    if built['status']!='BUILT' or built['artifacts']['pages']!=expected_pages:raise AssertionError('Installed entry could not really build '+oid)
                    hist=check([str(exe),'-I',str(entry),'--json','output','history',str(copied),'--output',oid],base,env)
                    report['installed_profile_builds'].append({'profile':profile,'pages':expected_pages,'status':'BUILT','review_status':'NOT_REVIEWED_NEW_BUILD','history':hist['status']})
                report['installed_tex_build']='Three profiles BUILT; new copied PDFs have not received new visual reviews'
            else:report['installed_tex_build']='NOT_EXECUTED (--no-build)'
        report['status']='PASS'
    except (AssertionError,ValueError,OSError,RuntimeError,subprocess.SubprocessError,zipfile.BadZipFile) as e:report.update(status='FAIL',failure=str(e))
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if report['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
