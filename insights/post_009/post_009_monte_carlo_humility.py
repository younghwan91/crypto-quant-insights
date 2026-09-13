"""Post 009: Monte Carlo Humility — return percentiles vs drawdown percentiles."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

OUT = Path(__file__).parent / "post_009_monte_carlo_humility.png"

BG    = "#0d1117"
FG    = "#e6edf3"
SUB   = "#8b949e"
GRID  = "#21262d"
GREEN = "#3fb950"
RED   = "#f85149"
BLUE  = "#58a6ff"
GOLD  = "#d29922"

# Data from r46
pct_labels = ["P1", "P5", "P10", "P25", "P50", "P75", "P90", "P95", "P99"]
balances   = [2184, 9032, 20280, 83181, 390471, 1828848, 7151000, 15520185, 71821298]
returns_pct = [9, 352, 914, 4059, 19424, 91342, 357450, 775909, 3590965]

dd_pct_labels = ["P5", "P25", "P50", "P75", "P95"]
dd_values     = [56.9, 66.3, 73.6, 81.2, 90.9]

horizon_labels  = ["1 Day", "1 Week", "1 Month", "1 Year"]
horizon_p50_ret = [0.2, 9.4, 54.0, 19424]   # return %
horizon_prob    = [50.2, 61.4, 74.5, 99.1]  # P(profit) %
horizon_mdd_p50 = [3.2, 20.8, 40.0, 73.6]  # MDD P50 %

fig = plt.figure(figsize=(18, 10), facecolor=BG)
fig.text(0.5, 0.955, "Monte Carlo Said I'd Have $390K. It Also Said 21% Chance of Ruin.",
         ha="center", fontsize=20, fontweight="bold", color=FG)
fig.text(0.5, 0.910,
         "10,000 paths · $2,000 initial · 785 trades/year · 4.73yr Binance trade pool · blended L/N=2.63",
         ha="center", fontsize=11, color=SUB)

gs = gridspec.GridSpec(1, 3, figure=fig,
                       left=0.06, right=0.97, top=0.84, bottom=0.13, wspace=0.40)

# ── Panel 1: Balance Percentiles (log scale) ─────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)
pct_x = np.arange(len(pct_labels))
bar_colors = [SUB if b < 390471 else GREEN if b == 390471 else BLUE for b in balances]
bar_colors[4] = GOLD  # P50 highlight
ax1.bar(pct_x, balances, color=bar_colors, width=0.6, zorder=3)
ax1.set_yscale("log")
ax1.set_xticks(pct_x)
ax1.set_xticklabels(pct_labels, fontsize=9, color=SUB)
ax1.set_ylabel("Final Balance ($, log scale)", color=SUB, fontsize=10)
ax1.set_title("1-Year Balance Distribution", color=FG, fontsize=12, pad=8)
ax1.tick_params(colors=SUB)
for sp in ax1.spines.values(): sp.set_edgecolor(GRID)
ax1.yaxis.set_tick_params(labelcolor=SUB)
ax1.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)

# Annotate P50
ax1.annotate("P50: $390K\n(+19,424%)",
             xy=(4, 390471), xytext=(2.5, 3_000_000),
             fontsize=9, color=GOLD,
             arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.2),
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#21262d", edgecolor=GOLD, alpha=0.9))
ax1.annotate("P1: $2,184\n(barely alive)",
             xy=(0, 2184), xytext=(0.3, 15000),
             fontsize=8, color=RED,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.0),
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#21262d", edgecolor=RED, alpha=0.9))

# ── Panel 2: Drawdown Distribution ──────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)
dd_x = np.arange(len(dd_pct_labels))
dd_colors = [RED if v >= 73 else GOLD if v >= 60 else SUB for v in dd_values]
dd_colors[2] = RED   # P50 = 73.6% highlighted
bars2 = ax2.bar(dd_x, dd_values, color=dd_colors, width=0.55, zorder=3)
for bar, val in zip(bars2, dd_values):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.8,
             f"{val:.1f}%", ha="center", va="bottom", fontsize=10, color=FG,
             fontweight="bold" if val == 73.6 else "normal")
ax2.axhline(73.6, color=RED, linestyle="--", linewidth=1.2, alpha=0.6, zorder=2)
ax2.set_xticks(dd_x)
ax2.set_xticklabels(dd_pct_labels, fontsize=10, color=SUB)
ax2.set_ylabel("Max Drawdown per Path (%)", color=SUB, fontsize=10)
ax2.set_ylim(0, 105)
ax2.set_title("Drawdown Distribution (same paths)", color=FG, fontsize=12, pad=8)
ax2.tick_params(colors=SUB)
for sp in ax2.spines.values(): sp.set_edgecolor(GRID)
ax2.yaxis.set_tick_params(labelcolor=SUB)
ax2.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
ax2.text(2, 76, "Median path\ndrawdown: 73.6%", ha="center", fontsize=8.5, color=RED,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="#21262d", edgecolor=RED, alpha=0.85))

# ── Panel 3: Horizon Risk Summary ────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)
h_x = np.arange(len(horizon_labels))
ax3.bar(h_x - 0.18, horizon_mdd_p50, width=0.33, color=RED, label="Median MDD (%)", zorder=3)
ax3.bar(h_x + 0.18, horizon_prob,    width=0.33, color=GREEN, label="P(profit) (%)", zorder=3)
for i, (mdd, prob) in enumerate(zip(horizon_mdd_p50, horizon_prob)):
    ax3.text(i - 0.18, mdd + 1, f"{mdd:.0f}%", ha="center", fontsize=8.5, color=FG)
    ax3.text(i + 0.18, prob + 1, f"{prob:.1f}%", ha="center", fontsize=8.5, color=FG)
ax3.set_xticks(h_x)
ax3.set_xticklabels(horizon_labels, fontsize=9.5, color=SUB)
ax3.set_ylabel("(%)", color=SUB, fontsize=10)
ax3.set_ylim(0, 115)
ax3.set_title("Horizon Risk: MDD vs P(Profit)", color=FG, fontsize=12, pad=8)
ax3.tick_params(colors=SUB)
for sp in ax3.spines.values(): sp.set_edgecolor(GRID)
ax3.yaxis.set_tick_params(labelcolor=SUB)
ax3.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
ax3.legend(facecolor="#21262d", edgecolor=GRID, labelcolor=FG, fontsize=9,
           loc="upper left")

# Key stats row
fig.text(0.25, 0.04, "P(Profit after 1yr): 99.1%", ha="center", fontsize=11,
         color=GREEN, fontweight="bold")
fig.text(0.50, 0.04, "P(Ruin < 50% capital): 21.1%", ha="center", fontsize=11,
         color=RED, fontweight="bold")
fig.text(0.75, 0.04, "Mean $4.65M  vs  Median $390K", ha="center", fontsize=11,
         color=GOLD, fontweight="bold")

fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {OUT}")
