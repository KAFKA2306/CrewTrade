# Index 7-Portfolio Optimization Report

**Generated:** 2025-11-01 14:27:21

## 代替ETF対応表

| 国内ETF | 代替指数 | オリジナル |
|---------|----------|-----------|
| 1655.T ｉＳ米国株 | S&P500指数 | ^GSPC |
| 2840.T ｉＦＥナ百無 | NASDAQ100 | ^NDX |
| 1364.T ｉシェア４百 | JPX日経400 | ^N225 |
| 314A.T ｉＳゴールド | LBMA Gold Price | GC=F |
| 2520.T 野村新興国株 | MSCIエマージング・マーケットIMI指数 | EEM |
| 2511.T 野村外国債券 | FTSE世界国債インデックス(除く日本) | TLT |
| 399A.T 上場高配５０ | 東証配当フォーカス100指数 | 1478.T |

**初期投資額:** ¥20,998,698（Max DD -20.63%バッファ込み、為替リスク排除、円建て運用）

## Portfolio Allocation

| Ticker | Name | Category | Weight |
|--------|------|----------|--------|
| ^GSPC | S&P 500 Index | equity | 11.98% |
| ^NDX | NASDAQ-100 Index | equity | 11.12% |
| ^N225 | Nikkei 225 Index | equity | 9.20% |
| GC=F | Gold Futures (COMEX) | commodity | 29.31% |
| EEM | iShares MSCI Emerging Markets ETF | equity | 6.39% |
| TLT | iShares 20+ Year Treasury Bond ETF | bonds | 9.31% |
| 1478.T | iShares MSCI Japan High Dividend ETF | equity | 22.69% |

## Risk Metrics

- **Portfolio Value:** ¥20,934,117
- **Loan Amount:** ¥10,000,000
- **Current LTV:** 47.77%
- **LTV Limit:** 60%
- **Warning Ratio:** 70%
- **Liquidation Ratio:** 85%

✅ **HEALTHY:** LTV within safe limits

## トレーニング設定と検証概要

- **最適化サンプル数:** 10,000
- **最適化目的関数ウェイト:** sharpe 60%, volatility 40%
- **制約条件:** min_weight=0.05, max_weight=0.30, max_volatility=0.15
- **リバランス頻度（検証時）:** 四半期（Q）
- **訓練期間 / テスト期間:** 5年 / 2年（ローリング）
- **最適化ルックバック:** 10y
- **最大ドローダウンバッファ:** 20.63%

### ウォークフォワード検証サマリー

- **評価期間数:** 2
- **平均アウトオブサンプル Sharpe:** 1.086 ± 1.515
- **平均年率リターン:** 10.03%
- **平均最大ドローダウン:** -14.87%
- **Stability Score:** 0.398

### 期間別ポートフォリオ構成（降順ウェイト）

| Period | 訓練期間 | テスト期間 | ウェイト構成 | Sharpe | Max DD |
|--------|-----------|------------|--------------|--------|--------|
| 1 | 2015-10-16〜2020-10-16 | 2020-10-16〜2022-10-16 | TLT 25.6%<br>^NDX 22.4%<br>GC=F 20.3%<br>1478.T 14.2%<br>EEM 6.2%<br>^GSPC 5.9%<br>^N225 5.5% | -0.429 | -20.99% |
| 2 | 2015-10-16〜2022-10-16 | 2022-10-16〜2024-10-16 | GC=F 25.3%<br>1478.T 22.0%<br>^NDX 18.0%<br>^GSPC 11.7%<br>TLT 11.5%<br>EEM 6.3%<br>^N225 5.1% | 2.600 | -8.74% |

## Visualizations

### Portfolio Allocation
100% stacked bar chart comparing asset weights across the optimized portfolio, reference strategies (Equal Weight, 60/40 Mix, Inverse-Vol, Min/Max variants), and walk-forward periods.
![Portfolio Allocation](./graphs/01_allocation.png)

### Cumulative Returns Comparison
Stacked area view of strategy share (Optimized, Equal Weight, reference mixes) with cumulative return overlay.
![Cumulative Returns](./graphs/02_cumulative_returns.png)

### Drawdown Evolution
Stacked drawdown contributions by asset category, with total drawdown overlay.
![Drawdown](./graphs/03_drawdown.png)

### LTV Stress Tests
Loan-to-Value ratio during historical crisis periods (COVID-19, 2022 Inflation).
![LTV Stress](./graphs/04_ltv_stress.png)

### Asset Contribution to Returns
Monthly positive/negative contribution by asset relative to category-colored baseline.
![Asset Contribution](./graphs/05_asset_contribution.png)

### Risk-Return Profile
Scatter plot comparing individual assets with multiple allocation strategies (Optimized, Equal Weight, 60/40 Mix, Inverse-Vol, Min Variance, Max Sharpe, Min Volatility, Min Drawdown, Max Kelly, Walk-Forward portfolios WF#1/WF#2).
![Risk-Return](./graphs/06_risk_return.png)

### Rolling Sharpe Ratio
252-day rolling Sharpe ratio showing risk-adjusted performance stability over time.
![Rolling Sharpe](./graphs/07_rolling_sharpe.png)

### Asset Correlation Matrix
Correlation heatmap revealing diversification benefits between assets.
![Correlation](./graphs/08_correlation.png)
