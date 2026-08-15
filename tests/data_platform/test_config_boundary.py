from pathlib import Path

import pytest

from crew.data_platform.registry import load_config


_MINIMAL_CONTRACT = """
contracts:
  example:
    contract_version: 1.0.0
    source: fixture
    primary_key: [id]
    strict_columns: true
    grain: one row per id
    revision_policy: append snapshots
    redistribution: test only
    fields:
      id: {type: string, nullable: false}
"""


def test_load_config_rejects_missing_storage(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("schema_version: 2\nsources: {}\n" + _MINIMAL_CONTRACT, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid data platform config"):
        load_config(path)


def test_load_config_rejects_non_boolean_enabled(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    content = (
        "schema_version: 2\n"
        "storage:\n  root: data/platform\n"
        "sources:\n  treasury:\n    enabled: 'yes'\n"
    ) + _MINIMAL_CONTRACT
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid data platform config"):
        load_config(path)


def test_load_config_preserves_source_specific_fields(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    content = (
        "schema_version: 2\n"
        "storage:\n  root: data/platform\n"
        "sources:\n"
        "  treasury:\n"
        "    adapter: treasury_yield_curve\n"
        "    enabled: true\n"
        "    dataset: treasury_par_yield_curve\n"
    ) + _MINIMAL_CONTRACT
    path.write_text(content, encoding="utf-8")

    config = load_config(path)

    assert config["sources"]["treasury"]["dataset"] == "treasury_par_yield_curve"


def test_load_config_rejects_contract_with_unknown_primary_key_field(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        "schema_version: 2\n"
        "storage:\n  root: data/platform\n"
        "sources: {}\n"
        "contracts:\n"
        "  broken:\n"
        "    contract_version: 1.0.0\n"
        "    source: fixture\n"
        "    primary_key: [missing]\n"
        "    grain: one row per id\n"
        "    revision_policy: append snapshots\n"
        "    redistribution: test only\n"
        "    fields:\n"
        "      id: {type: string, nullable: false}\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid data platform config"):
        load_config(path)
