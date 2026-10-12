# 2.1.0-rc2 candidate validation

This continues `vnext/2.1.0-rc2-hardening` from the verified remote
`ed8a1a006a008d0bc263839942838028df836e50`. It preserves the committed F1 scanner
and F4 design module. No historical example blob was changed: all 399 original
example files match the fetched baseline Git blob identities
(`historical-integrity.json`). No PR merge or Release has been performed.

## Current evidence and its scope

F1–F4 are IMPLEMENTED and TESTED. New source regression: **189 tests OK**
(47.732 s). The extracted installation passed the same **189 tests** (47.367 s)
in a fresh no-pip, no-system-site-packages venv with isolated Python. All 17
runtime modules came from the installation, all 70 member hashes verified,
all 20 profile/view resources executed, and knowledge-only initialization
created zero outputs. Seven historical and four current PDFs were actually
rebuilt and rendered in that isolated environment. Those new renders are
explicitly NOT VISUALLY REVIEWED.

The original four current PDFs were actually read: 24 time-compactness pages
and four Schur pages. Their current-policy package gates return RELEASABLE
with no errors. The reviewer mode is author_reread and identifies model-based
inspection honestly. Source-reading and page evidence are separate from
software test fixtures. See `real-acceptance/time-compactness-report.md`,
`real-acceptance/time-compactness-release.json`, `schur-lecture.md` and
`schur-lecture-release.json`.

