from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field

from crew.base import UseCaseConfig


class ManagerConfig(BaseModel):
    display_name: str
    cik: str


class LegendaryInvestorsConfig(UseCaseConfig):
    forms: List[str] = Field(default_factory=lambda: ["13F-HR", "13F-HR/A"])
    managers: Dict[str, ManagerConfig] = Field(default_factory=dict)
    minimum_history_quarters: int = Field(default=2, ge=2)
    top_holdings_limit: int = Field(default=20, ge=1, le=100)

    @property
    def manager_names(self) -> list[str]:
        return list(self.managers)
