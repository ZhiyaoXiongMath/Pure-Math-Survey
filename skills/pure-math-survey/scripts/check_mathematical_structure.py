#!/usr/bin/env python3
"""Check located result/proof evidence, NOT mathematical truth or prose quality.

Literal TeX inputs are expanded by validate_project. Unused preamble macros and
comments do not count as body results. Human readings remain mandatory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from datetime import date
from collections import Counter
from pathlib import Path, PurePosixPath

RESULTS = {'theorem', 'proposition', 'lemma', 'corollary'}
ROLES = {'principal-result', 'independent-result', 'technical-input', 'direct-consequence', 'boundary-result'}
TREATMENTS = {'full-proof', 'proof-sketch', 'quoted-input'}
LABEL = re.compile(r'\\label\s*\{([^{}]+)\}')
BEGIN = re.compile(r'\\begin\s*\{(theorem|proposition|lemma|corollary|proof|theoremrecall)\}')
SECTION = re.compile(r'\\section(\*)?\s*(?:\[[^\]]*\]\s*)?\{')
CITE = re.compile(r'\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^{}]+)\}')
REFERENCE = re.compile(r'\\(?:eqref|ref|pageref|nameref|autoref|cref|Cref)\s*\{([^{}]+)\}')
REFERENCE_ROLES = {'nearby-definition', 'standard-notation', 'prior-result', 'navigation', 'formula-repeated'}
PLACEHOLDER = re.compile(r'\\placeholder\b|\b(?:PENDING|TODO|TBD)\b|\[INSERT', re.I)


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        chars, slashes = [], 0
        for c in line:
            if c == '%' and slashes % 2 == 0:
                break
            chars.append(c)
            slashes = slashes + 1 if c == '\\' else 0
        lines.append(''.join(chars))
    return '\n'.join(lines)


def group_end(text: str, start: int) -> int:
    """Return the end of a braced argument whose opening brace is at start."""
    level = 0
    for i in range(start, len(text)):
        if text[i] in '{}':
            k = i - 1
            while k >= 0 and text[k] == '\\':
                k -= 1
            if (i - 1 - k) % 2:
                continue
            level += 1 if text[i] == '{' else -1
            if level == 0:
                return i + 1
    raise ValueError('unclosed braced section heading')


def inventory(expanded: str) -> dict:
    text = strip_comments(expanded)
    # Inventory numbers are offsets in the body, not source-file line claims.
    body = text.split(r'\begin{document}', 1)[-1].split(r'\end{document}', 1)[0]
    sections = []
    for m in SECTION.finditer(body):
        end = group_end(body, m.end()-1)
        title = body[m.end():end-1]
        lm = re.match(r'\s*\\label\s*\{([^{}]+)\}', body[end:])
        sections.append({'title': title, 'label': lm.group(1) if lm else '',
                         'starred': bool(m.group(1)), 'start': m.start(), 'heading_end': end})
    for i, sec in enumerate(sections):
        sec['index'] = i
        sec['end'] = sections[i+1]['start'] if i+1 < len(sections) else len(body)
    blocks = []
    for m in BEGIN.finditer(body):
        env = m.group(1)
        close = re.search(r'\\end\s*\{' + re.escape(env) + r'\}', body[m.end():])
        if not close:
            raise ValueError('unclosed ' + env + ' environment')
        end = m.end() + close.end()
        content = body[m.end():m.end()+close.start()]
        labels = LABEL.findall(content)
        sec = next((s for s in sections if s['start'] <= m.start() < s['end']), None)
        blocks.append({'environment':env, 'label': labels[0] if labels else '',
                       'labels':labels, 'section':sec['label'] if sec else '',
                       'section_index':sec['index'] if sec else -1,
                       'start':m.start(), 'end':end, 'text':content})
    return {'source_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'body_text':body,
            'sections':sections, 'results':[b for b in blocks if b['environment'] in RESULTS],
            'proofs':[b for b in blocks if b['environment']=='proof'],
            'recalls':[b for b in blocks if b['environment']=='theoremrecall'],
            'labels':LABEL.findall(body),
            'citation_keys':sorted({k.strip() for m in CITE.finditer(body) for k in m.group(1).split(',')}),
            'has_placeholder':bool(PLACEHOLDER.search(body)),
            'statement_reference_sites':[{'result':b['label'], 'section':b['section'],
                'targets':sorted({v.strip() for m in REFERENCE.finditer(b['text']) for v in m.group(1).split(',')})}
                for b in blocks if b['environment'] in RESULTS and REFERENCE.search(b['text'])]}


def shape_issues(inv: dict) -> list[str]:
    """A targeted regression screen, with no per-section or total result quota."""
    secs = inv['sections']
    if len(secs) < 2:
        return []
    first = secs[0]['index']
    introductory = [r for r in inv['results'] if r['section_index']==first]
    body = [r for r in inv['results'] if r['section_index'] > first]
    if introductory and not body:
        return ['BODY_RESULTS_ABSENT: introductory results exist, but the substantive body has no explicit result; a context-only or proof-only exception requires a located review.']
    return []


def _filled(value) -> bool:
    return (isinstance(value,str) and len(value.strip()) >= 12
            and not PLACEHOLDER.search(value) and value.strip().upper() not in {'PASS','VERIFIED','COMPLETE'})


def check_review(inv: dict, review: dict, tex_file: str) -> list[str]:
    errors = []
    if not isinstance(review, dict):
        return ['structure review must be a JSON object']
    schema = review.get('schema_version')
    current = schema == '1.1.0'
    if not isinstance(schema, str) or schema not in {'1.0.0', '1.1.0'}:
        errors.append('structure review schema_version must be 1.0.0 or 1.1.0')
    if review.get('tex_file') != tex_file:
        errors.append('structure review refers to a different TeX entrypoint')
    if review.get('source_sha256') != inv['source_sha256']:
        errors.append('STALE_STRUCTURE_REVIEW: expanded visible source changed or review is pending')
    if not isinstance(review.get('reviewer_mode'), str) or review.get('reviewer_mode') not in {'source-first-author-review','independent-review'}:
        errors.append('reviewer_mode must state author reread or actual independent review')
    try:
        value = review.get('reviewed_on', '')
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError('not an ISO date')
    except (ValueError, TypeError):
        errors.append('reviewed_on must be an actual ISO date')
    if inv['has_placeholder']:
        errors.append('UNRESOLVED_DRAFT: visible insertion text remains')
    section_rows = review.get('sections')
    result_rows = review.get('results')
    if not isinstance(section_rows,list) or not all(isinstance(x,dict) for x in section_rows):
        return errors + ['sections must be a list of section review objects']
    if not isinstance(result_rows,list) or not all(isinstance(x,dict) for x in result_rows):
        return errors + ['results must be a list of body-result review objects']
    labels = set(inv['labels'])
    if any(count > 1 for count in Counter(inv['labels']).values()):
        errors.append('DUPLICATE_LABELS: semantic labels must be unique in the expanded document')
    section_map = {}
    for row in section_rows:
        label = row.get('label')
        if not isinstance(label,str) or label in section_map:
            errors.append('duplicate or non-string section review label'); continue
        section_map[label]=row
    actual_sections=[s for s in inv['sections'] if current or not s['starred']]
    actual_sec_labels={s['label'] for s in actual_sections}
    if '' in actual_sec_labels:
        errors.append('each reviewed section, numbered or starred, needs a semantic label')
    if set(section_map)!=actual_sec_labels:
        errors.append('SECTION_COVERAGE: section review must match all actual author-written sections')
    first_index=actual_sections[0]['index'] if actual_sections else -1
    for s in actual_sections:
        row=section_map.get(s['label'],{})
        role=row.get('role')
        if not isinstance(role, str) or role not in {'introduction','results-and-mechanisms','context-only','proof-only'}:
            errors.append(f"{s['label']}: invalid section role")
        if role=='introduction' and s['index']!=first_index:
            errors.append(f"{s['label']}: body section cannot be relabelled introduction")
        for name in ('statement_reading','dependency_reading'):
            if not _filled(row.get(name)):
                errors.append(f"{s['label']}: {name} needs a substantive located answer")
        body_results=[r for r in inv['results'] if r['section']==s['label']]
        if role=='results-and-mechanisms' and not body_results:
            errors.append(f"{s['label']}: declared result section has no actual result")
        if isinstance(role, str) and role in {'context-only', 'proof-only'}:
            if body_results or not _filled(row.get('result_free_reason')):
                errors.append(f"{s['label']}: {role} needs a reason and must not hide actual results")
        if role == 'proof-only':
            target_labels = row.get('proved_result_labels')
            proof = next((b for b in inv['proofs'] if b['label'] == row.get('proof_label')
                          and b['section'] == s['label']), None)
            all_result_labels = {b['label'] for b in inv['results'] if b['label']}
            if (not isinstance(target_labels, list) or not target_labels
                    or not all(isinstance(x, str) and x in all_result_labels for x in target_labels)):
                errors.append(f"{s['label']}: proof-only must identify visible proved_result_labels")
            elif proof is None or not set(target_labels).issubset(
                    {x.strip() for m in REFERENCE.finditer(proof['text']) for x in m.group(1).split(',')}):
                errors.append(f"{s['label']}: proof-only needs a located proof referring to its targets")
        if current:
            expected = row.get('expected_result_labels')
            actual = [b['label'] for b in body_results]
            if (not isinstance(expected, list) or not all(isinstance(x, str) for x in expected)
                    or len(expected) != len(set(expected)) or set(expected) != set(actual)):
                errors.append(f"{s['label']}: EXPECTED_RESULT_COVERAGE: content-first labels differ from actual section results")
            for field in ('self_containment_reading', 'unstructured_claims_reading'):
                if not _filled(row.get(field)):
                    errors.append(f"{s['label']}: {field} needs a substantive located answer")
    body_results=[r for r in inv['results'] if r['section_index']>first_index]
    result_map={}
    for row in result_rows:
        label=row.get('label')
        if not isinstance(label,str) or not label or label in result_map:
            errors.append('duplicate or missing result review label'); continue
        result_map[label]=row
    actual_labels=[r['label'] for r in body_results]
    if len(actual_labels)!=len(set(actual_labels)) or '' in actual_labels:
        errors.append('body results require unique semantic labels')
    if set(result_map)!=set(actual_labels):
        errors.append('RESULT_COVERAGE: reviewed body labels must equal actual result labels, not just their count')
    proofs={p['label']:p for p in inv['proofs'] if p['label']}
    for r in body_results:
        label=r['label']; row=result_map.get(label,{})
        if row.get('environment')!=r['environment']:
            errors.append(f'{label}: reviewed environment differs from actual result')
        if not isinstance(row.get('logical_role'), str) or row.get('logical_role') not in ROLES:
            errors.append(f'{label}: missing valid logical role')
        for name in ('hypotheses','conclusion','statement_reading','dependency_reading'):
            if not _filled(row.get(name)):
                errors.append(f'{label}: {name} needs a substantive reviewer answer')
        if current:
            if not _filled(row.get('self_containment_reading')):
                errors.append(f'{label}: self_containment_reading needs a substantive located answer')
            refs = {x.strip() for m in REFERENCE.finditer(r['text']) for x in m.group(1).split(',')}
            ref_rows = row.get('reference_review')
            if (not isinstance(ref_rows, list) or not all(isinstance(x, dict) for x in ref_rows)):
                errors.append(f'{label}: reference_review must be a list')
            else:
                targets = [x.get('target') for x in ref_rows]
                if (not all(isinstance(x, str) for x in targets) or len(targets) != len(set(targets))
                        or set(targets) != refs):
                    errors.append(f'{label}: STATEMENT_REFERENCE_COVERAGE: review each literal statement reference')
                for ref in ref_rows:
                    if not isinstance(ref.get('role'), str) or ref.get('role') not in REFERENCE_ROLES or not _filled(ref.get('reason')):
                        errors.append(f'{label}: reference review needs its role and reader-access reason')
        local=row.get('local_context')
        if not isinstance(local,list) or not local or not all(isinstance(x,str) and x in labels for x in local):
            errors.append(f'{label}: local_context must locate existing definitions/notation')
        consumer=row.get('consumer')
        if not isinstance(consumer,str) or consumer not in labels:
            errors.append(f'{label}: consumer must locate an actual use or section')
        treatment=row.get('treatment')
        if not isinstance(treatment, str) or treatment not in TREATMENTS:
            errors.append(f'{label}: invalid proof treatment')
        keys=row.get('source_keys',[])
        if not isinstance(keys,list) or not all(isinstance(x,str) and x in inv['citation_keys'] for x in keys):
            errors.append(f'{label}: source_keys must occur in actual manuscript citations')
        if treatment=='quoted-input' and (not keys or not _filled(row.get('source_locator'))):
            errors.append(f'{label}: QUOTED_INPUT_WITHOUT_SOURCE: exact source and locator required')
        proof_label=row.get('proof_label','')
        if (isinstance(treatment, str) and treatment in {'full-proof','proof-sketch'}) or proof_label:
            p=proofs.get(proof_label) if isinstance(proof_label,str) else None
            if p is None:
                errors.append(f'{label}: PROOF_BOUNDARY_MISSING: no located proof environment')
            else:
                next_result=min([x['start'] for x in body_results if x['start']>r['start']] or [10**12])
                location = row.get('proof_location', 'adjacent')
                if location == 'deferred':
                    proof_targets = {x.strip() for m in REFERENCE.finditer(p['text']) for x in m.group(1).split(',')}
                    if (label not in proof_targets or treatment == 'quoted-input'
                            or not _filled(row.get('proof_location_reason'))):
                        errors.append(f'{label}: DEFERRED_PROOF_UNBOUND: identify the result in the proof heading/text and explain its placement')
                    # Do not infer an arbitrary later proof from proximity or count.
                    # The author must also give a visible forward locator near the result.
                    section = next((sec for sec in inv['sections'] if sec['index'] == r['section_index']), None)
                    end = min(next_result, section['end'] if section else next_result)
                    near = inv['body_text'][r['end']:end]
                    near_refs = {x.strip() for m in REFERENCE.finditer(near) for x in m.group(1).split(',')}
                    if p['label'] not in near_refs and (not p['section'] or p['section'] not in near_refs):
                        errors.append(f'{label}: DEFERRED_PROOF_UNBOUND: place a visible proof/section locator after the result')
                elif location != 'adjacent':
                    errors.append(f'{label}: proof_location must be adjacent or deferred')
                elif not (r['end']<=p['start']<next_result) or p['section']!=r['section']:
                    errors.append(f'{label}: proof is not attached to this result in its section')
                title = re.match(r'\s*\[([^]]*)\]', p['text'])
                sketch = bool(title and re.search(r'\b(?:sketch|outline)\b', title.group(1), re.I))
                if treatment == 'full-proof' and sketch:
                    errors.append(f'{label}: PROOF_TREATMENT_MISMATCH: a printed sketch/outline is not a full proof')
                if treatment == 'proof-sketch' and not sketch:
                    errors.append(f'{label}: PROOF_TREATMENT_MISMATCH: label the printed proof as a sketch or outline')
                if treatment=='quoted-input' and not re.match(r'\s*\[(?:Construction outline|Explanation|Proof sketch|Quoted proof outline)',p['text']):
                    errors.append(f'{label}: quoted-input explanation must not masquerade as a full proof')
    # A purely expository/context-only body can be legitimate; it requires real
    # section-level reasons rather than a fixed theorem quota.
    body_sec=[section_map.get(s['label'],{}) for s in actual_sections if s['index']>first_index]
    context_exception=bool(body_sec) and all(isinstance(s.get('role'),str) and s.get('role') in {'context-only', 'proof-only'} and _filled(s.get('result_free_reason')) for s in body_sec)
    if not context_exception:
        errors.extend(shape_issues(inv))
    return errors


def validate_document(root: Path, tex_file: str, expanded: str, review_path: str, *, require_schema: str | None = None) -> tuple[list[str], dict]:
    inv=inventory(expanded)
    if not isinstance(review_path, str):
        return ['structure_review path must be a string'],inv
    p=PurePosixPath(review_path)
    if (not review_path or p.is_absolute() or '\\' in review_path or ':' in review_path
            or any(x in {'','..','.'} for x in review_path.split('/'))):
        return ['unsafe or missing structure_review path'],inv
    path=root/review_path
    if not path.resolve().is_relative_to(root.resolve()):
        return ['structure_review path escapes project'],inv
    try:
        review=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,ValueError) as exc:
        return [f'structure review unavailable: {exc}'],inv
    errors = check_review(inv,review,tex_file)
    if require_schema and (not isinstance(review, dict) or review.get('schema_version') != require_schema):
        errors.append(f'CURRENT_REVIEW_REQUIRED: this project requires structure review schema {require_schema}')
    return errors,inv


def public_inventory(inv: dict) -> dict:
    return {k:v for k,v in inv.items() if k not in {'labels','citation_keys','body_text'}} | {
        'results':[{k:v for k,v in r.items() if k!='text'} for r in inv['results']],
        'proofs':[{k:v for k,v in r.items() if k!='text'} for r in inv['proofs']],
        'recalls':[{k:v for k,v in r.items() if k!='text'} for r in inv['recalls']]}


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=Path)
    parser.add_argument('--tex',required=True)
    parser.add_argument('--review')
    parser.add_argument('--inventory',action='store_true',help='Print coordinates/digest only; NOT a completed review')
    args=parser.parse_args()
    from validate_project import expand_tex, checked_path
    errors=[]; root=args.project.resolve()
    p=checked_path(root,args.tex,'entrypoint',errors)
    if p is None:
        print('\n'.join(errors),file=sys.stderr);return 1
    try:
        text,_=expand_tex(p,root,errors); inv=inventory(text)
        if args.inventory:
            print(json.dumps(public_inventory(inv),indent=2));return 1 if errors else 0
        if args.review:
            new,_=validate_document(root,args.tex,text,args.review);errors.extend(new)
        else:
            errors.extend(shape_issues(inv))
            errors.append('LOCATED_REVIEW_REQUIRED: inventory/shape checks alone do not complete the reader review')
    except (OSError,ValueError,TypeError) as exc:
        errors.append(str(exc))
    for error in errors:print(error,file=sys.stderr)
    if errors:return 1
    print('BODY STRUCTURE EVIDENCE CHECKS PASSED; source-bound records, not mathematical or readability certification')
    return 0

if __name__=='__main__':raise SystemExit(main())
