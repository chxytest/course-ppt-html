# 单文件 HTML Deck 规格 · course-ppt-html

> 阶段3 的实现依据。配合 `assets/template.html` 使用。目标是产出一个**零外部依赖、可离线打开、可本地翻页、可嵌视频、可录视频**的单 HTML 文件。

---

## 1. 文件结构（单文件）

一个 `index.html` 包含：`<style>`（全部 CSS，含 `:root` 主题变量）、`<body>`（`.deck` + 多张 `.slide`）、`<script>`（翻页/同步逻辑）。**不要引外部 CDN、不要引外部字体文件**（用系统字体栈），否则分发会断。

---

## 2. 主题变量（`:root`）

模板开头用 CSS 变量定义主题，全站只改这 6 行即可换肤：

```css
:root{
  --ink:#0a1f3d;        /* 主文字/深色块 */
  --paper:#f1f3f5;      /* 背景 */
  --accent:#002FA7;     /* 高亮锚点色（克莱因蓝 IKB） */
  --accent2:#E8552D;    /* 次级高亮（安全橙，用于路径/标注） */
  --muted:#6b7280;      /* 次要文字 */
  --line:#d8dce1;       /* 发丝线/网格 */
}
```

两套预设参考：
- **靛蓝瓷（科技/AI/研究）**：`--ink:#0a1f3d / --paper:#f1f3f5 / --accent:#002FA7`
- **瑞士克莱因蓝**：`--ink:#0a0a0a / --paper:#ffffff / --accent:#002FA7 / --accent2:#FFD400`

---

## 3. 翻页容器

```html
<div id="deck">
  <section class="slide light"> ... </section>
  <section class="slide light"> ... </section>
  <!-- 更多 slide -->
</div>
```

- 横排：`#deck{display:flex; transform:translateX(calc(-100% * idx)); transition:transform .6s}`
- 控制：`function go(i){ idx=...; deck.style.transform=...; if(window.syncVideos)syncVideos(idx); }`

---

## 4. 配图容器（🔴 关键写法）

```html
<div class="frame-img">
  <img src="assets/p03.jpeg" alt="描述">
</div>
```

对应 CSS（**必须 contain + overflow:visible + height:auto**，否则裁图）：

```css
.frame-img{ width:100%; overflow:visible; display:flex; justify-content:center; align-items:center; }
.frame-img img{ width:100%; height:auto; max-height:72vh; object-fit:contain; }
```

---

## 5. 视频容器（自动播放 + 翻页同步）

```html
<div class="frame-img">
  <video src="assets/v03.mp4" poster="assets/p03.jpeg"
         muted loop playsinline preload="metadata" title="描述"></video>
</div>
```

CSS：

```css
.frame-img video{ width:100%; height:auto; max-height:72vh; object-fit:contain; background:var(--paper); }
```

同步逻辑（通用，新增视频页**无需改 JS**）：

```js
function syncVideos(idx){
  document.querySelectorAll('.slide').forEach((s,i)=>{
    const v = s.querySelector('.frame-img > video');
    if(!v) return;
    if(i===idx){ v.play().catch(()=>{}); } else { v.pause(); v.currentTime=0; }
  });
}
```

在 `go()` 末尾调用：`if(window.syncVideos) syncVideos(idx);`

---

## 6. 导航与交互

- 键盘：`←`/`→` 翻页；`N` 切换讲师备注层；`B` 静态/动态切换（可选）。
- 圆点导航：每页一个 `.dot`，点击 `go(i)`。
- 触摸：`touchstart`/`touchend` 判断横滑方向。
- 讲师备注层：每个 `.slide` 内放 `<aside class="teacher-notes">...</aside>`，按 N 显示/隐藏（绝对定位覆盖，不干扰演示）。

---

## 7. 如何加一页

复制一个 `<section class="slide light">…</section>` 块，改内容即可。新增视频页只要把 `<img>` 换成第 5 节的 `<video>`，`syncVideos` 自动覆盖。

---

## 8. 校验清单（G3 前自查）

- [ ] 所有 `assets/pNN.jpeg` / `assets/vNN.mp4` 实际存在且 >10KB（无占位/失效）。
- [ ] 配图无裁切（`object-fit:contain`）。
- [ ] 过渡/居中类样式用 CSS `!important`，不靠内联 style。
- [ ] 视频页 `syncVideos` 在 `go()` 内被调用。
- [ ] 无外部 CDN / 字体依赖（可离线打开）。
- [ ] 起 `python3 -m http.server` 本地预览，逐页翻一遍确认。
