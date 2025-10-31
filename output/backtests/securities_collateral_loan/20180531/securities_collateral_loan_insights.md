# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 43
- ETFs with sufficient data: 27
- Candidate universe after filtering: 18
- Selected ETFs (max_sharpe): 7
- Excluded 9 ETF(s) with volatility > 25.0%
- Excluded 7 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 13.11%
- Portfolio annual volatility: 14.25%
- Portfolio Sharpe ratio: 0.920
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 13.11% | 14.25% | 0.920 | 0.25% | Yes |
| low_volatility | 10.13% | 12.06% | 0.840 | 0.25% |  |
| cost_focus | 12.31% | 13.60% | 0.905 | 0.26% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18261852
- Current loan ratio: 0.548
- Buffer to 70%: 21.77% drop
- Buffer to 85%: 35.58% drop
- Max drawdown (history): -20.53%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,435,667 | 0.608 | No | No |
| -20% | ¥14,609,482 | 0.684 | No | No |
| -30% | ¥12,783,296 | 0.782 | Yes | No |
| -40% | ¥10,957,111 | 0.913 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 494
- Forced liquidation events: 154

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
