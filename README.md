# course-ppt-html

> 编排式生成「单 HTML 文件交互课程/分享 PPT」的完整生产线。

把"能横向翻页、有 IP 插画、有微动视频、能录成成片"的网页 PPT，拆成 **6 个可控阶段**（资料确认 → 框架梳理 → 文档版方案 → 单 HTML 生成 → IP 配图生成 → 视频生成嵌入 → 整本录制），每阶段带**用户确认门（G0–G6）**与资料准备清单。

**本 skill 自包含**：克隆本仓库即可运行，无需任何私有资产。内置：
- `assets/template.html` — 开箱即用的单文件 HTML deck 模板（主题变量 / 翻页 / 视频同步 / 备注层）
- `references/` — 确认 SOP、踩坑册、deck 规格、IP 配图提示词模板
- `scripts/` — 整本录制的「截图 + 合成」Playwright + ffmpeg 脚本

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
3. 录制脚本（`scripts/`）在你的本地终端或 Codex 环境运行。

---

## 快速开始（6 阶段）

| 阶段 | 目标 | 确认门 |
|---|---|---|
| G0 前置 | 主题/受众/风格/IP 参考图齐备 | 进阶段1 |
| 1 框架 | 大纲 + 逐页核心信息（不含视觉） | G1 |
| 2 方案 | 逐页视觉规划 + 配图 shot list | G2 |
| 3 生成 | 单 HTML 可翻页 | G3 |
| 4 配图 | IP 形象一致、零水印 | G4 |
| 5 视频 | 插图会动 + 嵌入 | G5 |
| 6 录制 | 整本成片 | G6 交付 |

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
├── references/
│   ├── confirmation-sop.md      # G0–G6 确认门 + 用户资料清单
│   ├── pitfalls.md              # 5 类真实踩坑与预防
│   ├── html-deck-spec.md        # deck 规格（CSS 变量/翻页/syncVideos/容器写法）
│   └── ip-illustration.md       # IP 配图提示词模板 + 多工具替代
└── scripts/
    ├── capture.cjs              # 截图 + 取视频坐标 + 隐藏 video（Playwright）
    └── build_video.py           # ffmpeg 合成（contain 对齐 + concat）
```

---

## 录制整本视频（阶段6）

```bash
# 1) 起静态服务器
cd your-project && python3 -m http.server 8099

# 2) 截图 + 取视频坐标（隐藏 video 避免重影）
BASE_URL=http://127.0.0.1:8099/index.html OUT=/tmp/cap2 \
  node scripts/capture.cjs

# 3) 合成最终 mp4（把真实 vNN.mp4 叠回原坐标）
CAP=/tmp/cap2 ASSETS=./assets FINAL=./course-ppt-video.mp4 \
  python3 scripts/build_video.py
```

> ⚠️ headless Chromium 录不到 `<video>` 播放帧，所以走「截图 + 合成」法（详见 `references/pitfalls.md` 第四类）。

---

## 可选上游依赖（不安装也能用）

- **guizang-ppt-skill** — 更丰富的网页 PPT 视觉系统（电子杂志风 / 瑞士国际主义）。
  `npx skills add op7418/guizang-ppt-skill --skill guizang-ppt-skill`
- **ian-xiaohei-illustrations** — 怪诞手绘正文配图风格。
  `npx skills add helloianneo/ian-xiaohei-illustrations --skill ian-xiaohei-illustrations`

若使用上游 skill，请遵守其各自的 License 与使用边界。

---

## License

MIT © course-ppt-html contributors
