# Quant Insight #002 — Win Rate 70% vs R:R 2:1 — Which Actually Survives?

**Chart:** `post_002_wr_vs_rr.png`
**Research base:** r8 stress test · commit `3f63b4c` · 2026-02-20
**Data:** 6yr Binance USDT-M perpetuals · 50 symbols · 15m bars

---

## Key Finding

5 exit configurations stress-tested across 3 market regimes (Bull/Chop/Bear).

| Config | R:R | Actual WR | Breakeven WR | Safety Margin |
|--------|-----|-----------|--------------|---------------|
| Prod Baseline (High WR) | 0.60 | 68.5% | 62.5% | **6pp** ❌ |
| Config A (Balanced) | 1.16 | 67.6% | 46.3% | 21pp ✅ |
| Config B (Balanced+) | 1.22 | 66.7% | 45.0% | 22pp ✅ |
| Config C (Wide Stop) | 1.34 | 64.5% | 42.7% | 22pp ✅ |
| Config D (High R:R) | 1.66 | 56.8% | 37.6% | 19pp ✅ |

Breakeven WR = 1 / (1 + R:R)

## Regime PF Stability

| Config | Bull PF | Chop PF | Bear PF | Max Drop |
|--------|---------|---------|---------|----------|
| Prod Baseline | 1.38 | 1.32 | 1.27 | 0.11 |
| Config A | 1.39 | 1.30 | 1.28 | 0.11 |
| Config B | 1.40 | 1.32 | 1.25 | 0.15 |
| Config C | 1.41 | 1.28 | 1.28 | 0.13 |
| Config D | 1.31 | 1.27 | 1.25 | 0.06 |

## Core Lesson

Win rate is volatile metric — it changes with market regime.
R:R ratio is structural — determined by your exit logic, not market conditions.

Safety margin = actual WR − breakeven WR → this is the real edge buffer.
