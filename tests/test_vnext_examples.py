"""Minimal historical-byte regression; no old authored article is retained."""
from pathlib import Path
import tempfile
import unittest
from test_v2 import fixture, putnode, plan
from survey_core.snapshots import freeze_snapshot, verify_snapshot
from survey_core.models import load_plan
from survey_core.exports import prepare_output

class HistoricalSnapshotRepair(unittest.TestCase):
    def test_new_dependency_preserves_old_snapshot_and_shared_new_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=fixture(Path(td)/'project')
            old=freeze_snapshot(root)['artifacts']['snapshot_id']
            putnode(root,'N-normalization','definition',r'Use the real scalar convention $x\in\mathbb R$.')
            new=freeze_snapshot(root)['artifacts']['snapshot_id']
            self.assertNotEqual(old,new)
            self.assertFalse((root/f'snapshots/{old}/files/knowledge/nodes/N-normalization.md').exists())
            self.assertEqual(verify_snapshot(root,old)['status'],'VERIFIED')
            for profile in ('minimal','thematic','lecture'):
                path=plan(root,profile,profile)
                value=load_plan(path)
                value['selections'].append({'node_id':'N-normalization','role':'essential_bridge','statement_treatment':'full','proof_treatment':'none','reason':'Synthetic normalization dependency'})
                from survey_core.common import write_json
                write_json(path,value)
                prepare_output(root,path,draft=True)
                self.assertEqual(value['snapshot_id'],new)
                self.assertIn('N-normalization.tex',(path.parent/'manuscript/main.tex').read_text())

if __name__=='__main__':unittest.main()
