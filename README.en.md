# Pure Math Survey

> **2.1.0-rc1 is a development candidate, not a published release.** Install the complete skill directory from this branch or build its candidate ZIP. Historical release links below do not install vNext. See [four writing profiles](skills/pure-math-survey/references/editions.md).
> Minimal has exactly Main Results / Key Mathematical Ingredients / Connecting the Ingredients. Thematic requires supported synthesis, Lecture every promised derivation, and Paper authorized contribution, closest-prior-art and complete-proof reviews. Paper defaults to an unverified internal draft. Software cannot certify truth, originality or comprehension.
> Knowledge schema is 2.0.0; new plans and policy-bearing reviews use 2.1.0. No historical snapshot, manuscript or review is automatically migrated or accepted under the new policy.


[简体中文](README.md) | **English**

**Candidate 2.1.0-rc1; not a published Release.** Build source-grounded mathematical knowledge first, then write the requested English survey or lecture from an immutable snapshot.

The knowledge project stores precise questions, definitions, results, proof mechanisms, relations, examples, boundaries and scoped source evidence. It can be maintained without generating a manuscript. An author or agent performs the mathematical reading and writing; the tools check file contracts, fixed inputs, evidence bindings and actual builds.

| Profile | Reader task |
|---|---|
| **minimal** (default) | Get the precise answer, essential mechanism and decisive boundary quickly. |
| thematic | Understand related results and routes around a selected question. |
| lecture | Learn and reproduce all promised constructions, calculations and proof steps. |
| paper | Audit authorized original contributions, closest prior results and complete proofs; default to an unverified internal draft. |

Default requested output is **minimal + integrated**. Only requested profiles are produced. Foundations, results, methods and boundaries are overlapping knowledge views, not mandatory separate volumes. Only an explicit page limit is a hard length constraint.

## Install

**For the historical stable version only**, download [pure-math-survey-2.0.4.zip](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.4/pure-math-survey-2.0.4.zip)
and its checksum from the [v2.0.4 release](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.0.4).
Extract and copy the complete `pure-math-survey` folder to your host application's skills directory.
Alternatively, copy [skills/pure-math-survey](skills/pure-math-survey/) from this repository.

Release attachments provide only the installation archive and checksums. The examples below are stored in the repository and do not need to be downloaded separately to use the skill.
Knowledge/project/node/snapshot schema remains 2.0.0. New plans and policy-bearing reviews use 2.1.0; old software cannot parse them. Historical plans remain readable under their explicitly reported legacy policy, without modification.

## Use

```text
Use $pure-math-survey to build a knowledge base on [precise topic]. Do not write a manuscript yet.
```

```text
Use $pure-math-survey to write a minimal English survey on [topic] for [audience], using the reviewed knowledge project.
```

```text
Use $pure-math-survey to develop English lecture notes from this snapshot, with complete proofs of [specified steps].
```

Read the [workflow](skills/pure-math-survey/SKILL.md), [file contracts and commands](skills/pure-math-survey/references/contracts.md), and [validation boundaries](skills/pure-math-survey/references/validation.md).
New claims discovered during writing return to the knowledge project for review and a new snapshot. Both generated statements and supplied authoring materials are checked against that snapshot. Author self-review is recorded separately from independent review; compilation and hashes do not establish correctness.

## Examples

### dHYM: writing and layout reference

The six-page balanced dHYM survey, supplied by its author after multiple rounds of deliberate polishing, is the principal finished writing and layout reference. It moves from precise solvability results to proof mechanisms, local stability definitions and an explicit equality-wall example. Its length, outline and result counts are not requirements for other surveys.

- [Read the PDF](examples/dhym-balanced/dhym-survey-revised.pdf)
- [Standalone TeX source](examples/dhym-balanced/dhym-survey-revised.tex)
- [How to use this writing reference](skills/pure-math-survey/assets/reference-samples/dhym-balanced/README.md)

The example directory contains only a `.tex` and a `.pdf`. The TeX includes the required custom style and bibliography without changing the mathematical text; the PDF is the unchanged file supplied by the author.

### Schur complement: knowledge-to-output workflow

[Download the Schur-complement example](examples/schur-complement/pure-math-survey-2.0.4-schur-example.zip). It contains a nine-node knowledge project, actual source-reading notes, an immutable knowledge snapshot, a two-page minimal survey and a three-page lecture, demonstrating the full workflow. Its review mode is author self-review; it does not claim independent mathematical review. The original source PDF is not redistributed.

### Paired input/output example: Schur complement

**Input:**

```text
Use $pure-math-survey to study strict positive definiteness of finite real symmetric
block matrices with an invertible leading block. Build the knowledge base and read
the original sources, then write a minimal English survey and English lecture notes
from the same snapshot. Explain the strict boundary and exclude the general
singular-pivot extension.
```

**Corresponding output:** The repository's Schur example supplies the `project/`
knowledge project and fixed snapshot, `pdf/schur-minimal.pdf` (two pages),
`pdf/schur-lecture.pdf` (three pages), and their TeX manuscripts and review records.
These are completed artifacts of this example. New topics require actual reading,
writing and checks; initialization creates only a project, not a manuscript.

The public example omits old build history, temporary TeX files and raw command
logs. Machine paths in build/render records are redacted; mathematics, snapshots,
PDFs and page images are unchanged, with a new record of actual page inspection.

## Requirements and development

The native knowledge CLI uses Python 3.10+ and the standard library. Building PDFs requires pdfLaTeX, BibTeX and TeX packages loaded by `math-review.sty`; page counts and rendering use Poppler (`pdfinfo`, `pdftoppm`). STIX2 is preferred, with a reported Latin Modern fallback. Optional PDF image-comparison tools additionally use PyMuPDF and Pillow.

```sh
python -m unittest discover -s tests -v
python skills/pure-math-survey/scripts/validate_assets.py --json
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0-rc1.zip
python tools/verify_release.py ../pure-math-survey-2.1.0-rc1.zip --no-build
```

Tests cover snapshot and material integrity, scoped reviews, TeX body checks, history and packaging, including real TeX builds. Synthetic accepted records are software fixtures only. Linux CI runs on Python 3.10 and 3.12; a Windows machine without symlink creation privilege explicitly reports the corresponding test as skipped.

See [version notes](CHANGELOG.md). This release has no server, vector database, research scheduler or Research Studio bridge.

## License

The project's skill instructions, scripts, templates and documentation are licensed under the [MIT License](LICENSE), with `Copyright (c) 2026 ZhiyaoXiongMath`.

Mathematical example materials are reserved separately: contents of `examples/` and `skills/pure-math-survey/assets/reference-samples/dhym-balanced/`, including their TeX, PDFs, bibliographies and example projects, are excluded from this MIT grant. Adding this license grants no additional reuse permission for those materials and does not change existing third-party rights.

## vNext acceptance evidence

See [requirements and implementation map](docs/vnext/requirements.md), [actual validation and limitations](docs/vnext/validation.md), and [seven authored benchmark sources](examples/vnext/README.md). Six known-mathematics samples were compiled and author-reviewed; the Paper boundary sample is deliberately non-releasable. Independent review, real-reader feedback, and genuine original-Paper quality are NOT VERIFIED.
