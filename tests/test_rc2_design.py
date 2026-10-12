"""Design and historical-policy regressions; all fabricated reviews are synthetic."""
import copy
import unittest
from unittest.mock import patch
import test_vnext as v
from test_v2 import plan as legacy_plan, read_json, write_json, SurveyError
from survey_core.exposition import check_exposition_design
from survey_core.exports import prepare_output, validate_structure, output_inputs
from survey_core.build import build_output
from survey_core.release import assess_release, package_output
from survey_core.reviews import check_review_bindings, load_review
from survey_core.models import load_plan
from survey_core.profiles import RC1_SCHEMA, RC1_POLICY, POLICY, validate_plan_contract

class Design(unittest.TestCase):
    def setUp(self):
        self.t=v.VNext();self.t.setUp();self.t.editorial_policy=v.RC2_POLICY
    def tearDown(self):self.t.tearDown()
    def test_missing_empty_default_and_invalid_reference(self):
        p,plan=self.t.authored(draft=False);out=p.parent
        for text,expected in [('', 'EXPOSITION_DESIGN_MISSING'),
                ('Completed route [[N-unselected]].', 'EXPOSITION_DESIGN_INVALID_REFERENCE'),
                ('TODO: locate the key estimate', 'EXPOSITION_DESIGN_INCOMPLETE')]:
            (out/'outline.md').write_text(text)
            self.assertIn(expected,{e['code'] for e in validate_structure(self.t.root,plan['output_id'])['errors']})
        (out/'outline.md').unlink()
        self.assertEqual(check_exposition_design(out,plan)['status'],'NEEDS_WORK')
    def test_ordinary_words_quotes_and_code_are_allowed(self):
        p,plan=self.t.authored();(p.parent/'outline.md').write_text(
            '> TODO: quoted original task\n```python\nTODO: example_code\n```\nThe pending boundary is explicitly outside the stated domain.\n')
        self.assertEqual(check_exposition_design(p.parent,plan)['errors'],[])
    def test_reserved_marker_cannot_hide_in_comment_or_fence(self):
        p,plan=self.t.authored()
        for text in ('<!-- [[PMS_PENDING:route]] -->','```\n[[PMS_PENDING:route]]\n```'):
            (p.parent/'outline.md').write_text(text)
            self.assertEqual(check_exposition_design(p.parent,plan)['status'],'NEEDS_WORK')
        (p.parent/'outline.md').write_text(r'Literal syntax example: \[[PMS_PENDING:route]].')
        self.assertEqual(check_exposition_design(p.parent,plan)['status'],'COMPLETE')
    def test_deleted_markers_do_not_create_semantic_acceptance(self):
        p,plan=self.t.authored(draft=False);(p.parent/'outline.md').write_text('Done.')
        self.assertEqual(check_exposition_design(p.parent,plan)['status'],'COMPLETE')
        result=assess_release(self.t.root,plan['output_id'])
        self.assertIn('OUTPUT_SEMANTIC_REVIEW_PENDING',{e['code'] for e in result['errors']})
    def test_reprepare_preserves_all_author_files(self):
        p,plan=self.t.authored();paths=[p.parent/x for x in ('outline.md','manuscript/main.tex','manuscript/math-review.sty')]
        before=[x.read_bytes() for x in paths];prepare_output(self.t.root,p)
        self.assertEqual(before,[x.read_bytes() for x in paths])
    def test_draft_preview_builds_with_explicit_limitations(self):
        p,plan=self.t.make();prepare_output(self.t.root,p)
        result=build_output(self.t.root,plan['output_id']);self.assertEqual(result['status'],'BUILT')
        report=read_json(p.parent/'build/build-report.json')
        self.assertTrue(report['draft_preview']);self.assertTrue(report['preview_limitations'])
        self.t.failcode('DRAFT_NOT_RELEASABLE',package_output,self.t.root,plan['output_id'],self.t.base/'forbidden.zip')
        self.assertTrue(read_json(p)['draft'])
    def test_missing_outline_can_be_previewed_not_released(self):
        p,plan=self.t.authored();(p.parent/'outline.md').unlink()
        self.assertEqual(build_output(self.t.root,plan['output_id'])['status'],'BUILT')
        self.assertIn('EXPOSITION_DESIGN_MISSING',{e['code'] for e in assess_release(self.t.root,plan['output_id'])['errors']})
    def test_nondraft_design_cannot_build_or_change_draft_flag(self):
        p,plan=self.t.make(draft=False);prepare_output(self.t.root,p);before=p.read_bytes()
        self.t.failcode('BUILD_FAILED',build_output,self.t.root,plan['output_id'])
        self.assertEqual(p.read_bytes(),before)
    def test_draft_does_not_exempt_invalid_node_or_canonical(self):
        p,plan=self.t.authored();(p.parent/'outline.md').write_text('[[N-no-such-node]]')
        self.t.failcode('BUILD_FAILED',build_output,self.t.root,plan['output_id'])
        (p.parent/'generated/statements/N-main.tex').write_text('Changed claim')
        self.t.failcode('CANONICAL_STATEMENT_CHANGED',build_output,self.t.root,plan['output_id'])
    def test_outline_change_stales_review_and_refresh_does_not_bypass(self):
        p,plan=self.t.authored(draft=False);r=self.t.sem(p,plan)
        (p.parent/'outline.md').write_text('[[PMS_PENDING:connections]]')
        self.assertTrue(check_review_bindings(p.parent,r,output_inputs(p.parent)))
        r=self.t.sem(p,plan);write_json(p.parent/'evidence/synthetic.json',r)
        self.assertIn('EXPOSITION_DESIGN_INCOMPLETE',{e['code'] for e in assess_release(self.t.root,plan['output_id'])['errors']})
    def test_single_inspection_shared_by_all_review_locations(self):
        p,plan=self.t.authored();r=self.t.sem(p,plan)
        from survey_core.tex import inspect_tex
        from survey_core.release import semantic_scope_errors
        with patch('survey_core.tex.inspect_tex',wraps=inspect_tex) as scan:
            self.assertEqual(semantic_scope_errors(p.parent,plan,['N-main','N-def','N-q'],r),[])
            self.assertEqual(scan.call_count,1)

