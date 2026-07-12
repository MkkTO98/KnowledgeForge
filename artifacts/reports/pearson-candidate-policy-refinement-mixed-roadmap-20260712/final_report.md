# Pearson Candidate-Policy Refinement for the Mixed Production Roadmap — Final Report

## 1. Existing rules preserved
Preserved unchanged: coefficient-free construction; retained validated WDI evidence-pool boundary; same-entity/annual/raw/resolved-unit compatibility; minimum 30 aligned pairs and 0.85 coverage; self-pair/duplicate removal; prior canonical/frozen relationship exclusion; mechanical/direct-identity exclusions; deterministic pair ordering and metadata-only tie-breaking; package-ID uniqueness and collision checks; Campaign 41 frozen v1 authority.

## 2. Rules changed and production evidence
Changed rules:
- Semantic proximity is now primary over cross-family diversity. Evidence: Campaign 41 selected 8/8 semantically remote candidates; all were high time-risk.
- Diversity is secondary. Evidence: diversity validated infrastructure but over-selected cautionary/baseline relationships.
- Remote ordinary-batch share is capped at 25% of an 8-candidate batch by default. Evidence: 21-object review found 8/21 remote, all from Campaign 41.
- Time-risk category is required as visible metadata. Evidence: 14/14 numeric-diagnostic Pearson objects had high time-risk.
- Transformation-companion eligibility and candidate utility statements are required. Evidence: 5 strong-raw/weak-first-difference cases.

## 3. Semantic-proximity rubric
Classes: close, moderate, remote, unresolved.

Allowed fields: indicator code/name/definition, measurement concept, unit, frequency, transformation, entity, production family, numerator/denominator relationship visible in metadata, retained fingerprints, period scope.

Tie-break: explicit accepted pair rule > same family > demographic/health bridge > unresolved if missing definitions/units > remote.

Unresolved candidates require manual review. Optional local AI may advise from metadata only but cannot decide.

## 4. Time-risk input boundary
Permitted: prior accepted per-series time diagnostics, deterministic metadata risk flags, retained trend descriptors, monotonic/bounded metadata, and prior accepted diagnostic artifacts.

Forbidden: candidate-pair Pearson, first-difference, covariance, p-values, significance, lag results, preliminary result caches.

Categories: low, moderate, high, unknown. Unknown remains visible and is not low.

## 5. Transformation-companion eligibility rules
Raw candidates should prioritize a companion when time-risk is high/unknown, semantic proximity is remote, or unit/series type suggests embedded trend pressure.

Permitted recommendations: first differences, growth rates, percentage changes, or other already evidenced deterministic transformations.

Required checks: unit semantics, zero/negative behavior, bounded-ratio behavior, missingness after transformation, minimum transformed overlap, transformed-value interpretability.

No companion method was implemented or calculated.

## 6. Batch-composition defaults
Roadmap defaults, not Doctrine quotas:
- prefer close majority when available;
- use moderate with explicit justification;
- cap remote at <=25% of ordinary 8-candidate batch;
- max 3 candidates/entity;
- max 3 candidates/family-pair bucket;
- max 2 uses of one indicator/entity;
- unknown time-risk visible and non-dominating;
- cautionary/pressure-test candidates bounded minority.

## 7. Candidate-utility statement contract
Every future candidate must state before calculation: why worth canonizing, expected descriptive use, expected limitation, likely consumer use, purpose classification, and no coefficient/acceptance prediction.

## 8. Helper changes
Updated existing `tools/coefficient_free_pearson_candidate_registry.py` only as needed. Added prospective v2 dry-run functions and metadata generation. Default Campaign 41 v1 `build_outputs()` behavior remains unchanged. Added tests in `tests/test_coefficient_free_pearson_candidate_registry.py`.

## 9. Campaign 41 backward compatibility
Passed.
- Registry fingerprint: `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`
- Batch spec fingerprint: `sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2`
- Historical campaigns not retroactively invalidated.
- No canonical package mutated.

