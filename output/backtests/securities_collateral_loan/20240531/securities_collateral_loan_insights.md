# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 98
- ETFs with sufficient data: 77
- Candidate universe after filtering: 40
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 15 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 14.34%
- Portfolio annual volatility: 12.56%
- Portfolio Sharpe ratio: 1.141
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.34% | 12.56% | 1.141 | 0.21% | Yes |
| low_volatility | 14.47% | 11.76% | 1.230 | 0.22% |  |
| cost_focus | 14.17% | 12.56% | 1.128 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18297920
- Current loan ratio: 0.547
- Buffer to 70%: 21.93% drop
- Buffer to 85%: 35.70% drop
- Max drawdown (history): -18.02%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,468,128 | 0.607 | No | No |
| -20% | ¥14,638,336 | 0.683 | No | No |
| -30% | ¥12,808,544 | 0.781 | Yes | No |
| -40% | ¥10,978,752 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 984
- Forced liquidation events: 422

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
