# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 108
- ETFs with sufficient data: 17
- Candidate universe after filtering: 17
- Selected ETFs (max_sharpe): 14
- Excluded 28 ETF(s) with volatility > 25.0%
- Excluded 56 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 3.93%
- Portfolio annual volatility: 9.36%
- Portfolio Sharpe ratio: 0.419
- Weighted expense ratio: 0.22%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 3.93% | 9.36% | 0.419 | 0.22% | Yes |
| low_volatility | 6.13% | 6.73% | 0.911 | 0.17% |  |
| cost_focus | 4.45% | 7.19% | 0.619 | 0.20% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16600597
- Current loan ratio: 0.602
- Buffer to 70%: 13.94% drop
- Buffer to 85%: 29.13% drop
- Max drawdown (history): -46.30%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,940,537 | 0.669 | No | No |
| -20% | ¥13,280,477 | 0.753 | Yes | No |
| -30% | ¥11,620,418 | 0.861 | Yes | Yes |
| -40% | ¥9,960,358 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 216
- Forced liquidation events: 131

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
