# Post 007 — I Tried Dynamic Parameters. Static Won.

**Source:** r42 · commit `03b2b6b` · 2026-03-03  
**Script:** `research/active/r41_r50/r42_regime_adaptive_vr.py`  
**Verdict:** ❌ MARGINAL — not implemented

## Key Data

| Metric | Static | Adaptive | Δ |
|--------|-------:|---------:|--:|
| N (trades) | 2,265 | 1,628 | −637 |
| PF | 1.280 | 1.311 | +0.031 |
| EV (bp) | 32.1 | 35.7 | +3.6 |
| Ann. Return % | 187.2 | 134.0 | −53pp |
| Max DD % | 32.4 | 42.6 | +10.2pp |
| Calmar | 5.8 | 3.1 | −2.7 |

## Year-by-Year EV Delta (Adaptive − Static)
2020: +12.0 | 2021: −3.9 | 2022: −6.2 | 2023: +5.7 | 2024: +18.1 | 2025: +10.0 | 2026: −24.5

## Why Static Won
- VR signal itself already regime-filters (fewer setups fire in low-vol naturally)
- Trade count −28% → compounding advantage lost
- Complexity: 3 regimes × 6 params = 18 variables
- Regime thresholds are themselves a free parameter (overfitting risk)

## Chart
3 panels: EV by year grouped bars · Metrics comparison horizontal bars · Complexity vs Calmar scatter
