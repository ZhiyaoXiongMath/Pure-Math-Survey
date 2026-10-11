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

The incremental profiles.py module holds versioned editorial policy, plan constraints
and evidence checks. It is not a second knowledge store or mathematical reasoner.
Existing source, snapshot, material-integrity, build, review and package mechanisms remain.
New output/review contracts coexist with unchanged schema-2.0.0 knowledge and snapshots.
