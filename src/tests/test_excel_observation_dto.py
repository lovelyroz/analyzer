"""Tests for immutable, text-only Excel observation DTOs.

These tests are provided for owner-run validation; they were not executed
by the assistant.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.ingestion.excel.dto import (
    CellObservation,
    CellRange,
    CellRef,
    CellValueKind,
    Diagnostic,
    DiagnosticSeverity,
    ReaderProvenance,
    SourceArtifactObservation,
    WorkbookMetadataObservation,
    WorkbookObservation,
    WorksheetObservation,
    WorksheetVisibility,
)


def _cell_ref() -> CellRef:
    return CellRef(worksheet_ordinal=1, coordinate="A1", row_index=1, column_index=1)


def _source() -> SourceArtifactObservation:
    return SourceArtifactObservation(
        source_ref=None,
        file_name="sample.xlsx",
        format="xlsx",
        sha256="a" * 64,
        byte_length=128,
    )


def _reader() -> ReaderProvenance:
    return ReaderProvenance(
        reader_name="openpyxl",
        reader_version="3.1.5",
        profile_name="codal-text-only",
        profile_version="1",
        dto_schema_version="1",
    )


def test_cell_observation_preserves_literal_text_exactly():
    value = "  مبلغ فروش ۱۲۳٬۴۵۶٫۷۸  "
    cell = CellObservation(
        cell_ref=_cell_ref(),
        value_kind=CellValueKind.PRESENT_TEXT,
        data_type="s",
        text_value=value,
    )

    assert cell.text_value == value
    assert cell.unexpected_value is None


def test_blank_cell_is_not_zero_or_empty_text():
    cell = CellObservation(
        cell_ref=_cell_ref(),
        value_kind=CellValueKind.BLANK,
        data_type="n",
    )

    assert cell.text_value is None
    assert cell.unexpected_value is None


@pytest.mark.parametrize("value,data_type", [(123, "n"), (12.5, "n"), (True, "b"), ("=A1+B1", "f")])
def test_non_text_populated_cell_is_explicitly_unexpected(value, data_type):
    cell = CellObservation(
        cell_ref=_cell_ref(),
        value_kind=CellValueKind.UNEXPECTED_NON_TEXT,
        data_type=data_type,
        unexpected_value=value,
    )

    assert cell.value_kind is CellValueKind.UNEXPECTED_NON_TEXT
    assert cell.unexpected_value == value
    assert cell.text_value is None


def test_error_cell_preserves_error_token_and_diagnostic():
    diagnostic = Diagnostic(
        code="EXCEL_TEXT_ONLY_ERROR_CELL",
        severity=DiagnosticSeverity.ERROR,
        message="Excel error cells are not supported by the V1 text-only contract.",
        cell_ref=_cell_ref(),
    )
    cell = CellObservation(
        cell_ref=_cell_ref(),
        value_kind=CellValueKind.ERROR_VALUE,
        data_type="e",
        unexpected_value="#VALUE!",
        diagnostics=(diagnostic,),
    )

    assert cell.unexpected_value == "#VALUE!"
    assert cell.diagnostics[0].code == "EXCEL_TEXT_ONLY_ERROR_CELL"


def test_cell_observation_rejects_non_string_present_text():
    with pytest.raises(ValueError):
        CellObservation(
            cell_ref=_cell_ref(),
            value_kind=CellValueKind.PRESENT_TEXT,
            data_type="s",
            text_value=123,  # type: ignore[arg-type]
        )


def test_cell_observation_rejects_text_value_on_non_text_state():
    with pytest.raises(ValueError):
        CellObservation(
            cell_ref=_cell_ref(),
            value_kind=CellValueKind.BLANK,
            data_type="n",
            text_value="",
        )


def test_unexpected_non_text_requires_original_value():
    with pytest.raises(ValueError):
        CellObservation(
            cell_ref=_cell_ref(),
            value_kind=CellValueKind.UNEXPECTED_NON_TEXT,
            data_type="n",
        )


def test_nested_collections_must_be_tuples():
    with pytest.raises(TypeError):
        WorksheetObservation(
            ordinal=1,
            literal_name="Sheet1",
            visibility=WorksheetVisibility.VISIBLE,
            used_range=CellRange(1, 1, 1, 1, "A1"),
            merged_ranges=[],  # type: ignore[arg-type]
        )


def test_dto_instances_are_immutable():
    cell = CellObservation(
        cell_ref=_cell_ref(),
        value_kind=CellValueKind.PRESENT_TEXT,
        data_type="s",
        text_value="123",
    )

    with pytest.raises(FrozenInstanceError):
        cell.text_value = "456"  # type: ignore[misc]


def test_workbook_observation_requires_ordered_unique_worksheets():
    first = WorksheetObservation(
        ordinal=1,
        literal_name="Sheet1",
        visibility=WorksheetVisibility.VISIBLE,
        used_range=None,
    )
    second = WorksheetObservation(
        ordinal=2,
        literal_name="Sheet2",
        visibility=WorksheetVisibility.VISIBLE,
        used_range=None,
    )

    workbook = WorkbookObservation(
        source=_source(),
        reader=_reader(),
        metadata=WorkbookMetadataObservation(),
        worksheets=(first, second),
    )
    assert tuple(sheet.ordinal for sheet in workbook.worksheets) == (1, 2)

    with pytest.raises(ValueError):
        WorkbookObservation(
            source=_source(),
            reader=_reader(),
            metadata=WorkbookMetadataObservation(),
            worksheets=(second, first),
        )
