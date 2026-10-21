# Pure Math Survey

**简体中文** | [English](README.en.md)

当前发行候选为 **2.4.1**，政策 `minimal-rules-v22-lean-2.4.1`，运行合同 `minimal-lean-2.4.1`。本候选支持**在当前会话中建立知识库及撰写 Minimal**，软件版本标为 2.4.1，不表示已创建正式 tag 或 Release。知识和输出 schema 均为 3.0.0；轻量知识库保存同源单元、连接和短索引；Minimal 采用 rules.v22 内容与版式，并明确适配运行流程。

以固定版本的数学来源建立 canonical 知识，英文 Minimal 直接复用同一份正式陈述。文章采用 Main Results、Key Mathematical Ingredients、Connecting the Ingredients 三节，保留完整条件与结论，正确命名、定义并使用核心概念，准确注明来源，以简短文字解释关键连接。运行不指定模型、不强制子聊天，不要求审核角色、审核记录或成对快慢长稿。只建库交付来源、约定、知识单元、连接与索引；文章计划直接使用当前 KB，快照可选。重复 prepare 更新派生输入并保留已写稿件、提纲及样式；单元可连同依赖定义、约定和来源定位独立导出。写 Minimal 时先读简短运行适配，再读一次原始 rules.v22；只建库不加载排版规则。正文 11pt、边距至少 20mm、图中实质文字至少 10.5pt，题名与图计入正文六页上限，参考文献另起页。实际构建记录正文与总页数；TeX-only 不声称已测量页数。

```text
在当前会话使用 $pure-math-survey，阅读[来源文件或 URL 及版本]，研究[范围]，
面向[读者]建立 canonical 知识库，并用同一份正式陈述写一篇英文 Minimal。
```

只建库时说明“只交付知识库，不生成稿件或 PDF”。TeX-only 时说明只交付可编辑 TeX，PDF 和实际页数未测量。Thematic、Lecture、Paper 以及非 integrated view 明确不支持。旧 schema 2.x 项目不兼容，拒绝时保持原文件不变；仅添加相同运行合同不能转换为 schema 3.0.0，不提供自动迁移。

本版移除运行时审核／派工流程，安装包排除旧模式及其资源；这描述流程与资源范围，不代表已测得 token 或百分比收益。每篇模型身份、token 用量和完整运行耗时若无独立记录，应为 null 或不可用；构建／测试耗时不能代替整篇工作流耗时。

## 候选安装

需要 Python 3.10+。从当前源码检出目录构建候选：

```sh
python3 skills/pure-math-survey/scripts/package_release.py --output ../pms-install-check/pure-math-survey-2.4.1.zip
python3 tools/verify_release.py ../pms-install-check/pure-math-survey-2.4.1.zip --report ../pms-install-check/verification.json
```

校验器核对归档路径与哈希，在全新、无 pip 的虚拟环境解压，运行适用的工程测试和中性 Minimal TeX smoke。它检查软件行为，不认证论文数学；具体文章仍需真实来源内容和实际构建数据。PDF 检查需要 pdfLaTeX、BibTeX、样式需要的 TeX 包和 Poppler；`--no-build` 会报告验证未完成，不声称实际构建成功。若系统使用 `python` 命令，可相应替换 `python3`。

收到 ZIP 后，先用相邻 `.zip.sha256` 核对 SHA-256，再解压使用。将完整 `pure-math-survey/` 放入宿主 skill 目录，并单独保留旧安装。GitHub 自动生成的 Source code ZIP 不是安装包。候选生成或验证通过不表示 tag／Release 已发布；实际发布事实见 [GitHub Releases](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases)。

命令、知识存储与交付边界见 [SKILL 入口](skills/pure-math-survey/SKILL.md)及 [minimal runtime](skills/pure-math-survey/references/minimal-runtime.md)。数学来源保留各自权利，可读取不代表可再分发原文字节。代码、指令和模板使用 [MIT License](LICENSE)。

开发入口：[2.4.1 指南](docs/development/v2.4.1/DEVELOPMENT_GUIDE.zh-CN.md)、[分阶段工作流](docs/development/v2.4.1/PR_WORKFLOW.zh-CN.md)、[唯一开发状态](docs/development/v2.4.1/DEVELOPMENT_STATE.yaml)。这些文件不进入安装包，也不是运行必读内容。本候选属于开发工作，不是 2.4.1 正式发行；开发样例或工程检查不构成普遍数学正确性证明。
