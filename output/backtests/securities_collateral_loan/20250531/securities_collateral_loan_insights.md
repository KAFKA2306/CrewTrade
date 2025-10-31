# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 109
- ETFs with sufficient data: 95
- Candidate universe after filtering: 40
- Risk gate metric: max_asset_drawdown — Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown constraint; other limits remain for portfolio construction, not asset gating.

- Selected ETFs (max_sharpe): 6
- Excluded 6 ETF(s) with drawdown worse than -45.0%
- Portfolio annual return: 10.90%
- Portfolio annual volatility: 10.54%
- Portfolio Sharpe ratio: 1.034
- Weighted expense ratio: 0.14%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.90% | 10.54% | 1.034 | 0.14% | Yes |
| low_volatility | 11.78% | 10.96% | 1.075 | 0.23% |  |
| cost_focus | 14.21% | 14.03% | 1.013 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18322198
- Current loan ratio: 0.546
- Buffer to 70%: 22.03% drop
- Buffer to 85%: 35.79% drop
- Max drawdown (history): -13.98%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,489,978 | 0.606 | No | No |
| -20% | ¥14,657,758 | 0.682 | No | No |
| -30% | ¥12,825,538 | 0.780 | Yes | No |
| -40% | ¥10,993,319 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 118
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
