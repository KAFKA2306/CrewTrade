# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after filtering: 19
- Selected ETFs (max_sharpe): 6
- Excluded 11 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 18.09%
- Portfolio annual volatility: 13.90%
- Portfolio Sharpe ratio: 1.301
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 18.09% | 13.90% | 1.301 | 0.25% | Yes |
| low_volatility | 15.82% | 12.90% | 1.226 | 0.27% |  |
| cost_focus | 18.82% | 14.04% | 1.341 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18290697
- Current loan ratio: 0.547
- Buffer to 70%: 21.90% drop
- Buffer to 85%: 35.68% drop
- Max drawdown (history): -15.42%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,461,627 | 0.608 | No | No |
| -20% | ¥14,632,557 | 0.683 | No | No |
| -30% | ¥12,803,488 | 0.781 | Yes | No |
| -40% | ¥10,974,418 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 425
- Forced liquidation events: 327

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
