"""
Quant Insight #003 — The Long Bias That Stopped Working
=========================================================
Research base: direction asymmetry analysis (2026-02-21), commit 614a449
Data: 6yr USDT-M futures, 50 symbols, 17,165 trades

Key finding: Long positions had +25% EV advantage in 2020-21.
By 2025-26 that advantage fully reversed — shorts now outperform.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

BG_DARK   = '#0d1117'
BG_CARD   = '#161b22'
BG_BORDER = '#30363d'
TEXT_MAIN = '#f0f6fc'
TEXT_SUB  = '#8b949e'
GREEN     = '#3fb950'
RED       = '#f85149'
ACCENT    = '#58a6ff'
ORANGE    = '#d29922'
PURPLE    = '#bc8cff'

# ── Data from direction asymmetry research (2026-02-21) ──────────────────────
years = ['2020-21', '2021-22', '2022-23', '2023-24', '2024-25', '2025-26']
long_ev  = np.array([6.544, 4.679, 3.319, 2.833, 2.830, 2.353])
short_ev = np.array([4.706, 3.512, 2.434, 2.117, 2.710, 2.592])
gap      = long_ev - short_ev       # positive = Long wins, negative = Short wins
long_pf  = np.array([2.62, 1.70, 1.52, 1.52, 1.49, 1.39])
short_pf = np.array([2.14, 1.49, 1.33, 1.36, 1.44, 1.40])
long_wr  = np.array([66.4, 57.0, 56.0, 54.4, 53.6, 51.5])
short_wr = np.array([63.8, 55.9, 53.9, 53.1, 55.2, 54.6])

x = np.arange(len(years))

plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG_DARK)

gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.35,
                      top=0.81, bottom=0.09, left=0.07, right=0.97)
ax1 = fig.add_subplot(gs[0, :])   # EV% per year — full width
ax2 = fig.add_subplot(gs[1, 0])   # L-S gap bar
ax3 = fig.add_subplot(gs[1, 1])   # WR convergence

for ax in [ax1, ax2, ax3]:
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TEXT_MAIN, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_BORDER)
    ax.title.set_color(TEXT_MAIN)
    ax.xaxis.label.set_color(TEXT_SUB)
    ax.yaxis.label.set_color(TEXT_SUB)

# ── Chart 1: EV% per year (Long vs Short) ────────────────────────────────────
ax1.plot(x, long_ev,  color=GREEN, lw=2.8, marker='o', markersize=9,
         markerfacecolor=BG_DARK, markeredgewidth=2.5, label='Long EV% per trade', zorder=5)
ax1.plot(x, short_ev, color=RED,   lw=2.8, marker='s', markersize=9,
         markerfacecolor=BG_DARK, markeredgewidth=2.5, label='Short EV% per trade', zorder=5)

# shaded gap
ax1.fill_between(x, long_ev, short_ev,
                 where=(long_ev >= short_ev), alpha=0.12, color=GREEN, label='Long advantage')
ax1.fill_between(x, long_ev, short_ev,
                 where=(long_ev < short_ev),  alpha=0.18, color=RED,   label='Short advantage')

# value labels — long above, short below, avoid overlap at last points
for i, (l, s) in enumerate(zip(long_ev, short_ev)):
    ax1.text(i, l + 0.18, f'{l:.2f}%', ha='center', fontsize=8.5, color=GREEN,
             fontweight='bold', va='bottom')
    ax1.text(i, s - 0.18, f'{s:.2f}%', ha='center', fontsize=8.5, color=RED,
             fontweight='bold', va='top')

# reversal annotation
ax1.axvline(4.5, color=ORANGE, ls='--', lw=1.5, alpha=0.6)
ax1.text(4.55, 5.5, 'Reversal\npoint', color=ORANGE, fontsize=8.5,
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d', edgecolor=ORANGE, alpha=0.8))

ax1.set_xticks(x)
ax1.set_xticklabels(years, fontsize=10)
ax1.set_ylabel('Expected Value per Trade (%)', fontsize=9)
ax1.set_ylim(1.2, 7.5)
ax1.set_title('Long vs Short Expected Value per Trade — Year by Year (6yr, 50 symbols)',
              fontsize=11, fontweight='bold', pad=10)
legend = ax1.legend(fontsize=9, facecolor='#21262d', edgecolor=BG_BORDER, loc='upper right', ncol=2)
ax1.grid(axis='y', alpha=0.12, color=BG_BORDER)
ax1.set_xlim(-0.4, len(x) - 0.6)

# ── Chart 2: L-S gap bar ─────────────────────────────────────────────────────
bar_colors = [GREEN if g > 0 else RED for g in gap]
bars = ax2.bar(x, gap, color=bar_colors, alpha=0.85, edgecolor=BG_BORDER, linewidth=0.8, width=0.55)
ax2.axhline(0, color=TEXT_SUB, lw=1.2, alpha=0.5)
for b, g in zip(bars, gap):
    ypos = g + 0.05 if g >= 0 else g - 0.18
    ax2.text(b.get_x() + b.get_width()/2, ypos, f'{g:+.2f}pp',
             ha='center', fontsize=9, fontweight='bold',
             color=GREEN if g >= 0 else RED)

ax2.fill_between(np.linspace(-0.5, len(x)-0.5, 100), 0, -0.5,
                 alpha=0.06, color=RED)
ax2.text(len(x)*0.62, -0.32, 'Short territory', color=RED, fontsize=8, alpha=0.7)

ax2.set_xticks(x)
ax2.set_xticklabels(years, fontsize=8.5)
ax2.set_ylabel('Long minus Short EV (pp)', fontsize=9)
ax2.set_title('Long Alpha Decay:\nYearly EV Gap (Long − Short)', fontsize=11,
              fontweight='bold', pad=10)
ax2.set_ylim(-0.5, 2.2)
ax2.grid(axis='y', alpha=0.12, color=BG_BORDER)

# ── Chart 3: WR convergence ───────────────────────────────────────────────────
ax3.plot(x, long_wr,  color=GREEN, lw=2.5, marker='o', markersize=8,
         markerfacecolor=BG_DARK, markeredgewidth=2.5, label='Long WR')
ax3.plot(x, short_wr, color=RED,   lw=2.5, marker='s', markersize=8,
         markerfacecolor=BG_DARK, markeredgewidth=2.5, label='Short WR')

for i, (l, s) in enumerate(zip(long_wr, short_wr)):
    # long above, short below — at yr5/6 gap narrows so push further apart
    gap_wr = l - s
    long_offset = +0.5 if gap_wr > 1.5 else +0.9
    short_offset = -1.1 if gap_wr > 1.5 else -1.5
    ax3.text(i, l + long_offset,  f'{l:.1f}', ha='center', fontsize=8, color=GREEN, va='bottom')
    ax3.text(i, s + short_offset, f'{s:.1f}', ha='center', fontsize=8, color=RED,   va='top')

ax3.set_xticks(x)
ax3.set_xticklabels(years, fontsize=8.5)
ax3.set_ylabel('Win Rate (%)', fontsize=9)
ax3.set_title('Win Rate Convergence:\nLong WR fell, Short WR held steady',
              fontsize=11, fontweight='bold', pad=10)
ax3.legend(fontsize=9, facecolor='#21262d', edgecolor=BG_BORDER)
ax3.set_ylim(49, 69)
ax3.grid(axis='y', alpha=0.12, color=BG_BORDER)
ax3.set_xlim(-0.4, len(x) - 0.6)

# key annotation on WR chart
ax3.annotate('Long WR dropped\n14.9pp in 6 years',
             xy=(5, 51.5), xytext=(3.3, 64.5),
             fontsize=8, color=GREEN,
             arrowprops=dict(arrowstyle='->', color=GREEN, lw=1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d', edgecolor=GREEN, alpha=0.8))
ax3.annotate('Short WR: only\n−9.2pp drop',
             xy=(5, 54.6), xytext=(3.5, 57.5),
             fontsize=8, color=RED,
             arrowprops=dict(arrowstyle='->', color=RED, lw=1),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#21262d', edgecolor=RED, alpha=0.8))

# Title & footer
fig.text(0.5, 0.94, 'The Long Bias That Stopped Working — 6 Years of Crypto Direction Asymmetry',
         ha='center', fontsize=15, fontweight='bold', color=TEXT_MAIN)
fig.text(0.5, 0.905,
         '50 USDT-M perpetuals  |  6yr live Binance data  |  17,165 trades  |  L: 8,452 / S: 8,713',
         ha='center', fontsize=9.5, color=TEXT_SUB)
fig.text(0.5, 0.01,
         'Longs had a structural EV advantage of +1.84pp per trade in 2020-21. '
         'By 2025-26 that gap is gone — and reversed. '
         'Market structure changes. Your backtested edge should too.',
         ha='center', fontsize=9, color='#c9d1d9', style='italic',
         bbox=dict(boxstyle='round,pad=0.45', facecolor='#21262d', edgecolor='#444c56', alpha=0.85))

out = Path(__file__).parent / "post_003_long_short_reversal.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
print(f"Saved -> {out}")
plt.close()
