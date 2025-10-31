# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 35
- Candidate universe after filtering: 25
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 6 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 14.74%
- Portfolio annual volatility: 14.73%
- Portfolio Sharpe ratio: 1.001
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 14.74% | 14.73% | 1.001 | 0.23% | Yes |
| low_volatility | 11.67% | 13.53% | 0.863 | 0.28% |  |
| cost_focus | 13.20% | 14.60% | 0.904 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18299671
- Current loan ratio: 0.546
- Buffer to 70%: 21.93% drop
- Buffer to 85%: 35.71% drop
- Max drawdown (history): -16.48%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,469,704 | 0.607 | No | No |
| -20% | ¥14,639,737 | 0.683 | No | No |
| -30% | ¥12,809,770 | 0.781 | Yes | No |
| -40% | ¥10,979,803 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 650
- Forced liquidation events: 424

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
