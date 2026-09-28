"""Content-addressed atomic snapshots, byte verification and plan-scoped impact."""
from __future__ import annotations
from pathlib import Path
import re
import shutil
import tempfile
from .common import VERSION, all_files, atomic_bytes, canonical, file_inventory, read_json, require, result, safe, sha, write_json, writer
from .knowledge import inventory
from .dependencies import affected_dependents

def payload(project_id: str, files: list[dict]) -> dict:
    return {'schema_version': VERSION, 'project_id': project_id, 'files': files}

def load_snapshot(root: Path, snapshot_id: str) -> tuple[dict, Path]:
    require(bool(re.fullmatch('KB-[a-f0-9]{64}', snapshot_id)), 'SNAPSHOT_INVALID', 'Expected full SHA-256 snapshot ID')
    folder = safe(root, f'snapshots/{snapshot_id}')
    require(folder.is_dir(), 'UNKNOWN_REFERENCE', 'Snapshot is missing', f'snapshots/{snapshot_id}')
    m = read_json(safe(folder, 'manifest.json', True))
    require(m.get('schema_version') == VERSION, 'SCHEMA_UNSUPPORTED', 'Unsupported snapshot schema', f'snapshots/{snapshot_id}/manifest.json')
    require(m.get('snapshot_id') == snapshot_id and isinstance(m.get('project_id'), str) and isinstance(m.get('files'), list), 'SNAPSHOT_TAMPERED', 'Malformed snapshot manifest')
    require('KB-' + sha(canonical(payload(m['project_id'], m['files']))) == snapshot_id, 'SNAPSHOT_TAMPERED', 'Snapshot ID does not match manifest')
    paths = []
    for record in m['files']:
        require(set(record) == {'path', 'sha256', 'bytes'} and type(record['bytes']) is int, 'SNAPSHOT_TAMPERED', 'Invalid file manifest record')
        p = safe(folder, 'files/' + record['path'], True); data = p.read_bytes()
        require(sha(data) == record['sha256'] and len(data) == record['bytes'], 'SNAPSHOT_TAMPERED', 'Frozen file bytes differ', 'files/' + record['path'])
        paths.append(record['path'])
    require(paths == sorted(set(paths)), 'SNAPSHOT_TAMPERED', 'Snapshot file list not unique/canonical')
    actual = all_files(folder)
    require(set(actual) == {'manifest.json'} | {'files/' + p for p in paths}, 'SNAPSHOT_TAMPERED', 'Unexpected or missing frozen members')
    parent_project = read_json(root / 'project.json')
    require(parent_project.get('project_id') == m['project_id'], 'SNAPSHOT_PROJECT_MISMATCH', 'Snapshot belongs to a different project')
    require(read_json(folder / 'files/project.json')['project_id'] == m['project_id'], 'SNAPSHOT_TAMPERED', 'Internal project identity differs')
    return m, folder / 'files'

def verify_snapshot(root: Path, snapshot_id: str) -> dict:
    m, files = load_snapshot(root, snapshot_id)
    inventory(files)
    return result('kb.verify', 'VERIFIED', {'snapshot_id': snapshot_id, 'files': len(m['files']), 'meaning': 'byte identity only'})

def freeze_snapshot(root: Path) -> dict:
    with writer(root):
        inv = inventory(root)
        contents = {p: safe(root, p, True).read_bytes() for p in inv.files}
        records = [{'path': p, 'sha256': sha(b), 'bytes': len(b)} for p, b in sorted(contents.items())]
        value = payload(inv.project['project_id'], records); sid = 'KB-' + sha(canonical(value))
        snapshots = safe(root, 'snapshots'); snapshots.mkdir(exist_ok=True)
        target = snapshots / sid
        if target.exists():
            load_snapshot(root, sid)
            return result('kb.freeze', 'REUSED', {'snapshot_id': sid, 'manifest': f'snapshots/{sid}/manifest.json'})
        stage = Path(tempfile.mkdtemp(prefix='.pending-', dir=snapshots))
        try:
            for p, data in contents.items():
                atomic_bytes(stage / 'files' / p, data)
            # Verify staged bytes and reject concurrent changes even under the advisory lock.
            require(file_inventory(stage / 'files', inv.files) == records and file_inventory(root, inv.files) == records,
                    'SNAPSHOT_INPUT_CHANGED', 'Input changed while freezing; retry')
            write_json(stage / 'manifest.json', {**value, 'snapshot_id': sid})
            stage.rename(target)
        finally:
            if stage.exists(): shutil.rmtree(stage)
        load_snapshot(root, sid)
    return result('kb.freeze', 'FROZEN', {'snapshot_id': sid, 'manifest': f'snapshots/{sid}/manifest.json'})

