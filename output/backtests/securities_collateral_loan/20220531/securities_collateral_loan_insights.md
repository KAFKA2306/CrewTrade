# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 72
- ETFs with sufficient data: 10
- Candidate universe after filtering: 9
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 9
- Excluded 60 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 7.66%
- Portfolio annual volatility: 9.15%
- Portfolio Sharpe ratio: 0.837
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.66% | 9.15% | 0.837 | 0.17% | Yes |
| low_volatility | 7.66% | 9.15% | 0.837 | 0.17% |  |
| cost_focus | 7.66% | 9.15% | 0.837 | 0.17% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥24829499
- Current loan ratio: 0.403
- Buffer to 70%: 42.46% drop
- Buffer to 85%: 52.62% drop
- Max drawdown (history): -16.57%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥22,346,549 | 0.448 | No | No |
| -20% | ¥19,863,599 | 0.503 | No | No |
| -30% | ¥17,380,649 | 0.575 | No | No |
| -40% | ¥14,897,700 | 0.671 | No | No |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
