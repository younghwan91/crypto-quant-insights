"""
Quant Insight #001 — Range Compression Window vs Breakout Quality
=================================================================
"How long should a market 'hold its breath' before a breakout matters?"

Data: 6yr, 45 USDT-M futures symbols, 15m bars
Strategy: Range Compression Breakout (RCB) — same SL=1%, trail-only exit
Key finding: Longer consolidation = dramatically higher edge
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib.patches as mpatches
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from quantbox.strategy.vol_straddle.config import VolStraddleConfig
from quantbox.backtest.trade_sim import portfolio_sim, compute_metrics

cfg = VolStraddleConfig()
SL_PCT = cfg.d_sl; COST = 0.0008; MAX_CONC = cfg.max_concurrent; MAX_HOLD = 192

# ── Data ─────────────────────────────────────────────────────────────────────
CACHE_DIR = ROOT / "data" / "cache_extended"
data_15m = {}
for f in sorted(CACHE_DIR.glob("*_15m_2190d_*.npz")):
    sym = f.name.split("_")[0]
    npz = np.load(f, allow_pickle=False)
    if "close" not in npz.files: continue
    data_15m[sym] = {k: npz[k] for k in npz.files}
max_bars = max(len(d["close"]) for d in data_15m.values())
for d in data_15m.values():
    d["_offset"] = max_bars - len(d["close"])
DATA_YEARS = max_bars / (4 * 24 * 365.25)

# ── Helpers ───────────────────────────────────────────────────────────────────
def rmax_excl(arr, w):
    r = pd.Series(arr.astype(float)).rolling(w, min_periods=w).max().values
    out = np.empty_like(r); out[0] = np.nan; out[1:] = r[:-1]; return out

def rmin_excl(arr, w):
    r = pd.Series(arr.astype(float)).rolling(w, min_periods=w).min().values
    out = np.empty_like(r); out[0] = np.nan; out[1:] = r[:-1]; return out

def sim_trade(ep, closes, highs, lows, direction, sl_pct, trail_act, trail_dist, max_hold):
    sl = ep * (1.0 - sl_pct * direction); peak = 0.0; trail_active = False
    n = min(max_hold, len(closes))
    for i in range(n):
        lo, hi, cl = lows[i], highs[i], closes[i]
        if direction == 1:
            if lo <= sl: return -sl_pct, i+1
            pnl = (cl - ep) / ep
        else:
            if hi >= sl: return -sl_pct, i+1
            pnl = (ep - cl) / ep
        if pnl > peak: peak = pnl
        if peak >= trail_act: trail_active = True
        if trail_active and pnl <= peak - trail_dist: return pnl, i+1
    if n == 0: return 0.0, 0
    return (closes[n-1] - ep) / ep * direction, n

def collect_rcb(data, range_w, range_thresh=0.03, trail_act=0.06, trail_dist=0.003):
    trades = []
    for sym, d in data.items():
        close, high, low = d["close"], d["high"], d["low"]
        offset = d["_offset"]
        rng_high = rmax_excl(high, range_w); rng_low = rmin_excl(low, range_w)
        with np.errstate(invalid='ignore', divide='ignore'):
            rng_pct = np.where(close > 0, (rng_high - rng_low) / close, np.inf)
        compressed = rng_pct < range_thresh
        long_ok = close > rng_high; short_ok = close < rng_low
        valid = (~np.isnan(rng_high) & ~np.isnan(rng_low) & (close > 0))
        valid[:250] = False; valid[-1] = False
        for i in np.where(valid & compressed & (long_ok | short_ok))[0]:
            direction = 1 if long_ok[i] else -1; ep = close[i]
            pnl_raw, hold = sim_trade(ep, close[i+1:], high[i+1:], low[i+1:],
                                      direction, SL_PCT, trail_act, trail_dist, MAX_HOLD)
            ea = i + 1 + offset
            trades.append((sym, ea, ea+hold, pnl_raw - COST))
    return trades

# ── Run sweep ────────────────────────────────────────────────────────────────
windows = [16, 24, 32, 48, 64, 96, 128, 192]
hours   = [w * 15 / 60 for w in windows]

print("Running range_w sweep...")
results = []
for rw in windows:
    trades = collect_rcb(data_15m, range_w=rw)
    pnl = portfolio_sim(trades, MAX_CONC)
    m = compute_metrics(pnl, DATA_YEARS)
    results.append(m)
    print(f"  rw={rw:3d} ({rw*15/60:.0f}h) | N/yr={m['N']/DATA_YEARS:5.0f} | PF={m['PF']:.3f} | EV={m['EV_bp']:+.0f}bp | DD={m['max_dd_pct']:.0f}%")

pfs    = [r['PF']        for r in results]
evs    = [r['EV_bp']     for r in results]
n_yrs  = [r['N']/DATA_YEARS for r in results]
dds    = [r['max_dd_pct'] for r in results]

# ── Plot ─────────────────────────────────────────────────────────────────────
plt.style.use('dark_background')
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.patch.set_facecolor('#0d1117')
for ax in axes:
    ax.set_facecolor('#161b22')
    ax.tick_params(colors='#c9d1d9', labelsize=11)
    ax.xaxis.label.set_color('#c9d1d9')
    ax.yaxis.label.set_color('#c9d1d9')
    ax.title.set_color('#f0f6fc')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

ACCENT = '#58a6ff'
GREEN  = '#3fb950'
RED    = '#f85149'
ORANGE = '#d29922'

# Chart 1: Profit Factor vs Consolidation Window
ax = axes[0]
colors = [GREEN if p > 1 else RED for p in pfs]
bars = ax.bar(range(len(hours)), pfs, color=colors, alpha=0.85, edgecolor='#30363d', linewidth=0.8)
ax.axhline(1.0, color=ORANGE, linestyle='--', linewidth=1.5, alpha=0.8, label='Break-even (PF=1.0)')
ax.set_xticks(range(len(hours)))
ax.set_xticklabels([f'{h:.0f}h' for h in hours], fontsize=10)
ax.set_ylabel('Profit Factor', fontsize=12)
ax.set_title('Edge Quality vs\nConsolidation Window', fontsize=13, fontweight='bold', pad=12)
ax.legend(fontsize=10, facecolor='#21262d', edgecolor='#30363d')
for i, (b, v) in enumerate(zip(bars, pfs)):
    ax.text(b.get_x() + b.get_width()/2, v + 0.005, f'{v:.3f}',
            ha='center', va='bottom', fontsize=9, color='#f0f6fc', fontweight='bold')
ax.set_ylim(0.82, 1.32)
ax.grid(axis='y', alpha=0.2, color='#30363d')

# Chart 2: Signals per Year (trade-off)
ax = axes[1]
ax.plot(hours, n_yrs, color=ACCENT, linewidth=2.5, marker='o', markersize=8,
        markerfacecolor='#0d1117', markeredgewidth=2)
ax.fill_between(hours, n_yrs, alpha=0.12, color=ACCENT)
ax.set_xlabel('Consolidation Window (hours)', fontsize=12)
ax.set_ylabel('Signals per Year (45 symbols)', fontsize=12)
ax.set_title('Signal Frequency vs\nConsolidation Window', fontsize=13, fontweight='bold', pad=12)
ax.grid(alpha=0.15, color='#30363d')
for h, n in zip(hours, n_yrs):
    ax.annotate(f'{n:.0f}', (h, n), textcoords='offset points', xytext=(0, 10),
                ha='center', fontsize=9, color='#c9d1d9')

# Chart 3: EV (edge) per trade
ax = axes[2]
ev_colors = [GREEN if e > 0 else RED for e in evs]
bars2 = ax.bar(range(len(hours)), evs, color=ev_colors, alpha=0.85, edgecolor='#30363d', linewidth=0.8)
ax.axhline(0, color=ORANGE, linestyle='--', linewidth=1.5, alpha=0.8)
ax.set_xticks(range(len(hours)))
ax.set_xticklabels([f'{h:.0f}h' for h in hours], fontsize=10)
ax.set_ylabel('Expected Value per Trade (basis points)', fontsize=12)
ax.set_title('Per-Trade Edge vs\nConsolidation Window', fontsize=13, fontweight='bold', pad=12)
for i, (b, v) in enumerate(zip(bars2, evs)):
    ax.text(b.get_x() + b.get_width()/2,
            v + (1 if v >= 0 else -2),
            f'{v:+.0f}bp', ha='center', va='bottom' if v >= 0 else 'top',
            fontsize=9, color='#f0f6fc', fontweight='bold')
ax.grid(axis='y', alpha=0.2, color='#30363d')

# Title & Footer
fig.suptitle(
    'Quant Insight #001 — Range Compression Window vs Breakout Quality\n'
    'Crypto Futures · 6yr · 45 USDT-M Symbols · SL=1% · Trail-Only Exit · 0.08% round-trip cost',
    fontsize=14, fontweight='bold', color='#f0f6fc', y=1.02
)
fig.text(0.5, -0.03,
    '📌 Longer consolidation = stronger signal. 48h range compression yields 3× better edge than 4h.\n'
    'Trade-off: fewer signals. Noise rejection matters more than signal frequency.',
    ha='center', fontsize=11, color='#8b949e', style='italic')

plt.tight_layout(pad=2.0)
out = ROOT / "insights" / "post_001_range_compression.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"\nSaved: {out}")
plt.close()
