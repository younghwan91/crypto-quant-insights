# Post 005 — The Slot Count Sweet Spot

**Source:** r39 · commit `d70cd2f` · 2026-03-02  
**Script:** `research/active/r31_r40/r39_scaling_yearly.py`

## Key Data

| Slots | Calmar | AnnRet% | DD% | Aggression |
|------:|-------:|--------:|----:|----------:|
| 1     | 2.2    | 70.6    | 32.1 | 155 |
| 2     | 3.2    | 99.9    | 30.8 | 320 |
| 5     | 5.1    | 160.8   | 31.7 | 820 |
| 8     | 5.5    | 174.1   | 31.7 | 958 |
| **10** | **5.8** | **187.2** | **32.4** | **1,086 ★** |
| 12    | 5.4    | 189.7   | 35.3 | 1,024 |
| 15    | 5.5    | 195.4   | 35.3 | 1,075 |

## Key Findings
- Calmar peaks at 10 slots; 12+ causes DD increase without proportional Calmar gain
- TPD saturates: 0.45 (1 slot) → 1.03 (10 slots) → 1.04 (15 slots)
- Aggression score (AnnRet × Calmar) peaks at 10 slots (1,086)

## Chart
3 panels: Calmar line · Return vs DD grouped bars · Aggression score bars
