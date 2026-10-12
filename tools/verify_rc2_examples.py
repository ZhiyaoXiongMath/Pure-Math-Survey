#!/usr/bin/env python3
"""Recheck and rebuild authored rc2 inputs with a chosen installed runtime.

Never writes accepted readings. A rebuild has no inherited visual acceptance.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]


def verify(repository:Path,destination:Path,skill:Path,build:bool=True)->dict:
    if destination.exists():raise FileExistsError('Use a fresh verification directory')
    sys.path.insert(0,str(skill/'scripts'))
    import survey_core
    from survey_core.models import load_plan
    from survey_core.snapshots import verify_snapshot
    from survey_core.readiness import assess_readiness
    from survey_core.exports import prepare_output,validate_structure,output_inputs,verify_generated
    from survey_core.reviews import reviews_in,find_review
    from survey_core.release import semantic_scope_errors
    from survey_core.build import build_output,render_output
    from survey_core.profiles import OUTPUT_SCHEMA, RC2_POLICY
    from survey_core.common import sha
    if not Path(survey_core.__file__).resolve().is_relative_to(skill.resolve()):
        raise RuntimeError('Imported development runtime instead of requested installation')
    specs=[('time-compactness',repository/'examples/rc2/projects/time-compactness',
            ('thematic','minimal-methods','minimal-boundaries')),
           ('schur',repository/'examples/vnext/projects/schur',('rc2-lecture',))]
    report={'status':'PASS','runtime':str(Path(survey_core.__file__).resolve()),
            'outputs':[],'snapshots_verified':0,'new_pdf_visual_review':'NOT PERFORMED',
            'mathematical_reading':'Stored located author readings rechecked for bindings, not newly performed',
            'independent_mathematical_review':'NOT VERIFIED','real_reader_feedback':'NOT VERIFIED',
            'original_paper_quality':'NOT VERIFIED: no authorized original input'}
    spines=[];statements=[]
    for name,source,ids in specs:
        project=destination/name
        shutil.copytree(source,project,ignore=shutil.ignore_patterns('build','history','__pycache__'))
        for snapshot in sorted((project/'snapshots').glob('KB-*')):
            verify_snapshot(project,snapshot.name);report['snapshots_verified']+=1
        for oid in ids:
            out=project/'outputs'/oid;plan=load_plan(out/'plan.json')
            if (plan['schema_version'],plan.get('editorial_policy')) != (OUTPUT_SCHEMA,RC2_POLICY) or plan['draft']:
                raise AssertionError('Expected authored recorded rc2 nondraft output: '+oid)
            before={p:p.read_bytes() for p in (out/'outline.md',out/'manuscript/main.tex',out/'manuscript/math-review.sty')}
            verify_generated(project,plan)
            prepared=prepare_output(project,out/'plan.json')
            if any(p.read_bytes()!=value for p,value in before.items()):raise AssertionError('Prepare replaced authorship')
            if prepared['artifacts']['exposition_design']['status']!='COMPLETE':raise AssertionError('Incomplete concrete design')
            ready=assess_readiness(project,plan);structure=validate_structure(project,oid)
            if ready['status']!='READY' or structure['errors']:
                raise AssertionError({'output':oid,'readiness':ready,'structure':structure})
            review,errors=find_review(out,reviews_in(out,'evidence'),'output_semantic','output_ids',oid,
                output_inputs(out),lambda r:semantic_scope_errors(out,plan,ready['artifacts']['consumed_nodes'],r))
            if review is None:raise AssertionError({'output':oid,'semantic':errors})
            row={'project':name,'output_id':oid,'profile':plan['profile'],'view':plan['view'],
                 'recorded_policy':RC2_POLICY,'evaluated_policy':RC2_POLICY,'release_authorized':False,
                 'snapshot_id':plan['snapshot_id'],'readiness':'READY','structure':'STRUCTURALLY_VALID',
                 'stored_semantic_review_id':review['review_id'],'reviewer_mode':review['reviewer_mode'],
                 'design':'COMPLETE','prepared_from_requested_installation':True}
            if name=='time-compactness' and oid in {'minimal-methods','minimal-boundaries'}:
                spines.append((plan['snapshot_id'],set(plan['question_ids']),
                    {s['node_id'] for s in plan['selections'] if s['role']=='principal_answer'},
                    {s['node_id'] for s in plan['selections'] if s['role']=='boundary'},plan['comparison_group']))
                statements.append({s['node_id']:sha((out/'generated/statements'/f"{s['node_id']}.tex").read_bytes())
                                   for s in plan['selections'] if s['role']=='principal_answer'})
            if build:
                built=build_output(project,oid);rendered=render_output(project,oid,dpi=100)
                row.update(build=built['status'],pages=built['artifacts']['pages'],render=rendered['status'],
                           new_visual_review='NOT PERFORMED')
            else:row['build']='NOT EXECUTED (--no-build)'
            report['outputs'].append(row)
    if len(spines)!=2 or spines[0]!=spines[1] or not spines[0][-1] or statements[0]!=statements[1]:
        raise AssertionError('Methods/boundaries core or canonical statements differ')
    report['paired_canonical_spine']='IDENTICAL: emphasis quality needs actual reading'
    return report


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repository',type=Path,default=ROOT)
    ap.add_argument('--skill-root',type=Path,default=ROOT/'skills/pure-math-survey')
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--report',type=Path)
    ap.add_argument('--no-build',action='store_true');args=ap.parse_args()
    try:report=verify(args.repository.resolve(),args.output.resolve(),args.skill_root.resolve(),not args.no_build)
    except Exception as exc:report={'status':'FAIL','error':f'{type(exc).__name__}: {exc}'}
    text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(text,encoding='utf-8')
    print(text,end='');return 0 if report['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
