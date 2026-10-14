"""Neutral SYNTHETIC engineering fixtures; no literature reading or license audit."""
import copy
import json
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch
import test_vnext as v
from test_v2 import read_json, write_json, synthetic_reviews, now, SurveyError, SCRIPTS
from survey_core.common import file_hash, relpath, safe, all_files
from survey_core.knowledge import inventory, validate_knowledge
from survey_core.readiness import assess_readiness, assess_eligibility
from survey_core.sources import source_facts
from survey_core.snapshots import freeze_snapshot, load_snapshot
from survey_core.reviews import (source_inputs, review_template, validate_reviews,
                                 accept_review_candidate, plan_mathematical_template,
                                 plan_promise_scope_errors)
from survey_core.exports import prepare_output, verify_generated, validate_structure
from survey_core.release import assess_release

SYNTH = 'Synthetic supporting sections only; no actual mathematical reading or license audit.'
SOURCE = 'knowledge/sources/S-test.json'
REVIEW = 'evidence/reviews/source-S-test.json'


class SourceEligibility(unittest.TestCase):
    def setUp(self):
        self.t=v.VNext(); self.t.setUp(); self.root=self.t.root
    def tearDown(self): self.t.tearDown()
    def reset_reviews(self):
        synthetic_reviews(self.root); v.synthetic_policy_reviews(self.root)
    def online(self, permission='unknown', private=False):
        source=read_json(self.root/SOURCE)
        source['identifiers']['url']='https://example.invalid/synthetic-v1'
        source['access'].update(local_path=None, material_visibility='private' if private else 'public',
            material_hash_unavailable_reason='SYNTHETIC original not retained in this public project.',
            redistribution=dict(status=permission, checked_at=now() if permission=='denied' else None,
                                basis='Synthetic explicit refusal.' if permission=='denied' else 'Synthetic permission not checked.'))
        write_json(self.root/SOURCE,source)
        (self.root/'knowledge/material.txt').unlink(missing_ok=True)
        self.reset_reviews()
        record=read_json(self.root/REVIEW)
        record['scope']['source_reading']['S-test'].update(
            mode='original_text_private' if private else 'original_text_online',
            raw_bytes_unavailable_reason='SYNTHETIC external/private bytes omitted; no private path disclosed.')
        write_json(self.root/REVIEW,record)
        return source
    def codes(self, report): return {e['code'] for e in report['errors']}
    def candidate(self):
        p,plan=self.t.make(draft=False)
        plan['audience']='Synthetic reader can multiply real numbers.'
        plan['reader_goals']=['Reconstruct the synthetic multiplication only.']
        write_json(p,plan)
        candidate=self.root/'.cache/source-candidate'; record=read_json(self.root/REVIEW)
        record['review_id']='SYNTHETIC-FRESH-SOURCE'
        write_json(candidate/'evidence/reviews/fresh-source.json',record)
        return p,plan,candidate,record
    def accept(self,p):
        return accept_review_candidate(self.root,'.cache/source-candidate',relpath(self.root,p))
    def bytes(self):
        return {p:safe(self.root,p,True).read_bytes() for p in inventory(self.root).files}

    def cli(self, *args, exit_code=0):
        run=subprocess.run([sys.executable,'-I',str(SCRIPTS/'survey.py'),*map(str,args),'--json'],
                           capture_output=True,text=True)
        self.assertEqual(run.returncode,exit_code,run.stdout+run.stderr)
        self.assertEqual(run.stderr,'')
        return json.loads(run.stdout)

    def test_cli_retained_bytes_without_hash_are_unverified_and_keep_gates(self):
        p,plan=self.t.paper()
        source=read_json(self.root/SOURCE);source['access']['material_sha256']=None
        write_json(self.root/SOURCE,source);self.reset_reviews()
        report=self.cli('kb','validate',self.root)
        self.assertEqual(report['status'],'VALID')
        facts=report['artifacts']['source_facts'][0]
        self.assertEqual(facts['bytes'],'UNVERIFIED')
        self.assertIsNone(facts['recorded_sha256'])
        self.assertEqual(facts['reading'],'UNVERIFIED')
        review=self.cli('review','validate',self.root,'--record',REVIEW,exit_code=3)
        self.assertIn('SOURCE_MATERIAL_MISMATCH',self.codes(review))
        plan['snapshot_id']=freeze_snapshot(self.root)['artifacts']['snapshot_id'];write_json(p,plan)
        ready=self.cli('kb','readiness',self.root,'--plan',p,exit_code=3)
        self.assertEqual(ready['status'],'NEEDS_WORK')
        self.assertIn('SOURCE_MATERIAL_MISMATCH',self.codes(ready))
        self.assertEqual(ready['artifacts']['source_facts'][0]['bytes'],'UNVERIFIED')
        # Research qualification stays independent; it cannot bypass readiness.
        eligibility=self.cli('output','validate',self.root,'--output',plan['output_id'],'--stage','eligibility')
        self.assertEqual(eligibility['status'],'ELIGIBLE')
        draft=self.cli('output','prepare',self.root,'--plan',p)
        self.assertEqual(draft['status'],'DRAFT_PREPARED')
        self.assertIn('Paper Draft',(p.parent/'manuscript/main.tex').read_text())
        release=self.cli('output','validate',self.root,'--output',plan['output_id'],'--stage','release',exit_code=3)
        self.assertIn('DRAFT_NOT_RELEASABLE',self.codes(release))
        plan['draft']=False;write_json(p,plan)
        formal=self.cli('output','prepare',self.root,'--plan',p,exit_code=3)
        self.assertIn('READINESS_REQUIRED',self.codes(formal))
        plan['contributions'][0]['authorization']='';write_json(p,plan)
        eligibility=self.cli('output','validate',self.root,'--output',plan['output_id'],'--stage','eligibility')
        self.assertEqual(eligibility['status'],'UNVERIFIED')
        self.assertIn('PAPER_PROVENANCE_UNVERIFIED',self.codes(eligibility))
        formal=self.cli('output','prepare',self.root,'--plan',p,exit_code=2)
        self.assertIn('RESEARCH_ELIGIBILITY_REQUIRED',self.codes(formal))

    def test_cli_retained_bytes_matching_hash_are_verified(self):
        report=self.cli('kb','validate',self.root)
        self.assertEqual(report['status'],'VALID')
        facts=report['artifacts']['source_facts'][0]
        self.assertEqual(facts['bytes'],'VERIFIED')
        self.assertEqual(facts['recorded_sha256'],file_hash(self.root,'knowledge/material.txt'))

    def test_cli_retained_bytes_mismatching_hash_are_rejected(self):
        source=read_json(self.root/SOURCE);source['access']['material_sha256']='0'*64
        write_json(self.root/SOURCE,source)
        report=self.cli('kb','validate',self.root)
        self.assertEqual(report['status'],'VALID')
        facts=report['artifacts']['source_facts'][0]
        self.assertEqual(facts['bytes'],'REJECTED')
        self.assertEqual(facts['recorded_sha256'],'0'*64)
        self.assertNotEqual(facts['recorded_sha256'],file_hash(self.root,'knowledge/material.txt'))

    def test_positive_binding_permission_note_and_pending_template(self):
        path=self.root/'evidence/source-checks/permission.md';path.write_text(SYNTH)
        source=read_json(self.root/SOURCE);source['access']['permission_note']=relpath(self.root,path)
        write_json(self.root/SOURCE,source);self.reset_reviews()
        inv=inventory(self.root); required=source_inputs(inv,'S-test')
        self.assertIn(relpath(self.root,path),required)
        template=review_template(self.root,'source',['S-test'],required)
        scope=template['scope']['source_reading']['S-test']
        self.assertEqual(scope['mode'],'not_performed');self.assertEqual(scope['locators'],[])
        self.assertEqual(scope['reading_scope'],'');self.assertTrue(scope['unchecked_items'])
        self.assertEqual(template['disposition'],'revise')
        p,plan=self.t.make(draft=False);ready=assess_readiness(self.root,plan)
        self.assertEqual(ready['status'],'READY',ready['errors'])
        facts=ready['artifacts']['source_facts'][0]
        self.assertEqual([facts[k] for k in ('access','reading','bytes','redistribution')],['VERIFIED']*4)
        prepare_output(self.root,p);self.assertTrue((p.parent/'materials'/path.relative_to(self.root)).is_file())
        self.assertFalse((p.parent/'materials/knowledge/material.txt').exists())

    def test_unretained_reading_and_denied_unknown_rights_are_independent(self):
        for permission in ('unknown','denied'):
            self.online(permission,private=True)
            p,plan=self.t.make(oid=permission,draft=False)
            ready=assess_readiness(self.root,plan);self.assertEqual(ready['status'],'READY',ready['errors'])
            facts=ready['artifacts']['source_facts'][0]
            self.assertEqual(facts['reading'],'VERIFIED');self.assertEqual(facts['bytes'],'UNVERIFIED')
            self.assertEqual(facts['redistribution'],'UNVERIFIED' if permission=='unknown' else 'REJECTED')
            self.assertEqual(facts['redistribution_declared'],permission)
            result=prepare_output(self.root,p);self.assertEqual(result['status'],'PREPARED')
            _,frozen=load_snapshot(self.root,plan['snapshot_id'])
            self.assertFalse((frozen/'knowledge/material.txt').exists())
            self.assertNotIn('knowledge/material.txt',{r['path'] for r in verify_generated(self.root,plan)['consumed_inputs']})

    def test_legacy_records_are_unverified_without_migration(self):
        source=read_json(self.root/SOURCE)
        for key in ('availability','redistribution','material_visibility'):source['access'].pop(key)
        write_json(self.root/SOURCE,source);before=(self.root/SOURCE).read_bytes()
        result=validate_knowledge(self.root);self.assertEqual(result['status'],'VALID')
        facts=result['artifacts']['source_facts'][0]
        self.assertEqual(facts['access'],'UNVERIFIED');self.assertEqual(facts['redistribution'],'UNVERIFIED')
        self.assertEqual((self.root/SOURCE).read_bytes(),before)
        self.t.failcode('SOURCE_PRIVATE_ORIGINAL',freeze_snapshot,self.root)
        self.assertFalse((self.root/'snapshots').exists())

    def test_private_denied_unknown_retained_original_refused_before_snapshot(self):
        original=read_json(self.root/SOURCE)
        for visibility,permission,code in (('private','granted','SOURCE_PRIVATE_ORIGINAL'),
                ('public','denied','SOURCE_REDISTRIBUTION_REJECTED'),('public','unknown','SOURCE_REDISTRIBUTION_UNVERIFIED')):
            source=copy.deepcopy(original);source['access']['material_visibility']=visibility
            source['access']['redistribution']['status']=permission;write_json(self.root/SOURCE,source)
            self.t.failcode(code,freeze_snapshot,self.root)
            self.assertFalse((self.root/'snapshots').exists())

    def test_unretained_original_alias_cannot_hide_in_reading_note_or_review_input(self):
        original=(self.root/'knowledge/material.txt').read_bytes();self.online('unknown')
        for alias in ('evidence/source-checks/alias.md','support/source-alias.dat'):
            path=self.root/alias;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(original)
            record=read_json(self.root/REVIEW);record['inputs'].append(dict(path=alias,sha256=file_hash(self.root,alias)))
            write_json(self.root/REVIEW,record)
            self.t.failcode('SOURCE_ORIGINAL_ALIAS_UNSAFE',freeze_snapshot,self.root)
            self.assertFalse((self.root/'snapshots').exists());path.unlink()
            record['inputs'].pop();write_json(self.root/REVIEW,record)

    def test_public_original_alias_omitted_from_materials(self):
        alias='support/public-original-alias.dat';path=self.root/alias;path.parent.mkdir()
        path.write_bytes((self.root/'knowledge/material.txt').read_bytes())
        record=read_json(self.root/REVIEW);record['inputs'].append(dict(path=alias,sha256=file_hash(self.root,alias)))
        write_json(self.root/REVIEW,record)
        p,plan=self.t.make(draft=False);prepare_output(self.root,p)
        self.assertFalse((p.parent/'materials'/alias).exists())
        self.assertIn(alias,verify_generated(self.root,plan)['raw_sources_omitted'])

    def test_local_version_locator_scope_unchecked_work_aggregate(self):
        record=read_json(self.root/REVIEW);reading=record['scope']['source_reading']['S-test']
        for defect,value,code in (('version','wrong version','SOURCE_REVIEW_MISSING'),
            ('locators',['Unconsumed section'],'SOURCE_LOCATOR_UNCHECKED'),
            ('reading_scope','','SOURCE_REVIEW_MISSING'),('unchecked_items',['Actual omitted supporting paragraph.'],'SOURCE_REVIEW_MISSING')):
            candidate=copy.deepcopy(record);candidate['scope']['source_reading']['S-test'][defect]=value
            write_json(self.root/'.cache/bad-source.json',candidate)
            report=validate_reviews(self.root,['.cache/bad-source.json'])
            self.assertIn(code,self.codes(report))
        candidate=copy.deepcopy(record);candidate['scope']['source_reading']['S-test'].update(version='wrong',reading_scope='',unchecked_items=['Unread support.'])
        write_json(self.root/'.cache/bad-source.json',candidate)
        self.assertGreaterEqual(len(validate_reviews(self.root,['.cache/bad-source.json'])['errors']),2)

    def test_metadata_access_inadequate_is_not_actual_reading(self):
        for status,code in (('unknown','SOURCE_ACCESS_UNVERIFIED'),('unavailable','SOURCE_ACCESS_REJECTED')):
            source=read_json(self.root/SOURCE);source['access']['availability']['status']=status
            write_json(self.root/SOURCE,source);self.reset_reviews()
            p,plan=self.t.make(oid=status,draft=True);self.assertIn(code,self.codes(assess_readiness(self.root,plan)))
        source=read_json(self.root/SOURCE);source['access']['availability']['status']='accessible';source['access']['state']='metadata_only'
        write_json(self.root/SOURCE,source);self.reset_reviews()
        p,plan=self.t.make(oid='metadata');self.assertIn('SOURCE_REVIEW_MISSING',self.codes(assess_readiness(self.root,plan)))

    def test_metadata_bytes_note_permission_changes_stale_not_reaccepted(self):
        paths=[SOURCE,'knowledge/material.txt','evidence/source-checks/test.md','evidence/source-checks/permission.md']
        (self.root/paths[-1]).write_text(SYNTH)
        source=read_json(self.root/SOURCE);source['access']['permission_note']=paths[-1];write_json(self.root/SOURCE,source)
        self.reset_reviews();accepted=(self.root/REVIEW).read_bytes()
        for path in paths:
            before=(self.root/path).read_bytes();(self.root/path).write_bytes(before+b'\n')
            report=validate_reviews(self.root,[REVIEW]);self.assertIn('REVIEW_STALE',self.codes(report))
            self.assertEqual((self.root/REVIEW).read_bytes(),accepted);(self.root/path).write_bytes(before)
        source=read_json(self.root/SOURCE);source['access']['redistribution']['status']='unknown';write_json(self.root/SOURCE,source)
        self.assertIn('REVIEW_STALE',self.codes(validate_reviews(self.root,[REVIEW])))

    def test_source_candidate_accept_freeze_adopt_preserves_history(self):
        p,plan,candidate,record=self.candidate();before=self.bytes();old=plan['snapshot_id']
        report=self.accept(p);self.assertEqual(report['status'],'ACCEPTED',report['errors'])
        self.assertEqual(load_snapshot(self.root,old)[0]['snapshot_id'],old)
        for path,data in before.items():self.assertEqual(safe(self.root,path,True).read_bytes(),data)
        self.assertEqual(read_json(p)['snapshot_id'],old)
        plan['snapshot_id']=freeze_snapshot(self.root)['artifacts']['snapshot_id'];write_json(p,plan)
        self.assertNotEqual(plan['snapshot_id'],old);self.assertEqual(assess_readiness(self.root,plan)['status'],'READY')
        prepare_output(self.root,p);verify_generated(self.root,plan)

    def test_source_candidate_rejection_and_install_failure_leave_no_live_changes(self):
        p,plan,candidate,record=self.candidate();before=self.bytes()
        record['scope']['source_reading']['S-test']['locators']=['Unconsumed locator']
        write_json(candidate/'evidence/reviews/fresh-source.json',record)
        report=self.accept(p);self.assertIn('SOURCE_LOCATOR_UNCHECKED',self.codes(report));self.assertEqual(self.bytes(),before)
        record['scope']['source_reading']['S-test']['locators']=['Synthetic fixture paragraph 1']
        write_json(candidate/'evidence/reviews/fresh-source.json',record)
        from survey_core.common import atomic_bytes as actual
        def fail(path,data):
            if path==self.root/'evidence/reviews/fresh-source.json':raise OSError('Synthetic installation failure.')
            return actual(path,data)
        with patch('survey_core.common.atomic_bytes',fail):
            with self.assertRaises(OSError):self.accept(p)
        self.assertEqual(self.bytes(),before);self.assertFalse(list((self.root/'.cache').glob('.review-*')))
        self.assertFalse((self.root/'.survey-write.lock').exists())

    def test_knowledge_ready_paper_preview_and_research_qualification_independent(self):
        p,plan=self.t.make('paper');plan['contributions'][0]['classification']='known';write_json(p,plan)
        self.assertEqual(assess_readiness(self.root,plan)['status'],'READY')
        self.assertEqual(assess_eligibility(self.root,plan)['status'],'REJECTED')
        result=prepare_output(self.root,p);self.assertEqual(result['status'],'DRAFT_PREPARED')
        self.assertIn('Paper Draft',(p.parent/'manuscript/main.tex').read_text())
        self.assertTrue(result['artifacts']['preview_allowed'])
        self.assertIn('DRAFT_NOT_RELEASABLE',self.codes(assess_release(self.root,plan['output_id'])))
        plan['draft']=False;write_json(p,plan)
        self.t.failcode('RESEARCH_ELIGIBILITY_REQUIRED',prepare_output,self.root,p)
        # Rebinding the manifest cannot remove the independent structure gate.
        plan['draft']=True;write_json(p,plan);prepare_output(self.root,p)
        text=(p.parent/'manuscript/main.tex').read_text().replace(r'DRAFT\_UNVERIFIED','Unmarked')
        (p.parent/'manuscript/main.tex').write_text(text)
        self.assertIn('DRAFT_NOTICE_MISSING',self.codes(validate_structure(self.root,plan['output_id'])))

    def test_real_authorization_and_proof_thresholds_remain_separate(self):
        p,plan=self.t.paper();self.assertEqual(assess_eligibility(self.root,plan)['status'],'ELIGIBLE')
        self.assertEqual(assess_readiness(self.root,plan)['status'],'READY')
        c=plan['contributions'][0];c['authorization']=''
        result=assess_eligibility(self.root,plan);self.assertEqual(result['status'],'UNVERIFIED')
        self.assertIn('PAPER_PROVENANCE_UNVERIFIED',self.codes(result));self.assertEqual(assess_readiness(self.root,plan)['status'],'READY')
        c['authorization']=v.SYNTH;c['proof_status']='incomplete'
        self.assertIn('PAPER_PROOF_NOT_CLOSED',self.codes(assess_eligibility(self.root,plan)))

    def test_changed_contribution_invalidates_exact_plan_review_request(self):
        p,plan=self.t.paper();plan['audience']='Synthetic reader can multiply.';plan['reader_goals']=['Reconstruct synthetic computation.']
        write_json(p,plan);record,request=plan_mathematical_template(self.root,p,['N-main'])
        record.update(reviewer_mode='independent_review',reviewer='Synthetic nonauthor, no actual reading.')
        self.assertFalse(plan_promise_scope_errors(self.root,plan,record))
        plan['contributions'][0]['authorization']+=' Synthetic changed authorization.'
        self.assertIn('PLAN_REVIEW_SCOPE_MISMATCH',self.codes({'errors':plan_promise_scope_errors(self.root,plan,record)}))

    def test_private_reading_permission_or_review_alias_path_is_refused(self):
        private=self.root/'support/.private/input.md';private.parent.mkdir(parents=True);private.write_text(SYNTH)
        source=read_json(self.root/SOURCE);source['access']['permission_note']='support/.private/input.md'
        write_json(self.root/SOURCE,source)
        self.t.failcode('SOURCE_PRIVATE_ORIGINAL',freeze_snapshot,self.root)
        self.assertFalse((self.root/'snapshots').exists())
        source['access'].pop('permission_note');write_json(self.root/SOURCE,source)
        record=read_json(self.root/REVIEW);record['inputs'].append(dict(path='support/.private/input.md',sha256=file_hash(self.root,'support/.private/input.md')))
        write_json(self.root/REVIEW,record)
        self.t.failcode('SOURCE_PRIVATE_ORIGINAL',freeze_snapshot,self.root)
        self.assertIn('SOURCE_PRIVATE_ORIGINAL',self.codes(validate_reviews(self.root,[REVIEW])))

    def test_changed_consumed_locator_invalidates_source_scope_and_math_inputs(self):
        p,plan=self.t.make(draft=False);old=plan['snapshot_id']
        from survey_core.models import load_node, node_bytes
        path=self.root/'knowledge/nodes/N-main.md';node=load_node(path)
        node.meta['sources'][0]['locator']='Synthetic new paragraph not read'
        path.write_bytes(node_bytes(node.meta,node.body))
        plan['snapshot_id']=freeze_snapshot(self.root)['artifacts']['snapshot_id'];write_json(p,plan)
        ready=assess_readiness(self.root,plan)
        self.assertIn('SOURCE_LOCATOR_UNCHECKED',self.codes(ready));self.assertIn('REVIEW_STALE',self.codes(ready))
        oldplan=dict(plan,snapshot_id=old)
        self.assertEqual(assess_readiness(self.root,oldplan)['status'],'READY')

    def test_raw_bytes_alias_cannot_enter_package_even_if_release_gate_mocked(self):
        # This isolates the package byte guard, not a claimed release or build.
        p,plan=self.t.make(draft=False);prepare_output(self.root,p)
        alias=p.parent/'evidence/original-alias.txt';alias.parent.mkdir(exist_ok=True)
        alias.write_bytes((self.root/'knowledge/material.txt').read_bytes())
        from survey_core.release import package_output
        allowed={'errors':[], 'warnings':[], 'artifacts':{'snapshot_id':plan['snapshot_id']}}
        with patch('survey_core.release.assess_release',return_value=allowed):
            self.t.failcode('SOURCE_ORIGINAL_NOT_PACKAGED',package_output,self.root,plan['output_id'],self.t.base/'must-not-exist.zip')
        self.assertFalse((self.t.base/'must-not-exist.zip').exists())

    def test_malformed_new_facts_remain_unverified_without_typeerror(self):
        original=read_json(self.root/SOURCE)
        for key in ('availability','redistribution'):
            for value in (None,[], {'status':[]}, {'status':{}}, {'status':'granted','checked_at':{},'basis':[]}):
                source=copy.deepcopy(original);source['access'][key]=value;write_json(self.root/SOURCE,source)
                facts=validate_knowledge(self.root)['artifacts']['source_facts'][0]
                self.assertEqual(facts['access' if key=='availability' else 'redistribution'],'UNVERIFIED')
        write_json(self.root/SOURCE,original)
        record=read_json(self.root/REVIEW);record['reviewer']='';write_json(self.root/REVIEW,record)
        self.assertIn('SOURCE_REVIEW_MISSING',self.codes(validate_reviews(self.root,[REVIEW])))

    def test_plan_scoped_source_candidate_does_not_infer_unconsumed_reading(self):
        from test_v2 import putnode
        from survey_core.models import load_node, node_bytes
        putnode(self.root,'N-unconsumed','result','Synthetic unconsumed source result.',source=True,status='established')
        path=self.root/'knowledge/nodes/N-unconsumed.md';node=load_node(path)
        node.meta['sources'][0]['locator']='Synthetic unconsumed paragraph'
        path.write_bytes(node_bytes(node.meta,node.body))
        p,plan,candidate,record=self.candidate()
        self.assertEqual(assess_readiness(self.root,plan)['status'],'READY')
        report=self.accept(p);self.assertEqual(report['status'],'ACCEPTED',report['errors'])
        self.assertEqual(record['scope']['source_reading']['S-test']['locators'],['Synthetic fixture paragraph 1'])

    def test_freeze_rechecks_final_captured_source_permission_before_publish(self):
        from survey_core.sources import require_public_originals as actual
        source_before=(self.root/SOURCE).read_bytes()
        for visibility,permission,code in (('private','denied','SOURCE_PRIVATE_ORIGINAL'),
                                           ('public','denied','SOURCE_REDISTRIBUTION_REJECTED')):
            with self.subTest(visibility=visibility,permission=permission):
                (self.root/SOURCE).write_bytes(source_before)
                captured=[]
                def revoke_after_initial_check(inv):
                    actual(inv);captured.append(inv.root)
                    if inv.root==self.root:
                        source=read_json(self.root/SOURCE)
                        source['access']['material_visibility']=visibility
                        source['access']['redistribution'].update(status=permission,
                            basis='Synthetic explicit refusal during capture.')
                        write_json(self.root/SOURCE,source)
                with patch('survey_core.sources.require_public_originals',side_effect=revoke_after_initial_check):
                    self.t.failcode(code,freeze_snapshot,self.root)
                self.assertEqual(captured,[self.root])  # The second guard rejects its captured bytes.
                snapshots=self.root/'snapshots'
                self.assertFalse(list(snapshots.iterdir()))
                self.assertFalse((self.root/'.survey-write.lock').exists())

    def test_freeze_reuse_checks_captured_bytes_without_rewriting_history(self):
        from survey_core.sources import require_public_originals as actual
        before=(self.root/SOURCE).read_bytes();source=read_json(self.root/SOURCE)
        source['access']['material_visibility']='private'
        source['access']['redistribution'].update(status='denied',basis='Synthetic historical refusal.')
        write_json(self.root/SOURCE,source)
        # Construct a synthetic unsafe historical snapshot only to test refusal
        # of its reuse. This mocked fixture does not represent product acceptance.
        with patch('survey_core.sources.require_public_originals',return_value=None):
            sid=freeze_snapshot(self.root)['artifacts']['snapshot_id']
        folder=self.root/'snapshots'/sid
        historical={p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}
        (self.root/SOURCE).write_bytes(before)
        def revoke_after_initial_check(inv):
            actual(inv)
            if inv.root==self.root:write_json(self.root/SOURCE,source)
        with patch('survey_core.sources.require_public_originals',side_effect=revoke_after_initial_check):
            self.t.failcode('SOURCE_PRIVATE_ORIGINAL',freeze_snapshot,self.root)
        self.assertEqual(list((self.root/'snapshots').iterdir()),[folder])
        self.assertEqual({p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()},historical)
