# Development contract / 开发合同

This file fixes the four development stages and their boundaries. The repository-native [complete public PR-04 editorial development guide](PR04-EDITORIAL-GUIDE.md) now specifies all PR-04 writing obligations, implementation limits, and acceptance checks. Software remains 2.1.0; PR-01/02/03 did not upgrade the r4 editorial policy.

本文固定四阶段的范围与交付顺序；[PR04-EDITORIAL-GUIDE.md](PR04-EDITORIAL-GUIDE.md) 是仓库内 PR-04 的完整公开执行规范，包含四模式数学写作规则和可检验的验收边界。前三阶段已合并，PR-04 启动前必须核实最新 main 与现有代码。

| Stage / 阶段 | Main scope / 主范围 | Gate / 交付条件 |
|---|---|---|
| PR01 | Platform paths, resource installation and truthful Linux/Windows CI. 平台路径、资源安装与据实 CI。 | Merged as [PR #4](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/4). 已合并；历史证据保留。 |
| PR02 | Pending review templates for applicable canonical statements; exact author plan promises; aggregate validation; safely stage and accept final knowledge/evidence bytes. 实际适用 canonical 的 pending 模板、作者精确承诺、聚合校验、最终知识／证据字节的安全暂存接收。 | Neutral synthetic fixtures exercise plan → promise → review/coverage → staging → freeze → explicit adoption → readiness → prepare, plus refusal and rollback. 合成用例验证工程流程，不能替代真实数学审阅。 |
| PR03 | Original-source reading, controlling versions/locators, original material bytes and redistribution permission. Separate knowledge READY from Paper Draft and formal research eligibility. 原始来源阅读、版本／定位、原文字节、再分发权限；分离知识 READY、Paper Draft 与正式研究资格。 | Merged as [PR #6](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/6), merge `2f5510c6813c1562a67e094f0bc70bacacdcce04`; historical CI/review evidence retained. 已合并。 |
| PR04 | Four-mode writing; fast first and slow on demand; numbered statements without descriptive titles; accurate external references placed near use. 四模式成文，快层优先／慢层按需、编号但无描述标题的陈述、准确且就近的外部引用。 | **Read all of [PR04-EDITORIAL-GUIDE.md](PR04-EDITORIAL-GUIDE.md) before editing.** It provides the complete public operational rules derived from r6.3; no private source upload or old combined-PR prompt is required. New policy identity, affected positive/negative checks, real CI and non-author review remain necessary. |

Each stage has one main PR, actual CI evidence, independent review and user-controlled merge. A local candidate or green badge alone does not complete a stage. Status is maintained in [STATUS](STATUS.md); the linked GitHub PR/checks/review state is the live authority.

每阶段采用一个主 PR，完成真实 CI 与独立审核，由用户决定 Merge。状态页仅记已核实阶段；GitHub 的实时 PR／checks／review 状态是权威。

PR02 reuses existing plans, promise_projection, reviews, coverage, snapshots, readiness, safe paths, hashes and the single-writer file workflow. Requests are generated from the authored plan rather than a handwritten restatement. Templates fill identities, paths and hashes mechanically; actual reviewer identity, date, proof actions, statement findings, source basis and unchecked scope require real work. Batch checks aggregate independent omissions and report stale binding root causes. Candidate acceptance validates the final byte view, checks concurrent changes and restores touched files on installation failure. It introduces no database transaction system or second mathematical engine. Freeze and explicit plan adoption remain separate steps.

PR02 复用现有规则与普通文件暂存／单写入／回滚；生成模板不代表阅读或 accepted。来源、数学、理解、工程安装、编译与逐页检查各自按实际执行范围报告。skipped、NOT_EXECUTED 和缺失产物不能写成通过。历史 accepted、快照及验收轮次保持不可变，不重跑或重写来消除历史失败。私人原文、私有路径和聊天记录不进入公开提交。

## PR-04 bootstrap and lean execution / 第四阶段启动与最小复杂度

- First verify live `origin/main`, [STATUS.md](STATUS.md), and the [full PR-04 guide](PR04-EDITORIAL-GUIDE.md). Current public guide is authoritative for PR-04 editorial implementation; the historical private unredacted r6.3 source remains **private** and is not a required public repository artifact. No old single-PR Website orchestration is authorized.
- The preparation branch `codex/pr04-editorial` contains **documents only**; it is not an accepted PR or completed implementation. An explicitly authorized local Codex Controller should fetch that exact branch, ensure it descends from then-current main, and continue the **same branch** (and one subsequent PR) rather than duplicate documents or create another development branch. Do not modify `main` directly.
- Reuse current source, templates, review fields and TeX infrastructure; test discriminating failures, not cosmetic metrics. The stable reviewer does not author code. Routine CI and focused review fixes remain within one PR. Only the user may merge; release and actual mathematical E01–E05 are separate activities.
- Update [STATUS.md](STATUS.md) at an evidence-backed stage boundary, not after every CI log. Branch-head/CI links are real-time GitHub facts; avoid a commit solely to publish the final reviewed HEAD and thereby invalidate the review.
