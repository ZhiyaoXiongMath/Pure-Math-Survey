"""r4 executable policy regressions; all reviews are synthetic gate fixtures.

Passing these tests does not certify mathematics, authorship or PDF reading.
"""
import copy
import re
import unittest

import test_vnext as v
from test_v2 import putnode, read_json, write_json, SKILL
from survey_core.exports import prepare_output, validate_structure, output_inputs
from survey_core.profiles import (POLICY, OUTPUT_SCHEMA, MINIMAL_SECTIONS,
    UNDERSTANDING_READINGS, VIEW_TASKS, review_scope_template, semantic_profile_errors, validate_plan_contract)
from survey_core.reviews import load_review, knowledge_scope_errors, check_review_bindings
from survey_core.release import assess_release, package_output
from survey_core.knowledge import inventory


class R4Policy(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext(); self.t.setUp()

    def tearDown(self):
        self.t.tearDown()

    def codes(self, oid='new'):
        return {e['code'] for e in validate_structure(self.t.root, oid)['errors']}


    def test_exact_three_sections_all_principals_and_single_canonical_imports(self):
        putnode(self.t.root, 'N-second', 'result', r'For $x\in\mathbb R$, $x^2\geq0$.',
                [('N-def', 'uses_definition')], source=True, status='established')
        coverage = read_json(self.t.root/'knowledge/coverage.json')
        coverage['questions'][0]['answer_nodes'].append('N-second')
        write_json(self.t.root/'knowledge/coverage.json', coverage)
        v.synthetic_policy_reviews(self.t.root)
        p, plan = self.t.authored()
        body = (p.parent/'manuscript/main.tex').read_text()
        report = validate_structure(self.t.root, 'new')
        self.assertEqual(report['errors'], [])
        secs = report['artifacts']['tex_inventory']['sections']
        self.assertEqual([s['title'] for s in secs if not s['starred']], MINIMAL_SECTIONS)
        for key in ('N-main', 'N-second', 'N-def'):
            self.assertEqual(body.count('../generated/statements/'+key+'.tex'), 1)
        first = body.index(r'\section{Key Mathematical Ingredients}')
        for key in ('N-main', 'N-second'):
            self.assertLess(body.index('../generated/statements/'+key+'.tex'), first)
        # authored replaces the scaffold outline, so inspect a separate prepare.
        p2, _ = self.t.make(oid='outline'); prepare_output(self.t.root, p2)
        design = (p2.parent/'outline.md').read_text()
        self.assertIn('complete ALL principals in Main Results', design)
        self.assertNotIn('three-section layout is an explicit design choice', design)

    def test_missing_extra_wrong_order_and_wrong_title_are_rejected(self):
        p, _ = self.t.authored(); main = p.parent/'manuscript/main.tex'; original = main.read_text()
        cases = {
            'missing': original.replace(r'\section{Key Mathematical Ingredients}', ''),
            'extra': original.replace(r'\end{document}', r'\section{Fourth problem}Extra.\end{document}'),
            'order': original.replace('Key Mathematical Ingredients', 'TEMP').replace('Connecting the Ingredients', 'Key Mathematical Ingredients').replace('TEMP', 'Connecting the Ingredients'),
            'title': original.replace('Main Results', 'Main Theorems'),
        }
        for name, text in cases.items():
            with self.subTest(name=name):
                main.write_text(text)
                self.assertIn('MINIMAL_THREE_SECTIONS_REQUIRED', self.codes())

    def test_each_principal_must_appear_in_first_section(self):
        p, _ = self.t.authored(); main = p.parent/'manuscript/main.tex'; original = main.read_text()
        begin = original.index(r'\begin{theorem}'); end = original.index(r'\end{theorem}', begin)+len(r'\end{theorem}')
        result = original[begin:end]; without = original[:begin]+original[end:]
        for title in MINIMAL_SECTIONS[1:]:
            with self.subTest(section=title):
                main.write_text(without.replace(r'\section{'+title+'}', r'\section{'+title+'}\n'+result))
                self.assertIn('MINIMAL_PRINCIPAL_NOT_FIRST', self.codes())

    def test_subsections_reference_heading_and_exact_imports_pass(self):
        p, _ = self.t.authored(); main = p.parent/'manuscript/main.tex'
        text = main.read_text().replace(r'\section{Key Mathematical Ingredients}',
            r'\section{Key Mathematical Ingredients}\subsection{A consumed identity}')
        text = text.replace(r'\bibliographystyle{plain}', r'\section*{References}\bibliographystyle{plain}')
        main.write_text(text)
        self.assertEqual(self.codes(), set())

    def test_extra_unnumbered_body_appendix_and_numbering_escape_are_rejected(self):
        p, _ = self.t.authored(); main = p.parent/'manuscript/main.tex'; original = main.read_text()
        for command, code in [(r'\section*{A fourth mathematical problem}', 'MINIMAL_EXTRA_BODY_SECTION'),
                              (r'\appendix', 'MINIMAL_NUMBERING_UNSUPPORTED'),
                              (r'\setcounter{secnumdepth}{0}', 'MINIMAL_NUMBERING_UNSUPPORTED'),
                              (r'\renewcommand{\thesection}{}', 'MINIMAL_NUMBERING_UNSUPPORTED')]:
            with self.subTest(command=command):
                main.write_text(original.replace(r'\end{document}', command+r'\end{document}'))
                self.assertIn(code, self.codes())



    def test_four_modes_five_views_prepare_current_openings_and_keep_selection(self):
        for profile in ('minimal', 'thematic', 'lecture', 'paper'):
            selection = None
            for view in VIEW_TASKS:
                with self.subTest(profile=profile, view=view):
                    p, plan = self.t.authored(profile, profile+'-'+view, view=view)
                    body = (p.parent/'manuscript/main.tex').read_text()
                    self.assertEqual(self.codes(plan['output_id']), set())
                    self.assertEqual(r'\begin{abstract}' in body, profile == 'paper')
                    chosen = {(s['node_id'], s['role']) for s in plan['selections']}
                    if selection is None: selection = chosen
                    self.assertEqual(chosen, selection)
                    scope = review_scope_template(plan)
                    self.assertTrue(set(UNDERSTANDING_READINGS) <= scope['mode_findings'].keys())
                    self.assertEqual(scope['view'], view)
                    if profile == 'paper':
                        self.assertTrue(plan['draft'])
                        self.assertIn('DRAFT\\_UNVERIFIED', body)

    def test_abstract_and_disguised_presection_summaries_are_rejected_for_three_modes(self):
        for profile in ('minimal', 'thematic', 'lecture'):
            p, _ = self.t.authored(profile, profile); main = p.parent/'manuscript/main.tex'; original = main.read_text()
            index = original.index(r'\section{')
            for prefix in (r'\begin{abstract}Summary.\end{abstract}',
                           r'\subsection*{Overview}Summary.', r'\paragraph{Preface}Summary.',
                           'Untitled summary before the first section.'):
                with self.subTest(profile=profile, prefix=prefix):
                    main.write_text(original[:index]+prefix+original[index:])
                    self.assertIn('PROFILE_PRESECTION_TEXT_FORBIDDEN', self.codes(profile))
                    if 'abstract' in prefix: self.assertIn('PROFILE_ABSTRACT_FORBIDDEN', self.codes(profile))

    def test_hidden_summary_text_is_not_visible_opening_and_in_section_positioning_passes(self):
        p, _ = self.t.authored(); main = p.parent/'manuscript/main.tex'; original = main.read_text()
        index = original.index(r'\section{')
        main.write_text(original[:index]+'% A comment, not an abstract.\n'+
            r'\iffalse Hidden summary.\fi'+original[index:])
        self.assertEqual(self.codes(), set())
        main.write_text(original.replace(r'\section{Main Results}', r'\section{Main Results}Brief problem positioning.'))
        self.assertEqual(self.codes(), set())

    def test_nonminimal_later_section_counts_and_topic_titles_are_editable(self):
        for profile in ('thematic', 'lecture', 'paper'):
            p, _ = self.t.authored(profile, profile); main = p.parent/'manuscript/main.tex'; original = main.read_text()
            headings = list(re.finditer(r'\\section\{[^{}]+\}', original))
            # Merge all later responsibilities into one mathematical section.
            text = original
            for heading in reversed(headings[2:]): text = text[:heading.start()]+text[heading.end():]
            if profile != 'paper': text = text.replace(headings[0].group(), r'\section{The actual topic and target}')
            main.write_text(text)
            self.assertEqual(self.codes(profile), set())
            main.write_text(text.replace(r'\end{document}', r'\section{Further exact consequences}Reason.\end{document}'))
            self.assertEqual(self.codes(profile), set())

    def test_nonminimal_first_section_duties_cannot_be_moved_to_later_section(self):
        for profile in ('thematic', 'lecture', 'paper'):
            p, _ = self.t.authored(profile, profile); main = p.parent/'manuscript/main.tex'; text = main.read_text()
            begin = text.index(r'\begin{theorem}'); end = text.index(r'\end{theorem}', begin)+len(r'\end{theorem}')
            result = text[begin:end]; text = text[:begin]+text[end:]
            headings = list(re.finditer(r'\\section\{[^{}]+\}', text)); second = headings[1]
            main.write_text(text[:second.end()]+result+text[second.end():])
            self.assertIn('PAPER_PRINCIPAL_NOT_FIRST' if profile == 'paper' else 'PROFILE_GOAL_NOT_FIRST', self.codes(profile))

    def test_paper_requires_abstract_and_introduction_and_remains_draft_only(self):
        p, plan = self.t.authored('paper'); main = p.parent/'manuscript/main.tex'; original = main.read_text()
        main.write_text(re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}', '', original, flags=re.S))
        self.assertIn('PAPER_ABSTRACT_REQUIRED', self.codes())
        main.write_text(original.replace(r'\section{Introduction}', r'\section{Results}'))
        self.assertIn('PAPER_INTRODUCTION_REQUIRED', self.codes())
        main.write_text(original)
        report = assess_release(self.t.root, 'new')
        codes = {e['code'] for e in report['errors']}
        self.assertTrue({'DRAFT_NOT_RELEASABLE', 'PAPER_ORIGINAL_CONTRIBUTION_MISSING'} <= codes)
        self.t.failcode('DRAFT_NOT_RELEASABLE', package_output, self.t.root, 'new', self.t.base/'forbidden.zip')



    def test_reprepare_keeps_authored_current_text_outline_style_and_stales_reviews(self):
        p, plan = self.t.authored(); review = self.t.sem(p, plan)
        paths = [p.parent/x for x in ('manuscript/main.tex', 'outline.md', 'manuscript/math-review.sty')]
        before = [x.read_bytes() for x in paths]
        prepare_output(self.t.root, p)
        self.assertEqual(before, [x.read_bytes() for x in paths])
        self.assertEqual(check_review_bindings(p.parent, review, output_inputs(p.parent)), [])
        paths[1].write_text('Changed reading design.\n')
        self.assertTrue(check_review_bindings(p.parent, review, output_inputs(p.parent)))



if __name__ == '__main__':
    unittest.main()
