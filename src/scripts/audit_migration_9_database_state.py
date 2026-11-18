from __future__ import annotations

import sqlite3
from pathlib import Path

from src.models.normalized import RawFinancialFact

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "tehran_stock.db"
OUTPUT = ROOT / "reply.md"


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def main() -> None:
    lines = [
        "# Migration 9 database state audit",
        "",
        "- Mode: strictly read-only SQLite connection (mode=ro).",
        "- No schema changes, data changes, or tests are performed.",
        f"- Database: {DB_PATH}",
        "",
    ]

    if not DB_PATH.is_file():
        lines += [
            "## Result",
            "",
            "Database file not found at the configured project-root path.",
            "No alternative database was searched for or opened.",
        ]
        OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Audit written to: {OUTPUT}")
        print("Database file not found; no database was opened.")
        return

    uri = DB_PATH.resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        lines += ["## Migration ledger", ""]
        if "schema_migrations" not in tables:
            lines.append("schema_migrations table is absent.")
        else:
            rows = connection.execute(
                "SELECT version, name, applied_at FROM schema_migrations "
                "WHERE version = 9"
            ).fetchall()
            if rows:
                for row in rows:
                    lines.append(
                        f"- version={row['version']}; name={row['name']}; "
                        f"applied_at={row['applied_at']}"
                    )
            else:
                lines.append("No version 9 row exists.")

        lines += ["", "## raw_financial_facts schema", ""]
        if "raw_financial_facts" not in tables:
            lines.append("raw_financial_facts table is absent.")
        else:
            table_sql = connection.execute(
                "SELECT sql FROM sqlite_master "
                "WHERE type='table' AND name='raw_financial_facts'"
            ).fetchone()
            lines += [
                "```sql",
                table_sql["sql"] if table_sql and table_sql["sql"] else "(SQL unavailable)",
                "```",
                "",
                "| cid | column | type | not_null | default | primary_key |",
                "|---:|---|---|---:|---|---:|",
            ]
            columns = connection.execute(
                "PRAGMA table_info(raw_financial_facts)"
            ).fetchall()
            db_column_names = {row["name"] for row in columns}
            for row in columns:
                lines.append(
                    f"| {row['cid']} | {row['name']} | {row['type']} | "
                    f"{row['notnull']} | {row['dflt_value']} | {row['pk']} |"
                )

            model_column_names = set(RawFinancialFact.__table__.columns.keys())
            extra_columns = sorted(db_column_names - model_column_names)
            missing_columns = sorted(model_column_names - db_column_names)
            lines += [
                "",
                "### ORM comparison",
                "",
                f"- Columns in database but not in current RawFinancialFact ORM model: "
                f"{', '.join(extra_columns) if extra_columns else '(none)'}",
                f"- Columns in current ORM model but absent from database: "
                f"{', '.join(missing_columns) if missing_columns else '(none)'}",
                "",
                "### Target-column population (counts only; no values exposed)",
                "",
            ]
            for column_name in ("source_sheet", "source_column_header"):
                if column_name not in db_column_names:
                    lines.append(f"- {column_name}: column absent")
                    continue
                qcol = quote_identifier(column_name)
                row = connection.execute(
                    f"SELECT COUNT(*) AS total, "
                    f"COUNT({qcol}) AS non_null, "
                    f"COUNT(DISTINCT {qcol}) AS distinct_non_null "
                    f"FROM raw_financial_facts"
                ).fetchone()
                lines.append(
                    f"- {column_name}: total_rows={row['total']}; "
                    f"non_null={row['non_null']}; "
                    f"distinct_non_null={row['distinct_non_null']}"
                )

            lines += ["", "### Indexes", ""]
            indexes = connection.execute(
                "PRAGMA index_list(raw_financial_facts)"
            ).fetchall()
            if not indexes:
                lines.append("(none)")
            for index in indexes:
                lines.append(
                    f"- {index['name']}; unique={index['unique']}; "
                    f"origin={index['origin']}; partial={index['partial']}"
                )

            lines += ["", "### Foreign keys", ""]
            foreign_keys = connection.execute(
                "PRAGMA foreign_key_list(raw_financial_facts)"
            ).fetchall()
            if not foreign_keys:
                lines.append("(none)")
            for fk in foreign_keys:
                lines.append(
                    f"- {fk['from']} -> {fk['table']}.{fk['to']}; "
                    f"on_update={fk['on_update']}; on_delete={fk['on_delete']}"
                )

            lines += ["", "### Triggers", ""]
            triggers = connection.execute(
                "SELECT name, sql FROM sqlite_master "
                "WHERE type='trigger' AND tbl_name='raw_financial_facts' "
                "ORDER BY name"
            ).fetchall()
            if not triggers:
                lines.append("(none)")
            for trigger in triggers:
                lines += [f"- {trigger['name']}", "```sql",
                          trigger["sql"] or "(SQL unavailable)", "```"]

        lines += [
            "",
            "## Scope limitation",
            "",
            "This audit reports the current ledger row and the current structure "
            "of raw_financial_facts. Because the original Migration 9 implementation "
            "is unavailable, this output cannot prove that every possible Migration 9 "
            "side effect has been identified.",
        ]
    finally:
        connection.close()

    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Database audit written to: {OUTPUT}")
    print("Read-only audit completed. No database changes or tests were performed.")


if __name__ == "__main__":
    main()
