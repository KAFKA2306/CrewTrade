# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18313633
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.99% drop from current value
- Buffer to forced liquidation: 35.76% drop from current value
- Historical max drawdown (portfolio): -13.11%

## Optimization Summary
- Total ETFs evaluated: 51
- ETFs with sufficient data: 34
- Candidate universe after correlation filter: 19 (threshold 0.90)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1671.T(ＷＴＩ原油価格連動型上場投信), 1586.T(上場インデックスファンドＴＯＰ), 1578.T(上場インデックスファンド日経２)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1629.T(ＮＥＸＴ　ＦＵＮＤＳ　商社・卸), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1311.T(ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩ), 1681.T(上場インデックスファンド海外新)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 8.98%, volatility 10.69%, Sharpe 0.841, expense 0.23%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2013-05-31 to 2016-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 8.98% | - | - |
| Annual Volatility | 10.69% | ≤ 15% | ✅ |
| Sharpe Ratio | 0.841 | - | - |
| Weighted Expense Ratio | 0.23% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 8.98% | 10.69% | 0.841 | 0.23% | Yes |
| low_volatility | 12.17% | 12.81% | 0.950 | 0.25% |  |
| cost_focus | 10.09% | 11.71% | 0.862 | 0.23% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 13.33% | 15.05% | 0.886 | 0.14% | 5.885 |
| 2 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配 | 13.44% | 16.20% | 0.830 | 0.30% | 5.122 |
| 3 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 13.46% | 16.57% | 0.813 | 0.15% | 4.906 |
| 4 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 21.78% | 21.19% | 1.028 | 0.32% | 4.849 |
| 5 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 18.48% | 22.88% | 0.808 | 0.32% | 3.530 |
| 6 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 15.60% | 21.03% | 0.742 | 0.32% | 3.528 |
| 7 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 15.65% | 21.35% | 0.733 | 0.32% | 3.435 |
| 8 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００ | 12.33% | 19.08% | 0.646 | 0.28% | 3.384 |
| 9 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 11.80% | 18.76% | 0.629 | 0.15% | 3.355 |
| 10 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 16.33% | 22.44% | 0.728 | 0.32% | 3.243 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| コモディティ | 1 | ¥5,850,750 | 31.9% |
| 海外株式 | 2 | ¥3,855,898 | 21.1% |
| 国内株式 | 1 | ¥3,697,605 | 20.2% |
| 国内セクター | 1 | ¥2,984,100 | 16.3% |
| REIT | 1 | ¥1,925,280 | 10.5% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1614 | ¥3625.00 | ¥5850750 | 31.9% | N/A | 0.25% | 11.30% | 0.022 |
| 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 1941 | ¥1905.00 | ¥3697605 | 20.2% | 0.25% | 14.64% | 22.24% | 0.658 |
| 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 98 | ¥30450.00 | ¥2984100 | 16.3% | 0.32% | 21.78% | 21.19% | 1.028 |
| 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 1150 | ¥1935.00 | ¥2225250 | 12.2% | 0.24% | 6.30% | 16.04% | 0.393 |
| 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 1008 | ¥1910.00 | ¥1925280 | 10.5% | 0.14% | 13.33% | 15.05% | 0.886 |
| 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 643 | ¥2536.00 | ¥1630648 | 8.9% | 0.15% | 11.80% | 18.76% | 0.629 |

*Total: 6 ETFs, Portfolio value: ¥18,313,633*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2013 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -12.81% | 20.37% | -0.629 |
| 2013 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 17.28% | 17.76% | 0.973 |
| 2013 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 3.86% | 19.93% | 0.194 |
| 2013 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 17.04% | 15.81% | 1.078 |
| 2014 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 8.62% | 10.54% | 0.818 |
| 2014 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 30.18% | 16.69% | 1.808 |
| 2014 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 30.03% | 17.09% | 1.757 |
| 2014 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 28.20% | 11.23% | 2.511 |
| 2014 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 13.34% | 17.43% | 0.765 |
| 2014 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | 20.93% | 14.25% | 1.468 |
| 2015 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -6.37% | 10.90% | -0.584 |
| 2015 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -0.69% | 18.76% | -0.037 |
| 2015 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | -8.70% | 22.41% | -0.388 |
| 2015 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | -7.94% | 15.56% | -0.510 |
| 2015 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 25.67% | 19.87% | 1.292 |
| 2015 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | -2.34% | 15.17% | -0.154 |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.69% | 13.55% | 0.051 |
| 2016 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -7.07% | 23.34% | -0.303 |
| 2016 | 1595.T | ＮＺＡＭ　上場投信　東証ＲＥＩＴ指数　　　　　　　　　　　　 | 8.05% | 29.15% | 0.276 |
| 2016 | 1597.T | ＭＡＸＩＳ　Ｊリート上場投信 | 8.40% | 19.31% | 0.435 |
| 2016 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -0.65% | 30.29% | -0.022 |
| 2016 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳＡＩ） | -9.28% | 22.05% | -0.421 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2013 | -2.24% | 14.51% | -0.155 |
| 2014 | 64.81% | 28.53% | 2.271 |
| 2015 | -1.79% | 11.01% | -0.163 |
| 2016 | 0.51% | 12.84% | 0.040 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2016-06-01 to 2017-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 3.45% |
| Annualized Return | 3.55% |
| Annualized Volatility | 7.19% |
| Max Drawdown | -5.48% |
| Sharpe Ratio | 0.494 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 8.98% | 3.55% | -5.44% | ⚠️ |
| Annual Volatility | 10.69% | 7.19% | -3.50% | ✓ |
| Sharpe Ratio | 0.841 | 0.494 | -0.347 | ✓ |
| Max Drawdown | 0.00% | -5.48% | -5.48% | ✓ |

### ⚠️ Forward-Looking Bias Warning

Forward volatility changed by -32.7% relative to backtest period.

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
| -10% | ¥16482270 | 0.607 | No | No |
| -20% | ¥14650906 | 0.683 | No | No |
| -30% | ¥12819543 | 0.780 | Yes | No |
| -40% | ¥10988180 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 186 days
- First breach: 2013-05-31
- Last breach: 2014-03-04
- Max ratio: 0.970

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2013-05-31 | 0.868 |
| 2013-06-03 | 0.886 |
| 2013-06-04 | 0.882 |
| 2013-06-05 | 0.888 |
| 2013-06-06 | 0.895 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2014-02-26 | 0.775 |
| 2014-02-27 | 0.777 |
| 2014-02-28 | 0.778 |
| 2014-03-03 | 0.782 |
| 2014-03-04 | 0.780 |

### Forced Liquidation Summary (>= 85%)
- Total events: 178 days
