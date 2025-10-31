# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 219
- ETFs with sufficient data: 177
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 20.82%
- Portfolio annual volatility: 17.43%
- Portfolio Sharpe ratio: 1.195
- Weighted expense ratio: 0.44%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 20.82% | 17.43% | 1.195 | 0.44% | Yes |
| low_volatility | 21.63% | 16.12% | 1.342 | 0.47% |  |
| cost_focus | 21.08% | 16.51% | 1.277 | 0.47% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16602174
- Current loan ratio: 0.602
- Buffer to 70%: 13.95% drop
- Buffer to 85%: 29.14% drop
- Max drawdown (history): -16.64%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,941,956 | 0.669 | No | No |
| -20% | ¥13,281,739 | 0.753 | Yes | No |
| -30% | ¥11,621,522 | 0.861 | Yes | Yes |
| -40% | ¥9,961,304 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 192
- Forced liquidation events: 4

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
