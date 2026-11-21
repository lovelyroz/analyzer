"""Transactional writer and point-in-time reader for admitted Excel plans.

The writer resolves every external identity through explicit database bindings
and approval rows. It owns its SQLAlchemy session/transaction; no commit occurs
inside a fact loop. Legacy normalized tables are never written by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import hashlib
import json
import re
from typing import Mapping

from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker
from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter

from src.core.jalali import validate_jalali_date
from src.ingestion.approval_catalog import ApprovalResolutionError, resolve_approval
from src.ingestion.canonical_admission import CanonicalPersistencePlan, PlannedFact, ValueOrigin
from src.models.audit import IngestionRun
from src.models.canonical import (
    CanonicalApproval, CanonicalCompanyFiscalCalendar, CanonicalDimensionMember, CanonicalDimensionSet,
    CanonicalIngestionAudit,
    CanonicalFactProvenance, CanonicalFinancialFact, CanonicalFinancialPeriod,
    CanonicalIdentityBinding, CanonicalReport, CanonicalReportVersion,
)
from src.models.entity import Company, Industry
from src.models.normalized import FinancialMetric


class CanonicalWriteError(ValueError):
    """Stable, payload-free failure returned to the caller."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class ReportWriteMetadata:
    title: str
    version_number: int
    publication_datetime: datetime
    is_audited: bool
    is_restated: bool
    scenario_approval_ref: str
    scenario: str


@dataclass(frozen=True, slots=True)
class CanonicalWriteResult:
    ingestion_id: int
    report_version_id: int
    inserted_count: int
    duplicate_count: int
    rejected_count: int = 0


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_APPROVAL_KIND_ALIASES = {"unit": "source_unit", "currency": "source_currency", "scale": "source_scale"}


def write_canonical_plan(
    plan: CanonicalPersistencePlan,
    metadata: ReportWriteMetadata,
    session_factory: sessionmaker[Session],
    *,
    ingestion_id: int | None = None,
) -> CanonicalWriteResult:
    """Persist one whole report version or leave no canonical facts behind."""
    effective_ingestion_id = ingestion_id
    if effective_ingestion_id is None:
        found = len(plan.facts) if isinstance(plan, CanonicalPersistencePlan) and isinstance(plan.facts, tuple) else 0
        effective_ingestion_id = _start_run(session_factory, found)
    try:
        with session_factory() as session:
            with session.begin():
                result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
            return result
    except CanonicalWriteError as exc:
        _mark_failed(session_factory, effective_ingestion_id, exc.code, _plan_record_count(plan))
        raise
    except Exception as exc:
        _mark_failed(session_factory, effective_ingestion_id, "PERSISTENCE_FAILED", _plan_record_count(plan))
        raise CanonicalWriteError("PERSISTENCE_FAILED") from exc


