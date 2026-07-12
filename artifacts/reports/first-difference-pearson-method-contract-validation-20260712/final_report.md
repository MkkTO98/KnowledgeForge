# First-Difference Pearson Method Contract Validation Report

Date: 2026-07-12
Status: complete
Decision: A — method is validated and ready for a bounded canonical companion-production campaign, with the explicit scope that production is not performed by this task.

## 1. Final identifiers

- Transformation identifier: `wdi_annual_scalar_first_difference_v1`
- Transformation version: `1.0`
- Transformation contract fingerprint: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`
- Method identifier: `wdi_annual_scalar_first_difference_pearson_v1`
- Method version: `1.0`
- Method identity: `wdi_annual_scalar_first_difference_pearson_v1@1.0`
- Method contract fingerprint: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`

The method identifier is consistent with existing KnowledgeForge WDI annual-scalar Pearson naming while preserving the existing raw Pearson identifier as the base method.

## 2. Transformation formula and period semantics

Formula: `delta_x_t = x_t - x_(t-1)`.

The transformed observation is labeled by ending annual period `t` and represents the absolute change from `t-1` to `t`.

## 3. Missingness and gap behavior

- `t` and `t-1` must both be present, valid, and consecutive annual periods.
- The transformer does not bridge gaps.
- If 2001 is missing, a 2002 transformed value is not calculated from 2000.
- Duplicate entity-indicator-period keys fail closed.
- Non-finite inputs and non-finite transformed outputs fail closed.
- Transformation occurs before pairwise alignment.
- Pairwise alignment is by entity and ending transformed period.

## 4. Unit semantics

First differences are absolute differences in the original unit, not ratios.

Examples encoded in tests/specification:

- percent-of-GDP level -> year-to-year change in percentage points of GDP;
- percentage-share level -> year-to-year percentage-point change;
- per-100/per-1,000 rate -> absolute year-to-year change in that rate;
- currency level -> year-to-year change in the same currency unit;
- count level -> year-to-year change in count.

The method forbids labeling first differences as percentage growth, percent change, growth rate, or elasticity. No division-by-zero behavior is involved.

## 5. Minimum-overlap and coverage decision

Selected validation threshold:

- minimum aligned transformed observations: `30`;
- minimum transformed coverage: `0.85`.

Justification: Retained 1990-2024 annual fixtures have at most 34 first differences; 30 preserves raw Pearson v1's minimum evidentiary intent while allowing one-period transformation loss and limited retained missingness. This validation accepts the threshold for bounded companion production; future broader source classes may require revalidation.

This task validates the threshold for the retained WDI annual-scalar 1990-2024 evidence shape. Broader evidence classes require later revalidation.

## 6. Precision and rounding contract

- Decimal local context precision: `50`;
- rounding: `ROUND_HALF_EVEN`;
- canonical decimal places: `12`;
- canonical serialization strips insignificant trailing zeros and forbids scientific notation;
- zero transformed variance fails closed;
- non-finite Pearson results fail closed;
- population/sample covariance convention is inherited from raw Pearson v1 because covariance scaling cancels in Pearson r.

## 7. Fingerprints

Method and transformation fingerprints:

- transformation contract: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`;
- method contract: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`;
- validation registry: `sha256:100a0218aab154bf89f165ea0b39b278fd479e02c72d0af6d93a70a4974f1470`;
- validation case results: `sha256:4cb23b73311759f0f4f58278d7db4392fb56775fde5c3821fa9aa13c9487fe3d`;
- diagnostic reconciliation: `sha256:0051ab08bcef6ba5e6cfde1511598ac84653a7c30d24448a0078c73a94ec56af`;
- negative-case evidence: `sha256:46da90b75a5385ad4e2e0e156925781143bd1f88e7257a0b51009f5253380fcb`.

Fingerprint sensitivity proof:

- formula change affects method contract: `True`;
- input-order invariant: `True`;
- separate-process invariant: `True`;
- aligned-observation fingerprint: `sha256:b51e8a7355371099e987edea576b4323d34a26711e63f711c8cb36d58ad3acf5`.

## 8. Frozen validation cases

Registry: `artifacts/reports/first-difference-pearson-method-contract-validation-20260712/validation_registry.json`

Registry fingerprint: `sha256:100a0218aab154bf89f165ea0b39b278fd479e02c72d0af6d93a70a4974f1470`

The registry is coefficient-free and was frozen before validation coefficients were calculated. It includes multiple entities, close/remote pairs, strong-raw/weak-first-difference example, missing and complete coverage, and synthetic negative cases.

## 9. Validation coefficients

- `close_complete_nor_birth_under5`: -0.003511112671 over 34 aligned transformed observations; fingerprint `sha256:768f331dd6b7f093854c1bf0f1803878d05f47d8fda12f3db523a7c18eb86c91`
- `remote_missing_dnk_forest_broad_money`: -0.101990610667 over 33 aligned transformed observations; fingerprint `sha256:0620e0fb2ef601270e099e1c0ca6e6082d4d22487ea92f2291359cc3e80cbcc3`
- `strong_raw_weak_diff_swe_credit_internet`: 0.141137912446 over 34 aligned transformed observations; fingerprint `sha256:2c110fa049c75eac08a32bfa0942b1dae32d92cf382a9ae07bdb489c3271d9ea`
- `close_nor_birth_life`: 0.388758387248 over 34 aligned transformed observations; fingerprint `sha256:4aa52a1122f5461f2d5bb87a8cb136fe65d862e0c31cd12fd0138630aa6598e4`

## 10. Independent recomputation

The reusable implementation and independent reference oracle agreed at canonical precision in targeted tests. Separate-process deterministic recomputation also returned the same result fingerprint for the SWE private-credit/internet-users case.

## 11. Prior diagnostic reconciliation

