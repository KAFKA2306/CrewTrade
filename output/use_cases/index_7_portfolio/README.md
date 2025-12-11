# output/use_cases/index_7_portfolio

`use_case_runner index_7_portfolio` を実行すると、日付ごとのサブディレクトリが生成されます。各フォルダには以下の成果物が残ります。

- `index_7_portfolio_report.md` — グラフを埋め込んだMarkdownレポート。
- `graphs/*.png` — 可視化（資産配分、累積リターン、積み上げドローダウン、LTVストレス、寄与度、リスク・リターン散布図、ローリングシャープ、相関）全8枚。
- `optimized_portfolio.parquet` — 最適化後のウェイト・名称・カテゴリ情報。
- `validation_report.md`（検証実行時） — ウォークフォワードやストレステストのサマリー。

## カラーパレットと順序

可視化はカテゴリ順で並び・色分けを統一しています。カテゴリ（US株→日本株→新興国株→債券→ゴールド→その他）ごとに `seaborn` の同系色パレットを使用し、銘柄ごとに濃淡を割り当てます。`01_allocation.png`・`02_cumulative_returns.png`・`03_drawdown.png` はこのルールに従い、カテゴリが同じ銘柄は近い色味で表示されつつ各銘柄は別トーンになります。

## 実行コマンドの例

```bash
PYTHONPATH=AITradingCrew python3 -m ai_trading_crew.use_case_runner index_7_portfolio \
  --config AITradingCrew/config/use_cases/index_7_portfolio_original.yaml
```

最新の生成結果は `20251101/` を参照してください（グラフの見本と README が入っています）。
