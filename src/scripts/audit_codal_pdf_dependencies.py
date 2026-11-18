"""Read-only inventory of CODAL/PDF and legacy RawFinancialFact references.

Run from the repository root:
    python src/scripts/audit_codal_pdf_dependencies.py

Scans project text/source files only. It does not open the database, modify source
files, execute tests, or change project state other than writing reply.md.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "reply.md"
SELF = Path(__file__).resolve()

SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    "node_modules", "build", "dist",
}
TEXT_SUFFIXES = {
    ".py", ".pyi", ".toml", ".yaml", ".yml", ".json", ".ini",
    ".cfg", ".txt", ".ps1", ".bat", ".sh",
}
TERMS = [
    "RawFinancialFact",
    "raw_financial_facts",
    "RawLineInput",
    "ReportIngestionResult",
    "ingest_codal_report",
    "ingest_codal_pdf",
    "load_codal_pdf",
    "load_codal_pdf_from_url",
    "extract_raw_lines_from_pdf",
    "CodalExtractionResult",
    "CodalExtractionError",
    "CodalAcquisitionError",
    "acquire_local_pdf",
    "acquire_pdf_from_url",
    "acquire_codal_pdf",
    "parse_amount",
    "normalize_digits",
    "validate_raw_lines",
    "src.ingestion.codal",
]
PATTERN = re.compile("|".join(re.escape(term) for term in sorted(TERMS, key=len, reverse=True)))


def category(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("src/tests/") or "/tests/" in rel:
        return "TEST"
    if rel.startswith("src/scripts/") or "/scripts/" in rel:
        return "SCRIPT"
    if rel.startswith("src/"):
        return "PRODUCTION_SOURCE"
    return "ROOT_OR_CONFIG"


def main() -> None:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.resolve() in {SELF, OUTPUT.resolve()}:
            continue
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        files.append(path)

    files.sort(key=lambda p: p.relative_to(ROOT).as_posix().casefold())
    symbol_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    matched_files = 0
    sections: list[str] = []

    for path in files:
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError as exc:
            sections.append(f"### READ ERROR: {path.relative_to(ROOT)}\n{exc}")
            continue

        matches = []
        for line_number, line in enumerate(content.splitlines(), start=1):
            found = [match.group(0) for match in PATTERN.finditer(line)]
            if not found:
                continue
            for symbol in found:
                symbol_counts[symbol] += 1
            matches.append((line_number, line.rstrip()[:260], found))

        if not matches:
            continue

        matched_files += 1
        kind = category(path)
        category_counts[kind] += len(matches)
        rel = path.relative_to(ROOT).as_posix()
        rows = [f"### {rel} [{kind}]"]
        for line_number, line, found in matches:
            rows.append(
                f"- L{line_number} | symbols={', '.join(found)} | {line}"
            )
        sections.append("\n".join(rows))

    output = [
        "# CODAL/PDF dependency inventory",
        "",
        f"- Repository root: {ROOT}",
        f"- Text/source files scanned: {len(files)}",
        f"- Files with matches: {matched_files}",
        "- Database opened: NO",
        "- Source files changed: NO",
        "- Tests executed: NO",
        "",
        "## Match counts by category (matching lines)",
    ]
    for kind in ("PRODUCTION_SOURCE", "TEST", "SCRIPT", "ROOT_OR_CONFIG"):
        output.append(f"- {kind}: {category_counts[kind]}")
    output.extend(["", "## Match counts by symbol"])
    for symbol, count in sorted(symbol_counts.items()):
        output.append(f"- {symbol}: {count}")
    output.extend(["", "## File and line matches", ""])
    output.extend(sections or ["No matching references found."])

    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"Audit complete. Scanned {len(files)} text/source files.")
    print(f"Files with matches: {matched_files}")
    print(f"Report written to: {OUTPUT}")


if __name__ == "__main__":
    main()
