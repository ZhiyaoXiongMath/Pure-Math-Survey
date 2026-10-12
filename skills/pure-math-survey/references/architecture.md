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

## Daily-use main and bounded cooperation

The daily-use main owns the user's mathematical scope and live knowledge project;
it differs from a development-stage main updating this software. At startup save the
full request/latest corrections, required branches, reader operations, requested outputs,
actual project revision (commit or fixed file hashes), snapshot, allowed sources,
write boundaries, authored materials, historical reviews and outstanding gaps.

Delegate only useful bounded work with actual available tools and current authorization:
source reading, paired fast/slow candidate writing, read-only knowledge review, writing
from an accepted snapshot, mathematical/exposition review or inspection of the actual PDF.
Use isolated candidate files/patches; the main is the sole integration writer of live
KB/plan/manuscript. Pair writers on the same canonical/interface and have them check
both directions. Without suitable tools/authorization, main performs the same duties
serially and reports the actual roles; no invented dispatch, scheduler or database.

Persist task intent/input revision, role, source scope, owned candidate path, expected
files, acceptance tasks and limitations before dispatch. Record actual tool/task IDs;
use bounded waits and independent work, then read terminal state and returned files.
Creation, progress messages and elapsed time do not demonstrate completion. On acceptance
check revision, scope, hashes/files, sources, canonical consistency, fast/slow entrances,
independently reconstructed obligations and actual task answers. Reject stale revisions
and report specific repairs. Main accepts and integrates candidates serially, then
reviews/freezes a new snapshot. Knowledge-only ends without article prepare; requested
articles alone proceed from that accepted snapshot to design, writing and final review.

Resolve text conflicts in order; mathematical hypotheses/conclusion/interface conflicts
return to sources, never majority vote or completion order. New facts and reusable
explanations discovered while writing return to knowledge/review/new snapshot. Preserve
old reviews; changed consumed input makes current evidence stale and needs actual rereading,
not edited hashes or accepted fields. Existing invalidation is file-granular. A layout-only
edit still changes bound output inputs and requires current semantic/visual evidence.

On failure/unknown state read files and actual task status before retry or takeover.
Freeze the former writer before assigning overlapping work; late results remain isolated
candidates, never overwrite accepted inputs. On user stop cease dispatch, stop writes as
tools allow, accurately record still-running tasks and save revision/candidates/remaining
work; do not assume every task stopped or start scheduled continuation. Recovery/handoff
first reconciles actual files, old task states and authority before continuing.

Keep request/corrections, revisions, snapshots, candidates, states, task answers, source
locators, product/evidence hashes, remaining work and next step in accessible project notes
or private evidence files so chat loss is recoverable. A chat link alone is insufficient.
Do not pass unnecessary private directories, raw full chats or restricted source texts
to workers or public bundles. Distinguish access from redistribution permission.

### Bounded task and receipt notes (not CLI commands or new typed schemas)

Task: main/role/ID; full user branches and this scope; fixed revision/canonical/source
versions; reader operations; exact imports; allowed read/isolated-write paths; expected
files/patch and hashes; fast/slow subsection links; reverse-obligation audit; actual
reconstruction/reproduction/condition task; unresolved scope; stop/late-result boundary.

Receipt: actual terminal state; returned revision/files/hashes; read/retested scope;
canonical/condition consistency; bidirectional entrances; missing obligations and actual
task answers; all user branches; accepted serial integration or specific rejection;
new revision/snapshot and affected bindings; limitations/next step. PDF tasks additionally
need actual PDF, corresponding TeX/build logs and hashes. No blank template grants acceptance.

Report software, mathematics, exposition tasks, PDF observations and real-reader feedback
separately. Team/AI review is not external independent review or evidence that students
learned. Parallel coordination and genuine mathematical understanding need separate
verification; a serial environment cannot claim the parallel route was exercised.
