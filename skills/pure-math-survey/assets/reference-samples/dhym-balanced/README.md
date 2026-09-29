# Balanced dHYM writing reference

The user supplied this manuscript after multiple rounds of deliberate polishing.
It is the principal writing and layout reference introduced in Survey 2.0.3.

Read [dhym-survey-revised.pdf](dhym-survey-revised.pdf), a six-page account of
dHYM solvability and stability, or its [TeX source](dhym-survey-revised.tex).
The TeX, PDF, original style, BibTeX database and supplied bibliography output
are preserved byte for byte. [provenance.json](provenance.json) records their
identities. The separate
[article download](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.3/dHYM_survey_balanced_source.zip)
contains exactly a standalone TeX and the unchanged PDF. The standalone export
includes the style and bibliography in its TeX without changing the mathematical
text. Project manifests, editorial records and compilation logs are excluded.

## What to learn from it

- Section 1 establishes the equation and phase conventions, then states the
  three principal solvability answers.
- Section 2 develops the surface reduction and essential intermediate arguments,
  and identifies the deeper existence construction imported from the literature.
- Section 3 supplies the categorical definitions at their point of use, then
  connects a scaling result, an explicit correction calculation and an
  equality-wall example to the remaining categorical question.

Use these passages to study selection, local definitions, proof dependencies
and mathematical boundaries. The six-page length, three sections, result
counts and topic selection are not requirements for other surveys. Choose
scope and exposition for the actual question and reader; unnecessary immediate
full-statement repetition is not a writing goal.

## Rebuild without changing the reference

Copy the `.tex`, `.bbl`, `references.bib` and neighboring `math-review.sty`
to a separate directory, then run pdfLaTeX until the references stabilize:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error dhym-survey-revised.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error dhym-survey-revised.tex
```

The supplied `.bbl` is used directly. If editing the bibliography in a separate
working copy, regenerate it with BibTeX and rerun pdfLaTeX. No fonts or source
papers are redistributed. A different font/toolchain requires a fresh page review.

`scripts/build_checks.py` stages the article with either its supplied style
(`balanced-frozen`) or the current shared style (`balanced-current`), including
both bibliography files. These are reproduction/style checks on copies.

## Scope and provenance

The article's mathematical scope, literature date, preprint qualifications and
review limitations remain attached to it. Inclusion does not claim a new
independent mathematical review or complete current-frontier verification.
The separate Schur-complement release example demonstrates the
knowledge/snapshot/output workflow.
