# PR-04 four-mode editorial development guide / 四模式成文开发指南

**Revision:** 2026-10-15 · **Scope:** PR-04 only · **Status:** repository-based *development specification*, not implemented or accepted code.

## Authority and safe provenance

This is the **complete public operational guide for PR-04**, reconstructed from the mathematical/editorial requirements of the user's 2026-10-13 r6.3 guide. It preserves those substantive editorial rules and acceptance boundaries; it deliberately excludes the old combined PR / Website Chat orchestration, already-completed r5 engineering work, private source files, case-specific formulae and local private paths.

Read together with [CONTRACT.md](CONTRACT.md) (stage authorization, least-complexity engineering, reviewer/merge rules) and [STATUS.md](STATUS.md) (dated stage handoff). The **current GitHub main/PR/CI** outranks the state snapshot. This document is sufficient to start PR-04 without asking for the private r6.3 attachment. Do not assert that the unredacted private artifact was copied to the public repository. If a requirement actually needs the private exemplar to resolve a contradiction, mark that specific test `NOT_EXECUTED` / `BLOCKED` rather than guessing or broadening scope.

Pre-PR-04 repository baseline verified: `main` = `2f5510c6813c1562a67e094f0bc70bacacdcce04` (merged [PR #6](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/pull/6)); actual stage work must re-fetch and validate the current remote. PR-01/02/03 were already merged and must not be redeveloped merely to satisfy this document.

**Baseline runtime (before PR-04):** software 2.1.0, KB/snapshot schema 2.0.0, output/review schema 2.2.0, editorial policy `four-modes-2026-10-13-r4`. These identities have different meanings. PR-04 needs one explicit new editorial-policy decision and synchronously updated producer/consumer/verifier/tests; changing the guide revision does **not** itself demand a software/schema migration.

**Single objective:** improve mathematical manuscript writing across Minimal / Thematic / Lecture / Paper using already-reviewed fast knowledge first, proof-dependent slow knowledge on demand, numbered statement environments **without descriptive optional titles**, and accurate nearby attribution of imported mathematics. Respect canonical KB, proof promises, source binding, and formal Paper eligibility. Preserve already-merged R5 security and integrity fixes.

**Out of scope:** rerun historical E01–E05 research tasks, claim correctness of original mathematical conjectures, reimplement sources/Review/atomic acceptance, create a new provenance database or “automatic citation truth” service, import private dHYM samples, merge main, tag/Release, or start another PR. The PR-04 Goal/Controller may write only a bounded feature branch and hand off an OPEN PR for human merge.

## Part A — Normative mathematical/editorial contract

## 1. 产品架构及不变性

核心原则不是“准备四种独立知识库”，而是

\[
\boxed{\text{统一 canonical KB} + \text{成对快慢知识} + \text{按模式选择证明责任} \longrightarrow \text{四种正文}}.
\]

- **单一知识权威**：形式定义、命题、来源、证明依赖和状态由现有节点／来源文件承担；overview、route 和文章是解释和选择，不是二次 canonical。
- **快、慢是阅读尺度，不是两棵强制目录树**。复用已存在的 overview、problem route、node fast/slow 小节及其互相定位。
- **快知识必须有数学实质**：对象、准确输入、待解问题、主结论、核心中间对象、决定性操作、输出、使用条件、路线终点和慢知识入口。不是“定理目录”或“证明见附录”。
- **慢知识兑现承诺**：具体构造、恒等式、系数与归一化、极限、紧性、正性、外部定理精确接口、假设使用和反例／边界。不能以“常规”掩盖决定性跳步。
- 保留现有 immutable snapshot、proof promises、plan-scoped 非作者审阅、F1–F4、四项理解责任和 Paper `DRAFT_UNVERIFIED` 门槛。
- **知识-only 独立完成**；用户只要求 KB 时不建立虚假文章计划。
- 不新增模式、view、第二套知识 schema、自动化数学正确性判断器或常驻控制面。

## 2. 四模式统一的 Fast-first 工作协议

### 2.1 分阶段阅读：开篇优先快知识，而不是降低数学精度

**S0 — 确定文章范围和输入身份（控制台／作者）**

读取真实用户目标、读者基线、已有 KB snapshot、selected principals、ordered quantifiers、proof promises 与用户明确的页数范围。文献与 canonicals 必须已经过相应的知识审核；若仍是 draft，先如实标注。**只围绕被选中的问题和结果工作**，不用全文阅读不相干知识分支。

**S1 — 充分阅读快知识，构造文章主线（四模式共用）**

阅读与目标有关的 project overview、question routes 和节点的 fast passage，梳理

\[
\text{Question}\longrightarrow\text{Main Claim}\longrightarrow\text{Mechanisms}\longrightarrow\text{Critical Conditions/Boundaries}.
\]

分别记下：目标结果（精确节点 ID）、必要概念及直接公式、路线之间的真实关系、不能略过的限制、可以由读者暂时当作黑箱的深层输入，以及**每条将首次正式呈现的结果的真实归属（自身推导／外部引用／改写或特例／来源未核实）**。利用现有 `outputs/ID/outline.md` 撰写**一份文章主线**，不要创建新的强制 `fast-plan.json` 或每次阅读必填审计表。

**S2 — 完成第一节的可读草稿（fast-first opening）**

第一节写作主要使用 S1 的快知识，而**不是先把所有慢证明从头读完**。同时，全部正式主结果使用固定 snapshot 的完整 canonical 字节，必要的局部定义、准确归属和状态不可仅凭快摘要改写。读者不必为了理解一个完整主结论跳到远处查假设或主要等式。

四模式都要在第一节将**借自文献的正式主结果与准确来源相邻呈现**；可以写在环境前的导语，也可以写在紧接环境后的正文。没有可靠出处或版本时，先回查来源，不因快知识可读便补写猜测性的作者、定理号和出版信息。

Paper 特别注意：Introduction 中的最近已有工作、贡献差异不能只靠未核实的快摘要。开篇可先依据**已审且有来源支持**的快知识组织，但凡涉及新颖性或细节有疑点，必须准确核对对应原文与慢知识后才能算最终开篇完成。此规则禁止“快知识已写出新颖性声明，所以可以跳过 prior-art 阅读”。

**S3 — 根据实际正文责任定位慢知识，展开论证**

从每个 principal 的证明依赖反向确认真正需要的 lemma、proposition、计算、外部输入，再按需打开**精确慢知识小节**。对准备提升为辅助结论的论述，先判明它是直接取自文献、改写已知结论、独立推出，还是多个来源的组合，并在对应陈述或证明附近准确引用。尽量复用已审核推导，不重新发散研究。若慢知识不存在、内容与快知识不符、条件缺失，回到 live KB 修订与非作者复核，冻结新 snapshot 后显式采用；不能直接在正文中编出未经审核的新数学。

**S4 — 按证明依赖组织辅助结论及正文**

使用第 3 节统一规范。先完整陈述需要的主结果（开篇例外），随后每个辅助 Lemma/Proposition 原则上在其**首次实际使用的证明之前**完成陈述与证明。将独立分支分开写，不把几条独立路线排成错误的单链。

**S5 — 检查闭合与交付**

针对固定候选进行数学义务核对、当前输出结构、正文／PDF 实读、必要的有限复核；与计划约定的深度一致。对正文引用的慢步骤要能找到真实 KB／source 接口，但不用引入新的阅读遍历日志或重复审核整个固定快照。普通写作移动引理或修标点不自动触发重新研究原始文献。

### 2.2 哪些情况必须回读慢知识？

强制按需回读的触发器：开篇精确条件和快速表述冲突；未知常数／归一化／量词；缺少支撑主结论的关键引理；正文承诺完整计算、逼近、极限或正性；要对两项结果比较假设、推出非平凡关系；要声明 Paper 原创差异／proof closure；第一轮数学复核发现具体缺口。

**不能仅用快知识完成的工作**：Lecture 承诺的逐步证明、Paper 的完整原创证明、Thematic 的非平凡跨路线比较、Minimal 的决定性连接。快知识负责“**先决定讲什么、为什么**”；慢知识负责“**真正证明或准确调用**”。

### 2.3 一次阅读不等于一份新增记录

在现有 outline（只读 frozen KB 的编辑性消费文件）中可自然写明“本次用到的快路线、回读的慢节和未覆盖内容”。这是一种有用的作者说明，不增加新 schema；正式完整性继续由已有计划、输入摘要、proof findings 和实际文章位置承担。

## 3. 全部四模式共同的写作规范

### 3.1 主结果完整、准确、优先展示

- 在第一节开篇明确当前问题、未知量、读者必要的数学对象与完整 principal claims；Minimal 全部主结果，其他模式的首节按照原模式合同至少包含完整核心／代表性主结果；Paper 首节包含全部选定 principal claims，并特别准确标示原创新结果的贡献状态。
- canonical 是唯一数学字节权威。按现有 `\input{../generated/statements/N-*.tex}` 导入，不复制粘贴另写一个精简、可能漏假设的替代定理。
- 引用原始文献中的 `Theorem 1.5` 属来源定位，不代表本稿定理排版必须出现相同编号。
- 不将任何已知定理写作未经验证的原创结果；不把来源支持不足的比较或陈述变为确定性结论。首次正式陈述采用的文献结论应在其前／后紧邻注出控制版本和定位；该要求不自动强加于真正独立推导的本文结论。

### 3.2 全部数学陈述环境：保留类型和编号，不加描述性名称

**适用范围**：四模式中实际使用的 `theorem`、`lemma`、`proposition`、`corollary`、`definition`、`example`、`problem`、`remark`、`conjecture`，以及任何承担相同数学陈述功能的自定义环境（如 `claim`、`observation`、`assumption`、`question`、`exercise`）。不能只修前三类而遗漏其它环境。

- 保留各环境现有的计数器配置、自动编号、稳定 `\label`／`\ref`／实际支持的 `\autoref`，以及正确的 PDF 交叉引用；原本编号的环境继续编号，不为此改成无编号版，也不引入手填定理号。对原本配置为无编号的普通排版环境，不凭空强制新增编号。
- **不加任何可选的描述性数学名称**：例如 `\begin{theorem}[Existence]`、`\begin{lemma}[Uniqueness]`、`\begin{proposition}[Reduction]`、`\begin{definition}[Phase]`、`\begin{example}[Counterexample]`、`\begin{problem}[Open question]` 等都不合规。通过题注宏或重定义命题头部偷偷达到同样效果，也不合规。
- 在**相邻普通正文**可以准确解释结果用途、术语或来源，诸如 “We use the Calabi--Yau theorem” 或 “The following is a reformulation of ...” 都合法；重要数学定义的名称可在 `\begin{definition}` 正文中给出，不当作环境的括号标题。
- `\begin{proof}[Proof of Theorem~\ref{thm:main}]`、`\begin{proof}[Proof of the sufficiency direction]` 是指明**被证明对象**的 proof 标题，不是上述数学陈述的描述性名称，继续允许。旧有 `theoremrecall` 的 “(recalled)” 是复述状态提示而非新的数学昵称；不要趁此破坏其合法回忆与链接。
- `equation`、`align`、`itemize`、`abstract`、图片／表格环境等不是此处的**数学陈述环境**，不得把其正常选项误报为禁用名称。
- 仅在**实际可达、可显示的正文数学陈述**中做可选标题的结构检测。必须避免注释、未执行条件分支、未调用宏、引用的原始文献正文等误报。若复杂自定义环境使静态判断不可靠，应标为需人工排版检查，不能用破坏 TeX 功能的粗糙正则宣称通过。

合法例子（正文内容须由真实 canonical／证明提供）：

```latex
\begin{theorem}\label{thm:main}
\input{../generated/statements/N-MAIN.tex}
\end{theorem}

\begin{lemma}\label{lem:bridge}
% 在这里写已经证实的辅助数学陈述
\end{lemma}

\begin{proposition}\label{prop:criterion}
% 在这里写已审核的判据
\end{proposition}

\begin{definition}\label{def:phase}
% 在正文内定义相位，不能用 [Phase] 作环境标题
\end{definition}

\begin{example}\label{ex:model}
% 在正文内展示实际计算；如改编自文献，前后必须说明来源
\end{example}

\begin{proof}[Proof of Theorem~\ref{thm:main}]
% 用已完成的 Lemma、Proposition 支撑定理证明
\end{proof}
```

以上为**排版形式示意**，包含占位注释，非已通过结构、数学或 LaTeX 编译的完整范例。正式回归须使用可编译的合成 canonical 和实质正文。现有 `math-review.sty` 对 Theorem/Lemma/Proposition 的共享计数器通常无须修改，禁止把“不加名称”误改成“不编号”。

### 3.3 文献归属与就近引用：所有模式共用

#### 3.3.1 哪些结论必须注明出处？

| 数学陈述或材料的实际来源 | 是否须在附近引用 | 如何准确表述 |
|---|---|---|
| **逐字或等价重述已有 Theorem、Lemma、Proposition、Corollary** | **必须**；首次正式陈述前或后紧邻 | 指出作者／资料与准确 locator，例如原文 Theorem 1.5；保留真实版本与假设，不能改成本文新结果 |
| **文献结果的特例、转写、归一化调整或等价 reformulation** | **必须** | 注明 “special case of”／“adapted from”／“reformulation of”，列出本稿与原文在变量、正则性、归一化、条件或范围的实际差别；必要换算由正文论证支撑 |
| **由两个或更多外部结果拼接推出的中间判据** | **必须引用各个实质输入**，而不一定给本文新命题贴一个单一出处 | 区分哪些前提各来自哪篇文献，以及本文实际完成的连接；不可将组合后的结论错误归给单篇文献 |
| **外部深定理被包装为本稿 Lemma/Proposition 的工具接口** | **必须**，通常紧邻工具陈述，并在使用处检验假设 | 说明本稿只调用哪一部分、来源版本／定理号、正则性与参数匹配，不能把 imported proof 写作本文证明 |
| **本稿根据已有 KB 独立证明的新辅助 Lemma/Proposition** | 陈述本身**不强制**虚构引用；证明若用非平凡外部输入则要在其应用处引用 | 可写 “We now establish ...”；如证明借鉴文献方法，应诚实标注 “following the argument of ...” |
| **经典但非初等的标准定理、引理、判据** | **应有可核实参考依据**，如原始著作或可靠权威教材 | 常规代数计算无需为凑引用虚构来源；对 Calabi–Yau 类核心 imported inputs 应交代归属和明确使用接口 |
| **借用／改编的 Example、Problem、Question、Exercise** | **必须**在例题首次介绍时注明源或改编关系 | 独立构造的例题不用硬加来源；若实际使用某文献的反例或计算，说明它是否改编及关键区别 |
| **从文献采纳的 Definition、Assumption、Conjecture、重要 Remark/Observation** | 需要准确注明首次提出或所用版本，特别是非标准定义、未决猜想与实质比较判断 | 不得把来源中的 conjecture 写成本文已证明 result；通行定义无需每次机械重复引用；纯作者意见需与文献事实分开 |
| **用户提供、尚未公开的原创手稿或本稿作者的工作** | 不虚构公开 `\cite`；使用已授权的作者归属／内部 provenance，且仍须做相应 prior-art 核查 | 保留 Draft 与证明状态；不得因为没有正式 DOI 就误判“没有来源”或伪造已经发表 |

**决定因素是来源与数学作用，不是环境类型。** 特别地，不能要求每个 Lemma、Definition、Example 自动生成一条 `\cite`，也不能以参考文献数量替代真实来源支持。

#### 3.3.2 引用在正文中的位置

- **Introduction 的 borrowed Theorem**：在定理前紧邻导语，或在定理后紧邻一两句说明，写出原作者、工作及精确 locator；与 dHYM 样稿第一节 Theorem 后的定位方式一致。不得只在文章开头一段泛泛罗列十篇文献或只在末尾参考文献表列标题。
- **Key Mathematical Ingredients、Lecture 中的外部 Lemma/Proposition**：紧邻该辅助结果的第一次陈述标明归属；若引用的是一条深层外部工具而本稿只证明其局部应用，要说明 imported/derived 的边界。以后通过 Lemma~\ref{...} 再次使用该**已正确引注的本稿陈述**时，一般无须机械重复引用；但新的外部输入或新版本仍应引用。
- **本稿独立证明的局部结论**：如果证明纯粹用已建立的前文事实，可不增加引文；如果证明调用外部文献的关键定理，在调用该定理的语句、等式或证明附近注明出处、所用条件和输出。
- **定义、例子、问题、猜想**：把来源说明放在首次引入／正式显示的邻近正文；若是独立形成而非借用，不能凭类别强加作者名。
- **Paper**：原创 Theorem 不应在引文位置被误标为别人的定理；Introduction 的 nearest prior results、已知辅助陈述及 proof imports 则依本节准确引用，prior-art 检查和原创证明仍独立要求。
- **请保留 canonical statement 的唯一字节来源**：出处写在外部的 `main.tex` 导语／尾注或现有来源记录，不为加引文随意改写固定生成的定理内容。若改变的是定理的数学条件而非归属说明，则回到 KB 审阅／新快照流程。

**有效的 TeX 排版示例：**

```latex
We recall the following result of Lin~\cite[Theorem~1.5]{lin-source}.
\begin{theorem}\label{thm:known}
\input{../generated/statements/N-KNOWN.tex}
\end{theorem}

\begin{proposition}\label{prop:tool}
% 已核对的工具完整陈述
\end{proposition}
This is the constant-coefficient formulation of
\cite[Theorem~4.1]{lin-source}; we spell out the normalization below.

\begin{lemma}\label{lem:local}
% 作者根据已建立工具推导的真正局部结论
\end{lemma}
\begin{proof}
Apply Proposition~\ref{prop:tool}; ...
\end{proof}
```

`lin-source`、`N-KNOWN` 和注释为**说明性占位符**；它们不是对真实 Lin 定理的重新核查或可直接编译范例。文中允许的来源定位如 `\cite[Theorem~1.5]{...}`、`\cite[Section~4]{...}`、`\cite[Chapter~II, Theorem~3]{...}` 应匹配真实 edition/preprint version、原文的陈述与本稿实际使用的条件。

#### 3.3.3 来源核查与审阅责任

1. 作者先从 source/KB 记录辨认每项正式陈述的来源类别，再于首次正式陈述处安排相邻出处，不从模型记忆杜撰 DOI、原文编号、年份或书籍页码。来源冲突、勘误、出版版本差异须按已有 r5 与 `references/research-and-evidence.md` 核实。
2. 若是变体或推论，非作者审核须判断**真正引用的外部命题是否支持这组假设、量词、常数、结论与归一化**，并定位本文补充的推导；引用正确不等于新推论已证。
3. 利用已有 `source`、`mathematical`、`coverage`、`output_semantic`、`contribution` 审阅及 `statement_context`／`attribution` 等**已有**反馈项记录不当归属。不要新增每个环境一张 provenance 表、每条引用一条审计任务或重复原文阅读；已通过且输入未改变的实际证据可以有依据地复用。
4. 自动化只适合检查存在性与可见性候选（如合成样例中的引文是否在正文、是否在非执行分支、TeX 编译/引用是否有效）。**不存在可以靠一条正则或 `\cite` 计数验证所有数学来源归属的算法**。对于未经数学阅读无法证实的归属，报告 `REVIEW_REQUIRED`，而不是假定有 `\cite` 就 PASS 或没有 `\cite` 就 FAIL。
5. dHYM 只读参照：开篇三个 Theorem 后分别注明来源，第二节 Lin 与 CLT Proposition 后注明来源；第二节“经典输入” Lemma 的具体归属也值得检查各输入的实际支持。**不要修改参考 ZIP 来伪造所有引文完整，更不能从范例组织良好推出每项引用均已独立核实。**

### 3.4 将重要论证提升为 Lemma 或 Proposition

重要辅助结果满足以下任一条件时，优先使用正式数学环境：

1. 独立而精确的输入／输出，可用于多个后续步骤；
2. 清除了主证明的关键障碍（如唯一性、正性、投影锥、关键积分恒等式）；
3. 承担外部深层定理的具体应用接口（含本问题的假设验证）；
4. 后文需要重复引用该结论。

推荐分工：Lemma 强调局部辅助推导或技术步骤；Proposition 强调相对独立、完整的中间判据或值得单列的应用接口。**它们与全部正式数学陈述环境一样，都只显示已有类型与编号，不加描述性名称。** 不存在基于字数／公式数的绝对分类标准；单步代数变形、不再使用的普通说明不必强制命题化。

**位置原则**：主结果可以在第一节提前展示而证明留在后文；辅助结果则原则上在**相应证明第一次调用之前、尽可能靠近调用点**。例如 dHYM 的唯一性引理应在 Theorem 1.3 对应的证明之前，不因“唯一性通常放最后”而推后。

建立依赖关系 `A -> B`（B 的证明需要 A），在每条证明分支中尽量给出拓扑上可读的顺序。正文教学顺序不等同于全局拓扑排序：可先简述问题和最终结论；被证明的辅助结论不应依赖尚未实际建立、又未标为外部输入的后文结果。确有数学理由时允许明确且可追踪的前向引用，但不是默认模式。

区分 **编辑性引理提取** 与 **新数学事实**：将已审核的推导按读者需要单列为 Lemma，不要求每次创造一个独立 canonical 节点；真正新增的非平凡数学命题、假设或关系必须回写 canonical KB、重新审核和冻结。不能在 `main.tex` 偷增第二数学权威。

### 3.5 证明自洽和引用维护

- 每个主结果必要对象、域、假设、量词和结论完整；重要 Lemma/Proposition 尽量局部自洽，允许已明确限定的本节背景。
- 每个证明明确区分存在性、唯一性、必要性、充分性以及参数／背景选择。变量替换时交代输出与下一步的接口。
- 重排后检查 `\label`、`\ref`、`\eqref`、Proof heading 和 above/below/following/previous 等方向词；引用原文定理号与本文定理号不可混淆。
- 让编号／链接由 LaTeX 机制管理；不在正文手写 Lemma 3.4 这种脆弱数字。Theorem 与 Lemma/Proposition 均使用有效的正常自动编号和 `\label`／`\ref`。

### 3.6 数学可读性优先于机械排版指标

- 标题直接说数学问题，不出现 `Minimal`、`KB`、`fast/slow` 等开发词。
- `itemize` 用于真正并列的假设、相互独立的判据、同级结论或多条证明路线；一条连续推理链保持自然行文，不能逐句拆成 bullet。
- 普通解释段落**倾向** 2–3 行正常 PDF 排版，但**不强制拆断连续的证明论证**。只有对象、证明方向或主要逻辑阶段发生明显变化才另起段。Minimal v2 对“少切碎段落”的要求优先于以行数为目标的机械拆段。
- 必要的数学公式应在读者需要时展示，紧邻定义符号及解释用途；不能为了满足“公式密度”插入装饰表达式，也不能为压页而缩字号、缩页边距或删条件。
- 确定的 `max_pages` 仍仅来源于用户对该篇文稿的显式约束。例如 dHYM 参照稿要求不超过 7 页，不能将 7 页固定为所有 Minimal 的隐含上限。
- 保留当前 PDF 全页真实查看与必要例外说明，但**一次集中审阅足够**；对未变页面有身份依据时复用既有观察。

## 4. 四种模式的具体构造协议

| 模式 | 第一节由快知识完成的工作 | 后续何处读取／使用慢知识 | 来源与归属重点 | 不应发生的退化 |
|---|---|---|---|---|
| **Minimal** | 严格 `Main Results`：简要问题 + 必需定义 + 所选**全部完整**主结果 + 极简证明路线；无摘要 | `Key Mathematical Ingredients` 建立实际消耗的 Lemma/Proposition，`Connecting the Ingredients` 逐条完成关键连接；常规部分压缩 | 文献主定理紧邻陈述标注作者与具体出处；借用的工具也要归属，本文局部引理不被迫虚构文献 | 只列结果、第三节只有流程箭头、证明关键一步“标准”黑箱 |
| **Thematic** | 无摘要；精确问题、共同对象、**代表性完整**主结果，说明真正可比的参数与路线结构 | 后续按真实困难／方法／条件比较定点读慢推导与原文，再做有依据的 synthesis | 比较的每条外部结果及真实归一化/范围都有来源；组合推论与文献直接命题分开 | 按论文逐篇介绍、把不等价条件强行说成等价、虚构第二方法 |
| **Lecture** | 无摘要；学习目标、读者前提、完整核心目标定理、为什么选择这条学习／证明路线；不提前细读并铺开全部技术证明 | 每个承诺的构造、计算、估计、拓扑极限和首个应用按教学顺序逐一消费慢知识 | 经典与外部深定理首次陈述有归属；借用的例子/题目注明来源；作者自己的教学推导不强制“凑引用” | 第一节就是漫长技术预备、后文只给“可见”但不可复算的公式、把深层输入伪装成已证明 |
| **Paper** | 简洁诚实摘要后，`Introduction` 用**已核实的**快知识定位最近结果、困难、贡献状态、完整 principal claims、准确差异和证明路线 | 深度消费慢知识以完成**每项**原创新结果证明；最近结果支持、源文与差异需要实际核查；缺口保留 Draft | 引用已有结论而不误标原创；原创主结果与 prior work 关系清楚，证明中的每项 imported input 就近引注 | 经典结果改名为原创、Introduction 许诺后文无法兑现、PDF 编译通过就宣称正式可发表 |
### 4.1 Minimal 的范例迁移界限

从有实质审阅的编辑样稿抽象出通用原则：所有 principal results 首节完整陈述；必要的外部定理和数学接口在后文明确陈述；关键局部引理放在其首次使用之前；同级条件可以用 `itemize`；连贯证明不机械切段；外部结果和工具就近注明实际出处。本稿独立推得的引理不强加引用。

**范例不是可复制的证明、数学事实或统一页数限制**。真实私人样稿/原文不能因为用于编辑参照而进入公开仓库、CI fixture、发布包或 PR 描述；是否实际审核过范例数学原文和 PDF 页面必须单独报告。

### 4.2 Thematic 的额外约束

比较时明确同一数学对象和背景下的条件序：维数、rank、相位、正性、正则性、归一化、量词。若比较本身需要新推导，则对应关系必须在已审核 KB 中明确成立；不能仅用 fast route 图谱判断含蕴。每项被比较的文献结论要有各自准确引用；组合推论不得只引用其中一个来源。辅助 Lemma/Proposition 按各方法局部依赖放置，而不是要求所有专题共享一套人工统一定理链。

### 4.3 Lecture 的额外约束

第一节要告诉读者“本讲最终能算出／证明什么、缺什么工具”。后续每个正式辅助结论在第一次实际使用前建立；关键证明须包含输入、具体计算、输出与条件，不以增多定理环境冒充教学。借用教材的 Example／Problem 和首次引入的深定理须注明来源。可教学性优先于全局依赖次序，前提是必要接口先解释清楚。整篇长度由承诺深度而非固定页数决定。

### 4.4 Paper 的额外约束

与 r5 的 Paper readiness 分层一致：`kb readiness` 判断知识与证明责任，`output prepare` 允许诚实且清楚标识的工作 Draft，正式研究 `release/package` 独立检查真实原创性、完备证明、最近结果差异和授权。没有原创不等于存在证明缺口；确实未闭合的证明仍不能被“Draft”按钮洗成 READY。第一节快知识可以帮助组织 Introduction，但**不是**对原创性的独立证明。已有结果、作者自身新定理、改写的外部命题和未核实猜想必须在附近文字中准确区分；对 borrowed results 和 proof imports 的引用不能藏在论文末尾统一罗列。



## Part B — Minimal source change map (not a list of compulsory edits)

Follow the actual installed repository paths, not assumed older layouts:

| Existing area | Necessary responsibility |
|---|---|
| `skills/pure-math-survey/SKILL.md` | Concise common author duties: S0–S5, result title rule, attribution, stop at missing mathematics. Link detailed references rather than repeating a full guide. |
| `references/knowledge-to-manuscript.md`, `editions.md`, `introduction.md` | Fast-first opening and slow-on-demand proof responsibilities, mode-specific first-section obligations. |
| `references/writing-style.md`, `proofs-and-boundaries.md`, `research-and-evidence.md`, `output-review.md` | Unnamed-but-numbered math environments; actual borrowed/adapted/local attributions; dependency ordering; reuse existing mathematical/source review fields and evidence. |
| Four `assets/templates/profile-*.tex` | Real author-facing cues for canonical and source-grounded main results; no hardcoded fake `\\cite` per environment. |
| `assets/templates/math-review.sty`, `scripts/survey_core/exports.py` | Preserve counters/labels, existing generated canonical input and theorem recall. Change only where a real incompatibility exists. |
| `scripts/survey_core/structure.py`, `tex.py` | Detect real supported visible optional math environment titles without misclassifying proof-target headings or inert/comments. If TeX macros prevent sound automatic detection, retain a bounded manual review; avoid an unsound general-purpose TeX parser. |
| `scripts/survey_core/profiles.py`, `plans.py`, `exposition.py` | Expose/validate policy obligations while keeping one canonical truth; preserve existing proof promises. |
| `tools/verify_release.py`, current editorial-policy tests, README | Update one actual editorial-policy identity consistently with the new authoring policy. Keep output/schema identity unchanged unless proven necessary by changed serialized structure. No pretend migration of past r4 reviews. |
| `tests/` | Focused positive/negative fixtures, representative attribution/proof dependency reviews and current-platform CI. |

**Engineering simplicity:** start with current references/templates; modify code only when a demonstrable rule or safety invariant cannot be enforced by those. Don't add new database entities, citation quotas, artificial fast-read telemetry, a second dependency DAG, an independent review service, a new “approval” layer or redundant version fields. A normative writing rule may require independent semantic review instead of brittle automatic heuristics.

## Part C — PR-04 acceptance cases

### 7.1 四模式 × 五 view

在现有固定小型合成 KB fixtures 上，测试 4×5 种组合：全部保留正确 canonical 输入和真实首节结构；Minimal 始终三节；Thematic／Lecture 后续节数可变；Paper 具有简洁诚实摘要与 Introduction。所有正常示例第一节有对应快路线的作者提示，后续不注入未被选择的慢证明。

反例至少包括：首节遗漏必要 principal、改写 canonical 关键假设、以正文总结代替完整定理、隐藏结果环境、没有对应使用的模板 Lemma、未解关键步骤冒充 complete、Paper 把 known 改 original、Draft 标记移除却冒充可发布。凡需语义判断的，用真实非作者发现解释，不把结构检测说成懂数学。

### 7.2 所有数学陈述环境：编号、无描述性名称和引用回归

- 用真实合成 canonical、可编译 TeX 验证 Theorem、Lemma、Proposition、Corollary、Definition、Example、Problem、Remark、Conjecture 以及**确实定义并使用**的自定义陈述环境不显示 `[Description]` 之类的名称；保留原本的自动编号、链接和 `\label`／`\ref` 机制。原本无需编号的普通非陈述环境不被强行改号。
- 正例至少覆盖前三类与其它三类不同类型的无标题环境；反例覆盖 `\begin{theorem}[Existence]`、`\begin{lemma}[Uniqueness]`、`\begin{proposition}[Reduction]`、`\begin{definition}[Phase]`、`\begin{example}[Counterexample]`、`\begin{problem}[Open question]`，以及通过自定义头部产生描述性名称的实际用例。
- 负例与边界：数学正文的可选描述名称应按政策被纠正／拒绝；`\begin{proof}[Proof of Theorem~\ref{...}]` 应正常工作；正文中“Calabi--Yau theorem”、原文引用里的 “Theorem 1.5” 合法；注释、不可达环境与外文献内容不误报。若当前检测器无法可靠识别复杂宏，应准确报告人工审阅范围，不为全过引入脆弱 TeX 正则。
- 编辑性依赖重排后，核对 `\ref`、Proof heading、above/below、页码和 PDF 链接；机械通过并不证明数学推导成立。
- 参考样稿的环境和证明结构只能迁移编辑原则，不得硬编码私人实例的编号、公式或计算。

### 7.3 文献归属与相邻引用的内容验收

- **正例 1**：Introduction 的 borrowed Theorem 在前／后相邻正文标注真实 source identity 与精确 locator；同样适用于来自文献的 Lemma、Proposition、Corollary。
- **正例 2**：经过特化／归一化修改的 Proposition 在正文明确写出原文来源、改变的条件及本文核对的数学步骤；多个来源组合得到的本稿结论分别标明各输入的出处。
- **正例 3**：独立推出的 Lemma 无强加的 `\cite`，但其证明中使用了外部定理时真实标明来源和假设检查；真正自行计算的 Example 不被迫有来源；借用的 Example/Problem/Conjecture 有正确归属。
- **负例**：文献 Theorem 只有 bibliography 没有相邻出处、把 某个预印本中的 result 错标为另一篇不同条件的发表定理、`\cite` 虽存在但对应文献不支持该假设／版本、组合结果只引用一个输入、把外部 imported 定理伪称本文从头证明、文献归属写在 `\begin{theorem}[Source]` 中、引用仅出现在注释／隐藏正文。
- **核查手段**：结构／编译测试只能检查局部候选和引用有效性；版本、数学归属、定理 locator、假设适用性由使用既有记录的实际非作者数学／输出审阅核实。不得为每个环境强制生成一条 citation，也不得将“非空 citation”当语义 PASS。

### 7.4 按需慢知识（非机器伪认证）

准备阶段可在 outline 明确所选 fast passages 及预计慢节，作者实际写正文时只读所需细节；数学审阅验证被承诺的慢推导是否真正重现。编译结果只能证明结构／环境／引用，不证明阅读先后或证明正确。**不新增** fast-read 打卡字段、强制原始阅读全文次数或审阅通过概率指标。
### Current CI and regression inheritance

Test the existing repository test suites on Linux (supported Python 3.10 and 3.12) and Windows Python 3.12, including paths/symlinks/Windows junctions, source/private distribution, snapshotted inputs, actual install-package validation, isolation, TeX smoke and report artifacts. If a mandatory test is skipped or a success artifact is missing, it must not be called `PASS`. Every test report must be tied to the **current PR head** (and identify the GitHub synthetic merge checkout separately).

Review compatibility with PR-01/02/03 without reopening their development scope. Tests for old accepted files must preserve byte identities, never silently “upgrade” their mathematical review disposition. A synthetic fixture is evidence of software behavior, not a real source-reading, mathematical proof or article page-review result.

### Completeness / Definition of Done

- Actual in-scope edits to existing references, templates and minimal code; no unrelated code churn.
- Four profiles' opening and proof duties embodied in author-facing instructions, correct sources and canonical results.
- All supported genuine statement environment kinds **numbered and without descriptive optional titles**; `\\label`/`\\ref` and PDF links work where supported. `\\begin{proof}[Proof of Theorem~\\ref{...}]` is allowed.
- Borrowed/modified/composite result attribution written in adjacent *visible prose* and reviewed for source/version/hypotheses as far as evidence actually permits. Locally proven lemmas do not need fabricated citations.
- Real positive/negative tests discriminate wrong from right; old PR-01–03 security checks not weakened.
- One explicit editorial-policy version decision with consistent producer, verifier, tests and docs, protecting old accepted/snapshots. Avoid spurious schema upgrades.
- One bounded independent non-author code/security/editorial review at stable HEAD; if `CHANGES_REQUESTED`, repair and re-review only modified/affected evidence. If reviewer capability is absent, report `REVIEW_PENDING` and stop; do not self-review.
- Report source/principal/proof/PDF checks honestly as `PASS`, `FAIL`, `NOT_APPLICABLE`, `NOT_EXECUTED`, `BLOCKED` or `REVIEW_REQUIRED` as appropriate. CI PASS does not imply formal Paper Release or scientific originality.
- Deliver an **OPEN, unmerged PR** with its base/head SHA, actual jobs/artifact links and root findings, then **STOP**. Only the user may merge/tag/release. Update [STATUS.md](STATUS.md) once from verified live facts, not on every CI retry; do not create another commit solely to record the final HEAD and thereby invalidate a prior review.

**Reviewer / controller handoff:** Code authors may run their own checks, but an actual independent reviewer must not write the reviewed changes. Prefer the minimal set of one implementation worker and one independent read-only reviewer, with actual model/effort/worktree permissions recorded; writing model names in instructions does not establish which agent ran. A Codex `/goal` controls only this one stage and does not grant continuation into any new stage or permission to merge.

