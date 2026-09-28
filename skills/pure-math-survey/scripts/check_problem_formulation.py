#!/usr/bin/env python3
"""Validate a considered problem model and its located TeX evidence.

This checks a recorded model, dependency order and exact source bindings, NOT
mathematical truth, discovery completeness, reviewer independence or chronology.
The model lives inside the existing structure-review JSON, not a new registry.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROLES = {'fixed', 'fixed-class', 'reference', 'parameter', 'unknown', 'auxiliary'}
DECISIONS = {'in-scope', 'gauge', 'held-fixed', 'auxiliary', 'out-of-scope'}
RELATIONS = {'proved-equivalence', 'definitional-equivalence', 'proved-implication',
             'refuted', 'unresolved', 'unverified', 'not-selected'}
BINDING_ROLES = {'opening', 'answer', 'local-scope', 'body'}
PENDING = re.compile(r'\b(?:PENDING|TODO|TBD)\b|\[INSERT|\\placeholder', re.I)
LABEL = re.compile(r'\\label\s*\{([^{}]+)\}')


def filled(x) -> bool:
    return isinstance(x, str) and len(x.strip()) >= 12 and not PENDING.search(x)


def objects_list(value, name: str, errors: list[str]) -> list[dict]:
    if not isinstance(value, list) or not value or not all(isinstance(x, dict) for x in value):
        errors.append(name + ': expected a nonempty list of objects'); return []
    return value


def ids_list(value, allowed: set[str]) -> bool:
    return (isinstance(value, list) and all(isinstance(x, str) and x in allowed for x in value)
            and len(value) == len(set(value)))


def keyed(rows: list[dict], name: str, errors: list[str]) -> dict[str, dict]:
    out = {}
    for row in rows:
        key = row.get('id')
        if not isinstance(key, str) or not key or key in out:
            errors.append(name + ': missing or repeated id'); continue
        out[key] = row
    return out


def model_digest(model: dict) -> str:
    # Plan decisions, including the required destinations, are frozen separately
    # from post-authoring source excerpts and reader answers.
    core = {k: v for k, v in model.items() if k not in {'plan_sha256', 'bindings', 'reader_review'}}
    return hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def check_plan(model) -> list[str]:
    if not isinstance(model, dict):
        return ['PROBLEM_MODEL_ABSENT: complete problem_formulation before drafting']
    errors = []
    if model.get('schema_version') != '1.0.0':
        errors.append('problem_formulation schema_version must be 1.0.0')
    if model.get('status') != 'considered':
        errors.append('PROBLEM_NOT_CONSIDERED: scope decisions are pending')
    if not filled(model.get('selected_question')):
        errors.append('selected_question needs the actual mathematical question')
    obs = keyed(objects_list(model.get('objects'), 'objects', errors), 'objects', errors)
    for key, obj in obs.items():
        if not isinstance(obj.get('role'), str) or obj.get('role') not in ROLES:
            errors.append(key + ': invalid object role')
        for field in ('domain', 'meaning'):
            if not filled(obj.get(field)):
                errors.append(key + ': explain ' + field)
    context = model.get('fixed_context')
    if not ids_list(context, set(obs)):
        errors.append('fixed_context must identify distinct recorded objects'); context = []
    for key in context:
        if obs[key].get('role') not in ('fixed', 'fixed-class', 'reference'):
            errors.append('SILENT_FREEZE: variable object put into fixed_context: ' + key)
    variations = keyed(objects_list(model.get('variation_decisions'), 'variation_decisions', errors), 'variations', errors)
    for key, row in variations.items():
        if not isinstance(row.get('object'), str) or row.get('object') not in obs:
            errors.append(key + ': variation refers to an unknown object')
        if not isinstance(row.get('decision'), str) or row.get('decision') not in DECISIONS:
            errors.append(key + ': invalid variation decision')
        for field in ('candidate', 'admissible_domain', 'preserves', 'changes', 'reason'):
            if not filled(row.get(field)):
                errors.append(key + ': missing considered ' + field)
        if row.get('decision') == 'gauge' and not filled(row.get('equivalence_reason')):
            errors.append(key + ': gauge equivalence needs justification')
    questions = keyed(objects_list(model.get('questions'), 'questions', errors), 'questions', errors)
    for key, row in questions.items():
        if not filled(row.get('reading')) or not isinstance(row.get('binding'), str):
            errors.append(key + ': specify the question and its planned opening binding')
        prefix = objects_list(row.get('prefix'), key + '.prefix', errors)
        available = set(context)
        for q in prefix:
            obj = q.get('object')
            if not isinstance(obj, str) or obj not in obs or obj in available:
                errors.append(key + ': quantified object missing, repeated or already fixed'); continue
            if q.get('kind') not in ('forall', 'exists', 'exists-unique'):
                errors.append(key + ': invalid quantifier kind')
            if not isinstance(q.get('tex'), str) or not q.get('tex'):
                errors.append(key + ': missing displayed variable')
            if not filled(q.get('domain')):
                errors.append(key + ': quantifier has no explicit domain')
            if not ids_list(q.get('depends_on'), available):
                errors.append('FORWARD_DEPENDENCE: ' + key + '/' + obj)
            available.add(obj)
    relations = keyed(objects_list(model.get('relations'), 'relations', errors), 'relations', errors)
    for key, row in relations.items():
        if not ids_list(row.get('questions'), set(questions)) or not row.get('questions'):
            errors.append(key + ': relation must name existing question variants')
        if not isinstance(row.get('kind'), str) or row.get('kind') not in RELATIONS:
            errors.append(key + ': missing relation status')
        if not filled(row.get('justification')):
            errors.append('UNJUSTIFIED_RELATION: ' + key)
        if row.get('kind') in ('proved-equivalence', 'proved-implication'):
            if not filled(row.get('source_or_proof')) or not isinstance(row.get('answer_binding'), str):
                errors.append('UNJUSTIFIED_RELATION: locate the proof/source and main answer for ' + key)
    commitments = keyed(objects_list(model.get('commitments'), 'commitments', errors), 'commitments', errors)
    for key, row in commitments.items():
        if not filled(row.get('origin')) or not filled(row.get('content')):
            errors.append(key + ': identify actual user/input/scope content')
        if not isinstance(row.get('bindings'), list) or not row['bindings'] or not all(isinstance(x, str) for x in row['bindings']):
            errors.append('INPUT_COVERAGE: missing destination for ' + key)
    required = model.get('required_commitments')
    if not ids_list(required, set(commitments)) or set(required or []) != set(commitments):
        errors.append('INPUT_COVERAGE: required commitments must match the origin/destination records')
    local = model.get('local_scope_bindings')
    if not isinstance(local, list) or not all(isinstance(x, str) for x in local):
        errors.append('local_scope_bindings must list applicable local qualifications (empty is allowed)')
    for field in ('principal_answer', 'uniformity_policy', 'local_freezing_policy'):
        value = model.get(field)
        valid = isinstance(value, str) and bool(value) if field == 'principal_answer' else filled(value)
        if not valid:
            errors.append('missing ' + field)
    return errors


def _structure():
    p = Path(__file__).with_name('check_mathematical_structure.py')
    spec = importlib.util.spec_from_file_location('scope_structure', p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def tex_normalize(value: str) -> str:
    value = re.sub(r'\\(?:,|;|:|!|quad\b|qquad\b| )', '', value)
    return re.sub(r'\s+', '', value)


def check_release(expanded: str, review: dict) -> list[str]:
    if not isinstance(review, dict):
        return ['problem review must be a JSON object']
    model = review.get('problem_formulation')
    errors = check_plan(model)
    if errors:
        return errors
    if model.get('plan_sha256') != model_digest(model):
        errors.append('STALE_PROBLEM_PLAN: scope decisions changed or were not checked')
    structure = _structure()
    inv = structure.inventory(expanded)
    if review.get('source_sha256') != inv['source_sha256']:
        errors.append('STALE_PROBLEM_SOURCE: expanded visible source differs from review')
    text = structure.strip_comments(expanded)
    body = text.split(r'\begin{document}', 1)[-1].split(r'\end{document}', 1)[0]
    labels = {}
    for m in LABEL.finditer(body):
        if m.group(1) in labels:
            errors.append('duplicate source label: ' + m.group(1))
        labels[m.group(1)] = (m.start(), m.end())
    result = next((r for r in inv['results'] if r['label'] == model['principal_answer']), None)
    if result is None or result['section_index'] != 0:
        errors.append('MAIN_ANSWER_PLACEMENT: principal answer must occur in the opening section')
    bindings = keyed(objects_list(model.get('bindings'), 'bindings', errors), 'bindings', errors)
    resolved = {}
    for key, row in bindings.items():
        role = row.get('role')
        if not isinstance(role, str) or role not in BINDING_ROLES:
            errors.append(key + ': invalid binding role'); continue
        start, end = row.get('start_label'), row.get('end_label')
        if not isinstance(start, str) or not isinstance(end, str) or start not in labels or end not in labels:
            errors.append('SCOPE_ANCHOR_MISSING: ' + key); continue
        lo, hi = labels[start][1], labels[end][0]
        if lo >= hi:
            errors.append('SCOPE_ANCHOR_ORDER: ' + key); continue
        quote = row.get('quote')
        if not filled(quote):
            errors.append(key + ': source binding needs a substantive exact excerpt'); continue
        segment = body[lo:hi]
        # Whitespace may change; wording/math may not silently change.
        needle = tex_normalize(quote); haystack = tex_normalize(segment)
        if haystack.count(needle) != 1:
            errors.append('SCOPE_TEXT_MISMATCH: ' + key); continue
        if role == 'opening' and result and hi > result['start']:
            errors.append('LATE_SCOPE_REPAIR: ' + key + ' is not wholly before the principal answer')
        if role == 'answer' and result:
            result_text = tex_normalize(body[result['start']:result['end']])
            if needle not in result_text:
                errors.append('ANSWER_SCOPE_MISMATCH: ' + key + ' must be stated in the organizing main result')
        resolved[key] = row
    for q in model['questions']:
        row = resolved.get(q['binding'])
        if row is None or row['role'] != 'opening':
            errors.append('QUESTION_NOT_OPENING: ' + q['id']); continue
        quote = tex_normalize(row['quote'])
        actual = re.findall(r'\\(forall|exists)(!)?', quote)
        kinds = [a + ('-unique' if b else '') for a, b in actual]
        expected = [p['kind'] for p in q['prefix']]
        if kinds != expected:
            errors.append('QUANTIFIER_ORDER: ' + q['id']); continue
        cursor = 0
        for quant in q['prefix']:
            token = '\\' + quant['kind'].replace('-unique', '!') + tex_normalize(quant['tex'])
            pos = quote.find(token, cursor)
            if pos < 0:
                errors.append('QUANTIFIER_VARIABLE: ' + q['id']); break
            cursor = pos + len(token)
    for rel in model['relations']:
        if rel['kind'] in {'proved-equivalence', 'proved-implication'}:
            row = resolved.get(rel.get('answer_binding'))
            if row is None or row['role'] != 'answer':
                errors.append('RELATION_NOT_ANSWERED: ' + rel['id'])
    for obligation in model['commitments']:
        if any(b not in resolved for b in obligation['bindings']):
            errors.append('INPUT_COVERAGE: ' + obligation['id'])
    for key in ('problem_reading', 'distinctions_reading', 'dependency_reading'):
        rr = model.get('reader_review', {})
        if not isinstance(rr, dict) or not filled(rr.get(key)):
            errors.append('PROBLEM_READING_MISSING: ' + key)
    for binding in model['local_scope_bindings']:
        if binding not in resolved or resolved[binding]['role'] != 'local-scope':
            errors.append('LOCAL_SCOPE_MISSING: ' + binding)
    return errors


def load_review(root: Path, doc: dict) -> dict:
    value = doc.get('structure_review')
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('missing or unsafe structure_review path')
    path = root / value
    if Path(value).is_absolute() or '..' in Path(value).parts or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('structure_review escapes project')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('structure_review must be an object')
    return data


def validate_document(root: Path, doc: dict, expanded: str) -> list[str]:
    try:
        return check_release(expanded, load_review(root, doc))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return ['problem formulation review unavailable: ' + str(exc)]


def main() -> int:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from survey_core.adapters import dispatch
    native = dispatch('check_problem_formulation.py', sys.argv[1:])
    if native is not None: return native
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--stage', choices=('plan', 'release'), default='release')
    args = parser.parse_args(); root = args.project.resolve()
    errors, reports = [], []
    try:
        manifest = json.loads((root / 'project-manifest.json').read_text(encoding="utf-8-sig"))
        docs = manifest['documents']
        if not isinstance(docs, list) or not docs:
            raise ValueError('manifest documents must be a nonempty list')
        for doc in docs:
            if not isinstance(doc, dict):
                raise ValueError('document entries must be objects')
            review = load_review(root, doc); model = review.get('problem_formulation')
            found = check_plan(model)
            if args.stage == 'release' and not found:
                from validate_project import expand_tex, checked_path
                p = checked_path(root, doc['tex_file'], 'entrypoint', errors)
                if p is None:
                    continue
                expanded, _ = expand_tex(p, root, errors)
                found.extend(check_release(expanded, review))
            reports.append({'document': doc.get('tex_file'), 'errors': found,
                            'model_sha256': model_digest(model) if isinstance(model, dict) else None})
            errors.extend(found)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(str(exc))
    print(json.dumps({'stage': args.stage, 'status': 'PASS' if not errors else 'FAIL',
                      'documents': reports, 'errors': errors,
                      'limitation': 'Schema, dependencies and located evidence only; not mathematical certification.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
