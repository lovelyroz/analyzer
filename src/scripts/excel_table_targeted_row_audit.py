"""Owner-run, read-only audit of literal cell content around known table boundaries.

This utility exposes source cell coordinates and literal values for narrowly
selected row windows. It does not infer headers, financial meaning, or table
boundaries and does not modify the workbook.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from src.ingestion.excel.dto import CellValueKind
from src.ingestion.excel.reader import read_excel_file


DEFAULT_RANGES = "292:302,306:337,355:362,402:409"


def _parse_ranges(raw: str) -> tuple[tuple[int, int], ...]:
    parsed: list[tuple[int, int]] = []
    for item in raw.split(","):
        parts = item.strip().split(":", maxsplit=1)
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(
                f"Invalid row range {item!r}; expected START:END."
            )
        try:
            start, end = (int(part) for part in parts)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Invalid row range {item!r}; row numbers must be integers."
            ) from exc
        if start < 1 or end < start:
            raise argparse.ArgumentTypeError(
                f"Invalid row range {item!r}; require 1 <= START <= END."
            )
        parsed.append((start, end))
    if not parsed:
        raise argparse.ArgumentTypeError("At least one row range is required.")
    return tuple(parsed)


def _value(cell: object) -> str:
    if cell.value_kind is CellValueKind.PRESENT_TEXT:
        return repr(cell.text_value)
    if cell.value_kind is CellValueKind.PRESENT_NUMBER:
        return repr(cell.numeric_value)
    if cell.value_kind is CellValueKind.UNEXPECTED_NON_TEXT:
        return f"<unexpected {cell.data_type}: {cell.unexpected_value!r}>"
    if cell.value_kind is CellValueKind.ERROR_VALUE:
        return f"<error {cell.unexpected_value!r}>"
    return "<blank>"


def _audit(path: Path, sheet_ordinal: int, ranges: tuple[tuple[int, int], ...]) -> int:
    observation = read_excel_file(path)
    sheet = next(
        (item for item in observation.worksheets if item.ordinal == sheet_ordinal),
        None,
    )
    if sheet is None:
        print(f"ERROR: worksheet ordinal {sheet_ordinal} does not exist.")
        return 2

    print(f"Workbook: {path}")
    print(f"SHA-256: {observation.source.sha256}")
    print(f"Worksheet: {sheet.ordinal} / {sheet.literal_name}")
    print(f"Used range: {sheet.used_range.a1_range if sheet.used_range else '—'}")
    print(f"Observed cells: {len(observation.cells)}")

    sheet_cells = [
        cell for cell in observation.cells
        if cell.cell_ref.worksheet_ordinal == sheet_ordinal
    ]

    for start, end in ranges:
        print(f"\n===== ROW WINDOW {start}:{end} =====")
        intersecting_merges = [
            merged.a1_range for merged in sheet.merged_ranges
            if merged.min_row <= end and merged.max_row >= start
        ]
        print("Merged ranges: " + (", ".join(intersecting_merges) if intersecting_merges else "—"))

        for row_index in range(start, end + 1):
            row_cells = sorted(
                (
                    cell for cell in sheet_cells
                    if cell.cell_ref.row_index == row_index
                    and cell.value_kind in (
                        CellValueKind.PRESENT_TEXT,
                        CellValueKind.PRESENT_NUMBER,
                        CellValueKind.UNEXPECTED_NON_TEXT,
                        CellValueKind.ERROR_VALUE,
                    )
                ),
                key=lambda cell: cell.cell_ref.column_index,
            )
            if not row_cells:
                print(f"ROW {row_index}: <NO LITERAL VALUES>")
                continue
            parts = [
                f"{cell.cell_ref.coordinate}={_value(cell)}"
                for cell in row_cells
            ]
            print(f"ROW {row_index} ({len(row_cells)} populated): " + " | ".join(parts))

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Print literal cell values and merged-range topology for selected "
            "worksheet row windows; no table boundaries are inferred."
        )
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--sheet-ordinal", type=int, default=1)
    parser.add_argument("--ranges", type=_parse_ranges, default=_parse_ranges(DEFAULT_RANGES))
    args = parser.parse_args()

    if args.sheet_ordinal < 1:
        parser.error("--sheet-ordinal must be a positive integer")
    if not args.workbook.is_file():
        parser.error(f"Workbook does not exist: {args.workbook}")

    return _audit(args.workbook, args.sheet_ordinal, args.ranges)


if __name__ == "__main__":
    raise SystemExit(main())
