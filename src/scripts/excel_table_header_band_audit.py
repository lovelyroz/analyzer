"""Owner-run, read-only audit of multi-cell all-text row bands.

The utility groups physically adjacent rows containing at least two literal text
cells and no numeric/other populated cells. It prints neighboring physical rows,
column footprints, and merged-range geometry. It does not classify headers,
infer financial meaning, split regions, or modify workbooks.
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


def _value(cell: object, limit: int = 96) -> str:
    if cell.value_kind is CellValueKind.PRESENT_TEXT:
        rendered = repr(cell.text_value)
    elif cell.value_kind is CellValueKind.PRESENT_NUMBER:
        rendered = repr(cell.numeric_value)
    else:
        rendered = f"<{cell.value_kind.value}:{cell.unexpected_value!r}>"
    return rendered if len(rendered) <= limit else rendered[: limit - 3] + "..."


def _is_text_band_row(cells: list[object]) -> bool:
    return len(cells) >= 2 and all(
        cell.value_kind is CellValueKind.PRESENT_TEXT for cell in cells
    )


def _row_text(row_index: int, cells: list[object], merges: list[str]) -> str:
    if not cells:
        return f"row {row_index}: <EMPTY>"
    cells = sorted(cells, key=lambda item: item.cell_ref.column_index)
    text_count = sum(c.value_kind is CellValueKind.PRESENT_TEXT for c in cells)
    number_count = sum(c.value_kind is CellValueKind.PRESENT_NUMBER for c in cells)
    columns = ",".join(get_column_letter(c.cell_ref.column_index) for c in cells)
    values = " | ".join(
        f"{cell.cell_ref.coordinate}={_value(cell)}" for cell in cells
    )
    merge_text = f" merges={','.join(merges)}" if merges else ""
    return (
        f"row {row_index} [n={len(cells)} text={text_count} number={number_count} "
        f"columns={columns}]{merge_text}: {values}"
    )


def _audit(path: Path, max_bands: int, context_before: int, context_after: int) -> None:
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

        candidate_rows = sorted(
            row for row, cells in by_row.items() if _is_text_band_row(cells)
        )
        bands: list[list[int]] = []
        for row in candidate_rows:
            if not bands or row != bands[-1][-1] + 1:
                bands.append([row])
            else:
                bands[-1].append(row)

        print(
            f"\n### SHEET {sheet.ordinal} {sheet.literal_name} "
            f"| used={sheet.used_range.a1_range if sheet.used_range else '—'} "
            f"| all_text_rows={len(candidate_rows)} | adjacent_bands={len(bands)}"
        )
        if not bands:
            print("No multi-cell all-text rows.")
            continue

        for band_index, band in enumerate(bands[:max_bands], start=1):
            first, last = band[0], band[-1]
            print(
                f"\n[BAND {band_index}] rows={first}:{last} "
                f"band_height={len(band)}"
            )
            for row_index in range(max(1, first - context_before), last + context_after + 1):
                row_merges = [
                    merged.a1_range
                    for merged in sheet.merged_ranges
                    if merged.min_row <= row_index <= merged.max_row
                ]
                print(
                    "  "
                    + _row_text(
                        row_index,
                        by_row.get(row_index, []),
                        row_merges,
                    )
                )

        omitted = len(bands) - min(len(bands), max_bands)
        if omitted:
            print(
                f"\n... {omitted} additional all-text bands omitted; "
                "increase --max-bands."
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit physically adjacent multi-cell all-text row bands and their "
            "neighboring rows across representative Excel workbooks."
        )
    )
    parser.add_argument("workbooks", nargs="+", type=Path)
    parser.add_argument("--max-bands", type=int, default=200)
    parser.add_argument("--context-before", type=int, default=1)
    parser.add_argument("--context-after", type=int, default=2)
    args = parser.parse_args()
    if args.max_bands < 1:
        parser.error("--max-bands must be at least 1")
    if args.context_before < 0 or args.context_after < 0:
        parser.error("context row counts cannot be negative")
    missing = [str(path) for path in args.workbooks if not path.is_file()]
    if missing:
        parser.error("Workbook(s) not found: " + ", ".join(missing))
    for path in args.workbooks:
        _audit(path, args.max_bands, args.context_before, args.context_after)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
