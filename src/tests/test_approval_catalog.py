import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.ingestion.approval_catalog import (
    ApprovalResolutionError, canonical_scope_json, resolve_approval,
)
from src.models.canonical import CanonicalApproval


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    CanonicalApproval.__table__.create(engine)
    factory = sessionmaker(bind=engine)
    with factory() as db:
        yield db
    engine.dispose()


def _approval(session, reference="approved-1", *, scope=None, active=True):
    row = CanonicalApproval(
        approval_ref=reference,
        approval_kind="metric",
        external_identity="metric-revenue",
        scope_json=canonical_scope_json(scope),
        is_active=active,
    )
    session.add(row)
    session.flush()
    return row


def test_resolves_one_active_exact_scope_approval(session):
    expected = {"industry_code": "BANK", "report_type_id": "PERIODIC_FINANCIAL"}
    _approval(session, scope=expected)
    assert resolve_approval(
        session, approval_kind="metric", external_identity="metric-revenue",
        approval_ref="approved-1", expected_scope=expected,
    ).approval_ref == "approved-1"


def test_rejects_missing_approval(session):
    with pytest.raises(ApprovalResolutionError, match="APPROVAL_MISSING"):
        resolve_approval(session, approval_kind="metric", external_identity="metric-revenue",
                          approval_ref="unknown", expected_scope={})


def test_rejects_inactive_or_revoked_approval(session):
    _approval(session, active=False)
    with pytest.raises(ApprovalResolutionError, match="APPROVAL_REVOKED"):
        resolve_approval(session, approval_kind="metric", external_identity="metric-revenue",
                          approval_ref="approved-1", expected_scope={})


def test_rejects_reference_scoped_to_another_report_type(session):
    _approval(session, scope={"industry_code": "BANK", "report_type_id": "MONTHLY_ACTIVITY"})
    with pytest.raises(ApprovalResolutionError, match="APPROVAL_SCOPE_MISMATCH"):
        resolve_approval(session, approval_kind="metric", external_identity="metric-revenue",
                          approval_ref="approved-1",
                          expected_scope={"industry_code": "BANK", "report_type_id": "PERIODIC_FINANCIAL"})


def test_rejects_ambiguous_active_approvals_even_if_one_reference_was_supplied(session):
    expected = {"industry_code": "BANK"}
    _approval(session, "approved-1", scope=expected)
    _approval(session, "approved-2", scope=expected)
    with pytest.raises(ApprovalResolutionError, match="APPROVAL_AMBIGUOUS"):
        resolve_approval(session, approval_kind="metric", external_identity="metric-revenue",
                          approval_ref="approved-1", expected_scope=expected)
