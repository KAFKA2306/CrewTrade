# Output Directory

AITradingCrewが生成する全レポート・分析結果の出力先。

## ディレクトリ構造

```
output/
├── backtests/                 # バックテスト結果
├── backtests_debug/           # バックテストデバッグ情報
└── use_cases/                 # ユースケース別レポート
    ├── precious_metals_spread/
    ├── credit_spread/
    ├── yield_spread/
    └── securities_collateral_loan/
        └── {YYYYMMDD}/        # 日次ディレクトリ
            ├── *_report.md
            └── *_insights.md
```

## ファイル形式

### レポートファイル (`*_report.md`)
分析結果の構造化レポート。数値テーブル・統計・チャート等を含む。

### インサイトファイル (`*_insights.md`)
LLMによるAI解説。レポートを解釈し実行可能なインサイトを生成。

## 日次ディレクトリ命名規則

`{YYYYMMDD}` 形式（例: 20251031）で日次分離。同一ユースケースの時系列追跡が可能。

## ユースケース別出力例

### precious_metals_spread
- `precious_metals_spread_report.md`: ETFとスポット価格の乖離分析
- `precious_metals_spread_insights.md`: 裁定取引機会のAI解説

### credit_spread
- `credit_spread_report.md`: ジャンク債/トレジャリースプレッド分析
- `credit_spread_insights.md`: リスクオン/オフシグナル解説

### yield_spread
- `yield_spread_report.md`: イールドカーブ分析
- `yield_spread_insights.md`: 景気循環ステージ解説

### securities_collateral_loan
- `securities_collateral_loan_report.md`: 証券担保ローンリスク分析
  - LTV、補充ライン、ロスカットライン
  - 最適化モード時：ETFスクリーニング結果、最適ポートフォリオ
- `securities_collateral_loan_insights.md`: リスクシナリオ・推奨アクション

## データ永続化

- **コミット対象外**: `output/` ディレクトリ全体は `.gitignore` で除外
- **ローカル保持**: 生成されたレポートはローカル環境でのみ管理
- **再生成可能**: 全レポートは設定ファイルから再実行・再生成可能

## アクセス方法

レポートは標準Markdownビューアで閲覧可能：

```bash
cat output/use_cases/securities_collateral_loan/20251031/securities_collateral_loan_report.md

less output/use_cases/credit_spread/20251031/credit_spread_insights.md
```

VSCode等のエディタでプレビュー表示推奨。
