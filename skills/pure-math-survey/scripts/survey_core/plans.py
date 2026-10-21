"""Minimal selections and explicit alternative/conjunctive route groups from live KB."""
from __future__ import annotations
from pathlib import Path
from .common import RUNTIME_CONTRACT, relpath, require, result, safe, write_json, writer, identifier
from .dependencies import required_closure, route_inputs
from .knowledge import Inventory, inventory
from .models import load_project
from .profiles import OUTPUT_SCHEMA, POLICY, validate_plan_contract


def consumption(inv: Inventory,plan: dict) -> set[str]:
    seeds={s['node_id'] for s in plan['selections']}
    for route in inv.routes:
        if route['id'] in plan['route_ids']:seeds.add(route['target']);seeds.update(route_inputs(route))
    return required_closure(inv.nodes,seeds)


def consumed_paths(inv: Inventory,plan: dict) -> set[str]:
    ids=consumption(inv,plan);kr=inv.project['knowledge_root']
    paths={'project.json',inv.project['scope_file'],kr+'/conventions.tex',kr+'/routes.json'}
    sources=set()
    for key in ids:
        paths.add(inv.nodes[key].path);sources.update(s['source_id'] for s in inv.nodes[key].meta['sources'])
    for route in inv.routes:
        if route['id'] in plan['route_ids'] and route['source_locator']:sources.add(route['source_locator']['source_id'])
    for key in sources:
        paths.add(inv.source_paths[key])
        for name in ('reading_note','local_path','permission_note'):
            path=inv.sources[key]['access'].get(name)
            if path:paths.add(path)
    return paths


def validate_plan(root: Path,plan: dict,*,inv: Inventory|None=None) -> Inventory:
    load_project(root);validate_plan_contract(plan);inv=inv or inventory(root)
    selected={s['node_id']:s for s in plan['selections']}
    require(len(selected)==len(plan['selections']),'DUPLICATE_ID','Duplicate selection','plan.json')
    require(set(plan['route_ids']) <= {r['id'] for r in inv.routes},'UNKNOWN_REFERENCE','Unknown selected route','plan.json')
    for key,selection in selected.items():
        require(key in inv.nodes,'UNKNOWN_REFERENCE','Unknown selected node','plan.json',key)
        node=inv.nodes[key]
        if selection['statement_treatment']=='full':require(node.statement is not None,'CANONICAL_BLOCK_MISSING','Full statement needs canonical bytes',node.path,key)
        if selection['role']=='principal':require(node.statement is not None and selection['statement_treatment']=='full','PRINCIPAL_STATEMENT_INCOMPLETE','Principal needs a complete result',node.path,key)
    require(any(s['role']=='principal' for s in selected.values()),'PLAN_INVALID','Select a principal result','plan.json')
    # Definition closure is automatic; no duplicate per-plan definition registry.
    consumption(inv,plan)
    return inv


def create_plan(root: Path,output_id: str,profile='minimal',view='integrated',principals=None,title=None,max_pages=None) -> dict:
    load_project(root)
    require(profile=='minimal','PROFILE_UNSUPPORTED','Only minimal is supported');require(view=='integrated','VIEW_UNSUPPORTED','Only integrated is supported')
    require(identifier(output_id),'CONTRACT_INVALID','Invalid output ID')
    require(max_pages is None or type(max_pages) is int and max_pages>0,'CONTRACT_INVALID','max_pages must be positive or null')
    inv=inventory(root);principals=principals or [k for k,n in inv.nodes.items() if n.statement is not None and n.meta['role']=='principal']
    require(principals and all(k in inv.nodes and inv.nodes[k].statement is not None for k in principals),'PLAN_INVALID','Select actual principal results')
    seeds=set(principals);route_ids=set()
    while True:
        before=len(seeds)
        for route in inv.routes:
            if route['target'] in seeds:route_ids.add(route['id']);seeds.update(route_inputs(route))
        if len(seeds)==before:break
    ids=required_closure(inv.nodes,seeds)
    selections=[{'node_id':key,'role':'principal' if key in principals else inv.nodes[key].meta['role'],
        'statement_treatment':'full' if inv.nodes[key].statement is not None else 'explained_reference'} for key in sorted(ids,key=lambda k:(k not in principals,k))]
    plan={'schema_version':OUTPUT_SCHEMA,'runtime_contract':RUNTIME_CONTRACT,'editorial_policy':POLICY,'output_id':output_id,
        'profile':'minimal','view':'integrated','language':inv.project['language'],'title':title or inv.project['title'],
        'selections':selections,'route_ids':sorted(route_ids),'limits':{'max_pages':max_pages}}
    target=safe(root,f'outputs/{output_id}/plan.json');require(not target.exists(),'DESTINATION_EXISTS','Output plan exists',relpath(root,target))
    validate_plan(root,plan,inv=inv)
    with writer(root):
        require(not target.exists(),'DESTINATION_EXISTS','Output plan exists',relpath(root,target));write_json(target,plan)
    return result('output.plan','PLANNED',{'plan':relpath(root,target),'profile':'minimal','view':'integrated'})
