# Toastmasters Table Topics 交互套件（复用资产）

> 本文件沉淀「头马即兴演讲（Table Topics）题库 PPT / 互动应用」中**可跨场景复用**的交互组件、数据模型与主持稿模板。
> 它与「品牌主题色模板（Toastmasters Brand Manual 的 Loyal Blue / True Maroon / Happy Yellow + 渐变端点）」**正交**——
> 主题色模板已并入技能：`assets/toastmasters-theme.html`（含完整 CSS 令牌 + 参数化分级卡片），本文件只管**交互与内容结构**，主题色令牌见 §7。
>
> 适用：任何「N 道题目 + 选编号 + 多难度 + 主持串场」的现场互动场景（即兴演讲、知识竞赛、破冰游戏、题库 H5）。

---

## 0. 成品结构（一次成型的三件套）

| 交付物 | 文件 | 说明 |
|---|---|---|
| 互动题库 PPT | `toastmasters-ppt.html` | 单文件 HTML：封面 + 15 编号选题板 + 15 题详情页，支持 localStorage 已选持久化、难度切换、返回 |
| 互动答题应用 | `empathy-tabletopics-app.html` | 极简版：首页编号卡网格 + 详情页（范文/词汇/句型），适合手机或投屏 |
| 双语主持稿 | `table-topics-主持稿.md` | 开场 1.5min / 规则 3 句 / 串场 2–3 句 / 结尾 30s + 15 题中英对照表 |

三者共享同一份 `QUESTIONS` 数据模型（见 §3），换主题只改数据，不改交互。

---

## 1. 组件 A · 编号选题板（Number Pick Board）

**用途**：N 个编号卡，点击 → 标记已选（变色 + ✓ 徽标）+ 跳转对应页 + 计数；支持「二次确认重置」。
**已在两处复用**：PPT 第 2 页、互动应用首页。

### CSS
```css
#pptGrid{display:grid;grid-template-columns:repeat(5,1fr);gap:1vw;
  align-content:center;justify-content:center;max-width:min(64vw,820px);margin:0 auto;width:100%}
.ppt-card{aspect-ratio:1/1;width:100%;max-width:160px;max-height:160px;margin:0 auto;position:relative;
  display:flex;align-items:center;justify-content:center;
  font-family:var(--sans);font-weight:800;font-size:min(2.6vw,4.4vh);
  background:#fff;border:2px solid var(--grey-2);color:var(--grey-3);cursor:pointer;
  transition:transform .15s ease,background .15s ease}
.ppt-card:hover{transform:translateY(-3px)}
.ppt-card.picked{background:var(--grey-2);color:var(--ink);border-color:var(--grey-2)}
.ppt-card .badge{position:absolute;top:.5vh;right:.5vw;font-family:var(--mono);
  font-size:max(11px,.7vw);font-weight:600;color:var(--accent);display:none}
.ppt-card.picked .badge{display:block}
```

### HTML
```html
<div class="t-meta" id="pptCnt">Picked · <b>0</b> / 15</div>
<div id="pptGrid" style="flex:1;display:grid;grid-template-columns:repeat(5,1fr);gap:.9vw;align-content:center"></div>
<button id="pptReset">Reset · 重置</button>
```

### JS（自包含 IIFE，依赖外部 `go(n)` 翻页）
```js
(function(){
  var STORE='tm_ppt_picked', COUNT=15, picked=[];
  try{ picked=JSON.parse(localStorage.getItem(STORE)||'[]'); }catch(e){ picked=[]; }
  if(!Array.isArray(picked)) picked=[];
  function save(){ try{ localStorage.setItem(STORE,JSON.stringify(picked)); }catch(e){} }
  function render(){
    var grid=document.getElementById('pptGrid'); if(!grid) return; grid.innerHTML='';
    for(var n=1;n<=COUNT;n++){
      var c=document.createElement('div');
      c.className='ppt-card'+(picked.indexOf(n)>-1?' picked':'');
      c.innerHTML=n+'<span class="badge">✓ PICKED</span>';
      c.setAttribute('data-n',n);
      c.onclick=function(){
        var v=parseInt(this.getAttribute('data-n'),10);
        if(picked.indexOf(v)===-1){ picked.push(v); save(); }
        render();
        if(typeof go==='function') go(1+v); // 封面=0, 选题板=1, Qn=1+n
      };
      grid.appendChild(c);
    }
    var cnt=document.getElementById('pptCnt');
    if(cnt) cnt.innerHTML='Picked · <b>'+picked.length+'</b> / '+COUNT;
  }
  var rbtn=document.getElementById('pptReset');
  if(rbtn){
    rbtn.addEventListener('click',function(){
      if(picked.length===0){ rbtn.textContent='Nothing to reset';
        setTimeout(function(){rbtn.textContent='Reset · 重置';},1200); return; }
      if(rbtn.getAttribute('data-armed')){ picked=[]; save(); render();
        rbtn.removeAttribute('data-armed'); rbtn.textContent='Reset · 重置'; }
      else{ rbtn.setAttribute('data-armed','1'); rbtn.textContent='Confirm Reset?';
        setTimeout(function(){ if(rbtn.getAttribute('data-armed')){ rbtn.removeAttribute('data-armed');
          rbtn.textContent='Reset · 重置'; } },3000); }
    });
  }
  render();
})();
```

