# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 70
- ETFs with sufficient data: 63
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 5 ETF(s) with volatility > 25.0%
- Portfolio annual return: 22.56%
- Portfolio annual volatility: 11.22%
- Portfolio Sharpe ratio: 2.010
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 22.56% | 11.22% | 2.010 | 0.24% | Yes |
| low_volatility | 11.99% | 7.41% | 1.619 | 0.23% |  |
| cost_focus | 11.27% | 7.68% | 1.467 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18277068
- Current loan ratio: 0.547
- Buffer to 70%: 21.84% drop
- Buffer to 85%: 35.63% drop
- Max drawdown (history): -21.02%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,449,361 | 0.608 | No | No |
| -20% | ¥14,621,654 | 0.684 | No | No |
| -30% | ¥12,793,948 | 0.782 | Yes | No |
| -40% | ¥10,966,241 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 361
- Forced liquidation events: 259

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
