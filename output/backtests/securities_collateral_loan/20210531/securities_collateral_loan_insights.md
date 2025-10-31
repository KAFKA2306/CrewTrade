# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 65
- ETFs with sufficient data: 25
- Candidate universe after filtering: 16
- Selected ETFs (max_sharpe): 6
- Excluded 3 ETF(s) with volatility > 35.0%
- Excluded 36 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 14.76%
- Portfolio annual volatility: 13.73%
- Portfolio Sharpe ratio: 1.075
- Weighted expense ratio: 0.20%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.76% | 13.73% | 1.075 | 0.20% | Yes |
| low_volatility | 12.70% | 12.17% | 1.043 | 0.23% |  |
| cost_focus | 13.94% | 13.81% | 1.010 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18296520
- Current loan ratio: 0.547
- Buffer to 70%: 21.92% drop
- Buffer to 85%: 35.70% drop
- Max drawdown (history): -23.11%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,466,868 | 0.607 | No | No |
| -20% | ¥14,637,216 | 0.683 | No | No |
| -30% | ¥12,807,564 | 0.781 | Yes | No |
| -40% | ¥10,977,912 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 979
- Forced liquidation events: 357

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
