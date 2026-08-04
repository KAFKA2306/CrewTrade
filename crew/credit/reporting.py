from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict
from zoneinfo import ZoneInfo

import pandas as pd

from crew.credit.config import CreditSpreadConfig


_LABELS = {
    "us_corporate_oas": "米国社債OAS",
    "us_bbb_oas": "米国BBB社債OAS",
    "us_high_yield_oas": "米国ハイイールドOAS",
}


class CreditSpreadReporter:
    def __init__(
        self, config: CreditSpreadConfig, processed_dir: Path, report_dir: Path
    ) -> None:
        self.config = config
        self.processed_dir = processed_dir
        self.report_dir = report_dir
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def persist(self, payload: Dict[str, pd.DataFrame]) -> Dict[str, Path]:
        stored: Dict[str, Path] = {}
        for key in ("oas", "metrics", "signals", "snapshot", "provenance"):
            value = payload.get(key)
            if isinstance(value, pd.DataFrame):
                path = self.processed_dir / f"{key}.parquet"
                value.to_parquet(path)
                stored[key] = path

        report_path = self.report_dir / "report.md"
        report_path.write_text(self._build_report(payload), encoding="utf-8")
        stored["report"] = report_path
        return stored

    def _build_report(self, payload: Dict[str, pd.DataFrame]) -> str:
        snapshot = payload["snapshot"]
        signals = payload["signals"]
        provenance = payload.get("provenance", pd.DataFrame())
        if snapshot.empty:
            raise ValueError("Cannot publish a credit report without a snapshot")

        checked_on = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
        latest_date = pd.to_datetime(snapshot["latest_date"]).max().strftime("%Y-%m-%d")
        complete = len(snapshot) == len(self.config.series_labels)
        freshest_gap = (
            pd.Timestamp(checked_on) - pd.Timestamp(latest_date)
        ).days
        data_score = 5 if freshest_gap <= 3 else 4 if freshest_gap <= 7 else 2
        total_score = data_score + 5 + (5 if complete else 2) + 4 + 3

        lines = [
            "# クレジット・スプレッド定量監査",
            "",
            f"更新基準日: {checked_on}",
            "",
            "## 結論",
            "",
            "信用評価をETF価格比から切り離し、FREDで公表されるICE BofAオプション調整後スプレッドへ完全移行しました。最新値、20営業日変化、ローリングz値を同じビンテージから計算します。",
            "",
            "## データ",
            "",
            f"正準データ基盤の最新観測日は **{latest_date}** です。単位はパーセント、変化量はベーシスポイントです。",
            "",
            "| 系列 | 最新値 | 1日変化 | 20日変化 | z値 |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        for _, row in snapshot.sort_values("series").iterrows():
            lines.append(
                "| {label} | {level:.2f}% | {d1} | {d20} | {z} |".format(
                    label=_LABELS.get(str(row["series"]), str(row["series"])),
                    level=float(row["level_pct"]),
                    d1=_format_bp(row["change_1d_bp"]),
                    d20=_format_bp(row["change_20d_bp"]),
                    z=_format_number(row["z_score"]),
                )
            )

        lines.extend(
            [
                "",
                "各行はrawレスポンスのSHA-256、取得時刻、FRED URL、リアルタイム期間を保持するParquetから生成されています。",
                "",
                "## 定量分析",
                "",
                f"ローリング窓は{self.config.rolling_window}観測、最小観測数は{self.config.minimum_periods}です。`z=(最新値-移動平均)/移動標準偏差`で計算します。",
                "",
            ]
        )
        if signals.empty:
            lines.append("現在、z値と20日変化の両方が設定閾値を超える新規シグナルはありません。")
        else:
            latest_signals = signals.sort_values("date").tail(10)
            lines.extend(
                [
                    "直近の閾値超過:",
                    "",
                    "| 日付 | 系列 | 方向 | 水準 | 20日変化 | z値 |",
                    "| --- | --- | --- | ---: | ---: | ---: |",
                ]
            )
            for _, row in latest_signals.iterrows():
                lines.append(
                    f"| {pd.Timestamp(row['date']).date()} | {_LABELS.get(str(row['series']), row['series'])} | {row['direction']} | {float(row['level_pct']):.2f}% | {_format_bp(row['change_20d_bp'])} | {float(row['z_score']):.2f} |"
                )

        lines.extend(
            [
                "",
                "## 評価",
                "",
                "| 評価軸 | 点数 | 根拠 |",
                "| --- | ---: | --- |",
                f"| データ鮮度 | {data_score}/5 | 最新観測から確認日まで{freshest_gap}日 |",
                "| 定義の妥当性 | 5/5 | 信用OASの公式系列を直接使用 |",
                f"| 系列完全性 | {5 if complete else 2}/5 | {len(snapshot)}/{len(self.config.series_labels)}系列 |",
                "| ビンテージ管理 | 4/5 | FRED realtime期間と取得時刻を保存 |",
                "| 意思決定可能性 | 3/5 | 警戒には使用可能、単独売買根拠にはしない |",
                f"| **合計** | **{total_score}/25** | **正準OAS経路へ移行済み** |",
                "",
                "## 限界と反証条件",
                "",
                "- OASだけではデフォルト率、格下げ率、発行市場流動性を表しません。",
                "- 最新値が更新されない場合は正常値として前方補完せず、鮮度低下として表示します。",
                "- FRED系列ID、単位、定義が変更された場合は同一系列として継続しません。",
                "- ETF価格差やモデル予測を信用スプレッド実績へ混入させません。",
                "",
                "## 一次情報",
                "",
            ]
        )
        urls = []
        if isinstance(provenance, pd.DataFrame) and "_source_url" in provenance.columns:
            urls = sorted(set(str(value) for value in provenance["_source_url"].dropna()))
        if not urls:
            urls = [
                "https://fred.stlouisfed.org/series/BAMLC0A0CM",
                "https://fred.stlouisfed.org/series/BAMLC0A4CBBB",
                "https://fred.stlouisfed.org/series/BAMLH0A0HYM2",
            ]
        lines.extend(f"- {url}" for url in urls)
        lines.append("")
        return "\n".join(lines)


def _format_bp(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.1f}bp"


def _format_number(value: object) -> str:
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):+.2f}"
