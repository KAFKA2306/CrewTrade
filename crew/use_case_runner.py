import argparse
from datetime import datetime
from pathlib import Path

import yaml

from crew.use_cases import get_use_case_class, get_use_case_config_model
from crew.use_cases.base import UseCasePaths


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
    base_data_dir_local = Path("resources") / "data" / "use_cases" / name
    base_data_dir_repo = (
        Path(__file__).resolve().parent.parent
        / "resources"
        / "data"
        / "use_cases"
        / name
    )
    local_raw = base_data_dir_local / "raw"
    repo_raw = base_data_dir_repo / "raw"
    local_ready = local_raw.exists() and any(local_raw.iterdir())
    repo_ready = repo_raw.exists() and any(repo_raw.iterdir())
    if repo_ready:
        base_data_dir = base_data_dir_repo
    elif local_ready:
        base_data_dir = base_data_dir_local
    else:
        base_data_dir = (
            base_data_dir_local if base_data_dir_local.exists() else base_data_dir_repo
        )
    raw_data_dir = base_data_dir / "raw"
    processed_data_dir = base_data_dir / "processed"
    report_dir = (
        Path("output") / "use_cases" / name / datetime.today().strftime("%Y%m%d")
    )
    return UseCasePaths(
        raw_data_dir=raw_data_dir,
        processed_data_dir=processed_data_dir,
        report_dir=report_dir,
    )


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
