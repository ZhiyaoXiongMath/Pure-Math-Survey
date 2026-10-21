"""Lean readable knowledge, source-byte enforcement and mechanical diagnostics."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import tempfile
from .common import VERSION, SOFTWARE_VERSION, RUNTIME_CONTRACT, all_files, atomic_bytes, canonical, diagnostic, file_inventory, read_json, require, result, safe, sha, write_json, writer, identifier
from .models import Node, fields, load_node, load_project, load_source, text
from .dependencies import detect_cycles

@dataclass
class Inventory:
    root: Path
    project: dict
    nodes: dict[str, Node]
    sources: dict[str, dict]
    source_paths: dict[str, str]
    routes: list[dict]
    files: list[str]


def inventory(root: Path) -> Inventory:
    root=root.absolute();project=load_project(root);kr=project['knowledge_root'];scope=project['scope_file']
    require(safe(root,scope,True).read_text(encoding='utf-8').strip(),'SCOPE_EMPTY','Describe scope and exclusions',scope)
    safe(root,kr+'/conventions.tex',True)
    nodes,sources,source_paths={},{},{}
    for path in all_files(root,kr+'/nodes'):
        require(path.endswith('.md'),'CONTRACT_INVALID','Only Markdown nodes belong in nodes/',path)
        node=load_node(safe(root,path,True),path)
        require(node.id not in nodes,'DUPLICATE_ID','Duplicate node',path,node.id);nodes[node.id]=node
    for path in all_files(root,kr+'/sources'):
        require(path.endswith('.json'),'CONTRACT_INVALID','Only JSON sources belong in sources/',path)
        source=load_source(safe(root,path,True),path);key=source['id']
        require(key not in sources,'DUPLICATE_ID','Duplicate source',path)
        sources[key],source_paths[key]=source,path
    keys=[s['citation_key'] for s in sources.values()]
    require(len(keys)==len(set(keys)),'DUPLICATE_ID','Citation keys must be unique',kr+'/sources')
    def source_ref(ref,path):
        fields(ref,{'source_id':str,'locator':str},path);text(ref['locator'],path,'locator')
        require(ref['source_id'] in sources,'UNKNOWN_REFERENCE','Unknown source '+ref['source_id'],path)
        if ref.get('version') is not None:
            require(ref['version']==sources[ref['source_id']]['version'],'SOURCE_VERSION_CONFLICT','Locator version differs from source record',path)
    for key,node in nodes.items():
        for dep in node.meta['definition_refs']:
            require(dep in nodes,'UNKNOWN_REFERENCE','Missing definition '+dep,node.path,key)
            require(nodes[dep].meta['kind']=='definition','DEFINITION_REFERENCE_INVALID','definition_refs must refer to definitions',node.path,key)
        for ref in node.meta['sources']:source_ref(ref,node.path)
    route_path=kr+'/routes.json';obj=read_json(safe(root,route_path,True));fields(obj,{'schema_version':str,'routes':list},route_path)
    seen=set()
    for route in obj['routes']:
        fields(route,{'id':str,'premise_sets':list,'target':str,'mapping':str,'status':str},route_path)
        require(identifier(route['id'],'R-') and route['id'] not in seen,'DUPLICATE_ID','Invalid or duplicate route ID',route_path);seen.add(route['id'])
        require(route['status'] in {'stated','extracted','unresolved'},'CONTRACT_INVALID','Invalid route status',route_path)
        require(route['target'] in nodes,'UNKNOWN_REFERENCE','Missing route target '+route['target'],route_path)
        require(nodes[route['target']].statement is not None,'METHOD_NOT_RESULT','Route targets need a formal conclusion',route_path)
        text(route['mapping'],route_path,'mapping')
        require(route['premise_sets'],'CONTRACT_INVALID','At least one premise set is required',route_path)
        for group in route['premise_sets']:
            fields(group,{'nodes':list,'additional_inputs':list},route_path)
            require(group['nodes'] and len(group['nodes'])==len(set(group['nodes'])),'CONTRACT_INVALID','Premise sets need unique node IDs',route_path)
            for key in group['nodes']:
                require(key in nodes,'UNKNOWN_REFERENCE','Missing route premise '+str(key),route_path)
            require(all(isinstance(v,str) and v.strip() for v in group['additional_inputs']),'CONTRACT_INVALID','Additional inputs must be explicit text',route_path)
        require('source_locator' in route,'CONTRACT_INVALID','Explicit source_locator or null is required',route_path)
        if route['source_locator'] is not None:source_ref(route['source_locator'],route_path)
        else:require(route['status']=='unresolved','CONTRACT_INVALID','Unsupported route must be unresolved',route_path)
    detect_cycles(nodes,obj['routes'])
    paths=set(['project.json',scope,kr+'/conventions.tex',route_path]+all_files(root,kr+'/nodes')+all_files(root,kr+'/sources'))
    for source in sources.values():
        for name in ('local_path','reading_note','permission_note'):
            path=source['access'].get(name)
            if path:safe(root,path,True);paths.add(path)
    inv=Inventory(root,project,nodes,sources,source_paths,obj['routes'],sorted(paths))
    from .sources import require_source_bytes
    require_source_bytes(inv)
    for path in paths:
        if path.endswith('.md'):
            for target in re.findall(r'\[\[([NS]-[A-Za-z0-9._-]+)\]\]',safe(root,path,True).read_text(encoding='utf-8')):
                require(target in nodes or target in sources,'UNKNOWN_REFERENCE','Broken readable link '+target,path)
    return inv


def limitations(inv: Inventory) -> list[str]:
    notes=['Mechanical checks do not certify mathematics or source reading.']
    notes += ['Unresolved source status: '+k for k,n in inv.nodes.items() if n.meta['source_status']=='unresolved']
    notes += ['Unresolved route: '+r['id'] for r in inv.routes if r['status']=='unresolved']
    return notes


def write_run(root: Path, inv: Inventory, output_paths=None, build_state='not_requested', pages=None, main_pages=None) -> None:
    notes=limitations(inv)
    if build_state=='not_built':notes.append('Prepared scaffold: authoring and build are not complete.')
    write_json(safe(root,'run.json'),{'software_version':SOFTWARE_VERSION,'runtime_contract':RUNTIME_CONTRACT,
        'source_versions':{k:s['version'] for k,s in sorted(inv.sources.items())},
        'input_hash':sha(canonical(file_inventory(inv.root,inv.files))), 'output_paths':output_paths or [],
        'status':'failed' if build_state=='failed' else ('incomplete' if len(notes)>1 else 'complete'),'known_limitations':notes,'build_state':build_state,
        'main_pages':main_pages,'total_pages':pages,'elapsed_seconds':None,'tokens':None,
        'unavailable':['elapsed_seconds','tokens']+(['main_pages'] if main_pages is None else [])+(['total_pages'] if pages is None else [])})


def validate_knowledge(root: Path) -> dict:
    inv=inventory(root)
    from .sources import source_facts
    return result('kb.validate','VALID',{'project_id':inv.project['project_id'],'node_count':len(inv.nodes),'source_count':len(inv.sources),
        'route_count':len(inv.routes),'outputs_required':False,'source_facts':[source_facts(inv,k) for k in sorted(inv.sources)]},
        warnings=[diagnostic('SEMANTIC_NOT_CERTIFIED',s) for s in limitations(inv)])


def init_project(destination: Path,topic: str,scope: Path,title=None,language='en') -> dict:
    require(identifier(topic),'CONTRACT_INVALID','Invalid project ID')
    require(not destination.exists(),'DESTINATION_EXISTS','Initialize into a new directory',destination.name)
    body=scope.read_bytes();require(body.strip(),'SCOPE_EMPTY','Scope must not be empty',scope.name)
    destination.parent.mkdir(parents=True,exist_ok=True);stage=Path(tempfile.mkdtemp(prefix='.survey-init-',dir=destination.parent))
    try:
        write_json(stage/'project.json',{'schema_version':VERSION,'runtime_contract':RUNTIME_CONTRACT,'project_id':topic,'title':title or topic,'language':language,'scope_file':'scope.md','knowledge_root':'knowledge'})
        atomic_bytes(stage/'scope.md',body)
        atomic_bytes(stage/'knowledge/conventions.tex',b'% Shared notation; no claims are certified.\n')
        write_json(stage/'knowledge/routes.json',{'schema_version':VERSION,'routes':[]})
        (stage/'knowledge/nodes').mkdir();(stage/'knowledge/sources').mkdir()
        atomic_bytes(stage/'knowledge/index.md',b'# Knowledge index\n\nNo units yet.\n')
        write_run(stage,inventory(stage));stage.rename(destination)
    finally:
        if stage.exists():shutil.rmtree(stage)
    return result('init','INITIALIZED',{'project':str(destination),'outputs':[]})


def index_knowledge(root: Path) -> dict:
    inv=inventory(root)
    lines=['# Knowledge index','','Derived navigation; canonical statements live in nodes/.','']
    lines += [f"- [{k}](nodes/{k}.md): {n.meta['title']} ({n.meta['kind']}; {n.meta['role']})" for k,n in sorted(inv.nodes.items())]
    with writer(root):
        atomic_bytes(safe(root,inv.project['knowledge_root']+'/index.md'),('\n'.join(lines)+'\n').encode('utf-8'));write_run(root,inv)
    return result('kb.index','INDEXED',{'path':inv.project['knowledge_root']+'/index.md','nodes':len(inv.nodes)})