**调参**：改 `COUNT` 即改题数；改 `go(1+v)` 偏移量适配你的页序（本套封面=0、选题板=1、第 n 题=1+n）。

---

## 2. 组件 B · 难度切换（Easy / Medium / Hard）

**用途**：同一道题三种讲解深度，按钮高亮 + 面板切换 + 隐藏默认提示。三档配色已与品牌色对齐：
Easy=Happy Yellow、Medium=Loyal Blue、Hard=白底虚线 True Maroon。

### CSS（关键）
```css
.diff-bar{display:flex;gap:.8vw;margin-top:2.2vh;flex-wrap:wrap}
.diff-btn{/* 基础按钮样式 */}
.diff-btn[data-diff="easy"].on{background:var(--accent-bright);color:var(--ink)}
.diff-btn[data-diff="medium"].on{background:var(--ink);color:#fff}
.diff-btn[data-diff="hard"].on{background:var(--accent);color:#fff}
.diff-panel{display:none}
.diff-panel.on{display:block;animation:fade .3s ease}
.diff-default{/* 默认提示：请选择难度 / 2 分钟计时 */}
```

### HTML（每题一页）
```html
<div class="diff-bar">
  <button class="diff-btn" data-diff="easy">Easy</button>
  <button class="diff-btn" data-diff="medium">Medium</button>
  <button class="diff-btn" data-diff="hard">Hard</button>
</div>
<div class="diff-default">Please choose a difficulty. You have 2 minutes.</div>
<div class="diff-panel" data-diff="easy"><h3>Easy — Sample Answer</h3><div class="easyText"></div></div>
<div class="diff-panel" data-diff="medium"><h3>Medium — Vocabulary &amp; Patterns</h3>
  <div class="vocab"></div><ul class="patterns"></ul></div>
<div class="diff-panel" data-diff="hard"><div class="mark">No hints. Trust yourself.</div></div>
<a class="back-link" href="javascript:void(0)" onclick="go(1);return false">Back · 返回选题板</a>
```

### JS（每页独立，无全局污染）
```js
document.querySelectorAll('.diff-bar').forEach(function(bar){
  bar.querySelectorAll('.diff-btn').forEach(function(btn){
    btn.addEventListener('click',function(){
      var slide=btn.closest('.slide');
      var diff=btn.getAttribute('data-diff');
      slide.querySelectorAll('.diff-btn').forEach(function(b){ b.classList.toggle('on',b===btn); });
      slide.querySelectorAll('.diff-panel').forEach(function(p){ p.classList.toggle('on',p.getAttribute('data-diff')===diff); });
      var def=slide.querySelector('.diff-default'); if(def) def.style.display='none';
    });
  });
});
```

### 组件 C · 返回选题板（Back Link）
左下角固定返回，回到选题板（本套 `go(1)`）：
```css
.back-link{position:absolute;bottom:2vh;left:1.6vw;z-index:5;font-family:var(--mono);
  font-size:max(12px,.82vw);letter-spacing:.18em;text-transform:uppercase;
  color:var(--text-helper);cursor:pointer;text-decoration:none;opacity:.7;
  display:inline-flex;align-items:center;gap:.4em}
.back-link:hover{opacity:1;color:var(--ink)}
.back-link::before{content:"←";font-weight:600;opacity:.8}
```

---

## 3. 数据模型 · QUESTIONS（换主题只改这里）

```js
const QUESTIONS = [
  { n:1, q:"Do you think it is easy to understand how other people feel?",
    img:"assets/p01.png",
    easy:`多段英文范文，段落间用 \n 分隔；
          渲染时 split("\n").map(p=>'<p class="para">'+p+'</p>')，
          .para 用 text-indent:2em 首行缩进、line-height:1.6、单列从上到下`,
    vocab:["empathy","perspective","body language","misinterpret","emotional cue"], // ≤5 词
    patterns:["I don't think it is always easy to..., because...",
              "From my experience, I once misunderstood..., which taught me..."] },
  // ...n=2..15
];
```

| 字段 | 作用 | 约束 |
|---|---|---|
| `n` | 编号 | 1..N，与选题板 `go(1+n)` 对齐 |
| `q` | 题面（英文） | 简短问句 |
| `img` | 题头配图 | `assets/pNN.png`，落本地、文件名对齐引用 |
| `easy` | 范文 | 多段字符串（`\n` 分段）；首行缩进、单列 |
| `vocab` | 普通档关键词 | **≤5 个**，避免信息过载 |
| `patterns` | 普通档句型支架 | 2–3 条可套用句式 |

> 渲染注意：`.easy .para{text-indent:2em}` + 段落间**不要**加空行（用户明确要求 Easy 段落紧凑、无空白行）。

