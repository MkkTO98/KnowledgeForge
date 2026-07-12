# KnowledgeForge Durability-Destination Decision and Pre-Staging Remediation Plan

Date: 2026-07-12

## Decision

B — durability policy is complete and sensitive/local-path review is clean, but operational backup/checkpointing destination still requires approval and implementation before the validator can pass.

The updated validator also still blocks because canonical and recovery-critical implementation files are local-only/untracked. Staging is not durable recovery and was not performed.

## Evidence checked

Reviewed prior consolidated report, final closeout addendum, inventory, commit plan, sensitive scan, and current git state. The prior staged-file count was not accepted blindly: current `git diff --cached --name-status` is empty, and the validator parser was corrected so untracked files are not counted as staged.

## Artifact-class destination policy

- accepted_source_copies: D operational backup/checkpointing
- canonical_knowledge_object_package_json: A ordinary Git
- correlation_batch_specifications: A ordinary Git
- current_state_registries: D operational backup/checkpointing
- derivation_registries: A ordinary Git when append-only canonical provenance; D operational backup/checkpointing when mutable operational registry
- large_raw_provider_responses: C immutable external artifact storage
- manifest_indexes_fingerprints_evolution_records: A ordinary Git
- method_and_calculation_contracts: A ordinary Git
- outbox_transport_state: D operational backup/checkpointing
- postgresql_projection_and_backups: E projection deterministically rebuildable from durable canonical inputs; D backups for operational recovery only
- release_exports_and_histories: A ordinary Git while small text/audit artifacts fit current repository scale; C immutable external artifact storage when measured size stops being reviewable in ordinary Git
- reports_logs_generated_context: E for generated context/caches; A for decision-bearing compact reports; C for large raw logs/report bundles
- seen_release_registries: D operational backup/checkpointing
- sensitive_local_configuration: F sensitive/local-only and excluded
- small_evidence_fixtures: A ordinary Git
- source_code_and_tests: A ordinary Git
- task_decision_doctrine_roadmap_architecture_state_handoff_records: A ordinary Git

## Ordinary Git vs Git LFS/external storage justification

Current measured canonical JSON is 4214206 bytes across 538 packages, average 7833.1 bytes/package. Current small evidence fixtures and source/specification material are text, reviewable, deterministic, and central to reconstruction. Therefore ordinary Git is the correct primary destination for canonical JSON, methods, source, tests, specifications, governance records, and small deterministic fixtures.

Git LFS or immutable external artifact storage is reserved for genuinely large raw provider responses, full release histories, large logs/report bundles, and future binary/heavy artifacts. Introducing external storage for the current small text canonical repository would add operational complexity without improving current recoverability.

## Sensitive/local-path review

Actual secret blockers: 0. Unsafe absolute-path dependencies after remediation: 0. Reviewed false positives/historical local-path references: 128. No secret values are reproduced in reports.

Remediated during this task:
- `tools/external_outbox_poller_v1.py`: expands env/user variables in `root_location`.
- `config/external_outbox_sources.json`: replaced host-specific root with `${EIP_PROJECTS_ROOT}/...`.
- `tests/test_external_outbox_polling_supersession_v1.py`: replaced hardcoded host path with env override plus sibling-project default.
- `tools/macroforge_neutral_release_adapter_v1.py`: removed host-specific absolute forbidden-term literals.
- `tools/knowledge_repository.py` and `knowledge_repository/manifest.json`: repository manifest records portable `knowledge_repository` root instead of a host absolute path.

Full ledger: `sensitive_local_path_findings_ledger.json`.

## Staged-state inventory

Current staged paths: 0. Current cached diff: empty. No staged snapshot differs from working tree because there is no staged snapshot.

This differs from the previous report because the old validator incorrectly treated `??` untracked paths as staged. The validator has been corrected.

## Remaining machine-loss exposure

Current validator inventory reports 3,710 recovery-critical/historical files / 49,659,033 bytes still not recoverable from current remote. This includes all local canonical package state until an authorized durability action is performed.

## Validator result

Valid: False. Blocks: untracked_canonical_state_not_durable, untracked_recovery_critical_implementation_not_durable, operational_state_lacking_backup_destination.

## Alignment check

The policy protects the 538 canonical objects, all 4 statistical-summary objects, all 13 Pearson objects, reusable calculation engines/contracts, release-driven recomputation, immutable supersession history, PostgreSQL reconstruction/retrieval, and future deterministic expansion toward correlations/covariance/lags/trends by keeping canonical packages, method contracts, source/tests, specifications, and compact evidence in ordinary Git while treating PostgreSQL as rebuildable projection only.

The plan is not acceptable if it preserves only governance artifacts: group 02 canonical repository plus groups 03/05/06/07/08/11/12 are mandatory because they preserve substantive knowledge and calculation capability.

## Path-group sequence

See `updated_dependency_aware_durability_plan.json` for exact pathspecs, counts, destinations, dependencies, status counts, and validations.

## Architecture/doctrine classification

Repository inconsistency: canonical/recovery-critical operational state remains local-only and not recoverable from remote.

Governance inconsistency: fixed by explicit artifact-class policy and dependency-aware plan; no Production Doctrine amendment required.

Tooling/environment issue: prior staged count was a validator parsing bug; current staged state is empty. Host absolute path literals were parameterized or made portable where they were active dependencies.

## Recommended next gate

Authorize the smallest next step: implement/approve an operational backup/checkpoint destination for mutable registries and operational PostgreSQL backup policy, then rerun the validator. Only after that should staging authorization be requested for ordinary-Git groups.
