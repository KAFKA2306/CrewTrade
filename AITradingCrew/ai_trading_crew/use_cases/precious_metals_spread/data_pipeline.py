from pathlib import Path
from typing import Dict
import pandas as pd
from ai_trading_crew.use_cases.data_clients import PreciousMetalsDataClient, get_price_series
from ai_trading_crew.use_cases.precious_metals_spread.config import PreciousMetalsSpreadConfig


class PreciousMetalsSpreadDataPipeline:
    def __init__(self, config: PreciousMetalsSpreadConfig, raw_data_dir: Path) -> None:
        self.config = config
        self.client = PreciousMetalsDataClient(raw_data_dir)

    def collect(self) -> Dict[str, pd.DataFrame]:
        etf_frames = self.client.get_frames(self.config.etf_tickers, "etf", self.config.period)
        metal_frames = self.client.get_frames(self.config.metal_tickers, "metal", self.config.period)
        fx_frames = self.client.get_frames([self.config.fx_symbol], "fx", self.config.period)
        etf_series = self._combine_close(etf_frames)
        metal_series = self._combine_close(metal_frames)
        fx_series = self._combine_close(fx_frames)
        return {
            "etf": etf_series,
            "metal": metal_series,
            "fx": fx_series,
        }

    def _combine_close(self, frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        series_list = []
        for ticker, frame in frames.items():
            price_series = get_price_series(frame)
            series_list.append(price_series.rename(ticker))
        combined = pd.concat(series_list, axis=1)
        combined = combined.sort_index()
        return combined
