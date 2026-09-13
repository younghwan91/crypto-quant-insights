"""
Quant Insight #001 — "Why Your 3-Year Crypto Backtest is Lying to You"
======================================================================
Research base: r5 crash-era validation (2026-02-20)
Data: 6yr USDT-M futures, 50 symbols, COVID/Luna/FTX all included

Key finding: Top performers on 3-year data collapsed when tested on 6 years
with real crash regimes. MaxDD nearly doubled for the "winners."
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Data from r5 research (2026-02-20) ───────────────────────────────────────
# All 19 variants: name, 3yr_DD, 6yr_DD, 3yr_PF, 6yr_PF, 3yr_WR, 6yr_WR
variants = [
    # (label,           dd3,  dd6,   pf3,  pf6,   wr3,  wr6,  highlight)
    ("Baseline (prod)",  9.4, 25.3,  1.88, 1.27, 66.6, 61.9, "bad"),
    ("YK-Base",          7.2, 10.7,  2.07, 1.29, 67.1, 62.1, "neutral"),
    ("YK+DL25",          8.3, 12.4,  2.10, 1.29, 67.1, 62.1, "neutral"),
    ("YK+DL50",         10.0, 13.7,  2.11, 1.30, 67.1, 62.1, "neutral"),
    ("YK+Trail1.5x",     7.7, 12.5,  2.24, 1.27, 69.6, 64.0, "neutral"),
    ("YK+Trail1.5x+BE",  7.7, 12.6,  2.23, 1.28, 68.7, 63.1, "neutral"),
    ("YK+Trail2x ★3yr",  6.7, 13.2,  2.21, 1.26, 67.6, 61.7, "bad"),   # 3yr winner, 6yr loser
    ("DL+Trail+BE",      9.8, 14.1,  2.26, 1.28, 68.7, 63.1, "neutral"),
    ("DL+Trail2x",       8.3, 14.8,  2.23, 1.26, 67.6, 61.7, "neutral"),
    ("2-Slot ★6yr",      7.6,  8.2,  2.09, 1.31, 67.3, 62.5, "good"),   # 6yr winner
    ("4-Slot",           8.2, 13.0,  2.05, 1.28, 67.2, 61.9, "neutral"),
    ("Conf≥4 ★6yr",      9.0, 10.0,  2.26, 1.35, 68.8, 63.2, "good"),   # 6yr winner
    ("Steep Scale",      7.3, 11.0,  2.12, 1.30, 67.1, 62.1, "neutral"),
    ("Tight Equity",     7.7, 10.5,  2.07, 1.29, 67.1, 62.1, "good"),
    ("Wide Equity ★3yr", 7.0, 11.9,  2.07, 1.29, 67.1, 62.1, "bad"),    # looked good 3yr
    ("DL+4-Slot",        9.2, 13.8,  2.08, 1.28, 67.2, 61.9, "neutral"),
    ("DL+Scale",         8.0, 12.9,  2.14, 1.31, 67.1, 62.1, "neutral"),
    ("YK+ConfTrail",     9.4, 10.8,  2.05, 1.28, 67.0, 62.4, "neutral"),
    ("Ultra-Combo",      8.7, 14.7,  2.30, 1.29, 68.7, 63.1, "neutral"),
]

labels  = [v[0] for v in variants]
dd3     = np.array([v[1] for v in variants])
dd6     = np.array([v[2] for v in variants])
pf3     = np.array([v[3] for v in variants])
pf6     = np.array([v[4] for v in variants])
wr3     = np.array([v[5] for v in variants])
wr6     = np.array([v[6] for v in variants])
cats    = [v[7] for v in variants]
delta   = dd6 - dd3

COLOR_GOOD    = '#3fb950'   # green
COLOR_BAD     = '#f85149'   # red
COLOR_NEUTRAL = '#8b949e'   # gray
COLOR_ACCENT  = '#58a6ff'   # blue
BG_DARK       = '#0d1117'
BG_CARD       = '#161b22'
BG_BORDER     = '#30363d'
TEXT_MAIN     = '#f0f6fc'
TEXT_SUB      = '#8b949e'

def cat_color(c):
    return COLOR_GOOD if c == "good" else (COLOR_BAD if c == "bad" else COLOR_NEUTRAL)

plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 11))
fig.patch.set_facecolor(BG_DARK)

gs = fig.add_gridspec(2, 3, hspace=0.45, wspace=0.38,
                      top=0.78, bottom=0.08, left=0.06, right=0.97)
ax1 = fig.add_subplot(gs[0, :2])   # Main: DD bar comparison (wide)
ax2 = fig.add_subplot(gs[0, 2])    # Scatter: 3yr PF vs 6yr PF
ax3 = fig.add_subplot(gs[1, :])    # DD delta heatmap row

for ax in [ax1, ax2, ax3]:
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TEXT_MAIN, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_BORDER)
    ax.title.set_color(TEXT_MAIN)
    ax.xaxis.label.set_color(TEXT_SUB)
    ax.yaxis.label.set_color(TEXT_SUB)

# ── Chart 1: Grouped Bar — 3yr vs 6yr MaxDD ──────────────────────────────────
x = np.arange(len(labels))
w = 0.38

bar_colors_3 = [cat_color(c) if c != "neutral" else '#3d444d' for c in cats]
bar_colors_6 = [cat_color(c) if c != "neutral" else '#58a6ff' for c in cats]
# Override: 3yr bars always muted blue, 6yr bars colored by outcome
bars3 = ax1.bar(x - w/2, dd3, w, color='#21262d', edgecolor='#444c56',
                linewidth=0.8, label='MaxDD — 3-Year Backtest', zorder=3)
bars6 = ax1.bar(x + w/2, dd6, w,
                color=[cat_color(c) for c in cats],
                edgecolor=BG_BORDER, linewidth=0.8, alpha=0.9,
                label='MaxDD — 6-Year (with crashes)', zorder=3)

# Arrows showing growth
for i, (d3, d6, c) in enumerate(zip(dd3, dd6, cats)):
    ax1.annotate('', xy=(i + w/2, d6 + 0.3), xytext=(i - w/2, d3 + 0.3),
                 arrowprops=dict(arrowstyle='->', color=cat_color(c),
                                 lw=1.2, connectionstyle='arc3,rad=-0.15'),
                 zorder=5)

ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=38, ha='right', fontsize=8)
ax1.set_ylabel('Max Drawdown (%)', fontsize=10)
ax1.set_title('MaxDD: 3-Year Backtest  vs  6-Year with Crash Regimes\n'
              '(COVID Mar\'20 · China Ban May\'21 · Luna May\'22 · FTX Nov\'22)',
              fontsize=11, fontweight='bold', pad=10)
ax1.axhline(15, color=COLOR_BAD, ls='--', lw=1, alpha=0.5)
ax1.text(len(labels)-0.5, 15.4, 'Danger zone', color=COLOR_BAD, fontsize=8, ha='right')
ax1.grid(axis='y', alpha=0.15, color=BG_BORDER, zorder=0)
ax1.set_ylim(0, 30)

legend_patches = [
    mpatches.Patch(color='#21262d', edgecolor='#444c56', label='3-Year backtest DD'),
    mpatches.Patch(color=COLOR_GOOD, alpha=0.9, label='6-Year — Crash-stable ✓'),
    mpatches.Patch(color=COLOR_BAD,  alpha=0.9, label='6-Year — Fragile ✗'),
    mpatches.Patch(color=COLOR_ACCENT, alpha=0.9, label='6-Year — Neutral'),
]
ax1.legend(handles=legend_patches, fontsize=8, loc='upper left',
           facecolor='#21262d', edgecolor=BG_BORDER, framealpha=0.9)

# ── Chart 2: Scatter — 3yr PF vs 6yr PF ─────────────────────────────────────
sc_colors = [cat_color(c) for c in cats]
ax2.scatter(pf3, pf6, c=sc_colors, s=80, zorder=4, edgecolors='#30363d', linewidth=0.8)

# Diagonal line: where 3yr == 6yr
pf_min, pf_max = 1.2, 2.4
diag = np.linspace(pf_min, pf_max, 100)
ax2.plot(diag, diag, '--', color=TEXT_SUB, lw=1, alpha=0.5, label='No degradation')
ax2.fill_between(diag, diag, 1.0, alpha=0.06, color=COLOR_BAD)

# Annotate the key ones
annots = {
    "Baseline (prod)": ("left", "down"),
    "YK+Trail2x ★3yr": ("left", "up"),
    "2-Slot ★6yr": ("right", "up"),
    "Conf≥4 ★6yr": ("right", "down"),
}
for i, name in enumerate(labels):
    if name in annots:
        ha, va_dir = annots[name]
        dy = 0.02 if va_dir == "up" else -0.03
        ax2.annotate(name.replace(" ★3yr","").replace(" ★6yr",""),
                     (pf3[i], pf6[i]), (pf3[i] + (0.04 if ha=="right" else -0.04), pf6[i] + dy),
                     fontsize=7.5, color=sc_colors[i], ha=ha,
                     arrowprops=dict(arrowstyle='-', color=sc_colors[i], lw=0.8))

ax2.set_xlabel('Profit Factor — 3-Year', fontsize=10)
ax2.set_ylabel('Profit Factor — 6-Year', fontsize=10)
ax2.set_title('PF Degradation:\n3yr → 6yr', fontsize=11, fontweight='bold', pad=10)
ax2.set_xlim(1.8, 2.4); ax2.set_ylim(1.2, 1.45)
ax2.grid(alpha=0.12, color=BG_BORDER)
ax2.legend(fontsize=8, facecolor='#21262d', edgecolor=BG_BORDER)

# ── Chart 3: DD Delta Heatmap Row ─────────────────────────────────────────────
# Sort by delta for the heatmap
sort_idx = np.argsort(delta)
sorted_labels = [labels[i] for i in sort_idx]
sorted_delta  = delta[sort_idx]
sorted_cats   = [cats[i] for i in sort_idx]

# Color by magnitude
cmap_colors = []
for d in sorted_delta:
    if d < 2: cmap_colors.append(COLOR_GOOD)
    elif d < 5: cmap_colors.append(COLOR_NEUTRAL)
    elif d < 8: cmap_colors.append('#d29922')   # orange
    else: cmap_colors.append(COLOR_BAD)

bars_delta = ax3.barh(range(len(sorted_labels)), sorted_delta,
                      color=cmap_colors, edgecolor=BG_BORDER, linewidth=0.7, height=0.72)
ax3.set_yticks(range(len(sorted_labels)))
ax3.set_yticklabels(sorted_labels, fontsize=8.5)
ax3.set_xlabel('MaxDD Increase: 3yr → 6yr (percentage points)', fontsize=10)
ax3.set_title('Crash Resilience Ranking — DD Increase When Adding 3 Years of Real Crashes',
              fontsize=11, fontweight='bold', pad=10)
ax3.axvline(0, color=TEXT_SUB, lw=0.8)
ax3.axvline(5, color='#d29922', ls='--', lw=1, alpha=0.5)
ax3.axvline(10, color=COLOR_BAD, ls='--', lw=1, alpha=0.5)
ax3.text(5.15, -0.8, 'Warning', color='#d29922', fontsize=8)
ax3.text(10.15, -0.8, 'Fragile', color=COLOR_BAD, fontsize=8)
for i, (b, d, lbl) in enumerate(zip(bars_delta, sorted_delta, sorted_labels)):
    ax3.text(d + 0.15, i, f'+{d:.1f}pp', va='center', fontsize=8,
             color=TEXT_MAIN if d > 2 else COLOR_GOOD, fontweight='bold')
ax3.set_xlim(-0.5, 18)
ax3.grid(axis='x', alpha=0.12, color=BG_BORDER)

# ── Main Title ───────────────────────────────────────────────────────────────
fig.text(0.5, 0.965,
         'Why Your 3-Year Crypto Backtest is Lying to You',
         ha='center', fontsize=16, fontweight='bold', color=TEXT_MAIN)
fig.text(0.5, 0.925,
         '19 strategy variants · 50 USDT-M perpetual futures · 6 years of live Binance data · All 4 major crash regimes',
         ha='center', fontsize=10, color=TEXT_SUB)

# ── Key Takeaway Box ─────────────────────────────────────────────────────────
fig.text(0.5, 0.01,
         'The 3-year "winner" (Trail 2x, DD=6.7%) nearly doubled its drawdown to 13.2% under crash regimes.  '
         'The 6-year survivor: just 2 concurrent positions, DD only grew +0.6pp.  '
         'Test through crashes — not around them.',
         ha='center', fontsize=9.5, color='#c9d1d9', style='italic',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#21262d', edgecolor='#444c56', alpha=0.9))

out = Path(__file__).parent / "post_001_3yr_vs_6yr_crash_test.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
print(f"Saved → {out}")
plt.close()
