"""Exact canonical fragments and bounded writing materials; not automatic math prose."""
from __future__ import annotations
from pathlib import Path
import re
import shutil
import tempfile
import unicodedata
from .common import relpath, resolved_path, native_path, SKILL_ROOT, VERSION, all_files, atomic_bytes, canonical, diagnostic, file_hash, file_inventory, read_json, require, result, safe, sha, write_json, writer
from .models import load_plan, load_project
from .plans import consumption, consumed_paths, validate_plan
from .dependencies import topological

def tex_text(value:str)->str:
    special={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}',
             '–':'--','—':'---','’':"'",'“':'``','”':"''",'ä':r'\"a','ö':r'\"o','ü':r'\"u','é':r"\'e",'è':r'\`e','Ä':r'\"A','Ö':r'\"O','Ü':r'\"U'}
    return ''.join(special.get(c,c) for c in value)

def extract_statements(inv,ids:set[str])->dict[str,bytes]:
    return {f'statements/{k}.tex':inv.nodes[k].statement for k in sorted(ids) if inv.nodes[k].statement is not None}

def export_bibliography(inv,ids:set[str])->bytes:
    sources=sorted({s['source_id'] for k in ids for s in inv.nodes[k].meta['sources']} | {r['source_locator']['source_id'] for r in inv.routes if r['target'] in ids and r['source_locator']})
    entries=[]
    for key in sources:
        s=inv.sources[key]
        fields={'title':tex_text(s['title']),'author':' and '.join(tex_text(a) for a in s['authors']),
                'note':tex_text(f"Controlling version: {s['version'] or 'unverified'}."),
                'howpublished':tex_text(s.get('url') or '')}
        # A modern arXiv prefix such as 1904 is not the year 1904.
        # Prefer an explicit citation year, otherwise accept only a separated
        # calendar year in the controlling-version text (never an identifier).
        explicit=s.get('bibliography',{}).get('year')
        if explicit is not None:
            require(re.fullmatch(r'(?:19|20)\d{2}',str(explicit)), 'CONTRACT_INVALID', 'bibliography.year must be a calendar year', inv.source_paths[key])
            fields['year']=str(explicit)
        else:
            year=re.search(r'(?<![\d:/])(?:19|20)\d{2}(?![\d.])',str(s['version'] or ''))
            if year:fields['year']=year.group()
        entries.append('@misc{'+s['citation_key']+',\n'+',\n'.join(f'  {k} = {{{v}}}' for k,v in fields.items() if v)+'\n}')
    return ('% Generated from fixed source records; edit the knowledge records, not this file.\n\n'+'\n\n'.join(entries)+'\n').encode('utf-8')

def expected_generated(inv,plan:dict)->dict[str,bytes]:
    ids=consumption(inv,plan)
    return {**extract_statements(inv,ids),'conventions.tex':safe(inv.root,inv.project['knowledge_root']+'/conventions.tex',True).read_bytes(),
            'references.bib':export_bibliography(inv,ids), **route_fragments(inv,plan)}

def route_fragments(inv,plan:dict)->dict[str,bytes]:
    routes=[r for r in inv.routes if r['id'] in plan['route_ids']]
    lines=['% Derived relationship data. Author graph layout remains in manuscript/.']
    for route in routes:
        groups=[]
        for group in route['premise_sets']:
            nodes=', '.join(key+(' (method description; no formal conclusion)' if inv.nodes[key].meta['kind']=='method' and inv.nodes[key].statement is None else '') for key in group['nodes'])
            extra='; additional inputs: '+ '; '.join(group['additional_inputs']) if group['additional_inputs'] else ''
            groups.append('jointly {'+nodes+'}'+extra)
        description=route['id']+': '+ ' OR '.join(groups)+'; target '+route['target']+'. '+route['mapping']
        description+=' [unresolved: no asserted implication]' if route['status']=='unresolved' else ' [source-reported; not certified]'
        lines.append(tex_text(description)+r'\par')
    return {'routes.json':canonical({'schema_version':VERSION,'routes':routes})+b'\n',
            'routes.tex':('\n'.join(lines)+'\n').encode('utf-8')}


