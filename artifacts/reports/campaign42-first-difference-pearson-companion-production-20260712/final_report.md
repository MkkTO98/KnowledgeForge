# Campaign 42 — First-Difference Pearson Companion Production Final Report

Date: 2026-07-12
Outcome: A. successful end-to-end companion production

## 1. Frozen registry/specification verification

- Registry fingerprint: sha256:be7a085b5a74860c9a6c95fb2c9e6f45a066679d317fc743694959d502e3dc15 (verified)
- Specification fingerprint: sha256:ec3eaf0f735a888bc01f9cf394f015dd87eab3096be2690e75de0c4ec6f86d00 (verified)
- Transformation contract: wdi_annual_scalar_first_difference_v1@1.0 / sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f
- Method contract: wdi_annual_scalar_first_difference_pearson_v1@1.0 / sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade
- Gate checks: 43 passed, 0 failed

## 2-6. Candidate transformation coverage, coefficient, recomputation, diagnostic reconciliation, decision

| Candidate | Raw package | Companion package | Aligned transformed count | Coverage | Coefficient | Recompute | Prior diagnostic | Decision |
|---|---|---|---:|---:|---:|---:|---|---|
| campaign42-fd-pearson-companion-candidate-01 | `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-first-difference-pearson-companion-v1` | 33 | 1.000000000000 | -0.017407835395 | -0.017407835395 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-02 | `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-first-difference-pearson-companion-v1` | 34 | 1.000000000000 | -0.083567273412 | -0.083567273412 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-03 | `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-first-difference-pearson-companion-v1` | 34 | 1.000000000000 | -0.289912537517 | -0.289912537517 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-04 | `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-first-difference-pearson-companion-v1` | 31 | 1.000000000000 | -0.204185174675 | -0.204185174675 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-05 | `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-first-difference-pearson-companion-v1` | 34 | 1.000000000000 | -0.207863151096 | -0.207863151096 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-06 | `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-first-difference-pearson-companion-v1` | 34 | 1.000000000000 | 0.402109713928 | 0.402109713928 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-07 | `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1` | `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-first-difference-pearson-companion-v1` | 34 | 1.000000000000 | 0.141137912446 | 0.141137912446 | coefficient_match=True; aligned_count_match=True | accepted |
| campaign42-fd-pearson-companion-candidate-08 | `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1` | `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-first-difference-pearson-companion-v1` | 34 | 1.000000000000 | 0.161115218727 | 0.161115218727 | coefficient_match=True; aligned_count_match=True | accepted |

## 7. Accepted companion package IDs and fingerprints

| Companion package ID | Package manifest fingerprint |
|---|---|
| `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-first-difference-pearson-companion-v1` | `sha256:4aeb7776f59f69fb3eec2efca2bf7c1497be75fe83327bf1214e70fe00d20c55` |
| `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-first-difference-pearson-companion-v1` | `sha256:cbfda58034bcd6adfaba9449329f456db50ff2bcca69c50777e9832e690bd363` |
| `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-first-difference-pearson-companion-v1` | `sha256:6ae0f4a51759ff352d9823f336f17ad769652e78ddff9b91d81ce48110fa62d1` |
| `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-first-difference-pearson-companion-v1` | `sha256:c3a6b619dfdea2f06cf59201bb2e0e5a50e6a2365b922f0f93b3a23c91e3dce9` |
| `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-first-difference-pearson-companion-v1` | `sha256:de392b810557a68a948a37b61b81ca6a155a5ce0af9e94c32f4b3aef78be83d8` |
| `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-first-difference-pearson-companion-v1` | `sha256:0b09ca3e2c290c98be2096bd9b6420ecf78a67c92538bfe1e30bc696909ff16d` |
| `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-first-difference-pearson-companion-v1` | `sha256:d271bbc1e59088992a648d8551c49be46ca336d86e959f918d0366683121dd9d` |
| `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-first-difference-pearson-companion-v1` | `sha256:210f01be2a171e40108602a51f76f6aec758e3ae3eb2cfbf9721ed5938c610b9` |

## 8. Raw-to-companion links

| Raw package | Companion package |
|---|---|
| `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1` | `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-first-difference-pearson-companion-v1` |
| `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1` | `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-first-difference-pearson-companion-v1` |

## 9. Transformed-unit semantics

- campaign42-fd-pearson-companion-candidate-01: series_a=year-to-year percentage-point change in % of land area; series_b=year-to-year percentage-point change in % of land area
- campaign42-fd-pearson-companion-candidate-02: series_a=year-to-year change in percentage points of GDP; series_b=year-to-year change in percentage points of GDP
- campaign42-fd-pearson-companion-candidate-03: series_a=absolute year-to-year change in per 1,000 people; series_b=absolute year-to-year change in per 1,000 people
- campaign42-fd-pearson-companion-candidate-04: series_a=year-to-year percentage-point change in % of total; series_b=year-to-year percentage-point change in % of total
- campaign42-fd-pearson-companion-candidate-05: series_a=absolute year-to-year change in years; series_b=absolute year-to-year change in per 1,000 live births
- campaign42-fd-pearson-companion-candidate-06: series_a=year-to-year percentage-point change in % of population; series_b=absolute year-to-year change in per 100 people
- campaign42-fd-pearson-companion-candidate-07: series_a=year-to-year change in percentage points of GDP; series_b=year-to-year percentage-point change in % of population
- campaign42-fd-pearson-companion-candidate-08: series_a=year-to-year change in percentage points of GDP; series_b=absolute year-to-year change in per 100 people

