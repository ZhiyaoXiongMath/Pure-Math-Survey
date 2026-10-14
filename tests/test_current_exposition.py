"""Current hostile-input exposition gates; synthetic accepted fixtures only."""
from __future__ import annotations
import copy
from pathlib import Path
import tempfile
import unittest

import test_vnext as vnext
SYNTH = vnext.SYNTH
from test_v2 import read_json, write_json, now, putnode
from survey_core.tex import validate_locations
from survey_core.exports import prepare_output, validate_structure
from survey_core.profiles import semantic_profile_errors, outline
from survey_core.readiness import assess_readiness, assess_eligibility
from survey_core.reviews import mathematical_inputs, review_template, check_review_bindings
from survey_core.knowledge import inventory


def codes(errors):
    return {e['code'] for e in errors}


class Locations(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        (self.out / 'manuscript').mkdir()
    def tearDown(self):
        self.tmp.cleanup()
    def check(self, text, line, filename='main.tex'):
        (self.out / 'manuscript/main.tex').write_text(text, encoding='utf-8')
        return validate_locations(self.out, [dict(path='manuscript/'+filename,
            line_start=line, line_end=line)])
    def test_LOC01_comment_cannot_locate_proof(self):
        errors = self.check('% not a proof\n\\begin{document}\nActual proof.\n\\end{document}\n', 1)
        self.assertIn('REVIEW_LOCATION_NOT_IN_BODY', codes(errors))
    def test_LOC02_preamble_and_after_document(self):
        text = 'Preamble text\n\\begin{document}\nActual proof.\n\\end{document}\nAfterward\n'
        for line in (1, 5):
            with self.subTest(line=line):
                self.assertIn('REVIEW_LOCATION_NOT_IN_BODY', codes(self.check(text,line)))
    def test_LOC03_unreachable_file(self):
        (self.out/'manuscript/orphan.tex').write_text('A plausible but unconsumed proof.\n')
        self.assertIn('REVIEW_LOCATION_UNREACHABLE', codes(self.check(
            '\\begin{document}\nActual proof.\n\\end{document}\n', 1, 'orphan.tex')))
    def test_LOC04_definitions_and_inactive_branch(self):
        text = '\\begin{document}\n\\newcommand{\\unused}{Hidden proof}\n\\iffalse\nHidden\n\\else\nActual proof.\n\\fi\n\\end{document}\n'
        for line in (2,4):
            with self.subTest(line=line):
                self.assertIn('REVIEW_LOCATION_EMPTY', codes(self.check(text,line)))
        self.assertEqual(self.check(text,6), [])
    def test_LOC06_empty_label_environment(self):
        text = '\\begin{document}\n\\label{empty}\n\\begin{equation}\n\\end{equation}\nReal proof.\n\\end{document}\n'
        for line in (2,3,4):
            with self.subTest(line=line):
                self.assertIn('REVIEW_LOCATION_EMPTY', codes(self.check(text,line)))
    def test_LOC07_display_and_nested_literal_positive(self):
        (self.out/'manuscript/part.tex').write_text('\\[x^2\\geq0\\]\n')
        text = '\\begin{document}\n\\input{part.tex}\n\\end{document}\n'
        self.assertEqual(self.check(text,1,'part.tex'), [])
    def test_LOC10_invalid_member_not_masked_by_valid_member(self):
        text = '\\begin{document}\nReal proof.\n% only comment\n\\end{document}\n'
        self.check(text,2)
        errors = validate_locations(self.out,[dict(path='manuscript/main.tex',line_start=n,line_end=n) for n in (2,3)])
        self.assertIn('REVIEW_LOCATION_EMPTY', codes(errors))


class Hardening(unittest.TestCase):
    def setUp(self):
        self.fixture = vnext.VNext(); self.fixture.setUp(); self.fixture.editorial_policy=vnext.POLICY
    def tearDown(self):
        self.fixture.tearDown()
    def test_VIEW02_same_facts_different_reader_tasks(self):
        t=self.fixture; rows=[]
        for view in ('methods','boundaries'):
            p,v=t.make(oid=view,view=view); prepare_output(t.root,p)
            rows.append((v,(p.parent/'outline.md').read_text()))
        a,b=rows
        self.assertEqual({s['node_id'] for s in a[0]['selections']},{s['node_id'] for s in b[0]['selections']})
        self.assertNotEqual(a[0]['reader_goals'],b[0]['reader_goals'])
        self.assertNotEqual([s['reason'] for s in a[0]['selections']],[s['reason'] for s in b[0]['selections']])
        self.assertNotEqual(a[1],b[1])
    def test_PRIOR01_isolated_relation_is_not_comparison(self):
        t=self.fixture; t.isolated_comparison=True; p,v=t.paper(); v['draft']=False
        errors=assess_eligibility(t.root,v)['errors']
        self.assertIn('PAPER_COMPARISON_ENDPOINT_MISSING', codes(errors))
    def test_PRIOR09_endpoint_changes_stale_comparison_reading(self):
        t=self.fixture
        putnode(t.root,'N-compare','relation','Synthetic relation.',links=[('N-main','compares_with')],status='established')
        inv=inventory(t.root)
        r=review_template(t.root,'mathematical',['N-compare'],mathematical_inputs(inv,'N-compare'))
        path=t.root/'knowledge/nodes/N-main.md';path.write_bytes(path.read_bytes().replace(b'x=0',b'x=1'))
        self.assertIn('REVIEW_STALE',codes(check_review_bindings(t.root,r,mathematical_inputs(inventory(t.root),'N-compare'))))
    def test_PRIOR06_wrong_version_and_locator_not_accepted(self):
        t=self.fixture;p,v=t.paper();prepare_output(t.root,p);r=t.sem(p,v)
        entry=r['scope']['contribution_reviews']['N-main']
        entry.update(outcome='accepted',finding=SYNTH,locations=r['scope']['principal_locations']['N-main'],
            provenance_check=SYNTH,authorization_check=SYNTH,actual_difference=SYNTH,proof_closure=SYNTH,remaining_caveats=SYNTH,
            prior_art_searches=[dict(searched_at=now(),query=SYNTH,outcome=SYNTH,checked_source_ids=['S-test'])],
            prior_result_checks=[dict(prior_result_id='N-prior',source_id='S-test',version='WRONG VERSION',
                                     locator='Wrong page',outcome='accepted',finding=SYNTH)])
        self.assertIn('PAPER_PRIOR_SUPPORT_UNVERIFIED',codes(semantic_profile_errors(p.parent,v,r)))
    def test_DESIGN01_default_outline_is_not_completed_design(self):
        t=self.fixture;p,v=t.authored(draft=False)
        (p.parent/'outline.md').write_text(outline(v,[s['node_id'] for s in v['selections']]))
        self.assertEqual(assess_readiness(t.root,v)['status'],'READY')
        self.assertIn('EXPOSITION_DESIGN_INCOMPLETE',codes(validate_structure(t.root,v['output_id'])['errors']))
    def test_DESIGN07_first_prepare_reports_scaffold(self):
        t=self.fixture;p,v=t.make(draft=False)
        result=prepare_output(t.root,p)
        self.assertIn(result['status'],('PREPARED','DRAFT_PREPARED'))
        self.assertEqual(result['artifacts'].get('exposition_design',{}).get('status'),'NEEDS_WORK')


if __name__=='__main__':
    unittest.main()
