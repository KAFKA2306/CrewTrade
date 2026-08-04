from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from zoneinfo import ZoneInfo

import pandas as pd


_METRIC_LABELS = {
    "revenue": "売上高",
    "operating_income": "営業利益",
    "operating_cash_flow": "営業キャッシュフロー",
    "capital_expenditure": "設備投資",
    "free_cash_flow": "会社開示FCF",
    "remaining_performance_obligation": "残存履行義務",
    "unmapped": "未マッピングSEC fact",
}


class OracleEarningsReporter:
    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def produce_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        report = self._build_report(payload)
        output_path = self.report_dir / "report.md"
        output_path.write_text(report, encoding="utf-8")
        for key in ("filing_snapshot", "fact_snapshot", "derived_fcf", "coverage"):
            value = payload.get(key)
            if isinstance(value, pd.DataFrame):
                value.to_parquet(self.report_dir / f"{key}.parquet", index=False)
        return {"report_content": report, "report_file": str(output_path)}

    def _build_report(self, payload: Dict[str, Any]) -> str:
        filings = _frame(payload, "filing_snapshot")
        facts = _frame(payload, "fact_snapshot")
        derived_fcf = _frame(payload, "derived_fcf", required=False)
        coverage = _frame(payload, "coverage")
        if filings.empty or facts.empty:
            raise ValueError("Oracle report requires SEC filing and fact snapshots")

        checked_on = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
        latest_filing = pd.to_datetime(filings["filing_date"]).max()
        latest_fact_filed = pd.to_datetime(facts["filed_date"]).max()
        coverage_ratio = float(coverage.iloc[0]["coverage_ratio"])
        projection_enabled = bool(coverage.iloc[0]["model_projection_enabled"])
        freshness_days = (pd.Timestamp(checked_on) - latest_filing.normalize()).days
        freshness_score = 5 if freshness_days <= 45 else 4 if freshness_days <= 90 else 2
        coverage_score = 5 if coverage_ratio >= 0.8 else 3 if coverage_ratio >= 0.5 else 1
        total_score = freshness_score + 5 + coverage_score + 4 + 4

        lines = [
            "# Oracle実績・設備投資回収監査",
            "",
            f"更新基準日: {checked_on}",
            "",
            "## 結論",
            "",
            "Oracle分析の実績入力を静的YAMLからSEC EDGAR提出履歴とXBRL Company Factsへ切り替えました。モデル予測は既定で停止し、会社実績、提出日時、報告期間、独自導出値を分離します。",
            "",
            "## データ",
            "",
            f"最新の対象提出日は **{latest_filing.date()}**、最新factの提出日は **{latest_fact_filed.date()}** です。",
            "",
            "### 最新提出書類",
            "",
            "| Form | 提出日 | 報告対象日 | アクセッション番号 |",
            "| --- | --- | --- | --- |",
        ]
        for _, row in filings.sort_values("form").iterrows():
            report_date = (
                pd.Timestamp(row["report_date"]).date()
                if not pd.isna(row["report_date"])
                else "—"
            )
            lines.append(
                f"| {row['form']} | {pd.Timestamp(row['filing_date']).date()} | {report_date} | `{row['accession_number']}` |"
            )

        lines.extend(
            [
                "",
                "### 最新XBRL facts",
                "",
                "| 指標 | Concept | 期間末 | Form | 単位 | 値 |",
                "| --- | --- | --- | --- | --- | ---: |",
            ]
        )
        for _, row in facts.sort_values(["metric", "concept"]).iterrows():
            end_date = (
                pd.Timestamp(row["end_date"]).date()
                if not pd.isna(row["end_date"])
                else "—"
            )
            lines.append(
                f"| {_METRIC_LABELS.get(str(row['metric']), row['metric'])} | `{row['concept']}` | {end_date} | {row['form']} | {row['unit']} | {_format_value(row['value'], row['unit'])} |"
            )

        lines.extend(
            [
                "",
                "## 定量分析",
                "",
                f"設定した重要指標のXBRL充足率は **{coverage_ratio:.0%}** です。Company Factsの同一conceptでも四半期、累計、通期、単位、修正提出が異なるため、期間末と提出日を固定して比較します。",
                "",
            ]
        )
        if derived_fcf.empty:
            lines.append(
                "営業キャッシュフローと設備投資の同一期間factが揃わないため、独自FCFを生成していません。"
            )
        else:
            latest = derived_fcf.iloc[0]
            lines.extend(
                [
                    "同一期間の営業キャッシュフローと設備投資から導出した参考FCF:",
                    "",
                    "| 期間末 | 営業CF | 設備投資 | 導出FCF | 単位 |",
                    "| --- | ---: | ---: | ---: | --- |",
                    f"| {pd.Timestamp(latest['end_date']).date()} | {_format_value(latest['operating_cash_flow'], latest['unit'])} | {_format_value(latest['capital_expenditure'], latest['unit'])} | {_format_value(latest['derived_free_cash_flow'], latest['unit'])} | {latest['unit']} |",
                    "",
                    "このFCFはSEC factsからの独自導出値であり、Oracleが定義・公表した指標とは区別します。",
                ]
            )

        lines.extend(
            [
                "",
                "## 評価",
                "",
                "| 評価軸 | 点数 | 根拠 |",
                "| --- | ---: | --- |",
                f"| 開示鮮度 | {freshness_score}/5 | 最新提出から{freshness_days}日 |",
                "| 一次資料 | 5/5 | SEC accessionとCompany Factsを直接使用 |",
                f"| 指標充足 | {coverage_score}/5 | 設定指標の{coverage_ratio:.0%}を取得 |",
                "| 時点管理 | 4/5 | 報告期間、提出日、取得時刻、raw hashを保持 |",
                "| 予測分離 | 4/5 | モデル予測を既定停止し実績と分離 |",
                f"| **合計** | **{total_score}/25** | **SEC正準経路へ移行済み** |",
                "",
                "## 限界と反証条件",
                "",
                "- SEC Company Factsは会社IR資料の全ての非GAAP指標やクラウド区分を含みません。",
                "- RPOの会社固有conceptが取得できない場合、推測値で補完しません。",
                "- 四半期値と年初来累計値を期間調整せず比較しません。",
                "- 修正提出があれば旧factを上書きせず、アクセッション番号単位で保持します。",
                f"- モデル予測は現在 **{'有効' if projection_enabled else '停止'}** であり、実績として表示しません。",
                "",
                "## 一次情報",
                "",
            ]
        )
        urls = _source_urls(payload)
        lines.extend(f"- {url}" for url in urls)
        lines.append("")
        return "\n".join(lines)


def _frame(payload: Dict[str, Any], key: str, *, required: bool = True) -> pd.DataFrame:
    value = payload.get(key)
    if isinstance(value, pd.DataFrame):
        return value
    if required:
        raise TypeError(f"Expected DataFrame payload: {key}")
    return pd.DataFrame()


def _format_value(value: object, unit: object) -> str:
    numeric = float(value)
    unit_text = str(unit)
    if unit_text == "USD":
        magnitude = abs(numeric)
        if magnitude >= 1_000_000_000:
            return f"${numeric / 1_000_000_000:,.2f}B"
        if magnitude >= 1_000_000:
            return f"${numeric / 1_000_000:,.2f}M"
    return f"{numeric:,.2f}"


def _source_urls(payload: Dict[str, Any]) -> list[str]:
    urls: set[str] = set()
    for key in ("filings", "facts", "filing_snapshot", "fact_snapshot"):
        value = payload.get(key)
        if isinstance(value, pd.DataFrame) and "_source_url" in value.columns:
            urls.update(str(item) for item in value["_source_url"].dropna())
    return sorted(urls) or [
        "https://data.sec.gov/submissions/CIK0001341439.json",
        "https://data.sec.gov/api/xbrl/companyfacts/CIK0001341439.json",
    ]
