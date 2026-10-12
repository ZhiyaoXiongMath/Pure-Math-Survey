# Pure Math Survey

> **软件版本 2.1.0 发布准备；tag 与 GitHub Release 尚未发布。** 当前可复制仓库中的完整技能目录，或从源码构建本地安装包。四模式契约见[成文模式](skills/pure-math-survey/references/editions.md)。
> r3 Minimal 默认采用局部问题单元，就近组织完整结果、必要支点、关键连接与首次使用；旧 r2/rc1、rc2 保留严格三节政策；Thematic 核查路线比较；Lecture 兑现逐步证明；Paper 需授权原创贡献、最接近前人成果核查与闭合证明，默认只生成内部草稿。软件校验不保证数学正确、原创性或读者理解。
> 知识 schema 为 2.0.0，新输出计划与新版政策审阅为 2.2.0；旧快照、正文和审阅不被静默迁移，历史 accepted 不构成新版政策验收。


**简体中文** | [English](README.en.md)

**Pure Math Survey 2.1.0** 面向维护数学知识和撰写文章的作者：先建立有原始文献依据的知识库，再从固定的知识快照撰写所需的英文综述、讲义或研究论文草稿。

知识项目保存明确的问题、定义、结论、证明机制、结果之间的关系、例子、适用边界及对应的文献证据。它可以独立维护，不必生成文章。作者或代理负责数学阅读与写作；工具负责检查文件约定、固定输入、证据关联和实际编译。

| 写作模式 | 适用需求 |
|---|---|
| **minimal**（默认） | 快速掌握精确答案、核心机制和关键边界。 |
| thematic | 围绕一个问题理解相关结果及证明路线。 |
| lecture | 学习前置知识、计算步骤和明确要求展开的证明。 |
| paper | 核查获授权的原创贡献、最接近前人成果与完整证明；默认仅生成未验证内部草稿。 |

请求生成文章时，默认采用 **minimal + integrated**，只生成用户要求的模式。基础、结果、方法和边界是可以交叠的知识视角，不要求拆成若干卷；只有用户明确指定的页数上限才是硬性长度约束。

## 安装

当前请将本仓库中完整的 [skills/pure-math-survey](skills/pure-math-survey/) 文件夹复制到宿主应用的 skills 目录。也可以在仓库根目录构建本地安装包：

```sh
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0.zip
```

解压后，将其中完整的 `pure-math-survey` 文件夹放入宿主应用的 skills 目录。构建脚本同时生成包内文件清单与 ZIP 的 SHA-256 校验文件。`v2.1.0` tag 和 GitHub Release 尚未发布，目前没有该版本的正式下载附件。下方示例保存在仓库中，无需单独下载示例即可使用 skill。
本版本的软件版本为 2.1.0；知识与快照 schema 为 2.0.0，新计划及新版政策审阅 schema 为 2.2.0。旧软件不能读取新计划；旧成果按显式历史政策读取，不自动迁移。

## 使用

```text
使用 $pure-math-survey，为[精确主题]建立知识库，暂时不要写文章。
```

```text
使用 $pure-math-survey，基于已经审阅的知识项目，为[读者群体]撰写一篇关于[主题]的 minimal 英文综述。
```

```text
使用 $pure-math-survey，从这个知识快照撰写英文讲义，完整展开[指定步骤]的证明。
```

详细说明见[工作流程](skills/pure-math-survey/SKILL.md)、[文件约定与命令](skills/pure-math-survey/references/contracts.md)和[验证边界](skills/pure-math-survey/references/validation.md)。
写作中发现的新结论应先回到知识项目中审阅，再形成新快照。生成的陈述和已有写作材料都要与快照核对。作者自查与独立审阅分别记录；编译成功和文件校验不能证明数学正确。

## 示例

### dHYM：写作与排版参考

这份六页的 balanced dHYM 综述由作者经过多轮专门润色，是主要的成文与排版参考。它从精确的可解性结论进入证明机制，再就地引入稳定性定义，并给出明确的等号边界例子。它的页数、提纲和结论数量不构成其他综述的要求。

- [阅读 PDF](examples/dhym-balanced/dhym-survey-revised.pdf)
- [独立 TeX 源文件](examples/dhym-balanced/dhym-survey-revised.tex)
- [如何使用这份写作参考](skills/pure-math-survey/assets/reference-samples/dhym-balanced/README.md)

