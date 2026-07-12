# T-20260712 Campaign 43 Coefficient-Free First-Difference Companion Registry Freeze

Status: completed
Date: 2026-07-12

## Objective

Freeze a deterministic, coefficient-free Campaign 43 first-difference companion registry for the six remaining Campaign 41 raw Pearson relationships classified as high shared-time-trend risk, stopping before coefficient calculation, first-difference execution, KnowledgeObjectPackage construction, canonical publication, PostgreSQL projection, or production mutation.

## Candidate boundary

Exactly six relationships were evaluated:

1. DNK agricultural land / broad money
2. DNK agricultural land / private credit
3. DNK forest area / broad money
4. NOR crude birth rate / fossil electricity
5. NOR fossil electricity / under-5 mortality
6. NOR nonhydro renewable electricity / under-5 mortality

No additional candidate source was used.

## Outcome

Registry frozen with all six candidates included and zero exclusions.

- Registry: `specs/correlation_batches/campaign43_coefficient_free_first_difference_companion_registry.json`
- Registry fingerprint: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Freeze specification: `specs/correlation_batches/campaign43_first_difference_companion_registry_freeze_specification.json`
- Specification fingerprint: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`
- Validator/generator: `tools/campaign43_first_difference_companion_registry.py`
- Tests: `tests/test_campaign43_first_difference_companion_registry.py`
- Report: `artifacts/reports/campaign43-coefficient-free-first-difference-companion-registry-20260712/final_report.md`

## Boundary confirmation

No coefficients were calculated, no first-difference vectors were produced, no packages were constructed or published, and no PostgreSQL projection or production mutation was performed.

## Verification

Focused Campaign 43 registry tests passed under `python3 -m unittest`. Compatibility, canonical invariants, coherence, context health, architecture-to-reality audit, durability/sensitive-material validation, and `git diff --check` are recorded in the final report.

## Smallest next task

Campaign 43 production preflight and coefficient calculation from the frozen registry, stopping before canonical publication unless publication is separately authorized.
