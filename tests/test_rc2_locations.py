"""Remaining location probes use actual body computations in synthetic fixtures."""
import unittest
import test_rc2 as rc
import test_vnext as v
from test_v2 import write_json, SurveyError
from survey_core.tex import validate_locations
from survey_core.release import semantic_scope_errors, assess_release, package_output


class Locations(unittest.TestCase):
    setUp=rc.Locations.setUp
    tearDown=rc.Locations.tearDown
    check=rc.Locations.check
    def test_LOC05_shared_preamble_body_and_nested_input(self):
        (self.out/'manuscript/shared.tex').write_text('The actual computation is $0+0=0$.\n')
        (self.out/'manuscript/outer.tex').write_text('\\input{shared.tex}\n')
        text='\\input{shared.tex}\n\\begin{document}\n\\input{outer.tex}\n\\end{document}\n'
        self.assertEqual(self.check(text,1,'shared.tex'),[])
        self.assertIn('REVIEW_LOCATION_NOT_IN_BODY',rc.codes(self.check(text,1)))
    def test_LOC06_empty_input_and_style_not_proof(self):
        (self.out/'manuscript/empty.tex').write_text('% no computation\n')
        self.assertIn('REVIEW_LOCATION_EMPTY',rc.codes(self.check('\\begin{document}\n\\input{empty.tex}\n\\end{document}\n',2)))
        (self.out/'manuscript/style.sty').write_text('text\n')
        self.assertIn('REVIEW_LOCATION_INVALID',rc.codes(self.check('\\begin{document}\nProof\n\\end{document}\n',1,'style.sty')))
    def test_LOC07_range_with_comments_and_actual_content(self):
        self.check('\\begin{document}\n% comment\n\n$x^2=0$\n\\end{document}\n',4)
        self.assertEqual(validate_locations(self.out,[dict(path='manuscript/main.tex',line_start=2,line_end=4)]),[])
    def test_LOC08_crlf_percent_and_backslash_parity(self):
        path=self.out/'manuscript/main.tex'
        path.write_bytes(b'\\begin{document}\r\n\\% is a percent sign.\r\n\\\\% comment\r\n\\\\\\% visible percent\r\n\\end{document}\r\n')
        for line in (2,4):
            self.assertEqual(validate_locations(self.out,[dict(path='manuscript/main.tex',line_start=line,line_end=line)]),[])
        self.assertIn('REVIEW_LOCATION_EMPTY',rc.codes(validate_locations(self.out,[dict(path='manuscript/main.tex',line_start=3,line_end=3)])))
    def test_LOC11_else_nested_and_unsupported_dynamic(self):
        text='\\begin{document}\n\\iffalse\nHidden\n\\else\n\\iftrue\n$x=0$\n\\else\nHidden\n\\fi\n\\fi\n\\end{document}\n'
        self.assertEqual(self.check(text,6),[])
        self.assertIn('REVIEW_LOCATION_EMPTY',rc.codes(self.check(text,8)))
        for dynamic in (r'\input{\filename}',r'\ifnum1=1 Visible\else Hidden\fi'):
            self.assertIn('REVIEW_LOCATION_UNVERIFIABLE',rc.codes(self.check('\\begin{document}\n'+dynamic+'\n\\end{document}\n',2)))


class ReleaseLocations(unittest.TestCase):
    def setUp(self):self.t=v.VNext();self.t.setUp()
    def tearDown(self):self.t.tearDown()
    def test_LOC09_canonical_location_cannot_use_other_body(self):
        p,plan=self.t.authored();review=self.t.sem(p,plan)
        review['scope']['principal_locations']['N-main']=review['scope']['proof_locations']['N-main']
        errors=semantic_scope_errors(p.parent,plan,['N-main','N-def','N-q'],review)
        self.assertIn('REVIEW_LOCATION_INVALID',rc.codes(errors))
        self.assertTrue(any('canonical body input' in e['message'] for e in errors))
    def test_LOC12_freshly_bound_accepted_invalid_ordinary_locations_block_package(self):
        p,plan=self.t.authored(draft=False);main=p.parent/'manuscript/main.tex'
        main.write_text(main.read_text().replace(r'\end{document}','% location bait\n'+r'\end{document}'))
        review=self.t.sem(p,plan);line=main.read_text().splitlines().index('% location bait')+1
        bad=[dict(path='manuscript/main.tex',line_start=line,line_end=line)]
        review['scope']['proof_locations']['N-main']=bad
        for entry in review['scope']['mode_findings'].values():entry['locations']=bad
        write_json(p.parent/'evidence/hostile.json',review)
        self.assertIn('REVIEW_LOCATION_EMPTY',rc.codes(assess_release(self.t.root,plan['output_id'])['errors']))
        with self.assertRaises(SurveyError):package_output(self.t.root,plan['output_id'],self.t.base/'must-not-exist.zip')
        self.assertFalse((self.t.base/'must-not-exist.zip').exists())