def _write_in_transaction(
    session: Session,
    plan: CanonicalPersistencePlan,
    metadata: ReportWriteMetadata,
    ingestion_id: int | None,
) -> CanonicalWriteResult:
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
    first = plan.facts[0]

    existing = session.scalar(select(CanonicalReportVersion).where(
        CanonicalReportVersion.external_version_id == plan.report_version_id
    ))
    if existing is not None:
        report = session.get(CanonicalReport, existing.canonical_report_id)
        if report is None or not _same_version(session, existing, report, plan, metadata, company_id):
            raise CanonicalWriteError("REPORT_VERSION_CONFLICT")
        old_facts = session.scalars(select(CanonicalFinancialFact).where(
            CanonicalFinancialFact.report_version_id == existing.canonical_report_version_id
        )).all()
        if not _matches_existing_facts(session, old_facts, plan.facts, company_id, metadata):
            raise CanonicalWriteError("REPORT_VERSION_CONFLICT")
        duplicates = len(plan.facts) + plan.duplicate_count
        _complete_run(session, ingestion_id, 0, duplicates)
        assert ingestion_id is not None
        return CanonicalWriteResult(ingestion_id, existing.canonical_report_version_id, 0, duplicates)

    report = session.scalar(select(CanonicalReport).where(CanonicalReport.external_report_id == plan.report_id))
    if report is None:
        report = CanonicalReport(
            external_report_id=plan.report_id, company_id=company_id,
            report_type_id=first.report_type_id, title=metadata.title,
        )
        session.add(report)
        session.flush()
    elif (report.company_id != company_id or report.report_type_id != first.report_type_id
          or report.title != metadata.title):
        raise CanonicalWriteError("REPORT_IDENTITY_CONFLICT")

    reused_revision = session.scalar(select(CanonicalReportVersion).where(
        CanonicalReportVersion.canonical_report_id == report.canonical_report_id,
        CanonicalReportVersion.source_identity == plan.source_identity,
        CanonicalReportVersion.revision_identity == plan.revision_identity,
    ))
    if reused_revision is not None:
        raise CanonicalWriteError("SOURCE_REVISION_REUSED")
    reused_number = session.scalar(select(CanonicalReportVersion).where(
        CanonicalReportVersion.canonical_report_id == report.canonical_report_id,
        CanonicalReportVersion.version_number == metadata.version_number,
    ))
    if reused_number is not None:
        raise CanonicalWriteError("REPORT_VERSION_CONFLICT")
    highest_version = session.scalar(select(func.max(CanonicalReportVersion.version_number)).where(
        CanonicalReportVersion.canonical_report_id == report.canonical_report_id,
    ))
    if highest_version is not None and metadata.version_number <= highest_version:
        raise CanonicalWriteError("REPORT_VERSION_NOT_APPEND_ONLY")

    prior = None
    if plan.supersedes_version_id:
        prior = session.scalar(select(CanonicalReportVersion).where(
            CanonicalReportVersion.external_version_id == plan.supersedes_version_id,
            CanonicalReportVersion.canonical_report_id == report.canonical_report_id,
        ))
        if prior is None:
            raise CanonicalWriteError("SUPERSESSION_TARGET_MISSING")
    # Version numbers are append-only and cannot silently replace a prior row.
    version = CanonicalReportVersion(
        canonical_report_id=report.canonical_report_id,
        external_version_id=plan.report_version_id,
        version_number=metadata.version_number,
        publication_datetime=_normalize_datetime(metadata.publication_datetime),
        is_audited=metadata.is_audited,
        is_restated=metadata.is_restated,
        scenario_approval_ref=metadata.scenario_approval_ref,
        source_identity=plan.source_identity,
        revision_identity=plan.revision_identity,
        source_artifact_sha256=plan.source_artifact_sha256.lower(),
        extraction_standard_id=plan.extraction_standard_id,
        extraction_standard_approval_ref=plan.extraction_standard_approval_ref,
        template_id=first.template_id, template_version=first.template_version,
        template_sha256=first.template_sha256.lower(), template_approval_ref=template_approval_ref,
        extraction_owner=first.extraction_owner,
        supersedes_version_id=prior.canonical_report_version_id if prior else None,
    )
    session.add(version)
    session.flush()

    inserted = 0
    for fact in plan.facts:
        period = _get_or_create_period(session, fact, company_id)
        dimension_set = _get_or_create_dimensions(session, fact)
        metric_id = _resolve_binding(
            session, "metric", fact.metric_id, _approval_ref(fact, "metric"),
            {"industry_code": industry_code},
        )
        metric = session.get(FinancialMetric, metric_id)
        if metric is None:
            raise CanonicalWriteError("METRIC_NOT_FOUND")
        value_state = "ZERO_FALLBACK" if fact.value_origin is ValueOrigin.ZERO_FALLBACK else "REPORTED_VALUE"
        session.add(CanonicalFinancialFact(
            report_version_id=version.canonical_report_version_id,
            period_id=period.period_id, metric_id=metric_id,
            dimension_set_id=dimension_set.dimension_set_id,
            temporal_type=fact.period_identity[0],
            duration_basis=fact.duration_basis,
            value_integer=fact.value_integer, value_state=value_state,
            value_origin=fact.value_origin.value,
            source_unit=fact.source_unit, source_currency=fact.source_currency,
            source_scale=fact.source_scale, scenario=metadata.scenario,
        ))
        session.flush()
        stored = session.scalar(select(CanonicalFinancialFact).where(
            CanonicalFinancialFact.report_version_id == version.canonical_report_version_id,
            CanonicalFinancialFact.period_id == period.period_id,
            CanonicalFinancialFact.metric_id == metric_id,
            CanonicalFinancialFact.dimension_set_id == dimension_set.dimension_set_id,
        ))
        if stored is None:
            raise CanonicalWriteError("FACT_WRITE_FAILED")
        refs_json = json.dumps(fact.approval_references, ensure_ascii=False, separators=(",", ":"))
        session.add(CanonicalFactProvenance(
            fact_id=stored.fact_id, source_identity=fact.source_identity,
            revision_identity=fact.revision_identity,
            source_artifact_sha256=fact.source_artifact_sha256.lower(),
            worksheet_ordinal=fact.worksheet_ordinal, worksheet_name=fact.worksheet_name,
            source_coordinate=fact.source_coordinate, source_value_kind=fact.source_value_kind,
            extraction_owner=fact.extraction_owner,
            source_decimal_text=format(fact.source_value_decimal, "f"),
            source_token=fact.source_token,
            approval_references_json=refs_json,
        ))
        inserted += 1

    _complete_run(session, ingestion_id, inserted, plan.duplicate_count)
    assert ingestion_id is not None
    return CanonicalWriteResult(ingestion_id, version.canonical_report_version_id,
                                inserted, plan.duplicate_count)


