# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 36
- ETFs with sufficient data: 20
- Candidate universe after filtering: 13
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 13
- Excluded 16 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 15.83%
- Portfolio annual volatility: 14.02%
- Portfolio Sharpe ratio: 1.129
- Weighted expense ratio: 0.29%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.83% | 14.02% | 1.129 | 0.29% | Yes |
| low_volatility | 15.83% | 14.02% | 1.129 | 0.29% |  |
| cost_focus | 15.00% | 14.47% | 1.036 | 0.28% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥24723406
- Current loan ratio: 0.404
- Buffer to 70%: 42.22% drop
- Buffer to 85%: 52.41% drop
- Max drawdown (history): -15.62%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥22,251,065 | 0.449 | No | No |
| -20% | ¥19,778,724 | 0.506 | No | No |
| -30% | ¥17,306,384 | 0.578 | No | No |
| -40% | ¥14,834,043 | 0.674 | No | No |

## Historical Breach Counts
- Margin call events: 647
- Forced liquidation events: 25

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
