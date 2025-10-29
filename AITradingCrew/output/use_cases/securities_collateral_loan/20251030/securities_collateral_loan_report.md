# Securities Collateral Loan Risk Report

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥17310000
- Current loan ratio: 0.578
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 17.47% drop from current value
- Buffer to forced liquidation: 32.04% drop from current value
- Historical max drawdown (portfolio): -18.66%

## Collateral Breakdown
| Ticker | Description | Quantity | Price | Market Value |
| --- | --- | --- | --- | --- |
| 1489.T | Nikkei High Dividend Yield 50 ETF | 4000 | ¥2565.00 | ¥10260000 |
| 348A.T | Yomiuri 333 ETF | 30000 | ¥235.00 | ¥7050000 |

## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥15579000 | 0.642 | No | No |
| -20% | ¥13848000 | 0.722 | Yes | No |
| -30% | ¥12117000 | 0.825 | Yes | No |
| -40% | ¥10386000 | 0.963 | Yes | Yes |

## Historical Breaches
### Margin Call Alerts (>= 70%)
| Date | Loan Ratio |
| --- | --- |
| 2025-04-04 | 0.700 |
| 2025-04-07 | 0.779 |
| 2025-04-08 | 0.736 |
| 2025-04-09 | 0.763 |
| 2025-04-10 | 0.712 |
| 2025-04-11 | 0.727 |
| 2025-04-14 | 0.723 |
| 2025-04-15 | 0.717 |
| 2025-04-16 | 0.723 |
| 2025-04-17 | 0.714 |
| 2025-04-18 | 0.705 |
| 2025-04-21 | 0.714 |
| 2025-04-22 | 0.713 |

## Notes
- Loan ratio is calculated as outstanding balance divided by collateral market value.
- Rakuten Securities/Rakuten Bank requires top-up within 2 business days once the ratio reaches 70%, and may liquidate collateral immediately at 85%+.
- Borrowing limit is capped at approximately 60% of collateral value; ensure new acquisitions keep the loan ratio below 0.60 after execution.
- Interest is estimated on a simple basis and excludes taxes or transaction costs.
