# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 25
- Candidate universe after filtering: 17
- Selected ETFs (max_sharpe): 7
- Excluded 12 ETF(s) with volatility > 25.0%
- Excluded 4 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 15.53%
- Portfolio annual volatility: 14.07%
- Portfolio Sharpe ratio: 1.104
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.53% | 14.07% | 1.104 | 0.24% | Yes |
| low_volatility | 14.32% | 13.49% | 1.061 | 0.24% |  |
| cost_focus | 15.68% | 14.41% | 1.088 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18310204
- Current loan ratio: 0.546
- Buffer to 70%: 21.98% drop
- Buffer to 85%: 35.75% drop
- Max drawdown (history): -15.08%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,479,184 | 0.607 | No | No |
| -20% | ¥14,648,163 | 0.683 | No | No |
| -30% | ¥12,817,143 | 0.780 | Yes | No |
| -40% | ¥10,986,122 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 632
- Forced liquidation events: 412

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
