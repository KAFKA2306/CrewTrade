# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 121
- ETFs with sufficient data: 113
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Portfolio annual return: 17.19%
- Portfolio annual volatility: 18.49%
- Portfolio Sharpe ratio: 0.930
- Weighted expense ratio: 0.22%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 17.19% | 18.49% | 0.930 | 0.22% | Yes |
| low_volatility | 23.41% | 18.64% | 1.256 | 0.25% |  |
| cost_focus | 16.50% | 18.31% | 0.901 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16551484
- Current loan ratio: 0.604
- Buffer to 70%: 13.69% drop
- Buffer to 85%: 28.92% drop
- Max drawdown (history): -30.43%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,896,336 | 0.671 | No | No |
| -20% | ¥13,241,187 | 0.755 | Yes | No |
| -30% | ¥11,586,039 | 0.863 | Yes | Yes |
| -40% | ¥9,930,890 | 1.007 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 609
- Forced liquidation events: 318

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
