from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Mapping, Sequence

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.http import HttpClient


class SecSource:
    name = "sec_edgar"
    DATA_BASE_URL = "https://data.sec.gov"

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        user_agent_env = str(config.get("user_agent_env", "SEC_USER_AGENT"))
        user_agent = os.environ.get(user_agent_env, "").strip()
        if not user_agent:
            raise RuntimeError(
                f"SEC declared user agent is required in {user_agent_env}, "
                "for example 'CrewTrade admin@example.com'."
            )
        self.client = HttpClient(
            user_agent=user_agent,
            min_interval_seconds=max(
                0.12, float(config.get("min_interval_seconds", 0.15))
            ),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        filing_rows: list[dict[str, object]] = []
        fact_rows: list[dict[str, object]] = []
        raw_bundle: dict[str, object] = {"entities": {}}
        latest_url = self.DATA_BASE_URL
        latest_retrieved_at = None

        for entity_name, entity_config in dict(self.config.get("entities", {})).items():
            cik = str(entity_config["cik"]).zfill(10)
            submissions_payload = self.client.get(
                f"{self.DATA_BASE_URL}/submissions/CIK{cik}.json"
            )
            submissions_json = json.loads(submissions_payload.body)
            filing_rows.extend(
                parse_sec_submissions(
                    entity_name=str(entity_name), cik=cik, payload=submissions_json
                )
            )
            entity_raw: dict[str, object] = {"submissions": submissions_json}
            latest_url = submissions_payload.url
            latest_retrieved_at = submissions_payload.retrieved_at

            if bool(entity_config.get("companyfacts", False)):
                facts_payload = self.client.get(
                    f"{self.DATA_BASE_URL}/api/xbrl/companyfacts/CIK{cik}.json"
                )
                facts_json = json.loads(facts_payload.body)
                fact_rows.extend(
                    parse_sec_companyfacts(
                        entity_name=str(entity_name), cik=cik, payload=facts_json
                    )
                )
                entity_raw["companyfacts"] = facts_json
                latest_url = facts_payload.url
                latest_retrieved_at = facts_payload.retrieved_at
            raw_bundle["entities"][entity_name] = entity_raw

        raw_payload = json.dumps(
            raw_bundle, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        retrieved_at = (
            latest_retrieved_at
            if latest_retrieved_at is not None
            else pd.Timestamp.utcnow().to_pydatetime()
        )
        batches: list[DatasetBatch] = []
        if filing_rows:
            batches.append(
                DatasetBatch(
                    dataset="sec_filings",
                    source=self.name,
                    frame=pd.DataFrame.from_records(filing_rows),
                    primary_key=("entity_cik", "accession_number"),
                    source_url=latest_url,
                    raw_payload=raw_payload,
                    content_type="application/json",
                    retrieved_at=retrieved_at,
                    metadata={"entity_count": len(self.config.get("entities", {}))},
                )
            )
        if fact_rows:
            batches.append(
                DatasetBatch(
                    dataset="sec_company_facts",
                    source=self.name,
                    frame=pd.DataFrame.from_records(fact_rows),
                    primary_key=("fact_id",),
                    source_url=latest_url,
                    raw_payload=raw_payload,
                    content_type="application/json",
                    retrieved_at=retrieved_at,
                    metadata={"entity_count": len(self.config.get("entities", {}))},
                )
            )
        return batches


def parse_sec_submissions(
    *, entity_name: str, cik: str, payload: Mapping[str, Any]
) -> list[dict[str, object]]:
    recent = payload.get("filings", {}).get("recent", {})
    accessions = list(recent.get("accessionNumber", []))
    rows: list[dict[str, object]] = []
    for index, accession_number in enumerate(accessions):
        rows.append(
            {
                "entity_name": entity_name,
                "entity_cik": cik,
                "accession_number": accession_number,
                "filing_date": _date_at(recent, "filingDate", index),
                "report_date": _date_at(recent, "reportDate", index),
                "acceptance_datetime": _timestamp_at(
                    recent, "acceptanceDateTime", index
                ),
                "form": _value_at(recent, "form", index),
                "primary_document": _value_at(recent, "primaryDocument", index),
                "primary_doc_description": _value_at(
                    recent, "primaryDocDescription", index
                ),
                "file_number": _value_at(recent, "fileNumber", index),
                "is_xbrl": _value_at(recent, "isXBRL", index),
                "is_inline_xbrl": _value_at(recent, "isInlineXBRL", index),
            }
        )
    return rows


def parse_sec_companyfacts(
    *, entity_name: str, cik: str, payload: Mapping[str, Any]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for taxonomy, concepts in dict(payload.get("facts", {})).items():
        for concept, fact_definition in dict(concepts).items():
            label = fact_definition.get("label")
            description = fact_definition.get("description")
            for unit, observations in dict(fact_definition.get("units", {})).items():
                for observation in observations:
                    canonical = {
                        "entity_cik": cik,
                        "taxonomy": taxonomy,
                        "concept": concept,
                        "unit": unit,
                        "observation": observation,
                    }
                    fact_id = hashlib.sha256(
                        json.dumps(
                            canonical,
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                        ).encode("utf-8")
                    ).hexdigest()
                    rows.append(
                        {
                            "fact_id": fact_id,
                            "entity_name": entity_name,
                            "entity_cik": cik,
                            "taxonomy": taxonomy,
                            "concept": concept,
                            "label": label,
                            "description": description,
                            "unit": unit,
                            "value": observation.get("val"),
                            "start_date": _to_date(observation.get("start")),
                            "end_date": _to_date(observation.get("end")),
                            "filed_date": _to_date(observation.get("filed")),
                            "form": observation.get("form"),
                            "fiscal_year": observation.get("fy"),
                            "fiscal_period": observation.get("fp"),
                            "frame": observation.get("frame"),
                            "accession_number": observation.get("accn"),
                        }
                    )
    return rows


def _value_at(payload: Mapping[str, Any], key: str, index: int) -> object | None:
    values = payload.get(key, [])
    return values[index] if index < len(values) else None


def _date_at(payload: Mapping[str, Any], key: str, index: int) -> object | None:
    return _to_date(_value_at(payload, key, index))


def _timestamp_at(payload: Mapping[str, Any], key: str, index: int) -> object | None:
    value = _value_at(payload, key, index)
    return pd.to_datetime(value, utc=True) if value else None


def _to_date(value: object | None) -> object | None:
    return pd.to_datetime(value).date() if value else None
