# 証券担保ローン最適化

証券担保ローン（楽天銀行/楽天証券の株式担保ローン等）のリスク分析とポートフォリオ最適化。

## 概要

証券を担保に資金を借り入れる際のLTV（Loan-to-Value）、補充ライン、ロスカットラインを分析。最適化モードでは投信協会全ETF（~300銘柄）から最適な担保構成を自動生成。

## 動作モード

### 手動モード (`optimization.enabled: false`)
指定した担保資産構成でリスク分析のみ実行。

### 最適化モード (`optimization.enabled: true`)
投信協会Excelから全ETFを取得し、制約付き最適化を実行。

**最適化目的関数**:
```
max: w1 × Sharpe Ratio - w2 × Volatility
```

**制約条件**:
- 個別銘柄ウェイト: 5-35%
- カテゴリ別ウェイト: ≤50%
- ポートフォリオボラティリティ: ≤12%

**最適化手法**: ランダムサーチ（20,000サンプル）

## モジュール構成

- `config.py`: ローン条件・最適化パラメータ設定
- `data_pipeline.py`: ETFリスト取得・価格データ取得
- `etf_screening.py`: リスク指標計算（リターン・ボラティリティ・シャープ比）
- `optimizer.py`: 制約付きランダムサーチ最適化
- `analysis.py`: LTV分析・ストレステスト
- `reporting.py`: リスクレポート・最適化結果生成
- `insights.py`: AI解説生成
- `use_case.py`: BaseUseCase実装

## 実行方法

```bash
uv run -m ai_trading_crew.use_case_runner securities_collateral_loan --config config/use_cases/securities_collateral_loan.yaml
```

## 設定例

```yaml
loan_amount: 10000000.0
annual_interest_rate: 0.01875
collateral_period: "3y"
max_borrowing_ratio: 0.60
margin_call_threshold: 0.70
forced_liquidation_threshold: 0.85

collateral_assets:  # 手動モード用
  - ticker: "1306.T"
    name: "TOPIX連動型上場投資信託"
    quantity: 100
  - ticker: "1570.T"
    name: "日経平均レバレッジ・インデックス連動型上場投信"
    quantity: 50

optimization:
  enabled: true
  objective_weights:
    sharpe: 0.6
    volatility: 0.4
  constraints:
    min_weight: 0.05
    max_weight: 0.35
    max_category_weight: 0.5
    max_volatility: 0.15
  sample_size: 20000
  lookback: "3y"
  exclude_hedged_etfs: true
  correlation_threshold: 0.90
```

## 出力

`output/use_cases/securities_collateral_loan/{YYYYMMDD}/`:
- `securities_collateral_loan_report.md`: リスク分析レポート
  - LTV・補充ライン・ロスカットライン
  - ストレステスト（-10%, -20%, -30%シナリオ）
  - 最適化結果（有効化時）
- `securities_collateral_loan_insights.md`: リスクシナリオ・推奨アクション

`resources/data/use_cases/securities_collateral_loan/processed/`:
- `etf_risk_metrics.parquet`: 全ETFのリスク指標
- `optimized_portfolio.parquet`: 最適担保構成

## 分析指標

### リスク指標
- **LTV (Loan-to-Value)**: ローン金額 / 担保時価
- **補充ライン**: LTV ≥ 0.70 → 追加担保必要
- **ロスカットライン**: LTV ≥ 0.85 → 強制決済
- **バッファ**: 補充/ロスカットまでの下落余地

### 最適化スコア
- **Sharpe Ratio**: (リターン - リスクフリーレート) / ボラティリティ
- **Composite Score**: w1 × Sharpe - w2 × Volatility
- **Max Drawdown**: 最大下落幅（歴史的データ）

## ストレステスト

| シナリオ | 下落率 | LTV | ステータス |
|---|---|---|---|
| Current | 0% | 0.605 | 正常 |
| Moderate | -10% | 0.672 | 正常 |
| Severe | -20% | 0.756 | 補充必要 |
| Extreme | -30% | 0.864 | ロスカット |

## データソース

- **ETFリスト**: 投信協会 (https://www.toushin.or.jp/files/static/486/listed_fund_for_investor.xlsx)
- **価格データ**: Yahoo Finance (yfinance)
- **リスクフリーレート**: 日本国債10年利回り（FRED: DGS10/JPY proxy）
