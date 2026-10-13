# Pure Math Survey — R4 开发预览

**简体中文** | [English](README.en.md)

为需要整理数学文献、维护可追溯知识库，并撰写英文综述、讲义或研究草稿的作者提供工作流程：先真实阅读来源，构建可理解的快慢知识，再从审阅后的固定快照写出所请求的稿件。只建知识时不生成文章。

**本次为 `v2.1.0-r4-preview.1` 预发布，软件版本仍为 2.1.0。** 工程检查已通过，第二轮真实数学端到端测试仍在运行，不能据此称为稳定版或五项数学全部达标。详见[导师进度与验证范围](docs/r4/development-status.md)。

## 安装完整 skill

1. 打开 [GitHub 预发布页](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0-r4-preview.1)，下载附件 `pure-math-survey-2.1.0.zip` 和 `pure-math-survey-2.1.0.zip.sha256`。安装 ZIP 与 GitHub 自动生成的源码 ZIP 是不同文件。
2. 核对下载文件的 SHA-256，解压，把完整 `pure-math-survey/` 文件夹复制到宿主的用户 skill 目录。例如 Codex 的默认用户目录为 `~/.codex/skills/`；若宿主配置了其他目录，以该配置为准。保留 SKILL、references、scripts 和 assets，不能只复制 SKILL.md。
3. 在能够访问你的项目和来源文件的新聊天中引用 `$pure-math-survey`。调用聊天保留当前模型；运行控制台创建的文献、知识、写作及审阅工作聊天统一使用实际 `gpt-6-astra / ultra` 参数。

需要宿主支持新建、读取、等待和发送任务给 Codex 工作聊天，并可用 Astra/ultra。确定性脚本需要 Python 3.10+ 标准库；生成 PDF 还需 pdfLaTeX、BibTeX、样式所用 TeX 包和 Poppler 的 pdfinfo/pdftoppm。缺少能力时控制台会报告具体阻碍，不以串行角色扮演冒充实际派发。

正常安装和使用无需创建符号链接，也不需要本次工程测试使用的 UAC 提权步骤；该弹窗用于测试实际符号链接的安全拒绝，系统权限设置没有被修改。[构建与页面检查要求](skills/pure-math-survey/references/layout-and-build.md)提供安装内的原生流程。

## 第一次使用：先建立知识库

把下面提示中的目录改成自己的可写项目路径；附上已有来源，或允许控制台查找原始来源。明确哪些目录可读、哪些不可读：

```text
使用 $pure-math-survey，在 work/matrix-positivity 建立数学知识库。
主题：有限维实对称分块矩阵的正定性；要求首块可逆，排除奇异首块变体。
读者：掌握本科线性代数。请解释对象、全部条件、两向论证、实际使用的构造及边界。
先只构建和审阅知识，不生成文章或 PDF。查找并真实阅读支持这些结论的原始来源。
允许读取完整已安装 skill、我提供的来源和本项目；仅在本项目及其独占工作目录写入。
其他私人目录不在授权读取范围内；如需更多输入，请说明具体缺口。
本聊天作为控制台。我授权在本项目内新建必要的 Codex 工作聊天，全部使用
 gpt-6-astra / ultra，负责文献、成对快慢知识、写作和非作者审阅；授权本控制台
向这些聊天发送任务、继续、修订和停止指令，并读取结果交付。
```

这是用户实际发送的授权，文档中的提示本身不产生权限。已有同范围的有效授权会继续使用；只在宿主确有要求且缺少授权时补一次具体授权。控制台把准确的安装、来源和输出路径边界传给每个 worker，worker 不递归创建聊天。禁止全局同名 skill 与禁止所有全局辅助 skill 的范围不同，实际限制必须被遵守。

控制台组织来源阅读、知识候选及非作者审阅，核对返回的真实文件和证据，再单写整合权威知识。快层说明目标、输入、关键操作、输出、用途和条件；对应慢层完成承诺的推导与精确外部定理接口。你得到可编辑知识节点、项目综览、来源／审阅记录和明确的缺口；冻结快照只固定字节，不自动证明数学就绪。

## 再请求一份稿件

知识审阅后，可在同一聊天继续：

```text
请基于这个知识项目写一份英文 Minimal 综述，view=integrated，范围保持不变。
读者仍掌握本科线性代数；完整陈述主结果，展示决定性的两向论证和条件用途。
不要增加其他模式，也不要把已知结论称为原创。请交付可编辑 TeX 和可读 PDF；
只有实际通过当前交付检查时才提供可重建文章包，否则说明草稿状态或阻碍。
沿用本项目的工作聊天授权和读写边界。
```

控制台先协调这份稿件的具体读者与证明承诺，取得相应的真实非作者知识核查，把新证据纳入新快照，再由写作者完成正文。`prepare` 只生成固定材料和未完成脚手架；它不会自动写出合格证明。完成稿件还需要实际数学／成文审阅、TeX 构建、全部 PDF 页面观察及适用的解包重建。

正常完成的文章项目含 `outputs/ID/plan.json`、`outline.md`、`manuscript/main.tex`、固定 `generated/` 和 `materials/`、`build/main.pdf` 及对应审阅／构建证据；正式许可通过时另有可重建 ZIP。这是交付结构说明，不表示本 README 的初始化示例已生成这些文件。知识-only 项目没有隐含稿件。

要更新知识，说明新来源、纠正或新增问题，要求先核查并回流 live KB，再冻结新快照；旧快照和已交付文件保持不变。要再写 Lecture 或其他输出，给出新的读者／证明深度和数量，控制台取得相应证据并创建新输出，不覆盖旧稿。你无需手工填写审阅 JSON；这些记录由实际工作者完成并由控制台核对。未执行的工作不能写成 accepted。

