# Post 010 — The Exit You Never Optimize

## Research Source
`docs/backtest_results/202602/20260220_bdd85f0_alpha_search_r7_exit_grid_sweep.md`

## Key Data

### Cells achieving R:R ≥ 1.0 (out of 25 TP×SL combos each)
| Exit Mode | Cells (R:R ≥ 1.0) | Note |
|-----------|-------------------|------|
| Standard (fixed TP/SL) | 10/25 | most cells have R:R < 1.0 |
| Trail only             | 14/25 | improvement |
| Partial + Trail        | 25/25 | all cells pass |
| Partial + BE + Trail   | 25/25 | all cells pass |

### PF Stability
- PF range across all 101 variants: 1.23–1.35
- Standard deviation of PF: ~0.03 (remarkably stable)
- Conclusion: the edge is structural, not a function of TP/SL tuning

### Best per exit mode (representative)
| Mode | R:R | WR |
|------|-----|-----|
| Standard best      | 0.56 | 70.2% |
| Trail best         | 0.75 | 63.7% |
| Partial+Trail best | 1.16 | 67.6% |
| PT+BE+Trail best   | 1.22 | 66.7% |

## Core Insight
Switching exit mode (not TP/SL values) turns a "10 out of 25 cells working" setup into "25 out of 25 cells working." The PF barely moves — but the R:R profile changes dramatically.

## Strategy Exposure Check
- No signal logic, no parameter values for TP/SL
- Framed as: structural exit design observation
- "partial trail" is a general exit concept, not proprietary
