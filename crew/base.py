from __future__ import annotations

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

    def get_kronos_forecast(
        self,
        df: Any,
        x_timestamp: Any,
        y_timestamp: Any,
        pred_len: int = 120,
        temp: float = 1.0,
        top_p: float = 0.9,
        sample_count: int = 1,
    ) -> Any:
        from crew.utils.kronos_utils import get_kronos_forecast

        return get_kronos_forecast(
            df=df,
            x_timestamp=x_timestamp,
            y_timestamp=y_timestamp,
            pred_len=pred_len,
            temp=temp,
            top_p=top_p,
            sample_count=sample_count,
        )

    def run_kronos_forecasts(
        self,
        price_frames: Dict[str, Any],
        pred_len: int = 30,
        date_col: str = "Date",
    ) -> Dict[str, Any]:
        """
        Standardized Kronos forecasting loop for a dictionary of DataFrames.
        Expects price_frames used in analysis, typically with columns like 'Open', 'Close' etc.
        """
        import pandas as pd

        forecasts = {}

        for ticker, df in price_frames.items():
            if df is None or df.empty:
                continue

            try:
                # 1. Normalize DataFrame columns
                df = df.copy()
                df.columns = [str(c).lower() for c in df.columns]

                # 2. Ensure required columns (open/high/low/close/volume)
                # Fallback: if only close exists, propagate it
                if "close" in df.columns and "open" not in df.columns:
                    df["open"] = df["close"]
                    df["high"] = df["close"]
                    df["low"] = df["close"]

                if "volume" not in df.columns:
                    df["volume"] = 0.0

                # 3. Handle Date column
                # Look for 'date' in columns or index
                target_date_col = None
                if "date" in df.columns:
                    target_date_col = "date"
                else:
                    # Check index name
                    if df.index.name and df.index.name.lower() == "date":
                        df = df.reset_index()
                        target_date_col = df.columns[
                            0
                        ]  # Assuming index became first col
                    else:
                        # Try to reset index and see if it helps, or assume first column
                        # This is a bit risky but consistent with prev logic
                        if "date" not in df.columns:
                            df = df.reset_index()
                            target_date_col = df.columns[0]

                if target_date_col:
                    df["Date"] = pd.to_datetime(df[target_date_col])
                    df = df.sort_values("Date").reset_index(drop=True)

                    if len(df) > 30:
                        x_timestamp = df["Date"]
                        last_date = df["Date"].iloc[-1]
                        future_dates = [
                            last_date + pd.Timedelta(days=i + 1)
                            for i in range(pred_len)
                        ]
                        y_timestamp = pd.Series(future_dates)

                        pred_df = self.get_kronos_forecast(
                            df=df,
                            x_timestamp=x_timestamp,
                            y_timestamp=y_timestamp,
                            pred_len=pred_len,
                        )
                        forecasts[ticker] = pred_df.to_dict(orient="records")
            except Exception as e:
                # Log error but don't crash
                # In a real app we might use a logger, here we just print or store error
                # print(f"Kronos forecast failed for {ticker}: {e}")
                forecasts[ticker] = {"error": str(e)}

        return forecasts
