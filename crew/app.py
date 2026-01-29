import yaml
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Type

import pandas as pd
from pydantic import BaseModel


class UseCaseConfig(BaseModel):
    name: str


class BaseDataPipeline(ABC):
    def __init__(self, raw_data_dir: Path, config: Any = None):
        self.raw_data_dir = raw_data_dir
        self.config = config
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_data(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        saved_files = self.fetch_data_internal(targets, days)

        manual_dir = self.raw_data_dir / "manual"
        if manual_dir.exists():
            for name in targets.keys():
                manual_file = manual_dir / f"{name}.csv"
                if manual_file.exists():
                    self._merge_manual_data(name, manual_file)
                    saved_files[name] = str(self.raw_data_dir / f"{name}.parquet")

        return saved_files

    @abstractmethod
    def fetch_data_internal(
        self, targets: Dict[str, str], days: int
    ) -> Dict[str, str]: ...

    def _merge_manual_data(self, name: str, manual_file: Path):
        manual_df = pd.read_csv(manual_file)
        if "Date" in manual_df.columns and "Price" in manual_df.columns:
            manual_df["Date"] = pd.to_datetime(manual_df["Date"]).dt.date

            auto_file = self.raw_data_dir / f"{name}.parquet"
            if auto_file.exists():
                auto_df = pd.read_parquet(auto_file)
                # Ensure Date is comparable
                if not pd.api.types.is_datetime64_any_dtype(auto_df["Date"]):
                    auto_df["Date"] = pd.to_datetime(auto_df["Date"]).dt.date

                combined_df = pd.concat([auto_df, manual_df])
            else:
                combined_df = manual_df

            combined_df = combined_df.sort_values("Date").drop_duplicates(
                subset=["Date"], keep="last"
            )
            self._save(name, combined_df)

    def _save(self, name: str, df: pd.DataFrame):
        path = self.raw_data_dir / f"{name}.parquet"
        df.to_parquet(path, index=False)


class GenericUseCase:
    def __init__(
        self,
        config_path: Path,
        pipeline_class: Type[BaseDataPipeline],
        analyzer_class: Any,
        config_class: Type[UseCaseConfig] = UseCaseConfig,
    ):
        self.config_path = config_path
        self.pipeline_class = pipeline_class
        self.analyzer_class = analyzer_class
        self.config_class = config_class
        self.config = self._load_config()
        self.project_root = Path(__file__).resolve().parent.parent
        self.raw_data_dir = self.project_root / "data" / self.config.name

    def _load_config(self) -> UseCaseConfig:
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        if "name" not in config_data:
            config_data["name"] = self.config_path.stem
        return self.config_class(**config_data)

    def fetch_data(self) -> Dict[str, Any]:
        pipeline = self.pipeline_class(self.raw_data_dir, self.config)
        # Assuming config has 'targets' and 'days' - dynamic access or strict model?
        # For simplicity and generic support, we access attributes dynamically if they exist.
        targets = getattr(self.config, "targets", {})
        days = getattr(self.config, "days", 365)
        return pipeline.fetch_data(targets, days)

    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        analyzer = self.analyzer_class(
            self.config
            if hasattr(self.analyzer_class, "__init__")
            and "config" in self.analyzer_class.__init__.__code__.co_varnames
            else self.raw_data_dir
        )
        # Analyzer interface varies: some take config, some take dir.
        # We might need to standardize Analyzers or adapt here.
        # Looking at previous duplications: most take config. Imura takes raw_data_dir.
        # This is the "Adapter" part of Clean Arch.
        # For now, let's try to support the existing patterns or standardize.
        # ImuraFundAnalyzer(raw_data_dir)
        # Others(config)

        if isinstance(analyzer, self.analyzer_class):  # Already instantiated? No.
            pass

        # Inject raw_data_dir if not present, useful for Analyzers that need to load data from disk
        # when running separately from fetch.
        if not hasattr(analyzer, "raw_data_dir"):
            analyzer.raw_data_dir = self.raw_data_dir

        # Try instantiation
        try:
            # Basic dependency injection attempt
            return analyzer.evaluate(data_payload)
        except AttributeError:
            return analyzer.analyze(data_payload)

    def run(self):
        data = self.fetch_data()
        analysis = self.analyze(data)
        return {"data": data, "analysis": analysis}
