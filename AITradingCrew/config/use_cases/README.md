# Use Case Configuration Files

ユースケース別の設定ファイル（YAML）。

## securities_collateral_loan.yaml

証券担保ローンユースケースの設定。

### 基本設定

```yaml
name: securities_collateral_loan
period: 3y                      # 価格データ取得期間
loan_amount: 10000000           # ローン金額（円）
annual_interest_rate: 0.01875   # 年率金利
ltv_limit: 0.6                  # LTV上限（60%）
warning_ratio: 0.7              # 補充ライン（70%）
liquidation_ratio: 0.85         # ロスカットライン（85%）
```

### 手動モード用担保資産

```yaml
collateral_assets:
  - ticker: 1306.T
    quantity: 73
    description: NEXT FUNDS TOPIX ETF
  - ticker: 2568.T
    quantity: 118
    description: NASDAQ100 ETF (No Hedge)
```

### 最適化モード

#### 有効化

```yaml
optimization:
  enabled: true  # true: 最適化モード、false: 手動モード
```

#### 目的関数

```yaml
objective_weights:
  sharpe: 0.6       # シャープレシオウェイト
  volatility: 0.4   # ボラティリティウェイト（負の影響）
```

#### 制約条件

```yaml
constraints:
  min_weight: 0.05              # 個別銘柄最小ウェイト（5%）
  max_weight: 0.2               # 個別銘柄最大ウェイト（20%）
  max_category_weight: 0.5      # カテゴリ別最大ウェイト（50%）
  max_volatility: 0.12          # ポートフォリオ最大ボラティリティ（12%）
  max_asset_drawdown: 0.30      # 個別銘柄最大ドローダウン（30%）
  max_portfolio_drawdown: 0.25  # ポートフォリオ最大ドローダウン（25%）

  asset_allocation:
    bonds:
      min: 0.15                 # 債券最小配分（15%）
      max: 0.30                 # 債券最大配分（30%）
    gold:
      min: 0.15                 # 金最小配分（15%）
      max: 0.25                 # 金最大配分（25%）
    equity:
      min: 0.40                 # 株式最小配分（40%）
      max: 0.60                 # 株式最大配分（60%）
```

#### コア・サテライト戦略

```yaml
core_satellite:
  enabled: true               # コア・サテライト有効化
  core_weight: 0.60           # コア資産比率（60%）
  satellite_weight: 0.40      # サテライト資産比率（40%）
  core_rebalance_years: 2     # コア再構築サイクル（2年）
```

**動作:**
- **rebalance_year = 0**: 新規コア作成（シャープレシオ上位60%）
- **rebalance_year = 1**: 前年コア維持、サテライト40%を再最適化
- **rebalance_year = 2**: 前年コア維持、サテライト40%を再最適化
- **rebalance_year ≥ 2**: 次年度でコア再構築（rebalance_year → 0）

#### リスクポリシー

```yaml
risk_policy:
  primary_metric: max_asset_drawdown
  description: >
    Exclude ETFs solely when their trailing max drawdown exceeds the max_asset_drawdown
    constraint; other limits remain for portfolio construction, not asset gating.
```

#### パラメータ

```yaml
sample_size: 20000              # ランダムサーチサンプル数
lookback: 5y                    # 最適化用ルックバック期間
history_window: 5y              # 価格データ取得期間
walkforward_years: 5            # ウォークフォワード年数（デフォルト）
```

#### 最適化プロファイル

複数の最適化戦略を同時実行し、primary_profileを選択。

```yaml
profiles:
  - name: max_sharpe
    objective_weights:
      sharpe: 1.0
      volatility: 0.0
    correlation_threshold: 0.8
    max_portfolio_size: 20
    min_assets: 10

  - name: low_volatility
    objective_weights:
      sharpe: 0.0
      volatility: 1.0
    constraints_override:
      max_weight: 0.2
      min_weight: 0.05
    correlation_threshold: 0.8
    max_portfolio_size: 20
    min_assets: 10

  - name: cost_focus
    objective_weights:
      sharpe: 0.5
      volatility: 0.2
      expense: 0.3        # 費用率重視
    correlation_threshold: 0.8
    max_portfolio_size: 10
    min_assets: 10
    constraints_override:
      max_weight: 0.2
      min_weight: 0.05
```

### ストレステストシナリオ

```yaml
scenarios:
  - drop_pct: 0.1
    label: "-10%"
  - drop_pct: 0.2
    label: "-20%"
  - drop_pct: 0.3
    label: "-30%"
  - drop_pct: 0.4
    label: "-40%"
```

### 金利計算期間

```yaml
interest_horizons_days:
  - 30    # 30日
  - 90    # 90日
  - 180   # 180日
```

## 設定変更時の注意点

1. **コア・サテライト有効化**: `core_satellite.enabled: true`設定時は、`core_rebalance_years`に基づいてコアが自動的に維持/再構築される
2. **アセットアロケーション**: `asset_allocation`の合計が100%を超えないように設定（min合計≤100%, max合計≥100%）
3. **ドローダウン制約**: `max_asset_drawdown`が厳しすぎると、全ETFが除外される可能性あり
4. **プロファイル選択**: 最初にポートフォリオ生成に成功したプロファイルがprimary_profileとして採用

## バックテスト実行例

```bash
# 10年間のウォークフォワードバックテスト
uv run python -m ai_trading_crew.backtests.securities_collateral_loan_backtest \
  securities_collateral_loan \
  --config config/use_cases/securities_collateral_loan.yaml \
  --years 10

# 設定ファイルのカスタムパスを指定
uv run python -m ai_trading_crew.backtests.securities_collateral_loan_backtest \
  securities_collateral_loan \
  --config /path/to/custom_config.yaml \
  --years 15
```
