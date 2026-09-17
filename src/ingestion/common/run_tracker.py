"""Thin helpers around IngestionRun audit rows."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.models.audit import IngestionRun


def start_run(session: Session, source: str, records_found: int = 0) -> IngestionRun:
    run = IngestionRun(source=source, status="STARTED", records_found=records_found)
    session.add(run)
    session.flush()
    return run


def complete_run(
    run: IngestionRun,
    *,
    inserted: int = 0,
    updated: int = 0,
    failed: int = 0,
    error_log: Optional[str] = None,
) -> None:
    run.records_inserted = inserted
    run.records_updated = updated
    run.records_failed = failed
    run.error_log = error_log
    run.status = "COMPLETED"
    run.finished_at = datetime.utcnow()


def fail_run(
    session: Session,
    source: str,
    *,
    records_found: int = 0,
    records_failed: int = 0,
    error_log: Optional[str] = None,
) -> IngestionRun:
    run = IngestionRun(
        source=source,
        status="FAILED",
        records_found=records_found,
        records_failed=records_failed,
        error_log=error_log,
        finished_at=datetime.utcnow(),
    )
    session.add(run)
    session.commit()
    return run
