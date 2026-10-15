# Pure Math Survey 2.1.0

**简体中文** | [English](README.md)

先构建并审阅有原始来源支持的数学知识，再从不可变快照写出用户明确要求的英文综述、讲义或研究草稿。只建知识时止于知识和证据，不生成文章或 PDF。

软件 **2.1.0**；知识／快照 schema **2.0.0**；输出／政策审阅 schema **2.2.0**；当前成文政策 **four-modes-2026-10-15-r5**。当前安装仅支持 r4。明确旧／未知 policy 或不支持的输入给出清楚诊断，原文件保持不变；不提供 recorded 放行、历史模板选择或迁移服务。

## 直接在调用对话启动

补充准确主题、全部范围、每项所需产物的读者前提与承诺证明深度、项目路径、允许的安装／原始来源路径或 URL 及实际读写边界，由用户实际发送：

> 使用 $pure-math-survey 完成我指定的数学任务。本对话作为控制台；我授权本控制台在本项目内新建必要的 Codex 工作对话，统一使用 gpt-6-astra / ultra，负责文献阅读、成对快慢知识、写作和非作者审阅。我授权本控制台向这些工作对话发送任务、继续、修订和停止指令；请读取结果，只交付我要求的产物。

调用对话沿用当前模型与推理设置。控制台使用实际 create_thread 参数派发全部 Astra/ultra 工作对话，提示词中的模型名字不构成配置证据。授权来自人类原话或可定位可信来源；宿主要求明确新对话授权而当前缺少时只补一次，并继续独立的范围准备；已有有效授权不反复确认。worker 提示带 role=worker，禁止递归派发。

需要宿主支持新建、读取、列举、等待、发送任务工具及 gpt-6-astra / ultra。缺少授权、工具或模型时明确报告阻碍，不用控制台自写全文、串行扮演或低档代理冒充等价自动流程。控制台单写 canonical live KB，工作对话各写自己的候选／输出／审阅目录；关键验收必须由非作者承担。私人台账记录固定输入、真实 ID、pending／未知创建、去重、恢复与停止边界。参见[委派规则](references/dispatch.md)和[启动提示](references/user-start.md)。

实际派发须携带人类／父任务的准确读取边界，以及允许的安装资源、原始来源、固定快照输入和独占输出／证据路径；worker 在加载辅助流程前遵守这些边界。禁止全局同名 skill 不等于禁止所有全局 skill；明确的全局辅助 skill 禁令也包括 PDF skill。安装内的原生构建／页面检查说明已提供来源渲染、实际逐页查看及重建记录做法，无需越界加载全局辅助 skill。缺少允许的能力时报告阻碍，不跳过必要核查。

## 四模式共享一个知识权威

| 模式 | 开篇与后续正文 |
|---|---|
| **minimal**（默认） | 无摘要；严格 Main Results／Key Mathematical Ingredients／Connecting the Ingredients 三节；第一节完整给出全部主结果，第二节建立实际消费的可调用支点，第三节执行决定性连接。 |
| thematic | 无摘要；第一节准确提出问题、代表性完整主结果与比较条件；后续分析真实困难、方法机制并作有依据的综合。 |
| lecture | 无摘要；第一节给出学习目标、完整核心目标定理及忠实路线；后续按教学顺序兑现构造、计算、证明和首次应用。 |
| paper | 有简洁摘要；Introduction 比较最近已有工作、具体困难、完整新结果、准确差别与证明路线；后续完成严格证明。默认显著 DRAFT_UNVERIFIED。 |

只有 Minimal 固定主体节数、标题与顺序；必要子节和 References 不算第四数学主体节。Thematic、Lecture 不能保留改名的节前摘要。已知结果 Paper 草稿准确归属，不据此宣称原创或取得原创研究发布许可。

默认所请求文章为 **minimal + integrated**；只写要求的模式和数量。五种 view（integrated／foundations／results／methods／boundaries）改变侧重点，不改变事实或模式责任。快层说明目标、对象、输入、操作、输出、用途和条件；对应慢层完成承诺推导、假设核查及精确外部接口。prepare 只生成固定材料与未完成 TeX 脚手架，作者仍需实际成文。新可复用解释或数学修订回流 live KB，审阅后冻结新快照。参见[模式契约](references/editions.md)和[知识到 TeX／PDF](references/knowledge-to-manuscript.md)。

所有所需产物的具体读者能力和精确 proof promises 应在最终知识审阅前形成。非作者先重建责任，再真实逐项核查承诺步骤，形成 exact scope.proof_steps、实际 findings／定位与缺口；新 live evidence 之后冻结新快照，计划显式采用再 prepare。不得复制标签造 accepted、编辑旧 snapshot 或刷新旧 accepted 哈希。现有任务的集中反馈／复核与停止额度约束全部流程，不新增修订通道，也不成为所有用户的永久轮次上限。

## 安装与检查

把完整 pure-math-survey 文件夹复制到宿主 skill 目录，或从源码构建本地安装包；也可直接运行脚本：

```sh
python scripts/package_release.py --output ../pure-math-survey-2.1.0.zip
python scripts/survey.py --version --json
python scripts/validate_assets.py --json
python scripts/survey.py init --output my-topic --topic my-topic --scope my-scope.md --json
```

解压后使用完整目录，核对成员校验和与 ZIP SHA-256。初始化读取真实 UTF-8 范围文件，仅产生空的未验证知识项目。确定性 CLI 使用 Python 3.10+ 标准库；PDF 需要 pdfLaTeX、BibTeX 与 math-review.sty 所用包，页数／渲染需要 Poppler pdfinfo／pdftoppm。来源检索由助手工具执行；CLI 不派发对话，也不常驻调度。

阅读[SKILL](SKILL.md)、[字段与命令](references/contracts.md)、[构建要求](references/layout-and-build.md)和[验证边界](references/validation.md)。reprepare 保留作者正文、outline 与样式；不得编辑快照、materials 或 generated 权威片段。实际打开全部最终 PDF 页面，记录具体观察、修复、当前身份和普通解释文字约 2–3 个正常排版行目标的合理例外；渲染不等于检查。

正式文章打包须通过当前政策 RELEASABLE。未验证 Paper 可交付显著草稿 TeX／预览 PDF，正式打包须拒绝。旧政策运行验证不受支持；不得改号或迁移旧 accepted。软件安装 ZIP、数学文章包和软件 Release 是不同对象；结构测试、哈希、AI 非作者审阅、编译均不证明真值、原创性、外部同行评审或学生学习效果，应分别报告实际范围与限制。

## 范例与许可

旧生成文章、知识项目及 reference-sample 集合已从当前树和安装资源移除；Git 历史／私人备份保留原身份，不能导入作为答案或新验收。当前公开范例须从原始来源新生成并真正独立验收；本说明不宣称这些测试已运行。

指令、脚本、模板和文档遵循[MIT License](LICENSE)，Copyright (c) 2026 ZhiyaoXiongMath。数学范例及第三方原文保留各自权利；可读取不等于可再分发。私人授权／调度记录与受限原文不进入公开包。


`review validate` 批量报告证据缺项，`review accept` 暂存校验候选最终字节并在失败时回滚；随后仍须 freeze 与显式采用。模板覆盖适用 canonical 依赖且保持 pending。见[审阅与接收](references/proofs-and-boundaries.md#review-handoff-and-candidate-acceptance)。

原文访问、实际阅读范围、可验证字节与再分发权限独立据实报告；私有或未授权原文字节不能进入公开项目快照。知识 READY 与 Paper 正式研究资格分别设门槛。见[来源证据](references/research-and-evidence.md)。
