# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 89
- ETFs with sufficient data: 69
- Candidate universe after filtering: 30
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 20
- Excluded 15 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 3.62%
- Portfolio annual volatility: 12.23%
- Portfolio Sharpe ratio: 0.296
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 3.62% | 12.23% | 0.296 | 0.25% | Yes |
| low_volatility | 2.49% | 13.83% | 0.180 | 0.26% |  |
| cost_focus | 7.72% | 12.14% | 0.636 | 0.21% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18145084
- Current loan ratio: 0.551
- Buffer to 70%: 21.27% drop
- Buffer to 85%: 35.16% drop
- Max drawdown (history): -27.34%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,330,575 | 0.612 | No | No |
| -20% | ¥14,516,067 | 0.689 | No | No |
| -30% | ¥12,701,559 | 0.787 | Yes | No |
| -40% | ¥10,887,050 | 0.918 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 56
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
