# Quant Insight #013 — Kelly Said 154x. We Run 30x. Here's Why.

**Chart:** `post_013_kelly_leverage.png`  
**Research base:** Kelly Criterion re-computation after strategy improvement  
**Data:** 6yr Binance USDT-M · 60 symbols · live WR/RR metrics

---

## Key Finding

When the strategy improved, Kelly recommended 5x more leverage than we currently run. We didn't take it.

| | Original | After Improvement |
|---|---|---|
| Win Rate | 25.9% | 62.9% |
| R:R | 3.75 | 1.16 |
| Full Kelly | 30.7x | **154x** |
| Half Kelly | ~15x | **77x** |
| **Adopted** | **30x** | **30x (unchanged)** |

---

## Why 154x Is Mathematically Correct and Practically Wrong

Kelly computes per-trade, not portfolio-level.

At 30x with a 1% stop-loss:  
- Per-trade risk: 3% of total equity  
- 10 positions open: **30% at risk simultaneously** (before correlation)

At Half-Kelly 154x (77x/position):  
- 10 positions: **770% of equity at risk** — mathematically optimal, practically impossible

The Kelly formula assumes exact stable parameters, no excess slippage, and stationary win rate. None hold perfectly in live markets.

---

## Why WR Improvement Explodes Kelly Nonlinearly

Going from 25.9% to 62.9% WR doesn't double Kelly — it multiplies it ~50x when R:R is held constant.

The WR term sits inside a subtraction in the Kelly formula. Small changes in WR near the breakeven point cause outsized leverage swings.

---

## The Right Response

When parameters improve:  
**❌ Re-lever to the new Kelly**  
**✅ Treat new Kelly as confirmation current budget is conservative → evaluate more position slots, not more leverage per slot**

---

## MA Cluster Note

MA strategy: WR=36.7%, RR=2.21, Kelly=20.1x → adopted 21x (close to Kelly, risk-parity aligned with VR)

---

## LinkedIn Post (copy-paste ready)

See `post_013_kelly_leverage.txt`

---

*60 USDT-M perpetuals · 6yr live Binance data · Kelly computed from live WR/RR metrics*
