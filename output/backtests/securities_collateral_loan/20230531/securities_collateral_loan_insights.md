# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 13
- Candidate universe after filtering: 13
- Selected ETFs (max_sharpe): 13
- Excluded 8 ETF(s) with volatility > 25.0%
- Excluded 63 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 5.82%
- Portfolio annual volatility: 10.76%
- Portfolio Sharpe ratio: 0.541
- Weighted expense ratio: 0.16%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.82% | 10.76% | 0.541 | 0.16% | Yes |
| low_volatility | 6.96% | 7.48% | 0.931 | 0.17% |  |
| cost_focus | 5.39% | 7.21% | 0.747 | 0.14% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18267907
- Current loan ratio: 0.547
- Buffer to 70%: 21.80% drop
- Buffer to 85%: 35.60% drop
- Max drawdown (history): -17.74%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,441,116 | 0.608 | No | No |
| -20% | ¥14,614,326 | 0.684 | No | No |
| -30% | ¥12,787,535 | 0.782 | Yes | No |
| -40% | ¥10,960,744 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 232
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
