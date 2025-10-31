# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 25
- Candidate universe after filtering: 17
- Selected ETFs (max_sharpe): 9
- Excluded 12 ETF(s) with volatility > 25.0%
- Excluded 4 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 18.29%
- Portfolio annual volatility: 14.04%
- Portfolio Sharpe ratio: 1.303
- Weighted expense ratio: 0.22%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 18.29% | 14.04% | 1.303 | 0.22% | Yes |
| low_volatility | 15.85% | 12.46% | 1.272 | 0.23% |  |
| cost_focus | 17.99% | 13.62% | 1.321 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18268612
- Current loan ratio: 0.547
- Buffer to 70%: 21.80% drop
- Buffer to 85%: 35.60% drop
- Max drawdown (history): -15.23%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,441,751 | 0.608 | No | No |
| -20% | ¥14,614,890 | 0.684 | No | No |
| -30% | ¥12,788,028 | 0.782 | Yes | No |
| -40% | ¥10,961,167 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 527
- Forced liquidation events: 192

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