## 10. Dry-run successor-policy candidate set
- `nor_crude_birth_rate_under5_mortality` — NOR; SP.DYN.CBRT.IN × SH.DYN.MORT; semantic=close; time-risk=high; purpose=transformation_companion_candidate
- `nor_crude_birth_rate_life_expectancy` — NOR; SP.DYN.CBRT.IN × SP.DYN.LE00.IN; semantic=close; time-risk=high; purpose=transformation_companion_candidate
- `nor_crude_death_rate_under5_mortality` — NOR; SP.DYN.CDRT.IN × SH.DYN.MORT; semantic=close; time-risk=high; purpose=transformation_companion_candidate
- `swe_private_credit_mobile_cellular` — SWE; FS.AST.PRVT.GD.ZS × IT.CEL.SETS.P2; semantic=moderate; time-risk=high; purpose=baseline_relationship_knowledge
- `swe_private_credit_internet_users` — SWE; FS.AST.PRVT.GD.ZS × IT.NET.USER.ZS; semantic=moderate; time-risk=high; purpose=baseline_relationship_knowledge
- `dnk_agricultural_land_broad_money` — DNK; AG.LND.AGRI.ZS × FM.LBL.BMNY.GD.ZS; semantic=remote; time-risk=high; purpose=cautionary_relationship_knowledge
- `dnk_agricultural_land_private_credit` — DNK; AG.LND.AGRI.ZS × FS.AST.PRVT.GD.ZS; semantic=remote; time-risk=high; purpose=cautionary_relationship_knowledge

Summary:
- selected: 7
- semantic: {'close': 3, 'moderate': 2, 'remote': 2}
- time-risk: {'high': 7}
- purpose: {'baseline_relationship_knowledge': 2, 'cautionary_relationship_knowledge': 2, 'transformation_companion_candidate': 3}
- dry-run fingerprint: `sha256:6d330e347b57993ebc4456685c4b3655813e47e0725798c9285dca44fa6c3282`

## 11. Comparison with Campaign 41
Retained from Campaign 41: ['dnk_agricultural_land_broad_money', 'dnk_agricultural_land_private_credit', 'swe_private_credit_internet_users', 'swe_private_credit_mobile_cellular']

Deprioritized from Campaign 41: ['nor_fossil_electricity_under5_mortality', 'nor_nonhydro_renewable_electricity_under5_mortality', 'dnk_forest_area_broad_money', 'nor_crude_birth_rate_fossil_electricity']

Newly prioritized: ['nor_crude_birth_rate_under5_mortality', 'nor_crude_birth_rate_life_expectancy', 'nor_crude_death_rate_under5_mortality']

Reason: successor policy prioritizes semantic proximity and caps ordinary remote share; diversity remains secondary.

## 12. Proof no outcome-based selection occurred
Validation passed:
- coefficient-free source/artifact validation: True
- deterministic dry-run regeneration: True
- negative hidden outcome fields rejected: True
- dry-run proof flags reject candidate-pair Pearson, first-difference, covariance, p-values/significance, and preliminary result caches.

## 13. Local AI
Not used. Deterministic/manual metadata rules were sufficient. No local-AI infrastructure was built.

## 14. Verification results
- policy schema validation: True
- coefficient-free source/artifact validation: True
- Campaign 41 backward compatibility: True
- deterministic dry-run regeneration: True
- candidate-purpose/semantic validation: True
- batch-composition validation: True
- negative hidden outcome-field tests: True
- targeted policy tests: 10 passed in 0.48s
- complete test suite: 293 passed in 18.74s
- Python compilation: passed
- sensitive-material scan: 0 actual secret blockers; durability decision D from preserved unrelated residue
- coherence: blocks=[], warnings=['context health: context/active_context.md is 316.8 hours old; generated bundles are task-specific and should be regenerated when needed']
- context health: blocks=[], warnings=['context/active_context.md is 316.8 hours old; generated bundles are task-specific and should be regenerated when needed']
- architecture-to-reality audit: blocks=[], warnings=[]
- git diff --check: passed

## 15. Doctrine/architecture classification
Roadmap/policy refinement inside existing architecture. No Doctrine amendment, KnowledgeObjectPackage redesign, PostgreSQL schema change, new method implementation, Campaign 42, canonical package, or repository redesign.

## 16. Decision
A. successor policy is ready for a bounded Campaign 42 registry.

## 17. Smallest exact next task
Run a bounded Campaign 42 coefficient-free registry-freeze task using `pearson_candidate_policy_v2_mixed_roadmap@1.0`; stop before coefficient calculation, canonical packages, PostgreSQL writes/rebuilds, schema/doctrine changes, commit, or push.
