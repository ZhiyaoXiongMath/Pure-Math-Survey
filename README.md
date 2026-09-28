# Pure Math Survey

**Version 2.0.2.** Build source-grounded mathematical knowledge first, then write
the requested English survey or lecture from an immutable snapshot.

The knowledge project stores precise questions, definitions, results, proof
mechanisms, relations, examples, boundaries and scoped source evidence. It can
be maintained without generating a manuscript. An author or agent performs
the mathematical reading and writing; the tools check file contracts, fixed
inputs, evidence bindings and actual builds.

| Profile | Reader task |
|---|---|
| **minimal** (default) | Get the precise answer, essential mechanism and decisive boundary quickly. |
| thematic | Understand related results and routes around a selected question. |
| lecture | Learn the prerequisite steps, calculations and declared proofs. |

Default requested output is **minimal + integrated**. Only requested profiles
are produced. Foundations, results, methods and boundaries are overlapping
knowledge views, not mandatory separate volumes. Only an explicit page limit
is a hard length constraint.

## Install

Download [pure-math-survey-2.0.2.zip](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.2/pure-math-survey-2.0.2.zip)
and its checksum from the [release](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.0.2).
Extract and copy the single `pure-math-survey` folder to your host's skills
directory. Replace the complete skill folder rather than mixing releases.
Alternatively, copy [skills/pure-math-survey](skills/pure-math-survey/) from this repository.

Existing v1 projects are preserved through [explicit migration](docs/MIGRATION.md).
Software version 2.0.2 continues to use data schema 2.0.0, preserving existing
native v2 snapshot identities. The old [v1.8.1 release](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v1.8.1) remains available.

## Use

```text
Use $pure-math-survey to build a knowledge base on [precise topic]. Do not write a manuscript yet.
```

```text
Use $pure-math-survey to write a minimal survey on [topic] for [audience], using the reviewed knowledge project.
```

```text
Use $pure-math-survey to develop lecture notes from this snapshot, with complete proofs of [specified steps].
```

Read the [workflow](skills/pure-math-survey/SKILL.md),
[file contracts and commands](skills/pure-math-survey/references/contracts.md),
and [validation boundaries](skills/pure-math-survey/references/validation.md).
New claims discovered during writing return to the knowledge project for review
and a new snapshot. Both generated statements and supplied authoring materials
are checked against that snapshot. Author self-review is recorded separately
from independent review; compilation and hashes do not establish correctness.

## Example and verification

The [Schur-complement example](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.2/pure-math-survey-2.0.2-schur-example.zip)
contains a new nine-node knowledge project, its actual source-reading notes,
knowledge-only update history, a two-page minimal survey, a three-page lecture,
and review-change impact evidence. The author's source PDF is not redistributed.
It records author self-review, not independent mathematical review.

The release includes a validation summary. Behavioral tests cover snapshot and
material integrity, scoped reviews, TeX body checks, history, migration and
packaging. Tests with synthetic accepted records are software fixtures only.

## Requirements and development

The native knowledge CLI uses Python 3.10+ and the standard library. Building
PDFs requires pdfLaTeX, BibTeX and TeX packages loaded by math-review.sty;
page counts and rendering use Poppler (`pdfinfo`, `pdftoppm`). STIX2 is preferred,
with a reported Latin Modern fallback. Optional legacy image-comparison tools
may additionally use PyMuPDF and Pillow.

```sh
python -m unittest discover -s tests -v
python skills/pure-math-survey/scripts/validate_assets.py --json
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.0.2.zip
python tools/verify_release.py ../pure-math-survey-2.0.2.zip --no-build
```

The test suite includes real TeX builds. Linux CI runs it on Python 3.10 and 3.12,
including actual symbolic-link rejection. A Windows machine without symlink
creation privilege reports that one test as skipped; it does not silently pass it.
See [changes](CHANGELOG.md). This release has no server, vector database,
research scheduler or Research Studio bridge.
