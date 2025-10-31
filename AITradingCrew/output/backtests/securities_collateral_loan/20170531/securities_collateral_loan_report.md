# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18324056
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.04% drop from current value
- Buffer to forced liquidation: 35.80% drop from current value
- Historical max drawdown (portfolio): -10.01%

## Optimization Summary
- Total ETFs evaluated: 62
- ETFs with sufficient data: 46
- Candidate universe after correlation filter: 27 (threshold 0.90)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1397.T(ＳＭＤＡＭ　日経２２５上場投信), 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1629.T(ＮＥＸＴ　ＦＵＮＤＳ　商社・卸), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1596.T(ＮＺＡＭ　上場投信　ＴＯＰＩＸ), 1671.T(ＷＴＩ原油価格連動型上場投信), 1586.T(上場インデックスファンドＴＯＰ)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 4.72%, volatility 11.12%, Sharpe 0.425, expense 0.22%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2014-06-02 to 2017-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 4.72% | - | - |
| Annual Volatility | 11.12% | ≤ 15% | ✅ |
| Sharpe Ratio | 0.425 | - | - |
| Weighted Expense Ratio | 0.22% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 4.72% | 11.12% | 0.425 | 0.22% | Yes |
| low_volatility | 3.65% | 9.55% | 0.382 | 0.23% |  |
| cost_focus | 6.25% | 13.20% | 0.473 | 0.26% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし） | 10.82% | 23.39% | 0.463 | 0.20% | 1.979 |
| 2 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－ | 11.08% | 24.00% | 0.462 | 0.32% | 1.923 |
| 3 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 10.78% | 24.36% | 0.442 | 0.32% | 1.816 |
| 4 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（ | 7.50% | 20.39% | 0.368 | 0.30% | 1.804 |
| 5 | 1681.T | 上場インデックスファンド海外新興国株式（ＭＳＣＩエマージング | 7.14% | 20.79% | 0.343 | 0.24% | 1.651 |
| 6 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 7.76% | 21.75% | 0.357 | 0.32% | 1.640 |
| 7 | 1399.T | 上場インデックスファンドＭＳＣＩ日本株高配当低ボラティリティ | 8.42% | 24.46% | 0.344 | 0.35% | 1.407 |
| 8 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1.20% | 9.53% | 0.126 | N/A | 1.320 |
| 9 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | 5.96% | 22.37% | 0.267 | 0.32% | 1.192 |
| 10 | 1478.T | ｉシェアーズ　ＭＳＣＩ　ジャパン高配当利回り　ＥＴＦ | 5.09% | 21.57% | 0.236 | 0.19% | 1.093 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内株式 | 3 | ¥6,673,199 | 36.4% |
| コモディティ | 1 | ¥5,908,305 | 32.2% |
| その他 | 2 | ¥5,742,552 | 31.3% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1599 | ¥3695.00 | ¥5908305 | 32.2% | N/A | 1.20% | 9.53% | 0.126 |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 709 | ¥6550.00 | ¥4643950 | 25.3% | 0.20% | 10.82% | 23.39% | 0.463 |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 1309 | ¥1853.00 | ¥2425577 | 13.2% | 0.15% | 0.69% | 15.12% | 0.045 |
| 1399.T | 上場インデックスファンドＭＳＣＩ日本株高配当低ボラティリティ | 1464 | ¥1588.00 | ¥2324832 | 12.7% | 0.35% | 8.42% | 24.46% | 0.344 |
| 1398.T | ＳＭＤＡＭ　東証ＲＥＩＴ指数上場投信 | 1070 | ¥1797.00 | ¥1922790 | 10.5% | 0.22% | 3.16% | 22.92% | 0.138 |
| 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | 694 | ¥1583.00 | ¥1098602 | 6.0% | 0.04% | 1.71% | 23.36% | 0.073 |

*Total: 6 ETFs, Portfolio value: ¥18,324,056*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2014 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 10.01% | 11.11% | 0.901 |
| 2014 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 21.99% | 11.80% | 1.863 |
| 2014 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 36.09% | 19.50% | 1.851 |
| 2015 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -6.37% | 10.90% | -0.584 |
| 2015 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -7.94% | 16.91% | -0.470 |
| 2015 | 1398.T | ＳＭＤＡＭ　東証ＲＥＩＴ指数上場投信 | -4.93% | 25.85% | -0.191 |
| 2015 | 1399.T | 上場インデックスファンドＭＳＣＩ日本株高配当低ボラティリティ | -1.64% | 25.48% | -0.064 |
| 2015 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | 5.81% | 22.77% | 0.255 |
| 2015 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 8.94% | 23.38% | 0.382 |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.00% | 10.82% | 0.000 |
| 2016 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 6.15% | 17.55% | 0.350 |
| 2016 | 1398.T | ＳＭＤＡＭ　東証ＲＥＩＴ指数上場投信 | 6.26% | 24.34% | 0.257 |
| 2016 | 1399.T | 上場インデックスファンドＭＳＣＩ日本株高配当低ボラティリティ | 2.91% | 26.97% | 0.108 |
| 2016 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | -1.92% | 26.96% | -0.071 |
| 2016 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 1.05% | 26.34% | 0.040 |
| 2017 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 2.64% | 4.43% | 0.596 |
| 2017 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -5.84% | 7.98% | -0.732 |
| 2017 | 1398.T | ＳＭＤＡＭ　東証ＲＥＩＴ指数上場投信 | -4.01% | 20.14% | -0.199 |
| 2017 | 1399.T | 上場インデックスファンドＭＳＣＩ日本株高配当低ボラティリティ | 6.94% | 16.82% | 0.412 |
| 2017 | 1473.T | Ｏｎｅ　ＥＴＦ　トピックス | 3.41% | 12.47% | 0.274 |
| 2017 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.13% | 15.06% | 0.872 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2014 | 19.29% | 8.88% | 2.173 |
| 2015 | 38.46% | 26.02% | 1.478 |
| 2016 | 2.02% | 11.61% | 0.174 |
| 2017 | 3.66% | 6.26% | 0.585 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2017-06-01 to 2018-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 6.44% |
| Annualized Return | 6.24% |
| Annualized Volatility | 6.99% |
| Max Drawdown | -6.80% |
| Sharpe Ratio | 0.892 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 4.72% | 6.24% | +1.51% | ✓ |
| Annual Volatility | 11.12% | 6.99% | -4.12% | ✓ |
| Sharpe Ratio | 0.425 | 0.892 | +0.467 | ✓ |
| Max Drawdown | 0.00% | -6.80% | -6.80% | ✓ |

### ⚠️ Forward-Looking Bias Warning

Forward volatility changed by -37.1% relative to backtest period.

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
| -10% | ¥16491650 | 0.606 | No | No |
| -20% | ¥14659245 | 0.682 | No | No |
| -30% | ¥12826839 | 0.780 | Yes | No |
| -40% | ¥10994434 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 208 days
- First breach: 2014-06-02
- Last breach: 2015-09-02
- Max ratio: 0.953

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2014-06-02 | 0.953 |
| 2014-06-03 | 0.948 |
| 2014-06-04 | 0.950 |
| 2014-06-05 | 0.951 |
| 2014-06-06 | 0.947 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2015-08-27 | 0.730 |
| 2015-08-28 | 0.718 |
| 2015-08-31 | 0.719 |
| 2015-09-01 | 0.728 |
| 2015-09-02 | 0.737 |

### Forced Liquidation Summary (>= 85%)
- Total events: 115 days
