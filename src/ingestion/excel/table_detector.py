"""Conservative visual table-region candidate detection for CODAL XLSX observations.

This module identifies structural candidates only. It does not interpret headers,
financial metrics, periods, units, row meaning, or report scope.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import replace

from openpyxl.utils import get_column_letter

from src.ingestion.excel.dto import (
    CellRange,
    CellObservation,
    CellRef,
    CellValueKind,
    Diagnostic,
    DiagnosticDetail,
    DiagnosticSeverity,
    FragmentPresence,
    HeaderFragmentObservation,
    StructureStatus,
    TableObservation,
    WorkbookObservation,
)


DETECTION_METHOD = "conservative_blank_band_v1"
DETECTION_VERSION = "1"


def _contiguous_bands(values: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Split sorted occupied indices at one-or-more fully empty indices."""
    if not values:
        return ()
    bands: list[list[int]] = [[values[0]]]
    for value in values[1:]:
        if value > bands[-1][-1] + 1:
            bands.append([value])
        else:
            bands[-1].append(value)
    return tuple(tuple(band) for band in bands)


def _range_text(min_col: int, min_row: int, max_col: int, max_row: int) -> str:
    start = f"{get_column_letter(min_col)}{min_row}"
    end = f"{get_column_letter(max_col)}{max_row}"
    return start if start == end else f"{start}:{end}"


