# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 20
- Candidate universe after filtering: 11
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 12
- Excluded 64 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 6.80%
- Portfolio annual volatility: 6.50%
- Portfolio Sharpe ratio: 1.045
- Weighted expense ratio: 0.14%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 6.80% | 6.50% | 1.045 | 0.14% | Yes |
| low_volatility | 6.80% | 6.50% | 1.045 | 0.14% |  |
| cost_focus | 6.63% | 6.61% | 1.002 | 0.14% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥28982405
- Current loan ratio: 0.345
- Buffer to 70%: 50.71% drop
- Buffer to 85%: 59.41% drop
- Max drawdown (history): -13.62%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥26,084,165 | 0.383 | No | No |
| -20% | ¥23,185,924 | 0.431 | No | No |
| -30% | ¥20,287,684 | 0.493 | No | No |
| -40% | ¥17,389,443 | 0.575 | No | No |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
