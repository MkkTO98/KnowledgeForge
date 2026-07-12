# Repository-Wide Durability Inventory and Production Supersession-Code Correction

Date: 2026-07-11

## Decision

D — Canonical/recovery-critical state remains locally vulnerable.

Secondary blocker: sensitive/local-path findings require review before staging. Staging authorization is not requested.

## 1. Production supersession-code finding and correction

- Flawed reusable function: `tools/external_outbox_poller_v1.py::run_isolated_supersession_prototype`.
- Finding: the prior isolated prototype rewrote predecessor bytes by setting `confidence_quality.lifecycle_state` to `superseded`.
- Correction: `tools/external_outbox_poller_v1.py::run_isolated_supersession_prototype` now preserves predecessor bytes, appends a distinct successor package, writes external current-state registry entries, and appends supersession records.
- Additional production safeguard: `tools/knowledge_repository.py::persist_knowledge_object_packages` now refuses non-identical overwrite of an existing package id. This disables the general code path capable of lifecycle-state mutation inside existing package bytes.
- Remaining boundary: production canonical supersession is still not implemented; corrected code is tested without invoking production canonical releases.

## 2. Predecessor immutability proof

Regression tests prove:

- predecessor pre-hash equals post-hash;
- successor is distinct;
- supersession/current-state record exists outside predecessor bytes;
- current-state registry points to successor;
- history contains predecessor and successor;
- predecessor file is not opened for writing.

Verification command: `uvx --from pytest pytest tests/test_knowledge_repository.py tests/test_external_outbox_polling_supersession_v1.py tests/test_canonical_supersession_immutability_validator.py -q`.
Result: 14 passed.

## 3. Complete working-tree inventory

Status totals:

- canonical: 1083 files / 5855594 bytes
- ignored: 276 files / 6883541 bytes
- modified_tracked: 32 files / 173163 bytes
- recovery_critical: 3677 files / 46382539 bytes
- remote_tracked: 224 files / 496088 bytes
- sensitive_local: 1 files / 641 bytes
- staged: 322 files / 3458378 bytes
- tracked: 224 files / 496088 bytes
- untracked: 3922 files / 48094254 bytes

Category totals:

- derived_rebuildable: 140 files / 608859 bytes
- ephemeral_untracked: 269 files / 6880610 bytes
- historical_evidence_optional_main_git: 533 files / 13723010 bytes
- historical_evidence_or_external_storage: 335 files / 1601234 bytes
- must_track_git: 3103 files / 28240127 bytes
- operational_state_backup: 41 files / 4419402 bytes
- sensitive_ignored: 1 files / 641 bytes

Canonical repository counts:

- all canonical packages: 538
- Pearson objects: 13
- statistical-summary objects: 4
- Campaign 40 packages: 6
- manifest object count: 538
- actual package files: 538

Full file-level inventory with sizes and hashes: `inventory.json`.

Important staging caveat: `git status` currently reports 322 staged files / 3458378 bytes already present in the working tree state. I did not stage anything in this task and did not unstage anything because reset/checkout/revert/clean were forbidden.

## 4. Machine-loss recovery result

Assumption: machine disappears and only current remote Git repository remains.

Result: NOT recoverable.

Lost if machine disappears now:

- total lost recovery-critical/historical files: 3597
- total lost bytes: 46137234

Lost by category:

- historical_evidence_optional_main_git: 523 files / 13633681 bytes
- must_track_git: 3033 files / 28084151 bytes
- operational_state_backup: 41 files / 4419402 bytes

Capability recovery:

- all_13_pearson_objects: recoverable_from_remote=False; local_count=13
- all_538_canonical_packages: recoverable_from_remote=False; local_count=538
- all_four_statistical_summary_objects: recoverable_from_remote=False; local_count=4
- calculation_contracts_specs_methods: recoverable_from_remote=False
- campaign40_six_packages: recoverable_from_remote=False; local_count=6
- derivation_registry: recoverable_from_remote=False
- downstream_deltas: recoverable_from_remote=False
- evidence_fixtures: recoverable_from_remote=False
- external_handoff_evidence: recoverable_from_remote=False
- generic_batch_engine: recoverable_from_remote=False
- macroforge_adapter: recoverable_from_remote=False
- outbox_poller: recoverable_from_remote=False
- postgresql_projection: recoverable_from_remote=False
- relationship_export_contract: recoverable_from_remote=False
- release_inbox_seen_registry: recoverable_from_remote=False
- repository_manifest_and_fingerprint: recoverable_from_remote=False
- supersession_rules: recoverable_from_remote=False

