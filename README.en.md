# Pure Math Survey — R4 development preview

[简体中文](README.md) | **English**

For authors reading mathematical literature, maintaining traceable knowledge, and writing English surveys, lecture notes or research drafts. Read actual sources, build understandable fast/slow knowledge, then write only the requested manuscripts from a reviewed fixed snapshot. Knowledge-only work produces no article.

**This is prerelease `v2.1.0-r4-preview.1`; the software version remains 2.1.0.** Engineering checks pass, while the second real mathematical end-to-end round is still running. This is not a stable release or acceptance of all five mathematical cases. See [development status and evidence scope](docs/r4/development-status.md).

## Install the complete skill

1. Open the [GitHub prerelease page](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0-r4-preview.1) and download `pure-math-survey-2.1.0.zip` and `pure-math-survey-2.1.0.zip.sha256`. The installation ZIP differs from GitHub's automatically generated source ZIP.
2. Verify the download's SHA-256, extract it, and copy the complete `pure-math-survey/` folder into your host's user skills directory. For example, Codex's default user directory is `~/.codex/skills/`; use the host's configured directory if different. Keep SKILL, references, scripts and assets together; copying SKILL.md alone is insufficient.
3. Start a new chat that can access your project and sources, and invoke `$pure-math-survey`. The calling chat keeps its model. Its literature, knowledge, writing and review work chats are actually created with `gpt-6-astra / ultra` parameters.

The host needs Codex work-chat creation, reading, waiting and task-message tools, plus available Astra/ultra. Deterministic scripts require Python 3.10+ standard library. PDF generation additionally needs pdfLaTeX, BibTeX, the style's TeX packages and Poppler pdfinfo/pdftoppm. Missing capabilities are reported; serial role playing is not equivalent to actual dispatch.

Normal installation/use does not create symlinks or require the UAC elevation used in this engineering test. That prompt exercised rejection of an actual symlink; system permission settings were not changed. The installed [build and page-inspection instructions](skills/pure-math-survey/references/layout-and-build.md) provide the native workflow.

## First use: build knowledge

Replace the directory with your writable project path; attach available sources or permit original-source discovery. Specify what may and may not be read:

```text
Use $pure-math-survey to build a mathematical knowledge project at work/matrix-positivity.
Topic: positivity of finite real symmetric block matrices; require an invertible leading block
and exclude singular-pivot variants. Readers know undergraduate linear algebra. Explain the
objects, all conditions, both implications, the actual construction and its boundaries.
Build and review knowledge only for now; do not create an article or PDF. Find and actually
read original sources supporting these results.
You may read the complete installed skill, my supplied sources and this project. Write only
in this project and its exclusively owned work directories. Other private directories are
outside the read boundary; report any additional input needed.
This chat is the controller. I authorize necessary project-scoped Codex work chats, all using
 gpt-6-astra / ultra, for sources, paired fast/slow knowledge, writing and non-author review.
I authorize this controller to send those chats tasks, continuation, revisions and stop
instructions, read their results and deliver them.
```

Authorization comes from the human actually sending the instruction, not from this document. Existing valid authorization within the same scope is reused; a specific authorization is requested once only when the host requires it and it is missing. The controller forwards accurate installation/source/output boundaries to each worker, which does not recursively create chats. A ban on the global same-named skill differs from a ban on all global helper skills; the actual boundary must be respected.

The controller arranges source reading, knowledge candidates and non-author review, inspects actual returned files/evidence, and is the sole writer integrating canonical knowledge. Fast passages explain goals, inputs, decisive operations, outputs, consumers and conditions. Linked slow passages perform promised derivations and precise external-theorem applications. You receive editable nodes, a project overview, source/review records and explicit gaps. Freezing fixes bytes, not mathematical readiness.

## Then request a manuscript

After knowledge review, continue in the same chat:

```text
Write one English Minimal survey from this knowledge project, view=integrated, with unchanged scope.
Readers still know undergraduate linear algebra. State the complete main results and show the
 decisive two-way argument and where the conditions enter. Do not add other modes or call known
results original. Deliver editable TeX and a readable PDF; supply a rebuildable article package
only after its actual current delivery checks pass, otherwise explain draft status or blockers.
Reuse this project's work-chat authorization and read/write boundaries.
```

The controller first coordinates this manuscript's concrete reader/proof promises and obtains corresponding actual non-author knowledge checks. Fresh evidence enters a new snapshot, then a writer completes the body. `prepare` creates fixed materials and an unfinished scaffold; it does not automatically write a valid proof. Completion still requires mathematical/exposition review, TeX building, observation of every PDF page, and applicable unpacked rebuilding.

A completed article project contains `outputs/ID/plan.json`, `outline.md`, `manuscript/main.tex`, fixed `generated/` and `materials/`, `build/main.pdf`, and corresponding review/build evidence. A rebuildable ZIP is supplied when formal permission passes. This describes the delivery structure; it does not claim the initialization example below generated those files. Knowledge-only work has no implicit manuscript.

To update knowledge, identify new sources, corrections or questions and request verification into the live KB before freezing a new snapshot. Previous snapshots/delivered files remain unchanged. To request Lecture or another output, specify the new audience, proof depth and count; the controller obtains applicable evidence and creates a new output without overwriting an old article. You do not manually fill review JSON: actual workers produce the records and the controller checks them. Unperformed work cannot become accepted evidence.

## Choose a mode