class Compatibility(unittest.TestCase):
    setUp=Design.setUp
    tearDown=Design.tearDown
    def test_rc1_and_v2_read_without_mutating_and_cannot_release_as_rc2(self):
        p,plan=self.t.authored(draft=False)
        plan.update(schema_version=RC1_SCHEMA,editorial_policy=RC1_POLICY);write_json(p,plan)
        prepare_output(self.t.root,p);before={x:x.read_bytes() for x in p.parent.rglob('*') if x.is_file()}
        report=assess_release(self.t.root,plan['output_id'])
        self.assertIn('EDITORIAL_POLICY_REASSESSMENT_REQUIRED',{e['code'] for e in report['errors']})
        self.assertEqual(report['artifacts']['recorded_policy'],RC1_POLICY)
        self.assertEqual(report['artifacts']['evaluated_policy'],POLICY)
        historical=assess_release(self.t.root,plan['output_id'],policy_mode='recorded')
        self.assertFalse(historical['artifacts']['release_authorized'])
        self.assertEqual(before,{x:x.read_bytes() for x in before})
        old=legacy_plan(self.t.root,oid='v2');data=old.read_bytes();load_plan(old);self.assertEqual(old.read_bytes(),data)
    def test_mixed_schema_and_policy_rejected(self):
        p,plan=self.t.make(oid='schema')
        for schema,pol in [(RC1_SCHEMA,POLICY),('9.0.0',POLICY),('2.2.0',RC1_POLICY)]:
            bad=copy.deepcopy(plan);bad.update(schema_version=schema,editorial_policy=pol)
            with self.assertRaises(SurveyError):validate_plan_contract(bad)
        _,paper=self.t.paper();paper.update(schema_version=RC1_SCHEMA,editorial_policy=RC1_POLICY)
        with self.assertRaises(SurveyError):validate_plan_contract(paper)
    def test_old_review_cannot_carry_new_responsibilities(self):
        p,plan=self.t.authored();r=self.t.sem(p,plan)
        r.update(schema_version=RC1_SCHEMA);r['scope']['editorial_policy']=RC1_POLICY
        path=p.parent/'evidence/mixed.json';write_json(path,r)
        self.t.failcode('SCHEMA_UNSUPPORTED',load_review,path)

