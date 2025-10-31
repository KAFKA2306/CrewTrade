# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 47
- ETFs with sufficient data: 26
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 14
- Excluded 14 ETF(s) with volatility > 25.0%
- Excluded 7 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 3.99%
- Portfolio annual volatility: 14.03%
- Portfolio Sharpe ratio: 0.284
- Weighted expense ratio: 0.31%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 3.99% | 14.03% | 0.284 | 0.31% | Yes |
| low_volatility | 3.78% | 12.97% | 0.292 | 0.29% |  |
| cost_focus | 5.33% | 13.86% | 0.385 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16615308
- Current loan ratio: 0.602
- Buffer to 70%: 14.02% drop
- Buffer to 85%: 29.19% drop
- Max drawdown (history): -15.64%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,953,777 | 0.669 | No | No |
| -20% | ¥13,292,246 | 0.752 | Yes | No |
| -30% | ¥11,630,716 | 0.860 | Yes | Yes |
| -40% | ¥9,969,185 | 1.003 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 249
- Forced liquidation events: 79

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
