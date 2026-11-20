"""Pure, fail-closed boundary from approved Excel observations to input candidates.

This module creates transient DTOs only. It does not persist facts or perform
semantic discovery: callers must provide unique, approved identities and dates.
Numeric values are parsed from the Reader's literal text using Decimal.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum
import re

from openpyxl.utils.cell import coordinate_to_tuple, range_boundaries

from src.core.jalali import validate_jalali_date
from src.ingestion.excel.deterministic_matcher import TemplateMatchResult
from src.ingestion.excel.dto import CellObservation, CellValueKind, WorkbookObservation


class CandidateValidationError(ValueError):
    """Stable-code validation failure at the canonical-input boundary."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"{code}: {message}")


class TemporalType(StrEnum):
    INSTANT = "INSTANT"
    DURATION = "DURATION"


class DurationBasis(StrEnum):
    YTD = "YTD"
    STANDALONE = "STANDALONE"


@dataclass(frozen=True, slots=True)
class ApprovedSelection:
    """A caller-supplied selection with evidence that exactly one rule matched."""
    identity: str | None
    approved: bool
    candidate_count: int = 1
    approval_ref: str | None = None


@dataclass(frozen=True, slots=True)
class JalaliPeriod:
    temporal_type: TemporalType | None
    start: tuple[int, int, int] | None
    end: tuple[int, int, int] | None
    duration_basis: DurationBasis | None = None


@dataclass(frozen=True, slots=True)
class DimensionSelection:
    dimension: ApprovedSelection
    value: ApprovedSelection


@dataclass(frozen=True, slots=True)
class CanonicalInputSpec:
    company: ApprovedSelection
    report_type: ApprovedSelection
    report_version: ApprovedSelection
    metric: ApprovedSelection
    source_unit: ApprovedSelection
    source_currency: ApprovedSelection
    source_scale: ApprovedSelection
    period: JalaliPeriod | None
    period_mapping: ApprovedSelection | None = None
    source_label: ApprovedSelection | None = None
    source_header: ApprovedSelection | None = None
    dimensions: tuple[DimensionSelection, ...] = ()


@dataclass(frozen=True, slots=True)
class CanonicalInputCandidate:
    company_id: str
    report_type_id: str
    report_version_id: str
    template_id: str
    template_version: str
    template_sha256: str
    source_workbook_sha256: str
    worksheet_ordinal: int
    worksheet_name: str
    source_coordinate: str
    source_text: str
    metric_id: str
    source_label_id: str | None
    source_header_id: str | None
    value: Decimal
    source_unit: str
    source_currency: str
    source_scale: str
    temporal_type: TemporalType
    period_start_jalali: tuple[int, int, int]
    period_end_jalali: tuple[int, int, int]
    duration_basis: DurationBasis | None
    dimensions: tuple[tuple[str, str], ...]


_DECIMAL_TEXT = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def _selection(selection: ApprovedSelection | None, label: str) -> str:
    code_label = label.upper().replace(" ", "_")
    if selection is None or not selection.identity:
        raise CandidateValidationError(f"{code_label}_MISSING", f"{label} has no explicit identity.")
    if selection.candidate_count != 1:
        raise CandidateValidationError("MAPPING_AMBIGUOUS", f"{label} did not resolve to exactly one candidate.")
    if not selection.approved or not selection.approval_ref:
        raise CandidateValidationError("MAPPING_NOT_APPROVED", f"{label} lacks explicit approval evidence.")
    return selection.identity


def _period(period: JalaliPeriod | None) -> tuple[TemporalType, tuple[int, int, int], tuple[int, int, int], DurationBasis | None]:
    if period is None or period.temporal_type is None or period.start is None or period.end is None:
        raise CandidateValidationError("PERIOD_MISSING", "Explicit temporal type and Jalali endpoints are required.")
    try:
        start = validate_jalali_date(period.start, label="period start")
        end = validate_jalali_date(period.end, label="period end")
    except ValueError as exc:
        raise CandidateValidationError("JALALI_DATE_INVALID", str(exc)) from exc
    if start > end:
        raise CandidateValidationError("PERIOD_RANGE_INVALID", "Period start must not be after its end.")
    if period.temporal_type is TemporalType.INSTANT:
        if start != end:
            raise CandidateValidationError("INSTANT_RANGE_INVALID", "INSTANT start and end must be the same date.")
        if period.duration_basis is not None:
            raise CandidateValidationError("INSTANT_BASIS_INVALID", "INSTANT values cannot have a duration basis.")
    elif period.temporal_type is TemporalType.DURATION:
        if start == end:
            raise CandidateValidationError("DURATION_RANGE_INVALID", "DURATION must span more than one date.")
        if not isinstance(period.duration_basis, DurationBasis):
            raise CandidateValidationError("DURATION_BASIS_MISSING", "DURATION requires explicit YTD or STANDALONE basis.")
    else:
        raise CandidateValidationError("TEMPORAL_TYPE_INVALID", "Temporal type must be INSTANT or DURATION.")
    return period.temporal_type, start, end, period.duration_basis


