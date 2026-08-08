---
name: course-ppt-html
description: 编排式生成「单 HTML 文件交互课程/分享 PPT」的完整生产线。把"能横向翻页、有 IP 插画、有微动视频、能录成成片"的网页 PPT 拆成 6 个可控阶段（资料确认 → 框架梳理 → 文档版方案 → 单 HTML 生成 → IP 配图生成 → 视频生成嵌入 → 整本录制），每阶段带用户确认门（G0–G6）与资料准备清单。内置自包含单文件 HTML deck 模板（assets/template.html）、IP 插画提示词模板（references/ip-illustration.md）、以及 Playwright+ffmpeg 录制脚本（scripts/）。当用户说「帮我做一份 HTML 版课程 PPT / 分享 PPT / 演讲 slides，主题：XXX」「把这篇内容做成网页 PPT」「生成带插画动画的 H5 课件」时触发。核心铁律：生图/视频必落本地 assets/ 且文件名对齐引用；批量重生成先删旧图；带 video 的页面录制走「截图+合成」法。
---

# 课程 PPT · HTML 生产线（6 阶段编排）

> 定位：把"做一份能翻页、有 IP 插画、有微动视频、能录成成片"的网页 PPT 拆成可控阶段。
> 设计原则：**每个阶段结束都有用户确认门，不确认不进下一阶段**。需要用户给资料/拍板的地方，全部前置成标准化节点，不让用户反复在半成品上救火。
> 触发后先读 `references/confirmation-sop.md`（确认节点 + 资料清单）与 `references/pitfalls.md`（踩坑册），再按下方流程推进。

---

## 核心定位

为「一门课 / 一次分享 / 一场演讲」产出**单文件 HTML** 网页 PPT，可本地翻页、可录视频、可分发。需要：

- 个人 IP 形象配图（如汉堡 IP 小黑风）且跨图一致、零水印；
- 把插画做成 **3 秒微动视频**并嵌进 PPT，或把整本 PPT **录成一段视频**；
- 用户明确要"分阶段、先确认再继续"的协作方式。

本 skill 是**自包含**的：克隆本仓库即可运行，无需额外的私有资产。可选的更丰富视觉风格来自两个上游 skill（见文末「可选上游依赖」），但**不安装也能用**——`assets/template.html` 与 `references/ip-illustration.md` 已提供够用的内联方案。

---

## 先读这些参考（按阶段需要，不要一次塞满上下文）

- `references/confirmation-sop.md`：G0–G6 确认门话术 + 用户侧资料准备清单。
- `references/pitfalls.md`：生图 / HTML / 视频 / 录制 / 协作 5 类真实踩坑与预防。
- `references/html-deck-spec.md`：单文件 HTML deck 的规格（CSS 变量、翻页 JS、`syncVideos`、配图/视频容器写法）。
- `references/ip-illustration.md`：IP 插画提示词模板 + 多工具替代（GPT-Image / DALL·E / 小云雀 / 即梦）。
- `assets/template.html`：开箱即用的单文件 HTML deck 模板（含主题变量、翻页、视频同步、备注层）。
- `scripts/capture.cjs` + `scripts/build_video.py`：整本录制的「截图 + 合成」脚本。

---

## 何时使用

- 用户要给一门课 / 一次分享 / 一场演讲做**单文件 HTML** 网页 PPT（可本地翻页、可录视频、可分发）。
- 需要**个人 IP 形象配图**且要求跨图一致、零水印。
- 需要把插画做成**3 秒微动视频**并嵌进 PPT，或把整本 PPT**录成一段视频**。
- 用户明确要"分阶段、先确认再继续"的协作方式。

**不适用**：纯文字报告、需要多人实时协作编辑的 PPT、大段表格数据堆叠（用常规 PPT 工具）。

---

## 总览：6 阶段 + 7 个确认门

```
G0 前置沟通（资料齐备）──► 阶段1 框架梳理 ──G1──► 阶段2 文档版方案 ──G2──►
阶段3 单 HTML 生成 ──G3──► 阶段4 IP 配图 ──G4──► 阶段5 视频生成嵌入 ──G5──►
阶段6 整本录制 ──G6──► 交付
```

| 阶段 | 目标 | 主要工具（任选其一） | 确认门 |
|---|---|---|---|
| G0 前置 | 主题/受众/风格/IP 参考图齐备 | 对话 | 进阶段1 |
| 1 框架 | 大纲 + 逐页内容（不含视觉） | 对话/文档 | G1 |
| 2 方案 | 逐页视觉规划 + 配图 shot list | `references/confirmation-sop.md` 清单 | G2 |
| 3 生成 | 单 HTML 可翻页 | `assets/template.html` + `references/html-deck-spec.md` | G3 |
| 4 配图 | IP 形象一致、零水印 | `references/ip-illustration.md` + 任意生图工具 | G4 |
| 5 视频 | 插图会动 + 嵌入 | 小云雀/XYQ CLI 或本地视频模型 | G5 |
| 6 录制 | 整本成片 | `scripts/capture.cjs` + `scripts/build_video.py` | G6 |

