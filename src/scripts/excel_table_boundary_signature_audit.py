"""Read-only audit of compound structural patterns around all-text bands.

Flags a candidate signature only when a prior mixed/numeric row is followed by
one or more single-text rows and an all-text band, and that band is followed
by zero or more single-text rows and a mixed/numeric row. Flags are diagnostic
only; this utility never classifies headers, splits tables, or mutates workbooks.
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

POPULATED = {
    CellValueKind.PRESENT_TEXT,
    CellValueKind.PRESENT_NUMBER,
    CellValueKind.UNEXPECTED_NON_TEXT,
    CellValueKind.ERROR_VALUE,
}


def _kind(cells: list[object]) -> str:
    if not cells:
        return "EMPTY"
    if any(cell.value_kind in {
        CellValueKind.PRESENT_NUMBER,
        CellValueKind.UNEXPECTED_NON_TEXT,
        CellValueKind.ERROR_VALUE,
    } for cell in cells):
        return "MIXED_NUMERIC"
    if all(cell.value_kind is CellValueKind.PRESENT_TEXT for cell in cells):
        return "SINGLE_TEXT" if len(cells) == 1 else "MULTI_TEXT"
    return "OTHER"


def _value(cell: object, limit: int = 72) -> str:
    if cell.value_kind is CellValueKind.PRESENT_TEXT:
        value = repr(cell.text_value)
    elif cell.value_kind is CellValueKind.PRESENT_NUMBER:
        value = repr(cell.numeric_value)
    else:
        value = f"<{cell.value_kind.value}:{cell.unexpected_value!r}>"
    return value if len(value) <= limit else value[:limit - 3] + "..."


def _row_line(index: int, cells: list[object]) -> str:
    if not cells:
        return f"row {index} [EMPTY]"
    cells = sorted(cells, key=lambda item: item.cell_ref.column_index)
    columns = ",".join(get_column_letter(c.cell_ref.column_index) for c in cells)
    values = " | ".join(
        f"{c.cell_ref.coordinate}={_value(c)}" for c in cells
    )
    return f"row {index} [{_kind(cells)} n={len(cells)} columns={columns}]: {values}"


def _signature(
    first: int,
    last: int,
    by_row: dict[int, list[object]],
    before: int,
    after: int,
) -> tuple[bool, str, str]:
    prior = {
        row: _kind(by_row.get(row, []))
        for row in range(max(1, first - before), first)
    }
    prior_body = max(
        (row for row, kind in prior.items() if kind == "MIXED_NUMERIC"),
        default=None,
    )
    prior_gap = (
        [prior[row] for row in range(prior_body + 1, first)]
        if prior_body is not None else []
    )
    prior_ok = (
        prior_body is not None
        and "SINGLE_TEXT" in prior_gap
        and all(kind in {"SINGLE_TEXT", "EMPTY"} for kind in prior_gap)
    )

    following = {
        row: _kind(by_row.get(row, []))
        for row in range(last + 1, last + after + 1)
    }
    next_body = min(
        (row for row, kind in following.items() if kind == "MIXED_NUMERIC"),
        default=None,
    )
    following_gap = (
        [following[row] for row in range(last + 1, next_body)]
        if next_body is not None else []
    )
    following_ok = (
        next_body is not None
        and all(kind in {"SINGLE_TEXT", "EMPTY"} for kind in following_gap)
    )
    return (
        prior_ok and following_ok,
        f"prior_body={prior_body}; gap={','.join(prior_gap) or 'none'}",
        f"next_body={next_body}; gap={','.join(following_gap) or 'none'}",
    )


def _audit(path: Path, limit: int, before: int, after: int) -> None:
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
            if (cell.cell_ref.worksheet_ordinal == sheet.ordinal
                    and cell.value_kind in POPULATED):
                by_row[cell.cell_ref.row_index].append(cell)

        text_rows = sorted(
            row for row, cells in by_row.items()
            if len(cells) >= 2
            and all(c.value_kind is CellValueKind.PRESENT_TEXT for c in cells)
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
            f"| bands={len(bands)}"
        )
        flagged = 0
        for number, band in enumerate(bands[:limit], 1):
            first, last = band[0], band[-1]
            candidate, prior_text, following_text = _signature(
                first, last, by_row, before, after
            )
            flagged += int(candidate)
            band_cells = [c for row in band for c in by_row[row]]
            columns = {c.cell_ref.column_index for c in band_cells}
            merges = [
                m.a1_range for m in sheet.merged_ranges
                if m.min_row <= last and m.max_row >= first
                and m.min_column <= max(columns) and m.max_column >= min(columns)
            ]
            print(
                f"\n[BAND {number}] rows={first}:{last} "
                f"columns={','.join(get_column_letter(c) for c in sorted(columns))} "
                f"merges={','.join(merges) if merges else '—'}"
            )
            print(f"  SIGNATURE={'COMPOUND_CANDIDATE' if candidate else 'NO_MATCH'}")
            print(f"  PRIOR {prior_text}")
            print(f"  FOLLOWING {following_text}")
            for row in range(max(1, first - before), last + after + 1):
                cells = sorted(
                    by_row.get(row, []),
                    key=lambda c: c.cell_ref.column_index,
                )
                print("  " + _row_line(row, cells))
                row_merges = [
                    m.a1_range for m in sheet.merged_ranges
                    if m.min_row <= row <= m.max_row
                ]
                if row_merges:
                    print(f"    MERGES {','.join(row_merges)}")

        print(
            f"\nSUMMARY bands_printed={min(len(bands), limit)} "
            f"compound_candidates={flagged}"
        )
        if len(bands) > limit:
            print(f"... {len(bands) - limit} bands omitted; increase --max-bands.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit compound row patterns around all-text bands; no table splitting."
    )
    parser.add_argument("workbooks", nargs="+", type=Path)
    parser.add_argument("--max-bands", type=int, default=200)
    parser.add_argument("--context-before", type=int, default=6)
    parser.add_argument("--context-after", type=int, default=6)
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
