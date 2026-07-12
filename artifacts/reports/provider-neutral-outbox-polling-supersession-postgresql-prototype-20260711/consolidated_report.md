# Provider-Neutral Outbox Polling, Unified Release Registry, and Controlled Supersession/PostgreSQL Prototype

Date: 2026-07-11
Status: complete
Decision: A — Outbox polling and controlled supersession/incremental publication validated.
Next strategic direction: 2 — Deploy bounded periodic polling after server migration.

## Scope boundaries

No MacroForge files were modified. No MacroForge code was imported. No MacroForge PostgreSQL/private schemas were queried. No InsightForge files were modified. No production canonical Knowledge Objects were promoted. No production PostgreSQL schema was expanded. No cron/systemd/webhook/event bus was installed. Campaign 41 was not created. Production Doctrine and KnowledgeObjectPackage were not redesigned. No local AI retry was performed. No commit or push was performed.

## 1. Outbox polling implementation

Implemented KnowledgeForge-owned provider-neutral filesystem polling tool:

- `tools/external_outbox_poller_v1.py`
- `config/external_outbox_sources.json`

The source configuration records only source identity, root location, supported contract/version, discovery pattern, enabled state, manual polling mode, transfer destination, and scan limits. It does not encode MacroForge private tables/modules, correlation methods, KnowledgeForge derivations, or consumer writes.

The poller supports list-discovered, dry run, poll once, max releases, transport registry verification, registry inventory, and controlled successor prototype. It ignores `_staging` directories, validates manifest/export hash before transfer, copies into KnowledgeForge-owned staging, validates copied bytes, atomically publishes into the KnowledgeForge inbox, and never moves or modifies producer files.

## 2. Transfer and transport registry

Real poll result: `processed`.

- producer release ID: `macroforge-wdi-1990-2024-2b1a1c3d9e65b182`
- producer fingerprint: `sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67`
- export SHA-256: `1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86`
- manifest SHA-256: `2e46edaca1fae5aaa6b602c4137ce88d23903f1fa283397dcc1393d4b36d7e79`
- destination export: `artifacts/external-outbox-transport-v1/inbound/macroforge-neutral-evidence-release-outbox-local-v1/macroforge-wdi-1990-2024-2b1a1c3d9e65b182/macroforge-wdi-1990-2024-2b1a1c3d9e65b182.neutral-release.json`
- adapter: `knowledgeforge_macroforge_neutral_release_adapter_v1@1.0`

Transport registry verification: valid `True`, entries `2`.

Registry path: `artifacts/external-outbox-transport-v1/transport-registry.jsonl`.

## 3. Unified registry decision

Production authority for future real external releases is defined as:

`artifacts/release-inbox-unified-v1/seen-release-registry.jsonl`

Historical real MacroForge manual-handoff evidence is imported by copying the prior seen-release registry and accepted normalized release bytes. Test/conformance registries remain fixtures/evidence. Incompatible identities are not merged silently.

Decision artifact: `registry_consolidation_decision.md`.

## 4. Duplicate real-release result

The closeout-triggered MacroForge outbox artifact was recognized as identical to the previously manually processed release.

- producer release ID matched: `macroforge-wdi-1990-2024-2b1a1c3d9e65b182`
- producer release fingerprint matched: `sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67`
- export SHA matched: `1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86`
- normalized KnowledgeForge release fingerprint: `sha256:75a2b2a586df56523e3a5f81435b159f078af767d67de5adbda667e47c755060`
- seen-release result: `already_processed_identical_release`
- incremental recompute count: `0`
- duplicate rerun transport status: `already_transferred_identical`

No duplicate recomputation occurred. No duplicate canonical package was created.

## 5. Metadata sufficiency gate

Rules implemented/documented in `metadata_sufficiency_gate.md`:

A. Known registered indicator and compatible retained semantics: automatic deterministic recomputation permitted.
B. Known indicator but changed short label/unit: semantic review required/quarantine.
C. New unseen indicator with short label only: candidate registry proposal only; no automatic relationship generation.
D. Full definition/source metadata available and validated: eligible for deterministic applicability screening.

The gate explicitly forbids inferring full definitions from short labels and forbids local AI from filling missing provider semantics.

## 6. Controlled successor

Constructed isolated fixture release labeled `controlled_test_successor_not_provider_evidence`.

Changes:

