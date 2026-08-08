# Changelog

## 1.1.0 (2026-08-08)

- **移除阶段6「整本录制」**：该步骤为个人发视频用途，非课程 PPT 通用流程，从核心生产线剔除。
- 同步删除 `scripts/` 录制脚本（`capture.cjs` / `build_video.py`）、G6 确认门、踩坑册「整本录制」类。
- 阶段数 6 → 5；确认门 G0–G6 → G0–G5；`assets/template.html` 备注层/导出注释去掉「录制」措辞。
- 新增 `references/sample-prompts.md`：阶段3/4 的**样例提示词参考**（guizang 风格描述 / ian 角色卡+分镜），机制为「按需展示给用户调优、不写死、不强制弹」；样例内容待用户填入实际项目提示词后定稿。

## 1.0.0 (2026-08-08)

- 初始发布：6 阶段编排式 HTML 课程 PPT 生产线。
- 自包含设计：内置 `assets/template.html`、`references/`（确认 SOP / 踩坑册 / deck 规格 / IP 配图模板）、`scripts/`（Playwright 截图 + ffmpeg 合成）。
- 跨平台：支持 Claude Code / Codex（`npx skills add` 或 clone）与 ChatGPT（粘贴 SKILL.md 为指令）。
- 确认门 G0–G6 标准化，资料准备清单前置。
- 录制走「截图 + 合成」法，规避 headless Chromium 录不到 `<video>` 播放帧的问题。
