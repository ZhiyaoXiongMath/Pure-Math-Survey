"""Independent source facts; URL/hash/template never imply reading or permission."""
from __future__ import annotations
from .common import diagnostic, file_hash, valid_date, require
from .profiles import mapping, filled


def fact(record, allowed):
    record = mapping(record); status = record.get('status', 'unknown')
    if not isinstance(status,str) or status not in allowed or status == 'unknown': return 'UNVERIFIED'
    if not valid_date(record.get('checked_at')) or not filled(record.get('basis')): return 'UNVERIFIED'
    return 'VERIFIED' if status in {'accessible', 'granted'} else 'REJECTED'


def source_facts(inv, sid):
    source=inv.sources[sid]; access=source['access']; raw=access.get('local_path'); digest=access.get('material_sha256')
    bytes_status='UNVERIFIED'
    if raw and digest: bytes_status='VERIFIED' if file_hash(inv.root,raw)==digest else 'REJECTED'
    return {'source_id':sid, 'controlling_version':source['version'],
            'access':fact(access.get('availability'), {'accessible','unavailable','unknown'}),
            'reading_declared':access.get('state','not_declared'), 'bytes':bytes_status, 'recorded_sha256':digest,
            'redistribution':fact(access.get('redistribution'), {'granted','denied','unknown'}),
            'material_visibility':access.get('material_visibility','unknown'),
            'meaning':'Source declarations and rehashed bytes only; no automated reading or license determination.'}


def require_source_bytes(inv):
    """A supplied hash must match retained bytes, independently of reading status."""
    for sid,source in inv.sources.items():
        access=source['access']; raw=access.get('local_path'); expected=access.get('material_sha256')
        if raw and expected:
            require(file_hash(inv.root,raw)==expected, 'SOURCE_MATERIAL_MISMATCH',
                    'Retained original bytes differ from material_sha256; fix the source identity before use.',
                    inv.source_paths[sid])


def _source_hashes(inv, source):
    """Track actual retained bytes even when their optional declared hash is absent."""
    access=source['access']; hashes=set()
    if access.get('material_sha256'): hashes.add(access['material_sha256'])
    if access.get('local_path'): hashes.add(file_hash(inv.root,access['local_path']))
    return hashes


def original_hashes(inv):
    return {digest for source in inv.sources.values() for digest in _source_hashes(inv,source)}


def public_original_errors(inv):
    """Never stage public snapshots of private or unlicensed originals."""
    errors=[]
    for sid,source in inv.sources.items():
        access=source['access']; raw=access.get('local_path')
        if not raw: continue
        if access.get('material_visibility')!='public':
            errors.append(diagnostic('SOURCE_PRIVATE_ORIGINAL','Keep private originals outside the public project; use safe identity/hash and limitations with local_path null.',inv.source_paths[sid]))
        permission=fact(access.get('redistribution'), {'granted','denied','unknown'})
        if permission!='VERIFIED':
            errors.append(diagnostic('SOURCE_REDISTRIBUTION_REJECTED' if permission=='REJECTED' else 'SOURCE_REDISTRIBUTION_UNVERIFIED',
                'Public original bytes require explicit dated redistribution permission and its actual basis.',inv.source_paths[sid]))
    original_records={}
    for source in inv.sources.values():
        for digest in _source_hashes(inv,source):
            original_records.setdefault(digest,[]).append(source['access'])
    for path in inv.files:
        if any(part.casefold() in {'private','.private'} for part in path.split('/')):
            errors.append(diagnostic('SOURCE_PRIVATE_ORIGINAL','Private paths cannot enter public snapshot or authoring inputs.',path))
        matches=original_records.get(file_hash(inv.root,path),[])
        for access in matches:
            if access.get('material_visibility')!='public' or fact(access.get('redistribution'), {'granted','denied','unknown'})!='VERIFIED':
                errors.append(diagnostic('SOURCE_ORIGINAL_ALIAS_UNSAFE','Known original bytes, including reading-note aliases, require public visibility and actual redistribution authorization.',path))
    return errors


def original_input_paths(inv, paths):
    """Omit declared originals and their byte-identical aliases from authoring."""
    declared={s['access'].get('local_path') for s in inv.sources.values()}-{None}
    hashes=original_hashes(inv)
    return {p for p in paths if p in declared or file_hash(inv.root,p) in hashes}


def require_public_originals(inv):
    errors=public_original_errors(inv)
    if errors:
        first=errors[0]; require(False,first['code'],first['message'],first['path'])
