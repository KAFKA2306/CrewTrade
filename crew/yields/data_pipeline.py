from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients import YieldSpreadDataClient
from crew.clients.yield_spread import YieldSeriesRequest
from crew.yields.asset_client import AllocationAssetClient
from crew.yields.config import (
    AllocationConfig,
    YieldSeriesConfig,
    YieldSpreadConfig,
)


class YieldSpreadDataPipeline(BaseDataPipeline):
    def __init__(self, raw_data_dir: Path, config: YieldSpreadConfig) -> None:
        super().__init__(raw_data_dir, config)
        self.client = YieldSpreadDataClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        start_date = self._compute_start_date(self.config.period)
        requests = self._build_requests(self.config.series_configs)
        series_map = self.client.fetch_series(
            requests.values(), start_date, self.config.period
        )
        frame = self._assemble_frame(series_map)

        saved_files = {}
        self._save("series", frame)
        saved_files["series"] = str(self.raw_data_dir / "series.csv")

        allocation_cfg = self.config.allocation
        if allocation_cfg is not None and allocation_cfg.optimization.enabled:
            asset_prices = self._collect_allocation_prices(allocation_cfg)
            if asset_prices is not None:
                self._save("asset_prices", asset_prices)
                saved_files["asset_prices"] = str(
                    self.raw_data_dir / "asset_prices.csv"
                )

        return saved_files

    def _build_requests(
        self, configs: Dict[str, YieldSeriesConfig]
    ) -> Dict[str, YieldSeriesRequest]:
        requests: Dict[str, YieldSeriesRequest] = {}
        for key, cfg in configs.items():
            requests[key] = YieldSeriesRequest(
                source=cfg.source,
                identifier=cfg.identifier,
                scaling=cfg.scaling,
                field=cfg.field,
            )
        return requests

    def _assemble_frame(self, series_map: Dict[str, pd.Series]) -> pd.DataFrame:
        series_list: Dict[str, pd.Series] = {}
        for identifier, series in series_map.items():
            if isinstance(series, pd.DataFrame):
                if series.shape[1] != 1:
                    raise ValueError(
                        f"{identifier} returned unexpected columns: {list(series.columns)}"
                    )
                series = series.iloc[:, 0]
            series = series.rename(identifier)
            series_list[identifier] = series
        frame = pd.concat(series_list.values(), axis=1)
        frame.columns = list(series_list.keys())
        frame = frame.sort_index()
        frame = frame.ffill()
        return frame

    def _compute_start_date(self, period: str) -> datetime:
        period = period.lower()
        value = int(period[:-1])
        unit = period[-1]
        today = pd.Timestamp.today().normalize()
        if unit == "y":
            start = today - pd.DateOffset(years=value)
        elif unit == "m":
            start = today - pd.DateOffset(months=value)
        else:
            start = today - pd.DateOffset(days=value)
        return start.to_pydatetime()

    def _collect_allocation_prices(
        self, allocation_cfg: AllocationConfig
    ) -> pd.DataFrame | None:
        tickers: set[str] = set()
        for profile in (
            allocation_cfg.widening,
            allocation_cfg.neutral,
            allocation_cfg.tightening,
        ):
            tickers.update(profile.weights.keys())
        if not tickers:
            return None
        client = AllocationAssetClient(self.raw_data_dir)
        period = allocation_cfg.optimization.lookback
        try:
            prices = client.get_prices(sorted(tickers), period)
        except Exception:
            return None
        return prices


# Assume project root is 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "yields.yaml"


def main() -> None:
    from crew.app import GenericUseCase
    from crew.yields.analysis import YieldSpreadAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=YieldSpreadDataPipeline,
        analyzer_class=YieldSpreadAnalyzer,
        config_class=YieldSpreadConfig,
    )

    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()

    def _build_requests(
        self, configs: Dict[str, YieldSeriesConfig]
    ) -> Dict[str, YieldSeriesRequest]:
        requests: Dict[str, YieldSeriesRequest] = {}
        for key, cfg in configs.items():
            requests[key] = YieldSeriesRequest(
                source=cfg.source,
                identifier=cfg.identifier,
                scaling=cfg.scaling,
                field=cfg.field,
            )
        return requests

    def _assemble_frame(self, series_map: Dict[str, pd.Series]) -> pd.DataFrame:
        series_list: Dict[str, pd.Series] = {}
        for identifier, series in series_map.items():
            if isinstance(series, pd.DataFrame):
                if series.shape[1] != 1:
                    raise ValueError(
                        f"{identifier} returned unexpected columns: {list(series.columns)}"
                    )
                series = series.iloc[:, 0]
            series = series.rename(identifier)
            series_list[identifier] = series
        frame = pd.concat(series_list.values(), axis=1)
        frame.columns = list(series_list.keys())
        frame = frame.sort_index()
        frame = frame.ffill()
        return frame

    def _compute_start_date(self, period: str) -> datetime:
        period = period.lower()
        value = int(period[:-1])
        unit = period[-1]
        today = pd.Timestamp.today().normalize()
        if unit == "y":
            start = today - pd.DateOffset(years=value)
        elif unit == "m":
            start = today - pd.DateOffset(months=value)
        else:
            start = today - pd.DateOffset(days=value)
        return start.to_pydatetime()

    def _collect_allocation_prices(
        self, allocation_cfg: AllocationConfig
    ) -> pd.DataFrame | None:
        tickers: set[str] = set()
        for profile in (
            allocation_cfg.widening,
            allocation_cfg.neutral,
            allocation_cfg.tightening,
        ):
            tickers.update(profile.weights.keys())
        if not tickers:
            return None
        client = AllocationAssetClient(self.raw_data_dir)
        period = allocation_cfg.optimization.lookback
        try:
            prices = client.get_prices(sorted(tickers), period)
        except Exception:
            return None
        return prices
