# Verified development status / 已核实开发状态

**Observed:** 2026-10-15. **Live authority:** GitHub `main`, PRs, commits and Actions; this file is a compact **handoff snapshot**, not an approval or continuous monitor.

**Observed `main`:** `2f5510c6813c1562a67e094f0bc70bacacdcce04` (merged PR #6). Verify again at the start of each Codex session.

| Stage | Verified state | Next action / limitation |
|---|---|---|
| PR-01 — platform/CI | **MERGED**: [PR #4](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/4), merge `c22f390851eeb1a1ddfa0d8849380e892a521fa4`. | Engineering scope only; historical five-case mathematical E2E is not inferred. |
| PR-02 — Review handoff | **MERGED**: [PR #5](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/5), merge `9dd38edf92cd766b1b4e593d852e3298590056fc`. | Existing review/template/promise/snapshot interfaces are to be reused. |
| PR-03 — sources/Paper tiers | **MERGED**: [PR #6](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/6), merge `2f5510c6813c1562a67e094f0bc70bacacdcce04`. [CI run 38570999734](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38570999734) completed SUCCESS for its verified head; test results are engineering evidence. | No source/Paper eligibility refactor is authorized under PR-04. |
| PR-04 — four-mode editorial | **OPEN, UNMERGED:** [PR #7](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/7), continuing the existing `codex/pr04-editorial` preparation branch. Implementation adds policy `four-modes-2026-10-15-r5`; software and schema identities are unchanged. | At this observation, [first CI run](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38676436604) is in progress and independent review is pending. Current-head CI/job/artifact and independent-review receipts are maintained in the PR discussion, not by repeatedly committing this snapshot. Only the user may merge. |

## PR-04 required startup checks

1. Recheck `origin/main` and any open PR-04 branch/PR; never trust the dated snapshot over GitHub.
2. Read the repository's [CONTRACT.md](CONTRACT.md), **complete** [PR04-EDITORIAL-GUIDE.md](PR04-EDITORIAL-GUIDE.md), `skills/pure-math-survey/SKILL.md`, and relevant current references, templates and tests. Do not request the old private r6.3 attachment as a default substitute: the full public operational rules are now in the repository.
3. Synchronize a clean local branch/worktree to remote `codex/pr04-editorial`, **not** the former PR-03 worktree. Do not overwrite local changes or force-update remote refs.
4. The branch's current three documentation edits are a **preparatory source-of-truth step**, not proof that editorial code or mathematical outputs are already accepted.
5. Finish only PR-04 feature work and its one independent review. Report engineering `PASS`, `FAIL`, `NOT_APPLICABLE`, `BLOCKED` and mathematical/source/PDF `NOT_EXECUTED` honestly. Stop short of merge/tag/Release.

**No duplicate project-state system:** only this document is maintained. Actual PR head SHA, job/artifact links and final independent-review receipt belong in the PR discussion; do not keep committing this file just to copy volatile status.

**Excluded:** private original materials, historical E01–E05 mathematical replay, unreviewed research originality and any unauthorized next PR. These are not silently accepted by completing four engineering stages.

## PR-04 candidate evidence at this observation

- Remote preparation HEAD was verified as `7ea49ef160490dec6c754762ef29e84518bb09df`, descending from the observed main. The three preparation documents were read completely; no private original was imported.
- Local affected regressions: 50 tests passed; the final isolated fixture wording change was followed by 12 editorial tests passing, including 20 mode/view combinations and actual Tectonic positive/negative compilation. Asset validation exercised all 20 preparations and 69 installed resources; packaging and source checksums passed.
- Full local run: 337 tests, 5 errors from unavailable `pdflatex`, 4 skips (three Windows-only and one external TeX/Poppler capability). This is **not PASS**. The strict local isolated verifier likewise failed without pdfLaTeX. A separately extracted no-pip venv with isolated Python passed resource checks and actual Tectonic installed-style smoke; that partial evidence does not replace mandatory CI.
- Actual Controller and Developer sessions use `gpt-6.1-sol / high`; the Developer writes only the isolated PR-04 worktree by instruction (underlying access is not an OS sandbox). A separate `gpt-6-astra / xhigh` read-only reviewer preflight successfully read the fixed HEAD and had a probe write denied by the OS. No code review is claimed from this preflight. The stable candidate requires the actual non-author review receipt.
- Synthetic source/attribution/dependency fixtures are bounded engineering inputs. Real literature/source review, private dHYM page review, historical E01–E05 mathematical E2E, research originality, external peer review and any Release remain **NOT_EXECUTED**. No merge, tag, Release or next phase is authorized.
