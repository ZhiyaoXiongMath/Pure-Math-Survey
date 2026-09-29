"""Exact snapshot fragments and bounded writing materials; not automatic math prose."""
from __future__ import annotations
from pathlib import Path
import re
import shutil
import tempfile
import unicodedata
from .common import SKILL_ROOT, VERSION, all_files, atomic_bytes, canonical, diagnostic, file_hash, file_inventory, read_json, require, result, safe, sha, write_json, writer
from .models import load_plan
from .plans import consumption, consumed_paths, validate_plan
from .dependencies import topological
from .readiness import assess_readiness

def tex_text(value:str)->str:
    special={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}',
             '–':'--','—':'---','’':"'",'“':'``','”':"''",'ä':r'\"a','ö':r'\"o','ü':r'\"u','é':r"\'e",'è':r'\`e','Ä':r'\"A','Ö':r'\"O','Ü':r'\"U'}
    return ''.join(special.get(c,c) for c in value)

def extract_statements(inv,ids:set[str])->dict[str,bytes]:
    return {f'statements/{k}.tex':inv.nodes[k].statement for k in sorted(ids) if inv.nodes[k].statement is not None}

def export_bibliography(inv,ids:set[str])->bytes:
    sources=sorted({s['source_id'] for k in ids for s in inv.nodes[k].meta['sources']})
    entries=[]
    for key in sources:
        s=inv.sources[key]; identity=s['identifiers']
        fields={'title':tex_text(s['title']),'author':' and '.join(tex_text(a) for a in s['authors']),
                'note':tex_text(f"{s['publication_status']}; controlling version: {s['version'] or 'unverified'}."),
                'howpublished':tex_text(identity.get('doi') or identity.get('arxiv') or identity.get('journal_reference') or identity.get('user_file') or identity.get('url',''))}
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
        entries.append('@misc{'+key+',\n'+',\n'.join(f'  {k} = {{{v}}}' for k,v in fields.items() if v)+'\n}')
    return ('% Generated from fixed source records; edit the knowledge records, not this file.\n\n'+'\n\n'.join(entries)+'\n').encode('utf-8')

def expected_generated(inv,plan:dict)->dict[str,bytes]:
    ids=consumption(inv,plan)
    return {**extract_statements(inv,ids),'conventions.tex':safe(inv.root,inv.project['knowledge_root']+'/conventions.tex',True).read_bytes(),
            'references.bib':export_bibliography(inv,ids)}

def expected_materials(inv,plan:dict,ready:dict)->dict[str,bytes]:
    """Reconstruct authoring inputs from the immutable snapshot, not its copies.

    Original source files remain omitted, as in 2.0.0/2.0.1. Review records
    actually used by this selection are included even though they are not
    ordinary consumed knowledge paths. This preserves existing output bytes.
    """
    raw_files={s['access'].get('local_path') for s in inv.sources.values()}
    paths=consumed_paths(inv,plan)-raw_files
    from .reviews import reviews_in
    used=set(ready['artifacts']['used_review_ids'])
    paths|={p for p,r in reviews_in(inv.root) if r['review_id'] in used}
    return {p:safe(inv.root,p,True).read_bytes() for p in sorted(paths)}

