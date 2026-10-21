# Pure Math Survey

**简体中文** | [English](README.md)

当前开发候选为 **2.4.1-dev.4**，政策 `minimal-rules-v22-lean-2.4.1`，运行合同 `minimal-lean-2.4.1`。本 PR04 候选支持**在当前会话中建立知识库及撰写 Minimal**，不表示 2.4.1 已正式发布。知识和输出 schema 均为 3.0.0；轻量知识库保存同源单元、连接和短索引；Minimal 采用 rules.v22 内容与版式，并明确适配运行流程。

以固定版本的数学来源建立 canonical 知识，英文 Minimal 直接复用同一份正式陈述。文章采用 Main Results、Key Mathematical Ingredients、Connecting the Ingredients 三节，保留完整条件与结论，正确命名、定义并使用核心概念，准确注明来源，以简短文字解释关键连接。运行不指定模型、不强制子聊天，不要求审核角色、审核记录或成对快慢长稿。只建库交付来源、约定、知识单元、连接与索引；文章计划直接使用当前 KB，快照可选。重复 prepare 更新派生输入并保留已写稿件、提纲及样式；单元可连同依赖定义、约定和来源定位独立导出。写 Minimal 时先读简短运行适配，再读一次原始 rules.v22；只建库不加载排版规则。正文 11pt、边距至少 20mm、图中实质文字至少 10.5pt，题名与图计入正文六页上限，参考文献另起页。实际构建记录正文与总页数；TeX-only 不声称已测量页数。

```text
在当前会话使用 $pure-math-survey，阅读[来源文件或 URL 及版本]，研究[范围]，
面向[读者]建立 canonical 知识库，并用同一份正式陈述写一篇英文 Minimal。
```

只建库时说明“只交付知识库，不生成稿件或 PDF”。TeX-only 时说明只交付可编辑 TeX，PDF 和实际页数未测量。Thematic、Lecture、Paper 以及非 integrated view 明确不支持。旧 schema 2.x 项目保持不变；仅有相同运行合同不代表符合 schema 3.0.0，不提供自动迁移。

## 候选安装

需要 Python 3.10+。解压已核对哈希的候选安装包后，检查身份与资源：

```sh
python3 scripts/survey.py --version --json
python3 scripts/validate_assets.py --json
```

上述命令检查候选身份、安装资源和 Minimal 准备。仓库另有发行校验器，在全新、无 pip 的环境运行适用工程测试和中性 TeX smoke。这些检查验证软件行为，不认证论文数学。PDF 构建需要 pdfLaTeX、BibTeX、样式需要的 TeX 包和 Poppler；若系统使用 `python` 命令，可相应替换 `python3`。

收到 ZIP 后，先用相邻 `.zip.sha256` 核对 SHA-256，再解压使用。将完整 `pure-math-survey/` 放入宿主 skill 目录，并单独保留旧安装。GitHub 自动生成的 Source code ZIP 不是安装包。候选生成或验证通过不表示 tag／Release 已发布；实际发布事实见 [GitHub Releases](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases)。

命令、过渡存储与交付边界见 [SKILL 入口](SKILL.md)及 [minimal runtime](references/minimal-runtime.md)。数学来源保留各自权利，可读取不代表可再分发原文字节。代码、指令和模板使用 [MIT License](LICENSE)。
