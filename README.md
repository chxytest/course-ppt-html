# course-ppt-html

> 编排式生成「单 HTML 文件交互课程/分享 PPT」的完整生产线。

把"能横向翻页、有 IP 插画、有微动视频"的网页 PPT，拆成 **5 个可控阶段**（资料确认 → 框架梳理 → 文档版方案 → 单 HTML 生成 → IP 配图生成 → 视频生成嵌入），每阶段带**用户确认门（G0–G5）**与资料准备清单。

**本 skill 自带兜底模板可独立运行**：克隆本仓库即可跑（内置 `assets/template.html` / `references/ip-illustration.md` 作为降级兜底）。**推荐路径依赖两个核心技能**——`guizang-ppt-skill`（阶段3 视觉系统）与 `ian-xiaohei-illustrations`（阶段4 IP 配图）——**G0 前置检查会确认其就绪**（缺失则自动安装或走降级）。内置：
- `assets/template.html` — 开箱即用的单文件 HTML deck 模板（主题变量 / 翻页 / 视频同步 / 备注层，降级兜底用）
- `references/` — 确认 SOP、踩坑册、deck 规格、IP 配图提示词模板、依赖技能说明

---

## 安装

### Claude Code / Codex（有 shell）

```bash
# 方式一：skills CLI（推荐，自动装到 skills 目录）
npx skills add chxytest/course-ppt-html --skill course-ppt-html

# 方式二：手动 clone
git clone https://github.com/chxytest/course-ppt-html.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"   # 或 ~/.claude/skills
cp -R ./course-ppt-html "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后在 Agent 里直接说：

> 用 course-ppt-html 做一份 HTML 版课程 PPT，主题：如何成为一个 AI 时代的 OPC

### ChatGPT（自定义 GPT / Project）

1. 把本仓库 `SKILL.md` 全文 + `references/` 内容作为**知识/指令**粘贴进自定义 GPT 的 Instructions。
2. 让 GPT 负责规划、写 HTML、出配图提示词；生图/视频由你按提示词去 DALL·E / 小云雀 / 即梦执行，再把文件放回 `assets/`。

### WorkBuddy（原生支持 · 推荐）

WorkBuddy 的技能目录是 **`~/.workbuddy/skills/`**，把本仓库放进去即可被原生识别和调用，且能直接用到 WorkBuddy 专属能力（确认门交互、本地预览、文件分享、设计画布）。

```bash
# 方式一：git clone 到技能目录（推荐，便于后续 pull 更新）
git clone https://github.com/chxytest/course-ppt-html.git ~/.workbuddy/skills/course-ppt-html

# 方式二：已在本机有副本，直接 rsync（排除 .git / .DS_Store）
rsync -a --exclude='.git' --exclude='.DS_Store' \
  /path/to/course-ppt-html/ ~/.workbuddy/skills/course-ppt-html/
```

安装后在 WorkBuddy 对话框直接说：

> 用 course-ppt-html 做一份 HTML 版课程 PPT，主题：如何成为一个 AI 时代的 OPC

**WorkBuddy 原生存用优势**（相比纯文本 Agent）：

- **确认门交互**：阶段间的 G0–G5 用 WorkBuddy 的原生提问/选项卡片与用户对齐，比纯文本更顺。
- **本地预览与文件分享**：阶段3 起用本地静态服务器（`http://localhost:8080`）起预览，并用 `present_files` 直接在对话框内打开 HTML / 图片 / 视频，用户无需手动找文件。
- **设计画布（Ardot）**：若需要把 HTML 稿同步到 Ardot 设计画布做像素级微调，可接 `ardot-html-sync` / `ardot-prototype-replica` 技能。
- **依赖技能已就位**：`guizang-ppt-skill`（阶段3）与 `ian-xiaohei-illustrations`（阶段4）通常已装在 `~/.workbuddy/skills/`；G0 前置检查会确认，缺失则自动 `npx skills add` 或提示安装。
- **生图/视频链路**：WorkBuddy 可直接调 `gpt-image-2` / 小云雀 CLI（`xyq`）等生图，以及视频生成技能，无需用户手动搬运文件。

---

## 快速开始（5 阶段）

| 阶段 | 目标 | 确认门 |
|---|---|---|
| G0 前置 | 主题/受众/风格/IP 参考图齐备 | 进阶段1 |
| 1 框架 | 大纲 + 逐页核心信息（不含视觉） | G1 |
| 2 方案 | 逐页视觉规划 + 配图 shot list | G2 |
| 3 生成 | 单 HTML 可翻页 | G3 |
| 4 配图 | IP 形象一致、零水印 | G4 |
| 5 视频 | 插图会动 + 嵌入 | G5 |

每个确认门都**不确认不进下一阶段**。详细话术与资料清单见 `references/confirmation-sop.md`。

---

## 目录结构

```
course-ppt-html/
├── SKILL.md                      # 技能主文件（编排流程 + 铁律）
├── README.md                    # 本文件
├── LICENSE                      # MIT
├── VERSION                      # 版本号（与 CHANGELOG 对齐）
├── CHANGELOG.md
├── assets/
│   └── template.html            # 单文件 HTML deck 模板（复制为 index.html 后填充）
└── references/
│   ├── dependencies.md          # 两个核心依赖技能的作用/使用阶段/G0 前置检查/降级路径
│   ├── confirmation-sop.md      # G0–G5 确认门 + 用户资料清单
│   ├── pitfalls.md              # 4 类真实踩坑与预防
│   ├── html-deck-spec.md        # deck 规格（CSS 变量/翻页/syncVideos/容器写法）
│   ├── ip-illustration.md       # IP 配图提示词模板 + 多工具替代
│   └── sample-prompts.md        # 阶段3/4 样例提示词参考（按需展示调优，不写死）
```

---


## 核心依赖技能（前置检查必须）

本 skill 是编排器，在 **阶段3 / 阶段4** 推荐直接调用下面两个核心技能。**G0 前置检查会确认它们已就绪**（有 shell 时缺失自动 `npx skills add` 安装；无 shell 时请用户确认或走内置兜底）：

- **guizang-ppt-skill** — 单文件 HTML 网页 PPT 视觉系统（电子杂志风 / 瑞士国际主义）。**用于阶段3** 产出 HTML 视觉底座。
  `npx skills add op7418/guizang-ppt-skill --skill guizang-ppt-skill`
- **ian-xiaohei-illustrations** — 个人 IP 角色配图风格 DNA + 提示词模板（图生图锁人物、跨图一致、零水印）。**用于阶段4** 产出 IP 配图。
  `npx skills add helloianneo/ian-xiaohei-illustrations --skill ian-xiaohei-illustrations`

> 调用这两个技能时请遵守其各自的 License 与使用边界。内置 `assets/template.html` / `references/ip-illustration.md` 仅为降级兜底，不替代官方技能。完整前置检查流程见 `references/dependencies.md`。

---

## License

MIT © course-ppt-html contributors
