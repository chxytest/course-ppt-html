---
name: course-ppt-html
description: 编排式生成「单 HTML 文件交互课程/分享 PPT」的完整生产线，把"能横向翻页、有 IP 插画、有微动视频"的网页 PPT 拆成 5 个可控阶段（资料确认 → 框架梳理 → 文档版方案 → 单 HTML 生成 → IP 配图生成 → 视频生成嵌入），每阶段带用户确认门（G0–G5）与资料准备清单。本技能为编排器，推荐路径依赖 guizang-ppt-skill（阶段3 视觉系统）与 ian-xiaohei-illustrations（阶段4 IP 配图）两个核心技能，G0 前置检查确认其就绪（缺失则自动安装或走内置兜底）。当用户说「帮我做一份 HTML 版课程 PPT / 分享 PPT / 演讲 slides，主题：XXX」「把这篇内容做成网页 PPT」「生成带插画动画的 H5 课件」时触发。核心铁律：生图/视频必落本地 assets/ 且文件名对齐引用；批量重生成先删旧图。
---

# 课程 PPT · HTML 生产线（5 阶段编排）

> 定位：把"做一份能翻页、有 IP 插画、有微动视频"的网页 PPT 拆成可控阶段。
> 设计原则：**每个阶段结束都有用户确认门，不确认不进下一阶段**。需要用户给资料/拍板的地方，全部前置成标准化节点，不让用户反复在半成品上救火。
> 触发后先读 `references/confirmation-sop.md`（确认节点 + 资料清单）与 `references/pitfalls.md`（踩坑册），再按下方流程推进。

---

## 核心定位

为「一门课 / 一次分享 / 一场演讲」产出**单文件 HTML** 网页 PPT，可本地翻页、可录视频、可分发。需要：

- 个人 IP 形象配图（如汉堡 IP 小黑风）且跨图一致、零水印；

- 用户明确要"分阶段、先确认再继续"的协作方式。

本 skill 是**编排器**：它把两个核心能力技能串起来，贯穿 5 阶段输出成品。克隆本仓库即可运行（内置兜底模板 `assets/template.html` / `references/ip-illustration.md`），但**推荐路径依赖两个核心技能**——`guizang-ppt-skill`（阶段3 视觉系统）与 `ian-xiaohei-illustrations`（阶段4 IP 配图）。**G0 前置检查必须确认这两个技能已就绪**（缺失则自动安装或走降级）。完整说明见 `references/dependencies.md`。

---

## 先读这些参考（按阶段需要，不要一次塞满上下文）

- `references/dependencies.md`：两个核心依赖技能（guizang-ppt-skill / ian-xiaohei-illustrations）的作用、使用阶段、G0 前置检查与降级路径。
- `references/confirmation-sop.md`：G0–G5 确认门话术 + 用户侧资料准备清单。
- `references/pitfalls.md`：生图 / HTML / 视频 / 协作 4 类真实踩坑与预防。
- `references/html-deck-spec.md`：单文件 HTML deck 的规格（CSS 变量、翻页 JS、`syncVideos`、配图/视频容器写法）。
- `references/ip-illustration.md`：IP 插画提示词模板 + 多工具替代（GPT-Image / DALL·E / 小云雀 / 即梦）。
- `references/sample-prompts.md`：阶段3/4 **样例提示词参考**（guizang 风格描述 / ian 角色卡+分镜），**按需展示给用户调优，不写死、不强制弹**。
- `assets/template.html`：开箱即用的单文件 HTML deck 模板（含主题变量、翻页、视频同步、备注层）。


---

## 依赖技能（前置检查，必须）

本 skill 是**编排器**：它把下面两个核心能力技能串起来，贯穿 5 阶段输出成品。两个技能是**推荐路径的硬依赖**，G0 前置检查必须确认就绪（缺失则自动安装或走降级）。完整说明与检测/安装命令见 `references/dependencies.md`。

