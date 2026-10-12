# Pure Math Survey 2.1.0

> **软件版本 2.1.0 发布准备；tag 与 GitHub Release 尚未发布。** 当前可复制仓库中的完整技能目录，或从源码构建本地安装包。四模式契约见[成文模式](references/editions.md)。
> r3 Minimal 默认采用局部问题单元，就近组织完整结果、必要支点、关键连接与首次使用；旧 r2/rc1、rc2 保留严格三节政策；Thematic 核查路线比较；Lecture 兑现逐步证明；Paper 需授权原创贡献、最接近前人成果核查与闭合证明，默认只生成内部草稿。软件校验不保证数学正确、原创性或读者理解。
> 知识 schema 为 2.0.0，新输出计划与新版政策审阅为 2.2.0；旧快照、正文和审阅不被静默迁移，历史 accepted 不构成新版政策验收。


**简体中文** | [English](README.md)

先维护数学知识，再按需成文：确定范围 → 阅读原始文献 → 建立可读的知识节点、关系与证据 → 检查覆盖与就绪状态 → 固定不可变快照 → 制定文章计划 → 写作 → 实际校验、编译及逐页检查 → 交付。

**核心命令行工具只依赖 Python 3.10+ 标准库。** 本技能面向需要长期维护文献依据、数学结论和综述／讲义／研究论文草稿的作者。作者或代理执行文献阅读与数学写作，工具检查文件约定、依赖、固定输入及声明的证据。它不是自动定理证明器或无人值守的写作服务，不包含服务器、向量数据库、多代理调度器或 Studio 桥接；r3 要求知识库自身具有可用快路线和可复现慢解释，其实际质量须按任务验证。

## 写作与流程示例

[balanced dHYM 文稿](assets/reference-samples/dhym-balanced/README.md)由用户经过多轮润色后提供，是主要的写作和排版参考；其中的 TeX、PDF、样式与参考文献保持原字节不变。它的六页篇幅和章节／结论数量不是其他文章的要求。独立的 [Schur 补示例](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/tree/main/examples/schur-complement)演示从知识库到文章的完整流程。知识节点与快照仍为 2.0.0；新计划及带新版政策的审阅采用 2.2.0，不能由旧软件读取。

[文章示例目录](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/tree/main/examples/dhym-balanced)只有独立 TeX 和原始 PDF。TeX 已内嵌所需样式和参考文献，数学正文没有改变。示例放在仓库中；Release 附件只包含技能安装包与校验文件。

## 安装与运行

`v2.1.0` tag 和 GitHub Release 尚未发布，目前没有该版本的正式下载附件。请将仓库中完整的 `skills/pure-math-survey/` 文件夹复制到宿主应用的技能目录。也可以在仓库根目录运行 `python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0.zip`，解压本地安装包，再复制其中唯一的 `pure-math-survey/` 文件夹；构建脚本同时生成安装包与包内文件的校验信息。也可以直接运行解压后的脚本，无需安装 pip 包：

```sh
python pure-math-survey/scripts/survey.py --version --json
python pure-math-survey/scripts/validate_assets.py --json
python pure-math-survey/scripts/survey.py init --output my-topic --topic my-topic --scope my-scope.md --json
python pure-math-survey/scripts/survey.py kb validate my-topic --json
```

先在 `my-scope.md` 中写明真实的数学范围。初始化只建立知识项目，不生成文章。原生项目使用 `project.json` 和 2.0.0 数据格式。编译需要 pdfLaTeX、BibTeX 以及 `math-review.sty` 加载的宏包；实际页数检查和页面渲染使用 Poppler 的 `pdfinfo`、`pdftoppm`。环境提供时，`bibtex.original`／`bibtex8` 可作为有记录的替代程序。依赖细节见[排版与构建](references/layout-and-build.md)。确定性的核心工具不需要网络；文献发现由代理使用其可用工具完成，并如实记录。

## 最小输入输出示例

创建 UTF-8 编码的 `my-scope.md`：

```markdown
# Scope
Study strict positivity of finite real symmetric block matrices with an invertible
leading block. Exclude the general singular-pivot theorem.
```

再执行“安装与运行”中的初始化与验证命令。预期得到 `my-topic/` 知识项目，其中包含 `project.json`、`scope.md` 和 `knowledge/` 目录。初始化不会生成文章或 PDF；阅读文献、编写并审阅知识节点属于后续步骤。

## 四种写作模式与统一的知识依据

`minimal` 给出精确的核心答案、必要机制和关键边界；`thematic` 组织相关结论及有依据的关系；`lecture` 展开指定的前置知识、计算和证明；`paper` 要求获授权的原创贡献、最接近前人成果的实际阅读和完整证明，默认保持 `DRAFT_UNVERIFIED`。请求成文时默认采用 **minimal + integrated**。仅建库或更新知识不会隐含生成文章。PDF 是交付格式，不是第五种模式。Part I–IV 是可以交叠的基础、结果、方法和边界视角，不要求分成多卷。只有用户明确设置的 `max_pages` 才是硬性页数上限。

