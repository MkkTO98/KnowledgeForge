# Campaign 41 — Generic Correlation Engine Provenance Parameterization

Decision: A — generic engine is ready to execute the frozen Campaign 41 batch.

No Campaign 41 coefficient, covariance, significance, lag, trend, forecast, canonical package, PostgreSQL write/rebuild, relationship export, Campaign 42, commit, or push was performed.

## 1. Exact hardcoded fields removed
- statement ID prefix
- calculation dependency ID
- evidence reference ID
- validation judgment
- generated-statement origin
- provenance-lineage basis text

Removed from generic runtime `tools/correlation_batch_engine.py` and replaced with validated spec-level `package_provenance` metadata.

## 2. Specification-contract changes
Added required `package_provenance` metadata for production candidate specs:
- identity_namespace
- statement_id_template
- calculation_id_template
- evidence_ref_id_template
- validation_judgment
- statement_origin
- lineage_basis
- production_family_identity optional

Campaign 40 spec was minimally amended with metadata reproducing its existing output exactly. Campaign 41 original frozen spec was preserved unchanged and a successor readiness spec was created.

## 3. Deterministic derivation rules
- Allowed template fields: `campaign_id`, `identity_namespace`, `candidate_id`, `candidate_id_dash`.
- Generated IDs are rendered from templates, then validated by strict identifier rules.
- IDs must be deterministic, batch-unique, namespace-consistent with `expected_package_id`, non-path-like, and free of consumer-project terminology.
- Unknown template fields, duplicate generated IDs, missing metadata, malformed metadata, and campaign/package inconsistency fail closed.
- Numerical calculation remains independent from ID/provenance construction.

## 4. Campaign 40 compatibility result
- Accepted/rejected in no-publish compatibility run: 6 accepted, 2 rejected.
- Publication performed: False. PostgreSQL performed: False.
- All generated accepted package payloads identical to canonical Campaign 40 packages: True.
- `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1`: payload identical=True; statement `stmt-campaign40-agriculture-agricultural-forest-land-dnk-pearson-v1`; calculation `calc-campaign40-agriculture_agricultural_forest_land_dnk-pearson-v1`; evidence `ev-campaign40-agriculture_agricultural_forest_land_dnk-fixture`; fingerprint `sha256:40120d047386d0bcc224f57fc3ac311353099e1937a6b77aa494e7fa6ee1cab7`.
- `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1`: payload identical=True; statement `stmt-campaign40-demographic-birth-death-rates-nor-pearson-v1`; calculation `calc-campaign40-demographic_birth_death_rates_nor-pearson-v1`; evidence `ev-campaign40-demographic_birth_death_rates_nor-fixture`; fingerprint `sha256:17179471915a64d7c51979b3f8498e72913b2b6355356044f7ef7f9287923481`.
- `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1`: payload identical=True; statement `stmt-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-v1`; calculation `calc-campaign40-energy_fossil_nonhydro_renewables_nor-pearson-v1`; evidence `ev-campaign40-energy_fossil_nonhydro_renewables_nor-fixture`; fingerprint `sha256:d0bcf30588c6a5e3ef92bc9b3834fa26a357a056fa7b68812f476c63d74e9c01`.
- `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1`: payload identical=True; statement `stmt-campaign40-finance-credit-broad-money-dnk-pearson-v1`; calculation `calc-campaign40-finance_credit_broad_money_dnk-pearson-v1`; evidence `ev-campaign40-finance_credit_broad_money_dnk-fixture`; fingerprint `sha256:0e58c5e0f15b3700cf816c4d1dc1381967d91c064cdda322df4ac7d6fa88e2e1`.
- `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1`: payload identical=True; statement `stmt-campaign40-health-life-expectancy-under5-mortality-nor-pearson-v1`; calculation `calc-campaign40-health_life_expectancy_under5_mortality_nor-pearson-v1`; evidence `ev-campaign40-health_life_expectancy_under5_mortality_nor-fixture`; fingerprint `sha256:f84032acffae0a2144f361f926afe20bd2413b7261b7ae26565a6f22f19ca2bd`.
- `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1`: payload identical=True; statement `stmt-campaign40-infrastructure-internet-mobile-swe-pearson-v1`; calculation `calc-campaign40-infrastructure_internet_mobile_swe-pearson-v1`; evidence `ev-campaign40-infrastructure_internet_mobile_swe-fixture`; fingerprint `sha256:3ece432a998571df10d429e4cd68529b95b4806764df77fc0d626dc644b9ce29`.

## 5. Campaign 41 registry immutability result
- Registry fingerprint expected/matched: sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc / True.
- Frozen candidate registry was not modified.
- Original frozen spec fingerprint expected/matched: sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2 / True.

