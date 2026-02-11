from crew.base import UseCaseConfig
from .models import FinancialParams, Projections
class OracleEarningsConfig(UseCaseConfig):
    base_quarter: FinancialParams
    projections: Projections
