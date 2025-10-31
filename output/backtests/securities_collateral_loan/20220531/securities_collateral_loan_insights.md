# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 72
- ETFs with sufficient data: 58
- Candidate universe after filtering: 29
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 10
- Excluded 12 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 8.09%
- Portfolio annual volatility: 12.47%
- Portfolio Sharpe ratio: 0.649
- Weighted expense ratio: 0.27%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.09% | 12.47% | 0.649 | 0.27% | Yes |
| low_volatility | 7.10% | 12.55% | 0.566 | 0.26% |  |
| cost_focus | 10.43% | 13.23% | 0.788 | 0.27% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18213666
- Current loan ratio: 0.549
- Buffer to 70%: 21.57% drop
- Buffer to 85%: 35.41% drop
- Max drawdown (history): -27.41%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,392,299 | 0.610 | No | No |
| -20% | ¥14,570,932 | 0.686 | No | No |
| -30% | ¥12,749,566 | 0.784 | Yes | No |
| -40% | ¥10,928,199 | 0.915 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 281
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
