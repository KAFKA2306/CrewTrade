# ユースケースフレームワーク

拡張可能なユースケースアーキテクチャ。投資戦略分析・リスク管理のための独立したモジュール群。

## アーキテクチャ概要

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

## ディレクトリ構造

```
use_cases/
├── base.py                    # BaseUseCase抽象基底クラス
├── registry.py                # ユースケース登録・検索
├── __init__.py
├── data_clients/              # 共有データクライアント
│   ├── metals.py              # 貴金属データ
│   ├── fixed_income.py        # 債券データ
│   ├── yield_spread.py        # イールドスプレッド
│   ├── equities.py            # 株式・ETF
│   ├── toushin_kyokai.py      # 投信協会Excel
│   ├── jpx.py                 # JPXデータ
│   └── ticker_utils.py        # ティッカー正規化
├── precious_metals_spread/    # ETFとスポット価格の乖離分析
├── credit_spread/             # ジャンク債・トレジャリースプレッド
├── yield_spread/              # イールドスプレッド分析
└── securities_collateral_loan/ # 証券担保ローン最適化
```

## 実装済みユースケース

### precious_metals_spread（貴金属スプレッド）
ETF（1540, 1541, 1542, 1543）とスポット価格の乖離を監視。裁定取引機会を検出。

### credit_spread（クレジットスプレッド）
ジャンク債（HYG, JNK）とトレジャリー（TLT）のスプレッドを分析。リスクオン/オフシグナル。

### yield_spread（イールドスプレッド）
イールドカーブのスプレッド（10Y-2Y等）を監視。景気循環・リセッション予測。

### securities_collateral_loan（証券担保ローン）
証券担保ローンのリスク分析とポートフォリオ最適化。2つのモード：

- **手動モード**: 指定した担保資産でLTV・補充ライン・ロスカット分析
- **最適化モード**: 投信協会全ETF（~300銘柄）から最適担保構成を自動生成

最適化制約：
- 個別銘柄ウェイト: 5-35%
- カテゴリ別ウェイト: ≤50%
- ポートフォリオボラティリティ: ≤12%
- 目的関数: w1×シャープ比 - w2×ボラティリティ

## 実行方法

```bash
uv run -m ai_trading_crew.use_case_runner precious_metals_spread --config config/use_cases/precious_metals_spread.yaml
uv run -m ai_trading_crew.use_case_runner credit_spread --config config/use_cases/credit_spread.yaml
uv run -m ai_trading_crew.use_case_runner yield_spread --config config/use_cases/yield_spread.yaml
uv run -m ai_trading_crew.use_case_runner securities_collateral_loan --config config/use_cases/securities_collateral_loan.yaml
```

## 新規ユースケース追加

1. `use_cases/{new_use_case}/` ディレクトリ作成
2. `BaseUseCase` 継承クラス実装:
   ```python
   from ai_trading_crew.use_cases.base import BaseUseCase

   class NewUseCase(BaseUseCase):
       def run(self):
           # 実装
   ```
3. `registry.py` に登録:
   ```python
   "new_use_case": "ai_trading_crew.use_cases.new_use_case.use_case:NewUseCase"
   ```
4. `config/use_cases/{new_use_case}.yaml` 作成
5. 実行: `uv run -m ai_trading_crew.use_case_runner new_use_case --config ...`

## 標準モジュール構成テンプレート

各ユースケースは以下のモジュールで構成（省略可能）:

- `config.py`: パラメータ・設定クラス
- `data_pipeline.py`: データ取得・前処理
- `analysis.py`: 計算・分析ロジック
- `reporting.py`: レポート生成
- `insights.py`: AI解説生成
- `use_case.py`: BaseUseCase実装（エントリーポイント）

## データフロー

```
Config YAML
 ↓
use_case_runner.py (CLI引数パース)
 ↓
registry.py (ユースケースクラス取得)
 ↓
BaseUseCase.run() (実装クラス)
 ↓
data_pipeline → analysis → reporting → insights
 ↓
resources/data/use_cases/{use_case}/ (キャッシュ)
 ↓
output/use_cases/{use_case}/{YYYYMMDD}/ (レポート)
```

## データストレージパターン

- **Raw data cache**: `resources/data/use_cases/{use_case}/raw/*.parquet`
- **Processed data**: `resources/data/use_cases/{use_case}/processed/*.parquet`
- **Reports**: `output/use_cases/{use_case}/{YYYYMMDD}/*.md`

Parquet形式でキャッシュしAPI呼び出しを最小化。
