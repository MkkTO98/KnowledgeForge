# Operational State Backup, Restore, and Durability Gate Report

Date: 2026-07-12

## Scope

Authorized task: KnowledgeForge Operational State Backup, Restore, and Durability Gate.

Hard boundaries observed:

- No staging, commit, push, delete, reset, clean, checkout, restore, or revert.
- No canonical package mutation.
- No production PostgreSQL write.
- No Campaign 41.
- No scheduling installation.
- No MacroForge or InsightForge modification.

## Pre-task state

Repository inspection before implementation found:

- Branch: `main`.
- Cached/staged diff: empty.
- `tools/operational_state_checkpoint.py`: absent.
- `config/protected_state_v1.json`: absent.
- Existing checkpoint/backup/restore files by name search: none found.
- Pre-task durability validator output: `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/pre_task_validator/`.
- Pre-task validator decision: D.
- Pre-task blocks:
  - `untracked_canonical_state_not_durable`
  - `untracked_recovery_critical_implementation_not_durable`
  - `operational_state_lacking_backup_destination`

## Implemented architecture

### Versioned backup/checkpoint contract

Implemented `tools/operational_state_checkpoint.py` with contract:

- `knowledgeforge.operational_state_checkpoint.v1`

The checkpoint manifest records:

- checkpoint id;
- source project;
- git head;
- protected-state config path and hash;
- protected-state contract version;
- copied file records with bytes and SHA-256;
- skipped sensitive/material exclusions;
- PostgreSQL reconstruction evidence;
- `tested_local_only = true`;
- `machine_loss_durable = false`;
- `external_destination_configured = false`.

### Declarative protected-state configuration

Added `config/protected_state_v1.json` with contract:

- `knowledgeforge.protected_state.v1`

Protected operational state includes:

- release inbox state;
- unified seen-release/current-state registries;
- accepted source copies from release handoffs;
- external outbox transport state;
- external outbox failure-recovery state;
- external release handoff copies.

Canonical KnowledgeObjectPackage files are intentionally excluded because ordinary Git is their durability destination. PostgreSQL projection contents are intentionally excluded because PostgreSQL is a rebuildable operational projection, not canonical authority.

### Generic deterministic checkpoint creation

Command executed:

```bash
python3 tools/operational_state_checkpoint.py create \
  --config config/protected_state_v1.json \
  --destination artifacts/operational-state-checkpoints \
  --checkpoint-id 20260712-local-operational-state-gate
```

Output captured at:

- `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/checkpoint_create_output.json`

Created checkpoint:

- `artifacts/operational-state-checkpoints/20260712-local-operational-state-gate/`

Checkpoint result:

- file_count: 79
- total_bytes: 4,918,310
- skipped_count: 0
- tested_local_only: true
- machine_loss_durable: false
- external_destination_configured: false

### Generic isolated restore and validation

Command executed:

```bash
python3 tools/operational_state_checkpoint.py restore \
  --checkpoint artifacts/operational-state-checkpoints/20260712-local-operational-state-gate \
  --restore-root artifacts/reports/operational-state-backup-restore-durability-gate-20260712/isolated_restore
```

Output captured at:

- `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/restore_output.json`

Restore result:

- valid: true
- restored_file_count: 79
- restored_bytes: 4,918,310
- tested_local_only: true
- machine_loss_durable: false

The restore was isolated under the report directory and did not overwrite production repository files.

### Sensitive-material exclusions

The protected-state config excludes:

- `.env` files;
- `workspace_config.yaml`;
- credential/secret/private-key paths;
- private-key content markers;
- PostgreSQL connection-string content.

Failure-mode tests verify both path-based and content-based exclusion.

### PostgreSQL operational backup or reconstruction evidence

No production PostgreSQL write or dump was performed.

The checkpoint records PostgreSQL reconstruction evidence instead:

