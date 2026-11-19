# agent-review-experience

提升 review AI 编码代理（当前主要是终端里的 Claude Code）输出的体验和效率。这个主题的所有产物都放在这里：调研文档、prompt、配置、终端设置，以后还有小工具。

**核心目标**：在保持交付质量的前提下，减少人形成可靠判断所需的主动时间。围绕验收标准组织变化，用可追溯证据支持结论，按风险分配审阅注意力；终端摘要、Diff 与 HTML 服务于同一条审阅路径。

方法总览：[系统性提升 Agent 产物 Review 效率与体验](docs/review-system.md)（验收、风险分流、六个维度、跨产物证据与持续改进）。

终端与呈现专项调研：[docs/research-report.md](docs/research-report.md)（另有单文件 HTML 版 [docs/research-report.html](docs/research-report.html)，clone 后用浏览器打开）。

## 审阅闭环：本次新增的轻量入口

**先让输出便于判断，再按需收集证据、预审和生成阅读视图。** 不要求先替换终端主题或启用全部 Hook。

| 资产 | 用途 |
| --- | --- |
| [Review First 规则](claude/rules/review-first.md) | 常驻：结果、变化、优先审阅、验证缺口 |
| [Review Package Skill](claude/skills/review-package/SKILL.md) | 按需：范围 → 真实变化 → 版本与证据 → 交付包 |
| [只读预审 Agent](claude/agents/review-auditor.md) | 只允许读取与搜索；独立预审，不自动改代码 |
| [审阅模板](claude/skills/review-package/templates.md) | 代码 / 文档 / 分析，包含增量与证据过期处理 |
| [四组可复制提示词](prompts/review-workflow.md) | 交付包、独立预审、增量审阅、跨栈业务规则 |
| [安装与使用](docs/review-workflow.md) | 官方依据、能力边界、与已有配置的关系 |
| [一周试用](docs/review-pilot.md) | 检查是否减少人工时间、找证据与返工 |
| [产物归档约定](docs/asset-conventions.md) | 本主题产物统一入库，保留公开发布边界 |

在仓库根目录先预览，再确认安装：

```bash
python3 scripts/install-review-kit.py
python3 scripts/install-review-kit.py --apply
```

安装器仅处理四个审阅资产文件，不改 settings、权限、终端配置或已有 CLAUDE.md；同名不同内容默认拒绝，显式替换会备份。根目录 [CLAUDE.md](CLAUDE.md) 是本仓库维护约定，不是用户全局配置。

