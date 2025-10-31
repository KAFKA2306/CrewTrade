# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 69
- Candidate universe after filtering: 40
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 7
- Excluded 15 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 7.82%
- Portfolio annual volatility: 12.39%
- Portfolio Sharpe ratio: 0.631
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.82% | 12.39% | 0.631 | 0.21% | Yes |
| low_volatility | 8.74% | 9.44% | 0.926 | 0.22% |  |
| cost_focus | 8.86% | 13.98% | 0.634 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18300931
- Current loan ratio: 0.546
- Buffer to 70%: 21.94% drop
- Buffer to 85%: 35.72% drop
- Max drawdown (history): -18.73%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,470,838 | 0.607 | No | No |
| -20% | ¥14,640,745 | 0.683 | No | No |
| -30% | ¥12,810,652 | 0.781 | Yes | No |
| -40% | ¥10,980,559 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 496
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