def authoring_input_paths(inv, plan: dict) -> set[str]:
    return consumed_paths(inv, plan)


def expected_materials(inv,plan:dict)->dict[str,bytes]:
    """Copy selected canonical materials, omitting original source bytes."""
    from .sources import require_public_originals
    require_public_originals(inv)
    from .sources import original_input_paths
    inputs=authoring_input_paths(inv,plan)
    paths=inputs-original_input_paths(inv,inputs)
    return {p:safe(inv.root,p,True).read_bytes() for p in sorted(paths)}

def prepare_output(root:Path,plan_path:Path)->dict:
    load_project(root)
    plan=load_plan(plan_path);out=native_path(safe(root,'outputs/'+plan['output_id']), extended=True)
    require(resolved_path(plan_path)==resolved_path(out/'plan.json'),'PLAN_LOCATION_MISMATCH','Plan must be outputs/<output_id>/plan.json')
    inv=validate_plan(root,plan)
    data=expected_generated(inv,plan); ids=consumption(inv,plan);inputs=authoring_input_paths(inv,plan)
    materials=expected_materials(inv,plan)
    from .sources import original_input_paths
    manifest={'schema_version':VERSION,'input_hash':sha(canonical(file_inventory(inv.root,sorted(inputs)))),'output_id':plan['output_id'],
              'plan_sha256':sha(canonical(plan)),'consumed_nodes':sorted(ids),
              'consumed_inputs':file_inventory(inv.root,sorted(inputs)),
              'generated_files':[{'path':'generated/'+p,'sha256':sha(b),'bytes':len(b)} for p,b in sorted(data.items())],
              'raw_sources_omitted':sorted(original_input_paths(inv,inputs)),
              'meaning':'Exact stored bytes are reused; mechanical checks do not certify mathematics.'}
    with writer(root):
        from .knowledge import inventory
        current=inventory(root)
        require(expected_generated(current,plan)==data and expected_materials(current,plan)==materials,'PREPARE_INPUT_CHANGED','Knowledge changed before preparation; retry')
        require(file_inventory(inv.root,sorted(inputs))==manifest['consumed_inputs'],'PREPARE_INPUT_CHANGED','Knowledge changed before preparation; retry')
        stage=Path(tempfile.mkdtemp(prefix='.prepare-',dir=native_path(out, extended=True)))
        try:
            for p,b in data.items():atomic_bytes(stage/'generated'/p,b)
            write_json(stage/'generated/manifest.json',manifest)
            for p,b in materials.items():atomic_bytes(stage/'materials'/p,b)
            write_json(stage/'materials/materials-manifest.json',manifest)
            current=inventory(root)
            require(expected_generated(current,plan)==data and expected_materials(current,plan)==materials and file_inventory(inv.root,sorted(inputs))==manifest['consumed_inputs'],'PREPARE_INPUT_CHANGED','Knowledge changed while preparing; retry')
            if (out/'generated/manifest.json').exists():
                from .history import save_record
                previous={p:safe(out,p,True).read_bytes() for p in all_files(out) if not p.startswith(('history/','.prepare-'))}
                save_record(out,'preparation',previous)
            moved=[]
            try:
                for folder in ('generated','materials'):
                    target=out/folder; backup=stage/('old-'+folder)
                    if target.exists():target.rename(backup)
                    moved.append(folder)
                    (stage/folder).rename(target)
            except Exception:
                for folder in reversed(moved):
                    target=out/folder;backup=stage/('old-'+folder)
                    if target.exists():shutil.rmtree(target)
                    if backup.exists():backup.rename(target)
                raise
        finally:shutil.rmtree(native_path(stage, extended=True),ignore_errors=True)
        if not (out/'outline.md').exists():
            order=topological(inv.nodes,ids)
            from .profiles import outline
            atomic_bytes(out/'outline.md', outline(plan, order, inv.nodes).encode('utf-8'))
        if not (out/'manuscript/math-review.sty').exists():
            atomic_bytes(out/'manuscript/math-review.sty',(SKILL_ROOT/'assets/templates/math-review.sty').read_bytes())
        if not (out/'manuscript/main.tex').exists():
            from .profiles import VIEW_TASKS
            template=(SKILL_ROOT/'assets/templates'/f"profile-{plan['profile']}.tex").read_text(encoding='utf-8')
            snippets=[]; principals=[]; ingredients=[]
            selections={s['node_id']:dict(s) for s in plan['selections']}
            for key in topological(inv.nodes,ids):
                if key not in selections:
                    node=inv.nodes[key];selections[key]={'node_id':key,'role':node.meta['role'],'statement_treatment':'full' if node.statement is not None else 'explained_reference'}
            for s in selections.values():
                if inv.nodes[s['node_id']].meta['kind']=='definition':s['statement_treatment']='full'
                if s['statement_treatment']=='full':
                    key=s['node_id']; kind=inv.nodes[key].meta['kind']
                    env=inv.nodes[key].meta.get('statement_kind',{'definition':'definition','example':'example'}.get(kind,'theorem'))
                    snippet = f'\\begin{{{env}}}\\label{{node:{key}}}\n\\input{{../generated/statements/{key}.tex}}\n\\end{{{env}}}\n'
                    snippets.append(snippet)
                    (principals if s['role']=='principal' else ingredients).append(snippet)
            task='\\placeholder{'+tex_text(VIEW_TASKS[plan['view']])+'}'
            text=template.replace('@@TITLE@@',tex_text(plan['title'])).replace('@@STATEMENTS@@','\n'.join(snippets)).replace('@@PRINCIPALS@@','\n'.join(principals)).replace('@@INGREDIENTS@@','\n'.join(ingredients)).replace('@@VIEW_TASK@@',task)
            atomic_bytes(out/'manuscript/main.tex',text.encode())
        from .knowledge import write_run
        write_run(root,inv,[relpath(root,out)],'not_built')
    return result('output.prepare','PREPARED',{'output':relpath(root, out),'input_hash':manifest['input_hash'],
        'main_preserved':True,'authorship':'SCAFFOLD: preparation is not completed writing or mathematical certification.'})

