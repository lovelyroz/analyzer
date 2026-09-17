"""CODAL raw-line validation before persistence."""

from __future__ import annotations

from typing import List, Sequence

from src.ingestion.service import RawLineInput


def validate_raw_lines(raw_lines: Sequence[RawLineInput]) -> List[str]:
    """Return a list of validation error messages (empty if OK)."""
    errors: List[str] = []
    for idx, line in enumerate(raw_lines):
        if not line.item_name or not str(line.item_name).strip():
            errors.append(f"line {idx}: item_name is required")
    return errors
