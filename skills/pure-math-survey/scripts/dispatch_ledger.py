"""Private controller bookkeeping, not a chat dispatcher or mathematical reviewer.

Apply a JSON action with: python dispatch_ledger.py LEDGER ACTION.json
Only the controller writes this file. Host receipts and actual readings remain
external evidence; this helper checks local identities, files and transitions.
"""
import hashlib
import json
import os
from pathlib import Path
import sys

MODEL = "gpt-6-astra"
EFFORT = "ultra"
ROLES = {"source", "knowledge_author", "knowledge_review", "writer", "math_review", "pdf_review"}
REVIEW_ROLES = {"knowledge_review", "math_review", "pdf_review"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def required(data, names):
    for name in names:
        if not isinstance(data.get(name), str) or not data[name].strip():
            raise ValueError("missing nonempty " + name)


def hash_value(value):
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("input identity must be a lowercase SHA-256")


def within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def initialize(action):
    if action.get("caller_role") != "controller":
        raise ValueError("only controller may initialize dispatch bookkeeping; worker must not recurse")
    required(action, ("invocation", "parent_thread_id", "installed_identity", "project", "canonical_root"))
    auth = action.get("authorization", {})
    required(auth, ("human_text", "source", "scope"))
    if auth.get("create_chats") is not True or auth.get("parent_messages") is not True:
        raise ValueError("record the human's chat-creation and parent-message authorization")
    # These fields record the controller's verified source; text is not self-authorizing.
    return {"format": "pms-private-dispatch-v1", "invocation": action["invocation"],
            "parent_thread_id": action["parent_thread_id"], "installed_identity": action["installed_identity"],
            "project": action["project"], "canonical_root": str(Path(action["canonical_root"]).resolve()),
            "authorization": auth, "stopped": False, "tasks": {}}


def artifacts(task, entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError("completed task needs actual artifact files")
    result = []
    for item in entries:
        required(item, ("path", "sha256"))
        path = Path(item["path"]).resolve()
        if not within(path, Path(task["write_root"])) or not path.is_file():
            raise ValueError("artifact missing or outside owned directory")
        if digest(path) != item["sha256"]:
            raise ValueError("artifact hash mismatch")
        result.append({"path": str(path), "sha256": item["sha256"]})
    return result


def apply(ledger, action):
    operation = action.get("operation")
    if operation == "init":
        if ledger is not None:
            raise ValueError("ledger already exists; resume its invocation")
        return initialize(action), {"status": "initialized"}
    if not ledger or ledger.get("format") != "pms-private-dispatch-v1":
        raise ValueError("initialize the private dispatch ledger first")
    if operation == "status":
        return ledger, ledger
    if operation == "stop":
        required(action, ("reason",))
        ledger["stopped"] = True
        ledger["stop_reason"] = action["reason"]
        for task in ledger["tasks"].values():
            if task["state"] in {"reserved", "unknown", "pending", "running", "paused"}:
                task["state"] = "stop_requested"
        return ledger, {"status": "stop_requested", "running_may_remain": True}
    if operation == "reserve":
        if ledger["stopped"]:
            raise ValueError("stopped invocation cannot dispatch")
        required(action, ("task_id", "project_round", "role", "input_sha256", "output_target", "write_root"))
        if action["role"] not in ROLES:
            raise ValueError("unsupported worker role")
        hash_value(action["input_sha256"])
        if action.get("model") != MODEL or action.get("effort") != EFFORT:
            raise ValueError("all product workers require actual Astra/ultra parameters")
        key = [ledger["project"], action["project_round"], action["role"], action["input_sha256"], action["output_target"]]
        for task_id, task in ledger["tasks"].items():
            if task["key"] == key:
                return ledger, {"status": "reuse_or_reconcile", "task_id": task_id, "state": task["state"]}
        if action["task_id"] in ledger["tasks"]:
            raise ValueError("task ID already belongs to another intent")
        root = Path(action["write_root"]).resolve()
        canonical = Path(ledger["canonical_root"])
        if within(root, canonical) or within(canonical, root):
            raise ValueError("worker must not own canonical integration directory")
        for task in ledger["tasks"].values():
            other = Path(task["write_root"])
            if within(root, other) or within(other, root):
                raise ValueError("worker write directories must be exclusive")
        subject = action.get("subject_task_id")
        if action["role"] in REVIEW_ROLES and subject not in ledger["tasks"]:
            raise ValueError("review intent must identify its existing subject task")
        ledger["tasks"][action["task_id"]] = {"key": key, "role": action["role"], "input_sha256": action["input_sha256"],
            "write_root": str(root), "output_target": action["output_target"], "subject_task_id": subject,
            "requested_model": MODEL, "requested_effort": EFFORT, "actual_configuration": None,
            "state": "reserved", "thread_id": None, "client_thread_id": None, "artifacts": [], "acceptance": None}
        return ledger, {"status": "reserved", "task_id": action["task_id"]}
    required(action, ("task_id",))
    task = ledger["tasks"].get(action["task_id"])
    if task is None:
        raise ValueError("unknown task ID")
    if operation == "receipt":
        if ledger["stopped"]:
            raise ValueError("stopped invocation cannot reconcile into active work")
        state = action.get("state")
        if state not in {"unknown", "pending", "running"}:
            raise ValueError("receipt state must be unknown, pending or running")
        if task["state"] not in {"reserved", "unknown", "pending"}:
            raise ValueError("receipt already resolved")
        if state == "running":
            required(action, ("thread_id",))
            if action["thread_id"] in {task.get("client_thread_id"), action.get("client_thread_id")}:
                raise ValueError("clientThreadId cannot stand in for real threadId")
            subject = ledger["tasks"].get(task["subject_task_id"])
            if subject and action["thread_id"] == subject["thread_id"]:
                raise ValueError("critical review must be a non-author chat")
            task["thread_id"] = action["thread_id"]
        elif state == "pending":
            required(action, ("client_thread_id",))
            task["client_thread_id"] = action["client_thread_id"]
        task["state"] = state
        task["actual_configuration"] = action.get("actual_configuration")
        task["parameter_evidence"] = action.get("parameter_evidence", "unavailable")
        actual = task["actual_configuration"]
        if actual is not None:
            if not isinstance(actual, dict):
                raise ValueError("actual_configuration must be an observed object or null")
            if actual.get("model", MODEL) != MODEL or actual.get("effort", EFFORT) != EFFORT:
                task["state"] = "blocked_configuration"
                return ledger, {"status": "blocked_configuration", "thread_id": task["thread_id"]}
        return ledger, {"status": state, "thread_id": task["thread_id"]}
    if operation in {"pause", "resume"}:
        if ledger["stopped"] or not task["thread_id"]:
            raise ValueError("cannot resume stopped or unresolved task")
        if task["state"] not in {"running", "paused"}:
            raise ValueError("only pure interruption of existing work is resumable")
        if action.get("input_sha256") != task["input_sha256"]:
            raise ValueError("changed input is not pure interruption recovery")
        task["state"] = "paused" if operation == "pause" else "running"
        return ledger, {"status": task["state"], "thread_id": task["thread_id"]}
    if operation == "complete":
        if not task["thread_id"] or task["state"] not in {"running", "stop_requested"}:
            raise ValueError("completion needs resolved real task identity")
        if action.get("input_sha256") != task["input_sha256"]:
            raise ValueError("stale input identity")
        if action.get("actual_terminal_state") != "completed":
            raise ValueError("actual terminal completion is required")
        task["artifacts"] = artifacts(task, action.get("artifacts"))
        task["state"] = "late_completed" if ledger["stopped"] else "completed"
        return ledger, {"status": task["state"]}
    if operation == "accept":
        if ledger["stopped"] or task["state"] != "completed":
            raise ValueError("only completed current work can be accepted")
        required(action, ("finding",))
        artifacts(task, task["artifacts"])
        reviewer_id = action.get("reviewer_task_id")
        if task["role"] in {"knowledge_author", "writer"}:
            reviewer = ledger["tasks"].get(reviewer_id)
            required_role = "knowledge_review" if task["role"] == "knowledge_author" else "math_review"
            if not reviewer or reviewer["role"] != required_role or reviewer["subject_task_id"] != action["task_id"]:
                raise ValueError("critical acceptance needs corresponding non-author review")
            if reviewer["state"] not in {"completed", "accepted"} or reviewer["thread_id"] == task["thread_id"]:
                raise ValueError("review must be actually complete in a non-author chat")
            artifacts(reviewer, reviewer["artifacts"])
        task["acceptance"] = {"reviewer_task_id": reviewer_id, "finding": action["finding"]}
        task["state"] = "accepted"
        return ledger, {"status": "accepted", "mathematical_truth_verified_by_helper": False}
    raise ValueError("unsupported action")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("usage: dispatch_ledger.py LEDGER ACTION.json", file=sys.stderr)
        return 2
    path, action_path = map(Path, args)
    try:
        ledger = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        action = json.loads(action_path.read_text(encoding="utf-8"))
        ledger, result = apply(ledger, action)
        if action.get("operation") != "status":
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + ".tmp")
            temporary.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(temporary, path)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "blocked", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
