# Pure Math Survey

> **Software version 2.1.0 release preparation; the tag and GitHub Release are not published.** Copy the complete skill directory from this repository or build a local installation ZIP from source. See [four writing profiles](skills/pure-math-survey/references/editions.md).
> Under r3, Minimal uses local problem units keeping full results, needed points, decisive connections and first use nearby; historical r2/rc1 and rc2 retain the strict three-section policy. Thematic requires supported synthesis, Lecture every promised derivation, and Paper authorized contribution, closest-prior-art and complete-proof reviews. Paper defaults to an unverified internal draft. Software cannot certify truth, originality or comprehension.
> Knowledge schema is 2.0.0; new plans and policy-bearing reviews use 2.2.0. No historical snapshot, manuscript or review is automatically migrated or accepted under the new policy.


[简体中文](README.md) | **English**

**Pure Math Survey 2.1.0** is for authors maintaining mathematical knowledge and writing manuscripts: build source-grounded knowledge first, then write the requested English survey, lecture or research-paper draft from an immutable snapshot.

The knowledge project stores precise questions, definitions, results, proof mechanisms, relations, examples, boundaries and scoped source evidence. It can be maintained without generating a manuscript. An author or agent performs the mathematical reading and writing; the tools check file contracts, fixed inputs, evidence bindings and actual builds.

| Profile | Reader task |
|---|---|
| **minimal** (default) | Get the precise answer, essential mechanism and decisive boundary quickly. |
| thematic | Understand related results and routes around a selected question. |
| lecture | Learn and reproduce all promised constructions, calculations and proof steps. |
| paper | Audit authorized original contributions, closest prior results and complete proofs; default to an unverified internal draft. |

Default requested output is **minimal + integrated**. Only requested profiles are produced. Foundations, results, methods and boundaries are overlapping knowledge views, not mandatory separate volumes. Only an explicit page limit is a hard length constraint.

## Install

For now, copy the complete [skills/pure-math-survey](skills/pure-math-survey/) folder from this repository to your host application's skills directory. Alternatively, build a local installation archive from the repository root:

```sh
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0.zip
```

Extract and copy the complete `pure-math-survey` folder to your host application's skills directory. The build script also creates the member-checksum manifest and ZIP SHA-256 checksum file. The `v2.1.0` tag and GitHub Release are not published, so official download attachments for this version are not yet available. The examples below are stored in the repository and do not need to be downloaded separately to use the skill.
The software version is 2.1.0. Knowledge/project/node/snapshot schema remains 2.0.0. New plans and policy-bearing reviews use 2.2.0; old software cannot parse them. Historical plans remain readable under their explicitly reported legacy policy, without modification.

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
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0.zip
python tools/verify_release.py ../pure-math-survey-2.1.0.zip --report ../pure-math-survey-2.1.0-verification.json
```

Tests cover snapshot and material integrity, scoped reviews, TeX body checks, history and packaging, including real TeX builds. Synthetic accepted records are software fixtures only. Linux CI runs on Python 3.10 and 3.12; a Windows machine without symlink creation privilege explicitly reports the corresponding test as skipped.

See [version notes](CHANGELOG.md). This version has no server, vector database, research scheduler or Research Studio bridge; r3 requires fast routes and reproducible slow explanations in the knowledge base itself; their actual quality must be verified for each task.

## License

The project's skill instructions, scripts, templates and documentation are licensed under the [MIT License](LICENSE), with `Copyright (c) 2026 ZhiyaoXiongMath`.

Mathematical example materials are reserved separately: contents of `examples/` and `skills/pure-math-survey/assets/reference-samples/dhym-balanced/`, including their TeX, PDFs, bibliographies and example projects, are excluded from this MIT grant. Adding this license grants no additional reuse permission for those materials and does not change existing third-party rights.

## Validation evidence and boundaries

The [rc2 candidate validation record](docs/rc2/CANDIDATE.md) preserves that stage's actual results and commit identities; it does not replace verification of the final release commit. rc2 preserves the historical examples and adds a real Simon–Maitre–Barrett–Süli three-paper project, paired methods/boundaries manuscripts, and a new Schur Lecture. The [editable project](examples/rc2/projects/time-compactness/README.md) and scoped author/page observations are retained. Reviewed PDFs, page images and build records in the historical candidate materials apply only to their recorded bytes; a fresh PDF build needs its own visual review.

See also the [requirements and implementation map](docs/vnext/requirements.md), [actual validation and limitations](docs/vnext/validation.md), and [seven authored benchmark sources](examples/vnext/README.md). In those historical records, six known-mathematics samples were compiled and author-reviewed; the Paper boundary sample is deliberately non-releasable. Independent mathematical review, real-reader feedback, and genuine original-Paper originality and complete-proof quality remain NOT VERIFIED. A formal software release does not change those limitations.

## r3 daily-use responsibilities and evidence

The daily-use main fixes the full request/latest corrections, reader operations and
project revision, owns integration and checks returned artifacts. Use actual available
tools for bounded source/knowledge/review/PDF tasks in isolated candidates; record task
IDs, inputs, states and acceptance. Reject stale revisions, reconcile conflicts against
sources, freeze old writers before takeover, and retain late results as candidates.
Without delegation capability perform the same responsibilities serially and say so.
Save files/patches, task answers, hashes and remaining work so stopping/recovery does not
depend on chat access. This is distinct from a development-stage main and is not a
resident scheduler. Knowledge-only creates zero manuscripts and performs no article prepare.

The KB has three reading scales (overview, problem routes, nodes) sharing one canonical
authority. Its fast route exposes inputs, decisive operations and conditions with exact
slow-subsection links; slow passages discharge promised derivations, exact imports and
present applications with backlinks. Reusable explanations discovered in an article
return to live KB, review and a new snapshot before reuse. Classify actual input uses
as Assumed/Refreshable/Bridge-required. Reconstruct necessary obligations before checking
the author's list; save actual fast-route, slow-step and condition-change attempts and repairs.
Preserve every explicit branch; the seven-branch regression is not a required user syllabus.

All four modes actively target about 2–3 normal actual typeset lines for ordinary
explanatory prose. Longer blocks require improvement or a specific located reason,
alternatives considered and final PDF/hash reinspection; no source-line counting,
decorative formulas, forced breaks, smaller type or omitted assumptions. Inspect every
actual page. Five views change real reader tasks without changing mode duties or facts.
Retain F1 body locations, F2 view/design, F3 comparison plus primary prior support and F4
draft/design safety. Paper remains prominently DRAFT_UNVERIFIED by default.

Software remains 2.1.0, KB/snapshot schema 2.0.0 and output/review schema 2.2.0; r3 is
`four-modes-2026-10-12-r3`, distinct from rc2. Historical bytes and accepted records remain
unchanged; recorded assessment is not current package authorization. Formal tag/Release
publication remains paused. These rules are not completed acceptance: actual content,
PDF, isolated installation and critical review require fixed-candidate evidence. Report
software, mathematics, exposition attempts, PDF inspection and real-reader feedback
separately. AI/team review is not external peer or student evidence; genuine original
Paper originality/full research-proof quality remains NOT VERIFIED without actual input/review.