def resolve_plan_approvals(
    session: Session,
    plan: CanonicalPersistencePlan,
    metadata: ReportWriteMetadata,
) -> tuple[int, str, str]:
    """Shared approval boundary used by the Excel adapter and transactional writer."""
    _validate_plan_envelope(plan, metadata)
    if not plan.facts:
        raise CanonicalWriteError("BATCH_EMPTY")
    first = plan.facts[0]
    company_binding = _active_binding(session, "company", first.company_id)
    if company_binding is None or company_binding.approval_ref != _approval_ref(first, "company"):
        raise CanonicalWriteError("IDENTITY_BINDING_NOT_RESOLVED")
    company_id = company_binding.internal_id
    if any(item.company_id != first.company_id or item.report_id != plan.report_id
           or item.report_version_id != plan.report_version_id
           or item.report_type_id != first.report_type_id
           or item.source_identity != plan.source_identity
           or item.revision_identity != plan.revision_identity
           or item.source_artifact_sha256 != plan.source_artifact_sha256
           or item.extraction_standard_id != plan.extraction_standard_id
           or item.extraction_standard_approval_ref != plan.extraction_standard_approval_ref
           for item in plan.facts):
        raise CanonicalWriteError("PLAN_IDENTITY_MISMATCH")
    company = session.get(Company, company_id)
    if company is None:
        raise CanonicalWriteError("COMPANY_NOT_FOUND")
    industry = session.get(Industry, company.industry_id)
    if industry is None or industry.industry_code != "BANK":
        raise CanonicalWriteError("INDUSTRY_OUT_OF_SCOPE")
    _check_approval(session, "company", first.company_id, company_binding.approval_ref,
                    scope={"industry_code": industry.industry_code})
    industry_binding = _active_binding(session, "industry", industry.industry_code)
    if industry_binding is None or industry_binding.internal_id != industry.industry_id:
        raise CanonicalWriteError("INDUSTRY_BINDING_NOT_RESOLVED")
    _check_approval(session, "industry", industry.industry_code, industry_binding.approval_ref, scope={})
    _check_approval(session, "scenario", metadata.scenario, metadata.scenario_approval_ref, scope={})
    _check_approval(session, "extraction_standard", plan.extraction_standard_id,
                    plan.extraction_standard_approval_ref,
                    scope={"industry_code": industry.industry_code, "report_type_id": first.report_type_id})
    template_approval_refs = {
        _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    }
    if len(template_approval_refs) != 1:
        raise CanonicalWriteError("TEMPLATE_VERSION_MISMATCH")
    template_approval_ref = next(iter(template_approval_refs))
    _validate_report_calendar(session, plan.facts, company_id, first.report_type_id, industry.industry_code)
    return company_id, industry.industry_code, template_approval_ref


def ingest_excel_source(
    source: object,
    *,
    template: object,
    selections_by_coordinate: Mapping[str, object],
    revision: object,
    metadata: ReportWriteMetadata,
    session_factory: sessionmaker[Session],
    **adapter_options: object,
) -> tuple[object, CanonicalWriteResult]:
    """Run reader→matcher→admission→writer with a durable STARTED audit row."""
    from src.ingestion.excel.adapter import adapt_excel_source

    with session_factory() as session:
        run = IngestionRun(source="EXCEL", status="STARTED", records_found=0,
                           records_inserted=0, records_updated=0, records_failed=0)
        session.add(run)
        session.commit()
        ingestion_id = run.ingestion_id

    def validate_approvals(plan: CanonicalPersistencePlan) -> None:
        with session_factory() as validation_session:
            with validation_session.begin():
                resolve_plan_approvals(validation_session, plan, metadata)

    try:
        adapted = adapt_excel_source(
            source, template=template, selections_by_coordinate=selections_by_coordinate,
            admit=True, revision=revision, approval_validator=validate_approvals,
            **adapter_options,
        )
        if adapted.diagnostics or adapted.admission_plan is None:
            failure_code = adapted.diagnostics[0].code if adapted.diagnostics else "EXCEL_ADMISSION_REJECTED"
            _mark_failed(session_factory, ingestion_id, failure_code, max(1, len(adapted.submissions)))
            raise CanonicalWriteError(failure_code)
        with session_factory() as session:
            with session.begin():
                audit = session.get(IngestionRun, ingestion_id)
                if audit is None or audit.status != "STARTED":
                    raise CanonicalWriteError("INGESTION_AUDIT_INVALID")
                audit.records_found = len(adapted.submissions)
        result = write_canonical_plan(adapted.admission_plan, metadata, session_factory,
                                      ingestion_id=ingestion_id)
        return adapted, result
    except CanonicalWriteError:
        raise
    except Exception as exc:
        _mark_failed(session_factory, ingestion_id, "EXCEL_INGESTION_FAILED", 1)
        raise CanonicalWriteError("EXCEL_INGESTION_FAILED") from exc


