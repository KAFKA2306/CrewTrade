# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 33
- Candidate universe after filtering: 20
- Selected ETFs (max_sharpe): 7
- Excluded 9 ETF(s) with volatility > 25.0%
- Excluded 9 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 11.10%
- Portfolio annual volatility: 13.91%
- Portfolio Sharpe ratio: 0.798
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 11.10% | 13.91% | 0.798 | 0.26% | Yes |
| low_volatility | 6.28% | 9.37% | 0.671 | 0.24% |  |
| cost_focus | 9.67% | 13.15% | 0.735 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18270856
- Current loan ratio: 0.547
- Buffer to 70%: 21.81% drop
- Buffer to 85%: 35.61% drop
- Max drawdown (history): -16.97%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,443,770 | 0.608 | No | No |
| -20% | ¥14,616,685 | 0.684 | No | No |
| -30% | ¥12,789,599 | 0.782 | Yes | No |
| -40% | ¥10,962,514 | 0.912 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 274
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
