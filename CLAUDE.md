# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CrewTrade is a multi-agent AI trading analysis system built on CrewAI. The main component is **AITradingCrew**, which orchestrates 6 specialized AI agents to analyze stocks using news, social sentiment, technical indicators, ML forecasting, and fundamentals. The repository also includes freqtrade (crypto trading bot) and yahooquery (Yahoo Finance wrapper) as reference components.

## Core Commands

```bash
# Installation
uv sync

# Stock analysis (main workflow)
crewai run
uv run -m ai_trading_crew.main

# Use case execution
uv run -m ai_trading_crew.use_case_runner precious_metals_spread --config config/use_cases/precious_metals_spread.yaml
uv run -m ai_trading_crew.use_case_runner credit_spread --config config/use_cases/credit_spread.yaml
uv run -m ai_trading_crew.use_case_runner yield_spread --config config/use_cases/yield_spread.yaml
uv run -m ai_trading_crew.use_case_runner securities_collateral_loan --config config/use_cases/securities_collateral_loan.yaml

# Validation
python3 -m compileall ai_trading_crew
```

## Architecture

### Multi-Agent System (AITradingCrew/ai_trading_crew/)

6つのエージェントが協調動作:
1. **News Summarizer** - 金融ニュース収集（TipRanks, FinViz, Seeking Alpha, MarketWatch）
2. **Sentiment Summarizer** - StockTwitsから500+投稿を分析
3. **Technical Indicator** - 20+指標（RSI, MACD, Bollinger Bands等）
4. **TimeGPT Analyst** - Nixtla TimeGPTによるML予測
5. **Fundamental Analysis** - 財務比率、バリュエーション、アナリストレーティング
6. **Day Trader Advisor** - 最終的なトレーディングシグナル統合

### Execution Flow

```
市場概況分析（VIX, グローバル市場, S&P 500）
 ↓
個別銘柄分析（複数シンボルを並列処理）
 ↓
データ収集（News/Social/Technical/Fundamental/ML）
 ↓
エージェントベース解析パイプライン
 ↓
最終レポート生成（output/agents_outputs/{YYYYMMDD}/）
```

### Use Case Framework (ai_trading_crew/use_cases/)

拡張可能なユースケースアーキテクチャ:

```
use_case_runner.py
 ↓
registry.py (ユースケースクラス取得)
 ↓
base.py (BaseUseCase抽象クラス)
 ↓
具体的ユースケース実装
  ├── config.py (パラメータ)
  ├── data_pipeline.py (データ取得)
  ├── analysis.py (計算ロジック)
  ├── reporting.py (レポート出力)
  └── insights.py (AI解説生成)
```

**実装済みユースケース**:
- `precious_metals_spread/`: ETF（1540, 1541, 1542, 1543）とスポット価格の乖離分析
- `credit_spread/`: ジャンク債とトレジャリーのスプレッド監視
- `yield_spread/`: イールドスプレッド分析
- `securities_collateral_loan/`: 証券担保ローンのリスク分析とポートフォリオ最適化

### Data Flow

```
Input Sources
├── News APIs (TipRanks, FinViz, Seeking Alpha, MarketWatch)
├── Social (StockTwits via RapidAPI)
├── Market Data (TwelveData API)
├── ML Forecasts (Nixtla TimeGPT)
├── Technical (TA-Lib)
├── Macro (FRED API)
└── Price Data (yfinance)
     ↓
analysts/ (データフェッチャー)
     ↓
crew.py (エージェント処理)
     ↓
output/ (レポート生成)
```

### Directory Structure

```
AITradingCrew/
├── ai_trading_crew/
│   ├── analysts/              # データ取得・分析モジュール
│   ├── config/                # エージェント・タスク定義（YAML）
│   ├── use_cases/             # 拡張可能ユースケースフレームワーク
│   │   ├── base.py            # 抽象基底クラス
│   │   ├── registry.py        # ユースケース登録
│   │   ├── data_clients/      # データクライアント（metals, fixed_income, yields）
│   │   └── {use_case_name}/   # 各ユースケース実装
│   ├── utils/                 # ユーティリティ
│   ├── main.py                # メインエントリーポイント
│   ├── crew.py                # CrewAI crew定義
│   ├── stock_processor.py     # 株式処理オーケストレーション
│   ├── use_case_runner.py     # ユースケース実行
│   └── config.py              # 設定・LLM設定
├── config/use_cases/          # ユースケース設定YAML
├── resources/data/use_cases/  # キャッシュデータ（Parquet）
└── output/                    # 生成レポート
    ├── agents_inputs/{YYYYMMDD}/
    ├── agents_outputs/{YYYYMMDD}/
    └── use_cases/{use_case}/{YYYYMMDD}/
```

## Configuration

### Environment Variables (.env)

