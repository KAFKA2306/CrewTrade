# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 92
- ETFs with sufficient data: 15
- Candidate universe after filtering: 15
- Selected ETFs (max_sharpe): 6
- Excluded 18 ETF(s) with volatility > 25.0%
- Excluded 53 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 9.14%
- Portfolio annual volatility: 8.33%
- Portfolio Sharpe ratio: 1.097
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.14% | 8.33% | 1.097 | 0.17% | Yes |
| low_volatility | 7.47% | 7.08% | 1.055 | 0.15% |  |
| cost_focus | 6.22% | 7.64% | 0.814 | 0.16% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18312561
- Current loan ratio: 0.546
- Buffer to 70%: 21.99% drop
- Buffer to 85%: 35.76% drop
- Max drawdown (history): -10.88%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,481,305 | 0.607 | No | No |
| -20% | ¥14,650,049 | 0.683 | No | No |
| -30% | ¥12,818,793 | 0.780 | Yes | No |
| -40% | ¥10,987,537 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 243
- Forced liquidation events: 135

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
