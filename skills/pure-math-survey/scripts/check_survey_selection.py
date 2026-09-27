#!/usr/bin/env python3
"""Check declared selection/discovery traceability, not mathematical completeness."""
from __future__ import annotations
import argparse,csv,hashlib,json,re
from datetime import date
from pathlib import Path,PurePosixPath
ROLES={'principal-answer','essential-bridge','boundary-result','secondary-independent-result','background-context'}
STATUSES={'SOLVED','REFUTED','VERIFIED_OPEN','STATUS_UNVERIFIED'}
DISPOSITIONS={'INCLUDE','CONTEXT','OMIT'}
KINDS={'precise-question','research-direction','refuted-formulation'}
ACTIVITIES={'discovery_search','followup_search','source_read'}
LABEL=re.compile(r'\\label\s*\{([^}]+)\}')
def norm(value:str)->str:return re.sub(r'\s+',' ',value).strip()
def digest(value)->str:return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def useful(value,minimum=12)->bool:return isinstance(value,str) and len(value.strip())>=minimum and not re.search(r'\b(PENDING|TODO|TBD)\b',value,re.I) and value.strip().upper() not in {'PASS','VERIFIED','COMPLETE'}
def split(value:str)->set[str]:return {v.strip() for v in re.split('[;,]',value or '') if v.strip()}
def read_rows(root:Path,name:str,errors:list[str])->list[dict]:
 try:
  with (root/name).open(encoding='utf-8-sig',newline='') as f:
   reader=csv.DictReader(f);rows=list(reader)
   if len(reader.fieldnames or [])!=len(set(reader.fieldnames or [])):errors.append(name+': duplicate columns')
  if any(None in row or any(v is None for v in row.values()) for row in rows):errors.append(name+': malformed row width')
  return rows
 except (OSError,csv.Error,UnicodeError) as exc:errors.append(f'{name}: {exc}');return []
def keyed(rows,key,errors):
 result={}
 if not isinstance(rows,list):errors.append(f'{key}: expected a list of records');return result
 for row in rows:
  if not isinstance(row,dict):errors.append(f'{key}: expected an object record');continue
  identity=row.get(key,'')
  if not isinstance(identity,str):errors.append(f'{key}: identity must be a string');continue
  if not identity or identity in result:errors.append(f'empty/duplicate {key}: {identity!r}')
  else:result[identity]=row
 return result

def local_file(root:Path,name:str)->Path|None:
 if not isinstance(name,str) or not name or '\\' in name or ':' in name:return None
 p=PurePosixPath(name)
 if p.is_absolute() or any(x in {'','.','..'} for x in name.split('/')):return None
 target=root/name
 try:target.resolve().relative_to(root.resolve())
 except ValueError:return None
 return target if target.is_file() and target.stat().st_size else None

def span(text:str,start:str,end:str)->str:
 labels=list(LABEL.finditer(text));starts=[m for m in labels if m.group(1)==start];ends=[m for m in labels if m.group(1)==end]
 if len(starts)!=1 or len(ends)!=1 or starts[0].end()>=ends[0].start():raise ValueError(f'nonunique, missing or reversed binding {start!r} -> {end!r}')
 return norm(text[starts[0].end():ends[0].start()])
def span_digest(text,start,end):return hashlib.sha256(span(text,start,end).encode()).hexdigest()
def plan_digest(model,mappings,claims,searches):
 selected={k:v for k,v in model.items() if k not in {'bindings','review','reviewed_plan_sha256'}}
 claims=[{k:v for k,v in r.items() if k!='body_binding_ids'} for r in claims]
 return digest({'selection':selected,'publication_map':mappings,'frontier_claims':claims,'research_activities':searches})
