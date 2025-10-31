# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18323288
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.04% drop from current value
- Buffer to forced liquidation: 35.79% drop from current value
- Historical max drawdown (portfolio): -10.33%

## Optimization Summary
- Total ETFs evaluated: 40
- ETFs with sufficient data: 24
- Candidate universe after correlation filter: 17 (threshold 0.90)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 1699.T(ＮＥＸＴ　ＦＵＮＤＳ　ＮＯＭＵ), 1618.T(ＮＥＸＴ　ＦＵＮＤＳ　エネルギ), 1624.T(ＮＥＸＴ　ＦＵＮＤＳ　機械（Ｔ), 1632.T(ＮＥＸＴ　ＦＵＮＤＳ　金融（除), 1622.T(ＮＥＸＴ　ＦＵＮＤＳ　自動車・), 1629.T(ＮＥＸＴ　ＦＵＮＤＳ　商社・卸), 1623.T(ＮＥＸＴ　ＦＵＮＤＳ　鉄鋼・非), 1627.T(ＮＥＸＴ　ＦＵＮＤＳ　電力・ガ), 1615.T(ＮＥＸＴ　ＦＵＮＤＳ　東証銀行), 1633.T(ＮＥＸＴ　ＦＵＮＤＳ　不動産（), 1671.T(ＷＴＩ原油価格連動型上場投信)
- Excluded deep-drawdown ETFs (drawdown worse than -30.0%): 1625.T(ＮＥＸＴ　ＦＵＮＤＳ　電機・精), 1343.T(ＮＥＸＴ　ＦＵＮＤＳ　東証ＲＥ), 1311.T(ＮＥＸＴ　ＦＵＮＤＳ　ＴＯＰＩ), 1550.T(ＭＡＸＩＳ　海外株式（ＭＳＣＩ), 1681.T(上場インデックスファンド海外新)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return 5.73%, volatility 11.99%, Sharpe 0.478, expense 0.30%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2009-06-01 to 2012-05-31 (3.0 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | 5.73% | - | - |
| Annual Volatility | 11.99% | ≤ 15% | ✅ |
| Sharpe Ratio | 0.478 | - | - |
| Weighted Expense Ratio | 0.30% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | 5.73% | 11.99% | 0.478 | 0.30% | Yes |
| low_volatility | 9.62% | 14.95% | 0.643 | 0.24% |  |
| cost_focus | 5.45% | 13.14% | 0.415 | 0.28% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 8.66% | 20.73% | 0.418 | N/A | 2.015 |
| 2 | 1545.T | ＮＥＸＴ　ＦＵＮＤＳ　ＮＡＳＤＡＱ－１００（為替ヘッジなし） | 11.34% | 24.54% | 0.462 | 0.20% | 1.882 |
| 3 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 5.46% | 17.92% | 0.305 | 0.32% | 1.700 |
| 4 | 1547.T | 上場インデックスファンド米国株式（Ｓ＆Ｐ５００） | 7.37% | 22.59% | 0.326 | 0.15% | 1.445 |
| 5 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 6.53% | 21.67% | 0.301 | 0.32% | 1.390 |
| 6 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（ | 6.30% | 21.89% | 0.288 | 0.30% | 1.316 |
| 7 | 1680.T | 上場インデックスファンド海外先進国株式（ＭＳＣＩ－ＫＯＫＵＳ | -1.86% | 21.13% | -0.088 | 0.24% | -0.416 |
| 8 | 1619.T | ＮＥＸＴ　ＦＵＮＤＳ　建設・資材（ＴＯＰＩＸ－１７）上場投信 | -5.05% | 20.93% | -0.241 | 0.32% | -1.153 |
| 9 | 1631.T | ＮＥＸＴ　ＦＵＮＤＳ　銀行（ＴＯＰＩＸ－１７）上場投信 | -8.29% | 24.52% | -0.338 | 0.32% | -1.379 |
| 10 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配 | -4.17% | 16.12% | -0.259 | 0.30% | -1.606 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 国内セクター | 3 | ¥8,369,920 | 45.7% |
| コモディティ | 1 | ¥6,040,800 | 33.0% |
| 海外株式 | 1 | ¥2,077,460 | 11.3% |
| REIT | 1 | ¥1,835,108 | 10.0% |

### Top Holdings (out of 6 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 1678 | ¥3600.00 | ¥6040800 | 33.0% | N/A | 8.66% | 20.73% | 0.418 |
| 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 472 | ¥9520.00 | ¥4493440 | 24.5% | 0.32% | -4.94% | 13.26% | -0.373 |
| 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 177 | ¥13760.00 | ¥2435520 | 13.3% | 0.32% | 5.46% | 17.92% | 0.305 |
| 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 209 | ¥9940.00 | ¥2077460 | 11.3% | 0.30% | 6.30% | 21.89% | 0.288 |
| 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 1969 | ¥932.00 | ¥1835108 | 10.0% | 0.30% | -4.17% | 16.12% | -0.259 |
| 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 158 | ¥9120.00 | ¥1440960 | 7.9% | 0.32% | 6.53% | 21.67% | 0.301 |

*Total: 6 ETFs, Portfolio value: ¥18,323,288*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2009 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 4.72% | 19.38% | 0.244 |
| 2009 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 0.56% | 20.24% | 0.028 |
| 2009 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 13.27% | 17.03% | 0.779 |
| 2009 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | 0.46% | 14.65% | 0.031 |
| 2009 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 0.69% | 18.11% | 0.038 |
| 2010 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 11.35% | 16.22% | 0.700 |
| 2010 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 26.19% | 13.30% | 1.970 |
| 2010 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 7.01% | 16.18% | 0.433 |
| 2010 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | -11.30% | 17.14% | -0.659 |
| 2010 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -5.03% | 14.46% | -0.348 |
| 2010 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | -1.25% | 16.89% | -0.074 |
| 2011 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | 8.55% | 23.14% | 0.369 |
| 2011 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | -25.15% | 16.61% | -1.514 |
| 2011 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 0.21% | 24.51% | 0.009 |
| 2011 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 0.77% | 20.05% | 0.039 |
| 2011 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -7.13% | 14.37% | -0.496 |
| 2011 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 1.15% | 25.62% | 0.045 |
| 2012 | 1328.T | ＮＥＸＴ　ＦＵＮＤＳ　金価格連動型上場投信 | -0.55% | 16.54% | -0.033 |
| 2012 | 1345.T | 上場インデックスファンドＪリート（東証ＲＥＩＴ指数）隔月分配型 | 9.52% | 14.06% | 0.677 |
| 2012 | 1546.T | ＮＥＸＴ　ＦＵＮＤＳ　ダウ・ジョーンズ工業株３０種平均株価（為替ヘッジなし）連動 | 4.52% | 16.00% | 0.283 |
| 2012 | 1617.T | ＮＥＸＴ　ＦＵＮＤＳ　食品（ＴＯＰＩＸ－１７）上場投信 | 5.44% | 13.29% | 0.409 |
| 2012 | 1621.T | ＮＥＸＴ　ＦＵＮＤＳ　医薬品（ＴＯＰＩＸ－１７）上場投信 | -1.24% | 11.49% | -0.108 |
| 2012 | 1630.T | ＮＥＸＴ　ＦＵＮＤＳ　小売（ＴＯＰＩＸ－１７）上場投信 | 4.11% | 10.76% | 0.382 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2009 | 3.73% | 11.59% | 0.321 |
| 2010 | 15.38% | 16.19% | 0.950 |
| 2011 | -2.16% | 13.48% | -0.160 |
| 2012 | 1.90% | 10.10% | 0.188 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2012-06-01 to 2013-05-31 (1.0 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 36.52% |
| Annualized Return | 37.74% |
| Annualized Volatility | 12.37% |
| Max Drawdown | -6.34% |
| Sharpe Ratio | 3.051 |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | 5.73% | 37.74% | +32.01% | ⚠️ |
| Annual Volatility | 11.99% | 12.37% | +0.39% | ✓ |
| Sharpe Ratio | 0.478 | 3.051 | +2.573 | ✓ |
| Max Drawdown | 0.00% | -6.34% | -6.34% | ✓ |


## Interest Projection
| Days | Interest (¥) |
| --- | --- |
| 30 | ¥15410.96 |
| 90 | ¥46232.88 |
| 180 | ¥92465.75 |

## Stress Scenarios
| Scenario | Post Value (¥) | Loan Ratio | Margin Call? | Liquidation? |
| --- | --- | --- | --- | --- |
| -10% | ¥16490959 | 0.606 | No | No |
| -20% | ¥14658630 | 0.682 | No | No |
| -30% | ¥12826302 | 0.780 | Yes | No |
| -40% | ¥10993973 | 0.910 | Yes | Yes |
