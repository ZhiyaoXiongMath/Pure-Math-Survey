"""Online source metadata is not a retained-byte certificate (synthetic only)."""
import unittest
import test_vnext as v
from test_v2 import read_json,write_json,synthetic_reviews
from survey_core.readiness import assess_readiness


class OnlineSources(unittest.TestCase):
    def setUp(self):
        self.t=v.VNext();self.t.setUp();self.t.editorial_policy=v.RC2_POLICY
    def tearDown(self):self.t.tearDown()
    def source(self,retain_hash=True,locators=None,malformed_scope=False):
        p=self.t.root/'knowledge/sources/S-test.json';source=read_json(p)
        source['identifiers']['url']='https://example.invalid/synthetic-source'
        source['access'].update(local_path=None,material_hash_unavailable_reason='Synthetic fixture: original bytes not retained in this project.')
        if not retain_hash:source['access']['material_sha256']=None
        write_json(p,source)
        synthetic_reviews(self.t.root);v.synthetic_policy_reviews(self.t.root)
        rp=self.t.root/'evidence/reviews/source-S-test.json';review=read_json(rp)
        review['scope']['source_reading']=None if malformed_scope else {'S-test':dict(mode='original_text_online',version='Fixture v1',
            locators=['Synthetic fixture paragraph 1'] if locators is None else locators,
            raw_bytes_unavailable_reason='Synthetic test of a source-retention limitation, not a real source reading.')}
        write_json(rp,review)
    def test_known_hash_distinguished_from_missing_hash_without_certifying_bytes(self):
        for known in (True,False):
            self.source(known);p,plan=self.t.make(oid='known' if known else 'unknown')
            r=assess_readiness(self.t.root,plan);self.assertEqual(r['status'],'READY')
            self.assertIn('SOURCE_RAW_BYTES_NOT_RETAINED' if known else 'SOURCE_RAW_HASH_UNAVAILABLE',{e['code'] for e in r['warnings']})
    def test_online_locator_shapes_and_malformed_scope_block_without_crash(self):
        for i,locators in enumerate(('Section 1',{'page':1},[''],[1])):
            self.source(locators=locators);p,plan=self.t.make(oid='bad'+str(i))
            self.assertIn('SOURCE_REVIEW_MISSING',{e['code'] for e in assess_readiness(self.t.root,plan)['errors']})
        self.source(malformed_scope=True);p,plan=self.t.make(oid='null-scope')
        self.assertIn('SOURCE_REVIEW_MISSING',{e['code'] for e in assess_readiness(self.t.root,plan)['errors']})
