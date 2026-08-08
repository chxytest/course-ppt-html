# Changelog

## 1.0.0 (2026-08-08)

- 初始发布：6 阶段编排式 HTML 课程 PPT 生产线。
- 自包含设计：内置 `assets/template.html`、`references/`（确认 SOP / 踩坑册 / deck 规格 / IP 配图模板）、`scripts/`（Playwright 截图 + ffmpeg 合成）。
- 跨平台：支持 Claude Code / Codex（`npx skills add` 或 clone）与 ChatGPT（粘贴 SKILL.md 为指令）。
- 确认门 G0–G6 标准化，资料准备清单前置。
- 录制走「截图 + 合成」法，规避 headless Chromium 录不到 `<video>` 播放帧的问题。
