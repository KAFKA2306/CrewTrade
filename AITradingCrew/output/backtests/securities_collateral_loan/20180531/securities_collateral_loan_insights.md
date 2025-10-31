# Securities Collateral Loan Insight

## Optimization Summary
- Total ETFs evaluated: 70
- ETFs with sufficient data: 63
- Candidate universe after filtering: 40
- Selected ETFs (max_sharpe): 6
- Excluded 5 ETF(s) with volatility > 25.0%
- Portfolio annual return: 15.30%
- Portfolio annual volatility: 9.11%
- Portfolio Sharpe ratio: 1.679
- Weighted expense ratio: 0.21%

| Profile | Return | Volatility | Sharpe | Expense | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 15.30% | 9.11% | 1.679 | 0.21% | Yes |
| low_volatility | 10.17% | 6.95% | 1.462 | 0.26% |  |
| cost_focus | 14.21% | 8.92% | 1.593 | 0.22% |  |

## Current Profile
- Loan amount: ¥10,000,000.0
- Current collateral value: ¥18314338
- Current loan ratio: 0.546
- Buffer to 70%: 22.00% drop
- Buffer to 85%: 35.76% drop
- Max drawdown (history): -14.83%

## Stress Scenarios
| Scenario | Post Value | Loan Ratio | ≥70% | ≥85% |
| --- | --- | --- | --- | --- |
| -10% | ¥16,482,904 | 0.607 | No | No |
| -20% | ¥14,651,470 | 0.682 | No | No |
| -30% | ¥12,820,037 | 0.780 | Yes | No |
| -40% | ¥10,988,603 | 0.910 | Yes | Yes |

## Historical Breach Counts
- Margin call events: 69
- Forced liquidation events: 8

## Interest Projection (Simple)
| Days | Interest (¥) |
| --- | --- |
| 30 | 15,410.96 |
| 90 | 46,232.88 |
| 180 | 92,465.75 |