def prepare_output(root:Path,plan_path:Path,draft:bool=False)->dict:
    plan=load_plan(plan_path);out=safe(root,'outputs/'+plan['output_id'])
    require(plan_path.resolve()==(out/'plan.json').resolve(),'PLAN_LOCATION_MISMATCH','Plan must be outputs/<output_id>/plan.json')
    if draft and not plan['draft']:
        plan={**plan,'draft':True}
        with writer(root):write_json(plan_path,plan)
    inv=validate_plan(root,plan);ready=assess_readiness(root,plan)
    require(plan['draft'] or ready['status']=='READY','READINESS_REQUIRED','Formal preparation requires readiness; use explicit --draft for an internal manuscript','plan.json')
    data=expected_generated(inv,plan); ids=consumption(inv,plan);inputs=consumed_paths(inv,plan)
    raw_files={s['access'].get('local_path') for s in inv.sources.values()}
    materials=expected_materials(inv,plan,ready)
    manifest={'schema_version':VERSION,'snapshot_id':plan['snapshot_id'],'output_id':plan['output_id'],
              'plan_sha256':sha(canonical(plan)),'draft':plan['draft'],'consumed_nodes':sorted(ids),
              'consumed_inputs':file_inventory(inv.root,sorted(inputs)),
              'generated_files':[{'path':'generated/'+p,'sha256':sha(b),'bytes':len(b)} for p,b in sorted(data.items())],
              'raw_sources_omitted':sorted(x for x in raw_files if x and x in inputs),
              'meaning':'Exact stored bytes are reused; independent mathematical and output readings are still required.'}
    with writer(root):
        stage=Path(tempfile.mkdtemp(prefix='.prepare-',dir=out))
        try:
            for p,b in data.items():atomic_bytes(stage/'generated'/p,b)
            write_json(stage/'generated/manifest.json',manifest)
            for p,b in materials.items():atomic_bytes(stage/'materials'/p,b)
            write_json(stage/'materials/materials-manifest.json',manifest)
            for folder in ('generated','materials'):
                target=out/folder
                if target.exists():shutil.rmtree(target)
                (stage/folder).rename(target)
        finally:shutil.rmtree(stage,ignore_errors=True)
        if not (out/'outline.md').exists():
            order=topological(inv.nodes,ids) if plan['profile']=='lecture' else [s['node_id'] for s in plan['selections']]
            behavior={'minimal':'Put the usable question and exact answer early; retain the key calculation and decisive boundary.',
                      'thematic':'Organize by the selected question and supported relations, not a paper-by-paper bibliography.',
                      'lecture':'Develop prerequisite definitions and the promised proof steps; state imported inputs accurately.'}[plan['profile']]
            atomic_bytes(out/'outline.md',('# Writing task\n\n'+behavior+'\n\nReader goals:\n'+''.join('- '+g+'\n' for g in plan['reader_goals'])+'\nSuggested nodes (editable pedagogical order):\n'+''.join('- [['+k+']]\n' for k in order)+'\nNo semantic or visual review has been performed by this preparation command.\n').encode())
        if not (out/'manuscript/math-review.sty').exists():
            atomic_bytes(out/'manuscript/math-review.sty',(SKILL_ROOT/'assets/templates/math-review.sty').read_bytes())
        if not (out/'manuscript/main.tex').exists():
            template=(SKILL_ROOT/f"assets/templates/profile-{plan['profile']}.tex").read_text(encoding='utf-8')
            snippets=[]
            for s in plan['selections']:
                if s['statement_treatment']=='full':
                    key=s['node_id']; env='definition' if inv.nodes[key].meta['kind']=='definition' else 'theorem'
                    snippets.append(f'\\begin{{{env}}}\\label{{node:{key}}}\n\\input{{../generated/statements/{key}.tex}}\n\\end{{{env}}}\n')
            text=template.replace('@@TITLE@@',tex_text(plan['title'])).replace('@@STATEMENTS@@','\n'.join(snippets))
            notice='\\noindent\\textbf{DRAFT\\_UNVERIFIED: source and mathematical review may be incomplete.}\n' if plan['draft'] else ''
            atomic_bytes(out/'manuscript/main.tex',text.replace('@@DRAFT@@',notice).encode())
    return result('output.prepare','DRAFT_PREPARED' if plan['draft'] else 'PREPARED',{'output':out.relative_to(root).as_posix(),'snapshot_id':plan['snapshot_id'],'readiness':ready,'main_preserved':True})

