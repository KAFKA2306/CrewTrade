# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 25
- Candidate universe after filtering: 15
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 15
- Excluded 5 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 9.42%
- Portfolio annual volatility: 10.68%
- Portfolio Sharpe ratio: 0.881
- Weighted expense ratio: 0.17%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 9.42% | 10.68% | 0.881 | 0.17% | Yes |
| low_volatility | 9.42% | 10.68% | 0.881 | 0.17% |  |
| cost_focus | 9.46% | 9.88% | 0.958 | 0.16% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18280456
- Current loan ratio: 0.547
- Buffer to 70%: 21.85% drop
- Buffer to 85%: 35.64% drop
- Max drawdown (history): -13.74%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,452,410 | 0.608 | No | No |
| -20% | ¥14,624,365 | 0.684 | No | No |
| -30% | ¥12,796,319 | 0.781 | Yes | No |
| -40% | ¥10,968,274 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 85
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
