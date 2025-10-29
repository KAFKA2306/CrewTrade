![0_zFUNL_p_C-IEeoAQ (1)](https://github.com/user-attachments/assets/97e29d19-3d73-413c-a51e-67f8ad579432)


*Photo by Igor Omilaev on Unsplash*

# AI Trading Crew 🤖

## 毎日2時間の株式市場リサーチに疲れていませんか？代わりにこのエージェントAIシステムを使いましょう

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

### 🚀 このシステムの動作を見たいですか？

このAIエージェントシステムが実際にどのように機能するかの詳細と、実際の分析例を確認するには、私の詳細な[実践デモンストレーションと実装ガイド](https://ostiguyphilippe.medium.com/d53bbc54075f)をご覧ください。この記事では、完全なプロセスを説明し、AIエージェントがどのように協力してトレードインサイトを生成するかを正確に示しています。


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

### 🔑 APIキーの取得方法（すべて無料プランあり）:

1. **OpenRouter** (無料LLM): [openrouter.ai](https://openrouter.ai) - DeepSeek R1への無料アクセスを取得
2. **TwelveData** (金融データ): [twelvedata.com](https://twelvedata.com) - 無料プランあり
3. **Nixtla TimeGPT** (予測): [nixtla.io](https://nixtla.io) - AI予測API
4. **RapidAPI** (ソーシャルデータ): [rapidapi.com](https://rapidapi.com) - StockTwitsセンチメントデータ用
5. **FRED** (金利/マクロデータ): [fred.stlouisfed.org](https://fred.stlouisfed.org) - APIキーで金利指標を取得

### 4. 🎯 システムの実行

```bash
# トレーディングクルーを実行
crewai run

# または直接コマンドを使用
python -m ai_trading_crew.main
```

**これだけです！** 🎉 システムは設定された株式を分析し、トレード推奨を提供します。

---

## 📊 デフォルト設定

- **分析対象株式**: AAPL, NVDA, MSFT, AMZN, GLD, GOOGL, TSLA
- **市場概要**: SPY (S&P 500 ETF)
- **ニュースソース**: TipRanks, FinViz, Seeking Alpha, MarketWatch
- **ソーシャルデータ**: 銘柄ごとに500のStockTwits投稿
- **テクニカル指標**: 30日間の履歴コンテキストを持つ20以上の指標
- **予測モデル**: TimeGPT 1日先予測

## 📝 サンプル出力

```
**推奨**: 強気
**信頼度レベル**: 高

**主要要因**:
- 圧倒的なAIリーダーシップと成長要因: Q1 FY2026データセンター収益が前年同期比73%急増
- テクニカルブレイクアウトモメンタム: 価格が52週高値付近で終了、強気のMACDシグナル
- 圧倒的なソーシャルセンチメント: 213の強気シグナルがAI優位性と機関投資家のFOMOを引用
- ETFと機関投資家のサポート: 半導体ETFのトップ保有銘柄で過去最高のボリューム

**リターン/リスク評価**: $150–$153への上昇余地（5.3–6.6%の利益）が下落リスクを上回る...

**トレード根拠**: 市場開始時にロングポジションを開始し、$145.16を超えるブレイクアウトを目標に...
```

---

## 📦 利用可能なユースケース

| 名前 | 概要 | デフォルト設定 |
| --- | --- | --- |
| `precious_metals_spread` | 東京市場の貴金属ETFと先物価格の乖離を検出し、統計的な異常シグナルを抽出します。 | `config/use_cases/precious_metals_spread.yaml` |
| `credit_spread` | ジャンク社債ETFと米国債ETFの価格比率をモニタリングし、クレジットスプレッドの拡大/縮小を検知します。 | `config/use_cases/credit_spread.yaml` |
| `yield_spread` | ジャンク社債利回りと国債利回りのイールドスプレッドを追跡し、zスコアによる拡大/縮小シグナルとリスク配分ガイダンスを生成します。 | `config/use_cases/yield_spread.yaml` |

いずれのユースケースも以下のように実行できます:

```bash
python -m ai_trading_crew.use_case_runner credit_spread --config config/use_cases/credit_spread.yaml
# イールドスプレッドトラッカー
python -m ai_trading_crew.use_case_runner yield_spread --config config/use_cases/yield_spread.yaml
```

### リスク配分ガイダンスについて

`yield_spread` ユースケースでは、最新のスプレッドzスコアに応じて `Risk-On / Neutral / Defensive` の推奨ウェイトを提示します。`allocation.optimization.enabled` を `true` にすると、指定した候補アセットのリターン系列を使ってモンテカルロ探索で最大シャープレシオを推定し、推奨ウェイト・推定Sharpe・バックテスト指標（年間リターン/ボラティリティ/最大ドローダウン）をレポートに出力します。さらに `sensitivity_sample_sizes` を設定するとサンプル数ごとのシャープ安定度テーブルも生成されます。`config/use_cases/yield_spread.yaml` の `allocation` セクションでしきい値・ウェイト候補・最適化パラメータを調整できます。実行後は `output/use_cases/yield_spread/<日付>/yield_spread_report.md` を参照すると現在のレジームと推奨ウェイトが確認できます。

---

## 🛠️ カスタマイズ

`ai_trading_crew/config.py`の設定を変更することで分析をカスタマイズできます:

- **株式シンボルの変更**: `SYMBOLS`リストを更新
- **データ制限の調整**: `NEWS_FETCH_LIMIT`と`SOCIAL_FETCH_LIMIT`を変更
- **テクニカル指標**: 期間とパラメーターをカスタマイズ
- **LLMモデル**: 異なるAIモデル間で切り替え

---

## ⚠️ 免責事項

**このソフトウェアは情報提供のみを目的としており、金融アドバイスを構成するものではありません。** 投資決定を行う前に、常に独自の調査を行うか、ファイナンシャルアドバイザーに相談してください。過去のパフォーマンスは将来の結果を保証するものではありません。

---

## 📄 ライセンス

このプロジェクトはApache License 2.0の下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。

---

## 💡 このプロジェクトが気に入りましたか？サポートを表明してください！

⭐ **プロジェクトにスターを付ける**
🤝 **連絡を取り合うために[LinkedIn](https://www.linkedin.com/in/philippe-ostiguy/)で接続リクエストを送信してください**

ハッピーオートメーション！ 🚀📈
