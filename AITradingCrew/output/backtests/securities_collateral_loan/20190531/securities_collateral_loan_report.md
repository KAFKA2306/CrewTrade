# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18320323
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.02% drop from current value
- Buffer to forced liquidation: 35.78% drop from current value
- Historical max drawdown (portfolio): -6.23%

## Optimization Summary
- Total ETFs evaluated: 81
- ETFs with sufficient data: 67
- Candidate universe after correlation filter: 40 (threshold 0.90)
- Excluded hedged ETFs: 1496.T(ｉシェアーズ　米ドル建て投資適), 1482.T(ｉシェアーズ・コア　米国債７－), 1487.T(上場インデックスファンド米国債)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1498.T(Ｏｎｅ　ＥＴＦ　ＥＳＧ), 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1619.T(ＮＥＸＴ　ＦＵＮＤＳ　建設・資), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1485.T(ＭＡＸＩＳ　ＪＡＰＡＮ　設備・)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 5.60%, volatility 5.48%, Sharpe 1.022, expense 0.19%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2016-05-31 to 2019-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 5.60% | - | - |
| Annual Volatility | 5.48% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.022 | - | - |
| Weighted Expense Ratio | 0.19% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.60% | 5.48% | 1.022 | 0.19% | Yes |
| low_volatility | 4.08% | 5.76% | 0.709 | 0.21% |  |
| cost_focus | 4.42% | 6.47% | 0.683 | 0.18% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 10.34% | 8.50% | 1.216 | 0.14% | 14.295 |
| 2 | 1660.T | ＭＡＸＩＳ高利回りＪリート上場投信 | 9.65% | 8.47% | 1.139 | 0.14% | 13.454 |
| 3 | 1476.T | ｉシェアーズ・コア　Ｊリート　ＥＴＦ | 9.43% | 8.64% | 1.092 | 0.15% | 12.636 |
| 4 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 9.47% | 8.66% | 1.093 | 0.15% | 12.615 |
| 5 | 1398.T | ＳＭＤＡＭ　東証ＲＥＩＴ指数上場投信 | 9.54% | 8.73% | 1.094 | 0.22% | 12.537 |
| 6 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配 | 9.29% | 8.69% | 1.069 | 0.30% | 12.303 |
| 7 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 9.82% | 9.27% | 1.059 | 0.25% | 11.423 |
| 8 | 1488.T | ｉＦｒｅｅＥＴＦ　東証ＲＥＩＴ指数 | 8.63% | 9.23% | 0.935 | 0.15% | 10.133 |
| 9 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし） | 9.02% | 23.60% | 0.382 | 0.20% | 1.620 |
| 10 | 1596.T | ＮＺＡＭ　上場投信　ＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌｓ　 | 4.21% | 16.65% | 0.253 | 0.11% | 1.517 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内株式 | 2 | ¥6,529,707 | 35.6% |
| 債券 | 1 | ¥4,404,840 | 24.0% |
| コモディティ | 1 | ¥3,051,630 | 16.7% |
| REIT | 2 | ¥2,724,206 | 14.9% |
| その他 | 1 | ¥1,609,940 | 8.8% |

### Top Holdings (out of 7 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 2651 | ¥2045.00 | ¥5421295 | 29.6% | 0.15% | 9.47% | 8.66% | 1.093 |
| 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 213 | ¥20680.00 | ¥4404840 | 24.0% | 0.16% | -0.26% | 6.57% | -0.040 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 827 | ¥3690.00 | ¥3051630 | 16.7% | N/A | -1.48% | 7.53% | -0.196 |
| 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 877 | ¥1934.00 | ¥1696118 | 9.3% | 0.30% | 9.29% | 8.69% | 1.069 |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 202 | ¥7970.00 | ¥1609940 | 8.8% | 0.20% | 9.02% | 23.60% | 0.382 |
| 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 569 | ¥1948.00 | ¥1108412 | 6.1% | 0.25% | 9.82% | 9.27% | 1.059 |
| 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 524 | ¥1962.00 | ¥1028088 | 5.6% | 0.14% | 10.34% | 8.50% | 1.216 |

