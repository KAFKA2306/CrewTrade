# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18292737
- Current loan ratio: 0.547
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.90% drop from current value
- Buffer to forced liquidation: 35.69% drop from current value
- Historical max drawdown (portfolio): -17.75%

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 37
- Candidate universe after correlation filter: 24 (threshold 0.90)
- Excluded high-volatility ETFs (> 35.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1596.T(ＮＺＡＭ　上場投信　ＴＯＰＩＸ), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -35.0%): 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1681.T(上場インデックスファンド海外新)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 10.60%, volatility 13.75%, Sharpe 0.771, expense 0.23%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2014-06-02 to 2019-05-31 (5.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 10.60% | - | - |
| Annual Volatility | 13.75% | ≤ 15% | ✅ |
| Sharpe Ratio | 0.771 | - | - |
| Weighted Expense Ratio | 0.23% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 10.60% | 13.75% | 0.771 | 0.23% | Yes |
| low_volatility | 7.16% | 10.01% | 0.715 | 0.21% |  |
| cost_focus | 8.18% | 11.25% | 0.727 | 0.25% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1586.T | 上場インデックスファンドＴＯＰＩＸ　Ｅｘ－Ｆｉｎａｎｃｉａｌ | 9.76% | 29.73% | 0.328 | 0.09% | 0.729 |
| 2 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | 3.92% | 19.47% | 0.201 | 0.32% | 0.659 |
| 3 | 1311.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ　Ｃｏｒｅ　３０連動型上場投 | 3.61% | 18.75% | 0.192 | 0.19% | 0.631 |
| 4 | 1591.T | ＮＥＸＴ　ＦＵＮＤＳ　ＪＰＸ日経インデックス４００連動型上場 | 5.63% | 18.48% | 0.305 | 0.10% | 0.553 |
| 5 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 7.64% | 20.96% | 0.364 | 0.32% | 0.549 |
| 6 | 1599.T | ｉＦｒｅｅＥＴＦ　ＪＰＸ日経４００ | 5.84% | 18.53% | 0.315 | 0.18% | 0.549 |
| 7 | 1306.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ連動型上場投信 | 6.42% | 18.92% | 0.339 | 0.05% | 0.518 |
| 8 | 1592.T | 上場インデックスファンドＪＰＸ日経インデックス４００ | 5.82% | 18.27% | 0.319 | 0.10% | 0.506 |
| 9 | 1577.T | ＮＥＸＴ　ＦＵＮＤＳ　野村日本株高配当７０連動型上場投信 | 4.91% | 17.94% | 0.274 | 0.32% | 0.502 |
| 10 | 1593.T | ＭＡＸＩＳ　ＪＰＸ日経インデックス４００上場投信 | 5.92% | 18.38% | 0.322 | 0.08% | 0.502 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 2 | ¥5,237,100 | 28.6% |
| その他 | 1 | ¥4,526,960 | 24.7% |
| 海外株式 | 1 | ¥3,980,035 | 21.8% |
| REIT | 2 | ¥3,175,962 | 17.4% |
| コモディティ | 1 | ¥1,372,680 | 7.5% |

### Top Holdings (out of 7 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 568 | ¥7970.00 | ¥4526960 | 24.7% | 0.20% | 17.16% | 22.29% | 0.770 |
| 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 1219 | ¥3265.00 | ¥3980035 | 21.8% | 0.15% | 10.46% | 18.42% | 0.568 |
| 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 171 | ¥22100.00 | ¥3779100 | 20.7% | 0.32% | 11.56% | 20.10% | 0.575 |
| 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 1048 | ¥1962.00 | ¥2056176 | 11.2% | 0.14% | 5.20% | 12.07% | 0.431 |
| 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 81 | ¥18000.00 | ¥1458000 | 8.0% | 0.32% | 8.49% | 19.47% | 0.436 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 372 | ¥3690.00 | ¥1372680 | 7.5% | N/A | 1.51% | 9.08% | 0.167 |
| 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 579 | ¥1934.00 | ¥1119786 | 6.1% | 0.30% | 5.07% | 12.80% | 0.396 |

*Total: 7 ETFs, Portfolio value: ¥18,292,737*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2014 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 10.01% | 11.11% | 0.901 |
| 2014 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 21.88% | 11.77% | 1.858 |
| 2014 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 36.09% | 19.50% | 1.851 |
| 2014 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 29.68% | 16.54% | 1.794 |
| 2014 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 21.68% | 12.51% | 1.733 |
| 2014 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 8.77% | 18.34% | 0.478 |
| 2014 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 20.62% | 15.40% | 1.338 |
| 2015 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -6.37% | 10.90% | -0.584 |
| 2015 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | -7.64% | 16.85% | -0.453 |
| 2015 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 8.94% | 23.38% | 0.382 |
| 2015 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -0.69% | 18.76% | -0.037 |
| 2015 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | -7.94% | 15.56% | -0.510 |
| 2015 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 17.12% | 20.25% | 0.846 |
| 2015 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 14.16% | 21.60% | 0.655 |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.00% | 10.82% | 0.000 |
| 2016 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 5.89% | 16.89% | 0.349 |
| 2016 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 1.05% | 26.34% | 0.040 |
| 2016 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 4.95% | 22.82% | 0.217 |
| 2016 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 5.85% | 15.20% | 0.385 |
| 2016 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 2.05% | 27.61% | 0.074 |
| 2016 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -7.26% | 25.00% | -0.291 |
| 2017 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 6.94% | 5.29% | 1.312 |
| 2017 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | -10.38% | 8.03% | -1.293 |
| 2017 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 26.77% | 14.21% | 1.884 |
| 2017 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 14.00% | 11.33% | 1.236 |
| 2017 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | -9.44% | 7.81% | -1.209 |
| 2017 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 21.24% | 12.40% | 1.713 |
| 2017 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 11.81% | 13.20% | 0.894 |
| 2018 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -5.06% | 6.96% | -0.728 |
| 2018 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 7.76% | 8.66% | 0.896 |
| 2018 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | -3.81% | 25.86% | -0.148 |
| 2018 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -8.70% | 20.99% | -0.414 |
| 2018 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 7.34% | 8.67% | 0.847 |
| 2018 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | -13.10% | 20.22% | -0.648 |
| 2018 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | -10.18% | 19.05% | -0.535 |
| 2019 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.96% | 8.80% | 0.109 |
| 2019 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 7.15% | 9.36% | 0.764 |
| 2019 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 12.89% | 19.08% | 0.675 |
| 2019 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 9.53% | 15.18% | 0.628 |
| 2019 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 8.22% | 8.87% | 0.927 |
| 2019 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 16.93% | 15.24% | 1.111 |
| 2019 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 7.98% | 18.28% | 0.436 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2014 | 22.16% | 12.05% | 1.839 |
| 2015 | 3.59% | 15.02% | 0.239 |
| 2016 | 2.12% | 16.48% | 0.129 |
| 2017 | 12.69% | 7.65% | 1.659 |
| 2018 | -5.77% | 13.73% | -0.420 |
| 2019 | 10.66% | 10.79% | 0.988 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2019-05-31 to 2020-05-29 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 9.65% |
| Annualized Return | 9.68% |
| Annualized Volatility | 21.34% ⚠️ (Exceeds constraint) |
| Max Drawdown | -29.30% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 10.60% | 9.68% | -0.92% | ✓ |
| Annual Volatility | 13.75% | 21.34% | +7.59% | ⚠️ BREACH |
| Max Drawdown | 0.00% | -29.30% | -29.30% | ⚠️ |

### ⚠️ Forward-Looking Bias Warning

**IMPORTANT**: Forward period volatility (21.34%) **EXCEEDED** the backtest constraint (15%).
Forward volatility changed by +55.2% relative to backtest period.

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
| -10% | ¥16463463 | 0.607 | No | No |
| -20% | ¥14634190 | 0.683 | No | No |
| -30% | ¥12804916 | 0.781 | Yes | No |
| -40% | ¥10975642 | 0.911 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 262 days
- First breach: 2014-06-02
- Last breach: 2016-11-15
- Max ratio: 0.830

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2014-06-02 | 0.830 |
| 2014-06-03 | 0.826 |
| 2014-06-04 | 0.825 |
| 2014-06-05 | 0.825 |
| 2014-06-06 | 0.823 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2016-11-09 | 0.734 |
| 2016-11-10 | 0.700 |
| 2016-11-11 | 0.705 |
| 2016-11-14 | 0.701 |
| 2016-11-15 | 0.704 |