Provider re-query is not counted as recovery; mutable provider responses are not equivalent to retained evidence.

## 5. Artifact durability policy

A. Must be tracked in Git:
- canonical JSON packages;
- repository manifest/indexes/evolution records;
- specifications;
- method contracts;
- small deterministic evidence fixtures;
- source code and tests;
- governance decisions/tasks/state/handoff;
- release registry schemas/configuration.

B. Must be stored in durable external artifact storage:
- large raw provider responses;
- large release exports;
- large verification logs;
- large historical report bundles;
- isolated DB dumps once too large for ordinary Git.

C. May be regenerated from tracked canonical inputs:
- derived indexes;
- PostgreSQL projections;
- relationship export payloads when packages and query contracts are tracked.

D. Operational state requiring backup/checkpointing:
- release seen registries;
- external outbox transport registry;
- accepted source copies;
- current-state registries;
- durability inventories before staging.

E. Ephemeral and should remain untracked:
- `__pycache__`, `.pytest_cache`, generated active context bundles, temporary isolated runtime state.

F. Sensitive and must remain ignored:
- `workspace_config.yaml`, `.env`, credentials, private keys, local connection files.

G. Historical evidence retained but not necessarily in main Git:
- large raw provider snapshots and full release histories after immutable external artifact storage exists.

## 6. Size and storage decision

Current measured sizes:

- canonical object bytes: 4214206
- average canonical package bytes: 7833.1
- evidence fixture bytes: 1575398

Growth projection:

| relationship objects | canonical JSON bytes | evidence fixture bytes | release-history rough bytes |
|---:|---:|---:|---:|
| 100 | 783309 | 292824 | 1614201 |
| 1000 | 7833096 | 2928249 | 16142018 |
| 10000 | 78330966 | 29282490 | 161420185 |
| 100000 | 783309665 | 292824907 | 1614201858 |


Decision: hybrid storage.

- Ordinary Git is suitable for canonical JSON packages, specifications, method contracts, source/tests, and small registries.
- Git LFS or immutable artifact storage is required for growing raw evidence fixtures, large release exports, and large logs/reports.
- PostgreSQL backups are useful for operations but PostgreSQL must not be treated as the canonical backup.

## 7. Sensitive-material result

- blocker findings: 0
- findings requiring review/redaction before staging: 63
- scan passes: False

No secret values are exposed in this report. Main current issue is local absolute-path and keyword false-positive review across proposed tracked categories, plus `workspace_config.yaml` remains local-only/sensitive ignored.

## 8. Repository-wide validator result

- valid: False
- blocks: untracked_canonical_files_block_durability, untracked_recovery_critical_files_block_durability, sensitive_or_local_path_findings_require_review
- missing manifest packages: 0
- extra package files: 0
- untracked canonical count: 1083
- untracked recovery-critical count: 3576
- PostgreSQL not sole backup: True

## 9. Complete commit sequence

See `commit_plan.json` for machine-readable pathspecs/counts/sensitive findings. Logical groups:

