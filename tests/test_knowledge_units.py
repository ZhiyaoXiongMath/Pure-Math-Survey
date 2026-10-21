"""Reusable lean fixture: concept closure, joint/alternative routes and live updates."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import unicodedata
from unittest.mock import patch
from test_v2 import fixture,putnode,plan,authored_toy,load_node,node_bytes,read_json,write_json,SurveyError
from survey_core.common import VERSION,all_files,safe
from survey_core.knowledge import inventory,index_knowledge,validate_knowledge
from survey_core.plans import create_plan,consumption
from survey_core.exports import prepare_output,verify_generated,export_unit
from survey_core.history import verify_history


def lean_fixture(root):
    fixture(root)
    putnode(root,'N-notation','definition',r'Write $\mathbb R$ for the real numbers.',source=True)
    node=load_node(root/'knowledge/nodes/N-def.md');node.meta['definition_refs']=['N-notation'];node.meta['source_status']='extracted'
    (root/'knowledge/nodes/N-def.md').write_bytes(node_bytes(node.meta,node.body))
    for key in ('N-a','N-b','N-c'):
        putnode(root,key,'result',r'$0\cdot 0=0$.',source=True,definitions=['N-def'],role='ingredient',status='stated')
    putnode(root,'N-independent','result',r'$1+1=2$.',role='context')
    route={'id':'R-combine','premise_sets':[{'nodes':['N-a','N-b'],'additional_inputs':['H: a common real parameter']},
        {'nodes':['N-c'],'additional_inputs':['K: direct substitution']}],'target':'N-main',
        'mapping':'Use the joint pair under H, or the direct argument under K.',
        'source_locator':{'source_id':'S-test','locator':'Synthetic alternatives, paragraph 2'},'status':'extracted'}
    write_json(root/'knowledge/routes.json',{'schema_version':VERSION,'routes':[route]})
    return root


def tree(root):return {p:safe(root,p,True).read_bytes() for p in all_files(root)}


class LeanKnowledge(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.root=lean_fixture(self.base/'project')
    def tearDown(self):self.tmp.cleanup()
    def code(self,code,fn,*args):
        with self.assertRaises(SurveyError) as e:fn(*args)
        self.assertEqual(e.exception.diagnostic['code'],code)

    def test_kb_only_null_importance_and_short_index(self):
        self.assertEqual(validate_knowledge(self.root)['status'],'VALID');index_knowledge(self.root)
        self.assertIsNone(inventory(self.root).nodes['N-main'].meta['importance']['level'])
        paths=all_files(self.root)
        for excluded in ('outputs/','snapshots/','overview.md','discovery.md','coverage.json','reviews/'):
            self.assertFalse(any(excluded in p for p in paths),excluded)
        self.assertLess(len((self.root/'knowledge/index.md').read_text(encoding='utf-8').splitlines()),20)
        self.assertEqual(read_json(self.root/'run.json')['output_paths'],[])

    def test_joint_and_alternative_inputs_remain_grouped_and_branch_independent(self):
        p=plan(self.root);prepare_output(self.root,p)
        value=read_json(p);self.assertNotIn('snapshot_id',value)
        self.assertEqual(consumption(inventory(self.root),value),{'N-main','N-a','N-b','N-c','N-def','N-notation'})
        routes=read_json(p.parent/'generated/routes.json')['routes']
        self.assertEqual(routes,read_json(self.root/'knowledge/routes.json')['routes'])
        self.assertEqual(routes[0]['premise_sets'][0]['nodes'],['N-a','N-b'])
        self.assertEqual(routes[0]['premise_sets'][1],{'nodes':['N-c'],'additional_inputs':['K: direct substitution']})
        self.assertIn(b' OR ',(p.parent/'generated/routes.tex').read_bytes())
        self.assertNotIn('N-independent',verify_generated(self.root,value)['consumed_nodes'])

    def test_standalone_export_includes_recursive_definitions_conventions_sources_and_exact_bytes(self):
        putnode(self.root,'N-main','result',r'For $x$ as in Definition~\ref{node:N-def}, $x=0$ implies $x^2=0$.',
                definitions=['N-def'],source=True)
        destination=self.base/'unit';report=export_unit(self.root,'N-main',destination)
        self.assertEqual(set(report['artifacts']['included_nodes']),{'N-main','N-def','N-notation'})
        for key in ('N-main','N-def','N-notation'):
            self.assertEqual((destination/f'generated/statements/{key}.tex').read_bytes(),load_node(self.root/f'knowledge/nodes/{key}.md').statement)
        self.assertEqual((destination/'generated/conventions.tex').read_bytes(),(self.root/'knowledge/conventions.tex').read_bytes())
        self.assertTrue((destination/'materials/knowledge/sources/S-test.json').is_file())
        self.assertIn('Synthetic fixture paragraph 1',(destination/'unit.tex').read_text(encoding='utf-8'))
        self.assertFalse((destination/'materials/knowledge/material.txt').exists())
        # Resolve the definition cross-reference through real stable TeX/BibTeX passes.
        auxiliary=[]
        for command in (['pdflatex','-halt-on-error','-interaction=nonstopmode','-no-shell-escape','main.tex'],['bibtex','main'],
                        ['pdflatex','-halt-on-error','-interaction=nonstopmode','-no-shell-escape','main.tex'],
                        ['pdflatex','-halt-on-error','-interaction=nonstopmode','-no-shell-escape','main.tex']):
            proc=subprocess.run(command,cwd=destination,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            self.assertEqual(proc.returncode,0,proc.stdout.decode('utf-8',errors='replace')[-3000:])
            if command[0]=='pdflatex':auxiliary.append((destination/'main.aux').read_bytes())
        self.assertEqual(auxiliary[-2],auxiliary[-1],'Cross-references did not stabilize')
        from build_checks import log_issues
        self.assertEqual(log_issues((destination/'main.log').read_text(encoding='utf-8',errors='replace')),{})
        pdf_text=subprocess.run(['pdftotext','-layout','main.pdf','-'],cwd=destination,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(pdf_text.returncode,0,pdf_text.stderr)
        visible=' '.join(unicodedata.normalize('NFKC',pdf_text.stdout).split())
        definition=re.search(r'Definition (\d+(?:\.\d+)*)\. Let x',visible)
        self.assertIsNotNone(definition,visible)
        self.assertIn('For x as in Definition '+definition[1]+',',visible)
        self.assertNotIn('??',visible)
        self.assertTrue((destination/'main.pdf').read_bytes().startswith(b'%PDF-'))
        before=tree(self.root)
        self.code('DESTINATION_EXISTS',export_unit,self.root,'N-main',destination)
        self.code('UNSAFE_PATH',export_unit,self.root,'N-main',self.root/'intruding-export')
        self.assertEqual(tree(self.root),before)
        dangling=self.base/'dangling-unit'
        original=Path.is_symlink
        with patch.object(Path,'is_symlink',lambda p: True if p==dangling else original(p)):
            self.code('UNSAFE_PATH',export_unit,self.root,'N-main',dangling)
        self.assertFalse(dangling.exists());self.assertEqual(tree(self.root),before)

    def test_missing_reference_and_cycles_reject_without_writes(self):
        path=self.root/'knowledge/routes.json';original=read_json(path)
        for field,value,code in [('nodes',['N-missing'],'UNKNOWN_REFERENCE'),('nodes',['N-main'],'DEPENDENCY_CYCLE')]:
            obj=read_json(path);obj['routes'][0]['premise_sets'][0][field]=value;write_json(path,obj);before=tree(self.root)
            self.code(code,index_knowledge,self.root);self.assertEqual(tree(self.root),before);write_json(path,original)
        node_path=self.root/'knowledge/nodes/N-main.md';node=load_node(node_path);node.meta['definition_refs']=['N-absent'];node_path.write_bytes(node_bytes(node.meta,node.body))
        self.code('UNKNOWN_REFERENCE',inventory,self.root)

    def test_method_without_formal_interface_is_not_a_route_conclusion(self):
        putnode(self.root,'N-method','method',role='bridge')
        path=self.root/'knowledge/routes.json';obj=read_json(path);obj['routes'][0]['target']='N-method';write_json(path,obj)
        self.code('METHOD_NOT_RESULT',inventory,self.root)
        putnode(self.root,'N-method','method',r'If $x=0$, substitution gives $x^2=0$.',role='bridge')
        self.assertEqual(inventory(self.root).nodes['N-method'].meta['kind'],'method')
        obj['routes'][0]['status']='unresolved';obj['routes'][0]['source_locator']=None;write_json(path,obj)
        create_plan(self.root,'method',principals=['N-method']);p=self.root/'outputs/method/plan.json';prepare_output(self.root,p)
        self.assertIn(b'unresolved: no asserted implication',(p.parent/'generated/routes.tex').read_bytes())
        self.assertEqual(read_json(self.root/'run.json')['status'],'incomplete')

    def test_live_update_preserves_author_text_graph_layout_and_prior_output_bytes(self):
        p=plan(self.root);prepare_output(self.root,p);out=p.parent
        main=out/'manuscript/main.tex';main.write_bytes(main.read_bytes()+b'\n% Author introduction and connections\n')
        graph=out/'manuscript/architecture_graph.tex';graph.write_bytes(b'% Author-chosen coordinates and grouping.\n')
        (out/'build').mkdir();(out/'build/old-delivery.pdf').write_bytes(b'%PDF- synthetic preservation marker')
        old={k:safe(out,k,True).read_bytes() for k in ('manuscript/main.tex','manuscript/architecture_graph.tex','generated/statements/N-main.tex','build/old-delivery.pdf')}
        node=self.root/'knowledge/nodes/N-main.md';node.write_bytes(node.read_bytes().replace(b'x^2=0',b'x x=0'))
        prepare_output(self.root,p)
        self.assertEqual(main.read_bytes(),old['manuscript/main.tex']);self.assertEqual(graph.read_bytes(),old['manuscript/architecture_graph.tex'])
        self.assertEqual((out/'generated/statements/N-main.tex').read_bytes(),load_node(node).statement)
        histories=list((out/'history/preparation').glob('H-*/files'));self.assertEqual(len(histories),1)
        for name,data in old.items():self.assertEqual((histories[0]/name).read_bytes(),data)
        self.assertEqual(verify_history(self.root,'mini')['status'],'VERIFIED')

    def test_interrupted_prepare_replacement_restores_both_derived_trees(self):
        p=plan(self.root);prepare_output(self.root,p);out=p.parent
        before={k:v for k,v in tree(out).items() if k.startswith(('generated/','materials/'))}
        original=Path.rename
        def fail(path,target):
            if path.name=='materials' and path.parent.name.startswith('.prepare-'):raise OSError('Injected second rename failure')
            return original(path,target)
        with patch.object(Path,'rename',fail):
            with self.assertRaises(OSError):prepare_output(self.root,p)
        after={k:v for k,v in tree(out).items() if k.startswith(('generated/','materials/'))}
        self.assertEqual(before,after);verify_generated(self.root,read_json(p))

    def test_version_string_edit_does_not_migrate_old_containers_or_nodes(self):
        write_json(self.root/'knowledge/coverage.json',{'schema_version':VERSION,'questions':[]})
        before=tree(self.root);self.code('LEGACY_PROJECT_UNSUPPORTED',index_knowledge,self.root);self.assertEqual(tree(self.root),before)
        (self.root/'knowledge/coverage.json').unlink()
        path=self.root/'knowledge/nodes/N-main.md';node=load_node(path);node.meta['links']=[];path.write_bytes(node_bytes(node.meta,node.body))
        before=tree(self.root);self.code('CONTRACT_INVALID',index_knowledge,self.root);self.assertEqual(tree(self.root),before)

if __name__=='__main__':unittest.main()
