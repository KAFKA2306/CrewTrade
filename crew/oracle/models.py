from typing import Dict, List, Optional

from pydantic import BaseModel


class FinancialParams(BaseModel):
    period: str
    revenue_B: float
    operating_income_B: float
    capex_last_4q_B: float
    current_capex_intensity: Optional[float] = 0.55
    rpo_B: float
    cloud_revenue_growth_yoy_pct: float
    software_revenue_growth_yoy_pct: float
    software_seasonality_factors: List[float] = [1.0, 1.0, 1.0, 1.0]
    cloud_cannibalization_ratio: float = 0.0


class ProjectionScenario(BaseModel):
    cloud_growth_decay_rate: float
    software_growth_rate: float
    operating_margin_improvement: float
    capex_intensity_target: float
    rpo_growth_yoy: float


class Projections(BaseModel):
    quarters_to_project: int
    scenarios: Dict[str, ProjectionScenario]


class ProjectedQuarter(BaseModel):
    quarter_index: int
    period_label: str
    revenue_B: float
    operating_income_B: float
    capex_B: float
    rpo_B: float
    fcf_B: float
