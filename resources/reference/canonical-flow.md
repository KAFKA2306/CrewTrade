# CrewTrade canonical flow

CrewTrade の正準ユーザーフローは次の1本とする。

```text
一次情報 / 統制された非公開入力
  -> executable dataset contract
  -> immutable raw + SHA-256
  -> normalized bronze Parquet
  -> DuckDB catalogue / quality / lineage
  -> deterministic gold views
  -> use-case analysis
  -> Pages / report
```

## Source of truth

- 入力・利用権・dataset契約: `config/data_platform.yaml`
- use-case状態: `config/use_case_data_status.yaml`
- 正準処理: `crew/data_platform/`
- 正準分析: `crew/yields/` 等のuse-case package
- 公開成果: `output/use_cases/` と生成済み `docs/`

`docs/` は `web/build_static.py` が再生成する公開成果物であり、手書き設計文書の source of truth にはしない。生成済みPages、画像、調査用スクリプト、外部weekly research workflowもsource of truthにしない。

## Executable data contracts

adapterが返すdatasetは、保存前に `config/data_platform.yaml` の同名contractを必須とする。contractがないdataset、またはcontractと一致しないdatasetはbronzeへ保存しない。

現在の実装済みadapterが生成し得る8 datasetはすべてcontract対象とする。

- `treasury_par_yield_curve`
- `treasury_par_real_yield_curve`
- `rates_macro`
- `governed_source_registry`
- `jpx_etf_master`
- `sec_filings`
- `sec_company_facts`
- `sec_13f_holdings`

最低限、source、primary key、列集合、型、nullable、allowed/range/pattern、required metadataを機械検証する。鮮度を定義できるdatasetはfreshnessも検査する。grain、revision policy、redistributionはcontractに明示し、意味・更新・利用権を列schemaから切り離さない。

新しいadapter/datasetはcontractと契約試験を同じ変更で追加する。`union_by_name`等でschema driftを吸収して保存することを正準経路では認めない。

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
- contractを別ファイル群へ分散しない。正準registryは `config/data_platform.yaml` の1か所だけに置く。

## Repository ratchet

CIは少なくとも以下を直接検査する。

- 正準設定・処理・公開入口と、この正準契約が存在すること
- 実装済みdatasetのcontract coverageが100%であること
- schema drift、PK不整合、型・値域・列挙・pattern違反がfail closedになること
- 廃止済みweekly research workflowが再導入されていないこと
- root直下のChronos試験script / test plotが再導入されていないこと

新しい抽象化・workflow・データコピーは、既存の正準線では表現できない実利用要件が確認できる場合だけ追加する。
