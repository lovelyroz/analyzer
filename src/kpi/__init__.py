"""
KPI Specification Module (Stage 2)
"""

from src.kpi.schema import KPIResult
from src.kpi.period_utils import calculate_ttm, calculate_yoy_growth
from src.kpi.universal import UniversalKPIEngine
from src.kpi.conditional import ConditionalKPIEngine
from src.kpi.industry import IndustryKPIEngine
from src.kpi.engine import KPIEngine

__all__ = [
    "KPIResult",
    "calculate_ttm",
    "calculate_yoy_growth",
    "UniversalKPIEngine",
    "ConditionalKPIEngine",
    "IndustryKPIEngine",
    "KPIEngine",
]