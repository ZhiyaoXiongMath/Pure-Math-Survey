#!/usr/bin/env python3
"""Execute native resource/scaffold smoke checks; this is not mathematical review."""
from __future__ import annotations
import argparse
import ast
import json
import re
from pathlib import Path
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from package_release import selected_files
from survey_core.common import VERSION,write_json
from survey_core.knowledge import init_project,inventory
from survey_core.snapshots import freeze_snapshot
from survey_core.plans import create_plan
from survey_core.exports import prepare_output,verify_generated
from survey_core.models import load_plan
from survey_core.models import node_bytes
ROOT=Path(__file__).resolve().parents[1]

def check()->dict:
    files=selected_files(ROOT)
    for p in files:
        if p.endswith('.py'):ast.parse(files[p].decode('utf-8'),filename=p,feature_version=(3,10))
    checked_links = 0
    for name in ['SKILL.md'] + ['references/' + p.name for p in (ROOT/'references').glob('*.md')]:
        text = (ROOT/name).read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'): continue
            target = target.split('#', 1)[0]
            if target and not (ROOT/name).parent.joinpath(target).exists():
                raise ValueError(f'Broken runtime documentation link: {name}: {target}')
            checked_links += 1
    inventory(ROOT/'assets/v2/empty-project')
    exercised=[]
    with tempfile.TemporaryDirectory() as tmp:
        base=Path(tmp);scope=base/'scope.md';scope.write_text('Software-only fixture: show the implication x=0 implies x^2=0. No source or semantic certification.\n')
        project=base/'project';init_project(project,'asset-smoke',scope)
        common={'schema_version':VERSION,'id':'N-q','kind':'question','title':'Software fixture','facets':['foundations'],'question_ids':[],'mathematical_status':'unassessed','origin':'local_derivation','sources':[],'links':[]}
        (project/'knowledge/nodes').mkdir()
        (project/'knowledge/nodes/N-q.md').write_bytes(node_bytes(common,'# Question\n\nDoes $x=0$ imply $x^2=0$?'))
        (project/'knowledge/nodes/N-r.md').write_bytes(node_bytes({**common,'id':'N-r','kind':'result','question_ids':['N-q']},'# Result\n\n## Canonical statement\n\n```latex\nFor $x\\in\\mathbb R$, $x=0$ implies $x^2=0$.\n```\n\n## Provenance\n\nSoftware fixture only.'))
        write_json(project/'knowledge/coverage.json',{'schema_version':VERSION,'questions':[{'question_id':'N-q','answer_nodes':['N-r'],'mechanism_nodes':[],'boundary_nodes':[],'gaps':['Actual review not performed.'],'assessment':'pending','rationale':'Resource smoke test only.'}]})
        sid=freeze_snapshot(project)['artifacts']['snapshot_id']
        for profile in ('minimal','thematic','lecture'):
            create_plan(project,profile,sid,profile=profile,draft=True)
            p=project/f'outputs/{profile}/plan.json';prepare_output(project,p,draft=True);verify_generated(project,load_plan(p));exercised.append(profile)
    return {'status':'PASSED','runtime_members':len(files),'checked_documentation_links':checked_links,'profile_preparations_executed':exercised,
            'python_3_10_grammar':'parsed; not a Python 3.10 runtime test','mathematical_certification':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json',action='store_true');parser.parse_args()
    try:print(json.dumps(check(),indent=2))
    except Exception as e:print(json.dumps({'status':'FAILED','error':str(e)}));raise SystemExit(2)