def detect_visual_table_candidates(observation: WorkbookObservation) -> WorkbookObservation:
    """Return a new observation with conservative visual table candidates added.

    A candidate requires at least two occupied rows, two occupied columns, and
    three populated text cells. Fully empty rows/columns are strong separators.
    A merged range spanning a proposed separator makes the candidate AMBIGUOUS.

    Adjacent merged headings are retained as title evidence only; they do not
    expand candidate bounds and do not establish financial or table semantics.
    Declared Excel structured tables remain authoritative and are not duplicated.
    """
    cells_by_sheet: dict[int, list[CellObservation]] = defaultdict(list)
    for cell in observation.cells:
        if cell.value_kind is CellValueKind.PRESENT_TEXT:
            cells_by_sheet[cell.cell_ref.worksheet_ordinal].append(cell)

    existing_by_sheet: dict[int, list[TableObservation]] = defaultdict(list)
    for table in observation.tables:
        existing_by_sheet[table.worksheet_ordinal].append(table)

    new_tables: list[TableObservation] = []
    sheet_candidate_ordinals: dict[int, list[int]] = defaultdict(list)

    for sheet in observation.worksheets:
        sheet_cells = cells_by_sheet.get(sheet.ordinal, [])
        if not sheet_cells:
            continue

        by_row: dict[int, list[CellObservation]] = defaultdict(list)
        for cell in sheet_cells:
            by_row[cell.cell_ref.row_index].append(cell)

        row_bands = _contiguous_bands(tuple(sorted(by_row)))
        next_ordinal = max(
            (table.table_ordinal for table in existing_by_sheet.get(sheet.ordinal, [])),
            default=0,
        ) + 1

        for row_band in row_bands:
            band_cells = [cell for row in row_band for cell in by_row[row]]
            by_column: dict[int, list[CellObservation]] = defaultdict(list)
            for cell in band_cells:
                by_column[cell.cell_ref.column_index].append(cell)

            for column_band in _contiguous_bands(tuple(sorted(by_column))):
                region_cells = [
                    cell for cell in band_cells
                    if cell.cell_ref.column_index in column_band
                ]
                occupied_rows = tuple(sorted({c.cell_ref.row_index for c in region_cells}))
                occupied_columns = tuple(sorted({c.cell_ref.column_index for c in region_cells}))

                # A lone caption, label, or short note is not a table candidate.
                if len(occupied_rows) < 2 or len(occupied_columns) < 2 or len(region_cells) < 3:
                    continue

                min_row, max_row = occupied_rows[0], occupied_rows[-1]
                min_col, max_col = occupied_columns[0], occupied_columns[-1]

                # A merged range that bridges a blank separator invalidates certainty.
                crossing_merges = []
                for merged in sheet.merged_ranges:
                    bridges_row_separator = (
                        merged.min_row < min_row <= merged.max_row
                        or merged.min_row <= max_row < merged.max_row
                    )
                    bridges_column_separator = (
                        merged.min_column < min_col <= merged.max_column
                        or merged.min_column <= max_col < merged.max_column
                    )
                    if bridges_row_separator or bridges_column_separator:
                        crossing_merges.append(merged)

                # Do not duplicate or partially reinterpret an explicit structured table.
                overlaps_declared = any(
                    not (
                        table.bounds.max_row < min_row or table.bounds.min_row > max_row
                        or table.bounds.max_column < min_col or table.bounds.min_column > max_col
                    )
                    for table in existing_by_sheet.get(sheet.ordinal, [])
                )
                if overlaps_declared:
                    continue

                all_rows = tuple(sorted(by_row))
                all_columns = tuple(sorted({cell.cell_ref.column_index for cell in sheet_cells}))
                previous_rows = [value for value in all_rows if value < min_row]
                next_rows = [value for value in all_rows if value > max_row]
                weak_row_gap = (
                    bool(previous_rows) and min_row - previous_rows[-1] == 2
                ) or (
                    bool(next_rows) and next_rows[0] - max_row == 2
                )
                previous_columns = [value for value in all_columns if value < min_col]
                next_columns = [value for value in all_columns if value > max_col]
                weak_column_gap = (
                    bool(previous_columns) and min_col - previous_columns[-1] == 2
                ) or (
                    bool(next_columns) and next_columns[0] - max_col == 2
                )
                has_weak_separator = weak_row_gap or weak_column_gap
                is_ambiguous = bool(crossing_merges) or has_weak_separator
                status = StructureStatus.AMBIGUOUS if is_ambiguous else StructureStatus.CANDIDATE
                diagnostics: list[Diagnostic] = []
                if has_weak_separator:
                    diagnostics.append(Diagnostic(
                        code="EXCEL_TABLE_SINGLE_BLANK_SEPARATOR",
                        severity=DiagnosticSeverity.WARNING,
                        message="A single blank row or column is a weak separator and does not prove an independent table boundary.",
                        worksheet_ordinal=sheet.ordinal,
                        table_ordinal=next_ordinal,
                    ))
                if crossing_merges:
                    diagnostics.append(Diagnostic(
                        code="EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE",
                        severity=DiagnosticSeverity.WARNING,
                        message="A merged range spans a proposed visual table boundary; candidate bounds are ambiguous.",
                        worksheet_ordinal=sheet.ordinal,
                        table_ordinal=next_ordinal,
                        details=tuple(
                            DiagnosticDetail(key="merged_range", value=item.a1_range or "")
                            for item in crossing_merges
                        ),
                    ))

                # A nearby merged heading is evidence only, never a resolved caption.
                title_fragments: list[HeaderFragmentObservation] = []
                for merged in sheet.merged_ranges:
                    if not (0 < min_row - merged.max_row <= 2):
                        continue
                    if merged.max_column < min_col or merged.min_column > max_col:
                        continue
                    anchor = next((
                        cell for cell in sheet_cells
                        if cell.cell_ref.row_index == merged.min_row
                        and cell.cell_ref.column_index == merged.min_column
                    ), None)
                    if anchor is not None:
                        title_fragments.append(HeaderFragmentObservation(
                            literal_text=anchor.text_value,
                            source_cells=(anchor.cell_ref,),
                            level=1,
                            presence=FragmentPresence.EXPLICIT,
                            merge_anchor=anchor.cell_ref,
                        ))

                candidate = TableObservation(
                    worksheet_ordinal=sheet.ordinal,
                    table_ordinal=next_ordinal,
                    bounds=CellRange(
                        min_row=min_row,
                        min_column=min_col,
                        max_row=max_row,
                        max_column=max_col,
                        a1_range=_range_text(min_col, min_row, max_col, max_row),
                    ),
                    detection_method=DETECTION_METHOD,
                    detection_version=DETECTION_VERSION,
                    status=status,
                    title_fragments=tuple(title_fragments),
                    row_refs=occupied_rows,
                    column_refs=occupied_columns,
                    diagnostics=tuple(diagnostics),
                )
                new_tables.append(candidate)
                sheet_candidate_ordinals[sheet.ordinal].append(next_ordinal)
                next_ordinal += 1

    updated_sheets = tuple(
        replace(
            sheet,
            candidate_table_ordinals=tuple(sorted(set(
                sheet.candidate_table_ordinals
                + tuple(sheet_candidate_ordinals.get(sheet.ordinal, ()))
            ))),
        )
        for sheet in observation.worksheets
    )
    return replace(observation, worksheets=updated_sheets, tables=tuple(
        observation.tables + tuple(new_tables)
    ))
