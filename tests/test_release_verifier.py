"""Retain real child failure evidence without granting build acceptance."""
from pathlib import Path
import importlib.util
import copy
import json
import hashlib
import base64
import time
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release_verifier',ROOT/'tools/verify_release.py')
verifier=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class ReleaseVerifierEvidence(unittest.TestCase):
    def test_failed_child_retains_actual_inputs_and_output(self):
        with tempfile.TemporaryDirectory() as td:
            report={'checks':[]}
            with self.assertRaises(RuntimeError):
                with verifier.verification_workspace(report,Path(td)) as base:
                    (base/'input.tex').write_text('exact failed input',encoding='utf-8')
                    verifier.run_check([sys.executable,'-I','-c',
                        "print('actual build failure');raise SystemExit(7)"],base,os.environ.copy(),report,False)
            self.assertTrue(report['workspace']['retained'])
            self.assertEqual((base/'input.tex').read_text(),'exact failed input')
            self.assertEqual(report['checks'][0]['returncode'],7)
            self.assertIn('actual build failure',report['checks'][0]['stdout'])

    def test_success_cleanup_and_explicit_artifact_retention(self):
        with tempfile.TemporaryDirectory() as td:
            for keep in (False,True):
                report={'checks':[]}
                with verifier.verification_workspace(report,Path(td),keep) as base:
                    result=verifier.run_check([sys.executable,'-I','-c',
                        'print("{\\"status\\":\\"BUILT\\"}")'],base,os.environ.copy(),report)
                    self.assertEqual(result['status'],'BUILT')
                self.assertEqual(base.exists(),keep)

    def test_timeout_retains_partial_child_diagnostics(self):
        with tempfile.TemporaryDirectory() as td:
            report={'checks':[]}
            with self.assertRaises(subprocess.TimeoutExpired):
                with verifier.verification_workspace(report,Path(td)) as base:
                    verifier.run_check([sys.executable,'-I','-u','-c',
                        "import time;print('TeX still running',flush=True);time.sleep(30)"],
                        base,os.environ.copy(),report,False,timeout=3)
            self.assertTrue(base.exists())
            row=report['checks'][0]
            self.assertIsNone(row['returncode'])
            self.assertIn('TeX still running',row['stdout'])
            self.assertEqual(row['timeout_seconds'],3)