| 技能 | 作用 | 用于阶段 | 在流程中的角色 |
|---|---|---|---|
| `guizang-ppt-skill` | 单文件 HTML 网页 PPT 视觉系统（瑞士风 / 杂志风主题、版式、横翻页、动效） | **阶段3 · 单 HTML 生成** | 产出可翻页的 HTML 骨架与视觉风格（优先于内置 `assets/template.html`） |
| `ian-xiaohei-illustrations` | 个人 IP 角色配图风格 DNA + 提示词模板（图生图锁人物、跨图一致、零水印） | **阶段4 · IP 配图** | 产出跨图一致的 IP 插画（优先于内置 `references/ip-illustration.md`） |

**前置检查（G0 必做）**：
- 有 shell（Claude Code / Codex）：检测 skills 目录，缺失即自动 `npx skills add` 安装（命令见下）。
  ```bash
  npx skills add op7418/guizang-ppt-skill --skill guizang-ppt-skill
  npx skills add helloianneo/ian-xiaohei-illustrations --skill ian-xiaohei-illustrations
  ```
- 无 shell（ChatGPT）：向用户确认两技能是否已加载；若否，明确告知将走内置兜底（视觉 / IP 一致性较弱）并请用户确认。
- 内置 `assets/template.html` 与 `references/ip-illustration.md` **仅为降级兜底**，不替代官方技能。

---

## 何时使用

- 用户要给一门课 / 一次分享 / 一场演讲做**单文件 HTML** 网页 PPT（可本地翻页、可录视频、可分发）。
- 需要**个人 IP 形象配图**且要求跨图一致、零水印。
- 需要把插画做成**3 秒微动视频**并嵌进 PPT。
- 用户明确要"分阶段、先确认再继续"的协作方式。

**不适用**：纯文字报告、需要多人实时协作编辑的 PPT、大段表格数据堆叠（用常规 PPT 工具）。

---

## 总览：5 阶段 + 6 个确认门

```
G0 前置沟通（资料齐备）──► 阶段1 框架梳理 ──G1──► 阶段2 文档版方案 ──G2──►
阶段3 单 HTML 生成 ──G3──► 阶段4 IP 配图 ──G4──► 阶段5 视频生成嵌入 ──G5──► 交付
```

| 阶段 | 目标 | 主要工具（任选其一） | 确认门 |
|---|---|---|---|
| G0 前置 | 主题/受众/风格/IP 参考图齐备 | 对话 | 进阶段1 |
| 1 框架 | 大纲 + 逐页内容（不含视觉） | 对话/文档 | G1 |
| 2 方案 | 逐页视觉规划 + 配图 shot list | `references/confirmation-sop.md` 清单 | G2 |
| 3 生成 | 单 HTML 可翻页 | `assets/template.html` + `references/html-deck-spec.md` | G3 |
| 4 配图 | IP 形象一致、零水印 | `references/ip-illustration.md` + 任意生图工具 | G4 |
| 5 视频 | 插图会动 + 嵌入 | 小云雀/XYQ CLI 或本地视频模型 | G5 |

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
**工具**：**优先调用 `guizang-ppt-skill`** 产出单 HTML 视觉底座（瑞士风 / 杂志风主题、版式、横翻页、动效）；若该技能不可用，则基于内置 `assets/template.html`（复制为 `index.html` 后填充）。deck 规格见 `references/html-deck-spec.md`。
**样例提示词**：风格/主题色描述样例见 `references/sample-prompts.md`（guizang 段）。进入阶段3 时**可按需**展示给用户调优风格与主题色——**不强制弹**，仅在用户需要或你判断有助于对齐时展示，确认后再生成。
**关键注意**（详见 `references/pitfalls.md` 的 HTML/CSS 段）：
- 图片容器用 `object-fit:contain` + `overflow:visible` + `height:auto`，**不要** `cover`+`hidden`（会裁图）。
- 过渡/居中类修改用 CSS 规则加 `!important`，不要依赖内联 style（易被缓存/覆盖）。
- 交付本地预览（如 `http://localhost:8080/index.html` 或起一个静态服务器），让用户能直接在浏览器查看。

