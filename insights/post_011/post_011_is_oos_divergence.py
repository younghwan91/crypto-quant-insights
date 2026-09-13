"""
Quant Insight #011 — "Your In-Sample PF Was 2.16. Your Out-of-Sample PF Was 1.38."
====================================================================================
Research base: r59 OOS validation (2026-03-11)
Data: 60 USDT-M perpetuals, 6yr, IS: 2020-2022 / OOS: 2023-2025
7 parameter variants, optimized on IS only, evaluated on OOS without modification.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Data from r59 (2026-03-11) ─────────────────────────────────────────────
# 7 variants optimized on IS (2020-2022), evaluated on OOS (2023-2025)
variants = [
    # (label,           IS_PF,  OOS_PF, OOS/IS)
    ("Variant A",        2.16,   1.38,  0.64),
    ("Variant B",        2.41,   1.42,  0.59),
    ("Variant C",        2.67,   1.47,  0.55),
    ("Variant D",        2.93,   1.49,  0.51),
    ("Variant E",        3.14,   1.51,  0.48),
    ("Variant F",        3.35,   1.55,  0.46),
    ("Variant G",        3.51,   1.58,  0.45),
]

labels  = [v[0] for v in variants]
is_pf   = np.array([v[1] for v in variants])
oos_pf  = np.array([v[2] for v in variants])
ratio   = np.array([v[3] for v in variants])

# ── Colors ──────────────────────────────────────────────────────────────────
BG_DARK    = '#0d1117'
BG_CARD    = '#161b22'
BG_BORDER  = '#30363d'
TEXT_MAIN  = '#f0f6fc'
TEXT_SUB   = '#8b949e'
GREEN      = '#3fb950'
RED        = '#f85149'
ACCENT     = '#58a6ff'
ORANGE     = '#d29922'

plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG_DARK)

gs = fig.add_gridspec(1, 2, hspace=0.4, wspace=0.38,
                      top=0.82, bottom=0.12, left=0.07, right=0.97)
ax1 = fig.add_subplot(gs[0, 0])  # IS vs OOS PF grouped bars
ax2 = fig.add_subplot(gs[0, 1])  # OOS/IS ratio bars with threshold

for ax in [ax1, ax2]:
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TEXT_MAIN, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_BORDER)
    ax.title.set_color(TEXT_MAIN)
    ax.xaxis.label.set_color(TEXT_SUB)
    ax.yaxis.label.set_color(TEXT_SUB)

# ── Chart 1: IS vs OOS Profit Factor ─────────────────────────────────────
x = np.arange(len(labels))
w = 0.35

bars_is  = ax1.bar(x - w/2, is_pf,  w, color=ACCENT,  alpha=0.85,
                   edgecolor=BG_BORDER, linewidth=0.8, label='IS PF (2020–2022)', zorder=3)
bars_oos = ax1.bar(x + w/2, oos_pf, w, color=ORANGE, alpha=0.90,
                   edgecolor=BG_BORDER, linewidth=0.8, label='OOS PF (2023–2025)', zorder=3)

# Labels on bars
for bar in bars_is:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 0.03, f'{h:.2f}',
             ha='center', va='bottom', fontsize=8, color=ACCENT, fontweight='bold')
for bar in bars_oos:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 0.03, f'{h:.2f}',
             ha='center', va='bottom', fontsize=8, color=ORANGE, fontweight='bold')

ax1.axhline(1.0, color=RED, ls='--', lw=1.2, alpha=0.7, zorder=2)
ax1.text(len(labels) - 0.5, 1.04, 'Break-even (PF=1.0)',
         color=RED, fontsize=8, ha='right')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=9)
ax1.set_ylabel('Profit Factor', fontsize=10)
ax1.set_ylim(0, 4.2)
ax1.set_title('IS vs OOS Profit Factor\nAcross 7 Parameter Variants',
              fontsize=11, fontweight='bold', pad=10)
ax1.legend(fontsize=9, loc='upper left',
           facecolor='#21262d', edgecolor=BG_BORDER)
ax1.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# Annotation: winner-of-IS perspective
ax1.annotate('IS "winner"\n(PF 3.51)',
             xy=(6 - w/2, 3.51), xytext=(4.8, 3.75),
             fontsize=8, color=ACCENT,
             arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d',
                       edgecolor=ACCENT, alpha=0.85))
ax1.annotate('OOS result\n(PF 1.58)',
             xy=(6 + w/2, 1.58), xytext=(5.0, 2.1),
             fontsize=8, color=ORANGE,
             arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d',
                       edgecolor=ORANGE, alpha=0.85))

# ── Chart 2: OOS/IS Ratio ─────────────────────────────────────────────────
bar_colors = [RED if r < 0.85 else GREEN for r in ratio]
bars_r = ax2.bar(x, ratio, 0.55, color=bar_colors, alpha=0.88,
                 edgecolor=BG_BORDER, linewidth=0.8, zorder=3)

for bar, r in zip(bars_r, ratio):
    ax2.text(bar.get_x() + bar.get_width()/2, r + 0.008, f'{r:.2f}',
             ha='center', va='bottom', fontsize=9, color=TEXT_MAIN, fontweight='bold')

ax2.axhline(0.85, color=GREEN, ls='--', lw=1.5, alpha=0.8, zorder=2)
ax2.text(len(labels) - 1, 0.87, 'Threshold (0.85)',
         color=GREEN, fontsize=8.5, ha='right')

ax2.fill_between([-0.5, len(labels) - 0.5], 0, 0.85,
                 color=RED, alpha=0.06, zorder=1)

ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=9)
ax2.set_ylabel('OOS / IS Profit Factor Ratio', fontsize=10)
ax2.set_ylim(0, 1.05)
ax2.set_title('OOS/IS Ratio — All Variants Failed 0.85 Threshold\n'
              '(Range: 0.45 – 0.64,  every single one below the bar)',
              fontsize=11, fontweight='bold', pad=10)
ax2.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# Zero-crossing label
ax2.text(3, 0.12, 'All 7 variants\nbelow threshold',
         ha='center', va='bottom', fontsize=10, color=RED,
         fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#21262d',
                   edgecolor=RED, alpha=0.85))

# ── Title & Footer ───────────────────────────────────────────────────────────
fig.text(0.50, 0.93, 'Your In-Sample PF Was 2.16. Your Out-of-Sample PF Was 1.38.',
         ha='center', fontsize=16, fontweight='bold', color=TEXT_MAIN)
fig.text(0.50, 0.88,
         'IS/OOS validation: 7 variants, 60 USDT-M perpetuals, '
         'IS 2020–2022 / OOS 2023–2025 · strict temporal split',
         ha='center', fontsize=10, color=TEXT_SUB)

fig.text(0.50, 0.04,
         '60 USDT-M perpetuals  ·  6yr live Binance data  ·  '
         '7 variants  ·  IS: 2020–2022 / OOS: 2023–2025  ·  strict temporal split',
         ha='center', fontsize=9, color=TEXT_SUB, style='italic')

out = Path(__file__).parent / 'post_011_is_oos_divergence.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
print(f'Saved: {out}')
