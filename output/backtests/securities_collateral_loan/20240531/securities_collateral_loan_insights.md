# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 99
- ETFs with sufficient data: 38
- Candidate universe after filtering: 19
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 19
- Excluded 55 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.28%
- Portfolio annual volatility: 7.82%
- Portfolio Sharpe ratio: 1.443
- Weighted expense ratio: 0.18%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.28% | 7.82% | 1.443 | 0.18% | Yes |
| low_volatility | 11.28% | 7.82% | 1.443 | 0.18% |  |
| cost_focus | 9.23% | 6.77% | 1.364 | 0.15% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18184175
- Current loan ratio: 0.550
- Buffer to 70%: 21.44% drop
- Buffer to 85%: 35.30% drop
- Max drawdown (history): -11.91%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,365,758 | 0.611 | No | No |
| -20% | ¥14,547,340 | 0.687 | No | No |
| -30% | ¥12,728,923 | 0.786 | Yes | No |
| -40% | ¥10,910,505 | 0.916 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 898
- Forced liquidation events: 9

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
