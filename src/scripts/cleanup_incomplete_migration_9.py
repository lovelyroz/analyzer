from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "tehran_stock.db"
EXPECTED_MIGRATION_NAME = "codal_excel_source_metadata"
TARGET_COLUMNS = ("source_sheet", "source_column_header")


def inspect_state(connection: sqlite3.Connection) -> dict:
    migration = connection.execute(
        "SELECT version, name FROM schema_migrations WHERE version = 9"
    ).fetchone()
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(raw_financial_facts)")
    }
    indexes = connection.execute(
        "PRAGMA index_list(raw_financial_facts)"
    ).fetchall()
    triggers = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type='trigger' AND tbl_name='raw_financial_facts'"
    ).fetchall()
    counts = {}
    for column in TARGET_COLUMNS:
        if column in columns:
            quoted = '"' + column + '"'
            counts[column] = connection.execute(
                f"SELECT COUNT(*), COUNT({quoted}) FROM raw_financial_facts"
            ).fetchone()
    other_references = []
    for row in connection.execute(
        "SELECT type, name, sql FROM sqlite_master "
        "WHERE sql IS NOT NULL AND name <> 'raw_financial_facts'"
    ):
        sql = row[2].lower()
        if any(column.lower() in sql for column in TARGET_COLUMNS):
            other_references.append((row[0], row[1]))
    return {
        "migration": migration,
        "columns": columns,
        "indexes": indexes,
        "triggers": triggers,
        "counts": counts,
        "other_references": other_references,
        "max_version": connection.execute(
            "SELECT MAX(version) FROM schema_migrations"
        ).fetchone()[0],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safely remove the unimplemented Migration 9 residue."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create a SQLite backup and perform the destructive cleanup.",
    )
    args = parser.parse_args()

    if not DB_PATH.is_file():
        raise SystemExit(f"Database not found: {DB_PATH}")

    if args.apply:
        connection = sqlite3.connect(DB_PATH)
    else:
        connection = sqlite3.connect(DB_PATH.resolve().as_uri() + "?mode=ro", uri=True)

    try:
        connection.row_factory = sqlite3.Row
        version = connection.execute("SELECT sqlite_version()").fetchone()[0]
        state = inspect_state(connection)

        print(f"Database: {DB_PATH}")
        print(f"SQLite version: {version}")
        print(f"Migration 9 row: {tuple(state['migration']) if state['migration'] else None}")
        print(f"Maximum recorded migration: {state['max_version']}")
        for column in TARGET_COLUMNS:
            print(f"{column}: present={column in state['columns']}; "
                  f"counts={state['counts'].get(column)}")
        print(f"Indexes on raw_financial_facts: {len(state['indexes'])}")
        print(f"Triggers on raw_financial_facts: {len(state['triggers'])}")
        print(f"Other schema objects referencing target columns: "
              f"{state['other_references']}")

        if not args.apply:
            print("\nDRY RUN ONLY. No changes made.")
            print("Review this output, then rerun with --apply to make the backup and cleanup.")
            return

        if tuple(state["migration"] or ()) != (9, EXPECTED_MIGRATION_NAME):
            raise SystemExit("Safety stop: Migration 9 ledger row does not match the expected value.")
        if state["max_version"] != 9:
            raise SystemExit("Safety stop: migration 9 is not the highest recorded version.")
        if not set(TARGET_COLUMNS).issubset(state["columns"]):
            raise SystemExit("Safety stop: one or both expected columns are missing.")
        if state["indexes"] or state["triggers"]:
            raise SystemExit("Safety stop: indexes or triggers exist on raw_financial_facts.")
        if state["other_references"]:
            raise SystemExit("Safety stop: other schema objects reference the target columns.")
        if version < "3.35.0":
            raise SystemExit("Safety stop: SQLite version does not support DROP COLUMN.")

        backup_path = ROOT / (
            "tehran_stock_before_migration9_cleanup_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".db"
        )
        if backup_path.exists():
            raise SystemExit(f"Safety stop: backup path already exists: {backup_path}")

        backup = sqlite3.connect(backup_path)
        try:
            connection.backup(backup)
        finally:
            backup.close()
        print(f"Backup created: {backup_path}")

        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                'ALTER TABLE raw_financial_facts DROP COLUMN "source_column_header"'
            )
            connection.execute(
                'ALTER TABLE raw_financial_facts DROP COLUMN "source_sheet"'
            )
            connection.execute(
                "DELETE FROM schema_migrations WHERE version = 9 "
                "AND name = ?",
                (EXPECTED_MIGRATION_NAME,),
            )
            if connection.execute(
                "SELECT COUNT(*) FROM schema_migrations WHERE version = 9"
            ).fetchone()[0] != 0:
                raise RuntimeError("Migration 9 ledger row still exists.")
            remaining = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(raw_financial_facts)"
                )
            }
            if any(column in remaining for column in TARGET_COLUMNS):
                raise RuntimeError("One or more Migration 9 columns remain.")
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise RuntimeError(f"SQLite integrity_check failed: {integrity}")
            fk_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
            if fk_errors:
                raise RuntimeError(f"Foreign-key check failed: {fk_errors[:5]}")
            connection.commit()
        except Exception:
            connection.rollback()
            raise

        print("Cleanup completed.")
        print("Migration 9 ledger row and its two extra columns were removed.")
        print("The 505 raw financial fact rows were not deleted.")
        print("The backup preserves the pre-cleanup database, including removed column values.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
