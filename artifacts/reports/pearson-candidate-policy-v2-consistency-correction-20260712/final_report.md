# Pearson Candidate Policy v2 Consistency Correction and Transformation-Aware Sequencing Gate — Final Report

Date: 2026-07-12

## Decision

B. First-difference Pearson method validation should precede further raw production.

Do not freeze or execute Campaign 42 from the current evidence.

## 1. Cause of canonical candidates appearing in the dry-run

Cause: implementation/reporting defect.

The helper preserved a static prior-canonical/frozen exclusion inventory that ended at Campaign 40. It did not derive current canonical Pearson relationships from `knowledge_repository/objects/`, so four Campaign 41 relationships could reappear when the successor policy was run over the retained Campaign 40 evidence pool.

The four already canonical relationships in the historical output were:
- `swe_private_credit_mobile_cellular`
- `swe_private_credit_internet_users`
- `dnk_agricultural_land_broad_money`
- `dnk_agricultural_land_private_credit`

Trace artifact: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/inconsistency_trace.json`.

## 2. Whether that output was valid future-production evidence

No.

The seven-candidate output is now explicitly labeled historical comparison/audit output. It may show how v2 would have ranked the old pool under the historical exclusion set, but it is not a future-production candidate batch and must not justify a Campaign 42 registry freeze.

Artifact: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/dry-run/historical_comparison_not_candidate_batch.json`.

## 3. Exact correction

Implemented corrections:

1. Added current canonical Pearson relationship extraction from `knowledge_repository/objects/`.
2. Excluded current canonical relationships in future-production mode by same entity, raw/raw transformation, annual scope, and order-insensitive pair identity.
3. Added reversed-pair exclusion coverage through canonical sorted pair keys.
4. Split successor outputs into:
   - `historical_comparison`, not future-production evidence;
   - `future_production`, canonical-excluding eligibility output.
5. Added mode-boundary metadata so comparison mode cannot be mistaken for a production batch.
6. Corrected remote-cap arithmetic to use actual selected batch size.
7. Updated policy/spec, task, decision, roadmap, evolution log, state, and handoff artifacts.

Corrected files include:
- `tools/coefficient_free_pearson_candidate_registry.py`
- `tests/test_coefficient_free_pearson_candidate_registry.py`
- `specs/correlation_batches/pearson_candidate_policy_v2_mixed_roadmap.md`
- `artifacts/decisions/D-20260712-pearson-candidate-policy-v2-consistency-correction.md`
- `artifacts/tasks/T-20260712-pearson-candidate-policy-v2-consistency-correction.md`

## 4. Cause of the 25% cap violation

Cause: implementation/spec arithmetic defect.

The prior validation checked a nominal 8-candidate batch cap: `int(8 * 0.25) = 2`. The actual historical output contained only 7 selected candidates. Two remote candidates among seven is 28.5714%, which violates a literal 25% cap.

## 5. Corrected integer-cap semantics

Corrected rule:

`max_remote_count = floor(n * 0.25)`

where `n` is the actual selected ordinary-batch size.

No upward rounding is allowed if it would exceed the declared percentage.

Arithmetic proof:
- n=1 -> 0
- n=2 -> 0
- n=3 -> 0
- n=4 -> 1
- n=5 -> 1
- n=6 -> 1
- n=7 -> 1
- n=8 -> 2
- n=9 -> 2
- n=10 -> 2
- n=11 -> 2
- n=12 -> 3

