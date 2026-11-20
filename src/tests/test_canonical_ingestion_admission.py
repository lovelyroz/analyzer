"""Synthetic unit coverage for the pure canonical batch admission boundary.

Owner execution only; this suite is intentionally not run by the implementer.
"""
from dataclasses import replace
from decimal import Decimal
from io import BytesIO

import pytest
from openpyxl import Workbook
from openpyxl.styles import PatternFill

from src.ingestion.canonical_admission import (
    AdmissionCode,
    AdmissionRejected,
    CandidateSubmission,
    ExistingReportVersion,
    RevisionContext,
    SubmittedRecordKind,
    ValueOrigin,
    build_candidate_submission,
    prepare_canonical_batch,
)
from src.ingestion.excel.canonical_input import (
    ApprovedSelection,
    CanonicalInputSpec,
    CanonicalInputCandidate,
    CandidateValidationError,
    DurationBasis,
    JalaliPeriod,
    TemporalType,
)
from src.ingestion.excel.deterministic_matcher import TableRule, TemplateVersion, match_template
from src.ingestion.excel.dto import CellValueKind
from src.ingestion.excel.reader import read_excel_source


def _candidate(
    *, value=Decimal("12.5"), version="version-1", source_sha="a" * 64,
    metric="metric-sales", value_kind=CellValueKind.PRESENT_TEXT,
    source_text=None, native_integer=None, dimensions=(), dimension_refs=(),
):
    if source_text is None and value_kind is CellValueKind.PRESENT_TEXT:
        source_text = str(value)
    return CanonicalInputCandidate(
        company_id="company-1",
        report_type_id="report-periodic",
        report_version_id=version,
        template_id="template-fixture",
        template_version="1",
        template_sha256="b" * 64,
        source_workbook_sha256=source_sha,
        worksheet_ordinal=1,
        worksheet_name="Annual",
        source_coordinate="B2",
        extraction_owner="table-body",
        source_value_kind=value_kind,
        source_text=source_text,
        source_native_integer=native_integer,
        metric_id=metric,
        source_label_id="label-sales",
        source_header_id="header-current",
        value=value,
        source_unit="unit-rial",
        source_currency="currency-irr",
        source_scale="scale-unit",
        temporal_type=TemporalType.DURATION,
        period_start_jalali=(1404, 1, 1),
        period_end_jalali=(1404, 12, 29),
        duration_basis=DurationBasis.YTD,
        dimensions=dimensions,
        company_approval_ref="approval-company",
        report_type_approval_ref="approval-report-type",
        report_version_approval_ref="approval-report-version",
        metric_approval_ref="approval-metric",
        source_unit_approval_ref="approval-unit",
        source_currency_approval_ref="approval-currency",
        source_scale_approval_ref="approval-scale",
        period_mapping_id="period-map-1404-ytd",
        period_mapping_approval_ref="approval-period",
        source_label_approval_ref="approval-label",
        source_header_approval_ref="approval-header",
        dimension_approval_refs=dimension_refs,
    )


def _revision(*, version="version-1", revision="revision-1", source_sha="a" * 64, supersedes=None):
    return RevisionContext(
        report_id="report-1",
        report_version_id=version,
        company_id="company-1",
        source_identity="codal-report-9001",
        revision_identity=revision,
        source_artifact_sha256=source_sha,
        extraction_standard_id="standard-v1",
        extraction_standard_approval_ref="approval-standard-v1",
        supersedes_version_id=supersedes,
    )


def _codes(exc):
    return {item.code for item in exc.value.diagnostics}


def _approved(identity, approval_ref="fixture-approval"):
    return ApprovedSelection(identity, True, 1, approval_ref)


