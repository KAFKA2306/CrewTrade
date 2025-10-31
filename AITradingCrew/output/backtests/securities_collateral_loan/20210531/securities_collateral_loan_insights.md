# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 103
- ETFs with sufficient data: 32
- Candidate universe after filtering: 25
- Selected ETFs (max_sharpe): 9
- Excluded 32 ETF(s) with volatility > 25.0%
- Excluded 32 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 9.38%
- Portfolio annual volatility: 8.85%
- Portfolio Sharpe ratio: 1.061
- Weighted expense ratio: 0.15%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.38% | 8.85% | 1.061 | 0.15% | Yes |
| low_volatility | 7.39% | 7.90% | 0.936 | 0.15% |  |
| cost_focus | 7.75% | 8.67% | 0.894 | 0.17% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18302334
- Current loan ratio: 0.546
- Buffer to 70%: 21.95% drop
- Buffer to 85%: 35.72% drop
- Max drawdown (history): -13.03%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,472,101 | 0.607 | No | No |
| -20% | ¥14,641,867 | 0.683 | No | No |
| -30% | ¥12,811,634 | 0.780 | Yes | No |
| -40% | ¥10,981,400 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 33
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
