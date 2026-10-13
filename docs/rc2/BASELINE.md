> Historical development record: all policy claims, artifact paths, results and command transcripts below apply to that earlier revision. Removed examples/reports/tools remain in Git history or private backups; they are not current instructions, answer inputs or r4 acceptance. Follow [current product workflow](../r4/workflow.md) for new work.

# rc2 baseline, red tests, and explicit contract decision

Status: development in progress, NOT a completed rc2 release.

## Exact baseline and performed work

- Upstream main: `7bf87324071de6ea221ef5f491148debb31ccba0`, tree `a8c2e890b3d59c6410e349480e2efc0c7b23ed0a`.
- Development branch: `vnext/2.1.0-rc2-hardening`.
- Read-only audit workflow commit: `5c0a8440557f4bf67cb4de14401db3a311134f4a`. Its source archive was extracted locally; the local Git index reproduced tree `cc7fd69318ce945a2b07e4072b706ed98ce1a615` exactly.
- Fresh GitHub Actions run `38208529579`, job `114677297148`: 128 unchanged tests, 35.601s, OK.
- Downloaded source/evidence artifact `11728875496`, SHA-256 `105a1084ced6f04ebbdb230f3336ffe7b1d31818f29a92b37cc3e9f10daa6340`.
- Local unchanged regression: 128 tests, 34.417s, OK.
- Uploaded reproduction script executed on this exact runtime: F1, F2, F3 endpoints, F3 sources and F4 all reproduce. These probes demonstrate old defects; they do not validate new code.
- `python -m unittest discover -s tests -p test_rc2.py -v` on unchanged runtime: 14 tests, 17 failure assertions, exit 1. Positive literal formula/nested-input control passes. No skips or expected-failure annotations hide the red assertions.

Synthetic fixture reviews are software inputs only. No mathematics, originality, independent reading or new PDF-page acceptance is claimed by any test above.

## Contract decision

Software becomes `2.1.0-rc2`. KB/project/node/source/snapshot schema stays `2.0.0`. New output plans and policy-bearing reviews use schema `2.2.0`, policy `four-modes-2026-10-12-rc2`. Read legacy `2.0.0` and rc1 `2.1.0` under their explicit recorded contracts without mutation. Unknown or mixed combinations fail closed. Default current release/package requires rc2 review; historical validation is read-only, not a release bypass. New adoption uses new output IDs, never rewriting historical manuscripts, snapshots, packages or accepted records.

## Source responsibilities identified

| Requirement | Existing implementation and required change |
|---|---|
| F1 | `tex.inspect_tex/validate_locations`: retain original source/body context; all ordinary locations require meaningful reachable body content; canonical remains stronger. `release.semantic_scope_errors` shares a single scan with profile checks. |
| F4 | `profiles` design check reused by `exports.validate_structure` and release; `prepare_output` reports unfinished scaffold while preserving author files; `build_output` permits only explicitly draft-specific incompleteness, not arbitrary structure errors. KB readiness never depends on outline existence. |
| F3 | `models/profiles` typed comparison pairs and support checks; `plans.consumption` uses explicit pairs; `reviews.mathematical_inputs` binds actual comparison endpoints without turning navigation into proof dependence. |
| F2 | `plans.create_plan`, profile/view goals and selection reasons, outline and templates; semantic `view_focus` binding does not alter canonical statements or mode proof duties. |
| Compatibility | Explicit schema/policy routing in plans/reviews/CLI/release, preserving old bytes and distinguishing recorded assessment from current authorization. |
| Distribution | `validate_assets.py`, `package_release.py`, checksums, installed templates/references/agent, `tools/verify_release.py`, CI and actual installed execution all need synchronization. |

## Next acceptance boundary

F1–F4 runtime fixes, expanded adversarial matrix, real three-paper thematic/view manuscripts, compilation and page reading, isolated installation and final-head CI are not yet completed by this baseline commit. Formal original-Paper quality remains NOT VERIFIED without authorized original input. No merge or Release is authorized.
