# rc2 continuation evidence — 2026-10-12

This is an append-only continuation of the existing hardening branch. It does
not replace the rc1 report or claim completed rc2 acceptance.

## Packaging recovery

- Rechecked remote HEAD: `ed8a1a006a008d0bc263839942838028df836e50`.
- Recovered Actions run `38211383547`, job `114686108581`, artifact `11728798842`.
  Artifact SHA-256: `4d2d6ce3009f8c577f62aaec8b94694b03fc70004583ddaec2394ab86bfc51e9`.
- Verified all 491 archive blobs against the remote recursive Git tree.
- Reproduced all 142 tests locally: 7 failures, 4 errors (28.578 seconds).
  All four errors were the missing `exposition.py` installation allowlist entry.
- Added that existing module to the allowlist and installed-import regression.
  Full regression now executes 142 tests: 7 failures, **zero errors** (27.784 seconds).
  Remaining red tests explicitly cover F2, F3, F4 and the rc2 contract.
- The uploaded rc2 guide, reproduction ZIP and integrated r2 guide have the same
  SHA-256 as the previously resolved copies; no competing specification is used.

Status: packaging recovery IMPLEMENTED and TESTED. The entire candidate remains
BLOCKED by the seven retained hardening failures. Synthetic tests are not
mathematical, originality, independent-reader or visual acceptance.

## Versioned contracts and F4 integration

- Packaging commit dcdfef3 remote Actions run 38223711015: 142 tests,
  seven expected remaining failures and no packaging errors (53.265 seconds).
- New plans/reviews: schema 2.2.0 with four-modes-2026-10-12-rc2;
  explicit rc1 and v2.0 readers preserve historical contracts and bytes.
- Existing exposition.py is now used by prepare, structure and release.
  Explicit drafts may compile only enumerated incomplete-design/placeholder
  cases. Unsafe/canonical/invalid-reference failures remain hard errors.
- A recorded-policy assessment cannot grant current package permission.
- One ephemeral TeX scan is shared across all semantic location checks.
- Targeted design/compatibility regressions: 14 tests, OK (5.209 seconds).
  Full regression: 156 tests, four retained F2/F3 failures, zero errors
  (32.241 seconds). Resource smoke checks passed; no original Paper or
  mathematical-page acceptance is inferred.

Status: contract/F4 changes IMPLEMENTED and TESTED; candidate still BLOCKED
by the four retained F2/F3 assertions. Full completion is not claimed.

## F3 comparison and prior-support closure

- F4 commit e599975 remote Actions run 38224602338: 156 tests,
  four retained failures, zero errors (60.323 seconds).
- Every current original-contribution comparison is explicitly paired with a
  closest prior. Its established relation must name both endpoints with
  compares_with. Endpoint content participates in review binding without
  making comparison navigation a proof dependency.
- Each closest prior requires established primary support, matching version
  and normalized locator, and an accepted source-reading record bound to the
  actual source record and reading note. Online original-text access can omit
  unavailable raw bytes only with an explicit reason; a URL alone is not reading.
- Negative searches may record no hits. They do not supply known-prior support
  or waive the unverified status of an unsupported novelty claim.
- Targeted F3 regressions: 14 tests, OK (3.627 seconds). Full regression:
  170 tests, one retained F2 view assertion, zero errors (35.853 seconds).

Status: F3 IMPLEMENTED and TESTED with synthetic regression fixtures. Real
mathematical comparison and source-reading acceptance remain NOT VERIFIED.

## F2 view-aware writing and remaining F1 regressions

- F3 commit dcbb2ed remote Actions run 38225720369: 170 tests, only the
  retained VIEW02 failure, zero errors (69.293 seconds).
- Five views now affect editable reader goals, actual node-specific uses,
  candidate emphasis order, outline tasks and section-local writing prompts.
  The necessary node closure and all mode proof obligations stay intact.
  Missing view candidates produce an explicit design gap, not an invented node.
- Current output reviews bind the exact view and a located view_focus finding
  naming available nodes. Updating hashes alone cannot substitute a new reading.
- Added 20-combination interface checks, canonical/core preservation, stale-view
  and missing-node probes. Installed resource smoke executes all 20 combinations.
- Extended F1 coverage through LOC01–LOC12, including nested and repeated inputs,
  CRLF/escaped percent, canonical-location substitution and accepted but invalid
  body locations at the actual release/package gate. Synthetic positive proof
  findings now locate an explicit computation, not a theorem import line.
- Focused view tests: 7 OK (3.299 seconds); additional location tests: 7 OK
  (0.534 seconds). Full regression: 184 tests, OK (39.744 seconds).
