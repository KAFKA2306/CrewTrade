# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 71
- ETFs with sufficient data: 59
- Candidate universe after filtering: 48
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 20
- Excluded 10 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.86%
- Portfolio annual volatility: 13.35%
- Portfolio Sharpe ratio: 0.888
- Weighted expense ratio: 0.23%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.86% | 13.35% | 0.888 | 0.23% | Yes |
| low_volatility | 11.86% | 13.35% | 0.888 | 0.23% |  |
| cost_focus | 12.01% | 13.99% | 0.859 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18127076
- Current loan ratio: 0.552
- Buffer to 70%: 21.19% drop
- Buffer to 85%: 35.10% drop
- Max drawdown (history): -32.63%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,314,368 | 0.613 | No | No |
| -20% | ¥14,501,660 | 0.690 | No | No |
| -30% | ¥12,688,953 | 0.788 | Yes | No |
| -40% | ¥10,876,245 | 0.919 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 3991
- Forced liquidation events: 3437

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
