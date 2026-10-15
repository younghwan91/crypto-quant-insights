# Crypto Quant Insights 📈

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/younghwan91/crypto-quant-insights?style=social)](https://github.com/younghwan91/crypto-quant-insights)
[![GitHub forks](https://img.shields.io/github/forks/younghwan91/crypto-quant-insights?style=social)](https://github.com/younghwan91/crypto-quant-insights)
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

## ⭐ Star History & Support

[![Star History Chart](https://api.star-history.com/svg?repos=younghwan91/crypto-quant-insights&type=Date)](https://star-history.com/#younghwan91/crypto-quant-insights&Date)

If you find these empirical crypto trading findings and charts useful, please **[⭐ Star this repository](https://github.com/younghwan91/crypto-quant-insights)**!
- 🐛 Discussions & questions → [Issues](https://github.com/younghwan91/crypto-quant-insights/issues)
- 📈 Updates → [Follow @younghwan91](https://github.com/younghwan91)

## Related projects — open-source quant stack

Part of an open-source stack spanning Korean equities, US equities and crypto. Each repository stands on its own.

| Market | Project | What it is |
|---|---|---|
| ₿ Crypto | **[binance-quant-engine](https://github.com/younghwan91/binance-quant-engine)** | Crypto futures backtest & execution engine — zero lookahead, backtest↔live parity |
| 🇰🇷 Korean equities | **[kiwoom-client](https://github.com/younghwan91/kiwoom-client)** | Kiwoom Securities REST API client — full domestic-equity endpoint coverage, real-time WebSocket, sync + async (`pip install kiwoom-client`) |
| 🇰🇷 Korean equities | **[krx-fundamentals-client](https://github.com/younghwan91/krx-fundamentals-client)** | Korean corporate fundamentals Python client library — financial statements, valuation, dividends, screening (DART + KRX + Naver) |
| 🇰🇷 Korean equities | **[krx-news-client](https://github.com/younghwan91/krx-news-client)** | Korean market news & disclosure Python client library (DART + Hankyung + TheBell + Toss) |
| 🇰🇷 Korean equities | **[krx-quant-core](https://github.com/younghwan91/krx-quant-core)** | Shared Python core for Korean-equity quant systems — KRX tick, price-limit and session rules, date-aware transaction-tax cost model, Kiwoom order guards, DART material-disclosure risk classification, fill simulation, Deflated Sharpe and purged CV stats |
| 🇰🇷 Korean equities | **[fin-checkup](https://github.com/younghwan91/fin-checkup)** | Telegram alerts for risk disclosures + a DART/SEC financial health checkup — reports measurements and facts, never a recommendation |
| 🇰🇷 Korean equities | **[quant-airflow](https://github.com/younghwan91/quant-airflow)** | Airflow pipeline collecting Korean market data into TimescaleDB — delisted names included, so downstream backtests aren't survivorship-biased |
| 🇰🇷 Korean equities | **[swing-it](https://github.com/younghwan91/swing-it)** | KOSPI/KOSDAQ alpha validation framework — judged on the per-trade distribution, with random null controls, purged CV and Deflated Sharpe enforced as CI guardrails |
| 🇺🇸 US equities | **[portfolio-research](https://github.com/younghwan91/portfolio-research)** | US equity factor engine — walk-forward gated by Deflated Sharpe and PBO on point-in-time, survivorship-bias-free data (plus tactical ETF allocation: 9 pre-registered, 0 adopted) |
| 🇺🇸 US equities | **[macro-sector-agent](https://github.com/younghwan91/macro-sector-agent)** | Top-down US sector-cycle research — asks which industry has been forgotten, not what to buy; machine excludes, never picks |
| 🇺🇸 US equities | **[automated-stock-trading-systems](https://github.com/younghwan91/automated-stock-trading-systems)** | Backtester for Bensdorp's seven non-correlated trading systems (educational reimplementation) |

## Author

**Younghwan Chae** · [GitHub @younghwan91](https://github.com/younghwan91) · [LinkedIn](https://www.linkedin.com/in/younghwan-chae/)

See the full open-source quant stack on my [profile](https://github.com/younghwan91).