def build_candidate(
    observation: WorkbookObservation,
    match: TemplateMatchResult,
    *,
    coordinate: str,
    spec: CanonicalInputSpec,
) -> CanonicalInputCandidate:
    """Build one immutable candidate from one observed cell and explicit approvals."""
    if match.status != "MATCHED" or not match.template_id or not match.template_version:
        raise CandidateValidationError("STRUCTURE_NOT_APPROVED", "A successful approved-template match is required.")
    if (not _SHA256.fullmatch(match.template_sha256 or "") or
            not _SHA256.fullmatch(observation.source.sha256 or "") or
            match.source_workbook_sha256.lower() != observation.source.sha256.lower() or
            not match.worksheet_name or not match.worksheet_ordinal):
        raise CandidateValidationError("SOURCE_PROVENANCE_INVALID", "Template/source fingerprint provenance is invalid or mismatched.")
    if not isinstance(coordinate, str) or not coordinate:
        raise CandidateValidationError("SOURCE_COORDINATE_MISSING", "An exact source coordinate is required.")
    try:
        row, col = coordinate_to_tuple(coordinate)
    except (ValueError, TypeError) as exc:
        raise CandidateValidationError("SOURCE_COORDINATE_INVALID", "Source coordinate is not a valid A1 reference.") from exc
    cells = [cell for cell in observation.cells if cell.cell_ref.coordinate == coordinate
             and cell.cell_ref.worksheet_ordinal == match.worksheet_ordinal]
    if len(cells) != 1:
        if not cells and any(sheet.ordinal == match.worksheet_ordinal and sheet.literal_name == match.worksheet_name
                             for sheet in observation.worksheets):
            if any(_coordinate_in_range(coordinate, bounds) for _, bounds in match.coordinate_map):
                raise CandidateValidationError("SOURCE_VALUE_MISSING", "No literal value was observed at this in-scope coordinate.")
        raise CandidateValidationError("SOURCE_PROVENANCE_MISSING", "Coordinate must identify exactly one observed source cell.")
    cell: CellObservation = cells[0]
    sheet = next((item for item in observation.worksheets if item.ordinal == cell.cell_ref.worksheet_ordinal
                  and item.literal_name == match.worksheet_name), None)
    if sheet is None:
        raise CandidateValidationError("SOURCE_PROVENANCE_MISSING", "Observed cell has no worksheet identity.")
    if not any(_coordinate_in_range(coordinate, bounds) for _, bounds in match.coordinate_map):
        raise CandidateValidationError("STRUCTURAL_MAPPING_MISSING", "Source coordinate is outside matched template bounds.")
    if cell.value_kind is CellValueKind.BLANK:
        raise CandidateValidationError("SOURCE_VALUE_MISSING", "Blank source value cannot be replaced with zero.")
    if cell.value_kind is not CellValueKind.PRESENT_TEXT or cell.text_value is None:
        raise CandidateValidationError("SOURCE_VALUE_UNSUPPORTED", "V1 source value must be literal text.")
    literal = cell.text_value
    if not _DECIMAL_TEXT.fullmatch(literal):
        raise CandidateValidationError("SOURCE_NUMBER_INVALID", "Literal numeric text does not match the approved invariant decimal syntax.")
    try:
        amount = Decimal(literal)
    except InvalidOperation as exc:
        raise CandidateValidationError("SOURCE_NUMBER_INVALID", "Literal value cannot be represented as Decimal.") from exc
    if not amount.is_finite():
        raise CandidateValidationError("SOURCE_NUMBER_INVALID", "NaN and Infinity are not financial values.")

    company = _selection(spec.company, "company")
    report_type = _selection(spec.report_type, "report type")
    report_version = _selection(spec.report_version, "report version")
    metric = _selection(spec.metric, "metric")
    unit = _selection(spec.source_unit, "source unit")
    currency = _selection(spec.source_currency, "source currency")
    scale = _selection(spec.source_scale, "source scale")
    _selection(spec.period_mapping, "period mapping")
    label = _selection(spec.source_label, "source label") if spec.source_label is not None else None
    header = _selection(spec.source_header, "source header") if spec.source_header is not None else None
    temporal, start, end, basis = _period(spec.period)
    dimensions = tuple((_selection(item.dimension, "dimension"), _selection(item.value, "dimension value")) for item in spec.dimensions)
    if len({key for key, _ in dimensions}) != len(dimensions):
        raise CandidateValidationError("DIMENSION_AMBIGUOUS", "Dimension identities must be unique; implicit or duplicate dimensions are rejected.")

    return CanonicalInputCandidate(
        company, report_type, report_version, match.template_id, match.template_version,
        match.template_sha256.lower(), observation.source.sha256.lower(), sheet.ordinal,
        sheet.literal_name, coordinate, literal, metric, label, header, amount, unit,
        currency, scale, temporal, start, end, basis, dimensions,
    )


def _coordinate_in_range(coordinate: str, bounds: str) -> bool:
    try:
        row, col = coordinate_to_tuple(coordinate)
        left, top, right, bottom = range_boundaries(bounds)
        return left <= col <= right and top <= row <= bottom
    except (ValueError, TypeError):
        return False
