"""README 히어로 갤러리: insights/post_NNN 차트 여섯 장을 2×3 콘타크트 시트로.

실행 (레포 루트):
    uv run --with matplotlib --with pillow --with numpy python scripts/make_hero.py
→ docs/images/hero-light.png, docs/images/hero-dark.png
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import matplotlib.image as mpimg
import numpy as np
from matplotlib.patches import Rectangle

from hero_style import render_both

ROOT = pathlib.Path(__file__).resolve().parents[1]

# (포스트 번호, 짧은 제목, PNG 경로) — 표시 순서
PICKS = [
    ("001", "Why Your 3-Year Backtest is Lying to You", "insights/post_001/post_001_3yr_vs_6yr_crash_test.png"),
    ("002", "Win Rate 70% vs R:R 2:1", "insights/post_002/post_002_wr_vs_rr.png"),
    ("011", "IS PF 2.16 vs OOS PF 1.38", "insights/post_011/post_011_is_oos_divergence.png"),
    ("013", "Kelly Said 154x. We Run 30x.", "insights/post_013/post_013_kelly_leverage.png"),
    ("008", "More Leverage or More Positions?", "insights/post_008/post_008_leverage_vs_slots.png"),
    ("010", "The Exit You Never Optimize", "insights/post_010/post_010_exit_mode_beats_tpsl.png"),
]

ASPECT = 1.85          # 칸의 가로/세로. 원본(1.63~2.06)은 자기 배경색으로 패딩해 맞춘다
NCOLS, NROWS = 3, 2
FIG_W = 12.0
L, R, TOP_IN, BOT_IN, WSPACE, HSPACE = 0.01, 0.99, 0.38, 0.06, 0.05, 0.22


def pad_to_aspect(img: np.ndarray, aspect: float) -> np.ndarray:
    """원본 비율은 유지한 채 모서리 픽셀 색으로 캔버스를 넓혀 aspect 에 맞춘다 (왜곡 없음)."""
    h, w = img.shape[:2]
    bg = img[2, 2]
    if w / h < aspect:
        new_w = int(round(h * aspect)); pad = new_w - w
        out = np.empty((h, new_w, img.shape[2]), dtype=img.dtype); out[...] = bg
        out[:, pad // 2:pad // 2 + w] = img
    else:
        new_h = int(round(w / aspect)); pad = new_h - h
        out = np.empty((new_h, w, img.shape[2]), dtype=img.dtype); out[...] = bg
        out[pad // 2:pad // 2 + h, :] = img
    return out


def figsize():
    cell_w = FIG_W * (R - L) / (NCOLS + (NCOLS - 1) * WSPACE)
    cell_h = cell_w / ASPECT
    axes_h = cell_h * (NROWS + (NROWS - 1) * HSPACE)
    return (FIG_W, axes_h + TOP_IN + BOT_IN)


def draw(fig, axes, p):
    _, fig_h = fig.get_size_inches()
    fig.subplots_adjust(left=L, right=R, top=1 - TOP_IN / fig_h, bottom=BOT_IN / fig_h,
                        wspace=WSPACE, hspace=HSPACE)
    for ax, (num, title, rel) in zip(axes.flat, PICKS):
        img = pad_to_aspect(mpimg.imread(ROOT / rel), ASPECT)
        ax.imshow(img, interpolation="lanczos")
        ax.axis("off")
        # 라이트 모드에서 어두운 원본이 떠 보이지 않게 얇은 테두리
        ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fill=False,
                               edgecolor=p["grid"], linewidth=1.0, clip_on=False))
        ax.set_title(f"#{num}  {title}", color=p["ink"], fontsize=10.5, fontweight="bold",
                     loc="left", pad=5)


if __name__ == "__main__":
    paths = render_both(draw, out_dir=str(ROOT / "docs/images"), name="hero",
                        figsize=figsize(), nrows=NROWS, ncols=NCOLS)
    for path in paths:
        print(path)
