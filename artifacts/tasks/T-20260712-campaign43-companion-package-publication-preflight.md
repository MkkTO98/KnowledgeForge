# T-20260712 Campaign 43 Companion Package Publication Preflight

Status: completed locally; not published
Date: 2026-07-12

## Objective

Construct and validate exactly six non-canonical Campaign 43 first-difference Pearson companion KnowledgeObjectPackage candidates from the frozen registry and accepted calculation evidence, then prepare publication-readiness metadata without canonical publication.

## Inputs

- Registry fingerprint: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Freeze-spec fingerprint: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`
- Calculation-result fingerprint: `sha256:140eb37de9ef29a5363e0c60a6d87591b5ecd1c7538b1818abca75da306e2462`
- Canonical baseline: 554 packages, repository fingerprint `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`

## Outcome

Completed.

Constructed exactly six candidate packages outside `knowledge_repository/objects` under `artifacts/reports/campaign43-first-difference-companion-publication-preflight-20260712/candidate_packages/`.

Package-set fingerprint: `sha256:9ed161b9dcf7472b7e13979cbd9cd1a24f1ce3009108e677c41dace20277d559`

Expected post-publication state from safe temporary-repository dry run:

- package count: 560
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- PostgreSQL projected package count: 560
- Relationship Export counts: raw Pearson 21; first-difference Pearson 14

## Boundaries preserved

- No candidate package copied into the canonical repository.
- No canonical manifest/index/evolution mutation.
- No PostgreSQL projection or mutation.
- No Relationship Export publication.
- No coefficient recalculation or selective discard during package construction.
- No staging, commit, push, tag, schema, doctrine, or architecture change.
- Unrelated `architecture/architectureharvest/` deletions and local operational residue were not resolved or staged.

## Verification

- `python3 -m unittest tests.test_campaign43_first_difference_companion_publication_preflight tests.test_campaign43_first_difference_companion_calculation tests.test_campaign43_first_difference_companion_registry tests.test_campaign42_first_difference_companion_production tests.test_campaign42_first_difference_companion_registry tests.test_first_difference_pearson_method tests.test_relationship_export_v1 tests.test_postgresql_operational_projection` — 49 tests OK.
- `python3 tools/campaign43_first_difference_companion_publication_preflight.py --project . --write-artifacts` — 6 packages constructed outside canonical repository; expected publication count/fingerprint computed by temporary-copy dry run.
- Canonical validation — 554 packages, validation errors `[]`, fingerprint unchanged.
- `git diff --check` — passed.
- `python3 tools/check_coherence.py --project . --json` — 0 blocks; stale generated `context/active_context.md` warning only after concise handoff update.
- `python3 tools/context_health.py --project . --json` — 0 blocks; stale generated `context/active_context.md` warning only after concise handoff update.
- `python3 tools/architecture_reality_audit.py --project . --write-report` — 0 blocks, 0 warnings.
- `python3 tools/repository_wide_durability_validator.py --report /tmp/kf_campaign43_publication_preflight_durability_1783893295_460751` — exit 0; actual secret blockers 0; sensitive scan passed; unsafe absolute path dependencies 0; validator decision D because untracked recovery-critical files and operational checkpoint state are not machine-loss durable until committed/backed up.

## Remaining risk

The task is locally verified but not Git-durable. Campaign 43 artifacts remain local-only until an explicitly authorized durability publication/commit/push or external backup.
