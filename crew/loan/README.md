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
- アセットアロケーション: 債券15-30%、金15-25%、株式40-60%

**最適化手法**: HRP（階層的リスクパリティ）、フォールバック: ランダムサーチ（20,000サンプル）

## コア・サテライト戦略

### 概要

年次リバランスにおいて、ポートフォリオをコア（安定保有）とサテライト（機動的入替）に分割し、長期的な資産保全と短期的な収益機会を両立。

### 設定

```yaml
core_satellite:
  enabled: true
  core_weight: 0.60          # コア資産比率
  satellite_weight: 0.40     # サテライト資産比率
  core_rebalance_years: 2    # コア再構築サイクル（年）
```

### 実装ロジック (`analysis.py::_apply_core_satellite_strategy`)

#### 初年度またはコア再構築年

```python
needs_core_rebalance = (
    prev_portfolio is None or
    prev_metadata is None or
    prev_metadata.rebalance_year >= core_rebalance_years
)
```

**処理フロー:**
1. 最適化されたポートフォリオ全体をシャープレシオ順にソート
2. 上位60%をコア、下位40%をサテライトに分類
3. 各セグメントの重みを正規化（コア合計60%、サテライト合計40%）
4. `PortfolioMetadata`作成（rebalance_year=0、valid_until=現在+2年）

#### 2年目以降（コア維持年）

**処理フロー:**
1. 前年の`optimized_portfolio.parquet`と`portfolio_metadata.json`をロード
2. 前年コアポートフォリオを抽出
3. 価格データが無いETF（上場廃止等）を除外
4. 新規最適化されたサテライトポートフォリオを生成
5. コアとサテライトの重複ティッカーを除去（コア優先）
6. 各セグメントの重みを再正規化
7. `PortfolioMetadata`更新（rebalance_year += 1）

#### データ永続化

**処理済みデータ** (`resources/data/use_cases/securities_collateral_loan/processed_backtests/{YYYYMMDD}/`)

- `optimized_portfolio.parquet`:
  - カラム: `ticker`, `weight`, `portfolio_type` ("core" or "satellite"), `name`, `category`, etc.
- `portfolio_metadata.json`:
  ```json
  {
    "anchor_date": "2024-05-31T00:00:00",
    "portfolio_type": "mixed",
    "core_weight": 0.6,
    "satellite_weight": 0.4,
    "rebalance_year": 1,
    "valid_until": "2026-05-31T00:00:00",
    "optimization_method": "hrp"
  }
  ```

### ウォークフォワードバックテスト

**実行例:**

```bash
# 10年間のウォークフォワードバックテスト
uv run python -m ai_trading_crew.backtests.securities_collateral_loan_backtest \
  securities_collateral_loan \
  --config config/use_cases/securities_collateral_loan.yaml \
  --years 10
```

**年次フロー:**

```
2016: rebalance_year=0 → 新規コア作成
2017: rebalance_year=1 → コア維持、サテライト再構築
2018: rebalance_year=2 → コア維持、サテライト再構築
2019: rebalance_year=0 → コア再構築（rebalance_year≥2でトリガー）
2020: データ無し（スキップ）
2021: rebalance_year=0 → 新規コア作成（前年データ無し）
2022: rebalance_year=1 → コア維持
2023: rebalance_year=2 → コア維持
2024: rebalance_year=0 → コア再構築
2025: rebalance_year=1 → コア維持
```

### 利点

- **コア**: 高シャープレシオETFを長期保有→取引コスト削減、安定リターン
- **サテライト**: 年次最適化で市場環境変化に対応→収益機会獲得
- **税効率**: コア銘柄の保有継続で含み益課税を繰延
- **リスク管理**: 毎年40%の入替により、新規リスク要因への対応が可能

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