Compared objects: `14`

Mismatches: `0`

- `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1`: prior -0.017407835395; recomputed -0.017407835395; match=True (exact_decimal_match); n=33
- `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1`: prior -0.289912537517; recomputed -0.289912537517; match=True (exact_decimal_match); n=34
- `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1`: prior -0.204185174675; recomputed -0.204185174675; match=True (exact_decimal_match); n=31
- `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1`: prior -0.083567273412; recomputed -0.083567273412; match=True (exact_decimal_match); n=34
- `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1`: prior -0.207863151096; recomputed -0.207863151096; match=True (exact_decimal_match); n=34
- `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1`: prior 0.402109713928; recomputed 0.402109713928; match=True (exact_decimal_match); n=34
- `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1`: prior -0.018892915467; recomputed -0.018892915467; match=True (exact_decimal_match); n=33
- `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1`: prior 0.058190335423; recomputed 0.058190335423; match=True (exact_decimal_match); n=33
- `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1`: prior -0.101990610667; recomputed -0.101990610667; match=True (exact_decimal_match); n=33
- `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1`: prior 0.03778166456; recomputed 0.037781664561; match=True (new_value_matches_when_quantized_to_prior_11_decimal_places); n=33
- `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1`: prior -0.083376899169; recomputed -0.083376899169; match=True (exact_decimal_match); n=33
- `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1`: prior 0.3855860099; recomputed 0.3855860099; match=True (exact_decimal_match); n=31
- `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1`: prior 0.141137912446; recomputed 0.141137912446; match=True (exact_decimal_match); n=34
- `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1`: prior 0.161115218727; recomputed 0.161115218727; match=True (exact_decimal_match); n=34

No existing canonical raw package was updated. The reconciliation confirms the new reusable method reproduces existing non-promoted diagnostics exactly or at prior stored canonical precision.

## 12. Negative-case evidence

- `negative_non_consecutive_gap_no_bridge`: pass
- `negative_duplicate_period`: expected_fail — duplicate entity-indicator-period key
- `negative_unresolved_unit`: expected_fail — unresolved unit
- `negative_non_finite`: expected_fail — non-finite decimal value
- `negative_zero_variance`: expected_fail — zero variance transformed series
- `negative_insufficient_overlap`: expected_fail — insufficient aligned transformed observations

Negative evidence is stored at `artifacts/reports/first-difference-pearson-method-contract-validation-20260712/negative_case_evidence.json`.

## 13. Determinism results

- different ambient Decimal precision/rounding: passed by local-context isolation in tests;
- reordered raw inputs: passed;
- reordered aligned observations: passed through sorted-period canonicalization;
- repeated runs: passed;
- separate processes: passed;
- different temporary paths: no path-dependent method output was used for calculation identity.

## 14. Raw/companion/diagnostic distinction

1. Raw-level Pearson package: canonical raw-level relationship package using `wdi_annual_scalar_pearson_correlation_v1` semantics over raw aligned levels.
2. First-difference Pearson companion package: independently reproducible package using `wdi_annual_scalar_first_difference_pearson_v1` over transformed aligned first differences. It has its own method identity, transformed series fingerprints, aligned observation fingerprint, coefficient, limitations, and package fingerprint.
3. Non-promoted first-difference diagnostic embedded in a raw package: diagnostic limitation metadata only. It is not independently retrievable as a canonical relationship object and must not be treated as production companion knowledge.

A companion package must not supersede or rewrite the raw package, declare the raw result incorrect, imply causation, imply stationarity, imply statistical significance, make forecasts, or claim mechanism.

## 15. Companion-link representation result

Existing representation is sufficient. The simulated companion payload uses existing structured payload and provenance fields, including `companion_raw_package_id`, method identity/version, transformation state, raw/transformed period scopes, provenance envelope, limitations, and package fingerprints.

No new KnowledgeObjectPackage field is required.

## 16. PostgreSQL/export compatibility result

Representation simulation result:

- package representation valid: `True`;
- PostgreSQL projection compatible: `True`;
- Relationship Export Contract compatible: `True`;
- schema change required: `False`;
- new package field required: `False`.

No production PostgreSQL write, rebuild, or schema expansion was performed.

## 17. Statistical limitations

Every future method output must preserve these non-claims:

- causation
- stationarity
- statistical significance
- prediction
- forecast
- investment signal
- lead-lag structure

Expanded limitation text is encoded in the simulated package and implementation.

## 18. Verification status

Final verification outputs are stored under:

`artifacts/reports/first-difference-pearson-method-contract-validation-20260712/final-verification/`

Results:

- targeted first-difference tests: 8 passed, 5 subtests passed;
- complete test suite: 306 passed, 17 subtests passed;
- Python compilation: passed;
- method validation assertions: passed;
- artifact recomputation: passed;
- sensitive-material scan: 0 findings;
- coherence check: no blocks; stale generated `context/active_context.md` warning only;
- context-health check: no blocks; stale generated `context/active_context.md` warning only;
- architecture-to-reality audit: no blocks, no warnings;
- git diff --check: passed.

## 19. Doctrine and architecture classification

Classification: bounded deterministic method validation within existing architecture.

No Production Doctrine amendment, package redesign, PostgreSQL schema change, repository mutation, canonical package production, Campaign 42 execution, export publication, provider acquisition, MacroForge/InsightForge access, local AI use, commit, or push was performed.

## 20. Decision

A. The method is validated and ready for a bounded canonical companion-production campaign.

The next task must still be separately authorized and must freeze a coefficient-free companion-production registry before calculating production companion packages.

## 21. Smallest exact next task

Create a coefficient-free bounded first-difference Pearson companion-production registry for selected existing raw Pearson packages, preserving raw package immutability and stopping before coefficient calculation or canonical package publication.
