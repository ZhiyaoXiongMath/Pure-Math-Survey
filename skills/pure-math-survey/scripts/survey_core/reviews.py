"""Evidence binds actual bytes and an explicit scope; records are human assertions."""
from __future__ import annotations
from pathlib import Path
import re
from .common import VERSION, all_files, diagnostic, file_hash, read_json, require, relative, safe, valid_date
from .models import fields
from .dependencies import required_closure

def load_review(path: Path) -> dict:
    obj = read_json(path)
    fields(obj, {'review_id':str,'kind':str,'reviewer_mode':str,'inputs':list,'findings':list,'unchecked_items':list,'disposition':str}, path.name)
    if 'schema_version' in obj:
        require(obj['schema_version']==VERSION,'SCHEMA_UNSUPPORTED','Unsupported review schema',path.name)
    require(obj['kind'] in {'source','mathematical','coverage','output_semantic','visual'},'REVIEW_INVALID','Invalid review kind',path.name)
    require(obj['reviewer_mode'] in {'author_reread','independent_review','not_performed'},'REVIEW_INVALID','Do not label self-review independent',path.name)
    require(obj['disposition'] in {'accepted','revise','limited'} and 'reviewed_at' in obj,'REVIEW_INVALID','Invalid review disposition/date',path.name)
    require(obj['reviewed_at'] is None or valid_date(obj['reviewed_at']),'REVIEW_INVALID','Review date is not a real nonfuture date',path.name)
    require(obj['disposition']!='accepted' or (valid_date(obj['reviewed_at']) and obj['reviewer_mode']!='not_performed' and obj['findings']), 'REVIEW_INVALID','Accepted reviews require actual date, reviewer and findings',path.name)
    require(all(isinstance(x,str) and x.strip() for x in obj['findings']), 'REVIEW_INVALID', 'Findings must be substantive nonempty text entries',path.name)
    if obj['reviewer_mode']=='independent_review':
        require(isinstance(obj.get('reviewer'),str) and obj['reviewer'].strip(),'REVIEW_INVALID','An independent review must identify its actual reviewer; self-review is not independent',path.name)
    paths=[]
    for binding in obj['inputs']:
        fields(binding,{'path':str,'sha256':str},path.name); relative(binding['path'])
        require(re.fullmatch('[a-f0-9]{64}',binding['sha256']),'REVIEW_INVALID','Invalid binding hash',path.name)
        paths.append(binding['path'])
    require(len(paths)==len(set(paths)), 'REVIEW_INVALID','Duplicate input binding',path.name)
    require(isinstance(obj.get('scope',{}),dict),'REVIEW_INVALID','Review scope must be an object',path.name)
    return obj

def check_review_bindings(root: Path, review: dict, required: set[str] | None = None) -> list[dict]:
    errors=[]; paths=set()
    for binding in review['inputs']:
        p=binding['path']; paths.add(p); file=safe(root,p)
        if not file.is_file() or file_hash(root,p)!=binding['sha256']:
            errors.append(diagnostic('REVIEW_STALE',f"Review {review['review_id']} no longer matches this input",p))
    missing=(required or set())-paths
    if missing:
        errors.append(diagnostic('REVIEW_SCOPE_INSUFFICIENT',f"Review {review['review_id']} omits necessary inputs: {', '.join(sorted(missing))}"))
    return errors

def blocking_unchecked(review:dict)->list:
    return [v for v in review['unchecked_items'] if not (isinstance(v,dict) and v.get('blocking') is False and v.get('reason'))]

def reviews_in(root:Path, directory:str='evidence/reviews')->list[tuple[str,dict]]:
    result=[]
    for p in all_files(root,directory):
        if p.endswith('.json') and isinstance(read_json(safe(root,p,True)),dict) and 'review_id' in read_json(safe(root,p,True)):
            result.append((p,load_review(safe(root,p,True))))
    return result

def find_review(root:Path, records:list[tuple[str,dict]], kind:str, scope_field:str, key:str,
                required:set[str])->tuple[dict|None,list[dict]]:
    candidates=[]; diagnostics=[]
    for path,r in records:
        if r['kind']==kind and key in r.get('scope',{}).get(scope_field,[]):
            errors=check_review_bindings(root,r,required)
            if r['disposition']=='accepted' and not blocking_unchecked(r) and not errors:
                return r,[]
            candidates.append(r); diagnostics.extend(errors)
    return None,diagnostics

def source_inputs(inv, source_id:str)->set[str]:
    s=inv.sources[source_id]; out={inv.source_paths[source_id]}
    for field in ('reading_note','local_path'):
        if s['access'].get(field):out.add(s['access'][field])
    return out

def mathematical_inputs(inv,node_id:str)->set[str]:
    kr=inv.project['knowledge_root']; paths={'project.json',inv.project['scope_file'],kr+'/conventions.tex'}
    for key in required_closure(inv.nodes,{node_id}):
        paths.add(inv.nodes[key].path)
        for s in inv.nodes[key].meta['sources']:
            paths |= source_inputs(inv,s['source_id'])
    return paths

def coverage_inputs(inv,question_id:str)->set[str]:
    kr=inv.project['knowledge_root']
    paths={'project.json',inv.project['scope_file'],kr+'/coverage.json',kr+'/overview.md',kr+'/discovery.md',inv.nodes[question_id].path}
    for q in inv.coverage['questions']:
        if q['question_id']==question_id:
            for k in q['answer_nodes']+q['mechanism_nodes']+q['boundary_nodes']:
                paths.add(inv.nodes[k].path)
    return paths

def review_template(root:Path,kind:str,keys:list[str],required:set[str],scope:dict|None=None)->dict:
    return {'schema_version':VERSION,'review_id':'REPLACE-WITH-STABLE-REVIEW-ID','kind':kind,'reviewer_mode':'not_performed',
            'reviewed_at':None,'inputs':[{'path':p,'sha256':file_hash(root,p)} for p in sorted(required)],
            'scope':scope or { {'source':'source_ids','mathematical':'node_ids','coverage':'question_ids'}.get(kind,'output_ids'):keys},
            'findings':[],'unchecked_items':['Actual scoped reading and substantive findings have not been recorded.'], 'disposition':'revise'}
