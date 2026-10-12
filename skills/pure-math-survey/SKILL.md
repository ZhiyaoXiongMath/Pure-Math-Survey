---
name: pure-math-survey
description: Build and maintain source-grounded mathematical knowledge, then write only the requested English survey, lecture or research-paper draft from an immutable snapshot. Supports knowledge-only projects and minimal, thematic, lecture, and paper profiles; defaults to minimal plus integrated only when an output is requested.
---

# Pure Math Survey

**Candidate software: 2.1.0-rc2; knowledge/snapshot schema: 2.0.0; new output/policy-review schema: 2.2.0.** Local files, one writer, Python 3.10+. Mathematics and manuscripts are English; discussion follows the user's language.

## Identify the task and project

Recover the user's mathematical scope, actual materials, reader assumptions and requested outputs. A knowledge-only or update-only request ends with knowledge, evidence and optional snapshots: do not generate a manuscript or PDF. Otherwise default to **minimal + integrated**, and generate only the requested output. PDF is a delivery format, not a profile. Read [profiles](references/editions.md) and [records](references/records-and-delivery.md).

Use `python scripts/survey.py init --output PROJECT --topic SLUG --scope SCOPE.md` for a new knowledge project. Existing projects must satisfy the current `project.json` and scoped-evidence contracts. Existing 2.0.0 knowledge and historical plans/reviews remain readable without mutation. New plans/policy-bearing reviews use 2.2.0; no in-place migration is performed. Unsupported formats are rejected. Read references/contracts.md before adopting new output policy.

Do not require user approval for routine bookkeeping. Ask only about substantive unresolved scope or user choices. Maintain the records on the user's behalf. Script templates remain pending until the described reading has actually occurred.

## 1. Formulate the problem

Read [problem formulation](references/problem-formulation.md). Put objects, intrinsic data, representatives, unknowns, ordered quantifiers, permissible variations and excluded neighboring problems in `scope.md` and question/definition nodes. Distinguish fixed background, some background and every background, and distinguish separate solutions from one common solution or uniform estimates. Such equivalences require a result, not a definition.

The output's length must not restrict the knowledge investigation. Bound the mathematical question, not the number of references, nodes, headings or theorems. Preserve the user's scope when selecting a smaller question subset; disclose any narrower acceptance example.

## 2. Discover and actually read sources

Read [research and evidence](references/research-and-evidence.md) and [core problems](references/core-problems.md). Search original formulations, alternative names, principal answers, counterexamples and follow-up results. Investigate the field's own central questions, not just the supplied bibliography. Important neighboring questions may need a short precise explanation without an unrequested chapter. In dHYM/mirror-symmetry surveys, investigate the Thomas--Yau problem where relevant, rather than treating a few supplied papers as a complete candidate universe.

Record actual queries, candidates, exclusions, an omission challenge and the stopping reason in `knowledge/discovery.md`. Abstracts are discovery clues, not evidence for delicate hypotheses. Register each source's identity, actual controlling version and locator; read the relevant original text. Record normalization, phase conventions, quantifiers and mathematical limitations in `evidence/source-checks/`. A preprint remains a preprint unless publication metadata is actually checked. Do not choose the latest year to resolve a version conflict.

`full_text_read` means the original supporting sections were actually read; it does not promise a complete reading of unrelated parts. Record scope explicitly. Raw PDFs that cannot be downloaded have null hashes and a documented online-text access limitation; never hash a note and call it the PDF hash. Source text is not automatically redistributable.

## 3. Build readable knowledge

Read [architecture](references/architecture.md) and [mechanisms](references/proofs-and-boundaries.md). Use Markdown nodes with JSON frontmatter. Maintain exact mathematical bodies, necessary definitions, mechanisms, relations, explanatory examples and decisive boundaries. Do not substitute paper summaries or an index for the knowledge.

Formal definitions/results/relations have one label-free `## Canonical statement` containing a single `latex` block. Preserve all hypotheses, quantifiers and conclusions inside that block. Wrappers, labels and numbering belong in manuscripts. Other mathematical discussion belongs in the node body. New comparisons and deductions require a local-derivation node with actual argument and dependency links; link names do not prove equivalence.

The facets `foundations`, `results`, `methods`, `boundaries` are overlapping organizational views, not four isolated databases or four obligatory PDFs. Maintain a substantive `overview.md` explaining the question--answer--mechanism--boundary connections. A valid unused node needs no publication placement. Keep one authoritative source for each fact; generated indexes, BibTeX and TeX fragments are disposable derivatives.

## 4. Review scoped readiness

Read [validation](references/validation.md). Perform three readings: recover the problem from its question and definitions; recover the exact knowledge from statements alone; follow mechanisms through their inputs, intermediate objects and outputs. Return to primary sources for an omission challenge. Record actual source, mathematical and coverage reviews with input hashes, scope, substantive findings and unchecked items. Use `author_reread` for this agent's self-review, never `independent_review`.