def verify_generated(root:Path,plan:dict)->dict:
    inv=validate_plan(root,plan);out=safe(root,'outputs/'+plan['output_id']);expected=expected_generated(inv,plan)
    manifest=read_json(safe(out,'generated/manifest.json',True))
    require(manifest.get('plan_sha256')==sha(canonical(plan)),'GENERATED_INPUT_STALE','Plan changed; explicitly prepare again before use','generated/manifest.json')
    actual=set(all_files(out,'generated'))
    require(actual=={'generated/'+p for p in expected}|{'generated/manifest.json'},'CANONICAL_STATEMENT_CHANGED','Generated files have extra or missing content','generated')
    for p,b in expected.items():
        require(safe(out,'generated/'+p,True).read_bytes()==b,'CANONICAL_STATEMENT_CHANGED','Generated content differs from prepared knowledge','generated/'+p)
    expected_records=[{'path':'generated/'+p,'sha256':sha(b),'bytes':len(b)} for p,b in sorted(expected.items())]
    require(manifest.get('generated_files')==expected_records and manifest.get('consumed_inputs')==file_inventory(inv.root,sorted(authoring_input_paths(inv,plan))) and manifest.get('input_hash')==sha(canonical(manifest['consumed_inputs'])),
            'GENERATED_INPUT_STALE','Generated manifest does not bind actual fixed inputs','generated/manifest.json')
    # The generated theorem alone is insufficient: prose is written using all
    # supplied materials, which must retain the same recorded canonical inputs.
    materials=expected_materials(inv,plan)
    expected_members={'materials/'+p for p in materials}|{'materials/materials-manifest.json'}
    actual_members=set(all_files(out,'materials'))
    mismatch=sorted(expected_members ^ actual_members)
    require(not mismatch,'MATERIALS_CHANGED','Authoring materials gained or lost canonical inputs; explicitly prepare again',
            mismatch[0] if mismatch else 'materials')
    for p,b in materials.items():
        require(safe(out,'materials/'+p,True).read_bytes()==b,'MATERIALS_CHANGED',
                'Authoring material differs from the prepared knowledge; edit canonical knowledge and explicitly prepare again','materials/'+p)
    require(safe(out,'materials/materials-manifest.json',True).read_bytes()==safe(out,'generated/manifest.json',True).read_bytes(),
            'MATERIALS_CHANGED','Material manifest differs from the verified generation manifest','materials/materials-manifest.json')
    return manifest