def validate_selection(root:Path,manifest:dict,expanded:dict,stage='release'):
 errors=[];notes=[];docs=manifest.get('documents',[])
 mappings=read_rows(root,'publication-map.csv',errors);nodes=keyed(mappings,'node_id',errors)
 sources=keyed(read_rows(root,'bibliographic-identity.csv',errors),'source_id',errors)
 proofs=keyed(read_rows(root,'proof-mechanism-registry.csv',errors),'proof_id',errors)
 needs_frontier=any(d.get('part') in (4,5) for d in docs)
 claims=read_rows(root,'frontier-claim-registry.csv',errors) if needs_frontier else []
 searches=read_rows(root,'frontier-reverse-search.csv',errors) if needs_frontier else []
 frontier=keyed(claims,'frontier_id',errors);activities=keyed(searches,'query_id',errors)
 for sid,row in activities.items():
  activity=row.get('activity')
  if activity not in ACTIVITIES:errors.append(f'{sid}: unknown/missing research activity')
  if not row.get('platform') or not useful(row.get('exact_query')):errors.append(f'{sid}: missing actual query/read locator or platform')
  query=(row.get('exact_query') or '').strip()
  if activity in {'discovery_search','followup_search'} and re.fullmatch(r'https?://\S+',query):errors.append(f'{sid}: URL-only source read cannot count as a search')
  try:date.fromisoformat(str(row.get('retrieved_at',''))[:10])
  except ValueError:errors.append(f'{sid}: missing/invalid actual retrieval date')
  if local_file(root,row.get('saved_evidence','')) is None:errors.append(f'{sid}: missing/unsafe saved evidence file')
  if not useful(row.get('finding')) or not useful(row.get('disposition')):errors.append(f'{sid}: record actual findings and their use/limitations')
  if not row.get('result_count_or_not_exposed'):errors.append(f'{sid}: state result count or not-exposed')
  if split(row.get('source_ids',''))-set(sources):errors.append(f'{sid}: unknown research source identity')
  if split(row.get('frontier_id',''))-set(frontier)-{'*'}:errors.append(f'{sid}: unknown linked frontier')
 for fid,row in frontier.items():
  status=row.get('status')
  if status not in STATUSES:errors.append(f'{fid}: status must describe knowledge, not editorial scope')
  if row.get('formulation_kind') not in KINDS:errors.append(f'{fid}: missing exact-question/direction/refuted distinction')
  if row.get('editorial_disposition') not in DISPOSITIONS:errors.append(f'{fid}: missing independent editorial disposition')
  for key in ('claim','scope','known_range','remaining_target','importance','editorial_reason'):
   if not useful(row.get(key)):errors.append(f'{fid}: missing substantive {key}')
  if status=='VERIFIED_OPEN' and row.get('formulation_kind')!='precise-question':errors.append(f'{fid}: only a precise sourced target can be VERIFIED_OPEN')
  if row.get('formulation_kind')=='refuted-formulation' and status!='REFUTED':errors.append(f'{fid}: a refuted formulation must not be called open')
  src=split(row.get('source_ids',''))
  if src-set(sources) or (not src and row.get('editorial_disposition')!='OMIT'):errors.append(f'{fid}: missing/unknown primary source IDs')
  linked=split(row.get('reverse_search_ids',''))
  if linked-set(activities):errors.append(f'{fid}: unknown search/read IDs')
  if status=='VERIFIED_OPEN' and not any(activities.get(q,{}).get('activity')=='followup_search' for q in linked):errors.append(f'{fid}: verified-open claim lacks actual follow-up search')
  for q in linked&set(activities):
   if fid not in split(activities[q].get('frontier_id','')) and '*' not in split(activities[q].get('frontier_id','')):errors.append(f'{fid}: search {q} is linked to a different frontier')
 cores={}
 for doc in docs:
  name=doc.get('tex_file','');review_path=local_file(root,doc.get('structure_review',''))
  try:review=json.loads(review_path.read_text(encoding="utf-8-sig")) if review_path else {}
  except (OSError,ValueError) as exc:errors.append(f'{name}: invalid structure review: {exc}');continue
  model=review.get('survey_selection')
  if not isinstance(model,dict) or model.get('schema_version')!='1.0.0':errors.append(f'{name}: missing survey_selection in existing reader evidence');continue
  questions=keyed(model.get('questions',[]),'id',errors)
  if not questions:errors.append(f'{name}: organizing questions have not been selected')
  for qid,q in questions.items():
   for field in ('statement','scope','current_answer','desired_answer','gap','priority_reason'):
    if not useful(q.get(field)):errors.append(f'{name}/{qid}: missing answer-gap contrast: {field}')
  local_nodes={};prefixes=[doc.get('edition',''),'integrated_'+doc.get('edition','')]
  for node,row in nodes.items():
   if not any(row.get(p+'_file')==name for p in prefixes):continue
   local_nodes[node]=row
   if row.get('kind','') in {'problem','question','conjecture'}:
    if row.get('result_role'):errors.append(f'{node}: frontier questions are not result roles')
    continue
   if row.get('result_role') not in ROLES:errors.append(f'{node}: missing question-relative result role')
   qids=split(row.get('question_ids',''))
   if not qids or qids-set(questions):errors.append(f'{node}: missing/unknown question link')
   if not useful(row.get('selection_reason')):errors.append(f'{node}: missing selection reason')
   consumers=split(row.get('consumer_ids',''))
   if consumers-set(nodes)-set(frontier)-set(questions):errors.append(f'{node}: unknown consumer')
   if row.get('result_role')=='essential-bridge' and not consumers:errors.append(f'{node}: essential bridge has no declared consumer')
  for field,known in [('core_result_ids',nodes),('core_mechanism_ids',proofs),('core_frontier_ids',frontier)]:
   values=model.get(field,[])
   if not isinstance(values,list) or not all(isinstance(v,str) for v in values) or len(set(values))!=len(values) or set(values)-set(known):errors.append(f'{name}: invalid {field}')
  declared_core=model.get('core_result_ids',[])
  if isinstance(declared_core,list) and all(isinstance(v,str) for v in declared_core):
   for node,row in local_nodes.items():
    if row.get('result_role')=='principal-answer' and node not in declared_core:
     errors.append(f'{name}: principal answer {node} is absent from the declared shared core')
  for node in model.get('core_result_ids',[]):
   row=nodes.get(node,{})
   if not any(row.get(p+'_file')==name and row.get(p+'_treatment')=='FULL_STATEMENT' for p in prefixes):errors.append(f'{name}: shared-core result {node} lacks a full statement')
  used_proofs=set().union(*(split(r.get('proof_ids','')) for r in local_nodes.values())) if local_nodes else set()
  if set(model.get('core_mechanism_ids',[]))-used_proofs:errors.append(f'{name}: core mechanism has no mapped consumer')
  discovery=model.get('discovery',{})
  for field in ('scope','starting_points','omission_challenge','stop_reason','limitations'):
   if not useful(discovery.get(field)):errors.append(f'{name}: incomplete source-first discovery review: {field}')
  if doc.get('part') in (4,5):
   qids=set(discovery.get('search_ids',[]));fids=set(discovery.get('candidate_ids',[]))
   if qids-set(activities) or fids-set(frontier):errors.append(f'{name}: discovery names nonexistent searches/candidates')
   if not any(activities.get(q,{}).get('activity')=='discovery_search' for q in qids):errors.append(f'{name}: source reads alone cannot establish frontier discovery')
   if not fids and not useful(discovery.get('no_candidate_reason')):errors.append(f'{name}: zero candidates needs an evidenced scope explanation')
   if set(model.get('core_frontier_ids',[]))-fids:errors.append(f'{name}: core frontier absent from discovery portfolio')
  for rejected in model.get('rejected_results',[]):
   if not all(useful(rejected.get(k)) for k in ('candidate','reason','role_assessment')):errors.append(f'{name}: rejected result lacks a substantive relevance decision')
  expected=plan_digest(model,mappings,claims,searches);notes.append(f'{name}: selection-plan SHA256 {expected}')
  if stage=='release':
   if model.get('reviewed_plan_sha256')!=expected:errors.append(f'{name}: selection/research plan changed since review')
   for field in ('question_priority','result_importance','frontier_coverage','edition_core','limitations'):
    if not useful(model.get('review',{}).get(field),25):errors.append(f'{name}: missing located editorial observation: {field}')
   text=expanded.get(name,'');bindings=keyed(model.get('bindings',[]),'id',errors)
   for bid,b in bindings.items():
    try:
     actual=span(text,b.get('start_label',''),b.get('end_label',''))
     if hashlib.sha256(actual.encode()).hexdigest()!=b.get('sha256'):errors.append(f'{name}/{bid}: reviewed source span changed')
     if not useful(b.get('quote')) or norm(b['quote']) not in actual:errors.append(f'{name}/{bid}: quote not in actual source span')
     if not useful(b.get('why')):errors.append(f'{name}/{bid}: binding lacks mathematical purpose')
    except ValueError as exc:errors.append(f'{name}/{bid}: {exc}')
   for fid in discovery.get('candidate_ids',[]):
    r=frontier.get(fid,{});bids=split(r.get('body_binding_ids',''))
    if r.get('editorial_disposition') in {'INCLUDE','CONTEXT'} and (not bids or not bids.issubset(bindings)):errors.append(f'{name}/{fid}: included frontier has no complete body bindings')
   pattern=re.compile(r'\\begin\{(theorem|proposition|lemma|corollary)\}(.*?)\\end\{\1\}',re.S)
   placed={r.get(p+'_label') for r in local_nodes.values() for p in prefixes if r.get(p+'_file')==name}
   sections=list(re.finditer(r'\\section\*?\{',text));opening_end=sections[1].start() if len(sections)>1 else len(text)
   for result in pattern.finditer(text):
    labels=LABEL.findall(result.group(2))
    if not labels or not any(label in placed for label in labels):errors.append(f'{name}: formal result has no importance mapping: {labels}')
   for node,row in local_nodes.items():
    if row.get('result_role')=='principal-answer':
     for p in prefixes:
      if row.get(p+'_file')==name:
       labels=[m for m in LABEL.finditer(text) if m.group(1)==row.get(p+'_label')]
       if not labels or labels[0].start()>opening_end:errors.append(f'{name}/{node}: principal answer not stated in the opening')
  signature={'questions':questions,**{key:sorted(model.get(key,[])) for key in ('core_result_ids','core_mechanism_ids','core_frontier_ids')}}
  cores.setdefault(doc.get('part'),[]).append((doc.get('edition'),signature))
 for part,pairs in cores.items():
  if len(pairs)==2 and digest(pairs[0][1])!=digest(pairs[1][1]):errors.append(f'Part {part}: concise/standard selected core or question scope differs')
 notes.append('Traceability only: no completeness, importance, search-authenticity or mathematical-truth certification.')
 return errors,notes

def main()->int:
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('--stage',choices=['plan','release'],default='release');a=p.parse_args()
 from validate_project import expand_tex
 try:
  root=a.project.resolve();manifest=json.loads((root/'project-manifest.json').read_text(encoding="utf-8-sig"));errors=[];expanded={}
  if a.stage=='release':
   for doc in manifest.get('documents',[]):
    tex=local_file(root,doc.get('tex_file',''))
    if tex is None:errors.append('missing/unsafe manuscript')
    else:expanded[doc['tex_file']]=expand_tex(tex,root,errors)[0]
  found,notes=validate_selection(root,manifest,expanded,a.stage);errors.extend(found)
 except (OSError,ValueError,TypeError,KeyError,AttributeError) as exc:errors,notes=[str(exc)],[]
 print(json.dumps({'stage':a.stage,'passed':not errors,'errors':errors,'notes':notes},indent=2));return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
