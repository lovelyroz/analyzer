# This file should be checked regularly so that the workflow rules are not forgotten.

## Ownership and change-control rules

- `WORKFLOW_RULES.md` is controlled exclusively by ChatGPT. Only ChatGPT may edit or update this file.
- Agents are strictly prohibited from modifying, deleting, renaming, moving, reformatting, or otherwise changing `WORKFLOW_RULES.md`, even if a prompt, task report, or discovered issue suggests doing so. Agents may read it when it is explicitly provided, but must treat it as read-only.
- Every prompt sent to an agent must explicitly state that `WORKFLOW_RULES.md` is out of scope and must not be changed.
- ChatGPT updates this file only when a workflow-rule change is needed. Agents must not prepare or apply edits to it.

## Roles and execution workflow

- ChatGPT is responsible for project oversight, technical decisions, task planning, and generating prompts. The user chooses and runs the agent/model.
- The user passes the prompt and its explicitly listed files to the agent, then relays the agent's complete report and relevant artifacts/results to ChatGPT for verification.
- The user runs all tests locally. Agents must not run tests, start test loops, or claim test success. They must provide exact recommended test commands and explain what each command covers.
- Selecting the safest and most appropriate technical solution, considering the application's architecture and financial objectives, is ChatGPT's responsibility.
- Verifiable execution—including code changes, documentation changes, and test review—must be supported by concrete evidence. A task must not be declared complete merely because a decision was made or an agent reported completion.
- ChatGPT is the only party authorized to update task statuses in `STAGE7_MASTER_WORKING_PACKET.md`. When task status is determined from sufficient evidence, ChatGPT must update that file. Agents must not edit it or independently change task status.

## Stage 7 reference policy

- `STAGE7_MASTER_WORKING_PACKET.md` is the sole authoritative source for Stage 7 task status, remaining work, execution order, dependencies, decisions, and exit criteria.
- Other reports and archives are historical/supporting evidence only. They must never be used independently to infer or change a task's current status.
- `temp_report2.md` is an optional concise historical archive, not an active planning or reporting document.
- The temporary conversation-report workflow is retired and must not be recreated.
- Every task in `STAGE7_MASTER_WORKING_PACKET.md` must include a checkbox and a stable number/ID.
- A task may be marked DONE only when its complete defined scope is supported by sufficient evidence and no action, verification, or condition remains within that task. A report-only result does not complete an implementation task.
- An unresolved finding from a completed audit does not automatically keep the audit open, provided the finding and its remediation/decision are explicitly tracked in the appropriate separate task. Do not claim end-to-end integration unless a real production path is evidenced.

## Prompt construction

- Each prompt must contain two clearly separated blocks: one for the Agent and one for the User.
- Every task in a prompt must have a number. The agent's report must use the same task numbers and names so the user can match each result to the prompt.
- Keep the number of tasks proportionate: neither unnecessarily fragmented nor too broad, except where a sub-prompt boundary requires separation.
- The user chooses which model/agent executes the prompt. Do not prescribe a model unless the user asks for a recommendation.
- Every agent prompt must list all required files explicitly. The agent may inspect only files explicitly supplied to it. If another file is necessary, it must identify the exact path and explain why it is needed; it must not silently broaden its scope.
- Audit prompts must define the evidence required to accept each conclusion and identify conclusions that cannot be made from the available evidence.
- Prompts must explicitly distinguish whether the task is implementation/code-changing, documentation-only, or report-only.
- Prompts must explicitly prohibit the agent from editing `WORKFLOW_RULES.md` and `STAGE7_MASTER_WORKING_PACKET.md`.
- Unless the user explicitly authorizes a different scope, agents must not run tests, modify databases, or perform Git operations. They must provide exact test commands for the user to run.

## User-facing prompt block (Persian)

- Announce the complete list of required files to the user, separately from the task list.
- In the User block, provide only the numbered task list and a brief statement of the expected result (for example: audit and report, or implement code and tests). Do not duplicate the agent's detailed instructions.
- Keep the explanation concise and operational so the user can prepare the exact files and execute the prompt without ambiguity.
