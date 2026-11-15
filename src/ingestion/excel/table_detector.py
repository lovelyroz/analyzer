"""Conservative visual table-region candidate detection for CODAL XLSX observations.

This module identifies structural candidates only. It does not interpret headers,
financial metrics, periods, units, row meaning, or report scope.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import replace

from src.ingestion.excel.dto import (
    CellObservation,
    CellValueKind,
    Diagnostic,
    DiagnosticDetail,
    DiagnosticSeverity,
    HeaderFragmentObservation,
    CellRef,
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


def _cell_ref(cell: CellObservation) -> CellRef:
    return cell.cell_ref


def detect_visual_table_candidates(observation: WorkbookObservation) -> WorkbookObservation:
    """Return a new observation with conservative visual table candidates added.

    A candidate requires at least two occupied rows, two occupied columns, and
    three populated text cells. Fully empty rows/columns are treated as strong
    separators. A merged range crossing a proposed separator makes the
    affected candidate AMBIGUOUS instead of silently accepting the boundary.

    One-cell/one-row captions are retained only as adjacent title evidence when
    an immediately preceding merged heading overlaps the candidate columns.
    They are never treated as proof of a table or used to infer semantics.
    """
    cells_by_sheet: dict[int, list[CellObservation]] = defaultdict(list)
    for cell in observation.cells:
        if cell.value_kind is CellValueKind.PRESENT_TEXT:
            cells_by_sheet[cell.cell_ref.worksheet_ordinal].append(cell)

    existing = list(observation.tables)
    existing_by_sheet: dict[int, list[TableObservation]] = defaultdict(list)
    for table in existing:
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

            column_bands = _contiguous_bands(tuple(sorted(by_column)))
            for column_band in column_bands:
                region_cells = [
                    cell for cell in band_cells
                    if cell.cell_ref.column_index in column_band
                ]
                occupied_rows = tuple(sorted({c.cell_ref.row_index for c in region_cells}))
                occupied_columns = tuple(sorted({c.cell_ref.column_index for c in region_cells}))

                # A lone caption, label, or short note is not a table candidate.
                if len(occupied_rows) < 2 or len(occupied_columns) < 2 or len(region_cells) < 3:
                    continue

                min_row, max_row = min(occupied_rows), max(occupied_rows)
                min_col, max_col = min(occupied_columns), max(occupied_columns)
                crossing_merges = []
                for merged in sheet.merged_ranges:
                    crosses_row_gap = (
                        merged.min_row <= max_row and merged.max_row >= min_row
                        and any(min_row <= gap <= max_row for gap in range(merged.min_row, merged.max_row + 1))
                        and any(merged.min_row <= gap < merged.max_row for gap in range(min_row, max_row))
                    )
                    crosses_col_gap = (
                        merged.min_column <= max_col and merged.max_column >= min_col
                        and any(merged.min_column <= gap < merged.max_column for gap in range(min_col, max_col))
                    )
                    if crosses_row_gap or crosses_col_gap:
                        crossing_merges.append(merged)

                status = StructureStatus.AMBIGUOUS if crossing_merges else StructureStatus.CANDIDATE
                diagnostics: list[Diagnostic] = []
                if crossing_merges:
                    diagnostics.append(Diagnostic(
                        code="EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE",
                        severity=DiagnosticSeverity.WARNING,
                        message="A merged range crosses a proposed visual table boundary; candidate bounds are ambiguous.",
                        worksheet_ordinal=sheet.ordinal,
                        table_ordinal=next_ordinal,
                        details=tuple(
                            DiagnosticDetail(key="merged_range", value=item.a1_range or "")
                            for item in crossing_merges
                        ),
                    ))

                # Capture a merged heading immediately above the region as evidence,
                # but do not expand the data bounds or assert that it is a caption.
                title_fragments: list[HeaderFragmentObservation] = []
                for merged in sheet.merged_ranges:
                    if merged.max_row != min_row - 1:
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
                            source_cells=(_cell_ref(anchor),),
                            level=1,
                            presence=__import__(
                                "src.ingestion.excel.dto", fromlist=["FragmentPresence"]
                            ).FragmentPresence.EXPLICIT,
                            merge_anchor=_cell_ref(anchor),
                        ))

                # Do not resolve a candidate that overlaps a declared structured table.
                bounds_overlap = any(
                    not (
                        table.bounds.max_row < min_row or table.bounds.min_row > max_row
                        or table.bounds.max_column < min_col or table.bounds.min_column > max_col
                    )
                    for table in existing_by_sheet.get(sheet.ordinal, [])
                )
                if bounds_overlap:
                    continue

                candidate = TableObservation(
                    worksheet_ordinal=sheet.ordinal,
                    table_ordinal=next_ordinal,
                    bounds=__import__(
                        "src.ingestion.excel.dto", fromlist=["CellRange"]
                    ).CellRange(
                        min_row=min_row,
                        min_column=min_col,
                        max_row=max_row,
                        max_column=max_col,
                        a1_range=(
                            f"{__import__('openpyxl').utils.get_column_letter(min_col)}{min_row}:"
                            f"{__import__('openpyxl').utils.get_column_letter(max_col)}{max_row}"
                        ),
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
    return replace(
        observation,
        worksheets=updated_sheets,
        tables=tuple(existing + new_tables),
    )
