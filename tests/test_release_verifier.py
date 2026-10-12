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


class R3VerifierContracts(unittest.TestCase):
    """Synthetic verifier orchestration only; no accepted mathematics is created."""
    def valid_version(self):
        return {'version':'2.1.0','schema_version':'2.0.0','output_schema_version':'2.2.0',
                'editorial_policy':verifier.EXPECTED_POLICY,
                'supported_output_contracts':[{'schema_version':s,'editorial_policy':p}
                                              for s,p in sorted(verifier.EXPECTED_CONTRACTS)]}

    def test_installed_rc2_or_missing_old_capabilities_cannot_pass_as_r3(self):
        actual=self.valid_version()
        verifier.assert_installed_contract(actual)
        for key,value in (('editorial_policy','four-modes-2026-10-12-rc2'),
                          ('version','2.2.0'),('schema_version','2.1.0'),
                          ('supported_output_contracts',actual['supported_output_contracts'][:-1])):
            wrong=copy.deepcopy(actual);wrong[key]=value
            with self.subTest(key=key),self.assertRaises(AssertionError):verifier.assert_installed_contract(wrong)

    def test_r3_suite_must_really_execute_not_merely_total_old_tests(self):
        with self.assertRaises(AssertionError):verifier.installed_regression_summary('Ran 189 tests in 2s\nOK')
        with self.assertRaises(AssertionError):
            verifier.installed_regression_summary('test_case (test_r3_policy.R3.test_case) ... skipped reason\nRan 1 tests in 2s\nOK')
        summary=verifier.installed_regression_summary('test_case (test_r3_policy.R3.test_case) ... ok\nRan 190 tests in 2s\nOK')
        self.assertEqual((summary['tests'],summary['r3_policy_tests']),(190,1))

    def test_nonvisual_r3_semantic_failure_cannot_hide_behind_new_pdf_work(self):
        result={'artifacts':{'editorial_policy':verifier.EXPECTED_POLICY,'readiness':'READY',
                            'used_output_review_ids':['synthetic-semantic']},
                'errors':[{'code':'VISUAL_REVIEW_INCOMPLETE','path':'evidence'},
                          {'code':'REVIEW_STALE','message':'Review old-visual no longer matches this input','path':'build/main.pdf'}]}
        verifier.require_current_r3_semantics(result)
        for error in ({'code':'OUTPUT_SEMANTIC_REVIEW_PENDING','path':'evidence'},
                      {'code':'REVIEW_STALE','path':'manuscript/main.tex'},
                      {'code':'MODE_SEMANTIC_REVIEW_PENDING','path':'evidence'},
                      {'code':'REVIEW_STALE','message':'Rendered image bytes have changed','path':'evidence/pages/page-1.png'},
                      {'code':'DRAFT_NOT_RELEASABLE','path':'plan.json'}):
            bad=copy.deepcopy(result);bad['errors'].append(error)
            with self.subTest(error=error),self.assertRaises(AssertionError):verifier.require_current_r3_semantics(bad)

    def test_missing_r3_inputs_or_skipped_builds_remain_incomplete(self):
        for has_inputs,no_build in ((False,False),(True,True),(False,True)):
            self.assertEqual(verifier.verification_completion(has_inputs,no_build)[0],'INCOMPLETE')
        self.assertEqual(verifier.verification_completion(True,False),('PASS',[]))

    def test_default_manifest_is_discovered_but_explicit_path_takes_precedence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.assertIsNone(verifier.resolve_r3_manifest(None,root))
            default=root/'examples/r3/verification-manifest.json';default.parent.mkdir(parents=True);default.write_text('{}')
            self.assertEqual(verifier.resolve_r3_manifest(None,root),default)
            explicit=root/'requested.json'
            self.assertEqual(verifier.resolve_r3_manifest(explicit,root),explicit)

    def test_reviewed_rc2_layout_mapping_is_limited_to_each_approved_output(self):
        spec=importlib.util.spec_from_file_location('rc2_mapping',ROOT/'tools/verify_rc2_examples.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for oid in ('thematic','minimal-methods','minimal-boundaries'):
            selected=module.historical_layout_override('time-compactness',oid)
            self.assertEqual(selected['emergency_stretch_em'],2.0)
            self.assertTrue(selected['reason'])
        for project,oid in (('schur','rc2-lecture'),('other','thematic'),
                            ('r3','minimal-methods'),('time-compactness','unreviewed')):
            self.assertIsNone(module.historical_layout_override(project,oid))
        copy=module.historical_layout_override('time-compactness','thematic')
        copy['emergency_stretch_em']=9.0
        self.assertEqual(module.historical_layout_override('time-compactness','thematic')['emergency_stretch_em'],2.0)

    def test_example_failure_records_keep_progress_and_actual_log_location(self):
        with tempfile.TemporaryDirectory() as td:
            destination=Path(td);build=destination/'project/outputs/thematic/build';build.mkdir(parents=True)
            (build/'build-report.json').write_text(json.dumps({'status':'FAILED','blocking_log_issues':{'overflow':['11.1444pt']}}))
            (build/'main.log').write_text('Actual overflow diagnostic')
            for name in ('verify_rc2_examples','verify_vnext_examples'):
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
        specs=(('methods','minimal','methods'),('boundaries','minimal','boundaries'),
               ('thematic','thematic','integrated'),('lecture','lecture','integrated'),
               ('paper','paper','integrated'))
        for oid,profile,view in specs:
            out=project/'outputs'/oid;(out/'manuscript').mkdir(parents=True)
            plan={'output_id':oid,'schema_version':'2.2.0','editorial_policy':verifier.EXPECTED_POLICY,
                  'profile':profile,'view':view,'snapshot_id':'KB-synthetic','draft':profile=='paper',
                  'comparison_group':'synthetic-pair','question_ids':['N-q'],
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
                    self.assertEqual(verifier.load_r3_manifest(manifest)[0]['path'],project.resolve())
                else:
                    with self.assertRaises(ValueError):verifier.load_r3_manifest(manifest)

    def test_synthetic_orchestration_copies_sources_and_checks_paper_barrier(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);project,outputs=self.synthetic_project(base)
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
            result=verifier.verify_r3_outputs([{'path':project,'outputs':outputs}],base/'work',fake_check,
                Path(sys.executable),Path('synthetic-entry.py'),{},900,True)
            self.assertEqual(len(result['outputs']),5)
            self.assertEqual(before,{p:p.read_bytes() for p in before})
            self.assertEqual(sum('build' in cmd for cmd,_ in calls),5)
            self.assertEqual(sum('render' in cmd for cmd,_ in calls),5)
            self.assertEqual(result['outputs'][-1]['formal_package'],'BLOCKED: no archive created')

    def test_mismatched_minimal_spines_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);project,outputs=self.synthetic_project(base)
            path=project/'outputs/boundaries/generated/statements/N-main.tex';path.write_text('Different synthetic canonical')
            def check(command,*args,**kwargs):
                return {'errors':[{'code':'DRAFT_NOT_RELEASABLE'}]}
            with self.assertRaises(AssertionError):
                verifier.verify_r3_outputs([{'path':project,'outputs':outputs}],base/'work',check,
                    Path(sys.executable),Path('synthetic-entry.py'),{},900,False)

    def test_paper_nondraft_cannot_enter_real_r3_verification(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);project,outputs=self.synthetic_project(base)
            path=project/'outputs/paper/plan.json';plan=json.loads(path.read_text());plan['draft']=False
            path.write_text(json.dumps(plan))
            with self.assertRaises(AssertionError):
                verifier.verify_r3_outputs([{'path':project,'outputs':['paper']}],base/'work',lambda *a,**k:{},
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
        checked=verifier.require_current_r3_semantics(self.result,self.out)
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
                verifier.require_current_r3_semantics(bad,self.out)

    def test_missing_or_corrupt_current_png_cannot_hide_behind_old_visual_scope(self):
        image=self.out/'evidence/pages/page-8.png';original=image.read_bytes()
        for operation in ('missing','changed'):
            if operation=='missing':image.unlink()
            else:image.write_bytes(b'corrupt')
            with self.subTest(operation=operation),self.assertRaises(AssertionError):
                verifier.require_current_r3_semantics(self.result,self.out)
            image.write_bytes(original)

    def test_missing_invalid_or_stale_manifest_is_a_hard_failure(self):
        manifest=self.out/'evidence/render-manifest.json';original=manifest.read_bytes()
        for variant in (None,b'{',b'[]',json.dumps({'pdf_sha256':'wrong','pages':[]}).encode(),
                        json.dumps({'pdf_sha256':hashlib.sha256((self.out/'build/main.pdf').read_bytes()).hexdigest(),'pages':[]}).encode()):
            if variant is None:manifest.unlink()
            else:manifest.write_bytes(variant)
            with self.subTest(variant=variant),self.assertRaises((OSError,ValueError,AssertionError)):
                verifier.require_current_r3_semantics(self.result,self.out)
            manifest.write_bytes(original)

    def test_missing_or_changed_pdf_cannot_be_waived_as_visual_reading(self):
        pdf=self.out/'build/main.pdf';original=pdf.read_bytes()
        for operation in ('missing','changed'):
            if operation=='missing':pdf.unlink()
            else:pdf.write_bytes(b'%PDF-corrupt')
            with self.subTest(operation=operation),self.assertRaises(AssertionError):
                verifier.require_current_r3_semantics(self.result,self.out)
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
        self.assertEqual(verifier.require_current_r3_semantics(self.result,self.out)['visual_review_status'],
                         'NEW_VISUAL_REVIEW_REQUIRED')

    def test_known_old_visual_stale_is_pending_but_unknown_or_corruption_is_blocking(self):
        for message,allowed in (('Review old-visual no longer matches this input',True),
                                ('Review synthetic-semantic no longer matches this input',False),
                                ('Rendered image bytes have changed',False)):
            changed=copy.deepcopy(self.result)
            changed['errors'].append({'code':'REVIEW_STALE','path':'evidence/pages/page-1.png','message':message})
            if allowed:
                self.assertEqual(verifier.require_current_r3_semantics(changed,self.out)['visual_review_status'],
                                 'NEW_VISUAL_REVIEW_REQUIRED')
            else:
                with self.assertRaises(AssertionError):verifier.require_current_r3_semantics(changed,self.out)


if __name__=='__main__':unittest.main()
