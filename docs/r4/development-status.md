# R4 开发预览进度 / Development-preview status

[中文使用说明](../../README.md) · [English usage](../../README.en.md)

本页记录 `v2.1.0-r4-preview.1` 预发布准备时的实际范围，软件版本仍为 2.1.0。这是供检查与导师反馈的开发预览，不表示稳定版、五项数学全部验收或原创研究能力已验证。本文不把有限范围内的通过证据改称整项通过。

This page records the observed scope at prerelease preparation for `v2.1.0-r4-preview.1`, with software version 2.1.0. It is a development preview for inspection and supervisor feedback, not a stable release, acceptance of all five mathematical cases, or verified original-research capability. Bounded passing evidence is not promoted to whole-case acceptance.

## 工程 / Engineering

- Windows 管理员环境的独立安装：280/280 工程测试通过，0 skipped；安装包 69 个成员／68 个运行资源身份一致；3 页中性 TeX 构建检查通过。这些检查没有生成或批准一篇新数学文章。
- Independent installation in a Windows administrator environment: 280/280 engineering tests pass, 0 skipped; 69 archive members / 68 runtime resources match; a three-page neutral TeX build passes. These checks do not generate or accept a new mathematical article.
- 日常安装不需要创建 symlink 或执行这次测试的 UAC 步骤。提权弹窗是实际 symlink 安全拒绝测试；系统权限设置未修改。
- Normal installation needs neither symlink creation nor that test's UAC step. Elevation exercised actual symlink rejection; system permission settings were not changed.


- Linux 的 Python 3.10／3.12 main CI 已完成：[run 38336303282](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38336303282)。两个安装验证均为 INCOMPLETE：每个 job 的 280 项中，277 项实际执行并通过，3 项 Windows 专用测试跳过（扩展路径／UNC、junction 越界、Windows Job Object）。当前外部安装验证器遇到任何 skip 就报告整体 INCOMPLETE；不能据此称为 Linux 全通过或所有符号链接都未测试。Windows 本机同候选 280/280、零 skip 的独立证据仍成立；本次只记录，不修改运行代码、测试或验证器。
- Linux Python 3.10/3.12 main CI completed: [run 38336303282](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/actions/runs/38336303282). Both installation validations are INCOMPLETE: each job actually ran and passed 277 of 280 tests, skipping three Windows-specific tests (extended paths/UNC, junction escape and Windows Job Object). The current external installation verifier reports overall INCOMPLETE on any skip; this is neither complete Linux acceptance nor evidence that all symlink tests were unexecuted. Same-candidate independent Windows evidence remains 280/280 with zero skips. This finding is recorded without changing runtime code, tests or verifier.

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

当前第 2 轮 E01 Minimal 已由主控制台接管并优先推进，其余测试安全暂停；暂停不代表失败或通过。最新用户指令明确不启动第 3 轮；若第 2 轮不达标，就停止并报告，不继续运行代码修复。第一轮仍计数；原三轮上限仅属历史计划，不构成启动第三轮的授权，预发布或换聊天均不重置边界。普通产品没有永久开发轮数限制。用户现已授权 main 更新为当前预览快照；现有 tag 与安装附件不变。这不解除数学草稿的正式研究交付拒绝，也不展示失败稿为通过范例。

本轮 Schur Paper 的真实非作者知识审阅已经完成、无需返修，但普通 kb readiness --plan 对该已知结果报告缺少原创贡献并阻断。Schur 的后续预览、拒绝／变体检查和独立核实现均暂停，最终 E05 尚未验收；已有观察保留，不虚构原创性，不写成已解决或所有 Paper 都有确定缺陷。

The main controller has taken over and prioritizes Round 2 E01 Minimal; other tests are safely paused. Pause is neither failure nor acceptance. The latest human instruction explicitly forbids starting Round 3; if Round 2 does not meet the requirements, stop and report without further runtime fixes. Round 1 remains counted. The original three-round maximum is historical planning, not authorization for Round 3; a prerelease or new chat does not reset the boundary. The ordinary product has no permanent development-round limit. The user has now authorized updating main to the current preview snapshot; the existing tag and installation assets remain unchanged. This does not lift draft formal-research delivery refusal or present failed drafts as accepted exemplars.

In this round, Schur Paper's actual non-author knowledge review completed without revision, but ordinary kb readiness --plan reports a missing original contribution for this known result and blocks it. Further Schur preview, refusal/variant checks and independent verification are now paused; final E05 acceptance remains pending. Existing observations are preserved without inventing originality or claiming resolution/a defect in every Paper.

仍未验证 / Still unverified: 全五项最终达标、任意主题泛化、真实学生学习效果、外部同行评审、原创研究能力及任意环境重建 / final acceptance of all five cases, arbitrary-topic generalization, real student learning, external peer review, original-research capability and rebuilding in arbitrary environments.

[预发布页面 / Prerelease page](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0-r4-preview.1)
