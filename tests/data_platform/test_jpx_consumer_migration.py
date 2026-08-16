from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from crew.clients.index_mapping import IndexETFMappingClient
from crew.data_platform.contracts import DatasetBatch
from crew.data_platform.jpx_consumer import jpx_etf_master
from crew.data_platform.storage import DataPlatformStorage


def test_jpx_etf_master_reads_latest_canonical_snapshot(tmp_path: Path) -> None:
    root = tmp_path / "platform"
    storage = DataPlatformStorage(root)
    run_id = "20260816T000000Z-jpx"
    storage.start_run(run_id, ["jpx"])
    frame = pd.DataFrame(
        [
            {
                "as_of_date": date(2026, 8, 16),
                "ticker": "1655",
                "official_name": "iシェアーズ S&P 500 米国株 ETF",
                "index_name": "S&P 500",
                "manager": "ブラックロック・ジャパン",
                "manager_search_code": None,
                "trust_fee_text": "0.066%程度",
                "long_term_flag": True,
                "market_maker_status": "star",
            },
            {
                "as_of_date": date(2026, 8, 16),
                "ticker": "2568",
                "official_name": "上場インデックスファンド米国株式（NASDAQ100）為替ヘッジなし",
                "index_name": "NASDAQ-100",
                "manager": "日興アセットマネジメント",
                "manager_search_code": None,
                "trust_fee_text": "0.275%以内",
                "long_term_flag": True,
                "market_maker_status": "circle",
            },
        ]
    )
    storage.persist(
        run_id,
        DatasetBatch(
            dataset="jpx_etf_master",
            source="jpx",
            frame=frame,
            primary_key=("as_of_date", "ticker"),
            source_url="https://www.jpx.co.jp/equities/products/etfs/issues/01.html",
            raw_payload=b"official-jpx-fixture",
        ),
    )
    storage.finish_run(run_id, status="success")

    result = jpx_etf_master(root=root)

    assert result["ticker"].tolist() == ["1655", "2568"]
    assert result["official_name"].tolist()[0] == "iシェアーズ S&P 500 米国株 ETF"
    assert result["_raw_sha256"].nunique() == 1
    assert result["_source_url"].nunique() == 1


def test_jpx_mapping_uses_official_fields_without_inferred_category() -> None:
    master = pd.DataFrame(
        [
            {
                "ticker": "1655",
                "official_name": "iシェアーズ S&P 500 米国株 ETF",
                "index_name": "S&P 500",
                "manager": "ブラックロック・ジャパン",
            },
            {
                "ticker": "2237",
                "official_name": "S&P 500 配当貴族指数連動 ETF",
                "index_name": "S&P 500配当貴族指数",
                "manager": "テスト運用会社",
            },
        ]
    )
    client = IndexETFMappingClient(
        {
            "S&P500": {
                "keywords": ["s&p500", "s&p 500"],
                "exclude_keywords": ["配当", "貴族"],
            }
        }
    )

    result = client.get_mapping(master)

    assert result.to_dict(orient="records") == [
        {"index_name": "S&P500", "ticker": "1655.T", "official_ticker": "1655"}
    ]


def test_jpx_mapping_fails_closed_without_identity_columns() -> None:
    client = IndexETFMappingClient({"S&P500": {"keywords": ["s&p 500"]}})
    with pytest.raises(ValueError, match="manager"):
        client.get_mapping(
            pd.DataFrame(
                [
                    {
                        "ticker": "1655",
                        "official_name": "example",
                        "index_name": "S&P 500",
                    }
                ]
            )
        )


def test_index_etf_pipeline_no_longer_uses_toushin_product_master() -> None:
    pipeline = Path("crew/etf/data_pipeline.py").read_text(encoding="utf-8")
    mapping = Path("crew/clients/index_mapping.py").read_text(encoding="utf-8")

    assert "jpx_etf_master" in pipeline
    assert "ToushinKyokaiDataClient" not in pipeline
    assert "ToushinKyokaiDataClient" not in mapping
    assert "expected_categories" not in mapping
