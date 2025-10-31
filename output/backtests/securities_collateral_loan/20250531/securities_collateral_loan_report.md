# Securities Collateral Loan Risk Report

*Generated via automated portfolio optimization*

## Overview
- Loan amount: ¥10,000,000.0
- Annual interest rate: 1.875%
- Collateral period evaluated: 3y
- Current collateral market value: ¥18328405
- Current loan ratio: 0.546
- Max allowable borrowing ratio (Rakuten Securities): 0.60
- Margin call (補充) threshold: 0.70
- Forced liquidation threshold: 0.85
- Buffer to margin call: 22.06% drop from current value
- Buffer to forced liquidation: 35.81% drop from current value
- Historical max drawdown (portfolio): -11.38%

## Optimization Summary
- Total ETFs evaluated: 20
- ETFs with sufficient data: 12
- Candidate universe after correlation filter: 12 (threshold 0.90)
- Excluded hedged ETFs: 179A.T(グローバルＸ　超長期米国債　Ｅ), 183A.T(ＭＡＸＩＳ米国国債２０年超上場), 238A.T(ｉシェアーズ　米国債２５年超　)
- Excluded high-volatility ETFs (> 25.0% annualized volatility): 178A.T(グローバルＸ　革新的優良企業　), 182A.T(ＭＡＸＩＳ米国国債２０年超上場), 200A.T(ＮＥＸＴ　ＦＵＮＤＳ　日経半導), 221A.T(ＭＡＸＩＳ日経半導体株上場投信), 213A.T(上場インデックスファンド日経半)
- Selected profile: max_sharpe
- Selected portfolio metrics (backtest period): return -5.33%, volatility 11.47%, Sharpe -0.464, expense 0.20%

## Part 1: BACKTEST PERIOD ANALYSIS

**Purpose**: Portfolio construction and constraint validation
**Period**: 2024-07-25 to 2025-05-30 (0.8 years)
**Important**: These metrics are based on **historical data** used for optimization.
They do NOT guarantee future performance.

### Backtest Period Metrics
| Metric | Value | Constraint | Status |
| --- | --- | --- | --- |
| Annual Return | -5.33% | - | - |
| Annual Volatility | 11.47% | ≤ 15% | ✅ |
| Sharpe Ratio | -0.464 | - | - |
| Weighted Expense Ratio | 0.20% | < 0.40% | ✅ |


### Profile Metrics
| Profile | Annual Return | Volatility | Sharpe | Expense Ratio | Selected |
| --- | --- | --- | --- | --- | --- |
| max_sharpe | -5.33% | 11.47% | -0.464 | 0.20% | Yes |
| low_volatility | -8.57% | 13.09% | -0.655 | 0.22% |  |
| cost_focus | -6.66% | 11.80% | -0.564 | 0.21% |  |

### Top 10 ETFs by Composite Score
| Rank | Ticker | Name | Return | Volatility | Sharpe | Expense | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 237A.T | ｉシェアーズ　米国債２５年超　ロングデュレーション　ＥＴＦ | -36.06% | 24.17% | -1.492 | 0.14% | 0.870 |
| 2 | 188A.T | グローバルＸ　インド・トップ１０＋　ＥＴＦ | -5.82% | 22.69% | -0.257 | 0.38% | 0.630 |
| 3 | 180A.T | グローバルＸ　超長期米国債　ＥＴＦ | -17.12% | 17.87% | -0.958 | 0.10% | 0.600 |
| 4 | 201A.T | ｉシェアーズ　Ｎｉｆｔｙ　５０　インド株　ＥＴＦ | -4.35% | 21.00% | -0.207 | 0.35% | 0.540 |
| 5 | 236A.T | ｉシェアーズ　日本国債７－１０年　ＥＴＦ | -5.76% | 5.19% | -1.110 | 0.06% | 0.530 |
| 6 | 233A.T | ｉＦｒｅｅＥＴＦ　インドＮｉｆｔｙ５０ | -3.98% | 19.93% | -0.200 | 0.35% | 0.490 |
| 7 | 234A.T | グローバルＸ　ＭＳＣＩ　キャッシュフローキング－日本株式　Ｅ | -0.46% | 21.28% | -0.022 | 0.28% | 0.410 |
| 8 | 159A.T | ＮＥＸＴ　ＦＵＮＤＳ　ＪＰＸプライム１５０指数連動型上場投信 | 5.01% | 23.37% | 0.214 | 0.15% | 0.320 |
| 9 | 181A.T | ＭＡＸＩＳ米国国債１－３年上場投信（為替ヘッジなし） | 2.17% | 18.97% | 0.114 | 0.12% | 0.260 |
| 10 | 210A.T | ｉＦｒｅｅＥＴＦ　日経高利回りＲＥＩＴ指数 | -0.21% | 12.50% | -0.017 | 0.14% | 0.220 |