def output_inputs(out:Path)->set[str]:
    paths={'plan.json'}|set(all_files(out,'manuscript'))|set(all_files(out,'generated'))
    if safe(out,'outline.md').is_file():paths.add('outline.md')
    # Also bind the authoring materials actually supplied to the reader/agent.
    paths |= set(all_files(out,'materials'))
    return paths

def expand_tex(out:Path,path:Path,active:tuple[Path,...]=())->tuple[str,set[str]]:
    """Inspect the actual entry point with compiler-relative input resolution."""
    from .tex import inspect_tex
    require(resolved_path(path) == resolved_path(out/'manuscript/main.tex'), 'TEX_INPUT_UNSUPPORTED', 'Inspect from the actual entry point')
    scan = inspect_tex(out)
    return scan.text, scan.inputs

def validate_structure(root:Path,output_id:str)->dict:
    out=safe(root,'outputs/'+output_id);plan=load_plan(out/'plan.json');verify_generated(root,plan)
    from .tex import inspect_tex
    scan=inspect_tex(out);text=scan.text;used=scan.inputs
    from .structure import inventory as tex_inventory,public_inventory,statement_title_errors
    inv=tex_inventory(text);errors=list(scan.errors)+statement_title_errors(scan);warnings=[]
    # Ordinary boundary prose is allowed; explicit unfinished scaffold markers are not.
    inv['has_placeholder']=bool(re.search(r'\\placeholder\b|\b(?:TODO|TBD)\b|\[INSERT',text,re.I) or re.search(r'\bPENDING\b',text))
    labels=inv['labels']
    if len(labels)!=len(set(labels)):errors.append(diagnostic('DUPLICATE_LABEL','Repeated TeX labels','manuscript/main.tex'))
    if inv['has_placeholder']:errors.append(diagnostic('MANUSCRIPT_INCOMPLETE','Visible scaffold placeholders remain','manuscript/main.tex'))
    knowledge=validate_plan(root,plan)
    selected={s['node_id']:s for s in plan['selections']}
    for key in consumption(knowledge,plan):
        s=selected.get(key,{'node_id':key,'statement_treatment':'full' if knowledge.nodes[key].statement is not None else 'explained_reference'})
        path=f"generated/statements/{s['node_id']}.tex"
        if (s['statement_treatment']=='full' or knowledge.nodes[key].meta['kind']=='definition') and path not in scan.body_inputs:
            errors.append(diagnostic('CANONICAL_STATEMENT_MISSING','Full selected statement is not literally included in the visible manuscript body',path,s['node_id']))
    from .profiles import structure_errors
    profile_errors, profile_warnings = structure_errors(inv, plan, validate_plan(root, plan).nodes, text)
    errors += profile_errors; warnings += profile_warnings
    from .profiles import strict_minimal
    if strict_minimal(plan):
        from .structure import strip_comments
        for path in sorted(used | {'manuscript/main.tex'}):
            if path.startswith('manuscript/') and path.endswith('.tex'):
                raw=strip_comments(safe(out,path,True).read_text(encoding='utf-8'))
                if re.search(r'\\(?:re)?newcommand\s*(?:\{)?\\thesection\b|\\def\s*\\thesection\b',raw):
                    errors.append(diagnostic('MINIMAL_NUMBERING_UNSUPPORTED','Custom main-section numbering is not supported by the strict three-section contract.',path))
    from .profiles import policy
    return result('output.structure','NEEDS_WORK' if errors else 'STRUCTURALLY_VALID',{'tex_inventory':public_inventory(inv),'actual_literal_inputs':sorted(used),'body_inputs':sorted(scan.body_inputs),'canonical_locations':scan.locations,
        'editorial_policy':policy(plan)},errors,warnings)


