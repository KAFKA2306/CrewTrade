# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 52
- ETFs with sufficient data: 52
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 37.03%
- Portfolio annual volatility: 13.67%
- Portfolio Sharpe ratio: 2.710
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 37.03% | 13.67% | 2.710 | 0.30% | Yes |
| low_volatility | 35.87% | 13.12% | 2.733 | 0.31% |  |
| cost_focus | 38.31% | 13.95% | 2.746 | 0.29% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16581723
- Current loan ratio: 0.603
- Buffer to 70%: 13.85% drop
- Buffer to 85%: 29.05% drop
- Max drawdown (history): -16.41%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,923,551 | 0.670 | No | No |
| -20% | ¥13,265,378 | 0.754 | Yes | No |
| -30% | ¥11,607,206 | 0.862 | Yes | Yes |
| -40% | ¥9,949,034 | 1.005 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 674
- Forced liquidation events: 590

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
