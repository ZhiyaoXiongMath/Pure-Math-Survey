# Native file fields and reproducible operations

The software runtime is `2.1.0`. Project, knowledge, sources, snapshots and generated/build manifests retain schema `2.0.0`. Current output plans and policy-bearing mathematical/output-semantic reviews use schema `2.2.0` and `four-modes-2026-10-15-r5`. This installation supports current r5 only: explicit old/unknown policies or unsupported inputs are rejected without changing their files. Unchanged format numbers do not grant old-policy support or acceptance. See [output review](output-review.md) for whole-manuscript checks, actual body locations and build history. JSON has no duplicate keys or nonfinite numbers. Stable IDs use letters/digits/dot/underscore/hyphen, with N- and S- prefixes for nodes and sources; each filename equals its ID. All project-relative paths are POSIX, contain no traversal/absolute prefix and cross no symbolic links.

## Project and knowledge

project.json: schema_version, project_id, title, language, scope_file, knowledge_root; optional nullable literature_cutoff. Knowledge requires overview.md, conventions.tex, discovery.md, coverage.json. There need not be any output.

Node frontmatter is a JSON object between standalone `---` lines, followed by readable Markdown. Required fields: schema_version, id, kind, title, facets (nonempty), question_ids, mathematical_status, origin, sources, links. Kinds: question/definition/result/relation/mechanism/example/application/frontier. Status: unassessed/established/conjectural/open/refuted/not_applicable. Origin: primary_source/supplied_manuscript/local_derivation. Sources link source_id, exact locator and support/provenance role; optional version must match the controlling source. Relations are uses_definition/proof_input/explained_by/explains/compares_with/refutes/specializes.

A formal node has at most one `## Canonical statement`, containing only one fenced latex block. Definitions/results/relations require it. No theorem/definition/document wrapper, label or external input inside. The literal inner UTF-8 bytes, including internal line endings, are exported unchanged. Metadata titles organize knowledge, not obligatory theorem titles.

Source JSON: schema_version, id, kind (primary/supplied_manuscript), title, authors, publication_status, identifiers, version (explicit text/null), access. Access has state metadata_only/full_text_read, checked_at, material_sha256, local_path (explicit null allowed), optional reading_note. Original online reading without PDF bytes has the extra scoped limitation described in [source evidence](research-and-evidence.md). Unresolved version_conflicts block readiness. Optional bibliography.year supplies an explicit calendar year (1900–2099); otherwise export uses an unambiguous calendar year in version text, never the YYMM prefix of an arXiv identifier. An unavailable year is omitted, not guessed.

Coverage JSON: schema_version, questions. Each question has question_id, answer_nodes, mechanism_nodes, boundary_nodes, gaps, assessment pending/adequate/limited, rationale. An empty boundary list is allowed with substantive scope reasoning. Gap dispositions resolved/outside_explicit_scope require reason; other outstanding important gaps block readiness.

## Plan

Required: schema_version, output_id, snapshot_id, profile, view, language, title, audience, reader_goals, question_ids, prerequisites, selections, omissions, proof_obligations, limits, draft. Optional comparison_group and consume_overview (default true).

Selection: node_id; role principal_answer/essential_bridge/boundary/background/frontier; statement_treatment full/explained_reference; proof_treatment complete/sketch/mechanism/citation/none; reason. Omission: node_id/reason. An explicitly scoped prerequisite is either plain reader background or an object with node_id/scope/reason; only the object can mechanically discharge a specific unselected dependency.

Keep substantively selected question nodes when they express the actual requested target or boundary. Their role/status must describe what the node really asserts; a question/task description is not automatically an established theorem or principal answer. Principal mathematical results retain full canonical statements. Do not delete selected questions, mark unanswered claims established or narrow scope merely to pass validation; follow current kind/role/status diagnostics with truthful evidence.

Proof obligation: node_id, treatment complete/sketch/mechanism, nonempty required_steps, imported_inputs. An expanded proof selection must have step obligations directly or through selected explaining mechanisms. Imported inputs need explicit selection/prerequisite treatment. limits.max_pages is required and nullable; optional page_review_threshold is also nullable. A comparison group shares snapshot/question/core/boundary only when explicitly requested.

