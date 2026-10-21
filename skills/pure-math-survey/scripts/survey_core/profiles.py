"""Minimal rules.v22 policy with the lean runtime adaptation."""
from __future__ import annotations
import re
from .common import RUNTIME_CONTRACT, diagnostic, require

OUTPUT_SCHEMA = '3.0.0'
POLICY = 'minimal-rules-v22-lean-2.4.1'
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
    retired = {'snapshot_id','question_ids','prerequisites','omissions','reader_goals','draft', 'proof_obligations', 'contributions', 'comparison_group'} & plan.keys()
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
        add('MINIMAL_THREE_SECTIONS_REQUIRED', 'Use the three ordered body sections: ' + ' / '.join(MINIMAL_SECTIONS))
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
    prefix=re.sub(r'\\(?:raggedbottom|pmslayout|maketitle|noindent|par|smallskip|medskip|bigskip)\b', '', prefix)
    if prefix.strip():
        add('PROFILE_PRESECTION_TEXT_FORBIDDEN', 'Begin Main Results directly after the title')
    from .tex import visible_source
    for selection in plan['selections']:
        if selection['role'] != 'principal': continue
        key=selection['node_id']; statement=visible_source(nodes[key].statement.decode('utf-8')).strip()
        found=[r for r in inv['results'] if statement and statement in r['text']]
        if not found:
            add('PRINCIPAL_RESULT_ENVIRONMENT_MISSING', 'Include each full principal in a numbered result environment', key)
        elif not any(r['section_index'] == 0 for r in found):
            add('MINIMAL_PRINCIPAL_NOT_FIRST', 'Place each principal in Main Results', key)
    return errors, []


def outline(plan: dict, order: list[str], nodes: dict | None = None) -> str:
    return '\n'.join(['# Minimal writing notes', '', 'Live canonical knowledge; preparation records automatic input hashes.',
        'Policy: '+POLICY+'; six main pages, references start separately.',
        '', 'Use canonical statements from generated/. Explain only selected modules and their actual combinations.',
        'Keep conditions and source version/locator adjacent to each borrowed claim. Record limits honestly.',
        '', 'Selected nodes:', *['- [['+key+']]' for key in order], ''])


def layout_errors(out, scan) -> list[dict]:
    """Finite source checks for the supported template; page measurements come from TeX."""
    from .common import SKILL_ROOT, safe
    from .structure import strip_comments
    from .tex import visible_source
    errors=[]
    def add(message,path='manuscript/main.tex'):
        errors.append(diagnostic('MINIMAL_LAYOUT_INVALID',message,path))
    main=visible_source(safe(out,'manuscript/main.tex',True).read_text(encoding='utf-8'))
    document=re.search(r'\\documentclass\s*\[([^]]*)\]\s*\{amsart\}',main)
    if not document or '11pt' not in document[1].split(',') or 'twocolumn' in document[1]:
        add('Use the supported single-column 11pt amsart class')
    style=safe(out,'manuscript/math-review.sty',True)
    if style.read_bytes()!=(SKILL_ROOT/'assets/templates/math-review.sty').read_bytes():
        add('Keep the installed typography/measurement style unchanged; edit manuscript and graph layout','manuscript/math-review.sty')
    body=scan.text.split(r'\begin{document}',1)[-1].split(r'\end{document}',1)[0]
    if len(re.findall(r'\\pmslayout\b',body))!=1:
        add('Observe normal typography once with \\pmslayout after beginning the document')
    boundary=list(re.finditer(r'\\pmsmainend\b',body))
    if len(boundary)!=1:
        add('Use one \\pmsmainend boundary before the separate reference pages')
    else:
        tail=body[boundary[0].end():]
        if not re.search(r'\\bibliography\s*\{|\\begin\s*\{thebibliography\}',tail):
            add('References must follow \\pmsmainend on their own page')
        # The boundary is an actual main-page observation, not a free placement marker.
        tail=re.sub(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}','',tail,flags=re.S)
        tail=re.sub(r'\\(?:bibliographystyle|bibliography)\s*\{[^{}]*\}','',tail)
        if tail.strip():add('Only references may follow the main-page boundary')
    for path in sorted(scan.inputs):
        if not path.endswith('.tex'):continue
        raw=strip_comments(safe(out,path,True).read_text(encoding='utf-8'))
        if re.search(r'\\(?:resizebox|scalebox|twocolumn|tiny|scriptsize|footnotesize|small|baselinestretch|linespread|geometry|newgeometry)\b',raw):
            add('Preserve normal text/graph sizes, leading and margins; do not compress to meet the page limit',path)
        if re.search(r'\\(?:vspace|hspace)\*?\s*\{\s*-|\\(?:vskip|hskip)\s*-|\\(?:fontsize|baselineskip|textwidth|textheight|topmargin|oddsidemargin|evensidemargin|hoffset|voffset)\b|(?:^|[\[,])\s*(?:scale|xscale|yscale|transform shape)\s*(?:=|[,\]])',raw):
            add('Avoid negative layout spacing, custom font/geometry dimensions and whole-graph scaling',path)
        if re.search(r'\\(?:setcounter|addtocounter)\s*\{page\}|\\pagenumbering\b|PMS-(?:MAIN-PAGES|BODY-FONT|BASELINE|[A-Z]+-MARGIN)',raw):
            add('Preserve automatic page numbering and installed layout measurement markers',path)
    return errors
