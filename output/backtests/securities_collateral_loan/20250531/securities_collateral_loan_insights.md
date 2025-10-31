# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 109
- ETFs with sufficient data: 93
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 8 ETF(s) with volatility > 35.0%
- Portfolio annual return: 13.71%
- Portfolio annual volatility: 14.10%
- Portfolio Sharpe ratio: 0.972
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 13.71% | 14.10% | 0.972 | 0.21% | Yes |
| low_volatility | 11.69% | 11.07% | 1.056 | 0.17% |  |
| cost_focus | 14.39% | 14.67% | 0.981 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18256828
- Current loan ratio: 0.548
- Buffer to 70%: 21.75% drop
- Buffer to 85%: 35.56% drop
- Max drawdown (history): -18.66%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,431,145 | 0.609 | No | No |
| -20% | ¥14,605,462 | 0.685 | No | No |
| -30% | ¥12,779,780 | 0.782 | Yes | No |
| -40% | ¥10,954,097 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 442
- Forced liquidation events: 122

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
