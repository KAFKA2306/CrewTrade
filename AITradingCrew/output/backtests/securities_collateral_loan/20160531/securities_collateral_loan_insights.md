# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 26
- Candidate universe after filtering: 13
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 13
- Excluded 15 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 14.63%
- Portfolio annual volatility: 14.78%
- Portfolio Sharpe ratio: 0.990
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.63% | 14.78% | 0.990 | 0.27% | Yes |
| low_volatility | 14.63% | 14.78% | 0.990 | 0.27% |  |
| cost_focus | 13.48% | 15.40% | 0.875 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥23796307
- Current loan ratio: 0.420
- Buffer to 70%: 39.97% drop
- Buffer to 85%: 50.56% drop
- Max drawdown (history): -18.92%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥21,416,676 | 0.467 | No | No |
| -20% | ¥19,037,046 | 0.525 | No | No |
| -30% | ¥16,657,415 | 0.600 | No | No |
| -40% | ¥14,277,784 | 0.700 | Yes | No |

## Historical Breach Counts
- Margin call events: 395
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