**G3 确认点**：用户签字"HTML 视觉定稿（风格/排版/动效）"后，进阶段4。

---

## 阶段 4 · IP 配图生成（G4）⭐ 最高频踩坑区

**目标**：生成跨图一致、零水印的 IP 配图，落本地。
**工具**：**优先调用 `ian-xiaohei-illustrations`** 产出 IP 配图 shot list 与提示词（图生图锁人物、跨图一致、零水印）；若该技能不可用，则用内置 `references/ip-illustration.md`（含多工具替代矩阵）。生图工具任选：GPT-Image / DALL·E / 小云雀 / 即梦 / Midjourney。
**样例提示词**：角色卡 + 分镜动作样例见 `references/sample-prompts.md`（ian 段）。进入阶段4 时**可按需**展示给用户调优角色/动作/标注词——**不强制弹**，确认后再生成。
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

**G5 确认点**：用户确认"视频页范围 + 嵌入方式（自动播/点击播）"后，进交付（成品 PPT 完成）。

---


## 贯穿全程的执行铁律

1. 🔴 生图/视频必落本地 `assets/`，文件名对齐 HTML 引用。
2. 批量重生成前先删旧图。
3. 视频生成必带限频退避 + 幂等跳过重文件 + 轮询 ≥40 次。
4. 方案→实现后逐页 checklist 对账（配图/画板/视频标记逐页核销）。
5. 用补丁绕过的问题必须当轮回写主流程。

---

## 运行环境适配

- **在 Claude Code / Codex 中**：用普通对话直接问用户确认（无 `AskUserQuestion` 就用纯文本提问）；本地预览用 `python3 -m http.server` 起服务。
- **在 ChatGPT（无 shell）中**：你负责规划、写 HTML、出提示词；生图/视频由用户按提示词去小云雀 / DALL·E / 即梦执行，再把文件放回 `assets/`。
- **安装本 skill**：见 `README.md`（`npx skills add` 或 clone 到 `~/.claude/skills/` / `~/.codex/skills/`）。

---

## 核心依赖技能（前置检查必须）

本 skill 在 **阶段3 / 阶段4** 推荐直接调用下面两个核心技能（G0 前置检查确认就绪）：

- `guizang-ppt-skill`：单文件 HTML 网页 PPT 视觉系统（电子杂志风 / 瑞士国际主义，多套主题与版式）。安装：`npx skills add op7418/guizang-ppt-skill --skill guizang-ppt-skill`。**用于阶段3** 产出 HTML 视觉底座。
- `ian-xiaohei-illustrations`：个人 IP 角色配图风格 DNA + 提示词模板（图生图锁人物、跨图一致、零水印）。安装：`npx skills add helloianneo/ian-xiaohei-illustrations --skill ian-xiaohei-illustrations`。**用于阶段4** 产出 IP 配图。

> 调用这两个技能时请遵守其各自的 License 与使用边界。内置 `assets/template.html` / `references/ip-illustration.md` 仅为降级兜底，不替代官方技能。完整前置检查流程见 `references/dependencies.md`。

---

## 复用资产索引（全部在本仓库内）

- `assets/template.html`：阶段3 单文件 HTML deck 起点。
- `references/html-deck-spec.md`：deck 规格（CSS 变量 / 翻页 / syncVideos / 容器写法）。
- `references/ip-illustration.md`：阶段4 IP 配图提示词模板 + 多工具替代。
- `references/sample-prompts.md`：阶段3/4 样例提示词参考（按需展示给用户调优，不写死）。
- `references/dependencies.md`：两个核心依赖技能的作用、使用阶段、G0 前置检查与降级路径。
- `references/confirmation-sop.md`：G0–G5 确认门 + 资料清单。
- `references/pitfalls.md`：5 类真实踩坑与预防。


**详细踩坑册**见 `references/pitfalls.md`；**确认节点 + 资料清单**见 `references/confirmation-sop.md`。
