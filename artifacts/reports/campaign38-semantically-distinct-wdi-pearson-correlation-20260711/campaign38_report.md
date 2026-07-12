# Campaign 38 — Semantically Distinct WDI Pearson Correlation Pilot

Outcome: B — Successful with bounded operational pressure.

Frozen selection: DNK `SP.DYN.LE00.IN` life expectancy at birth, total (years) versus `SP.DYN.TFRT.IN` fertility rate, total (births per woman).
Selection decision fingerprint: `sha256:673084540acbd2fad36964951d3f9f2a0c26328af596867572c2b662770f8930`.

Coefficient: `-0.40932912178`.
Aligned pairs: 35.
Coverage: 1.

Package: `pkg-object-srcpkg-campaign38-dnk-life-expectancy-fertility-pearson-correlation-v1`.
Package manifest fingerprint: `sha256:73700b32f3cc0014fac70dbf7e2d16b7066373018ca2a3f4786988e521df27de`.
Repository count before: 528.
Repository count after: 529.
Repository fingerprint after: `sha256:d5bf5b56d3512aec3ae424e9daee05e09a22a50d77ad0633788175c2e97c1390`.

Construction risk: Life expectancy and fertility are distinct demographic measures with different units; no algebraic identity, direct component-total construction, shared denominator, or definitional embedding was found. Both are demographic model/statistical estimates, retained as a material methodology limitation.

Diagnostics, not promoted:
- series A vs annual time index: 0.991208102157
- series B vs annual time index: -0.414077438981
- first-difference sensitivity: -0.095578883279

Local AI: not retried; deferred until model-serving/routing evidence changes.
Campaign 39: not executed.


## Candidate selection summary

Frozen selected candidate: `demographic_life_expectancy_fertility_pair` for DNK.
Selection fingerprint: `sha256:673084540acbd2fad36964951d3f9f2a0c26328af596867572c2b662770f8930`.
Selection used metadata, unit, family-maturity, coverage, and interpretive-risk probes only; no coefficient was calculated before freeze.

Ranking:
- demographic_life_expectancy_fertility_pair: score 14, preferred entity DNK, coverage 35
- demographic_rate_pair: score 10, preferred entity DNK, coverage 35
- health_system_coverage_pair: score 10, preferred entity DNK, coverage 35
- education_coverage_pair: score 4, preferred entity SWE, coverage 24
- financial_depth_pair: score 2, preferred entity NOR, coverage 19

## PostgreSQL publication

PostgreSQL v1 rebuild and retrieval passed. Canonical/projected count: 529. Campaign 36-37 correlation objects remain retrievable: True. Retrieval friction: none requiring schema expansion or correlation-specific SQL fields.

## Governance-overhead result

Governance/support artifacts per substantive object: 15 / 1 = 15.0. Campaign 37 baseline was 9.0. The ratio is above the Campaign 37 replication baseline because Campaign 38 required frozen semantic selection evidence. This is bounded operational pressure, not doctrine/schema pressure.

## Outcome and next direction

Outcome: B — Successful with bounded operational pressure.

Recommended next direction: small heterogeneous correlation batch or correlation-family maturation assessment. Do not schedule another single-pair methodology pilot unless it tests a specific unresolved failure. Do not begin covariance or lag relationships yet.


## Final verification

Final verification artifacts are under `artifacts/reports/campaign38-semantically-distinct-wdi-pearson-correlation-20260711/final-verification/`.

Results:

- selection freeze verification: pass
- HTTPS/downgrade validation: pass
- unit resolution: pass
- offline fixture regeneration / no-promote rerun: pass
- normalization and alignment determinism: pass
- construction-risk checks: pass
- contract-fingerprint verification: pass
- independent coefficient recomputation: pass
- Decimal-context invariance: pass
- pair-order invariance: pass
- targeted Campaign 38 tests: pass
- full test suite: pass (`Ran 223 tests in 17.985s`, OK)
- Python compilation: pass
- repository validation: pass (529 objects)
- PostgreSQL rebuild and retrieval: pass
- historical-package immutability: pass
- coherence: 0 blocks, 1 stale-context warning
- context health: 0 blocks, 1 stale-context warning
- architecture-to-reality audit: 0 blocks, 0 warnings
- git diff --check: pass
- MacroForge dependency search: 0 runtime/package matches
- Campaign 39 production absence: pass
