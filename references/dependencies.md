# 依赖技能 · 前置检查与说明

`course-ppt-html` 是一个**编排型技能**：它自己不生产视觉资产，而是把两个核心能力技能串起来，贯穿 5 阶段流程，输出「能翻页、有 IP 插画、有微动视频」的单文件 HTML PPT。

这两个技能是**推荐路径的硬依赖**——本仓库内置了最小可用的兜底模板（`assets/template.html` / `references/ip-illustration.md`），但**官方推荐路径**依赖这两个技能以获得完整的视觉系统与一致的 IP 风格。**G0 前置检查必须确认它们已就绪。**

---

## 一、依赖清单与作用

| 技能 | 一句话作用 | 主要使用阶段 | 在流程中的角色 |
|---|---|---|---|
| `guizang-ppt-skill` | 单文件 HTML 网页 PPT 的视觉系统（瑞士国际主义 / 电子杂志风主题、版式、横翻页、动效） | **阶段3 · 单 HTML 生成** | 产出可翻页的 HTML 骨架与视觉风格 |
| `ian-xiaohei-illustrations` | 个人 IP 角色配图风格 DNA + 提示词模板（图生图锁人物、跨图一致、零水印） | **阶段4 · IP 配图生成** | 产出跨图一致的 IP 插画 |

### guizang-ppt-skill —— 用于阶段3
- 提供多套成熟主题（如「瑞士国际主义」「电子杂志 × 电子墨水」），含 CSS 变量、横翻页 JS、章节幕封、数据大字报、图片网格等版式与 WebGL 背景。
- `course-ppt-html` 阶段3 生成 HTML 时，**优先调用 `guizang-ppt-skill` 产出 HTML 视觉底座**（或以其模板为基底）；本仓库 `assets/template.html` 仅作为该技能缺失时的兜底骨架。
- 两者可共存：用 guizang 出视觉底座，再用 `course-ppt-html` 的 video 同步（`syncVideos`）、备注层（N 键）、接管后续阶段4–5。

### ian-xiaohei-illustrations —— 用于阶段4
- 提供 IP 角色的风格定义（线条 / 配色 / 比例）、图生图参考图锁定方式、零水印要点。
- `course-ppt-html` 阶段4 生成 IP 配图时，**优先调用 `ian-xiaohei-illustrations` 产出 shot list 与提示词**；本仓库 `references/ip-illustration.md` 作为该技能缺失时的兜底模板。
- 铁律不变：图生图锁人物、跨图一致、零水印、必落本地 `assets/` 且文件名对齐引用。

---

## 二、前置检查（G0 必做，进入阶段1 之前）

### 1. 检测是否已安装
- **Claude Code / Codex（有 shell）**：
  ```bash
  ls -d "${CLAUDE_SKILLS:-$HOME/.claude/skills}/guizang-ppt-skill" 2>/dev/null && echo "guizang OK" || echo "guizang MISSING"
  ls -d "${CODEX_SKILLS:-$HOME/.codex/skills}/guizang-ppt-skill" 2>/dev/null && echo "guizang OK(codex)" || true
  ls -d "$HOME/.claude/skills/ian-xiaohei-illustrations" 2>/dev/null && echo "ian OK" || echo "ian MISSING"
  ```
- **ChatGPT（无 shell）**：无法自动检测。在 G0 向用户确认「是否已加载这两个技能 / 是否可提供其提示词模板」；若否，走内置兜底并明确告知降级。

### 2. 缺失时的处理
- **环境支持 shell 且缺失**：自动执行安装（命令见下），安装成功后继续。
- **环境不支持 shell（如 ChatGPT）且缺失**：明确告知用户将使用内置兜底模板——视觉效果与 IP 一致性会弱于官方技能——请用户确认是否接受；或请用户先安装两个技能再继续。

### 3. 安装命令（权威）
```bash
# guizang-ppt-skill —— 阶段3 视觉系统
npx skills add op7418/guizang-ppt-skill --skill guizang-ppt-skill

# ian-xiaohei-illustrations —— 阶段4 IP 配图
npx skills add helloianneo/ian-xiaohei-illustrations --skill ian-xiaohei-illustrations
```
> 也可手动 clone 到对应的 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/`）。

---

## 三、降级路径（仅当依赖确实不可用）

| 缺失 | 降级方案 | 影响 |
|---|---|---|
| 无 `guizang-ppt-skill` | 用 `assets/template.html` 出 HTML | 功能完整，视觉风格较基础（无多主题/WebGL 背景） |
| 无 `ian-xiaohei-illustrations` | 用 `references/ip-illustration.md` 提示词模板（含多工具替代矩阵） | IP 风格需手动对齐，一致性弱于官方技能 |

降级时**必须在 G0 向用户说明**，并记录进最终交付说明。

---

## 四、使用边界

- 两个技能各自有 License 与使用边界，调用时遵守其约定。
- `course-ppt-html` 仅负责**串联与编排**，不修改依赖技能的内部逻辑；若依赖技能自身更新，以其最新版为准。
- 推荐路径下，阶段3 产物（guizang HTML）与阶段4 产物（ian 配图）通过 `course-ppt-html` 的引用对齐规则（`pNN.jpeg` / `vNN.mp4`）与视频同步（`syncVideos`）对接，无需改依赖技能源码。
