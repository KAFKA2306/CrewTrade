# Crew Package

投資戦略分析・リスク管理のための拡張可能なユースケースフレームワーク。

## ディレクトリ構造

```
crew/
├── base.py           # BaseUseCase抽象クラス
├── registry.py       # ユースケース登録
├── use_case_runner.py
├── clients/          # 共有データクライアント
├── imura/            # 井村ファンド分析
├── oracle/           # Oracle収益予測
├── credit/           # クレジットスプレッド
├── yields/           # イールドスプレッド
└── loan/             # 証券担保ローン
```

## 実行方法

```bash
task run:imura
uv run -m crew.use_case_runner imura --config config/use_cases/imura.yaml
```

## 新規ユースケース追加

1. `crew/{new_use_case}/` ディレクトリ作成
2. `BaseUseCase`継承クラス実装
3. `registry.py`に登録
4. `config/use_cases/{new_use_case}.yaml`作成

## モジュール構成

- `config.py`: パラメータ
- `data_pipeline.py`: データ取得
- `analysis.py`: 計算ロジック
- `reporting.py`: レポート生成
