from __future__ import annotations

import base64
import json
from typing import Any, Mapping, Sequence
from xml.etree import ElementTree

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.http import HttpClient


_TENOR_FIELDS = {
    "BC_1MONTH": "1M",
    "BC_1_5MONTH": "1.5M",
    "BC_2MONTH": "2M",
    "BC_3MONTH": "3M",
    "BC_4MONTH": "4M",
    "BC_6MONTH": "6M",
    "BC_1YEAR": "1Y",
    "BC_2YEAR": "2Y",
    "BC_3YEAR": "3Y",
    "BC_5YEAR": "5Y",
    "BC_7YEAR": "7Y",
    "BC_10YEAR": "10Y",
    "BC_20YEAR": "20Y",
    "BC_30YEAR": "30Y",
}

_REAL_TENOR_FIELDS = {
    "BC_5YEAR": "5Y",
    "BC_7YEAR": "7Y",
    "BC_10YEAR": "10Y",
    "BC_20YEAR": "20Y",
    "BC_30YEAR": "30Y",
}


class TreasuryYieldCurveSource:
    name = "us_treasury"
    NOMINAL_URL_TEMPLATE = (
        "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
        "pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value={year}"
    )
    REAL_URL_TEMPLATE = (
        "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
        "pages/xml?data=daily_treasury_real_yield_curve&field_tdr_date_value={year}"
    )

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        self.client = HttpClient(
            user_agent=str(config.get("user_agent", "CrewTrade data-platform")),
            min_interval_seconds=float(config.get("min_interval_seconds", 0.5)),
            timeout_seconds=float(config.get("timeout_seconds", 60.0)),
            max_attempts=int(config.get("max_attempts", 3)),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        years = {int(value) for value in self.config.get("years", [])}
        if not years:
            years = {pd.Timestamp.utcnow().year}
        sorted_years = sorted(years)

        nominal_payloads = [
            self.client.get(self.NOMINAL_URL_TEMPLATE.format(year=year))
            for year in sorted_years
        ]
        real_payloads = [
            self.client.get(self.REAL_URL_TEMPLATE.format(year=year))
            for year in sorted_years
        ]
        nominal = pd.DataFrame.from_records(
            row
            for payload in nominal_payloads
            for row in parse_treasury_yield_xml(
                payload.body,
                tenor_fields=_TENOR_FIELDS,
                curve_type="daily_treasury_par_yield_curve",
            )
        )
        real = pd.DataFrame.from_records(
            row
            for payload in real_payloads
            for row in parse_treasury_yield_xml(
                payload.body,
                tenor_fields=_REAL_TENOR_FIELDS,
                curve_type="daily_treasury_par_real_yield_curve",
            )
        )
        nominal = _filter_years(nominal, years)
        real = _filter_years(real, years)
        if nominal.empty:
            raise ValueError(f"Treasury nominal feed has no rows for {sorted_years}")
        if real.empty:
            raise ValueError(f"Treasury real feed has no rows for {sorted_years}")

        all_payloads = [*nominal_payloads, *real_payloads]
        retrieved_at = max(payload.retrieved_at for payload in all_payloads)
        retrieval_date = pd.Timestamp(retrieved_at).date()
        rates_macro = build_rates_macro(
            nominal,
            real,
            retrieval_date=retrieval_date,
        )
        if rates_macro.empty:
            raise ValueError("Treasury nominal and real curves have no comparable dates")

        raw_payload = json.dumps(
            {
                "documents": [
                    *[
                        {
                            "curve_type": "nominal",
                            "year": year,
                            "url": payload.url,
                            "body_base64": base64.b64encode(payload.body).decode(
                                "ascii"
                            ),
                        }
                        for year, payload in zip(
                            sorted_years, nominal_payloads, strict=True
                        )
                    ],
                    *[
                        {
                            "curve_type": "real",
                            "year": year,
                            "url": payload.url,
                            "body_base64": base64.b64encode(payload.body).decode(
                                "ascii"
                            ),
                        }
                        for year, payload in zip(sorted_years, real_payloads, strict=True)
                    ],
                ]
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
        common_metadata = {
            "years": sorted_years,
            "retrieval_mode": "official_year_xml_snapshots",
            "point_in_time_vintage": False,
            "http_request_count": len(all_payloads),
            "source_urls": [payload.url for payload in all_payloads],
        }
        return [
            DatasetBatch(
                dataset=str(
                    self.config.get("dataset", "treasury_par_yield_curve")
                ),
                source=self.name,
                frame=nominal,
                primary_key=("observation_date", "tenor"),
                source_url=nominal_payloads[-1].url,
                raw_payload=raw_payload,
                content_type="application/json",
                retrieved_at=retrieved_at,
                metadata={**common_metadata, "curve_type": "par_yield"},
            ),
            DatasetBatch(
                dataset=str(
                    self.config.get(
                        "real_dataset", "treasury_par_real_yield_curve"
                    )
                ),
                source=self.name,
                frame=real,
                primary_key=("observation_date", "tenor"),
                source_url=real_payloads[-1].url,
                raw_payload=raw_payload,
                content_type="application/json",
                retrieved_at=retrieved_at,
                metadata={**common_metadata, "curve_type": "par_real_yield"},
            ),
            DatasetBatch(
                dataset=str(self.config.get("rates_dataset", "rates_macro")),
                source=self.name,
                frame=rates_macro,
                primary_key=(
                    "series_id",
                    "observation_date",
                    "realtime_start",
                    "realtime_end",
                ),
                source_url=nominal_payloads[-1].url,
                raw_payload=raw_payload,
                content_type="application/json",
                retrieved_at=retrieved_at,
                metadata={
                    **common_metadata,
                    "derived_series": ["us_10y_breakeven"],
                    "source_series": [
                        "us_2y",
                        "us_10y",
                        "us_30y",
                        "us_10y_real",
                    ],
                },
            ),
        ]


def parse_treasury_yield_xml(
    payload: bytes,
    *,
    tenor_fields: Mapping[str, str] | None = None,
    curve_type: str = "daily_treasury_par_yield_curve",
) -> list[dict[str, object]]:
    fields = dict(tenor_fields or _TENOR_FIELDS)
    root = ElementTree.fromstring(payload)
    rows: list[dict[str, object]] = []
    for element in root.iter():
        if _local_name(element.tag) != "properties":
            continue
        values = {
            _local_name(child.tag): (child.text or "").strip()
            for child in list(element)
        }
        date_text = values.get("NEW_DATE") or values.get("Id")
        if not date_text:
            continue
        observation_date = pd.to_datetime(date_text).date()
        for field, tenor in fields.items():
            value_text = values.get(field)
            if not value_text:
                continue
            rows.append(
                {
                    "observation_date": observation_date,
                    "tenor": tenor,
                    "value": float(value_text),
                    "unit": "percent",
                    "curve_type": curve_type,
                }
            )
    return rows


def build_rates_macro(
    nominal: pd.DataFrame,
    real: pd.DataFrame,
    *,
    retrieval_date: object,
) -> pd.DataFrame:
    required_nominal = {"2Y": "us_2y", "10Y": "us_10y", "30Y": "us_30y"}
    nominal_subset = nominal[nominal["tenor"].isin(required_nominal)].copy()
    nominal_subset["label"] = nominal_subset["tenor"].map(required_nominal)
    real_10y = real[real["tenor"] == "10Y"].copy()
    real_10y["label"] = "us_10y_real"

    long_rows = pd.concat([nominal_subset, real_10y], ignore_index=True)
    snapshot_date = pd.to_datetime(retrieval_date).date()
    long_rows["series_id"] = long_rows["label"].map(
        {
            "us_2y": "TREASURY_NOMINAL_2Y",
            "us_10y": "TREASURY_NOMINAL_10Y",
            "us_30y": "TREASURY_NOMINAL_30Y",
            "us_10y_real": "TREASURY_REAL_10Y",
        }
    )
    long_rows["realtime_start"] = snapshot_date
    long_rows["realtime_end"] = snapshot_date
    long_rows["units"] = "Percent"
    long_rows["title"] = long_rows["label"].map(
        {
            "us_2y": "Daily Treasury Par Yield Curve Rate, 2-Year",
            "us_10y": "Daily Treasury Par Yield Curve Rate, 10-Year",
            "us_30y": "Daily Treasury Par Yield Curve Rate, 30-Year",
            "us_10y_real": "Daily Treasury Par Real Yield Curve Rate, 10-Year",
        }
    )

    nominal_10y = nominal[nominal["tenor"] == "10Y"][
        ["observation_date", "value"]
    ].rename(columns={"value": "nominal_10y"})
    real_10y_values = real[real["tenor"] == "10Y"][
        ["observation_date", "value"]
    ].rename(columns={"value": "real_10y"})
    breakeven = nominal_10y.merge(
        real_10y_values, on="observation_date", how="inner"
    )
    breakeven["value"] = breakeven["nominal_10y"] - breakeven["real_10y"]
    breakeven["series_id"] = "TREASURY_DERIVED_10Y_BREAKEVEN"
    breakeven["label"] = "us_10y_breakeven"
    breakeven["realtime_start"] = snapshot_date
    breakeven["realtime_end"] = snapshot_date
    breakeven["units"] = "Percent"
    breakeven["title"] = "10-Year Nominal Minus 10-Year Real Treasury Yield"

    columns = [
        "series_id",
        "label",
        "observation_date",
        "value",
        "realtime_start",
        "realtime_end",
        "units",
        "title",
    ]
    result = pd.concat(
        [long_rows[columns], breakeven[columns]], ignore_index=True
    )
    return result.sort_values(["observation_date", "label"]).reset_index(drop=True)


def _filter_years(frame: pd.DataFrame, years: set[int]) -> pd.DataFrame:
    if frame.empty:
        return frame
    observations = pd.to_datetime(frame["observation_date"])
    years_mask = observations.year.isin(years)
    return frame[years_mask].reset_index(drop=True)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]
