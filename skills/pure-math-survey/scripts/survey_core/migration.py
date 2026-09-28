"""Conservative v1 import into a new atomic directory; never inherit old PASS."""
from __future__ import annotations
from pathlib import Path
import csv
import difflib
import json
import re
import shutil
import tempfile
from .common import VERSION,all_files,atomic_bytes,file_hash,file_inventory,read_json,require,result,safe,sha,write_json
from .knowledge import init_project,inventory
from .models import load_node
from .snapshots import freeze_snapshot

def node_bytes(meta:dict,body:str)->bytes:
    return ('---\n'+json.dumps(meta,ensure_ascii=False,indent=2)+'\n---\n\n'+body.rstrip()+'\n').encode('utf-8')

def migrate_v1(old:Path,new:Path)->dict:
    old=old.absolute();new=new.absolute()
    require(old.is_dir() and not new.exists(),'DESTINATION_EXISTS','Migration requires existing input and a new destination')
    require(old!=new and old not in new.parents and new not in old.parents,'UNSAFE_PATH','Do not nest migration output inside its source')
    require(not (old/'project.json').exists(),'MIGRATION_NOT_V1','Native v2 project must not be interpreted as v1')
    original=file_inventory(old,all_files(old));new.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.migrate-',dir=new.parent));work=stage/'project'
    manifest=read_json(old/'project-manifest.json') if (old/'project-manifest.json').is_file() else {}
    title=manifest.get('topic') or manifest.get('title') or old.name
    if not isinstance(title,str):title=old.name
    report={'schema_version':VERSION,'status':'IMPORTED_UNVERIFIED','original_hashes':original,'items':[],'ambiguities':[],
            'manual_requirements':['Recover ordered quantifiers and surrounding definition scope.','Read original sources and resolve version/locator conflicts.',
                                   'Review imported mathematical candidates and proof mechanisms before assigning established status.',
                                   'Review question coverage; all historical PASS records remain provenance only.'],
            'historical_cutoff':manifest.get('literature_cutoff') or manifest.get('cutoff'),'unmigrated':[]}
    try:
        scope=stage/'scope.md'
        recovered=next((p for p in ('architecture.md','scope.md') if (old/p).is_file()),None)
        scope.write_text('# Migrated scope (unreviewed)\n\n'+(safe(old,recovered,True).read_text(encoding='utf-8') if recovered else 'Topic: '+title+'\n\nVariables, quantifiers and exclusions still require reconstruction from the preserved originals.'),encoding='utf-8')
        init_project(work,'migrated-'+re.sub('[^A-Za-z0-9._-]','-',old.name),scope,title)
        for f in original:atomic_bytes(work/'legacy/original'/f['path'],safe(old,f['path'],True).read_bytes())
        write_json(work/'knowledge/sources/S-imported.json',{'schema_version':VERSION,'id':'S-imported','kind':'supplied_manuscript','title':title,'authors':[],
                   'publication_status':'unknown','identifiers':{'user_file':old.name},'version':'Preserved v1 input; historical claims not reverified',
                   'access':{'state':'metadata_only','checked_at':None,'material_sha256':None,'local_path':None}})
        qid='N-imported-question'
        base={'schema_version':VERSION,'id':qid,'kind':'question','title':'Imported question requiring reconstruction','facets':['foundations'],
              'question_ids':[],'mathematical_status':'unassessed','origin':'supplied_manuscript',
              'sources':[{'source_id':'S-imported','locator':recovered or 'project-manifest.json / manuscript opening','role':'provenance'}],'links':[]}
        atomic_bytes(work/f'knowledge/nodes/{qid}.md',node_bytes(base,'# Imported scope\n\nRead scope.md and legacy/original/. No ordered quantifier reconstruction has yet been accepted.'))
        source_map={};bibtext='\n'.join(safe(old,f['path'],True).read_text(encoding='utf-8',errors='replace') for f in original if f['path'].endswith('.bib'))
        # BibTeX entry boundaries, not a claim of full TeX semantic parsing.
        entries=re.split(r'(?m)^\s*@',bibtext)
        for part in entries[1:]:
            m=re.match(r'(\w+)\s*\{\s*([^,\s]+),',part)
            if not m:continue
            key=m[2];sid='S-bib-'+re.sub('[^A-Za-z0-9._-]','-',key)
            if sid in source_map.values():report['ambiguities'].append({'source':key,'reason':'Duplicate bibliographic key/version; manual identity merge required.'});continue
            source_map[key]=sid
            def field(name):
                x=re.search(r'\b'+name+r'\s*=\s*\{(.*?)\}\s*(?:,|\n|$)',part,re.S|re.I)
                return re.sub(r'\s+',' ',x[1]).strip() if x else ''
            write_json(work/f'knowledge/sources/{sid}.json',{'schema_version':VERSION,'id':sid,'kind':'primary','title':field('title') or key,
                       'authors':[x.strip() for x in field('author').split(' and ') if x.strip()],'publication_status':'unknown',
                       'identifiers':{'legacy_bibtex_key':key,**({'doi':field('doi')} if field('doi') else {}),**({'url':field('url')} if field('url') else {})},
                       'version':None,'access':{'state':'metadata_only','checked_at':None,'material_sha256':None,'local_path':None}})
            report['items'].append({'source':'references.bib:'+key,'destination':f'knowledge/sources/{sid}.json','action':'Identity candidate only; no original-text reading or publication status inferred.'})
        # Retain controlling-version assertions as unverified metadata, never as new source reading.
        identity=old/'bibliographic-identity.csv'
        if identity.is_file():
            with identity.open(encoding='utf-8-sig',newline='') as stream: identity_rows=list(csv.DictReader(stream))
            for i,row in enumerate(identity_rows,2):
                key=row.get('source_id') or row.get('key')
                if not key:report['ambiguities'].append({'source':f'bibliographic-identity.csv:{i}','reason':'Missing source ID; row retained for manual reconciliation.'});continue
                sid=source_map.get(key,'S-bib-'+re.sub('[^A-Za-z0-9._-]','-',key));source_map[key]=sid
                p=work/f'knowledge/sources/{sid}.json'
                if p.exists():src=read_json(p)
                else:src={'schema_version':VERSION,'id':sid,'kind':'primary','title':row.get('title') or key,'authors':[a.strip() for a in row.get('authors','').split(';') if a.strip()],
                          'publication_status':'unknown','identifiers':{'legacy_source_id':key},'version':None,'access':{'state':'metadata_only','checked_at':None,'material_sha256':None,'local_path':None}}
                version=row.get('controlling_version') or row.get('arxiv_version') or None
                if src.get('version') and version and src['version']!=version:
                    report['ambiguities'].append({'source':f'bibliographic-identity.csv:{i}','code':'SOURCE_VERSION_CONFLICT','reason':'Different controlling versions remain unresolved.'})
                    src['version_conflicts']=[src['version'],version];src['version']=None
                elif version:src['version']=version
                for col,target in [('url','url'),('doi','doi'),('arxiv_id','arxiv')]:
                    if row.get(col):
                        if src['identifiers'].get(target) and src['identifiers'][target]!=row[col]:
                            report['ambiguities'].append({'source':f'bibliographic-identity.csv:{i}','code':'SOURCE_VERSION_CONFLICT','reason':f'Conflicting {target}; original values retained in legacy material.'})
                        else:src['identifiers'][target]=row[col]
                src['imported_identity_assertion']={'source':f'legacy/original/bibliographic-identity.csv:{i}','historical_locator':row.get('locator'),
                                                    'historical_checked_at':row.get('verified_on'),'not_reverified':True}
                write_json(p,src);report['items'].append({'source':f'bibliographic-identity.csv:{i}','destination':p.relative_to(work).as_posix(),'action':'Unverified identity/version assertion; old checked date is not a new access date.'})
        publication=[]
        if (old/'publication-map.csv').is_file():
            with (old/'publication-map.csv').open(encoding='utf-8-sig',newline='') as stream:publication=list(csv.DictReader(stream))
        candidate_mapping={}
        candidates=[]
        for f in original:
            if not f['path'].endswith('.tex'):continue
            raw=safe(old,f['path'],True).read_text(encoding='utf-8')
            pattern=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}',re.S)
            found=list(pattern.finditer(raw))
            for m in found:candidates.append((f['path'],raw[:m.start()].count('\n')+1,m[1],m[2],m.group()))
            if not found and ('canonical' in f['path'] or 'components' in Path(f['path']).parts) and raw.strip():
                candidates.append((f['path'],1,'theorem',raw,raw))
        ids=[]
        for index,(path,line,env,body,wrapped) in enumerate(candidates,1):
            key=f'N-import-{index:03d}';loc=f'{path}:{line}'
            no_labels=re.sub(r'\\label\s*\{[^{}]*\}','',body)
            diffs=[]
            for kind,before,after in [('wrappers',wrapped,body),('labels',body,no_labels)]:
                if before!=after:
                    diff=''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile=loc,tofile=key+':'+kind))
                    dpath=f'evidence/migration-diffs/{key}.{kind}.diff';atomic_bytes(work/dpath,diff.encode())
                    diffs.append({'kind':kind,'path':dpath,'before_sha256':sha(before.encode()),'after_sha256':sha(after.encode())})
            labels=re.findall(r'\\label\s*\{([^{}]*)\}',body)
            matches=[row for row in publication if row.get('canonical_component')==path or row.get('node_id') in labels or any(row.get(c) in labels for c in ('concise_label','standard_label','integrated_concise_label','integrated_standard_label'))]
            imported_facets=set(['foundations'] if env=='definition' else ['results'])
            for row in matches:
                facet={'1':'foundations','2':'results','3':'methods','4':'boundaries'}.get(str(row.get('owner_part')))
                if facet:imported_facets.add(facet)
                if row.get('node_id'):candidate_mapping[row['node_id']]=key
            sources=[{'source_id':'S-imported','locator':loc,'role':'provenance'}]
            for cite in re.findall(r'\\cite\w*\s*(?:\[[^\]]*\]\s*)*\{([^{}]+)\}',body):
                for k in cite.split(','):
                    if k.strip() in source_map:sources.append({'source_id':source_map[k.strip()],'locator':'Imported citation '+k.strip()+'; exact original theorem locator unverified','role':'support'})
            for row in matches:
                for source_key in re.split('[;,]',row.get('source_ids','')):
                    if source_key in source_map and not any(x['source_id']==source_map[source_key] for x in sources):
                        sources.append({'source_id':source_map[source_key],'locator':'Legacy publication map; exact original support unverified','role':'support'})
            meta={**base,'id':key,'kind':'definition' if env=='definition' else 'result','title':f'Imported {env} candidate {index}',
                  'facets':sorted(imported_facets),'question_ids':[qid],'sources':sources}
            text='# '+meta['title']+'\n\n## Canonical statement\n\n```latex\n'+no_labels.strip('\r\n')+'\n```\n\n## Import limitations\n\n'+loc+' is preserved in legacy/original/. Adjacent definitions, source locators, citation-key mappings, dependencies and mathematical validity require manual review.\n'
            target=work/f'knowledge/nodes/{key}.md';atomic_bytes(target,node_bytes(meta,text))
            try:load_node(target)
            except Exception as e:
                target.unlink();report['ambiguities'].append({'source':loc,'reason':'Unsupported canonical candidate retained only in original: '+str(e)});continue
            ids.append(key);report['items'].append({'source':loc,'destination':target.relative_to(work).as_posix(),'action':'Unassessed mathematical candidate; labels/wrappers removed only as individually recorded.','byte_changes':diffs})
        report['legacy_node_mapping']=candidate_mapping
        # CSV identities, proof and frontier rows remain authoritative only as historical evidence.
        for f in original:
            if f['path'].endswith('.csv'):
                with safe(old,f['path'],True).open(encoding='utf-8-sig',newline='') as stream:
                    rows=list(csv.DictReader(stream))
                if 'proof-mechanism' in f['path']:
                    for i,row in enumerate(rows,1):
                        key=f'N-mechanism-{i:03d}'
                        meta={**base,'id':key,'kind':'mechanism','title':'Imported proof mechanism candidate','facets':['methods'],'question_ids':[qid]}
                        atomic_bytes(work/f'knowledge/nodes/{key}.md',node_bytes(meta,'# Mechanism candidate\n\nHistorical row (not a complete proof):\n\n```json\n'+json.dumps(row,ensure_ascii=False,indent=2)+'\n```\n\nInputs, outputs and substantive steps must be reconstructed; no review accepted.'))
                report['unmigrated'].append({'source':f['path'],'destination':'legacy/original/'+f['path'],'reason':'Rows preserved for manual identity/dependency/placement reconciliation; historical status not promoted.'})
        for required in ('project-manifest.json','release-audit.csv','bibliographic-identity.csv'):
            if not (old/required).is_file():report['ambiguities'].append({'source':required,'reason':'Missing legacy field/table; import continues without manufacturing evidence.'})
        write_json(work/'knowledge/coverage.json',{'schema_version':VERSION,'questions':[{'question_id':qid,'answer_nodes':ids,'mechanism_nodes':[], 'boundary_nodes':[],
                   'gaps':['Reconstruct problem scope and original source support.','Identify necessary dependencies and decisive boundaries.'],'assessment':'pending','rationale':'Import preserves historical material but does not certify its mathematics or completeness.'}]})
        atomic_bytes(work/'knowledge/overview.md',('# Imported knowledge\n\n[['+qid+']] anchors the imported scope. '+str(len(ids))+' statement candidates are preserved without mathematical approval.\n\nReview the original context, reconstruct inputs and relationships, and challenge omissions before selecting an output. Historical PDFs are not native v2 releases.\n').encode())
        atomic_bytes(work/'knowledge/discovery.md',b'# Import provenance\n\nNo new literature search has been performed by migration. Original bibliography and any dated searches remain in legacy/original/; they are not upgraded to current reading evidence.\n')
        for i,row in enumerate(publication,2):
            key=row.get('node_id','')
            if key and key not in candidate_mapping:
                report['ambiguities'].append({'source':f'publication-map.csv:{i}','reason':'No safe canonical/inline statement candidate matched '+key+'; reconstruct manually from preserved original.'})
        report['node_candidates']=len(ids);report['source_map']=source_map
        report['historical_page_limit']=manifest.get('page_limit')
        if manifest.get('page_limit') is not None and manifest.get('max_pages') is None:
            report['ambiguities'].append({'source':'project-manifest.json:page_limit','reason':'Historical page_limit preserved but explicit user max_pages provenance is unclear; new max_pages remains null.'})
        inventory(work)
        sid=freeze_snapshot(work)['artifacts']['snapshot_id'];report['snapshot_id']=sid
        # Preserve legacy selections as draft plan proposals, never as reviewed outputs.
        documents=manifest.get('documents',[])
        for i,d in enumerate(documents if isinstance(documents,list) else [],1):
            if not isinstance(d,dict) or not ids:continue
            part=str(d.get('part',5));edition=d.get('edition','concise')
            view={'1':'foundations','2':'results','3':'methods','4':'boundaries'}.get(part,'integrated')
            profile='minimal' if part=='5' and edition=='concise' else 'thematic'
            from .plans import create_plan
            proposal=create_plan(work,f'legacy-{i}',sid,profile,view,[qid],ids,draft=True,max_pages=d.get('max_pages',manifest.get('max_pages')))
            report['items'].append({'source':f'project-manifest.json:documents[{i-1}]','destination':proposal['artifacts']['plan'],'action':'Draft proposal; preserve old reading depth during manual revision.','historical_edition':edition})
        write_json(work/'MIGRATION_REPORT.json',report)
        require(file_inventory(old,[x['path'] for x in original])==original,'MIGRATION_SOURCE_CHANGED','Input changed during migration')
        work.rename(new)
    finally:shutil.rmtree(stage,ignore_errors=True)
    return result('migrate','IMPORTED_UNVERIFIED',{'project':str(new),'report':'MIGRATION_REPORT.json','node_candidates':report['node_candidates'],'snapshot_id':report['snapshot_id'],'ambiguities':report['ambiguities']})
