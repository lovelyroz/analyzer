from dataclasses import dataclass
from typing import Optional, Any
from datetime import datetime

@dataclass
class KPIResult:
    company_id: int
    period_id: int
    kpi_code: str
    value: Optional[float]           # مقدار محاسبه‌شده (در صورت عدم وجود None)
    unit: str                        # PERCENTAGE, RATIO, CURRENCY_IRR, etc.
    quality_status: str              # VALID, MISSING, ESTIMATED, RESTATED
    calculation_timestamp: datetime
    metadata: Optional[dict] = None  # توضیحات عارضه‌یابی