# D-20260710 — PostgreSQL Operational Projection Acceptance and Production-Sequencing Gate

Status: accepted
Date: 2026-07-10
Decision type: bounded acceptance and sequencing decision

## Result

PostgreSQL acceptance result: **A. Accept the PostgreSQL operational projection as v1-complete.**

Production sequencing result: **3. PostgreSQL accepted; an existing evidence-input boundary must first be operationalized.**

## Acceptance basis

The acceptance gate independently re-verified only the already-approved criteria needed to establish whether the reported implementation state still held.

| Criterion | Result | Evidence |
| --- | --- | --- |
| KnowledgeForge-owned database exists | pass | `knowledgeforge` database present and owned by PostgreSQL role `mkkto` |
| Projection contains exactly 521 canonical packages | pass | canonical count `521`; projected count `521` |
| Canonical and projected package IDs match | pass | missing IDs `0`; extra IDs `0` |
| Package fingerprints match | pass | package fingerprint failures `0` |
| Payload fidelity passes | pass | payload fidelity failures `0` |
| Represented repository fingerprint matches canonical repository | pass | `sha256:9c7ebb9cc47f3dc58a06828fa334e53473b59f563845b1c64343840ee7a9479c` |
| Projection freshness passes | pass | projection `valid=true` |
| Supported discovery operations work | pass | package lookup, evidence-family filter, statement-type filter re-run |
| Stale projection detection fails closed | pass | stale probe returned `stale_or_invalid_projection` |
| Canonical packages remain unchanged | pass | 521/521 byte hashes unchanged relative to implementation pre-check |
| MacroForge database/schema remains unmodified | pass | `macroforge` has no `knowledgeforge_projection` schema |
| Campaign 34 remains absent | pass | `*campaign34*` file search returned `0` |

Machine-readable detail: `artifacts/reports/postgresql-acceptance-sequencing-20260710/postgresql_v1_acceptance_decision.json`.

## Security classification

- Current database-level isolation is sufficient for local single-user operation.
- Both KnowledgeForge and MacroForge databases are owned by PostgreSQL role `mkkto`.
- Therefore this is **not strong role-level isolation**.
- Stronger role separation is a future deployment/security concern, not a blocker, because the acceptance gate found no actual unauthorized cross-database behaviour.

## Remaining PostgreSQL v1 limitations

These are accepted v1 boundaries, not blockers:

- full rebuild only;
- no incremental synchronization;
- no consumer access;
- no InsightForge access;
- no API/service;
- no PostgreSQL-originated knowledge;
- no canonical package mutation;
- no future-rich-object relational schema expansion;
- local single-user role isolation only.

## Evidence-availability conclusion

KnowledgeForge currently has objective evidence in the form of canonical packages, production snapshots, reports, source references, hashes, release metadata, aggregate coverage/quality/provenance measurements, and deterministic campaign tools.

It does **not** currently retain locally accessible observation-level numerical WDI values sufficient for a genuine deeper deterministic numerical knowledge pilot such as statistical summaries, trends, correlations, covariance structures, or lag relationships.

Existing campaigns can be deterministically rerun to regenerate their retained aggregate/source-evidence artifacts. They do not independently prove operational reacquisition of observation-level values.

The accepted architecture already defines a compliant evidence-input boundary: external evidence systems or sources may provide immutable exports/snapshots, reproducibility handles, dataset/series references, source indicator metadata, release/vintage references, and source documentation references. KnowledgeForge may store references or small immutable snapshots where justified, but must not become the owner of full external observational datasets.

Missing observation-level access is therefore an implementation gap and sequencing issue, not an architectural contradiction.

## Production sequencing decision

Do not resume ordinary WDI breadth expansion now.

Do not start Campaign 34.

Before a deep deterministic knowledge pilot, operationalize the existing neutral evidence-input boundary for one bounded objective numerical evidence extract.

Recommended next bounded task:

**Neutral WDI Annual-Scalar Observation Evidence Input Fixture and Statistical-Summary Pilot Design Gate.**

The task should not implement a production campaign. It should define and verify the smallest compliant evidence input fixture required for a later statistical-summary pilot:

- one WDI annual-scalar mature family or sub-family;
- one or a few indicators;
- explicit source URL/API/export identity;
- source version/vintage/access date;
- immutable local snapshot or export fingerprint;
- selection/query fingerprint;
- units/entity/period identifiers;
- missingness encoding;
- deterministic recipe for producing a method-scoped statistical summary candidate;
- no MacroForge database access, no MacroForge runtime dependency, and no shared schema.

The preferred later pilot, after that boundary is operationalized, is a bounded statistical-summary object, not correlation/lag/covariance. It is the shallowest genuinely substantive deterministic pilot that can exercise numerical evidence without crossing into interpretation.

## Doctrine and architecture classification

Classification: preserves agreed architecture.

Justification:

- PostgreSQL remains a derived operational projection of canonical package JSON.
- Canonical package authority remains filesystem-backed `knowledge_repository/objects/*.json`.
- The evidence-access conclusion preserves the constitutional boundary that external observational systems own observations and KnowledgeForge owns reusable knowledge/evidence evaluations.
- The next step uses an already-defined evidence-input boundary instead of creating cross-project coupling.
- No Production Doctrine modification is required.

## Explicit prohibitions preserved

This decision does not authorize:

- Campaign 34;
- a new production campaign;
- consumer access;
- InsightForge access;
- an API/service;
- incremental synchronization;
- PostgreSQL schema expansion for hypothetical knowledge types;
- Production Doctrine modification;
- KnowledgeObjectPackage redesign;
- cross-project coupling;
- commit or push.
