"""r3 policy contracts. All accepted fixtures are synthetic software inputs.

These tests neither certify mathematics nor simulate a real reader/PDF review.
"""
import copy
import json
import subprocess
import sys
import unittest

import test_vnext as v
from test_v2 import putnode, plan as legacy_plan, read_json, write_json, SCRIPTS, SurveyError
from survey_core.exports import prepare_output, validate_structure, output_inputs, verify_generated
from survey_core.exposition import check_exposition_design
from survey_core.models import load_plan
from survey_core.plans import consumption, validate_plan
from survey_core.profiles import (OUTPUT_SCHEMA, POLICY, RC1_SCHEMA, RC1_POLICY,
    RC2_POLICY, LEGACY_POLICY, R3_READINGS, MINIMAL_SECTIONS, current,
    four_modes, rc2_capabilities, strict_old_minimal, validate_plan_contract,
    review_scope_template, semantic_profile_errors)
from survey_core.release import assess_release, package_output
from survey_core.reviews import load_review, review_template, check_review_bindings, knowledge_scope_errors


class R3Policy(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext()
        self.t.setUp()

    def tearDown(self):
        self.t.tearDown()

    def test_default_plan_and_cli_report_explicit_contract_pairs(self):
        p, plan = self.t.make()
        self.assertEqual((plan['schema_version'], plan['editorial_policy']), (OUTPUT_SCHEMA, POLICY))
        run = subprocess.run([sys.executable, str(SCRIPTS/'survey.py'), '--version', '--json'],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        reported = json.loads(run.stdout)['artifacts']
        self.assertEqual(reported['version'], '2.1.0')
        self.assertEqual(reported['schema_version'], '2.0.0')
        self.assertEqual(reported['editorial_policy'], POLICY)
        pairs = {(x['schema_version'], x['editorial_policy']) for x in reported['supported_output_contracts']}
        self.assertEqual(pairs, {('2.0.0', LEGACY_POLICY), (RC1_SCHEMA, RC1_POLICY),
                                (OUTPUT_SCHEMA, RC2_POLICY), (OUTPUT_SCHEMA, POLICY)})

    def test_twenty_r3_interfaces_keep_mode_view_and_core_selection(self):
        from survey_core.profiles import VIEW_TASKS, MODE_READINGS
        for profile in ('minimal', 'thematic', 'lecture', 'paper'):
            selections = None
            for view in VIEW_TASKS:
                with self.subTest(profile=profile, view=view):
                    p, plan = self.t.make(profile, profile+'-'+view, view=view)
                    prepare_output(self.t.root, p)
                    self.assertEqual(plan['editorial_policy'], POLICY)
                    actual = {(s['node_id'], s['role']) for s in plan['selections']}
                    if selections is None: selections = actual
                    self.assertEqual(actual, selections)
                    scope = review_scope_template(plan)
                    self.assertTrue(set(R3_READINGS + MODE_READINGS[profile]) <= scope['mode_findings'].keys())
                    self.assertEqual(scope['view'], view)
                    self.assertIn(VIEW_TASKS[view], (p.parent/'outline.md').read_text())
                    if profile == 'paper': self.assertTrue(plan['draft'])
        self.assertEqual(len(list((self.t.root/'outputs').iterdir())), 20)

    def test_current_and_capabilities_are_separate_for_all_recorded_policies(self):
        _, plan = self.t.make()
        for schema, policy, modes, rc2, strict, latest in [
                ('2.0.0', None, False, False, False, False),
                (RC1_SCHEMA, RC1_POLICY, True, False, True, False),
                (OUTPUT_SCHEMA, RC2_POLICY, True, True, True, False),
                (OUTPUT_SCHEMA, POLICY, True, True, False, True)]:
            with self.subTest(policy=policy):
                case = copy.deepcopy(plan)
                case['schema_version'] = schema
                if policy is None:
                    case.pop('editorial_policy'); case.pop('contributions')
                else:
                    case['editorial_policy'] = policy
                validate_plan_contract(case)
                self.assertEqual((four_modes(case), rc2_capabilities(case), strict_old_minimal(case), current(case)),
                                 (modes, rc2, strict, latest))

    def test_unknown_mixed_and_malformed_policy_pairs_fail_with_diagnostics(self):
        _, plan = self.t.make()
        for schema, policy in [(RC1_SCHEMA, POLICY), ('2.2.0', RC1_POLICY),
                               ('2.2.0', 'unknown'), ('2.2.0', None),
                               ('2.2.0', []), ('2.2.0', {}), ([], POLICY), ({}, POLICY)]:
            with self.subTest(schema=schema, policy=policy):
                bad = copy.deepcopy(plan)
                bad.update(schema_version=schema, editorial_policy=policy)
                with self.assertRaises(SurveyError):
                    validate_plan_contract(bad)

    def test_r3_review_template_requires_each_new_task_and_never_accepts(self):
        _, plan = self.t.make()
        scope = review_scope_template(plan)
        self.assertTrue(set(R3_READINGS) <= scope['mode_findings'].keys())
        for name in R3_READINGS:
            self.assertEqual(scope['mode_findings'][name],
                             {'outcome': 'not_performed', 'finding': '', 'locations': []})
        self.assertIn('results_first', scope['mode_findings'])

    def test_missing_or_unperformed_r3_responsibility_remains_pending(self):
        p, plan = self.t.authored()
        review = self.t.sem(p, plan)
        self.assertEqual(semantic_profile_errors(p.parent, plan, review), [])
        for name in R3_READINGS:
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
        for name in R3_READINGS:
            with self.subTest(name=name):
                bad = copy.deepcopy(review)
                bad['scope']['mode_findings'][name]['locations'] = [
                    {'path': 'manuscript/main.tex', 'line_start': 1, 'line_end': 1}]
                self.assertTrue(semantic_profile_errors(p.parent, plan, bad))
                write_json(p.parent/'evidence/bad-body.json', bad)
                report = assess_release(self.t.root, plan['output_id'])
                self.assertIn('OUTPUT_SEMANTIC_REVIEW_PENDING', {e['code'] for e in report['errors']})

    def test_old_accepted_review_never_supplies_new_r3_responsibilities(self):
        p, plan = self.t.authored()
        review = self.t.sem(p, plan)
        review['scope']['editorial_policy'] = RC2_POLICY
        for name in R3_READINGS: del review['scope']['mode_findings'][name]
        write_json(p.parent/'evidence/old.json', review)
        load_review(p.parent/'evidence/old.json')
        codes = {e['code'] for e in semantic_profile_errors(p.parent, plan, review)}
        self.assertIn('EDITORIAL_REVIEW_POLICY_MISMATCH', codes)
        self.assertIn('MODE_SEMANTIC_REVIEW_PENDING', codes)

    def test_review_cannot_disguise_r3_tasks_as_an_old_policy(self):
        p, plan = self.t.authored()
        original = self.t.sem(p, plan)
        for schema, policy in [(OUTPUT_SCHEMA, RC2_POLICY), (RC1_SCHEMA, RC1_POLICY), ('2.0.0', None)]:
            with self.subTest(policy=policy):
                bad = copy.deepcopy(original); bad['schema_version'] = schema
                if policy is None: bad['scope'].pop('editorial_policy')
                else: bad['scope']['editorial_policy'] = policy
                path = p.parent/'evidence/disguised.json'; write_json(path, bad)
                self.t.failcode('SCHEMA_UNSUPPORTED', load_review, path)

    def test_malformed_review_policies_fail_closed_without_typeerror(self):
        p, plan = self.t.authored(); original = self.t.sem(p, plan)
        for value in (None, [], {}, 7):
            bad = copy.deepcopy(original); bad['scope']['editorial_policy'] = value
            path = p.parent/'evidence/malformed.json'; write_json(path, bad)
            self.t.failcode('SCHEMA_UNSUPPORTED', load_review, path)
            with self.assertRaises(SurveyError):
                review_template(p.parent, 'output_semantic', ['new'], output_inputs(p.parent),
                                {'editorial_policy': value})

    def test_default_local_units_keep_multiple_complete_canonical_inputs_once(self):
        putnode(self.t.root, 'N-second', 'result', r'For $x\in\mathbb R$, $x^2\geq 0$.',
                [('N-def', 'uses_definition')], source=True, status='established')
        coverage = read_json(self.t.root/'knowledge/coverage.json')
        coverage['questions'][0]['answer_nodes'].append('N-second')
        write_json(self.t.root/'knowledge/coverage.json', coverage)
        v.synthetic_policy_reviews(self.t.root)
        p, plan = self.t.make(); prepare_output(self.t.root, p)
        body = (p.parent/'manuscript/main.tex').read_text()
        for key in ('N-main', 'N-second', 'N-def'):
            self.assertEqual(body.count('\\input{../generated/statements/'+key+'.tex}'), 1)
        self.assertLess(body.index('statements/N-main.tex'), body.index('statements/N-second.tex'))
        middle = body[body.index('statements/N-main.tex'):body.index('statements/N-second.tex')]
        self.assertIn('first use', middle)
        self.assertIn('decisive operations', middle)
        self.assertNotIn('@@', body)
        codes = {e['code'] for e in validate_structure(self.t.root, 'new')['errors']}
        self.assertNotIn('MINIMAL_THREE_SECTIONS_REQUIRED', codes)
        self.assertNotIn('MINIMAL_PRINCIPAL_NOT_FIRST', codes)
        self.assertNotIn('PRINCIPAL_RESULT_ENVIRONMENT_MISSING', codes)

    def test_same_local_body_is_legal_r3_but_rejected_by_each_old_strict_policy(self):
        p, plan = self.t.authored()
        self.assertEqual(validate_structure(self.t.root, 'new')['errors'], [])
        for schema, policy in [(RC1_SCHEMA, RC1_POLICY), (OUTPUT_SCHEMA, RC2_POLICY)]:
            with self.subTest(policy=policy):
                old = copy.deepcopy(plan); old.update(schema_version=schema, editorial_policy=policy)
                write_json(p, old); prepare_output(self.t.root, p)
                self.assertIn('MINIMAL_THREE_SECTIONS_REQUIRED',
                              {e['code'] for e in validate_structure(self.t.root, 'new')['errors']})

    def test_r3_may_choose_three_sections_but_still_needs_new_reading(self):
        p, plan = self.t.authored(policy=RC2_POLICY)
        before = (p.parent/'manuscript/main.tex').read_bytes()
        plan['editorial_policy'] = POLICY; write_json(p, plan); prepare_output(self.t.root, p)
        self.assertEqual(before, (p.parent/'manuscript/main.tex').read_bytes())
        self.assertEqual(validate_structure(self.t.root, 'new')['errors'], [])
        review = self.t.sem(p, plan)
        for name in R3_READINGS: del review['scope']['mode_findings'][name]
        self.assertIn('MODE_SEMANTIC_REVIEW_PENDING',
                      {e['code'] for e in semantic_profile_errors(p.parent, plan, review)})

    def test_legacy_preparation_uses_complete_old_template_without_new_tokens(self):
        p = legacy_plan(self.t.root, oid='legacy')
        prepare_output(self.t.root, p)
        body = (p.parent/'manuscript/main.tex').read_text()
        self.assertNotIn('@@', body)
        self.assertIn('\\input{../generated/statements/N-main.tex}', body)
        for section in MINIMAL_SECTIONS: self.assertIn(section, body)

    def test_rc2_still_checks_design_view_and_comparison_consumption(self):
        p, plan = self.t.make(); plan['editorial_policy'] = RC2_POLICY; write_json(p, plan)
        prepare_output(self.t.root, p)
        self.assertEqual(check_exposition_design(p.parent, plan)['status'], 'NEEDS_WORK')
        scope = review_scope_template(plan)
        self.assertTrue({'view_focus', 'exposition_design'} <= scope['mode_findings'].keys())
        self.assertFalse(set(R3_READINGS) & scope['mode_findings'].keys())
        # Comparison closure must remain active even though rc2 is not current.
        putnode(self.t.root, 'N-prior', 'result', r'For $x=0$, $0x=0$.', status='established')
        putnode(self.t.root, 'N-relation', 'relation', 'Synthetic relation; not a mathematical comparison.',
                [('N-main', 'compares_with'), ('N-prior', 'compares_with')], status='established')
        from survey_core.knowledge import inventory
        inv = inventory(self.t.root)
        plan['selections'].append({'node_id': 'N-relation', 'role': 'background',
                                  'statement_treatment': 'explained_reference',
                                  'proof_treatment': 'none', 'reason': v.SYNTH})
        self.assertIn('N-prior', consumption(inv, plan))

    def test_r3_reprepare_preserves_authored_bytes_and_stales_changed_review(self):
        p, plan = self.t.authored(); review = self.t.sem(p, plan)
        files = [p.parent/x for x in ('manuscript/main.tex', 'manuscript/math-review.sty', 'outline.md')]
        before = [x.read_bytes() for x in files]
        prepare_output(self.t.root, p)
        self.assertEqual(before, [x.read_bytes() for x in files])
        files[2].write_text('A revised actual exposition design.\n')
        self.assertTrue(check_review_bindings(p.parent, review, output_inputs(p.parent)))

    def test_switching_current_to_recorded_cannot_authorize_package(self):
        p, plan = self.t.authored(draft=False, policy=RC2_POLICY)
        review = self.t.sem(p, plan); write_json(p.parent/'evidence/old.json', review)
        current_report = assess_release(self.t.root, 'new')
        old_report = assess_release(self.t.root, 'new', policy_mode='recorded')
        self.assertIn('EDITORIAL_POLICY_REASSESSMENT_REQUIRED', {e['code'] for e in current_report['errors']})
        self.assertEqual(old_report['artifacts']['evaluated_policy'], RC2_POLICY)
        self.assertFalse(old_report['artifacts']['release_authorized'])
        self.t.failcode('RELEASE_NOT_READY', package_output, self.t.root, 'new', self.t.base/'no.zip')

    def test_r3_principal_tampering_and_paper_defaults_still_block(self):
        p, plan = self.t.authored()
        main = p.parent/'manuscript/main.tex'
        main.write_text(main.read_text().replace(r'\begin{theorem}', '').replace(r'\end{theorem}', ''))
        self.assertIn('PRINCIPAL_RESULT_ENVIRONMENT_MISSING',
                      {e['code'] for e in validate_structure(self.t.root, 'new')['errors']})
        (p.parent/'generated/statements/N-main.tex').write_text('Altered theorem')
        self.t.failcode('CANONICAL_STATEMENT_CHANGED', verify_generated, self.t.root, plan)
        p, paper = self.t.make('paper', 'paper-default', draft=False)
        self.assertTrue(paper['draft'])
        self.assertIn('PAPER_ORIGINAL_CONTRIBUTION_MISSING', self.t.readiness(paper))


class R3KnowledgeReview(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext(); self.t.setUp()
        from survey_core.knowledge import inventory
        self.inv = inventory(self.t.root)
        self.review_path = self.t.root/'evidence/reviews/new-coverage-N-q.json'
        self.review = load_review(self.review_path)

    def tearDown(self):
        self.t.tearDown()

    def test_existing_findings_and_inputs_validate_without_any_output(self):
        self.assertEqual(knowledge_scope_errors(self.inv, 'N-q', self.review), [])
        self.assertFalse((self.t.root/'outputs').exists())

    def test_each_required_task_needs_actual_scoped_finding(self):
        for task in R3_READINGS:
            with self.subTest(task=task):
                bad = copy.deepcopy(self.review)
                bad['findings'] = [x for x in bad['findings'] if not x.startswith(task+':')]
                self.assertIn('KNOWLEDGE_REVIEW_PENDING',
                              {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', bad)})

    def test_old_policy_acceptance_cannot_substitute_for_r3_knowledge_tasks(self):
        self.review_path.unlink()
        _, plan = self.t.make()
        self.assertIn('KNOWLEDGE_REVIEW_POLICY_REASSESSMENT_REQUIRED', self.t.readiness(plan))
        plan['editorial_policy'] = RC2_POLICY
        self.assertNotIn('KNOWLEDGE_REVIEW_POLICY_REASSESSMENT_REQUIRED', self.t.readiness(plan))

    def test_bad_or_missing_subsection_is_refused(self):
        for target in ('knowledge/nodes/N-q.md#not-a-section',
                       'knowledge/missing.md#fast', '../outside.md#fast',
                       'https://example.invalid/route.md#fast', 'knowledge/nodes/N-q.md'):
            with self.subTest(target=target):
                bad = copy.deepcopy(self.review)
                bad['findings'][0] = R3_READINGS[0] + ': ' + v.SYNTH + ' [Location](' + target + ')'
                self.assertIn('KNOWLEDGE_REVIEW_LOCATION_INVALID',
                              {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', bad)})

    def test_route_file_requires_actual_input_hash_and_stales_on_edit(self):
        from survey_core.common import file_hash
        route = self.t.root/'knowledge/route.md'
        route.write_text('# Fast route\n\nSynthetic route content, not mathematical evidence.\n')
        review = copy.deepcopy(self.review)
        review['findings'] = [task+': '+v.SYNTH+' [Route](knowledge/route.md#fast-route)' for task in R3_READINGS]
        self.assertIn('REVIEW_SCOPE_INSUFFICIENT',
                      {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', review)})
        review['inputs'].append({'path': 'knowledge/route.md', 'sha256': file_hash(self.t.root, 'knowledge/route.md')})
        self.assertEqual(knowledge_scope_errors(self.inv, 'N-q', review), [])
        route.write_text('# Fast route\n\nChanged synthetic route.\n')
        self.assertIn('REVIEW_STALE', {x['code'] for x in knowledge_scope_errors(self.inv, 'N-q', review)})

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
        self.assertEqual(set(review['scope']['checks']), set(R3_READINGS))
        self.assertEqual(review['disposition'], 'revise')
        self.assertEqual(review['reviewer_mode'], 'not_performed')
        self.assertFalse((self.t.root/'outputs').exists())


if __name__ == '__main__':
    unittest.main()
