# Migration 9 local source reconciliation audit

- Mode: read-only; no database access or mutation; no tests run.
- Repository: D:\winprojects\analyzer

## Git identity

HEAD:
1e919d2ab33ee52379cf395dbe4f75936a1cb597

Branch:
master

## Working tree status

(clean)

## Changed-file summary



## Staged-file summary



## Migration 9 references in local Python source

### src/scripts/audit_migration_9_source.py

1: from __future__ import annotations
2: 
3: import subprocess
4: from pathlib import Path
5: 
6: ROOT = Path(__file__).resolve().parents[2]
7: OUTPUT = ROOT / "reply.md"
8: TOKENS = (
9:     "codal_excel_source_metadata",
10:     "Migration(9",
11:     "Migration(version=9",
12:     "version = 9",
13:     "version=9",
14: )
15: 
16: def git(*args: str) -> str:
17:     try:
18:         result = subprocess.run(
19:             ["git", *args],
20:             cwd=ROOT,
21:             capture_output=True,
22:             text=True,
23:             encoding="utf-8",
24:             errors="replace",
25:             check=False,
26:         )
27:         return (result.stdout or result.stderr).strip()
28:     except Exception as exc:
29:         return f"GIT COMMAND ERROR: {exc}"

30: 

31: def source_files() -> list[Path]:

32:     roots = [ROOT / "src", ROOT / "tests"]

33:     found: list[Path] = []

### src/tests/test_stage7_valuation.py

1423:         financial_context=context,
1424:         data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
1425:     )
1426: 
1427: 
1428: def test_p32_input_refs_before_cutoff_leave_results_unchanged():
1429:     import dataclasses
1430: 
1431:     engine = ValuationEngine()
1432:     plain = engine.calculate_valuation(**_p32_kwargs())
1433:     refs = [
1434:         _p32_ref(datetime(2025, 12, 1)),
1435:         _p32_ref(datetime(2025, 6, 15, tzinfo=timezone.utc), version=9),
1436:     ]
1437:     with_refs = engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=refs))
1438:     first = dataclasses.asdict(plain)
1439:     second = dataclasses.asdict(with_refs)
1440:     first.pop("calculation_timestamp")
1441:     second.pop("calculation_timestamp")
1442:     assert first == second
1443: 
1444: 
1445: def test_p32_input_ref_after_cutoff_rejected_on_valuation_path():
1446:     engine = ValuationEngine()
1447:     with pytest.raises(ValueError, match="after the"):
1448:         engine.calculate_valuation(
1449:             **_p32_kwargs(forecast_input_refs=[_p32_ref(datetime(2026, 3, 1))])
1450:         )
1451: 
1452: 
1453: def test_p32_input_ref_at_cutoff_boundary_accepted():
1454:     engine = ValuationEngine()
1455:     result = engine.calculate_valuation(


## Migration directory files

- __init__.py (136 bytes)
- runner.py (8722 bytes)
