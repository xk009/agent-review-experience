# Claude Code Review 提效调研：终端呈现 × 结论先行 × HTML 产物

> 三个维度怎么做、先做哪几件：结论先行的输出结构收益最大，其次是 HTML 产物，终端美化是基础。所有配置项已对照 2026-11 官方文档（code.claude.com/docs）核实；标注"未实测"的地方尚未在真实环境验证。
>
> 调研日期：2026-11-14（UTC+8）。配置文件见仓库 `claude/` 与 `terminal/` 目录。

## 目录

- [核心结论](#核心结论)
- [今天就做的 Top 5](#今天就做的-top-5)
- [投入与收益](#投入与收益)
- [维度一：终端呈现](#维度一终端呈现)
- [维度二：输出结构（结论先行）](#维度二输出结构结论先行)
- [维度三：HTML 产物](#维度三html-产物)
- [落地路线图](#落地路线图)
- [待核实与注意事项](#待核实与注意事项)
- [来源](#来源)

## 核心结论

**一句话**：Review 效率的瓶颈在"信息先后顺序"和"载体"，不在配色。先用 Output Style 把每条回复变成"结论 → 改动 → 风险 → 待决策"，再把长内容甩给 HTML，终端只看摘要和 diff。

1. **结构维度收益最大，成本最低**：自定义 Output Style（`~/.claude/output-styles/`，务必加 `keep-coding-instructions: true`）+ 精简的 `~/.claude/CLAUDE.md` 就能让结论先行成为默认；内置的 `Concise` 风格可以当零成本起点。
2. **HTML 已经是 Anthropic Claude Code 团队自己在用的做法**（Thariq Shihipar 2026-05 的文章）。官方 Artifacts 能把 HTML 发布成实时更新的 claude.ai 页面，但需要 claude.ai 账号登录；走公司 API Key 或网关时用本地单文件 HTML + 自动打开代替。
3. **终端层面最值钱的是官方新功能**：`tui: fullscreen` + `/diff` 侧边 diff 面板、`/focus` 精简视图、`maxProseWidth` 限制行宽。字体和主题属于一次配好的基础设施。
4. **Android 背景的捷径**：Claude Code 的 JetBrains 插件官方支持 Android Studio，可以把 Android Studio 降级成"diff 查看器 + 跳转"，主战场留在 Ghostty。
5. **强制格式别靠 Stop hook 硬卡**：官方定位是 Output Style 和 CLAUDE.md 只是"指令"，hook 才是"保证"；用 prompt 型 Stop hook 校验格式可行，但每轮多一次模型调用，放到长期再试。

## 今天就做的 Top 5

| # | 做什么 | 耗时 | 对应文件 |
|---|---|---|---|
| 1 | 升级并写入基础显示设置：`claude update`，在 `~/.claude/settings.json` 写入 `theme: auto`、`tui: fullscreen`、`maxProseWidth: 100`、`language`。diff 面板要求 v2.1.287+，`maxProseWidth` 要求 v2.1.282+ | 5 分钟 | `claude/settings.json` |
| 2 | 装上结论先行的 Output Style：存为 `~/.claude/output-styles/pyramid.md`，重启后 `/output-style Pyramid`。想先试水就用 `/output-style concise` | 10 分钟 | `claude/output-styles/pyramid.md` |
| 3 | 养成 `/diff` 与 `/focus` 的 review 姿势：终端 ≥110 列时 `/diff` 在对话旁开面板，可按轮次（T1、T2…）看改动，点 `ask` 把单文件 diff 带进下一问；`/focus` 只显示提问、工具调用一行摘要和最终回复 | 0 | `claude/settings.json`（`tui`） |
| 4 | 换终端字体与行高：Ghostty + Maple Mono NF CN（中英 2:1 严格对齐）+ 行高加 15%，主题随系统亮暗切换 | 15 分钟 | `terminal/ghostty/config` |
| 5 | 长内容改走 HTML：装 `html-report` skill，并配上"写出 .html 就自动 open"的 PostToolUse hook | 10 分钟 | `claude/skills/html-report/SKILL.md`、`claude/hooks/` |

## 投入与收益

位置是基于"整天在终端 review"这一前提的主观估计，不是测量结果。

| 象限 | 措施 |
|---|---|
| 高收益、低投入（今天做） | Pyramid 输出风格；`/diff` 面板 + `/focus`；HTML 报告 skill |
| 高收益、高投入（排期做） | Artifacts 评论闭环；团队插件打包 |
| 低收益、低投入（顺手做） | 字体与主题；Statusline；difftastic |
| 低收益、高投入（暂缓） | Stop hook 校验格式 |

## 维度一：终端呈现

原则：终端负责"看摘要、看 diff、做决定"，不负责读长文。配色字体一次配好，真正提效的是官方的全屏渲染、diff 面板和视图模式。

### 终端选型

| 终端 | Shift+Enter | 完成通知 | 评价 |
|---|---|---|---|
| Ghostty | 原生支持 | 原生桌面通知 | **首选**：快、原生、配置简单 |
| Kitty | 原生支持 | 原生桌面通知 | 功能强，配置偏重 |
| iTerm2 | 原生支持 | 需打开提醒设置 | 稳；别用 `tmux -CC` 跑全屏模式 |
| WezTerm | 原生支持 | 未列出，需 hook | Lua 可编程，适合重度定制 |
| Warp | 原生支持 | 需 hook 或 `terminal_bell` | 块式 UI 与全屏 TUI 相性一般（经验判断，未实测） |
| Android Studio 终端 | 不支持 | 无 | 不建议当主终端 |

Shift+Enter 与通知行为来自官方 terminal-config 页；Android Studio 终端里换行只能用 `Ctrl+J` 或 `\` 加回车。

### 字体选型

| 字体 | 中英对齐 | 适合 |
|---|---|---|
| Maple Mono NF CN | 严格 2:1 | **首选**：自带中文、Nerd Font 图标、连字，Claude 状态符号有覆盖 |
| Sarasa Term SC（更纱黑体） | 严格 2:1 | 偏窄、信息密度高，长期稳定 |
| JetBrains Mono + 系统中文回退 | 不严格 | 沿用 AS 习惯；中文会被缩放，表格可能错位 |
| 霞鹜文楷等宽 | 2:1 | 阅读感好，适合看长文，写代码偏软 |

配置：[`terminal/ghostty/config`](../terminal/ghostty/config)、[`terminal/tmux/tmux.conf`](../terminal/tmux/tmux.conf)。

### Claude Code 内置显示设置

| 设置 / 命令 | 作用 | 建议 |
|---|---|---|
| `theme` | `auto` / `dark` / `light` / `*-daltonized` / `*-ansi` / `custom:<slug>` | `auto` 跟随终端；色弱或想要更强 diff 对比用 daltonized |
| `~/.claude/themes/*.json` | 自定义主题，可改 `diffAdded` 等 token，热加载 | 调 diff 底色和词级高亮 |
| `tui: fullscreen` | 无闪烁全屏渲染，支持鼠标，长会话内存稳定 | 开；diff 面板、`/focus` 都依赖它 |
| `/diff` | 侧边 diff 面板，按轮次看改动，`Ctrl+X B` 切换对比基准 | 核心 review 入口 |
| `/focus` 或 `viewMode` | 只显示提问、工具一行摘要（含 diffstat）、最终回复 | 日常开；排查问题时 `Ctrl+O` 展开 |
| `Ctrl+O` | 转录模式，`/` 搜索；按 `v` 在 `$EDITOR` 打开整段对话 | 长回复用编辑器读 |
| `maxProseWidth` | 正文按 N 列换行，表格和代码块仍用满宽度 | 80–100 |
| `verbose` | 工具输出全展开 | 默认关，调试 hook/MCP 时开 |
| `syntaxHighlightingDisabled` | 关掉 diff 和代码块高亮 | 保持默认 false |
| `language` | 回复语言，原样传给模型 | 如 `Simplified Chinese` |
| `externalEditorContext` | `Ctrl+G` 写 prompt 时把上条回复以注释带入编辑器 | 边看边回复很好用；写在 `~/.claude.json` |
| `statusLine` | 底部状态栏脚本，stdin 收到 JSON | 显示上下文占比、5 小时额度、分支、当前风格 |

配置：[`claude/settings.json`](../claude/settings.json)（其中的 hook 会在 Claude 写出任何 `.html` 后自动用浏览器打开，macOS `open`，依赖 `jq`）、[`claude/themes/review.json`](../claude/themes/review.json)、[`claude/hooks/statusline.sh`](../claude/hooks/statusline.sh)。

### Diff 怎么看

| 方式 | 什么时候用 | 说明 |
|---|---|---|
| `/diff` 面板 | Claude 改动时边看边审 | **首选**；按轮次过滤、单文件 ask |
| Android Studio diff（`diffTool: auto`） | 改动大、要跳定义、看上下文 | JetBrains 插件支持 AS；外部终端里 `/ide` 连接 |
| difftastic（`git dft`） | 重构、格式化混杂的改动 | 按语法树比较，过滤缩进与换行噪音 |
| `/code-review` | 提交前自查 | 内置 skill，`--fix` 直接改；`/security-review` 查安全 |
| HTML diff 报告 | 要给别人看或改动跨很多文件 | diff2html 渲染 + 批注，见维度三 |

配置：[`claude/claude.json.example`](../claude/claude.json.example)（`autoConnectIde`、`diffTool` 只认 `~/.claude.json`）、[`terminal/git/gitconfig`](../terminal/git/gitconfig)。

注意：Claude Code 自己的 diff 渲染用的是主题里的 `diffAdded` 等 token；difftastic 只影响你自己执行的 `git dft`。

## 维度二：输出结构（结论先行）

思路：用 Output Style 管"怎么说"（每条回复都生效），CLAUDE.md 管"你是谁、项目事实"，skill 管"特定场景的固定格式"，hook 管"必须发生的事"。官方文档明确：Output Style 只是指令，不保证每次都执行。

### 该用哪个机制

| 机制 | 作用范围 | 放什么 |
|---|---|---|
| Output Style | 主对话每条回复 | 结论先行的回复骨架、书写规范 |
| `~/.claude/CLAUDE.md` | 所有项目常驻 | 你的角色、沟通约定、HTML 存放约定 |
| 项目 CLAUDE.md / `.claude/rules/` | 单仓库；rules 可按 `paths` 限定 | 构建命令、模块约定、Kotlin 规范 |
| Skill（`/report`、`/html-report`） | 调用时或任务匹配时加载 | 长任务汇报格式、HTML 规范 |
| Hook | 生命周期事件，确定执行 | 写完 HTML 自动打开、完成通知、格式校验 |
| Subagent | 独立上下文 | 调研、review 等重任务，只回传摘要 |
| `--append-system-prompt` | 单次启动 | 临时实验某种格式 |

> ⚠️ **三个容易踩的坑**：自定义风格不写 `keep-coding-instructions: true` 会丢掉 Claude Code 内置的工程规范；`outputStyle` 的值大小写敏感，必须和 `name` 完全一致，否则回落到 Default；Output Style 不作用于普通 subagent（只作用于主对话和 fork），所以 CLAUDE.md 里也要留一句核心约定。

**内置风格可直接用**

- `Concise`：第一句给结果，去掉开场、过程叙述和结尾复述（v2.1.237+）
- `Explanatory`：附 Insight 块解释为什么这么写，适合读不熟的模块
- `Proactive`：少问常规问题，直接开干

**内置风格的局限**：没有固定的"风险 / 待决策"分节；不会自动判断什么时候改用 HTML；不了解你的 Android 验证命令。

### 可复制的配置

| 文件 | 安装位置 | 说明 |
|---|---|---|
| [`claude/output-styles/pyramid.md`](../claude/output-styles/pyramid.md) | `~/.claude/output-styles/pyramid.md` | 存好后重启，`/output-style Pyramid` 或 settings 设 `"outputStyle": "Pyramid"` |
| [`claude/CLAUDE.md`](../claude/CLAUDE.md) | 合并进 `~/.claude/CLAUDE.md` | 保持短，只放事实和硬约定；格式细节交给 Output Style |
| [`claude/skills/report/SKILL.md`](../claude/skills/report/SKILL.md) | `~/.claude/skills/report/SKILL.md` | 长任务结束时 `/report`；`!` 加反引号的命令会在加载时执行，把真实 diff stat 注入上下文 |

## 维度三：HTML 产物

Claude Code 团队的 Thariq Shihipar 公开说他几乎不再用 Markdown：超过 100 行的 Markdown 他自己都不读，HTML 能放表格、SVG 图、交互控件，更容易被人真正读完。代价是更多输出 token，以及你不方便手改。

### 什么场景值得用 HTML

| 场景 | 推荐载体 | 理由 |
|---|---|---|
| 多文件改动的 code review | **HTML** | diff + 行旁批注 + 严重度着色 + 折叠 |
| 方案对比 / 技术选型 | **HTML** | 对比表 + 每个方案一张图，推荐项高亮 |
| 架构、数据流、时序讲解 | **HTML** | SVG / Mermaid 图远胜 ASCII 图 |
| 数据分析（性能、crash、耗时） | **HTML** | 图表 + 可排序表格 |
| 排序、分桶、调参类决策 | **HTML（交互）** | 拖拽或滑块，再"复制为 prompt"回传 |
| 周报 / 给团队的进展同步 | HTML 或 Artifact | 链接一发即看，读完率高 |
| 单次小改动的回复 | 终端文本 | 结论先行已经够用 |
| 要进仓库、要人手改的文档 | Markdown | README、ADR、CLAUDE.md、git diff 友好 |
| 交给另一个 agent 的上下文 | Markdown | token 省，模型读得一样好 |

### 两条落地路线

| | 官方 Artifacts | 本地单文件 HTML |
|---|---|---|
| 怎么触发 | 说"做成 artifact"或 Claude 自行判断 | 说"做成 HTML"或 html-report skill |
| 查看 | 自动开浏览器，`Ctrl+]` 重开，`/artifacts` 列表 | `open` 文件；live-server 自动刷新 |
| 更新 | 同一 URL 原地更新，有版本 | 覆盖文件，浏览器刷新 |
| 分享与反馈 | 可分享；同组织成员评论，Claude 可读评论并回复 | 发文件或自己托管 |
| 前提 | Pro/Max/Team/Enterprise + claude.ai 登录 + Anthropic API | 无 |
| 不可用的情况 | API Key、网关、Bedrock/Vertex、`-p` 脚本模式、ZDR 组织 | 无 |
| 外部资源 | 仅 Google Fonts 与 cdnjs、unpkg、jsDelivr 等 5 个 CDN | 随意，但建议同样只用这几个 |

> ℹ️ **建议**：两条都走同一套 html-report 规范：只用内联 CSS 和 jsDelivr/cdnjs 的库，同一份 HTML 既能本地打开，也能直接发布成 Artifact。如果用的是公司 API Key 或代理网关，先默认走本地路线。

- Skill：[`claude/skills/html-report/SKILL.md`](../claude/skills/html-report/SKILL.md)（没有 `disable-model-invocation`，Claude 会在长输出时自己调用）
- 常用 prompt：[`prompts/html-prompts.md`](../prompts/html-prompts.md)
- 本地预览：一次性看用 `open file.html`；反复迭代用 `npx live-server .claude-reports` 或 `browser-sync start --server .claude-reports --files "*.html"`
- 社区参考：u-ichi/reviewable-html-workbench（在 HTML 上批注再让 Claude 读批注修改）、sidzan/html-artifacts（21 套模板）、Thariq 的 20 个示例

### Markdown 折中方案

| 工具 | 形态 | 适合 |
|---|---|---|
| glow | 终端 TUI 阅读器 | 不离开终端看 .md：`glow -p plan.md` |
| mdcat | 终端渲染输出 | Kitty/iTerm2 里可显示图片 |
| VS Code / Cursor 预览 | 侧边实时预览 | 装 Mermaid 预览扩展即可看图 |
| Typora | 所见即所得 | 需要手改的长文档 |
| Obsidian | 知识库 | 方案、调研沉淀成双链笔记 |
| Artifacts 发布 .md | claude.ai 样式化页面 | 官方支持 .md 源文件，带代码高亮 |

## 落地路线图

| 阶段 | 做什么 | 产出 |
|---|---|---|
| 今天 | Top 5：设置、Pyramid 风格、/diff 与 /focus、字体、HTML skill + hook | 默认结论先行，长内容进浏览器 |
| 一周内 | statusline；`/report` skill；difftastic；自定义 diff 主题；tmux 配置；Android Studio `/ide` 联动 | review 姿势固定下来 |
| 一周内 | 用 Explanatory 风格读不熟的模块；对比 Pyramid 与 Concise 一周的体感 | 确定个人默认风格 |
| 长期 | 把 Output Style + skills + hooks 打包成团队插件（插件可带 `output-styles/`），推给相机团队 | 团队统一的汇报与 review 格式 |
| 长期 | Artifacts 做进展看板和 review 评论闭环（若账号条件允许） | 评论直接驱动 Claude 修改 |
| 长期 | 试 prompt 型 Stop hook 校验"首句是否结论"；评估 Mods 做自定义面板 | 格式从"建议"变成"保证" |

## 待核实与注意事项

- 版本号：diff 面板 v2.1.287+、`maxProseWidth` v2.1.282+、`Concise` v2.1.237+，以 `claude --version` 为准。
- Artifacts 依赖访问 `api.anthropic.com` 和 claude.ai 登录；国内网络、公司代理或 API Key 方式下大概率不可用，需要实测。
- Ghostty 主题名（如 Catppuccin Latte/Mocha）以 `ghostty +list-themes` 为准；Warp 与全屏 TUI 的兼容是经验判断，未见官方说明。
- Stop hook 校验格式：官方提供 `last_assistant_message` 和防循环的 `stop_hook_active`，但每轮多一次模型调用、增加延迟，未实测成本。
- `language` 的值原样传给模型，不做校验；写 `Simplified Chinese` 或 `简体中文` 都可以，未对比效果差异。
- 自动打开 HTML 的 hook 每次 Write 都会开新标签页；频繁迭代时换成 live-server。

## 来源

- Output styles（官方）：https://code.claude.com/docs/en/output-styles
- Configure your terminal（主题、tmux、自定义主题 token）：https://code.claude.com/docs/en/terminal-config
- Fullscreen rendering（/focus、转录模式、diff 面板）：https://code.claude.com/docs/en/fullscreen
- Interactive mode：Review changes with /diff：https://code.claude.com/docs/en/interactive-mode
- Settings reference（maxProseWidth、viewMode、diffTool 等）：https://code.claude.com/docs/en/settings-reference
- Status line：https://code.claude.com/docs/en/statusline
- Share session output as artifacts：https://code.claude.com/docs/en/artifacts
- Hooks guide（prompt 型 Stop hook）：https://code.claude.com/docs/en/hooks-guide
- Memory：CLAUDE.md 与 .claude/rules：https://code.claude.com/docs/en/memory
- Skills（frontmatter、!命令注入）：https://code.claude.com/docs/en/skills
- JetBrains IDEs（含 Android Studio）：https://code.claude.com/docs/en/jetbrains
- The unreasonable effectiveness of HTML（claude.dev，2026-05-20）：https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/
- HTML 示例集（20 个单文件）：https://thariqs.github.io/html-effectiveness/
- HTML is the new Markdown（How I AI 访谈）：https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown
- sidzan/html-artifacts：https://github.com/sidzan/html-artifacts
- u-ichi/reviewable-html-workbench：https://github.com/u-ichi/reviewable-html-workbench
- Maple Mono 中文说明：https://github.com/subframe7536/maple-font/blob/variable/README_CN.md
- Ghostty 配置参考：https://ghostty.org/docs/config/reference
