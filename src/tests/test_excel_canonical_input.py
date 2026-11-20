"""Isolated tests for the approved Excel-to-canonical candidate boundary."""
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from io import BytesIO

import pytest
from openpyxl import Workbook

from src.ingestion.excel.canonical_input import (
    ApprovedSelection, CanonicalInputSpec, CandidateValidationError,
    DimensionSelection, DurationBasis, JalaliPeriod, TemporalType,
    build_candidate,
)
from src.ingestion.excel.deterministic_matcher import TableRule, TemplateVersion, match_template
from src.ingestion.excel.reader import read_excel_source


def _approved(identity):
    return ApprovedSelection(identity, True, 1, "fixture-approval")


def _spec(*, temporal=TemporalType.INSTANT, start=(1405, 8, 20), end=(1405, 8, 20), basis=None):
    return CanonicalInputSpec(
        company=_approved("fixture-company"), report_type=_approved("fixture-report-type"),
        report_version=_approved("fixture-report-version"), metric=_approved("fixture-metric"),
        source_unit=_approved("fixture-unit"), source_currency=_approved("fixture-currency"),
        source_scale=_approved("fixture-scale"), period=JalaliPeriod(temporal, start, end, basis),
        period_mapping=_approved("fixture-period-mapping"),
        source_label=_approved("fixture-label"), source_header=_approved("fixture-header"),
    )


def _inputs(value="12345678901234567890.1234567890123456789"):
    book = Workbook()
    sheet = book.active
    sheet.title = "Annual"
    sheet["A1"] = "Revenue"
    sheet["B1"] = "Amount"
    sheet["A2"] = "Operating revenue"
    sheet["B2"] = value
    stream = BytesIO()
    book.save(stream)
    observed = read_excel_source(stream.getvalue(), file_name="fixture.xlsx")
    template = TemplateVersion(
        template_id="fixture-template", version="1", approved=True,
        source_workbook_sha256="a" * 64, worksheet_name="Annual", worksheet_ordinal=1,
        tables=(TableRule(code="fixture-table", title_cell="A1", title_text="Revenue",
                          bounds="A1:B2", header_cells=(("B1", "Amount"),)),),
    )
    match = match_template(template, observed)
    assert match.status == "MATCHED"
    return observed, match


def _build(spec=None, value="12345678901234567890.1234567890123456789"):
    observation, match = _inputs(value)
    return build_candidate(observation, match, coordinate="B2", spec=spec or _spec())


def test_builds_immutable_instant_candidate_with_decimal_precision():
    candidate = _build()
    assert candidate.value == Decimal("12345678901234567890.1234567890123456789")
    assert candidate.value.as_tuple().digits == Decimal("12345678901234567890.1234567890123456789").as_tuple().digits
    assert candidate.temporal_type is TemporalType.INSTANT
    assert candidate.duration_basis is None
    assert candidate.source_coordinate == "B2"
    assert candidate.source_workbook_sha256
    with pytest.raises(FrozenInstanceError):
        candidate.metric_id = "other"


@pytest.mark.parametrize("basis", [DurationBasis.YTD, DurationBasis.STANDALONE])
def test_builds_duration_with_each_explicit_basis(basis):
    candidate = _build(_spec(temporal=TemporalType.DURATION, start=(1405, 1, 1), end=(1405, 8, 20), basis=basis))
    assert candidate.temporal_type is TemporalType.DURATION
    assert candidate.duration_basis is basis


@pytest.mark.parametrize("field,expected", [
    ("metric", "METRIC_MISSING"), ("source_unit", "SOURCE_UNIT_MISSING"),
    ("source_currency", "SOURCE_CURRENCY_MISSING"), ("source_scale", "SOURCE_SCALE_MISSING"),
])
def test_rejects_missing_semantic_identity(field, expected):
    with pytest.raises(CandidateValidationError, match=expected):
        _build(replace(_spec(), **{field: None}))


def test_rejects_ambiguous_or_unapproved_mapping():
    with pytest.raises(CandidateValidationError, match="MAPPING_AMBIGUOUS"):
        _build(replace(_spec(), metric=ApprovedSelection("fixture-metric", True, 2, "fixture-approval")))
    with pytest.raises(CandidateValidationError, match="MAPPING_NOT_APPROVED"):
        _build(replace(_spec(), metric=ApprovedSelection("fixture-metric", False, 1, None)))


def test_rejects_missing_or_invalid_period_and_jalali_range():
    with pytest.raises(CandidateValidationError, match="PERIOD_MISSING"):
        _build(replace(_spec(), period=None))
    with pytest.raises(CandidateValidationError, match="JALALI_DATE_INVALID"):
        _build(_spec(start=(1404, 12, 30), end=(1405, 1, 1)))
    with pytest.raises(CandidateValidationError, match="PERIOD_RANGE_INVALID"):
        _build(_spec(start=(1405, 8, 21), end=(1405, 8, 20)))
    with pytest.raises(CandidateValidationError, match="PERIOD_MAPPING_MISSING"):
        _build(replace(_spec(), period_mapping=None))


def test_rejects_missing_invalid_basis_and_instant_basis():
    with pytest.raises(CandidateValidationError, match="DURATION_BASIS_MISSING"):
        _build(_spec(temporal=TemporalType.DURATION, start=(1405, 1, 1), end=(1405, 8, 20)))
    with pytest.raises(CandidateValidationError, match="DURATION_BASIS_MISSING"):
        _build(_spec(temporal=TemporalType.DURATION, start=(1405, 1, 1), end=(1405, 8, 20), basis="QUARTER"))
    with pytest.raises(CandidateValidationError, match="INSTANT_BASIS_INVALID"):
        _build(_spec(basis=DurationBasis.YTD))


def test_missing_is_not_zero_and_explicit_zero_is_preserved():
    observation, match = _inputs("")
    with pytest.raises(CandidateValidationError, match="SOURCE_VALUE_MISSING"):
        build_candidate(observation, match, coordinate="B2", spec=_spec())
    assert _build(value="0").value == Decimal(0)


def test_rejects_missing_source_coordinate_and_invalid_numeric_text():
    observation, match = _inputs()
    with pytest.raises(CandidateValidationError, match="SOURCE_COORDINATE_MISSING"):
        build_candidate(observation, match, coordinate="", spec=_spec())
    with pytest.raises(CandidateValidationError, match="SOURCE_PROVENANCE_MISSING"):
        build_candidate(observation, match, coordinate="C9", spec=_spec())
    with pytest.raises(CandidateValidationError, match="SOURCE_NUMBER_INVALID"):
        _build(value="1,000")


def test_rejects_no_default_values_and_ambiguous_dimensions():
    with pytest.raises(CandidateValidationError, match="SOURCE_UNIT_MISSING"):
        _build(replace(_spec(), source_unit=None))
    duplicate_dims = (
        DimensionSelection(_approved("fixture-dimension"), _approved("fixture-value-1")),
        DimensionSelection(_approved("fixture-dimension"), _approved("fixture-value-2")),
    )
    with pytest.raises(CandidateValidationError, match="DIMENSION_AMBIGUOUS"):
        _build(replace(_spec(), dimensions=duplicate_dims))


def test_rejects_template_match_for_different_source_hash():
    observation, match = _inputs()
    with pytest.raises(CandidateValidationError, match="SOURCE_PROVENANCE_INVALID"):
        build_candidate(observation, replace(match, source_workbook_sha256="b" * 64), coordinate="B2", spec=_spec())
