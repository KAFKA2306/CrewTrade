# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 63
- ETFs with sufficient data: 37
- Candidate universe after filtering: 22
- Selected ETFs (max_sharpe): 14
- Excluded 18 ETF(s) with volatility > 25.0%
- Excluded 8 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.01%
- Portfolio annual volatility: 13.45%
- Portfolio Sharpe ratio: 0.818
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.01% | 13.45% | 0.818 | 0.26% | Yes |
| low_volatility | 11.72% | 12.79% | 0.916 | 0.28% |  |
| cost_focus | 10.29% | 12.46% | 0.826 | 0.25% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16641346
- Current loan ratio: 0.601
- Buffer to 70%: 14.16% drop
- Buffer to 85%: 29.30% drop
- Max drawdown (history): -17.03%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,977,211 | 0.668 | No | No |
| -20% | ¥13,313,077 | 0.751 | Yes | No |
| -30% | ¥11,648,942 | 0.858 | Yes | Yes |
| -40% | ¥9,984,808 | 1.002 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 265
- Forced liquidation events: 28

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
