"""Real file-operation regressions. Accepted review fixtures here are SYNTHETIC
mechanical gate inputs, not mathematical/source/visual acceptance evidence.
Actual mathematics and page observations are in the separate release example,
not this suite.
"""
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
from survey_core.readiness import assess_readiness
from survey_core.reviews import source_inputs,mathematical_inputs,coverage_inputs,review_template,load_review
from survey_core.migration import migrate_v1,node_bytes
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


def synthetic_reviews(root):
    inv=inventory(root)
    specs=[('source','S-test',source_inputs(inv,'S-test'))]
    specs += [('mathematical',k,mathematical_inputs(inv,k)) for k in inv.nodes]
    specs += [('coverage',k,coverage_inputs(inv,k)) for k,n in inv.nodes.items() if n.meta['kind']=='question']
    for kind,key,inputs in specs:
        r=review_template(root,kind,[key],inputs)
        r.update({'review_id':'SYNTHETIC-'+kind+'-'+key,'reviewer_mode':'author_reread','reviewed_at':now(),
                  'findings':['Synthetic accepted-state input for software gate testing only; not actual research acceptance.'],
                  'unchecked_items':[],'disposition':'accepted'})
        r['scope']['evidence_basis']='Synthetic software fixture; not a claim of an executed independent mathematical review.'
        write_json(root/f'evidence/reviews/{kind}-{key}.json',r)


def fixture(root,reviewed=False,second=False):
    scope=root.parent/(root.name+'-scope.md');scope.write_text('# Synthetic scope\n\nFor real x, verify x=0 implies x squared=0. No claim about mathematical survey quality.\n')
    init_project(root,'test-project',scope)
    state='established' if reviewed else 'unassessed'
    putnode(root,'N-q','question',questions=(),status=state)
    putnode(root,'N-def','definition',r'Let $x\in\mathbb R$.',status=state)
    putnode(root,'N-main','result',r'For $x\in\mathbb R$, $x=0$ implies $x^2=0$.',[('N-def','uses_definition')],source=True,status=state)
    (root/'evidence/source-checks').mkdir(parents=True)
    (root/'evidence/source-checks/test.md').write_text('# Synthetic source record\n\nA test harness material, not a literature-reading report.\n')
    (root/'knowledge/material.txt').write_text('Synthetic primary test material. For real x=0, x*x=0.\n')
    write_json(root/'knowledge/sources/S-test.json',{'schema_version':VERSION,'id':'S-test','kind':'primary','title':'Synthetic software fixture','authors':['Test harness'],
               'publication_status':'unpublished','identifiers':{'user_file':'Synthetic software test material'},'version':'Fixture v1',
               'access':{'state':'full_text_read' if reviewed else 'metadata_only','checked_at':now() if reviewed else None,
                         'material_sha256':file_hash(root,'knowledge/material.txt'),'local_path':'knowledge/material.txt','reading_note':'evidence/source-checks/test.md'}})
    qs=[{'question_id':'N-q','answer_nodes':['N-main'],'mechanism_nodes':[],'boundary_nodes':[],'gaps':[] if reviewed else ['Actual review not performed.'],
         'assessment':'adequate' if reviewed else 'pending','rationale':'A bounded synthetic software test; not a literature completeness claim.'}]
    if second:
        putnode(root,'N-q2','question',questions=(),status=state);putnode(root,'N-other','result',r'For $y\in\mathbb R$, $y^2\geq0$.',questions=('N-q2',),status=state)
        qs.append({'question_id':'N-q2','answer_nodes':['N-other'],'mechanism_nodes':[],'boundary_nodes':[],'gaps':[] if reviewed else ['Not reviewed.'],
                   'assessment':'adequate' if reviewed else 'pending','rationale':'Independent synthetic branch.'})
    write_json(root/'knowledge/coverage.json',{'schema_version':VERSION,'questions':qs})
    if reviewed:synthetic_reviews(root)
    return root


