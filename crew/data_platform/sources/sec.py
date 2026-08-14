from __future__ import annotations

import base64
import hashlib
import json
import os
from typing import Any, Mapping, Sequence
from xml.etree import ElementTree

import pandas as pd

from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.http import HttpClient


class SecSource:
    name = "sec_edgar"
    DATA_BASE_URL = "https://data.sec.gov"
    ARCHIVES_BASE_URL = "https://www.sec.gov/Archives/edgar/data"

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
            min_interval_seconds=max(0.12, float(config.get("min_interval_seconds", 0.15))),
        )

    def fetch(self) -> Sequence[DatasetBatch]:
        filing_rows: list[dict[str, object]] = []
        fact_rows: list[dict[str, object]] = []
        holding_rows: list[dict[str, object]] = []
        raw_bundle: dict[str, object] = {"entities": {}}
        latest_url = self.DATA_BASE_URL
        latest_retrieved_at = None

        for entity_name, entity_config in dict(self.config.get("entities", {})).items():
            cik = str(entity_config["cik"]).zfill(10)
            submissions_payload = self.client.get(f"{self.DATA_BASE_URL}/submissions/CIK{cik}.json")
            submissions_json = json.loads(submissions_payload.body)
            entity_filings = parse_sec_submissions(
                entity_name=str(entity_name), cik=cik, payload=submissions_json
            )
            filing_rows.extend(entity_filings)
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

            if bool(entity_config.get("thirteen_f_information_table", False)):
                holdings, documents, document_url, retrieved_at = self._fetch_13f_tables(
                    entity_name=str(entity_name),
                    cik=cik,
                    filings=entity_filings,
                    history_limit=int(entity_config.get("history_limit", 8)),
                )
                holding_rows.extend(holdings)
                entity_raw["thirteen_f_documents"] = documents
                if document_url:
                    latest_url = document_url
                if retrieved_at is not None:
                    latest_retrieved_at = retrieved_at

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
        if holding_rows:
            batches.append(
                DatasetBatch(
                    dataset="sec_13f_holdings",
                    source=self.name,
                    frame=pd.DataFrame.from_records(holding_rows),
                    primary_key=("holding_id",),
                    source_url=latest_url,
                    raw_payload=raw_payload,
                    content_type="application/json",
                    retrieved_at=retrieved_at,
                    metadata={
                        "filing_count": len({row["accession_number"] for row in holding_rows})
                    },
                )
            )
        return batches

    def _fetch_13f_tables(
        self,
        *,
        entity_name: str,
        cik: str,
        filings: Sequence[Mapping[str, object]],
        history_limit: int,
    ) -> tuple[list[dict[str, object]], list[dict[str, object]], str, object | None]:
        eligible = [
            filing for filing in filings if str(filing.get("form")) in {"13F-HR", "13F-HR/A"}
        ]
        eligible.sort(
            key=lambda item: (
                str(item.get("report_date") or ""),
                str(item.get("filing_date") or ""),
            ),
            reverse=True,
        )
        rows: list[dict[str, object]] = []
        documents: list[dict[str, object]] = []
        latest_url = ""
        latest_retrieved_at = None
        for filing in eligible[: max(1, history_limit)]:
            accession = str(filing["accession_number"])
            compact_accession = accession.replace("-", "")
            archive_cik = str(int(cik))
            directory_url = f"{self.ARCHIVES_BASE_URL}/{archive_cik}/{compact_accession}"
            index_payload = self.client.get(f"{directory_url}/index.json")
            index_json = json.loads(index_payload.body)
            candidates = _information_table_candidates(index_json)
            filing_document: dict[str, object] = {
                "accession_number": accession,
                "index_url": index_payload.url,
                "index": index_json,
                "information_tables": [],
            }
            for filename in candidates:
                document_payload = self.client.get(f"{directory_url}/{filename}")
                parsed = parse_13f_information_table(
                    entity_name=entity_name,
                    cik=cik,
                    accession_number=accession,
                    report_date=filing.get("report_date"),
                    filing_date=filing.get("filing_date"),
                    source_url=document_payload.url,
                    payload=document_payload.body,
                )
                if not parsed:
                    continue
                rows.extend(parsed)
                filing_document["information_tables"].append(
                    {
                        "filename": filename,
                        "url": document_payload.url,
                        "body_base64": base64.b64encode(document_payload.body).decode("ascii"),
                    }
                )
                latest_url = document_payload.url
                latest_retrieved_at = document_payload.retrieved_at
                break
            documents.append(filing_document)
        return rows, documents, latest_url, latest_retrieved_at


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
                "acceptance_datetime": _timestamp_at(recent, "acceptanceDateTime", index),
                "form": _value_at(recent, "form", index),
                "primary_document": _value_at(recent, "primaryDocument", index),
                "primary_doc_description": _value_at(recent, "primaryDocDescription", index),
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


