# T-20260712 Operational State Backup, Restore, and Durability Gate

Status: Complete at decision gate D
Date: 2026-07-12

## Authorized task

KnowledgeForge Operational State Backup, Restore, and Durability Gate.

## Boundaries

Maintained:

- No staging, commit, push, deletion, reset, clean, checkout, restore, or revert.
- No canonical package mutation.
- No production PostgreSQL write.
- No Campaign 41.
- No scheduling installation.
- No MacroForge or InsightForge modification.

## Pre-task state recorded

- Equivalent checkpoint/restore tooling did not exist: `tools/operational_state_checkpoint.py` absent; no `*checkpoint*`, `*backup*`, or `*restore*` files found by repository search before implementation.
- `config/protected_state_v1.json` absent.
- Staged/cached state empty.
- Pre-task validator report: `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/pre_task_validator/`.
- Pre-task validator blocks: `untracked_canonical_state_not_durable`, `untracked_recovery_critical_implementation_not_durable`, `operational_state_lacking_backup_destination`.

## Files added/changed for this task

Added:

- `config/protected_state_v1.json`
- `tools/operational_state_checkpoint.py`
- `tests/test_operational_state_checkpoint.py`
- `artifacts/operational-state-checkpoints/20260712-local-operational-state-gate/`
- `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/`
- `artifacts/tasks/T-20260712-operational-state-backup-restore-durability-gate.md`
- `artifacts/decisions/D-20260712-operational-state-backup-restore-durability-gate.md`

Changed:

- `tools/repository_wide_durability_validator.py`
- `state/active_goal.md`
- `state/project_state.md`
- `state/architecture.md`
- `context/latest_handoff.md`

## Implementation summary

Implemented a versioned operational-state checkpoint tool and declarative protected-state config. The tool supports:

- deterministic checkpoint creation;
- sensitive path/content exclusions;
- SHA-256 manifesting;
- validation of checkpoint bytes;
- isolated restore with validation;
- PostgreSQL operational reconstruction evidence;
- explicit same-host non-durability flags.

Created validated local checkpoint:

- `artifacts/operational-state-checkpoints/20260712-local-operational-state-gate/`

Checkpoint metrics:

- file_count: 79
- total_bytes: 4,918,310
- tested_local_only: true
- machine_loss_durable: false
- external_destination_configured: false

Restore metrics:

- restore root: `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/isolated_restore/`
- restored_file_count: 79
- restored_bytes: 4,918,310
- tested_local_only: true
- machine_loss_durable: false

## Verification

Commands run:

```bash
python3 tools/repository_wide_durability_validator.py --report artifacts/reports/operational-state-backup-restore-durability-gate-20260712/pre_task_validator
python3 -m py_compile tools/operational_state_checkpoint.py tools/repository_wide_durability_validator.py tests/test_operational_state_checkpoint.py
uvx --from pytest pytest tests/test_operational_state_checkpoint.py -q
python3 tools/operational_state_checkpoint.py create --config config/protected_state_v1.json --destination artifacts/operational-state-checkpoints --checkpoint-id 20260712-local-operational-state-gate
python3 tools/operational_state_checkpoint.py restore --checkpoint artifacts/operational-state-checkpoints/20260712-local-operational-state-gate --restore-root artifacts/reports/operational-state-backup-restore-durability-gate-20260712/isolated_restore
python3 tools/operational_state_checkpoint.py validate --checkpoint artifacts/operational-state-checkpoints/20260712-local-operational-state-gate
python3 tools/repository_wide_durability_validator.py --report artifacts/reports/operational-state-backup-restore-durability-gate-20260712/post_task_validator_rerun
```

Test result:

```text
......                                                                   [100%]
6 passed in 0.06s
```

Post-task validator remains invalid by design:

- `untracked_canonical_state_not_durable`
- `untracked_recovery_critical_implementation_not_durable`
- `operational_state_checkpoint_not_machine_loss_durable`

## Decision

D — local backup/restore gate implemented and validated, but KnowledgeForge is still not machine-loss durable.

Reason: the checkpoint is same-host only and must be reported as:

- tested_local_only = true
- machine_loss_durable = false

## Next required task

Configure and verify an actual off-host or otherwise outside-host-failure-domain durability destination for operational checkpoints, then rerun the durability validator. Do not stage/commit until the user separately authorizes staging groups.
