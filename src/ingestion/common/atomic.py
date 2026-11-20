"""Shared audit boundaries for atomic Market/FX ingestion."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.audit import IngestionRun


class IngestionAuditError(RuntimeError):
    """Raised when an ingestion run cannot be durably audited."""


def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _summary(*, duplicate_count: int, invalid_count: int, codes: list[str]) -> str:
    safe_codes = sorted({code for code in codes if code and code.replace("_", "").isalnum()})
    parts = [f"duplicate_count={duplicate_count}", f"invalid_count={invalid_count}"]
    if safe_codes:
        parts.append("codes=" + ",".join(safe_codes[:30]))
    return "; ".join(parts)


def create_started_run(session: Session, source: str, records_found: int) -> tuple[int, bool]:
    """Commit STARTED independently; return (audit id, can_continue)."""
    if session.new or session.dirty or session.deleted:
        raise IngestionAuditError("session has pending caller changes; ingestion boundary refused")
    session.rollback()
    run = IngestionRun(source=source, status="STARTED", records_found=records_found)
    try:
        session.add(run)
        session.flush()
        run_id = run.ingestion_id
        session.commit()
        return run_id, True
    except Exception:
        session.rollback()
    failed = IngestionRun(source=source, status="FAILED", records_found=records_found,
                          records_failed=records_found,
                          error_log="STARTED_AUDIT_FAILED; " + _summary(duplicate_count=0,
                                                                       invalid_count=0,
                                                                       codes=["AUDIT_START_FAILED"]),
                          finished_at=utc_now_naive())
    try:
        session.add(failed)
        session.flush()
        failed_id = failed.ingestion_id
        session.commit()
        return failed_id, False
    except Exception:
        session.rollback()
        raise IngestionAuditError("unable to persist STARTED or FAILED ingestion audit") from None


def finish_failed_run(session: Session, run_id: int, *, records_found: int,
                      duplicate_count: int, invalid_count: int, codes: list[str]) -> None:
    """Persist FAILED after canonical rollback in its own transaction."""
    session.rollback()
    try:
        run = session.get(IngestionRun, run_id)
        if run is None:
            raise IngestionAuditError("started ingestion audit row is missing")
        run.status = "FAILED"
        run.records_found = records_found
        run.records_inserted = 0
        run.records_updated = 0
        run.records_failed = records_found
        run.error_log = _summary(duplicate_count=duplicate_count,
                                 invalid_count=invalid_count, codes=codes)
        run.finished_at = utc_now_naive()
        session.commit()
    except Exception:
        session.rollback()
        raise IngestionAuditError("unable to persist FAILED ingestion audit") from None


def finish_completed_run(run: IngestionRun, *, records_found: int, records_inserted: int,
                         duplicate_count: int) -> None:
    run.status = "COMPLETED"
    run.records_found = records_found
    run.records_inserted = records_inserted
    run.records_updated = 0
    run.records_failed = 0
    run.error_log = _summary(duplicate_count=duplicate_count, invalid_count=0, codes=[])
    run.finished_at = utc_now_naive()

