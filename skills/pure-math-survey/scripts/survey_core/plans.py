"""Question-relative selection, explicit paired spines and proof promises."""
from __future__ import annotations
from pathlib import Path
from .common import relpath, VERSION, all_files, require, result, safe, write_json, writer, identifier
from .dependencies import required_closure
from .knowledge import Inventory, inventory
from .models import load_plan
from .snapshots import load_snapshot


def authored_promise_errors(plan: dict) -> list[dict]:
    """Shared authoring gate: matching bytes never complete generated prompts."""
    from .common import diagnostic
    from .profiles import filled
    from .exposition import PENDING, DEFAULT_AUDIENCE, VAGUE_AUDIENCE
    errors = []
    if not (filled(plan['audience']) and plan['audience'] not in {DEFAULT_AUDIENCE, VAGUE_AUDIENCE}
            and not PENDING.search(plan['audience'])
            and all(filled(goal) and not PENDING.search(goal) for goal in plan['reader_goals'])):
        errors.append(diagnostic('EXPOSITION_DESIGN_INCOMPLETE',
            'Author actual reader capabilities and goals before requesting plan review', 'plan.json'))
    if not all(filled(step) and not PENDING.search(step)
               for item in plan['proof_obligations'] for step in item['required_steps']):
        errors.append(diagnostic('PROOF_OBLIGATION_UNMET',
            'Replace generated prompts with actual exact step promises before requesting review', 'plan.json'))
    return errors


def promise_projection(plan: dict) -> dict:
    """Existing mathematical plan fields, without a circular snapshot identity."""
    from .profiles import validate_plan_contract
    validate_plan_contract(plan)
    return {k: plan[k] for k in ('output_id', 'profile', 'view', 'audience', 'reader_goals',
            'question_ids', 'prerequisites', 'selections', 'proof_obligations', 'contributions')}


def promise_request(plan: dict) -> tuple[str, bytes]:
    from .common import canonical, sha
    data = canonical(promise_projection(plan)) + b'\n'
    # Content-addressed requests never overwrite earlier reviewed promises.
    return f"evidence/p/{sha(data)}.json", data

def consumption(inv: Inventory, plan: dict) -> set[str]:
    explain = {s['node_id'] for s in plan['selections'] if s['proof_treatment'] not in {'citation','none'}}
    explain |= {o['node_id'] for o in plan['proof_obligations']}
    seeds = set(plan['question_ids']) | {s['node_id'] for s in plan['selections']}
    for obligation in plan['proof_obligations']:
        seeds.add(obligation['node_id']); seeds.update(obligation['imported_inputs'])
    for claim in plan.get('contributions', []):
        from .profiles import comparison_ids
        seeds.update(claim['closest_prior_results']); seeds.update(comparison_ids(claim))
    ids=required_closure(inv.nodes, seeds, explain)
    from .reviews import comparison_evidence_closure
    ids=comparison_evidence_closure(inv,ids)
    return ids

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

def validate_plan(root: Path, plan: dict, *, compare: bool = True, inv: Inventory | None = None) -> Inventory:
    from .profiles import validate_plan_contract, validate_profile_selection
    validate_plan_contract(plan)
    if inv is None:
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
    validate_profile_selection(inv, plan)
    if compare and plan.get('comparison_group'):
        def spine(p:dict)->tuple:
            return (p['snapshot_id'], set(p['question_ids']), {s['node_id'] for s in p['selections'] if s['role']=='principal_answer'}, {s['node_id'] for s in p['selections'] if s['role']=='boundary'})
        for path in sorted((root/'outputs').glob('*/plan.json')):
            other = load_plan(path)
            if other['output_id'] != plan['output_id'] and other.get('comparison_group')==plan['comparison_group']:
                require(spine(plan)==spine(other), 'PAIRED_CORE_MISMATCH', 'Explicit paired outputs must share snapshot, questions, principal answers and decisive boundaries', relpath(root, path))
    return inv

