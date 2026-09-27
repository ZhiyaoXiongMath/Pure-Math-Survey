# Pure Math Survey 1.8.1

Develop source-grounded English mathematical surveys with five selectable Parts and concise/standard editions. The default single-topic document is Part V concise.

## Changes

Reading-length guidance is non-blocking: a default overrun produces `REVIEW_NEEDED`, not a failed command. An explicit user `max_pages` remains a strict limit. Project validation applies the same distinction and checks that current PDFs are readable. Missing resources, corrupt PDFs and malformed input produce actionable errors rather than an empty success or traceback.

Body review covers author-written numbered and starred sections. A separately placed proof is supported through explicit forward and backward locators; printed proof-sketch labels must agree with the review. Important hypotheses, criteria, conclusion formulas, principal-answer coverage, natural variations, frontier discovery and the common concise/standard core remain intact. All ten templates use the same reading-length semantics.

Text files use explicit UTF-8; bibliography identifiers permit natural line breaks. Build reports retain located non-blocking warnings separately from failures. Archive creation uses private temporary files and preserves unrelated files.

The optional examples are the dHYM v6 article, the compact surface article, and the elementary quadratic/gradient examples. Their mathematical files and dated scope are retained; they are not current source authorities or automatic quality certificates.

## Install and use

Extract the ZIP. Place its `pure-math-survey` directory in the skills directory supported by your agent, then select `pure-math-survey` in that agent. The package does not install itself. Read [SKILL.md](SKILL.md) for the workflow. When replacing an existing installation, replace the directory rather than overlaying files, so removed resources cannot survive the update. Keep personal projects outside that directory.

From the extracted directory:

```sh
python scripts/validate_assets.py
python scripts/create_project.py --output /absolute/new/project --topic my-topic --documents 5:concise
python scripts/check_problem_formulation.py /absolute/new/project --stage plan
python scripts/check_survey_selection.py /absolute/new/project --stage plan
python scripts/check_mathematical_structure.py /absolute/new/project --tex my-topic-part5-integrated-concise.tex --inventory
python scripts/check_reading_budget.py /absolute/new/project
python scripts/validate_project.py /absolute/new/project
```

A new scaffold is deliberately pending. Research, replacement of insertion text, substantive reading, compilation and page inspection are necessary before delivery; project validation must not approve the untouched scaffold. Select any nonempty combination such as `1:concise,3:standard`; `suite` selects I--V concise, and `all` explicitly selects all ten.

Python 3.10+ is required. Builds need pdfLaTeX and the packages in `assets/templates/math-review.sty`. STIX2 is preferred, with a reported installed-font fallback. Reading-length diagnostics and current-project PDF validation use PyMuPDF; pixel comparison also uses PyMuPDF and Pillow. Font files and restricted source papers are not supplied.

Use [layout and build](references/layout-and-build.md) for article builds, [templates and examples](references/template-maintenance.md) for supplied-material builds, and [validation](references/validation.md) for reading evidence and limitations. `scripts/package_release.py` creates and reopens a checked skill archive without installing it or changing the source tree.
