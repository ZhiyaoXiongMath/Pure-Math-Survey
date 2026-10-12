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
