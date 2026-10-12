"""Versioned exposition policy, not a mathematical decision procedure.

Knowledge remains schema 2.0.0. New plans and policy-bearing reviews use 2.1.0;
legacy plans are read without mutation and are never called vNext-reviewed.
All accepted findings below are accountable reader assertions, not inferred truth.
"""
from __future__ import annotations
from pathlib import Path
import re
from .common import diagnostic, require, sha, valid_date

OUTPUT_SCHEMA = '2.1.0'
POLICY = 'four-modes-2026-10-11-r2'
LEGACY_POLICY = 'legacy-2.0.0'
PROFILES = {'minimal', 'thematic', 'lecture', 'paper'}
MINIMAL_SECTIONS = ['Main Results', 'Key Mathematical Ingredients', 'Connecting the Ingredients']
STATEMENT_ASPECTS = ('objects', 'domain', 'fixed_and_variable', 'hypotheses',
                     'equations', 'quantifiers', 'conclusion', 'status', 'local_definitions')
COMMON_READINGS = ('fast_path', 'reader_calibration', 'points', 'connections',
                   'limits', 'display_rhythm', 'statement_context')
MODE_READINGS = {
    'minimal': ('results_first', 'point_use', 'decisive_connections'),
    'thematic': ('question_structure', 'approach_mechanisms', 'comparison_basis', 'synthesis'),
    'lecture': ('motivation', 'worked_derivations', 'hypothesis_use', 'imported_inputs', 'model_boundary'),
    'paper': ('contribution_position', 'prior_art', 'proof_closure', 'attribution'),
}
GOALS = {
    'minimal': 'Recover the full results, callable ingredients, and decisive mathematical connections.',
    'thematic': 'Explain the question, mechanisms, comparable hypotheses and supported synthesis of routes.',
    'lecture': 'Reproduce the promised constructions, estimates and limits, identifying each hypothesis and imported input.',
    'paper': 'Audit the proposed original contribution against closest prior results and its entire proof.',
}
PROOF_PROMPTS = {
    'minimal': 'PENDING: name the decisive input, mathematical operation, output, and condition closing the connection.',
    'thematic': 'PENDING: identify the route mechanism and the exact assumptions and normalization supporting comparison.',
    'lecture': 'PENDING: enumerate the actual intermediate calculations, uniform estimates, limits and hypothesis uses promised here.',
    'paper': 'PENDING: enumerate every substantive step closing this proof, with exact imported inputs and remaining gaps.',
}