---

## 阶段 0 · 前置沟通（G0）

**目标**：确认资料齐备，避免后期返工。
**必读**：`references/confirmation-sop.md` → 「用户侧资料准备清单」。

执行：
1. 逐项对齐：主题、受众、演讲/阅读时长、视觉风格（瑞士风 / 杂志风二选一）、个人 IP 参考图（三视图或代表图）是否就绪、有无已有文章/大纲。
2. 若用户已给完整大纲 + 素材，可跳过澄清直接进阶段1。
3. **G0 确认点**：以上资料齐备，用户说"开始/进下一阶段"后，才进阶段1。

---

## 阶段 1 · 框架与内容梳理（G1）

**目标**：把内容骨架定对（这一阶段**不碰视觉**）。
**做法**：
- 基于用户素材梳理结构：开场 → 核心概念 → 方法/步骤 → 案例 → 总结 + 行动号召 → 附录。
- 产出大纲 + 逐页「页码/标题/核心信息」表（先不写布局/配图）。

**G1 确认点**：用户签字"大纲和逐页核心信息 OK"后，进阶段2。

---

## 阶段 2 · 文档版 PPT 方案设计（G2）

**目标**：在**不生成 HTML、不写页面代码**前提下，产出逐页视觉规划，与用户对齐。
**做法**：
- 填 7 列逐页表：页码 / 标题 / 核心信息 / 建议布局 / 是否需要配图 / 是否需要画板 / 讲稿备注。
- 明确：哪些页要 IP 配图（先出 shot list，4–8 张）、哪些页要可编辑画板、哪些页适合视频切片。
- **方案 → 实现的对账清单在此阶段就定好**，避免阶段3后漏项。

**G2 确认点**：用户签字"逐页视觉规划 + 配图 shot list OK"后，进阶段3。

---

## 阶段 3 · 生成单 HTML PPT（G3）

**目标**：产出可翻页的单 HTML。
**工具**：基于 `assets/template.html`（复制为 `index.html` 后填充），规格见 `references/html-deck-spec.md`。
**关键注意**（详见 `references/pitfalls.md` 的 HTML/CSS 段）：
- 图片容器用 `object-fit:contain` + `overflow:visible` + `height:auto`，**不要** `cover`+`hidden`（会裁图）。
- 过渡/居中类修改用 CSS 规则加 `!important`，不要依赖内联 style（易被缓存/覆盖）。
- 交付本地预览（如 `http://localhost:8080/index.html` 或起一个静态服务器），让用户能直接在浏览器查看。

**G3 确认点**：用户签字"HTML 视觉定稿（风格/排版/动效）"后，进阶段4。

---

## 阶段 4 · IP 配图生成（G4）⭐ 最高频踩坑区

**目标**：生成跨图一致、零水印的 IP 配图，落本地。
**工具**：`references/ip-illustration.md`（风格 DNA + 提示词模板）+ 任意生图工具（GPT-Image / DALL·E / 小云雀 / 即梦 / Midjourney）。
**🔴 执行铁律（必须严格遵守，详见 `references/pitfalls.md` 生图链路段）**：
1. **每次生图必落本地 `assets/`，文件名与 HTML 引用严格对齐**（如 `p03.jpeg`）。
2. **批量重生成前先删旧图**（杜绝 skip 逻辑残留旧图）。
3. 人物一致性：一律走**图生图（image-to-image）+ 角色参考图锁定**，纯文生图必漂移。
4. 水印：平台开"去除 AIGC 水印"开关优先，prompt 加 `ABSOLUTELY NO watermark` 辅助。
5. 🔴 **用一次性补丁绕过的问题 = 未修复**——凡是需"额外跑脚本"才能完成的，必须当轮回写主流程。

**G4 确认点**：用户看样张签字"人物一致/零水印/字体 OK"后，进阶段5。

---

## 阶段 5 · 视频生成与嵌入（G5）

**目标**：给指定页配图生成 3 秒微动视频，嵌入 PPT 自动播放。
**工具**：小云雀/XYQ CLI `generate-video`（若有）；否则用任意本地/云端视频模型。
**做法**：
- 视频页 `<img>` → `<video src="assets/vNN.mp4" poster="assets/pNN.jpeg" muted loop playsinline preload="metadata">`。
- 导航 `go()` 注入 `syncVideos(idx)`：进页 `play()`、离页 `pause()`+`currentTime=0`；`syncVideos` 用通用实现（遍历每页 `.frame-img > video`），新增页无需改 JS。规格见 `references/html-deck-spec.md`。
**关键注意**：
- 视频比图片慢（单页数分钟），**轮询上限 ≥40 次（8 分钟）**。
- 必带**限频退避重试**（60/90/120/150s）+ 每页间隔 20s + 幂等跳过重文件（防 `操作过于频繁` 类限频）。
- 落本地铁律同样适用：视频 rename 为 `vNN.mp4` 对齐引用。