def _blank_observation_and_match(source_value=""):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Annual"
    sheet["A1"] = "Revenue"
    sheet["B1"] = "Amount"
    if source_value == "":
        sheet["B2"].fill = PatternFill(fill_type="solid", fgColor="FFFFFF")
    else:
        sheet["B2"] = source_value
    stream = BytesIO()
    workbook.save(stream)
    observation = read_excel_source(stream.getvalue(), file_name="blank-fixture.xlsx")
    template = TemplateVersion(
        template_id="template-fixture", version="1", approved=True,
        source_workbook_sha256=observation.source.sha256,
        worksheet_name="Annual", worksheet_ordinal=1,
        tables=(TableRule(
            code="revenue", title_cell="A1", title_text="Revenue",
            bounds="A1:B2", header_cells=(("B1", "Amount"),),
            owned_ranges=("B2:B2",),
        ),),
    )
    match = match_template(template, observation)
    spec = CanonicalInputSpec(
        company=_approved("company-1"), report_type=_approved("report-periodic"),
        report_version=_approved("version-1"), metric=_approved("metric-sales"),
        source_unit=_approved("unit-rial"), source_currency=_approved("currency-irr"),
        source_scale=_approved("scale-unit"),
        period=JalaliPeriod(TemporalType.DURATION, (1404, 1, 1), (1404, 12, 29), DurationBasis.YTD),
        period_mapping=_approved("period-map"), source_label=_approved("label-sales"),
        source_header=_approved("header-current"),
    )
    return observation, match, spec


def test_valid_batch_returns_immutable_caller_owned_non_executable_plan():
    candidate = _candidate()
    plan = prepare_canonical_batch((candidate,), revision=_revision())

    assert len(plan.facts) == 1
    assert plan.facts[0].source_value_decimal == Decimal("12.5")
    assert plan.facts[0].value_integer == 13
    assert plan.transaction_owner == "CALLER"
    assert plan.atomicity_unit == "REPORT_VERSION"
    assert plan.execution_allowed is False
    assert not hasattr(plan.facts[0], "source_text")
    with pytest.raises((AttributeError, TypeError)):
        plan.facts = ()


def test_one_invalid_candidate_rejects_the_entire_batch():
    valid = _candidate()
    invalid = replace(valid, metric_id="", metric_approval_ref="")
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((valid, invalid), revision=_revision())
    assert AdmissionCode.IDENTITY_MISSING in _codes(exc)
    assert AdmissionCode.APPROVAL_REFERENCE_MISSING in _codes(exc)


def test_identical_in_batch_duplicate_collapses_and_payload_conflict_rejects_all():
    candidate = _candidate()
    plan = prepare_canonical_batch((candidate, candidate), revision=_revision())
    assert len(plan.facts) == 1
    assert plan.duplicate_count == 1

    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((candidate, replace(candidate, value=Decimal("13"), source_text="13")), revision=_revision())
    assert AdmissionCode.INTRA_BATCH_CONFLICT in _codes(exc)


@pytest.mark.parametrize("provenance_change", [
    lambda candidate: replace(candidate, template_sha256="c" * 64),
    lambda candidate: replace(
        candidate, source_header_id="header-prior", source_header_approval_ref="approval-header-prior",
    ),
    lambda candidate: replace(
        candidate, source_label_id="label-prior", source_label_approval_ref="approval-label-prior",
    ),
    lambda candidate: replace(candidate, extraction_owner="table-body-alternate"),
])
def test_economically_identical_duplicates_with_different_provenance_reject_order_independently(provenance_change):
    candidate = _candidate()
    alternate = provenance_change(candidate)
    diagnostics = []
    for batch in ((candidate, alternate), (alternate, candidate)):
        with pytest.raises(AdmissionRejected) as exc:
            prepare_canonical_batch(batch, revision=_revision())
        diagnostics.append(exc.value.diagnostics)
    assert diagnostics[0] == diagnostics[1]
    assert diagnostics[0][0].code is AdmissionCode.DUPLICATE_PROVENANCE_CONFLICT


def test_source_zero_and_approved_zero_fallback_have_distinct_states():
    reported_zero = _candidate(value=Decimal(0), source_text="0")
    reported_plan = prepare_canonical_batch((reported_zero,), revision=_revision())
    assert reported_plan.facts[0].value_integer == 0
    assert reported_plan.facts[0].value_origin is ValueOrigin.SOURCE_REPORTED

    missing_cell = _candidate(
        value=Decimal(0), value_kind=CellValueKind.BLANK, source_text=None,
    )
    fallback = CandidateSubmission(
        candidate=missing_cell,
        value_origin=ValueOrigin.ZERO_FALLBACK,
        zero_fallback_rule=ApprovedSelection("metric-sales", True, 1, "approved-zero-fallback-rule"),
    )
    fallback_plan = prepare_canonical_batch((fallback,), revision=_revision())
    assert fallback_plan.facts[0].value_integer == 0
    assert fallback_plan.facts[0].value_origin is ValueOrigin.ZERO_FALLBACK
    assert fallback_plan.facts[0].value_origin is not reported_plan.facts[0].value_origin


