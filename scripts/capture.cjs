#!/usr/bin/env node
/**
 * course-ppt-html · 阶段6 录制脚本（一）：截图 + 取视频坐标 + 隐藏 video
 *
 * 为什么不直接用 Playwright recordVideo：
 *   headless Chromium 不会把 <video> 的实际播放帧合成进录制流，
 *   录出来是冻结的 poster（帧差≈0）。所以改成：
 *     1) 翻页 -> 等动画 settle
 *     2) 截图前用 JS 隐藏 <video>（避免底图带 poster 导致双重图像）
 *     3) 截干净底图；同时用 getBoundingClientRect 取 video 精确坐标
 *     4) 后续 build_video.py 把真实 vNN.mp4 合成回去
 *
 * 用法：
 *   BASE_URL=http://127.0.0.1:8099/index.html OUT=/tmp/cap2 \
 *   node capture.cjs
 * 依赖：npm i playwright && npx playwright install chromium
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const BASE_URL = process.env.BASE_URL || 'http://127.0.0.1:8099/index.html';
const OUT = process.env.OUT || '/tmp/cap2';
const VP_W = parseInt(process.env.VP_W || '1280', 10);
const VP_H = parseInt(process.env.VP_H || '720', 10);
const SETTLE_MS = parseInt(process.env.SETTLE_MS || '1200', 10);

fs.mkdirSync(OUT, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: VP_W, height: VP_H }, deviceScaleFactor: 1 });
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  const count = await page.evaluate(() => document.querySelectorAll('.slide').length);
  console.log(`检测到 ${count} 页`);

  const rects = [];
  for (let i = 0; i < count; i++) {
    await page.evaluate((idx) => window.go(idx), i);
    await page.waitForTimeout(SETTLE_MS); // 等动画 settle，避免坐标溢出

    // 取视频坐标（在隐藏前读，坐标本身是布局属性不受影响）
    const info = await page.evaluate(() => {
      // 当前页 = 视口内 left≈0 的那张 slide（go() 已平移 deck）
      const slides = Array.from(document.querySelectorAll('.slide'));
      const cur = slides.findIndex(s => Math.abs(s.getBoundingClientRect().left) < 2);
      const sv = cur >= 0 ? slides[cur].querySelector('.frame-img > video') : null;
      if (!sv) return { hasVideo: false };
      const r = sv.getBoundingClientRect();
      return { hasVideo: true, src: sv.getAttribute('src'),
               x: Math.round(r.x), y: Math.round(r.y),
               w: Math.round(r.width), h: Math.round(r.height) };
    });

    // 隐藏 video 再截图（干净底图，无 poster 重影）
    await page.evaluate(() => {
      document.querySelectorAll('.frame-img > video').forEach(v => v.style.visibility = 'hidden');
    });
    await page.waitForTimeout(150);
    const file = path.join(OUT, `slide_${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: file }); // 视口截图 = 只录内容区
    // 恢复 video（供下一页选择器状态一致）
    await page.evaluate(() => {
      document.querySelectorAll('.frame-img > video').forEach(v => v.style.visibility = 'visible');
    });

    rects.push(info);
    console.log(`slide ${i + 1}: ${info.hasVideo ? 'video ' + info.src + ' @(' + info.x + ',' + info.y + ' ' + info.w + 'x' + info.h + ')' : 'static'}`);
  }

  fs.writeFileSync(path.join(OUT, 'rects.json'), JSON.stringify(rects, null, 2));
  await browser.close();
  console.log(`完成。截图+坐标已写入 ${OUT}/（rects.json + slide_XX.png）`);
})().catch(e => { console.error(e); process.exit(1); });
