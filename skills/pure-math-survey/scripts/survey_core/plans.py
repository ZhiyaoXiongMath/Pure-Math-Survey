"""Question-relative selection, explicit paired spines and proof promises."""
from __future__ import annotations
from pathlib import Path
from .common import VERSION, all_files, require, result, safe, write_json, writer, identifier
from .dependencies import required_closure
from .knowledge import Inventory, inventory
from .models import load_plan
from .snapshots import load_snapshot

def consumption(inv: Inventory, plan: dict) -> set[str]:
    explain = {s['node_id'] for s in plan['selections'] if s['proof_treatment'] not in {'citation','none'}}
    explain |= {o['node_id'] for o in plan['proof_obligations']}
    seeds = set(plan['question_ids']) | {s['node_id'] for s in plan['selections']}
    for obligation in plan['proof_obligations']:
        seeds.add(obligation['node_id']); seeds.update(obligation['imported_inputs'])
    return required_closure(inv.nodes, seeds, explain)

def consumed_paths(inv: Inventory, plan: dict) -> set[str]:
    ids = consumption(inv, plan); kr = inv.project['knowledge_root']
    paths = {'project.json', inv.project['scope_file'], kr + '/conventions.tex', kr + '/coverage.json', kr + '/discovery.md'}
    if plan.get('consume_overview', True): paths.add(kr + '/overview.md')
    sources = set()
    for key in ids:
        paths.add(inv.nodes[key].path)
        sources.update(s['source_id'] for s in inv.nodes[key].meta['sources'])
    for key in sources:
        paths.add(inv.source_paths[key])
        for field in ('reading_note','local_path'):
            if inv.sources[key]['access'].get(field): paths.add(inv.sources[key]['access'][field])
    return paths

def validate_plan(root: Path, plan: dict, *, compare: bool = True) -> Inventory:
    _, frozen = load_snapshot(root, plan['snapshot_id']); inv = inventory(frozen)
    selected = {s['node_id']: s for s in plan['selections']}
    require(len(selected) == len(plan['selections']), 'DUPLICATE_ID', 'Duplicate selection in plan', 'plan.json')
    omissions = {o['node_id'] for o in plan['omissions']}
    require(not (set(selected) & omissions), 'PLAN_INVALID', 'Node cannot be selected and omitted', 'plan.json')
    for q in plan['question_ids']:
        require(q in inv.nodes and inv.nodes[q].meta['kind']=='question', 'UNKNOWN_REFERENCE', 'Plan question is not a question node', 'plan.json', q)
    for key in set(selected) | omissions:
        require(key in inv.nodes, 'UNKNOWN_REFERENCE', 'Plan references unknown node', 'plan.json', key)
    for key,s in selected.items():
        if s['statement_treatment']=='full':
            require(inv.nodes[key].statement is not None, 'CANONICAL_BLOCK_MISSING', 'Full statement requested, but no canonical block', inv.nodes[key].path, key)
        if s['role']=='principal_answer':
            require(s['statement_treatment']=='full', 'PRINCIPAL_STATEMENT_INCOMPLETE', 'Principal answers must preserve the entire canonical statement', 'plan.json', key)
        if s['statement_treatment']=='explained_reference':
            require(inv.nodes[key].body.strip(), 'PLAN_INVALID', 'Explained reference requires readable local conditions/mechanism', 'plan.json', key)
    require(any(s['role']=='principal_answer' for s in selected.values()), 'PLAN_INVALID', 'Select an actual principal answer', 'plan.json')
    ids = consumption(inv, plan)
    prereqs = {p['node_id'] for p in plan['prerequisites'] if isinstance(p,dict)}
    for key in prereqs:
        require(key in inv.nodes, 'UNKNOWN_REFERENCE', 'Explicit prerequisite node missing', 'plan.json', key)
    unhandled = ids - set(selected) - set(plan['question_ids']) - prereqs
    require(not unhandled, 'DEPENDENCY_UNHANDLED', 'Select or explicitly scope prerequisite nodes: ' + ', '.join(sorted(unhandled)), 'plan.json')
    for q in inv.coverage['questions']:
        if q['question_id'] in plan['question_ids']:
            candidates = set(q['answer_nodes']+q['mechanism_nodes']+q['boundary_nodes'])
            require(not (candidates - set(selected) - omissions - prereqs), 'SELECTION_GAP', 'Related coverage candidate needs a selection or a reasoned omission: ' + ', '.join(sorted(candidates-set(selected)-omissions-prereqs)), 'plan.json', q['question_id'])
    obligations = {o['node_id']: o for o in plan['proof_obligations']}
    require(len(obligations)==len(plan['proof_obligations']), 'DUPLICATE_ID', 'Duplicate proof obligation', 'plan.json')
    for key,s in selected.items():
        if s['proof_treatment']=='complete':
            direct = obligations.get(key)
            mechanisms = [e['target'] for e in inv.nodes[key].meta['links'] if e['relation']=='explained_by']
            complete = direct and direct['treatment']=='complete'
            complete = complete or bool(mechanisms and all(m in obligations and obligations[m]['treatment']=='complete' for m in mechanisms))
            require(complete, 'PROOF_OBLIGATION_UNMET', 'A complete proof promise needs complete step obligations, not a sketch', 'plan.json', key)
    for o in plan['proof_obligations']:
        require(o['node_id'] in selected, 'PROOF_OBLIGATION_UNMET', 'Obligation must refer to a selected node', 'plan.json', o['node_id'])
        require(all(k in selected or k in prereqs for k in o['imported_inputs']), 'PROOF_OBLIGATION_UNMET', 'Imported inputs need explicit treatment', 'plan.json', o['node_id'])
    if compare and plan.get('comparison_group'):
        def spine(p:dict)->tuple:
            return (p['snapshot_id'], set(p['question_ids']), {s['node_id'] for s in p['selections'] if s['role']=='principal_answer'}, {s['node_id'] for s in p['selections'] if s['role']=='boundary'})
        for path in sorted((root/'outputs').glob('*/plan.json')):
            other = load_plan(path)
            if other['output_id'] != plan['output_id'] and other.get('comparison_group')==plan['comparison_group']:
                require(spine(plan)==spine(other), 'PAIRED_CORE_MISMATCH', 'Explicit paired outputs must share snapshot, questions, principal answers and decisive boundaries', path.relative_to(root).as_posix())
    return inv

