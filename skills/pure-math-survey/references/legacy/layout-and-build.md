# Historical v1 reference

This is retained legacy documentation. Native v2 follows ../records-and-delivery.md and the current SKILL.md.

# Layout and build

## Shared presentation profile

Use `assets/templates/math-review.sty` beside the selected entrypoints. This profile applies to all five parts and both editions; [The Part V guide](part-v-benchmark.md) explains the optional, purpose-specific examples.

| Setting | Profile |
|---|---|
| Class | `\documentclass[12pt,reqno]{amsart}` |
| Page | A4; centered text width `6.1in`; top and bottom `1.2in` |
| Header/footer geometry | `headheight=14pt`, `headsep=0.2in`, `footskip=0.5in` |
| Text and math fonts | Prefer STIX2 through TeX; warn and use Latin Modern when available if STIX2 is absent |
| Line spacing | `\linespread{1.1}`; no edition-specific compression |
| Paragraph tolerance | `\emergencystretch=1.2em`; not global `\sloppy` |
| Page breaks | `\widowpenalty=10000`, `\clubpenalty=10000`; `\pagestyle{plain}` |
| Lists | `leftmargin=*`, `topsep=0.35\baselineskip`, `itemsep=0.15\baselineskip`, `parsep=0pt`; roman enumerated conditions |
| Numbering | Section-based shared theorem counter and section-based equation numbers; unnumbered recalls display the original theorem number |
| Links | Blue internal/citation/URL links; linked TOC page numbers; numbered bookmarks of depth 2 |
| Contents | `tocdepth=1`; a concise section-level contents when appropriate; not a substitute for introduction statements |
| Page-space tool | `needspace` available for locally justified breaks |

Use the ordinary `amsart` title/abstract treatment. Put `abstract` before `\maketitle`. Do not add a decorative cover, running branding, colored theorem boxes or an audit dashboard to the research article. Give accurate metadata and real citations. Differences in the subject can justify mathematical hierarchy changes, not global readability reductions.

STIX2 absence is a recorded portability fallback, not an exact-match typography pass. Install dependencies through the local TeX environment where appropriate; never bundle or share font files. The release contains no font files. Engine/toolchain differences may change pagination and need a fresh visual review.

## Local repair, not global compression

Break a long equation using `align`, `aligned`, `gathered` or `cases`; preserve logical order and its number. A long theorem can continue naturally when needed. Do not force every theorem into a `samepage` block. Use `\Needspace` only after looking at the affected page, with a reasonable height for the actual statement; a request larger than the page creates rather than fixes trouble.

Keep a heading with its first meaningful content, a theorem label with its first hypothesis, and a proof ending with its closing argument where practical. Inspect paragraph, formula, list and bibliography breaks. No fixed whitespace ratio or density score can decide these questions. Do not use negative spacing, tiny formulas, a shrunken text font, squeezed margins or arbitrary page-count targets to hide a defect.

## Rebuild a real article

Copy the shared style and all actual dependencies into the project. For a pdfLaTeX project, a typical command is:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

Record the actual command and engine, including bibliography steps. Without `latexmk`, run `pdflatex` until auxiliary references and the contents stabilize; two runs may be insufficient. Use no shell escape for untrusted source, and inspect inputs before executing external commands. Compile all requested manuscripts, not unrequested companions.

The log must not retain undefined references/citations, duplicate labels or destinations, missing glyphs, missing inputs, fatal TeX errors or unresolved substantive overflows. The build report preserves exact non-blocking log lines in `nonblocking_log_warnings`. Review underfull-box and font-substitution warnings in context; warnings and failures are not interchangeable. A successful command does not establish a readable PDF.

## Render and inspect

Render every page with a real PDF renderer. Inspect full pages and enlarge dense formulas, theorem/list breaks, the first page, contents and bibliography. Contact sheets help identify pagination and gross defects but do not replace readable inspection of mathematical pages. Re-render after repairs and recheck affected pages and reference stability.

Where installed, the offline comparator is:

```sh
python scripts/compare_pdf.py reference.pdf candidate.pdf --output comparison
```

It uses PyMuPDF and Pillow, renders all pages, checks page boxes and reports exact pixel differences at the chosen resolution. It does not OCR or inspect mathematical truth. It can also emit contact sheets for page inspection. The JSON is build evidence, not another research audit registry.

## Reproduce this skill's maintenance checks

```sh
python scripts/validate_assets.py
python scripts/build_checks.py --output /absolute/path/to/checks
python scripts/compare_pdf.py \
  assets/reference-samples/dhym-v6/dhym-survey-polished-v6.pdf \
  /absolute/path/to/checks/v6-shared-style/v6-shared-style.pdf \
  --output /absolute/path/to/checks/reference-comparison
```

The build runner uses pdfLaTeX with no shell escape, checks stabilization and logs, and leaves sources unchanged. It compiles ten instructional scaffolds, the elementary example, the v6 example with original and shared preambles, and the compact example with current and frozen styles. The scaffolds deliberately retain insertion text and are not publication deliverables. The sample's mathematical content and date are preserved.

Real builds require a TeX distribution with AMS packages, `mathtools`, `geometry`, `enumitem`, `needspace` and `hyperref`; STIX2/Latin Modern and microtype are optional. The PDF comparator additionally requires PyMuPDF and Pillow and must report a missing dependency rather than pretend it rendered pages.

A style regression, source-structural test, full-page visual inspection, source-based mathematical review, independent review and new-topic generation evaluation are different activities. Report exactly which were executed. Do not call scaffold builds new research surveys or claim automatic writing-quality certification.
For bibliography identifiers that otherwise form unbreakable text, use a breakable URL display (for example, `\href{URL}{\nolinkurl{identifier}}`). Repair the local link layout rather than hiding warnings or shrinking the document. The bibliography generator applies this to arXiv and DOI displays.
