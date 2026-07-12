# T-20260712 Campaign 43 First-Difference Companion Calculation Gate

Status: completed
Date: 2026-07-12

## Objective

Execute the smallest bounded Campaign 43 follow-on task after registry freeze: calculate first-difference Pearson coefficients for the six frozen Campaign 43 candidates, without constructing KnowledgeObjectPackages, publishing canonical packages, projecting to PostgreSQL, or mutating production state.

## Inputs

- Frozen registry: `specs/correlation_batches/campaign43_coefficient_free_first_difference_companion_registry.json`
- Registry fingerprint: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Freeze spec: `specs/correlation_batches/campaign43_first_difference_companion_registry_freeze_specification.json`
- Spec fingerprint: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`

## Outcome

Completed. Six candidate coefficients were calculated from retained fixtures using `wdi_annual_scalar_first_difference_pearson_v1`.

Calculation result fingerprint: `sha256:140eb37de9ef29a5363e0c60a6d87591b5ecd1c7538b1818abca75da306e2462`

Results:

- DNK agricultural land / broad money: `-0.018892915467`, aligned transformed observations `33`
- DNK agricultural land / private credit: `0.058190335423`, aligned transformed observations `33`
- DNK forest area / broad money: `-0.101990610667`, aligned transformed observations `33`
- NOR crude birth rate / fossil electricity: `0.037781664561`, aligned transformed observations `33`
- NOR fossil electricity / under-5 mortality: `-0.083376899169`, aligned transformed observations `33`
- NOR nonhydro renewable electricity / under-5 mortality: `0.3855860099`, aligned transformed observations `31`

All candidates passed independent recomputation, aligned-count checks, retained-fixture fingerprint checks, and prior embedded diagnostic reconciliation at recorded precision.

## Verification

- `python3 -m unittest tests.test_campaign43_first_difference_companion_calculation tests.test_campaign43_first_difference_companion_registry tests.test_campaign42_first_difference_companion_production tests.test_campaign42_first_difference_companion_registry tests.test_first_difference_pearson_method tests.test_relationship_export_v1 tests.test_postgresql_operational_projection` — 42 tests OK.
- `python3 tools/campaign43_first_difference_companion_calculation.py --project . --write-artifacts` — calculated six candidates, no publication, no PostgreSQL projection, canonical immutability valid.
- Canonical validation: 554 object files, 554 manifest count, validation errors `[]`, repository fingerprint `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`.
- `git diff --check` — passed.
- `python3 tools/check_coherence.py --project . --json` — 0 blocks; warnings only for handoff size and stale generated active context.
- `python3 tools/context_health.py --project . --json` — 0 blocks; same warnings only.
- `python3 tools/architecture_reality_audit.py --project . --write-report` — 0 blocks, 0 warnings.
- `python3 tools/repository_wide_durability_validator.py --report /tmp/kf_campaign43_calc_durability.json` — sensitive scan passed, actual secret blockers 0, unsafe absolute path dependencies 0; pre-existing local durability findings remain.

## Boundary confirmations

- KnowledgeObjectPackages constructed: no.
- Canonical publication: no.
- PostgreSQL projection or mutation: no.
- Campaign 40-42 package mutation: no.
- New package files: no.
- Architecture/doctrine/schema redesign: no.

## Next smallest task

Campaign 43 append-only companion package construction and publication preflight from `artifacts/reports/campaign43-first-difference-companion-calculation-20260712/calculation_results.json`, stopping before publication unless publication is explicitly authorized.