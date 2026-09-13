# Quant Insight #014 — Backtest Said +$125. Live Delivered -$33. Same Signal, Same Bar.

**Chart:** `post_014_mfe_exit_gap.png`  
**Research base:** Trail exit execution gap analysis · 10,791 directional trades  
**Data:** 6yr Binance USDT-M · 60 symbols · intrabar vs bar-close execution model

---

## Key Finding

A trailing profit protection threshold was breached intrabar at +4.37%. The live system closed at bar close: -1.1%.

| | Backtest | Live | Gap |
|---|---|---|---|
| Price at exit | +4.17% (trail trigger) | -1.1% (bar close) | 5.27pp |
| P&L per slot (30x) | **+$125** | **-$33** | **$158** |

---

## The Mechanism

Both systems detected the **same threshold breach**. The difference:

- **Backtest**: assumes exit at the trailing stop trigger price (intrabar)
- **Live**: checks trailing stop at bar close, places market order at next price
- **In a spike-and-reverse bar**: bar close is far below the intrabar peak

This is not slippage. It's a **modeling assumption** — correct for backtest's purpose, incorrect as a live trading prediction.

---

## Measured Across 6 Years

| Metric | Value |
|--------|-------|
| Total directional trades | 10,791 |
| Trades hitting trail threshold | ~14.7% |
| Average backtest-to-live gap | **31bp per trade** |
| Top 5% spike-and-reverse bars | Avg gap **4.1%** price (~$123/slot) |

**Portfolio-level effect:**

| Model | PF (trail-exit trades only) |
|---|---|
| Intrabar execution (backtest) | 1.99 |
| Bar-close execution (live reality) | **1.41** |

29% reduction, concentrated in 14.7% of positions. Positions hitting fixed stops or time limits: **unaffected**.

---

## What This Means

The gap is predictable and quantifiable. The correct response:

1. Label backtest PF with execution model: "intrabar" or "bar-close"
2. Use bar-close model for live trading predictions
3. Consider server-side ratchet orders to narrow the gap

---

## LinkedIn Post (copy-paste ready)

See `post_014_mfe_exit_gap.txt`

---

*60 USDT-M perpetuals · 6yr live Binance data · 10,791 directional trades · trail exit analysis*
