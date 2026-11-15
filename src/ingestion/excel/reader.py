"""Read-only, text-only CODAL XLSX observation adapter (V1).

This module observes workbook structure and literal cell content only. It does
not normalize text, parse numbers/dates, infer financial semantics, or persist
raw observations.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from typing import TypeAlias
import zipfile

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.utils.datetime import CALENDAR_MAC_1904, CALENDAR_WINDOWS_1900

from src.ingestion.excel.dto import (
    CellObservation,
    CellRange,
    CellRef,
    CellValueKind,
    ColumnObservation,
    Diagnostic,
    DiagnosticDetail,
    DiagnosticSeverity,
    DeclaredTableObservation,
    MetadataItem,
    ReaderProvenance,
    RowObservation,
    SourceArtifactObservation,
    StructureStatus,
    TableObservation,
    WorkbookDateSystem,
    WorkbookMetadataObservation,
    WorkbookObservation,
    WorksheetObservation,
    WorksheetVisibility,
)

BytesSource: TypeAlias = bytes | bytearray | memoryview
PathSource: TypeAlias = str | Path


@dataclass(frozen=True, slots=True)
class ExcelReaderConfig:
    """Resource and provenance settings for the V1 reader.

    Defaults are deliberately above the largest used range documented in the
    current Markdown workbook audits. They are guardrails, not capacity claims.
    Callers may lower or raise them explicitly after measuring their workload.
    """

    max_file_bytes: int = 25 * 1024 * 1024
    max_total_cells: int = 500_000
    max_worksheets: int = 100
    profile_name: str = "codal-text-only"
    profile_version: str = "1"
    dto_schema_version: str = "1"

    def __post_init__(self) -> None:
        if self.max_file_bytes < 1 or self.max_total_cells < 1 or self.max_worksheets < 1:
            raise ValueError("Excel reader resource limits must be positive.")
        if not all((self.profile_name, self.profile_version, self.dto_schema_version)):
            raise ValueError("Excel reader profile and DTO versions must be non-empty.")


class ExcelSourceReadError(ValueError):
    """Fatal XLSX package, format, or resource-limit failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class ExcelSourceContractError(ExcelSourceReadError):
    """The workbook was readable but violates the text-only source contract."""

    def __init__(self, observation: WorkbookObservation) -> None:
        self.observation = observation
        super().__init__(
            "EXCEL_TEXT_ONLY_CONTRACT_VIOLATION",
            "The workbook contains one or more populated non-text or error cells.",
        )


def _read_source(
    source: BytesSource | PathSource,
    *,
    file_name: str | None,
    max_file_bytes: int,
) -> tuple[bytes, str | None, str | None]:
    if isinstance(source, (bytes, bytearray, memoryview)):
        payload = bytes(source)
        resolved_name = file_name
        if resolved_name is not None and Path(resolved_name).suffix.lower() != ".xlsx":
            raise ExcelSourceReadError("EXCEL_UNSUPPORTED_EXTENSION", "V1 reader accepts .xlsx files only.")
        return payload, resolved_name, None
    path = Path(source)
    if path.suffix.lower() != ".xlsx":
        raise ExcelSourceReadError("EXCEL_UNSUPPORTED_EXTENSION", "V1 reader accepts .xlsx files only.")
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise ExcelSourceReadError("EXCEL_SOURCE_UNREADABLE", f"Cannot read source file: {exc}") from exc
    return payload, file_name or path.name, str(path)


def _preflight_package(payload: bytes, config: ExcelReaderConfig) -> None:
    if len(payload) > config.max_file_bytes:
        raise ExcelSourceReadError(
            "EXCEL_FILE_SIZE_LIMIT_EXCEEDED",
            f"XLSX source is {len(payload)} bytes; configured limit is {config.max_file_bytes}.",
        )
    stream = BytesIO(payload)
    if not zipfile.is_zipfile(stream):
        raise ExcelSourceReadError("EXCEL_INVALID_PACKAGE", "Source is not a valid XLSX ZIP package.")
    try:
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            members = archive.infolist()
            if len(members) > 10_000:
                raise ExcelSourceReadError("EXCEL_PACKAGE_MEMBER_LIMIT_EXCEEDED", "XLSX package has too many members.")
            uncompressed_size = sum(item.file_size for item in members)
            if uncompressed_size > 250 * 1024 * 1024:
                raise ExcelSourceReadError(
                    "EXCEL_UNCOMPRESSED_SIZE_LIMIT_EXCEEDED",
                    "XLSX package exceeds the 250 MiB uncompressed safety limit.",
                )
            names = {item.filename for item in members}
            if "xl/workbook.xml" not in names or "[Content_Types].xml" not in names:
                raise ExcelSourceReadError("EXCEL_INVALID_PACKAGE", "XLSX package is missing required workbook parts.")
            if any(name.startswith("xl/externalLinks/") for name in names):
                # External links are not resolved; their presence is not needed for cell observations.
                pass
    except zipfile.BadZipFile as exc:
        raise ExcelSourceReadError("EXCEL_INVALID_PACKAGE", "XLSX ZIP package is corrupt.") from exc


