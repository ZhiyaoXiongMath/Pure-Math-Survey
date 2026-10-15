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


EXPECTED_POLICY = 'four-modes-2026-10-15-r5'
EXPECTED_CONTRACTS = {('2.2.0', EXPECTED_POLICY)}
REQUIRED_SUITES = ('test_current_policy', 'test_r4_policy', 'test_pr04_editorial',
                   'test_workflow_bindings', 'test_dispatch', 'test_source_eligibility')


def assert_installed_contract(artifacts:dict)->dict:
    """Current contract identity is separate from test success."""
    if (artifacts.get('version'), artifacts.get('schema_version'),
            artifacts.get('output_schema_version'), artifacts.get('editorial_policy')) != (
            '2.1.0', '2.0.0', '2.2.0', EXPECTED_POLICY):
        raise AssertionError('Installed runtime is not software 2.1.0 / KB 2.0.0 / output 2.2.0 / r5')
    contracts=artifacts.get('supported_output_contracts')
    if not isinstance(contracts,list) or len(contracts)!=1 or any(
            not isinstance(x,dict) or not isinstance(x.get('schema_version'),str) or
            not isinstance(x.get('editorial_policy'),str) for x in contracts):
        raise AssertionError('Installed runtime did not report the single current schema-policy contract')
    pairs={(x['schema_version'],x['editorial_policy']) for x in contracts}
    if pairs != EXPECTED_CONTRACTS:
        raise AssertionError('Installed schema-policy contract is missing or unsupported')
    return {'editorial_policy':EXPECTED_POLICY,'supported_contracts':artifacts['supported_output_contracts']}


