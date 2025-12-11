from pathlib import Path
from typing import Dict

import pandas as pd

from crew.app import BaseDataPipeline
from crew.clients import PreciousMetalsDataClient, get_price_series
from crew.metals.config import PreciousMetalsSpreadConfig


class PreciousMetalsSpreadDataPipeline(BaseDataPipeline):
    def __init__(self, raw_data_dir: Path, config: PreciousMetalsSpreadConfig) -> None:
        super().__init__(raw_data_dir, config)
        self.client = PreciousMetalsDataClient(raw_data_dir)

    def fetch_data_internal(self, targets: Dict[str, str], days: int) -> Dict[str, str]:
        etf_frames = self.client.get_frames(
            self.config.etf_tickers, "etf", self.config.period
        )
        metal_frames = self.client.get_frames(
            self.config.metal_tickers, "metal", self.config.period
        )
        fx_frames = self.client.get_frames(
            [self.config.fx_symbol], "fx", self.config.period
        )
        etf_series = self._combine_close(etf_frames)
        metal_series = self._combine_close(metal_frames)
        fx_series = self._combine_close(fx_frames)

        saved_files = {}
        for name, series in [
            ("etf", etf_series),
            ("metal", metal_series),
            ("fx", fx_series),
        ]:
            # Series to DataFrame for saving
            df = (
                series.reset_index()
                if isinstance(series, pd.DataFrame)
                else series.to_frame().reset_index()
            )
            # Standardize Date column if possible or rely on series logic
            # Existing code: _combine_close returns DataFrame with date index?
            # get_price_series returns Series with Date index I assume.
            # _combine_close: pd.concat(series_list, axis=1) -> DataFrame index is Date.
            # reset_index makes 'Date' a column.
            self._save(name, df)
            saved_files[name] = str(self.raw_data_dir / f"{name}.csv")

        return saved_files

    def _combine_close(self, frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        series_list = []
        for ticker, frame in frames.items():
            price_series = get_price_series(frame)
            series_list.append(price_series.rename(ticker))
        combined = pd.concat(series_list, axis=1)
        combined = combined.sort_index()
        return combined


# Assume project root is 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "use_cases" / "metals.yaml"


def main() -> None:
    from crew.app import GenericUseCase
    from crew.metals.analysis import PreciousMetalsSpreadAnalyzer

    use_case = GenericUseCase(
        config_path=CONFIG_FILE,
        pipeline_class=PreciousMetalsSpreadDataPipeline,
        analyzer_class=PreciousMetalsSpreadAnalyzer,
        config_class=PreciousMetalsSpreadConfig,
    )

    saved_files = use_case.fetch_data()
    for name, path in saved_files.items():
        print(f"Saved {name}: {path}")


if __name__ == "__main__":
    main()
