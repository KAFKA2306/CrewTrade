# index_7_portfolio（オリジナル指数）実行メモ

- 検証コマンド  
  `PYTHONPATH=AITradingCrew python3 -m ai_trading_crew.use_case_runner index_7_portfolio --config AITradingCrew/config/use_cases/index_7_portfolio_original.yaml`
- 出力ディレクトリ  
  `output/use_cases/index_7_portfolio/20251101/`
- データ取得期間  
  2015-10-16 〜 2025-10-31（取得した7指数の共通期間）

## 生成ファイル
- `index_7_portfolio_report.md`：8種類のグラフを埋め込んだMarkdownレポート
- `graphs/*.png`：資産配分〜相関ヒートマップまで8枚のPNG
- `optimized_portfolio.parquet`：最適化後ポートフォリオの構成

## 備考
- 設定ファイルは `AITradingCrew/config/use_cases/index_7_portfolio_original.yaml` を使用。国内ETFとは別ユニバースのため、検証目的でのみ利用。
- `validation.py` 内のウォークフォワード処理で `FutureWarning: 'M' is deprecated` が発生するため、将来的には `ME`（月末）頻度への変更を検討。
- `01_allocation.png` は最新ポートフォリオに加えて Equal Weight / 60/40 Mix / Inverse-Vol / Min Variance / Max Sharpe / Min Volatility / Min Drawdown / Max Kelly / 各ウォークフォワード期間のウェイトを100%積み上げ棒グラフで比較表示。
- `03_drawdown.png` は総ドローダウンに対する銘柄別寄与を積み上げ面グラフで可視化し、合計ドローダウン線を重ねています。
- Risk-Returnグラフでは、個別資産に加えて `Optimized` / `Equal Weight` / `60/40 Mix` / `Inverse-Vol` / `Min Variance` / `Max Sharpe` / `Min Volatility` / `Min Drawdown` / `Max Kelly` / `WF#1` / `WF#2` を散布図上に表示。
- 色設定は一元管理しており、US株→日本株→新興国株→債券→ゴールドの順で配色を固定（同じカテゴリは同色）。
- レポート内の「期間別ポートフォリオ構成」は `<br>` 区切りで全ティッカーのウェイトを降順表示。
