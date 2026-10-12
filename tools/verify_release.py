#!/usr/bin/env python3
"""Verify install ZIP, then execute it in a fresh no-pip virtual environment.

No host skill installation, source changes or new accepted reviews are made.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import importlib
import json
import os
import re
import signal
import time
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


@contextmanager
def verification_workspace(report:dict,parent:Path|None=None,keep:bool=False):
    """Keep failed build inputs and logs available for diagnosis."""
    if parent:parent.mkdir(parents=True,exist_ok=True)
    base=Path(tempfile.mkdtemp(prefix='pms-',dir=parent))
    workspace={'path':str(base.resolve()),'retained':keep}
    report['workspace']=workspace
    try:
        yield base
    except BaseException:
        workspace['retained']=True
        raise
    finally:
        if not workspace['retained']:shutil.rmtree(base)


EXPECTED_POLICY = 'four-modes-2026-10-12-r3'
EXPECTED_CONTRACTS = {('2.0.0', 'legacy-2.0.0'),
                      ('2.1.0', 'four-modes-2026-10-11-r2'),
                      ('2.2.0', 'four-modes-2026-10-12-rc2'),
                      ('2.2.0', EXPECTED_POLICY)}


def assert_installed_contract(artifacts:dict)->dict:
    """Version identity and declared compatibility are separate from test success."""
    if (artifacts.get('version'), artifacts.get('schema_version'),
            artifacts.get('output_schema_version'), artifacts.get('editorial_policy')) != (
            '2.1.0', '2.0.0', '2.2.0', EXPECTED_POLICY):
        raise AssertionError('Installed runtime is not software 2.1.0 / KB 2.0.0 / output 2.2.0 / r3')
    contracts=artifacts.get('supported_output_contracts')
    if not isinstance(contracts,list) or len(contracts)!=4 or any(
            not isinstance(x,dict) or not isinstance(x.get('schema_version'),str) or
            not isinstance(x.get('editorial_policy'),str) for x in contracts):
        raise AssertionError('Installed runtime did not report four exact schema-policy contracts')
    pairs={(x['schema_version'],x['editorial_policy']) for x in contracts}
    if pairs != EXPECTED_CONTRACTS:
        raise AssertionError('Installed schema-policy compatibility pairs are missing or unexpected')
    return {'editorial_policy':EXPECTED_POLICY,'supported_contracts':artifacts['supported_output_contracts']}


def installed_regression_summary(stderr:str)->dict:
    count=re.search(r'Ran (\d+) tests',stderr)
    r3_rows=[line for line in stderr.splitlines() if '(test_r3_policy.' in line]
    if not count or not r3_rows or any(not line.rstrip().endswith('... ok') for line in r3_rows):
        raise AssertionError('Installed regression must actually execute the r3 policy suite without skips')
    return {'tests':int(count[1]),'r3_policy_tests':len(r3_rows),'status':'PASS',
            'synthetic_gates_are_not_mathematical_acceptance':True}


def terminate_process_tree(proc:subprocess.Popen)->dict:
    """Terminate this check's own children as well as the Python/TeX parent."""
    if os.name=='nt':
        done=subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True,
                            text=True,encoding='utf-8',errors='replace',timeout=15)
        return {'method':'taskkill /T /F','returncode':done.returncode,
                'stdout':done.stdout,'stderr':done.stderr}
    try:
        os.killpg(proc.pid,signal.SIGKILL)
        return {'method':'killpg SIGKILL','returncode':0}
    except ProcessLookupError:
        return {'method':'killpg SIGKILL','returncode':0,'already_exited':True}