def test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path():
    observation, match, spec = _blank_observation_and_match()
    with pytest.raises(CandidateValidationError) as exc:
        build_candidate_submission(observation, match, coordinate="B2", spec=spec)
    assert exc.value.code == "SOURCE_VALUE_MISSING"
    with pytest.raises(CandidateValidationError) as exc:
        build_candidate_submission(
            observation, match, coordinate="B2", spec=spec,
            zero_fallback_rule=ApprovedSelection("different-metric", True, 1, "wrong-rule"),
        )
    assert exc.value.code == "ZERO_FALLBACK_APPROVAL_INVALID"

    rule = ApprovedSelection("metric-sales", True, 1, "approved-zero-fallback-rule")
    submission = build_candidate_submission(
        observation, match, coordinate="B2", spec=spec, zero_fallback_rule=rule,
    )
    assert submission.candidate.source_value_kind is CellValueKind.BLANK
    assert submission.candidate.source_text is None
    assert submission.candidate.source_native_integer is None
    assert submission.candidate.value == Decimal(0)
    assert submission.value_origin is ValueOrigin.ZERO_FALLBACK
    assert next(cell for cell in observation.cells if cell.cell_ref.coordinate == "B2").value_kind is CellValueKind.BLANK
    plan = prepare_canonical_batch(
        (submission,), revision=_revision(source_sha=observation.source.sha256),
    )
    assert plan.facts[0].value_origin is ValueOrigin.ZERO_FALLBACK

    zero_observation, zero_match, zero_spec = _blank_observation_and_match("0")
    reported_zero = build_candidate_submission(
        zero_observation, zero_match, coordinate="B2", spec=zero_spec,
    )
    assert reported_zero.candidate.source_value_kind is CellValueKind.PRESENT_TEXT
    assert reported_zero.candidate.source_text == "0"
    assert reported_zero.candidate.value == Decimal(0)
    zero_plan = prepare_canonical_batch(
        (reported_zero,), revision=_revision(source_sha=zero_observation.source.sha256),
    )
    assert zero_plan.facts[0].value_origin is ValueOrigin.SOURCE_REPORTED


def test_unapproved_or_inconsistent_zero_fallback_is_rejected():
    blank_candidate = _candidate(value=Decimal(0), value_kind=CellValueKind.BLANK, source_text=None)
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((CandidateSubmission(blank_candidate, value_origin=ValueOrigin.ZERO_FALLBACK),), revision=_revision())
    assert AdmissionCode.ZERO_FALLBACK_APPROVAL_MISSING in _codes(exc)

    nonzero = _candidate(value=Decimal(2), source_text="2")
    approved = ApprovedSelection("metric-sales", True, 1, "approved-rule")
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((CandidateSubmission(nonzero, value_origin=ValueOrigin.ZERO_FALLBACK, zero_fallback_rule=approved),), revision=_revision())
    assert AdmissionCode.ZERO_FALLBACK_SOURCE_UNSUPPORTED in _codes(exc)


def test_existing_identical_fact_is_unchanged_and_conflict_is_rejected():
    candidate = _candidate()
    initial = prepare_canonical_batch((candidate,), revision=_revision())
    known_version = ExistingReportVersion(
        report_id="report-1", report_version_id="version-1",
        source_identity="codal-report-9001", revision_identity="revision-1",
        source_artifact_sha256="a" * 64, extraction_standard_id="standard-v1",
    )
    replay = prepare_canonical_batch(
        (candidate,), revision=_revision(), existing_versions=(known_version,),
        existing_facts=initial.facts,
    )
    assert replay.facts == ()
    assert replay.unchanged_existing_count == 1

    conflicting = replace(candidate, value=Decimal("14"), source_text="14")
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch(
            (conflicting,), revision=_revision(), existing_versions=(known_version,),
            existing_facts=initial.facts,
        )
    assert AdmissionCode.EXISTING_FACT_CONFLICT in _codes(exc)


