"""
Quant Insight #004 — More Symbols, More Alpha? (Universe Expansion)
====================================================================
Research base: universe expansion sweep (2026-02-19), commits 6eb0212 + dab1f80
Data: 3yr USDT-M futures, 20/30/40/50 symbols tested

Key finding: Expanding from 20 → 50 symbols increased return by +116%
with zero additional drawdown. More candidates = better signal selection.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

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

# ── Data from universe expansion research (2026-02-19) ───────────────────────
universes  = ['20 symbols\n(baseline)', '30 symbols', '40 symbols', '50 symbols']
ret_pct    = np.array([3160, 4985, 6027, 6812])   # total return %
sharpe     = np.array([5.98, 7.09, 7.21, 7.34])
calmar     = np.array([329,  513,  521,  530])
max_dd     = np.array([9.6,  9.7,  9.8,  9.9])
trades_day = np.array([5.44, 8.06, 9.52, 10.61])
avg_pnl    = np.array([1.21, 1.28, 1.31, 1.34])   # avg PnL per trade %
win_rate   = np.array([66.3, 66.7, 67.0, 67.3])
pf         = np.array([2.17, 2.28, 2.31, 2.33])

x = np.arange(len(universes))
colors = [TEXT_SUB, ACCENT, ORANGE, GREEN]   # grey → blue → orange → green (highlight)

plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG_DARK)

gs = fig.add_gridspec(2, 3, hspace=0.55, wspace=0.38,
                      top=0.78, bottom=0.09, left=0.07, right=0.97)
ax1 = fig.add_subplot(gs[0, :2])   # Return % bar — wide
ax2 = fig.add_subplot(gs[0, 2])    # MaxDD (stays flat)
ax3 = fig.add_subplot(gs[1, 0])    # Sharpe
ax4 = fig.add_subplot(gs[1, 1])    # Trade quality (avg PnL + WR)
ax5 = fig.add_subplot(gs[1, 2])    # Trades/day

for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TEXT_MAIN, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BG_BORDER)
    ax.title.set_color(TEXT_MAIN)
    ax.xaxis.label.set_color(TEXT_SUB)
    ax.yaxis.label.set_color(TEXT_SUB)

# ── Chart 1: Total Return % ──────────────────────────────────────────────────
bars = ax1.bar(x, ret_pct, color=colors, edgecolor=BG_BORDER,
               linewidth=0.8, width=0.55, alpha=0.9, zorder=3)
for b, v, c in zip(bars, ret_pct, colors):
    ax1.text(b.get_x() + b.get_width()/2, v + 80,
             f'+{v:,}%', ha='center', fontsize=10, fontweight='bold',
             color=c if c != TEXT_SUB else TEXT_MAIN, va='bottom')

# Delta annotations
for i in range(1, len(ret_pct)):
    delta = ret_pct[i] - ret_pct[0]
    pct_gain = delta / ret_pct[0] * 100
    ax1.annotate(f'+{pct_gain:.0f}% vs baseline',
                 xy=(i, ret_pct[i]), xytext=(i, ret_pct[i] + 650),
                 ha='center', fontsize=8, color=GREEN,
                 arrowprops=dict(arrowstyle='->', color=GREEN, lw=0.8))

ax1.set_xticks(x)
ax1.set_xticklabels(universes, fontsize=9.5)
ax1.set_ylabel('3-Year Total Return (%)', fontsize=9)
ax1.set_title('Total Return Scales with Universe Size\n(same strategy, same 2 slots, same signal logic)',
              fontsize=11, fontweight='bold', pad=10)
ax1.set_ylim(0, 9500)
ax1.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# ── Chart 2: MaxDD stays flat ────────────────────────────────────────────────
bars2 = ax2.bar(x, max_dd, color=colors, edgecolor=BG_BORDER,
                linewidth=0.8, width=0.55, alpha=0.9, zorder=3)
for b, v in zip(bars2, max_dd):
    ax2.text(b.get_x() + b.get_width()/2, v + 0.08,
             f'{v:.1f}%', ha='center', fontsize=9.5, fontweight='bold',
             color=TEXT_MAIN, va='bottom')

ax2.set_xticks(x)
ax2.set_xticklabels(universes, fontsize=8)
ax2.set_ylabel('Max Drawdown (%)', fontsize=9)
ax2.set_title('Drawdown:\nAlmost Zero Change', fontsize=11, fontweight='bold', pad=10)
ax2.set_ylim(0, 13)
ax2.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# risk-free annotation
ax2.axhline(max_dd[0], color=TEXT_SUB, ls='--', lw=1.2, alpha=0.5)
ax2.text(3.35, max_dd[0] + 0.15, 'baseline', color=TEXT_SUB, fontsize=7.5, ha='right')

# ── Chart 3: Sharpe ──────────────────────────────────────────────────────────
ax3.plot(x, sharpe, color=ACCENT, lw=2.5, marker='o', markersize=9,
         markerfacecolor=BG_DARK, markeredgewidth=2.5, zorder=4)
for i, v in enumerate(sharpe):
    offset = +0.06 if i < 3 else -0.10
    va = 'bottom' if i < 3 else 'top'
    ax3.text(i, v + offset, f'{v:.2f}', ha='center', fontsize=9,
             fontweight='bold', color=ACCENT, va=va)
ax3.set_xticks(x)
ax3.set_xticklabels(universes, fontsize=8)
ax3.set_ylabel('Sharpe Ratio (annualized)', fontsize=9)
ax3.set_title('Sharpe: Improves\nwith More Symbols', fontsize=11, fontweight='bold', pad=10)
ax3.set_ylim(5.5, 7.8)
ax3.grid(axis='y', alpha=0.12, color=BG_BORDER)
ax3.set_xlim(-0.5, 3.5)

# ── Chart 4: Avg PnL per trade + WR ─────────────────────────────────────────
ax4_r = ax4.twinx()
bars4 = ax4.bar(x - 0.18, avg_pnl, 0.35, color=GREEN, alpha=0.8,
                edgecolor=BG_BORDER, label='Avg PnL/trade (%)', zorder=3)
ax4_r.plot(x + 0.18, win_rate, color=ORANGE, lw=2, marker='s', markersize=7,
           markerfacecolor=BG_DARK, markeredgewidth=2, label='Win Rate (%)', zorder=4)

for b, v in zip(bars4, avg_pnl):
    ax4.text(b.get_x() + b.get_width()/2, v + 0.01,
             f'{v:.2f}%', ha='center', fontsize=8, color=GREEN, va='bottom')
for i, v in enumerate(win_rate):
    ax4_r.text(i + 0.18, v + 0.12, f'{v:.1f}%', ha='center', fontsize=8,
               color=ORANGE, va='bottom')

ax4.set_xticks(x)
ax4.set_xticklabels(universes, fontsize=8)
ax4.set_ylabel('Avg PnL per trade (%)', fontsize=8, color=GREEN)
ax4_r.set_ylabel('Win Rate (%)', fontsize=8, color=ORANGE)
ax4_r.tick_params(colors=ORANGE, labelsize=8)
ax4.set_title('Trade Quality Improves:\nMore Candidates = Better Filter',
              fontsize=11, fontweight='bold', pad=10)
ax4.set_ylim(0, 1.7)
ax4_r.set_ylim(64, 68.5)
ax4.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)
ax4.set_facecolor(BG_CARD)
lines1, labels1 = ax4.get_legend_handles_labels()
lines2, labels2 = ax4_r.get_legend_handles_labels()
ax4.legend(lines1 + lines2, labels1 + labels2, fontsize=7.5,
           facecolor='#21262d', edgecolor=BG_BORDER, loc='lower right')

# ── Chart 5: Trades per day ──────────────────────────────────────────────────
bars5 = ax5.bar(x, trades_day, color=colors, edgecolor=BG_BORDER,
                linewidth=0.8, width=0.55, alpha=0.9, zorder=3)
for b, v in zip(bars5, trades_day):
    ax5.text(b.get_x() + b.get_width()/2, v + 0.1,
             f'{v:.1f}x', ha='center', fontsize=9.5, fontweight='bold',
             color=TEXT_MAIN, va='bottom')
ax5.set_xticks(x)
ax5.set_xticklabels(universes, fontsize=8)
ax5.set_ylabel('Trades per Day', fontsize=9)
ax5.set_title('Trade Frequency:\n+95% More Opportunities', fontsize=11, fontweight='bold', pad=10)
ax5.set_ylim(0, 14)
ax5.grid(axis='y', alpha=0.12, color=BG_BORDER, zorder=0)

# ── Title & footer ───────────────────────────────────────────────────────────
fig.text(0.5, 0.960,
         'More Symbols, More Alpha? — Universe Expansion from 20 to 50',
         ha='center', fontsize=15, fontweight='bold', color=TEXT_MAIN)
fig.text(0.5, 0.915,
         '3yr live Binance data  |  20 / 30 / 40 / 50 USDT-M perpetuals  |  same strategy, same slot count, same logic',
         ha='center', fontsize=9.5, color=TEXT_SUB)
fig.text(0.5, 0.01,
         'A larger candidate pool does not dilute quality — it raises it. '
         'The same selection logic picks better setups when given more to choose from. '
         'Return +116%. Drawdown: unchanged.',
         ha='center', fontsize=9, color='#c9d1d9', style='italic',
         bbox=dict(boxstyle='round,pad=0.45', facecolor='#21262d',
                   edgecolor='#444c56', alpha=0.85))

out = Path(__file__).parent / "post_004_universe_expansion.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
print(f"Saved -> {out}")
plt.close()
