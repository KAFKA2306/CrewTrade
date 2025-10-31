# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 20
- Candidate universe after filtering: 11
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 11
- Excluded 64 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 6.80%
- Portfolio annual volatility: 6.50%
- Portfolio Sharpe ratio: 1.045
- Weighted expense ratio: 0.14%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 6.80% | 6.50% | 1.045 | 0.14% | Yes |
| low_volatility | 6.80% | 6.50% | 1.045 | 0.14% |  |
| cost_focus | 6.63% | 6.61% | 1.002 | 0.14% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18254538
- Current loan ratio: 0.548
- Buffer to 70%: 21.74% drop
- Buffer to 85%: 35.55% drop
- Max drawdown (history): -9.70%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,429,084 | 0.609 | No | No |
| -20% | ¥14,603,630 | 0.685 | No | No |
| -30% | ¥12,778,176 | 0.783 | Yes | No |
| -40% | ¥10,952,722 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 309
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
