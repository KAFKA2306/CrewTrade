

VIX分析からStockTwitsセンチメントまで、無料LLMを使用する6つの専門AIエージェントが驚くほど正確なトレードシグナルを提供します。

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Framework-green.svg)](https://github.com/crewAIInc/crewAI)

---

## 🎯 これは何をするのか

このAIトレーディングクルーは、専門AIエージェントのチームを使用して、毎日の株式リサーチプロセス全体を自動化します。毎朝数時間かけて金融ニュースを手動で閲覧したり、テクニカル指標を分析したり、ソーシャルセンチメントを監視したりする代わりに、数分で**明確なトレード推奨**を取得できます。

**システムが提供するもの:**
- 🔍 **包括的な市場分析**: VIXボラティリティ、グローバル指数、通貨の動き
- 📰 **速報ニュース処理**: 主要金融ソースからの数十の記事
- 📱 **ソーシャルセンチメント分析**: 数千のStockTwits投稿と個人投資家のセンチメント
- 📊 **テクニカル指標分析**: トレンド、モメンタム、ボラティリティ、ボリュームをカバーする20以上の指標
- 🔮 **AI駆動型予測**: TimeGPTを使用した機械学習予測
- 💰 **ファンダメンタル分析**: 財務比率、アナリスト評価、本質的価値計算
- ⚡ **最終トレードシグナル**: 信頼度レベルを持つ明確な強気/中立/弱気推奨

---


## 🏗️ アーキテクチャ: AIエージェントの協力方法

システムは洗練された3段階のアプローチに従います:

### フェーズ1: 🌍 市場状況分析
- VIXボラティリティとグローバル市場環境を分析
- 市場概要指標としてS&P 500 (SPY)を処理
- 国際指数、通貨、オーバーナイトの動向を監視

### フェーズ2: 🔍 個別株式分析（6つの専門エージェント）
1. **📰 ニュース要約エージェント**: TipRanks、FinViz、Seeking Alpha、MarketWatchからの速報ニュースを処理
2. **📱 センチメント要約エージェント**: 500以上のStockTwits投稿を分析して個人投資家のセンチメントを把握
3. **📈 テクニカル指標エージェント**: 20以上の指標（RSI、MACD、ボリンジャーバンドなど）を計算
4. **🔮 TimeGPTアナリストエージェント**: Nixtlaの最先端モデルを使用した機械学習予測
5. **🔍 ファンダメンタル分析エージェント**: 財務健全性、バリュエーション指標、アナリストの意見
6. **🎯 デイトレーダーアドバイザーエージェント**: すべてのデータを実行可能なトレードシグナルに統合

---

## 🚀 インストールとセットアップ

### 前提条件
- Python 3.10+ (< 3.13)
- [UV](https://docs.astral.sh/uv/) または [Poetry](https://python-poetry.org/) (推奨) または pip

### 1. CrewAIフレームワークのインストール

**最新のインストール手順と要件については、公式[CrewAI GitHub](https://github.com/crewAIInc/crewAI)をご覧ください。**

```bash
# uvを使用（推奨）
uv add crewai[tools]

# または poetryを使用
poetry add "crewai[tools]"

# または pipを使用
pip install "crewai[tools]"
```

### 2. プロジェクトのクローンとインストール
```bash
# リポジトリをクローン
git clone https://github.com/philippe-ostiguy/AITradingCrew.git
cd AITradingCrew

# uvでインストール（推奨）
uv sync

# または poetryでインストール
poetry install

# または pipでインストール
pip install -e .
```

### 3. 🔑 必要なAPIキー

プロジェクトルートに`.env`ファイルを作成し、以下のAPIキーを設定します:

```bash
# LLMプロバイダー（OpenRouter推奨）
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_DEEPSEEK_R1=deepseek/deepseek-r1:free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# データプロバイダー
TWELVE_API_KEY=your_twelvedata_api_key_here
TIMEGPT_API_KEY=your_nixtla_api_key_here
RAPID_API_KEY=your_rapidapi_key_here
FRED_API_KEY=your_fred_api_key_here
```

### 4. 🎯 システムの実行

Taskfileを使用して簡単に実行できます：

```bash
# 全てのデータ取得と分析を実行
task process:all

# Imuraファンド分析のみ実行
task run:imura

# Oracle収益予測のみ実行
task run:oracle
```

または直接Pythonコマンドを使用：

```bash
# Imuraファンド分析
uv run -m ai_trading_crew.use_case_runner imura --config config/use_cases/imura.yaml
```

---

## 📦 利用可能なユースケース

| 名前 | 概要 | デフォルト設定 |
| --- | --- | --- |
| `imura` | 井村氏のポートフォリオ分析。 | `config/use_cases/imura.yaml` |
| `oracle` | Oracle収益予測モデル。 | `config/use_cases/oracle.yaml` |
| `precious_metals_spread` | 東京市場の貴金属ETFと先物価格の乖離を検出。 | `config/use_cases/precious_metals_spread.yaml` |
| `credit_spread` | ジャンク社債ETFと米国債ETFの価格比率をモニタリング。 | `config/use_cases/credit_spread.yaml` |
| `yield_spread` | ジャンク社債利回りと国債利回りのイールドスプレッドを追跡。 | `config/use_cases/yield_spread.yaml` |
| `securities_collateral_loan` | 証券担保ローンリスク分析。 | `config/use_cases/securities_collateral_loan.yaml` |

いずれのユースケースも以下のように実行できます:

```bash
uv run -m ai_trading_crew.use_case_runner credit_spread --config config/use_cases/credit_spread.yaml
# イールドスプレッドトラッカー
uv run -m ai_trading_crew.use_case_runner yield_spread --config config/use_cases/yield_spread.yaml
# 証券担保ローンリスク分析
uv run -m ai_trading_crew.use_case_runner securities_collateral_loan --config config/use_cases/securities_collateral_loan.yaml
```

### リスク配分ガイダンスについて

`yield_spread` ユースケースでは、最新のスプレッドzスコアに応じて `Risk-On / Neutral / Defensive` の推奨ウェイトを提示します。`config/use_cases/yield_spread.yaml` で設定可能です。

---

## 🛠️ カスタマイズ

`ai_trading_crew/config.py`の設定を変更することで分析をカスタマイズできます:

- **株式シンボルの変更**: `SYMBOLS`リストを更新
- **データ制限の調整**: `NEWS_FETCH_LIMIT`と`SOCIAL_FETCH_LIMIT`を変更
- **テクニカル指標**: 期間とパラメーターをカスタマイズ
- **LLMモデル**: 異なるAIモデル間で切り替え