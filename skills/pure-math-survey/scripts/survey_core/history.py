"""Immutable local build/render evidence. Current pointers are replaceable views."""
from __future__ import annotations
from pathlib import Path
import shutil
import tempfile

from .common import (all_files, atomic_bytes, canonical, read_json, require, safe,
                     sha, write_json, result)


def verify_record(folder: Path) -> dict:
    manifest = read_json(safe(folder, 'manifest.json', True))
    files = manifest.get('files', [])
    require(isinstance(files, list), 'HISTORY_TAMPERED', 'Invalid history file inventory', str(folder))
    payload = {'format': 'survey-artifact-history-1', 'kind': manifest.get('kind'), 'files': files}
    identity = 'H-' + sha(canonical(payload))
    require(manifest.get('history_id') == identity and
            (folder.name == identity or folder.name.startswith('.history-')),
            'HISTORY_TAMPERED', 'History manifest identity changed', str(folder))
    require([f['path'] for f in files] == sorted({f['path'] for f in files}),
            'HISTORY_TAMPERED', 'History members must be unique and sorted', str(folder))
    require(set(all_files(folder)) == {'manifest.json'} | {'files/' + f['path'] for f in files},
            'HISTORY_TAMPERED', 'History gained/lost a member', str(folder))
    for row in files:
        data = safe(folder, 'files/' + row['path'], True).read_bytes()
        require(len(data) == row['bytes'] and sha(data) == row['sha256'],
                'HISTORY_TAMPERED', 'Historical bytes changed', row['path'])
    return manifest


def save_record(out: Path, kind: str, data: dict[str, bytes]) -> dict:
    """Caller holds the project writer lock. Never overwrite an existing record."""
    require(kind in {'build', 'render', 'legacy-build'}, 'CONTRACT_INVALID', 'Invalid history kind')
    rows = [{'path': p, 'sha256': sha(b), 'bytes': len(b)} for p, b in sorted(data.items())]
    payload = {'format': 'survey-artifact-history-1', 'kind': kind, 'files': rows}
    identity = 'H-' + sha(canonical(payload))
    manifest = {**payload, 'history_id': identity}
    parent = safe(out, 'history/' + kind)
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / identity
    if target.exists():
        verify_record(target)
        return manifest
    stage = Path(tempfile.mkdtemp(prefix='.history-', dir=parent))
    try:
        for p, b in data.items():
            atomic_bytes(safe(stage, 'files/' + p), b)
        write_json(stage / 'manifest.json', manifest)
        verify_record(stage)
        require(not target.exists(), 'DESTINATION_EXISTS', 'Concurrent history creation refused', str(target))
        stage.rename(target)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return manifest


def archive_current(out: Path, kind: str) -> dict | None:
    prefixes = ('build', 'evidence') if kind == 'legacy-build' else ('evidence/pages',)
    paths = {p for prefix in prefixes for p in all_files(out, prefix)}
    if kind == 'render' and (out / 'evidence/render-manifest.json').is_file():
        paths.add('evidence/render-manifest.json')
    if not paths:
        return None
    return save_record(out, kind, {p: safe(out, p, True).read_bytes() for p in sorted(paths)})


def verify_history(root: Path, output_id: str) -> dict:
    out = safe(root, 'outputs/' + output_id)
    require(out.is_dir(), 'UNKNOWN_REFERENCE', 'Output directory is missing', 'outputs/' + output_id)
    records = []
    for path in sorted((out / 'history').glob('*/H-*')):
        records.append(verify_record(path))
    return result('output.history', 'VERIFIED', {'output_id': output_id,
                  'records': [{'history_id': r['history_id'], 'kind': r['kind'],
                               'files': len(r['files'])} for r in records],
                  'boundary': 'Historical bytes verified; no mathematical or new-page approval is granted.'})
