# agent-review-experience 工作约定

本仓库是「提升人类审阅 Coding Agent 产物的效率与体验」的统一产物源：
https://github.com/xk009/agent-review-experience

## 目标与边界
- 优化人工形成可靠判断的时间，而不只是输出的美观或篇幅。
- 本主题的新文档、prompt、配置、skill 和后续 app 源码优先维护在本仓库。
- `claude/CLAUDE.md` 是可安装的用户配置示例；本文件是仓库维护约定，二者不可混淆。
- 已有资产先复用；不要另建重复的规则、报告或目录。

## 写入与验证
- 目录、命名、来源与公开发布边界见 `docs/asset-conventions.md`。
- 面向人的交付先给结果、关键变化、优先审阅入口、验证与缺口。
- 软件功能和配置以官方文档核实，写明核对日期；不要把文档支持写成本机验证通过。
- 修改脚本后运行对应测试；未执行 Claude Code 或终端端到端验证时如实注明。
- 更新已有文件前读取当前内容；提交前检查差异，不覆盖他人的并行改动。
- 不自动安装到用户全局配置，不改权限策略，不自动升级 CLI。
- 仓库为公开用途：不得提交公司源码、内部任务记录、令牌、私人路径或未脱敏日志。
- 不将“统一产物仓库”理解为每个业务任务的原始审阅证据都应公开上传。

## 当前审阅闭环
入口：`docs/review-workflow.md`。
常驻规则：`claude/rules/review-first.md`。
按需流程：`claude/skills/review-package/`。
只读预审：`claude/agents/review-auditor.md`。
