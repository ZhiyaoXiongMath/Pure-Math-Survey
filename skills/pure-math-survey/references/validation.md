# Validation of a research project

Run the problem-formulation plan check before drafting and its release check on final expanded TeX. Read the opening for definitions, meaningful variations and ordered quantifiers before reading answers. Check user/input-to-opening-to-answer coverage, not only introduction/body consistency. Exact bindings and dependency checks detect specified regressions; they do not prove scope completeness or mathematical equivalence. See [problem formulation](problem-formulation.md).


Structural validation, source review, mathematical reading, compilation, visual inspection and archive checks answer different questions. Keep their evidence separate; none certifies the others.

## Runtime structural check

Run `python pure-math-survey/scripts/validate_project.py PROJECT`. The parser requires Python 3.10+; current-project PDF measurement also requires PyMuPDF. It checks the requested document set, safe literal braced inputs (including explicit `.bbl`), mapped component placements, labels, identity links and required audit rows. It does not interpret arbitrary TeX macros, verify evidence content or prove semantic equivalence. `--template-mode` is only an instructional preview, never publication acceptance. The real build must also resolve all dependencies.

Use [records and delivery](records-and-delivery.md) for the unchanged schema and conditional records. A PDF signature alone does not establish that the document opens. Current-project validation measures the actual PDFs; advisory reading-length overruns remain notes, while explicit user-limit breaches or unreadable PDFs are errors. Readable pages still do not establish successful visual inspection. A completed audit row is a declared review outcome, not an independently discovered fact.

## Source and mathematical reading

Follow [research and evidence](research-and-evidence.md) for source identity, exact controlling versions, theorem locators and search limits. Review hypotheses, quantifiers, phase or parameter ranges, regularity, conclusions and status against the source. Include surrounding comparisons and claimed implications: a correct canonical theorem can still sit beside false prose. When a source version changes, review affected claims again; a fingerprint only detects identity drift.

Read each requested document without undelivered parts. Check the selected question and its principal answers against the architecture fixed before drafting. Use the introduction-only and reverse-coverage tests in [introduction](introduction.md), the passage-level rules in [writing style](writing-style.md), and the depth tests in [editions](editions.md). These are substantive reading tests, not keyword, heading, theorem-count or page-ratio tests.

For each selected method, identify the precise input, the object constructed or estimated, and the output used next. Apply [proofs and boundaries](proofs-and-boundaries.md) to distinguish a local derivation, an imported theorem, a proof route and a complete-proof claim. Do not require recursively reproving the literature; do not accept technique names as a promised explanation. Review each claimed frontier status using [core problems](core-problems.md), even when no numbered Problem is printed.

## Evidence in existing audit rows

Record located findings and repairs in `release-audit.csv`, linking a shared review note where useful. Do not add a parallel approval table.

| Row | What its completed review actually covers |
|---|---|
| `source_identity`, `statement_verification` | Sources/versions and retained mathematical statements; disclose access limits beside the relevant source. |
| `reader_outcomes`, `edition_depth` | Independent readability, introduction/body coverage and the requested depth of actual passages. For V use [the article guide](part-v-benchmark.md). |
| `proof_depth` | Only the argument treatment actually promised and supplied, with exact imported inputs and unresolved steps. |
| `edition_semantic_consistency` | Shared statement meanings and surrounding prose. In a single edition, compare against its sources; do not claim an absent companion was reviewed. |
| `frontier_status` | Supported status within the selected scope, including settled or refuted formulations and version-qualified preprints. |
| `build_requested_documents`, `visual_requested_documents` | Actual entrypoints, stable references, log findings and every rendered page. |
| `archive_integrity` | Reopened archive membership, dependencies, safety and recomputed checksums. |

`proof_framework` and `decisive_mechanisms` are required only when Part III is requested. For V-only they may be absent or reasoned `NOT_APPLICABLE`; V method explanations remain subject to reader/depth review. Paired editions need comparison of actual common content and deeper treatment, not a page-ratio verdict. Single-edition work needs no invented paired review.

## Whole-body structure and self-containment

For each substantive section, first read the mathematics without counting environments. Identify its question, independently usable outputs, necessary proof inputs, and consumers. Then read local definitions and statements without proofs. Can the reader recover the exact assumptions, quantifiers, regularity, criterion and conclusion formulas? Finally follow the proof dependencies and all imported inputs. Review the entire body, not a chosen paragraph. A mixed argument wrapped in a proposition is still a failed reading.

