"""Retain real child failure evidence without granting build acceptance."""
from pathlib import Path
import importlib.util
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


if __name__=='__main__':unittest.main()
