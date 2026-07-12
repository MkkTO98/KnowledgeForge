# Campaign 36 — Bounded WDI Denmark Exports-Imports Share Pearson Correlation Pilot

Outcome: A — Successful correlation pilot.

Package promoted: `pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1`

Pearson coefficient: `0.988873850642`

Aligned observations: 35 of 35 expected annual periods, 1990–2024.

Repository count before: 526
Repository count after: 526
Repository fingerprint after: `sha256:e1a927077f1bb1a0b17293be465fbad17a36380ddd298ce038e3d6f5a7285a31`

Method: `wdi_annual_scalar_pearson_correlation_v1@1.0`
Contract fingerprint: `sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476`
Calculation evidence fingerprint: `sha256:e43f4350e99e73e0557cba370bcd35e4ea3d22d88211d125a37695dafac67033`
Combined aligned evidence fingerprint: `sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f`

Mechanical-overlap assessment: both indicators use GDP as denominator; exports/imports are economically related flows. This does not invalidate the object, but it blocks causal, predictive, significance, performance, mechanism, or investment interpretation.

Diagnostics, not promoted:
- exports vs time index: 0.952001314294
- imports vs time index: 0.95783860239
- first-difference sensitivity: 0.917424303831

Local AI retry: failed

Campaign 37: not executed.


## Final verification

Final verification artifacts are under `artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/final-verification/`.

Results:

- HTTPS and unit validation: pass
- downgrade validation: pass
- offline fixture regeneration / Campaign 36 rerun: pass
- repeated normalization / alignment determinism: pass
- method-contract fingerprint verification: pass
- independent coefficient recomputation: pass
- ambient Decimal-context and pair-order invariance: pass
- targeted Campaign 36 tests: pass
- full test suite: pass (`Ran 212 tests in 39.173s`, OK)
- Python compilation: pass
- canonical repository validation: pass (526 objects)
- PostgreSQL v1 verification and retrieval: pass
- existing-package immutability: pass
- coherence: 0 blocks, 1 stale-context warning
- context health: 0 blocks, 1 stale-context warning
- architecture-to-reality audit: 0 blocks, 0 warnings
- git diff --check: pass
- MacroForge dependency search: 0 runtime/package matches
- Campaign 37 production absence: pass