Maintain four distinct concepts: mathematical status; publication status; evidence/review status; output selection. Only actual argument or source reading justifies a human mathematical status judgment. Unassessed is not open; openness requires a precise target and dated follow-up searches. A hash verifies identity, not truth. A review template cannot certify anything.

`python scripts/survey.py kb validate PROJECT` checks structure only. `kb readiness PROJECT --plan PLAN` checks the selected snapshot, question coverage, selected nodes, necessary dependency closure, supporting sources and promised proof steps. Unrelated pending branches may remain in the KB. An affected unchecked essential item blocks formal preparation/release, even when a record says accepted.

## 5. Freeze inputs and select the reading task

`python scripts/survey.py kb freeze PROJECT` atomically creates or verifies/reuses `snapshots/KB-<full-sha256>`. Frozen bytes are never overwritten. Freeze is legal before mathematical readiness and does not confer it. `kb diff PROJECT --from OLD --to NEW` reports changes, affected dependents, consumed inputs and manuscript locations; historical outputs stay bound to their old snapshot.

Create an explicit plan with `output plan PROJECT --output ID --snapshot KB-...`; defaults are minimal/integrated. Set the audience, reader goals, prerequisites, selections, meaningful omissions and proof obligations. Read [selection](references/length-and-selection.md). Principal answers require complete canonical statements. Necessary local definitions and precise imported inputs cannot disappear during compression. An explicitly requested same-spine pair uses one comparison group with common questions, principals and decisive boundaries; unrelated output subsets need not have identical cores.

## 6. Prepare and write

Run `output prepare PROJECT --plan PROJECT/outputs/ID/plan.json`. Formal preparation requires readiness. Only explicit `--draft` permits a visibly `DRAFT_UNVERIFIED` internal scaffold; it can never be formally packaged. Preparation extracts exact statements, bibliography, conventions and bounded authoring materials. It preserves an existing manuscript instead of replacing authored prose. It does not automatically write a mathematical survey. Both generated fragments and all supplied `materials/` copies must match the fixed snapshot; structure/build/release reject altered, missing or extra materials. Keep editable author notes outside `materials/`; reprepare explicitly to restore copies while preserving the manuscript.

Read [introduction](references/introduction.md), [writing style](references/writing-style.md) and the selected [profile](references/editions.md). Insert complete statements through `\input{../generated/statements/N-....tex}`; only the surrounding wrapper/label/number may differ. Never hand-edit generated fragments. Minimal uses exactly three numbered main sections: Main Results, Key Mathematical Ingredients, Connecting the Ingredients. All principals appear completely in the first section; the second establishes genuinely consumed points and the third performs decisive mathematical connections. Thematic explains supported relationships and compares routes around its question. Lecture orders prerequisites and actually develops the promised calculations, intermediate lemmas and examples. Paper has an independent contribution/prior-art/full-proof contract. All four preserve exact shared claims.

For a finished writing/layout reference, consult the [user-polished balanced dHYM manuscript](assets/reference-samples/dhym-balanced/README.md) and [example roles](references/exposition-examples.md). Borrow useful local exposition, not its topic scope, six-page length or counts of sections and results. The separate Schur example demonstrates the knowledge-to-output workflow.

Do not invent decorative theorem or definition names. Author attributions are useful. Use mathematical formulas in place of wordy paraphrases, short clauses or itemized independent hypotheses, and focused conclusions. Put secondary consequences afterward. Omit trivial transitions. Repeat necessary local hypotheses rather than forcing needless backtracking. Examples must calculate, distinguish conditions or expose a boundary; no quotas. Neither page counts nor more words establish lecture quality.

New claims discovered while writing return to the KB for argument, review and a new snapshot before formal use. The surrounding prose must not enlarge a correct imported fragment. Minimal must be independently readable without an unrequested lecture; lecture must not claim full proofs of imported results. Paper must establish authorized original contributions, closest prior results and complete proofs; unverified or incomplete work stays internal draft.

## 7. Check, build, inspect and deliver

Use `output validate PROJECT --output ID --stage structure` for exact-fragment/literal-input and reusable TeX inventory checks. Read the entire final TeX of each version separately; record output-semantic findings against plan, actual source, generated fragments and authoring materials. Locate principal statements and every promised proof step. Software inventory guides reading; it does not understand or certify mathematical prose.

Run `output build PROJECT --output ID` to compile actual TeX/BibTeX until references stabilize. Run `output render PROJECT --output ID` to rasterize every actual page. Rendering is not inspection. Open every image, repair clipping, overlap, broken glyphs, bad page breaks and unreadable formulas; recompile/re-render and refresh affected review bindings. `output review-template ... --kind visual` creates a pending record only. Record substantive observations for each page against the actual PDF and image hashes. Read [build](references/layout-and-build.md).

