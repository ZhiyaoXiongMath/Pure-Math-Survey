# Pure Math Survey — Preview

[简体中文](README.md) | **English**

This is preview `v2.1.0-r4-preview.1` (software 2.1.0); mathematical end-to-end acceptance is still under verification. [Development status](docs/r4/development-status.md) records actual progress.

For authors organizing mathematical literature, maintaining traceable knowledge, and writing English surveys, lectures or research drafts.

## Modes

| Mode | Task and structure |
|---|---|
| **Minimal** | Understand complete results and decisive reasons concisely; no abstract, exactly Main Results / Key Mathematical Ingredients / Connecting the Ingredients, all complete principals in section one. |
| **Thematic** | Explore topical questions, genuine methods and synthesis under comparable conditions; no abstract, precise questions and representative complete results first. |
| **Lecture** | Reproduce constructions, calculations and proofs; no abstract, a full goal theorem and faithful route guide teaching derivations. |
| **Paper** | Organize research materials; concise abstract and full Introduction, accurate contribution position and arguments; visibly DRAFT_UNVERIFIED by default. |

**Minimal + integrated** defaults only when an article is requested without a mode. Five views—integrated, foundations, results, methods, boundaries—change emphasis, not facts or duties; generate only requested counts. Knowledge-only is not a fifth article mode and produces no manuscript.

Known results cannot be called original. Formal Paper research delivery requires real authorization, contribution verification and complete proofs; unverified drafts cannot be formally packaged. See [mode contracts](skills/pure-math-survey/references/editions.md).

## Start prompts

Download the complete `pure-math-survey-2.1.0.zip` and `pure-math-survey-2.1.0.zip.sha256` from the [Release page](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0-r4-preview.1). Verify and copy the whole extracted `pure-math-survey/` into the host skills directory (for example Codex's `~/.codex/skills/`), retaining references, scripts and assets. The automatically generated Source code ZIP is not the installation ZIP.

The host needs work-chat creation/read/wait/task-message tools and available `gpt-6-astra / ultra`. Scripts use Python 3.10+ standard library; PDFs need pdfLaTeX, BibTeX, the style's TeX packages and Poppler. Missing capabilities are reported; see [build requirements](skills/pure-math-survey/references/layout-and-build.md).

In a new chat send the shared authorization together with one prompt below. Replace brackets with your topic, audience, sources and project. These describe **requests and expected delivery, not completed mathematical examples**.

```text
This chat is the controller. I authorize gpt-6-astra / ultra work chats within [project path]
for sources, fast/slow knowledge, writing and non-author review, and task/continuation/revision/
stop messages to them; read their results. Read the complete installed skill, specified sources
and this project; write only within the project.
```

**Minimal**

```text
Use $pure-math-survey with [source files/URLs] for [topic and scope], for readers with
[background]. Write one English Minimal, view=integrated, with complete principals,
necessary ingredients and decisive reasons.
```

Expected: editable TeX, inspected PDF, and a rebuildable package when delivery permission passes.

**Thematic**

```text
Use $pure-math-survey with [source files/URLs] for [topic and scope], for readers with
[background]. Write one English Thematic around real questions/methods and synthesize
results under comparable conditions.
```

Expected: thematic TeX/PDF with actual source/review evidence, and an eligible rebuildable package.

**Lecture**

```text
Use $pure-math-survey with [source files/URLs] to teach [topic and scope], for readers with
[background]. Write one English Lecture fully developing [specified constructions,
calculations or proof steps], with disclosed external inputs.
```

Expected: lecture TeX/PDF fulfilling the promised derivations, and an eligible rebuildable package.

**Paper**

```text
Use $pure-math-survey with [my research materials and original sources] for [problem and scope],
for readers with [background]. Write one English Paper working draft; distinguish known,
candidate and unverified content, invent no originality, and retain DRAFT_UNVERIFIED.
```

Expected: visibly marked draft TeX and an allowed preview PDF; no formal article package without research-delivery verification.

**Knowledge only**

```text
Use $pure-math-survey to read [source files/URLs] and build knowledge for [topic and scope],
for readers with [background]. Explain results, conditions, fast routes and slow derivations;
do not produce an article or PDF.
```

Expected: overview, editable nodes, source/review records and explicit gaps. Authorization comes from your actual instruction and is reused within scope; users do not manually fill review JSON.

## How it runs

The calling chat is the controller and keeps its model. It dispatches real work chats, reads actual files and is the sole canonical knowledge integration writer. Fast passages explain goals, inputs, operations and uses; slow passages perform derivations and precise external-theorem applications. Non-authors check the requested proof promises.

```mermaid
flowchart TD
    A["Calling chat: controller"] --> B["Read actual original sources"]
    B --> C["Paired fast/slow knowledge"]
    C --> P["Knowledge goals and manuscript proof promises"]
    P --> D["Non-author knowledge review"]
    D -->|"Necessary knowledge revisions"| C
    D -->|"Required checks complete"| E["Fixed immutable snapshot"]
    E -->|"Knowledge only"| K["Knowledge and evidence delivery"]
    E -->|"Article requested"| F["Adopt the reviewed manuscript plan"]
    F --> G["Separate writer completes TeX"]
    G --> H["Mathematical and exposition review"]
    H -->|"Knowledge or argument gaps"| C
    H -->|"Body revisions"| G
    H -->|"Required review complete"| I["Compile PDF"]
    I --> J["Actually inspect every page"]
    J -->|"Layout revisions"| G
    J -->|"Actual delivery permission"| L["Eligible package or marked draft delivery"]
```

Plans/proof promises are fixed before output-specific knowledge review; the diagram's manuscript plan implements that reviewed design. Freezing fixes bytes, not readiness. `prepare` supplies materials/scaffolding; writers still author the body. Compilation, rendering and hashes replace neither mathematical checking nor all-page observation. Unmet conditions are reported, not waived.

Knowledge delivers overview/nodes/sources/evidence. Articles add plan, outline, `manuscript/main.tex`, fixed materials, `build/main.pdf` and review records. New sources/corrections return to knowledge review before a new snapshot, preserving old files. Specify each additional mode, audience and count: a snapshot may be shared, with separate writing/review.

Only current r4 is supported; old/unknown output contracts are rejected without file modification. See [entrypoint](skills/pure-math-survey/SKILL.md) and [validation limits](skills/pure-math-survey/references/validation.md). AI review is not external peer review or originality certification. Code/instructions/templates use [MIT License](LICENSE); mathematical materials and third-party sources retain their rights.
