"""Retained snapshot, canonical, safety and real-build regression fixtures."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
ROOT=Path(__file__).resolve().parents[1];SKILL=ROOT/'skills/pure-math-survey';SCRIPTS=SKILL/'scripts'
sys.path.insert(0,str(SCRIPTS))
from survey_core.common import VERSION,SurveyError,atomic_bytes,canonical,file_hash,now,read_json,sha,write_json,writer
from survey_core.models import load_node,load_plan,load_source
from survey_core.knowledge import inventory,init_project,index_knowledge,validate_knowledge
from survey_core.snapshots import freeze_snapshot,load_snapshot,verify_snapshot,diff_snapshots
from survey_core.plans import create_plan,validate_plan,consumption
from survey_core.exports import prepare_output,verify_generated,validate_structure
from survey_core.models import node_bytes
from survey_core.release import package_output,assess_release
from survey_core.build import build_output,render_output,reading_budget
from package_release import package,verify_archive


def putnode(root,key,kind,statement=None,links=(),questions=('N-q',),source=False,status='unassessed'):
    meta={'schema_version':VERSION,'id':key,'kind':kind,'title':'Synthetic software fixture '+key,'facets':['foundations','results'] if kind=='result' else ['foundations'],
          'question_ids':list(questions) if kind!='question' else [],'mathematical_status':status,'origin':'local_derivation',
          'sources':[{'source_id':'S-test','locator':'Synthetic fixture paragraph 1','role':'support'}] if source else [],'links':[{'target':k,'relation':r} for k,r in links]}
    body='# Software fixture\n\n'
    if statement is not None:body+='## Canonical statement\n\n```latex\n'+statement+'\n```\n\n## Local argument\n\n'
    body+='Synthetic test data, not a real research-source or semantic review. For $x=0$, multiplication gives $x^2=0$.\n'
    path=root/f'knowledge/nodes/{key}.md';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(node_bytes(meta,body));return path

def fixture(root,second=False):
    scope=root.parent/(root.name+'-scope.md');scope.write_text('# Synthetic scope\n\nFor real x, verify x=0 implies x squared=0. No claim about mathematical survey quality.\n')
    init_project(root,'test-project',scope)
    state='unassessed'
    putnode(root,'N-q','question',questions=(),status=state)
    putnode(root,'N-def','definition',r'Let $x\in\mathbb R$.',status=state)
    putnode(root,'N-main','result',r'For $x\in\mathbb R$, $x=0$ implies $x^2=0$.',[('N-def','uses_definition')],source=True,status=state)
    (root/'evidence/source-checks').mkdir(parents=True)
    (root/'evidence/source-checks/test.md').write_text('# Synthetic source record\n\nA test harness material, not a literature-reading report.\n')
    (root/'knowledge/material.txt').write_text('Synthetic primary test material. For real x=0, x*x=0.\n')
    write_json(root/'knowledge/sources/S-test.json',{'schema_version':VERSION,'id':'S-test','kind':'primary','title':'Synthetic software fixture','authors':['Test harness'],
               'publication_status':'unpublished','identifiers':{'user_file':'Synthetic software test material'},'version':'Fixture v1',
               'access':{'state':'metadata_only','checked_at':None,
                         'material_sha256':file_hash(root,'knowledge/material.txt'),'local_path':'knowledge/material.txt','reading_note':'evidence/source-checks/test.md', 'material_visibility':'public',
                         'availability':dict(status='accessible',checked_at=now(),basis='Synthetic fixture bytes accessible to test harness.'),
                         'redistribution':dict(status='granted',checked_at=now(),basis='Synthetic test material authored by this fixture; no external license claim.')}})
    qs=[{'question_id':'N-q','answer_nodes':['N-main'],'mechanism_nodes':[],'boundary_nodes':[],'gaps':[],
         'assessment':'pending','rationale':'A bounded synthetic software test; not a literature completeness claim.'}]
    if second:
        putnode(root,'N-q2','question',questions=(),status=state);putnode(root,'N-other','result',r'For $y\in\mathbb R$, $y^2\geq0$.',questions=('N-q2',),status=state)
        qs.append({'question_id':'N-q2','answer_nodes':['N-other'],'mechanism_nodes':[],'boundary_nodes':[],'gaps':[],
                   'assessment':'pending','rationale':'Independent synthetic branch.'})
    write_json(root/'knowledge/coverage.json',{'schema_version':VERSION,'questions':qs})
    return root

def authored_toy(root,oid='mini',two_pages=False):
    p=root/f'outputs/{oid}/plan.json';prepare_output(root,p)
    text=r'''\documentclass[12pt,reqno]{amsart}
\usepackage{math-review}
\input{../generated/conventions.tex}
\title{Synthetic build fixture}\date{}
\begin{document}\maketitle
\section{Main Results}
\begin{theorem}\label{thm:x}\input{../generated/statements/N-main.tex}\end{theorem}
\section{Key Mathematical Ingredients}
Let $x$ be real.
\begin{definition}\label{def:x}\input{../generated/statements/N-def.tex}\end{definition}
\section{Connecting the Ingredients}
\begin{proof}Multiplication gives $0\cdot0=0$.\end{proof}
'''
    if two_pages:text+='\\newpage\nThis second page exists to test the actual PDF page count, not a length quota.\n'
    text+='\\end{document}\n';(p.parent/'manuscript/main.tex').write_text(text)

def plan(root,oid='mini',profile='minimal',question='N-q',principal='N-main'):
    sid=freeze_snapshot(root)['artifacts']['snapshot_id']
    create_plan(root,oid,sid,profile=profile,questions=[question],principals=[principal])
    return root/f'outputs/{oid}/plan.json'


class Contracts(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.root=fixture(self.base/'project')
    def tearDown(self):self.tmp.cleanup()
    def code(self,code,func,*a,**kw):
        with self.assertRaises(SurveyError) as cm:func(*a,**kw)
        self.assertEqual(cm.exception.diagnostic['code'],code)
    def test_removed_commands_are_unavailable(self):
        for args in [('migrate',), ('import-v2',), ('kb', 'format', str(self.root))]:
            p=subprocess.run([sys.executable,str(SCRIPTS/'survey.py'),*args,'--json'],capture_output=True,text=True)
            self.assertEqual(p.returncode,2,p.stdout)
            self.assertIn('CLI_ARGUMENT_INVALID',p.stdout)
    def test_installer_excludes_retired_resources(self):
        archive=self.base/'current.zip';package(SKILL,archive)
        with zipfile.ZipFile(archive) as z:
            names=z.namelist()
        for name in names:
            self.assertFalse(any(part in name for part in ('/legacy/','/registries/','/migration.py','/compatibility.py','/adapters.py','/create_project.py','/project-manifest-template.json')))
            self.assertFalse('/templates/part' in name)
    def test_T01_zero_outputs(self):
        self.assertEqual(validate_knowledge(self.root)['status'],'VALID');self.assertFalse((self.root/'outputs').exists())
    def test_T02_unused_nodes(self):
        putnode(self.root,'N-unused','example',questions=());self.assertEqual(len(inventory(self.root).nodes),4)
    def test_T03_identical_freeze_reuse(self):
        a=freeze_snapshot(self.root);p=self.root/a['artifacts']['manifest'];stamp=p.stat().st_mtime_ns
        b=freeze_snapshot(self.root);self.assertEqual(a['artifacts']['snapshot_id'],b['artifacts']['snapshot_id']);self.assertEqual(b['status'],'REUSED');self.assertEqual(stamp,p.stat().st_mtime_ns)
    def test_T04_tamper_frozen_bytes(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];p=self.root/f'snapshots/{sid}/files/scope.md';p.write_bytes(p.read_bytes()+b'X')
        self.code('SNAPSHOT_TAMPERED',load_snapshot,self.root,sid)
    def test_T05_changed_hypothesis_new_snapshot(self):
        a=freeze_snapshot(self.root)['artifacts']['snapshot_id'];p=self.root/'knowledge/nodes/N-main.md';old=p.read_bytes();p.write_bytes(old.replace(b'x=0',b'x=1'))
        b=freeze_snapshot(self.root)['artifacts']['snapshot_id'];self.assertNotEqual(a,b);self.assertEqual((self.root/f'snapshots/{a}/files/knowledge/nodes/N-main.md').read_bytes(),old)
    def test_T06_missing_node_and_source(self):
        p=self.root/'knowledge/nodes/N-main.md';old=p.read_bytes();p.write_bytes(old.replace(b'N-def',b'N-missing'));self.code('UNKNOWN_REFERENCE',inventory,self.root)
        p.write_bytes(old.replace(b'S-test',b'S-missing'));self.code('UNKNOWN_REFERENCE',inventory,self.root)
    def test_T07_dependency_cycle_path(self):
        putnode(self.root,'N-def','definition',r'$x\in\mathbb R$.',[('N-main','proof_input')])
        with self.assertRaises(SurveyError) as c:inventory(self.root)
        self.assertEqual(c.exception.diagnostic['code'],'DEPENDENCY_CYCLE');self.assertIn('N-main',str(c.exception));self.assertIn('N-def',str(c.exception))
    def test_T08_navigation_loop_allowed(self):
        p=self.root/'knowledge/nodes/N-main.md';n=load_node(p);n.meta['links'].append({'target':'N-method','relation':'explained_by'});p.write_bytes(node_bytes(n.meta,n.body))
        putnode(self.root,'N-method','mechanism',links=[('N-main','explains')]);self.assertEqual(len(inventory(self.root).nodes),4)
    def test_T10_generated_condition_tamper(self):
        p=plan(self.root);prepare_output(self.root,p);f=p.parent/'generated/statements/N-main.tex';f.write_bytes(f.read_bytes().replace(b'x=0',b'x=1'));self.code('CANONICAL_STATEMENT_CHANGED',verify_generated,self.root,load_plan(p))
    def test_T12_locator_version_conflict(self):
        p=self.root/'knowledge/nodes/N-main.md';n=load_node(p);n.meta['sources'][0]['version']='Different journal theorem numbering';p.write_bytes(node_bytes(n.meta,n.body));self.code('SOURCE_VERSION_CONFLICT',inventory,self.root)
    def test_T20_interrupted_snapshot_atomic_retry(self):
        import survey_core.snapshots as mod
        original=mod.atomic_bytes;count=0
        def failed(p,b):
            nonlocal count
            count+=1
            if count==2:raise OSError('Injected write interruption')
            original(p,b)
        with patch.object(mod,'atomic_bytes',failed):
            with self.assertRaises(OSError):freeze_snapshot(self.root)
        self.assertEqual(list((self.root/'snapshots').glob('KB-*')),[]);self.assertEqual(list((self.root/'snapshots').glob('.pending-*')),[])
        self.assertEqual(freeze_snapshot(self.root)['status'],'FROZEN')
    def test_T24_cache_delete_and_relocation(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];index_knowledge(self.root);shutil.rmtree(self.root/'.cache');moved=self.base/'moved';self.root.rename(moved);index_knowledge(moved)
        self.assertEqual(freeze_snapshot(moved)['artifacts']['snapshot_id'],sid);self.assertEqual(verify_snapshot(moved,sid)['status'],'VERIFIED')
    def test_H01_default_minimal_integrated(self):
        p=load_plan(plan(self.root));self.assertEqual((p['profile'],p['view']),('minimal','integrated'))
    def test_H03_duplicate_json_and_unknown_schema(self):
        p=self.root/'project.json';raw=p.read_text();p.write_text(raw.replace('"schema_version": "2.0.0"','"schema_version": "2.0.0", "schema_version": "2.0.0"'));self.code('DUPLICATE_JSON_KEY',inventory,self.root)
        p.write_text(raw.replace('2.0.0','99.0.0'));self.code('SCHEMA_UNSUPPORTED',inventory,self.root)
    def test_H04_unsafe_relative_and_symlink(self):
        p=self.root/'project.json';s=read_json(p);s['scope_file']='../outside.md';write_json(p,s);self.code('UNSAFE_PATH',inventory,self.root)
    def test_H21_actual_symlink_rejected_when_available(self):
        link=self.root/'scope.md';link.unlink()
        try:
            link.symlink_to(self.base/'project-scope.md')
        except OSError as exc:
            import errno
            if getattr(exc,'winerror',None)==1314 or exc.errno in {errno.EPERM,errno.EACCES}:
                self.skipTest('OS does not permit creating symlinks; real symlink rejection must run in a capable CI job')
            raise
        self.code('UNSAFE_PATH',inventory,self.root)
    def test_H05_writer_lock_refuses_second_writer(self):
        with writer(self.root):self.code('WRITER_LOCKED',freeze_snapshot,self.root)
    def test_H06_canonical_CRLF_not_normalized(self):
        p=self.root/'knowledge/nodes/N-main.md';p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'));n=load_node(p);self.assertEqual(n.statement,r'For $x\in\mathbb R$, $x=0$ implies $x^2=0$.'.encode())
        pp=plan(self.root);prepare_output(self.root,pp);self.assertEqual((pp.parent/'generated/statements/N-main.tex').read_bytes(),n.statement)
    def test_H10_foreign_snapshot_not_accepted(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];v=read_json(self.root/'project.json');v['project_id']='foreign';write_json(self.root/'project.json',v);self.code('SNAPSHOT_PROJECT_MISMATCH',load_snapshot,self.root,sid)
    def test_H15_extra_frozen_file_is_tampering(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];(self.root/f'snapshots/{sid}/files/extra.txt').write_text('x');self.code('SNAPSHOT_TAMPERED',load_snapshot,self.root,sid)
    def test_H19_bibliography_does_not_treat_arxiv_prefix_as_year(self):
        from survey_core.exports import export_bibliography
        p=self.root/'knowledge/sources/S-test.json';v=read_json(p)
        v['version']='arXiv:1904.12221v1 (2019-04-27)';write_json(p,v)
        bib=export_bibliography(inventory(self.root),{'N-main'}).decode()
        self.assertIn('year = {2019}',bib);self.assertNotIn('year = {1904}',bib)
        v['version']='arXiv:1904.12221v1';write_json(p,v)
        self.assertNotIn('year = ',export_bibliography(inventory(self.root),{'N-main'}).decode())
    def test_H20_pending_boundary_is_not_a_scaffold(self):
        p=plan(self.root);authored_toy(self.root)
        main=p.parent/'manuscript/main.tex';raw=main.read_text()
        main.write_text(raw.replace(r'\end{document}',r'The broader proof remains pending and is not used here.\end{document}'))
        self.assertNotIn('MANUSCRIPT_INCOMPLETE',{e['code'] for e in validate_structure(self.root,'mini')['errors']})
        main.write_text(raw.replace(r'\end{document}',r'TODO: write this proof.\end{document}'))
        self.assertIn('MANUSCRIPT_INCOMPLETE',{e['code'] for e in validate_structure(self.root,'mini')['errors']})

if __name__=="__main__":unittest.main()