The final runtime commit `02d66046547a7581e3aff113720e89dffbc2d85d` passed
[PR run 38231441213](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38231441213)
on **Python 3.10 and 3.12**, each executing 189 source tests and 189 installed
tests plus eleven actual PDF builds. The actual logs were fetched; both CI
installation hashes match the delivered ZIP. The branch audit
[38231436703](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38231436703)
also succeeded. [PR #2](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/2)
is open and unmerged. Exact job IDs and timings are in `CI.json`.

## Failure reproduction and repaired responsibilities

The original run [38211383547](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38211383547)
at ed8a1a0 was reproduced: 142 tests, seven failures and four errors.
The first repair restored `scripts/survey_core/exposition.py` to the actual
installation allowlist. The same suite then had seven failures and zero errors.
Subsequent checked remote runs reduced those failures to four (F4/schema),
one (F3), and zero (F2/F1 completion). Actual commit/run/count records are in
`CONTINUATION.md`; `BASELINE.md` is preserved as a historical checkpoint.

| Item | Actual implementation | Regression evidence |
| --- | --- | --- |
| F1 | `tex.py`: reachable literal body, comments/definitions/conditionals, canonical imports; shared per-assessment inspection in release/profile review | LOC01–LOC14, invalid accepted locations blocked by actual release/package |
| F2 | `plans.py`, `profiles.py`, `exports.py`, mode templates: view goals, node uses, emphasis, actual outline tasks and located `view_focus` review | Twenty profile/view combinations, stale/missing view findings, same real canonical spine and distinct final manuscripts |
| F3 | `models.py`, `profiles.py`, `plans.py`, `reviews.py`: typed comparison pairs, both comparison endpoints, every closest prior and primary support/version/locator reading | Wrong pairs, unsupported/secondary sources, wrong versions/locators, missing reading and stale endpoint records rejected; synthetic Paper evidence is labelled synthetic |
| F4 | Retained `exposition.py` integrated into prepare, structure, release and bounded draft preview | Knowledge/output separation, default unfinished designs, preserved author files, invalid references and canonical faults remain blocking |
| Installation | `validate_assets.py`, `package_release.py`, `verify_release.py`, `verify_rc2_examples.py` | Resource allowlist/hash verification, fresh installed full regression and eleven actual PDF builds |

## Contract and historical compatibility

| Object | Version/policy | Permitted behavior |
| --- | --- | --- |
| Software/install package | 2.1.0-rc2 | Current implementation |
| KB/project/node/source/snapshot | 2.0.0 | Existing identities preserved |
| New plan/policy-bearing review | 2.2.0 / four-modes-2026-10-12-rc2 | All current F1–F4 duties |
| Historical rc1 output/review | 2.1.0 / four-modes-2026-10-11-r2 | Read-only recorded assessment; no current release bypass |
| Historical legacy output/review | 2.0.0 / legacy-2.0.0 | Original contract preserved; no silent migration |
| Visual and source readings | Their existing scoped contracts | Exact hashes and scope still required; a schema label alone is not acceptance |

Current release/package requires a current output ID and current-policy
readings. `RECORDED_VALID` is historical assessment, never new release
authorization. Old snapshots, manuscripts and accepted records were not edited.

## Actual mathematical acceptance

The topic is time compactness for linear embeddings, compact nonlinear maps
and seminormed positive cones. The initial two-paper snapshot and ready plan
were frozen before a third paper added five nodes and a restricted comparison.
A later source-date explanation was corrected through new records and a new
snapshot, preserving the earlier ones. The final methods and boundaries plans
have the same snapshot, question, principals, decisive boundaries, comparison
group and canonical statement bytes.

Thematic develops the three mechanisms and their comparison. Methods leads
with averages, two-point estimates and derivative moduli. Boundaries leads
with an actual endpoint ramp and image-only compactness, then checks precisely
which norms, measurable lifts and injectivity assumptions a transfer needs.
The Schur Lecture expands the shift, all block products, both inverse
compositions, sufficiency/necessity and a computed model and failure example.
These are expository treatments of known mathematics, not original Papers.

The original controlling Simon, Maitre and Barrett–Süli texts were accessed
and read. The PDFs are not redistributed; URLs, exact versions, recorded raw
hashes, source locators, own-word reading notes and explicit retention limits
are included. The unresolved justification in Barrett–Süli v2 after (2.8),
p.6, is disclosed without claiming its theorem false. The cone proof supplied
here uses the separately checked local reconstruction instead.

| Original reviewed PDF | Pages | SHA-256 |
| --- | ---: | --- |
| Thematic | 8 | `05efcf182083bcf5cbddb1fecb118f9f78a181c5801754861189a093d0efc9fa` |
| Minimal methods | 8 | `6f868234ffd5774e3634a260fe981e6f326fdba0f63bcdc441347d21eb20dc11` |
| Minimal boundaries | 8 | `475a10ee691915f84abd55faa1fbe4268491a9ba86ea7a45157e31501168a6ca` |
| Schur Lecture | 4 | `7052ed062048a1c1800c163b8ab134bac445a7757c607028396fa6c93eb8472f` |

## D1–D10 at this checkpoint

| Duty | Status | Evidence/remaining gate |
| --- | --- | --- |
| D1 | IMPLEMENTED, TESTED | F1 regression and release/package negatives |
| D2 | IMPLEMENTED, TESTED, REVIEWED | View-aware runtime plus actual paired manuscripts |
| D3 | IMPLEMENTED, TESTED | Both typed evidence chains, negative/stale cases; real formal original Paper NOT VERIFIED |
| D4 | IMPLEMENTED, TESTED | Complete prepare/structure/release/draft separation |
| D5 | IMPLEMENTED, TESTED | Explicit versions/policies; 399 original blobs unchanged |
| D6 | REVIEWED | Three real papers, increment, three finished outputs, all pages and Schur proof regression |
| D7 | TESTED, REVIEWED | Current code PR CI passes on Python 3.10/3.12: 189 source + 189 installed tests and eleven PDF builds per job |
| D8 | IMPLEMENTED, TESTED | CLI, templates, references, SKILL, agents, checksums and package agree |
| D9 | IMPLEMENTED, TESTED | Zero known unresolved F1–F4 requirements in the supported literal TeX model |
| D10 | REVIEWED | Explicit distinctions and limitations below |

Independent mathematical audit, actual target-reader feedback and the formal
quality of a genuine original Paper remain **NOT VERIFIED**. Without an authorized, fully proved original contribution and verified prior-art
evidence, formal Paper release remains **BLOCKED**. General TeX
execution is outside the explicit literal-body scanner model. The cause of
interrupted authoring locks/staging is NOT VERIFIED; inspected stale staging
was cleared and inventories retained, with no gate weakened. No CI failure is
being described as development completion. The code and topical candidate meet D1–D10, with those explicit validation
boundaries. The final documentation-only commit is also checked remotely before
delivery; it does not change the runtime or installation ZIP.

## Reproduce software verification

```sh
python -m unittest discover -s tests -v
python skills/pure-math-survey/scripts/validate_assets.py --json
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0-rc2.zip
python tools/verify_release.py ../pure-math-survey-2.1.0-rc2.zip --report ../clean-install.json
python tools/verify_rc2_examples.py --output ../fresh-rc2-builds --report ../rc2-builds.json
```

Git contains editable projects, immutable snapshots, scoped readings and
artifact identities. The separate candidate bundle retains actual original
PDFs, page PNGs, logs and build/render histories. Rebuilding never inherits
those visual observations. The install ZIP is 71 members with 70 verified
member hashes; its SHA-256 is
`4c25dee81dfc3b7bdb624f006e0b5385d1b4a7f325b2a0e76d85c926e753e411`.

## Complete diff review finding

The complete PR inventory was fetched in five pages: 498 changed files, no
deletions. Runtime/tests/contracts and mathematical manuscripts were inspected;
immutable/generated copies and exact stored bindings were mechanically checked.
Local source tree `a3152c4d47142dbc3638a54ede33244e2d17fb10` exactly matched
the pushed tree. See `diff-review.json` for the full inventory and scope.

The review found a called custom-environment control gap in F1. LOC13 first
failed on a setbox environment; the narrow scanner repair now checks invoked
begin/end definitions. Empty wrappers and unused definitions remain valid.
LOC14 confirms actual release/package rejection. Nine focused tests pass
(0.886 s); the complete source and installed counts above include this repair.
The original four reviewed PDFs still pass current release without changes.

The subsequent environment-control repair diff and resource hash changes were
reviewed after that initial inventory. All 499 code-candidate changes are
accounted for; this CI-record update adds only documentation. No old example
blob, accepted mathematical record, snapshot or manuscript was modified.