```bash
# LLM (デフォルト: DeepSeek R1 無料枠)
OPENROUTER_API_KEY
OPENROUTER_DEEPSEEK_R1
OPENROUTER_BASE_URL

# Data Providers
TWELVE_API_KEY
TIMEGPT_API_KEY
RAPID_API_KEY
FRED_API_KEY
```

### Key Files

- `AITradingCrew/ai_trading_crew/config.py`: Settings, LLM configs, symbols
- `AITradingCrew/ai_trading_crew/config/*.yaml`: Agent/task definitions
- `AITradingCrew/config/use_cases/*.yaml`: Use case parameters

## Adding New Use Cases

1. `ai_trading_crew/use_cases/{new_use_case}/` ディレクトリ作成
2. `BaseUseCase` を継承した実装クラス作成
3. `registry.py` に登録
4. `config/use_cases/{new_use_case}.yaml` 設定ファイル作成
5. `uv run -m ai_trading_crew.use_case_runner {new_use_case} --config ...` で実行

## Data Storage Patterns

- **Raw data cache**: `resources/data/use_cases/{use_case}/raw/*.parquet`
- **Processed data**: `resources/data/use_cases/{use_case}/processed/*.parquet`
- **Reports**: `output/use_cases/{use_case}/{YYYYMMDD}/*.md`
- **Agent outputs**: `output/agents_outputs/{YYYYMMDD}/`

**重要**: `resources/data/` および `output/` のアーティファクトはコミットしない

## Component Relationships

- **AITradingCrew**: メインアプリケーション（独立稼働）
- **freqtrade**: 暗号通貨トレーディングボット（参照実装、直接統合なし）
- **yahooquery**: Yahoo Finance APIラッパー（価格データソースとして利用可能）

3コンポーネントは疎結合。AITradingCrewは独自のデータソース（TwelveData, TimeGPT等）で完結動作。

## Securities Collateral Loan Optimization

### Overview

`securities_collateral_loan` ユースケースは証券担保ローン（楽天銀行/楽天証券の株式担保ローン等）のリスク分析とポートフォリオ最適化を提供。2つのモード：

- **手動モード** (`optimization.enabled: false`): 指定した担保資産構成でLTV、補充ライン、ロスカットラインを分析
- **最適化モード** (`optimization.enabled: true`): 投信協会の上場ファンドリスト（~300 ETF）から最適な担保構成を自動生成

### Optimization Features

投信協会Excelから全ETFを取得し、以下の制約付き最適化を実行：

```
目的関数: w1×シャープ比 - w2×ボラティリティ
制約条件:
  - 個別銘柄ウェイト: 5-35%
  - カテゴリ別ウェイト: ≤50%
  - ポートフォリオボラティリティ: ≤12%
最適化手法: ランダムサーチ（20,000サンプル）
```

### Configuration

`config/use_cases/securities_collateral_loan.yaml`:

```yaml
optimization:
  enabled: false  # trueで最適化モード有効化
  objective_weights:
    sharpe: 0.6
    volatility: 0.4
  constraints:
    min_weight: 0.05
    max_weight: 0.35
    max_category_weight: 0.5
    max_volatility: 0.12
  sample_size: 20000
  lookback: 3y
```

### Implementation

```
data_pipeline.py
  ├─ manual mode: collateral_assetsから価格データ取得
  └─ optimization mode: 投信協会Excel → 全ETF価格取得

analysis.py
  ├─ etf_screening.py: リスク指標計算（リターン、ボラティリティ、シャープ比）
  ├─ optimizer.py: 制約付きランダムサーチ
  └─ 既存LTV分析: 補充ライン、ロスカット、ストレスシナリオ

reporting.py
  ├─ Portfolio Optimization Results
  ├─ Top 10 ETFs by Composite Score
  └─ Collateral Breakdown（最適化結果）
```

### Data Clients

- **ToushinKyokaiDataClient** (`data_clients/toushin_kyokai.py`): 投信協会Excel自動ダウンロード・パース
- **YFinanceEquityDataClient**: 価格データ取得（既存）

### Output

- `resources/data/use_cases/securities_collateral_loan/processed/`
  - `etf_risk_metrics.parquet`: 全ETFのリスク指標
  - `optimized_portfolio.parquet`: 最適担保構成
- `output/use_cases/securities_collateral_loan/{YYYYMMDD}/`
  - `securities_collateral_loan_report.md`: リスク分析レポート
  - `securities_collateral_loan_insights.md`: AI解説

## Development Notes

- Python 3.10-3.13対応
- Package manager: UV推奨（`uv run *`を常用）
- Naming: snake_case files, PascalCase classes
- Parquet形式でデータキャッシュ（API呼び出し最小化）
- 日次ディレクトリ分割（YYYYMMDD）でレポート管理
- LLM agnostic設計（OpenRouter経由でDeepSeek R1無料枠デフォルト）
