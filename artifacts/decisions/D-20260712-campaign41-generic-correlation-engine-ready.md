# D-20260712 Campaign 41 generic correlation engine ready

Status: accepted
Date: 2026-07-12

## Decision
The generic correlation batch engine is ready to execute the frozen Campaign 41 batch after bounded provenance parameterization.

Outcome: A.

## Evidence
- Campaign 40 no-publish offline compatibility generated packages byte/logically identical to canonical Campaign 40 accepted packages.
- Campaign 41 original candidate registry remains unchanged with fingerprint `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`.
- Campaign 41 original frozen spec remains unchanged with fingerprint `sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2`.
- Campaign 41 readiness successor spec: `specs/correlation_batches/campaign41_ready_pearson_batch_spec.json`.
- Readiness spec fingerprint: `sha256:c292ac73bdb92dd9b89e8c9dcad7a64675ad7d814e4149cea828b408bbeea0c6`.
- Full test suite: 289 passed in 19.60s.

## Scope boundary
No Campaign 41 coefficient, covariance, p-value, significance, canonical package, PostgreSQL write/rebuild, relationship export, Campaign 42, commit, or push was performed.

## Doctrine/architecture
No Doctrine amendment, KnowledgeObjectPackage redesign, PostgreSQL schema expansion, or architecture reopening is required.
