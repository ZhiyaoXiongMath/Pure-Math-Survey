"""Neutral regressions for real file transitions, with SYNTHETIC review states.

These records test gates; they do not certify actual mathematics or nonauthors.
"""
import copy
import json
import subprocess
import sys
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

import test_vnext as v
from test_v2 import read_json, write_json, putnode, now, SCRIPTS
from survey_core.common import file_hash, sha, SurveyError, safe, native_path, relpath
from survey_core.knowledge import inventory
from survey_core.models import load_node, node_bytes, load_plan
from survey_core.snapshots import freeze_snapshot, load_snapshot
from survey_core.plans import create_plan, promise_request
from survey_core.reviews import (check_review_bindings, load_review, plan_mathematical_template,
                                 plan_promise_scope_errors)
from survey_core.readiness import assess_readiness
from survey_core.exports import prepare_output, verify_generated
from survey_core.profiles import STATEMENT_ASPECTS


class WorkflowBindings(unittest.TestCase):
    def setUp(self):
        self.t = v.VNext(); self.t.setUp()
    def tearDown(self):
        # The product receives ordinary paths. Only the fixture's explicitly
        # owned temporary tree needs native cleanup for >260-byte descendants.
        self.assertEqual(self.t.base.resolve(), Path(self.t.tmp.name).resolve())
        if self.t.base.exists():
            shutil.rmtree(native_path(self.t.base, extended=True))
        self.t.tearDown()

    def bind_auxiliary(self, name='support/neutral.md'):
        path = self.t.root/name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'Opaque synthetic auxiliary input; [[N-not-a-knowledge-registry]].\n')
        for review_path in (self.t.root/'evidence/reviews').glob('*.json'):
            record = read_json(review_path)
            record['inputs'].append({'path': name, 'sha256': file_hash(self.t.root, name)})
            write_json(review_path, record)
        return name

    def detailed_plan(self):
        p, plan = self.t.make(draft=False)
        plan['audience'] = 'Synthetic reader can multiply real numbers.'
        plan['reader_goals'] = ['Reconstruct this synthetic multiplication, not a mathematical acceptance claim.']
        plan['proof_obligations'][0]['required_steps'] = [
            'Use the fixed real number x=0 and substitute it in the two factors.',
            'Compute both factors and their product, preserving the asserted conclusion.']
        write_json(p, plan)
        return p, plan

    def synthetic_requested_review(self, p, plan):
        record, request = plan_mathematical_template(self.t.root, p, ['N-main'])
        record.update(review_id='SYNTHETIC-PLAN-READING', reviewer_mode='independent_review',
                      reviewer='Distinct synthetic reviewer identity, not a real reading',
                      reviewed_at=now(), findings=[v.SYNTH], unchecked_items=[], disposition='accepted')
        record['scope']['proof_steps']['N-main'] = list(plan['proof_obligations'][0]['required_steps'])
        for item in record['scope']['statement_reviews'].values():
            item['outcome'] = 'accepted'
            item.update({key: v.SYNTH for key in STATEMENT_ASPECTS})
        record['scope']['evidence_basis'] = v.SYNTH
        return record, request

    def adopt(self, p, plan):
        plan['snapshot_id'] = freeze_snapshot(self.t.root)['artifacts']['snapshot_id']
        write_json(p, plan)

    def test_safe_bound_auxiliary_survives_freeze_formal_readiness_and_materials(self):
        name = self.bind_auxiliary()
        reviews = {p.relative_to(self.t.root).as_posix(): p.read_bytes()
                   for p in (self.t.root/'evidence/reviews').glob('*.json')}
        p, plan = self.t.make(draft=False)
        manifest, frozen = load_snapshot(self.t.root, plan['snapshot_id'])
        self.assertIn(name, {r['path'] for r in manifest['files']})
        self.assertEqual(safe(frozen, name, True).read_bytes(), safe(self.t.root, name, True).read_bytes())
        for path, data in reviews.items():
            self.assertEqual(safe(frozen, path, True).read_bytes(), data)
            self.assertEqual(check_review_bindings(frozen, load_review(safe(frozen, path))), [])
        self.assertEqual(assess_readiness(self.t.root, plan)['status'], 'READY')
        prepare_output(self.t.root, p)
        self.assertTrue((p.parent/'materials'/name).is_file())
        self.assertFalse((p.parent/'materials/knowledge/material.txt').exists())
        self.assertIn(name, {r['path'] for r in verify_generated(self.t.root, plan)['consumed_inputs']})

    def test_missing_or_changed_input_is_never_fabricated_or_reaccepted(self):
        name = self.bind_auxiliary()
        for defect in ('missing', 'changed'):
            with self.subTest(defect=defect):
                file = safe(self.t.root, name)
                if file.exists(): file.unlink()
                if defect == 'changed': file.write_bytes(b'Changed actual bytes.\n')
                before = {p: p.read_bytes() for p in (self.t.root/'evidence/reviews').glob('*.json')}
                p, plan = self.t.make(oid=defect, draft=False)
                _, frozen = load_snapshot(self.t.root, plan['snapshot_id'])
                self.assertEqual(safe(frozen, name).exists(), defect == 'changed')
                self.assertEqual(before, {p: p.read_bytes() for p in before})
                self.assertIn('REVIEW_STALE', self.t.readiness(plan))

    def test_declared_unsafe_or_excluded_bindings_are_rejected_even_when_missing(self):
        path = self.t.root/'evidence/reviews/new-N-main.json'; original = read_json(path)
        for value in ('../escape.dat', 'outputs/nope.txt', 'snapshots/missing.dat', '.cache/missing.dat',
                      'evidence/reviews/new-N-main.json'):
            with self.subTest(path=value):
                bad = copy.deepcopy(original); bad['inputs'].append({'path': value, 'sha256': '0'*64})
                write_json(path, bad)
                with self.assertRaises(SurveyError): freeze_snapshot(self.t.root)
                self.assertFalse((self.t.root/'snapshots').exists())
        write_json(path, original)

    def test_excluded_and_self_case_aliases_fail_before_freezing(self):
        path = self.t.root/'evidence/reviews/new-N-main.json'; original = read_json(path)
        existing = self.t.root/'outputs/excluded.txt'; existing.parent.mkdir(exist_ok=True)
        existing.write_bytes(b'Existing excluded data.\n')
        for value in ('Outputs/excluded.txt', '.Cache/missing.dat', 'Snapshots/missing.dat',
                      'EVIDENCE/Reviews/NEW-n-MAIN.JSON'):
            with self.subTest(path=value):
                record = copy.deepcopy(original); record['inputs'].append({'path': value, 'sha256': '0'*64})
                write_json(path, record)
                self.t.failcode('REVIEW_BINDING_INVALID', freeze_snapshot, self.t.root)
                self.assertFalse((self.t.root/'snapshots').exists())
        write_json(path, original)

    def test_bound_auxiliary_concurrent_change_rejects_atomic_stage(self):
        name = self.bind_auxiliary()
        import survey_core.snapshots as mod
        atomic = mod.atomic_bytes; changed = False
        def mutate(path, data):
            nonlocal changed
            atomic(path, data)
            if path.as_posix().endswith(name) and not changed:
                changed = True; safe(self.t.root, name).write_bytes(b'Concurrent change.\n')
        with patch.object(mod, 'atomic_bytes', mutate):
            self.t.failcode('SNAPSHOT_INPUT_CHANGED', freeze_snapshot, self.t.root)
        self.assertEqual(list((self.t.root/'snapshots').glob('KB-*')), [])
        self.assertEqual(list((self.t.root/'snapshots').glob('.pending-*')), [])

    def test_detailed_or_missing_step_maps_stay_pending_without_semantic_inference(self):
        p, plan = self.detailed_plan()
        self.assertIn('PROOF_OBLIGATION_UNMET', self.t.readiness(plan))
        path = self.t.root/'evidence/reviews/new-N-main.json'; record = read_json(path)
        record['scope'].pop('proof_steps'); record['findings'] = ['Narrative praise is not an exact checked-step map.']
        write_json(path, record); self.adopt(p, plan)
        self.assertIn('PROOF_OBLIGATION_UNMET', self.t.readiness(plan))

    def test_plan_cli_creates_only_pending_bound_content_addressed_request(self):
        p, plan = self.detailed_plan()
        args = [sys.executable, str(SCRIPTS/'survey.py'), 'review', 'template', str(self.t.root),
                '--kind', 'mathematical', '--id', 'N-main', '--plan', 'outputs/new/plan.json',
                '--to', 'evidence/reviews/request.json', '--json']
        run = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        artifact = json.loads(run.stdout)['artifacts']; record = artifact['review']
        expected_path, data = promise_request(plan)
        self.assertEqual(artifact['promise_request'], expected_path)
        self.assertEqual(safe(self.t.root, expected_path, True).read_bytes(), data)
        projection = json.loads(data); self.assertNotIn('snapshot_id', projection)
        self.assertEqual(projection['proof_obligations'], plan['proof_obligations'])
        self.assertEqual(record['scope']['proof_steps'], {'N-def': [], 'N-main': []})
        self.assertEqual(record['scope']['statement_reviews']['N-main']['outcome'], 'not_performed')
        self.assertEqual((record['disposition'], record['reviewer_mode']), ('revise', 'not_performed'))
        again = subprocess.run(args, capture_output=True, text=True)
        self.assertNotEqual(again.returncode, 0); self.assertIn('DESTINATION_EXISTS', again.stdout)
        self.assertEqual(safe(self.t.root, expected_path, True).read_bytes(), data)

    def test_actual_exact_scoped_record_freeze_and_explicit_adoption_satisfy_gate(self):
        p, plan = self.detailed_plan(); old_snapshot = plan['snapshot_id']
        record, request = self.synthetic_requested_review(p, plan)
        write_json(self.t.root/'evidence/reviews/scoped.json', record)
        self.assertIn('PROOF_OBLIGATION_UNMET', self.t.readiness(plan))
        self.adopt(p, plan)
        self.assertNotEqual(plan['snapshot_id'], old_snapshot)
        self.assertEqual(assess_readiness(self.t.root, plan)['status'], 'READY')
        self.assertEqual(promise_request(plan)[0], request)
        _, old = load_snapshot(self.t.root, old_snapshot)
        self.assertFalse(safe(old, request).exists())
        prepare_output(self.t.root, p)
        self.assertTrue((p.parent/'materials'/request).exists())
        self.assertIn('SYNTHETIC-PLAN-READING', assess_readiness(self.t.root, plan)['artifacts']['used_review_ids'])

    def test_content_addressed_request_freezes_at_real_ordinary_windows_depth(self):
        self.ordinary_depth_flow('new')

    def test_legal_long_plan_identity_survives_actual_cli_and_snapshot_adoption(self):
        self.ordinary_depth_flow('identity-' + 'x' * 131)

    def ordinary_depth_flow(self, output_id):
        p, plan = self.detailed_plan()
        # A deeper ordinary root than the independently failing root. No device
        # prefix/TEMP override is supplied to the product CLI or snapshot APIs.
        label = 'ordinary-depth-'
        depth = max(100, len(str(self.t.base)) + 1 + len(label))
        component = label + 'd' * (depth - len(str(self.t.base)) - 1 - len(label))
        deep = self.t.base/component
        self.assertEqual(len(str(deep)), depth)
        self.assertGreaterEqual(len(str(deep)), 100)
        shutil.copytree(self.t.root, deep)
        try:
            plan_relative = f'outputs/{output_id}/plan.json'
            if output_id != 'new':
                # Exercise creation, including diagnostics and returned identity,
                # before authoring the actual detailed promises.
                created = create_plan(deep, output_id, plan['snapshot_id'], draft=False)
                self.assertEqual(created['artifacts']['plan'], plan_relative)
                self.assertGreaterEqual(len(str(deep/plan_relative)), 248)
                plan['output_id'] = output_id
                write_json(safe(deep, plan_relative, True), plan)
            relocated = safe(deep, plan_relative, True)
            self.assertEqual(relpath(deep, relocated), plan_relative)
            self.assertEqual(load_plan(deep/plan_relative), plan)
            args = [sys.executable, str(SCRIPTS/'survey.py'), 'review', 'template', str(deep),
                    '--kind', 'mathematical', '--id', 'N-main', '--plan', plan_relative,
                    '--to', 'evidence/reviews/deep-request.json', '--json']
            run = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            response = json.loads(run.stdout)['artifacts']; request = response['promise_request']
            record = response['review']
            self.assertEqual(record['scope']['proof_steps'], {'N-def': [], 'N-main': []})
            # Explicit synthetic independent record tests consumption only.
            record.update(review_id='SYNTHETIC-DEEP-PLAN', reviewer_mode='independent_review',
                          reviewer='Distinct synthetic reviewer; not an actual mathematical reading',
                          reviewed_at=now(), findings=[v.SYNTH], unchecked_items=[], disposition='accepted')
            record['scope']['proof_steps']['N-main'] = list(plan['proof_obligations'][0]['required_steps'])
            for item in record['scope']['statement_reviews'].values():
                item['outcome'] = 'accepted'
                item.update({key: v.SYNTH for key in STATEMENT_ASPECTS})
            record['scope']['evidence_basis'] = v.SYNTH
            write_json(deep/'evidence/reviews/deep-request.json', record)
            sid = freeze_snapshot(deep)['artifacts']['snapshot_id']
            manifest, files = load_snapshot(deep, sid)
            actual = files/request
            self.assertGreater(len(str(actual)), 260)
            accessible = safe(files, request, True)
            self.assertTrue(accessible.is_file())
            self.assertEqual(accessible.read_bytes(), promise_request(plan)[1])
            self.assertIn(request, {entry['path'] for entry in manifest['files']})
            self.assertEqual(check_review_bindings(files, load_review(files/'evidence/reviews/deep-request.json')), [])
            plan['snapshot_id'] = sid; write_json(relocated, plan)
            self.assertEqual(assess_readiness(deep, plan)['status'], 'READY')
            self.assertEqual(prepare_output(deep, relocated)['status'], 'PREPARED')
            verify_generated(deep, plan)
            out = safe(deep, 'outputs/' + output_id)
            self.assertEqual(safe(out, 'materials/' + request, True).read_bytes(), accessible.read_bytes())
            from survey_core.tex import inspect_tex, input_path
            inspection = inspect_tex(out)
            self.assertIn('generated/statements/N-main.tex', inspection.body_inputs)
            self.assertEqual(relpath(out, input_path(out, '../generated/statements/N-main.tex')),
                             'generated/statements/N-main.tex')
            self.t.failcode('UNSAFE_PATH', input_path, out, '../../../outside.tex')
            # Reprepare must preserve real author bytes also at the long identity.
            main = safe(out, 'manuscript/main.tex', True)
            authored = main.read_bytes() + b'\n% Actual preservation probe.\n'
            main.write_bytes(authored)
            prepare_output(deep, relocated)
            self.assertEqual(main.read_bytes(), authored)
            self.t.failcode('UNSAFE_PATH', relpath, deep, self.t.root/'project.json')
            self.t.failcode('UNSAFE_PATH', safe, deep, '../project.json')
            self.t.failcode('PLAN_LOCATION_MISMATCH', plan_mathematical_template,
                            deep, self.t.root/'outputs/new/plan.json', ['N-main'])
        finally:
            self.assertTrue(deep.resolve().is_relative_to(self.t.base.resolve()))
            shutil.rmtree(native_path(deep, extended=True))

    def test_native_identity_still_rejects_symlink_escape(self):
        link = self.t.root/'link'
        try:
            link.symlink_to(self.t.base, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'OS did not authorize directory symlink creation: {exc}')
        try:
            self.t.failcode('UNSAFE_PATH', safe, self.t.root, 'link/project/project.json', True)
            self.t.failcode('UNSAFE_PATH', safe, self.t.root,
                            relpath(self.t.root, native_path(link/'project/project.json', extended=True)), True)
        finally:
            link.unlink()

    def test_failed_final_snapshot_readability_rolls_back_named_destination(self):
        import survey_core.snapshots as mod
        with patch.object(mod, 'load_snapshot', side_effect=SurveyError('UNKNOWN_REFERENCE', 'Injected ordinary-path read failure')):
            self.t.failcode('UNKNOWN_REFERENCE', freeze_snapshot, self.t.root)
        self.assertEqual(list((self.t.root/'snapshots').glob('KB-*')), [])
        self.assertEqual(list((self.t.root/'snapshots').glob('.pending-*')), [])

    def test_scoped_record_requires_current_projection_and_real_nonauthor_mode(self):
        p, plan = self.detailed_plan(); original, _ = self.synthetic_requested_review(p, plan)
        for field, value in [('output_ids', ['other']), ('proof_steps', {'N-main': [v.STEP]})]:
            record = copy.deepcopy(original); record['scope'][field] = value
            write_json(self.t.root/'evidence/reviews/scoped.json', record); self.adopt(p, plan)
            self.assertNotEqual(assess_readiness(self.t.root, plan)['status'], 'READY')
        record = copy.deepcopy(original); record['reviewer_mode'] = 'author_reread'
        self.assertIn('PLAN_REVIEW_INDEPENDENT_REQUIRED', {e['code'] for e in plan_promise_scope_errors(self.t.root, plan, record)})
        for field, value in [('audience', 'Changed reader prerequisites'), ('view', 'methods')]:
            changed = copy.deepcopy(plan); changed[field] = value
            self.assertIn('PLAN_REVIEW_SCOPE_MISMATCH', {e['code'] for e in plan_promise_scope_errors(self.t.root, changed, original)})
        changed = copy.deepcopy(plan); changed['proof_obligations'][0]['treatment'] = 'complete'
        self.assertIn('PLAN_REVIEW_SCOPE_MISMATCH', {e['code'] for e in plan_promise_scope_errors(self.t.root, changed, original)})

    def test_request_refuses_changed_live_mathematical_bytes(self):
        p, _ = self.detailed_plan()
        node = self.t.root/'knowledge/nodes/N-main.md'; node.write_bytes(node.read_bytes()+b'\nChanged derivation.\n')
        self.t.failcode('PLAN_KNOWLEDGE_CHANGED', plan_mathematical_template, self.t.root, p, ['N-main'])
        self.assertFalse((self.t.root/'evidence/p').exists())

    def test_root_binding_failure_does_not_masquerade_as_unmapped_steps(self):
        name = self.bind_auxiliary(); p, plan = self.t.make(draft=False)
        # New snapshots retain changed bytes but keep original review hashes.
        safe(self.t.root, name).write_bytes(b'Unreviewed changed input.\n'); self.adopt(p, plan)
        codes = self.t.readiness(plan)
        self.assertIn('REVIEW_STALE', codes)
        self.assertNotIn('PROOF_OBLIGATION_UNMET', codes)
        # Genuine distinct authored actions still fail when bindings are valid.
        self.assertNotEqual(assess_readiness(self.t.root, plan)['status'], 'READY')

    def test_coverage_pending_remains_separate_from_honest_paper_refusal(self):
        p, plan = self.t.make('paper')
        self.assertIn('PAPER_ORIGINAL_CONTRIBUTION_MISSING', self.t.eligibility(plan))
        coverage = self.t.root/'knowledge/coverage.json'; value = read_json(coverage)
        value['questions'][0]['assessment'] = 'pending'; write_json(coverage, value); self.adopt(p, plan)
        self.assertIn('COVERAGE_PENDING', self.t.readiness(plan))

    def test_substantive_open_question_survives_all_views_without_becoming_theorem(self):
        putnode(self.t.root, 'N-inquiry', 'question', 'A genuine retained open task in this synthetic scope.', questions=(), status='open')
        cov = read_json(self.t.root/'knowledge/coverage.json')
        cov['questions'][0]['boundary_nodes'].append('N-inquiry')
        cov['questions'].append(dict(question_id='N-inquiry', answer_nodes=['N-inquiry'], mechanism_nodes=[], boundary_nodes=[],
                                    gaps=[], assessment='limited', rationale=v.SYNTH))
        write_json(self.t.root/'knowledge/coverage.json', cov)
        sid = freeze_snapshot(self.t.root)['artifacts']['snapshot_id']
        for view in v.VIEW_TASKS if hasattr(v, 'VIEW_TASKS') else ('integrated','foundations','results','methods','boundaries'):
            create_plan(self.t.root, view, sid, draft=True, view=view)
            p = self.t.root/f'outputs/{view}/plan.json'; plan = load_plan(p)
            selected = {s['node_id']: s for s in plan['selections']}
            self.assertEqual(selected['N-inquiry']['role'], 'frontier')
            self.assertEqual(selected['N-inquiry']['statement_treatment'], 'full')
            self.assertEqual(selected['N-inquiry']['proof_treatment'], 'none')
            self.assertEqual({k for k, s in selected.items() if s['role']=='principal_answer'}, {'N-main'})
            self.assertNotIn('N-q', selected)
            prepare_output(self.t.root, p)
            main = (p.parent/'manuscript/main.tex').read_text()
            self.assertIn(r'\begin{problem}\label{node:N-inquiry}', main)
            self.assertNotIn(r'\begin{theorem}\label{node:N-inquiry}', main)
        self.assertEqual(load_node(self.t.root/'knowledge/nodes/N-inquiry.md').meta['mathematical_status'], 'open')

    def test_unassessed_result_draft_is_legal_but_question_only_default_needs_result(self):
        p = self.t.root/'knowledge/nodes/N-main.md'; node = load_node(p)
        node.meta['mathematical_status'] = 'unassessed'; p.write_bytes(node_bytes(node.meta, node.body))
        sid = freeze_snapshot(self.t.root)['artifacts']['snapshot_id']
        create_plan(self.t.root, 'legal-draft', sid, draft=True)
        prepare_output(self.t.root, self.t.root/'outputs/legal-draft/plan.json')
        cov = read_json(self.t.root/'knowledge/coverage.json'); cov['questions'][0]['answer_nodes'] = ['N-q']
        write_json(self.t.root/'knowledge/coverage.json', cov)
        sid = freeze_snapshot(self.t.root)['artifacts']['snapshot_id']
        self.t.failcode('PLAN_INVALID', create_plan, self.t.root, 'no-result', sid, draft=True)
        self.assertFalse((self.t.root/'outputs/no-result/plan.json').exists())

    def test_explicit_question_principal_is_retained_honestly_without_proof_promise(self):
        putnode(self.t.root, 'N-inquiry', 'question', 'The retained open task, not a proved answer.', questions=(), status='open')
        cov = read_json(self.t.root/'knowledge/coverage.json')
        cov['questions'].append(dict(question_id='N-inquiry', answer_nodes=['N-inquiry'], mechanism_nodes=[], boundary_nodes=[],
                                    gaps=[], assessment='limited', rationale=v.SYNTH))
        write_json(self.t.root/'knowledge/coverage.json', cov)
        sid = freeze_snapshot(self.t.root)['artifacts']['snapshot_id']
        create_plan(self.t.root, 'explicit', sid, principals=['N-main', 'N-inquiry'], draft=True)
        p = self.t.root/'outputs/explicit/plan.json'; plan = load_plan(p)
        selected = {s['node_id']: s for s in plan['selections']}
        self.assertEqual(selected['N-inquiry']['role'], 'frontier')
        self.assertEqual(selected['N-inquiry']['statement_treatment'], 'full')
        self.assertEqual(selected['N-inquiry']['proof_treatment'], 'none')
        self.assertNotIn('N-inquiry', {o['node_id'] for o in plan['proof_obligations']})
        self.assertEqual({k for k, s in selected.items() if s['role']=='principal_answer'}, {'N-main'})
        self.t.failcode('PLAN_INVALID', create_plan, self.t.root, 'only-inquiry', sid, principals=['N-inquiry'], draft=True)




