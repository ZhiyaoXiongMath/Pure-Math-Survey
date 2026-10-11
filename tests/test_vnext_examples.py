"""Actual authored benchmarks, unlike synthetic gate fixtures in test_vnext.

This rechecks stored source-bound author observations; it does not perform an
independent mathematical reading or inspect new PDF pages automatically.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

class AuthoredBenchmarks(unittest.TestCase):
    def test_source_bound_benchmarks_and_paper_block(self):
        with tempfile.TemporaryDirectory() as td:
            p=subprocess.run([sys.executable,str(ROOT/'tools/verify_vnext_examples.py'),
                '--no-build','--output',str(Path(td)/'copy')],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            report=json.loads(p.stdout)
            self.assertEqual(len(report['outputs']),7)
            self.assertGreaterEqual(report['snapshots_verified'],5)
            for name in ('schur','compactness'):
                rows=[r for r in report['outputs'] if r['project']==name]
                self.assertEqual(len({r['statement_sha256'] for r in rows}),1)
                self.assertEqual({r['profile'] for r in rows if r['readiness']=='READY'},
                                 {'minimal','thematic','lecture'})
            paper=next(r for r in report['outputs'] if r['profile']=='paper')
            self.assertEqual(paper['formal_release'],'BLOCKED')
            self.assertEqual(report['new_pdf_visual_review'],'NOT PERFORMED')

    def test_norm_repair_preserves_historical_snapshots(self):
        root=ROOT/'examples/vnext/projects/compactness'
        snapshots=sorted((root/'snapshots').glob('KB-*'))
        old=[s for s in snapshots if not (s/'files/knowledge/nodes/N-norm.md').exists()]
        new=[s for s in snapshots if (s/'files/knowledge/nodes/N-norm.md').exists()]
        self.assertTrue(old and new)
        for mode in ('minimal','thematic','lecture'):
            out=root/'outputs'/mode
            plan=json.loads((out/'plan.json').read_text())
            self.assertTrue((root/'snapshots'/plan['snapshot_id']/'files/knowledge/nodes/N-norm.md').is_file())
            self.assertIn('generated/statements/N-norm.tex',(out/'manuscript/main.tex').read_text())

if __name__=='__main__':unittest.main()
