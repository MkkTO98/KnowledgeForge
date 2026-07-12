# D-20260710 — Neutral WDI Observation Evidence Fixture and Statistical-Summary Pilot Design Gate

Status: accepted
Date: 2026-07-10
Decision type: bounded evidence-input fixture and pilot-design gate

## Decision

Decision **A. Evidence fixture validated; statistical-summary pilot is ready for separate execution authorization.**

This decision does not execute or promote a statistical-summary production campaign. It does not create Campaign 34.

## Selected fixture

- Mature family: `external_wdi_annual_scalar_demographic_structure`
- Indicator: `SP.POP.TOTL` — Population, total
- Entity: Denmark (`DNK`)
- Period: 1990-2024 annual
- Observation slots: 35
- Observed values: 35
- Missing values: 0

## Evidence-input boundary result

KnowledgeForge independently acquired a bounded observation-level WDI fixture from the authoritative World Bank WDI API using KnowledgeForge-owned code. The fixture preserves exact raw response bytes, acquisition metadata, a deterministic selection contract, normalized observation-level evidence, explicit missingness policy, and reproducibility fingerprints.

The fixture is an evidence input. It is not a KnowledgeObjectPackage and not canonical knowledge.

## Fingerprints

- Selection fingerprint: `sha256:e5ec35208a8fcaa7561f19843b401b9751fb9246ef2e78185ea17bd5fef80d04`
- Raw fixture fingerprint: `sha256:39fd3decdfe4a78b7678104a5cdd97b2a487819dce587650405e8059f08a4e4e`
- Combined raw artifact fingerprint: `sha256:fd0be51504e4cf811a0e20e2858fdbafd567bbc4c9eaed5252f059282cc7153f`
- Normalized observation fingerprint: `sha256:01f10c90228540c31f2f873ee5b4930006c99bf430c7cb741f41a0e8157734b6`

## Mutable-source vintage limitation

Exact reproducibility is guaranteed from the retained local raw response bytes and normalized fixture. WDI source identity and freshness are represented through the request URLs, parameters, source id, indicator metadata, and `lastupdated` metadata. WDI did not expose a true immutable historical vintage identifier in the retained response; therefore the fixture does not claim that identical historical provider bytes can be reacquired from the mutable API later.

## Statistical-summary pilot readiness

A later pilot may be separately authorized to generate a strictly descriptive statistical-characterization KnowledgeObjectPackage over this fixture. The preferred pilot is a method-scoped statistical summary, not trend, correlation, covariance, lag, causation, forecasting, recommendation, or InsightForge work.

The later pilot must use the retained normalized fingerprint as input evidence and must remain canonical JSON projected through PostgreSQL v1 without schema expansion.

## Architecture classification

Classification: preserves agreed architecture.

Justification:

- uses the already-accepted external evidence-input boundary;
- does not make KnowledgeForge a general observational-data platform;
- does not query or depend on MacroForge;
- does not create shared schemas/databases/runtime dependencies;
- does not modify Production Doctrine;
- does not redesign KnowledgeObjectPackage;
- does not expand PostgreSQL projection schema.

## Next bounded task

If authorized separately: execute a bounded statistical-summary production pilot for `SP.POP.TOTL` / `DNK` / `1990-2024` using the retained fixture.

Do not start Campaign 34 automatically.