## 10. Limitations and non-claims

- Independently reproducible first-difference companions; they do not supersede or correct raw Pearson packages.
- They answer annual-change co-movement, not level co-movement.
- First differencing does not prove stationarity.
- Correlation does not imply causation.
- No significance, forecast, mechanism, lead-lag, recommendation, or investment signal is implied.
- Differencing may amplify noise.
- Results remain window- and revision-dependent.

## 11. Repository count and fingerprint before/after

- Before: 546 packages / sha256:c89c25ede69ec88a12f4791dba94b6199f2927721d0028420a65a74dd6ee735c
- After: 554 packages / sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b
- After classification: raw Pearson objects = 21; first-difference Pearson companions = 8; statistical-summary objects = 4.

## 12-14. Immutability, non-supersession, deterministic/idempotent rerun

- Pre-existing package immutability: True (changed_existing=[]; disappeared=[])
- Raw package non-supersession: True; all companion lineage previous_package_id is null and payload states does_not_supersede_raw_package=true.
- Idempotent republish: collision_safe=True; count=554; fingerprint=sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b

## 15-17. PostgreSQL and consumer-neutral export

- PostgreSQL validation: True; active projection count=554; repository fingerprint=sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b
- PostgreSQL exact retrieval, payload fidelity, package fingerprint fidelity, method/entity/indicator/lifecycle/provenance/package-fingerprint filters, and raw-to-companion navigation passed.
- Raw-vs-first-difference separation passed: first-difference transformation filter returns exactly 8 companions; raw Pearson method filter returns 21 and excludes companions.
- Relationship Export Contract + independent consumer simulation: True; consumers retrieved all eight, one exact companion, entity, either-indicator, transformation, method, raw reference, coefficient, period scope, transformed units, limitations/provenance, and zero-result queries deterministically.

## 18. Campaign 42 provenance clarity despite inherited ID stems

- Package IDs preserve frozen inherited raw-source campaign stems by authorization.
- Each companion package lineage records source_campaign=Campaign 42 and referenced_raw_source_campaign separately.
- Payload and provenance envelope include Campaign 42 registry and specification fingerprints; consumers need not infer production campaign from the inherited identifier stem.

## 19. Verification results

- Pre-execution gate: passed.
- Transformation/gap/unit/method/recompute/diagnostic/package checks: passed via `tests/test_campaign42_first_difference_companion_production.py` and production report.
- PostgreSQL projection/retrieval validation: passed.
- Relationship export and consumer simulation: passed.
- Targeted Campaign 42 production tests: passed (`5 passed in 1.32s`).
- Full test suite: passed (`316 passed, 17 subtests passed in 21.86s`).
- Python compilation: passed (`compileall-ok`).
- Repository-wide durability/sensitive scan: decision `D`; no actual secret blockers and no unsafe absolute-path dependencies, but durability is not complete because canonical/recovery-critical files remain untracked and operational checkpoint state is not machine-loss durable until commit/off-host backup.
- Coherence: passed with warnings only; no blocks.
- Context health: passed with warnings only; no blocks. After closeout handoff compaction, the remaining warning is stale generated `context/active_context.md` only.
- Architecture-to-reality audit: passed; `0 block(s), 0 warning(s)`; report `artifacts/reports/R-20260712-architecture-reality-audit.md`.
- `git diff --check`: passed.
- Final verification command outputs are recorded under `artifacts/reports/campaign42-first-difference-pearson-companion-production-20260712/final_verification/`.

Durability caveat: Campaign 42 production is complete, but repository durability is not complete until the new/modified canonical packages, specs, source/tests, task/decision/report/state records, and recovery-critical operational state are reviewed and committed/pushed or backed up according to the durability policy. No commit or push was performed.

## 20. Doctrine/architecture classification

- Doctrine amendment: not required.
- Architecture pressure: no redesign pressure reached.
- Canonical schema expansion: not performed.
- PostgreSQL schema expansion: not performed.
- This is bounded production using an approved companion-package pattern and existing PostgreSQL/export mechanisms.

## 21. Review trigger

- Review trigger reached: no Doctrine Review Trigger. Routine architecture-to-reality audit was run because closeout verification requested it and the repository crossed a canonical publication batch.

## 22. Outcome

A. successful end-to-end companion production

## 23. Smallest exact next task

Campaign 43 should not begin until a bounded post-Campaign-42 readiness gate verifies repository/report durability and decides whether the next production slice should expand first-difference companions or return to raw Pearson candidate production.
