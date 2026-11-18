# Migration 9 local source reconciliation audit

- Mode: read-only; no database access or mutation; no tests run.
- Repository: D:\winprojects\analyzer

## Git identity

HEAD:
e1828a1bb6d295cab645f71af6beea4ae6bd4d26

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

95:                     lines.append(f"{line_no + 1}: {source_lines[line_no]}")
96:                     emitted.add(line_no)
97:             lines.append("")
98:     if matched == 0:
99:         lines.append("No Migration 9 token found in local Python files under src/ or tests/.")
100: 
101:     lines.extend([
102:         "",
103:         "## Git history search across local refs",
104:         "",
105:         "### Commits adding/removing the exact Migration 9 identifier",
106:         "",
107:         git("log", "--all", "--format=%H%x09%ad%x09%s", "--date=iso-strict", "-S" + "codal_excel_source_metadata", "--", ".") or "(no matching commit found in local refs)",
108:         "",
109:         "### History of src/migrations/runner.py",
110:         "",
111:         git("log", "--all", "-30", "--format=%H%x09%ad%x09%s", "--date=iso-strict", "--", "src/migrations/runner.py") or "(no runner.py history found)",
112:         "",
113:         "### Local branches and tags",
114:         "",
115:         git("branch", "-a", "--no-color") or "(no branches listed)",
116:         git("tag", "--list") or "(no tags listed)",
117:         "",
118:         "## Migration directory files",
119:         "",
120:     ])
121:     migration_dir = ROOT / "src" / "migrations"
122:     if migration_dir.exists():
123:         for path in sorted(migration_dir.iterdir()):
124:             if path.is_file():
125:                 lines.append(f"- {path.name} ({path.stat().st_size} bytes)")
126:     else:
127:         lines.append("src/migrations directory not found.")

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


## Git history search across local refs

### Commits adding/removing the exact Migration 9 identifier

e1828a1bb6d295cab645f71af6beea4ae6bd4d26	2026-11-18T13:58:40+03:30	audit: extend Migration 9 check to local Git history
74bf3b8221a3841961e45ab1ec4ca6620a0952f3	2026-11-18T13:56:32+03:30	uiujskdfksdkfmmnvmxnvdk
1e919d2ab33ee52379cf395dbe4f75936a1cb597	2026-11-18T13:53:32+03:30	tools: add read-only Migration 9 source audit
03c3d3cf0637325b1874f71bb21c16ca37aa85e1	2026-11-18T11:28:06+03:30	reply
4a28f58b4a71118faccde9ac7d3a6eb2277ab80e	2026-11-18T00:55:35+03:30	reply
097452841d555f61c9cbddcd7f35df0190411384	2026-11-18T00:51:45+03:30	reply
2de04f411c6482cb6699556284cf615d45aedae5	2026-11-18T00:28:13+03:30	docs(database): record runtime migration source drift
8742704c0269e8d5ad14224500fb190b6e211cc9	2026-11-18T00:27:57+03:30	docs(database): record runtime SQLite migration reconciliation

### History of src/migrations/runner.py

5c0608e5e06dd6934c4fdb2196160ccfc39faa87	2026-11-01T14:05:26+03:30	S7P054–057 — Remove Forecast Output Persistence and Preserve Runtime Integration
84f9940933e481fffcedfc2d2647b4ec7f4301e9	2026-10-22T22:39:42+03:30	P45
1d6ae3e90fb90110ee4eb25b56b0479a7ff5437b	2026-10-19T14:33:29+03:30	Agent host session ce5b4e8d-41eb-4472-86b7-3e3c09155623 - baseline checkpoint
dc283e9a180f1321fffc23c2dde69c8a57ca0145	2026-10-01T20:22:07+03:30	prompt4_stage5
77abe3840c6976aa0aef77006603c1a08606cfa6	2026-09-17T11:32:48+03:30	fix: restore migration runner with version 6 fx_rates_jalali_components
9fb9541056a42dc29134c235dfef451ccca25410	2026-09-17T11:32:10+03:30	feat(fx): service ingest_fx_xlsx + migration 6 runner + tests
07dab699195b008a7e030a695a657b0de6b32b02	2026-09-17T09:51:32+03:30	fix: migration tests expect version 5; migration 5 skips if market_daily missing
99738b64273d460000e64a67ba7a9d9cd362f9ff	2026-09-17T09:43:53+03:30	feat(db): CHANGE-005 Jalali date components on market_daily (V1.2)
c8441fbf57dd1d56d7e65d001b62888d425e8c01	2026-09-17T00:30:55+03:30	Make report-version integrity migration fail safely
cc696522ed9847014c0b43b0277ba50c010771f5	2026-09-17T00:30:42+03:30	Add migration for single current report version invariant
249937f7946f326aa0b27534349ca7c724c28682	2026-09-17T00:28:13+03:30	Add migration for normalized multi-source provenance
e411464f7b2177450b909e507a82c3bdfff3daca	2026-09-17T00:16:38+03:30	Stage 1 Database Architecture V1

### Local branches and tags

* master
  stage7/remediation-2026-10-14
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
(no tags listed)

## Migration directory files

- __init__.py (136 bytes)
- runner.py (8722 bytes)
