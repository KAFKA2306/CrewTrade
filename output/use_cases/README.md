# Use Cases Output

各ユースケースの分析レポート出力ディレクトリ。

## 構造

```
use_cases/
├── precious_metals_spread/
│   └── {YYYYMMDD}/
├── credit_spread/
│   └── {YYYYMMDD}/
├── yield_spread/
│   └── {YYYYMMDD}/
└── securities_collateral_loan/
    └── {YYYYMMDD}/
```

各日次ディレクトリには以下のファイルが生成される：
- `{use_case}_report.md`: 構造化分析レポート
- `{use_case}_insights.md`: AI解説

## ユースケース別詳細

### precious_metals_spread/
ETFとスポット価格の乖離分析レポート。

**主要セクション**:
- 乖離率サマリー
- Z-scoreランキング
- 異常値検出（|Z-score| > 2.0）
- 裁定取引機会

### credit_spread/
ジャンク債/トレジャリースプレッド分析レポート。

**主要セクション**:
- 現在のスプレッド水準
- パーセンタイルランク（過去5年）
- トレンド分析（7日/30日MA）
- リスクオン/オフシグナル

### yield_spread/
イールドカーブスプレッド分析レポート。

**主要セクション**:
- スプレッド一覧（10Y-2Y, 10Y-3M, 30Y-5Y等）
- 逆イールド検出
- Z-score・パーセンタイル
- アロケーション推奨

### securities_collateral_loan/
証券担保ローンリスク分析・最適化レポート。

**主要セクション**:
- ローン概要（LTV, 補充ライン, ロスカットライン）
- 現在の担保構成
- ストレステスト（-10%, -20%, -30%）
- 最適化結果（有効化時）
  - ETFスクリーニング結果
  - 最適ポートフォリオ
  - パフォーマンス予測

## 日次追跡

同一ユースケースを日次実行することで時系列追跡が可能：

```bash
output/use_cases/credit_spread/20251028/credit_spread_report.md
output/use_cases/credit_spread/20251029/credit_spread_report.md
output/use_cases/credit_spread/20251030/credit_spread_report.md
output/use_cases/credit_spread/20251031/credit_spread_report.md
```

過去レポートと比較してトレンド変化を検証。

## データ永続化

このディレクトリは `.gitignore` で除外。生成されたレポートはローカル環境のみで管理。
