# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 56
- ETFs with sufficient data: 47
- Candidate universe after filtering: 39
- Selected ETFs (max_sharpe): 14
- Excluded 9 ETF(s) with volatility > 25.0%
- Portfolio annual return: 23.29%
- Portfolio annual volatility: 11.51%
- Portfolio Sharpe ratio: 2.024
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 23.29% | 11.51% | 2.024 | 0.27% | Yes |
| low_volatility | 22.03% | 11.02% | 2.000 | 0.28% |  |
| cost_focus | 23.84% | 11.86% | 2.010 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16594970
- Current loan ratio: 0.603
- Buffer to 70%: 13.92% drop
- Buffer to 85%: 29.11% drop
- Max drawdown (history): -15.31%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,935,473 | 0.669 | No | No |
| -20% | ¥13,275,976 | 0.753 | Yes | No |
| -30% | ¥11,616,479 | 0.861 | Yes | Yes |
| -40% | ¥9,956,982 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 603
- Forced liquidation events: 353

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
