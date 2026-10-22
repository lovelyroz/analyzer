from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from src.core.database import Base


def _utc_now_naive() -> datetime:
    """Return naive UTC for the existing DateTime storage convention."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    ingestion_id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)  # CODAL, OHLC, FX
    started_at = Column(DateTime, nullable=False, default=_utc_now_naive)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)  # STARTED, COMPLETED, FAILED
    records_found = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_log = Column(String, nullable=True)
