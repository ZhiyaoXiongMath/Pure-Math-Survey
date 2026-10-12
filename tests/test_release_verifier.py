"""Retain real child failure evidence without granting build acceptance."""
from pathlib import Path
import importlib.util
import copy
import json
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
                        base,os.environ.copy(),report,False,timeout=1)
            self.assertTrue(base.exists())
            row=report['checks'][0]
            self.assertIsNone(row['returncode'])
            self.assertIn('TeX still running',row['stdout'])
            self.assertEqual(row['timeout_seconds'],1)


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
                          {'code':'REVIEW_STALE','path':'build/main.pdf'}]}
        verifier.require_current_r3_semantics(result)
        for error in ({'code':'OUTPUT_SEMANTIC_REVIEW_PENDING','path':'evidence'},
                      {'code':'REVIEW_STALE','path':'manuscript/main.tex'},
                      {'code':'MODE_SEMANTIC_REVIEW_PENDING','path':'evidence'},
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
                    return {'artifacts':{'editorial_policy':verifier.EXPECTED_POLICY,'readiness':'READY','used_output_review_ids':['synthetic']},'errors':[{'code':'VISUAL_REVIEW_INCOMPLETE','path':'evidence'}]}
                if 'build' in command:return {'status':'BUILT','artifacts':{'pages':1}}
                if 'render' in command:return {'status':'RENDERED_NOT_REVIEWED'}
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
            base=Path(td);marker=base/'child-survived.txt'
            child="import pathlib,time;time.sleep(2);pathlib.Path("+repr(str(marker))+").write_text('survived')"
            parent="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(child)+"]);print('child spawned',flush=True);time.sleep(20)"
            report={'checks':[]}
            with self.assertRaises(subprocess.TimeoutExpired):
                verifier.run_check([sys.executable,'-I','-u','-c',parent],base,os.environ.copy(),report,False,timeout=1)
            time.sleep(2.2)
            self.assertFalse(marker.exists())
            self.assertEqual(report['checks'][0]['termination']['returncode'],0)
            self.assertIn('child spawned',report['checks'][0]['stdout'])


if __name__=='__main__':unittest.main()
