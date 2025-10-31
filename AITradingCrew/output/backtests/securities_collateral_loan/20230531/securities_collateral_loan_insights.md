# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 160
- ETFs with sufficient data: 124
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Excluded 17 ETF(s) with volatility > 25.0%
- Excluded 1 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.97%
- Portfolio annual volatility: 10.19%
- Portfolio Sharpe ratio: 1.175
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.97% | 10.19% | 1.175 | 0.27% | Yes |
| low_volatility | 12.72% | 9.71% | 1.310 | 0.29% |  |
| cost_focus | 13.19% | 10.32% | 1.279 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16592120
- Current loan ratio: 0.603
- Buffer to 70%: 13.90% drop
- Buffer to 85%: 29.09% drop
- Max drawdown (history): -8.47%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,932,908 | 0.670 | No | No |
| -20% | ¥13,273,696 | 0.753 | Yes | No |
| -30% | ¥11,614,484 | 0.861 | Yes | Yes |
| -40% | ¥9,955,272 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 428
- Forced liquidation events: 151

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