- projection tool exists: true
- projection tool: `tools/postgresql_operational_projection.py`
- projection tool SHA-256: `1b5e2e1aedc92950d150588ffeddcbdb7bc648749ce4d270efe72090b6388599`
- projection config example exists: true
- projection config example SHA-256: `d40387e75ce3fadbdedcf5a185f017278c98fef948a85670b6b4f12890a380db`
- canonical manifest exists: true
- canonical manifest SHA-256: `57d1ad875829223c4c454cb6485bc2038e8542396d6d17c86975d6bc221e59ad`
- canonical package count: 538
- `psql_available`: true
- `pg_dump_available`: true
- production database write allowed: false
- backup dump destination configured: false
- tested_local_only: true
- machine_loss_durable: false

Interpretation: PostgreSQL is recoverable as a projection from durable canonical packages plus projection code/config, but this task did not configure or verify any destination outside the host failure domain.

## Updated durability-validator semantics

Updated `tools/repository_wide_durability_validator.py` so operational state is no longer a binary missing-backup check only.

The validator now reports:

- whether a valid local checkpoint exists;
- whether the checkpoint covers currently exposed operational-state paths;
- whether restore evidence is local-only;
- whether machine-loss durability is actually true or false;
- whether PostgreSQL reconstruction evidence is present.

Post-task validator output:

- `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/post_task_validator_rerun/`

Post-task validator result:

- valid: false
- blocks:
  - `untracked_canonical_state_not_durable`
  - `untracked_recovery_critical_implementation_not_durable`
  - `operational_state_checkpoint_not_machine_loss_durable`
- operational_state_without_backup_count: 69
- selected checkpoint covered operational-state count: 69
- missing operational-state coverage count: 0
- tested_local_only: true
- machine_loss_durable: false
- actual_secret_blockers: 0
- unsafe_absolute_path_dependencies: 0

The previous block `operational_state_lacking_backup_destination` was replaced by `operational_state_checkpoint_not_machine_loss_durable` after the local checkpoint was created and validated.

## Failure-mode tests

Added `tests/test_operational_state_checkpoint.py` covering:

1. create + validate + isolated restore succeeds;
2. sensitive path exclusions are not copied;
3. sensitive content exclusions are not copied;
4. missing checkpoint file fails validation;
5. tampered checkpoint file fails validation;
6. restore refuses invalid checkpoint;
7. required protected path missing fails closed.

Targeted test output:

```text
......                                                                   [100%]
6 passed in 0.06s
```

## Durability decision gate

Decision: D.

Justification:

- Local operational-state checkpoint creation works.
- Isolated restore works.
- PostgreSQL reconstruction evidence is recorded.
- Sensitive exclusion behavior is tested.
- The validator recognizes that operational state now has a valid local checkpoint covering current operational-state files.
- However, the checkpoint is same-host only:
  - `tested_local_only = true`
  - `machine_loss_durable = false`
- Canonical and recovery-critical implementation files remain untracked/local-only.
- No external artifact storage, remote Git commit/push, off-host backup, or database backup destination was configured or verified.

Therefore KnowledgeForge is not yet machine-loss durable and staging authorization should still wait.

## Compatibility analysis

Preserved architecture:

- File-backed Knowledge Repository remains canonical authority.
- PostgreSQL remains an operational projection.
- Canonical packages are not backed up through operational-state checkpointing and were not mutated.
- The checkpoint tool is generic over declarative protected paths and does not encode MacroForge-specific runtime dependencies.
- Same-host restore is explicitly labeled local-only and non-machine-loss-durable.

Known compatibility limitation:

- The local checkpoint directory itself is not outside the host failure domain. It is useful for isolated restore validation and as a future backup payload, but it is not sufficient for disaster recovery.

## Recommended next gate

Before staging or claiming durability, configure and verify an actual destination outside the host failure domain for either:

1. ordinary Git remote durability for A-class files plus an off-host operational checkpoint destination; or
2. an immutable external artifact/backup destination for operational checkpoints, with restore validation from that destination.

Only after that should the validator be allowed to remove `operational_state_checkpoint_not_machine_loss_durable`.
