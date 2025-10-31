# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 140
- ETFs with sufficient data: 111
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Excluded 13 ETF(s) with volatility > 25.0%
- Excluded 2 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 12.49%
- Portfolio annual volatility: 11.44%
- Portfolio Sharpe ratio: 1.092
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 12.49% | 11.44% | 1.092 | 0.24% | Yes |
| low_volatility | 7.91% | 13.09% | 0.604 | 0.22% |  |
| cost_focus | 12.40% | 13.07% | 0.949 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16600110
- Current loan ratio: 0.602
- Buffer to 70%: 13.94% drop
- Buffer to 85%: 29.13% drop
- Max drawdown (history): -44.07%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,940,099 | 0.669 | No | No |
| -20% | ¥13,280,088 | 0.753 | Yes | No |
| -30% | ¥11,620,077 | 0.861 | Yes | Yes |
| -40% | ¥9,960,066 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 415
- Forced liquidation events: 264

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
