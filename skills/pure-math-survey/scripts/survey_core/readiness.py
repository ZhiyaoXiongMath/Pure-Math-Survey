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
    errors=[];warnings=[];used=[]; valid_math={}
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
            reading=(r or {}).get('scope',{}).get('source_reading',{}).get(sid,{})
            valid= (a.get('material_hash_unavailable_reason') and s['identifiers'].get('url') and
                    reading.get('mode')=='original_text_online' and reading.get('version')==s['version'] and
                    reading.get('locators') and reading.get('raw_bytes_unavailable_reason'))
            if not valid:add('SOURCE_REVIEW_MISSING','Missing raw hash requires an explicit original-text online reading scope, exact version, locators and material-access limitation',p)
            else:warnings.append(diagnostic('SOURCE_RAW_HASH_UNAVAILABLE','Original text was read online; raw PDF bytes were not obtained or byte-certified',p))
        if r:used.append(r['review_id'])
    for key in sorted(ids):
        n=inv.nodes[key];m=n.meta
        if m['mathematical_status']=='unassessed':add('MATHEMATICAL_REVIEW_PENDING','Node remains mathematically unassessed',n.path,key)
        if m['origin'] in {'supplied_manuscript','primary_source'} and not any(s['role']=='support' and inv.sources[s['source_id']]['kind']=='primary' for s in m['sources']):
            add('SOURCE_REVIEW_MISSING','Imported/primary claim needs an original supporting source, not only an attachment',n.path,key)
        r,diagnostics=find_review(inv.root,records,'mathematical','node_ids',key,mathematical_inputs(inv,key)); errors.extend(diagnostics)
        if not r:add('MATHEMATICAL_REVIEW_PENDING','Need an accepted mathematical reading of the node and necessary fixed inputs',n.path,key)
        else:
            valid_math[key]=r;used.append(r['review_id'])
            if m['origin']=='local_derivation' and not r.get('scope',{}).get('evidence_basis'):
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
        r,diagnostics=find_review(inv.root,records,'coverage','question_ids',qid,coverage_inputs(inv,qid));errors.extend(diagnostics)
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
