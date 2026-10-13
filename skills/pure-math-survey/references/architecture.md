# Knowledge and output architecture (v2)

`project.json`, `scope.md`, readable nodes and sources are authoritative. Knowledge exists independently of outputs. `overview.md` synthesizes the connections rather than listing files. Facets are overlapping views; principal importance is relative to the question in an output plan.

Nodes own their exact canonical statements and typed links. Sources own identity/version/access. Plans own audience, selections and proof promises. Manuscripts own explanation, wrappers and labels; generated fragments and indexes are never a second editable authority. `uses_definition` and `proof_input` are necessary dependencies. `explained_by` participates when explanation is promised; `explains`, `compares_with`, `specializes`, `refutes` are navigation, not a substitute for mathematical evidence. Definition/proof cycles are rejected; reciprocal explanation navigation is legal.

Scope and conventions are consumed by each output. An unconsumed independent node does not cause output invalidation. Shared scope/overview/coverage are file-granular, so a change to a consumed shared file conservatively requires review even when a human judges it editorial. `consume_overview: false` is allowed when the output genuinely does not consume it. Reuse fixed input for reproducibility; adopting new knowledge requires a new snapshot and explicit plan update.

## Project map and article contract

Read overview.md and reader-calibration.md in these references. The knowledge overview
is the multi-question, multi-route mathematical map, not an index or a Minimal section.
An output outline selects this reader's points, decisive connections and proof-detail
choices. Teaching order is not identical to dependency order. These layers share one
canonical node authority; new mathematics discovered in either returns to the KB.

The incremental profiles.py module holds current r4 editorial policy, plan constraints
and evidence checks. It is not a second knowledge store or mathematical reasoner.
Existing source, snapshot, material-integrity, build, review and package mechanisms remain.
New output/review contracts coexist with unchanged schema-2.0.0 knowledge and snapshots.

## Calling controller and bounded workers

The actual human invocation is the controller, preserving its model/effort. A dispatched `role=worker` task stays a worker without recursive creation. Read [dispatch](dispatch.md), [worker](worker.md) and [user authorization wording](user-start.md) for the installed role contract and actual Codex calls. Every product worker is created through create_thread with gpt-6-astra/ultra. Missing authorization, tools or model support blocks dispatch; serial role playing is not equivalent.

Every dispatch includes the exact human/parent read boundary plus permitted installation resources, original sources, fixed project/snapshot files and owned output paths. Workers enforce that boundary before loading helpers. Do not confuse a same-named-global-skill ban with an all-global ban, or use global PDF instructions to cross a real blanket ban. The installed native layout-and-build workflow supports actual source rendering, all-page article inspection and rebuild evidence.

The controller alone integrates canonical live KB and shared indexes; workers own separate candidate/output/review directories. Persist request/corrections, fixed installed/input identities, scope/reader, real parent/child IDs, requested/readable configuration, states, artifacts and acceptance in private ordinary files. Deduplicate before creation and reconcile unknown/pending receipts before retry. Resume applicable interrupted work. Accept only completed real tasks with inspected current files and non-author critical review; an accepted-shaped record is not mathematical truth.

Resolve hypothesis/conclusion conflicts against sources, not majority vote or completion order. New reusable explanations and mathematical corrections return to reviewed live KB and a new snapshot. Integration changing reviewed mathematics requires fresh corresponding review. Evidence remains file-bound; refreshed hashes cannot replace actual reading. Historical bytes and accepted records retain their identity.

Coordinate every planned output's exact reader and proof promises early. Non-author knowledge review performs the specified steps and records only actually checked exact scope.proof_steps with findings/locators/gaps. Safe plan-derived promise evidence and its declared source/KB inputs belong in fresh live evidence before freeze; mutable output paths are not frozen evidence dependencies. Adopt the new snapshot explicitly before prepare. Current r4 only is supported; old/unknown policy is rejected without modifying its files. Immutable file protection is not old-version runtime compatibility.

On user stop or a configured limit, cease dispatch, send authorized stop messages, save remaining work and quarantine late results. Report still-running chats when immediate interruption is unavailable. Recovery reconciles ledger, files and actual task state; it does not reset iteration limits or perform an entire already-applicable reception again. Private task records and restricted sources do not belong in public software/article bundles.

The CLI handles files, integrity, builds and validation; the calling chat orchestrates through actual host tools. There is no model API server, resident scheduler or Research Studio bridge. Report software, source/mathematics, exposition attempts, actual PDF observations and real-reader feedback separately. AI non-author review is not external peer review or proof of student learning.