*Total: 7 ETFs, Portfolio value: ¥18,320,323*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -0.69% | 8.50% | -0.081 |
| 2016 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -1.55% | 12.50% | -0.124 |
| 2016 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | -1.68% | 12.72% | -0.132 |
| 2016 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 7.25% | 10.59% | 0.684 |
| 2016 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.53% | 24.79% | 0.546 |
| 2016 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | -3.20% | 15.55% | -0.206 |
| 2016 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | -2.36% | 11.58% | -0.203 |
| 2017 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 6.94% | 5.29% | 1.312 |
| 2017 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -9.76% | 8.41% | -1.160 |
| 2017 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | -10.38% | 8.03% | -1.293 |
| 2017 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | -2.70% | 8.83% | -0.306 |
| 2017 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 26.77% | 14.21% | 1.884 |
| 2017 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | -8.35% | 10.30% | -0.811 |
| 2017 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | -9.44% | 7.81% | -1.209 |
| 2018 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -5.06% | 6.96% | -0.728 |
| 2018 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 6.70% | 8.90% | 0.753 |
| 2018 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 7.76% | 8.66% | 0.896 |
| 2018 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | -3.45% | 6.75% | -0.511 |
| 2018 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | -3.81% | 25.86% | -0.148 |
| 2018 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 7.34% | 9.73% | 0.754 |
| 2018 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 7.34% | 8.67% | 0.847 |
| 2019 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.96% | 8.80% | 0.109 |
| 2019 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 7.92% | 8.76% | 0.903 |
| 2019 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 7.15% | 9.36% | 0.764 |
| 2019 | 1486.T | 上場インデックスファンド米国債券（為替ヘッジなし） | 2.63% | 6.28% | 0.419 |
| 2019 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 12.89% | 19.08% | 0.675 |
| 2019 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 7.39% | 8.81% | 0.838 |
| 2019 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 8.22% | 8.87% | 0.927 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2016 | 34.55% | 45.42% | 0.761 |
| 2017 | -2.63% | 4.46% | -0.590 |
| 2018 | 1.13% | 5.79% | 0.195 |
| 2019 | 5.72% | 5.24% | 1.092 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2019-06-03 to 2020-05-29 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 6.25% |
| Annualized Return | 6.57% |
| Annualized Volatility | 22.70% ⚠️ (Exceeds constraint) |
| Max Drawdown | -30.67% |
| Sharpe Ratio | 0.290 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 5.60% | 6.57% | +0.98% | ✓ |
| Annual Volatility | 5.48% | 22.70% | +17.22% | ⚠️ BREACH |
| Sharpe Ratio | 1.022 | 0.290 | -0.733 | ⚠️ |
| Max Drawdown | 0.00% | -30.67% | -30.67% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (22.70%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +314.5% relative to backtest period.

This demonstrates that **historical constraints do NOT guarantee future compliance**.
Market regime changes can significantly alter risk characteristics.


## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16488291 | 0.607 | No | No |
| -20% | ¥14656258 | 0.682 | No | No |
| -30% | ¥12824226 | 0.780 | Yes | No |
| -40% | ¥10992194 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 61 days
- First breach: 2016-05-31
- Last breach: 2016-08-25
- Max ratio: 0.812

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2016-05-31 | 0.765 |
| 2016-06-01 | 0.763 |
| 2016-06-02 | 0.767 |
| 2016-06-03 | 0.764 |
| 2016-06-06 | 0.766 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2016-08-19 | 0.785 |
| 2016-08-22 | 0.790 |
| 2016-08-23 | 0.789 |
| 2016-08-24 | 0.787 |
| 2016-08-25 | 0.787 |