---

## 4. 主持稿模板（双语 · 直接套用）

固定四段 + 一张题表，换主题只填 `主题 / 今日一词 / 15 题中英对照`：

1. **开场（约 1.5 分钟）**：欢迎 → 点明主题与今日一词（一句话定义）→ 共情式钩子 → 规则（选编号 / 三难度 / 2 分钟）→ 邀请第一位。
2. **规则速记（3 句表格）**：① 选编号 1–N ② 三难度说明 ③ 每人 2 分钟。
3. **串场（通用 2–3 句）**：感谢上一位 → 有请下一位 → 没人主动则点名；附「时间到」「英文真棒」等赞美术语。
4. **结尾（约 30 秒）**：总结走心分享 → 集体鼓掌 → 把舞台还给主持人（占位名 `Evelyn`）。

> 交付格式：中英文对照分栏（**先英文后中文**），规则用表格，题目用 `# │ English │ 中文` 三列表。
> 详见成品 `table-topics-主持稿.md`。

---

## 5. 踩坑册（本套验证过的真实坑）

- **🔴 模板字符串逗号被吞（最高频）**：用正则批量删空行（`\n[\s]*\n+`→`\n`）时，若 `easy` 用反引号模板字符串，末尾 `,` 会被一并删掉 → JS 解析失败 → 首页/详情卡整片消失。修复：删空行后确认每个模板字面量后仍有 `,`。
- **jsdom 测试 lucide 时序**：外部 `lucide` 脚本会打乱内联业务 JS 时序；自测时把业务 JS 放在 lucide 脚本**之前**，并用 `global.matchMedia = ()=>({matches:false,addListener(){},removeListener(){}})` mock。
- **Logo 路径**：PPT 在 workspace 根目录，logo 在 `assets/toastmasters-logo.png` → 用 `assets/...` 而非 `images/...`；首页 logo 去半透明背景、与红色页底融合（`background:transparent`）。
- **校验器图像槽位**：`validate-swiss-deck` 要求 hero 槽位是 `s22-hero-21x9`（非 `16x10`），批量生成时统一替换。
- **选题板偏移**：`go(1+v)` 的 `1` 来自「封面=0、选题板=1」，若你的页序不同必须同步改偏移，否则跳错页。
- **难度按钮作用域**：`diff-bar` 切换 JS 用 `btn.closest('.slide')` 限定当前页，避免多页按钮互相串扰。

---

## 6. 一句话复用流程

1. 复制 `toastmasters-theme/index.html` 作视觉底座（含品牌色 token）→ 已并入技能后直接引用。
2. 注入 §1 选题板 + §2 难度切换 + §3 数据模型。
3. 按 §4 套主持稿模板，产出 `.md`。
4. 跑 `validate-swiss-deck.mjs` + jsdom 功能测试（防 §5 坑）。

---

## 7. 主题色令牌（Toastmasters Brand Manual 直译 CSS 变量）

> 来源：`assets/toastmasters-theme.html` 的 `:root`。做头马 / 品牌类 PPT 直接复制这套变量到自己的 `:root`，即可获得合规品牌色。

```css
:root{
  /* 主色 */
  --paper:#ffffff;          /* 主底色: 白 */
  --ink:#004165;            /* 文字主色 + 深色页背景: Loyal Blue (Pantone 302) */
  --accent:#772432;         /* 高亮锚点色: True Maroon (Pantone 188) */
  --accent-bright:#F2DF74;  /* 暗底高亮: Happy Yellow (Pantone 127) */

  /* 渐变端点（Brand Manual p.18 渐变规范） */
  --loyal-grad:#006094;     /* Blissful Blue (Loyal Blue 渐变端点) */
  --maroon-deep:#3B0104;    /* Deep Maroon (True Maroon 渐变深端) */
  --maroon-rich:#781327;    /* Rich Maroon (True Maroon 渐变亮端) */
  --gray-grad:#F5F5F5;      /* Fair Gray (Cool Gray 渐变端点) */

  /* 叠加透明度规范 */
  --overlay-loyal:rgba(0,65,101,.7);     /* Loyal Blue 70% 叠加 */
  --overlay-white:rgba(255,255,255,.7);  /* White 70% 叠加 */

  /* 淡化文字 */
  --text-secondary:#42565e;  /* Loyal Blue 淡化 */
}
```

### 参数化分级卡片（换场景改色不改结构）

三档难度 / 三档信息层级用统一变量驱动，避免写死：

```css
.tier-card{
  --tier-bg:var(--ink);      /* 该档背景色 */
  --tier-fg:#fff;            /* 该档前景色 */
  --tier-meta:var(--accent-bright);  /* 该档点缀/标签色 */
  background:var(--tier-bg);color:var(--tier-fg);
}
.tier-card .meta{color:var(--tier-meta)}
```

> 例：Easy=蓝底白字黄标 / Medium=maroon 底白字黄标 / Hard=深底白字黄标。换其他活动（知识竞赛/破冰）只改这三个变量即可，组件结构不变。
