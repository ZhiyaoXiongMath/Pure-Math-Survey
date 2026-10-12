"""Stored real authoring evidence, distinct from synthetic release-gate tests.

Bindings are rechecked; tests do not pretend to read mathematics or PDF pages.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class CurrentAuthoredBenchmarks(unittest.TestCase):
    def test_current_real_outputs_bind_and_preserve_the_shared_spine(self):
        with tempfile.TemporaryDirectory() as td:
            p=subprocess.run([sys.executable,str(ROOT/'tools/verify_rc2_examples.py'),
                '--no-build','--output',str(Path(td)/'copy')],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            report=json.loads(p.stdout)
            self.assertEqual(len(report['outputs']),4)
            self.assertEqual({(r['profile'],r['view']) for r in report['outputs']},
                {('thematic','integrated'),('minimal','methods'),
                 ('minimal','boundaries'),('lecture','methods')})
            self.assertTrue(all(r['reviewer_mode']=='author_reread' for r in report['outputs']))
            self.assertTrue(all(r['recorded_policy']=='four-modes-2026-10-12-rc2'
                                and r['evaluated_policy']==r['recorded_policy']
                                and not r['release_authorized'] for r in report['outputs']))
            self.assertEqual(report['new_pdf_visual_review'],'NOT PERFORMED')
            self.assertEqual(report['independent_mathematical_review'],'NOT VERIFIED')


if __name__=='__main__':unittest.main()
