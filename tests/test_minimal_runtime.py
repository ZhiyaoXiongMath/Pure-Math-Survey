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
            z.extractall(self.base/'extracted')
        packaged=self.base/'extracted/mini'
        rebuilt=self.base/'rebuilt'
        proc=subprocess.run([sys.executable,'-I',str(packaged/'rebuild.py'),'--output',str(rebuilt)],cwd=packaged,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        report=read_json(rebuilt/'rebuild-report.json')
        self.assertEqual(report['status'],'BUILT');self.assertEqual(report['input_hash'],read_json(path.parent/'generated/manifest.json')['input_hash'])
        self.assertTrue((rebuilt/'build/main.pdf').read_bytes().startswith(b'%PDF-'))
        # The build remains input-bound; no approval credential can repair stale bytes.
        main=path.parent/'manuscript/main.tex';main.write_bytes(main.read_bytes()+b'\n% Changed after build\n')
        self.assertIn('BUILD_STALE',{e['code'] for e in assess_release(self.root,'mini')['errors']})
        self.code('PACKAGE_NOT_READY',package_output,self.root,'mini',self.base/'stale.zip')

    def test_all_unsupported_modes_and_views_preserve_bytes(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];before=tree(self.root)
        for profile in ('thematic','lecture','paper'):
            self.code('PROFILE_UNSUPPORTED',create_plan,self.root,'bad',profile=profile)
            proc,report=self.cli('output','plan',self.root,'--output','bad','--profile',profile)
            self.assertEqual(proc.returncode,2);self.assertEqual(report['errors'][0]['code'],'PROFILE_UNSUPPORTED')
        for view in ('foundations','results','methods','boundaries'):
            self.code('VIEW_UNSUPPORTED',create_plan,self.root,'bad',view=view)
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
                 lambda:package_output(self.root,'mini',self.base/'never.zip'),lambda:create_plan(self.root,'other')]
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
        self.code('CONTRACT_INVALID',create_plan,self.root,'../outside')
        self.assertEqual(tree(self.root),before)
        path=plan(self.root);authored_toy(self.root);main=path.parent/'manuscript/main.tex'
        main.write_text(main.read_text(encoding='utf-8').replace(r'\end{document}',r'\input{../../scope.md}\end{document}'),encoding='utf-8')
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
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if isinstance(node,ast.ImportFrom):
                    self.assertNotIn((node.module or '').split('.')[-1],{'reviews','readiness','dispatch_ledger'})
        proc,r=self.cli('--version');self.assertEqual(proc.returncode,0)
        self.assertEqual(r['artifacts']['version'],'2.4.1-dev.3')
        self.assertEqual(r['artifacts']['runtime_contract'],RUNTIME_CONTRACT)
        self.assertEqual(r['artifacts']['supported_profiles'],['minimal'])

    def test_source_original_permission_and_alias_protections_remain(self):
        path=self.root/'knowledge/sources/S-test.json';obj=read_json(path);obj['access']['material_visibility']='private';write_json(path,obj)
        self.code('SOURCE_PRIVATE_ORIGINAL',freeze_snapshot,self.root)
        (self.root/'evidence/source-checks/test.md').write_bytes((self.root/'knowledge/material.txt').read_bytes())
        obj['access']['local_path']=None;write_json(path,obj)
        self.code('SOURCE_ORIGINAL_ALIAS_UNSAFE',freeze_snapshot,self.root)

    def test_source_hash_mismatch_rejects_kb_only_and_freeze_without_mutation(self):
        from survey_core.knowledge import validate_knowledge,index_knowledge
        raw=self.root/'knowledge/material.txt';raw.write_bytes(raw.read_bytes()+b'Changed original bytes.\n')
        (self.root/'evidence/source-checks/test.md').write_bytes(raw.read_bytes())
        before=tree(self.root)
        for operation in (validate_knowledge,index_knowledge,freeze_snapshot):
            self.code('SOURCE_MATERIAL_MISMATCH',operation,self.root)
            self.assertEqual(tree(self.root),before)
        proc,report=self.cli('kb','validate',self.root)
        self.assertEqual(proc.returncode,2)
        self.assertEqual(report['errors'][0]['code'],'SOURCE_MATERIAL_MISMATCH')
        self.assertEqual(tree(self.root),before)
        self.assertFalse((self.root/'outputs').exists())

    def test_changed_original_rejects_all_output_operations_without_mutation(self):
        path=plan(self.root);authored_toy(self.root)
        raw=self.root/'knowledge/material.txt';raw.write_bytes(raw.read_bytes()+b'changed')
        before=tree(self.root)
        for operation in [lambda:create_plan(self.root,'other'),lambda:prepare_output(self.root,path),
                          lambda:build_output(self.root,'mini'),lambda:package_output(self.root,'mini',self.base/'never.zip')]:
            self.code('SOURCE_MATERIAL_MISMATCH',operation);self.assertEqual(tree(self.root),before)
        self.assertFalse((self.base/'never.zip').exists())

    def test_actual_original_aliases_are_omitted_without_review_or_declared_hash(self):
        from survey_core.common import sha
        from survey_core.knowledge import validate_knowledge
        for declared in (True,False):
            with self.subTest(declared_hash=declared):
                root=fixture(self.base/('declared' if declared else 'unrecorded'))
                raw=(root/'knowledge/material.txt').read_bytes();digest=sha(raw)
                (root/'evidence/source-checks/test.md').write_bytes(raw)
                source_path=root/'knowledge/sources/S-test.json';source=read_json(source_path)
                if not declared:
                    source['access']['material_sha256']=None;write_json(source_path,source)
                check=validate_knowledge(root)
                self.assertEqual(check['artifacts']['source_facts'][0]['bytes'],'VERIFIED' if declared else 'UNVERIFIED')
                path=plan(root);authored_toy(root);out=path.parent
                self.assertFalse((out/'materials/knowledge/material.txt').exists())
                self.assertFalse((out/'materials/evidence/source-checks/test.md').exists())
                build_output(root,'mini');archive=self.base/(root.name+'.zip')
                self.assertEqual(package_output(root,'mini',archive)['status'],'PACKAGED')
                with zipfile.ZipFile(archive) as packaged:
                    self.assertFalse(any(sha(packaged.read(name))==digest for name in packaged.namelist()))
                self.assertFalse(any('reviews' in name.split('/') for name in all_files(root)))
                if not declared:
                    # An output-local alias is also refused at package time.
                    (out/'manuscript/original-copy.bin').write_bytes(raw)
                    build_output(root,'mini');before=tree(root)
                    self.code('SOURCE_ORIGINAL_NOT_PACKAGED',package_output,root,'mini',self.base/'alias.zip')
                    self.assertEqual(tree(root),before);self.assertFalse((self.base/'alias.zip').exists())

    def test_prepare_preserves_authoring_and_changed_canonical_updates_live(self):
        path=plan(self.root);authored_toy(self.root);main=path.parent/'manuscript/main.tex';old_main=main.read_bytes()
        old_statement=(path.parent/'generated/statements/N-main.tex').read_bytes()
        outline=path.parent/'outline.md';outline.write_bytes(b'Author connection notes.\n')
        node=self.root/'knowledge/nodes/N-main.md';node.write_bytes(node.read_bytes().replace(b'x^2=0',b'x x=0'))
        prepare_output(self.root,path)
        self.assertEqual(main.read_bytes(),old_main);self.assertEqual(outline.read_bytes(),b'Author connection notes.\n')
        self.assertIn(b'x x=0',(path.parent/'generated/statements/N-main.tex').read_bytes())
        old=list((path.parent/'history/preparation').glob('H-*/files/generated/statements/N-main.tex'))
        self.assertEqual(len(old),1);self.assertEqual(old[0].read_bytes(),old_statement)
        self.assertFalse((self.root/'snapshots').exists())

    def test_definition_closure_is_automatic_but_unrelated_method_is_not_consumed(self):
        putnode(self.root,'N-method','method')
        path=plan(self.root);prepare_output(self.root,path)
        consumed=verify_generated(self.root,load_plan(path))['consumed_nodes']
        self.assertEqual(set(consumed),{'N-main','N-def'})

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
