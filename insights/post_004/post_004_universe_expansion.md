# Quant Insight #004 — More Symbols, More Alpha?

**Chart:** `post_004_universe_expansion.png`
**Research base:** universe expansion sweep · commits `6eb0212` + `dab1f80` · 2026-02-19
**Data:** 3yr Binance USDT-M · 20/30/40/50 symbols · same strategy, 2 slots

---

## Results Table

| Universe | Total Return | Sharpe | Calmar | Max DD | Trades/Day | Avg PnL/trade | WR |
|----------|-------------|--------|--------|--------|------------|---------------|----|
| 20 symbols | +3,160% | 5.98 | 329 | 9.6% | 5.44 | 1.21% | 66.3% |
| 30 symbols | +4,985% | 7.09 | 513 | 9.7% | 8.06 | 1.28% | 66.7% |
| 40 symbols | +6,027% | 7.21 | 521 | 9.8% | 9.52 | 1.31% | 67.0% |
| 50 symbols | +6,812% | 7.34 | 530 | 9.9% | 10.61 | 1.34% | 67.3% |

## Key Insight

More candidates → selection filter picks better setups → quality improves, not degrades.
This is the opposite of the conventional wisdom about "watchlist noise."

## Diminishing Returns Pattern

| Step | Return Delta | DD Delta | Sharpe Delta |
|------|-------------|----------|-------------|
| 20 → 30 | +58% | +0.1pp | +19% |
| 30 → 40 | +21% | +0.1pp | +2% |
| 40 → 50 | +13% | +0.1pp | +2% |

First expansion (20→30) gives the biggest jump. Beyond 50, gains are likely marginal.
