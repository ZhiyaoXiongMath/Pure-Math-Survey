"""Ephemeral exposition-design checks; neither a KB gate nor a new authority.

Only known unfinished instructions and invalid references are mechanically
checked. Completing them does not establish mathematical quality or readability.
"""
from __future__ import annotations
from pathlib import Path
import re
from .common import diagnostic, safe

DEFAULT_AUDIENCE = ('[[PMS_PENDING:audience]] Specify topic-specific callable '
                    'capabilities, refreshable inputs and bridges to establish.')
VAGUE_AUDIENCE = ('General undergraduate mathematics and early doctoral background '
               'in the relevant field; specify the actual callable capabilities for this topic.')
PENDING = re.compile(r'(?<!\\)\[\[PMS_PENDING:[A-Za-z0-9_.-]+\]\]')
PREVIEW_DESIGN_CODES = {'EXPOSITION_DESIGN_INCOMPLETE', 'EXPOSITION_DESIGN_MISSING'}


def check_exposition_design(out: Path, plan: dict) -> dict:
    from .profiles import current, GOALS
    from .profiles import validate_plan_contract
    validate_plan_contract(plan)
    errors = []
    def add(message, path='outline.md', code='EXPOSITION_DESIGN_INCOMPLETE', key=None):
        errors.append(diagnostic(code, message, path, key))
    audience = plan.get('audience', '')
    if not isinstance(audience,str) or not audience.strip() or audience.strip() in {DEFAULT_AUDIENCE, VAGUE_AUDIENCE} or PENDING.search(audience):
        add('audience: replace the default with executable capabilities and inputs to refresh/build.', 'plan.json')
    goals = plan.get('reader_goals', [])
    if (not isinstance(goals,list) or not goals or any(not isinstance(g,str) or not g.strip() or
            g.strip() in set(GOALS.values()) or PENDING.search(g) for g in goals)):
        add('reader_goals: specify what this reader will be able to reconstruct for this actual topic.', 'plan.json')
    path = safe(out, 'outline.md')
    if not path.is_file() or not path.read_text(encoding='utf-8').strip():
        add('Exposition outline is missing or empty.', code='EXPOSITION_DESIGN_MISSING')
        return {'status': 'NEEDS_WORK', 'errors': errors, 'meaning': 'No semantic acceptance is inferred.'}
    text = path.read_text(encoding='utf-8')
    # Reserved generated markers remain unresolved even in comments or code fences.
    # A literal teaching example must escape its opening bracket: \[[PMS_PENDING:x]].
    for match in PENDING.finditer(text):
        add(f'Line {text.count(chr(10),0,match.start())+1}: unresolved {match[0]}')
    fence = None
    known_defaults = {VAGUE_AUDIENCE, DEFAULT_AUDIENCE, *GOALS.values()}
    for number, line in enumerate(text.splitlines(),1):
        stripped = line.strip()
        mark = re.match(r'^(`{3,}|~{3,})',stripped)
        if mark:
            kind = mark[1][0]
            if fence is None:
                fence = (kind,len(mark[1]))
            elif kind == fence[0] and len(mark[1]) >= fence[1]:
                fence = None
            continue
        if stripped in known_defaults:
            add(f'Line {number}: uncustomized audience or reader-goal instruction remains.')
        if fence is None and not stripped.startswith('>') and re.match(r'^(?:[-*+]\s+|\d+[.)]\s+)?(?:PENDING|TODO|TBD)\s*:',stripped,re.I):
            add(f'Line {number}: unresolved default task line.')
    available = set(plan['question_ids']) | {s['node_id'] for s in plan['selections']}
    available |= {p['node_id'] for p in plan['prerequisites'] if isinstance(p,dict)}
    for match in re.finditer(r'\[\[(N-[A-Za-z0-9._-]+)\]\]',text):
        key = match[1]
        if key not in available:
            add(f'Line {text.count(chr(10),0,match.start())+1}: node is absent or not available to this plan.',
                code='EXPOSITION_DESIGN_INVALID_REFERENCE',key=key)
    return {'status': 'NEEDS_WORK' if errors else 'COMPLETE', 'errors': errors,
            'meaning': 'Known unfinished markers and references only; actual exposition requires located semantic reading.'}