## Part 2: PORTFOLIO CONSTRUCTION

**Purpose**: Selected ETFs and portfolio composition at anchor date

### Collateral Breakdown
### By Category
| Category | ETF Count | Market Value | Weight |
| --- | --- | --- | --- |
| 上場投信 | 12 | ¥18,328,405 | 100.0% |

### Top Holdings (out of 12 ETFs)
| Ticker | Name | Quantity | Price | Market Value | Weight | Expense | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 201A.T | ｉシェアーズ　Ｎｉｆｔｙ　５０　インド株　ＥＴＦ | 8109 | ¥188.40 | ¥1527736 | 8.3% | 0.35% | -4.35% | 21.00% | -0.207 |
| 237A.T | ｉシェアーズ　米国債２５年超　ロングデュレーション　ＥＴＦ | 9933 | ¥153.80 | ¥1527695 | 8.3% | 0.14% | -36.06% | 24.17% | -1.492 |
| 234A.T | グローバルＸ　ＭＳＣＩ　キャッシュフローキング－日本株式　ＥＴＦ　 | 1520 | ¥1005.00 | ¥1527600 | 8.3% | 0.28% | -0.46% | 21.28% | -0.022 |
| 180A.T | グローバルＸ　超長期米国債　ＥＴＦ | 5732 | ¥266.50 | ¥1527578 | 8.3% | 0.10% | -17.12% | 17.87% | -0.958 |
| 159A.T | ＮＥＸＴ　ＦＵＮＤＳ　ＪＰＸプライム１５０指数連動型上場投信 | 2880 | ¥530.40 | ¥1527552 | 8.3% | 0.15% | 5.01% | 23.37% | 0.214 |
| 181A.T | ＭＡＸＩＳ米国国債１－３年上場投信（為替ヘッジなし） | 3189 | ¥479.00 | ¥1527531 | 8.3% | 0.12% | 2.17% | 18.97% | 0.114 |
| 236A.T | ｉシェアーズ　日本国債７－１０年　ＥＴＦ | 3181 | ¥480.20 | ¥1527516 | 8.3% | 0.06% | -5.76% | 5.19% | -1.110 |
| 235A.T | グローバルＸ　高配当３０－日本株式　ＥＴＦ | 1490 | ¥1025.00 | ¥1527250 | 8.3% | 0.28% | 2.55% | 16.32% | 0.156 |
| 133A.T | グローバルＸ　超短期米国債　ＥＴＦ | 1560 | ¥979.00 | ¥1527240 | 8.3% | 0.10% | 0.09% | 12.63% | 0.007 |
| 233A.T | ｉＦｒｅｅＥＴＦ　インドＮｉｆｔｙ５０ | 780 | ¥1958.00 | ¥1527240 | 8.3% | 0.35% | -3.98% | 19.93% | -0.200 |
| 188A.T | グローバルＸ　インド・トップ１０＋　ＥＴＦ | 1642 | ¥930.00 | ¥1527060 | 8.3% | 0.38% | -5.82% | 22.69% | -0.257 |
| 210A.T | ｉＦｒｅｅＥＴＦ　日経高利回りＲＥＩＴ指数 | 997 | ¥1531.00 | ¥1526407 | 8.3% | 0.14% | -0.21% | 12.50% | -0.017 |

*Total: 12 ETFs, Portfolio value: ¥18,328,405*

