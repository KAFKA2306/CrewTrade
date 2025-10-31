# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 219
- ETFs with sufficient data: 115
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 14
- Excluded 59 ETF(s) with volatility > 25.0%
- Excluded 3 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 15.14%
- Portfolio annual volatility: 11.69%
- Portfolio Sharpe ratio: 1.295
- Weighted expense ratio: 0.35%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.14% | 11.69% | 1.295 | 0.35% | Yes |
| low_volatility | 14.11% | 10.76% | 1.312 | 0.36% |  |
| cost_focus | 16.57% | 12.66% | 1.308 | 0.39% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16534680
- Current loan ratio: 0.605
- Buffer to 70%: 13.60% drop
- Buffer to 85%: 28.85% drop
- Max drawdown (history): -12.32%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,881,212 | 0.672 | No | No |
| -20% | ¥13,227,744 | 0.756 | Yes | No |
| -30% | ¥11,574,276 | 0.864 | Yes | Yes |
| -40% | ¥9,920,808 | 1.008 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 397
- Forced liquidation events: 184

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
