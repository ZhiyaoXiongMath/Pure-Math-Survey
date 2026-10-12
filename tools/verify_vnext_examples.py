#!/usr/bin/env python3
"""Reproduce authored known-mathematics examples; NEVER create accepted reviews.

Stored author readings concern exact source bytes. New PDFs are build evidence,
not newly observed pages. An original-research Paper is intentionally absent.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def verify(examples: Path, destination: Path, skill: Path, build: bool = True, report: dict | None = None) -> dict:
    if destination.exists():
        raise FileExistsError('Use a new output directory; historical evidence is not overwritten.')
    sys.path.insert(0, str(skill / 'scripts'))
    from survey_core.common import SurveyError, sha
    from survey_core.models import load_plan
    from survey_core.snapshots import verify_snapshot
    from survey_core.exports import validate_structure, output_inputs
    from survey_core.reviews import load_review, check_review_bindings
    from survey_core.release import semantic_scope_errors, package_output
    from survey_core.readiness import assess_readiness
    from survey_core.build import build_output, render_output
    import survey_core
    if not Path(survey_core.__file__).resolve().is_relative_to(skill.resolve()):
        raise RuntimeError('Runtime was imported from outside the requested installation.')
    report = report if report is not None else {}
    report.update({'status': 'PASS', 'runtime': str(Path(survey_core.__file__).resolve()),
              'original_paper_quality': 'NOT VERIFIED: no authorized original theorem',
              'independent_review': 'NOT VERIFIED', 'real_reader_feedback': 'NOT VERIFIED',
              'new_pdf_visual_review': 'NOT PERFORMED', 'outputs': [], 'snapshots_verified': 0})
    shutil.copytree(examples, destination)
    for name in ('schur', 'compactness'):
        project = destination / name
        for snapshot in sorted((project / 'snapshots').glob('KB-*')):
            verify_snapshot(project, snapshot.name)
            report['snapshots_verified'] += 1
        for path in sorted((project / 'outputs').glob('*/plan.json')):
            plan = load_plan(path); oid = plan['output_id']; out = path.parent
            # This is the fixed historical rc1 regression suite. New rc2
            # outputs are checked separately by verify_rc2_examples.py.
            if plan['schema_version'] == '2.2.0':
                continue
            structure = validate_structure(project, oid)
            if structure['errors']: raise AssertionError(structure['errors'])
            ready = assess_readiness(project, plan)
            review = load_review(out / 'evidence/author-semantic.json')
            binding = check_review_bindings(out, review, output_inputs(out))
            semantic = semantic_scope_errors(out, plan, ready['artifacts']['consumed_nodes'], review)
            row = {'project': name, 'profile': plan['profile'], 'output_id': oid,
                   'readiness': ready['status'], 'structure': structure['status'],
                   'stored_author_review': review['disposition'],
                   'statement_sha256': sha((out / 'generated/statements/N-main.tex').read_bytes())}
            if plan['profile'] == 'paper':
                if ready['status'] != 'NEEDS_WORK' or review['disposition'] == 'accepted':
                    raise AssertionError('Classical draft was relabeled original research.')
                try: package_output(project, oid, destination / 'forbidden-paper.zip')
                except SurveyError as exc:
                    if exc.diagnostic['code'] != 'DRAFT_NOT_RELEASABLE': raise
                else: raise AssertionError('Unverified Paper was formally packaged.')
                row['formal_release'] = 'BLOCKED'; row['draft_gate_codes'] = [e['code'] for e in ready['errors']]
            else:
                if ready['status'] != 'READY' or binding or semantic or review['disposition'] != 'accepted':
                    raise AssertionError({'readiness': ready['errors'], 'bindings': binding, 'semantic': semantic})
                row['semantic_evidence'] = 'Existing actual author reread, exact source binding verified'
            report['outputs'].append(row)
            if build:
                row['build'] = 'RUNNING'
                built = build_output(project, oid)
                if built['status'] != 'BUILT': raise AssertionError(built)
                rendered = render_output(project, oid, dpi=100)
                row.update(build='BUILT', pages=built['artifacts']['pages'], render=rendered['status'],
                           visual_review='NOT PERFORMED on this new build')
            else: row['build'] = 'NOT EXECUTED (--no-build)'
    return report


def record_failure_artifacts(destination:Path,report:dict)->None:
    """Preserve real build failure location without replacing prior successful rows."""
    import hashlib
    artifacts=[]
    for path in sorted(destination.rglob('build-report.json')) if destination.exists() else []:
        if path.parent.name!='build':continue
        try:
            data=json.loads(path.read_text(encoding='utf-8'))
            log=path.parent/'main.log'
            artifacts.append({'report':str(path),'status':data.get('status'),
                'blocking_log_issues':data.get('blocking_log_issues',{}),'failure':data.get('failure'),
                'log':str(log) if log.is_file() else None,
                'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest() if log.is_file() else None})
        except (OSError,ValueError) as exc:artifacts.append({'report':str(path),'read_error':str(exc)})
    report['output_directory']=str(destination)
    report['failure_artifacts']=artifacts
    for row in report.get('outputs',[]):
        if row.get('build')=='RUNNING':row['build']='FAILED'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--examples', type=Path, default=ROOT/'examples/vnext/projects')
    parser.add_argument('--skill-root', type=Path, default=ROOT/'skills/pure-math-survey')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--no-build', action='store_true')
    args = parser.parse_args()
    report = {}
    try:
        verify(args.examples, args.output, args.skill_root, not args.no_build, report)
    except Exception as exc:
        report.update(status='FAIL', error=f'{type(exc).__name__}: {exc}')
        record_failure_artifacts(args.output.resolve(), report)
    text = json.dumps(report, indent=2, ensure_ascii=False)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True); args.report.write_text(text, encoding='utf-8')
    print(text, end='')
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__': raise SystemExit(main())