def parse_13f_information_table(
    *,
    entity_name: str,
    cik: str,
    accession_number: str,
    report_date: object,
    filing_date: object,
    source_url: str,
    payload: bytes,
) -> list[dict[str, object]]:
    try:
        root = ElementTree.fromstring(payload)
    except ElementTree.ParseError:
        return []
    rows: list[dict[str, object]] = []
    for position, node in enumerate(
        element for element in root.iter() if _local_name(element.tag) == "infoTable"
    ):
        issuer = _descendant_text(node, "nameOfIssuer")
        cusip = _descendant_text(node, "cusip")
        if not issuer or not cusip:
            continue
        canonical = {
            "entity_cik": cik,
            "accession_number": accession_number,
            "position": position,
            "issuer": issuer,
            "title_of_class": _descendant_text(node, "titleOfClass"),
            "cusip": cusip,
            "put_call": _descendant_text(node, "putCall"),
        }
        holding_id = hashlib.sha256(
            json.dumps(canonical, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        rows.append(
            {
                "holding_id": holding_id,
                "entity_name": entity_name,
                "entity_cik": cik,
                "accession_number": accession_number,
                "report_date": _to_date(report_date),
                "filing_date": _to_date(filing_date),
                "issuer": issuer,
                "title_of_class": canonical["title_of_class"],
                "cusip": cusip,
                "figi": _descendant_text(node, "figi"),
                "reported_value": _to_number(_descendant_text(node, "value")),
                "reported_value_unit": "SEC_13F_as_filed",
                "shares_or_principal": _to_number(_descendant_text(node, "sshPrnamt")),
                "shares_or_principal_type": _descendant_text(node, "sshPrnamtType"),
                "put_call": canonical["put_call"],
                "investment_discretion": _descendant_text(node, "investmentDiscretion"),
                "other_manager": _descendant_text(node, "otherManager"),
                "voting_sole": _to_number(_descendant_text(node, "Sole")),
                "voting_shared": _to_number(_descendant_text(node, "Shared")),
                "voting_none": _to_number(_descendant_text(node, "None")),
                "source_document_url": source_url,
            }
        )
    return rows


def _information_table_candidates(index_payload: Mapping[str, Any]) -> list[str]:
    items = index_payload.get("directory", {}).get("item", [])
    names = [str(item.get("name", "")) for item in items]
    xml_names = [name for name in names if name.lower().endswith(".xml")]
    preferred = [name for name in xml_names if "info" in name.lower() and "table" in name.lower()]
    return preferred + [name for name in xml_names if name not in preferred]


def _descendant_text(node: ElementTree.Element, name: str) -> str | None:
    for child in node.iter():
        if _local_name(child.tag).lower() == name.lower():
            text = (child.text or "").strip()
            return text or None
    return None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _to_number(value: object | None) -> float | None:
    if value is None:
        return None
    text = str(value).replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


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
