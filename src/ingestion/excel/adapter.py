"""Fail-closed adapter from an XLSX source to canonical candidate submissions.

The adapter connects the existing reader, approved-template matcher, candidate
builder, and optional admission boundary. It performs no persistence or logging.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Callable

from openpyxl.utils.cell import coordinate_to_tuple, get_column_letter, range_boundaries

from src.ingestion.canonical_admission import (
    AdmissionRejected,
    CandidateSubmission,
    CanonicalPersistencePlan,
    RevisionContext,
    build_candidate_submission,
    prepare_canonical_batch,
)
from src.ingestion.excel.canonical_input import (
    ApprovedSelection,
    CanonicalInputSpec,
    CandidateValidationError,
)
from src.ingestion.excel.deterministic_matcher import TemplateMatchResult, TemplateVersion, match_template
from src.ingestion.excel.dto import WorkbookObservation
from src.ingestion.excel.reader import (
    BytesSource,
    ExcelReaderConfig,
    ExcelSourceContractError,
    ExcelSourceReadError,
    PathSource,
    read_excel_source,
)


@dataclass(frozen=True, slots=True)
class ExcelAdapterDiagnostic:
    code: str
    coordinate: str | None = None
    worksheet_ordinal: int | None = None
    identity: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExcelAdapterResult:
    observation: WorkbookObservation | None
    match: TemplateMatchResult | None
    submissions: tuple[CandidateSubmission, ...]
    admission_plan: CanonicalPersistencePlan | None
    diagnostics: tuple[ExcelAdapterDiagnostic, ...]

    @property
    def accepted(self) -> bool:
        return not self.diagnostics


_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def adapt_excel_source(
    source: BytesSource | PathSource,
    *,
    template: TemplateVersion | None,
    selections_by_coordinate: Mapping[str, CanonicalInputSpec],
    zero_fallback_rules_by_coordinate: Mapping[str, ApprovedSelection] | None = None,
    other_metric_approvals_by_coordinate: Mapping[str, ApprovedSelection] | None = None,
    expected_source_sha256: str | None = None,
    admit: bool = False,
    revision: RevisionContext | None = None,
    reader_config: ExcelReaderConfig | None = None,
    approval_validator: Callable[[CanonicalPersistencePlan], None] | None = None,
) -> ExcelAdapterResult:
    """Read, match, and build explicitly selected submissions; optionally admit.

    ``selections_by_coordinate`` is the caller's complete semantic/temporal
    selection for the observed cells in owned extraction ranges. Admission is
    only invoked when ``admit`` is exactly ``True`` and an explicit revision is
    supplied. Diagnostics contain codes and source coordinates, never cell
    values or complete financial payloads.
    """
    diagnostics: list[ExcelAdapterDiagnostic] = []
    if not isinstance(source, (str, Path, bytes, bytearray, memoryview)):
        diagnostics.append(ExcelAdapterDiagnostic("SOURCE_INPUT_INVALID"))
        return _result(None, None, (), None, diagnostics)
    try:
        observation = read_excel_source(source, config=reader_config)
    except ExcelSourceContractError as exc:
        observation = exc.observation
        diagnostics.extend(
            ExcelAdapterDiagnostic(
                item.code,
                item.cell_ref.coordinate if item.cell_ref is not None else None,
                item.worksheet_ordinal or (item.cell_ref.worksheet_ordinal if item.cell_ref is not None else None),
            )
            for item in observation.diagnostics
        )
        return _result(observation, None, (), None, diagnostics)
    except ExcelSourceReadError as exc:
        diagnostics.append(ExcelAdapterDiagnostic(exc.code))
        return _result(None, None, (), None, diagnostics)

    if template is None:
        diagnostics.append(ExcelAdapterDiagnostic("TEMPLATE_MISSING"))
        return _result(observation, None, (), None, diagnostics)
    if not isinstance(template, TemplateVersion):
        diagnostics.append(ExcelAdapterDiagnostic("TEMPLATE_INVALID"))
        return _result(observation, None, (), None, diagnostics)
    if not isinstance(selections_by_coordinate, Mapping):
        diagnostics.append(ExcelAdapterDiagnostic("SELECTIONS_INVALID"))
        return _result(observation, None, (), None, diagnostics)
    if admit is not True and admit is not False:
        diagnostics.append(ExcelAdapterDiagnostic("ADMISSION_FLAG_INVALID"))
        return _result(observation, None, (), None, diagnostics)
    if expected_source_sha256 is not None:
        if not isinstance(expected_source_sha256, str) or not _SHA256.fullmatch(expected_source_sha256):
            diagnostics.append(ExcelAdapterDiagnostic("EXPECTED_SOURCE_HASH_INVALID"))
            return _result(observation, None, (), None, diagnostics)
        if expected_source_sha256.lower() != observation.source.sha256.lower():
            diagnostics.append(ExcelAdapterDiagnostic("SOURCE_HASH_MISMATCH"))
            return _result(observation, None, (), None, diagnostics)

    try:
        match = match_template(template, observation)
    except (AttributeError, TypeError, ValueError):
        diagnostics.append(ExcelAdapterDiagnostic("TEMPLATE_MATCH_INPUT_INVALID"))
        return _result(observation, None, (), None, diagnostics)
    if match.status != "MATCHED":
        diagnostics.extend(
            ExcelAdapterDiagnostic(item.code, item.coordinate)
            for item in match.diagnostics
        )
        return _result(observation, match, (), None, diagnostics)
    if match.source_workbook_sha256.lower() != observation.source.sha256.lower():
        diagnostics.append(ExcelAdapterDiagnostic("MATCH_SOURCE_HASH_MISMATCH"))
        return _result(observation, match, (), None, diagnostics)

    specs: dict[str, CanonicalInputSpec] = {}
    for raw_coordinate, spec in selections_by_coordinate.items():
        coordinate = _normalize_coordinate(raw_coordinate)
        if coordinate is None:
            diagnostics.append(ExcelAdapterDiagnostic("SELECTION_COORDINATE_INVALID", str(raw_coordinate)))
            continue
        if coordinate in specs:
            diagnostics.append(ExcelAdapterDiagnostic("SELECTION_COORDINATE_DUPLICATE", coordinate))
            continue
        if not isinstance(spec, CanonicalInputSpec):
            diagnostics.append(ExcelAdapterDiagnostic("SEMANTIC_SELECTION_INVALID", coordinate))
            continue
        specs[coordinate] = spec

    fallback_rules: dict[str, ApprovedSelection] = {}
    rules_input = {} if zero_fallback_rules_by_coordinate is None else zero_fallback_rules_by_coordinate
    if not isinstance(rules_input, Mapping):
        diagnostics.append(ExcelAdapterDiagnostic("ZERO_FALLBACK_RULES_INVALID"))
    else:
        for raw_coordinate, rule in rules_input.items():
            coordinate = _normalize_coordinate(raw_coordinate)
            if coordinate is None:
                diagnostics.append(ExcelAdapterDiagnostic("FALLBACK_COORDINATE_INVALID", str(raw_coordinate)))
            elif coordinate in fallback_rules:
                diagnostics.append(ExcelAdapterDiagnostic("FALLBACK_COORDINATE_DUPLICATE", coordinate))
            elif not isinstance(rule, ApprovedSelection):
                diagnostics.append(ExcelAdapterDiagnostic("ZERO_FALLBACK_RULE_INVALID", coordinate))
            else:
                fallback_rules[coordinate] = rule

    other_approvals: dict[str, ApprovedSelection] = {}
    other_input = {} if other_metric_approvals_by_coordinate is None else other_metric_approvals_by_coordinate
    if not isinstance(other_input, Mapping):
        diagnostics.append(ExcelAdapterDiagnostic("OTHER_METRIC_APPROVALS_INVALID"))
    else:
        for raw_coordinate, approval in other_input.items():
            coordinate = _normalize_coordinate(raw_coordinate)
            if coordinate is None:
                diagnostics.append(ExcelAdapterDiagnostic("OTHER_APPROVAL_COORDINATE_INVALID", str(raw_coordinate)))
            elif coordinate in other_approvals:
                diagnostics.append(ExcelAdapterDiagnostic("OTHER_APPROVAL_COORDINATE_DUPLICATE", coordinate))
            elif not isinstance(approval, ApprovedSelection):
                diagnostics.append(ExcelAdapterDiagnostic("OTHER_METRIC_APPROVAL_INVALID", coordinate))
            else:
                other_approvals[coordinate] = approval

    owners_by_coordinate: dict[str, tuple[str, ...]] = {}
    for cell in observation.cells:
        if cell.cell_ref.worksheet_ordinal != match.worksheet_ordinal:
            continue
        coordinate = cell.cell_ref.coordinate
        owners = tuple(sorted(
            owner for owner, bounds in match.owned_coordinate_map
            if _coordinate_in_range(coordinate, bounds)
        ))
        if len(owners) > 1:
            diagnostics.append(ExcelAdapterDiagnostic("EXTRACTION_OWNERSHIP_AMBIGUOUS", coordinate))
        elif owners:
            owners_by_coordinate[coordinate] = owners
            if coordinate not in specs:
                diagnostics.append(ExcelAdapterDiagnostic("IN_SCOPE_SELECTION_MISSING", coordinate))

    for coordinate in specs:
        if coordinate not in owners_by_coordinate:
            diagnostics.append(ExcelAdapterDiagnostic("SELECTION_OUTSIDE_OWNED_RANGE", coordinate))
    for coordinate in fallback_rules:
        if coordinate not in specs:
            diagnostics.append(ExcelAdapterDiagnostic("FALLBACK_SELECTION_MISSING", coordinate))
    for coordinate in other_approvals:
        if coordinate not in specs:
            diagnostics.append(ExcelAdapterDiagnostic("OTHER_APPROVAL_SELECTION_MISSING", coordinate))

    submissions: list[CandidateSubmission] = []
    for coordinate in sorted(specs):
        if coordinate not in owners_by_coordinate:
            continue
        try:
            submissions.append(build_candidate_submission(
                observation,
                match,
                coordinate=coordinate,
                spec=specs[coordinate],
                zero_fallback_rule=fallback_rules.get(coordinate),
                other_metric_approval=other_approvals.get(coordinate),
            ))
        except CandidateValidationError as exc:
            diagnostics.append(ExcelAdapterDiagnostic(exc.code, coordinate))
        except (AttributeError, TypeError, ValueError):
            diagnostics.append(ExcelAdapterDiagnostic("CANDIDATE_BUILD_INPUT_INVALID", coordinate))

    if not submissions and not diagnostics:
        diagnostics.append(ExcelAdapterDiagnostic("CANDIDATES_EMPTY"))
    if diagnostics:
        return _result(observation, match, (), None, diagnostics)

    if admit:
        if revision is None:
            diagnostics.append(ExcelAdapterDiagnostic("REVISION_CONTEXT_REQUIRED"))
            return _result(observation, match, (), None, diagnostics)
        try:
            plan = prepare_canonical_batch(tuple(submissions), revision=revision)
        except AdmissionRejected as exc:
            diagnostics.extend(
                ExcelAdapterDiagnostic(item.code.value, identity=item.identity)
                for item in exc.diagnostics
            )
            return _result(observation, match, (), None, diagnostics)
        if approval_validator is not None:
            try:
                approval_validator(plan)
            except Exception as exc:
                code = getattr(exc, "code", "APPROVAL_CATALOG_VALIDATION_FAILED")
                diagnostics.append(ExcelAdapterDiagnostic(str(code)))
                return _result(observation, match, (), None, diagnostics)
        return _result(observation, match, tuple(submissions), plan, ())

    return _result(observation, match, tuple(submissions), None, ())


def _normalize_coordinate(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        row, column = coordinate_to_tuple(value)
        if row < 1 or column < 1:
            return None
        normalized = f"{get_column_letter(column)}{row}"
    except (TypeError, ValueError):
        return None
    return normalized if value == normalized else None


def _coordinate_in_range(coordinate: str, bounds: str) -> bool:
    try:
        row, column = coordinate_to_tuple(coordinate)
        left, top, right, bottom = range_boundaries(bounds)
        return left <= column <= right and top <= row <= bottom
    except (TypeError, ValueError):
        return False


def _result(
    observation: WorkbookObservation | None,
    match: TemplateMatchResult | None,
    submissions: tuple[CandidateSubmission, ...],
    plan: CanonicalPersistencePlan | None,
    diagnostics: list[ExcelAdapterDiagnostic] | tuple[ExcelAdapterDiagnostic, ...],
) -> ExcelAdapterResult:
    unique = set(diagnostics)
    ordered = tuple(sorted(
        unique,
        key=lambda item: (
            item.code,
            item.worksheet_ordinal or 0,
            item.coordinate or "",
            item.identity,
        ),
    ))
    return ExcelAdapterResult(observation, match, submissions, plan, ordered)
