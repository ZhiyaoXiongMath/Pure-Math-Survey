"""Readable project inventory and a legal knowledge-only initialization."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import tempfile
from .common import VERSION, all_files, atomic_bytes, diagnostic, file_inventory, read_json, require, result, safe, write_json, writer, identifier
from .models import Node, fields, load_node, load_project, load_source
from .dependencies import detect_cycles

@dataclass
class Inventory:
    root: Path
    project: dict
    nodes: dict[str, Node]
    sources: dict[str, dict]
    source_paths: dict[str, str]
    coverage: dict
    files: list[str]

def inventory(root: Path) -> Inventory:
    root = root.absolute(); project = load_project(root)
    kr = project['knowledge_root']; scope = project['scope_file']
    require(safe(root, scope, True).read_text(encoding='utf-8').strip(), 'SCOPE_EMPTY', 'Describe objects, quantifiers and exclusions', scope)
    for suffix in ('overview.md', 'conventions.tex', 'discovery.md', 'coverage.json'):
        safe(root, f'{kr}/{suffix}', True)
    nodes, sources, source_paths = {}, {}, {}
    for p in all_files(root, kr + '/nodes'):
        require(p.endswith('.md'), 'CONTRACT_INVALID', 'Only node Markdown belongs in nodes/', p)
        node = load_node(safe(root, p, True), p)
        require(node.id not in nodes, 'DUPLICATE_ID', f'Duplicate node {node.id}', p, node.id)
        nodes[node.id] = node
    for p in all_files(root, kr + '/sources'):
        require(p.endswith('.json'), 'CONTRACT_INVALID', 'Only source JSON belongs in sources/', p)
        obj = load_source(safe(root, p, True), p); key = obj['id']
        require(key not in sources, 'DUPLICATE_ID', f'Duplicate source {key}', p)
        sources[key], source_paths[key] = obj, p
    for key, n in nodes.items():
        for q in n.meta['question_ids']:
            require(q in nodes and nodes[q].meta['kind'] == 'question', 'UNKNOWN_REFERENCE', f'question_ids: {q}', n.path, key)
        for edge in n.meta['links']:
            require(edge['target'] in nodes, 'UNKNOWN_REFERENCE', f"links.{edge['relation']}: {edge['target']}", n.path, key)
        for src in n.meta['sources']:
            require(src['source_id'] in sources, 'UNKNOWN_REFERENCE', f"sources: {src['source_id']}", n.path, key)
            if src.get('version') is not None:
                require(src['version'] == sources[src['source_id']]['version'], 'SOURCE_VERSION_CONFLICT', f"Requested locator version {src['version']} differs from controlling source version", n.path, key)
    detect_cycles(nodes)
    cov = read_json(safe(root, kr + '/coverage.json', True))
    fields(cov, {'schema_version': str, 'questions': list}, kr + '/coverage.json')
    seen = set()
    for q in cov['questions']:
        fields(q, {'question_id': str, 'answer_nodes': list, 'mechanism_nodes': list, 'boundary_nodes': list,
                   'gaps': list, 'assessment': str, 'rationale': str}, kr + '/coverage.json')
        require(q['question_id'] in nodes and nodes[q['question_id']].meta['kind'] == 'question', 'UNKNOWN_REFERENCE', 'Unknown coverage question', kr + '/coverage.json', q['question_id'])
        require(q['question_id'] not in seen, 'DUPLICATE_ID', 'Duplicate coverage question', kr + '/coverage.json')
        seen.add(q['question_id'])
        require(q['assessment'] in {'pending', 'adequate', 'limited'} and q['rationale'].strip(), 'CONTRACT_INVALID', 'Invalid coverage assessment/rationale', kr + '/coverage.json')
        for group in ('answer_nodes', 'mechanism_nodes', 'boundary_nodes'):
            for key in q[group]:
                require(key in nodes, 'UNKNOWN_REFERENCE', f'coverage.{group}: {key}', kr + '/coverage.json', key)
    paths = set(['project.json', scope] + all_files(root, kr) + all_files(root, 'evidence'))
    for key, src in sources.items():
        for f in ('local_path', 'reading_note'):
            path = src['access'].get(f)
            if path:
                safe(root, path, True); paths.add(path)
    # Readable cross references are navigation, not another dependency registry.
    for p in paths:
        if p.endswith('.md'):
            for target in re.findall(r'\[\[([NS]-[A-Za-z0-9._-]+)\]\]', safe(root, p, True).read_text(encoding='utf-8')):
                require(target in nodes or target in sources, 'UNKNOWN_REFERENCE', f'Broken readable link [[{target}]]', p)
    for p in all_files(root, 'evidence/reviews'):
        if p.endswith('.json'):
            from .reviews import load_review
            review = load_review(safe(root, p, True))
            for binding in review['inputs']:
                require(not binding['path'].startswith(('snapshots/', 'outputs/', '.cache/')) and binding['path'] != p,
                        'REVIEW_BINDING_INVALID', 'Knowledge review may not bind snapshots, outputs, cache or itself', p)
                # Historical stale paths may be missing; retain the record, report on use.
    return Inventory(root, project, nodes, sources, source_paths, cov, sorted(paths))

def validate_knowledge(root: Path) -> dict:
    inv = inventory(root)
    pending = [k for k, n in inv.nodes.items() if n.meta['mathematical_status'] == 'unassessed']
    return result('kb.validate', 'VALID', {'project_id': inv.project['project_id'], 'node_count': len(inv.nodes), 'source_count': len(inv.sources),
                 'unassessed_nodes': pending, 'outputs_required': False}, warnings=[diagnostic('SEMANTIC_NOT_CERTIFIED', 'Structural validity is not mathematical readiness.')])

def init_project(destination: Path, topic: str, scope: Path, title: str | None = None, language: str = 'en') -> dict:
    require(identifier(topic), 'CONTRACT_INVALID', 'Invalid topic/project ID')
    require(not destination.exists(), 'DESTINATION_EXISTS', 'Initialize into a new directory', destination.name)
    body = scope.read_bytes(); require(body.strip(), 'SCOPE_EMPTY', 'Scope must not be empty', scope.name)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.survey-init-', dir=destination.parent))
    try:
        write_json(stage / 'project.json', {'schema_version': VERSION, 'project_id': topic, 'title': title or topic,
                   'language': language, 'scope_file': 'scope.md', 'knowledge_root': 'knowledge', 'literature_cutoff': None})
        atomic_bytes(stage / 'scope.md', body)
        atomic_bytes(stage / 'knowledge/overview.md', b'# Knowledge overview\n\nPending: reconstruct the question, answers, mechanisms and decisive boundaries.\nNo mathematical claims have been reviewed.\n')
        atomic_bytes(stage / 'knowledge/conventions.tex', b'% Project-wide mathematical notation. No claims are certified here.\n')
        atomic_bytes(stage / 'knowledge/discovery.md', b'# Discovery\n\nNo source search or original-text reading has been performed in this new project.\nRecord actual queries, candidates, omissions and stopping reasons here.\n')
        write_json(stage / 'knowledge/coverage.json', {'schema_version': VERSION, 'questions': []})
        inventory(stage)
        stage.rename(destination)
    finally:
        if stage.exists(): shutil.rmtree(stage)
    return result('init', 'INITIALIZED', {'project': str(destination), 'outputs': [], 'review_status': 'pending'})

def index_knowledge(root: Path) -> dict:
    inv = inventory(root)
    derived = {'schema_version': VERSION, 'project_id': inv.project['project_id'],
               'nodes': [{'id': k, 'title': n.meta['title'], 'kind': n.meta['kind'], 'facets': n.meta['facets'], 'path': n.path} for k,n in sorted(inv.nodes.items())],
               'files': file_inventory(root, inv.files)}
    with writer(root):
        write_json(safe(root, '.cache/index.json'), derived)
    return result('kb.index', 'INDEXED', {'path': '.cache/index.json', 'nodes': len(inv.nodes)})
