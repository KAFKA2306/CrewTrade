# Index 7 Portfolio Use Case

このディレクトリは「index_7_portfolio」ユースケースの実装をまとめています。分析・最適化からレポート生成、可視化までをワンストップで実行するためのモジュールが配置されています。

## 主なモジュール

- `analysis.py`  
  最適化ロジックとLTV計算を担当します。構成済みのインデックス Universe に対して `optimize_collateral_portfolio` を呼び出し、ポートフォリオ構成を返却します。
- `data_pipeline.py`  
  `YFinanceEquityDataClient` を利用して価格系列を収集し、`index_master` を組み立てます。
- `visualization.py`  
  レポート向けのグラフ出力を統括します。カテゴリ順序（US株→日本株→新興国株→債券→ゴールド→その他）に基づいて銘柄を並べ替え、カテゴリごとに同系色の5階調パレットから色を割り当てます。
- `reporting.py`  
  ポートフォリオ表・サマリー・ウォークフォワード検証結果と共に、可視化の PNG を Markdown レポートへ埋め込みます。
- `validation.py`  
  ウォークフォワード、ストレステスト、感度分析など評価系の処理を提供します。
- `use_case.py`  
  CLI 経由で実行されるエントリーポイント。データ収集→分析→レポートの3段階を順に呼び出します。

## 可視化と色設定

- カテゴリごとに以下のカラーパレットを採用し、銘柄数に応じて自動で濃淡を割り当てます。  
  US Equity = `sns.color_palette("Blues")` / Japan Equity = `Reds` / Emerging Equity = `Greens` / Bonds = `Purples` / Gold = `Oranges` / Other = `Greys`  
- `01_allocation.png`: 最適化ポートフォリオとリファレンス戦略（Inverse-Vol, Min/Max 系, Max Kelly, WF#1, WF#2 など）のウェイト構成を100%積み上げ棒グラフで比較。カテゴリごとに同一色相、銘柄ごとに濃淡が変わります。
- `02_cumulative_returns.png`: 戦略別の資産推移を100%積み上げエリアで示し、同じ色を使った折れ線で各戦略の累積リターン（ベース=1）を重ねています（縦軸ログスケール）。
- `03_drawdown.png`: ポートフォリオのピーク比減価を銘柄ごとの寄与に分解し、カテゴリに応じた色味の積み上げ面グラフ＋合計ドローダウン線でプロットします。

## 実行方法

```bash
PYTHONPATH=AITradingCrew python3 -m ai_trading_crew.use_case_runner index_7_portfolio \
  --config AITradingCrew/config/use_cases/index_7_portfolio_original.yaml
```

出力は `output/use_cases/index_7_portfolio/<YYYYMMDD>/` に保存され、レポート・グラフ・最適化済みポートフォリオ、ウォークフォワード結果が含まれます。
