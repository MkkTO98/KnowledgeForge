# T-20260712 Campaign 41 Assimilation and Pearson Path-to-100 Production-Utility Review

Status: completed
Date: 2026-07-12

## Objective
Assimilate the accepted Campaign 41 production result and review whether continuing raw-level Pearson production toward 100 relationship objects remains operationally useful as currently sequenced.

## Scope
Review-only and sequencing-only. No Campaign 42, no new coefficients, no new canonical packages, no canonical package mutation, no PostgreSQL write/rebuild, no schema expansion, no method implementation, no Production Doctrine amendment, no commit, and no push.

## Inputs
- Accepted Campaign 41 production result: 8 accepted Pearson packages, repository count 546, Pearson count 21, repository fingerprint `sha256:c89c25ede69ec88a12f4791dba94b6199f2927721d0028420a65a74dd6ee735c`.
- Canonical Pearson packages under `knowledge_repository/objects/`.
- Existing PostgreSQL projection in `knowledgeforge.knowledgeforge_projection` used read-only.
- Relationship Export Contract v1 used read-only.

## Outputs
- Assimilation closeout: `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/campaign41_assimilation_closeout.md`
- Machine-readable inventory: `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/pearson_utility_inventory.json`
- Inventory CSV: `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/pearson_utility_inventory.csv`
- Production utility review: `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/pearson_production_utility_review.md`
- Candidate-construction policy assessment: `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/candidate_construction_policy_assessment.md`
- Roadmap sequencing decision report: `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/roadmap_sequencing_decision_report.md`
- Decision: `artifacts/decisions/D-20260712-pearson-path-to-100-mixed-roadmap.md`

## Findings
- Campaign 41 assimilation required no additional schema/index work. Campaign 41 packages, raw coefficients, diagnostics, limitations, evidence provenance, and method provenance are discoverable through existing package payloads, PostgreSQL projection, and Relationship Export Contract v1.
- Complete Pearson inventory: 21 objects.
- Numeric time-index diagnostics available: 14.
- Numeric time-index diagnostics lacking: 7.
- Review-only high time-risk count among numeric-diagnostic objects: 14.
- Strong raw + weak first-difference pattern under review-only thresholds: 5.
- Semantic proximity distribution: 12 close, 1 moderate, 8 remote.
- Objects remain reusable for downstream consumers, but a subset is primarily cautionary/baseline knowledge rather than positive descriptive relationship knowledge.

## Outcome
Disposition E — adopt a mixed production roadmap.

The path-to-100 raw Pearson object-count target should no longer be the primary operational success measure. Preserve raw Pearson as a limited baseline descriptor, but sequence future work toward bounded candidate-policy refinement, transformation-aware relationships, and richer deterministic diagnostics.

## Verification
Final verification artifacts are under `artifacts/reports/campaign41-assimilation-pearson-path-to-100-review-20260712/final-verification/`.

## Smallest next task
Write a bounded Pearson candidate-policy refinement specification that adds semantic-proximity and time-risk stratification to coefficient-free registry construction, without calculating Campaign 42, implementing a new method, mutating packages, or changing schema/doctrine.
