# T-20260710 Bounded PostgreSQL Knowledge Repository Realization Decision

Status: complete
Classification: operational realization requirement; preserves existing architecture

## Objective

Determine the conceptual role PostgreSQL should play in KnowledgeForge after the 521-object repository milestone, without implementation, schema design, API/service/loader work, Campaign 34, Production Doctrine modification, KnowledgeObjectPackage redesign, or cross-project coupling.

## Result

Selected option: B — durable KnowledgeForge-owned PostgreSQL operational repository, deterministically derived and rebuildable from canonical KnowledgeObjectPackages, serving discovery and retrieval while canonical authority remains with the packages.

## Evidence

- repository objects inspected: 521
- repository fingerprint at decision time: `sha256:9c7ebb9cc47f3dc58a06828fa334e53473b59f563845b1c64343840ee7a9479c`
- full object scan median: 0.032258s
- package-id index lookup median: 2e-06s
- evidence-family filter lookup median: 6e-06s
- fingerprint lookup median: 1e-06s
- PostgreSQL required for current raw performance: false
- PostgreSQL justified for operational realization: true

## Deliverables

- `tools/postgresql_realization_decision.py`
- `tests/test_postgresql_realization_decision.py`
- `artifacts/reports/postgresql-realization-decision-20260710/bounded_postgresql_realization_decision_report.md`
- `artifacts/reports/postgresql-realization-decision-20260710/postgresql_realization_options_evidence_matrix.json`
- `artifacts/reports/postgresql-realization-decision-20260710/conceptual_responsibility_and_authority_model.json`
- `artifacts/reports/postgresql-realization-decision-20260710/risk_register.json`
- `artifacts/reports/postgresql-realization-decision-20260710/later_implementation_acceptance_criteria.json`
- `artifacts/decisions/D-20260710-bounded-postgresql-knowledge-repository-realization.md`

## Explicit non-actions

No PostgreSQL implementation, schema, table, migration, API, service, loader, Campaign 34, production-family resumption, doctrine modification, package redesign, repository alteration, MacroForge copy, shared database/schema/runtime, commit, or push was performed.

## Next decision/implementation posture

Stop at the decision gate. If implementation is later authorized, the smallest separately approvable slice is a KnowledgeForge-owned deterministic projection of existing packages for local discovery/retrieval and verification support, with full rebuildability and no consumer access contract in the first slice.
