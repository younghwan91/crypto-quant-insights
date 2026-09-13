"""Post 007: I Tried Dynamic Parameters. Static Won."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

OUT = Path(__file__).parent / "post_007_dynamic_params_failed.png"

BG   = "#0d1117"
FG   = "#e6edf3"
GRID = "#21262d"
ACC1 = "#58a6ff"   # static
ACC2 = "#3fb950"   # adaptive (better)
ACC3 = "#f85149"   # adaptive (worse)
GOLD = "#d29922"

years = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]
bl_ev  = [36.4, 35.4, 28.7, 32.6, 20.5, 27.1, 86.0]
adp_ev = [48.4, 31.5, 22.5, 38.3, 38.6, 37.1, 61.5]
delta  = [d - b for d, b in zip(adp_ev, bl_ev)]  # +12, -3.9, -6.2, +5.7, +18.1, +10.0, -24.5

metrics_labels = ["N (trades)", "PF", "EV (bp)", "Ann. Return %", "Max DD %", "Calmar"]
bl_vals   = [2265, 1.280, 32.1, 187.2, 32.4, 5.8]
adp_vals  = [1628, 1.311, 35.7, 134.0, 42.6, 3.1]

fig = plt.figure(figsize=(18, 11), facecolor=BG)
fig.text(0.5, 0.960, "I Tried Dynamic Parameters. Static Won.",
         ha="center", va="center", fontsize=26, fontweight="bold", color=FG)
fig.text(0.5, 0.915, "224 regime-adaptive variants vs static params · 6yr Binance · Low / Mid / High vol regimes",
         ha="center", va="center", fontsize=13, color="#8b949e")

gs = gridspec.GridSpec(1, 3, figure=fig,
                       left=0.07, right=0.97, top=0.83, bottom=0.13,
                       wspace=0.35)

# ── Panel 1: EV by year grouped bars ─────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)

x = np.arange(len(years))
w = 0.35
bars_b = ax1.bar(x - w/2, bl_ev,  width=w, color=ACC1, alpha=0.85, label="Static (Baseline)")
bars_a = ax1.bar(x + w/2, adp_ev, width=w, color=ACC2, alpha=0.70, label="Adaptive")

for i, (bb, ba, d) in enumerate(zip(bars_b, bars_a, delta)):
    col = ACC2 if d > 0 else ACC3
    sign = "+" if d > 0 else ""
    ax1.text(x[i], max(bl_ev[i], adp_ev[i]) + 1.5,
             f"{sign}{d:.1f}", ha="center", fontsize=8.5, color=col, fontweight="bold")

ax1.set_ylim(0, 110)
ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=9)
ax1.set_ylabel("EV per Trade (bp)", color=FG, fontsize=11)
ax1.set_title("EV by Year\n(Adaptive vs Static)", color=FG, fontsize=13, fontweight="bold", pad=10)
ax1.legend(facecolor=GRID, edgecolor=GRID, labelcolor=FG, fontsize=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values():
    spine.set_edgecolor(GRID)
ax1.grid(axis="y", color=GRID, linewidth=0.6)

ax1.text(0.5, 0.88, "Adaptive wins 4 of 7 years\nbut loses badly in 2022 & 2026",
         ha="center", transform=ax1.transAxes, fontsize=9, color="#8b949e",
         bbox=dict(facecolor=GRID, boxstyle="round,pad=0.3"))

# ── Panel 2: Overall metrics comparison ──────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

y_pos = np.arange(len(metrics_labels))
w2 = 0.35

# normalize for display (different units) - show relative bars and actual values
# use % of max for bar length, show actual values as labels
max_vals = [max(bl_vals[i], adp_vals[i]) for i in range(len(metrics_labels))]
bl_norm  = [bl_vals[i] / max_vals[i] * 100 for i in range(len(metrics_labels))]
adp_norm = [adp_vals[i] / max_vals[i] * 100 for i in range(len(metrics_labels))]

bars_b2 = ax2.barh(y_pos + w2/2, bl_norm,  height=w2, color=ACC1, alpha=0.85, label="Static")
bars_a2 = ax2.barh(y_pos - w2/2, adp_norm, height=w2, color=ACC2, alpha=0.70, label="Adaptive")

# label actual values
for i, (bb, ba) in enumerate(zip(bl_vals, adp_vals)):
    ax2.text(bl_norm[i] + 1, y_pos[i] + w2/2, f"{bb}", va="center", fontsize=9, color=FG)
    adp_col = ACC2 if adp_norm[i] >= bl_norm[i] else ACC3
    ax2.text(adp_norm[i] + 1, y_pos[i] - w2/2, f"{ba}", va="center", fontsize=9, color=adp_col)

ax2.set_xlim(0, 135)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(metrics_labels, fontsize=10)
ax2.set_title("Full Metrics Comparison\n(Static vs Adaptive)", color=FG, fontsize=13, fontweight="bold", pad=10)
ax2.legend(facecolor=GRID, edgecolor=GRID, labelcolor=FG, fontsize=10)
ax2.tick_params(colors=FG)
ax2.set_xticks([])
for spine in ax2.spines.values():
    spine.set_edgecolor(GRID)
ax2.grid(axis="x", color=GRID, linewidth=0.6)

# ── Panel 3: Complexity cost ───────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)

# scatter: complexity (variants) vs calmar improvement
items = [
    ("Static\n(baseline)", 0, 5.8, GOLD, 200),
    ("Adaptive\n(224 variants)", 224, 3.1, ACC3, 200),
]

for label, x_val, y_val, col, sz in items:
    ax3.scatter([x_val], [y_val], color=col, s=sz, zorder=5, edgecolors=FG, linewidth=1.5)
    ax3.text(x_val, y_val + 0.18, label, ha="center", fontsize=11, color=col, fontweight="bold")

ax3.annotate("", xy=(224, 3.1), xytext=(0, 5.8),
             arrowprops=dict(arrowstyle="-|>", color=ACC3, lw=2))
ax3.text(112, 4.6, "−2.7 Calmar\n−637 trades\n−53pp Ann. Return",
         ha="center", fontsize=10, color=ACC3,
         bbox=dict(facecolor=GRID, edgecolor=ACC3, boxstyle="round,pad=0.4"))

ax3.set_xlim(-40, 280)
ax3.set_ylim(0, 8)
ax3.set_xlabel("Number of Variants Tested", color=FG, fontsize=11)
ax3.set_ylabel("Calmar Ratio (Portfolio)", color=FG, fontsize=11)
ax3.set_title("Complexity vs\nRisk-Adjusted Return", color=FG, fontsize=13, fontweight="bold", pad=10)
ax3.tick_params(colors=FG)
for spine in ax3.spines.values():
    spine.set_edgecolor(GRID)
ax3.grid(color=GRID, linewidth=0.6)

# regime split table
ax3.text(0.5, 0.08,
         "Regime params: 3 × 6 = 18 variables\n"
         "EV/trade: +3.6 bp gain\n"
         "Trade count: 2,265 → 1,628 (−28%)",
         ha="center", transform=ax3.transAxes, fontsize=9.5, color=FG,
         bbox=dict(facecolor=GRID, edgecolor=GRID, boxstyle="round,pad=0.4"))

fig.text(0.5, 0.01,
         "Source: r42 · 224 variants (Low/Mid/High vol) · 6yr live Binance data · 50 USDT-M perpetuals",
         ha="center", fontsize=10, color="#8b949e",
         bbox=dict(facecolor=BG, edgecolor=GRID, boxstyle="round,pad=0.3"))

plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {OUT}")
