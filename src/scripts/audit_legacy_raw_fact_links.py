"""Read-only row-linkage audit for legacy raw_financial_facts.

Run from repository root:
    python src/scripts/audit_legacy_raw_fact_links.py

Reads tehran_stock.db in SQLite read-only mode and writes reply.md.
No schema or data is modified.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "tehran_stock.db"
REPORT_PATH = ROOT / "reply.md"

REFERENCES = (
    ("mapping_decisions", "raw_fact_id"),
    ("normalized_financial_fact_inputs", "raw_fact_id"),
    ("normalized_financial_facts", "raw_fact_id"),
)


def table_exists(connection: sqlite3.Connection, table: str) -> bool:
    return connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    ).fetchone() is not None


def columns_for(connection: sqlite3.Connection, table: str) -> set[str]:
    return {
        row[1]
        for row in connection.execute(f'PRAGMA table_info("{table}")').fetchall()
    }


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH.resolve().as_uri() + "?mode=ro", uri=True)
    lines = [
        "# Legacy RawFinancialFact Row-Linkage Audit",
        "",
        f"- Database: `{DB_PATH}`",
        "- Mode: read-only",
        "",
    ]

    try:
        if not table_exists(connection, "raw_financial_facts"):
            raise SystemExit("Table raw_financial_facts does not exist.")

        total = connection.execute(
            "SELECT COUNT(*) FROM raw_financial_facts"
        ).fetchone()[0]
        lines.extend([
            "## 1. Raw fact population",
            "",
            f"- Total raw facts: **{total}**",
            "",
            "## 2. Downstream references",
            "",
            "| Referencing table | Exists | Rows | Non-null raw_fact_id | Distinct raw facts referenced |",
            "|---|---:|---:|---:|---:|",
        ])

        reference_sets: dict[str, set[int]] = {}
        for table, column in REFERENCES:
            if not table_exists(connection, table):
                lines.append(f"| `{table}` | No | — | — | — |")
                reference_sets[table] = set()
                continue
            columns = columns_for(connection, table)
            if column not in columns:
                lines.append(f"| `{table}` | Yes | — | Missing column | — |")
                reference_sets[table] = set()
                continue
            qtable = f'"{table}"'
            qcolumn = f'"{column}"'
            row_count = connection.execute(
                f"SELECT COUNT(*) FROM {qtable}"
            ).fetchone()[0]
            non_null = connection.execute(
                f"SELECT COUNT(*) FROM {qtable} WHERE {qcolumn} IS NOT NULL"
            ).fetchone()[0]
            ids = {
                row[0]
                for row in connection.execute(
                    f"SELECT DISTINCT {qcolumn} FROM {qtable} "
                    f"WHERE {qcolumn} IS NOT NULL"
                ).fetchall()
            }
            reference_sets[table] = ids
            lines.append(
                f"| `{table}` | Yes | {row_count} | {non_null} | {len(ids)} |"
            )

        lines.extend(["", "## 3. Per-raw-fact linkage distribution", ""])
        for table, column in REFERENCES:
            if not table_exists(connection, table) or column not in columns_for(connection, table):
                continue
            qtable = f'"{table}"'
            qcolumn = f'"{column}"'
            lines.extend([f"### `{table}`", ""])
            distribution = connection.execute(
                f"SELECT link_count, COUNT(*) FROM ("
                f"SELECT r.raw_fact_id, COUNT(t.{qcolumn}) AS link_count "
                f"FROM raw_financial_facts r "
                f"LEFT JOIN {qtable} t ON t.{qcolumn}=r.raw_fact_id "
                f"GROUP BY r.raw_fact_id"
                f") GROUP BY link_count ORDER BY link_count"
            ).fetchall()
            lines.append("| Number of referencing rows per raw fact | Raw facts |")
            lines.append("|---:|---:|")
            for link_count, fact_count in distribution:
                lines.append(f"| {link_count} | {fact_count} |")
            lines.append("")

            orphan_count = connection.execute(
                f"SELECT COUNT(*) FROM {qtable} t "
                f"LEFT JOIN raw_financial_facts r ON r.raw_fact_id=t.{qcolumn} "
                f"WHERE t.{qcolumn} IS NOT NULL AND r.raw_fact_id IS NULL"
            ).fetchone()[0]
            lines.append(f"- Dangling non-NULL references: **{orphan_count}**")
            lines.append("")

        lines.extend(["## 4. Combined linkage across all three tables", ""])
        union_parts = []
        for table, column in REFERENCES:
            if table_exists(connection, table) and column in columns_for(connection, table):
                union_parts.append(
                    f'SELECT "{column}" AS raw_fact_id FROM "{table}" '
                    f'WHERE "{column}" IS NOT NULL'
                )
        if union_parts:
            union_sql = " UNION ALL ".join(union_parts)
            distribution = connection.execute(
                "SELECT link_count, COUNT(*) FROM ("
                "SELECT r.raw_fact_id, COUNT(u.raw_fact_id) AS link_count "
                "FROM raw_financial_facts r "
                f"LEFT JOIN ({union_sql}) u ON u.raw_fact_id=r.raw_fact_id "
                "GROUP BY r.raw_fact_id"
                ") GROUP BY link_count ORDER BY link_count"
            ).fetchall()
            lines.extend([
                "| Total references across all three tables per raw fact | Raw facts |",
                "|---:|---:|",
            ])
            for link_count, fact_count in distribution:
                lines.append(f"| {link_count} | {fact_count} |")
        else:
            lines.append("- No downstream reference tables with usable raw_fact_id columns.")
        lines.append("")

        lines.extend([
            "## 5. Interpretation limits",
            "",
            "- A reference count measures relational linkage, not semantic correctness or whether the referenced record is still needed.",
            "- A raw fact with zero references is not automatically safe to delete.",
            "- A normalized fact with a raw_fact_id may also have other provenance through normalized_financial_fact_inputs and mapping_decisions.",
            "- No rows were changed, deleted, updated, or migrated.",
            "",
        ])
    finally:
        connection.close()

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Audit completed. Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
