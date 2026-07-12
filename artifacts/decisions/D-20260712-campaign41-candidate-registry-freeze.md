# D-20260712 Campaign 41 candidate registry freeze

Status: accepted
Date: 2026-07-12

## Decision
Freeze the Campaign 41 coefficient-free Pearson candidate registry and batch specification with 8 candidates.

## Result
Outcome B: 8 structurally valid candidates are frozen, but a bounded reusable extension to `tools/correlation_batch_engine.py` is required before calculation.

All 8 candidates are advisory-classified as suitable only with strong non-promoted time-index diagnostics and explicit limitations. None is classified unsuitable for production despite structural validity.

## Frozen fingerprints
- Registry: `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`
- Batch specification: `sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2`

## Engine limitation
Campaign 40-specific hardcoding remains in statement_id, calc_id, evidence_ref_id, validation_judgment, generated statement origin, and provenance lineage_basis. These affect statement/evidence/calculation identity and provenance text, but do not require KnowledgeObjectPackage or Doctrine redesign.

## Authorization for later calculation
Later Campaign 41 calculation is authorized only after the generic Pearson engine is patched/tested to parameterize those package internals. Calculation must use exactly `specs/correlation_batches/campaign41_coefficient_free_pearson_batch_spec.json` unless a new explicit decision supersedes it.

## Verification
- Python compile passed.
- Targeted tests: 13 passed.
- Full tests: 278 passed.
- Registry/spec/fingerprint/evidence/package-ID/coefficient-free/deterministic-regeneration checks passed.
- Sensitive scan: actual_secret_blockers=0; unsafe_absolute_path_dependencies=0.
- Context/coherence: no blocks, stale generated active_context warning only.
- Architecture audit: 0 blocks, 0 warnings.
- Git diff checks passed.

## Non-decisions
No coefficients, covariance, p-values, significance measures, canonical packages, repository publication, PostgreSQL rebuild/write, relationship export, Campaign 42, Doctrine amendment, or commit/push were authorized or performed.