def _cell_range(min_row: int, min_column: int, max_row: int, max_column: int) -> CellRange:
    start = f"{get_column_letter(min_column)}{min_row}"
    end = f"{get_column_letter(max_column)}{max_row}"
    return CellRange(
        min_row=min_row,
        min_column=min_column,
        max_row=max_row,
        max_column=max_column,
        a1_range=start if start == end else f"{start}:{end}",
    )


def _visibility(state: str) -> WorksheetVisibility:
    return {
        "visible": WorksheetVisibility.VISIBLE,
        "hidden": WorksheetVisibility.HIDDEN,
        "veryHidden": WorksheetVisibility.VERY_HIDDEN,
    }.get(state, WorksheetVisibility.UNKNOWN)


def _date_system(epoch: object) -> WorkbookDateSystem:
    if epoch == CALENDAR_WINDOWS_1900:
        return WorkbookDateSystem.WINDOWS_1900
    if epoch == CALENDAR_MAC_1904:
        return WorkbookDateSystem.MAC_1904
    return WorkbookDateSystem.UNKNOWN


def _workbook_properties(workbook: object) -> tuple[MetadataItem, ...]:
    props = getattr(workbook, "properties", None)
    if props is None:
        return ()
    keys = (
        "creator", "title", "subject", "description", "keywords", "category",
        "language", "identifier", "lastModifiedBy", "revision", "version",
    )
    result: list[MetadataItem] = []
    for key in keys:
        value = getattr(props, key, None)
        if value is not None:
            result.append(MetadataItem(key=key, value=str(value)))
    for key in ("created", "modified"):
        value = getattr(props, key, None)
        if value is not None:
            result.append(MetadataItem(key=key, value=value.isoformat() if hasattr(value, "isoformat") else str(value)))
    return tuple(result)