Artifact: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/batch_composition_arithmetic_proof.json`.

## 6. Regression-test results

Targeted policy tests:
- 15 passed, 12 subtests passed.

Regression coverage added/proved:
- every currently canonical Pearson relationship is excluded from future-production mode;
- reversed canonical pairs are excluded;
- same entity/scope/transformation identity is handled through canonical sorted pair keys;
- comparison/audit mode cannot be mistaken for future-production mode;
- remote share never exceeds its declared cap in future-production mode;
- small-batch integer rounding is deterministic;
- Campaign 41 v1 registry/spec fingerprints remain unchanged;
- forbidden outcome fields remain rejected.

Policy consistency validation:
```json
{
  "campaign41_backward_compatibility_tests": true,
  "canonical_and_reversed_pair_exclusion_tests": true,
  "coefficient_free_validation": true,
  "comparison_mode_isolation_tests": true,
  "deterministic_regeneration": true,
  "future_purpose_distribution": {
    "cautionary_relationship_knowledge": 1,
    "transformation_companion_candidate": 3
  },
  "future_remote_share": 0.25,
  "future_selected_count": 4,
  "future_semantic_distribution": {
    "close": 3,
    "remote": 1
  },
  "future_time_risk_distribution": {
    "high": 4
  },
  "future_validation_expected_insufficient_batch": true,
  "hidden_outcome_field_negative_test": true,
  "historical_selected_count": 7,
  "remote_cap_arithmetic_tests": true,
  "remote_cap_examples": {
    "1": 0,
    "10": 2,
    "11": 2,
    "12": 3,
    "2": 0,
    "3": 0,
    "4": 1,
    "5": 1,
    "6": 1,
    "7": 1,
    "8": 2,
    "9": 2
  },
  "valid": true
}
```

## 7. Corrected historical comparison

Historical comparison selected 7 candidates. It is not a candidate batch.

Selected historical-comparison output:
- nor_crude_birth_rate_under5_mortality — canonical=False; semantic=close; time-risk=high; purpose=transformation_companion_candidate
- nor_crude_birth_rate_life_expectancy — canonical=False; semantic=close; time-risk=high; purpose=transformation_companion_candidate
- nor_crude_death_rate_under5_mortality — canonical=False; semantic=close; time-risk=high; purpose=transformation_companion_candidate
- swe_private_credit_mobile_cellular — canonical=True; semantic=moderate; time-risk=high; purpose=baseline_relationship_knowledge
- swe_private_credit_internet_users — canonical=True; semantic=moderate; time-risk=high; purpose=baseline_relationship_knowledge
- dnk_agricultural_land_broad_money — canonical=True; semantic=remote; time-risk=high; purpose=cautionary_relationship_knowledge
- dnk_agricultural_land_private_credit — canonical=True; semantic=remote; time-risk=high; purpose=cautionary_relationship_knowledge

Distribution:
- semantic: `{'close': 3, 'moderate': 2, 'remote': 2}`
- time-risk: `{'high': 7}`
- purpose: `{'baseline_relationship_knowledge': 2, 'cautionary_relationship_knowledge': 2, 'transformation_companion_candidate': 3}`
- remote share: 0.285714
- valid future-production evidence: `False`

Artifact: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/dry-run/historical_comparison_not_candidate_batch.json`.

## 8. Corrected future-production eligible set

Future-production mode selected 4 candidates after excluding current canonical Pearson relationships:
- nor_crude_birth_rate_under5_mortality — semantic=close; time-risk=high; purpose=transformation_companion_candidate; canonical=False
- nor_crude_birth_rate_life_expectancy — semantic=close; time-risk=high; purpose=transformation_companion_candidate; canonical=False
- nor_crude_death_rate_under5_mortality — semantic=close; time-risk=high; purpose=transformation_companion_candidate; canonical=False
- dnk_forest_area_private_credit — semantic=remote; time-risk=high; purpose=cautionary_relationship_knowledge; canonical=False

Validation status: `{'errors': ['fewer than 6 defensible future-production candidates remain'], 'valid': False}`.

The validation intentionally reports insufficient batch evidence because fewer than 6 defensible future-production candidates remain.

