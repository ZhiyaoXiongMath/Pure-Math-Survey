"""Strict native 2.0.0 contracts; UTF-8 canonical blocks are not rewritten."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import json
from .common import VERSION, decode, read_json, require, relative, identifier, valid_date, safe

FACETS = {'foundations', 'results', 'methods', 'boundaries'}
KINDS = {'question', 'definition', 'result', 'relation', 'mechanism', 'example', 'application', 'frontier'}
STATUSES = {'unassessed', 'established', 'conjectural', 'open', 'refuted', 'not_applicable'}
RELATIONS = {'uses_definition', 'proof_input', 'explained_by', 'explains', 'compares_with', 'refutes', 'specializes'}
PROFILES = {'minimal', 'thematic', 'lecture'}

def fields(obj: dict, required: dict[str, type], path: str = '') -> None:
    require(isinstance(obj, dict), 'CONTRACT_INVALID', 'Expected JSON object', path)
    for name, typ in required.items():
        require(name in obj and type(obj[name]) is typ, 'CONTRACT_INVALID', f'{name}: expected {typ.__name__}', path)
    if 'schema_version' in required:
        require(obj['schema_version'] == VERSION, 'SCHEMA_UNSUPPORTED', f"Unsupported schema: {obj['schema_version']}", path)

def text(value: object, path: str, field: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), 'CONTRACT_INVALID', f'{field}: nonempty text required', path)

@dataclass(frozen=True)
class Node:
    meta: dict
    body: str
    statement: bytes | None
    path: str

    @property
    def id(self) -> str:
        return self.meta['id']

def node_bytes(meta:dict,body:str)->bytes:
    return ('---\n'+json.dumps(meta,ensure_ascii=False,indent=2)+'\n---\n\n'+body.rstrip()+'\n').encode('utf-8')


def load_project(root: Path) -> dict:
    require(not (root / 'project-manifest.json').exists(), 'SCHEMA_UNSUPPORTED',
            'Only the current project.json contract is supported', 'project-manifest.json')
    candidates = list((root / 'evidence/reviews').glob('*.json'))
    candidates += list((root / 'outputs').glob('*/evidence/reviews/*.json'))
    candidates += list((root / 'outputs').glob('*/evidence/*review*.json'))
    for path in candidates:
        review = read_json(safe(root, path.relative_to(root).as_posix(), True))
        if isinstance(review, dict) and 'review_id' in review:
            require(isinstance(review.get('scope'), dict), 'REVIEW_FORMAT_UNSUPPORTED',
                    'Reviews must use the current scoped evidence contract', str(path.relative_to(root)))
    obj = read_json(root / 'project.json')
    fields(obj, {'schema_version': str, 'project_id': str, 'title': str, 'language': str, 'scope_file': str, 'knowledge_root': str}, 'project.json')
    require(identifier(obj['project_id']), 'CONTRACT_INVALID', 'Invalid stable project ID', 'project.json')
    for f in ('title', 'language'):
        text(obj[f], 'project.json', f)
    for f in ('scope_file', 'knowledge_root'):
        relative(obj[f])
    cutoff = obj.get('literature_cutoff')
    require(cutoff is None or valid_date(cutoff), 'CONTRACT_INVALID', 'Invalid literature_cutoff', 'project.json')
    return obj

def load_node(path: Path, relative_path: str | None = None) -> Node:
    loc = relative_path or path.name
    raw = path.read_bytes()
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f'{loc}: UTF-8 required') from e
    front = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', content, re.S)
    require(front, 'FRONTMATTER_INVALID', 'Use standalone --- lines around JSON frontmatter', loc)
    meta, body = decode(front[1], loc), front[2]
    fields(meta, {'schema_version': str, 'id': str, 'kind': str, 'title': str, 'facets': list, 'question_ids': list,
                  'mathematical_status': str, 'origin': str, 'sources': list, 'links': list}, loc)
    require(identifier(meta['id'], 'N-') and path.stem == meta['id'], 'NODE_ID_INVALID', 'Filename and stable N- ID must agree', loc)
    require(meta['kind'] in KINDS and meta['mathematical_status'] in STATUSES, 'CONTRACT_INVALID', 'Invalid node kind/status', loc)
    require(meta['origin'] in {'primary_source', 'supplied_manuscript', 'local_derivation'}, 'CONTRACT_INVALID', 'Invalid origin', loc)
    require(meta['facets'] and all(x in FACETS for x in meta['facets']) and len(set(meta['facets'])) == len(meta['facets']), 'CONTRACT_INVALID', 'Invalid facets', loc)
    text(meta['title'], loc, 'title'); text(body, loc, 'body')
    require(all(identifier(x, 'N-') for x in meta['question_ids']), 'CONTRACT_INVALID', 'Invalid question_ids', loc)
    for edge in meta['links']:
        fields(edge, {'target': str, 'relation': str}, loc)
        require(edge['relation'] in RELATIONS and identifier(edge['target'], 'N-'), 'CONTRACT_INVALID', 'Invalid typed link', loc)
    for src in meta['sources']:
        fields(src, {'source_id': str, 'locator': str, 'role': str}, loc)
        require(identifier(src['source_id'], 'S-') and src['role'] in {'support', 'provenance'}, 'CONTRACT_INVALID', 'Invalid source link', loc)
        text(src['locator'], loc, 'locator')
    headers = list(re.finditer(r'^## Canonical statement[ \t]*\r?$', body, re.M))
    require(len(headers) <= 1, 'CANONICAL_BLOCK_INVALID', 'At most one canonical statement', loc)
    statement = None
    if headers:
        part = body[headers[0].end():]
        part = re.split(r'\r?\n## ', part, maxsplit=1)[0]
        match = re.fullmatch(r'\s*```latex\r?\n(.*?)\r?\n```[ \t\r\n]*', part, re.S)
        require(match and match[1].strip(), 'CANONICAL_BLOCK_INVALID', 'Section must contain only one nonempty latex block', loc)
        statement = match[1].encode('utf-8')
        require(not re.search(r'\\(?:documentclass|label|input|include|usepackage)\b|\\(?:begin|end)\{(?:document|theorem|lemma|proposition|corollary|definition|question)\}', match[1]),
                'CANONICAL_WRAPPER_FORBIDDEN', 'Keep wrappers, labels, imports outside canonical mathematical body', loc)
    require(meta['kind'] not in {'definition', 'result', 'relation'} or statement is not None, 'CANONICAL_BLOCK_MISSING', 'Formal node requires canonical block', loc)
    return Node(meta, body, statement, loc)

def load_source(path: Path, relative_path: str | None = None) -> dict:
    loc = relative_path or path.name
    obj = read_json(path)
    fields(obj, {'schema_version': str, 'id': str, 'kind': str, 'title': str, 'authors': list,
                 'publication_status': str, 'identifiers': dict, 'access': dict}, loc)
    require('version' in obj and (obj['version'] is None or isinstance(obj['version'], str)), 'CONTRACT_INVALID', 'version must be explicit text or null', loc)
    require(identifier(obj['id'], 'S-') and path.stem == obj['id'], 'SOURCE_ID_INVALID', 'Filename and S- ID disagree', loc)
    require(obj['kind'] in {'primary', 'supplied_manuscript'} and obj['publication_status'] in {'published', 'preprint', 'unpublished', 'unknown'}, 'CONTRACT_INVALID', 'Invalid source classification', loc)
    text(obj['title'], loc, 'title')
    require(all(isinstance(a, str) and a.strip() for a in obj['authors']) and obj['identifiers'], 'CONTRACT_INVALID', 'Invalid authors/identity', loc)
    a = obj['access']; fields(a, {'state': str}, loc)
    require(a['state'] in {'metadata_only', 'full_text_read'}, 'CONTRACT_INVALID', 'Invalid access.state', loc)
    for key in ('checked_at', 'material_sha256', 'local_path'):
        require(key in a and (a[key] is None or isinstance(a[key], str)), 'CONTRACT_INVALID', f'access.{key} must be explicit', loc)
    require(a['checked_at'] is None or valid_date(a['checked_at']), 'CONTRACT_INVALID', 'Invalid actual reading date', loc)
    require(a['material_sha256'] is None or bool(re.fullmatch('[a-f0-9]{64}', a['material_sha256'])), 'CONTRACT_INVALID', 'Invalid material SHA-256', loc)
    for key in ('local_path', 'reading_note'):
        if a.get(key) is not None:
            relative(a[key])
    return obj

def load_plan(path: Path) -> dict:
    obj = read_json(path); loc = path.name
    if path.name == 'plan.json' and path.parent.parent.name == 'outputs':
        require(obj.get('output_id') == path.parent.name, 'PLAN_OUTPUT_MISMATCH',
                'Plan output_id must match its owning output directory', str(path))
    fields(obj, {'schema_version': str, 'output_id': str, 'snapshot_id': str, 'profile': str, 'view': str, 'language': str,
                 'title': str, 'audience': str, 'reader_goals': list, 'question_ids': list, 'prerequisites': list,
                 'selections': list, 'omissions': list, 'proof_obligations': list, 'limits': dict, 'draft': bool}, loc)
    require(identifier(obj['output_id']) and re.fullmatch('KB-[a-f0-9]{64}', obj['snapshot_id']), 'CONTRACT_INVALID', 'Invalid output/snapshot ID', loc)
    require(obj['profile'] in PROFILES and obj['view'] in FACETS | {'integrated'}, 'CONTRACT_INVALID', 'Invalid profile/view', loc)
    for key in ('title', 'audience', 'language'):
        text(obj[key], loc, key)
    require(obj['question_ids'] and all(identifier(x, 'N-') for x in obj['question_ids']) and obj['reader_goals'] and all(isinstance(g, str) and g.strip() for g in obj['reader_goals']), 'CONTRACT_INVALID', 'Specify questions and reader goals', loc)
    for s in obj['selections']:
        fields(s, {'node_id': str, 'role': str, 'statement_treatment': str, 'proof_treatment': str, 'reason': str}, loc)
        require(s['role'] in {'principal_answer', 'essential_bridge', 'boundary', 'background', 'frontier'} and s['statement_treatment'] in {'full', 'explained_reference'} and s['proof_treatment'] in {'complete', 'sketch', 'mechanism', 'citation', 'none'}, 'CONTRACT_INVALID', 'Invalid selection treatment', loc)
        text(s['reason'], loc, 'selection.reason')
    for o in obj['omissions']:
        fields(o, {'node_id': str, 'reason': str}, loc); text(o['reason'], loc, 'omission.reason')
    for p in obj['prerequisites']:
        require(isinstance(p, (str, dict)), 'CONTRACT_INVALID', 'Prerequisite must be prose or explicitly scoped node', loc)
        if isinstance(p, dict):
            fields(p, {'node_id': str, 'scope': str, 'reason': str}, loc)
            text(p['scope'], loc, 'prerequisite.scope'); text(p['reason'], loc, 'prerequisite.reason')
    for o in obj['proof_obligations']:
        fields(o, {'node_id': str, 'treatment': str, 'required_steps': list, 'imported_inputs': list}, loc)
        require(o['treatment'] in {'complete', 'sketch', 'mechanism'} and o['required_steps'] and all(isinstance(s, str) and s.strip() for s in o['required_steps']), 'PROOF_OBLIGATION_UNMET', 'Record actual promised steps', loc)
    require('max_pages' in obj['limits'], 'CONTRACT_INVALID', 'Explicit max_pages or null required', loc)
    for k in ('max_pages', 'page_review_threshold'):
        value = obj['limits'].get(k)
        require(value is None or (type(value) is int and value > 0), 'CONTRACT_INVALID', f'{k}: positive integer or null', loc)
    if obj.get('comparison_group') is not None:
        text(obj['comparison_group'], loc, 'comparison_group')
    return obj