def plan(root,oid='mini',profile='minimal',question='N-q',principal='N-main',draft=True,pair=None):
    sid=freeze_snapshot(root)['artifacts']['snapshot_id']
    create_plan(root,oid,sid,profile=profile,questions=[question],principals=[principal],draft=draft,comparison_group=pair)
    path=root/f'outputs/{oid}/plan.json'
    # A synthetic gate fixture imports the trivial answer; actual exposition promises are tested separately.
    value=read_json(path)
    for selection in value['selections']:
        if selection['proof_treatment']=='sketch':selection['proof_treatment']='citation'
    write_json(path,value)
    return path


def authored_toy(root,oid='mini',two_pages=False):
    p=root/f'outputs/{oid}/plan.json';prepare_output(root,p,draft=True)
    text=r'''\documentclass[12pt,reqno]{amsart}
\usepackage{math-review}
\input{../generated/conventions.tex}
\title{Synthetic build fixture}\date{}
\begin{document}\maketitle
\noindent\textbf{DRAFT\_UNVERIFIED: software fixture, not a surveyed research claim.}
Let $x$ be real.
\begin{definition}\label{def:x}\input{../generated/statements/N-def.tex}\end{definition}
\begin{theorem}\label{thm:x}\input{../generated/statements/N-main.tex}\end{theorem}
\begin{proof}Multiplication gives $0\cdot0=0$.\end{proof}
'''
    if two_pages:text+='\\newpage\nThis second page exists to test the actual PDF page count, not a length quota.\n'
    text+='\\end{document}\n';(p.parent/'manuscript/main.tex').write_text(text)


