# Proof responsibility is mode-specific

A mechanism node states inputs/dependencies, the constructed or estimated object,
actual decisive operations, output, next use and imported inputs. A typed relation edge
does not prove an implication: give the variable mapping and argument in a reviewed
node. New deductions discovered in an outline return to the KB.

A plan's `proof_obligations` names a selected node, treatment
`complete / sketch / mechanism`, exact `required_steps`, and `imported_inputs`.
Generated PENDING prompts are not actual steps and block formal readiness. The KB
mathematical review covers those exact promises; the output review supplies a substantive
finding and actual location for every promised step, not only one general proof checkbox.
A complete claim needs complete obligations. Imported inputs must be selected or explicitly
scoped prerequisites, with accurate source versions and mathematical interfaces.

## Form promises before output-specific knowledge review

Controller, knowledge authors and authors of all requested outputs coordinate concrete reader capabilities, selected goals and exact proof treatment/steps/imports before the first output-specific non-author knowledge review. A preparatory snapshot may be necessary to create actual plans with `output plan`; it fixes candidate bytes and does not grant readiness. Complete those plans without preparing manuscripts yet. Minimal, Thematic and Lecture may share a KB but require different step evidence.

Controller creates the pending requests at permitted project evidence paths before dispatching the non-author review. It passes the returned request, fixed template and allowed source/KB inputs to the reviewer; the reviewer writes only owned candidate evidence and controller integrates the actual result. Do not run a helper whose implicit request-output path falls outside that worker's actual write boundary. For each actual current plan, the installed helper interface is:

```sh
python scripts/survey.py review template PROJECT --kind mathematical --id N-RESULT --id N-BRIDGE --plan outputs/ID/plan.json --to evidence/reviews/NEW.json --json
```

Use actual node IDs and a fresh owned evidence path; `--plan` applies only to mathematical review. The helper returns `artifacts.promise_request`, a content-addressed `evidence/p/<fullSHA256>.json` containing the plan's mathematical/reader promise projection. Its payload includes output_id so the request remains output-specific. It excludes snapshot_id, preserves earlier requests and binds actual live source/KB inputs. Use the actual returned path rather than constructing a longer filename. If those bytes differ from the plan's candidate snapshot, PLAN_KNOWLEDGE_CHANGED requires explicit knowledge/plan reconciliation; do not overwrite hashes or silently assume equivalence.

The produced review is pending: `scope.proof_steps` is empty per node and canonical statement findings are not_performed. Neither the request nor template grants accepted status or proves any step. The actual non-author uses independent_review and a real reviewer identity, first reconstructs necessary obligations, then performs every specified substantive construction/calculation/interface check. Record **exact step strings actually checked** in scope.proof_steps with source/KB locators, attempted reasoning, conditions, failures and unchecked scope; do not blindly copy labels. Its scope.output_ids and bound promise request constrain this reading to the actual output contract; another mode's acceptance does not silently cover it.

Controller integrates fresh current evidence into live KB. Freeze a new snapshot containing the safe declared input closure, explicitly adopt its actual ID in yet-unprepared plans with unchanged reviewed promises, run readiness and then prepare. The excluded snapshot_id keeps the request projection stable during this adoption. Do not put mutable output plans into frozen review dependencies, edit an existing snapshot, regenerate an old accepted record or manually refresh its hashes. Missing proof/source support remains a failure, not a new route to draft or weakened promises. Any combined feedback/recheck allowance belongs to the task and applies across this process; no extra revision channel or permanent product cap is introduced.

| Mode | Proof responsibility |
|---|---|
| Minimal | Show the decisive point-to-result calculations/constructions; routine interiors may be compressed. Exact external inputs must not be disguised as independent proofs. |
| Thematic | Explain each selected route's mechanism and all nontrivial comparison claims; do not assert equivalence across mismatched assumptions. |
| Lecture | Develop every promised substantive calculation, estimate and limiting argument so it can be reproduced; disclose imported deep theorems and their exact use. |
| Paper | Every original principal has its own complete proof obligation, established authorized derivation, prior-result/comparison records and contribution review. All essential gaps block formal publication. |

Read fast and slow routes in both directions. Uniform constants, admissibility,
noncollapse, parameter branches, regularity, boundary conditions and convergence topology
cannot be removed merely because their proofs are technical. A new exercise needs a
checked solution or an explicit research-problem status. A model should actually execute
the method and test a real boundary. Finite numerical checks are not universal proofs.

Paper's originality check is not the same as proof closure. A correct proof of a known
result is useful in Lecture but is not thereby an original research contribution.
`DRAFT_UNVERIFIED` is the only path for unchecked or incomplete proposed contributions.

## Reverse obligation audit and exact imports

