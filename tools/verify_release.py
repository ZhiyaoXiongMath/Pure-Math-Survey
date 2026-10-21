#!/usr/bin/env python3
"""Verify install ZIP, then execute it in a fresh no-pip virtual environment.

Checks only the candidate installation and neutral Minimal build; source projects are not used.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
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


EXPECTED_POLICY = 'minimal-rules-v22-lean-2.4.1'
EXPECTED_RUNTIME = 'minimal-lean-2.4.1'
EXPECTED_CONTRACTS = {('3.0.0', EXPECTED_POLICY)}
REQUIRED_SUITES = ('test_knowledge_units', 'test_minimal_runtime', 'test_v2', 'test_materials',
                   'test_build_layout', 'test_history_longpath', 'test_tex_safety',
                   'test_release_verifier')


def assert_installed_contract(artifacts:dict)->dict:
    """Current contract identity is separate from test success."""
    if (artifacts.get('version'), artifacts.get('schema_version'),
            artifacts.get('output_schema_version'), artifacts.get('editorial_policy'),
            artifacts.get('runtime_contract')) != (
            '2.4.1-dev.4', '3.0.0', '3.0.0', EXPECTED_POLICY, EXPECTED_RUNTIME):
        raise AssertionError('Installed runtime does not match the PR04 candidate version, schemas, policy and runtime contract')
    contracts=artifacts.get('supported_output_contracts')
    if not isinstance(contracts,list) or len(contracts)!=1 or any(
            not isinstance(x,dict) or not isinstance(x.get('schema_version'),str) or
            not isinstance(x.get('editorial_policy'),str) for x in contracts):
        raise AssertionError('Installed runtime did not report the single current schema-policy contract')
    pairs={(x['schema_version'],x['editorial_policy']) for x in contracts}
    if pairs != EXPECTED_CONTRACTS:
        raise AssertionError('Installed schema-policy contract is missing or unsupported')
    return {'editorial_policy':EXPECTED_POLICY,'runtime_contract':EXPECTED_RUNTIME,
            'supported_contracts':artifacts['supported_output_contracts']}


# Declarations correspond to actual @skipUnless guards in the test suite.
# These are test identities, never substrings or skip-reason whitelists.
PLATFORM_ONLY_TESTS = {
    'test_history_longpath.HistoryPaths.test_real_junction_outside_project_is_rejected': 'nt',
    'test_history_longpath.HistoryPaths.test_extended_prefix_is_idempotent_and_unc_is_preserved': 'nt',
    'test_release_verifier.MinimalVerifierContracts.test_exited_parent_inherited_pipe_is_bounded_and_external_process_survives': 'nt',
}
CAPABILITY_REQUIRED_TESTS = frozenset({
    'test_v2.Contracts.test_H21_actual_symlink_rejected_when_available',
    'test_minimal_runtime.MinimalRuntime.test_actual_kb_prepare_build_package_without_review_records',
})
UNITTEST_RESULT = re.compile(
    # Python 3.10: (module.Class); Python 3.12: (module.Class.test_method).
    r'^(test\w+) \((test_\w+\.\w+)(?:\.(test\w+))?\) \.\.\. (ok|skipped .+|FAIL|ERROR)$'
)


def installed_regression_summary(stderr:str)->dict:
    """Only another OS's declared tests are N/A; every other skip is unresolved.

    Parse real verbose unittest identities, not arbitrary skip messages. Check
    the reported total and skip count so missing/partial logs cannot look green.
    """
    outcomes = {}
    for line in stderr.splitlines():
        match = UNITTEST_RESULT.fullmatch(line)
        if not match:
            continue
        display_name, case_path, repeated_method, status = match.groups()
        identity = case_path+'.'+display_name
        if (repeated_method is not None and repeated_method != display_name) or identity in outcomes:
            raise AssertionError('Malformed or duplicate installed unittest identity: '+identity)
        outcomes[identity] = (status.split(' ',1)[0],line)

    counts = re.findall(r'(?m)^Ran (\d+) tests? in [^\r\n]+$',stderr)
    summaries = re.findall(r'(?m)^OK(?: \(skipped=(\d+)\))?$',stderr)
    if len(counts)!=1 or len(summaries)!=1 or not outcomes:
        raise AssertionError('Installed unittest completion summary is absent or ambiguous')
    total = int(counts[0])
    skipped = sum(status=='skipped' for status,_ in outcomes.values())
    if total!=len(outcomes) or skipped!=int(summaries[0] or 0):
        raise AssertionError('Installed unittest counts do not match the actual verbose test outcomes')
    if any(status not in {'ok','skipped'} for status,_ in outcomes.values()):
        raise AssertionError('Installed regressions contain an actual test failure')

    suites = {name:[value for identity,value in outcomes.items()
                    if identity.startswith(name+'.')] for name in REQUIRED_SUITES}
    if any(not rows or not any(status=='ok' for status,_ in rows)
           for rows in suites.values()):
        raise AssertionError('Required installed minimal and safety suites must execute')

    not_applicable=[];unverified_capability=[];unexpected=[]
    for identity,required_os in PLATFORM_ONLY_TESTS.items():
        if identity not in outcomes:
            raise AssertionError('Declared platform regression missing: '+identity)
        status,line = outcomes[identity]
        if os.name!=required_os:
            if status!='skipped':
                raise AssertionError('Another-platform-only test was not skipped: '+identity)
            not_applicable.append(line)
        elif status=='skipped':
            unverified_capability.append(line)
    for identity in CAPABILITY_REQUIRED_TESTS:
        if identity not in outcomes:
            raise AssertionError('Required capability regression missing: '+identity)
        status,line=outcomes[identity]
        if status=='skipped':
            unverified_capability.append(line)
    declared=set(PLATFORM_ONLY_TESTS)|CAPABILITY_REQUIRED_TESTS
    for identity,(status,line) in outcomes.items():
        if status=='skipped' and identity not in declared:
            unexpected.append(line)
    unverified=unverified_capability+unexpected
    return {
        'tests':total,'executed':total-skipped,
        'required_suites':{name:len(rows) for name,rows in suites.items()},
        'platform':'windows' if os.name=='nt' else sys.platform,
        'status':'INCOMPLETE' if unverified else 'PASS',
        'not_applicable_tests':not_applicable,
        'unverified_capability_tests':unverified_capability,
        'unexpected_skip_tests':unexpected,
        'unverified_tests':unverified,
        'software_checks_are_not_mathematical_certification':True,
    }


def windows_job_process(command:list[str],**kwargs)->subprocess.Popen:
    """Assign a waiting wrapper before it can create any actual command child."""
    import ctypes
    from ctypes import wintypes as w
    class Basic(ctypes.Structure):
        _fields_=[('process_time',ctypes.c_int64),('job_time',ctypes.c_int64),
                  ('flags',w.DWORD),('minimum',ctypes.c_size_t),('maximum',ctypes.c_size_t),
                  ('active',w.DWORD),('affinity',ctypes.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
    class Extended(ctypes.Structure):
        _fields_=[('basic',Basic),('io',ctypes.c_uint64*6),('process_memory',ctypes.c_size_t),
                  ('job_memory',ctypes.c_size_t),('peak_process',ctypes.c_size_t),('peak_job',ctypes.c_size_t)]
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.CreateJobObjectW.argtypes=[ctypes.c_void_p,w.LPCWSTR];kernel.CreateJobObjectW.restype=w.HANDLE
    kernel.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD]
    kernel.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE]
    kernel.TerminateJobObject.argtypes=[w.HANDLE,w.UINT]
    kernel.CloseHandle.argtypes=[w.HANDLE]
    job=kernel.CreateJobObjectW(None,None)
    if not job:raise ctypes.WinError(ctypes.get_last_error())
    proc=None
    try:
        limits=Extended();limits.basic.flags=0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel.SetInformationJobObject(job,9,ctypes.byref(limits),ctypes.sizeof(limits)):
            raise ctypes.WinError(ctypes.get_last_error())
        # No target code executes until the parent assigns this wrapper to its
        # private job and communicate supplies GO. Descendants inherit the job.
        wrapper="import subprocess,sys; token=sys.stdin.readline(); sys.exit(subprocess.call(sys.argv[1:]) if token=='GO\\n' else 125)"
        proc=subprocess.Popen([sys.executable,'-I','-c',wrapper,*command],stdin=subprocess.PIPE,**kwargs)
        if not kernel.AssignProcessToJobObject(job,w.HANDLE(int(proc._handle))):
            raise ctypes.WinError(ctypes.get_last_error())
        proc._verification_job=(kernel,job)
        return proc
    except BaseException:
        if proc is not None:
            proc.kill();proc.communicate(timeout=15)
        kernel.CloseHandle(job)
        raise


def terminate_process_tree(proc:subprocess.Popen)->dict:
    """Terminate this check's own children as well as the Python/TeX parent."""
    if os.name=='nt':
        import ctypes
        kernel,job=proc._verification_job
        if not kernel.TerminateJobObject(job,1):raise ctypes.WinError(ctypes.get_last_error())
        return {'method':'TerminateJobObject','returncode':0,'scope':'private wrapper and all command descendants'}
    try:
        os.killpg(proc.pid,signal.SIGKILL)
        return {'method':'killpg SIGKILL','returncode':0}
    except ProcessLookupError:
        return {'method':'killpg SIGKILL','returncode':0,'already_exited':True}


