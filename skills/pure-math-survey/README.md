# Pure Math Survey 2.1.0

[简体中文](README.zh-CN.md) | **English**

Build and review source-grounded mathematical knowledge, then write only the requested English survey, lecture or research-paper draft from an immutable snapshot. Knowledge-only requests produce knowledge and evidence without a manuscript or PDF.

Software is **2.1.0**, knowledge/snapshot schema **2.0.0**, output/policy-review schema **2.2.0**, and current editorial policy **four-modes-2026-10-15-r5**. This installation supports current r5 only. Explicit old/unknown policies and unsupported inputs receive clear unsupported diagnostics; their files remain unchanged. There is no recorded-policy validation, historical-template selection or migration service.

## Start in the calling chat

Add your precise topic, full scope, reader prerequisites and proof depth for every requested output, project path, permitted installation/source paths or URLs and actual read/write boundaries to this human instruction:

> Use $pure-math-survey for my mathematical task. This chat is the controller. I authorize this controller to create necessary project-scoped Codex work chats, all using gpt-6-astra / ultra, for source reading, paired fast/slow knowledge, writing and non-author review. I authorize it to message these work chats with tasks, continuation, revisions and stop instructions; read their results and deliver only my requested outputs.

The calling chat keeps its current model/effort. Its workers are actual new chats created with model/effort arguments, not prose labels. Authorization must come from the human or trusted locatable human evidence. If the host needs explicit new-chat authorization and none exists, the controller asks once while preparing independent scope work; existing valid authorization is reused. Workers carry role=worker and do not recursively dispatch.

Required host capabilities include create/read/list/wait/message chat tools and gpt-6-astra / ultra. Missing authorization, tools or model support is a reported blocker. Serial role playing or lower-effort agents cannot count as an equivalent automatic workflow. The controller alone integrates canonical live knowledge; workers own isolated candidate/output/review directories. Critical acceptance comes from a non-author worker. Private task notes record fixed inputs, real IDs, pending/unknown creation, deduplication, recovery and stop boundaries. See [dispatch](references/dispatch.md) and [start prompt](references/user-start.md).

Each real dispatch carries the exact human/parent read boundaries and allowed installed resources, original sources, snapshot inputs and owned output/evidence paths. Workers enforce those boundaries before loading auxiliary workflows. A ban on the global same-named skill differs from a ban on all global skills; an actual blanket ban includes a global PDF skill. The installed native build/page-inspection reference supplies source rendering, real all-page observation and rebuild records without requiring a global helper. Missing permitted capability is reported, not bypassed.

## Four modes, one canonical knowledge base

| Profile | Opening and body |
|---|---|
| **minimal** (default) | No abstract. Exactly Main Results / Key Mathematical Ingredients / Connecting the Ingredients; all complete principals in section one, callable consumed inputs in section two, actual decisive reasoning in section three. |
| thematic | No abstract. First section states precise questions and representative full results with comparison conditions; body explains real difficulties, methods/mechanisms and supported synthesis. |
| lecture | No abstract. First section states objectives, full core goal theorem and faithful route; body teaches promised constructions, calculations, proofs and first uses. |
| paper | Concise abstract and full Introduction comparing prior work, difficulty, complete new results, precise differences and proof route; body completes rigorous proofs. Defaults visibly to DRAFT_UNVERIFIED. |

Only Minimal has fixed section count/titles/order. Necessary subsections and References do not add a fourth mathematical section. Thematic and Lecture cannot retain a renamed front matter summary. Known-result Paper drafts attribute known claims accurately; they do not establish novelty or receive original-research release permission.

Default requested output is **minimal + integrated**. Generate only requested modes/count. Five views (integrated/foundations/results/methods/boundaries) change emphasis, not facts or profile duties. All modes consume one reviewed knowledge snapshot. Fast passages expose targets, objects, inputs, operation, output, consumer and conditions; linked slow passages perform promised derivations and exact imports. Prepare creates fixed materials and an unfinished TeX scaffold; authors still write. New reusable explanations or changed mathematics return to reviewed live knowledge and a new snapshot. See [mode contracts](references/editions.md) and [knowledge to TeX/PDF](references/knowledge-to-manuscript.md).

Coordinate all requested outputs' concrete reader capabilities and exact proof promises before final knowledge review. A non-author reviewer reconstructs obligations, actually checks each promised step and records exact scope.proof_steps with real findings/locators and gaps. Fresh live evidence precedes a new snapshot and explicit plan adoption/prepare. Never copy labels into accepted records, edit old snapshots or refresh old accepted hashes. Existing task-specific feedback/recheck and stop allowances govern the whole process; there is no extra repair route or universal product round limit.

Use `review validate` for batch evidence diagnostics and `review accept` for final candidate staging with rollback; freeze and explicitly adopt afterward. Templates cover applicable canonical dependencies and remain pending. See [review handoff](references/proofs-and-boundaries.md#review-handoff-and-candidate-acceptance).

## Install and verify

Copy this complete folder to your host skills directory, or run the scripts directly.

```sh
python scripts/package_release.py --output ../pure-math-survey-2.1.0.zip
python scripts/survey.py --version --json
python scripts/validate_assets.py --json
python scripts/survey.py init --output my-topic --topic my-topic --scope my-scope.md --json
```

Extract the archive and use the complete pure-math-survey folder; verify its member checksums and archive SHA-256. Initialization needs a real UTF-8 scope file and creates an empty unverified knowledge project. The deterministic CLI uses Python 3.10+ and the standard library. PDF builds require pdfLaTeX, BibTeX and packages loaded by math-review.sty; page counting/rendering uses Poppler pdfinfo/pdftoppm. Source discovery uses the agent's tools; the CLI does not create chats or run a background scheduler.

Read [SKILL](SKILL.md), [file contracts/commands](references/contracts.md), [build requirements](references/layout-and-build.md) and [validation boundaries](references/validation.md). Reprepare preserves authored main/outline/style. Never edit frozen bytes, materials or generated canonical fragments. Inspect every actual final PDF page and record current identities, concrete findings, repairs and justified longer-block exceptions to ordinary prose's active 2–3 normal typeset-line target. Rendering is not inspection.

Formal article packaging requires current-policy RELEASABLE evidence. Unverified Paper may deliver a prominently marked draft TeX/preview PDF while formal packaging is rejected. Old-policy runtime validation is unsupported; do not rename or migrate old accepted evidence. Software installation ZIP, article package and software Release are distinct. Structural tests, hashes, AI non-author review and compilation do not prove truth, originality, external peer review or student learning; report each executed scope and remaining limitations separately.

## Examples and license

Old generated example manuscripts, knowledge projects and reference-sample bundles are removed from the current tree and installation. Historical identities remain recoverable in Git history/private backups; do not import them as answers or new acceptance. Current public exemplars require fresh source-grounded generation and actual independent acceptance; this documentation does not claim those tests have run.

Instructions, scripts, templates and documentation are covered by the [MIT License](LICENSE), Copyright (c) 2026 ZhiyaoXiongMath. Mathematical example materials and third-party originals retain their separate rights; access is not redistribution permission. Private authorization/dispatch notes and restricted source texts are excluded from public bundles.

Source access, actual scoped reading, verifiable bytes and original redistribution permission are independent facts; private/unauthorized original bytes cannot be frozen in a public project. Knowledge READY and Paper research eligibility have separate gates. See [source evidence](references/research-and-evidence.md).
