# AI 编码代理 review 提效：工具与实践全景（按好用程度排序）

> 调研时间：2026-11-14（UTC+8）。star 数和最近 push 日期是当天用 GitHub API 查的。排序依据：star 数、最近活跃度、在 awesome-claude-code 等社区清单里出现的情况，以及和"主力 IDE 是终端 Claude Code"这个场景的贴合度。没有做系统性的口碑统计，下面"推荐 / 不推荐"是综合判断。

## 一、社区项目与 Claude Code 配套工具

| # | 名称 | ⭐ / 活跃 | 一句话功能 | 对终端 Claude Code 用户的价值 | 结论 |
|---|---|---|---|---|---|
| 1 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | 10.6k / 当天有提交 | 通过 hook 拦截 ExitPlanMode，在可视化界面里对计划做批注、删改，再批准或打回；后来扩展到 diff、PR、HTML 产物的 review，反馈直接回传给 agent | 让你先 review 计划，而不是事后 review 500 行代码，这是最省力的环节 | **强烈推荐**：star 高、活跃，直接切在 Claude Code 的流程里 |
| 2 | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 58.0k / 当天有提交 | Claude Code 资源清单：skills、状态栏、工具、插件 | 找配套工具的第一入口，条目有人工审核 | **推荐**当索引用，不是工具本身 |
| 3 | [matt1398/claude-devtools](https://github.com/matt1398/claude-devtools) | 4.0k / 最近 push 2026-09-26 | 读取 `~/.claude/` 日志，可视化每次工具调用、内联 diff、token 归因、subagent 执行树 | 能看到终端折叠成"Edited 2 files"背后的全部细节，追溯"它为什么这么改" | **推荐**（排查和复盘用）；近两个月没更新，需留意 |
| 4 | [daaain/claude-code-log](https://github.com/daaain/claude-code-log) | 1.3k / 2026-11-11 | 把会话 JSONL 转成 HTML/Markdown，支持 TUI、watch、全文搜索 | 会话归档和事后阅读，`uvx` 一条命令就能跑 | 推荐（轻量归档） |
| 5 | [Nimbalyst/nimbalyst](https://github.com/Nimbalyst/nimbalyst) | 2.1k / 当天有提交 | Claude Code / Codex 的可视化工作台，以红绿 WYSIWYG diff 审批改动 | 对 Markdown、mermaid、数据模型这类非代码产物的 review 很直观 | 可选：比较重，相当于另一个 IDE，和"终端为主"的思路冲突 |
| 6 | [u-ichi/reviewable-html-workbench](https://github.com/u-ichi/reviewable-html-workbench) | 302 / 2026-09-10 | 在 agent 生成的 HTML 文档上划词批注，agent 读取批注后迭代 | 和"HTML 产物"路线配套 | 可试：小众，活跃度一般 |

**不推荐**：simonw/claude-code-transcripts（1.7k，2026-02 之后没有更新）；icanb/claude-view（3 star）、pitwall（1 star）、ccx（0 star），这三个思路不错但太早期。

## 二、官方最佳实践（让 AI 代码更易 review）

| # | 来源 | 核心做法 | 对你的价值 |
|---|---|---|---|
| 1 | [Anthropic：Claude Code Best practices](https://code.claude.com/docs/en/best-practices) | 给 Claude 一个能返回 pass/fail 的检查（测试、构建、lint），可以用 Stop hook 强制执行；要求它给出证据（跑了什么命令、输出是什么）；用 `/code-review` 在一个没看过对话的新 subagent 里审 diff；按 SPEC 审查时加上"skip style"，避免为了挑问题而过度修改 | **最该照做**：直接减少你要人工看的量 |
| 2 | [Anthropic：Code Review（托管）](https://code.claude.com/docs/en/code-review) | 多个 agent 并行审 PR，再经过一步验证去掉误报，按严重度给行内评论；不会批准或阻塞 PR；用 REVIEW.md 定制规则 | 团队级方案；需要 Team/Enterprise 套餐，不支持 ZDR |
| 3 | [OpenAI：Codex code review](https://github.com/openai/codex) | `/review` 和 `codex review --uncommitted/--base/--commit` 会起一个只读的专门 reviewer；可以用 `review_model` 单独给 review 指定更强的模型；GitHub 上评论 `@codex review` 只报 P0/P1；规则写在 AGENTS.md 的 `## Code Review Rules` 下 | "只报高优先级"和"review 用独立模型"两个思路值得照搬。这部分细节来自第三方教程对 OpenAI 文档的转述，以官方文档为准 |
| 4 | [Google：eng-practices](https://github.com/google/eng-practices)（23.3k，已归档） | 小 CL、好的 CL 描述、reviewer 先看设计再看细节 | 经典原则，正好用来约束 agent："一次只做一个小改动，并附上描述" |
| 5 | [GitHub Copilot code review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review) | 把 Copilot 加为 PR reviewer；用 `.github/copilot-instructions.md` 定制 review 规则 | 团队已经在用 GitHub Copilot 时零成本可用 |
| 6 | [Google：Gemini Code Assist 风格指南](https://developers.google.com/gemini-code-assist/docs/code-review-style-guide) | 用 `.gemini/styleguide.md` 写自然语言的 review 规则 | 和 1、3、5 是同一个模式：仓库里放一份 review 规则文件 |

共识：①计划先行（plan mode / Plannotator）；②小步提交、一次只做一件事；③让 agent 自己验证，并且贴出证据；④用一个没看过对话的 reviewer 做二审；⑤review 规则写成仓库文件；⑥只报高严重度，跳过风格类意见。

## 三、知名工具

### 3a. AI review 工具 / bot

| # | 名称 | 一句话功能 | 对终端 Claude Code 用户的价值 | 结论 |
|---|---|---|---|---|
| 1 | Claude Code 内置 [`/code-review`](https://code.claude.com/docs/en/code-review-local) | 在新 subagent 里审当前 diff，`--fix` 直接改，`ultra` 走云端多 agent 深审 | 零安装，所有套餐都能用，就在终端里 | **首选** |
| 2 | [OpenAI Codex review](https://github.com/openai/codex)（⭐135k） | `codex review --uncommitted` 非交互执行，可以放进 pre-push 脚本 | 换一个模型家族做交叉审查，降低"自己审自己"的盲区 | 推荐（如果已有 ChatGPT/Codex 订阅） |
| 3 | [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)（⭐9.9k） | GitHub Action：PR 里 `@claude` 就能 review 或修改 | 本地习惯延伸到 PR，可以复用 CLAUDE.md | 推荐（团队 PR 流程） |
| 4 | [qodo-ai/pr-agent](https://github.com/qodo-ai/pr-agent)（⭐16.1k） | 开源可自托管的 PR reviewer，`/review`、`/describe`、`/improve` | 公司代码不能外发时的选项，可以接自己的模型 | 可选（有私有化需求时） |
| 5 | [Greptile](https://www.greptile.com/agent) / [Graphite Agent（原 Diamond）](https://graphite.com/docs/ai-reviews) | 前者索引整个仓库，找跨文件的 bug；后者绑定 stacked PR 和 merge queue（Graphite 2025-12 被 Cursor 收购） | 都在云端 PR 层，和终端 review 关系不大 | **暂不推荐**个人用：收费，需要团队流程配合；Graphite 只适合已经在用 stacked PR 的团队 |

Copilot code review：团队用 GitHub Copilot 的话可以顺手开，对终端工作流没有额外帮助。

### 3b. Diff 查看 / review 界面

| # | 名称 | ⭐ / 活跃 | 一句话功能 | 对终端 Claude Code 用户的价值 | 结论 |
|---|---|---|---|---|---|
| 1 | Claude Code 内置 [`/diff` 侧栏](https://code.claude.com/docs/en/interactive-mode) | 官方功能 | 全屏模式下在对话旁显示改动，可按轮次（T1、T2…）过滤，点 `ask` 把单文件 diff 带进下一问 | 零安装，边看 Claude 改边审 | **首选** |
| 2 | [Wilfred/difftastic](https://github.com/Wilfred/difftastic) | 26.2k / 2026-11-13 | 按语法树做结构化 diff | agent 重构或顺手改格式时，过滤掉缩进和换行噪音；用 `git dft` 调用 | **推荐** |
| 3 | [jonas/tig](https://github.com/jonas/tig) | 13.4k / 2026-11-11 | 老牌 git TUI | 需要浏览提交历史时可用 | 可选，非必需 |

## 已评估、不采用

- ccusage（ccusage/ccusage，⭐19.4k）：只管成本和用量，与 review 无关。
- lazygit（jesseduffield/lazygit，⭐83.9k）：不需要独立 git TUI，用 `/diff` 侧栏代替。
- CodeRabbit（CLI + Claude Code 插件）：不用；二审用 `/code-review`（可选加 `codex review`）。
- tuicr（agavra/tuicr，⭐3.6k）：不用；行级反馈直接在 `/diff` 侧栏点 `ask` 或写进 prompt。
- delta（dandavison/delta，⭐32.7k）：不用；结构化 diff 用 difftastic。（依赖 delta 的 diffnav 随之不采用。）

## 最值得立刻尝试的 3 件事

1. **把 review 前移到计划阶段**：装 Plannotator，在 plan mode 结束时批注计划、打回修改，确认后才让它写代码。
2. **固定做一次 `/code-review` 二审**：每个改动结束先跑 `/code-review`（新 subagent，不受写代码时的推理影响），要求只报 P0/P1、skip style，并给出证据（命令和输出）；重要改动可再加跑 `codex review --uncommitted` 交叉审查。
3. **用内置 `/diff` 侧栏 + difftastic 看改动**：开 `tui: fullscreen`，`/diff` 边看边审、按轮次过滤、对可疑文件点 `ask`；重构类改动用 `git dft` 过滤格式噪音。
