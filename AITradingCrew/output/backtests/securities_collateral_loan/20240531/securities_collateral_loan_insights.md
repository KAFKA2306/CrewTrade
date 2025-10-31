# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 156
- ETFs with sufficient data: 122
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 7
- Excluded 6 ETF(s) with volatility > 25.0%
- Portfolio annual return: 20.20%
- Portfolio annual volatility: 8.60%
- Portfolio Sharpe ratio: 2.350
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 20.20% | 8.60% | 2.350 | 0.17% | Yes |
| low_volatility | 20.46% | 8.73% | 2.344 | 0.19% |  |
| cost_focus | 18.41% | 8.44% | 2.182 | 0.14% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18291148
- Current loan ratio: 0.547
- Buffer to 70%: 21.90% drop
- Buffer to 85%: 35.68% drop
- Max drawdown (history): -5.97%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,462,033 | 0.608 | No | No |
| -20% | ¥14,632,918 | 0.683 | No | No |
| -30% | ¥12,803,804 | 0.781 | Yes | No |
| -40% | ¥10,974,689 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 478
- Forced liquidation events: 294

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
