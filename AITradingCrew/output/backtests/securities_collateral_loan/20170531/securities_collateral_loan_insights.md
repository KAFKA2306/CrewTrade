# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 74
- ETFs with sufficient data: 52
- Candidate universe after filtering: 33
- Selected ETFs (max_sharpe): 14
- Excluded 20 ETF(s) with volatility > 25.0%
- Excluded 2 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 5.43%
- Portfolio annual volatility: 12.35%
- Portfolio Sharpe ratio: 0.439
- Weighted expense ratio: 0.34%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.43% | 12.35% | 0.439 | 0.34% | Yes |
| low_volatility | 5.13% | 10.83% | 0.473 | 0.36% |  |
| cost_focus | 5.54% | 11.37% | 0.487 | 0.38% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16623228
- Current loan ratio: 0.602
- Buffer to 70%: 14.06% drop
- Buffer to 85%: 29.23% drop
- Max drawdown (history): -16.08%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,960,905 | 0.668 | No | No |
| -20% | ¥13,298,582 | 0.752 | Yes | No |
| -30% | ¥11,636,260 | 0.859 | Yes | Yes |
| -40% | ¥9,973,937 | 1.003 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 163
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