All requested output plans expose concrete reader/proof promises before output-specific knowledge review. For a pending plan-scoped request use `review template PROJECT --kind mathematical --id NODE --plan outputs/ID/plan.json --to evidence/reviews/NEW.json --json`. `--plan` is mathematical-only. Its returned artifacts.promise_request names a content-addressed file under evidence/p; it excludes snapshot_id, binds actual live source/KB identity and preserves old requests. The template leaves scope.proof_steps empty and statement findings not_performed. A real non-author supplies exact actually checked steps/findings; scope.output_ids restricts the contract. PLAN_KNOWLEDGE_CHANGED rejects changed live mathematical/source bytes until knowledge and plan are explicitly reconciled. Fresh reviewed live evidence → new snapshot → explicit plan snapshot adoption → readiness/prepare is the sequence, detailed in [proof responsibilities](proofs-and-boundaries.md).

## CLI recipes

```sh
python scripts/survey.py init --output topic --topic topic-id --scope scope-input.md --json
python scripts/survey.py kb validate topic --json
python scripts/survey.py kb index topic --json
python scripts/survey.py kb freeze topic --json
python scripts/survey.py kb verify topic --snapshot KB-FULL_HASH --json
python scripts/survey.py output plan topic --output short --snapshot KB-FULL_HASH --json
python scripts/survey.py review template topic --kind mathematical --id N-RESULT --plan outputs/short/plan.json --to evidence/reviews/NEW.json --json
python scripts/survey.py kb readiness topic --plan topic/outputs/short/plan.json --json
python scripts/survey.py output prepare topic --plan topic/outputs/short/plan.json --draft --json
python scripts/survey.py output validate topic --output short --stage plan --json
python scripts/survey.py output validate topic --output short --stage structure --json
python scripts/survey.py output build topic --output short --json
python scripts/survey.py output render topic --output short --json
python scripts/survey.py output review-template topic --output short --kind output_semantic --to evidence/semantic-review.json --json
python scripts/survey.py output review-template topic --output short --kind visual --to evidence/render-review.json --json
python scripts/survey.py output validate topic --output short --stage release --json
python scripts/survey.py output package topic --output short --to short.zip --json
python scripts/survey.py kb diff topic --from KB-OLD_FULL_HASH --to KB-NEW_FULL_HASH --json
```

These recipes use placeholder IDs. init produces an empty unverified KB; add real scope-specific knowledge, evidence and coverage before a meaningful plan. After output plan, authors complete all concrete promises before the plan-scoped mathematical request. The reviewer performs the actual work; controller integrates fresh evidence, freezes a new snapshot and explicitly adopts its returned ID before readiness/prepare. The code block cannot perform those human/AI readings or plan edits. Prepare makes no mathematical claims and preserves existing prose. Fill review templates only after the actual recorded work. `--draft` permanently marks that plan draft until an explicit reviewed plan change/reprepare; never remove the flag merely to bypass readiness.

## Current r5 output policy (2.2.0)

New r5 plans use `editorial_policy: four-modes-2026-10-15-r5` and `contributions`
(an empty list outside Paper). The `profile` enum is minimal/thematic/lecture/paper.
Each Paper contribution has `node_id`, classification original/known/conjectural/unverified,
`provenance`, `authorization`, `actual_difference`, proof_status complete/incomplete/unverified,
`closest_prior_results`, `comparison_bindings` and `gaps`. Each binding contains
`comparison_node_id` and `prior_result_id`; do not keep a second comparison_nodes list. Classify every principal. Prior
results and comparison relations must be selected or explicitly scoped prerequisites.
These are references and editorial evidence, not another canonical statement store.