Artifact: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/dry-run/future_production_eligibility_excluding_canonical.json`.

## 9. Semantic/time-risk/purpose distribution of corrected future-production set

- semantic: `{'close': 3, 'remote': 1}`
- time-risk: `{'high': 4}`
- purpose: `{'cautionary_relationship_knowledge': 1, 'transformation_companion_candidate': 3}`
- remote count: 1
- selected count: 4
- remote share: 0.250000
- maximum remote count for actual selected size: 1

## 10. Whether a useful raw Campaign 42 batch remains possible

Not from the current retained 16-series evidence pool.

A raw Campaign 42 registry is technically possible only by weakening the corrected production gate or accepting a small high-time-risk batch. That would not materially advance the mixed-roadmap goal. The corrected future-production set contains only 4 candidates, all high time-risk, and 3 of them are explicitly transformation-companion candidates.

Conclusion: a useful raw-only Campaign 42 registry is not justified now.

## 11. Transformation-aware sequencing assessment

Existing production evidence supports first-difference method validation before further raw Pearson production:

- 14/14 numerically diagnosed Pearson objects are high time-risk.
- Five strong raw relationships have weak first-difference relationships.
- Campaign 41 produced 8/8 high-risk, semantically remote relationships.
- Corrected future-production v2 output contains 4/4 high-time-risk candidates.
- First-difference diagnostics already exist as non-promoted deterministic calculations.
- PostgreSQL and export paths already expose diagnostic data.

Assessment against options:

A. Freeze corrected raw Campaign 42 registry — reject now; corrected future-production evidence is too small and all high time-risk.
B. Validate first-difference Pearson method contract — adopt; narrowest justified next task.
C. Validate generic transformation-aware relationship contract — defer/reject for now; too broad without repeated evidence beyond first differences.
D. Prioritize standalone deterministic trend descriptors first — defer; useful later, but existing first-difference evidence is more directly tied to relationship weakness.
E. New neutral evidence release — defer; current evidence is sufficient for method-boundary validation.
F. Preserve roadmap without selecting implementation task — reject; enough evidence exists to select a bounded next task.

## 12. Proposed first-difference method boundary

No implementation was performed. Proposed validation boundary only:

Input contract:
- accepted retained annual scalar evidence fixtures;
- same entity;
- same frequency: annual;
- same raw source period scope before transformation;
- resolved units;
- deterministic observed-period alignment;
- retained raw fixture and normalized-observation fingerprints;
- explicit method contract identity distinct from raw Pearson.

Deterministic transformation formula:
- for each series value `x_t`, compute `delta_x_t = x_t - x_(t-1)`.
- only adjacent observed annual periods are eligible.

Period-label semantics:
- transformed observation is labeled by ending period `t`.
- it represents change from `t-1` to `t`.

Missing-value behavior:
- if either `x_t` or `x_(t-1)` is missing, `delta_x_t` is missing.
- pairwise relationship alignment occurs after transformation.

Minimum transformed overlap:
- must be separately validated; initial candidate threshold should be no weaker than raw Pearson's reproducibility intent.
- proposed validation question: whether to require at least 30 aligned transformed pairs or a justified lower threshold given one-period loss.

Unit semantics:
- transformed unit is original unit per year-to-year change, not a rate unless original unit already denotes a rate/percentage.
- package text must distinguish level correlation from change correlation.

Zero/negative-value considerations:
- first differences allow zero and negative transformed values.
- no division by zero occurs.
- bounded-ratio indicators can produce interpretable positive/negative percentage-point changes but require explicit unit labeling.

Fingerprint inputs:
- source normalized observations and fingerprints;
- transformation formula/version;
- period-label convention;
- missing-value rule;
- transformed observation table/fingerprint;
- alignment keys and aligned transformed periods;
- method contract fingerprint;
- engine/runtime version where applicable.

Provenance requirements:
- retain raw source provenance;
- retain deterministic transformation provenance;
- retain transformed-series fingerprint;
- retain relationship calculation fingerprint;
- record that first-difference package is a companion method, not a replacement for raw-level package.

Distinctions:
- raw Pearson package: correlation over raw levels.
- first-difference companion package: correlation over deterministic year-to-year changes.
- non-promoted diagnostic: internal/diagnostic calculation not canonicalized as knowledge object.

Architecture fit:
- existing KnowledgeObjectPackage can represent the method as a distinct method contract and generated statement without redesign.
- existing PostgreSQL projection can represent it unchanged as another package/statement/method identity; no schema change justified.

## 13. Existing package/PostgreSQL architecture sufficiency

Confirmed sufficient.

No Doctrine amendment, KnowledgeObjectPackage redesign, PostgreSQL schema change, repository redesign, package mutation, or PostgreSQL write/rebuild is justified by this corrective task.

## 14. Complete verification results

Verification folder: `artifacts/reports/pearson-candidate-policy-v2-consistency-correction-20260712/final-verification/`

Results:
- policy consistency validation: passed.
- targeted canonical/reversed/mode/cap/fingerprint/outcome tests: 15 passed, 12 subtests passed.
- complete test suite: 298 passed, 12 subtests passed in 19.45s.
- Python compilation: passed.
- sensitive-material scan: 0 actual secret blockers; durability validator still returns decision D due preserved unrelated untracked/recovery-critical residue.
- coherence check: no blocks; warning only for stale generated `context/active_context.md`.
- context-health check: no blocks; warning only for stale generated `context/active_context.md`.
- architecture-to-reality audit: no blocks, no warnings.
- git diff --check: passed.

## 15. Doctrine/architecture classification

Classification: corrective roadmap/policy decision inside existing architecture.

No:
- Campaign 42 registry freeze;
- Campaign 42 calculation;
- new Pearson or first-difference coefficients;
- canonical package creation or mutation;
- PostgreSQL write/rebuild/schema change;
- Doctrine amendment;
- KnowledgeObjectPackage redesign;
- broad transformation framework;
- broad local-AI infrastructure;
- commit or push;
- destructive cleanup.

## 16. Final decision

B. First-difference Pearson method validation should precede further raw production.

## 17. Smallest exact next task

Validate a bounded first-difference Pearson method contract using existing retained evidence and existing diagnostic evidence.

Stop before:
- coefficient production for canonical use;
- canonical package creation;
- PostgreSQL writes/rebuilds;
- schema changes;
- Doctrine changes;
- KnowledgeObjectPackage redesign;
- broad transformation-framework design;
- commit or push.
