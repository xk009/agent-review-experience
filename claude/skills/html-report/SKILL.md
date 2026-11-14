---
name: html-report
description: 把方案对比、架构说明、代码 review、数据分析、长计划输出为单文件 HTML 报告。输出超过约 80 行、含多方案对比、需要图表或多文件 diff review 时使用。
---

生成一个自包含的单文件 HTML，遵守以下规范。

结构（金字塔）
1. 顶部 TL;DR 卡片：1-3 句结论 + 状态徽章 + "需要你决策"清单（如有）。
2. 吸顶目录（sticky TOC）；各节用 <details> 可折叠，默认只展开前两节。
3. 每节按"结论 → 依据 → 细节"排列；方案对比用表格，推荐列高亮。
4. 长日志、完整代码放到末尾"附录"。

视觉
- 只用内联 CSS；用 CSS 变量定义色板，用 prefers-color-scheme 同时支持亮色/暗色。
- 正文字体 system-ui, "PingFang SC", "Microsoft YaHei"；代码字体 "JetBrains Mono", "Maple Mono NF CN", monospace。
- 正文最大宽度 860px，行高 1.7，中文段落不两端对齐。
- 严重度：高=红、中=橙、低=灰、建议=蓝；颜色 + 文字标签双编码（色弱友好）。

图与代码
- 架构/流程/时序图优先手写内联 SVG；复杂图可用 Mermaid（从 cdn.jsdelivr.net/npm/mermaid 加载），并保留 Mermaid 源码以便离线阅读。
- 代码高亮可用 highlight.js（cdnjs）；diff 用 diff2html（jsdelivr）渲染真实 git diff，side-by-side，在关键行旁加批注。
- 不引用外部图片，需要时用 data URI。

交付
- 写入 .claude-reports/YYYYMMDD-HHMM-<slug>.html，并确认该目录在 .gitignore 中。
- 终端回复只给 3-5 行结论摘要 + 文件路径，不复述 HTML 内容。
- 需要我回传选择时，页面加"复制为 prompt"按钮，把我的选择导出成可粘贴回 Claude Code 的文本。
