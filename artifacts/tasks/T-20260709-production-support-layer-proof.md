# TASK — Production Support Layer Investigation and Bounded Implementation Proof

Date: 2026-07-09
Status: completed
Type: bounded implementation proof

## Objective

Determine whether PEL-008 and PEL-009 should be implemented as two independent helpers or one minimal deterministic Production Support layer, then implement only the smallest behaviour-preserving support if justified.

## Decision

Implemented one minimal deterministic Production Support layer:

- `tools/production_support.py`

Reason: PEL-008 and PEL-009 are adjacent production mechanics around package construction and production-quality aggregation. One small module with two explicit functions is clearer than two scattered helpers and far smaller than a framework.

## Implemented scope

- `build_source_evidence_package(...)` for existing SourceEvidencePackage dictionary assembly.
- `aggregate_common_quality_metrics(...)` for repeated Campaigns 1-3 common production-quality metrics.
- Campaigns 0-3 now use the source package helper.
- Campaigns 1-3 now use the common quality metric helper.

## Excluded scope

No architecture redesign, workflow framework, validator change, taxonomy change, package model change, registry, schema, adapter, API, persistence layer, runtime infrastructure, local model generation, frontier model generation, or further helper extraction was implemented.

## Reports

- `artifacts/reports/R-20260709-production-support-investigation.md`
- `artifacts/reports/R-20260709-production-support-implementation-decision.md`
- `artifacts/reports/R-20260709-production-support-regression-verification.md`

## RED evidence

`python3 -m unittest tests.test_production_support -v` failed before implementation with `FileNotFoundError` for missing `tools/production_support.py`.

## GREEN/regression evidence

- targeted support/campaign tests: 11 tests OK;
- full suite: 34 tests OK;
- Campaigns 1-3 artifact equivalence: `compared 163 changed 0 missing 0` after normalizing only absolute output paths;
- Campaigns 0-3 reran successfully to production artifact paths.

## Final recommendation

Proceed to Campaign 4 using the refined deterministic Production Support implementation. Reject further helper extraction until repeated future production evidence justifies it.