# Declarations correspond to actual @skipUnless guards in the test suite.
# These are test identities, never substrings or skip-reason whitelists.
PLATFORM_ONLY_TESTS = {
    'test_history_longpath.HistoryPaths.test_real_junction_outside_project_is_rejected': 'nt',
    'test_history_longpath.HistoryPaths.test_extended_prefix_is_idempotent_and_unc_is_preserved': 'nt',
    'test_release_verifier.R4VerifierContracts.test_exited_parent_inherited_pipe_is_bounded_and_external_process_survives': 'nt',
}
CAPABILITY_REQUIRED_TESTS = frozenset({
    'test_v2.Contracts.test_H21_actual_symlink_rejected_when_available',
    'test_workflow_bindings.WorkflowBindings.test_native_identity_still_rejects_symlink_escape',
    'test_output_review.OutputReview.test_U22_real_build_then_failed_attempt_preserves_prior_build',
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
        raise AssertionError('Required installed policy, workflow and dispatch suites must execute')

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
        'synthetic_gates_are_not_mathematical_acceptance':True,
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


def current_render_inputs(out:Path,result:dict)->tuple[set[str],dict[str,set[str]]]:
    """Check current artifact bytes before deferring any older visual reading."""
    import hashlib
    from survey_core.common import safe,SurveyError
    built=json.loads((out/'build/build-report.json').read_text(encoding='utf-8'))
    render=json.loads((out/'evidence/render-manifest.json').read_text(encoding='utf-8'))
    if not isinstance(built,dict) or not isinstance(render,dict):
        raise AssertionError('Current build/render manifest must be an object')
    pdf=out/'build/main.pdf';pages=built.get('pages')
    if (built.get('status')!='BUILT' or type(pages) is not int or pages<=0
            or result.get('artifacts',{}).get('pages')!=pages or not pdf.is_file()
            or hashlib.sha256(pdf.read_bytes()).hexdigest()!=built.get('pdf_sha256')
            or render.get('pdf_sha256')!=built.get('pdf_sha256')):
        raise AssertionError('Current PDF/build/render identities are invalid')
    rows=render.get('pages')
    if (not isinstance(rows,list) or any(not isinstance(row,dict) or type(row.get('page')) is not int for row in rows)
            or [row.get('page') for row in rows]!=list(range(1,pages+1))):
        raise AssertionError('Current render manifest does not cover the entire PDF')
    required={'build/main.pdf','build/build-report.json','evidence/render-manifest.json'}
    for row in rows:
        path=row.get('path');digest=row.get('sha256')
        filename=re.fullmatch(r'evidence/pages/page-([0-9]+)\.png',path) if isinstance(path,str) else None
        if (not filename or int(filename[1])!=row['page']
                or not isinstance(digest,str) or not re.fullmatch('[a-f0-9]{64}',digest)):
            raise AssertionError('Current render manifest has an invalid page binding')
        try:file=safe(out,path,True)
        except SurveyError as exc:raise AssertionError('Current rendered page is missing or unsafe: '+path) from exc
        if hashlib.sha256(file.read_bytes()).hexdigest()!=digest:
            raise AssertionError('Current rendered image bytes have changed: '+path)
        required.add(path)
    visual_records={}
    for file in (out/'evidence').rglob('*.json'):
        record=json.loads(file.read_text(encoding='utf-8'))
        if (isinstance(record,dict) and record.get('kind')=='visual'
                and isinstance(record.get('scope'),dict)
                and result['artifacts'].get('output_id') in record['scope'].get('output_ids',[])):
            key=record.get('review_id')
            if not isinstance(key,str) or key in visual_records:
                raise AssertionError('Ambiguous visual review identity')
            bindings=record.get('inputs')
            if (not isinstance(bindings,list) or any(not isinstance(binding,dict)
                    or not isinstance(binding.get('path'),str) for binding in bindings)):
                raise AssertionError('Invalid visual review input bindings')
            visual_records[key]={binding['path'] for binding in bindings}
    return required,visual_records


def require_current_semantics(result:dict,out:Path|None=None)->dict:
    """Separate source/semantic acceptance from new-PDF visual work still to do."""
    artifacts=result.get('artifacts',{})
    if (artifacts.get('editorial_policy')!=EXPECTED_POLICY or artifacts.get('readiness')!='READY'
            or not artifacts.get('used_output_review_ids')):
        raise AssertionError('Actual current-policy input lacks a current bound semantic review/readiness result')
    visual_paths={'build/main.pdf','build/build-report.json','evidence/render-manifest.json'}
    visual_records={}
    if out is not None:visual_paths,visual_records=current_render_inputs(out,result)
    blocking=[];visual=[]
    for error in result.get('errors',[]):
        path=error.get('path','')
        message=error.get('message','')
        stale=re.fullmatch(r'Review (.+) no longer matches this input',message)
        stale_visual_record=(error.get('code')=='REVIEW_STALE' and stale
                and (path in visual_paths or (out is None and path.startswith('evidence/pages/')))
                and (out is None or stale[1] in visual_records))
        omitted=re.fullmatch(r'Review (.+) omits necessary inputs: (.+)',message)
        missing=set(omitted[2].split(', ')) if omitted else set()
        old_visual_scope=(out is not None and error.get('code')=='REVIEW_SCOPE_INSUFFICIENT'
                and omitted and omitted[1] in visual_records and missing
                and missing==visual_paths-visual_records[omitted[1]])
        # A missing/invalid fresh manifest is a damaged build artifact, not an
        # old visual-reading scope. current_render_inputs checks it explicitly.
        pending_reading=(error.get('code')=='VISUAL_REVIEW_INCOMPLETE'
                and path=='evidence')
        if pending_reading or stale_visual_record or old_visual_scope:
            visual.append(error)
        else:blocking.append(error)
    if blocking:raise AssertionError({'nonvisual_release_errors':blocking})
    return {'status':'CURRENT_BOUND_RECORDS_CHECKED','review_ids':artifacts['used_output_review_ids'],
            'new_pdf_visual_findings_pending':visual,
            'visual_review_status':'NEW_VISUAL_REVIEW_REQUIRED' if visual else 'CURRENT_VISUAL_RECORDS_CHECKED',
            'formal_release_authorized':False,
            'meaning':'Mechanical evidence/binding check; no new mathematical or page reading'}


def load_output_manifest(path:Path)->list[dict]:
    """Private verifier input only; does not add a mathematical project schema."""
    data=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict) or set(data)!={'projects'} or not isinstance(data['projects'],list) or not data['projects']:
        raise ValueError('output manifest needs a nonempty projects list')
    entries=[];seen=set()
    for item in data['projects']:
        if not isinstance(item,dict) or set(item)!={'path','outputs'} or not isinstance(item['path'],str):
            raise ValueError('Each output manifest project needs only path and outputs')
        source=(path.parent/item['path']).resolve()
        outputs=item['outputs']
        if not source.is_dir() or not (source/'project.json').is_file():raise ValueError('output source project does not exist: '+str(source))
        if not isinstance(outputs,list) or not outputs or any(not isinstance(x,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',x) for x in outputs):
            raise ValueError('output IDs must be nonempty safe identifiers')
        if len(outputs)!=len(set(outputs)) or source in seen:raise ValueError('Duplicate output project or output')
        seen.add(source);entries.append({'path':source,'outputs':outputs})
    return entries


def verify_outputs(entries:list[dict],base:Path,check,exe:Path,entry:Path,env:dict,build_timeout:int,build:bool,report:dict|None=None)->dict:
    """Rebuild only explicit explicit current-policy inputs, never manufacture review acceptance."""
    import hashlib
    result={'status':'RUNNING','outputs':[],
            'original_paper_quality':'NOT VERIFIED; an internal draft is not original research acceptance'}
    if report is not None:report['outputs']=result
    rows=result['outputs'];coverage=[];spines={}
    for index,item in enumerate(entries):
        source=item['path'];project=base/'verified-projects'/str(index)
        shutil.copytree(source,project,ignore=shutil.ignore_patterns('build','history','__pycache__'))
        for oid in item['outputs']:
            out=project/'outputs'/oid;plan=json.loads((out/'plan.json').read_text(encoding='utf-8'))
            if plan.get('output_id')!=oid or (plan.get('schema_version'),plan.get('editorial_policy'))!=('2.2.0',EXPECTED_POLICY):
                raise AssertionError('Requested real output does not carry r5 policy: '+oid)
            profile,view=plan.get('profile'),plan.get('view')
            if profile not in {'minimal','thematic','lecture','paper'}:raise AssertionError('Unknown real output profile')
            if profile=='paper' and plan.get('draft') is not True:raise AssertionError('The current Paper verification input must remain an internal draft: '+oid)
            if profile!='paper' and plan.get('draft'):raise AssertionError('Non-Paper current acceptance input must be an authored nondraft output: '+oid)
            source_hashes={name:hashlib.sha256((source/'outputs'/oid/name).read_bytes()).hexdigest()
                           for name in ('plan.json','outline.md','manuscript/main.tex')}
            call=lambda *args,**kwargs:check([str(exe),'-I',str(entry),'--json',*map(str,args)],base,env,**kwargs)
            call('kb','verify',project,'--snapshot',plan['snapshot_id'])
            call('output','validate',project,'--output',oid,'--stage','structure')
            if view!='integrated':raise AssertionError('The fixed five-output suite uses integrated view')
            coverage.append(profile)
            principals=sorted(x['node_id'] for x in plan['selections'] if x['role']=='principal_answer')
            canonical=tuple((key,hashlib.sha256((out/'generated/statements'/f'{key}.tex').read_bytes()).hexdigest()) for key in principals)
            spines.setdefault(index,[]).append((profile,plan['snapshot_id'],tuple(sorted(plan['question_ids'])),canonical))
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
                if profile!='paper':
                    release=call('output','validate',project,'--output',oid,'--stage','release',allowed_returncodes=(0,3))
                    row['semantic_validation']=require_current_semantics(release,out)
            else:row['build']='NOT EXECUTED (--no-build)'
            if profile=='paper':
                release=call('output','validate',project,'--output',oid,'--stage','release',allowed_returncodes=(3,))
                blocked=base/'forbidden-paper'/f'{index}-{oid}.zip'
                packaged=call('output','package',project,'--output',oid,'--to',blocked,allowed_returncodes=(3,))
                if any('DRAFT_NOT_RELEASABLE' not in {e.get('code') for e in r.get('errors',[])} for r in (release,packaged)) or blocked.exists():
                    raise AssertionError('Paper draft did not preserve its formal release/package barrier')
                row['formal_release']='BLOCKED: DRAFT_NOT_RELEASABLE'
                row['formal_package']='BLOCKED: no archive created'
    if len(entries)!=3 or sorted(coverage)!=['lecture','minimal','minimal','paper','thematic']:
        raise AssertionError('The fixed suite needs three projects and five outputs: two Minimal, Thematic, Lecture, draft Paper')
    comparison=[values for values in spines.values() if len(values)==3]
    if len(comparison)!=1 or {v[0] for v in comparison[0]}!={'minimal','thematic','lecture'}:
        raise AssertionError('One comparison project must supply all three requested modes')
    if len({v[1] for v in comparison[0]})!=1 or len({v[2] for v in comparison[0]})!=1:
        raise AssertionError('Comparison modes must consume the same snapshot and questions')
    if len({v[3] for v in comparison[0]})!=1:
        raise AssertionError('Comparison modes must preserve the same canonical principal spine')
    result['shared_comparison_snapshot']='IDENTICAL: mode quality requires independent reading'
    result['status']='BUILT_NOT_VISUALLY_REVIEWED' if build else 'NOT_EXECUTED'
    return result


def resolve_output_manifest(explicit:Path|None,repository:Path)->Path|None:
    if explicit is not None:return explicit
    default=repository/'examples/r4/verification-manifest.json'
    return default if default.is_file() else None


def verification_completion(has_inputs:bool,no_build:bool)->tuple[str,list[str]]:
    incomplete=[]
    if no_build:incomplete.append('Actual TeX builds were explicitly omitted')
    if not has_inputs:incomplete.append('Real five-output manuscript inputs were not supplied')
    return ('INCOMPLETE' if incomplete else 'PASS'),incomplete


def record_failure_artifacts(destination:Path,report:dict)->None:
    """Preserve real build failure location without replacing prior successful rows."""
    import hashlib
    artifacts=[]
    for path in sorted(destination.rglob('build-report.json')) if destination.exists() else []:
        if path.parent.name!='build':continue
        try:
            data=json.loads(path.read_text(encoding='utf-8'))
            log=path.parent/'main.log'
            artifacts.append({'report':str(path),'status':data.get('status'),
                'blocking_log_issues':data.get('blocking_log_issues',{}),'failure':data.get('failure'),
                'log':str(log) if log.is_file() else None,
                'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest() if log.is_file() else None})
        except (OSError,ValueError) as exc:artifacts.append({'report':str(path),'read_error':str(exc)})
    report['output_directory']=str(destination)
    report['failure_artifacts']=artifacts
    for row in report.get('outputs',[]):
        if row.get('build')=='RUNNING':row['build']='FAILED'


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=Path)
    ap.add_argument('--report',type=Path);ap.add_argument('--no-build',action='store_true',help='Explicitly skip external TeX; reported as NOT_EXECUTED.')
    ap.add_argument('--work-directory',type=Path,help='Parent of a short-lived staging directory; use a shallow path for deeply nested historical Windows artifacts.')
    ap.add_argument('--manifest',type=Path,help='Explicit three-project/five-output current-policy input list; missing input leaves full verification INCOMPLETE.')
    ap.add_argument('--engineering-only',action='store_true',help='Run isolated software checks and neutral TeX smoke only; does not claim five-case acceptance.')
    ap.add_argument('--tests-timeout',type=int,default=1200,help='Seconds allowed for the full installed regression suite (default 1200).')
    ap.add_argument('--build-timeout',type=int,default=1200,help='Seconds allowed per output build/render call (default 1200).')
    ap.add_argument('--keep-work-directory',action='store_true',help='Also retain successful installation/build artifacts. Failed verification artifacts are always retained.')
    args=ap.parse_args()
    if args.tests_timeout<=0 or args.build_timeout<=0:ap.error('Timeouts must be positive seconds')
    if args.engineering_only and args.manifest:ap.error('Choose engineering-only or the full five-output manifest')
    if not args.engineering_only:args.manifest=resolve_output_manifest(args.manifest,ROOT)
    report={'status':'RUNNING','checks':[],'archive':args.archive.name,'python':sys.version,
            'manifest':str(args.manifest.resolve()) if args.manifest else None,
            'timeouts':{'installed_tests':args.tests_timeout,'build_or_render':args.build_timeout},
            'scope':'Installation and build verification, not mathematical/exposition/page acceptance'}
    initial_status,initial_incomplete=verification_completion(bool(args.manifest),args.no_build)
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
            shutil.copytree(skill,suite/'skills/pure-math-survey')
            if any(not (suite/'tests'/f'{name}.py').is_file() for name in REQUIRED_SUITES):
                raise AssertionError('A required current behavior regression suite is unavailable for installed execution')
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
                smoke=check([str(exe),'-I',str(skill/'scripts/build_checks.py'),
                             '--output',str(base/'tex-smoke')],base,env,timeout=args.build_timeout)
                if smoke['status']!='PASS':raise AssertionError(smoke)
                report['installed_tex_smoke']=smoke
            else:report['installed_tex_smoke']='NOT_EXECUTED (--no-build)'
            if args.manifest:
                report['outputs']=verify_outputs(load_output_manifest(args.manifest.resolve()),base,check,exe,entry,env,args.build_timeout,not args.no_build,report)
            else:report['outputs']={'status':'NOT_EXECUTED','reason':'No fixed five-output manifest; engineering smoke is not mathematical acceptance'}
            report['status'],incomplete=verification_completion(bool(args.manifest),args.no_build)
            if args.engineering_only and not args.no_build and not args.manifest:
                report['status']='PASS'
                report['scope']='Engineering installation/regression/neutral TeX smoke only; five-output E2E NOT_EXECUTED'
                incomplete=[]
                report.pop('incomplete',None)
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
