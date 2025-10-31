# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 121
- ETFs with sufficient data: 34
- Candidate universe after filtering: 27
- Selected ETFs (max_sharpe): 14
- Excluded 45 ETF(s) with volatility > 25.0%
- Excluded 34 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 9.15%
- Portfolio annual volatility: 12.36%
- Portfolio Sharpe ratio: 0.740
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.15% | 12.36% | 0.740 | 0.17% | Yes |
| low_volatility | 8.72% | 9.76% | 0.894 | 0.18% |  |
| cost_focus | 9.39% | 10.69% | 0.878 | 0.16% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16603120
- Current loan ratio: 0.602
- Buffer to 70%: 13.96% drop
- Buffer to 85%: 29.14% drop
- Max drawdown (history): -19.92%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,942,808 | 0.669 | No | No |
| -20% | ¥13,282,496 | 0.753 | Yes | No |
| -30% | ¥11,622,184 | 0.860 | Yes | Yes |
| -40% | ¥9,961,872 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 306
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
