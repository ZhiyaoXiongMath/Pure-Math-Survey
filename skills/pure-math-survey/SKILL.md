---
name: pure-math-survey
description: Develop source-grounded English mathematical surveys and substantive revisions. Select any requested parts and concise/standard editions of a five-part series; organize around core research questions, precise principal answers, proof mechanisms and verified boundaries; deliver rebuildable TeX and inspected PDFs.
---

# Pure Math Survey

**Version:** 1.8.1

## Scope and selection

Write around a research question, not the union of available references. Reconstruct the definitions and audit natural variations before deciding what to fix. Do not inherit a source's parameter freeze as the survey's problem definition. Preserve the user's mathematical scope. Both editions preserve the core statements and key lemmas. Concise compresses proof interiors and routine calculations, not mathematical structure. Standard expands the same proof routes and constructions for deeper study. Dated examples never override the request or the current writing rules.

For an ordinary single-topic survey, default to Part V concise. An explicitly requested five-part series selects I–V concise. An end-to-end **test** of a specified part does not request the whole series. Standard or paired editions require a request; any nonempty subset is valid. Mathematical manuscripts and skill instructions are English; discussion and delivery notes may follow the user's language.

Read [length and selection](references/length-and-selection.md) and [editions](references/editions.md), then record the selection in the project manifest and existing architecture note. Use `scripts/create_project.py --documents 5:concise` for a V-only scaffold. All generated audit rows begin pending. Default reading-length thresholds include references and trigger a non-blocking editorial reread (`REVIEW_NEEDED`, exit 0). Only an explicit user `max_pages` is a page-count gate. Never shrink the shared readable typography, remove necessary statements or change mathematical scope to satisfy a default threshold.

## Formulate the problem before selecting answers

Read [problem formulation](references/problem-formulation.md) first. Identify intrinsic data, representatives, unknowns, gauge choices, admissible variations and excluded changes. Ask which apparent fixed choices are substantive, which are coordinates, and which can meaningfully vary while preserving the problem's invariants. Do not maximize generality indiscriminately. Record each material scope decision and why it matters in the existing architecture and reader evidence; unresolved questions may remain explicitly unresolved.

Write the chosen variation domains and ordered quantifiers in the opening, **before** principal answers. Distinguish a fixed-parameter equation, existence for some parameter and existence for every parameter. Their equivalence requires evidence; it is not a definition. A scope-defining answer belongs in the organizing main theorem, not a late remedial corollary. Track local freezing for an estimate or flow separately from the global question. Constant dependence and uniformity are different questions from existence.

Run `scripts/check_problem_formulation.py PROJECT --stage plan` before drafting; then check its source bindings at release. These are schema, order and evidence checks, not automated understanding. Read the opening without the bibliography: can the reader recover the objects, natural choices, scope and actual question? Trace user/input commitments into that opening and the answers, not just introduction-to-body agreement.

## Research before drafting

Read [research and evidence](references/research-and-evidence.md) and [core problems](references/core-problems.md). Discover organizing questions, original formulations, principal theorems and counterexamples before choosing the bibliography. Search established alternative names. Trace claims to primary sources and check current versions when their status may have changed. Separate mathematical status (solved, refuted, verified open, unverified) from editorial disposition (include, context, omit). Split partially resolved claims into the proved range and the remaining target. Failed search proves neither openness nor settlement.

An important neighboring problem may deserve a short sourced explanation without a new theory chapter. Do not invent an open problem to fill a template. For every V request, read [the Part V guide](references/part-v-benchmark.md) before drafting; every sample is optional for both editions. Part III owes its selected proof routes; Part V owes its own integrated explanation, not unrequested volumes.

## Discover the frontier and justify selection

Do not let the selected bibliography define the candidate universe. Before freezing the outline, reconstruct the field's own aims from primary introductions, original questions and current follow-up papers. Contrast the strongest established answer with what it does not explain, construct or make effectively testable. Search those gaps, including counterexamples and changes of formulation. A celebrated neighboring question cannot substitute for this task.

Use [core problems](references/core-problems.md) for discovery, reverse search, stopping and omission challenges. Use [architecture](references/architecture.md) for result importance: principal answer, essential bridge, boundary result, secondary independent result, background/context. Importance is relative to the selected question, not technical difficulty. A frontier question is not a result role. No number of Problems, environments, references or tests is required.

