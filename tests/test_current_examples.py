"""Current shared-canonical and non-overwrite regression; synthetic only."""
from pathlib import Path
import tempfile
import unittest
from test_v2 import fixture
from survey_core.snapshots import freeze_snapshot
from survey_core.plans import create_plan
from survey_core.exports import prepare_output

class CurrentPairedOutputs(unittest.TestCase):
    def test_current_modes_share_canonical_and_reprepare_preserves_author(self):
        with tempfile.TemporaryDirectory() as td:
            root=fixture(Path(td)/'project')
            sid=freeze_snapshot(root)['artifacts']['snapshot_id'];canonical=[]
            for view in ('methods','boundaries'):
                create_plan(root,view,sid,profile='minimal',view=view,draft=True,questions=['N-q'],principals=['N-main'])
                path=root/f'outputs/{view}/plan.json'
                prepare_output(root,path,draft=True)
                main=path.parent/'manuscript/main.tex';main.write_bytes(main.read_bytes()+b'\n% Synthetic author edit.\n');before=main.read_bytes()
                prepare_output(root,path,draft=True);self.assertEqual(main.read_bytes(),before)
                canonical.append((path.parent/'generated/statements/N-main.tex').read_bytes())
            self.assertEqual(canonical[0],canonical[1])

if __name__=='__main__':unittest.main()
