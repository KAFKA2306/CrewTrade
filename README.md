# Crew

Python 3.11+ | crewAI

## 構造

```
crew/          # メインパッケージ
config/        # YAML設定
output/        # レポート出力
resources/     # データキャッシュ
```

## セットアップ

```bash
uv sync
```

## 実行

```bash
task process:all          # 全実行
task fetch:imura          # データ取得
task analyze:imura        # 分析
```

## ユースケース

| 名前 | 設定 |
|------|------|
| imura | config/use_cases/imura.yaml |
| oracle | config/use_cases/oracle.yaml |
| credit | config/use_cases/credit.yaml |
| etf | - |
| loan | config/use_cases/loan.yaml |
| metals | config/use_cases/metals.yaml |
| portfolio | config/use_cases/portfolio.yaml |
| yields | config/use_cases/yields.yaml |

## 開発

```bash
task lint
task format
task test
```