# T-20260712 Campaign 41 generic correlation engine provenance parameterization

Status: completed
Outcome: A
Date: 2026-07-12

## Objective
Remove Campaign 40-specific package-internal hardcoding from `tools/correlation_batch_engine.py` while preserving exact Campaign 40 compatibility and proving Campaign 41 readiness without calculating Campaign 41 coefficients.

## Files changed
- `tools/correlation_batch_engine.py`
- `specs/correlation_batches/campaign40_first_end_to_end_spec_driven_pearson_batch.json`
- `specs/correlation_batches/campaign41_ready_pearson_batch_spec.json`
- `tests/test_correlation_engine_provenance_parameterization.py`
- `tests/test_coefficient_free_pearson_candidate_registry.py`
- report/decision/state/handoff artifacts for this task

## Verification
- Targeted tests: 24 passed.
- Full tests: 289 passed.
- Campaign 40 exact compatibility: all accepted package payloads identical.
- Campaign 41 readiness: valid, coefficient-free, candidate set unchanged.
- Architecture audit: 0 blocks, 0 warnings.
- Git diff checks passed.

## Boundaries preserved
No Campaign 41 calculation, canonical publication, PostgreSQL mutation, relationship export, Campaign 42, commit, or push.
