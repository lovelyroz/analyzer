# DB-TEST-002-CORRECTION — Stage 6 fixture alignment

Status: `OWNER_ACCEPTED`; Task DB-TEST-002 remains PARTIAL

## Cause

The prior owner-run command initially recorded 42 failures and 125 passes. After this correction, the owner reran the exact command and reported `167 passed in 55.40s`. This is acceptance evidence for the corrected Stage 6 suites; DB-TEST-002 remains PARTIAL because production integration and physical persistence limitations remain. All 42 failures in the three Stage 6 suites shared the same setup error: test helper `_record()` supplied `forecast_id` and `forecast_version` to `ForecastRecord`, whose runtime dataclass does not define either field. The current contract uses natural forecast fields; database identity and version assignment are not part of `ForecastRecord`.

## Changes

- `src/tests/test_stage6_p25_selection.py`: removed both unsupported fixture fields. Replaced the database-ID key test with a contract test showing that EvaluationKey changes when any of its forecast identity fields change, while changing forecast output revenue does not change identity.
- `src/tests/test_stage6_p25_adversarial.py`: removed both unsupported fixture fields. The conflicting-duplicate case now uses two records with the same contract identity and different revenue values, retaining the fail-closed quarantine assertion.
- `src/tests/test_stage6_evaluation_foundation.py`: removed both unsupported fixture fields.

Three fixture helpers were corrected and two existing test cases were updated to preserve meaningful coverage. The three files retain their 55 test function definitions (13, 18, and 24 respectively); no tests were deleted or skipped. Existing PIT, actual selection, scenario, horizon, model version, quality, and quarantine assertions remain in place.

No production code, schema, ORM, migration, or database files were changed.

## Verification and owner command

Tests were not run by this agent, as required by `PROMPT.md`. Static verification confirmed that all three files parse, no `ForecastRecord` fixture or override passes `forecast_id` or `forecast_version`, and `git diff --check` is clean.

Owner command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_codal_retire_001_20261121 src/tests/test_codal_extraction.py src/tests/test_codal_digit_normalization.py src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py src/tests/test_excel_source_reader.py src/tests/test_excel_observation_dto.py src/tests/test_canonical_ingestion_admission.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_stage6_p25_selection.py src/tests/test_stage6_p25_adversarial.py src/tests/test_stage6_evaluation_foundation.py
```

Owner acceptance: the owner executed the command above and reported `167 passed in 55.40s`. The corrected suites are accepted. DB-TEST-002 is not fully DONE while the broader integration and production persistence limitations remain.