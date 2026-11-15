"""Owner-run audit of structural formatting transitions between Excel rows.

This utility reports evidence only. It does not split tables, infer financial
meaning, or change workbook content.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from src.ingestion.excel.dto import CellValueKind, WorkbookObservation
from src.ingestion.excel.reader import read_excel_file


def _jaccard(left: set[object], right: set[object]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def _ranges(values: set[int]) -> str:
    if not values:
        return "—"
    ordered = sorted(values)
    groups: list[list[int]] = [[ordered[0]]]
    for value in ordered[1:]:
        if value == groups[-1][-1] + 1:
            groups[-1].append(value)
        else:
            groups.append([value])
    return ",".join(
        str(group[0]) if len(group) == 1 else f"{group[0]}-{group[-1]}"
        for group in groups
    )


def _row_profiles(observation: WorkbookObservation, worksheet_ordinal: int):
    rows: dict[int, list[object]] = defaultdict(list)
    for cell in observation.cells:
        if (
            cell.cell_ref.worksheet_ordinal == worksheet_ordinal
            and cell.value_kind in (CellValueKind.PRESENT_TEXT, CellValueKind.PRESENT_NUMBER)
        ):
            rows[cell.cell_ref.row_index].append(cell)

    profiles = {}
    for row_index, cells in rows.items():
        columns = {cell.cell_ref.column_index for cell in cells}
        styles = {cell.style_id for cell in cells if cell.style_id is not None}
        bottom = {
            cell.cell_ref.column_index for cell in cells
            if cell.border_bottom is not None
        }
        top = {
            cell.cell_ref.column_index for cell in cells
            if cell.border_top is not None
        }
        left = {
            cell.cell_ref.column_index for cell in cells
            if cell.border_left is not None
        }
        right = {
            cell.cell_ref.column_index for cell in cells
            if cell.border_right is not None
        }
        profiles[row_index] = {
            "cells": cells,
            "columns": columns,
            "styles": styles,
            "bottom": bottom,
            "top": top,
            "left": left,
            "right": right,
            "text": sum(cell.value_kind is CellValueKind.PRESENT_TEXT for cell in cells),
            "numeric": sum(cell.value_kind is CellValueKind.PRESENT_NUMBER for cell in cells),
            "bold": sum(cell.font_bold is True for cell in cells),
            "filled": sum(cell.fill_type is not None for cell in cells),
            "style_counts": Counter(cell.style_id for cell in cells if cell.style_id is not None),
            "border_tokens": sorted({
                f"{cell.cell_ref.coordinate}:{edge}={value}"
                for cell in cells
                for edge, value in (
                    ("T", cell.border_top), ("B", cell.border_bottom),
                    ("L", cell.border_left), ("R", cell.border_right),
                )
                if value is not None
            }),
        }
    return profiles


def _audit_sheet(observation: WorkbookObservation, worksheet_ordinal: int, limit: int) -> None:
    sheet = next(item for item in observation.worksheets if item.ordinal == worksheet_ordinal)
    profiles = _row_profiles(observation, worksheet_ordinal)
    print(f"\n### Worksheet {worksheet_ordinal}: {sheet.literal_name}")
    if len(profiles) < 2:
        print("- Not enough populated rows for row-boundary analysis.")
        return

    rows = sorted(profiles)
    transitions = []
    for previous_row, current_row in zip(rows, rows[1:]):
        previous = profiles[previous_row]
        current = profiles[current_row]
        gap = current_row - previous_row - 1
        column_similarity = _jaccard(previous["columns"], current["columns"])
        style_similarity = _jaccard(previous["styles"], current["styles"])
        bottom = previous["bottom"]
        top = current["top"]
        matched_edges = bottom & top
        any_edges = bottom | top
        border_signal = bool(any_edges)
        column_change = 1.0 - column_similarity
        style_change = 1.0 - style_similarity

        # Keep adjacent rows, one-blank-row gaps, and meaningful structural transitions.
        if not (
            gap <= 1
            or column_change >= 0.25
            or style_change >= 0.40
            or border_signal
        ):
            continue

        strength = (
            2.0 * column_change
            + 1.5 * style_change
            + (1.5 if matched_edges else 0.75 if border_signal else 0.0)
            + (0.5 if gap == 1 else 0.0)
        )
        transitions.append((
            strength, previous_row, current_row, gap, column_similarity,
            style_similarity, matched_edges, any_edges,
        ))

    transitions.sort(key=lambda item: (-item[0], item[1], item[2]))
    print(f"- Populated rows: {len(rows)}")
    print(f"- Reported transitions: {min(limit, len(transitions))} of {len(transitions)}")
    print("| Previous → current | Gap | Previous row (cols; text/num; bold/fill) | Current row (cols; text/num; bold/fill) | Col Jaccard | Style Jaccard | Shared bottom/top border cols | Border positions |")
    print("|---:|---:|---|---|---:|---:|---|---|")
    for item in transitions[:limit]:
        strength, previous_row, current_row, gap, col_sim, style_sim, matched, any_edges = item
        previous = profiles[previous_row]
        current = profiles[current_row]
        previous_summary = (
            f"{_ranges(previous['columns'])}; {previous['text']}/{previous['numeric']}; "
            f"{previous['bold']}/{previous['filled']}"
        )
        current_summary = (
            f"{_ranges(current['columns'])}; {current['text']}/{current['numeric']}; "
            f"{current['bold']}/{current['filled']}"
        )
        border_positions = "; ".join(
            previous["border_tokens"] + current["border_tokens"]
        ) or "—"
        print(
            f"| {previous_row} → {current_row} | {gap} | {previous_summary} "
            f"| {current_summary} | {col_sim:.2f} | {style_sim:.2f} "
            f"| {_ranges(matched)} | {border_positions} |"
        )

    print("\n#### Strongest row style profiles")
    for row_index in rows:
        profile = profiles[row_index]
        if profile["bold"] or profile["filled"] or profile["border_tokens"]:
            styles = ", ".join(
                f"{style}:{count}" for style, count in sorted(profile["style_counts"].items())
            ) or "—"
            borders = "; ".join(profile["border_tokens"]) or "—"
            print(
                f"- Row {row_index}: styles={styles}; bold={profile['bold']}; "
                f"filled={profile['filled']}; borders={borders}"
            )


def _audit_workbook(path: Path, limit: int) -> None:
    print(f"\n## {path.as_posix()}")
    try:
        observation = read_excel_file(path)
    except Exception as exc:
        print(f"- Reader error: {type(exc).__name__}: {exc}")
        return
    print(f"- Reader: ACCEPTED")
    print(f"- SHA-256: {observation.source.sha256}")
    print(f"- Observed cells: {len(observation.cells)}")
    for sheet in observation.worksheets:
        _audit_sheet(observation, sheet.ordinal, limit)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Excel row-boundary formatting evidence; no table splitting is performed."
    )
    parser.add_argument("workbooks", nargs="+", type=Path)
    parser.add_argument("--limit-per-sheet", type=int, default=80)
    args = parser.parse_args()
    if args.limit_per_sheet < 1:
        parser.error("--limit-per-sheet must be positive")
    for path in args.workbooks:
        if not path.is_file():
            print(f"\n## {path.as_posix()}\n- File not found.")
            continue
        _audit_workbook(path, args.limit_per_sheet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
