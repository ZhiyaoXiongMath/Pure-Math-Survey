"""Retained literal TeX safety without review records or review-location validators."""
from pathlib import Path
import tempfile
import unittest
from test_v2 import fixture,plan,authored_toy,validate_structure,SurveyError
from survey_core.tex import inspect_tex


class LiteralTeX(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=fixture(Path(self.tmp.name)/'project')
        self.path=plan(self.root);authored_toy(self.root);self.out=self.path.parent
        self.main=self.out/'manuscript/main.tex';self.original=self.main.read_text(encoding='utf-8')
    def tearDown(self):self.tmp.cleanup()
    def codes(self):return {e['code'] for e in validate_structure(self.root,'mini')['errors']}
    def test_canonical_inside_false_branch_or_uncalled_macro_is_not_visible(self):
        token=r'\input{../generated/statements/N-main.tex}'
        for hidden in (r'\iffalse '+token+r'\fi',r'\newcommand{\unused}{'+token+'}', '% '+token+'\n'):
            self.main.write_text(self.original.replace(token,hidden),encoding='utf-8')
            self.assertIn('CANONICAL_STATEMENT_MISSING',self.codes())
    def test_dynamic_or_hidden_execution_is_refused(self):
        for command in (r'\input{\filename}',r'\ifnum1=1 visible\fi',r'\newcommand{\hidden}{\setbox0=\vbox{hidden}}\hidden'):
            self.main.write_text(self.original.replace(r'\end{document}',command+r'\end{document}'),encoding='utf-8')
            try: scan=inspect_tex(self.out)
            except SurveyError as error: self.assertEqual(error.diagnostic['code'],'TEX_INPUT_UNSUPPORTED')
            else: self.assertTrue(scan.errors)
    def test_nested_literal_inputs_keep_exact_canonical_owner(self):
        token=r'\input{../generated/statements/N-main.tex}'
        (self.out/'manuscript/nested.tex').write_text(token+'\n',encoding='utf-8')
        self.main.write_text(self.original.replace(token,r'\input{nested.tex}'),encoding='utf-8')
        scan=inspect_tex(self.out)
        self.assertIn('generated/statements/N-main.tex',scan.body_inputs)
        self.assertTrue(any(x['path']=='manuscript/nested.tex' and x['input']=='generated/statements/N-main.tex' for x in scan.locations))
        self.assertFalse(self.codes())
    def test_after_document_canonical_is_not_body_input(self):
        token=r'\input{../generated/statements/N-main.tex}'
        self.main.write_text(self.original.replace(token,'')+'\n'+token,encoding='utf-8')
        self.assertIn('CANONICAL_STATEMENT_MISSING',self.codes())
    def test_duplicates_and_descriptive_headings_are_mechanically_diagnosed(self):
        self.main.write_text(self.original.replace(r'\label{def:x}',r'\label{thm:x}'),encoding='utf-8')
        self.assertIn('DUPLICATE_LABEL',self.codes())
        self.main.write_text(self.original.replace(r'\begin{theorem}',r'\begin{theorem}[A name]'),encoding='utf-8')
        self.assertIn('STATEMENT_DESCRIPTIVE_TITLE',self.codes())
    def test_unsafe_or_cyclic_input_is_refused(self):
        for token in (r'\input{../../scope.md}',r'\input{main.tex}'):
            self.main.write_text(self.original.replace(r'\end{document}',token+r'\end{document}'),encoding='utf-8')
            with self.assertRaises(SurveyError):inspect_tex(self.out)

if __name__=='__main__':unittest.main()
