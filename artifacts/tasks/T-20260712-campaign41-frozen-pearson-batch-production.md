# T-20260712 Campaign 41 Frozen Pearson Batch Production

Status: completed
Date: 2026-07-12

## Objective
Execute exactly `specs/correlation_batches/campaign41_ready_pearson_batch_spec.json` using the frozen eight-candidate set and retained validated fixtures; publish accepted Pearson packages append-only; rebuild the existing KnowledgeForge PostgreSQL projection; verify consumer-neutral retrieval/export.

## Inputs
- Ready spec: `specs/correlation_batches/campaign41_ready_pearson_batch_spec.json`
- Ready spec fingerprint: `sha256:c292ac73bdb92dd9b89e8c9dcad7a64675ad7d814e4149cea828b408bbeea0c6`
- Frozen registry fingerprint: `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`
- Retained fixture root: `artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https`

## Outcome
A. Successful end-to-end Campaign 41 production.

Eight frozen candidates were accepted as auditable finite-window descriptive Pearson relationships. No candidates were rejected. No candidate selection changed after calculation.

## Published packages
- `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1`

## Accounting
- Canonical object count: 538 -> 546
- Pearson-object count: 13 -> 21
- Statistical-summary count: 4 -> 4
- Repository fingerprint: `sha256:958c88d4be0bce735adcaaf3f236a7643aa80fd79846db23f4b521d05459771b` -> `sha256:c89c25ede69ec88a12f4791dba94b6199f2927721d0028420a65a74dd6ee735c`
- PostgreSQL projected count after rebuild: 546

## Reports
- Final report: `artifacts/reports/campaign41-frozen-pearson-batch-production-20260712/final_report.md`
- Final verification summary: `artifacts/reports/campaign41-frozen-pearson-batch-production-20260712/final-verification/final_verification_summary.json`
- Production machine report: `artifacts/reports/campaign41-frozen-pearson-batch-production-20260712/production/consolidated_machine_readable_report.json`
- Relationship export/consumer summary: `artifacts/reports/campaign41-frozen-pearson-batch-production-20260712/relationship_export/relationship_export_and_consumer_summary.json`

## Verification
- Frozen-input identity validation passed.
- Independent coefficient recomputation matched all eight packages.
- Non-promoted time-index diagnostics were produced and retrievable through package payloads/export.
- Pre-existing canonical package byte immutability passed.
- Deterministic no-publish rerun produced byte-identical package payloads.
- Append-only publish rerun was collision-protected.
- PostgreSQL projection verified with zero missing/extra package IDs and payload/fingerprint fidelity.
- Relationship Export Contract v1 and independent consumer simulation passed.
- Targeted tests: 35 passed.
- Complete suite: 289 passed.
- Python compilation, sensitive-material scan, coherence check, context-health check, architecture-to-reality audit, and git diff checks passed.

## Boundaries observed
No Campaign 42, no candidate changes, no new evidence acquisition, no covariance/significance/lag/trend/forecast/causal/recommendation/investment production, no MacroForge/InsightForge access, no PostgreSQL schema expansion, no Doctrine amendment, no destructive cleanup, no commit, and no push.
