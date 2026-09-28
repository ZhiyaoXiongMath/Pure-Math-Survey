# TeX build and full-page inspection

Reuse assets/templates/math-review.sty with 12pt amsart and its readable margins. Profile templates are thin placeholders, not mathematical answers. `output build` stages authored/generated inputs separately, runs pdfLaTeX without shell escape, BibTeX as needed, repeats until aux/toc/out/bbl stabilize, retains actual logs/dependencies/tool versions, and reads PDF page count with pdfinfo. Failed builds preserve their actual evidence.

Runtime core is standard-library Python 3.10+. PDF build requires TeX Live (or equivalent) with amsart, the packages loaded by math-review.sty, pdfLaTeX and BibTeX; render/release requires Poppler pdfinfo/pdftoppm. No pip dependency. `bibtex.original` or `bibtex8` is tried only as a recorded available fallback. `python scripts/survey.py --help` and subcommand help give actual flags.

Run render after a current build. Open every page at readable size. Inspect clipping, overlapping text, broken glyphs, formula line breaks, headings, page boundaries and references. Record page-specific observations only after inspection. A rasterization script cannot say pages were visually reviewed. Every rebuild changes the PDF identity; refresh page evidence before adopting it as the reviewed artifact.

Current-style and frozen-sample builds are separate tasks in build_checks.py. A style-sentinel mutation regression tests that each task really uses its intended style. The new-profile demonstrations have their own actual PDFs and evidence. Historical PDF typography does not define a v2 page quota.