1. 01-foundational-doctrine-state-architecture — 68 files / 401737 bytes; modified tracked=24; untracked=44; canonical_data_included=False; depends_on=none; message=`KnowledgeForge: 01 foundational doctrine state architecture`.
2. 02-canonical-knowledge-repository — 1083 files / 5855594 bytes; modified tracked=0; untracked=1083; canonical_data_included=True; depends_on=['01-foundational-doctrine-state-architecture']; message=`KnowledgeForge: 02 canonical knowledge repository`.
3. 03-mature-wdi-production-evidence — 1629 files / 19029000 bytes; modified tracked=0; untracked=1629; canonical_data_included=False; depends_on=['02-canonical-knowledge-repository']; message=`KnowledgeForge: 03 mature wdi production evidence`.
4. 04-postgresql-projection — 6 files / 93869 bytes; modified tracked=0; untracked=6; canonical_data_included=False; depends_on=['03-mature-wdi-production-evidence']; message=`KnowledgeForge: 04 postgresql projection`.
5. 05-statistical-summary-methods-objects — 88 files / 415863 bytes; modified tracked=0; untracked=88; canonical_data_included=False; depends_on=['04-postgresql-projection']; message=`KnowledgeForge: 05 statistical summary methods objects`.
6. 06-pearson-correlation-method-objects — 192 files / 941428 bytes; modified tracked=0; untracked=192; canonical_data_included=False; depends_on=['05-statistical-summary-methods-objects']; message=`KnowledgeForge: 06 pearson correlation method objects`.
7. 07-specification-driven-batch-engine-campaign40 — 98 files / 1308168 bytes; modified tracked=0; untracked=98; canonical_data_included=False; depends_on=['06-pearson-correlation-method-objects']; message=`KnowledgeForge: 07 specification driven batch engine campaign40`.
8. 08-relationship-export-contract — 105 files / 2599209 bytes; modified tracked=1; untracked=104; canonical_data_included=False; depends_on=['07-specification-driven-batch-engine-campaign40']; message=`KnowledgeForge: 08 relationship export contract`.
9. 09-release-automation-inbox-registries — 35 files / 3579739 bytes; modified tracked=0; untracked=35; canonical_data_included=False; depends_on=['08-relationship-export-contract']; message=`KnowledgeForge: 09 release automation inbox registries`.
10. 10-macroforge-adapter-real-handoff-evidence — 70 files / 2195404 bytes; modified tracked=0; untracked=70; canonical_data_included=False; depends_on=['09-release-automation-inbox-registries']; message=`KnowledgeForge: 10 macroforge adapter real handoff evidence`.
11. 11-outbox-polling — 80 files / 2690319 bytes; modified tracked=0; untracked=80; canonical_data_included=False; depends_on=['10-macroforge-adapter-real-handoff-evidence']; message=`KnowledgeForge: 11 outbox polling`.
12. 12-corrected-supersession-model — 41 files / 237143 bytes; modified tracked=0; untracked=41; canonical_data_included=False; depends_on=['11-outbox-polling']; message=`KnowledgeForge: 12 corrected supersession model`.
13. 13-documentation-final-handoff-and-durability — 113 files / 3401002 bytes; modified tracked=3; untracked=110; canonical_data_included=False; depends_on=['12-corrected-supersession-model']; message=`KnowledgeForge: 13 documentation final handoff and durability`.

Unassigned changed/untracked files: 363. This blocks safe staging until classified.

## 10. Temporary isolated DB cleanup assessment

- database: `knowledgeforge_immutability_gate_20260711`
- exists: True
- isolated schema only: True
- production depends on it: False
- evidence dump present: True
- safe to remove later: True
- deletion authorization required: True

Recommendation: keep it for now. If cleanup is desired, request separate explicit authorization to drop `knowledgeforge_immutability_gate_20260711`.

## 11. Exact next authorization requested

No staging authorization is requested.

Smallest remediation requested: authorize a durability-destination decision for recovery-critical untracked material, including whether large raw evidence/release-history/report categories should use ordinary Git, Git LFS, or immutable external artifact storage. After that decision, run a focused sensitive/local-path remediation pass before any staging.

## 12. Doctrine/architecture classification

- Repository inconsistency: remote Git does not contain the canonical/recovery-critical operational system now present locally.
- Governance inconsistency: previous staging grouping covered only the latest immutability task and not the whole operational system; corrected here by full inventory and full commit plan.
- Tooling/environment issue: pre-existing staged files are present; local ignored caches and `workspace_config.yaml` remain outside durability scope by design. PostgreSQL projection exists but is not canonical backup.

## 13. Verification results

See `final_verification.log` for raw output.

Key results:

- supersession regression tests: 14 passed;
- full test suite: 266 passed;
- canonical manifest validation: 538/538 objects, no missing/extra packages;
- repository-wide durability validator: failed as expected with Decision D blockers;
- Python compilation: passed;
- production PostgreSQL read-only check: databases listed `knowledgeforge` and `knowledgeforge_immutability_gate_20260711`;
- isolated DB retained and isolated;
- MacroForge checked read-only; InsightForge path missing/not git; no modifications made by this task;
- coherence: 0 blocks, stale generated context warning only;
- context health: 0 blocks, stale generated context warning only;
- architecture-to-reality audit: 0 blocks, 0 warnings;
- git diff --check: passed;
- no stage/commit/push by this task;
- strict Campaign 41 production-artifact check: no matches excluding prior absence-proof files.