**G5 确认点**：用户确认"视频页范围 + 嵌入方式（自动播/点击播）"后，进阶段6。

---

## 阶段 6 · 整本录制视频（G6）

**目标**：把全部页面翻页过程录成一段视频，每页 ≤5s，只录网页内容区（视口非全屏）。
**🔴 关键结论**：headless Chromium 的 Playwright `recordVideo` **录不到 `<video>` 播放帧**（录出来是冻结 poster，帧差≈0）。必须走**「截图 + 合成」法**（见 `references/pitfalls.md` 录制段 + `scripts/`）。
**做法**：
1. Playwright 翻页 `window.go(i)`，每页等 **1.2s 让动画 settle**。
2. 截图前用 JS `visibility:hidden` **隐藏 `<video>`**（避免底图带 poster → 双重图像），截干净底图后再恢复。
3. 用 JS `getBoundingClientRect()` 取 video 在 1280×720 视口内的精确坐标（必须在视口内，溢出即截图未 settle）。
4. ffmpeg 把真实 `vNN.mp4` 按 **object-fit:contain** 算裁剪框，overlay 回原坐标；视频页 4s、静态页 3s；全部段 concat。
5. 环境：用 `ffmpeg-static` 静态二进制（系统 ffmpeg 在某些 macOS 上损坏缺 libxcb）；`vNN.mp4` 真实尺寸非 1280×720 → 必须探测真实分辨率算 contain，不能假设。

脚本：`scripts/capture.cjs`（截图+取坐标+隐藏 video）、`scripts/build_video.py`（合成+contain 对齐），路径均已参数化。

**G6 确认点**：用户确认"录制参数（停留/视口/音轨）"后，交付成片（如 `course-ppt-video.mp4`）。

---

## 贯穿全程的执行铁律

1. 🔴 生图/视频必落本地 `assets/`，文件名对齐 HTML 引用。
2. 批量重生成前先删旧图。
3. 视频生成必带限频退避 + 幂等跳过重文件 + 轮询 ≥40 次。
4. 截图前动画完全 settle；叠加元素截图时先隐藏。
5. 方案→实现后逐页 checklist 对账（配图/画板/视频标记逐页核销）。
6. 用补丁绕过的问题必须当轮回写主流程。

---

## 运行环境适配

- **在 Claude Code / Codex 中**：用普通对话直接问用户确认（无 `AskUserQuestion` 就用纯文本提问）；本地预览用 `python3 -m http.server` 起服务。
- **在 ChatGPT（无 shell）中**：你负责规划、写 HTML、出提示词；生图/视频由用户按提示词去小云雀 / DALL·E / 即梦执行，再把文件放回 `assets/`。录制脚本（Playwright+ffmpeg）在用户本地或 Codex 环境跑。
- **安装本 skill**：见 `README.md`（`npx skills add` 或 clone 到 `~/.claude/skills/` / `~/.codex/skills/`）。

---

## 可选上游依赖（不安装也能用）

- `guizang-ppt-skill`：更丰富的网页 PPT 视觉系统（电子杂志风 / 瑞士国际主义，多套主题与版式）。安装：`npx skills add op7418/guizang-ppt-skill --skill guizang-ppt-skill`。阶段3 可直接调用它替代 `assets/template.html`。
- `ian-xiaohei-illustrations`：怪诞手绘正文配图风格。安装：`npx skills add helloianneo/ian-xiaohei-illustrations --skill ian-xiaohei-illustrations`。阶段4 可调用它替代 `references/ip-illustration.md` 的提示词模板。

> 若使用上游 skill，请遵守其各自的 License 与使用边界。

---

## 复用资产索引（全部在本仓库内）

- `assets/template.html`：阶段3 单文件 HTML deck 起点。
- `references/html-deck-spec.md`：deck 规格（CSS 变量 / 翻页 / syncVideos / 容器写法）。
- `references/ip-illustration.md`：阶段4 IP 配图提示词模板 + 多工具替代。
- `references/confirmation-sop.md`：G0–G6 确认门 + 资料清单。
- `references/pitfalls.md`：5 类真实踩坑与预防。
- `scripts/capture.cjs` + `scripts/build_video.py`：阶段6 录制「截图+合成」。

**详细踩坑册**见 `references/pitfalls.md`；**确认节点 + 资料清单**见 `references/confirmation-sop.md`。
