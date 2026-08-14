from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, StrictBool, ValidationError


class StorageConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    root: str = Field(min_length=1)
    canonical_timezone: str = Field(default="UTC", min_length=1)


class SourceConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    adapter: str | None = None
    enabled: StrictBool = False


class DataPlatformConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: Literal[1]
    storage: StorageConfig
    sources: dict[str, SourceConfig]


def load_validated_config(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Data platform config must be a mapping: {path}")
    try:
        validated = DataPlatformConfig.model_validate(payload)
    except ValidationError as error:
        raise ValueError(f"Invalid data platform config: {path}") from error
    return validated.model_dump(mode="python")
