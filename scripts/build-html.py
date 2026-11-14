#!/usr/bin/env python3
"""把 docs/research-report.md 渲染成单文件 HTML（内联 CSS、亮/暗色、吸顶目录）。

用法：pip install markdown && python3 scripts/build-html.py
"""
import re
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / "docs/research-report.md").read_text(encoding="utf-8")

# HTML 版用自动生成的侧边目录，去掉 Markdown 里手写的"目录"一节
src = re.sub(r"^## 目录\n.*?(?=^## )", "", src, flags=re.S | re.M)

md = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "sane_lists"],
    extension_configs={"toc": {"slugify": slugify_unicode, "toc_depth": "2-3"}},
)
body = md.convert(src)
toc = md.toc
title = "Claude Code Review 提效调研"

CSS = """
:root{--bg:#fbfaf8;--fg:#1f2328;--muted:#57606a;--line:#d8dee4;--card:#ffffff;--accent:#0969da;
--accent-bg:#ddf4ff;--warn-bg:#fff8c5;--code-bg:#f2f1ee;--th:#f6f8fa}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--fg:#e6edf3;--muted:#9da7b3;--line:#30363d;
--card:#161b22;--accent:#58a6ff;--accent-bg:#132a44;--warn-bg:#3a2f0b;--code-bg:#1f242c;--th:#1c2128}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
.layout{display:grid;grid-template-columns:260px minmax(0,860px);gap:40px;justify-content:center;padding:32px 24px}
nav.toc{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;font-size:14px}
nav.toc ul{list-style:none;padding-left:12px;margin:4px 0}nav.toc>div>ul{padding-left:0}
nav.toc a{color:var(--muted);text-decoration:none}nav.toc a:hover{color:var(--accent)}
main h1{font-size:28px;line-height:1.3;margin-top:0}
main h2{margin-top:48px;padding-bottom:6px;border-bottom:1px solid var(--line)}
main h3{margin-top:32px}
a{color:var(--accent)}
blockquote{margin:16px 0;padding:12px 16px;background:var(--accent-bg);border-left:4px solid var(--accent);border-radius:8px}
blockquote p{margin:4px 0}
main>p:first-of-type+ol,#核心结论+p{background:var(--card)}
#核心结论 + p{padding:14px 18px;border:2px solid var(--accent);border-radius:10px}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14.5px;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--th)}
code{font-family:"JetBrains Mono","Maple Mono NF CN",ui-monospace,monospace;font-size:.9em;background:var(--code-bg);padding:1px 5px;border-radius:4px}
pre{background:var(--code-bg);padding:12px;border-radius:8px;overflow:auto}
footer{color:var(--muted);font-size:13px;margin-top:48px}
@media (max-width:900px){.layout{grid-template-columns:1fr}nav.toc{position:static;max-height:none}}
"""

html = f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav class="toc"><strong>目录</strong>{toc}</nav>
<main>
{body}
<footer>由 scripts/build-html.py 从 docs/research-report.md 生成；改内容请改 Markdown 再重新生成。</footer>
</main>
</div>
</body>
</html>
"""
(ROOT / "docs/research-report.html").write_text(html, encoding="utf-8")
print("wrote docs/research-report.html")