def diff_snapshots(root: Path, old_id: str, new_id: str) -> dict:
    old_m, oldroot = load_snapshot(root, old_id); new_m, newroot = load_snapshot(root, new_id)
    a, b = inventory(oldroot), inventory(newroot)
    fa = {x['path']: x['sha256'] for x in old_m['files']}; fb = {x['path']: x['sha256'] for x in new_m['files']}
    changed_files = {p for p in fa.keys() | fb.keys() if fa.get(p) != fb.get(p)}
    added = sorted(b.nodes.keys() - a.nodes.keys()); removed = sorted(a.nodes.keys() - b.nodes.keys())
    changed = sorted(k for k in a.nodes.keys() & b.nodes.keys() if fa[a.nodes[k].path] != fb[b.nodes[k].path])
    source_changes = sorted(k for k in a.sources.keys() | b.sources.keys() if fa.get(a.source_paths.get(k, '')) != fb.get(b.source_paths.get(k, '')))
    changed_seeds = set(changed + removed + added)
    for inv in (a,b):
        for k,n in inv.nodes.items():
            if any(s['source_id'] in source_changes for s in n.meta['sources']): changed_seeds.add(k)
    deps = affected_dependents(a.nodes, changed_seeds) | affected_dependents(b.nodes, changed_seeds)
    outputs = []
    from .models import load_plan
    from .plans import consumed_paths, validate_plan, consumption
    for file in sorted((root / 'outputs').glob('*/plan.json')):
        plan = load_plan(file)
        if plan['snapshot_id'] != old_id:
            continue
        validate_plan(root, plan)
        consumed = consumed_paths(a, plan)
        selected_nodes=consumption(a,plan)
        selected_sources={ref['source_id'] for key in selected_nodes for ref in a.nodes[key].meta['sources']}
        review_hits=set()
        for rel in changed_files:
            if not rel.startswith('evidence/reviews/') or not rel.endswith('.json'):continue
            for frozen in (oldroot,newroot):
                rp=safe(frozen,rel)
                if not rp.is_file():continue
                review=read_json(rp);scope=review.get('scope',{})
                if (set(scope.get('node_ids',[])) & selected_nodes or
                    set(scope.get('source_ids',[])) & selected_sources or
                    set(scope.get('question_ids',[])) & set(plan['question_ids'])):
                    review_hits.add(rel)
        hits = sorted((consumed & changed_files) | review_hits)
        if hits:
            locations = []
            main = file.parent / 'manuscript/main.tex'
            lines = main.read_text(encoding='utf-8').splitlines() if main.exists() else []
            for p in hits:
                key = next((k for k,n in a.nodes.items() if n.path == p), None)
                found = [i+1 for i,line in enumerate(lines) if key and key in line]
                locations.append({'changed_input': p, 'node_id': key, 'manuscript_lines': found,
                                  'location': file.relative_to(root).as_posix() if not found else (file.parent/'manuscript/main.tex').relative_to(root).as_posix(),
                                  'action': 'Reassess consumed input, dependent proof and surrounding prose before adopting new snapshot.'})
            # B-inspired impact precision: inspect all literal body sections and
            # locate affected dependent statements, not only IDs in main.tex.
            from .tex import inspect_tex
            from .common import SurveyError
            nodes_affected = deps & consumption(a,plan)
            precise = []
            if main.is_file():
                try:
                    scan = inspect_tex(file.parent)
                    for loc in scan.locations:
                        key = Path(loc['input']).stem
                        if key in nodes_affected:
                            precise.append({**loc,'node_id':key,
                                            'project_path':(file.parent/loc['path']).relative_to(root).as_posix()})
                except (SurveyError,OSError):
                    # A missing/unfinished manuscript does not prevent KB diff.
                    pass
            outputs.append({'output_id': plan['output_id'], 'consumed_changes': hits, 'locations': locations,
                            'affected_nodes':sorted(nodes_affected),'authored_locations':precise,'review_changes':sorted(review_hits)})
    return result('kb.diff', 'COMPARED', {'from': old_id, 'to': new_id, 'added': added, 'removed': removed, 'changed': changed,
                  'source_changes': source_changes, 'affected_dependents': sorted(deps), 'changed_files': sorted(changed_files), 'affected_outputs': outputs,
                  'historical_outputs': 'Remain bound to old snapshot; no review record was rewritten.'})
