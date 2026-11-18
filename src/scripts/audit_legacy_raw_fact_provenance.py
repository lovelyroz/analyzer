"""Read-only audit of legacy RawFinancialFact provenance in the local SQLite DB.

Run from the repository root:
    python src/scripts/audit_legacy_raw_fact_provenance.py

Writes a Markdown report to reply.md. The database is opened read-only.
No database rows or schema are modified.
"""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "tehran_stock.db"
REPORT_PATH = ROOT / "reply.md"
FIELDS = (
    "source_sheet",
    "source_column_header",
    "source_section",
    "source_row",
    "source_column",
)


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")

    uri = DB_PATH.resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    lines: list[str] = [
        "# Legacy RawFinancialFact Provenance Audit",
        "",
        f"- Database: `{DB_PATH}`",
        "- Mode: read-only",
        "",
    ]

    try:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        if "raw_financial_facts" not in tables:
            raise SystemExit("Table raw_financial_facts does not exist.")

        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(raw_financial_facts)"
            )
        }
        total = connection.execute(
            "SELECT COUNT(*) FROM raw_financial_facts"
        ).fetchone()[0]
        lines.extend([
            "## 1. Raw fact population",
            "",
            f"- Total raw_financial_facts rows: **{total}**",
            "",
            "## 2. Provenance field population",
            "",
            "| Field | Exists | Non-null | Distinct non-null |",
            "|---|---:|---:|---:|",
        ])

        for field in FIELDS:
            if field not in columns:
                lines.append(f"| `{field}` | No | — | — |")
                continue
            qfield = quote_identifier(field)
            non_null = connection.execute(
                f"SELECT COUNT(*) FROM raw_financial_facts WHERE {qfield} IS NOT NULL"
            ).fetchone()[0]
            distinct = connection.execute(
                f"SELECT COUNT(DISTINCT {qfield}) FROM raw_financial_facts "
                f"WHERE {qfield} IS NOT NULL"
            ).fetchone()[0]
            lines.append(f"| `{field}` | Yes | {non_null} | {distinct} |")

        lines.extend(["", "## 3. Distinct-value samples", ""])
        for field in FIELDS:
            if field not in columns:
                continue
            qfield = quote_identifier(field)
            values = connection.execute(
                f"SELECT DISTINCT {qfield} AS value FROM raw_financial_facts "
                f"WHERE {qfield} IS NOT NULL ORDER BY {qfield} LIMIT 30"
            ).fetchall()
            lines.extend([f"### `{field}`", ""])
            if not values:
                lines.append("- No non-null values.")
            else:
                for row in values:
                    value = str(row["value"]).replace("\n", " ")
                    lines.append(f"- `{value}`")
            lines.append("")

        lines.extend(["## 4. Foreign-key references to raw_financial_facts", ""])
        references = []
        for table in sorted(tables):
            try:
                fk_rows = connection.execute(
                    f"PRAGMA foreign_key_list({quote_identifier(table)})"
                ).fetchall()
            except sqlite3.DatabaseError:
                continue
            for fk in fk_rows:
                if fk["table"] == "raw_financial_facts":
                    references.append(
                        (table, fk["from"], fk["to"], fk["on_delete"])
                    )
        if references:
            lines.extend([
                "| Referencing table | Column | Target | ON DELETE |",
                "|---|---|---|---|",
            ])
            for table, source, target, on_delete in references:
                lines.append(
                    f"| `{table}` | `{source}` | `{target}` | `{on_delete}` |"
                )
        else:
            lines.append("- No foreign-key references found.")
        lines.append("")

        lines.extend(["## 5. Application source references", ""])
        patterns = {
            field: re.compile(rf"\b{re.escape(field)}\b")
            for field in FIELDS
        }
        matches = {field: [] for field in FIELDS}
        src_root = ROOT / "src"
        for path in src_root.rglob("*.py"):
            if "scripts" in path.parts:
                continue
            try:
                source = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for field, pattern in patterns.items():
                for line_no, line in enumerate(source.splitlines(), 1):
                    if pattern.search(line):
                        matches[field].append((path.relative_to(ROOT), line_no, line.strip()))

        for field in FIELDS:
            lines.append(f"### `{field}`")
            lines.append("")
            if not matches[field]:
                lines.append("- No references found under `src` outside `src/scripts`.")
            else:
                for path, line_no, snippet in matches[field][:40]:
                    snippet = snippet.replace("|", "\\|")
                    lines.append(f"- `{path}:{line_no}`: `{snippet}`")
            lines.append("")

        lines.extend([
            "## 6. Interpretation boundary",
            "",
            "- This report measures legacy data population and source references only.",
            "- It does not decide which fields belong in the future canonical schema.",
            "- Do not drop or rewrite any field based on this report alone.",
            "- Migration 9 source/revision reconciliation remains a separate issue.",
            "",
        ])
    finally:
        connection.close()

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Audit completed. Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
