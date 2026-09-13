"""Post 008: More Leverage or More Positions? — leverage vs slot diversification."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

OUT = Path(__file__).parent / "post_008_leverage_vs_slots.png"

BG    = "#0d1117"
FG    = "#e6edf3"
SUB   = "#8b949e"
GRID  = "#21262d"
BLUE  = "#58a6ff"   # multi-slot (diversification)
RED   = "#f85149"   # single-slot leveraged
GOLD  = "#d29922"
GREEN = "#3fb950"

labels  = ["1×1x", "3×1x\n(slots)", "5×1x\n(slots)", "1×3x\n(lev)", "1×5x\n(lev)"]
ann_ret = [60.9, 134.7, 143.1, 170.1, 168.8]
max_dd  = [66.5,  74.8,  72.9,  97.2,  99.8]
calmar  = [ 0.9,   1.8,   2.0,   1.8,   1.7]
colors  = [SUB, BLUE, BLUE, RED, RED]

fig = plt.figure(figsize=(16, 9), facecolor=BG)
fig.text(0.5, 0.955, "More Leverage or More Positions?",
         ha="center", fontsize=24, fontweight="bold", color=FG)
fig.text(0.5, 0.910, "Same target return, different risk profile  ·  VR strategy  ·  6yr Binance USDT-M  ·  50 symbols",
         ha="center", fontsize=12, color=SUB)

gs = gridspec.GridSpec(1, 3, figure=fig,
                       left=0.07, right=0.97, top=0.83, bottom=0.14,
                       wspace=0.38)

x = np.arange(len(labels))
bar_w = 0.55

# ── Panel 1: Annual Return ──────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)
bars = ax1.bar(x, ann_ret, color=colors, width=bar_w, zorder=3)
for bar, val in zip(bars, ann_ret):
    ax1.text(bar.get_x() + bar.get_width()/2, val + 3,
             f"+{val:.1f}%", ha="center", va="bottom", fontsize=9, color=FG)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=9, color=SUB)
ax1.set_ylabel("Annual Return (%)", color=SUB, fontsize=10)
ax1.set_ylim(0, 210)
ax1.set_title("Annual Return", color=FG, fontsize=13, pad=8)
ax1.tick_params(colors=SUB)
for sp in ax1.spines.values(): sp.set_edgecolor(GRID)
ax1.yaxis.set_tick_params(labelcolor=SUB)
ax1.set_facecolor(BG)
ax1.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)

# ── Panel 2: Max Drawdown ────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)
bars2 = ax2.bar(x, max_dd, color=colors, width=bar_w, zorder=3)
ax2.axhline(100, color=RED, linestyle="--", linewidth=1.2, alpha=0.5, zorder=2)
ax2.text(4.35, 101.5, "Ruin", color=RED, fontsize=8, alpha=0.8)
for bar, val in zip(bars2, max_dd):
    ypos = val + 1.5
    ax2.text(bar.get_x() + bar.get_width()/2, ypos,
             f"{val:.1f}%", ha="center", va="bottom", fontsize=9, color=FG)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=9, color=SUB)
ax2.set_ylabel("Max Drawdown (%)", color=SUB, fontsize=10)
ax2.set_ylim(0, 115)
ax2.set_title("Max Drawdown", color=FG, fontsize=13, pad=8)
ax2.tick_params(colors=SUB)
for sp in ax2.spines.values(): sp.set_edgecolor(GRID)
ax2.yaxis.set_tick_params(labelcolor=SUB)
ax2.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)

# ── Panel 3: Calmar ─────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)
bars3 = ax3.bar(x, calmar, color=colors, width=bar_w, zorder=3)
for bar, val in zip(bars3, calmar):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 0.04,
             f"{val:.1f}", ha="center", va="bottom", fontsize=9, color=FG)
# highlight winner
ax3.scatter([2], [2.0], color=GOLD, s=180, zorder=5, marker="*")
ax3.text(2, 2.13, "best", ha="center", fontsize=8, color=GOLD)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, fontsize=9, color=SUB)
ax3.set_ylabel("Calmar Ratio", color=SUB, fontsize=10)
ax3.set_ylim(0, 2.6)
ax3.set_title("Calmar (Return / Max DD)", color=FG, fontsize=13, pad=8)
ax3.tick_params(colors=SUB)
for sp in ax3.spines.values(): sp.set_edgecolor(GRID)
ax3.yaxis.set_tick_params(labelcolor=SUB)
ax3.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)

# Legend
from matplotlib.patches import Patch
legend_els = [
    Patch(facecolor=BLUE, label="Multi-slot (diversification)"),
    Patch(facecolor=RED,  label="Single-slot (leverage)"),
    Patch(facecolor=SUB,  label="1×1x baseline"),
]
fig.legend(handles=legend_els, loc="lower center", ncol=3,
           facecolor="#21262d", edgecolor=GRID,
           labelcolor=FG, fontsize=10,
           bbox_to_anchor=(0.5, 0.02))

fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {OUT}")
