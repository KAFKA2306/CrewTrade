from pathlib import Path

import pytest

from crew.data_platform.registry import load_config


def test_load_config_rejects_missing_storage(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("schema_version: 1\nsources: {}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid data platform config"):
        load_config(path)


def test_load_config_rejects_non_boolean_enabled(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        "schema_version: 1\n"
        "storage:\n  root: data/platform\n"
        "sources:\n  treasury:\n    enabled: 'yes'\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid data platform config"):
        load_config(path)


def test_load_config_preserves_source_specific_fields(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(
        "schema_version: 1\n"
        "storage:\n  root: data/platform\n"
        "sources:\n"
        "  treasury:\n"
        "    adapter: treasury_yield_curve\n"
        "    enabled: true\n"
        "    dataset: treasury_par_yield_curve\n",
        encoding="utf-8",
    )

    config = load_config(path)

    assert config["sources"]["treasury"]["dataset"] == "treasury_par_yield_curve"
