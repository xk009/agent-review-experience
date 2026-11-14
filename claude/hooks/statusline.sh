#!/bin/bash
# ~/.claude/statusline.sh  （chmod +x，依赖 jq）
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(basename "$(echo "$input" | jq -r '.workspace.current_dir')")
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
FIVE=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty' | cut -d. -f1)
STYLE=$(echo "$input" | jq -r '.output_style.name // "default"')
BRANCH=$(git branch --show-current 2>/dev/null)

LINE="[$MODEL] $DIR"
[ -n "$BRANCH" ] && LINE="$LINE | $BRANCH"
LINE="$LINE | ctx $PCT%"
[ -n "$FIVE" ] && LINE="$LINE | 5h $FIVE%"
echo "$LINE | $STYLE"