def mapping(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def current(plan: dict) -> bool:
    return plan.get('schema_version') == OUTPUT_SCHEMA


def policy(plan: dict) -> str:
    return POLICY if current(plan) else LEGACY_POLICY


def filled(value: object) -> bool:
    return (isinstance(value, str) and bool(value.strip()) and
            not re.match(r'\s*(?:PENDING|TODO|TBD|REPLACE)(?:\b|_)', value, re.I))


def validate_plan_contract(plan: dict) -> None:
    """Schema checks only; an incomplete, explicitly draft plan is legal."""
    version = plan.get('schema_version')
    require(version in {'2.0.0', OUTPUT_SCHEMA}, 'SCHEMA_UNSUPPORTED', 'Unsupported output-plan schema', 'plan.json')
    if version == '2.0.0':
        require(plan.get('profile') in PROFILES - {'paper'}, 'SCHEMA_UNSUPPORTED',
                'Paper requires output schema 2.1.0; the legacy parser had only three profiles', 'plan.json')
        require('editorial_policy' not in plan and 'contributions' not in plan,
                'SCHEMA_UNSUPPORTED', 'Do not disguise new-policy fields as a legacy plan', 'plan.json')
        return
    require(plan.get('editorial_policy') == POLICY, 'EDITORIAL_POLICY_UNSUPPORTED', 'Explicit supported editorial policy required', 'plan.json')
    require(type(plan.get('contributions')) is list, 'CONTRACT_INVALID', '2.1.0 plans require contributions (empty outside Paper)', 'plan.json')
    if plan['profile'] != 'paper':
        require(not plan['contributions'], 'CONTRACT_INVALID', 'Contribution claims belong only to Paper', 'plan.json')
    seen = set()
    for item in plan['contributions']:
        require(isinstance(item, dict), 'CONTRACT_INVALID', 'Contribution must be an object', 'plan.json')
        for key in ('node_id', 'classification', 'provenance', 'authorization', 'actual_difference', 'proof_status'):
            require(type(item.get(key)) is str, 'CONTRACT_INVALID', f'Contribution {key} must be text', 'plan.json')
        for key in ('closest_prior_results', 'comparison_nodes', 'gaps'):
            require(type(item.get(key)) is list and all(type(x) is str and x.strip() for x in item[key]),
                    'CONTRACT_INVALID', f'Contribution {key} must be a text list', 'plan.json')
            require(len(item[key]) == len(set(item[key])), 'DUPLICATE_ID', f'Duplicate contribution {key}', 'plan.json')
        require(item['node_id'] not in seen, 'DUPLICATE_ID', 'Duplicate contribution claim', 'plan.json'); seen.add(item['node_id'])
        require(item['classification'] in {'original', 'known', 'conjectural', 'unverified'}, 'CONTRACT_INVALID', 'Invalid contribution classification', 'plan.json')
        require(item['proof_status'] in {'complete', 'incomplete', 'unverified'}, 'CONTRACT_INVALID', 'Invalid contribution proof_status', 'plan.json')


def validate_profile_selection(inv, plan: dict) -> None:
    validate_plan_contract(plan)
    if not current(plan):
        return
    selected = {s['node_id']: s for s in plan['selections']}
    available = set(selected) | {p['node_id'] for p in plan['prerequisites'] if isinstance(p, dict)}
    principals = {k for k, s in selected.items() if s['role'] == 'principal_answer'}
    if plan['profile'] == 'paper':
        require({c['node_id'] for c in plan['contributions']} == principals, 'CONTRIBUTION_COVERAGE_MISSING',
                'Classify every Paper principal, including borrowed or unverified claims', 'plan.json')
        for c in plan['contributions']:
            for key in c['closest_prior_results'] + c['comparison_nodes']:
                require(key in available and key in inv.nodes, 'CONTRIBUTION_INPUT_MISSING',
                        'Select or explicitly scope each prior-result/comparison node', 'plan.json', key)
            require(c['node_id'] not in c['closest_prior_results'], 'CONTRIBUTION_INVALID',
                    'A claim cannot be its own closest prior result', 'plan.json', c['node_id'])
            for key in c['comparison_nodes']:
                require(inv.nodes[key].meta['kind'] == 'relation', 'CONTRIBUTION_INVALID',
                        'Nontrivial comparisons must be canonical relation nodes, not unsourced outline prose', 'plan.json', key)


def principal_template(statement: bytes) -> dict:
    return {'canonical_sha256': sha(statement), 'outcome': 'not_performed',
            **{key: '' for key in STATEMENT_ASPECTS}}


def statement_errors(key: str, statement: bytes, review: dict) -> list[dict]:
    scope = mapping(review.get('scope'))
    entry = mapping(scope.get('statement_reviews')).get(key, {})
    valid = (review.get('schema_version') == OUTPUT_SCHEMA and scope.get('editorial_policy') == POLICY
             and isinstance(entry, dict) and entry.get('outcome') == 'accepted'
             and entry.get('canonical_sha256') == sha(statement)
             and all(filled(entry.get(k)) for k in STATEMENT_ASPECTS))
    return [] if valid else [diagnostic('PRINCIPAL_SELF_CONTAINED_REVIEW_PENDING',
        'Read this exact canonical claim in isolation: objects, domain, data/unknowns, hypotheses, equations, quantifiers, conclusion, status and local definitions; record actual findings.',
        'evidence', key)]


def statement_warnings(key: str, statement: bytes) -> list[dict]:
    text = statement.decode('utf-8')
    patterns = (r'\\(?:eqref|ref|autoref|cref|Cref)\s*\{',
                r'\b(?:as above|as before|above equation|standard positivity assumption)\b',
                r'\b(?:under|assume|assuming|satisfies|obeys|obtain)\s*\(?\s*(?:\d+\.\d+|H\d+)\b')
    return [diagnostic('STATEMENT_SELF_CONTAINED_RISK',
            'Principal statement contains a remote-reference/vague-condition candidate. This is an editorial warning, not a mathematical verdict; resolve in the statement reading or repair KB and freeze again.',
            f'generated/statements/{key}.tex', key)] if any(re.search(p, text, re.I) for p in patterns) else []


def profile_readiness_errors(inv, plan: dict) -> list[dict]:
    if not current(plan):
        return []
    errors = []
    def add(code, message, key=None):
        errors.append(diagnostic(code, message, 'plan.json', key))
    if any(not filled(s) for o in plan['proof_obligations'] for s in o['required_steps']):
        add('PROOF_OBLIGATION_UNMET', 'Replace generated proof prompts with actual node-grounded step promises before readiness.')
    for s in plan['selections']:
        if s['role'] == 'principal_answer' and inv.nodes[s['node_id']].meta['mathematical_status'] not in {'established', 'refuted'}:
            add('PRINCIPAL_STATUS_UNVERIFIED', 'An unassessed, open or conjectural principal is draft-only, not a proved main result.', s['node_id'])
    if plan['profile'] == 'lecture' and not any(o['treatment'] == 'complete' for o in plan['proof_obligations']):
        add('LECTURE_PROOF_PROMISE_MISSING', 'Lecture must teach actual promised derivations; imported inputs may remain external.')
    if plan['profile'] != 'paper':
        return errors
    originals = [c for c in plan['contributions'] if c['classification'] == 'original']
    if not originals:
        add('PAPER_ORIGINAL_CONTRIBUTION_MISSING', 'Known theorems or synthetic fixtures cannot establish an original research contribution.')
    selected = {s['node_id']: s for s in plan['selections']}
    obligations = {o['node_id']: o for o in plan['proof_obligations']}
    for c in plan['contributions']:
        key = c['node_id']; node = inv.nodes[key]
        if c['classification'] in {'conjectural', 'unverified'} or c['gaps']:
            add('PAPER_PROOF_GAP', 'Unverified claims and disclosed unresolved gaps remain internal-draft material.', key)
        if c['classification'] != 'original':
            continue
        if node.meta['origin'] not in {'local_derivation', 'supplied_manuscript'} or not filled(c['provenance']) or not filled(c['authorization']):
            add('PAPER_PROVENANCE_UNVERIFIED', 'Record actual authorized original derivation/manuscript provenance; borrowed results are not original.', key)
        if (c['proof_status'] != 'complete' or node.meta['mathematical_status'] != 'established'
                or selected[key]['proof_treatment'] != 'complete' or obligations.get(key, {}).get('treatment') != 'complete'):
            add('PAPER_PROOF_NOT_CLOSED', 'Each original principal requires an established node and its own complete proof obligation.', key)
        if not c['closest_prior_results'] or not c['comparison_nodes'] or not filled(c['actual_difference']):
            add('PAPER_PRIOR_ART_MISSING', 'Identify closest prior-result nodes, supported comparison relations and the precise difference.', key)
        # A proved original result cannot import a conjecture as a proof premise.
        # Discussion-only frontier selections are not proof dependencies.
        from .dependencies import required_closure
        proof_seeds = {key} | set(obligations.get(key, {}).get('imported_inputs', []))
        proof_ids = required_closure(inv.nodes, proof_seeds, proof_seeds)
        for dependency in proof_ids - {key}:
            dep = inv.nodes[dependency]
            if dep.meta['kind'] != 'question' and dep.meta['mathematical_status'] not in {'established', 'not_applicable'}:
                add('PAPER_PROOF_INPUT_UNVERIFIED', 'An original proof cannot depend on an open, refuted, conjectural or unassessed input.', dependency)
        if node.meta['origin'] == 'supplied_manuscript':
            sources = [inv.sources[x['source_id']] for x in node.meta['sources'] if x['role'] == 'provenance']
            if not any(x['kind'] == 'supplied_manuscript' and x['version'] and
                       x['access']['state'] == 'full_text_read' and x['access'].get('reading_note') and
                       valid_date(x['access'].get('checked_at')) for x in sources):
                add('PAPER_PROVENANCE_UNVERIFIED', 'A supplied original needs a versioned, actually read manuscript provenance record, not just authorization prose.', key)
        for prior in c['closest_prior_results']:
            n = inv.nodes[prior]
            if n.meta['mathematical_status'] != 'established' or not any(s['role'] == 'support' and inv.sources[s['source_id']]['kind'] == 'primary' for s in n.meta['sources']):
                add('PAPER_PRIOR_ART_MISSING', 'Closest prior results require established nodes and actual primary-source support.', prior)
    return errors


def review_scope_template(plan: dict) -> dict:
    if not current(plan):
        return {}
    keys = COMMON_READINGS + MODE_READINGS[plan['profile']]
    return {'editorial_policy': POLICY, 'statement_reviews': {},
            'mode_findings': {k: {'outcome': 'not_performed', 'finding': '', 'locations': []} for k in keys},
            'proof_step_findings': {o['node_id']: {s: {'outcome': 'not_performed', 'finding': '', 'locations': []}
                                    for s in o['required_steps']} for o in plan['proof_obligations']},
            'contribution_reviews': {c['node_id']: {'outcome': 'not_performed', 'finding': '', 'locations': [],
                'closest_prior_results': c['closest_prior_results'], 'prior_art_searches': [],
                'provenance_check': '', 'authorization_check': '', 'actual_difference': '',
                'proof_closure': '', 'remaining_caveats': ''}
                for c in plan['contributions'] if c['classification'] == 'original'}}


def semantic_profile_errors(out: Path, plan: dict, review: dict) -> list[dict]:
    if not current(plan):
        return []
    from .tex import validate_locations
    from .common import safe
    scope = mapping(review.get('scope')); errors = []
    if review.get('schema_version') != OUTPUT_SCHEMA or scope.get('editorial_policy') != POLICY:
        errors.append(diagnostic('EDITORIAL_REVIEW_POLICY_MISMATCH', 'Historical accepted evidence is not a new-policy reading.', 'evidence'))
    def check_entry(entry, name, key=None):
        if not isinstance(entry, dict) or entry.get('outcome') != 'accepted' or not filled(entry.get('finding')):
            errors.append(diagnostic('MODE_SEMANTIC_REVIEW_PENDING', f'Located substantive reading required: {name}', 'evidence', key))
            return
        errors.extend(validate_locations(out, entry.get('locations'), node_id=key))
    findings = mapping(scope.get('mode_findings'))
    for name in COMMON_READINGS + MODE_READINGS[plan['profile']]:
        check_entry(findings.get(name), name)
    for s in plan['selections']:
        if s['role'] == 'principal_answer':
            key = s['node_id']
            errors.extend(statement_errors(key, safe(out, f'generated/statements/{key}.tex', True).read_bytes(), review))
    step_findings = mapping(scope.get('proof_step_findings'))
    for obligation in plan['proof_obligations']:
        key = obligation['node_id']
        for step in obligation['required_steps']:
            check_entry(mapping(step_findings.get(key)).get(step), 'proof step: ' + step, key)
    if plan['profile'] == 'paper':
        for c in plan['contributions']:
            if c['classification'] != 'original':
                continue
            key = c['node_id']; entry = mapping(mapping(scope.get('contribution_reviews')).get(key))
            check_entry(entry, 'original contribution', key)
            required = ('provenance_check', 'authorization_check', 'actual_difference', 'proof_closure', 'remaining_caveats')
            searches = entry.get('prior_art_searches', [])
            valid_search = isinstance(searches, list) and bool(searches) and all(
                isinstance(s, dict) and valid_date(s.get('searched_at')) and filled(s.get('query'))
                and filled(s.get('outcome')) and isinstance(s.get('checked_source_ids'), list)
                and bool(s['checked_source_ids']) and all(isinstance(x, str) and x.startswith('S-') for x in s['checked_source_ids'])
                for s in searches)
            # The searched identities must be actual, snapshot-bound authoring source records.
            source_ids = {p.stem for p in (out/'materials').rglob('sources/S-*.json')}
            if valid_search:
                valid_search = all(set(s['checked_source_ids']) <= source_ids for s in searches)
            if (not all(filled(entry.get(k)) for k in required) or not valid_search
                    or entry.get('closest_prior_results') != c['closest_prior_results']):
                errors.append(diagnostic('PAPER_CONTRIBUTION_REVIEW_PENDING',
                    'Record actual dated prior-art searches against bound sources, closest results, authorization, precise difference, proof closure and caveats. Software cannot establish novelty.', 'evidence', key))
    return errors


def structure_errors(inv, plan: dict, nodes: dict, expanded: str) -> tuple[list[dict], list[dict]]:
    if not current(plan):
        return [], [diagnostic('LEGACY_EDITORIAL_POLICY', 'Only the historical 2.0.0 policy is being checked; this is not vNext acceptance.')]
    errors = []; warnings = []
    sections = inv['sections']; numbered = [s for s in sections if not s['starred']]
    if plan['profile'] == 'minimal':
        if [s['title'] for s in numbered] != MINIMAL_SECTIONS:
            errors.append(diagnostic('MINIMAL_THREE_SECTIONS_REQUIRED', 'Use exactly the three ordered numbered main sections: ' + ' / '.join(MINIMAL_SECTIONS), 'manuscript/main.tex'))
        # A fourth unnumbered mathematical section is not a bibliography escape.
        if any(s['starred'] and s['title'].strip().lower() not in {'references', 'bibliography'} for s in sections):
            errors.append(diagnostic('MINIMAL_EXTRA_BODY_SECTION', 'Only a bibliography may sit outside the three main sections.', 'manuscript/main.tex'))
        if sections and sections[0].get('title') != MINIMAL_SECTIONS[0]:
            errors.append(diagnostic('MINIMAL_RESULTS_FIRST', 'Do not put background or a bibliography before Main Results.', 'manuscript/main.tex'))
        if re.search(r'\\(?:setcounter|addtocounter)\s*\{(?:secnumdepth|section)\}', expanded) or re.search(r'\\appendix\b', expanded):
            errors.append(diagnostic('MINIMAL_NUMBERING_UNSUPPORTED', 'Do not suppress or reset the three main section numbers; use normal article numbering.', 'manuscript/main.tex'))
    for selection in plan['selections']:
        if selection['role'] != 'principal_answer':
            continue
        key = selection['node_id']; statement = nodes[key].statement
        warnings.extend(statement_warnings(key, statement))
        from .tex import visible_source
        visible_statement = visible_source(statement.decode('utf-8')).strip()
        candidates = [r for r in inv['results'] if visible_statement and visible_statement in r['text']]
        if not candidates:
            errors.append(diagnostic('PRINCIPAL_RESULT_ENVIRONMENT_MISSING', 'Put the full principal canonical input in a theorem/proposition/corollary/lemma environment.', 'manuscript/main.tex', key))
        elif plan['profile'] == 'minimal' and not any(r['section_index'] == 0 for r in candidates):
            errors.append(diagnostic('MINIMAL_PRINCIPAL_NOT_FIRST', 'Every principal belongs in Main Results, independently of view.', 'manuscript/main.tex', key))
    if plan['profile'] == 'paper' and not plan['draft'] and re.search(r'DRAFT(?:\\)?_UNVERIFIED', inv['body_text']):
        errors.append(diagnostic('PAPER_DRAFT_NOTICE_REMAINS', 'Resolve all draft conditions before explicitly promoting and rereviewing a Paper.', 'manuscript/main.tex'))
    return errors, warnings


def outline(plan: dict, order: list[str]) -> str:
    """Preparation proposes a reading task; it deliberately leaves work pending."""
    section_plans = {
        'minimal': '\n'.join(f'{i}. {title}' for i, title in enumerate(MINIMAL_SECTIONS, 1)),
        'thematic': 'Questions and principal results -> structural difficulty -> actual approach(es) -> supported comparison and synthesis. Do not invent a second route.',
        'lecture': 'Early goal theorem -> needed prerequisites/model -> construction -> worked lemmas/estimates -> closed promised proof -> useful boundary example. Titles and section count are editable.',
        'paper': 'Contributions and closest prior work -> new mechanism -> complete proofs -> justified consequences. Research-note or longer article structures are equally valid.',
    }
    lines = ['# Exposition Contract', '', f'Mode: {plan["profile"]}', f'Editorial policy: {policy(plan)}',
             f'Fixed snapshot: {plan["snapshot_id"]}', '', '## Target and reader', plan['audience'],
             GOALS[plan['profile']], 'Questions: ' + ', '.join(plan['question_ids']),
             'Principals: ' + ', '.join(s['node_id'] for s in plan['selections'] if s['role'] == 'principal_answer'),
             '', 'PENDING: specify what this topic-specific reader can DO; classify only used inputs as Assumed / Refreshable / Bridge-required, with reasons.',
             '', '## Points and decisive connections',
             'PENDING: choose the minimal useful points from the nodes below. For each give its exact input, output and actual consumer; do not copy canonical statements into this outline.',
             'PENDING: work backward from the result, then forward from the reader. Locate the real construction/estimate/variable change, its hypotheses and next input. Distinguish conjunctive premises, alternatives, branches and gaps.',
             '', 'Candidate nodes (dependency order is not automatically teaching order):',
             *['- [['+k+']]' for k in order], '', '## Proof obligations and imported inputs',
             *[f'- {o["node_id"]}: {o["treatment"]}; steps: {"; ".join(o["required_steps"])}; imported: {", ".join(o["imported_inputs"]) or "none declared"}' for o in plan['proof_obligations']],
             'PENDING: locate each promised detail in the planned manuscript; retain uniform constants, topology, admissibility, noncollapse and regularity in the fast route when decisive.',
             '', '## Mode-specific section plan', section_plans[plan['profile']],
             '', '## Limits and statement concerns',
             'PENDING: identify unproved/uncalled branches and exact node sections for slow reading. Inspect each principal alone and its neighboring prose; repair deficient canonical statements in KB, review and freeze a new snapshot.',
             '', '## Reading rhythm',
             'Prefer short prose alternating with mathematically useful displays. About four TYPESet lines is an editorial heuristic, never a source-line count, formula quota or permission to drop hypotheses.',
             '', '## Review boundary',
             'No semantic, originality, reader-comprehension or page review was performed by prepare. Project overview may cover many questions and routes; this outline selects just this manuscript.']
    if plan['profile'] == 'paper':
        lines += ['', '## Contribution contract',
                  'PENDING: audit every plan contribution against authorized provenance, closest verified prior results, supported difference, complete proof and caveats. No closed original contribution: DRAFT_UNVERIFIED only.']
    return '\n'.join(lines) + '\n'
