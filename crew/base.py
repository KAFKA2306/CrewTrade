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
        self, price_frames: Dict[str, Any], pred_len: int = 91
    ) -> Dict[str, Any]:
        """Minimized Kronos forecasting loop."""
        import pandas as pd
        forecasts = {}

        for ticker, df in price_frames.items():
            if df is None or df.empty: continue
            try:
                # Normalize columns and identify Date
                df = df.copy()
                df.columns = [str(c).lower() for c in df.columns]
                if "close" in df.columns and "open" not in df.columns:
                    for col in ["open", "high", "low"]: df[col] = df["close"]
                
                # Resilient Date handling
                if "date" not in df.columns:
                    df = df.reset_index()
                    date_col = next((c for c in df.columns if "date" in str(c).lower()), df.columns[0])
                    df.rename(columns={date_col: "Date"}, inplace=True)
                
                df["Date"] = pd.to_datetime(df["Date" if "Date" in df.columns else "date"])
                df = df.sort_values("Date").reset_index(drop=True)

                if len(df) > 30:
                    y_timestamp = pd.Series([df["Date"].iloc[-1] + pd.Timedelta(days=i + 1) for i in range(pred_len)])
                    pred_df = self.get_kronos_forecast(df, df["Date"], y_timestamp, pred_len)
                    forecasts[ticker] = pred_df.to_dict(orient="records")
            except Exception as e:
                forecasts[ticker] = {"error": str(e)}

        return forecasts
