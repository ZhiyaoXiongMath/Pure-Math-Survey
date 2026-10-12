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
