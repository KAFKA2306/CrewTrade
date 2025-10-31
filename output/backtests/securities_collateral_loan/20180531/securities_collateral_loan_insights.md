# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 43
- ETFs with sufficient data: 36
- Candidate universe after filtering: 25
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 8
- Excluded 7 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 11.86%
- Portfolio annual volatility: 14.49%
- Portfolio Sharpe ratio: 0.819
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.86% | 14.49% | 0.819 | 0.24% | Yes |
| low_volatility | 8.75% | 11.64% | 0.752 | 0.29% |  |
| cost_focus | 13.67% | 14.94% | 0.915 | 0.26% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18290206
- Current loan ratio: 0.547
- Buffer to 70%: 21.89% drop
- Buffer to 85%: 35.68% drop
- Max drawdown (history): -20.57%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,461,185 | 0.608 | No | No |
| -20% | ¥14,632,165 | 0.683 | No | No |
| -30% | ¥12,803,144 | 0.781 | Yes | No |
| -40% | ¥10,974,124 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 376
- Forced liquidation events: 90

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