def run_check(command:list[str],cwd:Path,env:dict,report:dict,decode:bool=True,timeout:int=180,allowed_returncodes:tuple[int,...]=(0,))->dict:
    if timeout<=0:raise ValueError('Check timeout must be positive')
    start=time.monotonic()
    options=dict(cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                 text=True,encoding='utf-8',errors='replace',start_new_session=os.name!='nt')
    proc=windows_job_process(command,**options) if os.name=='nt' else subprocess.Popen(command,**options)
    try:
        stdout,stderr=proc.communicate(input='GO\n' if os.name=='nt' else None,timeout=timeout)
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
            # Closing a pipe held by a surviving child can block on the reader
            # thread lock. Preserve the failed cleanup instead of hiding it.
        report['checks'].append({'command':command,'cwd':str(cwd),'returncode':None,
                                'timeout_seconds':timeout,'elapsed_seconds':time.monotonic()-start,
                                'stdout':stdout,'stderr':stderr,'termination':termination,'expected_returncodes':list(allowed_returncodes)})
        raise subprocess.TimeoutExpired(command,timeout,output=stdout,stderr=stderr) from exc
    finally:
        if os.name=='nt':
            kernel,job=proc._verification_job
            kernel.CloseHandle(job)
    row={'command':command,'cwd':str(cwd),'returncode':proc.returncode,
         'timeout_seconds':timeout,'elapsed_seconds':time.monotonic()-start,
         'stdout':stdout,'stderr':stderr,'expected_returncodes':list(allowed_returncodes)}
    report['checks'].append(row)
    if proc.returncode not in allowed_returncodes:raise RuntimeError(stdout+stderr)
    return json.loads(stdout) if decode else row


