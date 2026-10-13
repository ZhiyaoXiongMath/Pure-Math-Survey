"""Bookkeeping regressions; no simulated receipt is real dispatch evidence."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/pure-math-survey/scripts/dispatch_ledger.py"
SPEC = importlib.util.spec_from_file_location("pms_dispatch_ledger", SCRIPT)
dispatch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dispatch)


class DispatchBookkeepingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.identity = "1" * 64
        self.ledger, _ = dispatch.apply(None, {
            "operation": "init", "caller_role": "controller", "invocation": "test-invocation", "parent_thread_id": "test-parent",
            "project": "test-project", "canonical_root": str(self.root / "knowledge"),
            "installed_identity": "test-only-install-identity",
            "authorization": {"human_text": "test fixture, not an authorization grant", "source": "test-only",
                              "scope": "unit-test fixture", "create_chats": True, "parent_messages": True}})

    def action(self, operation, **kwargs):
        self.ledger, result = dispatch.apply(self.ledger, {"operation": operation, **kwargs})
        return result

    def reserve(self, name="author", role="knowledge_author", **kwargs):
        action = {"task_id": name, "project_round": "project-1", "role": role,
                  "input_sha256": self.identity, "output_target": name,
                  "write_root": str(self.root / name), "model": dispatch.MODEL, "effort": dispatch.EFFORT}
        action.update(kwargs)
        return self.action("reserve", **action)

    def start(self, name="author", thread="test-author-thread"):
        return self.action("receipt", task_id=name, state="running", thread_id=thread,
                           parameter_evidence="synthetic test receipt")

    def complete(self, name="author"):
        target = Path(self.ledger["tasks"][name]["write_root"]) / "result.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("Unit fixture only; not a mathematical acceptance.\n", encoding="utf-8")
        return self.action("complete", task_id=name, input_sha256=self.identity,
                           actual_terminal_state="completed", artifacts=[{"path": str(target), "sha256": dispatch.digest(target)}])

    def test_authorization_missing_and_wrong_effort_block(self):
        with self.assertRaises(ValueError):
            dispatch.initialize({"caller_role": "controller", "invocation": "i", "parent_thread_id": "p", "project": "x",
                                 "canonical_root": str(self.root), "installed_identity": "install",
                                 "authorization": {"human_text": "text", "source": "s", "scope": "x"}})
        with self.assertRaises(ValueError):
            self.reserve(effort="xhigh")
        self.assertEqual(self.ledger["tasks"], {})

    def test_worker_cannot_initialize_controller_and_observed_downgrade_blocks(self):
        with self.assertRaises(ValueError):
            dispatch.initialize({"caller_role": "worker"})
        self.reserve()
        result = self.action("receipt", task_id="author", state="running", thread_id="actual-test-thread",
                             actual_configuration={"model": dispatch.MODEL, "effort": "xhigh"})
        self.assertEqual(result["status"], "blocked_configuration")
        self.assertEqual(self.ledger["tasks"]["author"]["thread_id"], "actual-test-thread")
        with self.assertRaises(ValueError):
            self.complete()

    def test_dedup_reuses_pending_and_unknown_intent(self):
        self.reserve()
        self.action("receipt", task_id="author", state="unknown")
        result = self.reserve(name="duplicate", output_target="author", write_root=str(self.root / "duplicate"))
        self.assertEqual(result["task_id"], "author")
        self.action("receipt", task_id="author", state="pending", client_thread_id="temporary-client")
        result = self.reserve(name="duplicate", output_target="author")
        self.assertEqual(result["state"], "pending")
        self.assertEqual(len(self.ledger["tasks"]), 1)

    def test_pending_client_id_cannot_become_thread_id(self):
        self.reserve()
        self.action("receipt", task_id="author", state="pending", client_thread_id="temporary-client")
        with self.assertRaises(ValueError):
            self.start(thread="temporary-client")
        with self.assertRaises(ValueError):
            self.complete()
        self.start()
        self.assertEqual(self.ledger["tasks"]["author"]["actual_configuration"], None)

    def test_single_writer_and_exclusive_candidates(self):
        with self.assertRaises(ValueError):
            self.reserve(write_root=str(self.root / "knowledge" / "candidate"))
        self.reserve()
        with self.assertRaises(ValueError):
            self.reserve(name="other", write_root=str(self.root / "author" / "nested"))

    def test_same_input_interruption_resumes_original_chat(self):
        self.reserve()
        self.start()
        self.action("pause", task_id="author", input_sha256=self.identity)
        result = self.action("resume", task_id="author", input_sha256=self.identity)
        self.assertEqual(result["thread_id"], "test-author-thread")
        with self.assertRaises(ValueError):
            self.action("resume", task_id="author", input_sha256="2" * 64)

    def test_non_author_review_required_and_actual_files_checked(self):
        self.reserve()
        self.start()
        self.complete()
        with self.assertRaises(ValueError):
            self.action("accept", task_id="author", finding="not enough")
        self.reserve(name="review", role="knowledge_review", subject_task_id="author")
        with self.assertRaises(ValueError):
            self.start(name="review", thread="test-author-thread")
        self.start(name="review", thread="test-review-thread")
        self.complete(name="review")
        result = self.action("accept", task_id="author", reviewer_task_id="review", finding="unit-test assertion only")
        self.assertFalse(result["mathematical_truth_verified_by_helper"])

    def test_changed_artifact_cannot_gain_acceptance(self):
        self.reserve(role="source")
        self.start()
        self.complete()
        artifact = Path(self.ledger["tasks"]["author"]["artifacts"][0]["path"])
        artifact.write_text("Changed since completion", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.action("accept", task_id="author", finding="stale artifact")

    def test_review_accepted_before_author_remains_valid_acceptance_input(self):
        self.reserve()
        self.start()
        self.complete()
        self.reserve(name="review", role="knowledge_review", subject_task_id="author")
        self.start(name="review", thread="test-review-thread")
        self.complete(name="review")
        self.action("accept", task_id="review", finding="review receipt inspected in unit fixture")
        self.assertEqual(self.ledger["tasks"]["review"]["state"], "accepted")
        result = self.action("accept", task_id="author", reviewer_task_id="review", finding="unit-test assertion only")
        self.assertEqual(result["status"], "accepted")
        self.assertFalse(result["mathematical_truth_verified_by_helper"])

    def test_accepted_review_still_requires_unchanged_artifact(self):
        self.reserve()
        self.start()
        self.complete()
        self.reserve(name="review", role="knowledge_review", subject_task_id="author")
        self.start(name="review", thread="test-review-thread")
        self.complete(name="review")
        self.action("accept", task_id="review", finding="review receipt inspected in unit fixture")
        artifact = Path(self.ledger["tasks"]["review"]["artifacts"][0]["path"])
        artifact.write_text("Changed after review acceptance", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.action("accept", task_id="author", reviewer_task_id="review", finding="stale review cannot support author acceptance")

    def test_stop_preserves_late_result_but_blocks_acceptance_and_dispatch(self):
        self.reserve(role="source")
        self.start()
        result = self.action("stop", reason="human stop in fixture")
        self.assertTrue(result["running_may_remain"])
        self.assertEqual(self.complete()["status"], "late_completed")
        with self.assertRaises(ValueError):
            self.action("accept", task_id="author", finding="late")
        with self.assertRaises(ValueError):
            self.reserve(name="later")

    def test_stale_input_and_missing_file_completion_block(self):
        self.reserve()
        self.start()
        with self.assertRaises(ValueError):
            self.action("complete", task_id="author", input_sha256="2" * 64, actual_terminal_state="completed", artifacts=[])
        with self.assertRaises(ValueError):
            self.action("complete", task_id="author", input_sha256=self.identity, actual_terminal_state="completed",
                        artifacts=[{"path": str(self.root / "author" / "missing.md"), "sha256": self.identity}])


if __name__ == "__main__":
    unittest.main()
