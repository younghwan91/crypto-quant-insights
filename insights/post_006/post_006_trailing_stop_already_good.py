"""Post 006: Your Trailing Stop Is Probably Already Good Enough."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

OUT = Path(__file__).parent / "post_006_trailing_stop_already_good.png"

BG   = "#0d1117"
FG   = "#e6edf3"
GRID = "#21262d"
ACC1 = "#58a6ff"
ACC2 = "#3fb950"
ACC3 = "#f85149"
GOLD = "#d29922"
GRAY = "#484f58"

variants = [
    ("B-T07",  1022, "Tighter ATR×0.7",     False, True),
    ("P-PcDy", 1006, "POC dynamic floor",    False, False),
    ("L-TtSp", 1005, "Time step →0.5@25b",  False, False),
    ("A-Base", 1004, "Baseline",             True,  False),
    ("M-VwF5", 1004, "VWMA floor ×0.5",     False, False),
    ("N-VwF3", 1004, "VWMA floor ×0.3",     False, False),
    ("O-PcSt", 1004, "POC static floor",     False, False),
    ("S-MH4",  1004, "Max hold ×4.0",        False, False),
    ("T-MH5",  1004, "Max hold ×5.0",        False, False),
    ("E-SU30", 1004, "Step-up 30% @2×",     False, False),
    ("F-SU50", 1004, "Step-up 50% @2×",     False, False),
    ("G-SU50E",1004, "Step-up 50% @1.5×",   False, False),
    ("J-MPrg", 991,  "Progressive 2.0→0.3", False, False),
    ("Q-GAm",  993,  "Gain-adapt mild",      False, False),
    ("W-VwGA", 993,  "VWMA + gain-adapt",   False, False),
    ("K-TtLn", 965,  "Time linear 1.5→0.3", False, False),
    ("H-MP15", 969,  "Multi-phase 1.5→0.5", False, False),
    ("V-MPM4", 969,  "Multi-phase+MH4",      False, False),
    ("C-T15",  944,  "Looser ATR×1.5",       False, False),
    ("U-T15S", 944,  "Loose+step-up",        False, False),
    ("X-Full", 943,  "All combined",         False, False),
    ("I-MP20", 919,  "Multi-phase 2.0→0.3", False, False),
    ("R-GAa",  902,  "Gain-adapt aggressive",False, False),
    ("D-T20",  893,  "Very loose ATR×2.0",  False, False),
]

labels = [v[0] for v in variants]
calmars = [v[1] for v in variants]
is_base = [v[3] for v in variants]
is_best = [v[4] for v in variants]

fig = plt.figure(figsize=(18, 11), facecolor=BG)
fig.text(0.5, 0.960, "Your Trailing Stop Is Probably Already Good Enough",
         ha="center", va="center", fontsize=24, fontweight="bold", color=FG)
fig.text(0.5, 0.915, "24 trailing stop innovations tested · Runner win rate 99.9% · Best improvement: +1.8% Calmar",
         ha="center", va="center", fontsize=13, color="#8b949e")

gs = gridspec.GridSpec(1, 3, figure=fig,
                       left=0.07, right=0.97, top=0.83, bottom=0.10,
                       wspace=0.32)

# ── Panel 1: Calmar for all 24 variants (horizontal bar) ─────────────────
ax1 = fig.add_subplot(gs[0:2])
ax1.set_facecolor(BG)

y = np.arange(len(variants))
bar_colors = []
for base, best in zip(is_base, is_best):
    if best:
        bar_colors.append(ACC2)
    elif base:
        bar_colors.append(GOLD)
    else:
        bar_colors.append(ACC1)

# color zero-effect variants gray
zero_effect = {"E-SU30", "F-SU50", "G-SU50E", "S-MH4", "T-MH5", "M-VwF5", "N-VwF3"}
bar_colors = []
for v in variants:
    if v[0] in zero_effect:
        bar_colors.append(GRAY)
    elif v[4]:
        bar_colors.append(ACC2)
    elif v[3]:
        bar_colors.append(GOLD)
    else:
        bar_colors.append(ACC1)

bars = ax1.barh(y, calmars, color=bar_colors, height=0.7, alpha=0.9)
ax1.axvline(1004, color=GOLD, linestyle="--", linewidth=1.5, alpha=0.8, label="Baseline (1004)")

for i, (bar, val) in enumerate(zip(bars, calmars)):
    ax1.text(val + 3, bar.get_y() + bar.get_height()/2,
             f"{val}", va="center", fontsize=8.5, color=FG)

ax1.set_xlim(820, 1110)
ax1.set_yticks(y)
ax1.set_yticklabels(labels, fontsize=9)
ax1.set_xlabel("Calmar Ratio", color=FG, fontsize=11)
ax1.set_title("Calmar Across 24 Trailing Variants", color=FG, fontsize=13, fontweight="bold", pad=10)
ax1.tick_params(colors=FG)
for spine in ax1.spines.values():
    spine.set_edgecolor(GRID)
ax1.grid(axis="x", color=GRID, linewidth=0.6)

# Legend patches
from matplotlib.patches import Patch
legend_elements = [
    Patch(color=ACC2, label="Best (B-T07 tighter trail)"),
    Patch(color=GOLD, label="Baseline"),
    Patch(color=ACC1, label="Other variants"),
    Patch(color=GRAY, label="Zero effect (same as baseline)"),
]
ax1.legend(handles=legend_elements, facecolor=GRID, edgecolor=GRID,
           labelcolor=FG, fontsize=9, loc="lower right")

# ── Panel 3: Runner breakdown + bar comparison ────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)

# Trade composition pie
sizes = [70.6, 14.7, 14.7]
pie_labels = ["Pre-TP1 exits\n(70.6%)", "TP1 partial\n(14.7%)", "Runners\n(14.7%)"]
pie_colors = [ACC3, ACC1, ACC2]
wedges, _ = ax3.pie(sizes, labels=None, colors=pie_colors,
                     startangle=90, wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2))

ax3.set_title("Trade Composition\n& Runner WR", color=FG, fontsize=13, fontweight="bold", pad=10)

for i, (wedge, label) in enumerate(zip(wedges, pie_labels)):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x_t = 1.25 * np.cos(np.radians(angle))
    y_t = 1.25 * np.sin(np.radians(angle))
    ax3.text(x_t, y_t, label, ha="center", va="center",
             fontsize=9.5, color=FG)

# Center text
ax3.text(0, 0, "Runner\nWR\n99.9%", ha="center", va="center",
         fontsize=13, fontweight="bold", color=ACC2)

# Annotate runner avg bars below
ax3.text(0, -1.55,
         "Baseline runners exit in avg 6.9 bars\n"
         "Tighter trail (B-T07): 4.6 bars  → +190 trades\n"
         "Looser trail (D-T20): 18.4 bars → −788 trades",
         ha="center", va="center", fontsize=9.5, color=FG,
         bbox=dict(facecolor=GRID, edgecolor=GRID, boxstyle="round,pad=0.4"))

fig.text(0.5, 0.01,
         "Source: r12 · 24 trailing stop variants · 6yr live Binance data · 50 USDT-M perpetuals",
         ha="center", fontsize=10, color="#8b949e",
         bbox=dict(facecolor=BG, edgecolor=GRID, boxstyle="round,pad=0.3"))

plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {OUT}")