## 选择模式

| 模式 | 适合什么任务 | 必须形成的正文 |
|---|---|---|
| **minimal**（默认） | 快速理解完整结果与决定性理由 | 无摘要；严格 Main Results、Key Mathematical Ingredients、Connecting the Ingredients 三节；全部完整主结果在第一节。 |
| thematic | 理解专题中的真实方法及可比结论 | 无摘要；首节准确提出问题与代表性完整结果，后续分析困难、方法机制与有依据的综合。 |
| lecture | 学会复现构造、计算和证明 | 无摘要；首节给出完整核心目标定理及忠实路线，后续按声明的读者前提兑现推导与首次应用。 |
| paper | 整理研究贡献或内部研究草稿 | 保留简洁摘要和完整 Introduction；准确比较已有工作并完成证明。默认显著 DRAFT_UNVERIFIED。 |

只有 Minimal 固定主体节数／标题。默认所请求稿件为 minimal + integrated；只生成所需模式和数量。五种 view：integrated、foundations、results、methods、boundaries，改变解释重点而不改变事实。四模式共享一个 canonical 数学权威和不可变快照。

当前流程保留 F1–F4：实际正文中的证明／主结果定位、view 与设计一致性、真实比较及原始来源支持、未完成设计／草稿安全；同时要求义务覆盖、快路线重建、慢步骤复现和条件改变核查。普通解释文字主动以约 2–3 个正常排版行为目标，必要长陈述有具体理由，不能删假设或缩字凑行数。详见[模式契约](skills/pure-math-survey/references/editions.md)与[知识到稿件](skills/pure-math-survey/references/knowledge-to-manuscript.md)。

已知结果的正确证明不等于原创贡献。未经核实的 Paper 可以提供显著草稿及预览 PDF，正式研究 package 必须拒绝；编译成功、AI 非作者审阅或软件测试不证明原创性、外部同行评审或真实学生学习效果。

## 可选：工程 CLI 的真实初始化示例

聊天是日常入口，CLI 用于文件操作和工程检查，不负责派发聊天。下面是实际执行过的初始化与结构验证；在包含解压后 `pure-math-survey/` 的目录中，新建 UTF-8 `scope-input.md`：

```markdown
# Scope

Build a source-grounded knowledge project on positivity of finite real symmetric block matrices with an invertible leading block. Exclude singular-pivot variants. Readers know undergraduate linear algebra. This initialization demonstration does not request a manuscript or certify any theorem.
```

在可写的演示目录运行：

```sh
python pure-math-survey/scripts/survey.py --version --json
python pure-math-survey/scripts/survey.py init --output my-topic --topic matrix-positivity --scope scope-input.md --json
python pure-math-survey/scripts/survey.py kb validate my-topic --json
```

源码检出时，脚本相对路径为 `skills/pure-math-survey/scripts/survey.py`。本次实际调用同一版本 CLI，得到：

| 调用 | 实际结果 |
|---|---|
| --version | version=2.1.0；policy=four-modes-2026-10-13-r4；仅支持输出 schema 2.2.0 / 当前 r4。 |
| init | INITIALIZED；review_status=pending；outputs=[]。 |
| kb validate | VALID；node_count=0；source_count=0；警告 SEMANTIC_NOT_CERTIFIED。 |

生成 `my-topic/project.json`、`scope.md` 和 `knowledge/{overview.md,conventions.tex,discovery.md,coverage.json}`。这是空的未验证知识项目，没有审阅通过、文章、PDF 或文章包；结构有效不等于数学就绪。真实来源阅读、知识写作及审阅是后续步骤，不能用这项小演示冒充完整数学端到端验收。

## 当前验证、支持范围与许可

当前 Windows 独立安装的 **280/280 工程测试通过、0 skipped**；69 个安装成员／68 个运行资源的身份一致，3 页中性 TeX 构建检查通过。它们是工程与样式证据，不是五项数学全部通过的范例。第一轮整项未达标，已有部分范围内的数学／PDF 证据；当前第 2 轮继续完成。用户已要求不启动第 3 轮；若第 2 轮不达标就停止并报告，不继续运行代码修复。Schur Paper 本轮非作者知识审阅已完成、无需返修，但普通 kb readiness --plan 因已知结果缺少原创贡献而阻断；仍将完成真实 DRAFT_UNVERIFIED 预览、正式交付拒绝与三种变体检查。此项正在独立核实，最终 E05 尚未验收；这不是已解决结论，也不概括为所有 Paper 都有确定缺陷。详情见[开发进度](docs/r4/development-status.md)。

软件版本为 2.1.0，知识／快照 schema 为 2.0.0，输出／政策审阅 schema 为 2.2.0，当前政策为 four-modes-2026-10-13-r4。仅支持当前 r4；明确旧／未知契约会被拒绝且原文件不改，不提供 recorded 放行、历史模板选择或迁移服务。reprepare 保留作者正文／outline／样式，旧快照和证据不能通过手改哈希升级为 accepted。日常使用没有本次开发测试的固定三轮上限。

阅读[完整入口](skills/pure-math-survey/SKILL.md)、[命令与字段](skills/pure-math-survey/references/contracts.md)、[验证边界](skills/pure-math-survey/references/validation.md)。软件安装 ZIP、数学文章包和 GitHub 软件 Release 是不同对象。旧生成范例已移出当前公开集合；失败稿不作为通过范例展示。

指令、脚本、模板和文档遵循 [MIT License](LICENSE)，Copyright (c) 2026 ZhiyaoXiongMath。数学材料及第三方原文保留各自权利；可读取不等于可再分发。公开包不包含私人授权台账或受限原文。
