"""Explicit compatibility for the two independent 2.0.0 implementations.

They used the same schema string but different review/build contracts. Merely
reading a 2.0.0 tag must never promote a foreign attestation to native approval.
The B-contract importer preserves originals and exact mathematical body bytes,
but imports *candidates*, not approvals or already-published output projects.
"""
from __future__ import annotations
from pathlib import Path
import json
import re
import shutil
import tempfile
import zipfile

from .common import (VERSION, SOFTWARE_VERSION, all_files, atomic_bytes, canonical,
                     read_json, require, result, safe, sha, write_json)


def identify_contract(root: Path) -> dict:
    root = root.resolve()
    if (root / 'project-manifest.json').exists():
        return {'contract': 'mixed-manifests' if (root / 'project.json').exists() else 'v1', 'evidence': ['project-manifest.json']}
    require((root / 'project.json').is_file(), 'UNKNOWN_PROJECT', 'Missing project.json', str(root))
    obj = read_json(safe(root, 'project.json', True))
    require(obj.get('schema_version') == VERSION, 'SCHEMA_UNSUPPORTED', 'Unsupported on-disk schema', 'project.json')
    a, b = [], []
    # Snapshot roots contain the same evidence layout; only read, never mutate.
    candidates = list((root / 'evidence/reviews').glob('*.json'))
    candidates += list((root / 'outputs').glob('*/evidence/reviews/*.json'))
    candidates += list((root / 'outputs').glob('*/evidence/*review*.json'))
    for path in sorted(candidates):
        relative = path.relative_to(root).as_posix()
        r = read_json(safe(root, relative, True))
        if not isinstance(r, dict) or 'review_id' not in r:
            continue
        if isinstance(r.get('scope'), dict):
            a.append(relative)
        elif 'checks' in r or 'whole_manuscript' in r or 'limitations' in r:
            b.append(relative)
    if a and b:
        contract = 'mixed-review-contracts'
    elif b:
        contract = 'v2-b'
    elif a or obj.get('contract_flavor') == 'survey-local-v2':
        contract = 'v2-a-compatible'
    elif any((root / 'outputs').glob('*/build/latest*.json')):
        contract = 'v2-b'
    else:
        contract = 'v2-common-subset'
    return {'contract': contract, 'evidence': a + b,
            'schema_version': VERSION, 'executable_version': SOFTWARE_VERSION,
            'meaning': 'A compatible file shape is not a mathematical review.'}