def _validate_plan_envelope(plan: CanonicalPersistencePlan, metadata: ReportWriteMetadata) -> None:
    if not isinstance(plan, CanonicalPersistencePlan) or not plan.execution_allowed or not plan.physical_persistence_compatible:
        raise CanonicalWriteError("PLAN_NOT_EXECUTABLE")
    if (not isinstance(metadata, ReportWriteMetadata)
            or not isinstance(metadata.title, str) or not metadata.title.strip()
            or type(metadata.version_number) is not int or metadata.version_number < 1):
        raise CanonicalWriteError("REPORT_METADATA_INVALID")
    if type(metadata.is_audited) is not bool or type(metadata.is_restated) is not bool:
        raise CanonicalWriteError("REPORT_VERSION_FLAGS_INVALID")
    if not isinstance(metadata.scenario, str) or metadata.scenario not in {"ACTUAL", "FORECAST", "PLAN"}:
        raise CanonicalWriteError("SCENARIO_INVALID")
    if not isinstance(metadata.scenario_approval_ref, str) or not metadata.scenario_approval_ref.strip():
        raise CanonicalWriteError("SCENARIO_APPROVAL_MISSING")
    if (not isinstance(plan.report_id, str) or not plan.report_id.strip()
            or not isinstance(plan.report_version_id, str) or not plan.report_version_id.strip()
            or not isinstance(plan.facts, tuple) or not plan.facts):
        raise CanonicalWriteError("PLAN_IDENTITY_INVALID")
    if not isinstance(plan.source_artifact_sha256, str) or not _SHA256.fullmatch(plan.source_artifact_sha256.lower()):
        raise CanonicalWriteError("SOURCE_HASH_INVALID")
    if plan.atomicity_unit != "REPORT_VERSION" or plan.transaction_owner != "WRITER":
        raise CanonicalWriteError("PLAN_ATOMICITY_INVALID")
    if (type(plan.duplicate_count) is not int or plan.duplicate_count < 0
            or type(plan.unchanged_existing_count) is not int or plan.unchanged_existing_count < 0):
        raise CanonicalWriteError("PLAN_COUNTS_INVALID")
    if any(not isinstance(fact, PlannedFact) for fact in plan.facts):
        raise CanonicalWriteError("FACT_TYPE_INVALID")
    for fact in plan.facts:
        if (not isinstance(fact.period_identity, tuple) or len(fact.period_identity) != 3
                or not isinstance(fact.period_identity[0], str)
                or any(not isinstance(date_parts, tuple) or len(date_parts) != 3
                       or any(type(part) is not int for part in date_parts)
                       for date_parts in fact.period_identity[1:])):
            raise CanonicalWriteError("PERIOD_IDENTITY_INVALID")
        if (not isinstance(fact.approval_references, tuple)
                or any(not isinstance(item, tuple) or len(item) != 3
                       or not all(isinstance(part, str) and part.strip() for part in item)
                       for item in fact.approval_references)):
            raise CanonicalWriteError("APPROVAL_REFERENCES_INVALID")
        if any(not isinstance(value, str) or not value.strip() for value in (
            fact.company_id, fact.report_type_id, fact.report_id, fact.report_version_id,
            fact.metric_id, fact.extraction_standard_id, fact.extraction_standard_approval_ref,
            fact.source_identity, fact.revision_identity, fact.source_artifact_sha256,
        )):
            raise CanonicalWriteError("FACT_IDENTITY_INVALID")
        if (not isinstance(fact.dimensions, tuple)
                or any(not isinstance(pair, tuple) or len(pair) != 2
                       or not all(isinstance(part, str) and part.strip() for part in pair)
                       for pair in fact.dimensions)):
            raise CanonicalWriteError("DIMENSIONS_INVALID")
        if (fact.dimensions != tuple(sorted(fact.dimensions))
                or len({pair[0] for pair in fact.dimensions}) != len(fact.dimensions)):
            raise CanonicalWriteError("DIMENSIONS_NOT_CANONICAL")
    identities = [fact.identity for fact in plan.facts]
    if len(identities) != len(set(identities)):
        raise CanonicalWriteError("PLAN_DUPLICATE_FACT")
    _normalize_datetime(metadata.publication_datetime)


