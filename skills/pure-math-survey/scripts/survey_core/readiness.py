"""Plan-scoped evidence gate; structure, hashes and statuses do not prove mathematics."""
from __future__ import annotations
from pathlib import Path
from .common import diagnostic, file_hash, require, result, safe, valid_date
from .models import load_plan
from .plans import consumption,validate_plan
from .reviews import coverage_inputs,find_review,mathematical_inputs,reviews_in,source_inputs

def assess_readiness(root:Path,plan:dict|Path)->dict:
    if isinstance(plan,Path):plan=load_plan(plan)
    inv=validate_plan(root,plan); records=reviews_in(inv.root); ids=consumption(inv,plan)
    from .profiles import current, four_modes, profile_readiness_errors, statement_errors, statement_warnings, mapping
    errors=profile_readiness_errors(inv, plan);warnings=[];used=[]; valid_math={}
    principals={s['node_id'] for s in plan['selections'] if s['role']=='principal_answer'}
    obligations={o['node_id']:o for o in plan['proof_obligations']}
    supplied_originals={c['node_id'] for c in plan.get('contributions', []) if c['classification']=='original' and c['authorization'].strip()}
    def add(code,message,path='',node_id=None):errors.append(diagnostic(code,message,path,node_id))
    sources={s['source_id'] for k in ids for s in inv.nodes[k].meta['sources'] if s['role']=='support'}
    for sid in sorted(sources):
        s=inv.sources[sid];a=s['access'];p=inv.source_paths[sid]
        if s['kind']!='primary':
            add('SOURCE_REVIEW_MISSING','Supplied manuscript is provenance, not original-source verification',p);continue
        if s.get('version_conflicts'):
            add('SOURCE_VERSION_CONFLICT','Unresolved source-version candidates remain; resolve identities and locators before release',p)
        if not s['version']:
            add('SOURCE_VERSION_CONFLICT','Record the exact controlling version, not an inferred latest version',p)
        r,diagnostics=find_review(inv.root,records,'source','source_ids',sid,source_inputs(inv,sid));errors.extend(diagnostics)
        if a['state']!='full_text_read' or not valid_date(a['checked_at']) or not a.get('reading_note') or r is None:
            add('SOURCE_REVIEW_MISSING','Need actual original-text reading, dated locators and an accepted input-bound review',p)
        if a.get('local_path'):
            if not a.get('material_sha256') or file_hash(inv.root,a['local_path'])!=a['material_sha256']:
                add('SOURCE_MATERIAL_MISMATCH','Local source bytes differ from the declared original material hash',p)
        else:
            reading=mapping(mapping((r or {}).get('scope',{}).get('source_reading')).get(sid))
            locators=reading.get('locators')
            valid= (a.get('material_hash_unavailable_reason') and s['identifiers'].get('url') and
                    reading.get('mode')=='original_text_online' and reading.get('version')==s['version'] and
                    isinstance(locators,list) and locators and all(isinstance(x,str) and x.strip() for x in locators)
                    and reading.get('raw_bytes_unavailable_reason'))
            if not valid:add('SOURCE_REVIEW_MISSING','No retained raw file: require an explicit original-text online reading scope, exact version, locator list and material-access limitation',p)
            elif a.get('material_sha256'):
                warnings.append(diagnostic('SOURCE_RAW_BYTES_NOT_RETAINED','A raw-source hash is recorded, but no in-project copy is available to rehash; source reading is documented with this retention limitation.',p))
            else:warnings.append(diagnostic('SOURCE_RAW_HASH_UNAVAILABLE','Original text was read online; no raw-source hash or retained byte copy is available.',p))
        if r:used.append(r['review_id'])
    for key in sorted(ids):
        n=inv.nodes[key];m=n.meta
        if m['mathematical_status']=='unassessed':add('MATHEMATICAL_REVIEW_PENDING','Node remains mathematically unassessed',n.path,key)
        if m['origin'] in {'supplied_manuscript','primary_source'} and not (m['origin']=='supplied_manuscript' and key in supplied_originals) and not any(s['role']=='support' and inv.sources[s['source_id']]['kind']=='primary' for s in m['sources']):
            add('SOURCE_REVIEW_MISSING','Imported/primary claim needs an original supporting source, not only an attachment',n.path,key)
        principal_check = four_modes(plan) and key in principals
        if principal_check: warnings.extend(statement_warnings(key, n.statement))
        def candidate_check(r, key=key, n=n, principal_check=principal_check):
            # Select a review satisfying this plan, not merely the first valid
            # historical reading of these bytes. A different mode can promise
            # different steps without changing the authoritative statement.
            found = statement_errors(key, n.statement, r) if principal_check else []
            promised = set(obligations.get(key, {}).get('required_steps', []))
            done = r.get('scope', {}).get('proof_steps', {}).get(key, [])
            missing = promised - set(done)
            if missing:
                found.append(diagnostic('PROOF_OBLIGATION_UNMET',
                    'Candidate mathematical review omits promised steps: ' + '; '.join(sorted(missing)), n.path, key))
            return found
        r,diagnostics=find_review(inv.root,records,'mathematical','node_ids',key,mathematical_inputs(inv,key),extra_check=candidate_check); errors.extend(diagnostics)
        if principal_check and r is None: errors.extend(statement_errors(key,n.statement,{}))
        if not r:add('MATHEMATICAL_REVIEW_PENDING','Need an accepted mathematical reading of the node and necessary fixed inputs',n.path,key)
        else:
            valid_math[key]=r;used.append(r['review_id'])
            if (m['origin']=='local_derivation' or key in supplied_originals) and not r.get('scope',{}).get('evidence_basis'):
                add('MATHEMATICAL_REVIEW_PENDING','Local derivation review must state its actual proof basis',n.path,key)
        if m['mathematical_status']=='open':
            searches=(r or {}).get('scope',{}).get('reverse_search',{}).get(key,[])
            if not searches or not all(isinstance(x,dict) and valid_date(x.get('searched_at')) and x.get('query') and x.get('outcome') for x in searches):
                add('OPEN_STATUS_UNVERIFIED','An open claim needs actual dated follow-up searches and an exact remaining target',n.path,key)
    for qid in plan['question_ids']:
        q=next((x for x in inv.coverage['questions'] if x['question_id']==qid),None)
        gaps=[] if q is None else [g for g in q['gaps'] if not (isinstance(g,dict) and g.get('disposition') in {'resolved','outside_explicit_scope'} and g.get('reason'))]
        if q is None or q['assessment'] not in {'adequate','limited'} or gaps:
            add('COVERAGE_PENDING','Selected question coverage or important gaps remain unresolved',inv.project['knowledge_root']+'/coverage.json',qid)
        from .reviews import knowledge_scope_errors
        check = (lambda r, qid=qid: knowledge_scope_errors(inv, qid, r)) if current(plan) else None
        r,diagnostics=find_review(inv.root,records,'coverage','question_ids',qid,coverage_inputs(inv,qid),extra_check=check);errors.extend(diagnostics)
        if r is None:add('COVERAGE_PENDING','Need actual omission challenge and overview/scope/coverage review',node_id=qid)
        else:used.append(r['review_id'])
    obligations={o['node_id']:o for o in plan['proof_obligations']}
    for selection in plan['selections']:
        if selection['proof_treatment'] in {'sketch','mechanism'}:
            key=selection['node_id']
            mechanisms=[e['target'] for e in inv.nodes[key].meta['links'] if e['relation']=='explained_by']
            if key not in obligations and not (mechanisms and all(m in obligations for m in mechanisms)):
                add('PROOF_OBLIGATION_UNMET','A promised sketch or mechanism requires substantive step obligations before formal readiness',node_id=key)
    for o in plan['proof_obligations']:
        r=valid_math.get(o['node_id']);done=(r or {}).get('scope',{}).get('proof_steps',{}).get(o['node_id'],[])
        missing=set(o['required_steps'])-set(done)
        if missing:add('PROOF_OBLIGATION_UNMET','Mathematical review does not cover promised steps: '+ '; '.join(sorted(missing)),node_id=o['node_id'])
    # Deduplicate recurring stale diagnostics while retaining all distinct causes.
    unique=[];seen=set()
    for e in errors:
        k=(e['code'],e['path'],e['node_id'],e['message'])
        if k not in seen:seen.add(k);unique.append(e)
    return result('kb.readiness','NEEDS_WORK' if unique else 'READY',{'snapshot_id':plan['snapshot_id'],'consumed_nodes':sorted(ids),'used_review_ids':sorted(set(used))},unique,warnings)
