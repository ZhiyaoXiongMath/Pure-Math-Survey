#!/usr/bin/env python3
"""Execute installed Minimal resource checks; no mathematical certification."""
from __future__ import annotations
import argparse
import ast
import json
import re
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from package_release import selected_files
from survey_core.common import VERSION, SurveyError, write_json
from survey_core.knowledge import init_project, inventory
from survey_core.snapshots import freeze_snapshot
from survey_core.plans import create_plan
from survey_core.exports import prepare_output, verify_generated
from survey_core.models import load_plan, node_bytes

ROOT = Path(__file__).resolve().parents[1]


def check() -> dict:
    files = selected_files(ROOT)
    for name, data in files.items():
        if name.endswith('.py'):
            ast.parse(data.decode('utf-8'), filename=name, feature_version=(3, 10))
    checked_links = 0
    for name, data in files.items():
        if not name.endswith('.md'):
            continue
        for target in re.findall(r'\]\(([^)]+)\)', data.decode('utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            if not target:
                continue
            resolved = (ROOT / name).parent.joinpath(target).resolve()
            if not resolved.is_relative_to(ROOT) or resolved.relative_to(ROOT).as_posix() not in files:
                raise ValueError(f'Link is not an installed resource: {name}: {target}')
            checked_links += 1
    rejected = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        scope = base / 'scope.md'
        scope.write_text('Software fixture: x=0 implies x^2=0. No mathematical certification.\n', encoding='utf-8')
        project = base / 'project'
        init_project(project, 'asset-smoke', scope)
        common = {'schema_version': VERSION, 'id': 'N-q', 'kind': 'question',
                  'title': 'Software fixture', 'facets': ['foundations'], 'question_ids': [],
                  'mathematical_status': 'unassessed', 'origin': 'local_derivation',
                  'sources': [], 'links': []}
        (project / 'knowledge/nodes').mkdir(exist_ok=True)
        (project / 'knowledge/nodes/N-q.md').write_bytes(node_bytes(common, '# Question\n\nDoes $x=0$ imply $x^2=0$?'))
        (project / 'knowledge/nodes/N-r.md').write_bytes(node_bytes(
            {**common, 'id': 'N-r', 'kind': 'result', 'question_ids': ['N-q']},
            '# Result\n\n## Canonical statement\n\n```latex\nFor $x\\in\\mathbb R$, $x=0$ implies $x^2=0$.\n```\n\n## Method and use\n\nSubstitute zero into the square. Software fixture only.'))
        write_json(project / 'knowledge/coverage.json', {
            'schema_version': VERSION, 'questions': [{'question_id': 'N-q',
            'answer_nodes': ['N-r'], 'mechanism_nodes': [], 'boundary_nodes': [],
            'gaps': [], 'assessment': 'pending', 'rationale': 'Software fixture only.'}]})
        inventory(project)
        sid = freeze_snapshot(project)['artifacts']['snapshot_id']
        create_plan(project, 'minimal-integrated', sid, profile='minimal', view='integrated')
        path = project / 'outputs/minimal-integrated/plan.json'
        prepared = prepare_output(project, path)
        verify_generated(project, load_plan(path))
        if prepared['status'] != 'PREPARED':
            raise AssertionError('Minimal preparation did not complete')
        before = {p.relative_to(project).as_posix(): p.read_bytes()
                  for p in project.rglob('*') if p.is_file()}
        for profile, view in [('thematic', 'integrated'), ('lecture', 'integrated'),
                              ('paper', 'integrated'), ('minimal', 'foundations'),
                              ('minimal', 'results'), ('minimal', 'methods'),
                              ('minimal', 'boundaries')]:
            try:
                create_plan(project, 'unsupported', sid, profile=profile, view=view)
            except SurveyError as exc:
                if 'UNSUPPORTED' not in exc.diagnostic['code']:
                    raise AssertionError(f'Expected unsupported diagnostic: {exc}') from exc
                rejected.append(f'{profile}/{view}')
            else:
                raise AssertionError(f'Unsupported mode was accepted: {profile}/{view}')
        after = {p.relative_to(project).as_posix(): p.read_bytes()
                 for p in project.rglob('*') if p.is_file()}
        if before != after:
            raise AssertionError('Unsupported request mutated the fixture')
        if any(p.is_dir() and p.name == 'reviews' for p in project.rglob('*')):
            raise AssertionError('Minimal fixture created a runtime review directory')
    return {'status': 'PASSED', 'runtime_members': len(files),
            'checked_documentation_links': checked_links,
            'profile_preparations_executed': ['minimal'],
            'profile_view_preparations_executed': ['minimal-integrated'],
            'unsupported_requests_rejected': rejected,
            'python_3_10_grammar': 'parsed; not a Python 3.10 runtime test',
            'mathematical_certification': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    parser.parse_args()
    try:
        print(json.dumps(check(), indent=2))
    except Exception as exc:
        print(json.dumps({'status': 'FAILED', 'error': str(exc)}))
        raise SystemExit(2)
