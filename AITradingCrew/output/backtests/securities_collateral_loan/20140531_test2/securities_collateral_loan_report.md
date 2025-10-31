# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18305292
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.96% drop from current value
- Buffer to forced liquidation: 35.73% drop from current value
- Historical max drawdown (portfolio): -13.69%

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 27
- Candidate universe after correlation filter: 19 (threshold 0.90)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1329.T(ｉシェアーズ・コア　日経２２５), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1681.T(上場インデックスファンド海外新)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 17.28%, volatility 13.49%, Sharpe 1.280, expense 0.26%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2011-05-31 to 2014-05-30 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 17.28% | - | - |
| Annual Volatility | 13.49% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.280 | - | - |
| Weighted Expense Ratio | 0.26% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 17.28% | 13.49% | 1.280 | 0.26% | Yes |
| low_volatility | 14.71% | 12.32% | 1.194 | 0.24% |  |
| cost_focus | 16.01% | 12.97% | 1.235 | 0.27% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 19.18% | 16.79% | 1.142 | 0.32% | 6.801 |
| 2 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 19.08% | 17.49% | 1.091 | 0.32% | 6.236 |
| 3 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 23.10% | 20.51% | 1.126 | 0.15% | 5.490 |
| 4 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳ | 18.24% | 18.79% | 0.971 | 0.24% | 5.168 |
| 5 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし） | 26.14% | 22.60% | 1.157 | 0.20% | 5.118 |
| 6 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 13.51% | 16.25% | 0.831 | 0.32% | 5.114 |
| 7 | 1628.T | ＮＥＸＴ　ＦＵＮＤＳ　運輸・物流（ＴＯＰＩＸ－１７）上場投信 | 15.79% | 17.63% | 0.896 | 0.32% | 5.082 |
| 8 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－ | 17.39% | 18.78% | 0.926 | 0.32% | 4.932 |
| 9 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 17.76% | 19.44% | 0.914 | 0.15% | 4.703 |
| 10 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（ | 18.14% | 19.95% | 0.909 | 0.30% | 4.557 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 2 | ¥8,726,401 | 47.7% |
| その他 | 1 | ¥3,383,600 | 18.5% |
| 国内株式 | 2 | ¥3,238,367 | 17.7% |
| コモディティ | 1 | ¥1,926,220 | 10.5% |
| 海外株式 | 1 | ¥1,030,704 | 5.6% |

### Top Holdings (out of 7 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 266 | ¥21923.80 | ¥5831731 | 31.9% | 0.32% | 19.18% | 16.79% | 1.142 |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 880 | ¥3845.00 | ¥3383600 | 18.5% | 0.20% | 26.14% | 22.60% | 1.157 |
| 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 213 | ¥13590.00 | ¥2894670 | 15.8% | 0.32% | 17.39% | 18.78% | 0.926 |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 1309 | ¥1643.00 | ¥2150687 | 11.7% | 0.15% | 15.29% | 19.38% | 0.789 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 548 | ¥3515.00 | ¥1926220 | 10.5% | N/A | 0.56% | 19.37% | 0.029 |
| 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００） | 824 | ¥1320.00 | ¥1087680 | 5.9% | 0.28% | 12.27% | 16.92% | 0.725 |
| 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 591 | ¥1744.00 | ¥1030704 | 5.6% | 0.15% | 17.76% | 19.44% | 0.914 |

*Total: 7 ETFs, Portfolio value: ¥18,305,292*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2011 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -0.96% | 26.57% | -0.036 |
| 2011 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -20.92% | 14.15% | -1.478 |
| 2011 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | -7.83% | 30.53% | -0.257 |
| 2011 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | -18.34% | 28.08% | -0.653 |
| 2011 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 0.15% | 15.00% | 0.010 |
| 2011 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | -10.81% | 16.38% | -0.660 |
| 2011 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００） | -11.65% | 14.15% | -0.824 |
| 2012 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 14.78% | 15.30% | 0.966 |
| 2012 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 34.66% | 12.46% | 2.782 |
| 2012 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 28.81% | 19.15% | 1.505 |
| 2012 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 27.26% | 16.28% | 1.674 |
| 2012 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 18.77% | 13.84% | 1.357 |
| 2012 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 7.95% | 13.05% | 0.609 |
| 2012 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００） | 14.02% | 13.18% | 1.063 |
| 2013 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -14.80% | 20.92% | -0.708 |
| 2013 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 36.83% | 28.27% | 1.303 |
| 2013 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 66.67% | 20.71% | 3.219 |
| 2013 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 52.06% | 17.92% | 2.906 |
| 2013 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 38.84% | 20.19% | 1.924 |
| 2013 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 76.33% | 23.31% | 3.274 |
| 2013 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００） | 39.67% | 21.08% | 1.882 |
| 2014 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -0.71% | 9.66% | -0.073 |
| 2014 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 1.67% | 11.12% | 0.150 |
| 2014 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 0.79% | 21.26% | 0.037 |
| 2014 | 1550.T | ＭＡＸＩＳ　海外株式（ＭＳＣＩコクサイ）上場投信 | 0.69% | 13.55% | 0.051 |
| 2014 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 1.88% | 16.90% | 0.111 |
| 2014 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | -6.92% | 20.97% | -0.330 |
| 2014 | 1698.T | 上場インデックスファンド日本高配当（東証配当フォーカス１００） | -2.37% | 17.32% | -0.137 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2011 | -7.23% | 12.95% | -0.558 |
| 2012 | 19.64% | 10.27% | 1.912 |
| 2013 | 39.33% | 15.71% | 2.503 |
| 2014 | -0.43% | 13.06% | -0.033 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2014-06-02 to 2015-05-29 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 31.41% |
| Annualized Return | 32.75% |
| Annualized Volatility | 11.76% |
| Max Drawdown | -7.18% |
| Sharpe Ratio | 2.785 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 17.28% | 32.75% | +15.47% | ⚠️ |
| Annual Volatility | 13.49% | 11.76% | -1.73% | ✓ |
| Sharpe Ratio | 1.280 | 2.785 | +1.505 | ✓ |
| Max Drawdown | 0.00% | -7.18% | -7.18% | ✓ |


## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16474763 | 0.607 | No | No |
| -20% | ¥14644234 | 0.683 | No | No |
| -30% | ¥12813704 | 0.780 | Yes | No |
| -40% | ¥10983175 | 0.910 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 412 days
- First breach: 2011-05-31
- Last breach: 2013-01-29
- Max ratio: 0.916

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2011-05-31 | 0.841 |
| 2011-06-01 | 0.838 |
| 2011-06-02 | 0.849 |
| 2011-06-03 | 0.851 |
| 2011-06-06 | 0.856 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2013-01-23 | 0.724 |
| 2013-01-24 | 0.722 |
| 2013-01-25 | 0.712 |
| 2013-01-28 | 0.706 |
| 2013-01-29 | 0.704 |

### Forced Liquidation Summary (>= 85%)
- Total events: 184 days
