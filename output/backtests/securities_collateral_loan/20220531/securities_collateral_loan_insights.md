# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 72
- ETFs with sufficient data: 6
- Candidate universe after filtering: 6
- Selected ETFs (max_sharpe): 6
- Excluded 6 ETF(s) with volatility > 25.0%
- Excluded 58 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 7.01%
- Portfolio annual volatility: 8.83%
- Portfolio Sharpe ratio: 0.794
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.01% | 8.83% | 0.794 | 0.18% | Yes |
| low_volatility | 6.74% | 8.93% | 0.755 | 0.18% |  |
| cost_focus | 6.36% | 9.72% | 0.654 | 0.20% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18303146
- Current loan ratio: 0.546
- Buffer to 70%: 21.95% drop
- Buffer to 85%: 35.72% drop
- Max drawdown (history): -13.07%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,472,831 | 0.607 | No | No |
| -20% | ¥14,642,516 | 0.683 | No | No |
| -30% | ¥12,812,202 | 0.780 | Yes | No |
| -40% | ¥10,981,887 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 314
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
