"""
Quant Insight #013 — "Kelly Said 154x. We Run 30x. Here's Why That's the Right Choice."
=========================================================================================
Research base: r63 Kelly audit (2026-03-11)
Data: 60 USDT-M perpetuals, 6yr
Kelly computed from live WR/RR metrics at two strategy points.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Data from r63 Kelly audit ───────────────────────────────────────────────
# Two strategic states: initial and post-improvement
states = {
    'Initial\n(WR 25.9%, RR 3.75)': {'wr': 0.259, 'rr': 3.75, 'kelly': 30.7, 'adopted': 30},
    'Post-improvement\n(WR 62.9%, RR 1.16)': {'wr': 0.629, 'rr': 1.16, 'kelly': 154.0, 'adopted': 30},
}

# Kelly curve as WR varies (RR fixed at 1.16)
wr_range = np.linspace(0.20, 0.75, 200)
rr_fixed = 1.16
kelly_curve = (wr_range - (1 - wr_range) / rr_fixed) * 10 / 0.01  # L = f% × slots / SL%
kelly_curve = np.clip(kelly_curve, 0, 250)

# Colors
BG_DARK    = '#0d1117'
BG_CARD    = '#161b22'
BG_BORDER  = '#30363d'
TEXT_MAIN  = '#f0f6fc'
TEXT_SUB   = '#8b949e'
GREEN      = '#3fb950'
RED        = '#f85149'
ACCENT     = '#58a6ff'
ORANGE     = '#d29922'
PURPLE     = '#bc8cff'

plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG_DARK)

gs = fig.add_gridspec(1, 2, hspace=0.4, wspace=0.40,
                      top=0.82, bottom=0.12, left=0.07, right=0.97)
ax1 = fig.add_subplot(gs[0, 0])  # Kelly curve with WR
ax2 = fig.add_subplot(gs[0, 1])  # Bar comparison: Kelly vs Adopted leverage

for ax in [ax1, ax2]:
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TEXT_MAIN, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_BORDER)
    ax.title.set_color(TEXT_MAIN)
    ax.xaxis.label.set_color(TEXT_SUB)
    ax.yaxis.label.set_color(TEXT_SUB)

# ── Chart 1: Kelly vs WR curve ───────────────────────────────────────────
ax1.plot(wr_range * 100, kelly_curve, color=ACCENT, lw=2.5, zorder=4,
         label='Kelly leverage (R:R = 1.16, 10 slots, SL 1%)')

# Mark initial state (WR=25.9%)
kelly_initial_on_curve = max(0, (0.259 - (1 - 0.259) / 3.75) * 10 / 0.01)
ax1.scatter([25.9], [30.7], color=ORANGE, s=110, zorder=6, label='Initial: Kelly=30.7x')
ax1.axhline(30, color=ORANGE, ls='--', lw=1.2, alpha=0.6, zorder=3)
ax1.text(22, 33, 'Adopted: 30x', color=ORANGE, fontsize=8.5)

# Mark current state (WR=62.9%)
ax1.scatter([62.9], [154], color=RED, s=130, zorder=6, label='Post-improvement: Kelly=154x')
ax1.axhline(154, color=RED, ls='--', lw=1.2, alpha=0.5, zorder=3)
ax1.text(22, 157, 'New Kelly: 154x', color=RED, fontsize=8.5)

# Shade "dangerous zone" > 77x (half-kelly > adopted)
ax1.fill_between(wr_range * 100, 77, kelly_curve,
                 where=kelly_curve > 77,
                 color=RED, alpha=0.08, zorder=1, label='Half-Kelly > 77x (implausible)')

ax1.axhline(77, color=PURPLE, ls=':', lw=1.2, alpha=0.5, zorder=3)
ax1.text(22, 80, 'Half-Kelly at 154x = 77x leverage', color=PURPLE, fontsize=8)

ax1.set_xlabel('Win Rate (%)', fontsize=10)
ax1.set_ylabel('Full Kelly Leverage (x)', fontsize=10)
ax1.set_xlim(20, 76)
ax1.set_ylim(-10, 220)
ax1.set_title('Kelly Leverage vs Win Rate\n'
              '(R:R = 1.16 · 10 position slots · 1% stop-loss per trade)',
              fontsize=11, fontweight='bold', pad=10)
ax1.legend(fontsize=8, loc='upper left',
           facecolor='#21262d', edgecolor=BG_BORDER)
ax1.grid(alpha=0.12, color=BG_BORDER, zorder=0)

# Annotation: nonlinear jump
ax1.annotate('25.9% → 62.9% WR\n≈ ×50 Kelly jump',
             xy=(62.9, 154), xytext=(44, 175),
             fontsize=9, color=TEXT_MAIN,
             arrowprops=dict(arrowstyle='->', color=TEXT_MAIN, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d',
                       edgecolor=TEXT_SUB, alpha=0.85))

# ── Chart 2: Kelly vs Adopted Leverage Comparison ─────────────────────────
categories = ['Initial\n(WR 25.9%,\nRR 3.75)',
              'Post-improvement\n(WR 62.9%,\nRR 1.16)',
              'MA Cluster\n(WR 36.7%,\nRR 2.21)']
kelly_vals   = [30.7,  154.0, 20.1]
adopted_vals = [30.0,   30.0, 21.0]

x = np.arange(len(categories))
w = 0.35

bars_k = ax2.bar(x - w/2, kelly_vals, w, color=RED, alpha=0.80,
                 edgecolor=BG_BORDER, linewidth=0.8, label='Full Kelly', zorder=3)
bars_a = ax2.bar(x + w/2, adopted_vals, w, color=GREEN, alpha=0.88,
                 edgecolor=BG_BORDER, linewidth=0.8, label='Adopted Leverage', zorder=3)

for bar, val in zip(bars_k, kelly_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 2,
             f'{val:.0f}x', ha='center', va='bottom',
             fontsize=10, color=RED, fontweight='bold')
for bar, val in zip(bars_a, adopted_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 2,
             f'{val:.0f}x', ha='center', va='bottom',
             fontsize=10, color=GREEN, fontweight='bold')

# Danger annotation for the 154x bar
ax2.annotate('Portfolio risk:\n770% of equity\nacross 10 slots',
             xy=(1 - w/2, 154), xytext=(1.2, 168),
             fontsize=8.5, color=RED,
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d',
                       edgecolor=RED, alpha=0.85))

ax2.axhline(77, color=PURPLE, ls=':', lw=1.2, alpha=0.5)
ax2.text(2.5, 80, 'Half-Kelly = 77x', color=PURPLE, fontsize=8, ha='right')

ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=8.5)
ax2.set_ylabel('Leverage (x)', fontsize=10)
ax2.set_ylim(0, 190)
ax2.set_title('Full Kelly vs Adopted Leverage\n'
              'Post-improvement: Kelly 5x higher — still using 30x',
              fontsize=11, fontweight='bold', pad=10)
ax2.legend(fontsize=9, loc='upper center',
           facecolor='#21262d', edgecolor=BG_BORDER)
ax2.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# ── Title & Footer ───────────────────────────────────────────────────────────
fig.text(0.50, 0.93,
         'Kelly Said 154x. We Run 30x. Here\'s Why That\'s the Right Choice.',
         ha='center', fontsize=15, fontweight='bold', color=TEXT_MAIN)
fig.text(0.50, 0.88,
         'Win rate improved 25.9% → 62.9%  ·  Kelly multiplied ×50  ·  '
         'Leverage unchanged at 30x  ·  Portfolio constraint beats per-trade math',
         ha='center', fontsize=10, color=TEXT_SUB)

fig.text(0.50, 0.04,
         '60 USDT-M perpetuals  ·  6yr live Binance data  ·  '
         'Kelly computed from live WR/RR metrics  ·  MA: WR=36.7%, RR=2.21, Kelly=20.1x (adopted: 21x)',
         ha='center', fontsize=9, color=TEXT_SUB, style='italic')

out = Path(__file__).parent / 'post_013_kelly_leverage.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
print(f'Saved: {out}')
