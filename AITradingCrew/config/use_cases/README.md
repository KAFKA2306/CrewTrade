# Use Case Configurations

このディレクトリにはユースケースごとの YAML 設定ファイルが配置されています。代表的な例として `index_7_portfolio.yaml`（国内ETF版）と `index_7_portfolio_original.yaml`（オリジナル指数版）があり、いずれも以下の主要セクションで構成されています。

- `period` — データ取得期間（例: `20y`, `max`）。  
- `indices` — 利用するティッカーと名称、カテゴリ。カテゴリは可視化時の並び順・配色に利用されます。  
- `loan_amount` / `ltv_limit` / `warning_ratio` / `liquidation_ratio` — LTV 設定。  
- `optimization` — 目的関数の重み、制約（最小/最大ウェイト、最大ボラティリティ）、サンプルサイズ、ルックバック期間など。

## index_7_portfolio_original.yaml

- 米国 (`^GSPC`, `^NDX`)、日本 (`^N225`, `1478.T`)、新興国 (`EEM`)、債券 (`TLT`)、ゴールド (`GC=F`) の7資産を採用し、`period: max` で利用可能な最長期間をダウンロードします。  
- `visualization.py` ではカテゴリ順をもとに色を割り当てているため、カテゴリは `equity`, `commodity`, `bonds` など既存の定義に合わせて記述してください。

## 新しいユースケースを追加するには

1. YAMLファイルを同ディレクトリに追加。  
2. `indices` に必要なティッカーを列挙し、カテゴリを設定。  
3. 必要に応じて `optimization` セクションを調整。  
4. 実行は `PYTHONPATH=AITradingCrew python3 -m ai_trading_crew.use_case_runner <use_case_name> --config <yaml>` で行います。
