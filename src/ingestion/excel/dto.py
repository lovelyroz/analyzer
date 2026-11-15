"""Immutable, transient DTOs for CODAL Excel source observations.

V1 source cells must contain literal values, not formulas. Literal text and
literal numeric values are preserved in their native observed forms; unsupported
cell kinds are reported rather than coerced. These DTOs are not persistence models.
These DTOs are not persistence models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import StrEnum
from typing import TypeAlias


ScalarValue: TypeAlias = str | int | float | bool | date | datetime | time | timedelta | None


class WorkbookDateSystem(StrEnum):
    WINDOWS_1900 = "WINDOWS_1900"
    MAC_1904 = "MAC_1904"
    UNKNOWN = "UNKNOWN"


class WorksheetVisibility(StrEnum):
    VISIBLE = "VISIBLE"
    HIDDEN = "HIDDEN"
    VERY_HIDDEN = "VERY_HIDDEN"
    UNKNOWN = "UNKNOWN"


class StructureStatus(StrEnum):
    RESOLVED = "RESOLVED"
    CANDIDATE = "CANDIDATE"
    AMBIGUOUS = "AMBIGUOUS"
    UNSUPPORTED = "UNSUPPORTED"


class CellValueKind(StrEnum):
    PRESENT_TEXT = "PRESENT_TEXT"
    PRESENT_NUMBER = "PRESENT_NUMBER"
    BLANK = "BLANK"
    UNEXPECTED_NON_TEXT = "UNEXPECTED_NON_TEXT"
    ERROR_VALUE = "ERROR_VALUE"


class HeaderAxisKind(StrEnum):
    GROUP = "GROUP"
    MEASURE = "MEASURE"
    TEMPORAL = "TEMPORAL"
    PRESENTATION = "PRESENTATION"
    ROW_LABEL = "ROW_LABEL"
    UNIT_OR_BASIS = "UNIT_OR_BASIS"
    UNCLASSIFIED = "UNCLASSIFIED"


class FragmentPresence(StrEnum):
    EXPLICIT = "EXPLICIT"
    MERGED_INHERITED = "MERGED_INHERITED"
    BLANK = "BLANK"
    UNRESOLVED = "UNRESOLVED"


class DiagnosticSeverity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class CellRef:
    worksheet_ordinal: int
    coordinate: str
    row_index: int
    column_index: int

    def __post_init__(self) -> None:
        if self.worksheet_ordinal < 1 or self.row_index < 1 or self.column_index < 1:
            raise ValueError("Worksheet, row, and column indices must be 1-based positive integers.")
        if not self.coordinate:
            raise ValueError("Cell coordinate must not be empty.")


@dataclass(frozen=True, slots=True)
class CellRange:
    min_row: int
    min_column: int
    max_row: int
    max_column: int
    a1_range: str | None = None

    def __post_init__(self) -> None:
        if min(self.min_row, self.min_column) < 1:
            raise ValueError("Cell range indices must be 1-based positive integers.")
        if self.max_row < self.min_row or self.max_column < self.min_column:
            raise ValueError("Cell range maximum bounds must not precede minimum bounds.")


@dataclass(frozen=True, slots=True)
class DiagnosticDetail:
    key: str
    value: str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    severity: DiagnosticSeverity
    message: str
    worksheet_ordinal: int | None = None
    table_ordinal: int | None = None
    cell_ref: CellRef | None = None
    details: tuple[DiagnosticDetail, ...] = ()

    def __post_init__(self) -> None:
        if not self.code or not self.message:
            raise ValueError("Diagnostic code and message are required.")
        if not isinstance(self.details, tuple):
            raise TypeError("Diagnostic details must be an immutable tuple.")


@dataclass(frozen=True, slots=True)
class MetadataItem:
    key: str
    value: str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class SourceArtifactObservation:
    source_ref: str | None
    file_name: str | None
    format: str
    sha256: str
    byte_length: int

    def __post_init__(self) -> None:
        if not self.format or not self.sha256:
            raise ValueError("Source format and SHA-256 fingerprint are required.")
        if self.byte_length < 0:
            raise ValueError("Source byte length cannot be negative.")


@dataclass(frozen=True, slots=True)
class ReaderProvenance:
    reader_name: str
    reader_version: str
    profile_name: str
    profile_version: str
    dto_schema_version: str

    def __post_init__(self) -> None:
        if not all((self.reader_name, self.reader_version, self.profile_name,
                    self.profile_version, self.dto_schema_version)):
            raise ValueError("Reader provenance fields must be non-empty.")


@dataclass(frozen=True, slots=True)
class WorkbookMetadataObservation:
    date_system: WorkbookDateSystem = WorkbookDateSystem.UNKNOWN
    workbook_properties: tuple[MetadataItem, ...] = ()
    unsupported_features: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.workbook_properties, tuple) or not isinstance(self.unsupported_features, tuple):
            raise TypeError("Workbook metadata collections must be tuples.")


@dataclass(frozen=True, slots=True)
class DeclaredTableObservation:
    name: str
    display_name: str | None
    bounds: CellRange


@dataclass(frozen=True, slots=True)
class WorksheetObservation:
    ordinal: int
    literal_name: str
    visibility: WorksheetVisibility
    used_range: CellRange | None
    merged_ranges: tuple[CellRange, ...] = ()
    declared_tables: tuple[DeclaredTableObservation, ...] = ()
    candidate_table_ordinals: tuple[int, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if self.ordinal < 1 or not self.literal_name:
            raise ValueError("Worksheet ordinal and literal name are required.")
        for name in ("merged_ranges", "declared_tables", "candidate_table_ordinals", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be an immutable tuple.")
        if any(value < 1 for value in self.candidate_table_ordinals):
            raise ValueError("Candidate table ordinals must be 1-based positive integers.")


@dataclass(frozen=True, slots=True)
class HeaderFragmentObservation:
    literal_text: str | None
    source_cells: tuple[CellRef, ...]
    level: int
    presence: FragmentPresence
    merge_anchor: CellRef | None = None
    axis: HeaderAxisKind = HeaderAxisKind.UNCLASSIFIED

    def __post_init__(self) -> None:
        if self.level < 1:
            raise ValueError("Header level must be 1-based.")
        if not isinstance(self.source_cells, tuple):
            raise TypeError("Header source cells must be a tuple.")


@dataclass(frozen=True, slots=True)
class HeaderAxisObservation:
    axis: HeaderAxisKind
    fragments: tuple[HeaderFragmentObservation, ...]
    parent_axis_ref: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.fragments, tuple):
            raise TypeError("Header fragments must be a tuple.")


@dataclass(frozen=True, slots=True)
class RowObservation:
    worksheet_ordinal: int
    row_index: int
    label_fragments: tuple[HeaderFragmentObservation, ...] = ()
    parent_row_index: int | None = None
    outline_level: int | None = None
    cell_refs: tuple[CellRef, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if self.worksheet_ordinal < 1 or self.row_index < 1:
            raise ValueError("Worksheet and row indices must be 1-based.")
        for name in ("label_fragments", "cell_refs", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be an immutable tuple.")


@dataclass(frozen=True, slots=True)
class ColumnObservation:
    worksheet_ordinal: int
    column_index: int
    header_axes: tuple[HeaderAxisObservation, ...] = ()
    cell_refs: tuple[CellRef, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if self.worksheet_ordinal < 1 or self.column_index < 1:
            raise ValueError("Worksheet and column indices must be 1-based.")
        for name in ("header_axes", "cell_refs", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be a tuple.")


@dataclass(frozen=True, slots=True)
class TableObservation:
    worksheet_ordinal: int
    table_ordinal: int
    bounds: CellRange
    detection_method: str
    detection_version: str
    status: StructureStatus
    title_fragments: tuple[HeaderFragmentObservation, ...] = ()
    header_rows: tuple[int, ...] = ()
    header_columns: tuple[int, ...] = ()
    row_refs: tuple[int, ...] = ()
    column_refs: tuple[int, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if self.worksheet_ordinal < 1 or self.table_ordinal < 1:
            raise ValueError("Worksheet and table ordinals must be 1-based.")
        if not self.detection_method or not self.detection_version:
            raise ValueError("Table detection method and version are required.")
        for name in ("title_fragments", "header_rows", "header_columns", "row_refs", "column_refs", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be a tuple.")


@dataclass(frozen=True, slots=True)
class CellObservation:
    cell_ref: CellRef
    value_kind: CellValueKind
    data_type: str
    text_value: str | None = None
    numeric_value: int | float | None = None
    unexpected_value: ScalarValue = None
    number_format: str | None = None
    style_id: int | None = None
    merged_range: CellRange | None = None
    merged_anchor: CellRef | None = None
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if not self.data_type:
            raise ValueError("Excel cell data type code is required.")
        if self.value_kind is CellValueKind.PRESENT_TEXT and not isinstance(self.text_value, str):
            raise ValueError("PRESENT_TEXT cells must retain their literal text value.")
        if self.value_kind is not CellValueKind.PRESENT_TEXT and self.text_value is not None:
            raise ValueError("Only PRESENT_TEXT cells may carry text_value.")
        if self.value_kind is CellValueKind.PRESENT_NUMBER:
            if isinstance(self.numeric_value, bool) or not isinstance(self.numeric_value, (int, float)):
                raise ValueError("PRESENT_NUMBER cells must retain a literal int or float value.")
        elif self.numeric_value is not None:
            raise ValueError("Only PRESENT_NUMBER cells may carry numeric_value.")
        if self.value_kind in (CellValueKind.PRESENT_TEXT, CellValueKind.PRESENT_NUMBER, CellValueKind.BLANK) and self.unexpected_value is not None:
            raise ValueError("Present literal and blank cells cannot carry unexpected_value.")
        if self.value_kind is CellValueKind.UNEXPECTED_NON_TEXT and self.unexpected_value is None:
            raise ValueError("Unexpected non-text cells must retain their observed scalar value.")
        if self.value_kind is CellValueKind.ERROR_VALUE and not isinstance(self.unexpected_value, str):
            raise ValueError("Excel error cells must retain their literal error token.")
        if not isinstance(self.diagnostics, tuple):
            raise TypeError("Cell diagnostics must be an immutable tuple.")


@dataclass(frozen=True, slots=True)
class WorkbookObservation:
    source: SourceArtifactObservation
    reader: ReaderProvenance
    metadata: WorkbookMetadataObservation
    worksheets: tuple[WorksheetObservation, ...]
    tables: tuple[TableObservation, ...] = ()
    rows: tuple[RowObservation, ...] = ()
    columns: tuple[ColumnObservation, ...] = ()
    cells: tuple[CellObservation, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        for name in ("worksheets", "tables", "rows", "columns", "cells", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be an immutable tuple.")
        if not self.worksheets:
            raise ValueError("A workbook observation must contain at least one worksheet.")
        ordinals = tuple(sheet.ordinal for sheet in self.worksheets)
        if ordinals != tuple(sorted(ordinals)) or len(set(ordinals)) != len(ordinals):
            raise ValueError("Worksheets must be ordered by unique ascending ordinal.")
