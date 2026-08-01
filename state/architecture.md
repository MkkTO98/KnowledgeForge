# Architecture State

KnowledgeForge architecture remains canonical-package-first. The frozen Production Doctrine remains sufficient. Full KnowledgeObjectPackage JSON remains canonical. The filesystem-backed Knowledge Repository remains the authoritative canonical artifact layer, intermediate materialization, and governance/audit layer. PostgreSQL remains a deterministic v1 operational projection derived from canonical packages.

Current PostgreSQL projection role: discovery and retrieval over canonical packages while canonical authority remains with files. PostgreSQL may not originate or mutate canonical knowledge and does not participate in canonical fingerprints.

## Native Package Content Fingerprint v1 formalization — 2026-07-17

KnowledgeForge has published the documentation-only architecture for Package Content Fingerprint v1, deterministic governing-contract resolution, and the promotion–verification–admission–insertion–publication sequence. The architecture fixes one native-v1 release-authority family, derives checkpoint-qualified current authority from complete accepted-release evidence, separates technical validity from admission and insertion state, preserves exact serialized bytes through admission and publication proof, and completes canonical visibility only after stage-10 reconciliation and one atomic visibility switch.

The normative documents are `docs/package_content_fingerprint_v1.md`, `docs/governing_contract_resolution_profile_v1.md`, and `docs/promotion_verification_admission_publication_sequence_v1.md`, governed by the accepted decisions under `artifacts/decisions/`. This formalization is not implemented and grants no production authority. Schemas, executable conformance vectors, resolver and authority-record implementation, reader-gate/visibility mechanisms, migrations, native-v1 production, PostgreSQL changes, and export changes remain separately gated future work.

## Method v2 status — 2026-07-10

A bounded deterministic statistical-summary method v2 exists in `tools/deterministic_statistical_summary_v2.py` with contract `artifacts/methods/statistical_summary_calculation_contract_v2.json`. It establishes a local Decimal context independent of ambient Python Decimal state.

This is not a Production Doctrine change, KnowledgeObjectPackage redesign, PostgreSQL schema expansion, or architecture reopening. It is bounded computational-method remediation justified by Campaign 34.

## Production direction

KnowledgeForge production should now prioritize substantive deterministic knowledge packages over metadata-heavy breadth accumulation. Future statistical relationships, changes/growth measures, trend descriptors, correlations, covariance structures, lag relationships, and mathematical relationships remain sequencing guidance only; each requires separately accepted bounded methods before production.


## Release inbox architecture note — 2026-07-11

KnowledgeForge owns a provider-neutral, file-backed release-processing boundary: inbox, accepted releases, quarantine, processing evidence, and append-only seen-release registry. Operational release records are recovery-critical state. MacroForge compatibility is via neutral release contract/conformance package only, not shared code, private tables, credentials, or shared schema. Current implementation is manual CLI/no-promote only; canonical supersession and PostgreSQL update semantics remain unimplemented.

## External producer release handoff boundary

KnowledgeForge may consume externally supplied producer-neutral evidence releases through KnowledgeForge-owned adapters when the external contract is documented, producer fingerprints validate independently, and all semantics are mapped without guessing. Producers retain ownership of their export representation and fingerprints; KnowledgeForge retains ownership of ingestion, normalized release representation, inbox/registry state, no-promote recomputation, and canonical promotion decisions.

Current supported external producer contract: `macroforge.neutral_evidence_release_export.v1` via `knowledgeforge_macroforge_neutral_release_adapter_v1@1.0`.

This boundary forbids shared runtime code, MacroForge PostgreSQL/private-schema access, silent contract coercion, canonical promotion without a separate supersession decision, and scheduling before handoff generation semantics are proven.

## External release automation boundary

KnowledgeForge may use a provider-neutral manual outbox poller to copy immutable producer release artifacts into a KnowledgeForge-owned inbox, validate transport hashes, invoke KnowledgeForge-owned adapters, and record append-only transport evidence. Future real external releases should use `artifacts/release-inbox-unified-v1/seen-release-registry.jsonl` as the production registry authority. Automatic derivation processing remains gated by metadata sufficiency; production canonical supersession and incremental PostgreSQL publication require explicit future authorization.

