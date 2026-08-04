from __future__ import annotations

from typing import Dict, List

from pydantic import Field

from crew.base import UseCaseConfig


class OracleEarningsConfig(UseCaseConfig):
    entity_name: str = Field(default="oracle")
    forms: List[str] = Field(default_factory=lambda: ["10-K", "10-Q", "8-K"])
    concepts: Dict[str, List[str]] = Field(default_factory=dict)
    allow_model_projection: bool = Field(default=False)

    @property
    def requested_concepts(self) -> list[str]:
        return list(
            dict.fromkeys(
                concept
                for candidates in self.concepts.values()
                for concept in candidates
            )
        )
