# CODAL, Market and FX File Ingestion — Production Status

## Supported file contract

All supported file inputs are Excel workbooks (`.xlsx`/`.xls` where a reader exists) or CSV. PDF is excluded from CODAL, market, FX, and future file-ingestion workflows unless the owner makes a separate explicit decision. There is no PDF acquisition, OCR, extraction, conversion, compatibility API, or dependency in the active application.

## Current architecture

- Excel workbooks are read through `src/ingestion/excel/reader.py`; `adapter.py`, deterministic template matching, observation DTOs, canonical input candidates, and admission build a validated non-executable plan.
- CSV market and FX inputs use their respective adapters and existing atomic persistence boundaries.
- `src/ingestion/service.py` retains shared CODAL `RawLineInput` persistence and the Report/ReportVersion/RawFinancialFact identity, replay, version history, audit, and provenance contracts. Parsing happens before this persistence boundary.
- No Excel-to-canonical ORM writer currently exists. Excel-to-canonical persistence, approved production mappings, and associated end-to-end acceptance remain open work. That gap does not create a supported PDF route.

## Boundaries

This status does not authorize changes to ORM models, schema, migrations, the real database, or legacy financial records. Existing legacy raw-fact persistence remains for compatibility and direct parsed-row callers; this task does not add an Excel writer or redefine canonical persistence.

## Validation

The owner runs the repository focused Excel/admission and retained CODAL persistence contract suites. The CODAL contract tests use synthetic `RawLineInput` DTOs and an isolated in-memory database; they do not test file parsing. See database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md for the retirement inventory, exact owner command, and acceptance status.
