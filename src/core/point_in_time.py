from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.models.report import ReportVersion


def select_report_version(
    session: Session,
    report_id: int,
    cutoff: datetime,
) -> ReportVersion | None:
    """Return the latest published report version available at the PIT cutoff."""
    return (
        session.query(ReportVersion)
        .filter(
            and_(
                ReportVersion.report_id == report_id,
                ReportVersion.publication_datetime <= cutoff,
            )
        )
        .order_by(
            ReportVersion.publication_datetime.desc(),
            ReportVersion.version_number.desc(),
        )
        .first()
    )
