# Native file fields and reproducible operations

The candidate software runtime is `2.1.0-rc2`. Project, knowledge, sources, snapshots and generated/build manifests retain schema `2.0.0`. New output plans and policy-bearing mathematical/output-semantic reviews use schema `2.2.0`; historical `2.0.0` plans and reviews remain readable without mutation. See [output review](output-review.md) for whole-manuscript checks, actual body locations and build history. JSON has no duplicate keys or nonfinite numbers. Stable IDs use letters/digits/dot/underscore/hyphen, with N- and S- prefixes for nodes and sources; each filename equals its ID. All project-relative paths are POSIX, contain no traversal/absolute prefix and cross no symbolic links.

## Project and knowledge

project.json: schema_version, project_id, title, language, scope_file, knowledge_root; optional nullable literature_cutoff. Knowledge requires overview.md, conventions.tex, discovery.md, coverage.json. There need not be any output.

Node frontmatter is a JSON object between standalone `---` lines, followed by readable Markdown. Required fields: schema_version, id, kind, title, facets (nonempty), question_ids, mathematical_status, origin, sources, links. Kinds: question/definition/result/relation/mechanism/example/application/frontier. Status: unassessed/established/conjectural/open/refuted/not_applicable. Origin: primary_source/supplied_manuscript/local_derivation. Sources link source_id, exact locator and support/provenance role; optional version must match the controlling source. Relations are uses_definition/proof_input/explained_by/explains/compares_with/refutes/specializes.

A formal node has at most one `## Canonical statement`, containing only one fenced latex block. Definitions/results/relations require it. No theorem/definition/document wrapper, label or external input inside. The literal inner UTF-8 bytes, including internal line endings, are exported unchanged. Metadata titles organize knowledge, not obligatory theorem titles.

Source JSON: schema_version, id, kind (primary/supplied_manuscript), title, authors, publication_status, identifiers, version (explicit text/null), access. Access has state metadata_only/full_text_read, checked_at, material_sha256, local_path (explicit null allowed), optional reading_note. Original online reading without PDF bytes has the extra scoped limitation described in [source evidence](research-and-evidence.md). Unresolved version_conflicts block readiness. Optional bibliography.year supplies an explicit calendar year (1900–2099); otherwise export uses an unambiguous calendar year in version text, never the YYMM prefix of an arXiv identifier. An unavailable year is omitted, not guessed.

Coverage JSON: schema_version, questions. Each question has question_id, answer_nodes, mechanism_nodes, boundary_nodes, gaps, assessment pending/adequate/limited, rationale. An empty boundary list is allowed with substantive scope reasoning. Gap dispositions resolved/outside_explicit_scope require reason; other outstanding important gaps block readiness.

## Plan

Required: schema_version, output_id, snapshot_id, profile, view, language, title, audience, reader_goals, question_ids, prerequisites, selections, omissions, proof_obligations, limits, draft. Optional comparison_group and consume_overview (default true).

Selection: node_id; role principal_answer/essential_bridge/boundary/background/frontier; statement_treatment full/explained_reference; proof_treatment complete/sketch/mechanism/citation/none; reason. Omission: node_id/reason. An explicitly scoped prerequisite is either plain reader background or an object with node_id/scope/reason; only the object can mechanically discharge a specific unselected dependency.

Proof obligation: node_id, treatment complete/sketch/mechanism, nonempty required_steps, imported_inputs. An expanded proof selection must have step obligations directly or through selected explaining mechanisms. Imported inputs need explicit selection/prerequisite treatment. limits.max_pages is required and nullable; optional page_review_threshold is also nullable. A comparison group shares snapshot/question/core/boundary only when explicitly requested.

## CLI recipes

```sh
python scripts/survey.py init --output topic --topic topic-id --scope scope-input.md --json
python scripts/survey.py kb validate topic --json
python scripts/survey.py kb index topic --json
python scripts/survey.py kb freeze topic --json
python scripts/survey.py kb verify topic --snapshot KB-FULL_HASH --json
python scripts/survey.py output plan topic --output short --snapshot KB-FULL_HASH --json
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

These recipes use placeholder IDs. init produces an empty unverified KB; add real scope-specific knowledge, evidence and coverage before a meaningful plan. Prepare makes no mathematical claims and preserves existing prose. Fill review templates only after the actual recorded work. `--draft` permanently marks that plan draft until an explicit reviewed plan change/reprepare; never remove the flag merely to bypass readiness.

## Versioned output policy (2.2.0)

New plans require `editorial_policy: four-modes-2026-10-12-rc2` and `contributions`
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
local_definitions. `review template --principal-statements` produces pending entries.
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

## Historical compatibility, not silent migration

Schema 2.0.0 output plans use only the historical three modes and may not contain new
policy/contribution fields. Schema 2.2.0 plans cannot be read by the old 2.0.4 parser.
No in-place migration command is added. To adopt vNext, create a new output ID from an
appropriate snapshot, refine its new plan/outline, and perform the new readings. Repair
canonical statements in knowledge and freeze again when necessary. Old snapshots,
manuscripts and evidence remain unchanged; reprepare preserves authored prose and outline.
Legacy release checks explicitly identify `legacy-2.0.0`; they are not vNext acceptance.
Never manually downgrade a new plan to evade policy gates.

## rc2 adoption and design checks

| Output schema | Recorded policy | Current package authorization |
| --- | --- | --- |
| 2.0.0 | legacy-2.0.0 | Requires a new rc2 output |
| 2.1.0 | four-modes-2026-10-11-r2 | Requires a new rc2 output |
| 2.2.0 | four-modes-2026-10-12-rc2 | Only after current release checks |

Unknown or mixed schema/policy pairs fail closed. Use `output validate ... --stage
release --policy recorded` only for a read-only historical assessment: even a valid
result is RECORDED_VALID, never authorization to package. Package always rechecks
current policy. F1 location checks apply to historical evidence too.

Preparation reports `artifacts.exposition_design`; a default outline is NEEDS_WORK.
Structure and release reread audience, reader_goals and outline every time. Reserved
`[[PMS_PENDING:key]]` markers remain unfinished even in comments or code fences;
escape the opening bracket for a literal syntax example. Ordinary quoted TODO or
pending boundary explanations are not unfinished-task markers. Missing/empty
outline, known defaults and unresolved task lines block formal build and release.
Only explicitly draft plans may preview missing/incomplete design and manuscript
placeholders. Invalid outline node references, canonical and TeX safety errors
still block previews. Preview never flips draft or creates accepted evidence.

## Paper comparison and support evidence (rc2)

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
