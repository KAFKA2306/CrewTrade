# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 14
- Candidate universe after filtering: 9
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 9
- Excluded 20 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 10.47%
- Portfolio annual volatility: 13.59%
- Portfolio Sharpe ratio: 0.770
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.47% | 13.59% | 0.770 | 0.27% | Yes |
| low_volatility | 10.47% | 13.59% | 0.770 | 0.27% |  |
| cost_focus | 10.47% | 13.59% | 0.770 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18300271
- Current loan ratio: 0.546
- Buffer to 70%: 21.94% drop
- Buffer to 85%: 35.71% drop
- Max drawdown (history): -16.30%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,470,244 | 0.607 | No | No |
| -20% | ¥14,640,217 | 0.683 | No | No |
| -30% | ¥12,810,190 | 0.781 | Yes | No |
| -40% | ¥10,980,163 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 851
- Forced liquidation events: 215

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
