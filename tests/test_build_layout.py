"""Optional builder parameters preserve defaults and reject TeX injection."""
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/pure-math-survey/scripts'))
from survey_core.build import emergency_stretch_argument
from survey_core.common import SurveyError
spec=importlib.util.spec_from_file_location('standalone_rebuild',ROOT/'skills/pure-math-survey/assets/rebuild/rebuild.py')
standalone=importlib.util.module_from_spec(spec);spec.loader.exec_module(standalone)

class OptionalLineBreaking(unittest.TestCase):
    def test_original_default_and_two_builders_share_one_parameter_contract(self):
        self.assertEqual(emergency_stretch_argument(None),('main.tex',{}))
        self.assertEqual(standalone.emergency_stretch_argument(None),('main.tex',{}))
        for value in (0.5,2,2.0,10,1e-6,5e-324):
            with self.subTest(value=value):
                self.assertEqual(emergency_stretch_argument(value),standalone.emergency_stretch_argument(value))
                self.assertEqual(emergency_stretch_argument(value)[1]['emergency_stretch_em'],value)

    def test_tiny_parameter_is_plain_decimal_for_tex(self):
        argument,_=emergency_stretch_argument(1e-6)
        self.assertIn(r'\emergencystretch=0.000001em',argument)
        self.assertNotIn('1e-',argument)

    def test_nonfinite_out_of_range_or_tex_text_cannot_enter_command(self):
        for value in (-1,0,10.1,float('nan'),float('inf'),True,'2em',r'2\input{other}'):
            for helper,error in ((emergency_stretch_argument,SurveyError),(standalone.emergency_stretch_argument,ValueError)):
                with self.subTest(value=value,helper=helper.__module__),self.assertRaises(error):helper(value)



class MinimalLayout(unittest.TestCase):
    def setUp(self):
        import tempfile
        from test_v2 import fixture,plan,authored_toy
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.root=fixture(self.base/'project');self.plan=plan(self.root);authored_toy(self.root,two_pages=True)
        self.out=self.plan.parent;self.main=self.out/'manuscript/main.tex'
    def tearDown(self):self.tmp.cleanup()

    def test_actual_main_reference_boundary_and_overlength_failure_retain_evidence(self):
        from test_v2 import build_output,read_json
        from survey_core.build import check_build
        result=build_output(self.root,'mini')
        self.assertEqual((result['artifacts']['main_pages'],result['artifacts']['total_pages']),(2,3))
        report=read_json(self.out/'build/build-report.json')
        self.assertEqual(report['layout_measurements']['main_pages'],2)
        self.assertTrue(all(v>=20*72.27/25.4 for v in report['layout_measurements']['margins_pt'].values()))
        self.assertEqual(read_json(self.root/'run.json')['main_pages'],2)
        self.assertEqual(check_build(self.out)[1],[])
        previous=(self.out/'build/main.pdf').read_bytes()
        text=self.main.read_text(encoding='utf-8')
        self.main.write_text(text.replace(r'\pmsmainend',('\n'+r'\newpage Explicit extra main page.'+'\n')*5+r'\pmsmainend'),encoding='utf-8')
        with self.assertRaises(SurveyError):build_output(self.root,'mini')
        failed=read_json(self.out/'build/build-report.json')
        self.assertEqual((failed['status'],failed['main_pages'],failed['total_pages']),('FAILED',7,8))
        self.assertTrue(failed['layout_errors']);self.assertTrue((self.out/'build/main.log').is_file())
        self.assertEqual(read_json(self.root/'run.json')['status'],'failed')
        self.assertTrue(any(p.read_bytes()==previous for p in (self.out/'history').rglob('main.pdf')))

    def test_compression_and_false_boundary_reject_before_build_writes(self):
        from test_v2 import build_output
        from test_minimal_runtime import tree
        original=self.main.read_text(encoding='utf-8')
        variants=[original.replace('[11pt,reqno]','[10pt,reqno]'),
            original.replace(r'\input{architecture_graph.tex}',r'\scalebox{.5}{\input{architecture_graph.tex}}'),
            original.replace(r'\pmsmainend',r'\pmsmainend Hidden main text.'),
            original.replace(r'\pmsmainend',r'\setcounter{page}{1}\pmsmainend')]
        for text in variants:
            self.main.write_text(text,encoding='utf-8');before=tree(self.root)
            with self.assertRaises(SurveyError):build_output(self.root,'mini')
            self.assertEqual(tree(self.root),before)

if __name__=='__main__':unittest.main()
