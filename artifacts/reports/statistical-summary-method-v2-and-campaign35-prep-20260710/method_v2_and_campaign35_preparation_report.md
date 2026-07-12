# Bounded Numerical-Method v2 and Statistical-Summary Knowledge-Design Refinement

Status: complete decision gate.

Decision: **A — Method v2 validated; knowledge design refined; Campaign 35 is ready for separate execution authorization.**

No Campaign 35 execution, fixture acquisition, Campaign 34 package mutation, doctrine change, PostgreSQL schema expansion, MacroForge coupling, consumer access, commit, or push occurred.

## Calculation-contract v2

Method: `wdi_annual_scalar_statistical_summary_v2@2.0`

Contract fingerprint: `sha256:80e6b07fd98faf37401103776b6ef82f4ab981c5ea890b381b036058c460e8a0`

Internal precision: 50 decimal digits.
Internal rounding: ROUND_HALF_EVEN.
Canonical stored precision: 12 decimal places, trailing zeros stripped, negative zero canonicalized to zero, scientific notation forbidden.
Human display precision: 4 decimal places, separate from canonical storage and fingerprints.

## Precision justification

Precision 50 is pinned because WDI annual-scalar evidence can include large integer levels, fractional ratios/percentages, non-terminating means, and square roots for standard deviations. It is comfortably above the digits needed for current integer-valued population evidence and reasonable annual-scalar indicators, while remaining simple and deterministic. Canonical storage at 12 decimal places is enough for deterministic comparison of derived means/dispersion without printing arbitrary internal guard digits as evidence accuracy. Human display at 4 decimal places is concise and never affects fingerprints.

## Campaign 34 disposition

Campaign 34 remains historical v1 output. It was not modified. v1 depended on ambient Decimal context; v2 supersedes the method for future campaigns. Future campaigns must not claim v2 lineage for v1 calculations.

## Campaign 35 selected scope

Selected: **Campaign 35 — Bounded WDI Nordic Exports Share Statistical-Summary Replication**.

Indicator: `NE.EXP.GNFS.ZS` — Exports of goods and services (% of GDP).
Entities: DNK, SWE, NOR.
Period: 1990–2024 annual.
Expected evidence slots: 105.
Expected packages: 3, one per entity.
Execution status: not authorized in this task.

## Production objective

KnowledgeForge production now targets construction of a PostgreSQL-accessible repository of substantive, evidence-backed deterministic knowledge, not continued accumulation of predominantly governance, coverage, or provenance objects. Ordinary metadata-heavy WDI breadth campaigns remain paused unless they directly enable substantive knowledge production.
