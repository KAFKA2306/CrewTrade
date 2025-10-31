# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after filtering: 18
- Selected ETFs (max_sharpe): 6
- Excluded 2 ETF(s) with volatility > 35.0%
- Excluded 12 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 19.12%
- Portfolio annual volatility: 14.44%
- Portfolio Sharpe ratio: 1.325
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 19.12% | 14.44% | 1.325 | 0.24% | Yes |
| low_volatility | 15.09% | 12.08% | 1.248 | 0.24% |  |
| cost_focus | 17.05% | 13.27% | 1.285 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18303676
- Current loan ratio: 0.546
- Buffer to 70%: 21.95% drop
- Buffer to 85%: 35.72% drop
- Max drawdown (history): -15.81%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,473,308 | 0.607 | No | No |
| -20% | ¥14,642,941 | 0.683 | No | No |
| -30% | ¥12,812,573 | 0.780 | Yes | No |
| -40% | ¥10,982,206 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 506
- Forced liquidation events: 205

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
