"""Independent source facts; URL/hash/template never imply reading or permission."""
from __future__ import annotations
from .common import diagnostic, file_hash, valid_date, require
from .profiles import mapping, filled, normalize_locator


def fact(record, allowed):
    record = mapping(record); status = record.get('status', 'unknown')
    if not isinstance(status,str) or status not in allowed or status == 'unknown': return 'UNVERIFIED'
    if not valid_date(record.get('checked_at')) or not filled(record.get('basis')): return 'UNVERIFIED'
    return 'VERIFIED' if status in {'accessible', 'granted'} else 'REJECTED'


def source_facts(inv, sid, review=None, locators=None):
    source=inv.sources[sid]; access=source['access']; raw=access.get('local_path'); digest=access.get('material_sha256')
    bytes_status='UNVERIFIED'
    if raw and digest: bytes_status='VERIFIED' if file_hash(inv.root,raw)==digest else 'REJECTED'
    return {'source_id':sid, 'controlling_version':source['version'],
            'access':fact(access.get('availability'), {'accessible','unavailable','unknown'}),
            'reading':'VERIFIED' if review and not source_scope_errors(inv,sid,review,locators,check_access=False) else 'UNVERIFIED',
            'bytes':bytes_status, 'recorded_sha256':digest,
            'redistribution':fact(access.get('redistribution'), {'granted','denied','unknown'}),
            'redistribution_declared':mapping(access.get('redistribution')).get('status','unknown'),
            'material_visibility':access.get('material_visibility','unknown'),
            'meaning':'Recorded human assertions and rehashed bytes only; no automated reading or license determination.'}


def source_scope_errors(inv, sid, review, locators=None, *, check_access=True):
    source=inv.sources[sid]; access=source['access']; path=inv.source_paths[sid]; errors=[]
    def add(code,message): errors.append(diagnostic(code,message,path))
    reading=mapping(mapping(mapping(review).get('scope')).get('source_reading')).get(sid); reading=mapping(reading)
    if source.get('version_conflicts') or not filled(source['version']):
        add('SOURCE_VERSION_CONFLICT','Record an exact controlling version and resolve conflicting candidates.')
    availability=fact(access.get('availability'), {'accessible','unavailable','unknown'})
    if check_access and availability!='VERIFIED':
        add('SOURCE_ACCESS_REJECTED' if availability=='REJECTED' else 'SOURCE_ACCESS_UNVERIFIED',
            'Record actual dated access and its basis independently of URL, reading and redistribution.')
    if (access['state']!='full_text_read' or not valid_date(access['checked_at']) or not access.get('reading_note')
            or not review or review.get('reviewer_mode') not in ('author_reread','independent_review')
            or not filled(review.get('reviewer')) or not valid_date(review.get('reviewed_at')) or review.get('disposition')!='accepted'):
        add('SOURCE_REVIEW_MISSING','Need a dated actual original-text reading and accepted input-bound review.')
    declared=reading.get('locators')
    valid_locators=isinstance(declared,list) and bool(declared) and all(isinstance(x,str) and x.strip() for x in declared)
    expected=locators if locators is not None else [s['locator'] for n in inv.nodes.values()
                for s in n.meta['sources'] if s['source_id']==sid and s['role']=='support']
    if (reading.get('version')!=source['version'] or not valid_locators or not filled(reading.get('reading_scope'))
            or not isinstance(reading.get('unchecked_items'),list)):
        add('SOURCE_REVIEW_MISSING','Specify controlling version, locator list, actual reading scope and explicit unchecked items.')
    elif not {normalize_locator(x) for x in expected} <= {normalize_locator(x) for x in declared}:
        add('SOURCE_LOCATOR_UNCHECKED','Actual source reading must cover every consumed support locator, not only a nonempty list.')
    if reading.get('unchecked_items'):
        from .reviews import blocking_unchecked
        if isinstance(reading['unchecked_items'],list) and blocking_unchecked({'unchecked_items':reading['unchecked_items']}):
            add('SOURCE_REVIEW_MISSING','Blocking source-reading work remains unchecked.')
    raw=access.get('local_path')
    note=access.get('reading_note')
    if note and access.get('material_sha256')==file_hash(inv.root,note):
        add('SOURCE_MATERIAL_MISMATCH','A reading note or original-byte alias cannot certify original-text reading.')
    if raw:
        if raw in {access.get('reading_note'),access.get('permission_note')}:
            add('SOURCE_MATERIAL_MISMATCH','The reading or permission note cannot serve as original source bytes.')
        if reading.get('mode')!='original_text_local': add('SOURCE_REVIEW_MISSING','Retained bytes require explicit original_text_local reading scope.')
        if not access.get('material_sha256') or file_hash(inv.root,raw)!=access['material_sha256']:
            add('SOURCE_MATERIAL_MISMATCH','Original bytes differ from their declared hash; a note is not an original.')
    elif (reading.get('mode') not in ('original_text_online','original_text_private')
          or (reading.get('mode')=='original_text_online' and not filled(source['identifiers'].get('url')))
          or not filled(access.get('material_hash_unavailable_reason')) or not filled(reading.get('raw_bytes_unavailable_reason'))):
        add('SOURCE_REVIEW_MISSING','Unretained originals need actual online/private reading scope and explicit byte-retention limitations.')
    return errors


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
        digest=source['access'].get('material_sha256')
        if digest: original_records.setdefault(digest,[]).append(source['access'])
    for path in inv.files:
        if any(part.casefold() in {'private','.private'} for part in path.split('/')):
            errors.append(diagnostic('SOURCE_PRIVATE_ORIGINAL','Private paths cannot enter public snapshot or authoring inputs.',path))
        matches=original_records.get(file_hash(inv.root,path),[])
        for access in matches:
            if access.get('material_visibility')!='public' or fact(access.get('redistribution'), {'granted','denied','unknown'})!='VERIFIED':
                errors.append(diagnostic('SOURCE_ORIGINAL_ALIAS_UNSAFE','Known original bytes, including reading-note/review-input aliases, require public visibility and actual redistribution authorization.',path))
    return errors


def original_input_paths(inv, paths):
    """Omit declared originals and their byte-identical aliases from authoring."""
    declared={s['access'].get('local_path') for s in inv.sources.values()}-{None}
    hashes={s['access'].get('material_sha256') for s in inv.sources.values()}-{None}
    return {p for p in paths if p in declared or file_hash(inv.root,p) in hashes}


def require_public_originals(inv):
    errors=public_original_errors(inv)
    if errors:
        first=errors[0]; require(False,first['code'],first['message'],first['path'])