def run_check(command:list[str],cwd:Path,env:dict,report:dict,decode:bool=True,timeout:int=180,allowed_returncodes:tuple[int,...]=(0,))->dict:
    if timeout<=0:raise ValueError('Check timeout must be positive')
    start=time.monotonic()
    proc=subprocess.Popen(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,encoding='utf-8',errors='replace',
                          start_new_session=os.name!='nt',
                          creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name=='nt' else 0)
    try:
        stdout,stderr=proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode('utf-8',errors='replace') if isinstance(value,bytes) else value or ''
        stdout,stderr=decoded(exc.stdout),decoded(exc.stderr)
        try:
            termination=terminate_process_tree(proc)
            stdout,stderr=proc.communicate(timeout=15)
        except (OSError,subprocess.SubprocessError) as cleanup:
            termination={'method':'process-tree termination','error':str(cleanup),'children_stopped':'UNCONFIRMED'}
            proc.kill()
            proc.wait(timeout=15)
            for pipe in (proc.stdout,proc.stderr):
                if pipe:pipe.close()
        report['checks'].append({'command':command,'cwd':str(cwd),'returncode':None,
                                'timeout_seconds':timeout,'elapsed_seconds':time.monotonic()-start,
                                'stdout':stdout,'stderr':stderr,'termination':termination,'expected_returncodes':list(allowed_returncodes)})
        raise subprocess.TimeoutExpired(command,timeout,output=stdout,stderr=stderr) from exc
    row={'command':command,'cwd':str(cwd),'returncode':proc.returncode,
         'timeout_seconds':timeout,'elapsed_seconds':time.monotonic()-start,
         'stdout':stdout,'stderr':stderr,'expected_returncodes':list(allowed_returncodes)}
    report['checks'].append(row)
    if proc.returncode not in allowed_returncodes:raise RuntimeError(stdout+stderr)
    return json.loads(stdout) if decode else row


