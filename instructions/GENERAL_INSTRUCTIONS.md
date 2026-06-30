# General Instructions

ProjectForge is a boring, explicit operating structure for agent-supported projects.
Agents must prefer readable files, explicit decisions, and reversible changes over clever hidden automation.

Mandatory discipline:
- Start with Priority 1 context only: `CONSTITUTION.md`, `state/active_goal.md`, `state/project_state.md`, `state/architecture.md`, and `context/latest_handoff.md` when present. Add Priority 2 active tasks/relevant decisions/folder summaries only when task-scoped relevance is clear; use broader docs/reports/history only as justified Priority 3 expansion.
- Treat `context/active_context.md` as a generated task bundle, not mandatory startup context. Do not read stale active context by default; rebuild it with `tools/build_context.py` only when explicit context bundling or cloud governance is needed.
- Use folder `_SUMMARY.md` files before exploring large documentation/source trees, and retrieve only target files after summaries are insufficient.
- Keep `state/active_goal.md`, `state/project_state.md`, and `state/architecture.md` concise and current; move history, long verification logs, and large file-change inventories to handoffs, reports, task artifacts, or derived logs.
- Include `Context used:` in every run report.
- Use dry-run/preflight according to `simulation/dry_run_policy.yaml`.
- Store durable choices and deferred specifications as decision artifacts.
- Run the Architecture-to-Reality Audit with `python3 tools/architecture_reality_audit.py --project . --write-report` every 5-10 completed tasks, before major architecture changes, and before major governance reviews. Record results under `artifacts/reports/`; remediate blocks with implementation, documentation, state, template, and decision-artifact updates as appropriate before continuing major governance work.
- Do not push to GitHub without human approval.
- Do not create specialized agents without requesting approval and explaining why.
- If capability fails, escalate through local review, stronger local model, Codex/premium model, then human.
- If permissions, secrets, money, destructive operations, or production data are involved, escalate to human directly.

MetaHarvest consultation:
- Required for architecture definition, major architecture modifications, new subsystems, new agent roles, memory/context design, orchestration design, permission design, workflow redesign, scheduled architecture reviews, repeated implementation failures, and user-requested improvement scans.
- Not required for bug fixes, minor documentation edits, test additions, small utilities, or implementation work that does not alter architecture.
- Record local relevance and outcomes under `architecture/architectureharvest/`; mirror broadly useful lessons back to the configured external MetaHarvest provider's `adoption_log/` when appropriate.
