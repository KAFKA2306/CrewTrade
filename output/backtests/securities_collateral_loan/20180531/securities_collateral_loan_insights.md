# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 43
- ETFs with sufficient data: 29
- Candidate universe after filtering: 20
- Selected ETFs (max_sharpe): 6
- Excluded 1 ETF(s) with volatility > 35.0%
- Excluded 13 ETF(s) with drawdown worse than -35.0%
- Portfolio annual return: 13.69%
- Portfolio annual volatility: 14.55%
- Portfolio Sharpe ratio: 0.941
- Weighted expense ratio: 0.25%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 13.69% | 14.55% | 0.941 | 0.25% | Yes |
| low_volatility | 10.56% | 12.68% | 0.833 | 0.26% |  |
| cost_focus | 12.88% | 13.80% | 0.933 | 0.23% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18294442
- Current loan ratio: 0.547
- Buffer to 70%: 21.91% drop
- Buffer to 85%: 35.69% drop
- Max drawdown (history): -18.09%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,464,998 | 0.607 | No | No |
| -20% | ¥14,635,554 | 0.683 | No | No |
| -30% | ¥12,806,109 | 0.781 | Yes | No |
| -40% | ¥10,976,665 | 0.911 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 411
- Forced liquidation events: 229

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
