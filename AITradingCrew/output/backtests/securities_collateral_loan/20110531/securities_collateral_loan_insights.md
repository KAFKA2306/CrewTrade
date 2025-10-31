# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 37
- ETFs with sufficient data: 22
- Candidate universe after filtering: 15
- Selected ETFs (max_sharpe): 14
- Excluded 12 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 5.08%
- Portfolio annual volatility: 15.30%
- Portfolio Sharpe ratio: 0.332
- Weighted expense ratio: 0.35%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.08% | 15.30% | 0.332 | 0.35% | Yes |
| low_volatility | 8.98% | 14.54% | 0.617 | 0.27% |  |
| cost_focus | 7.93% | 15.43% | 0.514 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16632705
- Current loan ratio: 0.601
- Buffer to 70%: 14.11% drop
- Buffer to 85%: 29.27% drop
- Max drawdown (history): -30.13%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,969,434 | 0.668 | No | No |
| -20% | ¥13,306,164 | 0.751 | Yes | No |
| -30% | ¥11,642,894 | 0.859 | Yes | Yes |
| -40% | ¥9,979,623 | 1.002 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 140
- Forced liquidation events: 4

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