def export_unit(root:Path,node_id:str,destination:Path)->dict:
    """Standalone concept closure with exact canonical bytes and source locators."""
    from .knowledge import inventory
    from .dependencies import required_closure
    inv=inventory(root)
    ids=required_closure(inv.nodes,{node_id})
    plan={'selections':[{'node_id':k} for k in ids],'route_ids':[]}
    data={'generated/'+p:b for p,b in expected_generated(inv,plan).items()}
    data.update({'materials/'+p:b for p,b in expected_materials(inv,plan).items()})
    lines=[r'\input{generated/conventions.tex}']
    for key in topological(inv.nodes,ids):
        node=inv.nodes[key]
        if node.statement is not None:
            env=node.meta.get('statement_kind',{'definition':'definition','example':'example'}.get(node.meta['kind'],'theorem'))
            lines.append(r'\begin{'+env+'}'+r'\input{generated/statements/'+key+'.tex}'+r'\end{'+env+'}')
        for ref in node.meta['sources']:
            source=inv.sources[ref['source_id']]
            lines.append(r'\par Source: '+tex_text(ref['source_id']+'; '+ref['locator']+'; version '+str(source['version']))+r'~\cite{'+source['citation_key']+'}.')
    data['unit.tex']=('\n'.join(lines)+'\n').encode('utf-8')
    data['math-review.sty']=(SKILL_ROOT/'assets/templates/math-review.sty').read_bytes()
    data['main.tex']=(r'\documentclass[12pt]{amsart}'+'\n'+r'\usepackage{math-review}'+'\n'+r'\begin{document}\input{unit.tex}'+ '\n'+r'\bibliographystyle{plain}\bibliography{generated/references}\end{document}'+'\n').encode('utf-8')
    data['manifest.json']=canonical({'schema_version':VERSION,'node_id':node_id,'included_nodes':sorted(ids),
        'files':[{'path':p,'sha256':sha(v),'bytes':len(v)} for p,v in sorted(data.items())]})+b'\n'
    require(not destination.is_symlink(),'UNSAFE_PATH','Unit export destination is a symlink',str(destination))
    require(not destination.exists(),'DESTINATION_EXISTS','Unit export requires a new destination',str(destination))
    # Reject symlinked parent components and keep export away from canonical input paths.
    parent=destination.parent.absolute()
    for part in (parent,*parent.parents):require(not part.is_symlink(),'UNSAFE_PATH','Export parent is a symlink',str(part))
    require(resolved_path(root) not in resolved_path(destination).parents,'UNSAFE_PATH','Export outside the project to preserve canonical inputs',str(destination))
    parent.mkdir(parents=True,exist_ok=True);stage=Path(tempfile.mkdtemp(prefix='.unit-',dir=parent))
    try:
        for path,body in data.items():atomic_bytes(stage/path,body)
        require(not destination.exists(),'DESTINATION_EXISTS','Unit export destination exists',str(destination));stage.rename(destination)
    finally:
        if stage.exists():shutil.rmtree(stage)
    return result('kb.export','EXPORTED',{'destination':str(destination),'included_nodes':sorted(ids)})
