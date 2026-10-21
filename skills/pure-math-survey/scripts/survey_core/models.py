"""Strict native 3.0.0 contracts; UTF-8 canonical blocks are not rewritten."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import json
from .common import relpath, VERSION, decode, read_json, require, relative, identifier, valid_date, safe

KINDS = {'definition', 'result', 'method', 'example'}
ROLES = {'principal', 'ingredient', 'bridge', 'context', 'boundary'}
from .profiles import PROFILES, validate_plan_contract

def fields(obj: dict, required: dict[str, type], path: str = '', *, errors: list | None = None) -> None:
    from .common import diagnostic
    def check(ok, code, message):
        if errors is None:
            require(ok, code, message, path)
        elif not ok:
            errors.append(diagnostic(code, message, path))
    check(isinstance(obj, dict), 'CONTRACT_INVALID', 'Expected JSON object')
    if not isinstance(obj, dict): return
    for name, typ in required.items():
        check(name in obj and type(obj[name]) is typ, 'CONTRACT_INVALID', f'{name}: expected {typ.__name__}')
    if 'schema_version' in required and isinstance(obj.get('schema_version'), str):
        check(obj['schema_version'] == VERSION, 'SCHEMA_UNSUPPORTED', f"Unsupported schema: {obj['schema_version']}")

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
    from .common import RUNTIME_CONTRACT
    require(not (root / 'project-manifest.json').exists(), 'LEGACY_PROJECT_UNSUPPORTED',
            'Use the previous installation for old projects or extract into a new directory', 'project-manifest.json')
    obj = read_json(safe(root, 'project.json', True))
    require(isinstance(obj, dict) and obj.get('runtime_contract') == RUNTIME_CONTRACT and obj.get('schema_version') == VERSION,
            'LEGACY_PROJECT_UNSUPPORTED', 'This candidate requires a new minimal-lean-2.4.1 project; no automatic migration', 'project.json')
    fields(obj, {'schema_version': str, 'project_id': str, 'title': str, 'language': str, 'scope_file': str, 'knowledge_root': str}, 'project.json')
    require(identifier(obj['project_id']), 'CONTRACT_INVALID', 'Invalid stable project ID', 'project.json')
    for f in ('title', 'language'):
        text(obj[f], 'project.json', f)
    for f in ('scope_file', 'knowledge_root'):
        relative(obj[f])
    kr = obj['knowledge_root']
    require(not any(safe(root, kr+'/'+name).exists() for name in ('coverage.json', 'overview.md', 'discovery.md')),
            'LEGACY_PROJECT_UNSUPPORTED', 'Old knowledge containers are not a schema migration; create a new project', 'project.json')
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
    fields(meta, {'schema_version': str, 'id': str, 'kind': str, 'title': str, 'role': str,
                  'importance': dict, 'sources': list, 'definition_refs': list, 'source_status': str}, loc)
    require(not ({'facets','question_ids','mathematical_status','origin','links','assumptions','conclusions'} & meta.keys()),
            'CONTRACT_INVALID', 'Retired node containers are not a schema migration', loc)
    require(identifier(meta['id'], 'N-') and path.stem == meta['id'], 'NODE_ID_INVALID', 'Filename and stable N- ID must agree', loc)
    require(meta['kind'] in KINDS and meta['role'] in ROLES, 'CONTRACT_INVALID', 'Invalid independent kind or role', loc)
    require(meta['source_status'] in {'stated','extracted','imported','unresolved'}, 'CONTRACT_INVALID', 'Invalid source_status', loc)
    imp=meta['importance']; fields(imp, {'status':str,'reason':str}, loc)
    require('level' in imp and (imp['level'] is None or type(imp['level']) is int and 1 <= imp['level'] <= 5),
            'CONTRACT_INVALID', 'importance.level must be 1..5 or null', loc)
    require(imp['status'] in {'proposed','human_supplied','unassigned'}, 'CONTRACT_INVALID', 'Invalid importance.status', loc)
    require(all(identifier(x,'N-') for x in meta['definition_refs']) and len(set(meta['definition_refs']))==len(meta['definition_refs']),
            'CONTRACT_INVALID', 'Invalid definition_refs', loc)
    text(meta['title'], loc, 'title'); text(body, loc, 'body')
    for src in meta['sources']:
        fields(src, {'source_id': str, 'locator': str}, loc)
        require(identifier(src['source_id'], 'S-'), 'CONTRACT_INVALID', 'Invalid source link', loc)
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
        require(not re.search(r'\\(?:documentclass|label|input|include|usepackage)\b|\\(?:begin|end)\{(?:document|theorem|lemma|proposition|corollary|definition|question|example|conjecture)\}', match[1]),
                'CANONICAL_WRAPPER_FORBIDDEN', 'Keep wrappers, labels, imports outside canonical mathematical body', loc)
    require(meta['kind'] not in {'definition', 'result'} or statement is not None, 'CANONICAL_BLOCK_MISSING', 'Formal node requires canonical block', loc)
    require(meta.get('statement_kind', 'theorem') in {'definition','theorem','lemma','proposition','corollary','example'},
            'CONTRACT_INVALID', 'Invalid statement_kind', loc)
    return Node(meta, body, statement, loc)

def load_source(path: Path, relative_path: str | None = None) -> dict:
    loc = relative_path or path.name; obj = read_json(path)
    fields(obj, {'schema_version':str,'id':str,'title':str,'authors':list,'citation_key':str}, loc)
    require(not ({'kind','publication_status','identifiers'} & obj.keys()), 'CONTRACT_INVALID', 'Old source containers are not a schema migration', loc)
    require('version' in obj and (obj['version'] is None or isinstance(obj['version'],str)), 'CONTRACT_INVALID', 'version must be text or null', loc)
    require(identifier(obj['id'],'S-') and path.stem==obj['id'], 'SOURCE_ID_INVALID', 'Filename and S- ID disagree', loc)
    require(identifier(obj['citation_key']), 'CONTRACT_INVALID', 'Unsafe citation key', loc)
    text(obj['title'],loc,'title')
    require(all(isinstance(a,str) and a.strip() for a in obj['authors']), 'CONTRACT_INVALID', 'Invalid authors', loc)
    require(obj.get('url') is None or isinstance(obj['url'],str), 'CONTRACT_INVALID', 'url must be text or null', loc)
    a=obj.setdefault('access',{}); fields(a,{},loc)
    for key in ('local_path','reading_note','permission_note'):
        if a.get(key) is not None: relative(a[key])
    digest=a.get('material_sha256')
    require(digest is None or isinstance(digest,str) and bool(re.fullmatch('[a-f0-9]{64}',digest)), 'CONTRACT_INVALID', 'Invalid material SHA-256', loc)
    return obj


def load_plan(path: Path) -> dict:
    obj=read_json(path); loc=path.name; validate_plan_contract(obj)
    fields(obj, {'output_id':str,'profile':str,'view':str,'language':str,'title':str,'selections':list,'route_ids':list,'limits':dict}, loc)
    require(identifier(obj['output_id']), 'CONTRACT_INVALID', 'Invalid output ID', loc)
    if path.name=='plan.json' and path.parent.parent.name=='outputs':
        require(obj['output_id']==path.parent.name, 'PLAN_OUTPUT_MISMATCH', 'Plan output_id must match its owning directory',str(path))
    for key in ('title','language'): text(obj[key],loc,key)
    for selection in obj['selections']:
        fields(selection, {'node_id':str,'role':str,'statement_treatment':str},loc)
        require(identifier(selection['node_id'],'N-') and selection['role'] in ROLES and selection['statement_treatment'] in {'full','explained_reference'},
                'CONTRACT_INVALID','Invalid selection',loc)
    require(all(identifier(r,'R-') for r in obj['route_ids']) and len(set(obj['route_ids']))==len(obj['route_ids']), 'CONTRACT_INVALID','Invalid route_ids',loc)
    require('max_pages' in obj['limits'], 'CONTRACT_INVALID','Explicit max_pages or null required',loc)
    value=obj['limits']['max_pages']
    require(value is None or type(value) is int and value>0, 'CONTRACT_INVALID','max_pages must be positive or null',loc)
    return obj