class Contracts(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.root=fixture(self.base/'project')
    def tearDown(self):self.tmp.cleanup()
    def code(self,code,func,*a,**kw):
        with self.assertRaises(SurveyError) as cm:func(*a,**kw)
        self.assertEqual(cm.exception.diagnostic['code'],code)
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
    def test_T09_shared_exact_canonical(self):
        for oid,profile in [('mini','minimal'),('learn','lecture')]:prepare_output(self.root,plan(self.root,oid,profile),draft=True)
        a=self.root/'outputs/mini/generated/statements/N-main.tex';b=self.root/'outputs/learn/generated/statements/N-main.tex';self.assertEqual(a.read_bytes(),b.read_bytes());self.assertEqual(a.read_bytes(),load_node(self.root/'knowledge/nodes/N-main.md').statement)
    def test_T10_generated_condition_tamper(self):
        p=plan(self.root);prepare_output(self.root,p,True);f=p.parent/'generated/statements/N-main.tex';f.write_bytes(f.read_bytes().replace(b'x=0',b'x=1'));self.code('CANONICAL_STATEMENT_CHANGED',verify_generated,self.root,load_plan(p))
    def test_T11_impact_excludes_independent_output(self):
        other=fixture(self.base/'second',second=True)
        for oid,profile,q,ans in [('mini','minimal','N-q','N-main'),('learn','lecture','N-q','N-main'),('theme','thematic','N-q2','N-other')]:plan(other,oid,profile,q,ans)
        old=load_plan(other/'outputs/mini/plan.json')['snapshot_id'];p=other/'knowledge/nodes/N-def.md';p.write_bytes(p.read_bytes()+b'\nA changed definition input.\n');new=freeze_snapshot(other)['artifacts']['snapshot_id']
        r=diff_snapshots(other,old,new);self.assertEqual({x['output_id'] for x in r['artifacts']['affected_outputs']},{'mini','learn'})
    def test_T12_locator_version_conflict(self):
        p=self.root/'knowledge/nodes/N-main.md';n=load_node(p);n.meta['sources'][0]['version']='Different journal theorem numbering';p.write_bytes(node_bytes(n.meta,n.body));self.code('SOURCE_VERSION_CONFLICT',inventory,self.root)
    def test_T13_supplied_is_not_original_review(self):
        p=self.root/'knowledge/sources/S-test.json';s=read_json(p);s['kind']='supplied_manuscript';write_json(p,s)
        r=assess_readiness(self.root,plan(self.root));self.assertEqual(r['status'],'NEEDS_WORK');self.assertIn('SOURCE_REVIEW_MISSING',{x['code'] for x in r['errors']})
    def test_T14_accepted_stale_hash_rejected(self):
        r=fixture(self.base/'reviewed',True);p=r/'knowledge/nodes/N-main.md';p.write_bytes(p.read_bytes()+b'\nChanged conditions for re-review.\n');check=assess_readiness(r,plan(r,draft=False));self.assertIn('REVIEW_STALE',{x['code'] for x in check['errors']})
    def test_T15_separate_question_scopes(self):
        r=fixture(self.base/'reviewed',True,True)
        self.assertEqual(assess_readiness(r,plan(r,'one',draft=False))['status'],'READY')
        self.assertEqual(assess_readiness(r,plan(r,'two','thematic','N-q2','N-other',False))['status'],'READY')
    def test_T16_explicit_pair_mismatch(self):
        r=fixture(self.base/'second',second=True);plan(r,'one',pair='paired');self.code('PAIRED_CORE_MISMATCH',plan,r,'two','lecture','N-q2','N-other',True,'paired')
    def test_T17_actual_pdf_advisory_and_explicit_limit(self):
        p=plan(self.root);authored_toy(self.root,two_pages=True);b=build_output(self.root,'mini');self.assertEqual(b['artifacts']['pages'],2)
        obj=load_plan(p);obj['limits']['page_review_threshold']=1;write_json(p,obj);r=reading_budget(self.root,'mini');self.assertEqual(r['status'],'CHECKED');self.assertTrue(r['warnings']);self.assertFalse(r['errors'])
        obj['limits']['max_pages']=1;write_json(p,obj);r=reading_budget(self.root,'mini');self.assertEqual(r['status'],'NEEDS_WORK')
    def test_T18_inline_migration_missing_audits(self):
        old=self.base/'old';old.mkdir();raw=r'\begin{theorem}\label{a}Let $x=0$. Then $x^2=0$.\end{theorem}';(old/'main.tex').write_text(raw)
        new=self.base/'imported';migrate_v1(old,new);m=read_json(new/'MIGRATION_REPORT.json');self.assertEqual(m['node_candidates'],1);self.assertTrue(m['ambiguities']);self.assertEqual((new/'legacy/original/main.tex').read_text(),raw)
        self.assertTrue(list((new/'evidence/migration-diffs').glob('*.diff')));self.assertEqual(validate_knowledge(new)['status'],'VALID')
    def test_T19_legacy_PASS_never_promoted(self):
        old=self.base/'old';old.mkdir();(old/'main.tex').write_text(r'\begin{theorem}$0=0$.\end{theorem}');(old/'release-audit.csv').write_text('check,status,evidence\nmathematics,PASS,old claim\n')
        new=self.base/'new';migrate_v1(old,new);self.assertTrue(all(n.meta['mathematical_status']=='unassessed' for n in inventory(new).nodes.values()));self.assertFalse(list((new/'evidence/reviews').glob('*.json')))
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
    def test_T21_actual_archive_extraction_isolated_entry(self):
        z=self.base/'skill.zip';package(SKILL,z);self.assertGreater(verify_archive(z)['members'],120)
        dest=self.base/'unpacked'
        with zipfile.ZipFile(z) as archive:
            names=archive.namelist()
            self.assertFalse(any('/dhym-v6/' in n or '/dhym-compact/' in n for n in names))
            archive.extractall(dest)
        sample=dest/'pure-math-survey/assets/reference-samples/dhym-balanced'
        provenance=read_json(sample/'provenance.json')
        for name,record in provenance['files'].items():
            self.assertEqual(hashlib.sha256((sample/name).read_bytes()).hexdigest(),record['sha256'])
        entry=dest/'pure-math-survey/scripts/survey.py'
        p=subprocess.run([sys.executable,'-I',str(entry),'--json','--version'],capture_output=True,text=True,cwd=self.base);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['artifacts']['version'],'2.0.3')
        p=subprocess.run([sys.executable,'-I',str(entry.parent/'validate_assets.py'),'--json'],capture_output=True,text=True,cwd=self.base);self.assertEqual(p.returncode,0,p.stdout+p.stderr);self.assertEqual(json.loads(p.stdout)['profile_preparations_executed'],['minimal','thematic','lecture'])
    def test_T22_actual_current_and_frozen_style_builds(self):
        from build_checks import stage_balanced_sample,compile_one
        root=self.base/'styles';(root/'assets/templates').mkdir(parents=True);shutil.copytree(SKILL/'assets/reference-samples/dhym-balanced',root/'assets/reference-samples/dhym-balanced')
        original={p.name:p.read_bytes() for p in (root/'assets/reference-samples/dhym-balanced').iterdir()}
        current=(SKILL/'assets/templates/math-review.sty').read_bytes()+b'\n\\typeout{PMS-V2-CURRENT-STYLE-ONLY}\n';(root/'assets/templates/math-review.sty').write_bytes(current)
        seen={}
        for mode in ('current','frozen'):
            d=self.base/mode;entry=stage_balanced_sample(root,d,mode=mode);r=compile_one(d,entry.name,shutil.which('pdflatex'));self.assertEqual(r['status'],'PASS',r);seen[mode]=(d/(entry.stem+'.log')).read_text(errors='replace')
            self.assertEqual((d/'references.bib').read_bytes(),original['references.bib'])
            self.assertEqual((d/'dhym-survey-revised.bbl').read_bytes(),original['dhym-survey-revised.bbl'])
        self.assertIn('PMS-V2-CURRENT-STYLE-ONLY',seen['current']);self.assertNotIn('PMS-V2-CURRENT-STYLE-ONLY',seen['frozen'])
        self.assertEqual(original,{p.name:p.read_bytes() for p in (root/'assets/reference-samples/dhym-balanced').iterdir()})
    def test_balanced_staging_requires_supplied_bibliography(self):
        from build_checks import stage_balanced_sample
        root=self.base/'styles';sample=root/'assets/reference-samples/dhym-balanced'
        shutil.copytree(SKILL/'assets/reference-samples/dhym-balanced',sample)
        (sample/'dhym-survey-revised.bbl').unlink()
        destination=self.base/'missing-bibliography'
        with self.assertRaises(FileNotFoundError):stage_balanced_sample(root,destination,mode='frozen')
        self.assertFalse(destination.exists())
    def test_T23_draft_package_refused(self):
        p=plan(self.root);authored_toy(self.root);self.code('DRAFT_NOT_RELEASABLE',package_output,self.root,'mini',self.base/'forbidden.zip');self.assertFalse((self.base/'forbidden.zip').exists())
    def test_T24_cache_delete_and_relocation(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];index_knowledge(self.root);shutil.rmtree(self.root/'.cache');moved=self.base/'moved';self.root.rename(moved);index_knowledge(moved)
        self.assertEqual(freeze_snapshot(moved)['artifacts']['snapshot_id'],sid);self.assertEqual(verify_snapshot(moved,sid)['status'],'VERIFIED')
    def test_H01_default_minimal_integrated(self):
        p=load_plan(plan(self.root));self.assertEqual((p['profile'],p['view']),('minimal','integrated'))
    def test_H02_three_profiles_and_no_automatic_trio(self):
        p=plan(self.root);self.assertEqual(len(list((self.root/'outputs').iterdir())),1)
        for name in ('lecture','thematic'):plan(self.root,name,name)
        for p in (self.root/'outputs').glob('*/plan.json'):self.assertIn(prepare_output(self.root,p,True)['status'],{'DRAFT_PREPARED'})
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
        pp=plan(self.root);prepare_output(self.root,pp,True);self.assertEqual((pp.parent/'generated/statements/N-main.tex').read_bytes(),n.statement)
    def test_H07_review_template_never_accepts(self):
        inv=inventory(self.root);r=review_template(self.root,'mathematical',['N-main'],mathematical_inputs(inv,'N-main'));self.assertEqual(r['disposition'],'revise');self.assertIsNone(r['reviewed_at']);self.assertEqual(r['reviewer_mode'],'not_performed')
    def test_H08_legacy_dispatch_and_root_conflict(self):
        p=subprocess.run([sys.executable,str(SCRIPTS/'validate_project.py'),str(self.root),'--json'],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['status'],'VALID')
        write_json(self.root/'project-manifest.json',{});p=subprocess.run([sys.executable,str(SCRIPTS/'validate_project.py'),str(self.root),'--json'],capture_output=True,text=True);self.assertEqual(p.returncode,2);self.assertIn('MANIFEST_CONFLICT',p.stdout)
    def test_H09_future_review_date_invalid(self):
        r=fixture(self.base/'reviewed',True);p=r/'evidence/reviews/mathematical-N-main.json';v=read_json(p);v['reviewed_at']='2999-01-01';write_json(p,v);self.code('REVIEW_INVALID',load_review,p)
    def test_H10_foreign_snapshot_not_accepted(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];v=read_json(self.root/'project.json');v['project_id']='foreign';write_json(self.root/'project.json',v);self.code('SNAPSHOT_PROJECT_MISMATCH',load_snapshot,self.root,sid)
    def test_H11_complete_promise_needs_complete_obligation(self):
        p=plan(self.root);v=load_plan(p);next(x for x in v['selections'] if x['node_id']=='N-main')['proof_treatment']='complete';write_json(p,v);self.code('PROOF_OBLIGATION_UNMET',validate_plan,self.root,v)
    def test_H12_missing_pdf_cannot_be_visual_pass(self):
        p=plan(self.root);authored_toy(self.root);r=assess_release(self.root,'mini');self.assertIn('BUILD_FAILED',{x['code'] for x in r['errors']});self.assertEqual(r['status'],'NEEDS_WORK')
    def test_H13_actual_render_not_visual_review(self):
        p=plan(self.root);authored_toy(self.root);build_output(self.root,'mini');r=render_output(self.root,'mini');self.assertEqual(r['status'],'RENDERED_NOT_REVIEWED');check=assess_release(self.root,'mini');self.assertIn('VISUAL_REVIEW_INCOMPLETE',{x['code'] for x in check['errors']})
    def test_H14_interrupted_migration_is_atomic(self):
        old=self.base/'old';old.mkdir();(old/'main.tex').write_text(r'\begin{theorem}$0=0$.\end{theorem}');new=self.base/'new'
        import survey_core.migration as mod
        with patch.object(mod,'atomic_bytes',side_effect=OSError('Injected migration interruption')):
            with self.assertRaises(OSError):migrate_v1(old,new)
        self.assertFalse(new.exists());self.assertTrue((old/'main.tex').is_file());self.assertEqual(migrate_v1(old,new)['status'],'IMPORTED_UNVERIFIED')
    def test_H15_extra_frozen_file_is_tampering(self):
        sid=freeze_snapshot(self.root)['artifacts']['snapshot_id'];(self.root/f'snapshots/{sid}/files/extra.txt').write_text('x');self.code('SNAPSHOT_TAMPERED',load_snapshot,self.root,sid)
    def test_H16_nullable_source_hash_needs_scoped_evidence(self):
        r=fixture(self.base/'reviewed',True);p=r/'knowledge/sources/S-test.json';v=read_json(p);v['access']['local_path']=None;v['access']['material_sha256']=None;write_json(p,v);synthetic_reviews(r);c=assess_readiness(r,plan(r));self.assertIn('SOURCE_REVIEW_MISSING',{x['code'] for x in c['errors']})

    def test_H17_promised_sketch_cannot_be_ready_without_steps(self):
        r=fixture(self.base/'reviewed',True);p=plan(r,draft=False);v=read_json(p)
        next(x for x in v['selections'] if x['node_id']=='N-main')['proof_treatment']='sketch';write_json(p,v)
        check=assess_readiness(r,p);self.assertIn('PROOF_OBLIGATION_UNMET',{x['code'] for x in check['errors']})
    def test_H18_unresolved_source_versions_block_readiness(self):
        r=fixture(self.base/'reviewed',True);p=r/'knowledge/sources/S-test.json';v=read_json(p)
        v['version_conflicts']=['Candidate v1','Candidate journal'];write_json(p,v);synthetic_reviews(r)
        check=assess_readiness(r,plan(r,draft=False));self.assertIn('SOURCE_VERSION_CONFLICT',{x['code'] for x in check['errors']})

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

if __name__=='__main__':unittest.main(verbosity=2)
