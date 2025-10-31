# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 121
- ETFs with sufficient data: 102
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 7 ETF(s) with volatility > 25.0%
- Portfolio annual return: 13.36%
- Portfolio annual volatility: 8.50%
- Portfolio Sharpe ratio: 1.572
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 13.36% | 8.50% | 1.572 | 0.18% | Yes |
| low_volatility | 9.21% | 7.14% | 1.290 | 0.19% |  |
| cost_focus | 10.46% | 7.98% | 1.310 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18331128
- Current loan ratio: 0.546
- Buffer to 70%: 22.07% drop
- Buffer to 85%: 35.82% drop
- Max drawdown (history): -19.60%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,498,015 | 0.606 | No | No |
| -20% | ¥14,664,903 | 0.682 | No | No |
| -30% | ¥12,831,790 | 0.779 | Yes | No |
| -40% | ¥10,998,677 | 0.909 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 85
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
