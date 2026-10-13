"""Synthetic endpoint/support adversaries; no originality acceptance."""
import copy
import unittest
import test_vnext as v
from test_v2 import putnode, write_json, read_json, now, SurveyError
from survey_core.knowledge import inventory
from survey_core.models import load_node, node_bytes
from survey_core.exports import prepare_output
from survey_core.profiles import profile_readiness_errors, semantic_profile_errors, normalize_locator
from survey_core.reviews import mathematical_inputs, review_template, check_review_bindings, load_review
from survey_core.release import assess_release

class Prior(unittest.TestCase):
    def setUp(self):
        self.t=v.VNext();self.t.setUp();self.t.editorial_policy=v.POLICY;self.p,self.plan=self.t.paper()
    def tearDown(self):self.t.tearDown()
    def ready_codes(self,inv=None,plan=None):
        return {e['code'] for e in profile_readiness_errors(inv or inventory(self.t.root),plan or self.plan)}
    def semantic(self):
        prepare_output(self.t.root,self.p);r=self.t.sem(self.p,self.plan)
        e=r['scope']['contribution_reviews']['N-main']
        e.update(outcome='accepted',finding=v.SYNTH,locations=r['scope']['principal_locations']['N-main'],
                 provenance_check=v.SYNTH,authorization_check=v.SYNTH,actual_difference=v.SYNTH,proof_closure=v.SYNTH,remaining_caveats=v.SYNTH,
                 prior_art_searches=[dict(searched_at=now(),query='SYNTHETIC search',outcome='No additional directly comparable results in this synthetic query.',checked_source_ids=[])],
                 prior_result_checks=[dict(prior_result_id='N-prior',source_id='S-test',version='Fixture v1',locator='Synthetic fixture paragraph 1',outcome='accepted',finding=v.SYNTH)])
        return r,e
    def sem_codes(self,r):return {e['code'] for e in semantic_profile_errors(self.p.parent,self.plan,r)}
    def test_both_endpoints_and_typed_relation_required(self):
        inv=inventory(self.t.root)
        for links in ([],[('N-main','compares_with')],[('N-prior','compares_with')],
                      [('N-main','proof_input'),('N-prior','proof_input')],[('N-main','compares_with'),('N-def','compares_with')]):
            with self.subTest(links=links):
                inv.nodes['N-compare'].meta['links']=[dict(target=k,relation=r) for k,r in links]
                self.assertIn('PAPER_COMPARISON_ENDPOINT_MISSING',self.ready_codes(inv))
    def test_multiple_prior_endpoints_need_explicit_pair_coverage(self):
        putnode(self.t.root,'N-prior2','result',r'For real $x$, $x+0=x$.',source=True,status='established')
        inv=inventory(self.t.root);inv.nodes['N-compare'].meta['links'].append(dict(target='N-prior2',relation='compares_with'))
        plan=copy.deepcopy(self.plan);c=plan['contributions'][0];c['closest_prior_results'].append('N-prior2')
        self.assertIn('PAPER_COMPARISON_COVERAGE_MISSING',self.ready_codes(inv,plan))
        c['comparison_bindings'].append(dict(comparison_node_id='N-compare',prior_result_id='N-prior2'))
        self.assertNotIn('PAPER_COMPARISON_COVERAGE_MISSING',self.ready_codes(inv,plan))
    def test_binding_wrong_prior_does_not_count(self):
        self.plan['contributions'][0]['comparison_bindings'][0]['prior_result_id']='N-def'
        self.assertIn('PAPER_COMPARISON_PRIOR_INVALID',self.ready_codes())
    def test_negative_search_is_legal_with_actual_support_coverage(self):
        r,e=self.semantic();self.assertEqual(self.sem_codes(r),set())
    def test_unknown_unrelated_version_and_locator_rejected(self):
        r,e=self.semantic();self.assertEqual(self.sem_codes(r),set())
        for key,value in [('source_id','S-missing'),('source_id','S-unrelated'),('version','Fixture v2'),('locator',''),('locator','Synthetic fixture paragraph 2')]:
            with self.subTest(key=key,value=value):
                q=copy.deepcopy(r);q['scope']['contribution_reviews']['N-main']['prior_result_checks'][0][key]=value
                self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',self.sem_codes(q))
    def test_provenance_and_unread_source_do_not_support_prior(self):
        r,e=self.semantic();path=self.p.parent/'materials/knowledge/nodes/N-prior.md';node=load_node(path)
        node.meta['sources'][0]['role']='provenance';path.write_bytes(node_bytes(node.meta,node.body))
        self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',self.sem_codes(r))
        node.meta['sources'][0]['role']='support';path.write_bytes(node_bytes(node.meta,node.body))
        path=self.p.parent/'materials/knowledge/sources/S-test.json';source=read_json(path);source['access']['state']='metadata_only';write_json(path,source)
        self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',self.sem_codes(r))
    def test_reading_locator_missing_or_wrong_is_not_accepted(self):
        r,e=self.semantic();path=self.p.parent/'materials/evidence/reviews/source-S-test.json';source=read_json(path)
        for locators in ([],['Wrong section']):
            source['scope']['source_reading']['S-test']['locators']=locators;write_json(path,source)
            self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',self.sem_codes(r))
    def test_online_original_text_without_pdf_bytes_is_allowed(self):
        r,e=self.semantic();materials=self.p.parent/'materials';sp=materials/'knowledge/sources/S-test.json';source=read_json(sp)
        source['identifiers']['url']='https://example.invalid/synthetic-online-original'
        source['access'].update(local_path=None,material_sha256=None,material_hash_unavailable_reason='Synthetic online-only fixture; no PDF byte assertion.')
        write_json(sp,source)
        rp=materials/'evidence/reviews/source-S-test.json';review=read_json(rp)
        from survey_core.common import file_hash
        review['inputs']=[b for b in review['inputs'] if b['path']!='knowledge/material.txt']
        for b in review['inputs']:b['sha256']=file_hash(materials,b['path'])
        review['scope']['source_reading']['S-test'].update(mode='original_text_online',raw_bytes_unavailable_reason='Synthetic browser reading only.')
        write_json(rp,review)
        self.assertEqual(self.sem_codes(r),set())
        review['scope']['source_reading']['S-test'].pop('raw_bytes_unavailable_reason');write_json(rp,review)
        self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',self.sem_codes(r))
    def test_locator_aliases_are_narrow_not_fuzzy(self):
        self.assertEqual(normalize_locator('pp. 12–13'),normalize_locator('pages 12-13'))
        self.assertEqual(normalize_locator('Thm. 2.'),normalize_locator('Theorem 2'))
        self.assertNotEqual(normalize_locator('Theorem 2'),normalize_locator('Theorem 3'))
    def test_each_endpoint_change_stales_relation_but_unrelated_change_does_not(self):
        inv=inventory(self.t.root);r=review_template(self.t.root,'mathematical',['N-compare'],mathematical_inputs(inv,'N-compare'))
        putnode(self.t.root,'N-unrelated','result','For real x, x=x.',status='established')
        self.assertEqual(check_review_bindings(self.t.root,r,mathematical_inputs(inventory(self.t.root),'N-compare')),[])
        for key in ('N-main','N-prior'):
            path=self.t.root/f'knowledge/nodes/{key}.md';before=path.read_bytes();path.write_bytes(before+b'\nChanged endpoint condition.\n')
            self.assertIn('REVIEW_STALE',{e['code'] for e in check_review_bindings(self.t.root,r,mathematical_inputs(inventory(self.t.root),'N-compare'))})
            path.write_bytes(before)
    def test_navigation_cycle_is_not_proof_cycle(self):
        path=self.t.root/'knowledge/nodes/N-main.md';n=load_node(path);n.meta['links'].append(dict(target='N-compare',relation='compares_with'));path.write_bytes(node_bytes(n.meta,n.body))
        inv=inventory(self.t.root);self.assertIn(inv.nodes['N-main'].path,mathematical_inputs(inv,'N-compare'))
    def test_no_direct_prior_stays_unverified_without_waiver(self):
        c=self.plan['contributions'][0];c.update(closest_prior_results=[],comparison_bindings=[],waiver=True)
        self.assertIn('PAPER_PRIOR_ART_MISSING',self.ready_codes())
    def test_matching_hash_and_accepted_claim_do_not_hide_bad_support(self):
        r,e=self.semantic();e['prior_result_checks'][0]['version']='WRONG'
        write_json(self.p.parent/'evidence/synthetic-accepted.json',r)
        self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',{e['code'] for e in assess_release(self.t.root,self.plan['output_id'])['errors']})
    def test_typed_new_review_rejects_malformed_checks(self):
        r,e=self.semantic();e['prior_result_checks']=[dict(prior_result_id=3)]
        path=self.p.parent/'evidence/malformed.json';write_json(path,r)
        with self.assertRaises(SurveyError):load_review(path)

if __name__=='__main__':unittest.main()
