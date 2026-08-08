#!/usr/bin/env python3
"""
course-ppt-html · 阶段6 录制脚本（二）：把截图 + 真实视频合成最终成片

输入：
  CAP     目录，含 slide_XX.png（干净底图）+ rects.json（capture.cjs 产出）
  ASSETS  目录，含 vNN.mp4（真实插画微动视频）与 pNN.jpeg（静帧）
输出：
  FINAL   最终 mp4（默认 ./course-ppt-video.mp4）

逻辑：
  视频页：把 vNN.mp4 按 object-fit:contain 算裁剪框，overlay 回 rects 里的坐标，持 4s
  静态页：底图 hold 3s
  全部段 concat 成一条。

用法：
  CAP=/tmp/cap2 ASSETS=./assets FINAL=./course-ppt-video.mp4 \\
      python3 build_video.py
依赖：ffmpeg（或 ffmpeg-static；可用 FFMPEG 环境变量指定路径）
"""
import os, re, sys, subprocess, json

CAP = os.environ.get("CAP", "/tmp/cap2")
ASSETS = os.environ.get("ASSETS")
if not ASSETS:
    for cand in [os.path.join(CAP, "..", "assets"), "./assets", "../assets"]:
        if os.path.isdir(cand):
            ASSETS = os.path.abspath(cand); break
FINAL = os.environ.get("FINAL", "./course-ppt-video.mp4")
VP_W, VP_H = int(os.environ.get("VP_W", 1280)), int(os.environ.get("VP_H", 720))
VIDEO_SEC, STATIC_SEC, FPS = int(os.environ.get("VIDEO_SEC", 4)), int(os.environ.get("STATIC_SEC", 3)), int(os.environ.get("FPS", 25))

# ---- ffmpeg 路径解析 ----
def find_ffmpeg():
    if os.environ.get("FFMPEG") and os.path.exists(os.environ["FFMPEG"]):
        return os.environ["FFMPEG"]
    for cmd in ("ffmpeg",):
        try:
            subprocess.run([cmd, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return cmd
        except Exception:
            pass
    # ffmpeg-static（npm i ffmpeg-static 或 pip install ffmpeg-static）
    try:
        import ffmpeg_static  # pip 包
        return ffmpeg_static.ffmpeg
    except Exception:
        pass
    try:
        import subprocess as _sp
        p = _sp.run(["node", "-e", "console.log(require('ffmpeg-static'))"],
                    capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip()
    except Exception:
        pass
    sys.exit("找不到 ffmpeg，请装 ffmpeg-static 或设置 FFMPEG 环境变量")
FF = find_ffmpeg()

def vidsize(p):
    out = subprocess.run([FF, "-i", p], capture_output=True, text=True).stderr
    m = re.search(r",\s*(\d{3,4})x(\d{3,4}),", out)
    return (int(m.group(1)), int(m.group(2))) if m else (VP_W, VP_H)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAILED:", " ".join(cmd[:6]), "...")
        print(r.stderr[-500:]); sys.exit(1)

def even(n):
    return n if n % 2 == 0 else n + 1

rects = json.load(open(os.path.join(CAP, "rects.json")))
n = len(rects)
clips = []
for i, r in enumerate(rects):
    idx = i + 1
    base = os.path.join(CAP, f"slide_{idx:02d}.png")
    clip = os.path.join(CAP, f"clip_{idx:02d}.mp4")
    if r.get("hasVideo"):
        src = r["src"]
        vid = src if os.path.isabs(src) or os.path.exists(src) else os.path.join(ASSETS, os.path.basename(src))
        vw, vh = vidsize(vid)
        bx, by, bw, bh = r["x"], r["y"], r["w"], r["h"]
        scale = min(bw / vw, bh / vh)
        cw, ch = even(int(round(scale * vw))), even(int(round(scale * vh)))
        ox = bx + (bw - cw) // 2
        oy = by + (bh - ch) // 2
        run([FF, "-loop", "1", "-i", base, "-i", vid,
             "-filter_complex", f"[1:v]scale={cw}:{ch}[ov];[0:v][ov]overlay=x={ox}:y={oy}",
             "-t", str(VIDEO_SEC), "-r", str(FPS), "-an",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
             "-movflags", "+faststart", "-y", clip])
        print(f"  slide {idx:02d}: 视频 {os.path.basename(vid)} -> 合成 {cw}x{ch} @({ox},{oy})")
    else:
        run([FF, "-loop", "1", "-i", base, "-t", str(STATIC_SEC), "-r", str(FPS), "-an",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
             "-movflags", "+faststart", "-y", clip])
        print(f"  slide {idx:02d}: 静态 hold {STATIC_SEC}s")
    clips.append(clip)

# concat
lst = os.path.join(CAP, "clips.txt")
with open(lst, "w") as f:
    for c in clips:
        f.write(f"file '{os.path.abspath(c)}'\n")
run([FF, "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
     "-movflags", "+faststart", "-y", FINAL])
print(f"FINAL -> {FINAL}")
