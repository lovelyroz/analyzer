"""Read-only audit of column continuity from all-text bands into following rows.

This utility does not classify headers or split tables. It reports populated
column footprints, overlap with the preceding text-only band, row value-kind
counts, and merged-range geometry across a configurable physical-row window.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from openpyxl.utils import get_column_letter

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


def _column_list(columns: set[int] | tuple[int, ...]) -> str:
    return ",".join(get_column_letter(value) for value in sorted(columns)) or "—"


def _jaccard(left: set[int], right: set[int]) -> str:
    union = left | right
    if not union:
        return "—"
    return f"{len(left & right) / len(union):.3f}"


def _row_counts(cells: list[object]) -> tuple[int, int, int]:
    text = sum(cell.value_kind is CellValueKind.PRESENT_TEXT for cell in cells)
    number = sum(cell.value_kind is CellValueKind.PRESENT_NUMBER for cell in cells)
    other = len(cells) - text - number
    return text, number, other


def _row_line(row_index: int, cells: list[object], band_columns: set[int]) -> str:
    if not cells:
        return f"row {row_index}: <EMPTY> overlap=0/0 jaccard=—"
    ordered = sorted(cells, key=lambda cell: cell.cell_ref.column_index)
    columns = {cell.cell_ref.column_index for cell in ordered}
    text, number, other = _row_counts(ordered)
    overlap = len(columns & band_columns)
    ratio = f"{overlap}/{len(columns)}"
    values = " | ".join(
        f"{cell.cell_ref.coordinate}={_value(cell)}" for cell in ordered
    )
    return (
        f"row {row_index} [n={len(ordered)} text={text} number={number} "
        f"other={other} columns={_column_list(columns)} "
        f"band_overlap={ratio} jaccard={_jaccard(columns, band_columns)}]: {values}"
    )


def _value(cell: object, limit: int = 84) -> str:
    if cell.value_kind is CellValueKind.PRESENT_TEXT:
        rendered = repr(cell.text_value)
    elif cell.value_kind is CellValueKind.PRESENT_NUMBER:
        rendered = repr(cell.numeric_value)
    else:
        rendered = f"<{cell.value_kind.value}:{cell.unexpected_value!r}>"
    return rendered if len(rendered) <= limit else rendered[: limit - 3] + "..."


def _audit(path: Path, max_bands: int, lookahead_rows: int) -> None:
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
        by_row: dict[int, list[object]] = defaultdict(list)
        for cell in observation.cells:
            if (
                cell.cell_ref.worksheet_ordinal == sheet.ordinal
                and cell.value_kind in POPULATED_KINDS
            ):
                by_row[cell.cell_ref.row_index].append(cell)

        text_rows = sorted(
            row for row, cells in by_row.items()
            if len(cells) >= 2
            and all(cell.value_kind is CellValueKind.PRESENT_TEXT for cell in cells)
        )
        bands: list[list[int]] = []
        for row in text_rows:
            if not bands or row != bands[-1][-1] + 1:
                bands.append([row])
            else:
                bands[-1].append(row)

        print(
            f"\n### SHEET {sheet.ordinal} {sheet.literal_name} "
            f"| used={sheet.used_range.a1_range if sheet.used_range else '—'} "
            f"| text_rows={len(text_rows)} | bands={len(bands)}"
        )
        for index, band in enumerate(bands[:max_bands], start=1):
            band_cells = [cell for row in band for cell in by_row[row]]
            band_columns = {cell.cell_ref.column_index for cell in band_cells}
            min_col, max_col = min(band_columns), max(band_columns)
            first, last = band[0], band[-1]
            band_merges = [
                merged.a1_range for merged in sheet.merged_ranges
                if merged.min_row <= last and merged.max_row >= first
                and merged.min_column <= max_col and merged.max_column >= min_col
            ]
            print(
                f"\n[BAND {index}] rows={first}:{last} height={len(band)} "
                f"columns={_column_list(band_columns)} "
                f"column_span={get_column_letter(min_col)}:{get_column_letter(max_col)} "
                f"band_merges={','.join(band_merges) if band_merges else '—'}"
            )
            for row in band:
                cells = by_row[row]
                columns = {cell.cell_ref.column_index for cell in cells}
                print(
                    f"  HEADER_ROW {row} columns={_column_list(columns)} "
                    f"jaccard_to_band={_jaccard(columns, band_columns)}"
                )
            for row in range(last + 1, last + lookahead_rows + 1):
                print("  " + _row_line(row, by_row.get(row, []), band_columns))
                row_merges = [
                    merged.a1_range for merged in sheet.merged_ranges
                    if merged.min_row <= row <= merged.max_row
                    and merged.min_column <= max_col and merged.max_column >= min_col
                ]
                if row_merges:
                    print(f"    ROW_MERGES {','.join(row_merges)}")

            transition_merges = [
                merged.a1_range for merged in sheet.merged_ranges
                if merged.min_row <= last and merged.max_row > last
                and merged.min_column <= max_col and merged.max_column >= min_col
            ]
            if transition_merges:
                print(f"  MERGES_CROSSING_BAND_TO_BODY {','.join(transition_merges)}")

        omitted = len(bands) - min(len(bands), max_bands)
        if omitted:
            print(f"\n... {omitted} additional bands omitted; increase --max-bands.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit physical-row column continuity and merged geometry after "
            "all-text bands; does not classify headers or split tables."
        )
    )
    parser.add_argument("workbooks", nargs="+", type=Path)
    parser.add_argument("--max-bands", type=int, default=200)
    parser.add_argument("--lookahead-rows", type=int, default=6)
    args = parser.parse_args()
    if args.max_bands < 1:
        parser.error("--max-bands must be at least 1")
    if args.lookahead_rows < 1:
        parser.error("--lookahead-rows must be at least 1")
    missing = [str(path) for path in args.workbooks if not path.is_file()]
    if missing:
        parser.error("Workbook(s) not found: " + ", ".join(missing))
    for path in args.workbooks:
        _audit(path, args.max_bands, args.lookahead_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