def _validate_fact(session: Session, fact: PlannedFact, company_id: int, plan: CanonicalPersistencePlan,
                   industry_code: str) -> str:
    if not isinstance(fact.value_origin, ValueOrigin):
        raise CanonicalWriteError("VALUE_ORIGIN_INVALID")
    kind, start, end = fact.period_identity
    if kind not in {"INSTANT", "DURATION"}:
        raise CanonicalWriteError("TEMPORAL_TYPE_INVALID")
    try:
        start = validate_jalali_date(start, label="period start")
        end = validate_jalali_date(end, label="period end")
    except ValueError as exc:
        raise CanonicalWriteError("JALALI_DATE_INVALID") from exc
    if start > end or (kind == "INSTANT" and (start != end or fact.duration_basis is not None)):
        raise CanonicalWriteError("PERIOD_INVALID")
    if kind == "DURATION" and fact.duration_basis not in {"YTD", "STANDALONE"}:
        raise CanonicalWriteError("DURATION_BASIS_INVALID")
    metric_scope = {"industry_code": industry_code}
    metric_id = _resolve_binding(session, "metric", fact.metric_id, _approval_ref(fact, "metric"), metric_scope)
    metric = session.get(FinancialMetric, metric_id)
    if metric is None:
        raise CanonicalWriteError("METRIC_NOT_FOUND")
    if metric.is_derived:
        raise CanonicalWriteError("DERIVED_METRIC_PROHIBITED")
    if (metric.flow_or_stock == "STOCK") != (kind == "INSTANT"):
        raise CanonicalWriteError("METRIC_TEMPORAL_MISMATCH")
    if type(fact.value_integer) is not int or not -(2**63) <= fact.value_integer < 2**63:
        raise CanonicalWriteError("INTEGER_VALUE_INVALID")
    if not isinstance(fact.source_value_decimal, Decimal) or not fact.source_value_decimal.is_finite():
        raise CanonicalWriteError("DECIMAL_VALUE_INVALID")
    try:
        rounded = int(fact.source_value_decimal.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError, OverflowError) as exc:
        raise CanonicalWriteError("DECIMAL_VALUE_INVALID") from exc
    if rounded != fact.value_integer:
        raise CanonicalWriteError("ROUNDED_VALUE_MISMATCH")
    if not all(isinstance(value, str) and value.strip() for value in (
        fact.source_unit, fact.source_currency, fact.source_scale,
        fact.template_id, fact.template_version, fact.extraction_owner,
        fact.worksheet_name, fact.source_coordinate,
    )) or type(fact.worksheet_ordinal) is not int or fact.worksheet_ordinal < 1:
        raise CanonicalWriteError("FACT_PROVENANCE_INVALID")
    try:
        row, column = coordinate_to_tuple(fact.source_coordinate)
    except (TypeError, ValueError) as exc:
        raise CanonicalWriteError("SOURCE_COORDINATE_INVALID") from exc
    if fact.source_coordinate != f"{get_column_letter(column)}{row}":
        raise CanonicalWriteError("SOURCE_COORDINATE_INVALID")
    if not _SHA256.fullmatch(fact.template_sha256.lower()):
        raise CanonicalWriteError("TEMPLATE_HASH_INVALID")
    if fact.value_origin is ValueOrigin.ZERO_FALLBACK:
        if fact.value_integer != 0:
            raise CanonicalWriteError("ZERO_FALLBACK_INVALID")
        if fact.source_value_kind != "BLANK":
            raise CanonicalWriteError("ZERO_FALLBACK_SOURCE_INVALID")
        if not any(kind == "zero_fallback_rule" for kind, _, _ in fact.approval_references):
            raise CanonicalWriteError("ZERO_FALLBACK_APPROVAL_MISSING")
    elif fact.source_value_kind not in {"PRESENT_TEXT", "PRESENT_NUMBER"}:
        raise CanonicalWriteError("SOURCE_VALUE_KIND_INVALID")
    for approval_kind, identity, ref in fact.approval_references:
        resolved_kind = _APPROVAL_KIND_ALIASES.get(approval_kind, approval_kind)
        _check_approval(session, resolved_kind, identity, ref,
                        scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
    template_approval_ref = _template_approval_ref(session, fact)
    if fact.extraction_standard_id != plan.extraction_standard_id:
        raise CanonicalWriteError("EXTRACTION_STANDARD_MISMATCH")
    return template_approval_ref


def _approval_ref(fact: PlannedFact, kind: str) -> str:
    for approval_kind, identity, reference in fact.approval_references:
        if approval_kind == kind:
            return reference
    raise CanonicalWriteError("APPROVAL_REFERENCE_MISSING")


def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                    *, identity: str | None = None) -> dict[str, str]:
    scopes: dict[str, dict[str, str]] = {
        "company": {"industry_code": industry_code},
        "report_type": {"company_id": fact.company_id},
        "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                          "report_version_id": fact.report_version_id},
        "industry": {},
        "metric": {"industry_code": industry_code},
        "source_unit": {"metric_id": fact.metric_id},
        "source_currency": {"metric_id": fact.metric_id},
        "source_scale": {"metric_id": fact.metric_id},
        "period_mapping": {"report_type_id": fact.report_type_id,
                           "temporal_type": fact.period_identity[0],
                           "duration_basis": fact.duration_basis or "INSTANT"},
        "source_label": {"report_type_id": fact.report_type_id,
                         "template_id": fact.template_id, "template_version": fact.template_version,
                         "template_sha256": fact.template_sha256.lower()},
        "source_header": {"report_type_id": fact.report_type_id,
                          "template_id": fact.template_id, "template_version": fact.template_version,
                          "template_sha256": fact.template_sha256.lower()},
        "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
        "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
    }
    if kind == "dimension_value":
        dimensions = [dimension for dimension, value in fact.dimensions
                      if value == identity]
        if len(dimensions) != 1:
            raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
        scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                        "dimension_id": dimensions[0]}
    if kind not in scopes:
        raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
    return scopes[kind]