`output validate PROJECT --output ID --stage release` rechecks actual files and all required evidence. Only `RELEASABLE` outputs can use `output package PROJECT --output ID --to FILE.zip`. Packages contain editable TeX, generated fragments, styles, selected knowledge/evidence, a plan and a standalone rebuild entry. Reopen and verify the archive. Exclude fonts, private data and restricted source texts. Only explicit user `max_pages` blocks length; suggestions are nonblocking reread prompts, never a reason to shrink typography or alter mathematical scope.

Report actual source-reading, semantic, build, render, page-inspection and reproducibility evidence separately. State the lack of independent review when applicable. Deliver only requested outputs and preserve lawful knowledge-only use.

## Maintenance boundary

Read [template maintenance](references/template-maintenance.md). Run executable asset checks, behavior tests and current/frozen style builds separately. A historical sample is not new-profile acceptance. The installation archive has an explicit nested-resource whitelist; test the extracted entry in an isolated environment.

This is Survey, not Research Studio. Preserve stable IDs, exact content, source versions, dependencies, snapshots and review status. Do not create Studio native markers, receipts, research phases, schedulers or a bridge skill. Ordinary Survey folders are not claimed to be natively importable by Studio.

## Manuscript review and build history

Read [output review](references/output-review.md) before release. Require canonical inputs in the actual document body, seven explicit whole-manuscript reading checks and real proof/principal locations. A template never grants acceptance. Preserve review and build attempts; a failed new build must not destroy or silently reuse the last successful build. Source, semantic and visual approval each require the actual recorded work.

## vNext exposition and publication contract

Before writing, read [reader calibration](references/reader-calibration.md),
[project overview](references/overview.md), [four profiles](references/editions.md)
and [self-contained writing](references/writing-style.md). Default to undergraduate
general plus topic-specific early doctoral capabilities; classify current inputs as
Assumed / Refreshable / Bridge-required. Work backward from the result and forward
from this reader. Fast understanding exposes actual inputs, decisive operations,
outputs and conditions; slow proofs must support exactly that route.

Keep the project overview a readable multi-question map, not a node list or Minimal's
third section. The per-output outline carries this article's choices. New implications
and comparisons discovered there return to reviewed KB nodes. Four knowledge views
do not generate four files and do not override mode responsibilities.

Principal results must be statement-self-contained: objects/domain, fixed vs unknown,
complete hypotheses, important equations, quantifiers/dependence, conclusion and status.
Review them alone and check surrounding prose. Repair deficient canonical nodes before
freezing again; do not change exported fragments. `review template PROJECT --kind
mathematical --id N-ID --principal-statements --to evidence/reviews/NEW.json` prepares
pending explicit self-contained observations, never an acceptance. New output-semantic
templates also require actual common/mode findings and every promised proof-step location.

Prefer short prose alternating with useful displayed equations, objects or estimates.
About four normal typeset lines is an editorial heuristic, not a hard line limit. Do
not add ornamental formulas, force breaks, shrink fonts or delete mathematics. Check
real PDFs and explain reasonable exceptions in existing page/semantic findings.

Paper planning defaults to DRAFT_UNVERIFIED. Classify every principal, bind authorized
provenance, closest verified prior-result and comparison nodes, exact difference and
complete proof obligations. A formal paper needs actual dated prior-art and full-proof
reading. Classic examples and synthetic tests cannot certify originality. Only an
explicitly promoted, ready and fully rereviewed plan may pass existing formal gates.

Historical releases keep their old policy, bytes and reviews; they are never reported
as newly accepted. Reprepare preserves existing main.tex and outline.md, not an automatic
upgrade. Software checks identity, structure and evidence, not mathematical truth,
reader understanding, authorization or originality. Author rereading remains author
rereading, even in another tool or context. Report unperformed independent and real-reader
checks separately. This candidate is not a formally published Release.

## rc2 design and historical policy

Read `artifacts.exposition_design` after prepare. Complete topic-specific audience,
reader goals and outline; structure and release reject unresolved default tasks.
Keep preview drafts visibly unverified. Repeated prepare preserves authored main,
outline and style. Knowledge readiness never requires an output outline.
Adopt rc2 with a new output ID and schema 2.2.0. Do not rewrite historical outputs.

Treat `view` as a reader task within the requested profile. Use the generated
node-specific reasons and emphasis order as editable navigation; inspect actual
node content before claiming a relation. Methods develops input-to-output
operations; boundaries locates failing hypotheses and distinguishes noncoverage
from counterexamples. Preserve the full principal, dependencies, decisive
boundaries and profile proof promises in every view. When no suitable node exists,
record the gap or justify why none is needed, returning new claims to the KB.
Record the current `scope.view` and a substantive `mode_findings.view_focus`
with available `node_ids` and actual body locations in each output reading.
Changing the view requires a fresh reading even if canonical bytes stay identical.
`--policy recorded` is a read-only assessment, never current release authorization.
