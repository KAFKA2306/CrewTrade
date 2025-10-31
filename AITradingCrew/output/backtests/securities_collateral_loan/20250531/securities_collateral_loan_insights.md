# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 34
- ETFs with sufficient data: 24
- Candidate universe after filtering: 14
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 14
- Excluded 6 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 8.97%
- Portfolio annual volatility: 9.09%
- Portfolio Sharpe ratio: 0.986
- Weighted expense ratio: 0.15%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.97% | 9.09% | 0.986 | 0.15% | Yes |
| low_volatility | 8.97% | 9.09% | 0.986 | 0.15% |  |
| cost_focus | 7.36% | 7.70% | 0.956 | 0.15% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18307345
- Current loan ratio: 0.546
- Buffer to 70%: 21.97% drop
- Buffer to 85%: 35.74% drop
- Max drawdown (history): -9.89%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,476,610 | 0.607 | No | No |
| -20% | ¥14,645,876 | 0.683 | No | No |
| -30% | ¥12,815,141 | 0.780 | Yes | No |
| -40% | ¥10,984,407 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 84
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
