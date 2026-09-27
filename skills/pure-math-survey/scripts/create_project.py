#!/usr/bin/env python3
"""Create an explicitly selected, unverified scaffold; never overwrite a project."""
from __future__ import annotations
import argparse
import csv
import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEMS = {1: 'foundations', 2: 'results', 3: 'methods', 4: 'boundaries', 5: 'integrated'}


def length_settings():
    spec = importlib.util.spec_from_file_location("pms_length_settings", ROOT / "scripts/check_reading_budget.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_selection(value: str) -> list[tuple[int, str]]:
    if value == 'suite':
        return [(p, 'concise') for p in STEMS]
    if value == 'all':
        return [(p, e) for p in STEMS for e in ('concise', 'standard')]
    result = []
    for raw in value.split(','):
        match = re.fullmatch(r'([1-5]):(concise|standard)', raw.strip())
        if not match:
            raise ValueError('Use a selection such as 5:standard, a comma-separated list, suite, or all.')
        item = (int(match.group(1)), match.group(2))
        if item in result:
            raise ValueError('Repeated part/edition selection.')
        result.append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--topic', required=True)
    parser.add_argument('--documents', default='5:concise', help='Default 5:concise; suite gives I–V concise; all explicitly gives ten.')
    parser.add_argument('--max-pages', type=int, help='Explicit user maximum for each selected PDF, including references; no maximum is set by default.')
    args = parser.parse_args()
    if args.max_pages is not None and args.max_pages < 1:
        parser.error('--max-pages must be positive')
    lengths = length_settings()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.topic):
        parser.error('Topic must be a lowercase alphanumeric filename slug separated by hyphens.')
    try:
        selection = parse_selection(args.documents)
    except ValueError as exc:
        parser.error(str(exc))
    out = args.output.expanduser().resolve()
    if out == ROOT or out.is_relative_to(ROOT):
        parser.error('Destination must be outside the skill.')
    if out.exists():
        parser.error('Destination already exists; no files were overwritten.')
    out.mkdir(parents=True)
    documents = []
    for part, edition in selection:
        name = f'part{part}-{STEMS[part]}-{edition}'
        stem = f'{args.topic}-{name}'
        shutil.copy2(ROOT / 'assets/templates' / (name + '.tex'), out / (stem + '.tex'))
        documents.append({'part': part, 'edition': edition, 'tex_file': stem + '.tex', 'pdf_file': stem + '.pdf', 'page_review_threshold': (lengths.CONCISE if edition == 'concise' else lengths.STANDARD)[part]})
    if args.max_pages is not None:
        for doc in documents:
            doc['max_pages'] = args.max_pages
    (out / 'evidence').mkdir()
    for doc in documents:
        review_path = 'evidence/' + Path(doc['tex_file']).stem + '-structure-review.json'
        doc['structure_review'] = review_path
        (out / review_path).write_text(json.dumps({'schema_version':'1.1.0', 'tex_file':doc['tex_file'], 'source_sha256':'PENDING', 'reviewer_mode':'PENDING', 'reviewed_on':'PENDING', 'sections':[], 'results':[], 'problem_formulation':json.loads((ROOT/'assets/problem-formulation-template.json').read_text(encoding="utf-8-sig")), 'survey_selection':json.loads((ROOT/'assets/survey-selection-template.json').read_text(encoding="utf-8-sig"))}, indent=2) + '\n', encoding="utf-8")
    shutil.copy2(ROOT / 'assets/templates/math-review.sty', out / 'math-review.sty')
    manifest = {'schema_version': '1.0.0', 'skill_version': '1.8.1', 'language': 'en', 'topic': args.topic,
                'literature_cutoff': '[Set from actual source verification]',
                'requested_documents': [{'part': p, 'edition': e} for p, e in selection],
                'documents': documents}
    (out / 'project-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding="utf-8")
    names = ['bibliographic-identity', 'proof-mechanism-registry', 'publication-map']
    if any(p in (4, 5) for p, _ in selection):
        names += ['frontier-claim-registry', 'frontier-reverse-search']
    for name in names:
        with (ROOT / f'assets/registries/{name}-template.csv').open(newline='', encoding='utf-8') as f:
            header = next(csv.reader(f))
        with (out / (name + '.csv')).open('w', newline='', encoding='utf-8') as f:
            csv.writer(f, lineterminator='\n').writerow(header)
    shutil.copy2(ROOT / 'assets/registries/release-audit-template.csv', out / 'release-audit.csv')
    (out / 'architecture.md').write_text(
        '# Unverified draft architecture\n\nRecord the actual task, scope, selected documents and sources.\n'
        'First reconstruct definitions and meaningful variation domains; classify intrinsic data, representatives and gauges.\n'
        'Complete problem_formulation in the existing reader evidence and run the plan check before drafting.\n'
        'Put the selected domains and quantified questions before answers; justify relationships instead of assuming them.\n'
        'Track input/user commitments and local freezes separately; a late scope corollary is not a repair.\n'
        'Identify organizing questions and principal conclusions before local refinements.\n'
        'Discover domain-native frontier candidates before freezing the bibliography; challenge omissions from primary sources.\n'
        'Classify results by question-relative importance; record roles and consumers in the publication map.\n'
        'Complete survey_selection in the same reader evidence; distinguish actual searches from source reads.\n'
        'Review the advisory reading-length threshold; set max_pages only for an explicit user limit. Retain core results and necessary proof inputs.\n'
        'Map each principal body result to its substantive Introduction statement.\n'
        'Record Introduction-only reading, hypothesis consistency and actual verification.\n'
        'Draft each body task as local definitions, usable results, necessary inputs, and proof/source treatment before prose.\n'
        'In each section record expected_result_labels, self_containment_reading, and unstructured_claims_reading.\n'
        'Review body-result reference_review entries for actual reader access, not a ban on references.\n'
        'Read the entire body statement-only and then by proof dependencies; do not treat a build as writing approval.\n'
        'Concise retains that structure; standard deepens proof interiors. Evidence starts pending.\n'
        'These are pending tasks, not completed research or PASS evidence.\n', encoding="utf-8")
    (out / 'README.md').write_text(
        '# Unverified survey scaffold\n\nReplace all insertion text and metadata with actual mathematics.\n'
        'No research, PDF, source sample or completed verification is supplied.\n'
        'The Introduction must state the actual main conclusions, not a roadmap.\n'
        'Read the skill validation contract before publishing.\n', encoding="utf-8")
    print(f'Created {len(documents)} unverified template source(s): {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
