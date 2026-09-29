# 2.0.1 的发布检查与兼容性

当前运行版本为 2.0.3；活动数据 schema 仍为 2.0.0。不要为了显示新版本改写知识节点、计划、审阅或固定快照的 schema/version：这会改变哈希和历史身份。

## 正文与语义审阅

主要定理使用位于实际 document body 中的字面 `\input{../generated/statements/N-ID.tex}`。注释、preamble、未调用宏定义、字面 `\iffalse` 不证明定理已显示。嵌套 input 的解析工作目录与实际 TeX 编译一致，即 manuscript/。动态文件名、路径越界和循环拒绝；不要把此检查器当作完整 TeX 解释器。

通过 output_semantic 必须完成全文复读，并记录七项 checks：whole_manuscript、canonical_use、conditions_quantifiers、selection、attribution、proof_obligations、readability。principal_locations 与 proof_locations 使用真实 `path`、`line_start`、`line_end`；主要定理定位必须命中正文中相应生成片段的字面输入。行号存在并不证明数学正确，仍需真实复读。

模板始终是 pending；不能覆盖已有记录。原 A 输出会因旧定位不足被要求重审，不应自动转换旧 accepted。多个候选记录分别完整检查，失效的旧记录不能遮蔽有效的新记录。未来日期或未来时间戳被拒绝；日期不带时区时允许真实 UTC+14 日历日期，带时区的时刻最多允许五分钟钟差。`independent_review` 需填实际 reviewer 身份，但该字段本身不是独立性证明。

## 不可变构建历史

`python scripts/survey.py output history PROJECT --output ID --json`

每次构建/渲染保存到 `outputs/ID/history/{build,legacy-build,render}/H-...`，用 manifest 校验实际字节。旧成功结果先保存，新失败也记录；不得用旧成功 PDF 掩盖新失败。`history/latest-build.json` 是可刷新的指针，不是通过记录。更换 PDF 或页图需要新的实际视觉审阅。

## 两种 2.0.0 合同

`python scripts/survey.py kb format PROJECT --json`

A 的 scope 型审阅与 B 的 checks 型审阅不同。仅由 schema 2.0.0 不能推断二者等价。B/mixed 项目不能静默加载为已认可的 A 项目。

`python scripts/survey.py import-v2 --from OLD-B --output NEW --json`

显式导入保留稳定 ID、精确正文、来源与依赖，把原项目整体归档。活动数学状态 unassessed，活动阅读 metadata_only，覆盖 pending，活动 accepted 审阅为零、输出为零。原快照和输出仍在原始归档中；新项目必须重新核查、冻结和制订计划。目标目录必须不存在。

## 保持不变

知识独立合法；输出默认 minimal + integrated；thematic/lecture 是不同组织与证明深度；PDF 不是第四种 profile。固定定理从快照机械提取。v1 命令与 migrate 不假装产生已核查的 v2 知识。无 Studio 桥接、服务器或调度器。核心运行仅 Python 标准库；TeX/BibTeX/Poppler 为 PDF 外部工具。

## 2.0.2 材料校验与兼容修复

结构、构建和发布检查会从固定快照重算写作材料集合及字节。修改、删除、增加 materials 文件，修改复制的审阅记录或陈旧 materials manifest 会触发 MATERIALS_CHANGED，并定位失配路径。原始来源文件仍按既有规则省略；既有正确的 2.0.0/2.0.1 输出无需改写清单或旧审阅。作者笔记放在 materials 外；显式 prepare 可恢复副本，同时保留 manuscript 与 outline。

项目文本明确按 UTF-8 读取，旧入口支持隔离 Python 导入。符号链接创建权限不足的测试会明确跳过；支持符号链接的 CI 必须实际执行该用例。测试、迁移和重新准备都不授予新的数学认可。
