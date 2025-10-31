# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 45
- Candidate universe after filtering: 29
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 7
- Excluded 6 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 7.82%
- Portfolio annual volatility: 10.86%
- Portfolio Sharpe ratio: 0.720
- Weighted expense ratio: 0.24%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 7.82% | 10.86% | 0.720 | 0.24% | Yes |
| low_volatility | 6.68% | 10.40% | 0.642 | 0.28% |  |
| cost_focus | 8.20% | 12.25% | 0.669 | 0.20% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18293992
- Current loan ratio: 0.547
- Buffer to 70%: 21.91% drop
- Buffer to 85%: 35.69% drop
- Max drawdown (history): -14.84%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,464,593 | 0.607 | No | No |
| -20% | ¥14,635,194 | 0.683 | No | No |
| -30% | ¥12,805,794 | 0.781 | Yes | No |
| -40% | ¥10,976,395 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 14
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