def load_r3_manifest(path:Path)->list[dict]:
    """Private verifier input only; does not add a mathematical project schema."""
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict) or set(data)!={'projects'} or not isinstance(data['projects'],list) or not data['projects']:
        raise ValueError('r3 manifest needs a nonempty projects list')
    entries=[];seen=set()
    for item in data['projects']:
        if not isinstance(item,dict) or set(item)!={'path','outputs'} or not isinstance(item['path'],str):
            raise ValueError('Each r3 manifest project needs only path and outputs')
        source=(path.parent/item['path']).resolve()
        outputs=item['outputs']
        if not source.is_dir() or not (source/'project.json').is_file():raise ValueError('r3 source project does not exist: '+str(source))
        if not isinstance(outputs,list) or not outputs or any(not isinstance(x,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',x) for x in outputs):
            raise ValueError('r3 output IDs must be nonempty safe identifiers')
        if len(outputs)!=len(set(outputs)) or source in seen:raise ValueError('Duplicate r3 project or output')
        seen.add(source);entries.append({'path':source,'outputs':outputs})
    return entries


def verify_r3_outputs(entries:list[dict],base:Path,check,exe:Path,entry:Path,env:dict,build_timeout:int,build:bool,report:dict|None=None)->dict:
    """Rebuild only explicit real r3 inputs, never manufacture review acceptance."""
    import hashlib
    result={'status':'RUNNING','outputs':[],
            'original_paper_quality':'NOT VERIFIED; an internal draft is not original research acceptance'}
    if report is not None:report['r3_outputs']=result
    rows=result['outputs'];coverage=set();spines={}
    for index,item in enumerate(entries):
        source=item['path'];project=base/'r3-projects'/str(index)
        shutil.copytree(source,project,ignore=shutil.ignore_patterns('build','history','__pycache__'))
        for oid in item['outputs']:
            out=project/'outputs'/oid;plan=json.loads((out/'plan.json').read_text(encoding='utf-8'))
            if plan.get('output_id')!=oid or (plan.get('schema_version'),plan.get('editorial_policy'))!=('2.2.0',EXPECTED_POLICY):
                raise AssertionError('Requested real output does not carry r3 policy: '+oid)
            profile,view=plan.get('profile'),plan.get('view')
            if profile not in {'minimal','thematic','lecture','paper'}:raise AssertionError('Unknown real output profile')
            if profile=='paper' and plan.get('draft') is not True:raise AssertionError('The r3 Paper verification input must remain an internal draft: '+oid)
            if profile!='paper' and plan.get('draft'):raise AssertionError('Non-Paper r3 acceptance input must be an authored nondraft output: '+oid)
            source_hashes={name:hashlib.sha256((source/'outputs'/oid/name).read_bytes()).hexdigest()
                           for name in ('plan.json','outline.md','manuscript/main.tex')}
            call=lambda *args,**kwargs:check([str(exe),'-I',str(entry),'--json',*map(str,args)],base,env,**kwargs)
            call('kb','verify',project,'--snapshot',plan['snapshot_id'])
            call('output','validate',project,'--output',oid,'--stage','structure')
            coverage.add((profile,view))
            if profile=='minimal' and view in {'methods','boundaries'}:
                principals=sorted(x['node_id'] for x in plan['selections'] if x['role']=='principal_answer')
                boundaries=sorted(x['node_id'] for x in plan['selections'] if x['role']=='boundary')
                group=plan.get('comparison_group')
                if not group or not principals:raise AssertionError('Paired r3 Minimal inputs need an explicit comparison group and principal spine')
                canonical=tuple((key,hashlib.sha256((out/'generated/statements'/f'{key}.tex').read_bytes()).hexdigest()) for key in principals)
                spine=(group,plan['snapshot_id'],tuple(sorted(plan['question_ids'])),tuple(principals),tuple(boundaries),canonical)
                spines.setdefault(spine,set()).add(view)
            row={'source_project':str(source),'verification_project':str(project),'output_directory':str(out),
                 'build_report':str(out/'build/build-report.json'),'output_id':oid,'profile':profile,'view':view,
                 'editorial_policy':plan['editorial_policy'],'snapshot_id':plan['snapshot_id'],
                 'comparison_group':plan.get('comparison_group'),
                 'source_sha256':source_hashes,'new_visual_review':'NOT PERFORMED',
                 'mathematical_reading':'NOT PERFORMED; software verification only'}
            rows.append(row)
            if build:
                built=call('output','build',project,'--output',oid,timeout=build_timeout)
                rendered=call('output','render',project,'--output',oid,timeout=build_timeout)
                row.update(build=built['status'],pages=built['artifacts']['pages'],render=rendered['status'])
            else:row['build']='NOT EXECUTED (--no-build)'
            if profile=='paper':
                release=call('output','validate',project,'--output',oid,'--stage','release',allowed_returncodes=(3,))
                blocked=base/'forbidden-paper'/f'{index}-{oid}.zip'
                packaged=call('output','package',project,'--output',oid,'--to',blocked,allowed_returncodes=(3,))
                if any('DRAFT_NOT_RELEASABLE' not in {e.get('code') for e in r.get('errors',[])} for r in (release,packaged)) or blocked.exists():
                    raise AssertionError('Paper draft did not preserve its formal release/package barrier')
                row['formal_release']='BLOCKED: DRAFT_NOT_RELEASABLE'
                row['formal_package']='BLOCKED: no archive created'
    profiles={p for p,_ in coverage}
    missing={'minimal','thematic','lecture','paper'}-profiles
    if missing or not {('minimal','methods'),('minimal','boundaries')}<=coverage:
        raise AssertionError('Real r3 inputs require all four profiles and Minimal methods/boundaries; missing '+str(sorted(missing)))
    if not any({'methods','boundaries'}<=views for views in spines.values()):
        raise AssertionError('r3 Minimal methods/boundaries do not share the requested snapshot, question, principal, boundary and canonical spine')
    result['paired_canonical_spine']='IDENTICAL: actual emphasis still requires reading'
    result['status']='BUILT_NOT_VISUALLY_REVIEWED' if build else 'NOT_EXECUTED'
    return result


def resolve_r3_manifest(explicit:Path|None,repository:Path)->Path|None:
    if explicit is not None:return explicit
    default=repository/'examples/r3/verification-manifest.json'
    return default if default.is_file() else None


def verification_completion(has_r3_inputs:bool,no_build:bool)->tuple[str,list[str]]:
    incomplete=[]
    if no_build:incomplete.append('Actual TeX builds were explicitly omitted')
    if not has_r3_inputs:incomplete.append('Real r3 manuscript inputs were not supplied')
    return ('INCOMPLETE' if incomplete else 'PASS'),incomplete


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=Path)
    ap.add_argument('--report',type=Path);ap.add_argument('--no-build',action='store_true',help='Explicitly skip external TeX; reported as NOT_EXECUTED.')
    ap.add_argument('--example-root',type=Path,help='Directory containing the authored schur and compactness projects (default: examples/vnext/projects).')
    ap.add_argument('--work-directory',type=Path,help='Parent of a short-lived staging directory; use a shallow path for deeply nested historical Windows artifacts.')
    ap.add_argument('--r3-manifest',type=Path,help='Private JSON projects/path/outputs input list for actual r3 manuscripts; missing input leaves verification INCOMPLETE.')
    ap.add_argument('--tests-timeout',type=int,default=1200,help='Seconds allowed for the full installed regression suite (default 1200).')
    ap.add_argument('--build-timeout',type=int,default=1200,help='Seconds allowed per example-verifier or r3 build/render call (default 1200).')
    ap.add_argument('--keep-work-directory',action='store_true',help='Also retain successful installation/build artifacts. Failed verification artifacts are always retained.')
    args=ap.parse_args()
    if args.tests_timeout<=0 or args.build_timeout<=0:ap.error('Timeouts must be positive seconds')
    args.r3_manifest=resolve_r3_manifest(args.r3_manifest,ROOT)
    report={'status':'RUNNING','checks':[],'archive':args.archive.name,'python':sys.version,
            'r3_manifest':str(args.r3_manifest.resolve()) if args.r3_manifest else None,
            'timeouts':{'installed_tests':args.tests_timeout,'build_or_render':args.build_timeout},
            'scope':'Installation and build verification, not mathematical/exposition/page acceptance'}
    initial_status,initial_incomplete=verification_completion(bool(args.r3_manifest),args.no_build)
    if initial_incomplete:report['incomplete']=initial_incomplete
    def check(command:list[str],cwd:Path,env:dict,decode:bool=True,timeout:int=180,allowed_returncodes:tuple[int,...]=(0,))->dict:
        return run_check(command,cwd,env,report,decode,timeout,allowed_returncodes)
    try:
        report['archive_verification']=verify_archive(args.archive)
        with verification_workspace(report,args.work_directory,args.keep_work_directory) as base:
            dest=base/'unpacked'
            with zipfile.ZipFile(args.archive) as z:z.extractall(dest)
            venv.EnvBuilder(with_pip=False,system_site_packages=False).create(base/'venv')
            exe=base/'venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
            env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
            skill=dest/'pure-math-survey';entry=skill/'scripts/survey.py'
            v=check([str(exe),'-I',str(entry),'--json','--version'],base,env)
            report['installed_policy']=assert_installed_contract(v['artifacts'])
            code="import importlib,json,pkgutil,sys;sys.path.insert(0,"+repr(str(skill/'scripts'))+");import survey_core;mods={m.name:importlib.import_module('survey_core.'+m.name).__file__ for m in pkgutil.iter_modules(survey_core.__path__)};print(json.dumps({'prefix':sys.prefix,'modules':mods}))"
            loaded=check([str(exe),'-I','-c',code],base,env)
            if not loaded['modules'] or any(not Path(f).is_relative_to(skill) for f in loaded['modules'].values()):raise AssertionError('Imported source-tree module instead of installed one')
            assets=check([str(exe),'-I',str(skill/'scripts/validate_assets.py'),'--json'],base,env)
            if set(assets['profile_preparations_executed'])!={'minimal','thematic','lecture','paper'}:raise AssertionError('Not all installed profile resources executed')
            if len(assets['profile_view_preparations_executed'])!=20:raise AssertionError('Not all installed view resources executed')
            # Reuse the real regression suite, but replace its entire runtime
            # tree with the verified archive. No import can fall back to the
            # development skill; -I also removes user/site/PYTHONPATH leakage.
            suite=base/'installed-suite'
            shutil.copytree(ROOT/'tests',suite/'tests',ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(ROOT/'tools',suite/'tools',ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(ROOT/'examples/vnext/projects',suite/'examples/vnext/projects',
                            ignore=shutil.ignore_patterns('build','history','__pycache__'))
            shutil.copytree(ROOT/'examples/rc2/projects',suite/'examples/rc2/projects',
                            ignore=shutil.ignore_patterns('build','history','__pycache__'))
            if (ROOT/'examples/r3').is_dir():
                shutil.copytree(ROOT/'examples/r3',suite/'examples/r3',ignore=shutil.ignore_patterns('build','history','__pycache__'))
            shutil.copytree(skill,suite/'skills/pure-math-survey')
            if not (suite/'tests/test_r3_policy.py').is_file():raise AssertionError('No r3 behavior regression suite is available to execute against the installation')
            executed=check([str(exe),'-I','-m','unittest','discover','-s',str(suite/'tests'),'-v'],base,env,False,timeout=args.tests_timeout)
            report['installed_regression']=installed_regression_summary(executed['stderr'])
            (base/'scope.md').write_text('# Scope\n\nRecord incidence-matrix conventions without requesting any manuscript.\n')
            project=base/'notebook'
            check([str(exe),'-I',str(entry),'--json','init','--output',str(project),'--topic','clean-install','--scope',str(base/'scope.md')],base,env)
            check([str(exe),'-I',str(entry),'--json','kb','validate',str(project)],base,env)
            f=check([str(exe),'-I',str(entry),'--json','kb','freeze',str(project)],base,env)
            check([str(exe),'-I',str(entry),'--json','kb','verify',str(project),'--snapshot',f['artifacts']['snapshot_id']],base,env)
            if list((project/'outputs').glob('*/plan.json')):raise AssertionError('Knowledge initialization generated a manuscript')
            report['clean_environment']={'venv_with_pip':False,'system_site_packages':False,'isolated_python':True,'runtime_modules_imported':len(loaded['modules']),'knowledge_only_outputs':0}
            if not args.no_build:
                example=args.example_root or ROOT/'examples/vnext/projects'
                if not example.is_dir():raise FileNotFoundError('Supply --example-root with the vNext source projects, or explicitly use --no-build.')
                reproduced=check([str(exe),'-I',str(ROOT/'tools/verify_vnext_examples.py'),
                    '--skill-root',str(skill),'--examples',str(example),'--output',str(base/'relocated-examples')],base,env,timeout=args.build_timeout)
                if reproduced['status']!='PASS':raise AssertionError(reproduced)
                report['installed_profile_builds']=reproduced['outputs']
                current=check([str(exe),'-I',str(ROOT/'tools/verify_rc2_examples.py'),
                    '--repository',str(ROOT),'--skill-root',str(skill),
                    '--output',str(base/'relocated-rc2')],base,env,timeout=args.build_timeout)
                if current['status']!='PASS':raise AssertionError(current)
                report['installed_rc2_builds']=current['outputs']
                report['installed_tex_build']='Eleven historical PDFs BUILT and rendered using the isolated installed runtime: seven rc1 and four rc2; these are not r3 manuscripts and new PDFs are NOT VISUALLY REVIEWED'
            else:report['installed_tex_build']='NOT_EXECUTED (--no-build)'
            if args.r3_manifest:
                report['r3_outputs']=verify_r3_outputs(load_r3_manifest(args.r3_manifest.resolve()),base,check,exe,entry,env,args.build_timeout,not args.no_build,report)
            else:report['r3_outputs']={'status':'NOT_EXECUTED','reason':'No --r3-manifest supplied; historical builds cannot stand in for actual r3 manuscripts'}
            report['status'],incomplete=verification_completion(bool(args.r3_manifest),args.no_build)
            if incomplete:
                report['incomplete']=incomplete
                report['workspace']['retained']=True
    except (AssertionError,ValueError,OSError,RuntimeError,subprocess.SubprocessError,zipfile.BadZipFile) as e:report.update(status='FAIL',failure=str(e))
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if report['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