## Canonical supersession immutability rule

Canonical package JSON bytes are immutable. Supersession must append a successor package and record current/superseded identity outside package bytes in a current-state registry/projection plus append-only supersession/evolution records. PostgreSQL projections should separate immutable package payload from current-state rows. Production incremental publication remains deferred until consistency and rollback guarantees are explicitly decided.

Repository persistence may not rewrite an existing package id with different bytes. `persist_knowledge_object_packages` is an append/idempotent persistence primitive: identical re-persistence is allowed, but non-identical overwrite is rejected. Publish successors as distinct package ids and externalize lifecycle/current-state transitions.

## Durability architecture note — 2026-07-11

KnowledgeForge is not durability-ready while canonical packages, recovery-critical registries, evidence fixtures, method contracts, and release histories remain local-only. Ordinary Git is suitable for canonical JSON packages, source/tests/specs/method contracts, small registries, state, task, and decision records. Large raw evidence, release exports, full release histories, large logs/reports, and database dumps require Git LFS or immutable external artifact storage before they scale. PostgreSQL remains an operational projection and is never a sole backup for canonical or evidence state.

## Durability destination policy — 2026-07-12

Current measured material supports ordinary Git as the primary durability destination for canonical KnowledgeObjectPackage JSON, manifest/index/evolution metadata, method/calculation contracts, correlation/batch specifications, source/tests, small evidence fixtures, compact decision-bearing reports, and task/decision/doctrine/roadmap/architecture/state/handoff records. Git LFS or immutable external artifact storage is reserved for genuinely large raw provider responses, full release histories, large logs/report bundles, database dumps retained as evidence, or future measured artifacts that no longer fit ordinary Git review. Mutable seen-release/current-state/outbox registries and PostgreSQL backups require operational backup/checkpointing; PostgreSQL remains a rebuildable projection, never canonical authority.

## Operational state checkpoint boundary — 2026-07-12

KnowledgeForge has a versioned local operational-state checkpoint/restore primitive for mutable release inbox, seen-release/current-state, accepted source copy, and outbox transport state. The checkpoint contract is `knowledgeforge.operational_state_checkpoint.v1`; protected-state configuration is `knowledgeforge.protected_state.v1`. The primitive supports deterministic manifesting, sensitive exclusions, validation, isolated restore, and PostgreSQL reconstruction evidence. Same-host checkpoints are recovery/restore evidence only and must not be represented as disaster durability: `tested_local_only = true`, `machine_loss_durable = false`, and `external_destination_configured = false` until an off-host or outside-host-failure-domain destination is actually configured and verified.

## Evidence Portfolio production realization — 2026-07-30

The first bounded pilot confirmed that an Evidence Portfolio is an execution/accounting composition over accepted candidate-registry, campaign, calculation, KnowledgeObjectPackage, canonical repository, promotion, operational-view and projection contracts. It is not a canonical object type or parallel batching subsystem.

Evidence-Card-equivalent outputs are operational views of canonical result records. Their count remains separate from canonical package count, source-series count, transformations, bundles, dependency clusters, exclusions, nulls, redundancies and failures.

The existing filesystem authority and rebuildable PostgreSQL projection represented the two promoted baseline-characterization packages without schema change. Direct package/projection consumption is adequate; relationship-specific export metadata does not generalize to baseline characterization. No architecture amendment or new decision was required.

## Evidence Portfolio conformance profile v1 — 2026-08-02

`knowledgeforge.evidence_portfolio.conformance.v1@1.0` is the accepted prospective conformance layer over the existing Evidence Portfolio composition. It closes the reviewed accounting, question-to-evidence, transformation-identity and dependence gaps without introducing a canonical type, evidence family, calculation method, database, projection schema or parallel subsystem.

The profile uses deterministic, versioned envelopes with embedded parsed historical source objects, exact source/report bindings, phase-aware candidate/result accounting, directional traceability, source-bound transformations and separately derived source-series/provider/acquisition/method dependence clusters. Envelope validation proves self-consistency; governed-source comparison remains a separate authentication requirement. Historical Norway/Sweden surfaces remain immutable and require explicit adaptation. Live producer admission, publication, a third portfolio and any canonical/PostgreSQL mutation remain separately gated.
