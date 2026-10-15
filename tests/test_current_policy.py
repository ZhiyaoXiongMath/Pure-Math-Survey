"""Current r4 understanding and evidence contracts. All accepted fixtures are synthetic software inputs.

These tests neither certify mathematics nor simulate a real reader/PDF review.
"""
import copy
import json
import subprocess
import sys
import unittest

import test_vnext as v
from test_v2 import putnode, read_json, write_json, SCRIPTS, SurveyError
from survey_core.exports import prepare_output, validate_structure, output_inputs, verify_generated
from survey_core.exposition import check_exposition_design
from survey_core.models import load_plan
from survey_core.plans import consumption, validate_plan
from survey_core.profiles import (OUTPUT_SCHEMA, POLICY, UNDERSTANDING_READINGS,
    MINIMAL_SECTIONS, current, validate_plan_contract, review_scope_template, semantic_profile_errors)
from survey_core.release import assess_release, package_output
from survey_core.reviews import load_review, review_template, check_review_bindings, knowledge_scope_errors


class CurrentPolicy(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext()
        self.t.setUp()
        self.t.editorial_policy = POLICY

    def tearDown(self):
        self.t.tearDown()

    def test_only_current_output_pair_is_reported_and_supported(self):
        _, plan = self.t.make()
        self.assertTrue(current(plan))
        run = subprocess.run([sys.executable, str(SCRIPTS/'survey.py'), '--version', '--json'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)['artifacts']
        self.assertEqual((report['version'], report['schema_version'], report['output_schema_version']), ('2.1.0', '2.0.0', '2.2.0'))
        self.assertEqual(report['supported_output_contracts'], [{'schema_version': OUTPUT_SCHEMA, 'editorial_policy': POLICY}])

    def test_explicit_old_unknown_or_malformed_output_and_review_pairs_fail_without_mutation(self):
        p, plan = self.t.authored(); review = self.t.sem(p, plan)
        pairs = [('2.0.0', None), ('2.1.0', 'four-modes-2026-10-11-r2'),
                 (OUTPUT_SCHEMA, 'four-modes-2026-10-12-rc2'), (OUTPUT_SCHEMA, 'four-modes-2026-10-12-r3'),
                 (OUTPUT_SCHEMA, 'unknown'), (OUTPUT_SCHEMA, []), (OUTPUT_SCHEMA, {})]
        for schema, policy in pairs:
            with self.subTest(policy=policy):
                bad = copy.deepcopy(plan); bad.update(schema_version=schema, editorial_policy=policy)
                write_json(p, bad); before = p.read_bytes()
                with self.assertRaises(SurveyError): load_plan(p)
                with self.assertRaises(SurveyError): prepare_output(self.t.root, p)
                self.assertEqual(p.read_bytes(), before)
                record = copy.deepcopy(review); record['schema_version'] = schema
                record['scope']['editorial_policy'] = policy
                target = p.parent/'evidence/obsolete.json'; write_json(target, record); before = target.read_bytes()
                with self.assertRaises(SurveyError): load_review(target)
                self.assertEqual(target.read_bytes(), before)

    def test_recorded_cli_is_not_available(self):
        p, _ = self.t.authored()
        run = subprocess.run([sys.executable, str(SCRIPTS/'survey.py'), 'output', 'validate', str(self.t.root),
                              '--output', 'new', '--stage', 'release', '--policy', 'recorded', '--json'], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('CLI_ARGUMENT_INVALID', run.stdout)





    def test_current_review_template_requires_each_new_task_and_never_accepts(self):
        _, plan = self.t.make()
        scope = review_scope_template(plan)
        self.assertTrue(set(UNDERSTANDING_READINGS) <= scope['mode_findings'].keys())
        for name in UNDERSTANDING_READINGS:
            self.assertEqual(scope['mode_findings'][name],
                             {'outcome': 'not_performed', 'finding': '', 'locations': []})
        self.assertIn('results_first', scope['mode_findings'])

    def test_missing_or_unperformed_current_responsibility_remains_pending(self):
        p, plan = self.t.authored()
        review = self.t.sem(p, plan)
        self.assertEqual(semantic_profile_errors(p.parent, plan, review), [])
        for name in UNDERSTANDING_READINGS:
            for defect in ('missing', 'unperformed', 'empty'):
                with self.subTest(name=name, defect=defect):
                    bad = copy.deepcopy(review)
                    entry = bad['scope']['mode_findings'][name]
                    if defect == 'missing': del bad['scope']['mode_findings'][name]
                    elif defect == 'unperformed': entry['outcome'] = 'not_performed'
                    else: entry['finding'] = ''
                    self.assertIn('MODE_SEMANTIC_REVIEW_PENDING',
                                  {x['code'] for x in semantic_profile_errors(p.parent, plan, bad)})

    def test_all_new_findings_require_real_body_locations_even_if_accepted(self):
        p, plan = self.t.authored()
        review = self.t.sem(p, plan)
        for name in UNDERSTANDING_READINGS:
            with self.subTest(name=name):
                bad = copy.deepcopy(review)
                bad['scope']['mode_findings'][name]['locations'] = [
                    {'path': 'manuscript/main.tex', 'line_start': 1, 'line_end': 1}]
                self.assertTrue(semantic_profile_errors(p.parent, plan, bad))
                write_json(p.parent/'evidence/bad-body.json', bad)
                report = assess_release(self.t.root, plan['output_id'])
                self.assertIn('OUTPUT_SEMANTIC_REVIEW_PENDING', {e['code'] for e in report['errors']})



    def test_malformed_review_policies_fail_closed_without_typeerror(self):
        p, plan = self.t.authored(); original = self.t.sem(p, plan)
        for value in (None, [], {}, 7):
            bad = copy.deepcopy(original); bad['scope']['editorial_policy'] = value
            path = p.parent/'evidence/malformed.json'; write_json(path, bad)
            self.t.failcode('SCHEMA_UNSUPPORTED', load_review, path)
            with self.assertRaises(SurveyError):
                review_template(p.parent, 'output_semantic', ['new'], output_inputs(p.parent),
                                {'editorial_policy': value})






    def test_current_reprepare_preserves_authored_bytes_and_stales_changed_review(self):
        p, plan = self.t.authored(); review = self.t.sem(p, plan)
        files = [p.parent/x for x in ('manuscript/main.tex', 'manuscript/math-review.sty', 'outline.md')]
        before = [x.read_bytes() for x in files]
        prepare_output(self.t.root, p)
        self.assertEqual(before, [x.read_bytes() for x in files])
        files[2].write_text('A revised actual exposition design.\n')
        self.assertTrue(check_review_bindings(p.parent, review, output_inputs(p.parent)))


    def test_current_principal_tampering_and_paper_defaults_still_block(self):
        p, plan = self.t.authored()
        main = p.parent/'manuscript/main.tex'
        main.write_text(main.read_text().replace(r'\begin{theorem}', '').replace(r'\end{theorem}', ''))
        self.assertIn('PRINCIPAL_RESULT_ENVIRONMENT_MISSING',
                      {e['code'] for e in validate_structure(self.t.root, 'new')['errors']})
        (p.parent/'generated/statements/N-main.tex').write_text('Altered theorem')
        self.t.failcode('CANONICAL_STATEMENT_CHANGED', verify_generated, self.t.root, plan)
        p, paper = self.t.make('paper', 'paper-default', draft=False)
        self.assertTrue(paper['draft'])
        self.assertIn('PAPER_ORIGINAL_CONTRIBUTION_MISSING', self.t.eligibility(paper))


class CurrentKnowledgeReview(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext(); self.t.setUp()
        self.t.editorial_policy = POLICY
        from survey_core.knowledge import inventory
        self.inv = inventory(self.t.root)
        self.review_path = self.t.root/'evidence/reviews/new-coverage-N-q.json'
        self.review = load_review(self.review_path)
        self.review['scope']['editorial_policy'] = POLICY
        write_json(self.review_path, self.review)

    def tearDown(self):
        self.t.tearDown()

    def test_existing_findings_and_inputs_validate_without_any_output(self):
        self.assertEqual(knowledge_scope_errors(self.inv, 'N-q', self.review), [])
        self.assertFalse((self.t.root/'outputs').exists())

    def test_each_required_task_needs_actual_scoped_finding(self):
        for task in UNDERSTANDING_READINGS:
            with self.subTest(task=task):
                bad = copy.deepcopy(self.review)
                bad['findings'] = [x for x in bad['findings'] if not x.startswith(task+':')]
                self.assertIn('KNOWLEDGE_REVIEW_PENDING',
                              {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', bad)})


    def test_bad_or_missing_subsection_is_refused(self):
        for target in ('knowledge/nodes/N-q.md#not-a-section',
                       'knowledge/missing.md#fast', '../outside.md#fast',
                       'https://example.invalid/route.md#fast', 'knowledge/nodes/N-q.md'):
            with self.subTest(target=target):
                bad = copy.deepcopy(self.review)
                bad['findings'][0] = UNDERSTANDING_READINGS[0] + ': ' + v.SYNTH + ' [Location](' + target + ')'
                self.assertIn('KNOWLEDGE_REVIEW_LOCATION_INVALID',
                              {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', bad)})

    def test_route_file_requires_actual_input_hash_and_stales_on_edit(self):
        from survey_core.common import file_hash
        route = self.t.root/'knowledge/route.md'
        route.write_text('# Fast route\n\nSynthetic route content, not mathematical evidence.\n')
        review = copy.deepcopy(self.review)
        review['findings'] = [task+': '+v.SYNTH+' [Route](knowledge/route.md#fast-route)' for task in UNDERSTANDING_READINGS]
        self.assertIn('REVIEW_SCOPE_INSUFFICIENT',
                      {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', review)})
        review['inputs'].append({'path': 'knowledge/route.md', 'sha256': file_hash(self.t.root, 'knowledge/route.md')})
        self.assertEqual(knowledge_scope_errors(self.inv, 'N-q', review), [])
        route.write_text('# Fast route\n\nChanged synthetic route.\n')
        self.assertIn('REVIEW_STALE', {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', review)})

    def test_hidden_or_literal_anchors_never_satisfy_actual_readiness(self):
        from survey_core.common import file_hash
        from survey_core.readiness import assess_readiness
        cases = {
            'visible heading': ('# Visible\n\n## Actual section\n\nSynthetic derivation.\n', True),
            'visible explicit anchor': ('# Visible\n\n<a id="actual-section"></a>\n\nSynthetic derivation.\n', True),
            'literal comment before visible heading': ('`<!--` is literal code.\n\n## Actual section\n\nSynthetic derivation.\n', True),
            'heading only': ('## Actual section\n', False),
            'anchor only': ('<a id="actual-section"></a>\n', False),
            'comment-only body': ('## Actual section\n\n<!-- Hidden derivation. -->\n', False),
            'code-only body': ('## Actual section\n\n```python\nprint("hidden")\n```\n', False),
            'descendant content': ('## Actual section\n\n### Calculation\n\nFor $x=0$, $x+x=0$.\n', True),
            'displayed mathematics': ('## Actual section\n\n\\[x+x=0.\\]\n', True),
            'canonical and explanatory text': ('## Actual section\n\n```latex\nx+x=0\n```\n\nThis is the canonical identity used below.\n', True),
            'next peer is not content': ('## Actual section\n\n## Other section\n\nOther computation.\n', False),
            'indented-only body': ('## Actual section\n\n    hidden computation\n', False),
            'inline-code-only body': ('## Actual section\n\n`hidden computation`\n', False),
            'reference definition only': ('## Actual section\n\n[unused]: https://example.invalid "No rendered body"\n', False),
            'multiline reference definition': ('## Actual section\n\n[unused]: https://example.invalid\n  "No rendered body"\n', False),
            'split reference destination': ('## Actual section\n\n[unused]:\n  https://example.invalid "No rendered body"\n', False),
            'paragraph after reference and blank': ('## Actual section\n\n[unused]: https://example.invalid\n\n"Actual visible explanation."\n', True),
            'quoted tilde code only': ('## Actual section\n\n> ~~~python\n> print(0)\n> ~~~\n', False),
            'list tilde code only': ('## Actual section\n\n- ~~~python\n  print(0)\n  ~~~\n', False),
            'ordered tilde code only': ('## Actual section\n\n1. ~~~python\n   print(0)\n   ~~~\n', False),
            'list backtick code only': ('## Actual section\n\n- ```python\n  print(0)\n  ```\n', False),
            'ordered backtick code only': ('## Actual section\n\n1. ```python\n   print(0)\n   ```\n', False),
            'list actual paragraph': ('## Actual section\n\n- Set $x=0$ and substitute into $x+x$.\n', True),
            'ordered actual paragraph': ('## Actual section\n\n1. Set $x=0$ and substitute into $x+x$.\n', True),
            'horizontal rule only': ('## Actual section\n\n___\n', False),
            'spaced horizontal rule': ('## Actual section\n\n_ _ _\n', False),
            'reference then real paragraph': ('## Actual section\n\n[unused]: https://example.invalid\n\nActual computation: $x=0$.\n', True),
            'metadata frontmatter': ('---\ntitle: |\n  ## Actual section\n---\n\n# Visible\n', False),
            'HTML comment': ('# Visible\n\n<!--\n## Actual section\n\nHidden text.\n-->\n', False),
            'inline code': ('# Visible\n\n`<a id="actual-section">` is code.\n', False),
            'two-backtick code': ('# Visible\n\n``<a id="actual-section">``\n', False),
            'multiline code anchor': ('# Visible\n\n`code\n<a id="actual-section">\nend`\n', False),
            'multiline code heading': ('# Visible\n\n`code\n## Actual section\nend`\n', False),
            'indented code': ('# Visible\n\n    <a id="actual-section">\n', False),
            'tab-indented code': ('# Visible\n\n\t<a id="actual-section">\n', False),
            'fenced code': ('# Visible\n\n```md\n## Actual section\n```\n', False),
            'raw HTML': ('<div hidden>\n<div>\n</div>\n## Actual section\n</div>\n', False),
            'same-line nested HTML': ('<div hidden><div>\n</div>\n## Actual section\n</div>\n', False),
            'HTML nonvoid self-close': ('<div hidden/>\n## Actual section\n</div>\n', False),
            'escaped anchor': ('# Visible\n\n\\<a id="actual-section">\n', False),
            'after closing comment same line': ('<!-- hidden\n-->## Actual section\n', False),
        }
        route = self.t.root/'knowledge/route.md'
        for number, (name, (text, accepted)) in enumerate(cases.items()):
            with self.subTest(name=name):
                route.write_text(text)
                review = copy.deepcopy(self.review)
                review['findings'] = [task+': '+v.SYNTH+' [Section](knowledge/route.md#actual-section)' for task in UNDERSTANDING_READINGS]
                review['inputs'].append({'path': 'knowledge/route.md', 'sha256': file_hash(self.t.root, 'knowledge/route.md')})
                write_json(self.review_path, review)
                _, plan = self.t.make(oid='anchor-'+str(number), draft=False)
                report = assess_readiness(self.t.root, plan)
                self.assertEqual(report['status'], 'READY' if accepted else 'NEEDS_WORK')
                if not accepted:
                    self.assertIn('KNOWLEDGE_REVIEW_LOCATION_INVALID', {e['code'] for e in report['errors']})

    def test_visible_heading_code_and_comment_duplicate_keep_correct_slug(self):
        from survey_core.reviews import markdown_anchors
        text = '<!--\n## The `actual` section\n-->\n\n## The `actual` section\n'
        self.assertEqual(markdown_anchors(text), {'the-actual-section'})

    def test_missing_nodes_or_checks_are_not_accepted(self):
        for field, value, expected in [('checks', [], 'KNOWLEDGE_REVIEW_PENDING'),
                                      ('checks', {}, 'KNOWLEDGE_REVIEW_PENDING'),
                                      ('node_ids', ['N-q'], 'KNOWLEDGE_REVIEW_SCOPE_INSUFFICIENT'),
                                      ('node_ids', [None], 'KNOWLEDGE_REVIEW_SCOPE_INSUFFICIENT')]:
            bad = copy.deepcopy(self.review); bad['scope'][field] = value
            self.assertIn(expected, {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', bad)})

    def test_cli_coverage_template_is_pending_and_creates_no_manuscript(self):
        run = subprocess.run([sys.executable, str(SCRIPTS/'survey.py'), 'review', 'template',
                              str(self.t.root), '--kind', 'coverage', '--id', 'N-q', '--json'],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        review = json.loads(run.stdout)['artifacts']['review']
        self.assertEqual(review['scope']['editorial_policy'], POLICY)
        self.assertEqual(set(review['scope']['checks']), set(UNDERSTANDING_READINGS))
        self.assertEqual(review['disposition'], 'revise')
        self.assertEqual(review['reviewer_mode'], 'not_performed')
        self.assertFalse((self.t.root/'outputs').exists())


if __name__ == '__main__':
    unittest.main()
