#!/bin/bash
# PostToolUse hook（matcher: Write）：Claude 写出 .html 文件后用浏览器自动打开（macOS `open`）。
# 与 claude/settings.json 中内联的 command 等价，二选一即可。依赖 jq。
# 注意（未实测）：每次 Write 都会开一个新标签页；频繁迭代时改用 live-server。
f=$(jq -r '.tool_input.file_path // empty')
case "$f" in
  *.html) open "$f" ;;
esac
exit 0
