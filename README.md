# CrewTrade — マルチエージェント金融調査・時系列分析

**公開ダッシュボード:** https://kafka2306.github.io/CrewTrade/

CrewTradeは、CrewAIを用いて金融データの取得、定量分析、レポート生成、時系列予測をユースケースごとに実行する研究プロジェクトです。

市場データ、計算結果、モデル予測、文章による解釈を分離し、インサンプル成績だけで投資戦略の有効性を断定しないことを前提とします。

## 主な機能

- Yahoo Financeなどからの市場データ取得
- 株式、ETF、金利、金属、半導体の分析
- ポートフォリオと証券担保ローンのリスク計算
- 基準指数とのリターン・リスク比較
- インサンプルとアウト・オブ・サンプルの分離
- CrewAIによる調査・分析タスクの分担
- Amazon Chronos系モデルを使った時系列予測実験
- Markdown・画像・静的HTMLレポートの生成
- GitHub Pagesへの分析結果公開

## 公開処理

GitHub Actionsは、`main`への変更時に依存関係を同期し、`web/build_static.py`で`docs/`を生成してGitHub Pagesへ公開します。

公開ダッシュボードは、ユースケースごとに生成済みレポートを一覧表示します。掲載値は各レポートの作成日時点の結果であり、リアルタイム価格ではありません。

## 主なユースケース

| ユースケース | 設定ファイル | 主な目的 |
| --- | --- | --- |
| `imura` | `config/use_cases/imura.yaml` | ファンド・指数比較、リターンとリスク分析 |
| `oracle` | `config/use_cases/oracle.yaml` | 個別企業・時系列予測の研究 |
| `credit` | `config/use_cases/credit.yaml` | 信用・クレジット関連分析 |
| `etf` | — | ETF比較 |
| `loan` | `config/use_cases/loan.yaml` | 証券担保ローンなどのリスク分析 |
| `metals` | `config/use_cases/metals.yaml` | 金属・コモディティ分析 |
| `portfolio` | `config/use_cases/portfolio.yaml` | ポートフォリオ分析 |
| `yields` | `config/use_cases/yields.yaml` | 金利・利回り分析 |
| `semiconductors` | `config/use_cases/semiconductors.yaml` | 半導体関連分析 |
| `legendary_investors` | `config/use_cases/legendary_investors.yaml` | 著名投資家の公開情報を用いた調査 |

設定ファイルが存在しないユースケースは、実装内の既定値または個別スクリプトを使用します。

## 技術構成

- Python 3.11
- CrewAI
- `uv`
- pandas / NumPy
- yfinance / yahooquery / pandas-datareader
- PyTorch / Transformers / Chronos Forecasting
- Nixtla
- Flask
- Matplotlib
- Playwright・Crawl4AI系の取得処理

依存関係の正本は`pyproject.toml`です。

## セットアップ

```bash
uv sync
```

Python要件は`>=3.11,<3.12`です。

APIキーや外部サービスの認証情報が必要なユースケースでは、ローカルの環境変数または非公開設定を使用してください。秘密情報をコミットしないでください。

## 実行

```bash
task process:all   # データ取得から分析までをまとめて実行
task fetch:all     # データ取得
task run           # 分析を実行
```

CLIエントリポイント:

```bash
uv run crew
uv run run_crew
uv run train
uv run replay
uv run test
```

Web画面をローカルで起動するタスクが利用できる構成では、次を実行します。

```bash
task serve
```

## 分析品質の確認項目

- データの対象期間と取得日時を残す
- 配当・分割・通貨・市場休業日の扱いを明示する
- インサンプルとOOSを分離する
- 比較指数と計算条件をそろえる
- 手数料、税、スリッページを含まない結果を実績と呼ばない
- 予測モデルの入力期間、予測期間、評価指標を保存する
- LLMによる文章と定量計算結果を区別する
- 取得失敗や欠損を推測で補完しない

## 注意

- 過去の成績は将来の収益を保証しません
- Chronosなどの予測値は確定的な将来価格ではありません
- 公開レポートの数値は、作成時点のデータと実装に依存します
- 本プロジェクトは投資助言、売買推奨、運用実績の保証ではありません

**README最終監査:** 2026-08-01
