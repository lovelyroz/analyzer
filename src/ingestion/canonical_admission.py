"""Pure all-or-nothing admission and logical persistence-plan preparation.

This module deliberately has no SQLAlchemy/session dependency. The returned
plan describes one REPORT_VERSION atomic unit for a future caller-owned
transaction; it is not an executable ORM write plan.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from enum import StrEnum
import re

from src.core.jalali import validate_jalali_date
from src.ingestion.excel.canonical_input import (
    ApprovedSelection,
    CanonicalInputCandidate,
    CanonicalInputSpec,
    DurationBasis,
    TemporalType,
    build_candidate,
)
from src.ingestion.excel.deterministic_matcher import TemplateMatchResult
from src.ingestion.excel.dto import CellValueKind, WorkbookObservation


class AdmissionCode(StrEnum):
    BATCH_EMPTY = "BATCH_EMPTY"
    BATCH_CONTEXT_INVALID = "BATCH_CONTEXT_INVALID"
    CANDIDATE_TYPE_INVALID = "CANDIDATE_TYPE_INVALID"
    RAW_ROW_PROHIBITED = "RAW_ROW_PROHIBITED"
    CALCULATED_FACT_PROHIBITED = "CALCULATED_FACT_PROHIBITED"
    IDENTITY_MISSING = "IDENTITY_MISSING"
    APPROVAL_REFERENCE_MISSING = "APPROVAL_REFERENCE_MISSING"
    MAPPING_AMBIGUOUS = "MAPPING_AMBIGUOUS"
    REPORT_VERSION_MISMATCH = "REPORT_VERSION_MISMATCH"
    COMPANY_MISMATCH = "COMPANY_MISMATCH"
    SOURCE_ARTIFACT_MISMATCH = "SOURCE_ARTIFACT_MISMATCH"
    CANDIDATE_INVALID = "CANDIDATE_INVALID"
    VALUE_MISSING = "VALUE_MISSING"
    VALUE_INVALID = "VALUE_INVALID"
    SOURCE_NUMBER_MISMATCH = "SOURCE_NUMBER_MISMATCH"
    SOURCE_FLOAT_PRECISION_UNAVAILABLE = "SOURCE_FLOAT_PRECISION_UNAVAILABLE"
    ZERO_FALLBACK_INVALID = "ZERO_FALLBACK_INVALID"
    ZERO_FALLBACK_APPROVAL_MISSING = "ZERO_FALLBACK_APPROVAL_MISSING"
    OTHER_APPROVAL_MISSING = "OTHER_APPROVAL_MISSING"
    INTEGER_RANGE_EXCEEDED = "INTEGER_RANGE_EXCEEDED"
    INTRA_BATCH_CONFLICT = "INTRA_BATCH_CONFLICT"
    DUPLICATE_PROVENANCE_CONFLICT = "DUPLICATE_PROVENANCE_CONFLICT"
    EXISTING_FACT_CONFLICT = "EXISTING_FACT_CONFLICT"
    EXISTING_VERSION_CONFLICT = "EXISTING_VERSION_CONFLICT"
    SOURCE_REVISION_REUSED = "SOURCE_REVISION_REUSED"
    SUPERSESSION_TARGET_MISSING = "SUPERSESSION_TARGET_MISSING"
    SUPERSESSION_IDENTITY_INVALID = "SUPERSESSION_IDENTITY_INVALID"
    ZERO_FALLBACK_SOURCE_UNSUPPORTED = "ZERO_FALLBACK_SOURCE_UNSUPPORTED"


class ValueOrigin(StrEnum):
    SOURCE_REPORTED = "SOURCE_REPORTED"
    ZERO_FALLBACK = "ZERO_FALLBACK"


class SubmittedRecordKind(StrEnum):
    CANONICAL_INPUT = "CANONICAL_INPUT"
    RAW_ROW = "RAW_ROW"
    CALCULATED = "CALCULATED"


@dataclass(frozen=True, slots=True)
class AdmissionDiagnostic:
    code: AdmissionCode
    identity: tuple[str, ...] = ()


class AdmissionRejected(ValueError):
    """Whole-batch rejection with stable, sorted diagnostics."""

    def __init__(self, diagnostics: tuple[AdmissionDiagnostic, ...]) -> None:
        self.diagnostics = diagnostics
        codes = ",".join(item.code.value for item in diagnostics)
        super().__init__(codes)


@dataclass(frozen=True, slots=True)
class RevisionContext:
    report_id: str
    report_version_id: str
    company_id: str
    source_identity: str
    revision_identity: str
    source_artifact_sha256: str
    extraction_standard_id: str
    extraction_standard_approval_ref: str
    supersedes_version_id: str | None = None


@dataclass(frozen=True, slots=True)
class CandidateSubmission:
    candidate: object
    record_kind: SubmittedRecordKind = SubmittedRecordKind.CANONICAL_INPUT
    value_origin: ValueOrigin = ValueOrigin.SOURCE_REPORTED
    zero_fallback_rule: ApprovedSelection | None = None
    other_metric_approval: ApprovedSelection | None = None


@dataclass(frozen=True, slots=True)
class ExistingReportVersion:
    report_id: str
    report_version_id: str
    source_identity: str
    revision_identity: str
    source_artifact_sha256: str
    extraction_standard_id: str


@dataclass(frozen=True, slots=True)
class PlannedFact:
    company_id: str
    report_type_id: str
    report_id: str
    report_version_id: str
    period_identity: tuple[str, tuple[int, int, int], tuple[int, int, int]]
    metric_id: str
    dimensions: tuple[tuple[str, str], ...]
    source_value_decimal: Decimal
    value_integer: int
    value_origin: ValueOrigin
    source_unit: str
    source_currency: str
    source_scale: str
    duration_basis: str | None
    extraction_standard_id: str
    extraction_standard_approval_ref: str
    source_identity: str
    revision_identity: str
    source_artifact_sha256: str
    template_id: str
    template_version: str
    template_sha256: str
    extraction_owner: str
    approval_references: tuple[tuple[str, str, str], ...]

    @property
    def identity(self) -> tuple[object, ...]:
        return (
            self.report_version_id,
            self.period_identity,
            self.metric_id,
            self.dimensions,
        )

    @property
    def payload(self) -> tuple[object, ...]:
        return (
            self.company_id,
            self.report_type_id,
            self.metric_id,
            self.dimensions,
            self.source_value_decimal,
            self.value_integer,
            self.value_origin,
            self.source_unit,
            self.source_currency,
            self.source_scale,
            self.period_identity[0],
            self.duration_basis,
        )

    @property
    def provenance(self) -> tuple[object, ...]:
        source_mapping = tuple(
            item for item in self.approval_references
            if item[0] in ("source_label", "source_header")
        )
        return (
            self.template_id, self.template_version, self.template_sha256,
            source_mapping, self.extraction_owner, self.approval_references,
        )


@dataclass(frozen=True, slots=True)
class CanonicalPersistencePlan:
    report_id: str
    report_version_id: str
    source_identity: str
    revision_identity: str
    source_artifact_sha256: str
    extraction_standard_id: str
    extraction_standard_approval_ref: str
    supersedes_version_id: str | None
    facts: tuple[PlannedFact, ...]
    duplicate_count: int
    unchanged_existing_count: int
    preserved_report_version_ids: tuple[str, ...]
    persistence_target: str = "DB-DES-001 logical canonical input contract"
    atomicity_unit: str = "REPORT_VERSION"
    transaction_owner: str = "CALLER"
    execution_allowed: bool = False
    physical_persistence_compatible: bool = False
    persistence_block_code: str = "PHYSICAL_SCHEMA_INCOMPATIBLE"


_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
_DECIMAL_TEXT = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
_INT64_MIN = -(2**63)
_INT64_MAX = (2**63) - 1


def prepare_canonical_batch(
    submissions: tuple[CandidateSubmission, ...] | list[CandidateSubmission],
    *,
    revision: RevisionContext,
    existing_versions: tuple[ExistingReportVersion, ...] = (),
    existing_facts: tuple[PlannedFact, ...] = (),
) -> CanonicalPersistencePlan:
    """Validate a whole report-version batch and return a non-executable plan.

    This function never opens a database, starts a transaction, commits, or
    mutates its inputs. Existing state is supplied as immutable snapshots.
    """
    diagnostics: list[AdmissionDiagnostic] = []
    if not submissions:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.BATCH_EMPTY))
    if not isinstance(revision, RevisionContext):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.BATCH_CONTEXT_INVALID))
        raise _rejected(diagnostics)
    _validate_revision(revision, diagnostics)
    if any(item.code is AdmissionCode.BATCH_CONTEXT_INVALID for item in diagnostics):
        raise _rejected(diagnostics)

    known_versions: dict[str, ExistingReportVersion] = {}
    for version in existing_versions:
        prior = known_versions.get(version.report_version_id)
        if prior is not None:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.EXISTING_VERSION_CONFLICT))
        else:
            known_versions[version.report_version_id] = version
    if revision.supersedes_version_id is not None:
        prior = known_versions.get(revision.supersedes_version_id)
        if prior is None:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.SUPERSESSION_TARGET_MISSING))
        elif prior.report_id != revision.report_id or prior.report_version_id == revision.report_version_id:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.SUPERSESSION_IDENTITY_INVALID))
        elif prior.revision_identity == revision.revision_identity:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.SOURCE_REVISION_REUSED))

    same_revision_versions = [
        item for item in existing_versions
        if item.source_identity == revision.source_identity and item.revision_identity == revision.revision_identity
    ]
    if any(item.report_version_id != revision.report_version_id for item in same_revision_versions):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.SOURCE_REVISION_REUSED))

    existing_version = known_versions.get(revision.report_version_id)
    if existing_version is not None and (
        existing_version.report_id != revision.report_id
        or existing_version.source_identity != revision.source_identity
        or existing_version.revision_identity != revision.revision_identity
        or not isinstance(existing_version.source_artifact_sha256, str)
        or existing_version.source_artifact_sha256.lower() != revision.source_artifact_sha256.lower()
        or existing_version.extraction_standard_id != revision.extraction_standard_id
    ):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.EXISTING_VERSION_CONFLICT))

    planned: list[PlannedFact] = []
    for submission in submissions:
        if isinstance(submission, CanonicalInputCandidate):
            submission = CandidateSubmission(candidate=submission)
        if not isinstance(submission, CandidateSubmission):
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_TYPE_INVALID))
            continue
        if not isinstance(submission.record_kind, SubmittedRecordKind):
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_TYPE_INVALID))
            continue
        if submission.record_kind is SubmittedRecordKind.RAW_ROW:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.RAW_ROW_PROHIBITED))
            continue
        if submission.record_kind is SubmittedRecordKind.CALCULATED:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.CALCULATED_FACT_PROHIBITED))
            continue
        if not isinstance(submission.candidate, CanonicalInputCandidate):
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_TYPE_INVALID))
            continue
        fact = _prepare_fact(submission, revision, diagnostics)
        if fact is not None:
            planned.append(fact)

    if diagnostics:
        raise _rejected(diagnostics)

    # Canonical identity is version + exact period + metric + approved dimensions.
    unique_by_identity: dict[tuple[object, ...], PlannedFact] = {}
    duplicate_count = 0
    for fact in planned:
        prior = unique_by_identity.get(fact.identity)
        if prior is None:
            unique_by_identity[fact.identity] = fact
        elif prior.payload == fact.payload:
            if prior.provenance == fact.provenance:
                duplicate_count += 1
            else:
                diagnostics.append(AdmissionDiagnostic(
                    AdmissionCode.DUPLICATE_PROVENANCE_CONFLICT,
                    _identity_text(fact.identity),
                ))
        else:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.INTRA_BATCH_CONFLICT, _identity_text(fact.identity)))

    existing_by_identity: dict[tuple[object, ...], PlannedFact] = {}
    for old_fact in existing_facts:
        if old_fact.identity in existing_by_identity:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.EXISTING_FACT_CONFLICT, _identity_text(old_fact.identity)))
        else:
            existing_by_identity[old_fact.identity] = old_fact
    output_facts: list[PlannedFact] = []
    unchanged_existing_count = 0
    for identity, fact in unique_by_identity.items():
        old = existing_by_identity.get(identity)
        if old is None:
            if existing_version is not None:
                diagnostics.append(AdmissionDiagnostic(AdmissionCode.EXISTING_FACT_CONFLICT, _identity_text(identity)))
            else:
                output_facts.append(fact)
        elif (
            old.payload == fact.payload
            and old.provenance == fact.provenance
            and old.revision_identity == fact.revision_identity
            and old.extraction_standard_id == fact.extraction_standard_id
            and old.source_identity == fact.source_identity
        ):
            unchanged_existing_count += 1
        else:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.EXISTING_FACT_CONFLICT, _identity_text(identity)))

    # Facts already attached to a known version but absent from the submitted batch
    # indicate an incomplete replay; never treat it as an incremental append.
    if existing_version is not None:
        old_keys = {fact.identity for fact in existing_facts if fact.report_version_id == revision.report_version_id}
        new_keys = set(unique_by_identity)
        if old_keys != new_keys:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.EXISTING_VERSION_CONFLICT))

    if diagnostics:
        raise _rejected(diagnostics)

    return CanonicalPersistencePlan(
        report_id=revision.report_id,
        report_version_id=revision.report_version_id,
        source_identity=revision.source_identity,
        revision_identity=revision.revision_identity,
        source_artifact_sha256=revision.source_artifact_sha256.lower(),
        extraction_standard_id=revision.extraction_standard_id,
        extraction_standard_approval_ref=revision.extraction_standard_approval_ref,
        supersedes_version_id=revision.supersedes_version_id,
        facts=tuple(sorted(output_facts, key=lambda item: _identity_text(item.identity))),
        duplicate_count=duplicate_count,
        unchanged_existing_count=unchanged_existing_count,
        preserved_report_version_ids=tuple(sorted({item.report_version_id for item in existing_versions})),
    )


def build_candidate_submission(
    observation: WorkbookObservation,
    match: TemplateMatchResult,
    *,
    coordinate: str,
    spec: CanonicalInputSpec,
    zero_fallback_rule: ApprovedSelection | None = None,
    other_metric_approval: ApprovedSelection | None = None,
) -> CandidateSubmission:
    """Build and bind a candidate, permitting BLANK only with explicit fallback approval."""
    candidate = build_candidate(
        observation, match, coordinate=coordinate, spec=spec,
        zero_fallback_rule=zero_fallback_rule,
    )
    if zero_fallback_rule is None:
        return CandidateSubmission(candidate, other_metric_approval=other_metric_approval)
    return CandidateSubmission(
        candidate,
        value_origin=ValueOrigin.ZERO_FALLBACK,
        zero_fallback_rule=zero_fallback_rule,
        other_metric_approval=other_metric_approval,
    )


def _validate_revision(revision: RevisionContext, diagnostics: list[AdmissionDiagnostic]) -> None:
    required = (
        revision.report_id, revision.report_version_id, revision.company_id,
        revision.source_identity, revision.revision_identity,
        revision.extraction_standard_id, revision.extraction_standard_approval_ref,
    )
    if any(not isinstance(value, str) or not value.strip() for value in required):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.BATCH_CONTEXT_INVALID))
    if not isinstance(revision.source_artifact_sha256, str) or not _SHA256.fullmatch(revision.source_artifact_sha256):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.BATCH_CONTEXT_INVALID))


def _prepare_fact(
    submission: CandidateSubmission,
    revision: RevisionContext,
    diagnostics: list[AdmissionDiagnostic],
) -> PlannedFact | None:
    candidate = submission.candidate
    assert isinstance(candidate, CanonicalInputCandidate)
    initial_diagnostic_count = len(diagnostics)
    key = (candidate.report_version_id, candidate.metric_id)
    required_ids = (
        candidate.company_id, candidate.report_type_id, candidate.report_version_id,
        candidate.metric_id, candidate.source_unit, candidate.source_currency,
        candidate.source_scale, candidate.period_mapping_id, candidate.template_id,
        candidate.template_version, candidate.extraction_owner,
    )
    required_refs = (
        candidate.company_approval_ref, candidate.report_type_approval_ref,
        candidate.report_version_approval_ref, candidate.metric_approval_ref,
        candidate.source_unit_approval_ref, candidate.source_currency_approval_ref,
        candidate.source_scale_approval_ref, candidate.period_mapping_approval_ref,
    )
    identity_missing = any(not isinstance(value, str) or not value.strip() for value in required_ids)
    approvals_missing = any(not isinstance(value, str) or not value.strip() for value in required_refs)
    if identity_missing:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.IDENTITY_MISSING, key))
    if approvals_missing:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.APPROVAL_REFERENCE_MISSING, key))
    if identity_missing or approvals_missing:
        return None
    if candidate.report_version_id != revision.report_version_id:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.REPORT_VERSION_MISMATCH, key))
    if candidate.company_id != revision.company_id:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.COMPANY_MISMATCH, key))
    if not isinstance(candidate.source_workbook_sha256, str):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_INVALID, key))
    elif candidate.source_workbook_sha256.lower() != revision.source_artifact_sha256.lower():
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.SOURCE_ARTIFACT_MISMATCH, key))
    if (not isinstance(candidate.template_sha256, str)
            or not _SHA256.fullmatch(candidate.template_sha256)
            or not isinstance(candidate.source_workbook_sha256, str)
            or not _SHA256.fullmatch(candidate.source_workbook_sha256)):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_INVALID, key))

    if candidate.source_label_id is not None and not candidate.source_label_approval_ref:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.APPROVAL_REFERENCE_MISSING, key))
    if candidate.source_header_id is not None and not candidate.source_header_approval_ref:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.APPROVAL_REFERENCE_MISSING, key))
    if (not isinstance(candidate.dimensions, tuple)
            or not isinstance(candidate.dimension_approval_refs, tuple)
            or any(not isinstance(item, tuple) or len(item) != 2 for item in candidate.dimensions)
            or any(not isinstance(item, tuple) or len(item) != 4 for item in candidate.dimension_approval_refs)):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_INVALID, key))
    elif len(candidate.dimensions) != len(candidate.dimension_approval_refs):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.APPROVAL_REFERENCE_MISSING, key))
    elif any(
        len(refs) != 4 or not all(isinstance(value, str) and value.strip() for value in refs)
        or (dimension, value) != (refs[0], refs[2])
        for (dimension, value), refs in zip(candidate.dimensions, candidate.dimension_approval_refs)
    ):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.APPROVAL_REFERENCE_MISSING, key))
    if len({dimension for dimension, _ in candidate.dimensions}) != len(candidate.dimensions):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.MAPPING_AMBIGUOUS, key))

    try:
        start = validate_jalali_date(candidate.period_start_jalali, label="period start")
        end = validate_jalali_date(candidate.period_end_jalali, label="period end")
        if start > end:
            raise ValueError("period range is reversed")
        if candidate.temporal_type is TemporalType.INSTANT:
            if start != end or candidate.duration_basis is not None:
                raise ValueError("invalid instant temporal shape")
        elif candidate.temporal_type is TemporalType.DURATION:
            if start == end or candidate.duration_basis not in (DurationBasis.YTD, DurationBasis.STANDALONE):
                raise ValueError("invalid duration temporal shape")
        else:
            raise ValueError("temporal type missing or invalid")
    except (ValueError, TypeError):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.CANDIDATE_INVALID, key))
        return None

    if not isinstance(candidate.value, Decimal) or not candidate.value.is_finite():
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_INVALID, key))
        return None
    if submission.value_origin is ValueOrigin.SOURCE_REPORTED:
        if candidate.source_value_kind is CellValueKind.BLANK:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_MISSING, key))
        elif candidate.source_value_kind is CellValueKind.PRESENT_TEXT:
            if candidate.source_text is None:
                diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_MISSING, key))
            else:
                try:
                    if not _DECIMAL_TEXT.fullmatch(candidate.source_text):
                        raise InvalidOperation
                    lexical_value = Decimal(candidate.source_text)
                except (InvalidOperation, ValueError):
                    diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_INVALID, key))
                else:
                    if not lexical_value.is_finite() or lexical_value != candidate.value:
                        diagnostics.append(AdmissionDiagnostic(AdmissionCode.SOURCE_NUMBER_MISMATCH, key))
        elif candidate.source_value_kind is CellValueKind.PRESENT_NUMBER:
            if type(candidate.source_native_integer) is not int:
                diagnostics.append(AdmissionDiagnostic(AdmissionCode.SOURCE_FLOAT_PRECISION_UNAVAILABLE, key))
            elif Decimal(candidate.source_native_integer) != candidate.value:
                diagnostics.append(AdmissionDiagnostic(AdmissionCode.SOURCE_NUMBER_MISMATCH, key))
        else:
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_MISSING, key))
    elif submission.value_origin is ValueOrigin.ZERO_FALLBACK:
        rule = submission.zero_fallback_rule
        if (
            rule is None or not rule.approved or rule.candidate_count != 1
            or not rule.identity or rule.identity != candidate.metric_id or not rule.approval_ref
        ):
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.ZERO_FALLBACK_APPROVAL_MISSING, key))
        if (
            candidate.source_value_kind is not CellValueKind.BLANK
            or candidate.source_text is not None or candidate.source_native_integer is not None
            or candidate.value != Decimal(0)
        ):
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.ZERO_FALLBACK_SOURCE_UNSUPPORTED, key))
    else:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_INVALID, key))

    other_approval_ref: str | None = None
    if candidate.metric_id.startswith("OTHER_"):
        other = submission.other_metric_approval
        if (
            other is None or not other.approved or other.candidate_count != 1
            or other.identity != candidate.metric_id or not other.approval_ref
        ):
            diagnostics.append(AdmissionDiagnostic(AdmissionCode.OTHER_APPROVAL_MISSING, key))
        else:
            other_approval_ref = other.approval_ref

    try:
        rounded = int(candidate.value.to_integral_value(rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError, OverflowError):
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.VALUE_INVALID, key))
        return None
    if rounded < _INT64_MIN or rounded > _INT64_MAX:
        diagnostics.append(AdmissionDiagnostic(AdmissionCode.INTEGER_RANGE_EXCEEDED, key))

    if len(diagnostics) != initial_diagnostic_count:
        return None

    approvals: list[tuple[str, str, str]] = [
        ("company", candidate.company_id, candidate.company_approval_ref),
        ("report_type", candidate.report_type_id, candidate.report_type_approval_ref),
        ("report_version", candidate.report_version_id, candidate.report_version_approval_ref),
        ("metric", candidate.metric_id, candidate.metric_approval_ref),
        ("unit", candidate.source_unit, candidate.source_unit_approval_ref),
        ("currency", candidate.source_currency, candidate.source_currency_approval_ref),
        ("scale", candidate.source_scale, candidate.source_scale_approval_ref),
        ("period_mapping", candidate.period_mapping_id, candidate.period_mapping_approval_ref),
    ]
    if candidate.source_label_id is not None:
        approvals.append(("source_label", candidate.source_label_id, candidate.source_label_approval_ref or ""))
    if candidate.source_header_id is not None:
        approvals.append(("source_header", candidate.source_header_id, candidate.source_header_approval_ref or ""))
    approvals.extend(("dimension", dim, ref) for dim, ref, _, _ in candidate.dimension_approval_refs)
    approvals.extend(("dimension_value", value, ref) for _, _, value, ref in candidate.dimension_approval_refs)
    if other_approval_ref:
        approvals.append(("other_metric_rule", candidate.metric_id, other_approval_ref))
    if submission.value_origin is ValueOrigin.ZERO_FALLBACK and submission.zero_fallback_rule:
        approvals.append(("zero_fallback_rule", submission.zero_fallback_rule.identity or "", submission.zero_fallback_rule.approval_ref or ""))

    return PlannedFact(
        company_id=candidate.company_id,
        report_type_id=candidate.report_type_id,
        report_id=revision.report_id,
        report_version_id=candidate.report_version_id,
        period_identity=(candidate.temporal_type.value, start, end),
        metric_id=candidate.metric_id,
        dimensions=tuple(sorted(candidate.dimensions)),
        source_value_decimal=candidate.value,
        value_integer=rounded,
        value_origin=submission.value_origin,
        source_unit=candidate.source_unit,
        source_currency=candidate.source_currency,
        source_scale=candidate.source_scale,
        duration_basis=candidate.duration_basis.value if candidate.duration_basis else None,
        extraction_standard_id=revision.extraction_standard_id,
        extraction_standard_approval_ref=revision.extraction_standard_approval_ref,
        source_identity=revision.source_identity,
        revision_identity=revision.revision_identity,
        source_artifact_sha256=revision.source_artifact_sha256.lower(),
        template_id=candidate.template_id,
        template_version=candidate.template_version,
        template_sha256=candidate.template_sha256.lower(),
        extraction_owner=candidate.extraction_owner,
        approval_references=tuple(sorted(set(approvals))),
    )


def _identity_text(identity: tuple[object, ...]) -> tuple[str, ...]:
    return tuple(repr(part) for part in identity)


def _rejected(diagnostics: list[AdmissionDiagnostic]) -> AdmissionRejected:
    unique = {(item.code, item.identity): item for item in diagnostics}
    return AdmissionRejected(tuple(unique[key] for key in sorted(unique, key=lambda item: (item[0].value, item[1]))))
