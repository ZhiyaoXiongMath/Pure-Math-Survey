# Pure Math Survey

**简体中文** | [English](README.en.md)

**版本 2.0.3。** 先建立有原始文献依据的数学知识库，再从固定的知识快照撰写所需的英文综述或讲义。

知识项目保存明确的问题、定义、结论、证明机制、结果之间的关系、例子、适用边界及对应的文献证据。它可以独立维护，不必生成文章。作者或代理负责数学阅读与写作；工具负责检查文件约定、固定输入、证据关联和实际编译。

| 写作模式 | 适用需求 |
|---|---|
| **minimal**（默认） | 快速掌握精确答案、核心机制和关键边界。 |
| thematic | 围绕一个问题理解相关结果及证明路线。 |
| lecture | 学习前置知识、计算步骤和明确要求展开的证明。 |

请求生成文章时，默认采用 **minimal + integrated**，只生成用户要求的模式。基础、结果、方法和边界是可以交叠的知识视角，不要求拆成若干卷；只有用户明确指定的页数上限才是硬性长度约束。

## 安装

从 [v2.0.3 Release](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/tag/v2.0.3) 下载
[pure-math-survey-2.0.3.zip](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/releases/download/v2.0.3/pure-math-survey-2.0.3.zip)
及校验文件。解压后，将其中完整的 `pure-math-survey` 文件夹放入宿主应用的 skills 目录。
也可以直接复制本仓库的 [skills/pure-math-survey](skills/pure-math-survey/) 文件夹。

Release 附件只提供安装包和校验文件；下方示例保存在仓库中，无需单独下载示例即可使用 skill。
软件版本为 2.0.3，当前数据格式的 schema 编号为 2.0.0；该编号不是旧版软件兼容入口。

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

[下载 Schur 补示例](examples/schur-complement/pure-math-survey-2.0.3-schur-example.zip)。它包含九个知识节点、实际的文献阅读记录、固定的知识快照，以及两页 minimal 综述和三页 lecture 讲义，用于演示完整工作流程。记录的审阅方式是作者自查，未声称独立数学审阅；原始文献 PDF 不随示例分发。

## 环境要求与开发

知识库命令行工具只使用 Python 3.10+ 标准库。生成 PDF 需要 pdfLaTeX、BibTeX 和 `math-review.sty` 加载的 TeX 宏包；页数检查和页面渲染使用 Poppler（`pdfinfo`、`pdftoppm`）。字体优先使用 STIX2，缺失时会报告改用 Latin Modern。可选的 PDF 图像比较工具还使用 PyMuPDF 和 Pillow。

```sh
python -m unittest discover -s tests -v
python skills/pure-math-survey/scripts/validate_assets.py --json
python skills/pure-math-survey/scripts/package_release.py --output ../pure-math-survey-2.0.3.zip
python tools/verify_release.py ../pure-math-survey-2.0.3.zip --no-build
```

测试覆盖快照与材料完整性、范围明确的审阅、TeX 正文检查、历史记录和打包，并包含实际 TeX 编译。测试中人工构造的审阅记录仅用于软件测试。Linux CI 使用 Python 3.10 和 3.12；Windows 若无创建符号链接的权限，会明确跳过对应的一项测试。

参见[版本说明](CHANGELOG.md)。当前版本不包含服务器、向量数据库、研究调度器或 Research Studio 桥接功能。

## 许可证

本项目的 skill 指令、脚本、模板及说明文档采用 [MIT 许可证](LICENSE)，版权声明为 `Copyright (c) 2026 ZhiyaoXiongMath`。

数学示例材料单独保留：`examples/` 和 `skills/pure-math-survey/assets/reference-samples/dhym-balanced/` 下的内容不在本次 MIT 授权范围内，包含其中的 TeX、PDF、参考文献及示例项目。此次添加许可证不为这些材料授予额外的复用许可，也不改变第三方材料原有的权利。
