# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 44
- ETFs with sufficient data: 40
- Candidate universe after filtering: 32
- Selected ETFs (max_sharpe): 6
- Excluded 4 ETF(s) with volatility > 25.0%
- Portfolio annual return: 18.73%
- Portfolio annual volatility: 9.68%
- Portfolio Sharpe ratio: 1.934
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 18.73% | 9.68% | 1.934 | 0.26% | Yes |
| low_volatility | 18.38% | 10.15% | 1.810 | 0.26% |  |
| cost_focus | 20.33% | 10.86% | 1.873 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18302001
- Current loan ratio: 0.546
- Buffer to 70%: 21.94% drop
- Buffer to 85%: 35.72% drop
- Max drawdown (history): -12.80%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,471,801 | 0.607 | No | No |
| -20% | ¥14,641,601 | 0.683 | No | No |
| -30% | ¥12,811,401 | 0.781 | Yes | No |
| -40% | ¥10,981,201 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 451
- Forced liquidation events: 152

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