def create_plan(root: Path, output_id: str, snapshot_id: str, profile: str='minimal', view: str='integrated',
                questions: list[str]|None=None, principals:list[str]|None=None, title:str|None=None, draft:bool=False,
                comparison_group:str|None=None, max_pages:int|None=None) -> dict:
    require(identifier(output_id), 'CONTRACT_INVALID', 'Invalid output ID')
    from .models import PROFILES, FACETS
    require(profile in PROFILES and view in FACETS|{'integrated'}, 'CONTRACT_INVALID', 'Invalid profile/view')
    _, frozen = load_snapshot(root, snapshot_id); inv = inventory(frozen)
    questions = questions or [k for k,n in inv.nodes.items() if n.meta['kind']=='question']
    answer_candidates = {k for q in inv.coverage['questions'] if q['question_id'] in questions for k in q['answer_nodes']}
    # An unassessed result is a legal explicit/draft target. A substantive open
    # question remains a frontier, not an automatically asserted proved answer.
    requested_principals = principals or sorted(answer_candidates)
    require(all(key in inv.nodes for key in requested_principals), 'UNKNOWN_REFERENCE', 'Requested principal is not a known node', 'plan.json')
    principal_questions = {key for key in requested_principals if inv.nodes[key].meta['kind'] == 'question'}
    principals = [key for key in requested_principals if key not in principal_questions]
    require(principals, 'PLAN_INVALID', 'Select an actual principal result; open questions remain frontier material', 'plan.json')
    seeds = set(principals) | principal_questions; roles = {k:'principal_answer' for k in principals}
    roles.update({key: 'frontier' if inv.nodes[key].meta['mathematical_status'] in {'open','conjectural','unassessed'} else 'background'
                  for key in principal_questions})
    for q in inv.coverage['questions']:
        if q['question_id'] in questions:
            for field,role in [('answer_nodes','background'),('mechanism_nodes','essential_bridge'),('boundary_nodes','boundary')]:
                seeds.update(q[field]); roles.update({k:role for k in q[field] if k not in roles})
    ids = required_closure(inv.nodes, seeds | set(questions), seeds) - (set(questions) - set(roles))
    for key in ids:
        if inv.nodes[key].meta['kind'] == 'question' and roles.get(key) != 'principal_answer':
            roles[key] = 'frontier' if inv.nodes[key].meta['mathematical_status'] in {'open','conjectural','unassessed'} else roles.get(key,'background')
    from .profiles import view_match, view_reason, VIEW_TASKS
    selections = []
    for key in sorted(ids,key=lambda k:(0 if roles.get(k)=='principal_answer' else
                      1 if view_match(inv.nodes[k].meta,view,roles.get(k,'background')) else 2,k)):
        n = inv.nodes[key]
        selections.append({'node_id':key, 'role':roles.get(key,'background'),
                           'statement_treatment':'full' if n.statement is not None else 'explained_reference',
                           'proof_treatment':'mechanism' if n.meta['kind']=='mechanism' else ('sketch' if key in principals else 'none'),
                           'reason':view_reason(n.meta,view,roles.get(key,'background'))})
    plan = {'schema_version':VERSION,'output_id':output_id,'snapshot_id':snapshot_id,'profile':profile,'view':view,
            'language':inv.project['language'],'title':title or inv.project['title'],'audience':'Readers of the selected mathematical scope; refine prerequisites before release.',
            'reader_goals':['Recover the selected question, exact principal answer, mechanism and decisive boundary.'],
            'question_ids':questions,'prerequisites':[],'selections':selections,'omissions':[],'proof_obligations':[],
            'limits':{'max_pages':max_pages,'page_review_threshold':None},'comparison_group':comparison_group,'draft':draft}
    from .profiles import OUTPUT_SCHEMA, POLICY, GOALS, PROOF_PROMPTS
    from .exposition import DEFAULT_AUDIENCE
    plan.update(schema_version=OUTPUT_SCHEMA, editorial_policy=POLICY, contributions=[],
                audience=DEFAULT_AUDIENCE,
                reader_goals=['[[PMS_PENDING:reader_goals]] '+GOALS.get(profile, 'Select a supported profile.'),
                              '[[PMS_PENDING:view_goal]] '+VIEW_TASKS[view]])
    # These are authoring prompts, not automatically satisfied mathematical promises.
    for selection in selections:
        if selection['role'] == 'principal_answer':
            selection['proof_treatment'] = {'minimal':'mechanism', 'thematic':'sketch', 'lecture':'complete', 'paper':'complete'}.get(profile, 'sketch')
        if selection['proof_treatment'] in {'complete','sketch','mechanism'}:
            plan['proof_obligations'].append({'node_id':selection['node_id'], 'treatment':selection['proof_treatment'],
                'required_steps':[PROOF_PROMPTS.get(profile, 'PENDING: select a supported profile.')],
                'imported_inputs':[e['target'] for e in inv.nodes[selection['node_id']].meta['links'] if e['relation']=='proof_input']})
    if profile == 'paper':
        plan['draft'] = True  # Promotion is a separate explicit, reviewed plan edit.
        plan['contributions'] = [{'node_id':key, 'classification':'unverified',
            'provenance':'PENDING: identify the authorized derivation or supplied manuscript; do not relabel known work.',
            'authorization':'', 'closest_prior_results':[], 'comparison_bindings':[],
            'actual_difference':'', 'proof_status':'unverified',
            'gaps':['Contribution, closest prior work and proof closure have not been reviewed.']} for key in principals]
    target = safe(root, f'outputs/{output_id}/plan.json')
    require(not target.exists(), 'DESTINATION_EXISTS', 'Output plan already exists', relpath(root, target))
    # Round-trip through the strict loader before committing.
    from .models import PROFILES, FACETS
    require(profile in PROFILES and view in FACETS|{'integrated'}, 'CONTRACT_INVALID', 'Invalid profile/view')
    validate_plan(root,plan)
    with writer(root): write_json(target,plan)
    return result('output.plan','PLANNED',{'plan':relpath(root, target),'profile':profile,'view':view,'review_status':'pending'})