验证：安装器 8 项临时目录测试通过；Claude Code 实际运行、终端效果和真实提效仍待试用。详见 [验证边界](docs/review-workflow.md#验证状态与试用)。

## 原有调研与配置目录

```
.
├── README.md
├── docs/
│   ├── research-report.md          # 调研报告（中文，结论先行）
│   └── research-report.html        # 同内容单文件 HTML（亮/暗色、侧边目录）
├── claude/                         # Claude Code 配置 → 安装到 ~/.claude/
│   ├── CLAUDE.md                   # 用户级 CLAUDE.md 片段 → 合并进 ~/.claude/CLAUDE.md
│   ├── settings.json               # settings 示例 → 合并进 ~/.claude/settings.json
│   ├── claude.json.example         # autoConnectIde / diffTool → 合并进 ~/.claude.json
│   ├── output-styles/pyramid.md    # 结论先行 Output Style → ~/.claude/output-styles/
│   ├── skills/report/SKILL.md      # /report 长任务汇报 → ~/.claude/skills/report/
│   ├── skills/html-report/SKILL.md # 单文件 HTML 报告规范 → ~/.claude/skills/html-report/
│   ├── hooks/open-html.sh          # 写出 .html 后自动打开（PostToolUse 钩子）
│   ├── hooks/hooks.open-html.json  # 以脚本形式注册上面钩子的 settings 片段
│   ├── hooks/statusline.sh         # 状态栏脚本 → ~/.claude/statusline.sh
│   └── themes/review.json          # 加强 diff 对比的自定义主题 → ~/.claude/themes/
├── terminal/
│   ├── ghostty/config              # Ghostty：Maple Mono NF CN、行高、亮/暗主题
│   ├── tmux/tmux.conf              # tmux：官方推荐 4 行 + 鼠标
│   └── git/gitconfig               # difftastic（git dft）+ zdiff3
├── prompts/html-prompts.md         # 常用 HTML 产物 prompt（相机业务示例）
└── scripts/build-html.py           # 从 Markdown 重新生成 HTML 报告
```

## 快速开始：今天就能做的 Top 5

> 先 `claude update`。下面的命令会覆盖同名文件；如果你已有 `~/.claude/settings.json`、`~/.claude/CLAUDE.md` 或 `~/.claude.json`，请手动合并，不要直接覆盖。

1. **基础显示设置（5 分钟）**：把 [claude/settings.json](claude/settings.json) 的 `theme`、`tui`、`maxProseWidth`、`language`、`outputStyle` 合并进 `~/.claude/settings.json`。diff 面板需要 v2.1.287+，`maxProseWidth` 需要 v2.1.282+。
2. **结论先行 Output Style（10 分钟）**：
   ```bash
   mkdir -p ~/.claude/output-styles && cp claude/output-styles/pyramid.md ~/.claude/output-styles/
   ```
   重启 Claude Code，执行 `/output-style Pyramid`。同时把 [claude/CLAUDE.md](claude/CLAUDE.md) 合并进 `~/.claude/CLAUDE.md`（Output Style 对普通 subagent 不生效，CLAUDE.md 里要留一份核心约定）。
3. **用 `/diff` 和 `/focus` 做 review（零成本）**：需要 `tui: fullscreen`（第 1 步已开）且终端至少 110 列。`Ctrl+O` 进入转录模式，按 `v` 用编辑器读长回复。
4. **终端字体与主题（15 分钟）**：
   ```bash
   brew install --cask ghostty font-maple-mono-nf-cn
   mkdir -p ~/.config/ghostty && cp terminal/ghostty/config ~/.config/ghostty/config
   ```
   用 tmux 的话把 [terminal/tmux/tmux.conf](terminal/tmux/tmux.conf) 合并进 `~/.tmux.conf`。
5. **长内容改走 HTML（10 分钟）**：
   ```bash
   mkdir -p ~/.claude/skills && cp -r claude/skills/html-report claude/skills/report ~/.claude/skills/
   cp claude/hooks/statusline.sh ~/.claude/statusline.sh && chmod +x ~/.claude/statusline.sh
   ```
   自动打开 HTML 的钩子已经内联在 [claude/settings.json](claude/settings.json) 的 `hooks` 段里，依赖 `jq`，打开用的是 macOS 的 `open`。如果想用脚本方式注册，就改用 [claude/hooks/hooks.open-html.json](claude/hooks/hooks.open-html.json) 和 [claude/hooks/open-html.sh](claude/hooks/open-html.sh)，两种方式选一种。之后遇到长回复，直接说"做成 HTML"；prompt 示例见 [prompts/html-prompts.md](prompts/html-prompts.md)。

一周内可以接着做：`/report` 汇报 skill、状态栏、[difftastic（git dft）](terminal/git/gitconfig)、[自定义 diff 主题](claude/themes/review.json)，以及 Android Studio 联动（[claude/claude.json.example](claude/claude.json.example)，在外部终端执行 `/ide`）。长期计划见报告里的"落地路线图"。

## 待确认事项（未实测）

- [ ] 版本号：上面写的 v2.1.287+ / v2.1.282+ / v2.1.237+ 以 `claude --version` 和官方文档为准。
- [ ] Artifacts：需要 claude.ai 登录，并且能访问 `api.anthropic.com`。在国内网络、公司代理或 API Key 方式下大概率不可用，需要实测；不可用就走本地 HTML。
- [ ] Ghostty 主题名 `Catppuccin Latte/Mocha`：用 `ghostty +list-themes` 核对。
- [ ] Warp 和全屏 TUI 是否兼容：目前只是经验判断，没找到官方说明。
- [ ] 用 prompt 型 Stop hook 校验格式：每轮多一次模型调用，成本和延迟还没测。
- [ ] `language` 写 `Simplified Chinese` 还是 `简体中文`：效果差异没对比过。
- [ ] 自动打开 HTML 的钩子每次 Write 都会开一个新标签页；频繁迭代时改用 `npx live-server .claude-reports`。
- [ ] 以上所有配置都只是按官方文档写出来的，还没有在 bingo 的机器上实际跑过。

## 维护

- 改报告：编辑 `docs/research-report.md`，然后执行 `pip install markdown && python3 scripts/build-html.py` 重新生成 HTML。
- 配置文件和报告引用的是同一份内容，改配置就直接改 `claude/` 和 `terminal/` 下的文件。
