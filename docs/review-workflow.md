# 从审阅优先到可追溯交付

**目标：更快形成可靠判断，不是更快读完全部输出。**

本次增补建立在已有研究报告、Pyramid 输出风格、`report` / `html-report` Skill 和终端配置之上，不另造 App 或更换主 IDE。

## 先选择你需要的能力

| 遇到的问题 | 优先采用 | 资产 |
| --- | --- | --- |
| 每次都要解释希望如何输出 | 简短常驻规则 | [review-first](../claude/rules/review-first.md) |
| 看懂摘要后仍要自己找 diff、测试和风险 | 按需生成审阅包 | [review-package](../claude/skills/review-package/SKILL.md) |
| 不熟悉另一端实现，担心实现者遗漏 | 请求只读预审 | [review-auditor](../claude/agents/review-auditor.md) |
| 第二轮又从头读一遍 | 增量审阅 | [可复制提示词](../prompts/review-workflow.md) |
| 长方案或分析难以定位 | 复用现有 HTML 阅读视图 | [html-report](../claude/skills/html-report/SKILL.md) |

## 哪些职责不应混在一起

Rules 定义长期交付约定；Output Style 主要负责语气与呈现；Skill 执行按需流程；子代理提供受限工具下的专项检查。Rules 不等于强制格式校验，Skill 也不会仅因写了“只读”就形成权限隔离。[1][2][3]

本仓库的 `review-auditor` 明确只开放 Read、Glob、Grep；主会话准备 diff，子代理不能执行 shell 或测试。它拥有分开的上下文，但可能仍用相同模型，不能承诺消除共同盲点。[3]

已有 Pyramid 的用户不要再维护两份互相矛盾的任务骨架。保留其语言风格，将新的审阅问题与证据要求合并即可；本次安装器不改 Output Style。轻量入口不要求启用旧的全部主题、Hook 或 HTML 自动生成设置。

## 安装：默认只预览，不碰全局设置

在仓库根目录运行（Python 3.9+）：

```bash
python3 scripts/install-review-kit.py
```

确认输出后执行：

```bash
python3 scripts/install-review-kit.py --apply
```

仅安装四个文件到 `~/.claude/`：一条规则、一份子代理定义，以及 Skill 主文件和模板。
不修改 `settings.json`、`CLAUDE.md`、终端配置、权限或 Hook。目标有不同内容时整次预检拒绝写入；同内容跳过。

需要替换同名旧版时，先对照差异，再使用：

```bash
python3 scripts/install-review-kit.py --apply --overwrite
```

旧文件保存在 `~/.claude/.review-kit-backups/<时间及随机标识>/`。逐文件原子替换，但不是四文件事务；系统写入错误时检查输出和备份。安装器拒绝目标内的符号链接，使用 dotfiles 链接管理的用户应自行合并或显式指定真实目录。

项目级安装可将目标改成具体项目的 `.claude`，不要同时装两份同内容规则：

```bash
python3 scripts/install-review-kit.py --target /path/to/project/.claude
# 核对后，在同一条命令后追加 --apply
```

用户级 Rules、Skills 和 Agents 的发现路径依据官方文档；新建会话后检查 `/context all` 中的规则、`/` 菜单中的 `review-package`，并实际请求一次子代理验证。命令可用性依本机版本和组织策略。[1][2][3][4]

## 使用方式

```text
/review-package 当前任务，只准备轻量 Markdown 审阅包。比较基线是 <ref>，重点检查默认行为与异常分支，不运行新构建。
```

```text
/review-package 当前跨端小改动。先给业务规则表，再调用 review-auditor 独立预审；不修改代码。最后标明仍需我判断的事项。
```

```text
/review-package 对照上一轮 <报告路径> 做增量审阅，列出哪些变化使旧验证失效。需要 HTML 阅读视图，关键风险保持可见。
```

以上为自定义 Skill 的自然语言参数，不是 Claude Code 原生开关。未安装时使用 [prompts/review-workflow.md](../prompts/review-workflow.md)。

## 交付物的最小闭环

需求与验收目标 → 确定真实变化范围 → 收集版本与证据 → 按需只读预审 → 审阅包 → 人工决定接受、退回或补验。

轻量包可以只是一页 Markdown。复杂包再加入行为规则表、发现记录和 HTML。不要用文件数量衡量完成度。

代码范围必须区分提交、暂存、未暂存和相关新增文件；`git diff` 的不同比较对象及未跟踪文件状态见 Git 官方说明。[5][6]
工作区可以在 HEAD 不变时继续变化，所以包中另记内容快照。发现变化后不能只刷新报告时间，还需重新判断受影响的验证。

对于文档，证据可以是来源、版本差异和计算复核；对于数据分析，首先暴露时间窗、样本及口径。完整结构见 [模板](../claude/skills/review-package/templates.md)。

## 与已有功能的关系

`report` 用于日常阶段汇报，`review-package` 用于需要判断与证据追溯的交付，`html-report` 用于阅读呈现；不必每次全跑一遍。
官方当前的 `/code-review` 与 `/review` 别名是可选的本地审查入口，但本仓库不依赖它们来保证只读，也不默认启用自动修复。[4]
已有终端主题、TUI、diff 配置保持原样；本次不声称它们已在用户本机验证。

## 验证状态与试用

本轮可通过标准库测试检查安装器：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

静态语法、安装器临时目录测试与真实 Claude Code 执行是三种不同证据。未在实际客户端运行前，这套流程属于可试用版本，不能宣称已有提效结果。
验收步骤和记录方法见 [一周试用](review-pilot.md)。

## 官方依据

核对日期：2026-11-14。以下支持产品机制和 Git 语义；工作流、模板与优先级是本仓库的设计建议，不是厂商保证。

[1] https://code.claude.com/docs/en/memory — 持久指令、用户规则与加载核查。

[2] https://code.claude.com/docs/en/skills — Skill 目录、手动调用、参数与加载控制。

[3] https://code.claude.com/docs/en/sub-agents — 子代理工具白名单与独立上下文。

[4] https://code.claude.com/docs/en/commands — 命令可用性、审查入口和别名。

[5] https://git-scm.com/docs/git-diff — 不同比较对象的 diff。

[6] https://git-scm.com/docs/git-status — 工作区、暂存区与未跟踪状态。
