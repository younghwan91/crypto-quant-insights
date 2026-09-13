# Post 006 — Your Trailing Stop Is Probably Already Good Enough

**Source:** r12 · commit `0b7936d` · 2026-02-21  
**Script:** `scripts/alpha_search_r12.py`

## Key Data

| Variant | Description | Calmar | vs Baseline |
|---------|-------------|-------:|------------|
| B-T07 ★ | Tighter trail ATR×0.7 | 1022 | +1.8% |
| A-Base | Baseline | 1004 | — |
| E-SU30/F-SU50/G | Step-up variants | 1004 | 0% |
| S-MH4/T-MH5 | Max hold extended | 1004 | 0% |
| D-T20 | Very loose ATR×2.0 | 893 | −11% |

## Trade Composition
- Pre-TP1 exits: 70.6% (losses determined here)
- TP1 partial: 14.7%
- Runners (post-TP1): 14.7% — WR 99.9%, avg 6.9 bars

## Why Zero-Effect Variants Failed
- Step-up: runners exit in 6.9 bars, never reach 2× trigger
- Max hold: 0 time exits — already exiting naturally
- VWMA floor: always below existing ATR trail

## Practical Winner
B-T07 (tighter): 4.6 bars avg → +190 trades → +1.6% return via slot turnover

## Chart
Horizontal bar (24 variants sorted) · Donut chart (trade composition + runner WR)