def create_plan(root: Path, output_id: str, snapshot_id: str, profile: str='minimal', view: str='integrated',
                questions: list[str]|None=None, principals:list[str]|None=None, title:str|None=None, draft:bool=False,
                comparison_group:str|None=None, max_pages:int|None=None) -> dict:
    require(identifier(output_id), 'CONTRACT_INVALID', 'Invalid output ID')
    _, frozen = load_snapshot(root, snapshot_id); inv = inventory(frozen)
    questions = questions or [k for k,n in inv.nodes.items() if n.meta['kind']=='question']
    principals = principals or sorted({k for q in inv.coverage['questions'] if q['question_id'] in questions for k in q['answer_nodes']})
    seeds = set(principals); roles = {k:'principal_answer' for k in principals}
    for q in inv.coverage['questions']:
        if q['question_id'] in questions:
            for field,role in [('mechanism_nodes','essential_bridge'),('boundary_nodes','boundary')]:
                seeds.update(q[field]); roles.update({k:role for k in q[field] if k not in roles})
    ids = required_closure(inv.nodes, seeds | set(questions), seeds) - set(questions)
    selections = []
    for key in sorted(ids):
        n = inv.nodes[key]
        selections.append({'node_id':key, 'role':roles.get(key,'background'),
                           'statement_treatment':'full' if n.statement is not None else 'explained_reference',
                           'proof_treatment':'mechanism' if n.meta['kind']=='mechanism' else ('sketch' if key in principals else 'none'),
                           'reason':'Required by the selected question or its dependency closure; refine during editorial selection.'})
    plan = {'schema_version':VERSION,'output_id':output_id,'snapshot_id':snapshot_id,'profile':profile,'view':view,
            'language':inv.project['language'],'title':title or inv.project['title'],'audience':'Readers of the selected mathematical scope; refine prerequisites before release.',
            'reader_goals':['Recover the selected question, exact principal answer, mechanism and decisive boundary.'],
            'question_ids':questions,'prerequisites':[],'selections':selections,'omissions':[],'proof_obligations':[],
            'limits':{'max_pages':max_pages,'page_review_threshold':None},'comparison_group':comparison_group,'draft':draft}
    target = safe(root, f'outputs/{output_id}/plan.json')
    require(not target.exists(), 'DESTINATION_EXISTS', 'Output plan already exists', target.relative_to(root).as_posix())
    # Round-trip through the strict loader before committing.
    from .models import PROFILES, FACETS
    require(profile in PROFILES and view in FACETS|{'integrated'}, 'CONTRACT_INVALID', 'Invalid profile/view')
    validate_plan(root,plan)
    with writer(root): write_json(target,plan)
    return result('output.plan','PLANNED',{'plan':target.relative_to(root).as_posix(),'profile':profile,'view':view,'review_status':'pending'})
