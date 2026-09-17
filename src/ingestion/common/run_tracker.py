"""Wrapper around IngestionRun for consistent audit recording."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.models.audit import IngestionRun


class IngestionRunTracker:
    """Manages lifecycle of a single IngestionRun record.

    Guarantees that every run ends in COMPLETED or FAILED and never
    silently drops records without updating counters.
    """

    def __init__(self, session: Session, source: str):
        self.session = session
        self.source = source
        self.run: Optional[IngestionRun] = None

    def start(self, records_found: int = 0) -> IngestionRun:
        self.run = IngestionRun(
            source=self.source,
            status="STARTED",
            records_found=records_found,
            records_inserted=0,
            records_updated=0,
            records_failed=0,
        )
        self.session.add(self.run)
        self.session.flush()
        return self.run

    def record_success(self, inserted: int = 0, updated: int = 0) -> None:
        if self.run is None:
            raise RuntimeError("IngestionRunTracker.start() must be called first")
        self.run.records_inserted = (self.run.records_inserted or 0) + inserted
        self.run.records_updated = (self.run.records_updated or 0) + updated

    def record_failure(self, failed: int = 1, error: Optional[str] = None) -> None:
        if self.run is None:
            raise RuntimeError("IngestionRunTracker.start() must be called first")
        self.run.records_failed = (self.run.records_failed or 0) + failed
        if error:
            existing = self.run.error_log or ""
            self.run.error_log = (existing + "\n" + error).strip()

    def complete(self) -> IngestionRun:
        if self.run is None:
            raise RuntimeError("IngestionRunTracker.start() must be called first")
        self.run.status = "COMPLETED"
        self.run.finished_at = datetime.utcnow()
        self.session.flush()
        return self.run

    def fail(self, error: str) -> IngestionRun:
        if self.run is None:
            self.run = IngestionRun(
                source=self.source,
                status="FAILED",
                records_found=0,
                records_failed=0,
                error_log=error,
                finished_at=datetime.utcnow(),
            )
            self.session.add(self.run)
        else:
            self.run.status = "FAILED"
            self.run.error_log = error
            self.run.finished_at = datetime.utcnow()
        self.session.flush()
        return self.run