def _check_approval(session: Session, kind: str, identity: str, ref: str | None,
                    *, scope: Mapping[str, str] | None = None) -> CanonicalApproval:
    try:
        return resolve_approval(session, approval_kind=kind, external_identity=identity,
                                approval_ref=ref, expected_scope=scope)
    except ApprovalResolutionError as exc:
        raise CanonicalWriteError(exc.code) from exc


def _template_approval_ref(session: Session, fact: PlannedFact) -> str:
    row = _check_approval(
        session, "template", f"{fact.template_id}:{fact.template_version}:{fact.template_sha256}", None,
        scope={"company_id": fact.company_id, "report_type_id": fact.report_type_id,
               "template_id": fact.template_id, "template_version": fact.template_version,
               "template_sha256": fact.template_sha256.lower()},
    )
    return row.approval_ref


def _active_binding(session: Session, kind: str, external_identity: str) -> CanonicalIdentityBinding | None:
    return session.scalar(select(CanonicalIdentityBinding).where(
        CanonicalIdentityBinding.identity_kind == kind,
        CanonicalIdentityBinding.external_identity == external_identity,
        CanonicalIdentityBinding.is_active.is_(True),
    ))


def _resolve_binding(session: Session, kind: str, external_identity: str, approval_ref: str,
                     scope: Mapping[str, str]) -> int:
    binding = _active_binding(session, kind, external_identity)
    if binding is not None and binding.approval_ref == approval_ref:
        _check_approval(session, kind, external_identity, approval_ref, scope=scope)
    if binding is None:
        raise CanonicalWriteError("IDENTITY_BINDING_NOT_RESOLVED")
    if binding.approval_ref != approval_ref:
        raise CanonicalWriteError("IDENTITY_BINDING_NOT_RESOLVED")
    return binding.internal_id


def _validate_report_calendar(
    session: Session,
    facts: tuple[PlannedFact, ...],
    company_id: int,
    report_type_id: str,
    industry_code: str,
) -> None:
    # The 3/6/9/12-month cumulative rule is specific to the reviewed BANK
    # PERIODIC_FINANCIAL standard. MONTHLY_ACTIVITY has a separate standard;
    # never apply periodic-report assumptions to it.
    if report_type_id != "PERIODIC_FINANCIAL":
        return
    calendar = session.get(CanonicalCompanyFiscalCalendar, company_id)
    for fact in facts:
        if fact.period_identity[0] != "DURATION" or fact.duration_basis != "YTD":
            continue
        start = fact.period_identity[1]
        if calendar is None:
            raise CanonicalWriteError("FISCAL_YEAR_START_UNKNOWN")
        if not calendar.source_identity.strip():
            raise CanonicalWriteError("FISCAL_YEAR_SOURCE_MISSING")
        company_external_id = fact.company_id
        _check_approval(
            session, "fiscal_year_start_month",
            f"{company_external_id}:{calendar.fiscal_year_start_month}",
            calendar.approval_ref, scope={"company_id": company_external_id, "industry_code": industry_code},
        )
        # Owner-approved company calendar contract: month is explicit and
        # fiscal year starts on day 1 of that Jalali month.
        if start[1] != calendar.fiscal_year_start_month or start[2] != 1:
            raise CanonicalWriteError("YTD_START_MISMATCH")
        _kind, _start, end = fact.period_identity
        months = (end[0] - start[0]) * 12 + end[1] - start[1] + 1
        if months not in {3, 6, 9, 12} or not _is_month_end(end):
            raise CanonicalWriteError("BANK_YTD_PERIOD_ALIGNMENT_INVALID")


