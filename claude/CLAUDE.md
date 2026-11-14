# 关于我
- 相机团队 Android 研发 + AI 研发提效负责人；主力 Kotlin/Java，Gradle 构建。
- 我主要在终端里 review 你的输出，注意力是瓶颈。

# 沟通约定（所有会话生效）
- 中文，结论先行：第一句回答"结果是什么"。
- 改完代码必须说明：改了哪些文件、为什么、怎么验证的、哪些没验证。
- 需要我拍板的点单独列出并给推荐选项；没有就不写这一节。
- 长内容（>80 行、多方案对比、图、diff review）走 HTML 报告，终端只放摘要 + 路径。
- HTML 报告统一放 `.claude-reports/`，文件名 `YYYYMMDD-HHMM-主题.html`。

# 项目验证命令（示例，按仓库替换）
- 编译：`./gradlew :app:assembleDebug`
- 单测：`./gradlew testDebugUnitTest`
