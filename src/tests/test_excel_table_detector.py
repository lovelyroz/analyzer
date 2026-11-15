"""Owner-run tests for conservative visual Excel table candidate detection."""
from io import BytesIO

from openpyxl import Workbook

from src.ingestion.excel.dto import StructureStatus
from src.ingestion.excel.reader import read_excel_source
from src.ingestion.excel.table_detector import detect_visual_table_candidates


def _observation(workbook: Workbook):
    stream = BytesIO()
    workbook.save(stream)
    return read_excel_source(stream.getvalue())


def test_detects_two_independent_vertical_tables_separated_by_blank_row():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["A", "B"])
    sheet.append(["1", "2"])
    sheet.append([])
    sheet.append(["C", "D"])
    sheet.append(["3", "4"])

    result = detect_visual_table_candidates(_observation(workbook))

    assert len(result.tables) == 2
    assert [table.bounds.a1_range for table in result.tables] == ["A1:B2", "A4:B5"]
    assert all(table.status is StructureStatus.AMBIGUOUS for table in result.tables)
    assert all(table.diagnostics[0].code == "EXCEL_TABLE_SINGLE_BLANK_SEPARATOR" for table in result.tables)
    assert result.worksheets[0].candidate_table_ordinals == (1, 2)


def test_detects_side_by_side_regions_separated_by_empty_column():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "Left A"
    sheet["B1"] = "Left B"
    sheet["A2"] = "1"
    sheet["B2"] = "2"
    sheet["D1"] = "Right A"
    sheet["E1"] = "Right B"
    sheet["D2"] = "3"
    sheet["E2"] = "4"

    result = detect_visual_table_candidates(_observation(workbook))

    assert [table.bounds.a1_range for table in result.tables] == ["A1:B2", "D1:E2"]
    assert all(table.status is StructureStatus.AMBIGUOUS for table in result.tables)


def test_preserves_nearby_merged_caption_as_evidence_not_as_table_bounds():
    workbook = Workbook()
    sheet = workbook.active
    sheet.merge_cells("A1:B1")
    sheet["A1"] = "عنوان جدول"
    sheet["A3"] = "Header A"
    sheet["B3"] = "Header B"
    sheet["A4"] = "one"
    sheet["B4"] = "two"

    result = detect_visual_table_candidates(_observation(workbook))

    assert len(result.tables) == 1
    table = result.tables[0]
    assert table.bounds.a1_range == "A3:B4"
    assert len(table.title_fragments) == 1
    assert table.title_fragments[0].literal_text == "عنوان جدول"
    assert table.status is StructureStatus.AMBIGUOUS
    assert any(item.code == "EXCEL_TABLE_SINGLE_BLANK_SEPARATOR" for item in table.diagnostics)


def test_merged_range_bridging_candidate_boundary_makes_status_ambiguous():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "A"
    sheet["B1"] = "B"
    sheet["A2"] = "1"
    sheet["B2"] = "2"
    sheet.merge_cells("A2:A4")
    sheet["B4"] = "C"
    sheet["C4"] = "D"
    sheet["B5"] = "3"
    sheet["C5"] = "4"

    result = detect_visual_table_candidates(_observation(workbook))

    assert len(result.tables) == 2
    second = result.tables[1]
    assert second.status is StructureStatus.AMBIGUOUS
    assert any(item.code == "EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE" for item in second.diagnostics)


def test_two_blank_rows_provide_a_stronger_separator_for_candidates():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["A", "B"])
    sheet.append(["1", "2"])
    sheet.append([])
    sheet.append([])
    sheet.append(["C", "D"])
    sheet.append(["3", "4"])

    result = detect_visual_table_candidates(_observation(workbook))

    assert len(result.tables) == 2
    assert all(table.status is StructureStatus.CANDIDATE for table in result.tables)

def test_single_row_caption_or_note_is_not_promoted_to_table():
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "فروش ماهانه"
    sheet["A3"] = "یادداشت"

    result = detect_visual_table_candidates(_observation(workbook))

    assert result.tables == ()


def test_detector_is_repeatable_and_does_not_change_source_cells():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Header A", "Header B"])
    sheet.append(["one", "two"])
    source = _observation(workbook)

    first = detect_visual_table_candidates(source)
    second = detect_visual_table_candidates(source)

    assert first == second
    assert first.cells == source.cells
    assert source.tables == ()


def test_numeric_literal_cells_participate_in_visual_table_detection():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["شرح", "مقدار"])
    sheet.append(["فروش", 1250])
    sheet.append(["تعداد", 0])

    result = detect_visual_table_candidates(_observation(workbook))

    assert len(result.tables) == 1
    assert result.tables[0].bounds.a1_range == "A1:B3"
    assert result.tables[0].column_refs == (1, 2)
