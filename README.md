# Pure Math Survey — 预览版

**简体中文** | [English](README.en.md)

当前为 `v2.1.0-r4-preview.1` 预览版（软件 2.1.0），数学端到端流程仍在验证；[开发状态](docs/r4/development-status.md)单独记录实际进度。

面向整理数学文献、维护知识库、撰写英文综述或讲义的作者。先阅读原始来源，把结果、条件、论证和边界组织为可追溯知识，再写用户要求的稿件；也支持研究草稿。

## 安装

在 [Release 页面](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.1.0-r4-preview.1)下载 `pure-math-survey-2.1.0.zip` 和 `.zip.sha256` 附件，核对 SHA-256。使用完整安装 ZIP，不能用 GitHub 自动生成的源码 ZIP 代替。

解压后把完整 `pure-math-survey/` 放入宿主 skill 目录，如 Codex 默认的 `~/.codex/skills/`。保留 references、scripts、assets，不只复制 SKILL.md。新聊天引用 `$pure-math-survey` 即可开始。

宿主需支持新建、读取、等待及给工作聊天发送任务，并提供 `gpt-6-astra / ultra`。脚本使用 Python 3.10+ 标准库；PDF 构建另需 pdfLaTeX、BibTeX、样式依赖的 TeX 包和 Poppler。缺少能力时报告阻碍；详见[构建要求](skills/pure-math-survey/references/layout-and-build.md)。

## 怎么运行

调用聊天就是控制台，保留你当前的模型设置。你说明主题范围、读者、来源和输出后，控制台：

1. 实际派发 Astra/ultra 工作聊天，阅读原始来源，核实版本、条件和引用。
2. 构建快慢知识：快层解释目标、输入、关键操作和用途；慢层展开对应推导与外部定理接口。
3. 让非作者审阅知识及所请求稿件的证明承诺，核对实际文件后单写整合知识。
4. 冻结不可变快照；只建知识的请求在知识与证据处结束。
5. 为所需稿件安排独立写作者，消费固定快照并实际完成 TeX。`prepare` 只是材料与脚手架，不等于文章。
6. 非作者核查数学与成文，构建 PDF 并查看全部页面；通过交付检查时提供适用的可重建包。

用户不需要手填审阅 JSON，也不能用编译或哈希代替数学核查。未验证 Paper 保持显著 `DRAFT_UNVERIFIED`，正式研究打包拒绝；已知结果不能虚构为原创。

## 可复制的启动提示

替换项目目录、主题和来源范围，由你实际发送授权：

```text
使用 $pure-math-survey，在 work/matrix-positivity 建立知识库。
主题：有限维实对称分块矩阵的正定性，首块可逆，排除奇异首块变体。
读者掌握本科线性代数。先只建知识，不生成文章或 PDF；阅读我提供的
原始来源，也可查找原始来源，解释全部条件、两向论证和边界。
允许读取完整安装 skill、指定来源和本项目；仅在本项目的工作目录写入。
本聊天是控制台。我授权创建必要的 gpt-6-astra / ultra 工作聊天，负责
文献、快慢知识、写作和非作者审阅；授权向它们发送任务、继续、修订、
停止指令并读取结果。其他读取范围如有需要，请具体说明。
```

同范围的有效授权会复用；控制台把真实读写边界传给 worker，worker 不递归派发。仅文档中出现提示并不产生授权。

后续可以说：“基于这个项目写一份英文 Minimal，view=integrated，范围和读者不变；完整给出主结果与决定性理由，交付 TeX、PDF 和符合条件的重建包，沿用授权。”首次就要文章时也可直接明确这个输出；未指定模式的文章默认 Minimal + integrated。

知识交付含综览、节点、来源／审阅记录和缺口。稿件另有计划、outline、`manuscript/main.tex`、固定材料、`build/main.pdf` 和证据；这是交付结构，不表示下方小示例已生成文章。更新时提供新来源或纠正，先核查知识再冻结新快照，旧文件不改。多输出须分别说明读者、模式和数量；可以共享快照，但独立写作和审阅。

## 模式与侧重点

| 模式 | 用途与结构 |
|---|---|
| Minimal | 无摘要；Main Results / Key Mathematical Ingredients / Connecting the Ingredients 三节，全部完整主结果在第一节。 |
| Thematic | 无摘要；准确问题、代表性结果、真实方法及可比条件下的综合。 |
| Lecture | 无摘要；完整目标定理、忠实路线与可复现的构造／计算／证明。 |
| Paper | 简洁摘要与完整 Introduction，准确贡献定位和证明；默认未验证草稿，原创正式交付有额外门槛。 |

五种 view：integrated、foundations、results、methods、boundaries。它们改变重点，不改变数学事实或模式责任；只生成所请求的输出。详见[模式契约](skills/pure-math-survey/references/editions.md)。

## 真实 CLI 小示例（可选）

聊天是日常入口，CLI 负责文件操作。已有实跑使用 UTF-8 `scope-input.md`：

```markdown
# Scope

Build a source-grounded knowledge project on positivity of finite real symmetric block matrices with an invertible leading block. Exclude singular-pivot variants. Readers know undergraduate linear algebra. This initialization demonstration does not request a manuscript or certify any theorem.
```

在安装 ZIP 解压后的父目录运行：

```sh
python pure-math-survey/scripts/survey.py init --output my-topic --topic matrix-positivity --scope scope-input.md --json
python pure-math-survey/scripts/survey.py kb validate my-topic --json
```

实际结果：`INITIALIZED`、`review_status=pending`、`outputs=[]`；验证为 `VALID`、0 节点、0 来源，并有 `SEMANTIC_NOT_CERTIFIED` 警告。创建了 project.json、scope.md 和 knowledge 下的综览／约定／发现／覆盖文件，没有文章或 PDF。结构有效不等于数学就绪。

当前仅支持 r4，旧／未知输出契约明确拒绝且原文件不改。[完整入口](skills/pure-math-survey/SKILL.md)与[验证边界](skills/pure-math-survey/references/validation.md)说明其余责任；AI 审阅不等于外部同行评审或原创性认证。代码、指令和模板遵循 [MIT License](LICENSE)，数学材料及第三方来源保留各自权利。