def _get_or_create_period(session: Session, fact: PlannedFact, company_id: int) -> CanonicalFinancialPeriod:
    kind, start, end = fact.period_identity
    months_length = None
    if kind == "INSTANT":
        months_length = 0
    elif start[2] == 1 and _is_month_end(end):
        months = (end[0] - start[0]) * 12 + end[1] - start[1] + 1
        if months > 0:
            months_length = months
    query = select(CanonicalFinancialPeriod).where(
        CanonicalFinancialPeriod.company_id == company_id,
        CanonicalFinancialPeriod.temporal_type == kind,
        CanonicalFinancialPeriod.start_year == start[0], CanonicalFinancialPeriod.start_month == start[1], CanonicalFinancialPeriod.start_day == start[2],
        CanonicalFinancialPeriod.end_year == end[0], CanonicalFinancialPeriod.end_month == end[1], CanonicalFinancialPeriod.end_day == end[2],
    )
    period = session.scalar(query)
    if period is not None:
        return period
    period = CanonicalFinancialPeriod(
        company_id=company_id, temporal_type=kind,
        start_year=start[0], start_month=start[1], start_day=start[2],
        end_year=end[0], end_month=end[1], end_day=end[2],
        months_length=months_length,
    )
    session.add(period)
    session.flush()
    return period


def _get_or_create_dimensions(session: Session, fact: PlannedFact) -> CanonicalDimensionSet:
    key_text = json.dumps(fact.dimensions, ensure_ascii=False, separators=(",", ":"))
    key = hashlib.sha256(key_text.encode("utf-8")).hexdigest()
    dimension_set = session.scalar(select(CanonicalDimensionSet).where(CanonicalDimensionSet.canonical_key == key))
    if dimension_set is None:
        dimension_set = CanonicalDimensionSet(canonical_key=key)
        session.add(dimension_set)
        session.flush()
    else:
        existing_members = tuple(sorted(session.execute(
            select(CanonicalDimensionMember.dimension_id,
                   CanonicalDimensionMember.dimension_value_id)
            .where(CanonicalDimensionMember.dimension_set_id == dimension_set.dimension_set_id)
        ).all()))
        if existing_members != fact.dimensions:
            raise CanonicalWriteError("DIMENSION_KEY_CONFLICT")
        return dimension_set
    refs = {(kind, identity): ref for kind, identity, ref in fact.approval_references}
    for dimension, value in fact.dimensions:
        session.add(CanonicalDimensionMember(
            dimension_set_id=dimension_set.dimension_set_id,
            dimension_id=dimension, dimension_value_id=value,
            dimension_approval_ref=refs[("dimension", dimension)],
            value_approval_ref=refs[("dimension_value", value)],
        ))
    session.flush()
    return dimension_set


def _same_version(session: Session, version: CanonicalReportVersion, report: CanonicalReport,
                  plan: CanonicalPersistencePlan, metadata: ReportWriteMetadata, company_id: int) -> bool:
    first = plan.facts[0]
    supersedes_id = None
    if plan.supersedes_version_id is not None:
        supersedes_id = session.scalar(select(CanonicalReportVersion.canonical_report_version_id).where(
            CanonicalReportVersion.external_version_id == plan.supersedes_version_id,
            CanonicalReportVersion.canonical_report_id == report.canonical_report_id,
        ))
    return all((
        report.company_id == company_id,
        report.report_type_id == first.report_type_id,
        report.title == metadata.title,
        version.version_number == metadata.version_number,
        version.publication_datetime == _normalize_datetime(metadata.publication_datetime),
        version.is_audited == metadata.is_audited,
        version.is_restated == metadata.is_restated,
        version.scenario_approval_ref == metadata.scenario_approval_ref,
        version.source_identity == plan.source_identity,
        version.revision_identity == plan.revision_identity,
        version.source_artifact_sha256 == plan.source_artifact_sha256.lower(),
        version.extraction_standard_id == plan.extraction_standard_id,
        version.extraction_standard_approval_ref == plan.extraction_standard_approval_ref,
        version.template_id == first.template_id,
        version.template_version == first.template_version,
        version.template_sha256 == first.template_sha256.lower(),
        version.template_approval_ref == _template_approval_ref(session, first),
        version.supersedes_version_id == supersedes_id,
    ))


