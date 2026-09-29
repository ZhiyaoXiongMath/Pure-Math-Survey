# Pure Math Survey

**Version 2.0.3.** Build source-grounded mathematical knowledge first, then write
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

Download [pure-math-survey-2.0.3.zip](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.3/pure-math-survey-2.0.3.zip)
and its checksum from the [release](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.0.3).
Extract and copy the single `pure-math-survey` folder to your host's skills
directory. Replace the complete skill folder rather than mixing releases.
Alternatively, copy [skills/pure-math-survey](skills/pure-math-survey/) from this repository.

Software version is 2.0.3; its data format uses schema 2.0.0.

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

## Examples and verification

The [balanced dHYM survey](skills/pure-math-survey/assets/reference-samples/dhym-balanced/README.md)
is the principal research-survey writing and layout reference: a six-page manuscript
supplied by the user after multiple rounds of polishing. It moves from precise
solvability results to proof mechanisms, local stability definitions and an
explicit equality-wall example. Its source and PDF are preserved unchanged;
its length, outline and result counts are not requirements for other surveys.
Download the [PDF](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.3/dhym-survey-revised.pdf)
or the [TeX/PDF archive](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.3/dHYM_survey_balanced_source.zip).
The archive contains exactly two files: a standalone TeX with its style and
bibliography included, and the unchanged PDF. It contains no project manifests,
editorial records, build logs or development history.

The [Schur-complement example](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.3/pure-math-survey-2.0.3-schur-example.zip)
is the separate workflow demonstration. It contains a nine-node knowledge project, its actual source-reading notes,
an immutable knowledge snapshot, a two-page minimal survey and a three-page lecture.
The author's source PDF is not redistributed.
It records author self-review, not independent mathematical review.

Behavioral tests in this repository cover snapshot and
material integrity, scoped reviews, TeX body checks, history and
packaging. Tests with synthetic accepted records are software fixtures only.

## Requirements and development

The native knowledge CLI uses Python 3.10+ and the standard library. Building
PDFs requires pdfLaTeX, BibTeX and TeX packages loaded by math-review.sty;
page counts and rendering use Poppler (`pdfinfo`, `pdftoppm`). STIX2 is preferred,
with a reported Latin Modern fallback. Optional PDF image-comparison tools
may additionally use PyMuPDF and Pillow.

```sh
python -m unittest discover -s tests -v
python skills/pure-math-survey/scripts/validate_assets.py --json
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.0.3.zip
python tools/verify_release.py ../pure-math-survey-2.0.3.zip --no-build
python tools/package_dhym_example.py --output ../dHYM_survey_balanced_source.zip
```

The test suite includes real TeX builds. Linux CI runs it on Python 3.10 and 3.12,
including actual symbolic-link rejection. A Windows machine without symlink
creation privilege reports that one test as skipped; it does not silently pass it.
See [changes](CHANGELOG.md). This release has no server, vector database,
research scheduler or Research Studio bridge.
