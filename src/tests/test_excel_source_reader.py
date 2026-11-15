"""Owner-run tests for the text-only openpyxl source reader.

The assistant authors these tests but does not execute them.
"""
from io import BytesIO

import pytest
from openpyxl import Workbook

from src.ingestion.excel.dto import CellValueKind, StructureStatus, WorksheetVisibility
from src.ingestion.excel.reader import (
    ExcelReaderConfig,
    ExcelSourceContractError,
    ExcelSourceReadError,
    read_excel_source,
)


def _xlsx_bytes(workbook: Workbook) -> bytes:
    stream = BytesIO()
    workbook.save(stream)
    return stream.getvalue()


def test_reader_preserves_literal_persian_text_and_source_fingerprint():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "گزارش"
    literal = "  مبلغ فروش ۱۲۳٬۴۵۶٫۷۸\t"
    sheet["A1"] = literal
    payload = _xlsx_bytes(workbook)

    result = read_excel_source(payload, file_name="sample.xlsx")

    assert result.source.sha256
    assert result.source.byte_length == len(payload)
    assert result.source.file_name == "sample.xlsx"
    assert result.cells[0].value_kind is CellValueKind.PRESENT_TEXT
    assert result.cells[0].text_value == literal
    assert result.worksheets[0].literal_name == "گزارش"


def test_reader_preserves_worksheet_order_visibility_and_merged_ranges():
    workbook = Workbook()
    first = workbook.active
    first.title = "First"
    first["B2"] = "عنوان"
    first.merge_cells("B2:C2")
    second = workbook.create_sheet("Hidden")
    second.sheet_state = "hidden"
    second["A1"] = "متن"

    result = read_excel_source(_xlsx_bytes(workbook))

    assert [sheet.literal_name for sheet in result.worksheets] == ["First", "Hidden"]
    assert result.worksheets[0].visibility is WorksheetVisibility.VISIBLE
    assert result.worksheets[1].visibility is WorksheetVisibility.HIDDEN
    assert result.worksheets[0].merged_ranges[0].a1_range == "B2:C2"
    assert result.worksheets[0].used_range.a1_range == "B2:C2"
    anchor = next(cell for cell in result.cells if cell.cell_ref.coordinate == "B2")
    assert anchor.merged_anchor.coordinate == "B2"


@pytest.mark.parametrize(
    "value,data_type,expected_kind",
    [
        (123, "n", CellValueKind.UNEXPECTED_NON_TEXT),
        (True, "b", CellValueKind.UNEXPECTED_NON_TEXT),
        ("=1+1", "f", CellValueKind.UNEXPECTED_NON_TEXT),
        ("#VALUE!", "e", CellValueKind.ERROR_VALUE),
    ],
)
def test_reader_rejects_entire_workbook_for_populated_non_text_cells(value, data_type, expected_kind):
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "valid text"
    sheet["B2"] = value
    sheet["B2"].data_type = data_type

    with pytest.raises(ExcelSourceContractError) as caught:
        read_excel_source(_xlsx_bytes(workbook))

    observation = caught.value.observation
    invalid = next(cell for cell in observation.cells if cell.cell_ref.coordinate == "B2")
    assert invalid.value_kind is expected_kind
    assert invalid.diagnostics[0].severity.value == "ERROR"
    assert len(observation.diagnostics) == 1
    assert observation.diagnostics[0].cell_ref.coordinate == "B2"


def test_reader_collects_all_contract_violations_before_rejecting():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = 1
    sheet["B2"] = True
    sheet["C3"] = "bad formula"
    sheet["C3"].data_type = "f"

    with pytest.raises(ExcelSourceContractError) as caught:
        read_excel_source(_xlsx_bytes(workbook))

    assert [item.cell_ref.coordinate for item in caught.value.observation.diagnostics] == [
        "A1", "B2", "C3"
    ]


def test_reader_keeps_blank_cells_out_of_sparse_cell_observations():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "left"
    sheet["C1"] = "right"

    result = read_excel_source(_xlsx_bytes(workbook))

    assert [cell.cell_ref.coordinate for cell in result.cells] == ["A1", "C1"]
    assert result.worksheets[0].used_range.a1_range == "A1:C1"
    assert tuple(row.row_index for row in result.rows) == (1,)
    assert tuple(column.column_index for column in result.columns) == (1, 2, 3)
    assert result.rows[0].cell_refs[0].coordinate == "A1"
    assert result.columns[2].cell_refs[0].coordinate == "C1"


def test_reader_is_repeatable_for_identical_source_bytes():
    workbook = Workbook()
    workbook.active["A1"] = "متن"
    payload = _xlsx_bytes(workbook)

    first = read_excel_source(payload)
    second = read_excel_source(payload)

    assert first.source.sha256 == second.source.sha256
    assert first == second


def test_reader_rejects_invalid_package():
    with pytest.raises(ExcelSourceReadError) as caught:
        read_excel_source(b"not an xlsx file")
    assert caught.value.code == "EXCEL_INVALID_PACKAGE"


def test_reader_enforces_configured_cell_scan_limit():
    workbook = Workbook()
    workbook.active["B2"] = "text"

    with pytest.raises(ExcelSourceReadError) as caught:
        read_excel_source(
            _xlsx_bytes(workbook),
            config=ExcelReaderConfig(max_total_cells=1),
        )
    assert caught.value.code == "EXCEL_CELL_SCAN_LIMIT_EXCEEDED"


def test_reader_records_declared_structured_table_as_resolved_structure():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Header A", "Header B"])
    sheet.append(["one", "two"])
    from openpyxl.worksheet.table import Table, TableStyleInfo

    table = Table(displayName="SourceTable", ref="A1:B2")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    sheet.add_table(table)

    result = read_excel_source(_xlsx_bytes(workbook))

    assert len(result.tables) == 1
    assert result.tables[0].status is StructureStatus.RESOLVED
    assert result.tables[0].detection_method == "excel_structured_table"
    assert result.tables[0].bounds.a1_range == "A1:B2"
    assert result.worksheets[0].candidate_table_ordinals == (1,)
