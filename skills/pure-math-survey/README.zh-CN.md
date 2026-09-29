# Pure Math Survey 2.0.4

**简体中文** | [English](README.md)

先维护数学知识，再按需成文：确定范围 → 阅读原始文献 → 建立可读的知识节点、关系与证据 → 检查覆盖与就绪状态 → 固定不可变快照 → 制定文章计划 → 写作 → 实际校验、编译及逐页检查 → 交付。

**核心命令行工具只依赖 Python 3.10+ 标准库。** 本技能面向需要长期维护文献依据、数学结论和综述／讲义的作者。作者或代理执行文献阅读与数学写作，工具检查文件约定、依赖、固定输入及声明的证据。它不是自动定理证明器或无人值守的写作服务，不包含服务器、向量数据库、多代理调度器或 Studio 桥接。

## 写作与流程示例

[balanced dHYM 文稿](assets/reference-samples/dhym-balanced/README.md)由用户经过多轮润色后提供，是主要的写作和排版参考；其中的 TeX、PDF、样式与参考文献保持原字节不变。它的六页篇幅和章节／结论数量不是其他文章的要求。独立的 [Schur 补示例](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/tree/main/examples/schur-complement)演示从知识库到文章的完整流程。数据格式仍为 2.0.0。

[文章示例目录](https://github.com/ZhiyaoXiongMath/Pure-Math-Survey/tree/main/examples/dhym-balanced)只有独立 TeX 和原始 PDF。TeX 已内嵌所需样式和参考文献，数学正文没有改变。示例放在仓库中；Release 附件只包含技能安装包与校验文件。

## 安装与运行

解压 `pure-math-survey-2.0.4.zip`，将其中唯一的 `pure-math-survey/` 文件夹完整复制到宿主应用的技能目录。也可以直接运行脚本，无需安装 pip 包：

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

## 三种写作模式与统一的知识依据

`minimal` 给出精确的核心答案、必要机制和关键边界；`thematic` 组织相关结论及有依据的关系；`lecture` 展开指定的前置知识、计算和证明。请求成文时默认采用 **minimal + integrated**。仅建库或更新知识不会隐含生成文章。PDF 是交付格式，不是第四种模式。Part I–IV 是可以交叠的基础、结果、方法和边界视角，不要求分成多卷。只有用户明确设置的 `max_pages` 才是硬性页数上限。

只在知识节点中编辑规范数学陈述，用 `kb freeze` 固定快照，再以 `output plan ... --snapshot KB-...` 创建明确的文章计划。细化读者、选材和证明步骤，在正式准备前检查相应范围的就绪状态。`output prepare` 生成快照中的精确片段与待写作框架，不会凭空完成文章。`--draft` 允许准备尚未核查的内部草稿，但不允许正式发布。重新准备会保留已写的 `main.tex`；采用不同快照前应重新审阅。

`kb diff` 报告新增、修改、删除的知识及受影响的输出。旧快照和输出保持可重建。校验读取实际文件，不继承缓存中的 PASS 标签。渲染只生成图片，不代表已完成视觉审阅；接受视觉证据前必须阅读每一页。

## 安装包内容

安装 ZIP 包含支持的运行资源，包括 `survey_core` 模块、写作模式、参考材料与重建工具。仓库测试、开发日志和用户文稿的编辑记录不进入安装包。工作流程见 [SKILL.md](SKILL.md)，数据格式和命令见[文件约定](references/contracts.md)。仅支持当前的项目和审阅记录格式。

软件测试不构成独立审阅，也不能保证一般的数学正确性。验收证据记录实际执行的、范围明确的作者重读及其限制；来源哈希、实际编译和 PDF 页面检查是不同的证据。

## 许可证

技能指令、脚本、模板和说明文档采用 [MIT 许可证](LICENSE)，版权声明为 `Copyright (c) 2026 ZhiyaoXiongMath`。

随包提供的 `assets/reference-samples/dhym-balanced/` 数学参考材料，包括 TeX、PDF、参考文献及用户提供的样式，不在本次 MIT 授权范围内。仓库中的独立 `examples/` 目录同样排除在外。本次不为这些材料授予额外复用许可，也不改变第三方已有权利。
