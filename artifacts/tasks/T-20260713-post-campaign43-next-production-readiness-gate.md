# T-20260713 Post-Campaign-43 Next Production Readiness Gate

Status: completed; selected correction implemented locally
Date: 2026-07-13

## Objective

Select exactly one smallest bounded next production or production-enabling task after Campaign 43, without beginning implementation.

## Baseline

- Starting `HEAD` and `origin/main`: `bda3f13808bf70c7b108bcf215f98f5789d937fe`
- Canonical packages: 560
- Repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- PostgreSQL projection: valid at 560 packages
- Relationship Export: 35 relationships, 21 raw Pearson, 14 first-difference Pearson, no raw/first-difference overlap

## Outcome

Selected path D: bounded production-enabling correction.

The smallest next task is to convert `tests/test_operational_state_checkpoint.py` from an undeclared `pytest` dependency to standard-library `unittest` semantics, preserving production behavior and operational-state-checkpoint coverage, then prove repository-wide unittest discovery runs cleanly.

## Evidence examined

See `artifacts/reports/post-campaign43-next-production-readiness-gate-20260713/final_report.md`.

## Decision record

`artifacts/decisions/D-20260713-post-campaign43-next-production-readiness-gate.md`

## Boundaries

This task did not calculate coefficients, execute transformations, construct packages, publish packages, mutate PostgreSQL production state, modify Relationship Export outputs intentionally, change doctrine, change architecture, stage, commit, or push.

## Verification

Decision-artifact verification preserved canonical and PostgreSQL state. Full unittest discovery was intentionally run as evidence and failed exactly at the isolated undeclared `pytest` import in `tests/test_operational_state_checkpoint.py`; this failure is the selected production-enabling defect, not an unresolved blocker to the decision gate.
