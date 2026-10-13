# Controller: actual Codex work chats

The installed skill's human invocation is the controller. Preserve that chat's model and effort. A task explicitly marked `role=worker` remains a worker; it never recursively dispatches. Use [worker instructions](worker.md) and [human start wording](user-start.md). These installed resources are sufficient without a development guide.

## Authorization and supported tools

Read the human's original instruction or trusted, locatable evidence. Save its exact relevant text, source chat/turn identifier and project/role/path/message boundaries in a private project note. A parent assistant's request to relay text is not authorization. The human must have authorized creating work chats and parent-to-worker task/continuation/revision/stop messages; forward that original evidence, not a new assistant-generated grant. Workers normally return through final text and owned files, read by the controller; they have no automatic right to message the parent or other chats.

Every actual dispatch carries the human/parent's accurate read boundary, the installed resource allowlist/root, permitted original-source paths/URLs and fixed versions, read-only project/snapshot inputs, exclusive output/evidence paths and explicit forbidden locations. Do not send a shortened boundary that changes its meaning. Workers apply it before loading any helper workflow. A prohibition on the global copy of the same-named skill is distinct from a prohibition on all global skills; do not turn one into the other. A real all-global ban also covers a generic PDF skill. Prefer the allowed installed [native PDF workflow](layout-and-build.md); report missing permitted capability rather than bypassing a boundary or skipping source/full-page work.

If a host requires explicit new-chat authorization and it is missing, request it once for this project, explaining the host's requirement. Continue independent preparation. Reuse existing authorization within its bounds. Scope expansion requires new authorization only for the actual expansion. Authorization is not implied by reading this resource, opening a file or the default prompt merely existing.

Inspect the current host declarations. Required tools are `create_thread`, `list_projects` for a project destination, `list_threads`/`read_thread`, `wait_threads` and `send_message_to_thread` for authorized continuations. All new product workers use actual `model: "gpt-6-astra", thinking: "ultra"` arguments. Model names in prompt prose do not select a model. Keep user service-speed settings; ultra is an effort value, not a speed guarantee or generic API parameter. Do not assert an unverified account-plan requirement.

For a repository-backed destination call `list_projects` first and use its returned project ID. Choose the authorized local project or projectless destination. Do not create a worktree unless requested. Supply the installed absolute SKILL path and the bounded worker prompt below. An illustrative structured call is:

```json
{
  "model": "gpt-6-astra",
  "thinking": "ultra",
  "title": "Bounded project source reading",
  "target": {"type": "projectless", "directoryName": "owned-project-candidate"},
  "prompt": "role=worker; invocation=<fixed invocation>; parent_thread_id=<real controller ID>; installed_skill=<allowed absolute SKILL path>. Before loading helpers, obey the exact human/parent read boundaries and installed-resource/original-source/output allowlist supplied below; then read allowed references/worker.md. Duty, fixed input identities, all planned reader/proof promises, exclusive candidate directory, expected files, review/stop boundaries and original human authorization evidence follow."
}
```

Replace placeholders with real values before calling. Capture the actual receipt. Tool acceptance of model/effort proves only that parameters were accepted; record readable actual configuration separately or explicitly report it unavailable. Recheck configuration on continuation; pass the same model/effort if an override is needed and supported. An unavailable model, rejected effort, missing tool or missing required authorization blocks dispatch. Keep prepared materials and diagnostics. Controller self-writing, serial role playing, internal agents and lower efforts cannot count as equivalent successful dispatch.

## Bounded work and dependencies

Group useful responsibilities; do not create one chat per command. Source readers extract exact statements, assumptions, quantifiers, proof interfaces, locators and unread scope. Knowledge authors produce paired fast/slow candidates on one canonical authority while each requested output's authors coordinate its concrete reader/proof promises. Create preliminary authored plans from a preparatory snapshot if the CLI needs one; freeze does not imply readiness. A non-author knowledge reviewer receives all applicable promises before output-specific review, reconstructs routes, actually performs each required step and audits conditions. Controller serially integrates live KB and fresh reviewed evidence, freezes the final authoring snapshot and explicitly adopts it before prepare. Writers then consume only that reviewed fixed snapshot and their profile/view. Non-author mathematical/exposition and PDF/package review can share one chat when inputs are compatible. Deterministic builds, hashes and file checks can run directly in the controller.

