# T-20260712 Pearson Candidate Policy v2 Consistency Correction and Transformation-Aware Sequencing Gate

Status: completed
Date: 2026-07-12

## Objective
Correct the v2 Pearson candidate-policy inconsistencies and decide whether raw Campaign 42 registry work or transformation-aware method validation should come next.

## Root causes
1. Canonical Campaign 41 candidates appeared because future-production mode used a static prior-exclusion list that ended at Campaign 40. Classification: implementation/reporting defect. The artifact was historical comparison output, not valid future-production evidence.
2. Remote-share validation passed because the implementation applied a nominal 8-candidate capacity cap (`int(8 * 0.25) = 2`) while the actual output contained 7 candidates. Classification: implementation/spec arithmetic defect.
3. Mixed-roadmap sequencing was overstated because the corrected future-production dry-run leaves only 4 candidates, all high time-risk. Classification: decision/reporting defect in prior disposition A.

## Corrective work
- Added current canonical Pearson relationship extraction from `knowledge_repository/objects/`.
- Added separate historical-comparison and future-production dry-run modes.
- Added exact integer remote-cap semantics: `floor(n * 0.25)` for actual selected size `n`.
- Added regression tests for canonical/reversed exclusion, mode isolation, remote arithmetic, Campaign 41 fingerprints, deterministic/coefficient-free behavior, and forbidden outcome fields.
- Corrected the v2 specification and prior v2 decision status.
- Created corrective decision `D-20260712-pearson-candidate-policy-v2-consistency-correction.md`.

## Corrected artifacts
- Historical comparison: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/dry-run/historical_comparison_not_candidate_batch.json`
- Future-production eligibility: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/dry-run/future_production_eligibility_excluding_canonical.json`
- Inconsistency trace: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/inconsistency_trace.json`
- Arithmetic proof: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/batch_composition_arithmetic_proof.json`

## Corrected future-production dry-run
Selected 4 non-frozen candidates:
- `nor_crude_birth_rate_under5_mortality`
- `nor_crude_birth_rate_life_expectancy`
- `nor_crude_death_rate_under5_mortality`
- `dnk_forest_area_private_credit`

Distribution:
- semantic proximity: 3 close, 1 remote
- time risk: 4 high
- purpose: 3 transformation-companion candidates, 1 cautionary relationship knowledge

This is insufficient for a useful raw Campaign 42 registry.

## Decision
B. first-difference Pearson method validation should precede further raw production.

## Verification
See `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/final-verification/`.
