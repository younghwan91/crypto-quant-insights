# Quant Insight #011 — Your IS PF Was 2.16. Your OOS PF Was 1.38.

**Chart:** `post_011_is_oos_divergence.png`  
**Research base:** IS/OOS validation · 7 parameter variants · 60 USDT-M perpetuals  
**Data:** 6yr Binance USDT-M · IS: 2020-2022 (2.9yr) / OOS: 2023-2025 (3.1yr) · strict temporal split

---

## Key Finding

7 parameter variants were optimized on IS data only, then evaluated on OOS without modification.

| Metric | Range |
|--------|-------|
| IS Profit Factors | 2.16 – 3.51 |
| OOS Profit Factors | 1.38 – 1.58 |
| OOS/IS Ratio | 0.45 – 0.64 |
| Passed OOS/IS ≥ 0.85 | **0 of 7** |

Every single variant dropped 36–55% from IS to OOS PF. None passed the standard 0.85 OOS/IS threshold.

---

## Why the Gap Exists

The 2020–2022 IS window included COVID recovery, a sustained bull market, the China mining ban, Luna, and FTX — a full boom-and-bust cycle generating exceptional directional edge for momentum signals.

The 2023–2025 OOS window is market normalization: shorter trends, momentum competing with mean-reversion, no structural bull market tailwind.

A model calibrated on 2020–2022 is partially calibrated on extraordinary conditions. Its IS PF contains that windfall. The OOS PF doesn't.

---

## Practical Implication

OOS PF of 1.38 over 3.1 years of real data (2023–2025) is a meaningful result. The implication is not that the strategy failed — it's that presenting the IS number as the expected live number requires a disclosure: **it spans the most favorable directional period in crypto history.**

**Structural check:** If your IS period includes 2021, decompose how much of your total IS return came from that single year. If it exceeds 40%, your IS number is partially a 2021 proxy.

---

## LinkedIn Post (copy-paste ready)

See `post_011_is_oos_divergence.txt`

---

*60 USDT-M perpetuals · 6yr live Binance data · 7 variants · IS: 2020-2022 / OOS: 2023-2025 · strict temporal split*
