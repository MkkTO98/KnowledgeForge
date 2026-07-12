# D-20260712 Operational State Backup, Restore, and Durability Gate

Date: 2026-07-12

## Decision

D — adopt a local operational-state checkpoint/restore mechanism as a validated recovery primitive, but do not treat it as machine-loss durability.

## Context

The prior durability-destination decision classified mutable operational registries, accepted source copies, outbox transport state, and PostgreSQL operational backups/reconstruction evidence as requiring operational backup/checkpointing before staging authorization could be considered.

Before this task, no equivalent checkpoint/restore implementation existed in KnowledgeForge.

## Adopted

KnowledgeForge now has:

- a versioned checkpoint contract: `knowledgeforge.operational_state_checkpoint.v1`;
- a declarative protected-state contract: `knowledgeforge.protected_state.v1`;
- deterministic file copying with SHA-256 manifesting;
- sensitive path/content exclusions;
- isolated restore and validation;
- PostgreSQL reconstruction evidence;
- validator semantics distinguishing local checkpoint coverage from machine-loss durability.

## Rejected

Rejected any claim that a same-host checkpoint is durable against machine loss.

A same-host checkpoint must be reported as:

- `tested_local_only = true`
- `machine_loss_durable = false`

## Deferred

Deferred until separately authorized:

- off-host backup destination configuration;
- immutable external artifact storage integration;
- remote Git durability/staging/commit/push;
- production PostgreSQL dump scheduling;
- scheduling/cron/systemd installation.

## Architectural justification

This preserves KnowledgeForge architecture because:

- canonical KnowledgeObjectPackage JSON remains file-backed canonical authority;
- ordinary Git remains the planned durability destination for canonical and A-class source/state artifacts;
- operational checkpointing is limited to mutable operational state;
- PostgreSQL remains a rebuildable projection, not canonical truth;
- the mechanism is generic over protected paths and does not depend on MacroForge or InsightForge runtime interfaces.

## Verification evidence

Primary report:

- `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/operational_state_backup_restore_report.md`

Validated checkpoint:

- `artifacts/operational-state-checkpoints/20260712-local-operational-state-gate/`

Post-task validator:

- `artifacts/reports/operational-state-backup-restore-durability-gate-20260712/post_task_validator_rerun/`

Post-task validator blocks:

- `untracked_canonical_state_not_durable`
- `untracked_recovery_critical_implementation_not_durable`
- `operational_state_checkpoint_not_machine_loss_durable`
