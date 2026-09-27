# Project format, records and delivery

Use `problem_formulation` inside each document's existing structure-review JSON. Its object/variation/question model is completed at planning; source bindings, reader answers and a model digest are completed at release. `scripts/check_problem_formulation.py` defines the exact schema. Do not create parallel scope registries. The manifest's existing `structure_review` pointer is reused.


## Manifest and source layout

The skill and current shared style version are `1.8.1`. The manifest and registry schema is `1.0.0`; the current structure-review schema is `1.1.0`. Skill versions and schema versions have different roles. `project-manifest.json` has `language: "en"`, `skill_version: "1.8.1"`, and a `documents` array containing integer `part` 1--5, `edition` (`concise` or `standard`), `tex_file`, `pdf_file`, and `structure_review`. Paths are safe project-relative POSIX paths and maintained text files are UTF-8. `page_review_threshold` is optional non-blocking guidance; `max_pages` is an optional explicit user maximum, never inferred from defaults. See [reading-length behavior](length-and-selection.md).

Without `requested_documents`, the schema requires all ten part/edition combinations. Otherwise that field is a nonempty list of unique objects with exactly `part` and `edition`; `documents` must match it exactly. Record the user's selection before drafting, never infer it from finished files. Preserve the actual scope of an update. A V-only standard manifest is:

```json
{
  "schema_version": "1.0.0",
  "skill_version": "1.8.1",
  "language": "en",
  "requested_documents": [{"part": 5, "edition": "standard"}],
  "documents": [
    {"part": 5, "edition": "standard",
     "tex_file": "topic-part5-integrated-standard.tex",
     "pdf_file": "topic-part5-integrated-standard.pdf",
     "structure_review": "evidence/topic-part5-integrated-standard-structure-review.json"}
  ]
}
```

Names may follow `<topic>-part1-foundations-concise.tex` and the matching stems for `part2-results`, `part3-methods`, `part4-boundaries` and `part5-integrated`, each at its requested depth. Deliver matching PDFs and all rebuild dependencies: the shared style, canonical components, bibliography and any actual additional inputs. V-only needs no standalone I–IV artifacts and no companion edition. Its own selected survey contract governs its content.

## Mathematical ownership and placements

`publication-map.csv` records each formal result and its question-relative role and placement. Nonrepeated local statements may stay inline; map them without fragmenting every result into a component. Its fields are:

```text
node_id,kind,owner_part,canonical_component,source_ids,proof_ids,
concise_file,concise_label,standard_file,standard_label,
concise_treatment,standard_treatment,limitation_note,
integrated_concise_file,integrated_concise_label,integrated_concise_treatment,
integrated_standard_file,integrated_standard_label,integrated_standard_treatment
```

`owner_part` is 1–4 and identifies the mathematical role, not a demanded deliverable: elementary facts may be owned by I, main results by II, technical arguments by III and frontier Problems by IV. A node can appear only in V. The unprefixed concise/standard slots refer to the owner; each `integrated_*` slot refers to the corresponding V edition. Each file must match that actual manifest document. Locations use descriptive mathematical labels rather than internal IDs. Source/proof IDs link their registries; use semicolons for lists.

A canonical component is body-only TeX: no document or theorem-like wrapper, including no `problem` or recall wrapper, and no `\label` commands. Put the environment, name, numbering and primary label around its `\input` in the manuscript. Hypothesis lists and mathematical displays belong in the body. The same complete mathematical statement is reused wherever `FULL_STATEMENT` is selected. Other prose can be rewritten or reorganized.

| Treatment | Valid requested placements | Coordinates and body |
|---|---|---|
| `FULL_STATEMENT` | All parts and editions | The actual document and one mapped primary semantic label; inline for a once-used statement, or an input of the canonical body when shared/repeated; useful local recalls reuse that body |
| `REFERENCE_ONLY` | I–IV concise and both V editions | Actual document and unique label, accurate source/locator and independently usable local explanation; no body input; reason in `limitation_note` |
| `OMITTED_WITH_REASON` | I–IV concise and both V editions | Empty file and label; no input of the component in this actual part/edition; substantive reason in `limitation_note` |
| `NOT_REQUESTED` | Only an unrequested document | Empty file and label; never a substitute for treatment inside a requested document |

