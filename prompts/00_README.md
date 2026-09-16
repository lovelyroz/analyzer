# Analyzer V1 — Stage Execution Prompts

These are the clean, implementation-oriented prompts for the nine locked stages of Analyzer V1.

## Authority order

1. `00_a_Master_Architecture.md`
2. `01_Stage1_Data_Foundation.md` … `09_Stage9_Decision_Dashboard.md`
3. Approved contract amendments recorded in `99_Architecture_Change_Log.md`
4. Database architecture references `11_Database_Architecture_Stage1.md` and `12_Database_Architecture_V1.md`, plus approved database amendments
5. `10_Implementation_Status.md`
6. The corresponding prompt in this directory is the execution instruction, not a replacement for the locked specification.

The prompt files translate validated contracts into repeatable agent instructions. They must not introduce new requirements.

## Global execution rule

For every stage:

**Read → Inspect → Implement → Test → Audit → CI → Lock**

Do not redesign a locked stage because of an implementation defect. If a genuine contract or architecture contradiction is found, stop, document the exact contradiction, and use the project change-control process.

## Global invariants

- `NULL != 0`.
- Point-in-Time correctness is mandatory.
- Report versions and historical model versions remain reproducible.
- No silent substitution of missing data.
- No silent proxying between economically different data sources.
- No duplicate upstream calculations without explicit justification.
- No hidden score, bonus, vote, or signal.
- No double counting of correlated evidence.
- Every material output is traceable to its inputs and version.
- CI status must come from an actual relevant workflow run.

## Stage prompts

| Stage | Prompt |
|---|---|
| 1 | `01_Stage1_Implementation_Prompt.md` |
| 2 | `02_Stage2_Implementation_Prompt.md` |
| 3 | `03_Stage3_Implementation_Prompt.md` |
| 4 | `04_Stage4_Implementation_Prompt.md` |
| 5 | `05_Stage5_Implementation_Prompt.md` |
| 6 | `06_Stage6_Implementation_Prompt.md` |
| 7 | `07_Stage7_Implementation_Prompt.md` |
| 8 | `08_Stage8_Implementation_Prompt.md` |
| 9 | `09_Stage9_Implementation_Prompt.md` |

Use only the prompt corresponding to the stage being implemented or audited. Do not paste all nine prompts into an agent context when only one stage is required.

These prompts are intentionally concise. The locked stage specification and approved amendments remain the detailed source of truth.
