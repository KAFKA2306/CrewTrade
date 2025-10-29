from pathlib import Path
import argparse
from datetime import datetime
import yaml
from ai_trading_crew.use_cases import get_use_case_class, get_use_case_config_model
import ai_trading_crew.use_cases.precious_metals_spread  # noqa: F401
import ai_trading_crew.use_cases.credit_spread  # noqa: F401
import ai_trading_crew.use_cases.yield_spread  # noqa: F401
from ai_trading_crew.use_cases.base import UseCasePaths


def build_config(name: str, config_path: str | None):
    config_model = get_use_case_config_model(name)
    if config_path is None:
        return config_model(name=name)
    with Path(config_path).open("r", encoding="utf-8") as stream:
        payload = yaml.safe_load(stream)
    if payload is None:
        payload = {}
    payload["name"] = name
    return config_model(**payload)


def build_paths(name: str) -> UseCasePaths:
    base_data_dir = Path("resources") / "data" / "use_cases" / name
    raw_data_dir = base_data_dir / "raw"
    processed_data_dir = base_data_dir / "processed"
    report_dir = Path("output") / "use_cases" / name / datetime.today().strftime("%Y%m%d")
    return UseCasePaths(raw_data_dir=raw_data_dir, processed_data_dir=processed_data_dir, report_dir=report_dir)


def run_use_case(name: str, config_path: str | None):
    config = build_config(name, config_path)
    paths = build_paths(name)
    use_case_cls = get_use_case_class(name)
    use_case = use_case_cls(config, paths)
    return use_case.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--config", dest="config_path")
    args = parser.parse_args()
    run_use_case(args.name, args.config_path)


if __name__ == "__main__":
    main()
