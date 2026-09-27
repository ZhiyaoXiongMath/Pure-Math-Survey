# Pure Math Survey

**Version 1.8.1.** A skill for source-grounded English mathematical surveys and substantive revisions, delivered as rebuildable TeX and inspected PDFs.

Default to Part V concise. An explicitly requested series selects Parts I–V concise; any nonempty part/edition selection is supported. Both concise and standard preserve core statements and key lemmas. Concise compresses proof interiors and routine calculations; standard develops the same mathematical routes more fully.

| Part | Reading task |
|---|---|
| I. Foundations and Models | Understand the objects, questions and explanatory models. |
| II. Results and Relations | Understand precise conclusions, conditions and relationships. |
| III. Proofs and Methods | Understand selected proof routes and decisive mechanisms. |
| IV. Applications, Boundaries and Problems | Understand applications, established limits and verified open problems. |
| V. A Thematic Review | Read one integrated account organized around a central question. |

## Install

Download [pure-math-survey-1.8.1.zip](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v1.8.1/pure-math-survey-1.8.1.zip) from the [latest release](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/latest). Extract it and copy the `pure-math-survey` folder into your local skills directory.

Alternatively, copy [skills/pure-math-survey](skills/pure-math-survey/) from this repository.

## Use

Invoke the skill with your topic, audience and requested parts or editions:

```text
Use $pure-math-survey to write Part V concise on [topic] for [audience].
```

The skill reconstructs definitions and ordered quantifiers before selecting answers, researches beyond the selected bibliography, and distinguishes mathematical status from editorial selection. It checks primary sources and their versions, states principal answers with necessary hypotheses, retains them in the shared concise/standard core, and explains the proof mechanisms. It supports revisions of existing surveys while preserving the requested scope.

See [SKILL.md](skills/pure-math-survey/SKILL.md) for the workflow and the [skill README](skills/pure-math-survey/README.md) for helper commands. Templates and optional reference samples support drafting and typesetting; source review and mathematical judgment remain essential.

## Requirements

Python 3.10+ is required for helper scripts. TeX builds use pdfLaTeX and the packages in `math-review.sty`. PDF utilities use PyMuPDF; pixel comparisons also use Pillow. STIX2 is the preferred font, with a reported Latin Modern fallback.
