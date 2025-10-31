# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18321382
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.03% drop from current value
- Buffer to forced liquidation: 35.79% drop from current value
- Historical max drawdown (portfolio): -11.33%

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 25
- Candidate universe after correlation filter: 18 (threshold 0.90)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1629.T(ＮＥＸＴ　ＦＵＮＤＳ　商社・卸), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1311.T(ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩ), 1550.T(ＭＡＸＩＳ　海外株式（ＭＳＣＩ), 1681.T(上場インデックスファンド海外新)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 16.29%, volatility 13.75%, Sharpe 1.185, expense 0.24%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2010-05-31 to 2013-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 16.29% | - | - |
| Annual Volatility | 13.75% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.185 | - | - |
| Weighted Expense Ratio | 0.24% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 16.29% | 13.75% | 1.185 | 0.24% | Yes |
| low_volatility | 16.32% | 13.75% | 1.187 | 0.23% |  |
| cost_focus | 14.33% | 12.82% | 1.118 | 0.27% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 21.20% | 18.20% | 1.165 | 0.32% | 6.399 |
| 2 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 13.30% | 15.63% | 0.851 | 0.32% | 5.448 |
| 3 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 23.83% | 21.75% | 1.096 | 0.15% | 5.039 |
| 4 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（ | 21.26% | 21.18% | 1.004 | 0.30% | 4.738 |
| 5 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳ | 18.32% | 20.03% | 0.915 | 0.24% | 4.566 |
| 6 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 19.29% | 20.58% | 0.938 | 0.32% | 4.557 |
| 7 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし） | 24.70% | 23.57% | 1.048 | 0.20% | 4.445 |
| 8 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 11.99% | 18.48% | 0.649 | 0.32% | 3.511 |
| 9 | 1554.T | 上場インデックスファンド世界株式（ＭＳＣＩ　ＡＣＷＩ）除く日 | 16.75% | 21.87% | 0.766 | 0.24% | 3.502 |
| 10 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－ | 12.02% | 18.57% | 0.647 | 0.32% | 3.485 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 3 | ¥6,367,880 | 34.8% |
| 海外株式 | 1 | ¥3,711,600 | 20.3% |
| コモディティ | 1 | ¥3,698,660 | 20.2% |
| 国内株式 | 1 | ¥2,335,392 | 12.7% |
| その他 | 1 | ¥2,207,850 | 12.1% |

### Top Holdings (out of 7 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 2062 | ¥1800.00 | ¥3711600 | 20.3% | 0.15% | 23.83% | 21.75% | 1.096 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 911 | ¥4060.00 | ¥3698660 | 20.2% | N/A | 9.99% | 20.41% | 0.490 |
| 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 233 | ¥13750.00 | ¥3203750 | 17.5% | 0.32% | 13.30% | 15.63% | 0.851 |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 1632 | ¥1431.00 | ¥2335392 | 12.7% | 0.15% | 12.52% | 20.98% | 0.597 |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 718 | ¥3075.00 | ¥2207850 | 12.1% | 0.20% | 24.70% | 23.57% | 1.048 |
| 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 172 | ¥11540.00 | ¥1984880 | 10.8% | 0.32% | 12.02% | 18.57% | 0.647 |
| 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 89 | ¥13250.00 | ¥1179250 | 6.4% | 0.32% | 19.29% | 20.58% | 0.938 |

*Total: 7 ETFs, Portfolio value: ¥18,321,382*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2010 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.91% | 14.45% | 0.063 |
| 2010 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 23.89% | 15.47% | 1.545 |
| 2010 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 15.47% | 17.80% | 0.869 |
| 2010 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 9.10% | 16.79% | 0.542 |
| 2010 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 0.78% | 14.27% | 0.054 |
| 2010 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | -1.34% | 14.97% | -0.090 |
| 2010 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | -4.08% | 16.64% | -0.245 |
| 2011 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 8.55% | 23.14% | 0.369 |
| 2011 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -25.49% | 18.05% | -1.412 |
| 2011 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | -2.42% | 26.94% | -0.090 |
| 2011 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | -4.77% | 24.85% | -0.192 |
| 2011 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -7.13% | 14.37% | -0.496 |
| 2011 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | -11.74% | 21.20% | -0.554 |
| 2011 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 1.15% | 25.62% | 0.045 |
| 2012 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 14.78% | 15.30% | 0.966 |
| 2012 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 34.66% | 12.46% | 2.782 |
| 2012 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 28.81% | 19.15% | 1.505 |
| 2012 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 29.74% | 16.73% | 1.777 |
| 2012 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 12.34% | 12.59% | 0.980 |
| 2012 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 7.95% | 13.05% | 0.609 |
| 2012 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 10.62% | 10.85% | 0.979 |
| 2013 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -2.29% | 21.77% | -0.105 |
| 2013 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 21.17% | 36.27% | 0.584 |
| 2013 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 34.34% | 22.75% | 1.509 |
| 2013 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 33.53% | 22.39% | 1.498 |
| 2013 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 26.96% | 21.71% | 1.242 |
| 2013 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 39.37% | 20.61% | 1.910 |
| 2013 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 36.74% | 21.86% | 1.680 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2010 | 42.25% | 33.01% | 1.280 |
| 2011 | -5.36% | 14.26% | -0.376 |
| 2012 | 19.64% | 10.04% | 1.955 |
| 2013 | 22.59% | 17.06% | 1.324 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2013-06-03 to 2014-05-30 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 11.94% |
| Annualized Return | 12.41% |
| Annualized Volatility | 13.01% |
| Max Drawdown | -6.70% |
| Sharpe Ratio | 0.954 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 16.29% | 12.41% | -3.88% | ✓ |
| Annual Volatility | 13.75% | 13.01% | -0.74% | ✓ |
| Sharpe Ratio | 1.185 | 0.954 | -0.231 | ✓ |
| Max Drawdown | 0.00% | -6.70% | -6.70% | ✓ |


## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16489244 | 0.607 | No | No |
| -20% | ¥14657106 | 0.682 | No | No |
| -30% | ¥12824967 | 0.780 | Yes | No |
| -40% | ¥10992829 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 605 days
- First breach: 2010-05-31
- Last breach: 2012-11-20
- Max ratio: 1.146

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2010-05-31 | 1.078 |
| 2010-06-01 | 1.077 |
| 2010-06-02 | 1.080 |
| 2010-06-03 | 1.072 |
| 2010-06-04 | 1.080 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2012-11-14 | 0.716 |
| 2012-11-15 | 0.712 |
| 2012-11-16 | 0.715 |
| 2012-11-19 | 0.707 |
| 2012-11-20 | 0.702 |

### Forced Liquidation Summary (>= 85%)
- Total events: 97 days
