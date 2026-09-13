# Post 008 — More Leverage or More Positions?

## Research Source
`docs/backtest_results/202603/20260302_9d01aa4_scaling_r38.md` (Part 5: leverage vs slot diversification)

## Key Data

| Config | Ann.Ret | Max DD | Calmar |
|--------|---------|--------|--------|
| 1slot × 1x  | +60.9%  | 66.5%  | 0.9 |
| 3slot × 1x  | +134.7% | 74.8%  | 1.8 |
| 5slot × 1x  | +143.1% | 72.9%  | 2.0 ← best Calmar |
| 1slot × 3x  | +170.1% | 97.2%  | 1.8 |
| 1slot × 5x  | +168.8% | 99.8%  | 1.7 |

Cross-trade PnL correlation ρ = 0.051 → near-zero, which is why diversification works.

## Core Insight
5slot×1x and 1slot×5x both deliver ~140-170% annual return. But 5slot achieves this with 72.9% DD vs 99.8% for 1slot×5x. Diversification dominates concentrated leverage.

## Strategy Exposure Check
- No signal logic mentioned
- No parameter names
- Only market structure observation: diversification vs leverage tradeoff
