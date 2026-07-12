# T-20260712 Pearson Candidate-Policy Refinement for Mixed Production Roadmap

Status: completed
Date: 2026-07-12

## Objective
Write and validate a bounded successor specification for coefficient-free Pearson candidate construction after the accepted mixed-roadmap decision.

## Context inspected
- `tools/coefficient_free_pearson_candidate_registry.py`
- Campaign 40 batch specification and Campaign 40 registry
- Campaign 41 frozen registry and freeze decision
- `D-20260712-pearson-path-to-100-mixed-roadmap.md`
- 21-object Pearson utility inventory

## Work performed
- Created versioned successor specification: `specs/correlation_batches/pearson_candidate_policy_v2_mixed_roadmap.md`.
- Updated the existing generic coefficient-free helper with prospective v2 dry-run functions only; v1 Campaign 41 default behavior remains unchanged.
- Added tests for v2 dry-run validity, coefficient-free proof, semantic/purpose contract, hidden outcome field rejection, and Campaign 41 fingerprint preservation.
- Produced dry-run evidence over the retained 16-series Campaign 40 pool.
- Created policy decision artifact: `artifacts/decisions/D-20260712-pearson-candidate-policy-v2-mixed-roadmap.md`.

## Dry-run result
The successor policy produced 7 non-frozen defensible candidates:
- `nor_crude_birth_rate_under5_mortality`
- `nor_crude_birth_rate_life_expectancy`
- `nor_crude_death_rate_under5_mortality`
- `swe_private_credit_mobile_cellular`
- `swe_private_credit_internet_users`
- `dnk_agricultural_land_broad_money`
- `dnk_agricultural_land_private_credit`

Distribution:
- semantic proximity: 3 close, 2 moderate, 2 remote
- time risk: 7 high
- purpose: 3 transformation-companion candidates, 2 baseline relationship candidates, 2 cautionary relationship candidates

## Backward compatibility
- Campaign 41 registry fingerprint preserved: `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`.
- Campaign 41 batch spec fingerprint preserved: `sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2`.
- No canonical packages were mutated.

## Verification
See `artifacts/reports/pearson-candidate-policy-refinement-mixed-roadmap-20260712/final-verification/`.

## Outcome
A. successor policy is ready for a bounded Campaign 42 registry task.
