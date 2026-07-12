# D-20260712-campaign42-first-difference-pearson-companion-production

Status: accepted
Date: 2026-07-12

Decision: Accept Campaign 42 as successful end-to-end first-difference Pearson companion production.

Rationale: The eight frozen candidates passed identity, raw package, retained evidence, transformation, method, independent recomputation, embedded diagnostic reconciliation, package validation, append-only canonical publication, PostgreSQL projection, and Relationship Export Contract validation. Companion packages are independently retrievable and explicitly do not supersede raw Pearson packages.

Consequences:
- Canonical repository count increased from 546 to 554.
- Repository fingerprint changed from sha256:c89c25ede69ec88a12f4791dba94b6199f2927721d0028420a65a74dd6ee735c to sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b.
- Raw Pearson objects remain 21 and first-difference Pearson companions are separately classified as 8.
- PostgreSQL remains a projection only; no schema expansion was authorized or performed.
- Campaign 42 provenance is explicit despite inherited raw-source campaign stems in frozen package IDs.
- Final verification found no correctness, coherence, context-health, architecture-audit, compile, test, or whitespace blockers.
- Durability remains a separate unresolved repository-publication/backup concern: the repository-wide validator returned decision D because recovery-critical files are untracked/not yet committed and operational checkpoint state is not machine-loss durable. This does not invalidate Campaign 42 production, but it blocks representing the work as durable.

Non-decisions:
- No Doctrine amendment.
- No KnowledgeObjectPackage redesign.
- No Campaign 43 authorization.
- No inferential/statistical-significance/forecast/causal/investment-signal claim.
- No commit or push.
