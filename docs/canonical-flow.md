# CrewTrade canonical flow

CrewTrade の正準ユーザーフローは次の1本とする。

```text
一次情報 / 統制された非公開入力
  -> immutable raw + SHA-256
  -> normalized bronze Parquet
  -> DuckDB catalogue / quality / lineage
  -> deterministic gold views
  -> use-case analysis
  -> Pages / report
```

## Source of truth

- 入力契約: `config/data_platform.yaml`
- use-case状態: `config/use_case_data_status.yaml`
- 正準処理: `crew/data_platform/`
- 正準分析: `crew/yields/` 等のuse-case package
- 公開成果: `output/use_cases/` と `docs/`

生成済みPages、画像、調査用スクリプト、外部weekly research workflowはsource of truthにしない。

## 主要KPI

1. 正準データ取得・品質検査の成功率
2. 公開データの鮮度
3. 推測補完なしで利用可能な成果物数

実測できないKPIを推定値で埋めない。

## Non-goals

- 正準データ基盤と独立した実験用予測パイプラインを増やさない。
- 一度きりのresearch scriptや生成画像をrepository rootへ保存しない。
- 外部reusable workflowによる定期調査をproduction data pathと混在させない。
- 利用権・provenance・比較可能性が不足する値を推測で公開しない。

## Repository ratchet

CIは少なくとも以下を直接検査する。

- 正準設定・処理・公開入口が存在すること
- 廃止済みweekly research workflowが再導入されていないこと
- root直下のChronos試験script / test plotが再導入されていないこと

新しい抽象化・workflow・データコピーは、既存の正準線では表現できない実利用要件が確認できる場合だけ追加する。
