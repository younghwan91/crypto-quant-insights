# Crypto Quant Insights 📈

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-younghwan--chae-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/younghwan-chae/)

Short, chart-backed research notes from validating a live Binance USDT-M futures system — what held up out-of-sample, what looked good and quietly wasn't, and why. Each post is self-contained: the finding, the chart, and the script that generated it.

The strategy itself (signal generation, live parameters, P&L) stays private — see [binance-quant-engine](https://github.com/younghwan91/binance-quant-engine) for the public infra these findings were measured on. What's here is the *methodology and validation results*, not the alpha.

## Posts

| # | Title |
|---|---|
| 001 | [Why Your 3-Year Crypto Backtest is Lying to You](insights/post_001/post_001_3yr_vs_6yr_crash_test.md) |
| 002 | [Win Rate 70% vs R:R 2:1 — Which Actually Survives?](insights/post_002/post_002_wr_vs_rr.md) |
| 003 | [The Long Bias That Stopped Working](insights/post_003/post_003_long_short_reversal.md) |
| 004 | [More Symbols, More Alpha?](insights/post_004/post_004_universe_expansion.md) |
| 005 | [The Slot Count Sweet Spot](insights/post_005/post_005_slot_count_sweet_spot.md) |
| 006 | [Your Trailing Stop Is Probably Already Good Enough](insights/post_006/post_006_trailing_stop_already_good.md) |
| 007 | [I Tried Dynamic Parameters. Static Won.](insights/post_007/post_007_dynamic_params_failed.md) |
| 008 | [More Leverage or More Positions?](insights/post_008/post_008_leverage_vs_slots.md) |
| 009 | [Monte Carlo Humility](insights/post_009/post_009_monte_carlo_humility.md) |
| 010 | [The Exit You Never Optimize](insights/post_010/post_010_exit_mode_beats_tpsl.md) |
| 011 | [Your IS PF Was 2.16. Your OOS PF Was 1.38.](insights/post_011/post_011_is_oos_divergence.md) |
| 012 | [132 Configs Tested. Only 1 Was Profitable Every Single Year.](insights/post_012/post_012_yearly_consistency.md) |
| 013 | [Kelly Said 154x. We Run 30x. Here's Why.](insights/post_013/post_013_kelly_leverage.md) |
| 014 | [Backtest Said +$125. Live Delivered -$33. Same Signal, Same Bar.](insights/post_014/post_014_mfe_exit_gap.md) |

Each folder also has a `.py` script that regenerates its chart from the numbers in the write-up, and a `.txt` with the raw output those numbers came from.

## License

MIT — reuse the charts/scripts, just don't claim the strategy P&L as your own backtest.

---

**Younghwan Chae** · [GitHub @younghwan91](https://github.com/younghwan91) · [LinkedIn](https://www.linkedin.com/in/younghwan-chae/)
