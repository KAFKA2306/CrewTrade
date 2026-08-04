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


class TreasuryYieldCurveSource:
    name = "us_treasury"
    URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        self.client = HttpClient(
            user_agent=str(config.get("user_agent", "CrewTrade data-platform")),
            min_interval_seconds=float(config.get("min_interval_seconds", 0.5)),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        years = [int(value) for value in self.config.get("years", [])]
        if not years:
            years = [pd.Timestamp.utcnow().year]
        rows: list[dict[str, object]] = []
        raw_documents: list[dict[str, str]] = []
        latest_url = self.URL
        latest_retrieved_at = None
        for year in sorted(set(years)):
            payload = self.client.get(
                self.URL,
                params={
                    "data": "daily_treasury_yield_curve",
                    "field_tdr_date_value": year,
                },
            )
            rows.extend(parse_treasury_yield_xml(payload.body))
            raw_documents.append(
                {
                    "year": str(year),
                    "url": payload.url,
                    "body_base64": base64.b64encode(payload.body).decode("ascii"),
                }
            )
            latest_url = payload.url
            latest_retrieved_at = payload.retrieved_at
        frame = pd.DataFrame.from_records(rows)
        return [
            DatasetBatch(
                dataset=str(
                    self.config.get("dataset", "treasury_par_yield_curve")
                ),
                source=self.name,
                frame=frame,
                primary_key=("observation_date", "tenor"),
                source_url=latest_url,
                raw_payload=json.dumps(
                    {"documents": raw_documents}, ensure_ascii=False, sort_keys=True
                ).encode("utf-8"),
                content_type="application/json",
                retrieved_at=latest_retrieved_at
                if latest_retrieved_at is not None
                else pd.Timestamp.utcnow().to_pydatetime(),
                metadata={"years": years, "curve_type": "par_yield"},
            )
        ]


def parse_treasury_yield_xml(payload: bytes) -> list[dict[str, object]]:
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
        for field, tenor in _TENOR_FIELDS.items():
            value_text = values.get(field)
            if not value_text:
                continue
            rows.append(
                {
                    "observation_date": observation_date,
                    "tenor": tenor,
                    "value": float(value_text),
                    "unit": "percent",
                    "curve_type": "daily_treasury_par_yield_curve",
                }
            )
    return rows


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]