class R4VerifierContracts(unittest.TestCase):
    """Synthetic verifier orchestration only; no accepted mathematics is created."""
    def valid_version(self):
        return {'version':'2.1.0','schema_version':'2.0.0','output_schema_version':'2.2.0',
                'editorial_policy':verifier.EXPECTED_POLICY,
                'supported_output_contracts':[{'schema_version':s,'editorial_policy':p}
                                              for s,p in sorted(verifier.EXPECTED_CONTRACTS)]}

    def test_obsolete_extra_or_missing_contracts_cannot_pass_as_current(self):
        actual=self.valid_version()
        verifier.assert_installed_contract(actual)
        for key,value in (('editorial_policy','four-modes-2026-10-12-rc2'),
                          ('version','2.2.0'),('schema_version','2.1.0'),
                          ('supported_output_contracts',[]),
                          ('supported_output_contracts',actual['supported_output_contracts']+[
                              {'schema_version':'2.0.0','editorial_policy':'legacy-2.0.0'}]),
                          ('supported_output_contracts',[
                              {'schema_version':'2.2.0','editorial_policy':'four-modes-2026-10-12-r3'}])):
            wrong=copy.deepcopy(actual);wrong[key]=value
            with self.subTest(key=key),self.assertRaises(AssertionError):verifier.assert_installed_contract(wrong)

    @staticmethod
    def installed_lines(platform='posix'):
        """Synthetic verbose log with all mandatory regressions, never a real run."""
        lines=[f'test_case ({name}.Current.test_case) ... ok'
               for name in verifier.REQUIRED_SUITES]
        for identity,required_os in sorted(verifier.PLATFORM_ONLY_TESTS.items()):
            outcome='ok' if platform==required_os else "skipped 'another-platform only'"
            lines.append(f'{identity.rsplit(".",1)[-1]} ({identity}) ... {outcome}')
        for identity in sorted(verifier.CAPABILITY_REQUIRED_TESTS):
            lines.append(f'{identity.rsplit(".",1)[-1]} ({identity}) ... ok')
        return lines

    @staticmethod
    def installed_log(lines):
        skips=sum(' ... skipped ' in line for line in lines)
        return ('\n'.join(lines)+f'\nRan {len(lines)} tests in 2s\n'
                +(f'OK (skipped={skips})' if skips else 'OK'))

    def test_current_suites_must_really_execute_without_skips_or_failures(self):
        with self.assertRaises(AssertionError):
            verifier.installed_regression_summary('Ran 189 tests in 2s\nOK')
        lines=self.installed_lines()
        for name in verifier.REQUIRED_SUITES:
            bad=[line for line in lines if f'({name}.' not in line]
            with self.subTest(missing_suite=name),self.assertRaises(AssertionError):
                verifier.installed_regression_summary(self.installed_log(bad))
        for name in verifier.REQUIRED_SUITES:
            index=next(i for i,line in enumerate(lines) if f'({name}.' in line)
            for outcome in ("skipped 'unavailable'",'FAIL','ERROR'):
                bad=lines.copy();bad[index]=bad[index].replace('... ok',f'... {outcome}')
                with self.subTest(suite=name,outcome=outcome),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))
        with patch.object(verifier.os,'name','posix'):
            summary=verifier.installed_regression_summary(self.installed_log(lines))
        self.assertEqual(summary['tests'],len(lines))
        self.assertEqual(summary['required_suites'],{name:1 for name in verifier.REQUIRED_SUITES})
        self.assertEqual(summary['status'],'PASS')
        self.assertEqual(len(summary['not_applicable_tests']),3)
        self.assertEqual(summary['unverified_tests'],[])
        self.assertEqual(summary['executed'],len(lines)-3)

    def test_windows_symlink_permission_skip_is_incomplete_never_pass(self):
        lines=self.installed_lines('nt')
        identity='test_workflow_bindings.WorkflowBindings.test_native_identity_still_rejects_symlink_escape'
        index=next(i for i,line in enumerate(lines) if f'({identity})' in line)
        unavailable=(lines[index].replace('... ok',
            '... skipped "OS did not authorize directory symlink creation: [WinError 1314] denied"'))
        lines[index]=unavailable
        with patch.object(verifier.os,'name','nt'):
            result=verifier.installed_regression_summary(self.installed_log(lines))
            self.assertEqual(result['status'],'INCOMPLETE')
            self.assertEqual(result['not_applicable_tests'],[])
            self.assertEqual(result['unverified_capability_tests'],[unavailable])
            self.assertEqual(result['unverified_tests'],[unavailable])
            # Even a misleading or unfamiliar reason may never reclassify this
            # current-platform symlink check as NOT_APPLICABLE.
            for reason in ('WinError 5','Windows path syntax','arbitrary'):
                bad=lines.copy();bad[index]=unavailable.replace(
                    'OS did not authorize directory symlink creation: [WinError 1314] denied',reason)
                self.assertEqual(verifier.installed_regression_summary(
                    self.installed_log(bad))['status'],'INCOMPLETE')
            for outcome in ('FAIL','ERROR'):
                bad=lines.copy();bad[index]=unavailable.split('... skipped ')[0]+'... '+outcome
                with self.subTest(outcome=outcome),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))
        with patch.object(verifier.os,'name','posix'),self.assertRaises(AssertionError):
            verifier.installed_regression_summary(self.installed_log(lines))

    def test_nonrequired_skipped_test_also_prevents_regression_pass(self):
        lines=self.installed_lines()
        skipped="test_optional (test_other.Optional.test_optional) ... skipped 'unavailable'"
        with patch.object(verifier.os,'name','posix'):
            result=verifier.installed_regression_summary(self.installed_log(lines+[skipped]))
        self.assertEqual(result['status'],'INCOMPLETE')
        self.assertEqual(result['unexpected_skip_tests'],[skipped])
        self.assertEqual(result['unverified_tests'],[skipped])

    def test_linux_symlinks_and_windows_only_cases_are_distinct(self):
        lines=self.installed_lines()
        with patch.object(verifier.os,'name','posix'):
            result=verifier.installed_regression_summary(self.installed_log(lines))
            self.assertEqual(result['status'],'PASS')
            self.assertEqual(len(result['not_applicable_tests']),3)
            self.assertEqual(result['unverified_capability_tests'],[])
            for identity in verifier.CAPABILITY_REQUIRED_TESTS:
                index=next(i for i,line in enumerate(lines) if f'({identity})' in line)
                bad=lines.copy()
                bad[index]=bad[index].replace('... ok'," ... skipped 'capability unavailable'")
                summary=verifier.installed_regression_summary(self.installed_log(bad))
                self.assertEqual(summary['status'],'INCOMPLETE')
                self.assertEqual(len(summary['unverified_capability_tests']),1)

    def test_platform_required_and_missing_checks_never_pass(self):
        linux=self.installed_lines()
        win=self.installed_lines('nt')
        with patch.object(verifier.os,'name','nt'):
            self.assertEqual(verifier.installed_regression_summary(
                self.installed_log(win))['status'],'PASS')
            for identity in verifier.PLATFORM_ONLY_TESTS:
                index=next(i for i,line in enumerate(win) if f'({identity})' in line)
                bad=win.copy();bad[index]=bad[index].replace('... ok',
                    " ... skipped 'permission or implementation missing'")
                self.assertEqual(verifier.installed_regression_summary(
                    self.installed_log(bad))['status'],'INCOMPLETE')
        with patch.object(verifier.os,'name','posix'):
            for identity in verifier.PLATFORM_ONLY_TESTS:
                index=next(i for i,line in enumerate(linux) if f'({identity})' in line)
                bad=linux.copy();bad[index]=bad[index].replace(
                    "... skipped 'another-platform only'",'... ok')
                with self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))
            for identity in [*verifier.PLATFORM_ONLY_TESTS,
                             *verifier.CAPABILITY_REQUIRED_TESTS]:
                bad=[line for line in linux if f'({identity})' not in line]
                with self.subTest(missing=identity),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(self.installed_log(bad))

    def test_unittest_totals_duplicate_and_partial_logs_cannot_pass(self):
        lines=self.installed_lines()
        with patch.object(verifier.os,'name','posix'):
            good=self.installed_log(lines)
            for log in (good.replace(f'Ran {len(lines)} tests', 'Ran 999 tests'),
                        good.replace('OK (skipped=3)','OK (skipped=2)'),
                        good.replace('OK (skipped=3)','FAILED (failures=1)'),
                        self.installed_log(lines+[lines[0]]),
                        good.replace(lines[0],lines[0].replace(
                            '(test_current_policy.Current.', '(test_other.Current.'))):
                with self.subTest(log=log[-100:]),self.assertRaises(AssertionError):
                    verifier.installed_regression_summary(log)

    def test_nonvisual_current_semantic_failure_cannot_hide_behind_new_pdf_work(self):
        result={'artifacts':{'editorial_policy':verifier.EXPECTED_POLICY,'readiness':'READY',
                            'used_output_review_ids':['synthetic-semantic']},
                'errors':[{'code':'VISUAL_REVIEW_INCOMPLETE','path':'evidence'},
                          {'code':'REVIEW_STALE','message':'Review old-visual no longer matches this input','path':'build/main.pdf'}]}
        verifier.require_current_semantics(result)
        for error in ({'code':'OUTPUT_SEMANTIC_REVIEW_PENDING','path':'evidence'},
                      {'code':'REVIEW_STALE','path':'manuscript/main.tex'},
                      {'code':'MODE_SEMANTIC_REVIEW_PENDING','path':'evidence'},
                      {'code':'REVIEW_STALE','message':'Rendered image bytes have changed','path':'evidence/pages/page-1.png'},
                      {'code':'DRAFT_NOT_RELEASABLE','path':'plan.json'}):
            bad=copy.deepcopy(result);bad['errors'].append(error)
            with self.subTest(error=error),self.assertRaises(AssertionError):verifier.require_current_semantics(bad)

    def test_missing_current_inputs_or_skipped_builds_remain_incomplete(self):
        for has_inputs,no_build in ((False,False),(True,True),(False,True)):
            self.assertEqual(verifier.verification_completion(has_inputs,no_build)[0],'INCOMPLETE')
        self.assertEqual(verifier.verification_completion(True,False),('PASS',[]))

    def test_default_manifest_is_discovered_but_explicit_path_takes_precedence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.assertIsNone(verifier.resolve_output_manifest(None,root))
            default=root/'examples/r4/verification-manifest.json';default.parent.mkdir(parents=True);default.write_text('{}')
            self.assertEqual(verifier.resolve_output_manifest(None,root),default)
            explicit=root/'requested.json'
            self.assertEqual(verifier.resolve_output_manifest(explicit,root),explicit)

    def test_engineering_only_does_not_discover_or_execute_default_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);manifest=root/'examples/r4/verification-manifest.json'
            manifest.parent.mkdir(parents=True);manifest.write_text('Deliberately unreadable output manifest')
            stdout=StringIO()
            with patch.object(verifier,'ROOT',root), patch.object(sys,'argv',['verify_release','missing.zip','--engineering-only']), redirect_stdout(stdout):
                self.assertEqual(verifier.main(),1)  # The missing archive is the actual failure.
            report=json.loads(stdout.getvalue())
            self.assertIsNone(report['manifest'])
            self.assertNotIn('outputs',report)
            self.assertNotIn('output manifest',report['failure'])

    def test_engineering_only_and_explicit_full_manifest_conflict(self):
        with patch.object(sys,'argv',['verify_release','missing.zip','--engineering-only','--manifest','explicit.json']):
            with self.assertRaises(SystemExit) as caught:verifier.main()
            self.assertEqual(caught.exception.code,2)

    def test_example_failure_records_keep_progress_and_actual_log_location(self):
        with tempfile.TemporaryDirectory() as td:
            destination=Path(td);build=destination/'project/outputs/thematic/build';build.mkdir(parents=True)
            (build/'build-report.json').write_text(json.dumps({'status':'FAILED','blocking_log_issues':{'overflow':['11.1444pt']}}))
            (build/'main.log').write_text('Actual overflow diagnostic')
            for name in ('verify_release',):
                spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/f'{name}.py')
                module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                report={'outputs':[{'output_id':'previous','build':'BUILT'},{'output_id':'thematic','build':'RUNNING'}]}
                module.record_failure_artifacts(destination,report)
                self.assertEqual(report['outputs'][0]['build'],'BUILT')
                self.assertEqual(report['outputs'][1]['build'],'FAILED')
                self.assertEqual(report['failure_artifacts'][0]['log'],str(build/'main.log'))
                self.assertEqual(report['failure_artifacts'][0]['blocking_log_issues'],{'overflow':['11.1444pt']})

    def synthetic_project(self,base):
        project=base/'source';project.mkdir();(project/'project.json').write_text('{}')
        specs=(('minimal','minimal','integrated'),('second','minimal','integrated'),
               ('thematic','thematic','integrated'),('lecture','lecture','integrated'),
               ('paper','paper','integrated'))
        for oid,profile,view in specs:
            out=project/'outputs'/oid;(out/'manuscript').mkdir(parents=True)
            plan={'output_id':oid,'schema_version':'2.2.0','editorial_policy':verifier.EXPECTED_POLICY,
                  'profile':profile,'view':view,'snapshot_id':'KB-synthetic','draft':profile=='paper',
                  'comparison_group':'synthetic-comparison','question_ids':['N-q'],
                  'selections':[{'node_id':'N-main','role':'principal_answer'}]}
            (out/'generated/statements').mkdir(parents=True)
            (out/'generated/statements/N-main.tex').write_text('Synthetic canonical bytes; not mathematics.')
            (out/'plan.json').write_text(json.dumps(plan))
            (out/'outline.md').write_text('Synthetic orchestration fixture, not a mathematical design.')
            (out/'manuscript/main.tex').write_text('% Synthetic orchestration fixture, no mathematical acceptance.')
        return project,[x[0] for x in specs]

    def test_manifest_resolves_relative_projects_and_rejects_duplicates_and_paths(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);project,outputs=self.synthetic_project(base);manifest=base/'manifest.json'
            for selected in (outputs,['../paper'],['paper','paper'],[]):
                manifest.write_text(json.dumps({'projects':[{'path':'source','outputs':selected}]}))
                if selected==outputs:
                    self.assertEqual(verifier.load_output_manifest(manifest)[0]['path'],project.resolve())
                else:
                    with self.assertRaises(ValueError):verifier.load_output_manifest(manifest)

    def synthetic_entries(self,base):
        import shutil
        project,outputs=self.synthetic_project(base)
        single=base/'single';paper=base/'draft'
        for dest,ids in ((single,['second']),(paper,['paper'])):
            dest.mkdir();(dest/'project.json').write_text('{}')
            for oid in ids:shutil.copytree(project/'outputs'/oid,dest/'outputs'/oid)
        return [{'path':single,'outputs':['second']},
                {'path':project,'outputs':['minimal','thematic','lecture']},
                {'path':paper,'outputs':['paper']}]

    def test_synthetic_orchestration_copies_sources_and_checks_paper_barrier(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);entries=self.synthetic_entries(base);project=entries[1]['path']
            before={p:p.read_bytes() for p in project.rglob('*') if p.is_file()};calls=[]
            def fake_check(command,cwd,env,**kwargs):
                calls.append((command,kwargs))
                if 'package' in command or ('release' in command and command[command.index('--output')+1]=='paper'):
                    self.assertEqual(kwargs['allowed_returncodes'],(3,))
                    return {'errors':[{'code':'DRAFT_NOT_RELEASABLE'}]}
                if 'release' in command:
                    return {'artifacts':{'output_id':command[command.index('--output')+1],'pages':1,'editorial_policy':verifier.EXPECTED_POLICY,'readiness':'READY','used_output_review_ids':['synthetic']},'errors':[{'code':'VISUAL_REVIEW_INCOMPLETE','path':'evidence'}]}
                if 'build' in command:return {'status':'BUILT','artifacts':{'pages':1}}
                if 'render' in command:
                    output=Path(command[command.index('--output')-1])/'outputs'/command[command.index('--output')+1]
                    CurrentVisualScope.write_artifacts(output,pages=1)
                    return {'status':'RENDERED_NOT_REVIEWED'}
                return {'status':'CHECKED'}
            result=verifier.verify_outputs(entries,base/'work',fake_check,
                Path(sys.executable),Path('synthetic-entry.py'),{},900,True)
            self.assertEqual(len(result['outputs']),5)
            self.assertEqual(before,{p:p.read_bytes() for p in before})
            self.assertEqual(sum('build' in cmd for cmd,_ in calls),5)
            self.assertEqual(sum('render' in cmd for cmd,_ in calls),5)
            self.assertEqual(result['outputs'][-1]['formal_package'],'BLOCKED: no archive created')

    def test_mismatched_comparison_snapshots_or_principals_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);entries=self.synthetic_entries(base)
            path=entries[1]['path']/'outputs/thematic/generated/statements/N-main.tex'
            path.write_text('Different synthetic canonical')
            def check(command,*args,**kwargs):
                return {'errors':[{'code':'DRAFT_NOT_RELEASABLE'}]}
            with self.assertRaises(AssertionError):
                verifier.verify_outputs(entries,base/'work',check,
                    Path(sys.executable),Path('synthetic-entry.py'),{},900,False)

    def test_paper_nondraft_cannot_enter_current_draft_verification(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);project,outputs=self.synthetic_project(base)
            path=project/'outputs/paper/plan.json';plan=json.loads(path.read_text());plan['draft']=False
            path.write_text(json.dumps(plan))
            with self.assertRaises(AssertionError):
                verifier.verify_outputs([{'path':project,'outputs':['paper']}],base/'work',lambda *a,**k:{},
                    Path(sys.executable),Path('unused'),{},900,False)

    def test_timeout_terminates_descendants_not_only_the_python_parent(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);pid_file=base/'child.pid'
            child="import time;time.sleep(30)"
            parent=("import pathlib,subprocess,sys,time;p=subprocess.Popen([sys.executable,'-c',"+repr(child)+"]);"
                    "pathlib.Path("+repr(str(pid_file))+").write_text(str(p.pid));"
                    "print('child spawned',flush=True);time.sleep(30)")
            report={'checks':[]}
            with self.assertRaises(subprocess.TimeoutExpired):
                verifier.run_check([sys.executable,'-I','-u','-c',parent],base,os.environ.copy(),report,False,timeout=3)
            pid=int(pid_file.read_text())
            if os.name=='nt':
                import ctypes
                from ctypes import wintypes
                kernel=ctypes.WinDLL('kernel32',use_last_error=True)
                kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
                kernel.OpenProcess.restype=wintypes.HANDLE
                kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
                kernel.CloseHandle.argtypes=[wintypes.HANDLE]
                handle=kernel.OpenProcess(0x1000,False,pid)
                if handle:
                    try:
                        code=wintypes.DWORD()
                        self.assertTrue(kernel.GetExitCodeProcess(handle,ctypes.byref(code)))
                        self.assertNotEqual(code.value,259,'Descendant is STILL_ACTIVE after timeout cleanup')
                    finally:kernel.CloseHandle(handle)
                else:self.assertEqual(ctypes.get_last_error(),87,'Unable to confirm child process termination')
            else:
                state=Path(f'/proc/{pid}/stat')
                if state.exists():self.assertEqual(state.read_text().split()[2],'Z')
                else:
                    with self.assertRaises(ProcessLookupError):os.kill(pid,0)
            self.assertEqual(report['checks'][0]['termination']['returncode'],0)
            self.assertIn('child spawned',report['checks'][0]['stdout'])

    @unittest.skipUnless(os.name=='nt','Windows Job Object lifetime contract')
    def test_exited_parent_inherited_pipe_is_bounded_and_external_process_survives(self):
        import ctypes
        from ctypes import wintypes as w
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);pidfile=base/'orphan.pid'
            child="import time;print('child holds pipe',flush=True);time.sleep(30)"
            parent=("import pathlib,subprocess,sys;p=subprocess.Popen([sys.executable,'-I','-u','-c',"+repr(child)+"]);"
                    "pathlib.Path("+repr(str(pidfile))+").write_text(str(p.pid));print('parent exits',flush=True)")
            unrelated=subprocess.Popen([sys.executable,'-I','-c','import time;time.sleep(30)'])
            try:
                report={'checks':[]};started=time.monotonic()
                with self.assertRaises(subprocess.TimeoutExpired):
                    verifier.run_check([sys.executable,'-I','-u','-c',parent],base,os.environ.copy(),report,False,timeout=3)
                self.assertLess(time.monotonic()-started,10)
                self.assertIsNone(unrelated.poll(),'An unrelated process was terminated')
                self.assertIn('parent exits',report['checks'][0]['stdout'])
                self.assertIn('child holds pipe',report['checks'][0]['stdout'])
                self.assertEqual(report['checks'][0]['termination']['method'],'TerminateJobObject')
                kernel=ctypes.WinDLL('kernel32',use_last_error=True)
                kernel.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];kernel.OpenProcess.restype=w.HANDLE
                kernel.GetExitCodeProcess.argtypes=[w.HANDLE,ctypes.POINTER(w.DWORD)]
                kernel.CloseHandle.argtypes=[w.HANDLE]
                handle=kernel.OpenProcess(0x1000,False,int(pidfile.read_text()))
                if handle:
                    try:
                        code=w.DWORD();self.assertTrue(kernel.GetExitCodeProcess(handle,ctypes.byref(code)))
                        self.assertNotEqual(code.value,259)
                    finally:kernel.CloseHandle(handle)
                else:self.assertEqual(ctypes.get_last_error(),87)
            finally:
                unrelated.terminate();unrelated.wait(timeout=10)