上述示例目录只有 `.tex` 和 `.pdf` 两个文件。TeX 已包含所需的自定义样式和参考文献，数学正文未改变；PDF 保留作者提供的原文件。

### Schur 补：知识库到文章的流程示例

[下载 Schur 补示例](examples/schur-complement/pure-math-survey-2.0.4-schur-example.zip)。它包含九个知识节点、实际的文献阅读记录、固定的知识快照，以及两页 minimal 综述和三页 lecture 讲义，用于演示完整工作流程。记录的审阅方式是作者自查，未声称独立数学审阅；原始文献 PDF 不随示例分发。

### 输入输出示例：Schur 补

**输入：**

```text
使用 $pure-math-survey，研究有限维实对称分块矩阵在左上块可逆时的严格正定判据。
先建立知识库并审阅原始来源，再从同一快照分别写 minimal 英文综述和 lecture 英文讲义，
说明严格不等式的边界，并排除奇异主块的一般推广。
```

**对应输出：** 仓库中的 Schur 补示例提供 `project/` 知识项目、固定快照、
`pdf/schur-minimal.pdf`（两页）和 `pdf/schur-lecture.pdf`（三页），以及各自的 TeX 正文和审阅记录。
这些是该示例已经完成的成果；新主题需要实际阅读、写作与核查，初始化命令只建立项目，不会自动生成文章。

公开示例已移除旧构建历史、临时编译文件和原始命令日志；构建与渲染记录中的机器路径已脱敏，
数学内容、知识快照、PDF 和页面图片保持不变，并重新绑定了实际页面检查记录。

## 环境要求与开发

知识库命令行工具只使用 Python 3.10+ 标准库。生成 PDF 需要 pdfLaTeX、BibTeX 和 `math-review.sty` 加载的 TeX 宏包；页数检查和页面渲染使用 Poppler（`pdfinfo`、`pdftoppm`）。字体优先使用 STIX2，缺失时会报告改用 Latin Modern。可选的 PDF 图像比较工具还使用 PyMuPDF 和 Pillow。

```sh
python -m unittest discover -s tests -v
python skills/pure-math-survey/scripts/validate_assets.py --json
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.1.0.zip
python tools/verify_release.py ../pure-math-survey-2.1.0.zip --report ../pure-math-survey-2.1.0-verification.json
```

测试覆盖快照与材料完整性、范围明确的审阅、TeX 正文检查、历史记录和打包，并包含实际 TeX 编译。测试中人工构造的审阅记录仅用于软件测试。Linux CI 使用 Python 3.10 和 3.12；Windows 若无创建符号链接的权限，会明确跳过对应的一项测试。

参见[版本说明](CHANGELOG.md)。当前版本不包含服务器、向量数据库、研究调度器或 Research Studio 桥接功能；r3 要求知识库自身具有可用快路线和可复现慢解释，其实际质量须按任务验证。

## 许可证

本项目的 skill 指令、脚本、模板及说明文档采用 [MIT 许可证](LICENSE)，版权声明为 `Copyright (c) 2026 ZhiyaoXiongMath`。

数学示例材料单独保留：`examples/` 和 `skills/pure-math-survey/assets/reference-samples/dhym-balanced/` 下的内容不在本次 MIT 授权范围内，包含其中的 TeX、PDF、参考文献及示例项目。此次添加许可证不为这些材料授予额外的复用许可，也不改变第三方材料原有的权利。

## 验证证据与边界

[rc2 候选验证记录](docs/rc2/CANDIDATE.md)保留该阶段的实际结果和提交标识，不能替代正式版最终提交的验证。rc2 保留历史示例，新增 Simon–Maitre–Barrett–Süli 三篇原始论文的实际知识项目、配对的 methods／boundaries 文稿及新的 Schur 讲义。[可编辑项目](examples/rc2/projects/time-compactness/README.md)和有明确范围的作者／页面观察记录均予保留。历史候选材料中的已审阅 PDF、页面图片和构建记录只证明其对应字节；重新构建的 PDF 需要自己的视觉审阅。

另见[需求与实现对照](docs/vnext/requirements.md)、[实际验证及限制](docs/vnext/validation.md)和[七个已有基准文稿](examples/vnext/README.md)。这些历史记录中的六个已知数学样例曾编译并由作者重读；Paper 边界样例有意保持不可正式交付。独立数学审阅、真实读者反馈以及真正原创 Paper 的原创性与完整证明质量仍未验证。软件正式发布不改变这些限制。

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
