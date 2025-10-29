from __future__ import annotations

from typing import Dict, Optional

import pandas as pd

from ai_trading_crew.use_cases.yield_spread.config import AllocationConfig


def compute_allocation(
    allocation_config: AllocationConfig,
    snapshot: pd.DataFrame,
) -> Dict[str, object] | None:
    if allocation_config is None or snapshot.empty:
        return None

    latest = snapshot.iloc[-1]
    z_score = float(latest.get("z_score", 0.0))
    spread_bp = float(latest.get("spread_bp", 0.0))

    if z_score >= allocation_config.upper_z:
        profile = allocation_config.widening
        regime = profile.label
    elif z_score <= allocation_config.lower_z:
        profile = allocation_config.tightening
        regime = profile.label
    else:
        profile = allocation_config.neutral
        regime = profile.label

    normalized_weights = _normalize_weights(profile.weights)

    return {
        "regime": regime,
        "z_score": z_score,
        "spread_bp": spread_bp,
        "weights": normalized_weights,
    }


def _normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        return weights
    return {asset: round(weight / total, 4) for asset, weight in weights.items()}
