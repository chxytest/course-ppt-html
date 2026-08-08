# Changelog

## 1.2.3 (2026-08-08)
- 把「依赖技能内置风格速查」同步进 SKILL.md 的「核心依赖技能」章节（guizang 2 风格 + 主题色/版式清单、ian 风格 DNA + 原仓库地址，并加"按需展示确认"提示）。

## 1.2.2 (2026-08-08)

- **README 新增「依赖技能内置风格速查」段**：说明 guizang-ppt-skill 内置 2 套风格（电子杂志风 5 套主题色 / 瑞士风 4 套功能色 + 22 版式）与 ian-xiaohei-illustrations 内置风格 DNA（汉堡 IP、浅灰洁净背景、3D转2D 手办质感、红橙蓝批注），并附两技能原 GitHub 地址；注明"用户问可直接发清单，或访问原仓库查看完整细节"。

## 1.2.1 (2026-08-08)

- **补全 WorkBuddy 接入说明**（用户指出原 docs 只写了 Claude/Codex/ChatGPT，缺 WorkBuddy 自身）：
  - `README.md` 新增「WorkBuddy（原生支持 · 推荐）」安装段：clone 到 `~/.workbuddy/skills/` 或 rsync 同步；列举 WorkBuddy 专属优势（确认门原生交互 / `present_files` 预览分享 / Ardot 画布 / 依赖技能已就位 / 生图视频直调）。
  - `SKILL.md`「运行环境适配」新增 WorkBuddy 条目；安装指引改为四平台并列（WorkBuddy / Claude / Codex / ChatGPT）。

## 1.2.0 (2026-08-08)

- **定稿 `references/sample-prompts.md`**：用 OPC 项目的**真实用户提示词原文**替换原反向推导样例。按 5 段组织 —— ① PPT+IP 配图总调度（阶段3+4）② 个人 IP 三视图（阶段4 前置 ★可复用）③ 文档版 PPT 方案（阶段2 ★可复用）④ 配图转视频（阶段5）⑤ ian 适配成自己 IP 形象（阶段4 风格迁移）。
- 保留「不写死、不强制弹」机制：样例仅作沟通调优锚点，每次新项目须展示→用户改→确认后再生成。
- 同步更新 SKILL.md 四处引用（资源清单 + 阶段3/4 样例引导 + 末尾资源索引）指向新的 5 段结构。

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