Record located findings in the existing `structure_review` supporting `reader_outcomes`, `proof_depth` and `edition_depth`. Current projects use structure-review schema `1.1.0`. Section records identify expected result labels, self-containment findings and the disposition of claims left in prose. Body-result records additionally review each literal statement reference and say why the needed mathematics is locally available. A reference to a standard term or nearby long definition is allowed; do not replace reader judgment with a ban on references.

Run `scripts/check_mathematical_structure.py PROJECT --tex FILE --inventory`, then supply the actual review with `--review RECORD`. It checks literal-input expansion, labels, expected/actual result coverage, proof attachment, quoted-source locators, reference-review coverage and the reviewed source fingerprint. It cannot decide whether a prose claim deserved a lemma or whether the reviewer understood the mathematics. Update the fingerprint only after rereading the changed source and affected pages.

`validate_project.py` invokes this evidence check for current manifests. The documented older manifest contracts remain readable, but new projects must not downgrade their declared version to bypass review. A context-only section needs a substantive reason. A proof-only section can prove an already visible result without inventing an intermediate lemma; its proof and target labels must be bound in the review. Cover every literal author-written section, including starred sections, with a semantic label. Numbering is not an exemption from reading. For a deliberately deferred body proof, record `proof_location: "deferred"` and a specific `proof_location_reason`; place a forward proof/section reference after the result and identify the result in the later proof. This supports separate proof sections without borrowing an unrelated proof. A printed sketch or outline must be reviewed as `proof-sketch`, not `full-proof`. Counts describe syntax and are not quality scores.

## Findings and disposition

Repair mathematical errors, missing necessary hypotheses, unsupported core status claims and absent promised explanations before completing the affected check. A disclaimer does not repair a broken core. Apply the same local repair/recheck discipline to bloated statements, trivial transitions, ambiguous conditions, misleading notation or rendered overflow. Useful self-contained repetition is not a defect.

Keep source-access, reviewer-independence and search-coverage limits precise. With no independent agent, perform a separate source-first author reread and disclose that it is not independent review. Do not invent a reviewer or an additional gate. Reject an unsupported objection with a reason; sustain valid defects and recheck their dependents. Retain material findings and their actual disposition, not just a PASS label.

## Build, visual inspection and archive

Compile every requested entrypoint until references stabilize, including the required bibliography step. Inspect errors, undefined references/citations, duplicate labels, missing glyphs and substantive box overflow. Record commands, engine, dependency versions and actual results.

Render and inspect every page: title, theorem conditions and numbering, notation, equation breaks, references, bibliography and page boundaries. Repair local issues locally. A genuine shared-style change requires affected regression builds. Never shrink type or margins merely to satisfy a length limit. Check standalone exports as actual additional entrypoints, not as assumed copies.

Reopen the delivered archive, compare its intended member set and recompute hashes. Exclude unsafe paths, symlinks, font files, private data and omitted dependencies. Provide an external archive digest. Do not inherit an earlier archive or frozen-sample verdict.

## Honest conclusions and stopping

Use `DELIVERABLE_WITHIN_PROTOCOL` when the requested core and necessary checks are completed within scope; use `DELIVERABLE_WITH_LIMITATIONS` for a satisfied core with disclosed supplementary limits or the permitted author-reread fallback. Unresolved core defects or missing mandatory checks require `INCOMPLETE`, or `BLOCKED` when input/capability prevents continuation. Do not introduce new audit status names or weaken the protocol to pass.

A source-first reread is not independent review; checking a theorem is not checking its entire proof. Structural acceptance, successful builds, page counts and CSV statuses do not establish mathematical quality. Once the necessary checks and local repairs are complete, stop rather than expanding the requested task.

## Tools and their limits

[Templates and example builds](template-maintenance.md) describes current/frozen style staging. Run `scripts/validate_assets.py` and real `scripts/build_checks.py` builds after relevant changes. Development tests and their records belong outside the installed skill. Optional `scripts/compare_pdf.py` page/text/pixel comparisons establish only the reported reproduction properties, not mathematical quality.

Run `check_survey_selection.py PROJECT --stage plan` before drafting and `--stage release` after the source-first review. Project validation invokes the release check. The declared shared core must contain every local principal answer even when only one edition is requested. Additional secondary results are allowed when they do not replace that core. Bound source spans and schema checks do not certify that the selected roles are mathematically appropriate or that discovery is exhaustive.
