"""Authoritative, exact-scope resolution for canonical catalog approvals."""
from __future__ import annotations

import json
from typing import Mapping

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.canonical import CanonicalApproval


class ApprovalResolutionError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def canonical_scope_json(scope: Mapping[str, str] | None = None) -> str:
    value = {} if scope is None else dict(scope)
    if any(not isinstance(key, str) or not isinstance(item, str) for key, item in value.items()):
        raise ApprovalResolutionError("APPROVAL_SCOPE_INVALID")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def resolve_approval(
    session: Session,
    *,
    approval_kind: str,
    external_identity: str,
    expected_scope: Mapping[str, str] | None,
    approval_ref: str | None = None,
) -> CanonicalApproval:
    """Resolve one active catalog row and reject stale, foreign, or ambiguous approvals."""
    if not approval_kind or not external_identity:
        raise ApprovalResolutionError("APPROVAL_IDENTITY_MISSING")
    scope_json = canonical_scope_json(expected_scope)
    if approval_ref is not None:
        row = session.scalar(select(CanonicalApproval).where(CanonicalApproval.approval_ref == approval_ref))
        if row is None:
            raise ApprovalResolutionError("APPROVAL_MISSING")
        if not row.is_active:
            raise ApprovalResolutionError("APPROVAL_REVOKED")
        if row.approval_kind != approval_kind or row.external_identity != external_identity:
            raise ApprovalResolutionError("APPROVAL_SCOPE_MISMATCH")
        if row.scope_json != scope_json:
            raise ApprovalResolutionError("APPROVAL_SCOPE_MISMATCH")

    matches = session.scalars(select(CanonicalApproval).where(
        CanonicalApproval.approval_kind == approval_kind,
        CanonicalApproval.external_identity == external_identity,
        CanonicalApproval.scope_json == scope_json,
        CanonicalApproval.is_active.is_(True),
    ).order_by(CanonicalApproval.approval_id)).all()
    if len(matches) > 1:
        raise ApprovalResolutionError("APPROVAL_AMBIGUOUS")
    if not matches:
        raise ApprovalResolutionError("APPROVAL_MISSING")
    if approval_ref is not None and matches[0].approval_ref != approval_ref:
        raise ApprovalResolutionError("APPROVAL_SCOPE_MISMATCH")
    return matches[0]