I–IV standard placements retain `FULL_STATEMENT`. V may omit side branches, intermediate lemmas or minor examples outside its own core in either edition. It may reference accurately with the assumptions needed for independent reading, not delegate necessary content to an undelivered volume. Its own advertised main-result understanding and core Problems cannot be omitted to satisfy a parser. Explain reasons separately by placement in the existing note when they differ. Core selection and adequacy of reasons are human judgments.

For a useful full recall within a document, input the same canonical body again rather than creating a second node or a divergent copy. The mapped primary label must still appear exactly once; the recall can use `theoremrecall` with that label. Keep wrapper labels unique and component bodies label-free. The validator allows repeated full-body inputs and reports them for substantive rereading; it still rejects inputs at `REFERENCE_ONLY` or omitted placements. No extra repetition ledger or schema is required. See the [worked example](exposition-examples.md#canonical-repetition-without-label-conflicts).

A source theorem that bundles a principal answer with subsidiary claims may be represented by several supported nodes. Preserve the controlling source, hypotheses, original relationship and all conclusions retained in the review. A corollary needing extra hypotheses must state them; do not change an existing canonical node silently to make an overlong theorem look shorter.

Every node needs at least one actual requested full or referenced placement; do not create unused placeholder nodes. Ordinary local cross-references are not additional map rows. Extra cross-part placements can use `canonical-crosswalk.csv`. After fixing a shared statement, check actual affected documents, their surrounding prose and status claims.

## Required and conditional records

Use [registry templates](../assets/registries/) as formats, not as a demand to instantiate every collection. For runtime structural validation the project needs `bibliographic-identity.csv`, `proof-mechanism-registry.csv`, `publication-map.csv` and `release-audit.csv`. The proof registry can be header-only when no proof nodes are used; a method explanation is not a fabricated complete-proof record. Bibliographic identities and publication nodes must be real and nonempty.

Retain the research records actually used: scope/protocol, architecture and edition plan; search replay, source manifest, screening, identity/version decisions and conventions; canonical results and proof provenance; relevant theory/history relationships; frontier claims and reverse searches; and verification/build/visual evidence. Update dispositions, prospective holdouts and insertion checks are conditional on the actual task. Do not manufacture unrelated empty audit tables. Existing filenames containing theorem, estimate or geometry terminology do not impose a kind of mathematics. Choose CSV or JSONL representations as useful rather than duplicating evidence without purpose. The concept field `geometric_intuition` accepts algebraic, structural, combinatorial or other intuition appropriate to the subject; omit unused intuition with a note. A linked architecture/proof note may supply optional descriptive details.

`release-audit.csv` has `check,status,evidence,note`. Never prefill PASS. Required checks are `source_identity`, `statement_verification`, `proof_depth`, `reader_outcomes`, `edition_depth`, `edition_semantic_consistency`, `frontier_status`, `build_requested_documents`, `visual_requested_documents` and `archive_integrity`.

Only a request containing III requires `proof_framework` and `decisive_mechanisms`, covering the requested III editions. Without III these rows may be omitted or use `NOT_APPLICABLE` with a reason, including in V-only projects. If III and V are both requested, V's lighter contract does not waive III's checks. V method explanations and relationships are reviewed in `reader_outcomes` and `edition_depth`, not a new audit table.

For IV or V, `frontier_status` requires completed review within the part's own scope, including a supported settled-scope conclusion when appropriate. It cannot be waived for lack of a problem list. Without IV/V a genuinely inapplicable frontier check may be `NOT_APPLICABLE` with a reason. All other required checks remain applicable: for example, single-edition semantic consistency checks the actual source/body/prose scope rather than claiming a comparison with an absent counterpart.

`proof_depth` records actual argument treatment and declared bounds. A V method sketch does not require a full proof; its evidence should describe the sketch and imports actually reviewed. `reader_outcomes` checks document-specific promises and locations; `edition_depth` checks the selected backbone, real concise selection and standard's added understanding. Accepted completed statuses are `PASS`, `VERIFIED` and `COMPLETE`, each with nonempty evidence. Give the actual scope, locations, repair/recheck outcome and any residual limitation in the existing evidence/note fields or their linked note. These statuses do not mean that every source proof was rederived or that an independent review occurred. Use the [finding dispositions](validation.md#findings-and-disposition); do not mark an unmet mandatory check complete merely by adding a disclaimer. The program verifies records, not the truth or adequacy of the judgments.

### Architecture and proof notes

Use the architecture/proof notes for core questions, document commitments, routes, selected targets and permitted imports. The proof registry's descriptive fields include `supports_node_ids`, `method_family`, `declared_inputs`, `dependencies`, `proof_treatment`, `closure_status`, `core_question`, `explanation_role`, `decisive_mechanism`, `route_locations`, `mechanism_locations`, `application_or_boundary` and `early_explanation_check`. A linked note can hold the same explanation; no extra table is required.

Locations identify the document edition and actual section, label or page, not just a shared filename. For an executed explanation check, retain its date, draft passage, outputs, first unsupported inference or checked closure, source/proof locators, revision and affected recheck. Match its depth to the actual promise: V without a deep-proof commitment needs a method account, not an imported III checklist.

## Rebuildable archive and final delivery

Include requested PDFs and TeX, actual rebuild dependencies, the manifest/map, scope and architecture, shared research records and applicable verification evidence. If delivered PDFs are external to the archive by explicit design, identify and checksum-link them. Keep author-only reasoning, confidential documents and restricted source text out; preserve lawful locators instead.

Record the TeX engine, bibliography procedure and exact build commands. Use ordinary ZIP and Python tools. Hash the explicit selected member set in `artifact-checksums.txt`, excluding the checksum file itself. Reopen the ZIP, reject unsafe paths, duplicates and symlinks, compare members and recompute hashes. Provide the archive SHA-256 outside it. An exit code does not certify mathematics.

List all requested reader documents and disclose any absent requested item. Unrequested parts and editions are outside scope, not missing. Give a reasoned completion status and actual limitations.

## Introduction coverage without a new registry

Extend the existing architecture note, not the schema: identify each selected principal conclusion, its introduction and body locations, necessary local definitions, controlling source and any explicit special-case restriction. Keep precise statements in the master theorem matrix/canonical bodies and formal placements in the publication map. A body-to-introduction link is an ordinary local relationship, not an extra map row for every recall.

`reader_outcomes` evidence records the introduction-only reading and the reverse body check with actual labels or passages. `edition_depth` records coherent concise selection and substantive standard development; `statement_verification` records scope/quantifier fidelity; `edition_semantic_consistency` records shared statement agreement. The existing build and visual rows cover [the presentation profile](layout-and-build.md), page inspection and any documented font fallback. Do not add `introduction-pass.csv`, another principal-result registry, new completed statuses or a separate V audit layer.

When an optional example is used, record its purpose and inspected passages in the existing architecture/release evidence. No sample reading is mandatory beyond the generic Part V guide. The frozen sample is not a newly verified source and does not change the manuscript's literature cutoff. The sample itself is a standalone historical deliverable, not a claim that its original package follows this project's manifest schema.

The project manifest schema is `1.0.0`; new projects declare skill version `1.8.1`. Existing manifest contracts remain readable, but source and reader evidence must be reviewed rather than inherited as current approval. The structural validator supports literal braced TeX inputs, including explicit `.bbl` inputs. For a macro-expanded standalone export, validate its source project and then build and visually inspect the exported entrypoint. A literal-input parser is not a general TeX interpreter.

## Located body-structure evidence

The manifest declares `skill_version` and `documents[].structure_review` in its current schema. Each review file is a JSON object with `schema_version: "1.1.0"`, `tex_file`, `source_sha256` (SHA-256 of comment-stripped, literal-input-expanded TeX), `reviewer_mode`, `reviewed_on`, `sections`, and `results`. New scaffolds start with empty records and a pending fingerprint.

Each section record has `label`, `role` (`introduction`, `results-and-mechanisms`, `proof-only`, or `context-only`), `statement_reading`, `dependency_reading`, and, for context-only, `result_free_reason`. Reading fields contain located substantive answers, not booleans or PASS. Every literal author-written section is covered, numbered or starred; each has a semantic label. Bibliography or other headings generated by TeX macros are outside the literal parser and remain part of the page review. Each current section also records `expected_result_labels` (the distinct formal results the content-first reading expects there), `self_containment_reading`, and `unstructured_claims_reading` (what remains in prose and why). The expected labels must match the actual result labels in that section. A `proof-only` section has `result_free_reason`, `proof_label`, and `proved_result_labels`; its located proof must refer to those visible results and the section contains no new independent result.

Each body result record has `label`, `environment`, `logical_role`, `local_context` (a list of existing labels), `hypotheses`, `conclusion`, `consumer` (an existing label), `treatment` (`full-proof`, `proof-sketch`, or `quoted-input`), `proof_label` (required for local proofs/sketches), `source_keys`, and `source_locator` (required for quoted inputs). It also records `statement_reading`, `dependency_reading`, and `self_containment_reading`. The `reference_review` list has one object for each distinct literal statement reference: `target`, `role` (`nearby-definition`, `standard-notation`, `prior-result`, `navigation`, or `formula-repeated`), and a substantive `reason` explaining reader access to the needed content. An empty list is correct when no literal reference occurs. These fields document judgments; matching them does not establish self-containment. These are reviewer observations. The tool does not understand whether a mathematical hypothesis is true or sufficient. A quoted result may have an explanatory proof block, but that block must be labelled as an outline, not represented as a full proof. A local sketch must also be printed as a sketch or outline. For a proof intentionally placed elsewhere, set `proof_location: "deferred"`, give `proof_location_reason`, reference that proof or section immediately after the result, and reference the proved result inside the located proof. The default is `adjacent`; unrelated later proofs cannot satisfy it. A shared later proof may name multiple results explicitly.

The checker prints the source digest and inventory with `--inventory`; this does not issue a completed review. Review the actual source/PDF before writing the matching digest. Ordinary comments are excluded from the digest; changes to visible formulas, statements, proofs, or included bibliography invalidate it. Typography and PDF inspection retain their separate checks.

## Selection and discovery records

The manifest `skill_version` selects its validation contract, not a label to bypass checks. New projects use `1.8.1`. Add survey_selection to existing structure_review JSON, not a second ledger. Its questions contain statement, scope, current_answer, desired_answer, gap and priority_reason. Record core_result_ids, core_mechanism_ids and core_frontier_ids shared across requested editions.

Append result_role, question_ids, selection_reason and consumer_ids to publication-map.csv. Append formulation_kind, known_range, remaining_target, importance, editorial_disposition, editorial_reason, source_ids and body_binding_ids to frontier-claim-registry.csv. Append activity, source_ids and finding to frontier-reverse-search.csv. See core-problems.md and architecture.md for meanings. Discovery has scope, starting_points, search_ids, candidate_ids, omission_challenge, stop_reason and limitations; zero candidates requires a substantive no_candidate_reason.

Bind each included/context frontier to actual unique label-delimited source spans with exact quotations, why and SHA256. Review question_priority, result_importance, frontier_coverage, edition_core and limitations with specific observations. Plan and source hashes detect changes, not understanding or honesty. The checker cannot discover an unrecorded mathematical omission.

Use explicit mathematical status and an independent editorial disposition. A source read is not a performed search query. Unfinished fields remain pending. Run `check_survey_selection.py` at plan/release stages. Canonical bodies serve shared or repeated statements; a once-used mapped statement may be inline.
