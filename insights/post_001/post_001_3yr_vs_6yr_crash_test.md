# Quant Insight #001 — Why Your 3-Year Crypto Backtest is Lying to You

**Chart:** `post_001_3yr_vs_6yr_crash_test.png`  
**Research base:** r5 crash-era validation · commit `0690b0f` · 2026-02-20  
**Data:** 6yr Binance USDT-M perpetuals · 50 symbols · 15m bars  
**Crashes covered:** COVID (Mar '20) · China Ban (May '21) · Luna (May '22) · FTX (Nov '22)

---

## Key Finding

19 strategy variants were backtested on **3 years**, then re-tested on **6 years** including all major crash regimes.

| Variant | 3yr MaxDD | 6yr MaxDD | Change | Verdict |
|---|---|---|---|---|
| Trailing 2× (3yr winner) | **6.7%** | 13.2% | +6.5pp | ❌ Fragile |
| Wide Equity | 7.0% | 11.9% | +4.9pp | ❌ Fragile |
| Baseline (prod at the time) | 9.4% | **25.3%** | +15.9pp | ❌❌ Catastrophic |
| **2-Slot (6yr survivor)** | 7.6% | **8.2%** | **+0.6pp** | ✅ Crash-stable |
| Conf≥4 | 9.0% | 10.0% | +1.0pp | ✅ Stable |

PF degradation was universal — all 19 variants dropped from ~2.0–2.3 (3yr) to ~1.26–1.35 (6yr). That's **expected**. The question is not "did it degrade?" but "which degraded least?"

---

## Why the 3yr Winner Failed

The trailing 2× variant looked perfect on 2023–2025 data (mostly trending bull).  
During crash regimes, trailing runners **hold positions longer** through violent reversals — amplifying drawdown exactly when you can least afford it.

## Why the 2-Slot Config Survived

With only 2 simultaneous positions, during crash days when 50 coins dump in lockstep, maximum correlated exposure is capped. More slots = more correlated losses on crash days.

---

## LinkedIn Post (copy-paste ready)

---

Most crypto backtests never see a real crash.

I validated 19 strategy variants across 6 years of live Binance data — COVID, China ban, Luna, FTX all included.

The 3-year winner: 6.7% max drawdown. Clean equity curve. Deploy-ready by every metric.

Add the crash years. That same variant hit 13.2% drawdown. Nearly doubled.

The config that held? Not the most optimized. Not the highest R:R. Just a simple concurrency cap — 2 simultaneous positions instead of 4. MaxDD grew +0.6pp across all four crashes while others blew past 13–25%.

**Optimization finds what works in the data you gave it. Stress testing finds what breaks when the data gets real.**

If your backtest window doesn't include at least one major crash regime, you're not validating a strategy — you're validating a bull market assumption.

→ Test through crashes. Not around them.

---
*50 USDT-M perpetuals · 6yr live data · 19 variants · COVID / Luna / FTX included*

#AlgoTrading #QuantFinance #CryptoTrading #Backtesting #RiskManagement

---