class ReviewCandidateWorkflow(unittest.TestCase):
    setUp = WorkflowBindings.setUp
    tearDown = WorkflowBindings.tearDown
    detailed_plan = WorkflowBindings.detailed_plan
    adopt = WorkflowBindings.adopt
    """All assertions below are SYNTHETIC engineering fixtures, never readings."""

    def candidate(self):
        from survey_core.reviews import review_template, coverage_inputs, knowledge_scope_template
        p, plan = self.detailed_plan()
        keys = ['N-main', 'N-def', 'N-q']
        record, request = plan_mathematical_template(self.t.root, p, keys)
        record.update(review_id='SYNTHETIC-CANDIDATE-MATH', reviewer_mode='independent_review',
                      reviewer='Distinct synthetic fixture identity; no mathematical reading',
                      reviewed_at=now(), findings=[v.SYNTH], unchecked_items=[], disposition='accepted')
        record['scope']['proof_steps']['N-main'] = list(plan['proof_obligations'][0]['required_steps'])
        record['scope']['evidence_basis'] = v.SYNTH
        for item in record['scope']['statement_reviews'].values():
            item.update(outcome='accepted', **{key: v.SYNTH for key in STATEMENT_ASPECTS})
        inv = inventory(self.t.root)
        cov = read_json(self.t.root/'knowledge/coverage.json')
        cov['questions'][0]['rationale'] += ' SYNTHETIC candidate byte transition.'
        candidate = self.t.root/'.cache/candidate'
        write_json(candidate/'knowledge/coverage.json', cov)
        coverage = review_template(self.t.root, 'coverage', ['N-q'], coverage_inputs(inv, 'N-q'),
                                  knowledge_scope_template(inv, ['N-q']))
        coverage.update(review_id='SYNTHETIC-CANDIDATE-COVERAGE', reviewer_mode='independent_review',
                        reviewer='Distinct synthetic fixture identity', reviewed_at=now(), unchecked_items=[], disposition='accepted')
        from survey_core.profiles import UNDERSTANDING_READINGS
        coverage['findings'] = [f'{task}: {v.SYNTH} [Actual fixture section](knowledge/nodes/N-q.md#software-fixture)'
                                for task in UNDERSTANDING_READINGS]
        for binding in coverage['inputs']:
            if binding['path'] == 'knowledge/coverage.json':
                binding['sha256'] = sha((candidate/'knowledge/coverage.json').read_bytes())
        write_json(candidate/'evidence/reviews/candidate-math.json', record)
        write_json(candidate/'evidence/reviews/candidate-coverage.json', coverage)
        return p, plan, candidate, record, request

    def accept(self, p):
        from survey_core.reviews import accept_review_candidate
        return accept_review_candidate(self.t.root, '.cache/candidate', relpath(self.t.root, p))

    def live_bytes(self):
        return {path: safe(self.t.root, path, True).read_bytes() for path in inventory(self.t.root).files}

    def test_candidate_cli_complete_plan_promise_review_stage_freeze_adopt_prepare(self):
        p, plan, candidate, record, request = self.candidate()
        old_snapshot, old_files = load_snapshot(self.t.root, plan['snapshot_id'])
        old_manifest = copy.deepcopy(old_snapshot)
        old_reviews = {path.name: path.read_bytes() for path in (self.t.root/'evidence/reviews').glob('*.json')}
        run = subprocess.run([sys.executable, str(SCRIPTS/'survey.py'), 'review', 'accept', str(self.t.root),
                              '--candidate', '.cache/candidate', '--plan', relpath(self.t.root, p), '--json'],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout)['status'], 'ACCEPTED')
        self.assertEqual(load_snapshot(self.t.root, plan['snapshot_id'])[0], old_manifest)
        for name, data in old_reviews.items(): self.assertEqual((self.t.root/'evidence/reviews'/name).read_bytes(), data)
        self.assertEqual(read_json(p)['snapshot_id'], plan['snapshot_id'])
        self.adopt(p, plan)
        self.assertEqual(assess_readiness(self.t.root, plan)['status'], 'READY')
        self.assertEqual(prepare_output(self.t.root, p)['status'], 'PREPARED')
        verify_generated(self.t.root, plan)
        self.assertEqual(promise_request(plan)[0], request)
        run = subprocess.run([sys.executable, str(SCRIPTS/'survey.py'), 'review', 'validate', str(self.t.root),
                              '--record', 'evidence/reviews/candidate-math.json',
                              '--record', 'evidence/reviews/candidate-coverage.json', '--plan', relpath(self.t.root, p), '--json'],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertFalse(list((self.t.root/'.cache').glob('.review-*')))

    def test_pending_templates_cover_every_scoped_canonical_and_real_identity_slots(self):
        from survey_core.reviews import review_template, mathematical_inputs
        p, plan = self.detailed_plan()
        template, request = plan_mathematical_template(self.t.root, p, ['N-main'])
        self.assertEqual(set(template['scope']['statement_reviews']), {'N-main', 'N-def'})
        self.assertEqual(template['scope']['proof_steps'], {'N-main': [], 'N-def': []})
        self.assertEqual(template['reviewer'], '')
        self.assertEqual(template['scope']['evidence_basis'], '')
        self.assertEqual(template['reviewer_mode'], 'not_performed')
        self.assertIsNone(template['reviewed_at'])
        self.assertTrue(template['unchecked_items'])
        inv = inventory(self.t.root)
        generic = review_template(self.t.root, 'mathematical', ['N-def'], mathematical_inputs(inv, 'N-def'))
        self.assertEqual(set(generic['scope']['statement_reviews']), {'N-def'})
        self.assertEqual(generic['scope']['statement_reviews']['N-def']['outcome'], 'not_performed')

    def test_batch_aggregates_independent_missing_fields_and_valid_record_omissions(self):
        from survey_core.reviews import validate_reviews
        p, plan, candidate, record, request = self.candidate()
        write_json(self.t.root/'evidence/reviews/missing-a.json', {'kind': 'mathematical', 'inputs': [{}]})
        write_json(self.t.root/'.cache/missing-b.json', {'review_id': 'SYNTHETIC'})
        del record['scope']['statement_reviews']['N-def']
        record['scope']['proof_steps'].pop('N-q')
        write_json(self.t.root/'.cache/omissions.json', record)
        report = validate_reviews(self.t.root, ['evidence/reviews/missing-a.json', '.cache/missing-b.json', '.cache/omissions.json'], plan)
        self.assertEqual(report['status'], 'NEEDS_WORK')
        fields = [error for error in report['errors'] if error['code'] == 'CONTRACT_INVALID']
        self.assertGreater(len(fields), 10)
        self.assertTrue(any(error['node_id'] == 'N-def' for error in report['errors']))
        self.assertTrue(any(error['node_id'] == 'N-q' for error in report['errors']))

    def test_canonical_omission_and_wrong_promise_reject_without_live_mutation(self):
        for defect in ('canonical', 'promise', 'generic', 'author'):
            with self.subTest(defect=defect):
                p, plan, candidate, record, request = self.candidate()
                before = self.live_bytes()
                if defect == 'canonical': record['scope']['statement_reviews'].pop('N-def')
                elif defect == 'promise': record['inputs'] = [binding for binding in record['inputs'] if binding['path'] != request]
                elif defect == 'generic': record['scope'].pop('output_ids')
                else: record['reviewer_mode'] = 'author_reread'
                write_json(candidate/'evidence/reviews/candidate-math.json', record)
                result = self.accept(p)
                self.assertEqual(result['status'], 'NEEDS_WORK')
                self.assertEqual(self.live_bytes(), before)
                shutil.rmtree(candidate)
                shutil.rmtree(p.parent)

    def test_stale_bytes_report_binding_root_without_false_step_omissions(self):
        p, plan, candidate, record, request = self.candidate()
        path = candidate/'knowledge/nodes/N-main.md'; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((self.t.root/'knowledge/nodes/N-main.md').read_bytes() + b'\nSynthetic changed body.\n')
        before = self.live_bytes(); result = self.accept(p)
        self.assertEqual(result['status'], 'NEEDS_WORK')
        codes = {error['code'] for error in result['errors']}
        self.assertIn('REVIEW_STALE', codes)
        self.assertNotIn('PROOF_OBLIGATION_UNMET', codes)
        self.assertEqual(self.live_bytes(), before)

    def test_candidate_path_escape_symlink_and_existing_evidence_are_rejected(self):
        from survey_core.reviews import accept_review_candidate
        p, plan, candidate, record, request = self.candidate(); before = self.live_bytes()
        self.t.failcode('UNSAFE_PATH', accept_review_candidate, self.t.root, '../candidate', relpath(self.t.root, p))
        write_json(candidate/'outputs/forbidden/plan.json', plan)
        self.t.failcode('UNSAFE_PATH', self.accept, p)
        shutil.rmtree(candidate/'outputs')
        write_json(candidate/'evidence/reviews/new-N-main.json', record)
        self.t.failcode('DESTINATION_EXISTS', self.accept, p)
        (candidate/'evidence/reviews/new-N-main.json').unlink()
        link = candidate/'knowledge/escaped.md'
        try: link.symlink_to(self.t.root/'knowledge/overview.md')
        except (OSError, NotImplementedError) as exc: self.skipTest(f'Actual symlink creation unavailable: {exc}')
        self.t.failcode('UNSAFE_PATH', self.accept, p)
        link.unlink()
        self.assertEqual(self.live_bytes(), before)

    def test_concurrent_plan_candidate_and_live_inputs_reject_staging(self):
        from survey_core.readiness import assess_readiness as actual
        for target in ('plan', 'candidate', 'live'):
            with self.subTest(target=target):
                p, plan, candidate, record, request = self.candidate()
                before = self.live_bytes()
                changed = False
                def assess(root, value, **kwargs):
                    nonlocal changed
                    result = actual(root, value, **kwargs)
                    if not changed:
                        changed = True
                        path = p if target == 'plan' else candidate/'knowledge/coverage.json' if target == 'candidate' else self.t.root/'knowledge/discovery.md'
                        path.write_bytes(path.read_bytes() + b'\n')
                    return result
                with patch('survey_core.readiness.assess_readiness', assess):
                    self.t.failcode('REVIEW_INPUT_CHANGED', self.accept, p)
                self.assertFalse((self.t.root/'evidence/reviews/candidate-math.json').exists())
                if target == 'live': (self.t.root/'knowledge/discovery.md').write_bytes(before['knowledge/discovery.md'])
                self.assertEqual(self.live_bytes(), before)
                shutil.rmtree(candidate); shutil.rmtree(p.parent)

    def post_install_change(self, target):
        from survey_core.readiness import assess_readiness as actual
        p, plan, candidate, record, request = self.candidate()
        before = self.live_bytes(); changed = False
        changed_path = p if target == 'plan' else candidate/'knowledge/coverage.json' if target == 'candidate_bytes' else candidate/'knowledge/late.md'
        def assess(root, value, **kwargs):
            nonlocal changed
            result = actual(root, value, **kwargs)
            if root == self.t.root:
                self.assertEqual(result['status'], 'READY')
                self.assertTrue((self.t.root/'evidence/reviews/candidate-math.json').is_file())
                changed = True
                if target == 'plan':
                    updated = read_json(p)
                    updated['reader_goals'].append('SYNTHETIC concurrent new reader promise after installation.')
                    self.assertNotEqual(promise_request(updated)[0], request)
                    write_json(p, updated)
                elif target == 'candidate_bytes':
                    updated = read_json(changed_path)
                    updated['questions'][0]['rationale'] += ' SYNTHETIC concurrent candidate revision.'
                    write_json(changed_path, updated)
                else:
                    changed_path.write_bytes(b'SYNTHETIC concurrent new candidate member.\n')
            return result
        with patch('survey_core.readiness.assess_readiness', assess):
            self.t.failcode('REVIEW_INPUT_CHANGED', self.accept, p)
        self.assertTrue(changed)
        self.assertEqual(self.live_bytes(), before)
        self.assertFalse((self.t.root/'evidence/reviews/candidate-math.json').exists())
        self.assertFalse((self.t.root/'evidence/reviews/candidate-coverage.json').exists())
        self.assertFalse(list((self.t.root/'.cache').glob('.review-*')))
        self.assertFalse((self.t.root/'.survey-write.lock').exists())
        # Rollback owns installed files, not the concurrent actor's inputs.
        self.assertTrue(changed_path.is_file())
        if target == 'plan': self.assertNotEqual(promise_request(read_json(p))[0], request)
        elif target == 'candidate_bytes': self.assertIn('concurrent candidate revision', read_json(changed_path)['questions'][0]['rationale'])

    def test_post_install_plan_change_restores_live_bytes(self):
        self.post_install_change('plan')

    def test_post_install_candidate_byte_change_restores_live_bytes(self):
        self.post_install_change('candidate_bytes')

    def test_post_install_candidate_membership_change_restores_live_bytes(self):
        self.post_install_change('candidate_members')

    def unfinished_matching_candidate(self, target):
        from survey_core.exposition import DEFAULT_AUDIENCE
        from survey_core.reviews import validate_reviews
        p, plan, candidate, record, request = self.candidate(); before = self.live_bytes()
        if target == 'reader':
            plan['audience'] = DEFAULT_AUDIENCE
            plan['reader_goals'] = ['[[PMS_PENDING:reader_goals]] Unfinished synthetic goals.']
            code = 'EXPOSITION_DESIGN_INCOMPLETE'
        else:
            plan['proof_obligations'][0]['required_steps'] = ['[[PMS_PENDING:proof]]']
            record['scope']['proof_steps']['N-main'] = ['[[PMS_PENDING:proof]]']
            code = 'PROOF_OBLIGATION_UNMET'
        write_json(p, plan)
        new_request, data = promise_request(plan)
        self.assertNotEqual(new_request, request)
        target_file = safe(candidate, new_request)
        target_file.parent.mkdir(parents=True, exist_ok=True); target_file.write_bytes(data)
        record['inputs'] = [binding for binding in record['inputs'] if binding['path'] != request]
        record['inputs'].append({'path': new_request, 'sha256': sha(data)})
        record_path = candidate/'evidence/reviews/candidate-math.json'; write_json(record_path, record)
        # Exact projection/hash/checked strings deliberately match the unfinished
        # actual plan. They must not bypass the same authoring rule as template.
        report = self.accept(p)
        self.assertEqual(report['status'], 'NEEDS_WORK')
        self.assertIn(code, {error['code'] for error in report['errors']})
        batch = validate_reviews(self.t.root, [relpath(self.t.root, record_path)], plan)
        self.assertIn(code, {error['code'] for error in batch['errors']})
        self.t.failcode(code, plan_mathematical_template, self.t.root, p, ['N-main'])
        self.assertEqual(self.live_bytes(), before)
        self.assertFalse((self.t.root/'evidence/reviews/candidate-math.json').exists())
        self.assertFalse(safe(self.t.root, new_request).exists())
        self.assertFalse(list((self.t.root/'.cache').glob('.review-*')))
        self.assertFalse((self.t.root/'.survey-write.lock').exists())

    def test_matching_candidate_request_cannot_bypass_unfinished_reader_design(self):
        self.unfinished_matching_candidate('reader')

    def test_matching_candidate_steps_cannot_bypass_pending_proof_prompt(self):
        self.unfinished_matching_candidate('proof')

    def batch_unsafe_binding(self, directory, *, malformed=False):
        from survey_core.reviews import validate_reviews
        p, plan, candidate, record, request = self.candidate()
        alias = self.t.root/'support/alias.md'; alias.parent.mkdir(parents=True, exist_ok=True)
        try: alias.symlink_to(self.t.root/'knowledge/nodes/N-main.md')
        except (OSError, NotImplementedError) as exc: self.skipTest(f'Actual symlink creation unavailable: {exc}')
        unsafe = copy.deepcopy(record)
        unsafe['review_id'] = 'SYNTHETIC-UNSAFE-BATCH-BINDING'
        unsafe['inputs'].append({'path': 'support/alias.md', 'sha256': sha(alias.read_bytes())})
        unsafe_path = directory + '/unsafe-record.json'
        write_json(self.t.root/unsafe_path, unsafe)
        missing = copy.deepcopy(record)
        missing['review_id'] = 'SYNTHETIC-INDEPENDENT-CANONICAL-OMISSIONS'
        missing['scope']['statement_reviews'].pop('N-main')
        missing['scope']['statement_reviews'].pop('N-def')
        missing_path = directory + '/missing-statements.json'
        write_json(self.t.root/missing_path, missing)
        paths = [unsafe_path, missing_path]
        if malformed:
            malformed_path = directory + '/malformed-record.json'
            write_json(self.t.root/malformed_path, {'kind': 'mathematical', 'inputs': [{}]})
            paths.append(malformed_path)
        report = validate_reviews(self.t.root, paths, plan)
        self.assertEqual(report['status'], 'NEEDS_WORK')
        self.assertTrue(any(error['code'] == 'UNSAFE_PATH' and error['path'] == 'support/alias.md'
                            for error in report['errors']))
        omitted = {error['node_id'] for error in report['errors']
                   if error['code'] == 'PRINCIPAL_SELF_CONTAINED_REVIEW_PENDING'}
        self.assertEqual(omitted, {'N-main', 'N-def'})
        self.assertFalse(any(error['code'] == 'PROOF_OBLIGATION_UNMET' for error in report['errors']))
        if malformed:
            self.assertTrue(any(error['code'] == 'CONTRACT_INVALID' and error['path'] == malformed_path
                                for error in report['errors']))

    def test_batch_unsafe_binding_keeps_independent_canonical_omissions(self):
        self.batch_unsafe_binding('.cache')

    def test_stored_unsafe_and_malformed_reviews_keep_independent_canonical_omissions(self):
        self.batch_unsafe_binding('evidence/reviews', malformed=True)

    def test_candidate_capture_change_cannot_rebaseline_old_staged_bytes(self):
        from survey_core.common import file_inventory as actual
        p, plan, candidate, record, request = self.candidate(); before = self.live_bytes()
        changed = False
        def capture(root, paths):
            nonlocal changed
            if root == candidate and not changed:
                changed = True
                coverage = candidate/'knowledge/coverage.json'
                updated = read_json(coverage)
                updated['questions'][0]['rationale'] += ' SYNTHETIC capture-window mutation.'
                write_json(coverage, updated)
            return actual(root, paths)
        with patch('survey_core.common.file_inventory', capture):
            self.t.failcode('REVIEW_INPUT_CHANGED', self.accept, p)
        self.assertTrue(changed)
        self.assertEqual(self.live_bytes(), before)
        self.assertFalse((self.t.root/'evidence/reviews/candidate-math.json').exists())
        self.assertIn('capture-window mutation', read_json(candidate/'knowledge/coverage.json')['questions'][0]['rationale'])
        self.assertFalse(list((self.t.root/'.cache').glob('.review-*')))
        self.assertFalse((self.t.root/'.survey-write.lock').exists())

    def test_writer_conflict_and_partial_install_failure_restore_all_original_bytes(self):
        from survey_core.common import writer, atomic_bytes as actual
        p, plan, candidate, record, request = self.candidate(); before = self.live_bytes()
        with writer(self.t.root): self.t.failcode('WRITER_LOCKED', self.accept, p)
        failed = False
        def write(path, data):
            nonlocal failed
            actual(path, data)
            if path == self.t.root/'evidence/reviews/candidate-math.json' and not failed:
                failed = True
                raise OSError('Synthetic post-write installation failure')
        with patch('survey_core.common.atomic_bytes', write):
            with self.assertRaisesRegex(OSError, 'Synthetic'): self.accept(p)
        self.assertTrue(failed)
        self.assertEqual(self.live_bytes(), before)
        self.assertFalse(list((self.t.root/'.cache').glob('.review-*')))
        self.assertFalse((self.t.root/'.survey-write.lock').exists())


    def test_unfinished_author_promises_do_not_create_a_request(self):
        p, plan = self.detailed_plan()
        plan['proof_obligations'][0]['required_steps'] = ['PENDING: perform a real derivation']
        write_json(p, plan)
        request, data = promise_request(plan)
        self.t.failcode('PROOF_OBLIGATION_UNMET', plan_mathematical_template, self.t.root, p, ['N-main'])
        self.assertFalse(safe(self.t.root, request).exists())
        plan['proof_obligations'][0]['required_steps'] = [v.STEP]
        plan['reader_goals'] = ['[[PMS_PENDING:reader_goals]] Unfinished authoring prompt']
        write_json(p, plan)
        self.t.failcode('EXPOSITION_DESIGN_INCOMPLETE', plan_mathematical_template, self.t.root, p, ['N-main'])


if __name__ == '__main__': unittest.main()