### Annual Performance by ETF
| Year | Ticker | Name | Return | Volatility | Sharpe |
| --- | --- | --- | --- | --- | --- |
| 2024 | 133A.T | グローバルＸ　超短期米国債　ＥＴＦ | 3.27% | 15.07% | 0.217 |
| 2024 | 159A.T | ＮＥＸＴ　ＦＵＮＤＳ　ＪＰＸプライム１５０指数連動型上場投信 | 2.99% | 28.26% | 0.106 |
| 2024 | 180A.T | グローバルＸ　超長期米国債　ＥＴＦ | -1.26% | 12.11% | -0.104 |
| 2024 | 181A.T | ＭＡＸＩＳ米国国債１－３年上場投信（為替ヘッジなし） | 4.23% | 23.12% | 0.183 |
| 2024 | 188A.T | グローバルＸ　インド・トップ１０＋　ＥＴＦ | -1.97% | 19.28% | -0.102 |
| 2024 | 201A.T | ｉシェアーズ　Ｎｉｆｔｙ　５０　インド株　ＥＴＦ | -1.43% | 21.01% | -0.068 |
| 2024 | 210A.T | ｉＦｒｅｅＥＴＦ　日経高利回りＲＥＩＴ指数 | -2.21% | 10.09% | -0.219 |
| 2024 | 233A.T | ｉＦｒｅｅＥＴＦ　インドＮｉｆｔｙ５０ | 1.57% | 16.31% | 0.096 |
| 2024 | 234A.T | グローバルＸ　ＭＳＣＩ　キャッシュフローキング－日本株式　ＥＴＦ　 | 2.56% | 15.54% | 0.165 |
| 2024 | 235A.T | グローバルＸ　高配当３０－日本株式　ＥＴＦ | 0.59% | 15.23% | 0.039 |
| 2024 | 236A.T | ｉシェアーズ　日本国債７－１０年　ＥＴＦ | -1.64% | 3.28% | -0.499 |
| 2024 | 237A.T | ｉシェアーズ　米国債２５年超　ロングデュレーション　ＥＴＦ | -9.27% | 17.94% | -0.517 |
| 2025 | 133A.T | グローバルＸ　超短期米国債　ＥＴＦ | -8.93% | 12.60% | -0.709 |
| 2025 | 159A.T | ＮＥＸＴ　ＦＵＮＤＳ　ＪＰＸプライム１５０指数連動型上場投信 | -0.17% | 25.24% | -0.007 |
| 2025 | 180A.T | グローバルＸ　超長期米国債　ＥＴＦ | -10.63% | 22.08% | -0.481 |
| 2025 | 181A.T | ＭＡＸＩＳ米国国債１－３年上場投信（為替ヘッジなし） | -7.92% | 15.19% | -0.521 |
| 2025 | 188A.T | グローバルＸ　インド・トップ１０＋　ＥＴＦ | -6.72% | 27.84% | -0.241 |
| 2025 | 201A.T | ｉシェアーズ　Ｎｉｆｔｙ　５０　インド株　ＥＴＦ | -6.08% | 24.80% | -0.245 |
| 2025 | 210A.T | ｉＦｒｅｅＥＴＦ　日経高利回りＲＥＩＴ指数 | 4.86% | 14.86% | 0.327 |
| 2025 | 233A.T | ｉＦｒｅｅＥＴＦ　インドＮｉｆｔｙ５０ | -5.50% | 22.38% | -0.246 |
| 2025 | 234A.T | グローバルＸ　ＭＳＣＩ　キャッシュフローキング－日本株式　ＥＴＦ　 | -3.46% | 25.20% | -0.137 |
| 2025 | 235A.T | グローバルＸ　高配当３０－日本株式　ＥＴＦ | 0.49% | 17.24% | 0.028 |
| 2025 | 236A.T | ｉシェアーズ　日本国債７－１０年　ＥＴＦ | -2.58% | 6.41% | -0.402 |
| 2025 | 237A.T | ｉシェアーズ　米国債２５年超　ロングデュレーション　ＥＴＦ | -16.86% | 28.54% | -0.591 |

### Annual Portfolio Performance
| Year | Return | Volatility | Sharpe |
| --- | --- | --- | --- |
| 2024 | 72.75% | 57.64% | 1.262 |
| 2025 | -5.61% | 12.64% | -0.444 |

## Part 3: FORWARD PERIOD PERFORMANCE ⭐

**Purpose**: Actual realized risk and return during holding period
**Period**: 2025-06-02 to 2025-10-31 (0.4 years)
**Important**: This is the **ACTUAL PERFORMANCE** after portfolio construction.

### Forward Period Metrics
| Metric | Value |
| --- | --- |
| Cumulative Return | 11.41% |
| Annualized Return | 29.84% |
| Annualized Volatility | 6.66% |
| Max Drawdown | -1.69% |


### Backtest vs Forward Comparison

| Metric | Backtest Period | Forward Period | Difference | Status |
| --- | --- | --- | --- | --- |
| Annual Return | -5.33% | 29.84% | +35.17% | ⚠️ |
| Annual Volatility | 11.47% | 6.66% | -4.82% | ✓ |
| Max Drawdown | 0.00% | -1.69% | -1.69% | ✓ |

### ⚠️ Forward-Looking Bias Warning

Forward volatility changed by -42.0% relative to backtest period.

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
| -10% | ¥16495565 | 0.606 | No | No |
| -20% | ¥14662724 | 0.682 | No | No |
| -30% | ¥12829884 | 0.779 | Yes | No |
| -40% | ¥10997043 | 0.909 | Yes | Yes |

## Historical Breaches
### Margin Call Summary (>= 70%)
- Total events: 19 days
- First breach: 2024-07-25
- Last breach: 2024-08-21
- Max ratio: 0.941

**First 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2024-07-25 | 0.890 |
| 2024-07-26 | 0.875 |
| 2024-07-29 | 0.871 |
| 2024-07-30 | 0.868 |
| 2024-07-31 | 0.868 |

**Last 5 events:**
| Date | Loan Ratio |
| --- | --- |
| 2024-08-15 | 0.904 |
| 2024-08-16 | 0.893 |
| 2024-08-19 | 0.906 |
| 2024-08-20 | 0.785 |
| 2024-08-21 | 0.790 |

### Forced Liquidation Summary (>= 85%)
- Total events: 17 days
