# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 53
- ETFs with sufficient data: 37
- Candidate universe after filtering: 28
- Selected ETFs (max_sharpe): 14
- Excluded 15 ETF(s) with volatility > 25.0%
- Excluded 1 ETF(s) with drawdown worse than -30.0%
- Portfolio annual return: 24.20%
- Portfolio annual volatility: 13.67%
- Portfolio Sharpe ratio: 1.770
- Weighted expense ratio: 0.30%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 24.20% | 13.67% | 1.770 | 0.30% | Yes |
| low_volatility | 21.50% | 12.75% | 1.686 | 0.33% |  |
| cost_focus | 24.14% | 13.85% | 1.743 | 0.31% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥16597649
- Current loan ratio: 0.602
- Buffer to 70%: 13.93% drop
- Buffer to 85%: 29.12% drop
- Max drawdown (history): -16.47%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥14,937,884 | 0.669 | No | No |
| -20% | ¥13,278,119 | 0.753 | Yes | No |
| -30% | ¥11,618,354 | 0.861 | Yes | Yes |
| -40% | ¥9,958,590 | 1.004 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 466
- Forced liquidation events: 395

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