def verification_completion(no_build: bool) -> tuple[str, list[str]]:
    incomplete = ['Neutral Minimal TeX smoke was explicitly omitted'] if no_build else []
    return ('INCOMPLETE' if incomplete else 'PASS'), incomplete


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=Path)
    ap.add_argument('--report',type=Path);ap.add_argument('--no-build',action='store_true',help='Skip the neutral TeX smoke; regression capability checks still run and verification is INCOMPLETE.')
    ap.add_argument('--work-directory',type=Path,help='Parent of a short-lived staging directory; use a shallow path for deeply nested historical Windows artifacts.')
    ap.add_argument('--manifest',type=Path,help=argparse.SUPPRESS)
    ap.add_argument('--engineering-only',action='store_true',help='Compatibility alias; candidate verification always performs engineering checks only.')
    ap.add_argument('--tests-timeout',type=int,default=1200,help='Seconds allowed for the full installed regression suite (default 1200).')
    ap.add_argument('--build-timeout',type=int,default=1200,help='Seconds allowed per output build/render call (default 1200).')
    ap.add_argument('--keep-work-directory',action='store_true',help='Also retain successful installation/build artifacts. Failed verification artifacts are always retained.')
    args=ap.parse_args()
    if args.tests_timeout<=0 or args.build_timeout<=0:ap.error('Timeouts must be positive seconds')
    if args.manifest:ap.error('Historical output manifests are unsupported; this verifier uses a neutral Minimal smoke.')
    report={'status':'RUNNING','checks':[],'archive':args.archive.name,'python':sys.version,
            'timeouts':{'installed_tests':args.tests_timeout,'build_or_render':args.build_timeout},
            'scope':'Candidate installation, regression and neutral Minimal build checks; no mathematical or page certification'}
    _,initial_incomplete=verification_completion(args.no_build)
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
            if assets['profile_preparations_executed']!=['minimal']:raise AssertionError('Installed preparation did not exercise only Minimal')
            if assets['profile_view_preparations_executed']!=['minimal-integrated']:raise AssertionError('Installed preparation did not exercise the fixed integrated view')
            report['installed_assets']=assets
            # Reuse the real regression suite, but replace its entire runtime
            # tree with the verified archive. No import can fall back to the
            # development skill; -I also removes user/site/PYTHONPATH leakage.
            suite=base/'installed-suite'
            shutil.copytree(ROOT/'tests',suite/'tests',ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(ROOT/'tools',suite/'tools',ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(skill,suite/'skills/pure-math-survey')
            if any(not (suite/'tests'/f'{name}.py').is_file() for name in REQUIRED_SUITES):
                raise AssertionError('A required current behavior regression suite is unavailable for installed execution')
            executed=check([str(exe),'-I','-m','unittest','discover','-s',str(suite/'tests'),'-v'],base,env,False,timeout=args.tests_timeout)
            report['installed_regression']=installed_regression_summary(executed['stderr'])
            (base/'scope.md').write_text('# Scope\n\nRecord incidence-matrix conventions without requesting any manuscript.\n')
            project=base/'notebook'
            check([str(exe),'-I',str(entry),'--json','init','--output',str(project),'--topic','clean-install','--scope',str(base/'scope.md')],base,env)
            check([str(exe),'-I',str(entry),'--json','kb','validate',str(project)],base,env)
            check([str(exe),'-I',str(entry),'--json','kb','index',str(project)],base,env)
            if (project/'snapshots').exists():raise AssertionError('Knowledge-only smoke created a forced snapshot')
            if list((project/'outputs').glob('*/plan.json')):raise AssertionError('Knowledge initialization generated a manuscript')
            report['clean_environment']={'venv_with_pip':False,'system_site_packages':False,'isolated_python':True,'runtime_modules_imported':len(loaded['modules']),'knowledge_only_outputs':0}
            if not args.no_build:
                smoke=check([str(exe),'-I',str(skill/'scripts/build_checks.py'),
                             '--output',str(base/'tex-smoke')],base,env,timeout=args.build_timeout)
                if smoke['status']!='PASS':raise AssertionError(smoke)
                report['installed_tex_smoke']=smoke
            else:report['installed_tex_smoke']='NOT_EXECUTED (--no-build)'
            report['status'],incomplete=verification_completion(args.no_build)
            if report['installed_regression']['unverified_tests']:
                report['status']='INCOMPLETE'
                incomplete.append('Installed platform-applicable tests skipped; capability or unexpected skips must be resolved on this host')
            if incomplete:
                report['incomplete']=incomplete
                report['workspace']['retained']=True
    except (AssertionError,ValueError,OSError,RuntimeError,subprocess.SubprocessError,zipfile.BadZipFile) as e:report.update(status='FAIL',failure=str(e))
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if report['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
