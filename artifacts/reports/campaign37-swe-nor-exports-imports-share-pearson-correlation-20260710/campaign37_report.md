# Campaign 37 — SWE/NOR Exports-Imports Share Pearson Correlation Replication

Outcome: A — Successful controlled replication.

Evidence decision: fresh_reacquisition — Campaign 35 contains exports-share evidence only under a statistical-summary selection contract; Campaign 37 requires a consolidated dual-series correlation fixture with imports companion evidence and directly comparable metadata. Reuse conditions are therefore cumbersome/uncertain, so fresh bounded exports/imports evidence was acquired.

Accepted packages: 2

Coefficients:
- SWE: `0.968490740983`
- NOR: `-0.477418804478`

Repository count before: 526
Repository count after: 528
Repository fingerprint after: `sha256:c2d9842ccdc97863f9e704b04c3cdeaf405a4a1d0bb48b5976e263af9bb11e30`

Method: `wdi_annual_scalar_pearson_correlation_v1@1.0`
Contract fingerprint: `sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476`
Combined fixture fingerprint: `sha256:72264fb528f0452ed9570b870ae55c0dbe597e780b87c34bcf03511ad086d81f`

Diagnostics, not promoted:
- SWE: exports/time 0.848708181971; imports/time 0.916117346948; first-difference 0.928904323881
- NOR: exports/time 0.201630951838; imports/time -0.153613748322; first-difference -0.532592716581

Local AI: not retried. Existing 45-second and 120-second qwen3:4b attempts failed; current local screening route deferred until model-serving/routing evidence changes.

Campaign 38: not executed.


## PostgreSQL publication

PostgreSQL v1 rebuild and retrieval passed. Canonical/projected count: 528. Family query count: 3 and includes Campaign 36 plus both Campaign 37 packages. Retrieval friction: none requiring schema expansion or correlation-specific relational indexes.

## Governance-overhead result

Governance/support artifacts per accepted substantive package: 18 / 2 = 9.0. Campaign 36 baseline was 13 / 1 = 13.0. The ratio fell, so entity replication is not operationally blocked by governance overhead.

## Replication assessment

Outcome: A — Successful controlled replication.

## Next direction

Recommended: one semantically distinct correlation-pair pilot before declaring the correlation family mature or scaling broadly. Do not repeat the same exports/imports pair across more countries unless a later task identifies entity-scaling problems. Do not begin covariance or lag relationships yet.


## Final verification

Final verification artifacts are under `artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/final-verification/`.

Results:

- HTTPS/downgrade validation: pass
- unit resolution: pass
- offline fixture regeneration / no-promote rerun: pass
- normalization and alignment determinism: pass
- contract-fingerprint verification: pass
- independent coefficient recomputation: pass
- Decimal-context invariance: pass
- pair-order invariance: pass
- targeted Campaign 37 tests: pass
- full test suite: pass (`Ran 217 tests in 16.899s`, OK)
- Python compilation: pass
- repository validation: pass (528 objects)
- PostgreSQL rebuild and retrieval: pass
- historical-package immutability: pass
- coherence: 0 blocks, 1 stale-context warning
- context health: 0 blocks, 1 stale-context warning
- architecture-to-reality audit: 0 blocks, 0 warnings
- git diff --check: pass
- MacroForge dependency search: 0 runtime/package matches
- Campaign 38 production absence: pass
