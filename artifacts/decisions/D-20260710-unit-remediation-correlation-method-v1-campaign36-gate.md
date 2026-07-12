# Bounded WDI Unit-Semantics Remediation and Correlation-Method Design/Falsification Gate

Decision: A — Unit remediation passed; correlation method validated; Campaign 36 ready for separate execution authorization.

## Unit remediation

Unsafe generic unit fallback removed. Normalization now fails closed on unresolved units. Population `persons` is definition-derived; exports share `percent of GDP` is definition-derived from authoritative WDI metadata.

## Campaign 35 scaling evidence

Campaign 35 remains accepted as successful bounded replication: 3 substantive packages, repository count 525, PostgreSQL projection count 525, governance ratio 5.333333333333333 versus Campaign 34 baseline ~24:1.

## Correlation boundary

KnowledgeForge may preserve deterministic mathematical relationships between explicitly scoped evidence series. It must not claim causation, explanation, prediction, economic significance, statistical significance, stationarity, trend, lead/lag, investment relevance, or recommendations.

## Method contract

- method: `wdi_annual_scalar_pearson_correlation_v1@1.0`
- contract fingerprint: `sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476`
- Decimal precision: 50
- minimum aligned pairs: 30
- coverage threshold: 0.85

## Candidate comparison

- trade_exports_imports_dnk: selected (aligned probe 35; risks: none)
- health_birth_death_rates_dnk: reject (aligned probe 35; risks: high_demographic_structure_interpretive_risk)
- education_primary_secondary_enrollment_dnk: reject (aligned probe 23; risks: insufficient_aligned_evidence, missingness_or_methodology_risk)
- financial_credit_broad_money_dnk: reject (aligned probe 35; risks: conceptual_overlap_financial_depth)
- same_indicator_exports_dnk_swe: defer (aligned probe 35; risks: none)
- mechanical_trade_total_reject: reject (aligned probe 35; risks: component_vs_total, component_vs_total)

Selected Campaign 36 pilot: `Campaign 36 — Bounded WDI Denmark Exports-Imports Share Pearson Correlation Pilot`.

## Local-AI experiment

Status: failed. Disposition: advisory only; no frontier model substituted.

## PostgreSQL compatibility

Existing PostgreSQL v1 projects full canonical JSON payload into JSONB plus generic package/evidence family/statement/lifecycle/fingerprint/provenance lookup fields; a future correlation package remains canonical JSON and does not require correlation-specific columns.

## Roadmap sequence

1. Statistical-summary mechanics validated.
2. Unit-semantics defect remediated.
3. Correlation method designed and falsified.
4. One bounded correlation production pilot.
5. Correlation replication across a small controlled scope.
6. Only then consider covariance, lag relationships, broader correlation maps, and consumer-facing access.

This is operational guidance, not automatic authorization beyond a separately approved Campaign 36.
