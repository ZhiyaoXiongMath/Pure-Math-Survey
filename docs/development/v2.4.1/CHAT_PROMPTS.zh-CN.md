# 2.4.1 分阶段开发提示词

这些提示是供用户选择后实际发送的模板，**模板存在本身不构成仓库修改、消息发送、合并或发布授权**。阶段 ID 与 GitHub PR 编号不同。

首次启动上传完整开发包；PR-01 合并后，规范和状态已在仓库，后续通常只给仓库及实际 PR 链接即可。每个阶段都分开发和独立审查，不让一个开发聊天自动完成全部阶段。

## A. 第一次：只做 PR-01

```text
请作为 Pure-Math-Survey 2.4.1 的开发负责人，使用 GitHub 连接操作：
https://github.com/ZhiyaoXiongMath/Pure-Math-Survey

我已上传 Pure-Math-Survey-2.4.1-Development-Package.zip。
先解压，读 START-HERE.zh-CN.md，再读开发指南、PR_WORKFLOW、
DEVELOPMENT_RULES 和 DEVELOPMENT_STATE。

本聊天只实施 PR-01：将合同、原始 rules.v22、唯一开发状态和交接规范
落入仓库，创建/增补根 AGENTS.md，给旧合同和状态加历史及新入口指针。
不要额外提交私人转写原文，不要改写 rules 原文。

先核实最新 main、已有相关分支及 PR，再继续实际工作；不要重新设计方案。
我授权你为 PR-01 创建或接续开发分支、修改所需仓库文件、提交、推送，
并创建一个 PR。运行本阶段必要检查。此聊天不合并、不发布、不实施 PR-02。

完成时给我真实 PR 链接、所做检查、尚未做的事情，以及可复制到新聊天的
独立审查提示。不要只给计划；应完成到可审查的实际 PR。
```

## B. 每个 PR 的独立审查

将下面唯一的占位符替换为实际 PR 链接；不要沿用上一次的 PR 或 SHA。

```text
请独立审查这个 Pure-Math-Survey 2.4.1 PR：
[实际 PR URL]

你是独立审查者，不参与该 PR 的实现。
先读取当前 PR HEAD、base、diff、相关 checks，以及仓库根 AGENTS.md、
docs/development/v2.4.1/DEVELOPMENT_STATE.yaml、DEVELOPMENT_RULES.zh-CN.md，
再读取开发指南和 PR_WORKFLOW 中本阶段适用的部分。
这些规范优先从被审 PR 的实际 head_sha 读取，不默认从 main 读取；
尤其 PR-01 的新文件尚未合并到 main。对 base 的旧规范只作差异背景。

本次目标是 minimal-only、无运行审核、同源轻量 KB 与 rules.v22 成文。
不要用旧四模式/r4/r5 审核义务否定本次已明确取消的流程。
只审当前阶段范围及受影响风险，复用已有有效证据，发现具体问题才补查。
不要重新跑整篇论文审核或为没有实际风险的点加测试。

我授权你把审查结论提交为该 PR 的 GitHub review 或 comment；
不要修改实现、合并或发布。
如有问题，按影响给出文件位置、为什么有问题和最小修复建议；
无阻塞问题则明确说明，并列出实际检查范围和未检查项。
把实际审查的 HEAD 及结果链接写在回复里，不为记录它创建新提交。
```

## C. 返回原开发聊天：只修当前 PR

```text
请继续当前 Pure-Math-Survey 2.4.1 PR，按这个实际审查结果修正：
[review URL 或粘贴具体问题]

先核实当前 HEAD 与审查所基于的版本，读取 STATE。
只修有依据的问题和受影响行为；不扩大阶段范围，不恢复运行审核。
我授权你在原分支修改、提交和推送，并更新该 PR 的必要说明。
运行相关检查后，给出新 HEAD、修正对应关系和需要补审的范围。
不合并、不发布、不提前做下一阶段。
```

## D. 如果希望助手完成一次合并

用户也可以在 GitHub 手动合并；已经手动合并时跳过此提示。

