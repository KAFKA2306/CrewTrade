# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 15
- Candidate universe after filtering: 9
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 9
- Excluded 19 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 10.49%
- Portfolio annual volatility: 13.44%
- Portfolio Sharpe ratio: 0.781
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.49% | 13.44% | 0.781 | 0.27% | Yes |
| low_volatility | 10.49% | 13.44% | 0.781 | 0.27% |  |
| cost_focus | 10.49% | 13.44% | 0.781 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥25225179
- Current loan ratio: 0.396
- Buffer to 70%: 43.37% drop
- Buffer to 85%: 53.36% drop
- Max drawdown (history): -18.88%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥22,702,662 | 0.441 | No | No |
| -20% | ¥20,180,144 | 0.495 | No | No |
| -30% | ¥17,657,626 | 0.566 | No | No |
| -40% | ¥15,135,108 | 0.661 | No | No |

## Historical Breach Counts
- Margin call events: 0
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
