# Post 009 — Monte Carlo Humility

## Research Source
`docs/backtest_results/202603/20260307_3a2d26b_r46_monte_carlo.md`

## Key Data

### Balance Percentiles (1-year horizon, 10,000 paths)
| Percentile | Final Balance | Return |
|-----------|--------------|--------|
| P1  | $2,184   | +9%       |
| P10 | $20,280  | +914%     |
| P25 | $83,181  | +4,059%   |
| P50 | $390,471 | +19,424%  |
| P75 | $1.83M   | +91,342%  |
| P90 | $7.15M   | +357,450% |

### Drawdown Percentiles (same paths)
| Percentile | Max DD |
|-----------|--------|
| P5  | 56.9% |
| P25 | 66.3% |
| P50 | 73.6% |
| P75 | 81.2% |
| P95 | 90.9% |

### Summary Stats
- P(profit after 1yr) = 99.1%
- P(ruin < 50% of capital) = 21.1%
- Mean = $4.65M (dominated by right tail outliers)
- Median = $390K

## Core Insight
"Profitable" and "risky" are both true simultaneously. The same 10,000 paths that show 99.1% profit probability also show 73.6% median drawdown. The mean ($4.65M) vs median ($390K) gap reveals extreme right-tail skew.

## Strategy Exposure Check
- No signal logic, no parameter names
- Framed as: compound return math + behavioral finance observation
- No leverage numbers cited explicitly
