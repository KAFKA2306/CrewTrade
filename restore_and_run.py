import os
import subprocess
from pathlib import Path

# Ensure directories
Path("ai_trading_crew/use_cases/imura").mkdir(parents=True, exist_ok=True)

files = {
    "ai_trading_crew/use_case_runner.py": r'''import argparse
from datetime import datetime
from pathlib import Path

import yaml

from ai_trading_crew.use_cases import get_use_case_class, get_use_case_config_model
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
''',
    "ai_trading_crew/use_cases/base.py": r'''from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel


class UseCaseConfig(BaseModel):
    name: str


class UseCasePaths(BaseModel):
    raw_data_dir: Path
    processed_data_dir: Path
    report_dir: Path


class BaseUseCase(ABC):
    def __init__(self, config: UseCaseConfig, paths: UseCasePaths) -> None:
        self.config = config
        self.paths = paths

    def run(self) -> Dict[str, Any]:
        data_payload = self.fetch_data()
        analysis_payload = self.analyze(data_payload)
        report_payload = self.produce_report(analysis_payload)
        return {
            "data": data_payload,
            "analysis": analysis_payload,
            "report": report_payload,
        }

    @abstractmethod
    def fetch_data(self) -> Dict[str, Any]: ...

    @abstractmethod
    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]: ...

    @abstractmethod
    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]: ...
''',
    "ai_trading_crew/use_cases/registry.py": r'''from typing import Type, Dict
from .base import BaseUseCase, UseCaseConfig


class UseCaseRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseUseCase]] = {}
        self._config_registry: Dict[str, Type[UseCaseConfig]] = {}

    def register(self, name: str, cls: Type[BaseUseCase], config_model: Type[UseCaseConfig]) -> None:
        self._registry[name] = cls
        self._config_registry[name] = config_model

    def get(self, name: str) -> Type[BaseUseCase]:
        return self._registry[name]

    def get_config_model(self, name: str) -> Type[UseCaseConfig]:
        return self._config_registry[name]


_use_case_registry = UseCaseRegistry()


def register_use_case(name: str, cls: Type[BaseUseCase], config_model: Type[UseCaseConfig]) -> None:
    _use_case_registry.register(name, cls, config_model)


def get_use_case_class(name: str) -> Type[BaseUseCase]:
    return _use_case_registry.get(name)


def get_use_case_config_model(name: str) -> Type[UseCaseConfig]:
    return _use_case_registry.get_config_model(name)
''',
    "ai_trading_crew/use_cases/__init__.py": r'''from .registry import get_use_case_class, get_use_case_config_model
# from . import index_7_portfolio
from . import imura


__all__ = [
    "get_use_case_class",
    "get_use_case_config_model",
]
''',
    "ai_trading_crew/use_cases/imura/config.py": r'''from typing import Dict
from ai_trading_crew.use_cases.base import UseCaseConfig


class ImuraFundConfig(UseCaseConfig):
    days: int = 365
    targets: Dict[str, str] = {
        "Fundnote_Kaihou": "BK311251",
        "Nikkei225_Proxy": "998407.O",
        "JPX400_ETF": "1591.T",
        "TSE_Growth250_ETF": "2516.T",
        "NASDAQ100_ETF": "1545.T",
    }
''',
    "ai_trading_crew/use_cases/imura/data.py": r'''import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from pathlib import Path
from typing import Dict


class ImuraFundDataPipeline:
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = raw_data_dir
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_data(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        saved_files = {}
        for name, symbol in targets.items():
            df = self._get_historical_data(symbol, days)
            file_path = self.raw_data_dir / f"{name}.csv"
            df.to_csv(file_path, index=False)
            print(f"Saved {name} data to {file_path}")
            saved_files[name] = str(file_path)
        return saved_files

    def _get_historical_data(self, symbol: str, days: int) -> pd.DataFrame:
        url = f"https://finance.yahoo.co.jp/quote/{symbol}/history"
        all_data = []
        page = 1
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)
        str_start = start_date.strftime("%Y%m%d")
        current_to_date = end_date
        str_to = current_to_date.strftime("%Y%m%d")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        while True:
            params = {"from": str_start, "to": str_to, "timeFrame": "d", "page": page}
            resp = requests.get(url, params=params, headers=headers)
            soup = BeautifulSoup(resp.content, "html.parser")
            table = soup.find("table")
            if not table:
                break
            rows = table.find_all("tr")
            if len(rows) <= 1:
                break

            header_cols = [th.text.strip() for th in rows[0].find_all("th")]
            price_idx = 1
            for i, h in enumerate(header_cols):
                if "终値" in h or "基準価額" in h:
                    price_idx = i
                    break

            data_found = False
            stop_fetching = False
            for row in rows[1:]:
                cols = row.find_all(["td", "th"])
                if len(cols) <= price_idx:
                    continue
                date_str = cols[0].text.strip()
                price_str = cols[price_idx].text.strip()
                dt = (
                    datetime.datetime.strptime(date_str, "%Y年%m月%d日").date()
                    if "年" in date_str
                    else datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
                )
                if dt < start_date:
                    stop_fetching = True
                    break
                all_data.append(
                    {"Date": dt, "Price": float(price_str.replace(",", ""))}
                )
                data_found = True

            if not data_found or stop_fetching:
                break
            page += 1

        df = pd.DataFrame(all_data)
        if df.empty:
            return df
        df = df.sort_values("Date").drop_duplicates(subset=["Date"])
        return df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
''',
    "ai_trading_crew/use_cases/imura/analysis.py": r'''from typing import Dict, Any
from pathlib import Path


class ImuraFundAnalyzer:
    def __init__(self, raw_data_dir: Path):
        self.raw_data_dir = raw_data_dir

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "analyzed", "data_points": len(data_payload)}
''',
    "ai_trading_crew/use_cases/imura/reporting.py": r'''from typing import Dict, Any
from pathlib import Path


class ImuraFundReporter:
    def __init__(self, report_dir: Path):
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        report_file = self.report_dir / "report.md"
        with open(report_file, "w") as f:
            f.write(f"# Imura Fund Analysis Report\n\nAnalysis result: {analysis_payload}")
        return {"report_path": str(report_file)}
''',
    "ai_trading_crew/use_cases/imura/imura_fund_case.py": r'''from typing import Dict, Any
from ai_trading_crew.use_cases.base import BaseUseCase, UseCaseConfig, UseCasePaths
from .data import ImuraFundDataPipeline
from .analysis import ImuraFundAnalyzer
from .reporting import ImuraFundReporter
from .config import ImuraFundConfig


class ImuraFundUseCase(BaseUseCase):
    def __init__(self, config: UseCaseConfig, paths: UseCasePaths):
        super().__init__(config, paths)
        if not isinstance(self.config, ImuraFundConfig):
            pass

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = ImuraFundDataPipeline(self.paths.raw_data_dir)
        return pipeline.fetch_data(self.config.targets, self.config.days)

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = ImuraFundAnalyzer(self.paths.raw_data_dir)
        return analyzer.analyze(data_payload)

    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        reporter = ImuraFundReporter(self.paths.report_dir)
        return reporter.produce_report(analysis_payload)
''',
    "ai_trading_crew/use_cases/imura/__init__.py": r'''from ai_trading_crew.use_cases.registry import register_use_case
from .imura_fund_case import ImuraFundUseCase
from .config import ImuraFundConfig

register_use_case("imura", ImuraFundUseCase, ImuraFundConfig)
''',
}

for path, content in files.items():
    print(f"Writing {path}...")
    with open(path, "w") as f:
        f.write(content)

print("Running usage case...")
env = os.environ.copy()
env["PYTHONPATH"] = os.getcwd()
subprocess.run([".venv/bin/python", "ai_trading_crew/use_case_runner.py", "imura", "--config", "config/use_cases/imura.yaml"], env=env, check=True)
print("Done.")
