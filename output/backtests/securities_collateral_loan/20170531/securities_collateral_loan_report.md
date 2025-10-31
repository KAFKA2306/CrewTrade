# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18291710
- Current loan ratio: 0.547
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 21.90% drop from current value
- Buffer to forced liquidation: 35.68% drop from current value
- Historical max drawdown (portfolio): -16.24%

## Optimization Summary
- Total ETFs evaluated: 41
- ETFs with sufficient data: 34
- Candidate universe after correlation filter: 23 (threshold 0.90)
- Excluded deep-drawdown ETFs (drawdown worse than -45.0%): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1631.T(ＮＥＸＴ　ＦＵＮＤＳ　銀行（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1329.T(ｉシェアーズ・コア　日経２２５), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Selected profile: max_sharpe

### Portfolio Variants
| Variant | Source Profile | Annual Return | Annual Volatility | Sharpe | Kelly (r/σ²) |
| --- | --- | --- | --- | --- | --- |
| Max Sharpe Portfolio | max_sharpe | 18.15% | 14.07% | 1.290 | 9.174 |
| Minimum-Variance Portfolio | low_volatility | 14.14% | 12.11% | 1.167 | 9.640 |
| Max Kelly Criterion Portfolio | low_volatility | 14.14% | 12.11% | 1.167 | 9.640 |

**Max Sharpe Portfolio Holdings (max_sharpe)**
| Ticker | Weight | Weight (Realized) | Quantity | Price | Name |
| --- | --- | --- | --- | --- | --- |
| 1629.T | 6.85% | 6.83% | 45 | ¥27,750 | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 |
| 1328.T | 17.81% | 17.84% | 883 | ¥3,695 | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 |
| 1343.T | 15.31% | 15.35% | 1515 | ¥1,853 | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 |
| 1620.T | 11.73% | 11.65% | 96 | ¥22,200 | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 |
| 1545.T | 31.66% | 31.73% | 886 | ¥6,550 | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 |
| 1626.T | 16.64% | 16.61% | 152 | ¥19,990 | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 |

**Minimum-Variance Portfolio Holdings (low_volatility)**
| Ticker | Weight | Weight (Realized) | Quantity | Price | Name |
| --- | --- | --- | --- | --- | --- |
| 1328.T | 25.74% | 25.77% | 1277 | ¥3,695 | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 |
| 1681.T | 6.60% | 6.60% | 865 | ¥1,398 | 上場インデックスファンド海外新興国株式（ＭＳＣＩエマージング） |
| 1343.T | 17.10% | 17.12% | 1692 | ¥1,853 | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 |
| 1626.T | 25.27% | 25.22% | 231 | ¥19,990 | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 |
| 1617.T | 9.56% | 9.55% | 53 | ¥33,000 | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 |
| 1698.T | 15.72% | 15.74% | 1628 | ¥1,770 | 上場インデックスファンド日本高配当（東証配当フォーカス１００） |

**Max Kelly Criterion Portfolio Holdings (low_volatility)**
| Ticker | Weight | Weight (Realized) | Quantity | Price | Name |
| --- | --- | --- | --- | --- | --- |
| 1328.T | 25.74% | 25.77% | 1277 | ¥3,695 | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 |
| 1681.T | 6.60% | 6.60% | 865 | ¥1,398 | 上場インデックスファンド海外新興国株式（ＭＳＣＩエマージング） |
| 1343.T | 17.10% | 17.12% | 1692 | ¥1,853 | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 |
| 1626.T | 25.27% | 25.22% | 231 | ¥19,990 | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 |
| 1617.T | 9.56% | 9.55% | 53 | ¥33,000 | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 |
| 1698.T | 15.72% | 15.74% | 1628 | ¥1,770 | 上場インデックスファンド日本高配当（東証配当フォーカス１００） |

### Filter Diagnostics
- Applied Asset Filters: max drawdown ≥ -45.0%

**Removed for deep drawdown**
| Ticker | Name |
| --- | --- |
| 1699.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵＲＡ原油インデックス連動型上場投信 |
| 1631.T | ＮＥＸＴ　ＦＵＮＤＳ　銀行（ＴＯＰＩＸ－１７）上場投信 |
| 1632.T | ＮＥＸＴ　ＦＵＮＤＳ　金融（除く銀行）（ＴＯＰＩＸ－１７）上場投信 |
| 1623.T | ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非鉄（ＴＯＰＩＸ－１７）上場投信 |
| 1615.T | ＮＥＸＴ　ＦＵＮＤＳ　東証銀行業株価指数連動型上場投信 |
| 1329.T | ｉシェアーズ・コア　日経２２５　ＥＴＦ |
| 1671.T | ＷＴＩ原油価格連動型上場投信 |

- Selected portfolio metrics (backtest period): return 18.15%, volatility 14.07%, Sharpe 1.290, expense 0.25%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2012-05-31 to 2017-05-31 (5.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 18.15% | - | - |
| Annual Volatility | 14.07% | ≤ 15% | ✅ |
| Sharpe Ratio | 1.290 | - | - |
| Weighted Expense Ratio | 0.25% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 18.15% | 14.07% | 1.290 | 0.25% | Yes |
| low_volatility | 14.14% | 12.11% | 1.167 | 0.27% |  |
| cost_focus | 18.23% | 14.95% | 1.219 | 0.25% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1618.T | ＮＥＸＴ　ＦＵＮＤＳ　エネルギー資源（ＴＯＰＩＸ－１７）上場 | 4.88% | 26.61% | 0.183 | 0.32% | 0.863 |
| 2 | 1627.T | ＮＥＸＴ　ＦＵＮＤＳ　電力・ガス（ＴＯＰＩＸ－１７）上場投信 | 10.28% | 26.11% | 0.394 | 0.32% | 0.839 |
| 3 | 1633.T | ＮＥＸＴ　ＦＵＮＤＳ　不動産（ＴＯＰＩＸ－１７）上場投信 | 18.86% | 29.72% | 0.635 | 0.32% | 0.800 |
| 4 | 1622.T | ＮＥＸＴ　ＦＵＮＤＳ　自動車・輸送機（ＴＯＰＩＸ－１７）上場 | 16.41% | 25.03% | 0.656 | 0.32% | 0.717 |
| 5 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 12.62% | 21.82% | 0.579 | 0.32% | 0.702 |
| 6 | 1624.T | ＮＥＸＴ　ＦＵＮＤＳ　機械（ＴＯＰＩＸ－１７）上場投信 | 19.17% | 25.18% | 0.761 | 0.32% | 0.698 |
| 7 | 1625.T | ＮＥＸＴ　ＦＵＮＤＳ　電機・精密（ＴＯＰＩＸ－１７）上場投信 | 19.97% | 24.55% | 0.814 | 0.32% | 0.634 |
| 8 | 1311.T | ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩＸ　Ｃｏｒｅ　３０連動型上場投 | 15.19% | 21.32% | 0.712 | 0.19% | 0.595 |
| 9 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1.45% | 13.53% | 0.107 | N/A | 0.566 |
| 10 | 1681.T | 上場インデックスファンド海外新興国株式（ＭＳＣＩエマージング | 11.31% | 18.88% | 0.599 | 0.24% | 0.551 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 3 | ¥6,418,430 | 35.1% |
| その他 | 1 | ¥5,803,300 | 31.7% |
| コモディティ | 1 | ¥3,262,685 | 17.8% |
| 国内株式 | 1 | ¥2,807,295 | 15.3% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 886 | ¥6550.00 | ¥5803300 | 31.7% | 0.20% | 26.65% | 21.79% | 1.223 |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 883 | ¥3695.00 | ¥3262685 | 17.8% | N/A | 1.45% | 13.53% | 0.107 |
| 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 152 | ¥19990.00 | ¥3038480 | 16.6% | 0.32% | 22.96% | 21.26% | 1.080 |
| 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 1515 | ¥1853.00 | ¥2807295 | 15.3% | 0.15% | 14.97% | 18.00% | 0.832 |
| 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 96 | ¥22200.00 | ¥2131200 | 11.7% | 0.32% | 21.12% | 21.54% | 0.980 |
| 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 45 | ¥27750.00 | ¥1248750 | 6.8% | 0.32% | 12.62% | 21.82% | 0.579 |

*Total: 6 ETFs, Portfolio value: ¥18,291,710*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2012 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 15.42% | 14.39% | 1.071 |
| 2012 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 22.00% | 10.70% | 2.057 |
| 2012 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.65% | 18.71% | 0.730 |
| 2012 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 12.68% | 17.96% | 0.706 |
| 2012 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 13.27% | 13.08% | 1.014 |
| 2012 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 8.89% | 18.06% | 0.492 |
| 2013 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -14.80% | 20.92% | -0.708 |
| 2013 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 36.83% | 28.27% | 1.303 |
| 2013 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 66.67% | 20.71% | 3.219 |
| 2013 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 40.54% | 22.73% | 1.784 |
| 2013 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 76.33% | 23.31% | 3.274 |
| 2013 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 29.01% | 21.62% | 1.342 |
| 2014 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 8.62% | 10.54% | 0.818 |
| 2014 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 24.63% | 11.53% | 2.136 |
| 2014 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 37.88% | 20.22% | 1.873 |
| 2014 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 21.90% | 19.01% | 1.152 |
| 2014 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 2.81% | 19.46% | 0.144 |
| 2014 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 8.31% | 18.56% | 0.448 |
| 2015 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -6.37% | 10.90% | -0.584 |
| 2015 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -7.94% | 16.91% | -0.470 |
| 2015 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 8.94% | 23.38% | 0.382 |
| 2015 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 13.49% | 19.95% | 0.676 |
| 2015 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 17.12% | 20.25% | 0.846 |
| 2015 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 0.70% | 21.40% | 0.033 |
| 2016 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 0.00% | 10.82% | 0.000 |
| 2016 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | 6.15% | 17.55% | 0.350 |
| 2016 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 1.05% | 26.34% | 0.040 |
| 2016 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 3.57% | 27.93% | 0.128 |
| 2016 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 2.05% | 27.61% | 0.074 |
| 2016 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 4.72% | 28.66% | 0.165 |
| 2017 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 2.64% | 4.43% | 0.596 |
| 2017 | 1343.T | ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥＩＴ指数連動型上場投信 | -5.84% | 7.98% | -0.732 |
| 2017 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし）連動型上場投信 | 13.13% | 15.06% | 0.872 |
| 2017 | 1620.T | ＮＥＸＴ　ＦＵＮＤＳ　素材・化学（ＴＯＰＩＸ－１７）上場投信 | 9.80% | 14.08% | 0.696 |
| 2017 | 1626.T | ＮＥＸＴ　ＦＵＮＤＳ　情報通信・サービスその他（ＴＯＰＩＸ－１７）上場投信 | 11.43% | 12.68% | 0.901 |
| 2017 | 1629.T | ＮＥＸＴ　ＦＵＮＤＳ　商社・卸売（ＴＯＰＩＸ－１７）上場投信 | 2.51% | 15.97% | 0.157 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2012 | 15.07% | 10.54% | 1.430 |
| 2013 | 29.04% | 15.41% | 1.885 |
| 2014 | 19.13% | 11.38% | 1.681 |
| 2015 | 3.58% | 14.03% | 0.255 |
| 2016 | 2.40% | 15.16% | 0.158 |
| 2017 | 6.49% | 7.65% | 0.849 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2017-05-31 to 2018-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 11.64% |
| Annualized Return | 11.64% |
| Annualized Volatility | 9.47% |
| Max Drawdown | -8.24% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 18.15% | 11.64% | -6.51% | ⚠️ |
| Annual Volatility | 14.07% | 9.47% | -4.59% | ✓ |
| Max Drawdown | 0.00% | -8.24% | -8.24% | ✓ |

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
| -10% | ¥16462539 | 0.607 | No | No |
| -20% | ¥14633368 | 0.683 | No | No |
| -30% | ¥12804197 | 0.781 | Yes | No |
| -40% | ¥10975026 | 0.911 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 559 days
- First breach: 2012-05-31
- Last breach: 2014-10-24
- Max ratio: 1.103

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2012-05-31 | 1.092 |
| 2012-06-01 | 1.102 |
| 2012-06-04 | 1.103 |
| 2012-06-05 | 1.095 |
| 2012-06-06 | 1.083 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2014-10-20 | 0.712 |
| 2014-10-21 | 0.716 |
| 2014-10-22 | 0.704 |
| 2014-10-23 | 0.703 |
| 2014-10-24 | 0.701 |

### Forced Liquidation Summary (>= 85%)
- Total events: 197 days
