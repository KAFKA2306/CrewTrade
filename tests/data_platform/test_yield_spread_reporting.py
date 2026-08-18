from __future__ import annotations

import pandas as pd

from crew.yields.config import DEFAULT_CONFIG
from crew.yields.reporting import YieldSpreadReporter


def test_report_orders_treasury_maturities_and_has_no_custom_score(tmp_path) -> None:
    reporter = YieldSpreadReporter(DEFAULT_CONFIG, tmp_path / "processed", tmp_path / "report")
    payload: dict[str, object] = {
        "spread_snapshot": pd.DataFrame(
            [
                {
                    "spread": "us_2s10s",
                    "latest_date": "2026-08-17",
                    "short_rate_pct": 4.19,
                    "long_rate_pct": 4.72,
                    "spread_bp": 53.0,
                    "change_20d_bp": 14.0,
                    "z_score": 2.07,
                }
            ]
        ),
        "macro_snapshot": pd.DataFrame(
            [{"series": "us_10y", "latest_date": "2026-08-17", "value_pct": 4.72}]
        ),
        "curve_snapshot": pd.DataFrame(
            [
                {"observation_date": "2026-08-17", "tenor": "10Y", "value": 4.72},
                {"observation_date": "2026-08-17", "tenor": "1.5M", "value": 3.80},
                {"observation_date": "2026-08-17", "tenor": "30Y", "value": 5.31},
                {"observation_date": "2026-08-17", "tenor": "1M", "value": 3.79},
                {"observation_date": "2026-08-17", "tenor": "2Y", "value": 4.19},
            ]
        ),
        "signals": pd.DataFrame(),
    }

    report = reporter._build_report(payload)

    positions = [report.index(f"| {tenor} |") for tenor in ("1M", "1.5M", "2Y", "10Y", "30Y")]
    assert positions == sorted(positions)
    assert "## 評価" not in report
    assert "/25" not in report