def test_correction_uses_new_version_and_preserves_the_prior_version():
    original_candidate = _candidate()
    original = prepare_canonical_batch((original_candidate,), revision=_revision())
    known = ExistingReportVersion(
        report_id="report-1", report_version_id="version-1",
        source_identity="codal-report-9001", revision_identity="revision-1",
        source_artifact_sha256="a" * 64, extraction_standard_id="standard-v1",
    )
    corrected_candidate = _candidate(version="version-2", source_sha="c" * 64, value=Decimal("15"), source_text="15")
    corrected = prepare_canonical_batch(
        (corrected_candidate,),
        revision=_revision(version="version-2", revision="revision-2", source_sha="c" * 64, supersedes="version-1"),
        existing_versions=(known,), existing_facts=original.facts,
    )
    assert corrected.report_version_id == "version-2"
    assert corrected.supersedes_version_id == "version-1"
    assert {fact.report_version_id for fact in corrected.facts} == {"version-2"}
    assert corrected.preserved_report_version_ids == ("version-1",)


def test_missing_and_ambiguous_identities_reject_the_batch():
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((replace(_candidate(), source_currency=""),), revision=_revision())
    assert AdmissionCode.IDENTITY_MISSING in _codes(exc)

    ambiguous_dims = _candidate(
        dimensions=(("dimension-region", "north"), ("dimension-region", "south")),
        dimension_refs=(("dimension-region", "approval-region", "north", "approval-north"),
                        ("dimension-region", "approval-region", "south", "approval-south")),
    )
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((ambiguous_dims,), revision=_revision())
    assert AdmissionCode.MAPPING_AMBIGUOUS in _codes(exc)


def test_other_metric_requires_its_exact_approved_identity():
    candidate = _candidate(metric="OTHER_MISC_APPROVED")
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((candidate,), revision=_revision())
    assert AdmissionCode.OTHER_APPROVAL_MISSING in _codes(exc)

    approved = CandidateSubmission(
        candidate=candidate,
        other_metric_approval=ApprovedSelection("OTHER_MISC_APPROVED", True, 1, "approved-other-rule"),
    )
    plan = prepare_canonical_batch((approved,), revision=_revision())
    assert ("other_metric_rule", "OTHER_MISC_APPROVED", "approved-other-rule") in plan.facts[0].approval_references


@pytest.mark.parametrize(
    "record_kind,expected",
    [(SubmittedRecordKind.RAW_ROW, AdmissionCode.RAW_ROW_PROHIBITED),
     (SubmittedRecordKind.CALCULATED, AdmissionCode.CALCULATED_FACT_PROHIBITED)],
)
def test_raw_rows_and_calculated_facts_are_prohibited(record_kind, expected):
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((CandidateSubmission(_candidate(), record_kind=record_kind),), revision=_revision())
    assert expected in _codes(exc)


def test_unwrapped_raw_observation_is_rejected_and_no_transaction_side_effects_exist():
    class SessionSpy:
        calls = 0

        def begin(self):
            self.calls += 1

        def commit(self):
            self.calls += 1

    session = SessionSpy()
    with pytest.raises(AdmissionRejected) as exc:
        prepare_canonical_batch((object(),), revision=_revision())
    assert AdmissionCode.CANDIDATE_TYPE_INVALID in _codes(exc)
    plan = prepare_canonical_batch((_candidate(),), revision=_revision())
    assert session.calls == 0
    assert plan.transaction_owner == "CALLER"
    assert plan.execution_allowed is False


def test_plan_and_diagnostics_are_deterministic_independent_of_input_order():
    first = _candidate(value=Decimal("3"), source_text="3")
    second = _candidate(value=Decimal("4"), source_text="4", metric="metric-cost")
    forward = prepare_canonical_batch((first, second), revision=_revision())
    reverse = prepare_canonical_batch((second, first), revision=_revision())
    assert forward == reverse

    conflict_a = replace(first, value=Decimal("5"), source_text="5")
    conflict_b = replace(first, value=Decimal("6"), source_text="6")
    with pytest.raises(AdmissionRejected) as left:
        prepare_canonical_batch((conflict_a, conflict_b), revision=_revision())
    with pytest.raises(AdmissionRejected) as right:
        prepare_canonical_batch((conflict_b, conflict_a), revision=_revision())
    assert left.value.diagnostics == right.value.diagnostics
