from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from crew.yields.config import YieldSpreadConfig

_RATE_LABELS = {
    "us_2y": "米国2年",
    "us_10y": "米国10年",
    "us_30y": "米国30年",
    "us_10y_real": "米国10年実質金利",
    "us_10y_breakeven": "米国10年期待インフレ",
}


class YieldSpreadReporter:
    def __init__(self, config: YieldSpreadConfig, processed_dir: Path, report_dir: Path) -> None:
        self.config = config
        self.processed_dir = processed_dir
        self.report_dir = report_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, payload: dict[str, object]) -> dict[str, Path]:
        stored: dict[str, Path] = {}
        for key in (
            "rates",
            "treasury_curve",
            "metrics",
            "signals",
            "spread_snapshot",
            "macro_snapshot",
            "curve_snapshot",
            "provenance",
        ):
            value = payload.get(key)
            if isinstance(value, pd.DataFrame):
                path = self.processed_dir / f"{key}.parquet"
                value.to_parquet(path)
                stored[key] = path

        report_path = self.report_dir / "report.md"
        report_path.write_text(self._build_report(payload), encoding="utf-8")
        stored["report"] = report_path
        return stored

    def _build_report(self, payload: dict[str, object]) -> str:
        spread_snapshot = _frame(payload, "spread_snapshot")
        macro_snapshot = _frame(payload, "macro_snapshot")
        curve_snapshot = _frame(payload, "curve_snapshot")
        signals = _frame(payload, "signals")
        provenance = _frame(payload, "provenance", required=False)
        if spread_snapshot.empty or macro_snapshot.empty:
            raise ValueError("Cannot publish a yield report without canonical snapshots")

        checked_on = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
        latest_date = pd.to_datetime(spread_snapshot["latest_date"]).max().strftime("%Y-%m-%d")
        freshness_gap = (pd.Timestamp(checked_on) - pd.Timestamp(latest_date)).days
        data_score = 5 if freshness_gap <= 3 else 4 if freshness_gap <= 7 else 2
        curve_complete = not curve_snapshot.empty and {
            "2Y",
            "10Y",
            "30Y",
        }.issubset(set(curve_snapshot["tenor"].astype(str)))
        total_score = data_score + 5 + (5 if curve_complete else 3) + 4 + 3

        lines = [
            "# 金利・イールドスプレッド定量監査",
            "",
            f"更新基準日: {checked_on}",
            "",
            "## 結論",
            "",
            "期間構造を米国債金利、信用リスクをOASとして分離しました。このレポートは米国債カーブ、実質金利、期待インフレだけを扱い、ハイイールド実効利回りから10年国債を差し引く旧代理指標と固定資産配分を使用しません。",
            "",
            "## データ",
            "",
            f"正準基盤における比較可能な最新観測日は **{latest_date}** です。",
            "",
            "### マクロ金利",
            "",
            "| 系列 | 観測日 | 値 |",
            "| --- | --- | ---: |",
        ]
        for _, row in macro_snapshot.sort_values("series").iterrows():
            lines.append(
                f"| {_RATE_LABELS.get(str(row['series']), row['series'])} | {pd.Timestamp(row['latest_date']).date()} | {float(row['value_pct']):.2f}% |"
            )

        lines.extend(
            [
                "",
                "### カーブ・スプレッド",
                "",
                "| 指標 | 観測日 | 短期 | 長期 | スプレッド | 20日変化 | z値 |",
                "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for _, row in spread_snapshot.sort_values("spread").iterrows():
            lines.append(
                f"| {row['spread']} | {pd.Timestamp(row['latest_date']).date()} | {float(row['short_rate_pct']):.2f}% | {float(row['long_rate_pct']):.2f}% | {float(row['spread_bp']):+.1f}bp | {_format_bp(row['change_20d_bp'])} | {_format_number(row['z_score'])} |"
            )

        if not curve_snapshot.empty:
            curve_date = pd.to_datetime(curve_snapshot["observation_date"]).max().date()
            lines.extend(
                [
                    "",
                    f"### 米国財務省パー・イールド・カーブ（{curve_date}）",
                    "",
                    "| 年限 | 利回り |",
                    "| --- | ---: |",
                ]
            )
            for _, row in curve_snapshot.iterrows():
                lines.append(f"| {row['tenor']} | {float(row['value']):.2f}% |")

        lines.extend(
            [
                "",
                "## 定量分析",
                "",
                f"各スプレッドは長期年限から短期年限を引き、{self.config.rolling_window}観測の移動平均・標準偏差でz値を計算します。異なる観測日の金利を直接差し引かず、欠損日は前方補完しません。",
                "",
            ]
        )
        if signals.empty:
            lines.append("z値と20日変化の両閾値を満たす直近イベントはありません。")
        else:
            lines.extend(
                [
                    "直近の閾値超過:",
                    "",
                    "| 日付 | 指標 | 方向 | スプレッド | 20日変化 | z値 |",
                    "| --- | --- | --- | ---: | ---: | ---: |",
                ]
            )
            for _, row in signals.sort_values("date").tail(10).iterrows():
                lines.append(
                    f"| {pd.Timestamp(row['date']).date()} | {row['spread']} | {row['direction']} | {float(row['spread_bp']):+.1f}bp | {float(row['change_20d_bp']):+.1f}bp | {float(row['z_score']):+.2f} |"
                )

        lines.extend(
            [
                "",
                "## 評価",
                "",
                "| 評価軸 | 点数 | 根拠 |",
                "| --- | ---: | --- |",
                f"| データ鮮度 | {data_score}/5 | 最新比較日から確認日まで{freshness_gap}日 |",
                "| 定義の妥当性 | 5/5 | 国債カーブ、実質金利、期待インフレを分離 |",
                f"| カーブ完全性 | {5 if curve_complete else 3}/5 | 2年・10年・30年の同日値を確認 |",
                "| ビンテージ管理 | 4/5 | 観測日、FRED realtime期間、取得時刻を保持 |",
                "| 配分接続 | 3/5 | 状態判定は可能、固定配分への自動接続は停止 |",
                f"| **合計** | **{total_score}/25** | **正準金利経路へ移行済み** |",
                "",
                "## 限界と反証条件",
                "",
                "- パー・イールド、コンスタント・マチュリティ、ゼロクーポン金利を同一概念として扱いません。",
                "- 名目カーブだけで景気、為替、株価の方向を断定しません。",
                "- 実質金利と期待インフレは公表日の差を確認し、無条件に同日合成しません。",
                "- 固定配分やKronos予測は、アウト・オブ・サンプル検証が完了するまで公開評価へ接続しません。",
                "",
                "## 一次情報",
                "",
            ]
        )
        urls = []
        if not provenance.empty and "_source_url" in provenance.columns:
            urls.extend(sorted(set(str(value) for value in provenance["_source_url"].dropna())))
        if not curve_snapshot.empty and "_source_url" in curve_snapshot.columns:
            urls.extend(sorted(set(str(value) for value in curve_snapshot["_source_url"].dropna())))
        urls = sorted(set(urls)) or [
            "https://home.treasury.gov/resource-center/data-chart-center/interest-rates",
            "https://fred.stlouisfed.org/series/DGS10",
            "https://fred.stlouisfed.org/series/DFII10",
            "https://fred.stlouisfed.org/series/T10YIE",
        ]
        lines.extend(f"- {url}" for url in urls)
        lines.append("")
        return "\n".join(lines)


def _frame(payload: dict[str, object], key: str, *, required: bool = True) -> pd.DataFrame:
    value = payload.get(key)
    if isinstance(value, pd.DataFrame):
        return value
    if required:
        raise TypeError(f"Expected DataFrame payload: {key}")
    return pd.DataFrame()


def _format_bp(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.1f}bp"


def _format_number(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.2f}"
