# 2.4.1 设计依据与仓库基线

观察日期：2026-10-21（Asia/Shanghai）。这是设计证据和可复查定位，不是安装包运行时报告。

## 1. 初始设计任务

目标是设计 Pure-Math-Survey 2.4.1：只上线 minimal，其他模式暂时下线；移除运行过程审核，尽量减少完成知识库及文章所需的 token；写作依据 rules.v22；知识库参考讨论转写，并作为 minimal 的内容来源；交付分步 PR、交接逻辑、持久化规范和开发状态。

本节记录初始设计包的任务与授权：当时只授权设计交付，未创建远程分支/PR、修改仓库、合并或发布。后续授权及实施进度见唯一 DEVELOPMENT_STATE.yaml，并以 GitHub 实况核实。

## 2. 两份上传来源

| 来源 | 身份 | 本设计的使用方式 |
| --- | --- | --- |
| `rules.v22.txt` | 22,806 bytes；SHA-256 `452a4d7548c23bc75fe8fec6299ae9777a3e6763eb5f955063d938c2f3b6b2c7` | 原文冻结；内容/排版保留，审核流程按本轮要求显式适配 |
| `讨论数学形式化验证相关工作.md` | 137,795 bytes；SHA-256 `f6e59d20ee4793c9346d057f3de1a25ebd3507d94d76b00a8a78240771eef8f7` | 提炼知识内容、粒度、重要性及轻量目标；完整稿不随本包再次分发 |

转写自身说明：未逐句回听、部分术语不确定、未可靠区分说话人。下表只提炼反复一致的产品目标，不将其中数学举例、模型能力、费用或规模估计写成可靠事实。

### 2.1 转写中的相关位置

| 时间位置 | 可采用的需求 | 2.4.1 对应决定 |
| --- | --- | --- |
| 00:00:40–00:04:24 | 可读数学框架与底层形式化是有区别的任务 | 不加入 Lean 或公理级重证 |
| 00:14:59–00:17:27；00:22:04–00:23:58 | 知识包括定义、条件、结论、技术；标注要有依据 | 核心概念独立可索引；结果有完整条件与结论 |
| 00:27:19–00:28:45；00:32:26–00:34:14 | 论文拆出核心框架和约 5–10 步，每步说明知识与技术 | 按主要阶段选模块，不固定总节点数 |
| 00:35:56–00:36:54；01:17:21–01:18:49 | 知识和技术应能积累为可复用的库 | 同一个节点格式容纳结果与方法，避免两套系统 |
| 01:19:19–01:19:49；02:00:25–02:01:54 | 例子、反例及不可行路线也能有用 | 只收录范围内必要边界，不自动找反例 |
| **01:20:59–01:21:36** | 重要性分层与知识先后次序不同 | 重要性候选、阅读作用、依赖关系分开 |
| 01:21:36–01:22:31；01:51:35–01:52:44 | 派发和重型流程过重，先快速获得所需因素 | 当前会话完成，不强制多角色及审核 |
| 01:27:43–01:30:29；01:36:22–01:36:51 | 主结论、关键知识、技术路线、组装及图 | 三节 Minimal 与同源 routes/TikZ |
| 01:36:52–01:40:01 | 已有证明不必整套再校验 | 提取准确接口，不复现完整证明审核 |
| 01:56:30–01:59:48 | 先明确重要知识；重要贡献也可能是定义或方法 | 不只抽 theorem，不追求强填五层 |
| 02:40:00–02:47:24 | 单有 overview/逻辑概要看不出具体可用知识 | 必须有可调用数学单元，索引只负责导航 |
| 02:50:22–02:51:51 | 定理形式、条件和核心步骤应清楚 | canonical 陈述、源定位和关键连接 |
| 03:21:32–03:22:34 | 展开深度由复用需要决定 | 不扩写不用的内部细节 |

不能从录音推导“本版必须批跑 500 篇”“消耗只能是某个账户额度百分比”“必须十分钟完成”“自动赋确定分值”等结论。本版为以后打分试验提供材料，不实施训练、打分器或排序。

### 2.2 rules 的关键依据

内容同源及颗粒度来自 #002–#005、#016–#027、#033–#045、#049–#052。局部完整陈述与定义复用来自 #003、#052–#067、#088–#089 及末尾 Reading contract。六页与排版来自 #001、#015、#081、#086–#095。无描述性结果标题与相邻来源来自 #062–#065。

取消审核的适配根据本轮直接指令，具体覆盖 #095–#097、#099 的流程要求及 qa.md；#100 转为开发规范。其余涉及检查的词汇按首次准确抽取和有限机械构建实施，不另开 reviewer。

## 3. 已核实仓库身份

