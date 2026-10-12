# rc2 Schur Lecture: authoring and review handoff

Created on 2026-10-12 as a new output at `examples/vnext/projects/schur/outputs/rc2-lecture`. The plan uses schema `2.2.0`, policy `four-modes-2026-10-12-rc2`, profile `lecture`, view `methods`, and the unchanged snapshot `KB-714ebb540c07ca2585ac455f40d642f6920d708a8a3ce1f91f4e4000d41f12cd`.

## Reader task and manuscript

The lecture teaches the classical positive-definiteness criterion by choosing the shift through mixed-term matching, expanding every block product, checking both inverse compositions, and proving sufficiency and necessity separately. The reader can multiply real matrices, transpose products, and expand a scalar square. Positive definiteness and the square-map zero-kernel criterion are refreshed. The Schur-complement formula and block change of variables are built in the text.

The full principal appears early through the unchanged canonical `N-main` input. The square identity and inverse-map canonical inputs are also included, with their derivations developed. The scalar case A=2, B=1, C=1 is computed, including its fixed-y minimum. The example A=-1, B=0, C=1 identifies the failed sign step. Singular-block cases are identified as noncoverage, with no pseudoinverse claim. The separate congruence comparison is omitted with a plan/outline rationale.

Main proof locations in `manuscript/main.tex`:

| Responsibility | Lines |
| --- | --- |
| Principal canonical input | 15–17 |
| Reader inputs | 36–43 |
| Scalar-to-block shift construction | 45–73 |
| Full square expansion | 76–89 |
| Both inverse compositions | 109–120 |
| Sufficiency | 125–135 |
| Necessity for every nonzero y | 137–144 |
| Computed model and failure boundary | 149–172 |

## Actual readings and immutable inputs

The supplied guide r2 Appendix A, sections A.1–A.5, was reread from the local task input. Its SHA256 `2e8c5ab518cc40f62a2085ec573ac3c53c81ad9cf53e0fefe9e38f2d35420188` matches the fixed `S-guide` record. The existing project nodes, old authored Lecture, plan, overview, source identity and reading note were read to reconstruct the argument. Old accepted labels were not used as a substitute for the current manuscript reading.

Runtime readiness legitimately reuses the existing scoped mathematical and coverage records for this unchanged snapshot and exact three proof promises. The new output-local `evidence/current-mathematical-reread.json` supplements those records with actual current calculations, binding fixed authoring-material copies. `evidence/author-semantic.json` is a fresh current-policy `author_reread`, with all seven whole-manuscript checks, isolated principal findings, located mode/view findings, and a located finding for each exact promised proof step. No independent review, real-reader experiment, external prior-art search or originality claim is made.

A before/after SHA256 comparison covered all 197 pre-existing Schur project files. All remained byte-identical; no new project file occurred outside `outputs/rc2-lecture`. No KB, snapshot, historical output, runtime, test, tool or GitHub file was changed by this authoring task.

## Commands, diagnostics and build

Commands were run through `python skills/pure-math-survey/scripts/survey.py` from the repository root:

- `output plan ... --output rc2-lecture --snapshot KB-714ebb...12cd --profile lecture --view methods`: `PLANNED`.
- `kb readiness ... --plan .../outputs/rc2-lecture/plan.json`: `READY`.
- `output prepare ...`: `PREPARED`; reported the expected incomplete generated outline tasks in `artifacts.exposition_design`. Those tasks were replaced with the concrete authored outline.
- First `output validate ... --stage structure`: `EXPOSITION_DESIGN_INVALID_REFERENCE`, outline line 24, because an omitted `N-comparison` node was written as a wiki reference outside the available selection. The first build consequently returned `BUILD_FAILED` with that structural error before invoking the compiler. The omission was retained as ordinary prose; the selected mathematics was unchanged.
- Subsequent structure check: `STRUCTURALLY_VALID`, with no errors or warnings.
- `output build ... --output rc2-lecture`: `BUILT`, four pages, stable references, no blocking log issues. Tools were pdfTeX 3.141592653-2.6-1.40.25 (TeX Live 2023/Debian) and BibTeX 0.99d. The shared style reported its documented nonblocking STIX2-unavailable fallback-font warning.
- `output render ... --output rc2-lecture`: `RENDERED_NOT_REVIEWED`, all four pages at 120 dpi.
- Current `output validate ... --stage release` at this authoring handoff: `NEEDS_WORK`, with exactly `VISUAL_REVIEW_INCOMPLETE`; the current semantic review was selected and readiness was `READY`. The warning `NO_INDEPENDENT_REVIEW` remains accurate.

The PDF skill was read. Its required create marker succeeded immediately before manuscript authoring and before the first compile. Build and render histories were retained. A mistaken output-review-template destination created a redundant pending template nested within this new output; that redundant newly created path was removed and the correct output-relative evidence path used. No historical file was affected.

## Visual review handoff

The PDF is `outputs/rc2-lecture/build/main.pdf`, SHA256 `7052ed062048a1c1800c163b8ab134bac445a7757c607028396fa6c93eb8472f`, four pages. The actual page images are `evidence/pages/page-1.png` through `page-4.png`. The pending `evidence/visual-review.json` is a template only; it confers no acceptance. The parent reviewer owns opening all four images, any necessary layout revision, page-specific findings and final release/package authorization. This handoff does not claim that rendering is visual inspection.

A scaled-preview concern about the page 2 footer was checked against the full-resolution image and PDF bounding boxes. The final body line and footer have a clear gap (approximately 26 pt); no collision was found. No layout edit or rebuild was made in response. The original PDF and rendered page identities remain unchanged.

## Root completion after author handoff

The root actually opened all four rendered pages and recorded page-specific
observations in `evidence/root-page-review.json`. The exact PDF and images
remain unchanged. Current-policy assessment is now RELEASABLE, with no errors
and the accurate NO_INDEPENDENT_REVIEW warning; see
`schur-lecture-release.json`. A reviewed output ZIP was created by the real
package gate. The redundant nested pending template mentioned above was found
still present at root inspection and removed after confirming it was
`not_performed`/`revise`, with no actual findings or accepted evidence.
