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
    def fetch_data(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def analyze(self, data_payload: Dict[str, Any]) -> Dict[str, Any]:
        ...

    @abstractmethod
    def produce_report(self, analysis_payload: Dict[str, Any]) -> Dict[str, Any]:
        ...
