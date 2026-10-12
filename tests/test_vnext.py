"""vNext behavioral/adversarial tests. ALL accepted records here are SYNTHETIC.

They exercise executable gates, not truth, originality or reader comprehension.
Actual known-mathematics benchmarks and author findings live in examples/vnext.
"""
from __future__ import annotations
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from test_v2 import (fixture, synthetic_reviews, putnode, plan as legacy_plan,
                     ROOT, SKILL, SCRIPTS, SurveyError, read_json, write_json, now)
from survey_core.common import file_hash, sha
from survey_core.models import load_plan, load_node
from survey_core.knowledge import inventory, validate_knowledge
from survey_core.plans import create_plan, validate_plan
from survey_core.snapshots import freeze_snapshot, verify_snapshot
from survey_core.exports import prepare_output, validate_structure, verify_generated, output_inputs
from survey_core.reviews import review_template, mathematical_inputs, load_review
from survey_core.release import semantic_scope_errors, assess_release, package_output
from survey_core.readiness import assess_readiness
from survey_core.profiles import (POLICY, RC2_POLICY, OUTPUT_SCHEMA, MINIMAL_SECTIONS, COMMON_READINGS,
    MODE_READINGS, STATEMENT_ASPECTS, principal_template, review_scope_template,
    statement_warnings, semantic_profile_errors, validate_plan_contract)
from package_release import package

STEP='Substitute x=0 into x times x and obtain zero.'
SYNTH='SYNTHETIC gate fixture, not mathematical, original-research or reader acceptance.'
CHECKS=['whole_manuscript','canonical_use','conditions_quantifiers','selection','attribution','proof_obligations','readability']


def synthetic_policy_reviews(root):
    inv=inventory(root)
    for key,n in inv.nodes.items():
        scope={'editorial_policy':POLICY,'node_ids':[key],'evidence_basis':SYNTH,
               'proof_steps':{key:[STEP]},'statement_reviews':{}}
        if n.statement is not None:
            item=principal_template(n.statement);item.update(outcome='accepted')
            item.update({k:SYNTH for k in STATEMENT_ASPECTS});scope['statement_reviews'][key]=item
        rec=review_template(root,'mathematical',[key],mathematical_inputs(inv,key),scope)
        rec.update(review_id='SYNTHETIC-NEW-'+key,reviewer_mode='author_reread',reviewed_at=now(),
                   findings=[SYNTH],unchecked_items=[],disposition='accepted')
        write_json(root/f'evidence/reviews/new-{key}.json',rec)
    # Explicitly synthetic r3 knowledge-task evidence, separate from manuscript
    # findings; the cited sections and input bytes must still really exist.
    from survey_core.reviews import coverage_inputs, knowledge_scope_template
    from survey_core.profiles import R3_READINGS
    for q in inv.coverage['questions']:
        key=q['question_id'];scope=knowledge_scope_template(inv,[key])
        scope['evidence_basis']=SYNTH
        rec=review_template(root,'coverage',[key],coverage_inputs(inv,key),scope)
        rec.update(review_id='SYNTHETIC-KNOWLEDGE-'+key,reviewer_mode='author_reread',reviewed_at=now(),
                   findings=[f'{task}: {SYNTH} [Actual fixture section]({inv.nodes[key].path}#software-fixture)' for task in R3_READINGS],
                   unchecked_items=[],disposition='accepted')
        write_json(root/f'evidence/reviews/new-coverage-{key}.json',rec)