Each worker receives fixed scope, accurate read boundaries, reader capabilities, actual source/input hashes, owned write paths, expected files, acceptance responsibilities and stop boundary. Before final knowledge review, controller and authors expose every planned output's precise reader/proof promises, not merely its profile name. Non-author reviewers check each exact required step through actual source/KB work and return fresh evidence with `scope.proof_steps`, findings and gaps; no automatic accepted labels. Controller alone integrates canonical live KB and new evidence, freezes a new snapshot and explicitly adopts it in the plan before prepare. Authors own distinct candidate/output directories; reviewers own distinct evidence directories. Integration changing reviewed mathematics requires affected fresh non-author review within the existing authorized feedback/recheck allowance. Independent chat identity establishes author separation, not truth or external peer review.

## Deduplication, receipts and recovery

Keep a lightweight private ledger outside public article/software packages. Record invocation, installed/candidate identity, project/round, duty, fixed input hash, output target, parent/child IDs, requested parameters, readable actual configuration, paths, status, artifacts and acceptance. The optional `scripts/dispatch_ledger.py` checks local bookkeeping; it does not create chats, verify human authority, model configuration or mathematics.

To use the helper, save a UTF-8 JSON action and run `python scripts/dispatch_ledger.py PRIVATE_LEDGER.json ACTION.json`. It writes the ledger atomically; only the controller calls it. Each action has `operation` and the fields below. IDs/configuration must come from actual host receipts, not the unit-test fixtures. The helper's authorization object records the controller's verification, never generates a grant.

| Operation | Required content |
|---|---|
| init | caller_role=controller; invocation, real parent_thread_id, installed_identity, project, canonical_root; authorization with human_text, source, scope, create_chats=true and parent_messages=true. |
| reserve | task_id, project_round, role, input_sha256, output_target, exclusive write_root, model=gpt-6-astra and effort=ultra. Reviewer roles also name subject_task_id. |
| receipt | task_id and state=unknown/pending/running; pending has client_thread_id, running has real thread_id. Add parameter_evidence and actual_configuration (observed model/effort fields or null). A known mismatch blocks completion. |
| pause / resume | task_id and unchanged input_sha256; resume keeps the resolved thread. |
| complete | task_id, unchanged input_sha256, actual_terminal_state=completed and artifacts as existing owned path/sha256 pairs. |
| accept | task_id, concrete finding and, for knowledge_author/writer, a completed corresponding non-author reviewer_task_id. Rechecks actual artifact hashes; the finding is the controller's responsibility. |
| stop | reason; records stop_requested and isolates late completion without claiming chats were interrupted. |
| status | Reads the current ledger. |

Roles are source, knowledge_author, knowledge_review, writer, math_review and pdf_review. The helper has no dispatch tool or worker entry, no mathematical schema fields and no automatic acceptance. Richer source/refusal/error notes can remain in private project notes; do not manufacture new schema fields merely to use it.

Before creation match **project/round + duty + input identity + output target** against running, pending, unknown or reusable completed work. Persist intent before the call. If creation's outcome is unknown, inspect existing chats and reconcile by intent/parent/input before retry; never repeat blindly. A `clientThreadId` is temporary. Resolve setup via actual host status/list/read receipts and obtain the real `threadId` before waits/messages; do not pass a client ID as a thread ID. If the host cannot resolve it, report pending/blocker and preserve intent.

Use `wait_threads` with real IDs and cursors, bounded waits and useful independent work. Read final state and actual returned files. Completed status alone is insufficient: verify input/install identity, scope, expected artifacts and hashes, source support, canonical/fast/slow consistency and non-author acceptance before advancing dependencies. Do not wake busy workers repeatedly. For same-input pure interruption reconcile files and current task state, then resume the original authorized chat. Changed rules, sources or content requirements create a new input identity, with a new round only when the user's test protocol requires it; never reset a configured limit by switching chats or machines.

## Stop and late results

Honor user pause/stop and any explicit iteration boundary. Stop dispatch, save state, and send stop instructions to authorized active workers. If tools cannot interrupt a running chat immediately, list it as still running; do not claim it stopped. Late results remain isolated and cannot enter a stopped candidate. Resume only after a human resumption and reconcile task/file state. Do not create a background automation unless requested. Product daily use has no universal three-round limit; a finite limit from the user's specific testing task must persist and cannot be silently expanded.
