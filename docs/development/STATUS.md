# Verified development status / 已核实开发状态

**Observed:** 2026-10-16. **Live authority:** GitHub `main`, PRs, commits and Actions; this file is a compact **handoff snapshot**, not an approval or continuous monitor.

**Observed `main`:** `d76e18f7d863f2b755f4e4aa9089e88b03d9c99f` (merged PR #8). Verify again at the start of each Codex session. Software is 2.1.0, KB/snapshot schema 2.0.0, output/review schema 2.2.0, and editorial policy `four-modes-2026-10-15-r5`.

| Stage | Verified state | Next action / limitation |
|---|---|---|
| PR-01 — platform/CI | **MERGED**: [PR #4](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/4), merge `c22f390851eeb1a1ddfa0d8849380e892a521fa4`. | Engineering scope only; historical five-case mathematical E2E is not inferred. |
| PR-02 — Review handoff | **MERGED**: [PR #5](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/5), merge `9dd38edf92cd766b1b4e593d852e3298590056fc`. | Existing review/template/promise/snapshot interfaces are to be reused. |
| PR-03 — sources/Paper tiers | **MERGED**: [PR #6](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/6), merge `2f5510c6813c1562a67e094f0bc70bacacdcce04`. [CI run 38570999734](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38570999734) completed SUCCESS for its verified head; test results are engineering evidence. | No source/Paper eligibility refactor is authorized under PR-04. |
| PR-04 — four-mode editorial | **MERGED:** [PR #7](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/7), merge `9f1793411f8a878373836a29c4241f60b0745c16`. Policy is `four-modes-2026-10-15-r5`; software and schema identities are unchanged. | Historical implementation CI and independent review remain in the PR; the later actual-main CI below covers the integrated software. |
| Python 3.10 procfs test race | **MERGED:** [PR #8](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/8), merge `d76e18f7d863f2b755f4e4aa9089e88b03d9c99f`. Only `tests/test_release_verifier.py` changed from the mathematical baseline. | [Actual main CI](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38846120380): Linux Python 3.10, Linux Python 3.12 and Windows Python 3.12 all SUCCESS. Runtime, mathematical rules and installed resources are byte-identical to the completed comparison-theorem acceptance. |

## Release preparation / 发行准备

The completed comparison-theorem mathematical acceptance is reused within its original scope: one frozen KB, four outputs totaling 50 pages, three permitted formal expository packages, and a known-result `DRAFT_UNVERIFIED` Paper with expected eligibility/formal-delivery refusal. Four process/bookkeeping exceptions and the unverified scope remain disclosed; protocol compliance is not an unqualified PASS. This does not clear the distinct historical E01–E05 failures/pauses or certify originality, external human peer review, real student learning or cross-platform mathematical reconstruction.

已完成的比较定理数学验收按原范围复用：一个冻结 KB、四项共 50 页正文／草稿、三项许可通过的正式阐述文章包；已知结果 Paper 保持显著草稿，资格及正式交付拒绝符合预期。四项流程／记账例外与未验证范围保留，协议不是无例外 PASS；历史 E01–E05 的失败／暂停不被清零，也不认证原创性、外部人工同行评审、真实学生学习或跨平台数学重建。

The `release/v2.1.0-prep` work is documentation only. Its current HEAD must pass the three required CI jobs, followed by independent non-author review. Keep the preparation PR OPEN for user-controlled merge; no tag or Release before that merge and explicit continuation. Final publication still requires checks bound to the final main commit. See [release notes](../releases/v2.1.0.md). Live PR/check/review links belong in the PR discussion, without another status-only commit.

发行准备仅更新文档，须先取得当前 HEAD 三平台 CI 成功，再完成独立非作者审查。准备 PR 保持 OPEN，由用户决定合并；此前不创建 tag 或 Release。合并并获明确继续授权后，再绑定最终 main 完成正式发行检查。

## Historical PR-04 startup snapshot — 2026-10-15

The sections below preserve the earlier startup/candidate observations, including failed or partial local checks. They describe that historical stage; they do not replace the merged state or authorize new work.

以下保留旧启动／候选观察及失败、部分完成的本地检查，均属于历史阶段，不替代上方已合并状态，也不授予新工作权限。

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
