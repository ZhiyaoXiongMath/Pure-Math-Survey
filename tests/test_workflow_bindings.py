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
        item = record['scope']['statement_reviews']['N-main']; item['outcome'] = 'accepted'
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
        self.assertEqual(record['scope']['proof_steps'], {'N-main': []})
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
            self.assertEqual(record['scope']['proof_steps'], {'N-main': []})
            # Explicit synthetic independent record tests consumption only.
            record.update(review_id='SYNTHETIC-DEEP-PLAN', reviewer_mode='independent_review',
                          reviewer='Distinct synthetic reviewer; not an actual mathematical reading',
                          reviewed_at=now(), findings=[v.SYNTH], unchecked_items=[], disposition='accepted')
            record['scope']['proof_steps']['N-main'] = list(plan['proof_obligations'][0]['required_steps'])
            item = record['scope']['statement_reviews']['N-main']; item['outcome'] = 'accepted'
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
        self.assertIn('PAPER_ORIGINAL_CONTRIBUTION_MISSING', self.t.readiness(plan))
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


if __name__ == '__main__': unittest.main()
