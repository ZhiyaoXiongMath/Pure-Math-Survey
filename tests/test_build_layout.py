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
        for value in (0.5,2,2.0,10):
            with self.subTest(value=value):
                self.assertEqual(emergency_stretch_argument(value),standalone.emergency_stretch_argument(value))
                self.assertEqual(emergency_stretch_argument(value)[1]['emergency_stretch_em'],value)

    def test_nonfinite_out_of_range_or_tex_text_cannot_enter_command(self):
        for value in (-1,0,10.1,float('nan'),float('inf'),True,'2em',r'2\input{other}'):
            for helper,error in ((emergency_stretch_argument,SurveyError),(standalone.emergency_stretch_argument,ValueError)):
                with self.subTest(value=value,helper=helper.__module__),self.assertRaises(error):helper(value)

if __name__=='__main__':unittest.main()
