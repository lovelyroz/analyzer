"""Owner-run, read-only cross-workbook audit of title/note/header row patterns.

The utility reports structural row shapes around single-cell literal-text rows.
It does not classify financial meaning, split regions, or modify workbooks.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from src.ingestion.excel.dto import CellValueKind
from src.ingestion.excel.reader import (
    ExcelSourceContractError,
    ExcelSourceReadError,
    read_excel_file,
)


POPULATED_KINDS = {
    CellValueKind.PRESENT_TEXT,
    CellValueKind.PRESENT_NUMBER,
    CellValueKind.UNEXPECTED_NON_TEXT,
    CellValueKind.ERROR_VALUE,
}


def _cell_value(cell: object, limit: int = 88) -> str:
    if cell.value_kind is CellValueKind.PRESENT_TEXT:
        value = repr(cell.text_value)
    elif cell.value_kind is CellValueKind.PRESENT_NUMBER:
        value = repr(cell.numeric_value)
    else:
        value = f"<{cell.value_kind.value}:{cell.unexpected_value!r}>"
    if len(value) > limit:
        return value[: limit - 3] + "..."
    return value


def _row_signature(cells: list[object]) -> str:
    text_count = sum(c.value_kind is CellValueKind.PRESENT_TEXT for c in cells)
    number_count = sum(c.value_kind is CellValueKind.PRESENT_NUMBER for c in cells)
    other_count = len(cells) - text_count - number_count
    return (
        f"n={len(cells)} text={text_count} number={number_count} "
        f"other={other_count}"
    )


def _row_line(row_index: int, cells: list[object], merges: list[str]) -> str:
    if not cells:
        return f"row {row_index}: <empty>"
    values = " | ".join(
        f"{cell.cell_ref.coordinate}={_cell_value(cell)}"
        for cell in sorted(cells, key=lambda item: item.cell_ref.column_index)
    )
    merge_text = f" merges={','.join(merges)}" if merges else ""
    return f"row {row_index} [{_row_signature(cells)}]{merge_text}: {values}"


def _audit_workbook(path: Path, max_per_sheet: int) -> None:
    print(f"\n## WORKBOOK {path}")
    try:
        observation = read_excel_file(path)
    except ExcelSourceContractError as exc:
        observation = exc.observation
        print("Reader: REJECTED (diagnostic evidence only)")
        print(f"SHA-256: {observation.source.sha256}")
    except ExcelSourceReadError as exc:
        print(f"Reader: ERROR {exc.code}: {exc}")
        return
    else:
        print("Reader: ACCEPTED")
        print(f"SHA-256: {observation.source.sha256}")

    for sheet in observation.worksheets:
        cells_by_row: dict[int, list[object]] = defaultdict(list)
        for cell in observation.cells:
            if (
                cell.cell_ref.worksheet_ordinal == sheet.ordinal
                and cell.value_kind in POPULATED_KINDS
            ):
                cells_by_row[cell.cell_ref.row_index].append(cell)

        row_indices = sorted(cells_by_row)
        row_positions = {row: index for index, row in enumerate(row_indices)}
        single_text_rows = [
            row for row in row_indices
            if len(cells_by_row[row]) == 1
            and cells_by_row[row][0].value_kind is CellValueKind.PRESENT_TEXT
        ]

        print(
            f"\n### SHEET {sheet.ordinal} {sheet.literal_name} "
            f"| used={sheet.used_range.a1_range if sheet.used_range else '—'} "
            f"| populated_rows={len(row_indices)} "
            f"| single_text_rows={len(single_text_rows)}"
        )
        if not single_text_rows:
            print("No single-cell literal-text rows.")
            continue

        shown = single_text_rows[:max_per_sheet]
        for row in shown:
            pos = row_positions[row]
            context_rows = row_indices[pos:min(pos + 4, len(row_indices))]
            context_cells = [cells_by_row[item] for item in context_rows]

            pattern = "NO_HEADER_PATTERN_WITHIN_NEXT_3_POPULATED_ROWS"
            if len(context_cells) >= 2:
                next_row = context_cells[1]
                if (
                    len(next_row) >= 2
                    and all(c.value_kind is CellValueKind.PRESENT_TEXT for c in next_row)
                ):
                    pattern = "SINGLE_TEXT_THEN_ALL_TEXT_ROW"
                elif len(context_cells) >= 3:
                    second, third = context_cells[1], context_cells[2]
                    if (
                        len(second) == 1
                        and second[0].value_kind is CellValueKind.PRESENT_TEXT
                        and len(third) >= 2
                        and all(c.value_kind is CellValueKind.PRESENT_TEXT for c in third)
                    ):
                        pattern = "SINGLE_TEXT_NOTE_THEN_ALL_TEXT_ROW"
                    elif any(c.value_kind is CellValueKind.PRESENT_NUMBER for c in next_row):
                        pattern = "SINGLE_TEXT_THEN_MIXED_ROW"

            print(f"\n[{pattern}] anchor_row={row}")
            for context_row, row_cells in zip(context_rows, context_cells):
                row_merges = [
                    merged.a1_range
                    for merged in sheet.merged_ranges
                    if merged.min_row <= context_row <= merged.max_row
                ]
                print("  " + _row_line(context_row, row_cells, row_merges))

            nearby_merges = [
                merged.a1_range for merged in sheet.merged_ranges
                if merged.min_row <= row + 3 and merged.max_row >= row
            ]
            if nearby_merges:
                print("  nearby merged ranges: " + ", ".join(nearby_merges))

        omitted = len(single_text_rows) - len(shown)
        if omitted:
            print(f"\n... {omitted} additional single-text rows omitted; increase --max-per-sheet.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit row-shape patterns around single-cell literal-text rows "
            "across representative Excel workbooks; no table splitting occurs."
        )
    )
    parser.add_argument("workbooks", nargs="+", type=Path)
    parser.add_argument(
        "--max-per-sheet",
        type=int,
        default=100,
        help="Maximum single-text row contexts per worksheet (default: 100).",
    )
    args = parser.parse_args()
    if args.max_per_sheet < 1:
        parser.error("--max-per-sheet must be at least 1")

    missing = [str(path) for path in args.workbooks if not path.is_file()]
    if missing:
        parser.error("Workbook(s) not found: " + ", ".join(missing))

    for path in args.workbooks:
        _audit_workbook(path, args.max_per_sheet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