Before accepting the supplied step list, derive necessary work from the full target,
declared reader operations and actual materials. Compare afterward to find missing
object identifications, normalization, singular starts, parameter uniformity,
topology/regularity, endpoints and hypothesis consumption. Add omissions to the real
design/body responsibilities and then locate them; valid locations for an incomplete
list do not close the proof or learning route.

An exact deep theorem can be imported with attribution, scope and assumption checks.
Its present substitution, object conversion and output use may be the decisive bridge:
do not black-box these or relabel treatment as citation to avoid the reader's task.
Perform fast reconstruction, a concrete slow derivation and a condition-change test,
saving actual attempts, failures and repairs. A route failing is not proof the theorem
is false. Knowledge-only uses real node/route review findings, never an article created
to obtain locations; article records bind their actual substantive body.


## Review handoff and candidate acceptance

Finish the concrete plan's audience, reader goals and exact required_steps before
requesting review; generated authoring prompts are rejected. Author the actual
outline/design as part of the writing responsibility. The request is the existing
promise_projection of that plan, with one stable content-addressed identity;
changing snapshot_id alone does not change the promises. Do not handwrite a second
version of the promise list or treat template generation as reading.

```sh
python scripts/survey.py review template PROJECT --kind mathematical --id N-RESULT --plan outputs/ARTICLE/plan.json --to evidence/reviews/NEW.json --json
python scripts/survey.py review validate PROJECT --record evidence/reviews/NEW.json --record evidence/reviews/NEW-COVERAGE.json --plan outputs/ARTICLE/plan.json --json
```

Mathematical templates include applicable canonical statements in the requested
node's necessary dependency/comparison scope, not only principal answers. They
leave the actual reviewer, date, statement findings, checked proof_steps and
local-derivation evidence_basis unfinished. Source templates expose original-text
reading mode, version and locators. Coverage templates identify all four knowledge
checks; real findings cite bound knowledge subsections. A nonauthor reconstructs
obligations and records only actions actually checked, with source/KB locations
and gaps. A separate AI task is not external peer review.

Batch validation uses the same field, binding, statement, proof and coverage rules.
It reports independent omissions across records and scope nodes; stale records
report binding failures before dependent proof-step consequences. --plan requires
plan-specific mathematical candidates to identify the actual output, bind the
exact generated request and name the actual independent reviewer. Validation is
mechanical evidence checking, not mathematical acceptance.

Prepare candidate files in a project-local .cache/CANDIDATE directory whose
members mirror project-relative paths. Generate and perform reviews against a
complete working view of the final candidate knowledge, source and coverage bytes;
do not refresh old accepted hashes. When mathematics changes, first align the
authored preparatory snapshot and plan in that working project before generating
the request. Copy only the resulting changed knowledge and fresh evidence members
into the candidate directory. Review records and promise requests must use new
paths; historical evidence and snapshots cannot be replaced. Supported candidate
members are under the declared knowledge root, evidence/reviews, evidence/p or
evidence/source-checks. Project/scope, outputs, snapshots, symlinks, traversal,
deletions and arbitrary project files are excluded.

```sh
python scripts/survey.py review accept PROJECT --candidate .cache/CANDIDATE --plan outputs/ARTICLE/plan.json --json
python scripts/survey.py kb freeze PROJECT --json
# Explicitly update the existing plan's snapshot_id to the returned reviewed snapshot.
python scripts/survey.py kb readiness PROJECT --plan outputs/ARTICLE/plan.json --json
python scripts/survey.py output prepare PROJECT --plan outputs/ARTICLE/plan.json --json
```

Accept stages a combined final byte view, batch-checks its fresh review records
and runs existing readiness against that live view. It holds the existing writer
lock, compares the plan/candidate/live inputs for concurrent changes, checks final
installed bytes, and restores touched files on installation failure. Ordinary
validation failures leave live knowledge/evidence unchanged. It does not freeze,
adopt, prepare, perform reading or turn a Paper eligibility failure into success.
Those responsibilities and PR03's knowledge/Paper separation remain explicit.

## Editorial auxiliaries and their consumers

A reusable precise interface, decisive bottleneck or external theorem's application interface should be stated as a numbered unnamed Lemma/Proposition near and before the proof that first uses it. Separate existence/uniqueness, necessity/sufficiency and independent branches. Explain substitutions and the output passed to the next step. Principal statements may appear in the opening with proofs later; justified forward references must be explicit and traceable. Establishing every auxiliary in one global chain is not required. Existing reviewed derivations may be extracted for exposition without creating redundant canonical nodes; genuinely new facts, hypotheses or comparisons must go back through KB review and freeze. Reordering requires checking labels, proof-target headings and directional prose.