- Installed-resource scaffold smoke: 20 profile/view combinations, 31 runtime
  documentation links, PASS. Skill frontmatter validation and diff whitespace:
  PASS. Historical manual audit retained; obsolete deleted-branch trigger removed.

Status: F1–F4 software IMPLEMENTED and locally TESTED. This result is not remote
CI acceptance, a real mathematical reading, PDF observation or candidate delivery.
Real three-paper authoring and final installed-environment acceptance are ongoing.

## Recovered remote and isolated test loop

- Commit 307dd831: remote run 38226754768, job 114736041828, **184 tests OK**
  (77.515 seconds), successful Actions conclusion.
- Built the install ZIP from that runtime: 71 members, 70 verified member hashes;
  SHA-256 `75a49d5b5a657bd819d7576f0a84fa3bedbd0e783d8baa8358a4b2bc23c21a7e`.
- Extended verify_release.py to copy the full regression harness around only
  the extracted skill, execute all 184 tests with isolated Python in a fresh
  no-pip/no-system-site-packages venv, and check all 20 installed view resources.
  This actual installed run passed, imported 17 installed modules, kept
  knowledge-only outputs at zero, and rebuilt/rendered all seven historical
  rc1 benchmark PDFs. Those new renders were explicitly NOT VISUALLY REVIEWED.
- Historical verifier now selects the fixed rc1 suite, leaving new rc2 outputs
  to their separate acceptance path. Initial installation attempt encountered
  an unfinished rc2 Lecture while globbing historical outputs; the scope fix
  above preserves the original seven scenarios and the rerun passed.
- Source regression after verifier changes: 184 tests OK (45.580 seconds).

Status: reliable source/installed/remote test loop TESTED. Candidate mathematics
and final PR CI remain separate unfinished acceptance responsibilities.

## Source-retention finding from actual authoring

- Three real primary PDFs were downloaded, hashed and read, but are not
  redistributed in the project. Readiness previously described every absent
  in-project source file as an unavailable hash. It now distinguishes a
  recorded hash with unretained bytes (`SOURCE_RAW_BYTES_NOT_RETAINED`) from
  genuinely absent raw hash/bytes. Neither condition certifies retained bytes.
- Online source scopes now reject malformed or empty locator lists with
  SOURCE_REVIEW_MISSING instead of accepting a truthy scalar or crashing on a
  null nested scope. Source/version/actual-reading duties remain unchanged.
- Visual diagnostics no longer imply the observer must have been human; each
  record must truthfully identify actual observations and reviewer method.
- Focused tests: two tests OK (0.811 seconds). Complete fresh source regression:
  186 tests OK (42.055 seconds); all 20 resource preparations also passed.
  This 186-test run is new execution, not the earlier conversation's assertion.

Status: these narrow authoring findings IMPLEMENTED and TESTED. faf7934 remote
run 38227400876 was still installing TeX at the latest observation; no completed
CI result is inferred for that run here.

## Remote loop confirmed after source-retention fix

- The previously pending run 38227400876 (faf7934) completed successfully.
- Run 38228676928 at 3df41200, job 114742439518, also completed successfully.
  Its actual job log was retrieved, not inferred from local counts.
- Fresh extracted-package verification at 3df41200 passed 186 tests in isolated
  Python, checked 70 member hashes, imported all 17 installed runtime modules,
  prepared 20 profile/view combinations, and rebuilt/rendered the original seven
  benchmarks. Installation ZIP SHA-256:
  `11fa729ca89153f91f6e89b6cbca955e8fcc2f56ed16170e22647c1027fb38b5`.
- These are software results. New rebuilds do not inherit visual acceptance;
  mathematical and rendered-page readings are recorded on their own exact inputs.

## Real authoring integrated with installation verification

- Completed real three-paper time-compactness Thematic and same-spine methods /
  boundaries outputs, eight pages each; new Schur Lecture, four pages.
- Scoped original-source/author semantic readings and actual root observations
  of all 28 final pages are retained. All four current release/package gates
  pass, with independent-review limits accurately reported.
- Added a real-source contract regression and current-output verifier that
  preserves authored files, rechecks evidence, and compares the canonical spine.
  Fresh source full regression: 187 tests OK (44.074 seconds).
- Fresh isolated installation: 187 tests OK (44.878 seconds), all 20 resources,
  seven historical and four current actual PDF builds/renders. Newly rebuilt
  PDFs correctly remain NOT VISUALLY REVIEWED.
- All 399 original example blobs match the original ed8a1a0 remote tree.
- No accepted historical snapshot/output/review was rewritten. Pagination fixes
  in the two new Minimal outputs received new semantic records; old accepted
  author records were retained and affected final pages reopened.

Status: local source/installed tests and actual mathematical/page author readings
are complete for this group. Final pushed-head PR CI is a separate pending gate.
