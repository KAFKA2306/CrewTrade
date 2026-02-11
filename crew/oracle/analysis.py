from typing import Any, Dict
from .config import OracleEarningsConfig
from .models import ProjectedQuarter
class OracleEarningsAnalyzer:
    def __init__(self, config: OracleEarningsConfig) -> None:
        self.config = config
    def evaluate(self, data_payload: Dict[str, Any] = None) -> Dict[str, Any]:
        config = self.config
        base = config.base_quarter
        results = {}
        for scenario_name, scenario in config.projections.scenarios.items():
            quarterly_data = []
            cloud_rev = 7.0
            other_rev = 9.1
            seasonality = (
                base.software_seasonality_factors
                if base.software_seasonality_factors
                else [1.0] * 4
            )
            normalized_software_runrate = other_rev / seasonality[1]
            current_margin = base.operating_income_B / base.revenue_B
            for i in range(1, config.projections.quarters_to_project + 1):
                cloud_growth = (
                    base.cloud_revenue_growth_yoy_pct
                    * (scenario.cloud_growth_decay_rate**i)
                    / 100.0
                )
                prev_cloud = cloud_rev
                cloud_rev *= 1 + cloud_growth / 4
                normalized_software_runrate *= (
                    1 + (scenario.software_growth_rate * i) / 100.0 / 4
                )
                normalized_software_runrate -= (
                    cloud_rev - prev_cloud
                ) * base.cloud_cannibalization_ratio
                software_rev = normalized_software_runrate * seasonality[(1 + i) % 4]
                total_rev = cloud_rev + software_rev
                current_margin += scenario.operating_margin_improvement / 100.0
                target_intensity = scenario.capex_intensity_target
                start_intensity = base.current_capex_intensity or 0.55
                capex = total_rev * (
                    start_intensity
                    + (target_intensity - start_intensity)
                    * (i / config.projections.quarters_to_project)
                )
                quarterly_data.append(
                    ProjectedQuarter(
                        quarter_index=i,
                        period_label=f"FY{2026 + (2 + i - 1) // 4} Q{(2 + i - 1) % 4 + 1}",
                        revenue_B=total_rev,
                        operating_income_B=total_rev * current_margin,
                        capex_B=capex,
                        rpo_B=base.rpo_B
                        * ((1 + scenario.rpo_growth_yoy) ** (0.25 * i)),
                        fcf_B=(total_rev * current_margin) - capex,
                    )
                )
            results[scenario_name] = quarterly_data
        return {"projections": results, "base_quarter": base}
