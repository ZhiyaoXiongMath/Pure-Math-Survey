"""Minimal candidate integration and byte-preserving refusal; synthetic mathematics only."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from test_v2 import (fixture, plan, authored_toy, putnode, SCRIPTS, SKILL, SurveyError,
                     read_json, write_json, load_plan, load_node, prepare_output, freeze_snapshot,
                     build_output, package_output, validate_structure, inventory)
from survey_core.common import all_files, atomic_bytes, safe, RUNTIME_CONTRACT
from survey_core.plans import create_plan
from survey_core.snapshots import load_snapshot
from survey_core.exports import verify_generated
from survey_core.release import assess_release


def tree(root):
    return {p: safe(root,p,True).read_bytes() for p in all_files(root)}


class MinimalRuntime(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.root=fixture(self.base/'project')
    def tearDown(self):self.tmp.cleanup()
    def code(self,expected,fn,*args,**kwargs):
        with self.assertRaises(SurveyError) as got:fn(*args,**kwargs)
        self.assertEqual(got.exception.diagnostic['code'],expected)
    def cli(self,*args):
        proc=subprocess.run([sys.executable,'-I',str(SCRIPTS/'survey.py'),*map(str,args),'--json'],capture_output=True,text=True)
        return proc,json.loads(proc.stdout)

    def test_actual_kb_prepare_build_package_without_review_records(self):
        path=plan(self.root);authored_toy(self.root)
        self.assertNotIn('proof_obligations',load_plan(path))
        self.assertFalse(any('reviews' in p.split('/') for p in all_files(self.root)))
        self.assertEqual(build_output(self.root,'mini')['status'],'BUILT')
        self.assertEqual(assess_release(self.root,'mini')['status'],'PACKAGEABLE')
        archive=self.base/'output.zip';self.assertEqual(package_output(self.root,'mini',archive)['status'],'PACKAGED')
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
            self.assertFalse(any('reviews' in n.split('/') for n in names))
            self.assertTrue(z.read('mini/build/main.pdf').startswith(b'%PDF-'))
            self.assertEqual(z.read('mini/generated/statements/N-main.tex'),load_node(self.root/'knowledge/nodes/N-main.md').statement)
            self.assertFalse(any(n.endswith('/knowledge/material.txt') for n in names))
        # The build remains input-bound; no approval credential can repair stale bytes.
        main=path.parent/'manuscript/main.tex';main.write_bytes(main.read_bytes()+b'\n% Changed after build\n')
        self.assertIn('BUILD_STALE',{e['code'] for e in assess_release(self.root,'mini')['errors']})
        self.code('PACKAGE_NOT_READY',package_output,self.root,'mini',self.base/'stale.zip')

    def test_all_unsupported_modes_and_views_preserve_bytes(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];before=tree(self.root)
        for profile in ('thematic','lecture','paper'):
            self.code('PROFILE_UNSUPPORTED',create_plan,self.root,'bad',sid,profile=profile)
            proc,report=self.cli('output','plan',self.root,'--output','bad','--snapshot',sid,'--profile',profile)
            self.assertEqual(proc.returncode,2);self.assertEqual(report['errors'][0]['code'],'PROFILE_UNSUPPORTED')
        for view in ('foundations','results','methods','boundaries'):
            self.code('VIEW_UNSUPPORTED',create_plan,self.root,'bad',sid,view=view)
        self.assertEqual(tree(self.root),before)

    def test_old_commands_and_draft_option_are_explicitly_retired(self):
        before=tree(self.root)
        for args in [('review','template',self.root),('review','accept',self.root),('kb','readiness',self.root),
                     ('output','review-template',self.root),('output','prepare',self.root,'--draft')]:
            proc,r=self.cli(*args);self.assertEqual(proc.returncode,2)
            self.assertIn(r['errors'][0]['code'],{'COMMAND_UNSUPPORTED','OPTION_UNSUPPORTED'})
        self.assertEqual(tree(self.root),before)

    def test_legacy_projects_reject_before_any_atomic_or_writer_calls(self):
        path=plan(self.root);prepare_output(self.root,path);obj=read_json(self.root/'project.json');obj.pop('runtime_contract');write_json(self.root/'project.json',obj)
        before=tree(self.root)
        actions=[lambda:freeze_snapshot(self.root),lambda:prepare_output(self.root,path),lambda:build_output(self.root,'mini'),
                 lambda:package_output(self.root,'mini',self.base/'never.zip'),lambda:create_plan(self.root,'other',load_plan(path)['snapshot_id'])]
        for action in actions:
            with patch('os.open',side_effect=AssertionError('A legacy project attempted a write')):
                self.code('LEGACY_PROJECT_UNSUPPORTED',action)
        for args in [('kb','index',self.root),('kb','freeze',self.root),('output','render',self.root,'--output','mini')]:
            proc,r=self.cli(*args);self.assertEqual(proc.returncode,2);self.assertEqual(r['errors'][0]['code'],'LEGACY_PROJECT_UNSUPPORTED')
        self.assertEqual(tree(self.root),before);self.assertFalse((self.base/'never.zip').exists())

    def test_legacy_plan_or_unsupported_loaded_profile_preserves_project(self):
        path=plan(self.root);original=read_json(path)
        for field,value,code in [('runtime_contract',None,'LEGACY_PROJECT_UNSUPPORTED'),('profile','lecture','PROFILE_UNSUPPORTED'),
                                 ('view','methods','VIEW_UNSUPPORTED'),('editorial_policy','four-modes-2026-10-15-r5','EDITORIAL_POLICY_UNSUPPORTED')]:
            obj=dict(original);obj[field]=value;write_json(path,obj);before=tree(self.root)
            self.code(code,prepare_output,self.root,path);self.assertEqual(tree(self.root),before)

    def test_invalid_plan_and_tex_paths_preserve_original_bytes(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];before=tree(self.root)
        self.code('CONTRACT_INVALID',create_plan,self.root,'../outside',sid)
        self.assertEqual(tree(self.root),before)
        path=plan(self.root);authored_toy(self.root);main=path.parent/'manuscript/main.tex'
        main.write_text(main.read_text().replace(r'\end{document}',r'\input{../../scope.md}\end{document}'))
        before=tree(self.root)
        with self.assertRaises(SurveyError):build_output(self.root,'mini')
        self.assertEqual(tree(self.root),before)

    def test_review_files_are_not_loaded_or_frozen(self):
        # An unrelated malformed historical file cannot become an active credential.
        path=self.root/'evidence/reviews/old.json';path.parent.mkdir();path.write_bytes(b'not JSON')
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];m,_=load_snapshot(self.root,sid)
        self.assertFalse(any('/reviews/' in x['path'] for x in m['files']))
        p=plan(self.root);prepare_output(self.root,p);verify_generated(self.root,load_plan(p))
        self.assertEqual(path.read_bytes(),b'not JSON')

    def test_runtime_reachability_has_no_audit_modules_or_dispatch(self):
        modules=SCRIPTS/'survey_core'
        for name in ('reviews.py','readiness.py','exposition.py'):self.assertFalse((modules/name).exists())
        self.assertFalse((SCRIPTS/'dispatch_ledger.py').exists())
        for path in modules.glob('*.py'):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn((node.module or '').split('.')[-1],{'reviews','readiness','dispatch_ledger'})
        proc,r=self.cli('--version');self.assertEqual(proc.returncode,0)
        self.assertEqual(r['artifacts']['version'],'2.4.1-dev.2')
        self.assertEqual(r['artifacts']['runtime_contract'],RUNTIME_CONTRACT)
        self.assertEqual(r['artifacts']['supported_profiles'],['minimal'])

    def test_source_original_permission_and_alias_protections_remain(self):
        path=self.root/'knowledge/sources/S-test.json';obj=read_json(path);obj['access']['material_visibility']='private';write_json(path,obj)
        self.code('SOURCE_PRIVATE_ORIGINAL',freeze_snapshot,self.root)
        obj['access']['local_path']=None;write_json(path,obj)
        self.code('SOURCE_ORIGINAL_ALIAS_UNSAFE',freeze_snapshot,self.root)

    def test_prepare_preserves_authoring_and_changed_canonical_uses_new_snapshot(self):
        path=plan(self.root);authored_toy(self.root);main=path.parent/'manuscript/main.tex';old_main=main.read_bytes()
        outline=path.parent/'outline.md';outline.write_bytes(b'Author connection notes.\n')
        old_sid=load_plan(path)['snapshot_id'];node=self.root/'knowledge/nodes/N-main.md';node.write_bytes(node.read_bytes().replace(b'x^2=0',b'x x=0'))
        new_sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];obj=load_plan(path);obj['snapshot_id']=new_sid;write_json(path,obj)
        prepare_output(self.root,path)
        self.assertEqual(main.read_bytes(),old_main);self.assertEqual(outline.read_bytes(),b'Author connection notes.\n')
        self.assertIn(b'x x=0',(path.parent/'generated/statements/N-main.tex').read_bytes())
        self.assertIn(b'x^2=0',(self.root/'snapshots'/old_sid/'files/knowledge/nodes/N-main.md').read_bytes())

    def test_selection_closure_retains_main_module_without_inventing_dependency_explanation(self):
        from survey_core.models import node_bytes
        putnode(self.root,'N-method','mechanism',links=[('N-main','explains')])
        putnode(self.root,'N-extra','mechanism')
        main=self.root/'knowledge/nodes/N-main.md';node=load_node(main)
        node.meta['links'].append({'target':'N-method','relation':'explained_by'})
        main.write_bytes(node_bytes(node.meta,node.body))
        definition=self.root/'knowledge/nodes/N-def.md';node=load_node(definition)
        node.meta['links'].append({'target':'N-extra','relation':'explained_by'})
        definition.write_bytes(node_bytes(node.meta,node.body))
        path=plan(self.root);prepare_output(self.root,path)
        consumed=verify_generated(self.root,load_plan(path))['consumed_nodes']
        self.assertIn('N-method',consumed);self.assertNotIn('N-extra',consumed)

    def test_interrupted_atomic_write_keeps_previous_bytes(self):
        path=self.root/'scope.md';before=path.read_bytes()
        with patch('os.replace',side_effect=OSError('Injected interrupted replace')):
            with self.assertRaises(OSError):atomic_bytes(path,b'replacement')
        self.assertEqual(path.read_bytes(),before);self.assertFalse(list(path.parent.glob('.scope.md.*')))

    def test_snapshot_final_verification_failure_rolls_back_named_snapshot(self):
        import survey_core.snapshots as mod
        with patch.object(mod,'load_snapshot',side_effect=OSError('Injected final name read failure')):
            with self.assertRaises(OSError):freeze_snapshot(self.root)
        self.assertFalse(list((self.root/'snapshots').glob('KB-*')))
        self.assertFalse(list((self.root/'snapshots').glob('.pending-*')))

if __name__=='__main__':unittest.main()
