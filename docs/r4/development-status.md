# R4 开发预览进度 / Development-preview status

[中文使用说明](../../README.md) · [English usage](../../README.en.md)

本页记录 `v2.1.0-r4-preview.1` 预发布准备时的实际范围，软件版本仍为 2.1.0。这是供检查与导师反馈的开发预览，不表示稳定版、五项数学全部验收或原创研究能力已验证。本文不把有限范围内的通过证据改称整项通过。

This page records the observed scope at prerelease preparation for `v2.1.0-r4-preview.1`, with software version 2.1.0. It is a development preview for inspection and supervisor feedback, not a stable release, acceptance of all five mathematical cases, or verified original-research capability. Bounded passing evidence is not promoted to whole-case acceptance.

## 工程 / Engineering

- Windows 管理员环境的独立安装：280/280 工程测试通过，0 skipped；安装包 69 个成员／68 个运行资源身份一致；3 页中性 TeX 构建检查通过。这些检查没有生成或批准一篇新数学文章。
- Independent installation in a Windows administrator environment: 280/280 engineering tests pass, 0 skipped; 69 archive members / 68 runtime resources match; a three-page neutral TeX build passes. These checks do not generate or accept a new mathematical article.
- 日常安装不需要创建 symlink 或执行这次测试的 UAC 步骤。提权弹窗是实际 symlink 安全拒绝测试；系统权限设置未修改。
- Normal installation needs neither symlink creation nor that test's UAC step. Elevation exercised actual symlink rejection; system permission settings were not changed.

## 第一轮 / Round 1

五项整项结论均为失败，但原因并非“全部数学都错误”。保留原轮次与证据，不展示失败稿为通过的公开范例。

All five whole-case verdicts failed; this does not mean all the mathematics was wrong. Original round identities/evidence are preserved, and failed drafts are not displayed as accepted public exemplars.

| 案例 / Case | 有限证据与整项失败原因 / Bounded evidence and whole-case failure |
|---|---|
| E01 · dHYM Minimal | 完整 19 页文章在限定范围内有来源、数学、PDF／重建证据；planner 漏掉实质 question，整项 FAIL_SOFTWARE_QUESTION_SELECTION。 / The complete 19-page article has bounded source, mathematical, PDF/rebuild evidence; the planner omitted a substantive question, giving FAIL_SOFTWARE_QUESTION_SELECTION overall. |
| E02–E04 · comparison Minimal/Thematic/Lecture | freeze 未包含辅助 review.inputs，且缺少输出精确证明承诺的审阅绑定；未形成正文／PDF，整项失败。 / Freeze omitted auxiliary review.inputs, and output-specific detailed proof promises lacked review binding; bodies/PDFs were not produced and the cases failed. |
| E05 · Schur Paper | 经典 6 页显著草稿及预期正式交付拒绝有有限可用证据；worker 越界读取被禁止的全局 PDF skill，整项 FAIL_PROCESS_BOUNDARY。 / The classic-result six-page visible draft and expected formal-delivery refusals have bounded usable evidence; a worker read a forbidden global PDF skill, giving FAIL_PROCESS_BOUNDARY overall. |

## 当前候选与第二轮 / Current candidate and Round 2

已作通用修复：仅支持当前 r4、声明审阅输入的安全快照闭包、所有请求输出的精确 reader/proof promises 与真实非作者步骤核查、保留实质 question、准确传播并执行读取边界。安装内提供原生来源／PDF 全页查看与重建做法；模板和 pending 请求不产生 accepted。

Generic repairs address current-r4-only support, safe snapshot closure of declared review inputs, detailed reader/proof promises for all requested outputs with actual non-author step checks, substantive question retention, and accurate read-boundary propagation/enforcement. Installed resources provide native source/PDF all-page inspection and rebuilding; templates and pending requests do not grant acceptance.

当前第 2 轮继续完成。最新用户指令明确不启动第 3 轮；若第 2 轮不达标，就停止并报告，不继续运行代码修复。第一轮仍计数；原三轮上限仅属历史计划，不构成启动第三轮的授权，预发布或换聊天均不重置边界。普通产品没有永久开发轮数限制。预发布只提供当前快照，不移动 main，不解除数学草稿的正式研究交付拒绝，也不展示失败稿为通过范例。

本轮 Schur Paper 的真实非作者知识审阅已经完成、无需返修，但普通 kb readiness --plan 对该已知结果报告缺少原创贡献并阻断。控制台仍将完成真实 DRAFT_UNVERIFIED 预览、正式交付拒绝与三种变体检查，不虚构原创性。该项正在既定 Astra/xhigh 独立核实，最终 E05 尚未验收；不得写成已解决或所有 Paper 都有确定缺陷。

Current Round 2 continues. The latest human instruction explicitly forbids starting Round 3; if Round 2 does not meet the requirements, stop and report without further runtime fixes. Round 1 remains counted. The original three-round maximum is historical planning, not authorization for Round 3; a prerelease or new chat does not reset the boundary. The ordinary product has no permanent development-round limit. The prerelease provides only the current snapshot, does not move main or lift draft formal-research delivery refusal, and does not present failed drafts as accepted exemplars.

In this round, Schur Paper's actual non-author knowledge review completed without revision, but ordinary kb readiness --plan reports a missing original contribution for this known result and blocks it. The controller will still complete actual DRAFT_UNVERIFIED preview, formal-delivery refusal and three variant checks without inventing originality. The established Astra/xhigh independent verification is ongoing and final E05 acceptance is pending. This must not be described as resolved or as a confirmed defect in every Paper.

仍未验证 / Still unverified: 全五项最终达标、任意主题泛化、真实学生学习效果、外部同行评审、原创研究能力及任意环境重建 / final acceptance of all five cases, arbitrary-topic generalization, real student learning, external peer review, original-research capability and rebuilding in arbitrary environments.

[预发布页面 / Prerelease page](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0-r4-preview.1)
