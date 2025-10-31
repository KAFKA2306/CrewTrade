# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 32
- ETFs with sufficient data: 19
- Candidate universe after filtering: 11
- Selected ETFs (max_sharpe): 11
- Excluded 11 ETF(s) with volatility > 25.0%
- Excluded 2 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 2.84%
- Portfolio annual volatility: 15.72%
- Portfolio Sharpe ratio: 0.180
- Weighted expense ratio: 0.26%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 2.84% | 15.72% | 0.180 | 0.26% | Yes |
| low_volatility | 9.88% | 14.56% | 0.679 | 0.27% |  |
| cost_focus | 7.64% | 14.99% | 0.509 | 0.24% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18285106
- Current loan ratio: 0.547
- Buffer to 70%: 21.87% drop
- Buffer to 85%: 35.66% drop
- Max drawdown (history): -28.64%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,456,595 | 0.608 | No | No |
| -20% | ¥14,628,085 | 0.684 | No | No |
| -30% | ¥12,799,574 | 0.781 | Yes | No |
| -40% | ¥10,971,064 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 8
- Forced liquidation events: 0

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