New-policy mathematical reviews use scope.editorial_policy and statement_reviews keyed
by principal node. Each entry binds canonical_sha256, outcome and actual observations for
objects/domain/fixed_and_variable/hypotheses/equations/quantifiers/conclusion/status/
local_definitions. `review template` now produces pending entries for all applicable canonical dependencies; `--principal-statements` retains its requested-canonical check. Batch `review validate` and staged `review accept` reuse these rules; see [review handoff](proofs-and-boundaries.md#review-handoff-and-candidate-acceptance).
Only actual readings may set accepted. Missing new-policy findings cannot inherit an old
accepted review. Nodes may receive these richer reviews without changing node schemas.

New-policy output-semantic scopes additionally contain mode_findings, proof_step_findings
and (for original Paper principals) contribution_reviews. Each reading entry has outcome,
finding and actual manuscript locations. See output-review.md for keys and responsibility.
Every obligation step requires its own located finding. Paper entries also record
closest_prior_results, prior_art_searches (searched_at/query/outcome/checked_source_ids),
provenance_check, authorization_check, actual_difference, proof_closure and remaining_caveats.
Source IDs must exist in the bound materials. These records remain review assertions;
no script claims to decide mathematical truth, comprehension, authorization or novelty.

## Current support and file protection

Only schema-2.2.0 r5 output plans/policy reviews participate in the current output flow. Explicit old/unknown policy, unsupported schema and mismatched inputs receive unsupported diagnostics, not automatic migration or reclassification. This installation has no old-policy validation/rebuild continuation, recorded-policy release route or historical template selector. Consult a corresponding historical software version for old work; preserve Git history, backups, prior evidence and source files unchanged.

Within current r5, repair canonical statements in live knowledge, obtain fresh applicable review, freeze a new snapshot and explicitly adopt it downstream. Reprepare preserves authored manuscript, outline and style; immutable snapshots and prior evidence remain protected. Those file protections are current safety behavior, not promises of backward compatibility. Package requires the current release checks. Never rename an old policy or edit accepted hashes to evade them.

## Current design checks

Preparation reports `artifacts.exposition_design`; a default outline is NEEDS_WORK.
Structure and release reread audience, reader_goals and outline every time. Reserved
`[[PMS_PENDING:key]]` markers remain unfinished even in comments or code fences;
escape the opening bracket for a literal syntax example. Ordinary quoted TODO or
pending boundary explanations are not unfinished-task markers. Missing/empty
outline, known defaults and unresolved task lines block formal build and release.
Only explicitly draft plans may preview missing/incomplete design and manuscript
placeholders. Invalid outline node references, canonical and TeX safety errors
still block previews. Preview never flips draft or creates accepted evidence.

## Paper comparison and support evidence (schema 2.2.0)

Each original contribution binds explicit `(comparison_node_id, prior_result_id)`
pairs. The relation must use compares_with links to both the contribution node
and that prior; every closest prior requires its own explicit pair. Navigation
is not proof dependence. Mathematical relation reviews bind compared endpoints
and their supporting versions, without making navigation cycles proof cycles.

Each output contribution review includes `prior_result_checks`: objects with
prior_result_id, source_id, version, locator, outcome and finding. At least one
accepted primary support check is required per prior. All submitted checks are
validated. A provenance-only or unrelated source cannot supply support. The
source review must bind the source record and reading note, and its
`scope.source_reading[S-ID]` must name the controlling version and list the
actual locators read. Local originals also bind their material hash; online-only
original readings retain explicit access limitations and null raw hashes.

Locator normalization is deliberately narrow: case, whitespace, terminal
punctuation, page/p./pp., theorem/thm., section/sec./section sign, and dash glyphs.
No approximate text similarity or inferred theorem numbering is used.

Prior-art searches record dated queries and outcomes independently. Empty
checked_source_ids is valid for a negative search. Named hits must be fixed
material source IDs, but hits alone never establish support. Source review
records copied into materials must still match their actual bound inputs.
Without directly comparable prior evidence, keep an explicit draft; no waiver
can authorize formal publication. Read every claimed comparison in the same
unknowns, quantifiers, dimension, parameters, regularity and normalization.

## Current responsibilities and evidence closure

Software 2.1.0, knowledge/snapshot schema 2.0.0 and output/policy-review schema 2.2.0 remain distinct. Current r5 retains four profiles, five views, strict Minimal three sections, F1–F4 and obligation coverage, fast-route reconstruction, slow-step reproduction and condition transfer. Removing old runtime policy/template support removes none of these duties. Old files remain unchanged and old acceptance never upgrades automatically.

R5 reuses existing plan/outline, scope/findings, mode_findings and page_findings. No mathematical schema shape changes or typed route database are introduced. Private invocation/task records are independent local bookkeeping, not node/output/review fields and not public package content. Read dispatch.md for controller/worker authorization, fixed Astra/ultra parameters and task identity handling; the deterministic CLI does not orchestrate chats.

Keep actual mathematical review inputs safely inside project-relative, nonsymlink paths. A review may depend on a plan-derived authoring-promise request and source/KB files; all declared legitimate inputs must remain available in the new frozen evidence closure. Do not point frozen review inputs into mutable output directories, recursively include snapshots, or hand-copy files into an existing snapshot. Use fresh live evidence and a new freeze. A closed hash inventory proves availability/identity, not that the reviewer actually checked a promised step.


PR03 additive source metadata: `access.availability` and `access.redistribution` are independent dated facts with `status`, `checked_at`, `basis`; `material_visibility` concerns original bytes only, and optional safe `permission_note` participates in the existing source byte closure. Missing fields remain unverified without a schema migration. Source-review scopes require explicit controlling version, consumed locators, actual `reading_scope`, mode and `unchecked_items`. See [source evidence](research-and-evidence.md) for statuses and public/private handling. Paper plan research eligibility is evaluated separately from knowledge READY without weakening formal release reviews.