def read_excel_source(
    source: BytesSource | PathSource,
    *,
    source_ref: str | None = None,
    file_name: str | None = None,
    config: ExcelReaderConfig | None = None,
) -> WorkbookObservation:
    """Read one XLSX source into an immutable observation.

    On a text-only contract violation, raises ExcelSourceContractError after
    scanning the workbook; the exception exposes the complete observation and
    all cell-level diagnostics so the caller can reject the entire report.
    """
    settings = config or ExcelReaderConfig()
    payload, resolved_name, resolved_path = _read_source(
        source, file_name=file_name, max_file_bytes=settings.max_file_bytes
    )
    _preflight_package(payload, settings)

    try:
        workbook = load_workbook(
            BytesIO(payload),
            read_only=False,
            data_only=False,
            keep_links=False,
        )
    except Exception as exc:
        raise ExcelSourceReadError("EXCEL_WORKBOOK_UNREADABLE", f"openpyxl could not read XLSX: {exc}") from exc

    try:
        sheet_names = tuple(workbook.sheetnames)
        if not sheet_names:
            raise ExcelSourceReadError("EXCEL_NO_WORKSHEETS", "Workbook contains no worksheets.")
        if len(sheet_names) > settings.max_worksheets:
            raise ExcelSourceReadError(
                "EXCEL_WORKSHEET_LIMIT_EXCEEDED",
                f"Workbook has {len(sheet_names)} worksheets; configured limit is {settings.max_worksheets}.",
            )

        declared_table_specs: list[tuple[int, int, TableObservation]] = []
        worksheet_shells: list[tuple[object, int, tuple[CellRange, ...], tuple[object, ...]]] = []
        total_scan_cells = 0
        for worksheet_ordinal, worksheet_name in enumerate(sheet_names, start=1):
            worksheet = workbook[worksheet_name]
            max_row = max(int(worksheet.max_row or 1), 1)
            max_column = max(int(worksheet.max_column or 1), 1)
            scan_count = max_row * max_column
            total_scan_cells += scan_count
            if total_scan_cells > settings.max_total_cells:
                raise ExcelSourceReadError(
                    "EXCEL_CELL_SCAN_LIMIT_EXCEEDED",
                    f"Workbook requires scanning {total_scan_cells} cells; configured limit is {settings.max_total_cells}.",
                )
            merged_ranges = tuple(
                sorted(
                    (_cell_range(r.min_row, r.min_col, r.max_row, r.max_col) for r in worksheet.merged_cells.ranges),
                    key=lambda item: (item.min_row, item.min_column, item.max_row, item.max_column),
                )
            )
            worksheet_shells.append((worksheet, worksheet_ordinal, merged_ranges, ()))

        cell_observations: list[CellObservation] = []
        row_observations: list[RowObservation] = []
        column_observations: list[ColumnObservation] = []
        worksheet_observations: list[WorksheetObservation] = []
        table_observations: list[TableObservation] = []
        workbook_diagnostics: list[Diagnostic] = []

        for worksheet, worksheet_ordinal, merged_ranges, _ in worksheet_shells:
            populated_bounds: list[tuple[int, int]] = []
            row_cells: dict[int, list[CellRef]] = {}
            column_cells: dict[int, list[CellRef]] = {}
            local_diagnostics: list[Diagnostic] = []
            merged_by_coordinate: dict[tuple[int, int], CellRange] = {}
            for merged in merged_ranges:
                for row_index in range(merged.min_row, merged.max_row + 1):
                    for column_index in range(merged.min_column, merged.max_column + 1):
                        merged_by_coordinate[(row_index, column_index)] = merged

            for row in worksheet.iter_rows():
                for cell in row:
                    value = cell.value
                    has_literal = value is not None
                    has_style = bool(getattr(cell, "has_style", False))
                    if not has_literal and not has_style:
                        continue
                    if has_literal or has_style:
                        populated_bounds.append((cell.row, cell.column))
                    cell_ref = CellRef(
                        worksheet_ordinal=worksheet_ordinal,
                        coordinate=cell.coordinate,
                        row_index=cell.row,
                        column_index=cell.column,
                    )
                    merged_range = merged_by_coordinate.get((cell.row, cell.column))
                    merged_anchor = None
                    if merged_range is not None:
                        anchor_coordinate = f"{get_column_letter(merged_range.min_column)}{merged_range.min_row}"
                        merged_anchor = CellRef(
                            worksheet_ordinal=worksheet_ordinal,
                            coordinate=anchor_coordinate,
                            row_index=merged_range.min_row,
                            column_index=merged_range.min_column,
                        )

                    diagnostic: Diagnostic | None = None
                    if value is None:
                        observation = CellObservation(
                            cell_ref=cell_ref,
                            value_kind=CellValueKind.BLANK,
                            data_type=cell.data_type or "n",
                            number_format=cell.number_format,
                            style_id=cell.style_id,
                            merged_range=merged_range,
                            merged_anchor=merged_anchor,
                        )
                    elif cell.data_type == "e":
                        diagnostic = Diagnostic(
                            code="EXCEL_TEXT_ONLY_ERROR_CELL",
                            severity=DiagnosticSeverity.ERROR,
                            message="Excel error cells violate the V1 text-only source contract.",
                            worksheet_ordinal=worksheet_ordinal,
                            cell_ref=cell_ref,
                        )
                        observation = CellObservation(
                            cell_ref=cell_ref,
                            value_kind=CellValueKind.ERROR_VALUE,
                            data_type=cell.data_type,
                            unexpected_value=value if isinstance(value, str) else str(value),
                            number_format=cell.number_format,
                            style_id=cell.style_id,
                            merged_range=merged_range,
                            merged_anchor=merged_anchor,
                            diagnostics=(diagnostic,),
                        )
                    elif isinstance(value, str) and cell.data_type in ("s", "inlineStr", "str"):
                        observation = CellObservation(
                            cell_ref=cell_ref,
                            value_kind=CellValueKind.PRESENT_TEXT,
                            data_type=cell.data_type,
                            text_value=value,
                            number_format=cell.number_format,
                            style_id=cell.style_id,
                            merged_range=merged_range,
                            merged_anchor=merged_anchor,
                        )
                    else:
                        diagnostic = Diagnostic(
                            code="EXCEL_TEXT_ONLY_NON_TEXT_CELL",
                            severity=DiagnosticSeverity.ERROR,
                            message="Populated non-text cells violate the V1 text-only source contract.",
                            worksheet_ordinal=worksheet_ordinal,
                            cell_ref=cell_ref,
                            details=(DiagnosticDetail("data_type", str(cell.data_type)),),
                        )
                        observation = CellObservation(
                            cell_ref=cell_ref,
                            value_kind=CellValueKind.UNEXPECTED_NON_TEXT,
                            data_type=cell.data_type or "n",
                            unexpected_value=value,
                            number_format=cell.number_format,
                            style_id=cell.style_id,
                            merged_range=merged_range,
                            merged_anchor=merged_anchor,
                            diagnostics=(diagnostic,),
                        )

                    cell_observations.append(observation)
                    row_cells.setdefault(cell.row, []).append(cell_ref)
                    column_cells.setdefault(cell.column, []).append(cell_ref)
                    if diagnostic is not None:
                        local_diagnostics.append(diagnostic)
                        workbook_diagnostics.append(diagnostic)

            used_range = None
            for merged in merged_ranges:
                populated_bounds.extend(((merged.min_row, merged.min_column), (merged.max_row, merged.max_column)))
            if populated_bounds:
                used_range = _cell_range(
                    min(row for row, _ in populated_bounds),
                    min(column for _, column in populated_bounds),
                    max(row for row, _ in populated_bounds),
                    max(column for _, column in populated_bounds),
                )

            declared_tables: list[tuple[str, str | None, CellRange]] = []
            for table_name in worksheet.tables:
                table = worksheet.tables[table_name]
                table_ref = getattr(table, "ref", None)
                if not table_ref:
                    continue
                try:
                    from openpyxl.utils.cell import range_boundaries
                    min_col, min_row, max_col, max_row = range_boundaries(table_ref)
                    bounds = _cell_range(min_row, min_col, max_row, max_col)
                except Exception:
                    continue
                declared_tables.append((str(table_name), getattr(table, "displayName", None), bounds))
            declared_tables.sort(key=lambda item: (item[2].min_row, item[2].min_column, item[0]))
            worksheet_table_ordinals: list[int] = []
            for name, display_name, bounds in declared_tables:
                table_ordinal = len(table_observations) + 1
                worksheet_table_ordinals.append(table_ordinal)
                table_observations.append(
                    TableObservation(
                        worksheet_ordinal=worksheet_ordinal,
                        table_ordinal=table_ordinal,
                        bounds=bounds,
                        detection_method="excel_structured_table",
                        detection_version="1",
                        status=StructureStatus.RESOLVED,
                        header_rows=(bounds.min_row,) if getattr(table, "headerRowCount", 1) else (),
                        row_refs=tuple(range(bounds.min_row, bounds.max_row + 1)),
                        column_refs=tuple(range(bounds.min_column, bounds.max_column + 1)),
                        diagnostics=(),
                    )
                )

            if used_range is not None:
                for row_index in range(used_range.min_row, used_range.max_row + 1):
                    row_observations.append(
                        RowObservation(
                            worksheet_ordinal=worksheet_ordinal,
                            row_index=row_index,
                            cell_refs=tuple(sorted(row_cells.get(row_index, ()), key=lambda ref: ref.column_index)),
                        )
                    )
                for column_index in range(used_range.min_column, used_range.max_column + 1):
                    column_observations.append(
                        ColumnObservation(
                            worksheet_ordinal=worksheet_ordinal,
                            column_index=column_index,
                            cell_refs=tuple(sorted(column_cells.get(column_index, ()), key=lambda ref: ref.row_index)),
                        )
                    )

            worksheet_observations.append(
                WorksheetObservation(
                    ordinal=worksheet_ordinal,
                    literal_name=worksheet.title,
                    visibility=_visibility(worksheet.sheet_state),
                    used_range=used_range,
                    merged_ranges=merged_ranges,
                    declared_tables=tuple(
                        DeclaredTableObservation(name=name, display_name=display_name, bounds=bounds)
                        for name, display_name, bounds in declared_tables
                    ),
                    candidate_table_ordinals=tuple(worksheet_table_ordinals),
                    diagnostics=tuple(local_diagnostics),
                )
            )

        date_system = _date_system(workbook.epoch)
        metadata = WorkbookMetadataObservation(
            date_system=date_system,
            workbook_properties=_workbook_properties(workbook),
            unsupported_features=(),
        )
        observation = WorkbookObservation(
            source=SourceArtifactObservation(
                source_ref=source_ref or resolved_path,
                file_name=resolved_name,
                format="xlsx",
                sha256=sha256(payload).hexdigest(),
                byte_length=len(payload),
            ),
            reader=ReaderProvenance(
                reader_name="openpyxl",
                reader_version=__import__("openpyxl").__version__,
                profile_name=settings.profile_name,
                profile_version=settings.profile_version,
                dto_schema_version=settings.dto_schema_version,
            ),
            metadata=metadata,
            worksheets=tuple(worksheet_observations),
            tables=tuple(table_observations),
            rows=tuple(row_observations),
            columns=tuple(column_observations),
            cells=tuple(cell_observations),
            diagnostics=tuple(workbook_diagnostics),
        )
        if workbook_diagnostics:
            raise ExcelSourceContractError(observation)
        return observation
    finally:
        workbook.close()


def read_excel_file(
    path: PathSource,
    *,
    source_ref: str | None = None,
    config: ExcelReaderConfig | None = None,
) -> WorkbookObservation:
    """Convenience wrapper for reading an XLSX path."""
    return read_excel_source(path, source_ref=source_ref, config=config)
