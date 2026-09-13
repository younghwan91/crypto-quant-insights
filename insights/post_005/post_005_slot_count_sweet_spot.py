"""Post 005: The Slot Count Sweet Spot — parallel positions vs Calmar ratio."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

OUT = Path(__file__).parent / "post_005_slot_count_sweet_spot.png"

BG   = "#0d1117"
FG   = "#e6edf3"
GRID = "#21262d"
ACC1 = "#58a6ff"   # blue — main line
ACC2 = "#3fb950"   # green — return
ACC3 = "#f85149"   # red — drawdown
GOLD = "#d29922"   # highlight peak

slots    = [1, 2, 5, 8, 10, 12, 15]
calmar   = [2.2, 3.2, 5.1, 5.5, 5.8, 5.4, 5.5]
ann_ret  = [70.6, 99.9, 160.8, 174.1, 187.2, 189.7, 195.4]
dd       = [32.1, 30.8, 31.7, 31.7, 32.4, 35.3, 35.3]
aggr     = [155, 320, 820, 958, 1086, 1024, 1075]

fig = plt.figure(figsize=(18, 11), facecolor=BG)
fig.text(0.5, 0.960, "The Slot Count Sweet Spot",
         ha="center", va="center", fontsize=26, fontweight="bold", color=FG)
fig.text(0.5, 0.915, "Calmar ratio by simultaneous position count · VR Squeeze · 6yr Binance USDT-M",
         ha="center", va="center", fontsize=14, color="#8b949e")

gs = gridspec.GridSpec(1, 3, figure=fig,
                       left=0.07, right=0.97, top=0.83, bottom=0.13,
                       wspace=0.32)

# ── Panel 1: Calmar vs Slots ─────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)
ax1.plot(slots, calmar, color=ACC1, linewidth=2.5, zorder=3)
ax1.scatter(slots, calmar, color=ACC1, s=60, zorder=4)

peak_idx = calmar.index(max(calmar))
ax1.scatter([slots[peak_idx]], [calmar[peak_idx]], color=GOLD, s=180, zorder=5,
            edgecolors=FG, linewidth=1.5)
ax1.annotate(f"Peak\n{calmar[peak_idx]:.1f}",
             xy=(slots[peak_idx], calmar[peak_idx]),
             xytext=(slots[peak_idx] - 2.8, calmar[peak_idx] + 0.2),
             color=GOLD, fontsize=11, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.5))

for s, c in zip(slots, calmar):
    ax1.annotate(f"{c:.1f}", xy=(s, c),
                 xytext=(0, 10), textcoords="offset points",
                 ha="center", fontsize=9, color=FG)

ax1.set_ylim(0, 7.5)
ax1.set_xlabel("Simultaneous Positions (Slots)", color=FG, fontsize=11)
ax1.set_ylabel("Calmar Ratio", color=FG, fontsize=11)
ax1.set_title("Calmar Ratio", color=FG, fontsize=13, fontweight="bold", pad=10)
ax1.set_xticks(slots)
ax1.tick_params(colors=FG)
ax1.spines[:].set_color(GRID)
for spine in ax1.spines.values():
    spine.set_edgecolor(GRID)
ax1.yaxis.label.set_color(FG)
ax1.xaxis.label.set_color(FG)
ax1.grid(axis="y", color=GRID, linewidth=0.6)

# ── Panel 2: AnnRet vs DD ───────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

x = np.arange(len(slots))
w = 0.35
bars_r = ax2.bar(x - w/2, ann_ret, width=w, color=ACC2, alpha=0.85, label="Ann. Return %")
bars_d = ax2.bar(x + w/2, dd, width=w, color=ACC3, alpha=0.85, label="Max Drawdown %")

for bar, val in zip(bars_r, ann_ret):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f"{val:.0f}%", ha="center", va="bottom", fontsize=8, color=FG)
for bar, val in zip(bars_d, dd):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f"{val:.1f}%", ha="center", va="bottom", fontsize=8, color=FG)

# highlight 12+ slot DD jump
ax2.axvline(x=x[4] + 0.5, color=ACC3, linestyle="--", linewidth=1.2, alpha=0.7)
ax2.text(x[4] + 0.6, 215, "↑ DD\nrises", color=ACC3, fontsize=9, va="top")

ax2.set_ylim(0, 240)
ax2.set_xticks(x)
ax2.set_xticklabels([str(s) for s in slots])
ax2.set_xlabel("Simultaneous Positions (Slots)", color=FG, fontsize=11)
ax2.set_title("Return vs Drawdown", color=FG, fontsize=13, fontweight="bold", pad=10)
ax2.legend(facecolor=GRID, edgecolor=GRID, labelcolor=FG, fontsize=10)
ax2.tick_params(colors=FG)
ax2.spines[:].set_color(GRID)
for spine in ax2.spines.values():
    spine.set_edgecolor(GRID)
ax2.grid(axis="y", color=GRID, linewidth=0.6)

# ── Panel 3: Aggression Score ────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)

colors_a = [GOLD if s == 10 else ACC1 for s in slots]
bars_a = ax3.bar(slots, aggr, color=colors_a, alpha=0.85, width=1.4)
for bar, val in zip(bars_a, aggr):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
             f"{val:,}", ha="center", va="bottom", fontsize=9, color=FG)

ax3.set_ylim(0, 1350)
ax3.set_xticks(slots)
ax3.set_xlabel("Simultaneous Positions (Slots)", color=FG, fontsize=11)
ax3.set_ylabel("AnnRet × Calmar", color=FG, fontsize=11)
ax3.set_title("Aggression Score\n(Ann. Return × Calmar)", color=FG, fontsize=13, fontweight="bold", pad=10)
ax3.tick_params(colors=FG)
ax3.spines[:].set_color(GRID)
for spine in ax3.spines.values():
    spine.set_edgecolor(GRID)
ax3.grid(axis="y", color=GRID, linewidth=0.6)

# annotate peak
ax3.annotate("Peak at\n10 slots",
             xy=(10, 1086),
             xytext=(12.5, 1086),
             color=GOLD, fontsize=10, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.5))

fig.text(0.5, 0.01,
         "Source: r39 · 132 variants · 6yr live Binance data · 1–15 slot sweep",
         ha="center", fontsize=10, color="#8b949e",
         bbox=dict(facecolor=BG, edgecolor=GRID, boxstyle="round,pad=0.3"))

plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {OUT}")