| Profile | Use | Required body |
|---|---|---|
| **minimal** (default) | Understand complete results and decisive reasons quickly. | No abstract; exactly Main Results, Key Mathematical Ingredients, Connecting the Ingredients; all complete principals in section one. |
| thematic | Understand genuine methods and comparable conclusions within a topic. | No abstract; first section states precise questions and representative complete results, then difficulties, mechanisms and supported synthesis. |
| lecture | Learn to reproduce constructions, calculations and proofs. | No abstract; first section gives the full core goal theorem and faithful route, then promised derivations and first uses from declared prerequisites. |
| paper | Organize research contributions or an internal research draft. | Concise abstract and full Introduction; accurate prior comparisons and rigorous proofs. Defaults visibly to DRAFT_UNVERIFIED. |

Only Minimal fixes the main section count/titles. Default requested output is minimal + integrated; only requested modes/count are produced. Five views—integrated, foundations, results, methods, boundaries—change emphasis, not facts. Four modes share one canonical mathematical authority and immutable snapshots.

Current duties retain F1–F4: actual body locations for proofs/principals, view/design consistency, real comparisons and original-source support, and incomplete-design/draft safety. Obligation coverage, fast-route reconstruction, slow-step reproduction and condition-transfer checks remain required. Ordinary explanatory prose actively targets about 2–3 normal typeset lines; necessary long statements need specific reasons, never omitted hypotheses or smaller type. See [mode contracts](skills/pure-math-survey/references/editions.md) and [knowledge to manuscripts](skills/pure-math-survey/references/knowledge-to-manuscript.md).

A correct known-result proof is not an original contribution. Unverified Paper may deliver a prominent draft and preview PDF; formal research packaging must reject it. Compilation, AI non-author review and software tests do not establish originality, external peer review or real student learning.

## Optional: an actually executed CLI initialization example

Chat is the daily entrypoint. The CLI performs file operations/engineering checks and does not dispatch chats. This initialization and structural validation were actually executed. In a directory containing the extracted `pure-math-survey/` folder, create UTF-8 `scope-input.md`:

```markdown
# Scope

Build a source-grounded knowledge project on positivity of finite real symmetric block matrices with an invertible leading block. Exclude singular-pivot variants. Readers know undergraduate linear algebra. This initialization demonstration does not request a manuscript or certify any theorem.
```

Run in the writable demonstration directory:

```sh
python pure-math-survey/scripts/survey.py --version --json
python pure-math-survey/scripts/survey.py init --output my-topic --topic matrix-positivity --scope scope-input.md --json
python pure-math-survey/scripts/survey.py kb validate my-topic --json
```

For a source checkout, the relative script path is `skills/pure-math-survey/scripts/survey.py`. The actual run with this version's CLI returned:

| Call | Actual result |
|---|---|
| --version | version=2.1.0; policy=four-modes-2026-10-13-r4; only output schema 2.2.0 / current r4 is supported. |
| init | INITIALIZED; review_status=pending; outputs=[]. |
| kb validate | VALID; node_count=0; source_count=0; SEMANTIC_NOT_CERTIFIED warning. |

Files created: `my-topic/project.json`, `scope.md` and `knowledge/{overview.md,conventions.tex,discovery.md,coverage.json}`. This is an empty unverified knowledge project, without accepted review, article, PDF or article package. Structural validity is not mathematical readiness. Actual source reading, knowledge writing and review are later steps; this small example is not full mathematical end-to-end acceptance.

## Current verification, support and license

The current Windows independent installation passed **280/280 engineering tests with 0 skipped**. The 69 archive members / 68 runtime resources match their fixed identities, and a three-page neutral TeX build check passed. These are engineering/style evidence, not five accepted mathematical exemplars. Round 1 failed overall with some bounded mathematical/PDF evidence. Current Round 2 continues; the user has required that Round 3 not start. If Round 2 fails, stop and report without further runtime fixes. In this round, Schur Paper's non-author knowledge review completed without revision, but ordinary kb readiness --plan blocks the known result for lacking an original contribution. Actual DRAFT_UNVERIFIED preview, formal-delivery refusal and three variant checks will still be completed. Independent verification is ongoing and final E05 acceptance is pending; this is neither a resolved finding nor a claim that every Paper has a confirmed defect. See [development status](docs/r4/development-status.md).

Software is 2.1.0, knowledge/snapshot schema is 2.0.0, output/policy-review schema is 2.2.0, and policy is four-modes-2026-10-13-r4. Only current r4 is supported; explicit old/unknown contracts are rejected without modifying their files. No recorded-policy release route, historical template selection or migration service is provided. Reprepare preserves authored body/outline/style; previous snapshots/evidence cannot be upgraded to accepted through edited hashes. Daily use has no fixed three-round limit from this development test.

Read the [full entrypoint](skills/pure-math-survey/SKILL.md), [commands/fields](skills/pure-math-survey/references/contracts.md), and [validation boundaries](skills/pure-math-survey/references/validation.md). Software installation ZIP, mathematical article package and GitHub software Release are distinct. Old generated exemplars are absent from the current public set; failed drafts are not presented as accepted examples.

Instructions, scripts, templates and documentation use the [MIT License](LICENSE), Copyright (c) 2026 ZhiyaoXiongMath. Mathematical material and third-party originals retain their rights; reading access is not redistribution permission. Public packages exclude private authorization ledgers and restricted originals.
