"""Minimal-only transition policy; schema 3 and v22 layout follow in later stages."""
from __future__ import annotations
import re
from .common import RUNTIME_CONTRACT, diagnostic, require

OUTPUT_SCHEMA = '2.2.0'
POLICY = 'minimal-transition-pr02'
POLICIES = {OUTPUT_SCHEMA: (POLICY,)}
SUPPORTED_CONTRACTS = {(OUTPUT_SCHEMA, POLICY)}
PROFILES = {'minimal'}
MINIMAL_SECTIONS = ['Main Results', 'Key Mathematical Ingredients', 'Connecting the Ingredients']
VIEW_TASKS = {'integrated': 'Explain each selected module briefly: its input, mathematical operation, output and actual next use.'}


def mapping(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def filled(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def supported_contract(version: object, name: object) -> bool:
    return isinstance(version, str) and isinstance(name, str) and (version, name) in SUPPORTED_CONTRACTS


def validate_plan_contract(plan: dict) -> None:
    require(isinstance(plan, dict), 'CONTRACT_INVALID', 'Output plan must be an object', 'plan.json')
    require(plan.get('runtime_contract') == RUNTIME_CONTRACT, 'LEGACY_PROJECT_UNSUPPORTED',
            'Output belongs to an unsupported runtime contract; use a new project', 'plan.json')
    require(plan.get('profile') == 'minimal', 'PROFILE_UNSUPPORTED', 'Only minimal is supported', 'plan.json')
    require(plan.get('view') == 'integrated', 'VIEW_UNSUPPORTED', 'Only the fixed integrated view is supported', 'plan.json')
    require(plan.get('schema_version') == OUTPUT_SCHEMA, 'SCHEMA_UNSUPPORTED', 'Unsupported output schema', 'plan.json')
    require(supported_contract(plan.get('schema_version'), plan.get('editorial_policy')), 'EDITORIAL_POLICY_UNSUPPORTED',
            'Unsupported output policy; no automatic migration', 'plan.json')
    retired = {'draft', 'proof_obligations', 'contributions', 'comparison_group'} & plan.keys()
    require(not retired, 'CONTRACT_INVALID', 'Retired plan fields: ' + ', '.join(sorted(retired)), 'plan.json')
    for selection in plan.get('selections', []):
        require(isinstance(selection, dict) and 'proof_treatment' not in selection,
                'CONTRACT_INVALID', 'Selections describe use, not proof promises', 'plan.json')


def policy(plan: dict) -> str:
    validate_plan_contract(plan)
    return plan['editorial_policy']


def strict_minimal(plan: dict) -> bool:
    validate_plan_contract(plan)
    return plan['profile'] == 'minimal'


def structure_errors(inv, plan: dict, nodes: dict, expanded: str) -> tuple[list[dict], list[dict]]:
    """Preserve literal statement/section protections, without semantic approval."""
    validate_plan_contract(plan)
    errors = []; sections = inv['sections']; numbered = [s for s in sections if not s['starred']]
    def add(code, message, key=None):
        errors.append(diagnostic(code, message, 'manuscript/main.tex', key))
    if [s['title'] for s in numbered] != MINIMAL_SECTIONS:
        add('MINIMAL_THREE_SECTIONS_REQUIRED', 'Use the transition template three ordered body sections: ' + ' / '.join(MINIMAL_SECTIONS))
    if any(s['starred'] and s['title'].strip().lower() not in {'references', 'bibliography'} for s in sections):
        add('MINIMAL_EXTRA_BODY_SECTION', 'Only a bibliography may sit outside the three main sections')
    if sections and sections[0]['title'] != MINIMAL_SECTIONS[0]:
        add('MINIMAL_RESULTS_FIRST', 'Begin with Main Results')
    if re.search(r'\\(?:setcounter|addtocounter)\s*\{(?:secnumdepth|section)\}|\\appendix\b', expanded):
        add('MINIMAL_NUMBERING_UNSUPPORTED', 'Keep normal numbered sections')
    body=inv['body_text']; first=sections[0] if sections else None
    if re.search(r'\\(?:begin|end)\s*\{abstract\}', body):
        add('PROFILE_ABSTRACT_FORBIDDEN', 'Put brief problem positioning in Main Results')
    prefix=body[:first['start']] if first else body
    prefix=re.sub(r'\\(?:maketitle|noindent|par|smallskip|medskip|bigskip)\b', '', prefix)
    if prefix.strip():
        add('PROFILE_PRESECTION_TEXT_FORBIDDEN', 'Begin Main Results directly after the title')
    from .tex import visible_source
    for selection in plan['selections']:
        if selection['role'] != 'principal_answer': continue
        key=selection['node_id']; statement=visible_source(nodes[key].statement.decode('utf-8')).strip()
        found=[r for r in inv['results'] if statement and statement in r['text']]
        if not found:
            add('PRINCIPAL_RESULT_ENVIRONMENT_MISSING', 'Include each full principal in a numbered result environment', key)
        elif not any(r['section_index'] == 0 for r in found):
            add('MINIMAL_PRINCIPAL_NOT_FIRST', 'Place each principal in Main Results', key)
    return errors, []


def outline(plan: dict, order: list[str], nodes: dict | None = None) -> str:
    return '\n'.join(['# Minimal writing notes', '', 'Snapshot: '+plan['snapshot_id'],
        'Policy: '+POLICY+' (transition template; final v22 layout is not implemented yet).',
        '', 'Use canonical statements from generated/. Explain only selected modules and their actual combinations.',
        'Keep conditions and source version/locator adjacent to each borrowed claim. Record limits honestly.',
        '', 'Selected nodes:', *['- [['+key+']]' for key in order], ''])