- 仓库：[ZhiyaoXiongMath/Pure-Math-Survey](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey)。
- 实际 main：[3db6cdd53b524698053de4aa98603e7a9ed9742b](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/commit/3db6cdd53b524698053de4aa98603e7a9ed9742b)。
- 最新正式 Release：[v2.1.0](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0)，2026-10-16 发布，非 draft、非 prerelease。
- 软件 `2.1.0`，KB/snapshot schema `2.0.0`，output/review schema `2.2.0`，policy `four-modes-2026-10-15-r5`；见固定提交的 [README](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/README.md)。
- 当时的 tree 没有 AGENTS.md；旧开发入口是 docs/development/CONTRACT.md 与 STATUS.md。实际实施前重新核对，不能假定以后仍不存在。

设计直接读取 GitHub 元数据及固定提交文件。源码仅部分取回供分析；没有把部分文件目录当作完整 git checkout，没有执行现有测试或论文生成。

## 4. 必须改到的实际代码位置

以下路径均相对上述固定提交。给出的行号用于这次定位，后续改动后以实际文件为准。

| 位置 | 观察事实及影响 |
| --- | --- |
| [SKILL.md](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/SKILL.md)，12–22 行 | 强制 Astra/ultra 工作聊天，缺派工能力阻塞；轻量默认必须解除 |
| 同文件，28–44 行 | 广泛来源流程、成对 fast/slow、非作者知识/理解审核；不能沿用为隐含要求 |
| [cli.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/cli.py)，13–38 行 | 四 profile、五 view、review/readiness/eligibility 等活跃命令，需真实收缩 |
| [models.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/models.py)，69–105 行 | 现有 JSON frontmatter 与 canonical 字面 LaTeX 可复用；删减非必要字段 |
| [knowledge.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/knowledge.py)，22–78 行 | inventory 本身加载 reviews，强制 overview/discovery/coverage，非纯提示词问题 |
| [readiness.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/readiness.py)，13–90 行 | source/math/coverage 审阅硬门禁 |
| [exports.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/exports.py)，48–81、130–153 行 | prepare/verify_generated 重复依赖 readiness，携带 review 闭包 |
| [snapshots.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/snapshots.py)，41–83 行 | 冻结含 review bindings，不宜仅取消入口再保留底层要求 |
| [release.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/survey_core/release.py)，47–106 行 | 正式打包要求 semantic/visual accepted，需新产物完成语义 |
| [profile-minimal.tex](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/assets/templates/profile-minimal.tex) | 12pt amsart、三节、无默认六页与新页书目；与 v22 有实质差异 |
| [package_release.py](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/skills/pure-math-survey/scripts/package_release.py)，20–100 行 | 严格清单包含旧模式与审核/派工资源，新增/删除须同步清单与 checksums |
| `scripts/validate_assets.py` 与 `tools/verify_release.py` | 当前验证四模式×五视图；需变为 minimal 正向 + 下线模式拒绝的有效用例 |
| [.github/workflows/ci.yml](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/.github/workflows/ci.yml) | Linux Python 3.10/3.12、Windows Python 3.12 及安装/TeX 工程检查，可保留相关能力 |
| [旧开发合同](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/docs/development/CONTRACT.md)与[旧状态](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/blob/3db6cdd53b524698053de4aa98603e7a9ed9742b/docs/development/STATUS.md) | 旧阶段要求用户掌握 merge；状态仍有发行准备描述，真实 Release 已存在，说明交接必须查实时状态 |

此外 `agents/openai.yaml` 的 default prompt 仍提 r4，而当前政策是 r5；本次应统一入口说明，不只改 README。

## 5. 由设计作出的选择

以下是为了落地而提出的设计决定，不冒称录音已有精确规范：

- 使用五个顺序 PR；每个 PR 一次有限独立代码审查。
- KB 与 output schema 升为 3.0.0；不增加自动迁移器。
- 保留 Markdown + JSON frontmatter + canonical LaTeX，继续使用现有基础工具。
- 用单一 STATE 和 GitHub 实况交接；不另建 HANDOFF 状态副本。
- 重要性可空，用 proposed/human_supplied/unassigned 区分来源；不强行赋权。
- 默认实际编译 PDF，最多两轮局部错误修复；不运行视觉审核链。
- 三节 Minimal 骨架继续使用，内部分组服从真实依赖；原始 rules 的优先性保持。

这些选择可在实施中因具体证据局部调整，但必须在当前 PR 与 STATE 说明原因，不能默默恢复审核、扩大产品范围或放弃数学内容要求。

## 6. 初始设计包交付时未实施与未取得的数据

没有新版代码、PR、安装包、真实论文端到端运行或 token 对照测量。仓库中的既有发布验证是旧版事实，不能当作 2.4.1 验收通过。本文所有“应当”“目标”描述均为未来合同。