只在知识节点中编辑规范数学陈述，用 `kb freeze` 固定快照，再以 `output plan ... --snapshot KB-...` 创建明确的文章计划。细化读者、选材和证明步骤，在正式准备前检查相应范围的就绪状态。`output prepare` 生成快照中的精确片段与待写作框架，不会凭空完成文章。`--draft` 允许准备尚未核查的内部草稿，但不允许正式发布。重新准备会保留已写的 `main.tex`；采用不同快照前应重新审阅。

`kb diff` 报告新增、修改、删除的知识及受影响的输出。旧快照和输出保持可重建。校验读取实际文件，不继承缓存中的 PASS 标签。渲染只生成图片，不代表已完成视觉审阅；接受视觉证据前必须阅读每一页。

## 安装包内容

安装 ZIP 包含支持的运行资源，包括 `survey_core` 模块、写作模式、参考材料与重建工具。仓库测试、开发日志和用户文稿的编辑记录不进入安装包。工作流程见 [SKILL.md](SKILL.md)，数据格式和命令见[文件约定](references/contracts.md)。当前知识采用 schema 2.0.0，新计划／审阅采用 2.2.0；历史计划／审阅可以按其记录政策读取，但不能授权当前政策下的正式打包。

软件测试不构成独立审阅，也不能保证一般的数学正确性。独立数学审阅、真实读者反馈及真正原创 Paper 的原创性与完整证明质量仍未验证；软件正式发布不改变这些限制。验收证据记录实际执行的、范围明确的作者重读及其限制；来源哈希、实际编译和 PDF 页面检查是不同的证据。

## 许可证

技能指令、脚本、模板和说明文档采用 [MIT 许可证](LICENSE)，版权声明为 `Copyright (c) 2026 ZhiyaoXiongMath`。

随包提供的 `assets/reference-samples/dhym-balanced/` 数学参考材料，包括 TeX、PDF、参考文献及用户提供的样式，不在本次 MIT 授权范围内。仓库中的独立 `examples/` 目录同样排除在外。本次不为这些材料授予额外复用许可，也不改变第三方已有权利。

## r3 日常使用职责与证据

日常使用 main 固定完整请求、最新纠正、读者可执行操作与项目 revision，负责唯一集成和实物验收。
按需要使用真实可用工具向隔离候选任务委派来源、知识、审阅和 PDF 工作，记录实际任务 ID、输入、
状态和接收。拒收过期 revision；数学冲突回来源；接替前冻结旧写者；迟到结果只保留候选。
无委派能力时串行执行相同职责并如实说明。保存文件／补丁、任务实际回答、哈希和未完成项，
使停止／恢复不依赖聊天可读。这不同于开发阶段 main，也不是常驻调度平台。
knowledge-only 不新增文章，不调用文章 prepare。

KB 具有 overview、问题路线、节点三个阅读尺度，共用单一 canonical。快路线显示输入、关键操作
和决定条件，链接到具体慢层小节；慢层兑现承诺推导、精确导入与本次应用，并反向标明路线和消费处。
文章中形成的可复用解释回 live KB，经审阅和新 snapshot 后采用。按本次用法区分 Assumed／
Refreshable／Bridge-required。先从目标与读者逆推义务，再检查作者清单；保存快层重建、慢层实作、
条件改变的实际回答、失败和修复。保留所有明确主题分支；七分支回归不是每个用户的强制课程。

四模式普通解释正文主动以正常字号页宽下约 2–3 个实际排版行为目标。长块须改进或记录具体位置、
保留理由、曾考虑的改法、最终 PDF 哈希和复看范围；禁止 TeX 源码计行、装饰公式、强制换行、缩字体
或删条件。实际检查所有页面。五 view 改变真实读者任务，不改变模式职责或数学事实。
保留 F1 正文定位、F2 视角／设计、F3 比较与前人 primary 支持、F4 草稿／设计安全。
Paper 默认显著 DRAFT_UNVERIFIED。

软件仍为 2.1.0，KB／snapshot schema 2.0.0，output／review schema 2.2.0；r3 政策为
`four-modes-2026-10-12-r3`，与 rc2 分开。旧字节和 accepted 保持原样；recorded 读取不授权当前
正式打包。正式 tag／Release 继续暂停。规范文字不等于验收完成；实际内容、PDF、独立安装和关键
复核须针对固定候选留证。分开报告程序、数学、讲解任务、PDF 检查和真实读者反馈；团队／AI 审阅
不是外部同行或学生实测。无实际原创输入与相应审阅，真实 Paper 原创性及完整研究证明质量仍为
NOT VERIFIED。
