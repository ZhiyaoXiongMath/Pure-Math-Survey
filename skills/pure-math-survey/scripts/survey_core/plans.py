"""Minimal selection from one immutable canonical knowledge snapshot."""
from __future__ import annotations
from pathlib import Path
from .common import RUNTIME_CONTRACT, relpath, require, result, safe, write_json, writer, identifier
from .dependencies import required_closure
from .knowledge import Inventory, inventory
from .models import load_project
from .snapshots import load_snapshot
from .profiles import OUTPUT_SCHEMA, POLICY, validate_plan_contract


def consumption(inv: Inventory, plan: dict) -> set[str]:
    seeds=set(plan['question_ids']) | {s['node_id'] for s in plan['selections']}
    explained={s['node_id'] for s in plan['selections']
               if s['role'] in {'principal_answer','essential_bridge','boundary'}}
    return required_closure(inv.nodes, seeds, explained)


def consumed_paths(inv: Inventory, plan: dict) -> set[str]:
    ids=consumption(inv,plan); kr=inv.project['knowledge_root']
    paths={'project.json',inv.project['scope_file'],kr+'/conventions.tex'}
    for name in ('coverage.json','overview.md','discovery.md'):
        if safe(inv.root,kr+'/'+name).is_file(): paths.add(kr+'/'+name)
    sources=set()
    for key in ids:
        paths.add(inv.nodes[key].path)
        sources.update(s['source_id'] for s in inv.nodes[key].meta['sources'])
    for key in sources:
        paths.add(inv.source_paths[key])
        for field in ('reading_note','local_path','permission_note'):
            if inv.sources[key]['access'].get(field): paths.add(inv.sources[key]['access'][field])
    return paths


def validate_plan(root: Path, plan: dict, *, inv: Inventory | None = None) -> Inventory:
    load_project(root)
    validate_plan_contract(plan)
    if inv is None:
        _,frozen=load_snapshot(root,plan['snapshot_id']); inv=inventory(frozen)
    selected={s['node_id']:s for s in plan['selections']}
    require(len(selected)==len(plan['selections']),'DUPLICATE_ID','Duplicate selection','plan.json')
    omissions={o['node_id'] for o in plan['omissions']}
    require(not (set(selected)&omissions),'PLAN_INVALID','Node cannot be selected and omitted','plan.json')
    for q in plan['question_ids']:
        require(q in inv.nodes and inv.nodes[q].meta['kind']=='question','UNKNOWN_REFERENCE','Plan question is not a question node','plan.json',q)
    for key in set(selected)|omissions:
        require(key in inv.nodes,'UNKNOWN_REFERENCE','Plan references unknown node','plan.json',key)
    for key,s in selected.items():
        if s['statement_treatment']=='full':
            require(inv.nodes[key].statement is not None,'CANONICAL_BLOCK_MISSING','Full statement needs a canonical block',inv.nodes[key].path,key)
        if s['role']=='principal_answer':
            require(inv.nodes[key].meta['kind'] in {'result','relation'} and s['statement_treatment']=='full',
                    'PRINCIPAL_STATEMENT_INCOMPLETE','Principal must be an entire canonical result or relation','plan.json',key)
    require(any(s['role']=='principal_answer' for s in selected.values()),'PLAN_INVALID','Select an actual principal answer','plan.json')
    prereqs={p['node_id'] for p in plan['prerequisites'] if isinstance(p,dict)}
    for key in prereqs:
        require(key in inv.nodes,'UNKNOWN_REFERENCE','Explicit prerequisite node missing','plan.json',key)
    unhandled=consumption(inv,plan)-set(selected)-set(plan['question_ids'])-prereqs
    require(not unhandled,'DEPENDENCY_UNHANDLED','Select or scope prerequisite nodes: '+', '.join(sorted(unhandled)),'plan.json')
    return inv


def create_plan(root: Path, output_id: str, snapshot_id: str, profile: str='minimal', view: str='integrated',
                questions: list[str]|None=None, principals:list[str]|None=None, title:str|None=None,
                max_pages:int|None=None) -> dict:
    load_project(root)
    require(profile=='minimal','PROFILE_UNSUPPORTED','Only minimal is supported')
    require(view=='integrated','VIEW_UNSUPPORTED','Only the fixed integrated view is supported')
    require(identifier(output_id),'CONTRACT_INVALID','Invalid output ID')
    require(max_pages is None or (type(max_pages) is int and max_pages>0),'CONTRACT_INVALID','max_pages must be positive or null')
    _,frozen=load_snapshot(root,snapshot_id); inv=inventory(frozen)
    questions=questions or [k for k,n in inv.nodes.items() if n.meta['kind']=='question']
    principals=principals or sorted({k for q in inv.coverage['questions'] if q['question_id'] in questions for k in q['answer_nodes']})
    require(principals,'PLAN_INVALID','Select an actual principal result','plan.json')
    require(all(k in inv.nodes and inv.nodes[k].meta['kind'] in {'result','relation'} for k in principals),
            'PLAN_INVALID','Principals must be known result or relation nodes','plan.json')
    roles={k:'principal_answer' for k in principals}; seeds=set(principals)
    for q in inv.coverage['questions']:
        if q['question_id'] in questions:
            for field,role in [('mechanism_nodes','essential_bridge'),('boundary_nodes','boundary')]:
                seeds.update(q[field]);roles.update({k:role for k in q[field] if k not in roles})
    ids=required_closure(inv.nodes,seeds|set(questions),seeds)-set(questions)
    selections=[]
    for key in sorted(ids,key=lambda k:(roles.get(k)!='principal_answer',k)):
        n=inv.nodes[key]
        selections.append({'node_id':key,'role':roles.get(key,'background'),
            'statement_treatment':'full' if n.statement is not None else 'explained_reference',
            'reason':'Selected principal or a dependency needed to explain its method and conditions.'})
    plan={'schema_version':OUTPUT_SCHEMA,'runtime_contract':RUNTIME_CONTRACT,'editorial_policy':POLICY,
          'output_id':output_id,'snapshot_id':snapshot_id,'profile':'minimal','view':'integrated',
          'language':inv.project['language'],'title':title or inv.project['title'],
          'audience':'Readers of the selected mathematical scope.',
          'reader_goals':['Understand the selected result, its necessary modules and their combination.'],
          'question_ids':questions,'prerequisites':[],'selections':selections,'omissions':[],
          'limits':{'max_pages':max_pages}}
    target=safe(root,f'outputs/{output_id}/plan.json')
    require(not target.exists(),'DESTINATION_EXISTS','Output plan already exists',relpath(root,target))
    validate_plan(root,plan)
    with writer(root):
        require(not target.exists(),'DESTINATION_EXISTS','Output plan already exists',relpath(root,target))
        write_json(target,plan)
    return result('output.plan','PLANNED',{'plan':relpath(root,target),'profile':'minimal','view':'integrated'})
