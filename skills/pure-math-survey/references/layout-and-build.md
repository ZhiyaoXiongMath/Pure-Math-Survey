# Native TeX, source reading and full-page inspection

Use this installed reference with permitted local tools; it does not require reading a global PDF skill. First apply the task's actual read/write boundary and source/output allowlist. A same-named global-skill ban and an all-global-skill ban are different; neither changes the need for actual source reading, mathematical review or opening every article page. If a required viewer/tool is unavailable within the boundary, record the precise blocker rather than substituting text extraction or a successful build for visual inspection.

## Required tools and fixed inputs

The core uses Python 3.10+ standard library. TeX builds need pdfLaTeX, BibTeX and packages loaded by the installed assets/templates/math-review.sty (12pt amsart and readable margins). Poppler pdfinfo/pdftoppm provide page counts/images; pdftotext is useful for original-source text, but image inspection is still needed for controlling formulas. `bibtex.original`/`bibtex8` are tried only as recorded available executable alternatives. Use installed scripts and current CLI help, not a different global installation. Current r4 templates are unfinished scaffolds; they do not supply mathematical answers or historical-policy support.

Before build, fix the actual plan/snapshot, authored TeX/style, generated fragments and materials, and verify applicable readiness and substantive findings. `output build` stages those inputs, uses pdfLaTeX without shell escape, runs BibTeX when needed and repeats until auxiliaries stabilize. Actual command results, tool versions, dependencies, log diagnostics, source inputs, PDF hash and page count remain in build/build-report.json. Failed attempts remain evidence; a previous PDF does not make the failed latest attempt pass. Disabled shell escape is not an operating-system sandbox: compile only permitted trusted inputs.

## Build, render and open every article page

Replace PROJECT/ID with the actual allowed project/output, using the installed script path:

```sh
python scripts/survey.py output validate PROJECT --output ID --stage structure --json
python scripts/survey.py output build PROJECT --output ID --json
python scripts/survey.py output render PROJECT --output ID --dpi 150 --json
python scripts/survey.py output review-template PROJECT --output ID --kind visual --to evidence/NEW-visual.json --json
```

The actual PDF is outputs/ID/build/main.pdf. Read outputs/ID/build/build-report.json and evidence/render-manifest.json. The render manifest reports the fixed PDF hash and an ordered `pages` list with page number, output-relative PNG path and SHA-256; resolve each listed path under outputs/ID, never guess a filename. Native render checks that every PDF page has an image and returns RENDERED_NOT_REVIEWED.

Open **each** listed PNG at readable size with the host's permitted local image-view tool, such as `view_image` using the resolved absolute path. The calling tool must actually return the image for inspection; listing filenames, embedding links for the user, rasterizing or extracting text does not establish your observation. Inspect all page bodies, formulas, theorem conditions, glyphs, references, headings, page breaks, clipping/overlap and normal prose rhythm. Zoom/reopen unclear regions as needed. If no permitted visual tool can expose pixels, retain the images and report visual review blocked; do not invent page findings.

Only after actual inspection fill the fresh pending visual record. Preserve its required input bindings and ordered all-page scope; supply concrete page/block/equation observations, corresponding TeX locations, defects/repairs or justified long-block exceptions. Ordinary explanatory prose actively targets about 2–3 normal typeset lines; complete statements/necessary continuous proofs can be longer with specific reasons. Never force breaks, shrink typography, decorate with equations or omit conditions to meet the target.

After any repair rebuild and rerender. New PDF/page identities need current evidence; old observations may be reused only for verified identical page images, with honest scope, and do not automatically grant current semantic acceptance. Preserve prior attempts/reviews rather than editing their hashes. A page count or successful command does not prove readability or mathematics.

## Read actual original sources within their allowed scope

For an allowed local original PDF, retain its identity and controlling version, then use Poppler directly if needed:

```sh
pdfinfo ORIGINAL.pdf
pdftotext -layout ORIGINAL.pdf OWNED-source-text.txt
pdftoppm -f FIRST_PAGE -l LAST_PAGE -png -r 150 ORIGINAL.pdf OWNED-source-page
```

Replace all placeholders; text/images go only to the worker's allowed evidence/cache path. Read the relevant original sections and open rendered pages containing controlling statements, equations, definitions and proof interfaces. Distinguish PDF index pages from printed locators and record the exact sections/theorems/pages read. Text extraction alone can lose symbols or quantifiers. Do not hash notes as original bytes, claim inaccessible pages were read, or redistribute private originals. Online-only originals need actual reading with exact locators/version and explicit retention limitations; abstracts remain discovery clues. Use [source evidence](research-and-evidence.md) for current records.

## Actual package rebuild and evidence

Current r4 formal packaging requires the actual release checks. Explicit Paper draft preview stays prominently DRAFT_UNVERIFIED; its formal package refusal is recorded rather than bypassed.

For a permitted current article package, extract to a new allowed directory and inspect its member/checksum inventory. From that extracted package run:

```sh
python -I rebuild.py --output NEW_OUTSIDE_PACKAGE_DIRECTORY
```

The destination must be new and outside the package. Inspect rebuild-report.json, commands, log diagnostics, auxiliary convergence, tool versions, source_package_verified, page count and rebuilt PDF identity. A successful rebuilt PDF is reproducibility evidence, not a new visual review. To inspect its pages use permitted pdfinfo/pdftoppm and the local image viewer as above, then save fresh actual observations in owned evidence. Keep the original reviewed package/PDF unchanged. Report original and rebuilt file identities, actual build/page scope, failures and unverified portability separately. Do not promise old-policy package support or arbitrary-environment rebuilding.
