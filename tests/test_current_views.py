"""Software contracts, not 20 mathematical manuscripts or reader studies."""
import copy
import unittest
from pathlib import Path
import test_vnext as v
from test_v2 import read_json, write_json
from survey_core.exports import prepare_output, validate_structure, output_inputs
from survey_core.profiles import VIEW_TASKS, MODE_READINGS, review_scope_template, semantic_profile_errors
from survey_core.reviews import check_review_bindings
from survey_core.plans import consumption, validate_plan


class Views(unittest.TestCase):
    def setUp(self):
        self.t=v.VNext();self.t.setUp();self.t.editorial_policy=v.POLICY
    def tearDown(self):self.t.tearDown()
    def test_all_twenty_interfaces_preserve_core_and_mode_obligations(self):
        for profile in ('minimal','thematic','lecture','paper'):
            baseline=None
            for view in VIEW_TASKS:
                with self.subTest(profile=profile,view=view):
                    oid=profile+'-'+view;p,plan=self.t.make(profile,oid,view=view)
                    prepare_output(self.t.root,p)
                    selected={(s['node_id'],s['role'],s['statement_treatment'],s['proof_treatment']) for s in plan['selections']}
                    if baseline is None:baseline=selected
                    self.assertEqual(selected,baseline)
                    self.assertIn(VIEW_TASKS[view],plan['reader_goals'][1])
                    self.assertTrue(all(s['node_id'] in s['reason'] and VIEW_TASKS[view] in s['reason'] for s in plan['selections']))
                    self.assertIn(VIEW_TASKS[view],(p.parent/'outline.md').read_text())
                    self.assertIn(VIEW_TASKS[view],(p.parent/'manuscript/main.tex').read_text())
                    scope=review_scope_template(plan)
                    self.assertEqual(scope['view'],view)
                    self.assertTrue(set(MODE_READINGS[profile]) <= scope['mode_findings'].keys())
                    self.assertIn('view_focus',scope['mode_findings'])
                    self.assertEqual(set(scope['proof_step_findings']),{o['node_id'] for o in plan['proof_obligations']})
        self.assertEqual(len(list((self.t.root/'outputs').iterdir())),20)
    def test_one_request_creates_only_that_output(self):
        p,plan=self.t.make(oid='only',view='boundaries');prepare_output(self.t.root,p)
        self.assertEqual([x.name for x in (self.t.root/'outputs').iterdir()],['only'])
    def test_missing_candidate_is_a_gap_not_invented_node(self):
        p,plan=self.t.make(view='methods');prepare_output(self.t.root,p)
        self.assertIn('no dedicated methods candidate',(p.parent/'outline.md').read_text())
        self.assertEqual({s['node_id'] for s in plan['selections']},{'N-main','N-def'})
    def test_minimal_views_keep_exact_canonical_and_sections(self):
        canonical=[]
        for view in ('methods','boundaries'):
            p,plan=self.t.authored(oid=view,view=view)
            plan['comparison_group']='same-spine';write_json(p,plan);prepare_output(self.t.root,p)
            self.assertEqual(validate_structure(self.t.root,view)['errors'],[])
            canonical.append((p.parent/'generated/statements/N-main.tex').read_bytes())
        self.assertEqual(*canonical)
    def test_view_change_stales_review_and_fresh_hash_is_insufficient(self):
        p,plan=self.t.authored(view='methods');review=self.t.sem(p,plan)
        plan['view']='boundaries';write_json(p,plan)
        self.assertTrue(check_review_bindings(p.parent,review,output_inputs(p.parent)))
        prepare_output(self.t.root,p)
        review['inputs']=self.t.sem(p,plan)['inputs']
        self.assertIn('VIEW_REVIEW_MISMATCH',{e['code'] for e in semantic_profile_errors(p.parent,plan,review)})
    def test_view_focus_requires_located_finding_and_available_nodes(self):
        p,plan=self.t.authored();review=self.t.sem(p,plan)
        for change,code in [({'node_ids':['N-absent']},'VIEW_FOCUS_NODE_INVALID'),
                            ({'node_ids':[]},'VIEW_FOCUS_NODE_INVALID'),
                            ({'locations':[]},'REVIEW_LOCATION_INVALID'),
                            ({'outcome':'not_performed'},'MODE_SEMANTIC_REVIEW_PENDING')]:
            with self.subTest(change=change):
                bad=copy.deepcopy(review);bad['scope']['mode_findings']['view_focus'].update(change)
                self.assertIn(code,{e['code'] for e in semantic_profile_errors(p.parent,plan,bad)})
    def test_view_emphasis_reorders_candidates_without_changing_closure(self):
        from test_v2 import putnode
        from test_vnext import synthetic_policy_reviews
        putnode(self.t.root,'N-operation','mechanism',None,links=[('N-def','proof_input')],status='established')
        coverage=read_json(self.t.root/'knowledge/coverage.json')
        coverage['questions'][0]['mechanism_nodes']=['N-operation'];write_json(self.t.root/'knowledge/coverage.json',coverage)
        synthetic_policy_reviews(self.t.root)
        plans=[self.t.make(oid=view,view=view)[1] for view in ('foundations','methods')]
        self.assertEqual(*[{s['node_id'] for s in p['selections']} for p in plans])
        self.assertNotEqual(*[[s['node_id'] for s in p['selections']] for p in plans])
        self.assertEqual(*[consumption(validate_plan(self.t.root,p),p) for p in plans])