def verify_generated(root:Path,plan:dict)->dict:
    inv=validate_plan(root,plan);out=safe(root,'outputs/'+plan['output_id']);expected=expected_generated(inv,plan)
    manifest=read_json(safe(out,'generated/manifest.json',True))
    require(manifest.get('snapshot_id')==plan['snapshot_id'] and manifest.get('plan_sha256')==sha(canonical(plan)),'GENERATED_INPUT_STALE','Plan changed; explicitly prepare again before use','generated/manifest.json')
    actual=set(all_files(out,'generated'))
    require(actual=={'generated/'+p for p in expected}|{'generated/manifest.json'},'CANONICAL_STATEMENT_CHANGED','Generated files have extra or missing content','generated')
    for p,b in expected.items():
        require(safe(out,'generated/'+p,True).read_bytes()==b,'CANONICAL_STATEMENT_CHANGED','Generated content differs from fixed snapshot','generated/'+p)
    expected_records=[{'path':'generated/'+p,'sha256':sha(b),'bytes':len(b)} for p,b in sorted(expected.items())]
    require(manifest.get('generated_files')==expected_records and manifest.get('consumed_inputs')==file_inventory(inv.root,sorted(consumed_paths(inv,plan))),
            'GENERATED_INPUT_STALE','Generated manifest does not bind actual fixed inputs','generated/manifest.json')
    # The generated theorem alone is insufficient: prose is written using all
    # supplied materials, which must retain the same snapshot authority.
    materials=expected_materials(inv,plan,assess_readiness(root,plan))
    expected_members={'materials/'+p for p in materials}|{'materials/materials-manifest.json'}
    actual_members=set(all_files(out,'materials'))
    mismatch=sorted(expected_members ^ actual_members)
    require(not mismatch,'MATERIALS_CHANGED','Authoring materials gained or lost snapshot inputs; explicitly prepare again',
            mismatch[0] if mismatch else 'materials')
    for p,b in materials.items():
        require(safe(out,'materials/'+p,True).read_bytes()==b,'MATERIALS_CHANGED',
                'Authoring material differs from the fixed snapshot; edit knowledge and freeze, or prepare again','materials/'+p)
    require(safe(out,'materials/materials-manifest.json',True).read_bytes()==safe(out,'generated/manifest.json',True).read_bytes(),
            'MATERIALS_CHANGED','Material manifest differs from the verified generation manifest','materials/materials-manifest.json')
    return manifest

def output_inputs(out:Path)->set[str]:
    paths={'plan.json','outline.md'}|set(all_files(out,'manuscript'))|set(all_files(out,'generated'))
    # Also bind the authoring materials actually supplied to the reader/agent.
    paths |= set(all_files(out,'materials'))
    return paths

def expand_tex(out:Path,path:Path,active:tuple[Path,...]=())->tuple[str,set[str]]:
    """Inspect the actual entry point with compiler-relative input resolution."""
    from .tex import inspect_tex
    require(path.resolve() == (out/'manuscript/main.tex').resolve(), 'TEX_INPUT_UNSUPPORTED', 'Inspect from the actual entry point')
    scan = inspect_tex(out)
    return scan.text, scan.inputs

def validate_structure(root:Path,output_id:str)->dict:
    out=safe(root,'outputs/'+output_id);plan=load_plan(out/'plan.json');verify_generated(root,plan)
    from .tex import inspect_tex
    scan=inspect_tex(out);text=scan.text;used=scan.inputs
    from .structure import inventory as tex_inventory,public_inventory
    inv=tex_inventory(text);errors=list(scan.errors);warnings=[]
    # Ordinary boundary prose is allowed; explicit unfinished scaffold markers are not.
    inv['has_placeholder']=bool(re.search(r'\\placeholder\b|\b(?:TODO|TBD)\b|\[INSERT',text,re.I) or re.search(r'\bPENDING\b',text))
    labels=inv['labels']
    if len(labels)!=len(set(labels)):errors.append(diagnostic('DUPLICATE_LABEL','Repeated TeX labels','manuscript/main.tex'))
    if inv['has_placeholder']:errors.append(diagnostic('MANUSCRIPT_INCOMPLETE','Visible scaffold placeholders remain','manuscript/main.tex'))
    for s in plan['selections']:
        path=f"generated/statements/{s['node_id']}.tex"
        if s['statement_treatment']=='full' and path not in scan.body_inputs:
            errors.append(diagnostic('CANONICAL_STATEMENT_MISSING','Full selected statement is not literally included in the visible manuscript body',path,s['node_id']))
    body=text.split(r'\begin{document}',1)[-1].split(r'\end{document}',1)[0]
    if plan['draft'] and not re.search(r'DRAFT(?:\\)?_UNVERIFIED|DRAFT\\_UNVERIFIED',body):
        errors.append(diagnostic('DRAFT_NOTICE_MISSING','Unverified manuscript must visibly identify its draft status','manuscript/main.tex'))
    return result('output.structure','NEEDS_WORK' if errors else 'STRUCTURALLY_VALID',{'tex_inventory':public_inventory(inv),'actual_literal_inputs':sorted(used),'body_inputs':sorted(scan.body_inputs),'canonical_locations':scan.locations},errors,warnings)