def import_v2_b(old: Path, new: Path) -> dict:
    """Atomic, non-destructive import; old snapshots/plans/reviews stay archived."""
    old, new = old.resolve(), new.absolute()
    require(not new.exists(), 'DESTINATION_EXISTS', 'Import destination must not exist', str(new))
    require(not new.resolve().is_relative_to(old), 'UNSAFE_PATH', 'Import destination cannot be inside its source', str(new))
    identified = identify_contract(old)
    require(identified['contract'] in {'v2-b', 'v2-common-subset'}, 'IMPORT_FORMAT_MISMATCH',
            'This command imports the B 2.0.0 contract or its evidence-free common subset', str(old))
    original = {p: safe(old, p, True).read_bytes() for p in all_files(old)}
    project = read_json(safe(old, 'project.json', True))
    new.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.import-v2-', dir=new.parent))
    try:
        # The full original tree is retained byte-for-byte in one local archive.
        backup = stage / 'legacy/v2-b/original.zip'
        backup.parent.mkdir(parents=True)
        with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as z:
            for p, data in sorted(original.items()):
                info = zipfile.ZipInfo(p, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, data)
        with zipfile.ZipFile(backup) as z:
            require(z.testzip() is None and all(z.read(p) == data for p, data in original.items()),
                    'IMPORT_BACKUP_FAILED', 'Original archive byte verification failed')
        project['contract_flavor'] = 'survey-local-v2'
        kroot = project['knowledge_root']
        # Preserve readable working knowledge and source evidence, not executable
        # output/build state or review assertions under the active authority.
        for p, data in original.items():
            if p == project['scope_file'] or p.startswith(kroot + '/') or p.startswith('evidence/source-checks/'):
                atomic_bytes(safe(stage, p), data)
        converted = []
        from .models import load_node
        for path in sorted((stage / kroot / 'nodes').glob('*.md')):
            raw = path.read_bytes().decode('utf-8')
            match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', raw, re.S)
            require(match, 'FRONTMATTER_INVALID', 'Expected JSON-frontmatter node', str(path))
            original_node = load_node(path, path.relative_to(stage).as_posix())
            meta = original_node.meta.copy()
            previous = meta['mathematical_status']
            meta['mathematical_status'] = 'unassessed'
            data = ('---\n' + json.dumps(meta, ensure_ascii=False, indent=2) + '\n---\n' + match[2]).encode('utf-8')
            atomic_bytes(path, data)
            node = load_node(path, path.relative_to(stage).as_posix())
            converted.append({'node_id': node.id, 'prior_status': previous, 'new_status': 'unassessed',
                              'body_preserved': node.body == match[2],
                              'canonical_sha256': sha(node.statement) if node.statement is not None else None})
        for path in sorted((stage / kroot / 'sources').glob('*.json')):
            source = read_json(path)
            a = source['access']
            a['state'], a['checked_at'] = 'metadata_only', None
            for key in ('reading_note', 'local_path'):
                ref = a.get(key)
                if ref:
                    require(ref in original, 'UNKNOWN_REFERENCE', 'Source material is missing from import', ref)
                    atomic_bytes(safe(stage, ref), original[ref])
            write_json(path, source)
        coverage = read_json(safe(stage, kroot + '/coverage.json', True))
        for q in coverage['questions']:
            q['assessment'] = 'pending'
            q['gaps'] = list(q['gaps']) + ['Imported from the distinct B 2.0.0 evidence contract; new scoped native source/mathematical/coverage reviews are required.']
        write_json(stage / kroot / 'coverage.json', coverage)
        write_json(stage / 'project.json', project)
        from .knowledge import validate_knowledge
        validate_knowledge(stage)
        source_manifest = [{'path': p, 'sha256': sha(data), 'bytes': len(data)} for p, data in sorted(original.items())]
        report = {'status': 'IMPORTED_UNVERIFIED', 'source_contract': identified,
                  'software_version': SOFTWARE_VERSION, 'project_id': project['project_id'],
                  'nodes': converted, 'original_files': source_manifest,
                  'archive': 'legacy/v2-b/original.zip', 'archive_sha256': sha(backup.read_bytes()),
                  'active_accepted_reviews': 0, 'active_outputs': 0,
                  'preserved_in_archive': ['original snapshots and identities', 'output plans and TeX', 'old mathematical/source/semantic/visual reviews', 'build histories and PDFs'],
                  'next_steps': ['Read the imported scope and exact node bodies.', 'Re-establish source, mathematical and coverage evidence using the native review templates.', 'Freeze the new knowledge; explicitly create the requested output plans.'],
                  'boundary': 'No theorem was re-proved, no prior PASS was inherited, and no Studio format was created.'}
        write_json(stage / 'IMPORT_REPORT.json', report)
        atomic_bytes(stage / 'IMPORT_REPORT.zh-CN.md', ('# B 合同导入\n\n原始文件完整保留在 `legacy/v2-b/original.zip`；具体 SHA-256 见 `IMPORT_REPORT.json`。\n\n数学正文、稳定节点 ID 和规范陈述保留。活动状态降为待核查，旧审阅、快照、计划和 PDF 只作为原件归档。未生成文稿，不继承 PASS。\n').encode())
        require(not new.exists(), 'DESTINATION_EXISTS', 'Destination appeared during import', str(new))
        stage.rename(new)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return result('import-v2', 'IMPORTED_UNVERIFIED', {'project': str(new), 'report': 'IMPORT_REPORT.json',
                  'nodes': len(converted), 'active_accepted_reviews': 0, 'active_outputs': 0})
