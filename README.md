# Pure Math Survey

**简体中文** | [English](README.en.md)

当前开发候选为 **2.4.1-dev.2**，政策 `minimal-transition-pr02`，运行合同 `minimal-lean-2.4.1`。本 PR02 候选支持**在当前会话中建立知识库及撰写 Minimal**，不表示 2.4.1 已正式发布。知识／快照 schema 暂为 2.0.0，输出 schema 暂为 2.2.0；轻量 schema 和 rules.v22 最终版式属于后续阶段。

以固定版本的数学来源建立 canonical 知识，英文 Minimal 直接复用同一份正式陈述。文章采用 Main Results、Key Mathematical Ingredients、Connecting the Ingredients 三节，保留完整条件与结论，正确命名、定义并使用核心概念，准确注明来源，以简短文字解释关键连接。运行不指定模型、不强制子聊天，不要求审核角色、审核记录或成对快慢长稿。

```text
在当前会话使用 $pure-math-survey，阅读[来源文件或 URL 及版本]，研究[范围]，
面向[读者]建立 canonical 知识库，并用同一份正式陈述写一篇英文 Minimal。
```

只建库时说明“只交付知识库，不生成稿件或 PDF”。TeX-only 时说明只交付可编辑 TeX，PDF 和实际页数未测量。Thematic、Lecture、Paper 以及非 integrated view 明确不支持。缺少新运行合同的旧项目保持不变，不提供自动迁移。

## 候选安装

需要 Python 3.10+。从当前源码检出目录构建候选：

```sh
python3 skills/pure-math-survey/scripts/package_release.py --output ../pms-install-check/pure-math-survey-2.4.1-dev.2.zip
python3 tools/verify_release.py ../pms-install-check/pure-math-survey-2.4.1-dev.2.zip --report ../pms-install-check/verification.json
```

校验器核对归档路径与哈希，在全新、无 pip 的虚拟环境解压，运行适用的工程测试和中性 Minimal TeX smoke。它不认证论文数学，也不代表 PR04 最终版式已经实现。PDF 检查需要 pdfLaTeX、BibTeX、样式需要的 TeX 包和 Poppler；`--no-build` 会报告验证未完成，不声称实际构建成功。若系统使用 `python` 命令，可相应替换 `python3`。

收到 ZIP 后，先用相邻 `.zip.sha256` 核对 SHA-256，再解压使用。将完整 `pure-math-survey/` 放入宿主 skill 目录，并单独保留旧安装。GitHub 自动生成的 Source code ZIP 不是安装包。候选生成或验证通过不表示 tag／Release 已发布；实际发布事实见 [GitHub Releases](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases)。

命令、过渡存储与交付边界见 [SKILL 入口](skills/pure-math-survey/SKILL.md)及 [minimal runtime](skills/pure-math-survey/references/minimal-runtime.md)。数学来源保留各自权利，可读取不代表可再分发原文字节。代码、指令和模板使用 [MIT License](LICENSE)。

开发入口：[2.4.1 指南](docs/development/v2.4.1/DEVELOPMENT_GUIDE.zh-CN.md)、[分阶段工作流](docs/development/v2.4.1/PR_WORKFLOW.zh-CN.md)、[唯一开发状态](docs/development/v2.4.1/DEVELOPMENT_STATE.yaml)。这些文件不进入安装包，也不是运行必读内容。PR03 轻量 KB 和 PR04 六页版式不属于 PR02 已完成能力。