class VNext(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
        self.root=fixture(self.base/'project',reviewed=True)
        synthetic_policy_reviews(self.root)
    def tearDown(self):self.tmp.cleanup()
    def make(self,profile='minimal',oid='new',draft=True,refine=True,view='integrated',policy=None):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id']
        create_plan(self.root,oid,sid,profile=profile,draft=draft,view=view)
        p=self.root/f'outputs/{oid}/plan.json';v=read_json(p)
        v['editorial_policy']=policy or getattr(self,'editorial_policy',POLICY)
        write_json(p,v)
        if refine:
            for o in v['proof_obligations']:o['required_steps']=[STEP]
            write_json(p,v)
        return p,v
    def authored(self,profile='minimal',oid='new',draft=True,view='integrated',policy=None):
        p,v=self.make(profile,oid,draft,view=view)
        if policy is not None:v['editorial_policy']=policy
        v['audience']='Synthetic fixture reader can substitute real numbers and multiply.'
        v['reader_goals']=['Reconstruct the substitution of zero in x times x; no research acceptance.']
        write_json(p,v);prepare_output(self.root,p)
        (p.parent/'outline.md').write_text('Synthetic design: multiply the assumed x=0 to obtain x squared=0. This is only a software fixture.\n')
        text=(p.parent/'manuscript/main.tex').read_text()
        # This synthetic manuscript is explicitly not a mathematical benchmark.
        import re
        text=re.sub(r'\\placeholder\{[^{}]*\}',SYNTH,text)
        text=text.replace(r'\bibliography{../generated/references}',r'\nocite{S-test}\bibliography{../generated/references}')
        (p.parent/'manuscript/main.tex').write_text(text)
        return p,v
    def codes(self,oid='new'):
        return {x['code'] for x in validate_structure(self.root,oid)['errors']}
    def readiness(self,v):return {x['code'] for x in assess_readiness(self.root,v)['errors']}
    def failcode(self,code,fn,*a,**kw):
        with self.assertRaises(SurveyError) as cm:fn(*a,**kw)
        self.assertEqual(cm.exception.diagnostic['code'],code)
    def sem(self,p,v):
        # Explicitly author a real (trivial) computation in this SYNTHETIC
        # fixture. Proof findings must never point merely at a theorem input.
        out=p.parent;main=out/'manuscript/main.tex';text=main.read_text()
        computation=r'For $x=0$, substitution gives $x^2=0\cdot 0=0$. This is a synthetic software fixture.'
        if computation not in text:
            text=text.replace(r'\end{document}',computation+'\n'+r'\end{document}');main.write_text(text)
        lines=text.splitlines()
        def loc(n):return {'path':'manuscript/main.tex','line_start':n,'line_end':n}
        principal=next(i for i,l in enumerate(lines,1) if 'statements/N-main.tex' in l)
        proof=lines.index(computation)+1
        scope=review_scope_template(v)
        scope.update(output_ids=[v['output_id']],profile=v['profile'],node_ids=['N-q','N-def','N-main'],
            whole_manuscript=True,checks=CHECKS,principal_locations={'N-main':[loc(principal)]},
            proof_steps={o['node_id']:o['required_steps'] for o in v['proof_obligations']},
            proof_locations={o['node_id']:[loc(proof)] for o in v['proof_obligations']})
        for key in scope['mode_findings']:scope['mode_findings'][key]={'outcome':'accepted','finding':SYNTH,'locations':[loc(proof)]}
        if 'view_focus' in scope['mode_findings']:scope['mode_findings']['view_focus']['node_ids']=['N-main']
        for steps in scope['proof_step_findings'].values():
            for key in steps:steps[key]={'outcome':'accepted','finding':SYNTH,'locations':[loc(proof)]}
        item=principal_template((out/'generated/statements/N-main.tex').read_bytes());item['outcome']='accepted'
        item.update({k:SYNTH for k in STATEMENT_ASPECTS});scope['statement_reviews']['N-main']=item
        r=review_template(out,'output_semantic',[v['output_id']],output_inputs(out),scope)
        r.update(review_id='SYNTHETIC-OUTPUT',reviewer_mode='author_reread',reviewed_at=now(),disposition='accepted',findings=[SYNTH],unchecked_items=[])
        return r
    def paper(self):
        putnode(self.root,'N-prior','result',r'For $x\in\mathbb R$, $0x=0$.',source=True,status='established')
        putnode(self.root,'N-compare','relation',r'This is only a synthetic comparison fixture; it asserts no novelty.',
                links=[] if getattr(self,'isolated_comparison',False) else [('N-main','compares_with'),('N-prior','compares_with')],status='established')
        synthetic_reviews(self.root);synthetic_policy_reviews(self.root)
        source_path=self.root/'evidence/reviews/source-S-test.json';source_review=read_json(source_path)
        source_review['scope']['source_reading']={'S-test':dict(mode='original_text_local',version='Fixture v1',locators=['Synthetic fixture paragraph 1'])}
        write_json(source_path,source_review)
        p,v=self.make('paper')
        for key in ['N-prior','N-compare']:
            v['selections'].append({'node_id':key,'role':'background','statement_treatment':'full','proof_treatment':'citation','reason':SYNTH})
        v['contributions']=[dict(node_id='N-main',classification='original',provenance=SYNTH,authorization=SYNTH,
            actual_difference=SYNTH,proof_status='complete',closest_prior_results=['N-prior'],comparison_bindings=[dict(comparison_node_id='N-compare',prior_result_id='N-prior')],gaps=[])]
        write_json(p,v)
        return p,v

    def test_V41_earlier_math_review_does_not_shadow_new_proof_scope(self):
        path=self.root/'evidence/reviews/new-N-main.json'
        later=read_json(path)
        changed_step='SYNTHETIC second mode obligation, not mathematical evidence.'
        later['review_id']='SYNTHETIC-LATER-PROOF'
        later['scope']['proof_steps']['N-main']=[changed_step]
        write_json(self.root/'evidence/reviews/zz-later-proof.json',later)
        p,v=self.make(draft=False)
        v['proof_obligations'][0]['required_steps']=[changed_step]
        write_json(p,v)
        result=assess_readiness(self.root,v)
        self.assertEqual(result['status'],'READY',result['errors'])
        self.assertIn('SYNTHETIC-LATER-PROOF',result['artifacts']['used_review_ids'])

    def test_V42_no_math_review_of_new_promised_step_still_blocks(self):
        p,v=self.make(draft=False)
        v['proof_obligations'][0]['required_steps']=['SYNTHETIC unchecked new promise.']
        self.assertIn('PROOF_OBLIGATION_UNMET',self.readiness(v))

    def test_V01_four_cli_modes_and_distinct_outlines(self):
        outlines=set()
        for profile in ['minimal','thematic','lecture','paper']:
            with self.subTest(profile=profile):
                p,v=self.make(profile,profile)
                run=subprocess.run([sys.executable,str(SCRIPTS/'survey.py'),'output','prepare',str(self.root),'--plan',str(p),'--json'],capture_output=True,text=True)
                self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                text=(p.parent/'outline.md').read_text();outlines.add(text)
                self.assertIn('Exposition Contract',text);self.assertIn('Assumed / Refreshable / Bridge-required',text)
                self.assertIn('PENDING',text);self.assertEqual(load_plan(p)['editorial_policy'],POLICY)
        self.assertEqual(len(outlines),4)
    def test_V02_new_defaults_have_real_mode_specific_proof_work_pending(self):
        for mode in ['minimal','thematic','lecture','paper']:
            p,v=self.make(mode,mode,refine=False)
            self.assertIn('PROOF_OBLIGATION_UNMET',self.readiness(v))
            self.assertNotIn('Readers of the selected mathematical scope',v['audience'])
            self.assertTrue(v['proof_obligations'])
    def test_V03_minimal_real_three_sections_and_methods_view(self):
        self.authored(view='methods',policy=RC2_POLICY);self.assertEqual(self.codes(),set())
    def test_V04_minimal_extra_numbered_section_fails(self):
        p,v=self.authored(policy=RC2_POLICY);main=p.parent/'manuscript/main.tex'
        main.write_text(main.read_text().replace(r'\end{document}',r'\section{Appendix}Extra.\end{document}'))
        self.assertIn('MINIMAL_THREE_SECTIONS_REQUIRED',self.codes())
    def test_V05_background_before_results_fails(self):
        p,v=self.authored(policy=RC2_POLICY);m=p.parent/'manuscript/main.tex'
        m.write_text(m.read_text().replace(r'\section{Main Results}',r'\section*{Background}\section{Main Results}'))
        self.assertIn('MINIMAL_RESULTS_FIRST',self.codes())
    def test_V06_titles_in_comments_false_or_uncalled_macro_do_not_count(self):
        p,v=self.authored(policy=RC2_POLICY);m=p.parent/'manuscript/main.tex';original=m.read_text()
        for wrapper in [lambda x:'%'+x,lambda x:r'\iffalse '+x+r'\fi',lambda x:r'\newcommand{\unused}{'+x+'}']:
            with self.subTest(wrapper=wrapper):
                m.write_text(original.replace(r'\section{Key Mathematical Ingredients}',wrapper(r'\section{Key Mathematical Ingredients}')))
                self.assertIn('MINIMAL_THREE_SECTIONS_REQUIRED',self.codes())
    def test_V07_principal_in_later_section_fails(self):
        p,v=self.authored(policy=RC2_POLICY);m=p.parent/'manuscript/main.tex';t=m.read_text();a=t.index(r'\begin{theorem}');b=t.index(r'\end{theorem}',a)+len(r'\end{theorem}')
        theorem=t[a:b];t=t[:a]+t[b:];t=t.replace(r'\section{Connecting the Ingredients}',r'\section{Connecting the Ingredients}'+theorem);m.write_text(t)
        self.assertIn('MINIMAL_PRINCIPAL_NOT_FIRST',self.codes())
    def test_V08_plain_principal_input_without_formal_result_fails(self):
        p,v=self.authored(policy=RC2_POLICY);m=p.parent/'manuscript/main.tex'
        m.write_text(m.read_text().replace(r'\begin{theorem}', '').replace(r'\end{theorem}',''))
        self.assertIn('PRINCIPAL_RESULT_ENVIRONMENT_MISSING',self.codes())
    def test_V09_section_number_suppression_fails(self):
        p,v=self.authored(policy=RC2_POLICY);m=p.parent/'manuscript/main.tex';t=m.read_text()
        for control in [r'\setcounter{secnumdepth}{-1}',r'\renewcommand{\thesection}{}',r'\appendix']:
            with self.subTest(control=control):
                m.write_text(t.replace(r'\begin{document}',control+r'\begin{document}'))
                self.assertIn('MINIMAL_NUMBERING_UNSUPPORTED',self.codes())
    def test_V10_thematic_and_lecture_do_not_require_fixed_sections(self):
        for mode in ['thematic','lecture']:
            p,v=self.authored(mode,mode);m=p.parent/'manuscript/main.tex'
            m.write_text(m.read_text().replace(r'\end{document}',r'\section{Additional useful model}Model.\end{document}'))
            self.assertFalse(self.codes(mode))
    def test_V11_self_contained_hazard_is_advisory_not_global_eqref_ban(self):
        self.assertTrue(statement_warnings('N-main',b'Under (1.2), obtain (1.7).'))
        self.assertTrue(statement_warnings('N-main',br'Assume \eqref{a}. Then the conclusion above holds.'))
        p,v=self.authored();m=p.parent/'manuscript/main.tex'
        m.write_text(m.read_text().replace(r'\end{document}',r'In the proof use \eqref{identity}.\end{document}'))
        self.assertNotIn('STATEMENT_SELF_CONTAINED_RISK',{x['code'] for x in validate_structure(self.root,'new')['warnings']})
    def test_V12_old_math_accepted_record_cannot_pass_new_statement_reading(self):
        for path in (self.root/'evidence/reviews').glob('new-*.json'):path.unlink()
        p,v=self.make();self.assertIn('PRINCIPAL_SELF_CONTAINED_REVIEW_PENDING',self.readiness(v))
    def test_V13_later_valid_math_record_is_not_shadowed_by_old_record(self):
        p,v=self.make(draft=False);self.assertFalse(self.readiness(v))
    def test_V14_statement_review_hash_and_each_aspect_required(self):
        path=self.root/'evidence/reviews/new-N-main.json';original=read_json(path)
        for aspect in [*STATEMENT_ASPECTS,'canonical_sha256','outcome']:
            with self.subTest(aspect=aspect):
                v=copy.deepcopy(original);v['scope']['statement_reviews']['N-main'][aspect]=''
                write_json(path,v);p,pl=self.make(oid='case-'+aspect)
                self.assertIn('PRINCIPAL_SELF_CONTAINED_REVIEW_PENDING',self.readiness(pl))
        write_json(path,original)
    def test_V15_legacy_plan_preserved_and_labeled_not_new_acceptance(self):
        p=legacy_plan(self.root);before=p.read_bytes();prepare_output(self.root,p,draft=True)
        main=p.parent/'manuscript/main.tex';main.write_text('Author historical prose.\n');outline=p.parent/'outline.md';outline.write_text('Authored historical outline.\n')
        prepare_output(self.root,p);self.assertEqual(p.read_bytes(),before);self.assertEqual(main.read_text(),'Author historical prose.\n');self.assertEqual(outline.read_text(),'Authored historical outline.\n')
    def test_V16_schema_downgrade_and_paper_disguised_as_legacy_rejected(self):
        p,v=self.make();v['schema_version']='2.0.0';write_json(p,v)
        self.failcode('SCHEMA_UNSUPPORTED',load_plan,p)
        v.pop('editorial_policy');v.pop('contributions');v['profile']='paper';write_json(p,v)
        self.failcode('SCHEMA_UNSUPPORTED',load_plan,p)
    def test_V17_new_prepare_preserves_authored_text_outline_and_snapshots(self):
        p,v=self.authored();main=p.parent/'manuscript/main.tex';outline=p.parent/'outline.md'
        outline.write_text('Author-selected route, not the whole project overview.\n')
        before=[main.read_bytes(),outline.read_bytes()];prepare_output(self.root,p)
        self.assertEqual(before,[main.read_bytes(),outline.read_bytes()]);self.assertEqual(verify_snapshot(self.root,v['snapshot_id'])['status'],'VERIFIED')
    def test_V18_knowledge_only_keeps_zero_outputs(self):
        validate_knowledge(self.root);freeze_snapshot(self.root)
        self.assertFalse((self.root/'outputs').exists())
    def test_V19_legacy_semantic_checkboxes_not_current_acceptance(self):
        p,v=self.authored();r=self.sem(p,v);r['schema_version']='2.0.0';r['scope'].pop('editorial_policy')
        self.assertIn('EDITORIAL_REVIEW_POLICY_MISMATCH',{x['code'] for x in semantic_scope_errors(p.parent,v,['N-main','N-def','N-q'],r)})
    def test_V20_current_semantic_synthetic_positive_contract(self):
        p,v=self.authored();self.assertEqual(semantic_scope_errors(p.parent,v,['N-main','N-def','N-q'],self.sem(p,v)),[])
    def test_V21_every_mode_finding_must_have_content_and_location(self):
        p,v=self.authored();original=self.sem(p,v)
        for key in COMMON_READINGS+MODE_READINGS['minimal']:
            with self.subTest(key=key):
                r=copy.deepcopy(original);r['scope']['mode_findings'][key]['finding']=''
                self.assertTrue(semantic_profile_errors(p.parent,v,r))
                r=copy.deepcopy(original);r['scope']['mode_findings'][key]['locations']=[]
                self.assertTrue(semantic_profile_errors(p.parent,v,r))
    def test_V22_semantic_failure_cases_are_reviewed_not_automatically_inferred(self):
        cases=[('minimal','point_use','Points are not used by the third section.'),
               ('minimal','decisive_connections','The only transition is standard argument; the decisive substitution is missing.'),
               ('minimal','statement_context','The surrounding text changes some into every.'),
               ('minimal','display_rhythm','The inserted display is ornamental and does not advance this argument.'),
               ('thematic','comparison_basis','The purported equivalence changes regularity and normalization.'),
               ('thematic','question_structure','Only author/year summaries occur; no mathematical question organizes the text.'),
               ('lecture','worked_derivations','The promised nonlinear limit is not justified in the stated weak topology.'),
               ('lecture','imported_inputs','An imported result is incorrectly described as proved here.')]
        for i,(mode,key,finding) in enumerate(cases):
            with self.subTest(finding=finding):
                p,v=self.authored(mode,str(i));r=self.sem(p,v)
                r['scope']['mode_findings'][key].update(outcome='revise',finding=finding)
                self.assertTrue(semantic_profile_errors(p.parent,v,r))
    def test_V23_lecture_step_missing_even_with_global_proof_check_fails(self):
        p,v=self.authored('lecture');r=self.sem(p,v);r['scope']['proof_step_findings']['N-main']={}
        self.assertIn('MODE_SEMANTIC_REVIEW_PENDING',{x['code'] for x in semantic_profile_errors(p.parent,v,r)})
    def test_V24_malformed_new_review_maps_fail_closed_without_crash(self):
        p,v=self.authored();original=self.sem(p,v)
        for key in ['mode_findings','proof_step_findings','statement_reviews']:
            r=copy.deepcopy(original);r['scope'][key]=[]
            self.assertTrue(semantic_profile_errors(p.parent,v,r))
    def test_V25_statement_semantic_rejection_for_omitted_quantifier(self):
        p,v=self.authored();r=self.sem(p,v);r['scope']['statement_reviews']['N-main'].update(outcome='revise',quantifiers='The intended universal quantifier is absent from the actual statement.')
        self.assertTrue(semantic_profile_errors(p.parent,v,r))
    def test_V26_pending_review_template_never_accepts(self):
        p,v=self.authored();run=subprocess.run([sys.executable,str(SCRIPTS/'survey.py'),'output','review-template',str(self.root),'--output','new','--kind','output_semantic','--json'],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout);import json
        r=json.loads(run.stdout)['artifacts']['review'];self.assertEqual(r['reviewer_mode'],'not_performed');self.assertNotEqual(r['disposition'],'accepted');self.assertTrue(semantic_profile_errors(p.parent,v,r))
    def test_V27_principal_review_cli_creates_pending_exact_hash(self):
        run=subprocess.run([sys.executable,str(SCRIPTS/'survey.py'),'review','template',str(self.root),'--kind','mathematical','--id','N-main','--principal-statements','--json'],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout);import json
        r=json.loads(run.stdout)['artifacts']['review'];self.assertEqual(r['schema_version'],OUTPUT_SCHEMA);self.assertEqual(r['scope']['statement_reviews']['N-main']['outcome'],'not_performed')
    def test_V28_paper_defaults_draft_even_without_draft_flag(self):
        p,v=self.make('paper',draft=False);self.assertTrue(v['draft']);self.assertEqual(v['contributions'][0]['classification'],'unverified')
        self.assertIn('PAPER_ORIGINAL_CONTRIBUTION_MISSING',self.readiness(v))
    def test_V29_paper_no_prior_art_cannot_be_formal(self):
        p,v=self.paper();v['contributions'][0]['closest_prior_results']=[]
        self.assertIn('PAPER_PRIOR_ART_MISSING',self.readiness(v))
    def test_V30_paper_gap_or_incomplete_proof_cannot_be_formal(self):
        p,v=self.paper();self.assertFalse(self.readiness(v),self.readiness(v))
        c=v['contributions'][0];c['gaps']=['Unproved uniform estimate.'];self.assertIn('PAPER_PROOF_GAP',self.readiness(v))
        c['gaps']=[];c['proof_status']='incomplete';self.assertIn('PAPER_PROOF_NOT_CLOSED',self.readiness(v))
    def test_V31_classic_result_cannot_supply_paper_originality(self):
        p,v=self.paper();v['contributions'][0]['classification']='known'
        self.assertIn('PAPER_ORIGINAL_CONTRIBUTION_MISSING',self.readiness(v))
    def test_V32_paper_requires_authorized_provenance_and_comparison_relation(self):
        p,v=self.paper();v['contributions'][0]['authorization']='';self.assertIn('PAPER_PROVENANCE_UNVERIFIED',self.readiness(v))
        v['contributions'][0]['comparison_bindings'][0]['comparison_node_id']='N-def';self.failcode('CONTRIBUTION_INVALID',validate_plan,self.root,v)
    def test_V33_paper_unknown_prior_and_self_prior_rejected(self):
        p,v=self.paper();c=v['contributions'][0];c['closest_prior_results']=['N-absent']
        # consumption may discover the unknown before profile checks; both reject, never ignore.
        with self.assertRaises(SurveyError):validate_plan(self.root,v)
        c['closest_prior_results']=['N-main'];self.failcode('CONTRIBUTION_INVALID',validate_plan,self.root,v)
    def test_V34_paper_draft_notice_removal_does_not_enable_package(self):
        p,v=self.authored('paper');m=p.parent/'manuscript/main.tex';m.write_text(m.read_text().replace(r'DRAFT\_UNVERIFIED','Unmarked'))
        self.assertIn('DRAFT_NOTICE_MISSING',self.codes())
        self.failcode('DRAFT_NOT_RELEASABLE',package_output,self.root,'new',self.base/'no.zip')
        self.assertFalse((self.base/'no.zip').exists())
    def test_V35_paper_boolean_flip_still_blocked(self):
        p,v=self.authored('paper');v['draft']=False;write_json(p,v)
        self.failcode('READINESS_REQUIRED',prepare_output,self.root,p)
    def test_V36_paper_semantic_prior_art_is_additional_to_lecture(self):
        p,v=self.paper();prepare_output(self.root,p)
        r=self.sem(p,v);key='N-main';loc=r['scope']['principal_locations'][key]
        entry={'outcome':'accepted','finding':SYNTH,'locations':loc,'closest_prior_results':['N-prior'],
               'prior_art_searches':[dict(searched_at=now(),query='SYNTHETIC query',outcome=SYNTH,checked_source_ids=['S-test'])]}
        entry.update({x:SYNTH for x in ['provenance_check','authorization_check','actual_difference','proof_closure','remaining_caveats']})
        entry['prior_result_checks']=[dict(prior_result_id='N-prior',source_id='S-test',version='Fixture v1',locator='Synthetic fixture paragraph 1',outcome='accepted',finding=SYNTH)]
        r['scope']['contribution_reviews'][key]=entry
        self.assertEqual(semantic_profile_errors(p.parent,v,r),[])
        for defect in ['missing','unknown-source','future']:
            q=copy.deepcopy(r)
            if defect=='missing':q['scope']['contribution_reviews'][key]['prior_art_searches']=[]
            elif defect=='unknown-source':q['scope']['contribution_reviews'][key]['prior_art_searches'][0]['checked_source_ids']=['S-fiction']
            else:q['scope']['contribution_reviews'][key]['prior_art_searches'][0]['searched_at']='2999-01-01'
            self.assertIn('PAPER_CONTRIBUTION_REVIEW_PENDING',{x['code'] for x in semantic_profile_errors(p.parent,v,q)})
    def test_V37_install_archive_contains_executable_policy_and_all_resources(self):
        target=self.base/'candidate.zip';package(SKILL,target)
        with zipfile.ZipFile(target) as z:
            names=z.namelist()
            for rel in ['scripts/survey_core/profiles.py','references/reader-calibration.md','references/overview.md','assets/templates/profile-paper.tex']:
                self.assertIn('pure-math-survey/'+rel,names)
            z.extractall(self.base/'installed')
        entry=self.base/'installed/pure-math-survey/scripts/survey.py'
        run=subprocess.run([sys.executable,'-I',str(entry),'--version','--json'],cwd=self.base,capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout);self.assertIn('2.1.0',run.stdout)
    def test_V38_generated_fragment_edit_still_rejected(self):
        p,v=self.authored();(p.parent/'generated/statements/N-main.tex').write_text('A supposedly improved theorem.')
        self.failcode('CANONICAL_STATEMENT_CHANGED',verify_generated,self.root,v)
    def test_V39_thematic_one_route_contract_has_no_artificial_route_quota(self):
        p,v=self.authored('thematic');r=self.sem(p,v)
        r['scope']['mode_findings']['approach_mechanisms']['finding']='SYNTHETIC: only one genuine route is claimed; its assumptions and limitations are recorded.'
        self.assertEqual(semantic_profile_errors(p.parent,v,r),[])
    def test_V40_bad_review_scope_rejected_not_attribute_error(self):
        p,v=self.authored();r=self.sem(p,v);r['scope']=[];q=p.parent/'evidence/bad.json';write_json(q,r)
        self.failcode('REVIEW_INVALID',load_review,q)

if __name__=='__main__':unittest.main()
