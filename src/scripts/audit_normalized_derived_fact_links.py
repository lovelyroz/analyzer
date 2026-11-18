"""Read-only linkage audit for normalized and derived financial fact tables.

Run from repository root:
    python src/scripts/audit_normalized_derived_fact_links.py

Reads tehran_stock.db in SQLite read-only mode and writes reply.md.
No schema or database rows are modified.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "tehran_stock.db"
REPORT_PATH = ROOT / "reply.md"

TABLES = (
    "normalized_financial_facts",
    "normalized_financial_fact_inputs",
    "derived_financial_facts",
    "derived_financial_fact_inputs",
)

# source table/column -> target table/primary key
REFERENCES = (
    ("normalized_financial_facts", "raw_fact_id", "raw_financial_facts", "raw_fact_id"),
    ("normalized_financial_facts", "mapping_decision_id", "mapping_decisions", "mapping_decision_id"),
    ("normalized_financial_fact_inputs", "normalized_fact_id", "normalized_financial_facts", "fact_id"),
    ("normalized_financial_fact_inputs", "raw_fact_id", "raw_financial_facts", "raw_fact_id"),
    ("normalized_financial_fact_inputs", "mapping_decision_id", "mapping_decisions", "mapping_decision_id"),
    ("derived_financial_facts", "source_report_version_id", "report_versions", "report_version_id"),
    ("derived_financial_fact_inputs", "derived_fact_id", "derived_financial_facts", "derived_fact_id"),
    ("derived_financial_fact_inputs", "normalized_fact_id", "normalized_financial_facts", "fact_id"),
    ("derived_financial_fact_inputs", "derived_input_fact_id", "derived_financial_facts", "derived_fact_id"),
)

PRIMARY_KEYS = {
    "normalized_financial_facts": "fact_id",
    "normalized_financial_fact_inputs": "input_id",
    "derived_financial_facts": "derived_fact_id",
    "derived_financial_fact_inputs": "input_id",
}


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


def qname(identifier: str) -> str:
    """Quote a fixed identifier from this script's allowlisted constants."""
    return '"' + identifier.replace('"', '""') + '"'


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH.resolve().as_uri() + "?mode=ro", uri=True)
    lines = [
        "# Normalized / Derived FinancialFact Linkage Audit",
        "",
        f"- Database: `{DB_PATH}`",
        "- Mode: SQLite read-only",
        "- Scope: row counts, FK-like reference counts, per-parent linkage, dangling references and duplicate input links",
        "",
    ]

    try:
        lines.extend([
            "## 1. Table population",
            "",
            "| Table | Exists | Rows | Columns |",
            "|---|---:|---:|---:|",
        ])
        for table in TABLES:
            if not table_exists(connection, table):
                lines.append(f"| `{table}` | No | — | — |")
                continue
            columns = columns_for(connection, table)
            count = connection.execute(
                f"SELECT COUNT(*) FROM {qname(table)}"
            ).fetchone()[0]
            lines.append(f"| `{table}` | Yes | {count} | {len(columns)} |")

        lines.extend(["", "## 2. Reference inventory", ""])
        lines.extend([
            "| Source reference | Target | Source rows | Non-NULL | Distinct target IDs | Dangling |",
            "|---|---|---:|---:|---:|---:|",
        ])

        usable = []
        for source_table, source_column, target_table, target_pk in REFERENCES:
            if not table_exists(connection, source_table) or not table_exists(connection, target_table):
                lines.append(
                    f"| `{source_table}.{source_column}` | `{target_table}.{target_pk}` | — | — | — | TABLE MISSING |"
                )
                continue
            if source_column not in columns_for(connection, source_table) or target_pk not in columns_for(connection, target_table):
                lines.append(
                    f"| `{source_table}.{source_column}` | `{target_table}.{target_pk}` | — | — | — | COLUMN MISSING |"
                )
                continue

            qs, qc, qt, qpk = map(qname, (source_table, source_column, target_table, target_pk))
            total = connection.execute(f"SELECT COUNT(*) FROM {qs}").fetchone()[0]
            non_null = connection.execute(
                f"SELECT COUNT(*) FROM {qs} WHERE {qc} IS NOT NULL"
            ).fetchone()[0]
            distinct = connection.execute(
                f"SELECT COUNT(DISTINCT {qc}) FROM {qs} WHERE {qc} IS NOT NULL"
            ).fetchone()[0]
            dangling = connection.execute(
                f"SELECT COUNT(*) FROM {qs} s LEFT JOIN {qt} t ON t.{qpk}=s.{qc} "
                f"WHERE s.{qc} IS NOT NULL AND t.{qpk} IS NULL"
            ).fetchone()[0]
            usable.append((source_table, source_column, target_table, target_pk))
            lines.append(
                f"| `{source_table}.{source_column}` | `{target_table}.{target_pk}` | {total} | {non_null} | {distinct} | {dangling} |"
            )

        lines.extend(["", "## 3. Per-parent linkage distribution", ""])
        for source_table, source_column, target_table, target_pk in usable:
            qs, qc, qt, qpk = map(qname, (source_table, source_column, target_table, target_pk))
            distribution = connection.execute(
                f"SELECT link_count, COUNT(*) FROM ("
                f"SELECT t.{qpk}, COUNT(s.{qc}) AS link_count "
                f"FROM {qt} t LEFT JOIN {qs} s ON s.{qc}=t.{qpk} "
                f"GROUP BY t.{qpk}"
                f") GROUP BY link_count ORDER BY link_count"
            ).fetchall()
            lines.extend([
                f"### `{source_table}.{source_column}` → `{target_table}.{target_pk}`",
                "",
                "| References per target row | Target rows |",
                "|---:|---:|",
            ])
            for link_count, target_count in distribution:
                lines.append(f"| {link_count} | {target_count} |")
            if not distribution:
                lines.append("| — | 0 |")
            lines.append("")

        lines.extend(["## 4. Duplicate input-link groups", ""])
        duplicate_specs = (
            (
                "normalized_financial_fact_inputs",
                ("normalized_fact_id", "raw_fact_id", "mapping_decision_id"),
            ),
            (
                "derived_financial_fact_inputs",
                ("derived_fact_id", "normalized_fact_id", "derived_input_fact_id", "input_role"),
            ),
        )
        for table, columns in duplicate_specs:
            if not table_exists(connection, table):
                lines.append(f"- `{table}`: table missing")
                continue
            present = columns_for(connection, table)
            if not set(columns).issubset(present):
                lines.append(f"- `{table}`: required columns missing")
                continue
            grouped = ", ".join(qname(column) for column in columns)
            duplicate_groups = connection.execute(
                f"SELECT COUNT(*) FROM (SELECT {grouped}, COUNT(*) AS n "
                f"FROM {qname(table)} GROUP BY {grouped} HAVING COUNT(*) > 1)"
            ).fetchone()[0]
            lines.append(f"- `{table}`: duplicate key groups = **{duplicate_groups}**")

        lines.extend(["", "## 5. SQLite foreign-key integrity", ""])
        fk_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
        lines.append(f"- Rows returned by `PRAGMA foreign_key_check`: **{len(fk_errors)}**")
        if fk_errors:
            lines.append("")
            lines.append("| Table | Rowid | Parent table | FK index |")
            lines.append("|---|---:|---|---:|")
            for row in fk_errors[:100]:
                lines.append(f"| `{row[0]}` | {row[1]} | `{row[2]}` | {row[3]} |")
            if len(fk_errors) > 100:
                lines.append(f"| … | … | … | … |")
                lines.append(f"- Additional FK violations omitted: {len(fk_errors) - 100}")

        lines.extend([
            "",
            "## 6. Interpretation limits",
            "",
            "- This is a read-only snapshot of this exact database file; it does not prove the state of other environments, backups or external consumers.",
            "- Linkage counts do not prove semantic correctness or that a row is safe to delete.",
            "- A zero-row result does not authorize table, column or FK removal.",
            "- Missing tables/columns are reported explicitly; they are not interpreted as zero rows.",
            "- No database schema or row was changed.",
            "",
        ])
    finally:
        connection.close()

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Audit completed. Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