```text
我授权你合并这个 PR：
[实际 PR URL]

先确认当前实际 HEAD、相关 CI、审查结论及未解决阻塞；
如果 HEAD 自审查后有实现内容变化，须有独立审查者对变化及受影响部分的补审；
不得由原实现者以自查替代独立补审。尚缺补审时保留具体待合并 PR 并说明缺项，
不要从头重审无变化的部分。仅 base/元数据变化则核实其实际影响。
条件满足时合并该 PR，使用可用的 expected-head 防止竞态。
沿用仓库/当前已约定合并方式，不改无关分支或历史。
合并后核实实际 merge SHA；不要为了把这个 SHA 写回当前 PR 而再造提交。

本次不实施下一阶段、不发布版本。给我实际合并结果和下一阶段开发提示。
若存在未解决阻塞，说明具体对象和原因，不猜测通过。
```

## E. PR-01 之后：自动判断并做下一个阶段

这是后续最常用的提示，免去手填 PR-02/03/04/05；“自动判断”仍只执行一个当前阶段。

```text
请继续开发 Pure-Math-Survey 2.4.1：
https://github.com/ZhiyaoXiongMath/Pure-Math-Survey

先读取根 AGENTS.md，以及 docs/development/v2.4.1/ 中的
DEVELOPMENT_STATE.yaml、DEVELOPMENT_RULES.zh-CN.md 和 PR_WORKFLOW.zh-CN.md。
首次接手再读 DEVELOPMENT_GUIDE.zh-CN.md。
查询 GitHub 实际 main、已有相关分支/PR、checks/review/merge，不仅看状态文件。

如果前一阶段已经合并，在当前新阶段顺带登记真实 merge SHA，
只执行下一个尚未完成的阶段；如果当前 PR 仍 open，就接续它，
按实际情况修正或交付审查，不越过未合并阶段另开下一条实现。
如果已有同阶段工作，续用而不重启。

我授权你完成当前一个阶段所需的分支、仓库修改、提交、推送及 PR 创建/更新。
按本阶段验收要求运行必要检查，更新唯一 STATE；不要增加运行时审核。
本聊天不合并、不发布、不自动完成余下所有阶段。

完成时给我实际 PR、实现范围、真实验证、剩余问题和新聊天独立审查提示。
如果全部阶段已经合并，报告实际发行准备/Release 状态，不另开空的开发 PR。
```

## F. PR-05 合并后：正式发布

只有在用户准备正式发布时发送。候选包、说明和相关检查应已经具备。

```text
请正式发布 Pure-Math-Survey 2.4.1：
https://github.com/ZhiyaoXiongMath/Pure-Math-Survey

我授权你在核实 PR-05 已合并及当前相关检查完成后，
从实际最终合并提交构建/核对 pure-math-survey-2.4.1.zip 和 .sha256，
创建 v2.4.1 tag 与正式 GitHub Release，并上传安装包及校验文件。

先查询现有 tag/Release，避免重复或覆盖既有发布；如请求已完成，直接核实并报告。
保留旧版本及历史用户数据。不得把 GitHub Source code ZIP 当成安装包。
不得在没有相关证据时声称数学已独立验证或 token 已节省某个百分比。

发布后检查 tag 指向、Release 状态、附件及校验值，给我正式下载链接和
最短安装/使用说明。不要为登记自身最终 SHA 创建无意义的额外 PR。
```

## G. 无法判断之前进行到哪一步时

```text
请恢复 Pure-Math-Survey 2.4.1 的开发状态：
https://github.com/ZhiyaoXiongMath/Pure-Math-Survey

读取根 AGENTS.md、2.4.1 STATE 和 PR 流程，再核实实际分支、PR、HEAD、
检查、审查、合并和 Release。先做只读恢复，不重新设计或另起实现。
告诉我当前准确阶段、已经完成的工作、当前实际阻碍，以及应该发送
开发/审查/修正/合并/发布中的哪一条提示；如当前会话已有明确授权，
在该授权内直接继续完成，不再次索取相同许可。
```
