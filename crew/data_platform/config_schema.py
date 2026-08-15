from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, StrictBool, ValidationError, model_validator


class StorageConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    root: str = Field(min_length=1)
    canonical_timezone: str = Field(default="UTC", min_length=1)


class SourceConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    adapter: str | None = None
    enabled: StrictBool = False


class FieldContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["any", "string", "number", "integer", "date", "datetime", "boolean", "json"]
    nullable: StrictBool = True
    allowed: list[Any] | None = None
    minimum: float | None = None
    maximum: float | None = None
    pattern: str | None = None


class FreshnessContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str = Field(min_length=1)
    max_age_days: int = Field(ge=0)


class DatasetContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    primary_key: list[str] = Field(min_length=1)
    strict_columns: StrictBool = True
    fields: dict[str, FieldContract] = Field(min_length=1)
    freshness: FreshnessContract | None = None
    required_metadata: list[str] = Field(default_factory=list)
    grain: str = Field(min_length=1)
    revision_policy: str = Field(min_length=1)
    redistribution: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_references(self) -> Self:
        missing_pk = sorted(set(self.primary_key).difference(self.fields))
        if missing_pk:
            raise ValueError(f"primary_key fields missing from contract fields: {missing_pk}")
        if self.freshness and self.freshness.field not in self.fields:
            raise ValueError(f"freshness field missing from contract fields: {self.freshness.field}")
        return self


class DataPlatformConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: Literal[2]
    storage: StorageConfig
    sources: dict[str, SourceConfig]
    contracts: dict[str, DatasetContract] = Field(min_length=1)


def load_validated_config(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Data platform config must be a mapping: {path}")
    try:
        validated = DataPlatformConfig.model_validate(payload)
    except ValidationError as error:
        raise ValueError(f"Invalid data platform config: {path}") from error
    return validated.model_dump(mode="python")