## 6. Campaign 41 specification disposition and fingerprint
- Original frozen spec preserved unchanged: `specs/correlation_batches/campaign41_coefficient_free_pearson_batch_spec.json`.
- Historical copy preserved: `artifacts/reports/campaign41-generic-correlation-engine-provenance-parameterization-20260712/campaign41_original_frozen_spec_preserved.json`.
- Successor readiness spec: `specs/correlation_batches/campaign41_ready_pearson_batch_spec.json`.
- Successor readiness spec fingerprint: `sha256:c292ac73bdb92dd9b89e8c9dcad7a64675ad7d814e4149cea828b408bbeea0c6`.
- Successor readiness spec byte SHA-256: `sha256:3ee44bcfa024c3999ad11a60343760585ac43957b745d8f3b2eb743d5e7a918d`.
- Change type: non-candidate provenance metadata only.

## 7. Candidate set and expected package IDs unchanged
- `dnk_agricultural_land_broad_money` unchanged=True; expected package `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1`.
- `nor_fossil_electricity_under5_mortality` unchanged=True; expected package `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1`.
- `swe_private_credit_mobile_cellular` unchanged=True; expected package `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1`.
- `dnk_agricultural_land_private_credit` unchanged=True; expected package `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1`.
- `nor_nonhydro_renewable_electricity_under5_mortality` unchanged=True; expected package `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1`.
- `swe_private_credit_internet_users` unchanged=True; expected package `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1`.
- `dnk_forest_area_broad_money` unchanged=True; expected package `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1`.
- `nor_crude_birth_rate_fossil_electricity` unchanged=True; expected package `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1`.
- All candidate identities/order/evidence/transformations/expected package IDs unchanged: True.

## 8. Campaign 41 engine-readiness result
- Ready spec validation: True.
- Candidate count: 8.
- Unique generated statement/calculation/evidence IDs: True.
- Coefficient-free validation: True; forbidden result paths: [].

## 9. Time-index diagnostic readiness
- All eight candidates can receive diagnostic-only annual time-index series using candidate entity: True.
- Diagnostic path is generic and not campaign-specific.
- Diagnostic metadata remains non-promoted and can be represented through existing `diagnostic_limitations` package structure.
- Campaign 41 diagnostics were not calculated.

## 10. Remaining campaign-specific runtime literals
- Remaining Campaign 40/41 literals in `tools/correlation_batch_engine.py`: 0.
- Classification: none remain in generic runtime code. Campaign-specific literals remain only in versioned specs/tests/artifacts as expected.

## 11. Negative-test results
Focused tests passed for missing provenance metadata, malformed/path-like metadata, unknown template field, cross-candidate ID collision, campaign/package identity inconsistency, deterministic IDs, unique IDs, Campaign 41 no-calculation validation, and candidate entity time-index construction.

## 12. Complete verification results
- Python compilation: passed (`python3 -m compileall -q tools tests`).
- Targeted engine/provenance/coefficient-free tests: 24 passed in 0.32s.
- Full test suite: 289 passed in 19.60s.
- Campaign 40 no-publish compatibility: package payload and fingerprints identical.
- Campaign 41 readiness/immutability/coefficient-free checks: passed.
- Sensitive scan: actual secret blockers 0; unsafe absolute-path dependencies 0; known durability validator D remains due unrelated untracked recovery-critical implementation and non-machine-loss operational checkpoint residuals.
- Context health: no blocks; stale generated `context/active_context.md` warning only.
- Coherence: no blocks; stale generated context warning only.
- Architecture-to-reality audit: 0 blocks, 0 warnings.
- Git diff checks: `git diff --check` and `git diff --cached --check` passed.
- Canonical repository unchanged: 538 packages, fingerprint `sha256:958c88d4be0bce735adcaaf3f236a7643aa80fd79846db23f4b521d05459771b`.

## 13. Doctrine/architecture classification
- Doctrine Review Trigger: not reached.
- Architecture drift: not detected.
- KnowledgeObjectPackage redesign: not required.
- PostgreSQL schema expansion: not required.
- Change is bounded reusable parameterization of an existing generic engine.

## 14. No calculation or publication confirmation
- campaign41_coefficients_calculated: False
- canonical_packages_created: False
- postgresql_written_or_rebuilt: False
- relationship_export_run: False
- campaign42_started: False
- commit_or_push: False

## 15. Decision
A. generic engine is ready to execute the frozen Campaign 41 batch.

## 16. Smallest exact next task
Execute Campaign 41 using exactly `specs/correlation_batches/campaign41_ready_pearson_batch_spec.json`, retained validated fixtures/offline reuse, no PostgreSQL write unless separately authorized, and publish only if the next task explicitly authorizes coefficient calculation and canonical package creation.