Extend the existing publication map, frontier records and reader evidence; do not make a second audit database. Run `scripts/check_survey_selection.py PROJECT --stage plan`, then its release check after the actual source-first review. These tests check declared traceability and source bindings, not whether all worthwhile questions were discovered. Concise and standard retain the same selected core; extra depth is not a license to select another mathematical spine.

## Introduction and statements

[Introduction](references/introduction.md) governs principal-answer coverage. Define indispensable notation first and state the actual principal answers with their necessary hypotheses. A roadmap or citation does not replace a statement. Perform an introduction-only reading test and check coverage in both directions: every principal promise is delivered, and every principal body conclusion is visible in the introduction. Supporting lemmas need not become principal theorems.

[Writing style](references/writing-style.md) governs expression. Do not invent decorative names for definitions or results; author attribution is useful. Keep each statement focused on its essential conclusion. Use short clauses or itemized independent hypotheses rather than long sentences. Put secondary consequences afterward unless essential to the result. Write important assumptions, the decisive criterion, and the conclusion formulas inside each theorem, proposition, lemma, or corollary. A bare external formula number is not a substitute. Standard terms and a nearby long definition may be referenced; repeat only what prevents real backtracking. Reuse a label-free canonical body for actual repeated statements. There is no fixed theorem count. This does not license an introduction-only theorem structure: independently usable body results and essential proof inputs must remain explicit statements, followed by a clearly bounded proof, proof sketch or sourced explanation.

## Mechanisms and editions

[Proofs and boundaries](references/proofs-and-boundaries.md) governs explanation depth. For each selected mechanism identify its input, the object constructed or estimated, and the output used next. Explain a difficult interface with a calculation, lemma or precisely located imported theorem. Technique names alone are not an explanation. Before explanatory prose, draft the mathematical objects, each independently usable result, its necessary inputs, and its proof or source treatment. Apply the selected Part template by those roles, not by copying its headings or filling every slot. Extract hypotheses and conclusions first; do not retrofit theorem wrappers around an unchanged essay. Separate survey derivations from quoted results and preserve the latter's actual range.

Prefer formulas to wordy paraphrases. Omit trivial transitions; a definition or substantive mathematical sentence is often sufficient. Retain examples only when they compute a model, explain an assumption, distinguish formulations or exhibit failure. Do not impose quotas for examples or Problems. Concise compresses depth, not branch conditions, regularity or truth status.

## Verification and delivery

Use [records and delivery](references/records-and-delivery.md) for file/schema details and [validation](references/validation.md) for checks and finding dispositions. Reuse existing records rather than adding parallel audit tables. Canonical components serve actual reuse or export, not compulsory fragmentation of every lemma. Keep bibliography identity, controlling version, locator and status traceable. A changed bibliographic fingerprint requires source review; a matching fingerprint does not certify mathematics.

After a source-first omission challenge against the candidate universe, review in three passes: recover the question and variation domains from the opening; read local definitions and statements without proofs to recover the knowledge; then follow proof inputs, intermediate outputs, constant dependence and closure. For every substantive body section, record the expected result labels, any claims remaining in prose and why, self-containment findings, and actual proof dependencies in the existing reader/depth evidence. Read the entire body, not a representative paragraph. Run `scripts/check_mathematical_structure.py`; its reference sites and source bindings direct review but do not grade prose. Its fingerprint and coverage checks do not certify those answers. A successful build or a previous review label never grants writing-example status. Before recommending a new complete example, read its entire final TeX and PDF and resolve structural findings; retained examples remain bounded, dated references. Compile from clean inputs until references stabilize; inspect all rendered pages and recheck affected pages after repairs. Reopen archives, verify member hashes and exclude font files, private data and restricted source texts. Keep production notes out of the article. Distinguish source checking, mathematical review, compilation, rendering and reproduction. Disclose when independent review is unavailable; an author reread is not independent review.

Report the actual evidence, remaining limitations and requested deliverables using the statuses in validation. Stop after necessary checks and repairs; do not add unrequested volumes. A single successful topic is not evidence of general mathematical reliability.

## Maintenance

Read [template maintenance](references/template-maintenance.md) and [layout and build](references/layout-and-build.md). Run `scripts/validate_assets.py` and `scripts/build_checks.py`, then inspect renders. Current-style regression must use `assets/templates/math-review.sty`; frozen reproduction must use the sample's bundled style in a separate target. Test with deliberately different dependencies so a stale copy cannot pass unnoticed. Preserve frozen evidence unchanged and date new verification separately.
