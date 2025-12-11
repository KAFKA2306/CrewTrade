# Securities Collateral Loan Backtest

証券担保ローンユースケースのウォークフォワードバックテストスクリプト。

## 概要

`securities_collateral_loan_backtest.py`は年次アンカー日付ごとに以下を実行:

1. **データ収集**: 過去価格データ、ETFマスターデータ取得
2. **前年ポートフォリオロード**: `_load_previous_portfolio()`で前年の最適化結果とメタデータを読込
3. **分析・最適化**: HRPまたはランダムサーチでポートフォリオ最適化
4. **コア・サテライト戦略適用**: 前年データとrebalance_year判定に基づき、コア維持またはコア再構築
5. **フォワードテスト**: 最適化ポートフォリオの翌年パフォーマンスをシミュレーション
6. **レポート生成**: 分析結果、フォワードテストメトリクス、メタデータを保存

## コア・サテライト戦略の実装

### 前年ポートフォリオのロード (`_load_previous_portfolio`)

```python
def _load_previous_portfolio(self, anchor: pd.Timestamp) -> Tuple[pd.DataFrame | None, PortfolioMetadata | None]:
    prev_year = anchor.year - 1
    prev_anchor = pd.Timestamp(year=prev_year, month=anchor.month, day=anchor.day)

    prev_dir = self.processed_base_dir / prev_anchor.strftime("%Y%m%d")
    portfolio_path = prev_dir / "optimized_portfolio.parquet"
    metadata_path = prev_dir / "portfolio_metadata.json"

    if not portfolio_path.exists():
        return None, None

    portfolio = pd.read_parquet(portfolio_path)
    metadata = None
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            metadata_dict = json.load(f)
            metadata = PortfolioMetadata(**metadata_dict)

    return portfolio, metadata
```

### バックテストループ

```python
for year_index, anchor in enumerate(anchors):
    # 前年のポートフォリオとメタデータをロード
    prev_portfolio, prev_metadata = self._load_previous_portfolio(anchor)
    data_payload['previous_portfolio'] = prev_portfolio
    data_payload['previous_metadata'] = prev_metadata
    data_payload['year_index'] = year_index

    # 分析・最適化（コア・サテライト戦略を内部で適用）
    analysis_payload = analyzer.evaluate(data_payload)

    # レポート生成（メタデータも保存）
    report_payload = reporter.persist(analysis_payload)
```

### データフロー

```
Anchor 2024-05-31 (year_index=0)
  ├─ _load_previous_portfolio(2024-05-31) → 2023年データ検索
  │   └─ 20230531/optimized_portfolio.parquet, portfolio_metadata.json
  ├─ analyzer.evaluate()
  │   └─ _apply_core_satellite_strategy()
  │       ├─ 前年データあり → コア維持 or コア再構築判定
  │       └─ 前年データなし → 新規コア作成
  └─ reporter.persist()
      └─ 20240531/optimized_portfolio.parquet, portfolio_metadata.json 保存
```

### 年次進行例

```
2016-05-31 (year_index=0): 前年データ無し → 新規コア作成 (rebalance_year=0)
2017-05-31 (year_index=1): 2016データロード → コア維持 (rebalance_year=1)
2018-05-31 (year_index=2): 2017データロード → コア維持 (rebalance_year=2)
2019-05-31 (year_index=3): 2018データロード → コア再構築 (rebalance_year=0)
```

## Execution Command

To run the backtest, use the following command from the root of the `AITradingCrew` directory:

```bash
python ai_trading_crew/backtests/securities_collateral_loan_backtest.py securities_collateral_loan
```

You can also specify the number of years to backtest using the `--years` argument:

```bash
python ai_trading_crew/backtests/securities_collateral_loan_backtest.py securities_collateral_loan --years 5
```

## Summary

This script automates the historical backtesting of the securities collateral loan strategy, providing insights into its performance over various periods.