class CurrentVisualScope(unittest.TestCase):
    """Synthetic byte-binding fixtures only, never page/mathematical acceptance."""
    @staticmethod
    def write_artifacts(out,pages=8):
        (out/'build').mkdir(parents=True,exist_ok=True)
        (out/'evidence/pages').mkdir(parents=True,exist_ok=True)
        pdf=b'%PDF-1.4\nSynthetic artifact identity fixture, not a manuscript.\n'
        (out/'build/main.pdf').write_bytes(pdf)
        digest=hashlib.sha256(pdf).hexdigest()
        (out/'build/build-report.json').write_text(json.dumps({'status':'BUILT','pages':pages,'pdf_sha256':digest}))
        png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6S1cAAAAASUVORK5CYII=')
        rows=[]
        for number in range(1,pages+1):
            path=f'evidence/pages/page-{number}.png';(out/path).write_bytes(png)
            rows.append({'page':number,'path':path,'sha256':hashlib.sha256(png).hexdigest()})
        (out/'evidence/render-manifest.json').write_text(json.dumps({'pdf_sha256':digest,'pages':rows}))

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.out=Path(self.temp.name)
        self.write_artifacts(self.out)
        self.review={'review_id':'old-visual','kind':'visual','scope':{'output_ids':['example']},
                     'inputs':[{'path':p} for p in ['build/main.pdf','build/build-report.json','evidence/render-manifest.json']+
                               [f'evidence/pages/page-{n}.png' for n in range(1,8)]]}
        (self.out/'evidence/old-visual.json').write_text(json.dumps(self.review))
        self.result={'artifacts':{'output_id':'example','pages':8,'editorial_policy':verifier.EXPECTED_POLICY,
                                 'readiness':'READY','used_output_review_ids':['synthetic-semantic']},
                     'errors':[{'code':'REVIEW_SCOPE_INSUFFICIENT','path':'',
                                'message':'Review old-visual omits necessary inputs: evidence/pages/page-8.png'},
                               {'code':'VISUAL_REVIEW_INCOMPLETE','path':'evidence'}]}

    def tearDown(self):self.temp.cleanup()

    def test_new_page_from_old_visual_scope_requires_actual_new_review(self):
        before={p:p.read_bytes() for p in self.out.rglob('*') if p.is_file()}
        checked=verifier.require_current_semantics(self.result,self.out)
        self.assertEqual(checked['visual_review_status'],'NEW_VISUAL_REVIEW_REQUIRED')
        self.assertFalse(checked['formal_release_authorized'])
        self.assertEqual(len(checked['new_pdf_visual_findings_pending']),2)
        self.assertEqual(before,{p:p.read_bytes() for p in before})

    def test_insufficient_semantic_or_unknown_review_never_becomes_visual(self):
        for message in ('Review synthetic-semantic omits necessary inputs: evidence/pages/page-8.png',
                        'Review old-visual omits necessary inputs: manuscript/main.tex',
                        'Semantic review omits consumed nodes: N-missing',
                        'Review old-visual omits necessary inputs: evidence/pages/page-9.png'):
            bad=copy.deepcopy(self.result);bad['errors'][0]['message']=message
            with self.subTest(message=message),self.assertRaises(AssertionError):
                verifier.require_current_semantics(bad,self.out)

    def test_missing_or_corrupt_current_png_cannot_hide_behind_old_visual_scope(self):
        image=self.out/'evidence/pages/page-8.png';original=image.read_bytes()
        for operation in ('missing','changed'):
            if operation=='missing':image.unlink()
            else:image.write_bytes(b'corrupt')
            with self.subTest(operation=operation),self.assertRaises(AssertionError):
                verifier.require_current_semantics(self.result,self.out)
            image.write_bytes(original)

    def test_missing_invalid_or_stale_manifest_is_a_hard_failure(self):
        manifest=self.out/'evidence/render-manifest.json';original=manifest.read_bytes()
        for variant in (None,b'{',b'[]',json.dumps({'pdf_sha256':'wrong','pages':[]}).encode(),
                        json.dumps({'pdf_sha256':hashlib.sha256((self.out/'build/main.pdf').read_bytes()).hexdigest(),'pages':[]}).encode()):
            if variant is None:manifest.unlink()
            else:manifest.write_bytes(variant)
            with self.subTest(variant=variant),self.assertRaises((OSError,ValueError,AssertionError)):
                verifier.require_current_semantics(self.result,self.out)
            manifest.write_bytes(original)

    def test_missing_or_changed_pdf_cannot_be_waived_as_visual_reading(self):
        pdf=self.out/'build/main.pdf';original=pdf.read_bytes()
        for operation in ('missing','changed'):
            if operation=='missing':pdf.unlink()
            else:pdf.write_bytes(b'%PDF-corrupt')
            with self.subTest(operation=operation),self.assertRaises(AssertionError):
                verifier.require_current_semantics(self.result,self.out)
            pdf.write_bytes(original)

    def test_poppler_zero_padded_page_names_remain_valid(self):
        manifest=self.out/'evidence/render-manifest.json';data=json.loads(manifest.read_text())
        for row in data['pages']:
            target=f"evidence/pages/page-{row['page']:02d}.png"
            (self.out/row['path']).rename(self.out/target);row['path']=target
        manifest.write_text(json.dumps(data))
        self.review['inputs']=[{'path':p} for p in ['build/main.pdf','build/build-report.json','evidence/render-manifest.json']+
                              [f'evidence/pages/page-{n:02d}.png' for n in range(1,8)]]
        (self.out/'evidence/old-visual.json').write_text(json.dumps(self.review))
        self.result['errors'][0]['message']='Review old-visual omits necessary inputs: evidence/pages/page-08.png'
        self.assertEqual(verifier.require_current_semantics(self.result,self.out)['visual_review_status'],
                         'NEW_VISUAL_REVIEW_REQUIRED')

    def test_known_old_visual_stale_is_pending_but_unknown_or_corruption_is_blocking(self):
        for message,allowed in (('Review old-visual no longer matches this input',True),
                                ('Review synthetic-semantic no longer matches this input',False),
                                ('Rendered image bytes have changed',False)):
            changed=copy.deepcopy(self.result)
            changed['errors'].append({'code':'REVIEW_STALE','path':'evidence/pages/page-1.png','message':message})
            if allowed:
                self.assertEqual(verifier.require_current_semantics(changed,self.out)['visual_review_status'],
                                 'NEW_VISUAL_REVIEW_REQUIRED')
            else:
                with self.assertRaises(AssertionError):verifier.require_current_semantics(changed,self.out)


if __name__=='__main__':unittest.main()
