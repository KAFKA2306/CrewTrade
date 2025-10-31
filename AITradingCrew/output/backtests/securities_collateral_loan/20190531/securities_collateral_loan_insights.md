# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 81
- ETFs with sufficient data: 67
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 4 ETF(s) with volatility > 25.0%
- Excluded 7 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 5.02%
- Portfolio annual volatility: 6.76%
- Portfolio Sharpe ratio: 0.742
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.02% | 6.76% | 0.742 | 0.18% | Yes |
| low_volatility | 3.49% | 4.86% | 0.718 | 0.18% |  |
| cost_focus | 7.11% | 7.93% | 0.897 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18300467
- Current loan ratio: 0.546
- Buffer to 70%: 21.94% drop
- Buffer to 85%: 35.71% drop
- Max drawdown (history): -6.39%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,470,420 | 0.607 | No | No |
| -20% | ¥14,640,374 | 0.683 | No | No |
| -30% | ¥12,810,327 | 0.781 | Yes | No |
| -40% | ¥10,980,280 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
