"""
Quant Insight #002 — Win Rate 70% vs R:R 2:1 — Which Actually Survives?
=========================================================================
Research base: r8 stress test (2026-02-20), commit 3f63b4c
Data: 6yr USDT-M futures, 50 symbols

Key finding: High win-rate config dies if WR drops 6pp.
High R:R configs survive 19-22pp WR drops. Structurally different beasts.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BG_DARK   = '#0d1117'
BG_CARD   = '#161b22'
BG_BORDER = '#30363d'
TEXT_MAIN = '#f0f6fc'
TEXT_SUB  = '#8b949e'
GREEN     = '#3fb950'
RED       = '#f85149'
ACCENT    = '#58a6ff'
ORANGE    = '#d29922'

# ── Data from r8 research (2026-02-20) ───────────────────────────────────────
# Breakeven WR analysis: BE_WR = 1 / (1 + R:R)
configs = [
    # (name,                 rr,    be_wr, actual_wr, margin_pp, pf_bull, pf_chop, pf_bear)
    ("Prod Baseline\n(High WR)",    0.60,  62.5, 68.5,  6.0, 1.38, 1.32, 1.27),
    ("Config A\n(Balanced)",        1.16,  46.3, 67.6, 21.3, 1.39, 1.30, 1.28),
    ("Config B\n(Balanced+)",       1.22,  45.0, 66.7, 21.7, 1.40, 1.32, 1.25),
    ("Config C\n(Wide Stop)",       1.34,  42.7, 64.5, 21.8, 1.41, 1.28, 1.28),
    ("Config D\n(High R:R)",        1.66,  37.6, 56.8, 19.2, 1.31, 1.27, 1.25),
]
names     = [c[0] for c in configs]
rr        = np.array([c[1] for c in configs])
be_wr     = np.array([c[2] for c in configs])
actual_wr = np.array([c[3] for c in configs])
margin    = np.array([c[4] for c in configs])
pf_bull   = np.array([c[5] for c in configs])
pf_chop   = np.array([c[6] for c in configs])
pf_bear   = np.array([c[7] for c in configs])

plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG_DARK)

gs = fig.add_gridspec(2, 2, hspace=0.5, wspace=0.35,
                      top=0.81, bottom=0.08, left=0.07, right=0.97)
ax1 = fig.add_subplot(gs[0, 0])   # WR margin bar chart
ax2 = fig.add_subplot(gs[0, 1])   # WR breakdown (actual vs breakeven)
ax3 = fig.add_subplot(gs[1, :])   # Regime PF heatmap

for ax in [ax1, ax2, ax3]:
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TEXT_MAIN, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_BORDER)
    ax.title.set_color(TEXT_MAIN)
    ax.xaxis.label.set_color(TEXT_SUB)
    ax.yaxis.label.set_color(TEXT_SUB)

x = np.arange(len(names))

# ── Chart 1: WR Safety Margin ────────────────────────────────────────────────
bar_colors = [RED if m < 10 else (ORANGE if m < 15 else GREEN) for m in margin]
bars = ax1.bar(x, margin, color=bar_colors, edgecolor=BG_BORDER,
               linewidth=0.8, width=0.55, alpha=0.9, zorder=3)
ax1.axhline(10, color=ORANGE, ls='--', lw=1.2, alpha=0.7)
ax1.axhline(5, color=RED, ls='--', lw=1.2, alpha=0.7)
ax1.text(len(x) - 0.5, 10.3, 'Comfortable', color=ORANGE, fontsize=8, ha='right')
ax1.text(len(x) - 0.5, 5.3, 'Danger', color=RED, fontsize=8, ha='right')
for b, m in zip(bars, margin):
    ax1.text(b.get_x() + b.get_width()/2, m + 0.3, f'+{m:.1f}pp',
             ha='center', fontsize=9, fontweight='bold', color=TEXT_MAIN)
ax1.set_xticks(x)
ax1.set_xticklabels(names, fontsize=8.5)
ax1.set_ylabel('WR Safety Margin (pp before breakeven)', fontsize=9)
ax1.set_title('How Much Can Win Rate Drop\nBefore Strategy Breaks?', fontsize=11,
              fontweight='bold', pad=10)
ax1.set_ylim(0, 27)
ax1.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# ── Chart 2: Actual WR vs Breakeven WR ───────────────────────────────────────
bar_w = 0.35
bars_actual = ax2.bar(x - bar_w/2, actual_wr, bar_w, color=ACCENT,
                      alpha=0.85, label='Actual Win Rate', edgecolor=BG_BORDER, zorder=3)
bars_be = ax2.bar(x + bar_w/2, be_wr, bar_w, color=RED,
                  alpha=0.65, label='Breakeven Win Rate', edgecolor=BG_BORDER, zorder=3)
for i, (a, b) in enumerate(zip(actual_wr, be_wr)):
    ax2.annotate('', xy=(i + bar_w/2, b), xytext=(i - bar_w/2, a),
                 arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5,
                                 connectionstyle='arc3,rad=0.2'), zorder=5)
ax2.set_xticks(x)
ax2.set_xticklabels(names, fontsize=8.5)
ax2.set_ylabel('Win Rate (%)', fontsize=9)
ax2.set_ylim(30, 75)
ax2.set_title('Actual WR vs Breakeven WR\n(gap = buffer before ruin)', fontsize=11,
              fontweight='bold', pad=10)
ax2.legend(fontsize=8, facecolor='#21262d', edgecolor=BG_BORDER)
ax2.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# ── Chart 3: Regime PF heatmap ────────────────────────────────────────────────
regime_data = np.array([pf_bull, pf_chop, pf_bear]).T   # shape (5, 3)
regimes = ['Bull Market', 'Choppy/Sideways', 'Bear Market']

# draw as grouped lines instead of heatmap
regime_colors = [GREEN, ORANGE, RED]
regime_labels = ['Bull (41.7% of 6yr)', 'Chop (28.5%)', 'Bear (29.8%)']
# label offsets per regime: bull above, chop middle-above, bear below — avoid stack overlap
label_offsets = [+0.010, +0.004, -0.010]
for j, (color, label, offset) in enumerate(zip(regime_colors, regime_labels, label_offsets)):
    pf_vals = regime_data[:, j]
    ax3.plot(x, pf_vals, color=color, linewidth=2.5, marker='o',
             markersize=9, markerfacecolor=BG_DARK, markeredgewidth=2.5,
             label=label, zorder=4)
    for i, v in enumerate(pf_vals):
        va = 'bottom' if offset >= 0 else 'top'
        ax3.text(i, v + offset, f'{v:.2f}', ha='center', fontsize=8,
                 va=va, color=color, fontweight='bold')

ax3.axhline(1.0, color=TEXT_SUB, ls='--', lw=1, alpha=0.4)
ax3.fill_between(np.linspace(-0.5, len(x)-0.5, 100), 1.0, 0.9,
                 alpha=0.07, color=RED)
ax3.set_xticks(x)
ax3.set_xticklabels(names, fontsize=9)
ax3.set_ylabel('Profit Factor by Market Regime', fontsize=9)
ax3.set_title('Does Edge Hold Across All Market Regimes?\n'
              '(Bull / Chop / Bear — classified by 30-day BTC return)',
              fontsize=11, fontweight='bold', pad=10)
ax3.legend(fontsize=9, facecolor='#21262d', edgecolor=BG_BORDER, loc='upper right')
ax3.set_ylim(1.20, 1.52)
ax3.set_xlim(-0.5, len(x) - 0.5)
ax3.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# Key callouts
ax3.annotate('Prod (High WR):\nonly 6pp safety margin',
             xy=(0, pf_bear[0]), xytext=(0.6, 1.225),
             fontsize=8, color=RED,
             arrowprops=dict(arrowstyle='->', color=RED, lw=1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d', edgecolor=RED, alpha=0.85))
ax3.annotate('High R:R:\n19-22pp safety margin',
             xy=(4, pf_bear[4]), xytext=(2.85, 1.475),
             fontsize=8, color=GREEN,
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d', edgecolor=GREEN, alpha=0.85))

# Title & footer
fig.text(0.5, 0.955, 'Win Rate 70% vs R:R 2:1 — Which Strategy Actually Survives?',
         ha='center', fontsize=15, fontweight='bold', color=TEXT_MAIN)
fig.text(0.5, 0.905,
         '50 USDT-M perpetuals  |  6yr live Binance data  |  0.04%/side fees  |  Bull / Chop / Bear regime',
         ha='center', fontsize=9.5, color=TEXT_SUB)
fig.text(0.5, 0.01,
         'High win-rate strategies are fragile by design: their edge disappears faster as conditions change. '
         'High R:R strategies have structural safety margins that make them more robust to regime shifts.',
         ha='center', fontsize=9, color='#c9d1d9', style='italic',
         bbox=dict(boxstyle='round,pad=0.45', facecolor='#21262d', edgecolor='#444c56', alpha=0.85))

out = Path(__file__).parent / "post_002_wr_vs_rr.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
print(f"Saved -> {out}")
plt.close()
