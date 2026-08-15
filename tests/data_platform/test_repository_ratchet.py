from pathlib import Path

from crew.data_platform.registry import load_config

ROOT = Path(__file__).resolve().parents[2]


def test_canonical_flow_contract_exists() -> None:
    required = [
        ROOT / "config" / "data_platform.yaml",
        ROOT / "config" / "use_case_data_status.yaml",
        ROOT / "crew" / "data_platform",
        ROOT / "output" / "use_cases",
        ROOT / "resources" / "reference" / "canonical-flow.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert not missing, f"canonical flow paths missing: {missing}"


def test_every_implemented_dataset_has_an_executable_contract() -> None:
    config = load_config(ROOT / "config" / "data_platform.yaml")
    expected = {
        "treasury_par_yield_curve",
        "treasury_par_real_yield_curve",
        "rates_macro",
        "governed_source_registry",
        "jpx_etf_master",
        "sec_filings",
        "sec_company_facts",
        "sec_13f_holdings",
    }

    assert set(config["contracts"]) == expected


def test_obsolete_research_paths_do_not_return() -> None:
    forbidden = [
        ROOT / ".github" / "workflows" / "weekly-repo-research.yml",
        ROOT / "research_chronos.py",
        ROOT / "chronos_test_plot.png",
    ]
    present = [str(path.relative_to(ROOT)) for path in forbidden if path.exists()]
    assert not present, f"superseded research artifacts present: {present}"