- appended DNK 2025 exports/imports observations;
- revised one historical DNK exports observation;
- left SWE/NOR evidence unchanged;
- predecessor reference explicit.

Successor release ID: `macroforge-wdi-1990-2024-2b1a1c3d9e65b182-controlled-successor-v2`.
Successor release fingerprint: `sha256:2b69cfee26ee6922d630317c4d8f699301a1c5fc0f674b3337ed965531197d5e`.

## 7. Canonical supersession result

Isolated file-backed repository result: valid `True`.

- predecessor package lifecycle: `superseded`
- successor package lifecycle: `accepted`
- changed package count: `1`
- unchanged package count: `2`
- repository fingerprint: `sha256:3835f9961eff4eb0b10872c9d419bb74b99c787eef9e79bf1d5acee618046636`

Original package remains historically retrievable in the isolated repository, successor has a distinct identity/version, predecessor reference is explicit, SWE/NOR packages are not rewritten, and rerun was idempotent in tests.

## 8. Isolated PostgreSQL result

A temporary isolated PostgreSQL database was created, populated, queried, dumped for evidence, and dropped. Production PostgreSQL was not modified.

- database: `knowledgeforge_isolated_outbox_20260711`
- createdb exit: `0`
- rows before: `0`
- rows after: `4`
- inserted/updated rows: `4`
- execution seconds: `0.116974`
- dropdb exit: `0`

Changed-since query returned DNK predecessor/successor rows only.

Evidence: `isolated/isolated_postgresql_result.json` and `isolated/isolated_postgresql_schema_dump.sql`.

## 9. Incremental/full comparison

Decision: retain full rebuild for now; adopt incremental update later only after bounded consistency decision.

- incremental rows touched: `2`
- full rebuild rows: `4`
- divergence risk: incremental higher unless transactional current uniqueness is enforced
- recovery complexity: full rebuild lower; incremental requires rollback/invalidation journal

Reason: incremental projection is promising and smaller, but production adoption needs transactional current uniqueness, invalidation/rollback journal, and consistency gates.

## 10. Compact delta result

Compact delta identifies new producer release, changed observation scope, affected DNK derivation, new current package, historical predecessor, unchanged SWE/NOR relationships, limitations, and fingerprints.

- compact delta bytes: `1027`
- full downstream delta bytes: `2174`
- raw successor release bytes: `191704`

## 11. Failure/recovery

Failure fixtures result: producer files untouched `True`.

Cases: `[{'case': 'missing_manifest', 'status': 'quarantined'}, {'case': 'unsupported_contract', 'status': 'unsupported_contract'}, {'case': 'adapter_failure', 'status': 'processing_failed'}, {'case': 'failed_copy', 'status': 'transfer failed'}, {'case': 'retry_after_failure', 'status': 'retry_succeeded'}]`

Covered by automated tests and fixtures: incomplete/staging ignored, missing manifest, hash mismatch, unsupported contract, duplicate identical release, transfer failure, adapter failure, metadata gate failure classes, retry after failure, and restart/idempotence through append-only registries.

## 12. Durability status

Durability inventory: `45` files, `1743910` bytes.

Status: not durable until committed/pushed or externally backed up. Local existence is not machine-loss recovery. Recovery-critical assets include source config, transport registry, production seen-release registry, accepted transferred releases, adapter records, processing evidence, downstream deltas, and supersession evidence.

## 13. Eventing decision

Decision: A now, B later after server deployment.

Keep manual poll command now. Actual release cadence is low, latency needs are weak, and failure recovery benefits from explicit manual review. Periodic cron polling is reasonable later after server deployment and backup/monitoring are in place. No scheduler was installed.

## 14. Doctrine and architecture classification

Classification: doctrine-preserving architecture extension. Adds provider-neutral external-source configuration, transport registry, unified release-registry authority, metadata sufficiency gate, and isolated supersession/projection evidence. Does not alter Production Doctrine, KnowledgeObjectPackage design, production canonical repository, or production PostgreSQL schema.

## 15. Verification source files

- execution/list_discovered.json
- execution/dry_run.json
- execution/poll_once_result.json
- execution/poll_once_duplicate_result.json
- execution/transport_registry_verification.json
- execution/registry_inventory.json
- isolated/controlled_supersession_result.json
- isolated/isolated_postgresql_result.json
- failure-recovery/failure_recovery_result.json
- durability/durability_inventory.json
- verification/production_unchanged_check.json
