"""2.0.1 regressions from adversarial comparison, not mathematical attestations."""
from __future__ import annotations
import ast
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from test_v2 import (ROOT, SKILL, fixture, plan, authored_toy, putnode,
                     synthetic_reviews, read_json, write_json, SurveyError, now)
from survey_core.common import SOFTWARE_VERSION, VERSION, valid_date, file_hash
from survey_core.tex import inspect_tex, validate_locations
from survey_core.exports import validate_structure, output_inputs
from survey_core.models import load_plan, load_project, load_node
from survey_core.release import semantic_scope_errors, assess_release
from survey_core.reviews import load_review, review_template
from survey_core.readiness import assess_readiness
from survey_core.snapshots import freeze_snapshot, diff_snapshots, verify_snapshot
from survey_core.history import save_record, verify_record, verify_history
from survey_core.build import build_output, render_output
from survey_core.compatibility import identify_contract, import_v2_b
from survey_core.knowledge import validate_knowledge
from package_release import package, verify_archive

CHECKS=['whole_manuscript','canonical_use','conditions_quantifiers','selection','attribution','proof_obligations','readability']

class Integration201(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
        self.root=fixture(self.base/'project',True);plan(self.root,draft=False);authored_toy(self.root)
        self.out=self.root/'outputs/mini';self.main=self.out/'manuscript/main.tex'
    def tearDown(self):self.tmp.cleanup()
    def failcode(self,code,fn,*args,**kw):
        with self.assertRaises(SurveyError) as ctx:fn(*args,**kw)
        self.assertEqual(ctx.exception.diagnostic['code'],code)
    def principal_location(self):
        n=next(i for i,line in enumerate(self.main.read_text().splitlines(),1) if 'statements/N-main.tex' in line)
        return {'path':'manuscript/main.tex','line_start':n,'line_end':n}
    def semantic(self):
        r=review_template(self.out,'output_semantic',['mini'],output_inputs(self.out))
        r.update(review_id='SYNTHETIC201',reviewer_mode='author_reread',reviewed_at=now(),
                 disposition='accepted',unchecked_items=[],findings=['Synthetic gate input only; no real mathematical review is asserted.'])
        r['scope']={'output_ids':['mini'],'profile':'minimal','node_ids':['N-q','N-main','N-def'],
            'whole_manuscript':True,'checks':CHECKS.copy(),'principal_locations':{'N-main':[self.principal_location()]},'proof_locations':{},'proof_steps':{}}
        return r
    def codes(self):return {x['code'] for x in validate_structure(self.root,'mini')['errors']}
    def test_U01_preamble_reference_is_not_statement(self):
        text=self.main.read_text();ref=r'\input{../generated/statements/N-main.tex}'
        self.main.write_text(text.replace(ref,'').replace(r'\begin{document}',ref+'\n'+r'\begin{document}'))
        self.assertNotIn('generated/statements/N-main.tex',inspect_tex(self.out).body_inputs)
        self.assertTrue(self.codes())
    def test_U02_uncalled_macro_reference_is_not_statement(self):
        text=self.main.read_text();ref=r'\input{../generated/statements/N-main.tex}'
        self.main.write_text(text.replace(ref,r'\newcommand{\unused}{'+ref+'}'))
        self.assertNotIn('generated/statements/N-main.tex',inspect_tex(self.out).body_inputs)
        self.assertTrue(self.codes())
    def test_U03_literal_false_branch_is_not_statement(self):
        text=self.main.read_text();ref=r'\input{../generated/statements/N-main.tex}'
        self.main.write_text(text.replace(ref,r'\iffalse '+ref+r'\fi'))
        self.assertNotIn('generated/statements/N-main.tex',inspect_tex(self.out).body_inputs)
    def test_U04_nested_inputs_follow_compiler_working_directory(self):
        (self.out/'manuscript/sections').mkdir();ref=r'\input{../generated/statements/N-main.tex}'
        self.main.write_text(self.main.read_text().replace(ref,r'\input{sections/answer.tex}'))
        (self.out/'manuscript/sections/answer.tex').write_text(ref)
        scan=inspect_tex(self.out);self.assertIn('generated/statements/N-main.tex',scan.body_inputs)
        self.assertIn('manuscript/sections/answer.tex',{x['path'] for x in scan.locations})
        self.assertFalse(scan.errors)
    def test_U05_output_directory_owns_plan_identity(self):
        p=self.out/'plan.json';v=read_json(p);v['output_id']='another';write_json(p,v)
        self.failcode('PLAN_OUTPUT_MISMATCH',load_plan,p)
    def test_U06_semantic_nonexistent_location_refused(self):
        loc={'path':'manuscript/imaginary.tex','line_start':1,'line_end':1}
        self.assertTrue(validate_locations(self.out,[loc],node_id='N-main',canonical=True))
    def test_U07_semantic_out_of_range_refused(self):
        loc=self.principal_location();loc['line_end']=99999
        self.assertTrue(validate_locations(self.out,[loc]))
    def test_U08_semantic_wrong_existing_location_refused(self):
        loc={'path':'manuscript/main.tex','line_start':1,'line_end':1}
        self.assertTrue(validate_locations(self.out,[loc],node_id='N-main',canonical=True))
    def test_U09_semantic_real_location_passes(self):
        self.assertEqual(validate_locations(self.out,[self.principal_location()],node_id='N-main',canonical=True),[])
    def test_U10_whole_manuscript_flag_required(self):
        r=self.semantic();r['scope']['whole_manuscript']=False
        self.assertTrue(semantic_scope_errors(self.out,load_plan(self.out/'plan.json'),['N-main'],r))
    def test_U11_all_reading_checks_required(self):
        r=self.semantic();r['scope']['checks'].remove('conditions_quantifiers')
        self.assertTrue(semantic_scope_errors(self.out,load_plan(self.out/'plan.json'),['N-main'],r))
    def test_U12_proof_locations_required(self):
        r=self.semantic();p=load_plan(self.out/'plan.json');p['proof_obligations']=[{'node_id':'N-main','required_steps':['multiply']}]
        r['scope']['proof_steps']['N-main']=['multiply']
        self.assertTrue(semantic_scope_errors(self.out,p,['N-main'],r))
        r['scope']['proof_locations']['N-main']=[{'path':'manuscript/main.tex','line_start':10,'line_end':10}]
        self.assertEqual(semantic_scope_errors(self.out,p,['N-main'],r),[])
    def test_U13_valid_new_record_supersedes_legacy_scope(self):
        old=self.semantic();old['scope']['principal_locations']={'N-main':'unvalidated prose'}
        write_json(self.out/'evidence/a-old-review.json',old)
        newer=self.semantic();newer['review_id']='SYNTHETIC201-new';write_json(self.out/'evidence/z-new-review.json',newer)
        r=assess_release(self.root,'mini')
        self.assertIn('SYNTHETIC201-new',r['artifacts']['used_output_review_ids'])
        self.assertNotIn('OUTPUT_SEMANTIC_REVIEW_PENDING',{x['code'] for x in r['errors']})
    def test_U14_future_year_rejected(self):self.assertFalse(valid_date('2999-01-01'))
    def test_U15_future_timestamp_rejected(self):self.assertFalse(valid_date((datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()))
    def test_U16_independent_review_requires_identity(self):
        r=self.semantic();r['reviewer_mode']='independent_review';p=self.out/'evidence/test-review.json';write_json(p,r)
        self.failcode('REVIEW_INVALID',load_review,p)
    def test_U17_review_template_cannot_overwrite_existing(self):
        target=self.root/'evidence/keep.json';target.write_bytes(b'original evidence')
        p=subprocess.run([sys.executable,str(SKILL/'scripts/survey.py'),'review','template',str(self.root),'--kind','mathematical','--id','N-main','--to','evidence/keep.json','--json'],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0);self.assertEqual(target.read_bytes(),b'original evidence')
    def test_U18_output_template_pending_and_nonoverwriting(self):
        cmd=[sys.executable,str(SKILL/'scripts/survey.py'),'output','review-template',str(self.root),'--output','mini','--kind','output_semantic','--to','evidence/pending.json','--json']
        a=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(a.returncode,0,a.stdout)
        r=read_json(self.out/'evidence/pending.json');self.assertEqual(r['reviewer_mode'],'not_performed');self.assertFalse(r['scope']['whole_manuscript'])
        old=(self.out/'evidence/pending.json').read_bytes();b=subprocess.run(cmd,capture_output=True,text=True)
        self.assertNotEqual(b.returncode,0);self.assertEqual((self.out/'evidence/pending.json').read_bytes(),old)
    def test_U19_unattached_hash_is_not_original_material(self):
        p=self.root/'knowledge/sources/S-test.json';s=read_json(p);s['access']['local_path']=None;write_json(p,s);synthetic_reviews(self.root)
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];p=self.out/'plan.json';v=read_json(p);v['snapshot_id']=sid;write_json(p,v)
        r=assess_readiness(self.root,p);self.assertIn('SOURCE_REVIEW_MISSING',{x['code'] for x in r['errors']})
    def test_U20_history_reuse_preserves_bytes(self):
        data={'inputs/main.tex':b'first','compiled/report.json':b'{"status":"FAILED"}'}
        a=save_record(self.out,'build',data);folder=self.out/'history/build'/a['history_id'];stamp=(folder/'manifest.json').stat().st_mtime_ns
        b=save_record(self.out,'build',data);self.assertEqual(a,b);self.assertEqual(stamp,(folder/'manifest.json').stat().st_mtime_ns)
        save_record(self.out,'build',{'inputs/main.tex':b'second'});self.assertEqual((folder/'files/inputs/main.tex').read_bytes(),b'first')
    def test_U21_history_tamper_refused(self):
        a=save_record(self.out,'build',{'inputs/main.tex':b'first'});folder=self.out/'history/build'/a['history_id'];(folder/'files/inputs/main.tex').write_bytes(b'changed')
        self.failcode('HISTORY_TAMPERED',verify_record,folder)
    @unittest.skipUnless(shutil.which('pdflatex') and shutil.which('pdftoppm'),'External TeX/Poppler unavailable')
    def test_U22_real_build_then_failed_attempt_preserves_prior_build(self):
        build_output(self.root,'mini');render_output(self.root,'mini');first=read_json(self.out/'history/latest-build.json')['history_id']
        old=self.out/'history/build'/first/'files/compiled/main.pdf';data=old.read_bytes()
        self.main.write_text(self.main.read_text().replace(r'\end{document}',r'\undefinedCommand'+ '\n'+r'\end{document}'))
        with self.assertRaises(SurveyError):build_output(self.root,'mini')
        self.assertEqual(read_json(self.out/'history/latest-build.json')['status'],'FAILED')
        self.assertEqual(old.read_bytes(),data);self.assertGreaterEqual(len(verify_history(self.root,'mini')['artifacts']['records']),3)
        self.assertNotEqual(read_json(self.out/'build/build-report.json')['status'],'BUILT')
    def foreign(self):
        root=fixture(self.base/'foreign');p=root/'evidence/reviews/review.json';p.parent.mkdir(parents=True,exist_ok=True)
        write_json(p,{'review_id':'FOREIGN-SYNTHETIC','checks':{},'disposition':'accepted','limitations':[]})
        return root
    def test_U23_foreign_contract_detected_not_silently_loaded(self):
        root=self.foreign();self.assertEqual(identify_contract(root)['contract'],'v2-b')
        self.failcode('FORMAT_MIGRATION_REQUIRED',load_project,root)
    def test_U24_import_preserves_body_and_original_archive(self):
        root=self.foreign();raw=(root/'knowledge/nodes/N-main.md').read_bytes();oldnode=load_node(root/'knowledge/nodes/N-main.md')
        new=self.base/'imported';r=import_v2_b(root,new);self.assertEqual(r['status'],'IMPORTED_UNVERIFIED')
        node=load_node(new/'knowledge/nodes/N-main.md');self.assertEqual(oldnode.body,node.body);self.assertEqual(oldnode.statement,node.statement)
        self.assertEqual(node.meta['mathematical_status'],'unassessed');self.assertFalse((new/'outputs').exists());self.assertFalse((new/'evidence/reviews').exists())
        with zipfile.ZipFile(new/'legacy/v2-b/original.zip') as z:self.assertEqual(z.read('knowledge/nodes/N-main.md'),raw)
        self.assertEqual(validate_knowledge(new)['status'],'VALID')
    def test_U25_import_destination_not_overwritten(self):
        root=self.foreign();self.failcode('DESTINATION_EXISTS',import_v2_b,root,self.root)
    def test_U26_mixed_review_contract_refused(self):
        root=self.foreign();write_json(root/'evidence/reviews/native.json',self.semantic())
        self.assertEqual(identify_contract(root)['contract'],'mixed-review-contracts')
        self.failcode('FORMAT_MIGRATION_REQUIRED',load_project,root)
    def test_U27_review_only_change_has_scoped_impact(self):
        old=load_plan(self.out/'plan.json')['snapshot_id'];p=self.root/'evidence/reviews/mathematical-N-main.json';v=read_json(p);v['findings'].append('Changed synthetic review conclusion for an impact regression.');write_json(p,v)
        new=freeze_snapshot(self.root)['artifacts']['snapshot_id'];r=diff_snapshots(self.root,old,new)
        self.assertEqual(r['artifacts']['changed'],[]);self.assertEqual(r['artifacts']['affected_outputs'][0]['output_id'],'mini')
        self.assertEqual(r['artifacts']['affected_outputs'][0]['review_changes'],['evidence/reviews/mathematical-N-main.json'])
    def test_U28_impact_reports_nested_authored_location(self):
        (self.out/'manuscript/sections').mkdir();ref=r'\input{../generated/statements/N-main.tex}'
        self.main.write_text(self.main.read_text().replace(ref,r'\input{sections/answer.tex}'));(self.out/'manuscript/sections/answer.tex').write_text(ref)
        old=load_plan(self.out/'plan.json')['snapshot_id'];p=self.root/'knowledge/nodes/N-def.md';p.write_bytes(p.read_bytes()+b'\nChanged input.')
        new=freeze_snapshot(self.root)['artifacts']['snapshot_id'];r=diff_snapshots(self.root,old,new)
        locations=r['artifacts']['affected_outputs'][0]['authored_locations'];self.assertIn('manuscript/sections/answer.tex',{x['path'] for x in locations})
    def test_U29_schema_stable_runtime_patch_version(self):
        self.assertEqual(VERSION,'2.0.0');self.assertEqual(SOFTWARE_VERSION,'2.0.3')
        sid=load_plan(self.out/'plan.json')['snapshot_id'];self.assertEqual(verify_snapshot(self.root,sid)['status'],'VERIFIED')
    def test_U30_python_310_grammar(self):
        for p in (SKILL/'scripts').rglob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p),feature_version=(3,10))
    def test_U31_installer_contains_and_executes_new_modules(self):
        destination=self.base/'skill.zip';package(SKILL,destination);verify_archive(destination)
        unpacked=self.base/'installed'
        with zipfile.ZipFile(destination) as z:z.extractall(unpacked)
        skill=unpacked/'pure-math-survey'
        code="import sys,json;sys.path.insert(0,"+repr(str(skill/'scripts'))+");from survey_core import tex,history,compatibility;print(json.dumps([tex.__file__,history.__file__,compatibility.__file__]))"
        p=subprocess.run([sys.executable,'-I','-c',code],capture_output=True,text=True,cwd=self.base)
        self.assertEqual(p.returncode,0,p.stderr);self.assertTrue(all(Path(f).is_relative_to(skill) for f in json.loads(p.stdout)))
