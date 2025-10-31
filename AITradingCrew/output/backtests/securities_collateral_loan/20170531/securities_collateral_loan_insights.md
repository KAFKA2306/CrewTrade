# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 74
- ETFs with sufficient data: 74
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 10.36%
- Portfolio annual volatility: 17.96%
- Portfolio Sharpe ratio: 0.577
- Weighted expense ratio: 0.45%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.36% | 17.96% | 0.577 | 0.45% | Yes |
| low_volatility | 12.71% | 19.12% | 0.665 | 0.49% |  |
| cost_focus | 11.27% | 17.72% | 0.636 | 0.49% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16579945
- Current loan ratio: 0.603
- Buffer to 70%: 13.84% drop
- Buffer to 85%: 29.04% drop
- Max drawdown (history): -22.48%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,921,950 | 0.670 | No | No |
| -20% | ¥13,263,956 | 0.754 | Yes | No |
| -30% | ¥11,605,962 | 0.862 | Yes | Yes |
| -40% | ¥9,947,967 | 1.005 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 478
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
