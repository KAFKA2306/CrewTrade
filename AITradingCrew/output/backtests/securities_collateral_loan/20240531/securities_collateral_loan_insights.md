# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 187
- ETFs with sufficient data: 157
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 28.48%
- Portfolio annual volatility: 13.92%
- Portfolio Sharpe ratio: 2.046
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 28.48% | 13.92% | 2.046 | 0.27% | Yes |
| low_volatility | 30.26% | 13.96% | 2.168 | 0.33% |  |
| cost_focus | 29.09% | 13.77% | 2.113 | 0.29% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16509514
- Current loan ratio: 0.606
- Buffer to 70%: 13.47% drop
- Buffer to 85%: 28.74% drop
- Max drawdown (history): -8.29%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,858,562 | 0.673 | No | No |
| -20% | ¥13,207,611 | 0.757 | Yes | No |
| -30% | ¥11,556,659 | 0.865 | Yes | Yes |
| -40% | ¥9,905,708 | 1.010 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 661
- Forced liquidation events: 498

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
