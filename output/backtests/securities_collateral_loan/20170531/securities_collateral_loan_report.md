# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18303676
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.95% drop from current value
- Buffer to forced liquidation: 35.72% drop from current value
- Historical max drawdown (portfolio): -15.81%

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after correlation filter: 18 (threshold 0.90)
- Excluded high-volatility ETFs (> 35.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1329.T(ｉシェアーズ・コア　日経２２５)
- Excluded deep-drawdown ETFs (drawdown worse than -35.0%): 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1671.T(ＷＴＩ原油価格連動型上場投信), 1681.T(上場インデックスファンド海外新)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 19.12%, volatility 14.44%, Sharpe 1.325, expense 0.24%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2012-05-31 to 2017-05-31 (5.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 19.12% | - | - |
| Annual Volatility | 14.44% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.325 | - | - |
| Weighted Expense Ratio | 0.24% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 19.12% | 14.44% | 1.325 | 0.24% | Yes |
| low_volatility | 15.09% | 12.08% | 1.248 | 0.24% |  |
| cost_focus | 17.05% | 13.27% | 1.285 | 0.25% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 12.62% | 21.82% | 0.579 | 0.32% | 0.702 |
| 2 | 1311.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ　Ｃｏｒｅ　３０連動型上場投 | 15.19% | 21.32% | 0.712 | 0.19% | 0.595 |
| 3 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1.45% | 13.53% | 0.107 | N/A | 0.566 |
| 4 | 1306.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ連動型上場投信 | 18.63% | 21.63% | 0.861 | 0.05% | 0.507 |
| 5 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 16.55% | 20.44% | 0.810 | 0.32% | 0.502 |
| 6 | 1346.T | ＭＡＸＩＳ　日経２２５上場投信 | 19.80% | 22.26% | 0.890 | 0.12% | 0.498 |
| 7 | 1320.T | ｉＦｒｅｅＥＴＦ　日経２２５（年１回決算型） | 19.89% | 22.33% | 0.891 | 0.12% | 0.478 |
| 8 | 1308.T | 上場インデックスファンドＴＯＰＩＸ | 18.61% | 21.32% | 0.873 | 0.05% | 0.473 |
| 9 | 1321.T | ＮＥＸＴ　ＦＵＮＤＳ　日経２２５連動型上場投信 | 19.81% | 22.23% | 0.891 | 0.09% | 0.444 |
| 10 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 17.24% | 20.37% | 0.846 | 0.32% | 0.434 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 3 | ¥6,963,935 | 38.0% |
| その他 | 2 | ¥5,897,480 | 32.2% |
| 国内株式 | 1 | ¥5,442,261 | 29.7% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 2937 | ¥1853.00 | ¥5442261 | 29.7% | 0.15% | 14.97% | 18.00% | 0.832 |
| 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | 1652 | ¥1865.00 | ¥3080980 | 16.8% | 0.24% | 17.36% | 17.01% | 1.020 |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 430 | ¥6550.00 | ¥2816500 | 15.4% | 0.20% | 26.65% | 21.79% | 1.223 |
| 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 135 | ¥19990.00 | ¥2698650 | 14.7% | 0.32% | 22.96% | 21.26% | 1.080 |
| 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 67 | ¥33000.00 | ¥2211000 | 12.1% | 0.32% | 19.91% | 19.53% | 1.019 |
| 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 122 | ¥16838.40 | ¥2054285 | 11.2% | 0.32% | 16.55% | 20.44% | 0.810 |

*Total: 6 ETFs, Portfolio value: ¥18,303,676*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2012 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 22.00% | 10.70% | 2.057 |
| 2012 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.65% | 18.71% | 0.730 |
| 2012 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | 24.27% | 14.36% | 1.690 |
| 2012 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 12.65% | 14.25% | 0.887 |
| 2012 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 13.27% | 13.08% | 1.014 |
| 2012 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 12.35% | 11.26% | 1.096 |
| 2013 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 36.83% | 28.27% | 1.303 |
| 2013 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 66.67% | 20.71% | 3.219 |
| 2013 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | 46.73% | 17.97% | 2.601 |
| 2013 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 38.84% | 20.19% | 1.924 |
| 2013 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 76.33% | 23.31% | 3.274 |
| 2013 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 38.21% | 23.32% | 1.638 |
| 2014 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 24.63% | 11.53% | 2.136 |
| 2014 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 37.88% | 20.22% | 1.873 |
| 2014 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | 24.20% | 15.99% | 1.514 |
| 2014 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 13.34% | 17.43% | 0.765 |
| 2014 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 2.81% | 19.46% | 0.144 |
| 2014 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 21.08% | 16.98% | 1.241 |
| 2015 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -7.94% | 16.91% | -0.470 |
| 2015 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 8.94% | 23.38% | 0.382 |
| 2015 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | -7.49% | 15.19% | -0.493 |
| 2015 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 25.67% | 19.87% | 1.292 |
| 2015 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 17.12% | 20.25% | 0.846 |
| 2015 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 14.16% | 21.60% | 0.655 |
| 2016 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 6.15% | 17.55% | 0.350 |
| 2016 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 1.05% | 26.34% | 0.040 |
| 2016 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | -0.89% | 20.99% | -0.042 |
| 2016 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -3.62% | 24.83% | -0.146 |
| 2016 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 2.05% | 27.61% | 0.074 |
| 2016 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -7.26% | 25.00% | -0.291 |
| 2017 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -5.84% | 7.98% | -0.732 |
| 2017 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.13% | 15.06% | 0.872 |
| 2017 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日本 | 4.31% | 13.48% | 0.319 |
| 2017 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 11.71% | 13.12% | 0.893 |
| 2017 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 11.43% | 12.68% | 0.901 |
| 2017 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 1.44% | 15.37% | 0.093 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2012 | 18.15% | 9.22% | 1.968 |
| 2013 | 46.78% | 17.62% | 2.654 |
| 2014 | 21.46% | 12.23% | 1.755 |
| 2015 | 3.11% | 14.58% | 0.213 |
| 2016 | 0.86% | 16.93% | 0.051 |
| 2017 | 3.70% | 7.62% | 0.486 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2017-05-31 to 2018-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 6.69% |
| Annualized Return | 6.69% |
| Annualized Volatility | 8.44% |
| Max Drawdown | -8.57% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 19.12% | 6.69% | -12.43% | ⚠️ |
| Annual Volatility | 14.44% | 8.44% | -6.00% | ✓ |
| Max Drawdown | 0.00% | -8.57% | -8.57% | ✓ |

### ⚠️ Forward-Looking Bias Warning

Forward volatility changed by -41.5% relative to backtest period.

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
| -10% | ¥16473308 | 0.607 | No | No |
| -20% | ¥14642941 | 0.683 | No | No |
| -30% | ¥12812573 | 0.780 | Yes | No |
| -40% | ¥10982206 | 0.911 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 506 days
- First breach: 2012-05-31
- Last breach: 2014-10-17
- Max ratio: 1.275

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2012-05-31 | 1.241 |
| 2012-06-01 | 1.252 |
| 2012-06-04 | 1.275 |
| 2012-06-05 | 1.268 |
| 2012-06-06 | 1.258 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2014-08-07 | 0.701 |
| 2014-08-08 | 0.709 |
| 2014-08-11 | 0.700 |
| 2014-10-16 | 0.705 |
| 2014-10-17 | 0.710 |

### Forced Liquidation Summary (>= 85%)
- Total events: 205 days
