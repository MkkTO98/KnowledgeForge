# Campaign 43 First-Difference Companion Calculation Gate

Date: 2026-07-12
Status: calculated, not published

## Scope

This task executed Campaign 43 first-difference Pearson coefficient calculation from the frozen six-candidate registry only.

Authorized boundary observed:

- calculated first-difference Pearson coefficients from retained KnowledgeForge fixtures;
- did not construct KnowledgeObjectPackages;
- did not publish canonical packages;
- did not rebuild or mutate PostgreSQL;
- did not mutate raw Campaign 41 packages;
- did not change Doctrine, package schema, PostgreSQL schema, or Relationship Export Contract.

## Frozen inputs verified

- Registry: `specs/correlation_batches/campaign43_coefficient_free_first_difference_companion_registry.json`
- Registry fingerprint: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Freeze spec: `specs/correlation_batches/campaign43_first_difference_companion_registry_freeze_specification.json`
- Freeze spec fingerprint: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`
- Method contract fingerprint: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`
- Transformation contract fingerprint: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`
- Method validation-registry fingerprint: `sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657`

## Calculation artifacts

- Helper: `tools/campaign43_first_difference_companion_calculation.py`
- Tests: `tests/test_campaign43_first_difference_companion_calculation.py`
- Pre-execution gate: `artifacts/reports/campaign43-first-difference-companion-calculation-20260712/pre_execution_gate.json`
- Calculation results: `artifacts/reports/campaign43-first-difference-companion-calculation-20260712/calculation_results.json`
- Candidate result fingerprints: `artifacts/reports/campaign43-first-difference-companion-calculation-20260712/candidate_result_fingerprints.json`

Candidate result fingerprint: `sha256:140eb37de9ef29a5363e0c60a6d87591b5ecd1c7538b1818abca75da306e2462`

## Results

| Candidate | Relationship | Coefficient | Aligned transformed observations | Prior diagnostic reconciliation |
|---|---|---:|---:|---|
| 01 | DNK agricultural land / broad money | -0.018892915467 | 33 | exact decimal match |
| 02 | DNK agricultural land / private credit | 0.058190335423 | 33 | exact decimal match |
| 03 | DNK forest area / broad money | -0.101990610667 | 33 | exact decimal match |
| 04 | NOR crude birth rate / fossil electricity | 0.037781664561 | 33 | matches prior diagnostic when quantized to prior 11 decimal places |
| 05 | NOR fossil electricity / under-5 mortality | -0.083376899169 | 33 | exact decimal match |
| 06 | NOR nonhydro renewable electricity / under-5 mortality | 0.3855860099 | 31 | exact decimal match |

All six calculations passed independent recomputation, retained-fixture fingerprint checks, aligned-count checks, and prior embedded diagnostic reconciliation at recorded precision.

## Canonical immutability

Canonical repository state remained unchanged:

- package count: 554
- repository fingerprint: `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`
- changed canonical object files: none
- new canonical package files: none
- Campaign 40-42 packages: unchanged
- PostgreSQL production mutation: none

## Architecture/doctrine classification

This is bounded method execution from an already frozen registry. No Doctrine change, package schema change, PostgreSQL schema change, Relationship Export Contract redesign, or broad transformation framework is required.

## Publication posture

The calculation output is ready for a separately authorized publication preflight. Publication itself remains unauthorized.

The smallest next task is: Campaign 43 append-only companion package construction and canonical publication preflight from `calculation_results.json`, stopping before publication unless publication is explicitly authorized in that task.