def _matches_existing_facts(session: Session, rows: list[CanonicalFinancialFact], facts: tuple[PlannedFact, ...],
                            company_id: int, metadata: ReportWriteMetadata) -> bool:
    if len(rows) != len(facts):
        return False
    for fact in facts:
        kind, start, end = fact.period_identity
        period = session.scalar(select(CanonicalFinancialPeriod).where(
            CanonicalFinancialPeriod.company_id == company_id,
            CanonicalFinancialPeriod.temporal_type == kind,
            CanonicalFinancialPeriod.start_year == start[0], CanonicalFinancialPeriod.start_month == start[1], CanonicalFinancialPeriod.start_day == start[2],
            CanonicalFinancialPeriod.end_year == end[0], CanonicalFinancialPeriod.end_month == end[1], CanonicalFinancialPeriod.end_day == end[2],
        ))
        metric_binding = session.scalar(select(CanonicalIdentityBinding).where(
            CanonicalIdentityBinding.identity_kind == "metric", CanonicalIdentityBinding.external_identity == fact.metric_id,
        ))
        key_text = json.dumps(fact.dimensions, ensure_ascii=False, separators=(",", ":"))
        dkey = hashlib.sha256(key_text.encode("utf-8")).hexdigest()
        dims = session.scalar(select(CanonicalDimensionSet).where(CanonicalDimensionSet.canonical_key == dkey))
        row = next((item for item in rows if period and metric_binding and dims
                    and item.period_id == period.period_id and item.metric_id == metric_binding.internal_id
                    and item.dimension_set_id == dims.dimension_set_id), None)
        if row is None or row.value_integer != fact.value_integer or row.value_origin != fact.value_origin.value or row.duration_basis != fact.duration_basis or row.temporal_type != kind or row.source_unit != fact.source_unit or row.source_currency != fact.source_currency or row.source_scale != fact.source_scale or row.scenario != metadata.scenario:
            return False
        provenance = session.scalar(select(CanonicalFactProvenance).where(CanonicalFactProvenance.fact_id == row.fact_id))
        refs_json = json.dumps(fact.approval_references, ensure_ascii=False, separators=(",", ":"))
        if provenance is None or provenance.source_identity != fact.source_identity or provenance.revision_identity != fact.revision_identity or provenance.source_artifact_sha256 != fact.source_artifact_sha256.lower() or provenance.worksheet_ordinal != fact.worksheet_ordinal or provenance.worksheet_name != fact.worksheet_name or provenance.source_coordinate != fact.source_coordinate or provenance.source_value_kind != fact.source_value_kind or provenance.source_decimal_text != format(fact.source_value_decimal, "f") or provenance.source_token != fact.source_token or provenance.approval_references_json != refs_json:
            return False
    return True


def _start_run(session_factory: sessionmaker[Session], records_found: int) -> int:
    with session_factory() as session:
        with session.begin():
            run = IngestionRun(source="EXCEL", status="STARTED", records_found=records_found,
                               records_inserted=0, records_updated=0, records_failed=0)
            session.add(run)
            session.flush()
            return run.ingestion_id


def _plan_record_count(plan: object) -> int:
    if not isinstance(plan, CanonicalPersistencePlan) or not isinstance(plan.facts, tuple):
        return 1
    duplicate_count = plan.duplicate_count if type(plan.duplicate_count) is int and plan.duplicate_count > 0 else 0
    return max(len(plan.facts) + duplicate_count, 1)


def _complete_run(session: Session, ingestion_id: int | None, inserted: int, duplicates: int) -> None:
    if ingestion_id is None:
        raise CanonicalWriteError("INGESTION_AUDIT_REQUIRED")
    run = session.get(IngestionRun, ingestion_id)
    if run is None or run.status != "STARTED":
        raise CanonicalWriteError("INGESTION_AUDIT_INVALID")
    run.status = "COMPLETED"
    run.finished_at = _utc_now_naive()
    run.records_inserted = inserted
    run.records_updated = 0
    run.records_failed = 0
    run.records_found = max(run.records_found or 0, inserted + duplicates)
    detail = session.get(CanonicalIngestionAudit, ingestion_id)
    if detail is None:
        detail = CanonicalIngestionAudit(ingestion_id=ingestion_id)
        session.add(detail)
    detail.records_accepted = inserted
    detail.records_duplicate = duplicates
    detail.records_rejected = 0
    detail.error_code = None


def _mark_failed(session_factory: sessionmaker[Session], ingestion_id: int, code: str,
                 rejected_count: int) -> None:
    try:
        with session_factory() as session:
            with session.begin():
                run = session.get(IngestionRun, ingestion_id)
                if run is not None and run.status == "STARTED":
                    run.status = "FAILED"
                    run.finished_at = _utc_now_naive()
                    run.records_failed = max(run.records_failed or 0, 1)
                    run.error_log = code
                detail = session.get(CanonicalIngestionAudit, ingestion_id)
                if detail is None:
                    detail = CanonicalIngestionAudit(ingestion_id=ingestion_id)
                    session.add(detail)
                detail.records_rejected = max(detail.records_rejected or 0, rejected_count, 1)
                detail.error_code = code
    except Exception:
        # The caller still receives the stable write error; audit storage failure
        # is never allowed to expose source values or raw exception text.
        return


def _normalize_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise CanonicalWriteError("PUBLICATION_TIME_INVALID")
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _is_month_end(value: tuple[int, int, int]) -> bool:
    for day in range(31, 27, -1):
        try:
            validate_jalali_date((value[0], value[1], day), label="month end")
            return value[2] == day
        except ValueError:
            continue
    return False


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

