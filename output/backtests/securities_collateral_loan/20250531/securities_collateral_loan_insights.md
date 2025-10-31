# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 25
- Candidate universe after filtering: 15
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 15
- Excluded 5 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 12.02%
- Portfolio annual volatility: 10.70%
- Portfolio Sharpe ratio: 1.123
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 12.02% | 10.70% | 1.123 | 0.17% | Yes |
| low_volatility | 12.02% | 10.70% | 1.123 | 0.17% |  |
| cost_focus | 14.21% | 10.90% | 1.304 | 0.19% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18275540
- Current loan ratio: 0.547
- Buffer to 70%: 21.83% drop
- Buffer to 85%: 35.63% drop
- Max drawdown (history): -12.17%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,447,986 | 0.608 | No | No |
| -20% | ¥14,620,432 | 0.684 | No | No |
| -30% | ¥12,792,878 | 0.782 | Yes | No |
| -40% | ¥10,965,324 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 311
- Forced liquidation events: 2

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
