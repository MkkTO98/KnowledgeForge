# Decision: Bounded PostgreSQL Knowledge Repository Realization

Date: 2026-07-10
Status: Accepted decision-gate result; smallest implementation slice authorized and implemented on 2026-07-10
Classification: operational realization requirement; preserves existing architecture

## Decision

Select Option B:

> A durable KnowledgeForge-owned PostgreSQL operational repository, deterministically derived and rebuildable from canonical KnowledgeObjectPackages, serving discovery and retrieval while canonical authority remains with the packages.

## What this decision authorizes

This decision authorizes only a future separately approved implementation slice to realize a derived PostgreSQL operational repository under KnowledgeForge ownership.

It does not implement PostgreSQL and does not authorize implementation by itself.

## What this decision does not authorize

- no PostgreSQL implementation in this task;
- no SQL DDL, schemas, tables, migrations, APIs, services, or loaders in this task;
- no Campaign 34 or resumed ordinary production;
- no Production Doctrine modification;
- no KnowledgeObjectPackage redesign;
- no alteration of the canonical filesystem repository;
- no MacroForge implementation copy;
- no shared schema, runtime code, database ownership, or cross-project coupling;
- no consumer writes or consumer-defined KnowledgeForge structures.

## Evidence basis

Primary artifacts:

- `artifacts/reports/postgresql-realization-decision-20260710/bounded_postgresql_realization_decision_report.md`
- `artifacts/reports/postgresql-realization-decision-20260710/postgresql_realization_options_evidence_matrix.json`
- `artifacts/reports/postgresql-realization-decision-20260710/conceptual_responsibility_and_authority_model.json`
- `artifacts/reports/postgresql-realization-decision-20260710/risk_register.json`
- `artifacts/reports/postgresql-realization-decision-20260710/later_implementation_acceptance_criteria.json`

Measured repository evidence:

- repository objects inspected: 521
- full object scan median: 0.032258s
- package-id index lookup median: 0.000002s
- evidence-family filter index lookup median: 0.000006s
- fingerprint lookup median: 0.000000s
- provenance/lineage scan median: 0.000182s

Measured conclusion: PostgreSQL is not required today for raw performance.

Architectural conclusion: PostgreSQL is justified now for operational realization, downstream usability, future scale readiness, and richer deterministic knowledge retrieval.

## Existing commitments reconciled

- Full `KnowledgeObjectPackage` JSON remains canonical.
- Filesystem-backed packages remain the authoritative canonical artifact layer.
- Indexes, manifests, and evolution records remain deterministic structures derived from packages.
- PostgreSQL is an operational representation for discovery and retrieval, not canonical authority.
- KnowledgeForge remains independently owned; no cross-project schema/runtime/database ownership is introduced.

## Rejected options

- Option A rejected: disposable projection is too weak for the accepted operational repository end state, though rebuildability from packages remains required.
- Option C rejected: co-authority introduces authority ambiguity and dual-write risk without evidence.
- Option D rejected: database canonicality conflicts with accepted canonical-package architecture; 521 objects is not sufficient evidence.
- Option E rejected: filesystem performance is adequate, but filesystem-only operation fails to realize the accepted operational discovery/retrieval end state.

## Authority and consistency model

- Canonical authority: full `KnowledgeObjectPackage` JSON under `knowledge_repository/objects/`.
- PostgreSQL role: durable KnowledgeForge-owned operational repository for discovery, retrieval, traversal, verification support, and bulk access, derived from canonical packages.
- PostgreSQL may originate canonical knowledge: no.
- PostgreSQL may mutate canonical knowledge: no.
- PostgreSQL must be fully rebuildable from canonical packages: yes.
- PostgreSQL participates in canonical fingerprints: no.
- PostgreSQL may have a projection/rebuild fingerprint for divergence detection, but it does not replace package or repository fingerprints.
- If PostgreSQL and canonical packages disagree, canonical packages win; PostgreSQL is stale/invalid and must fail closed or degrade to canonical filesystem reads until rebuilt/reconciled.

## Downstream boundary

Independent consumers such as InsightForge may later retrieve KnowledgeForge knowledge through KnowledgeForge-owned read-only projections, exported deterministic snapshots, future KnowledgeForge-owned query interfaces, or direct canonical package consumption.

Direct consumption does not authorize:

- shared database ownership;
- shared schema ownership;
- shared runtime code;
- consumer writes;
- consumer-defined KnowledgeForge structures.

## Ordering decision

PostgreSQL realization should occur before deeper deterministic-knowledge campaigns. This is not because current filesystem performance fails, but because future richer objects should be discoverable, retrievable, traversable, bulk-exportable, and reproducibly snapshotted from the start.

## Smallest later implementation slice

If separately authorized, the smallest acceptable implementation slice is a KnowledgeForge-owned, local, deterministic PostgreSQL projection of existing canonical KnowledgeObjectPackages sufficient for package-id lookup, evidence-family/statement-type/lifecycle/fingerprint filtering, provenance-lineage discovery, repository snapshot verification, and canonical-package retrieval pointers.

The first slice must exclude consumer access contracts, shared schemas, PostgreSQL-originated knowledge, Campaign 34, new production families, and rich statistical schema expansion.

## Future expansion gates

- Consumer-facing access requires a separate downstream consumption contract decision.
- Rich statistical relationship projection requires successful deeper deterministic-knowledge campaigns first or an explicit design gate.
- Incremental synchronization requires full-rebuild proof first and a separate consistency decision.
- Direct InsightForge access requires an explicit read-only boundary decision after local KnowledgeForge projection proves stable.
