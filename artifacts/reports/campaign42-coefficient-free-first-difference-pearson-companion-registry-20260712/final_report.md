# Campaign 42 — Coefficient-Free First-Difference Pearson Companion Registry

Date: 2026-07-12
Status: completed
Decision: A — registry frozen and ready for separately authorized Campaign 42 companion production.

## Boundary

This task froze a coefficient-free selection registry only.

No Campaign 42 coefficients were calculated. No first-difference transformations were executed for production. No canonical companion packages were created. No canonical repository object was mutated. No PostgreSQL write/rebuild or relationship export execution was performed.

## Frozen artifacts

- Frozen registry: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/campaign42_coefficient_free_companion_registry.json`
- Declarative production specification: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/campaign42_declarative_companion_production_specification.json`
- Repository spec copies:
  - `specs/correlation_batches/campaign42_coefficient_free_first_difference_pearson_companion_registry.json`
  - `specs/correlation_batches/campaign42_first_difference_pearson_companion_production_specification.json`
- Expected package-ID manifest: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/expected_package_id_manifest.json`
- Raw-to-companion link manifest: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/raw_to_companion_link_manifest.json`
- Evidence/method compatibility report: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/evidence_method_compatibility_report.json`
- Coefficient-independence proof: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/coefficient_independence_proof.json`
- Deterministic regeneration proof: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/deterministic_regeneration_proof.json`
- Post-freeze diagnostic honesty audit: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/post_freeze_diagnostic_honesty_audit.json`
- Complete eligibility inventory: `artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/complete_21_package_eligibility_inventory.json`

## Accepted contracts

- Transformation: `wdi_annual_scalar_first_difference_v1@1.0`
- Transformation contract fingerprint: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`
- Method: `wdi_annual_scalar_first_difference_pearson_v1@1.0`
- Method contract fingerprint: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`
- Validation registry fingerprint: `sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657`

These contracts were accepted as fixed inputs and were not altered.

## Registry/specification fingerprints

- Registry fingerprint: `sha256:be7a085b5a74860c9a6c95fb2c9e6f45a066679d317fc743694959d502e3dc15`
- Specification fingerprint: `sha256:ec3eaf0f735a888bc01f9cf394f015dd87eab3096be2690e75de0c4ec6f86d00`

Deterministic regeneration result: registry and specification fingerprints were identical across repeated generation.

## Exact coefficient-independent selection policy

Selection enumerated canonical raw Pearson packages directly from `knowledge_repository/objects`.

Allowed inputs:

1. canonical raw package ID;
2. raw package fingerprint;
3. entity;
4. indicator identities;
5. raw package campaign/order metadata parsed from canonical IDs;
6. semantic-proximity class derived from non-numeric indicator/family metadata;
7. diagnostic metadata presence flag only;
8. retained evidence fixture existence and fingerprints;
9. raw units and transformed-unit compatibility;
10. expected transformed overlap/coverage feasibility from period availability only;
11. existing companion exclusion.

Disallowed selection inputs:

- raw Pearson magnitude;
- first-difference diagnostic magnitude;
- sign;
- expected surprise;
- p-value;
- significance;
- covariance;
- lag result;
- forecast;
- consumer/investment interest in numerical result.

Tie-breaking:

1. semantic-proximity priority;
2. diagnostic-coverage gap;
3. raw package campaign/order;
4. entity;
5. canonical raw package ID.

Remote cautionary cases were capped at two. Zero remote cases were needed because six close and two moderate eligible candidates satisfied the 8-candidate target.

## Complete 21-package eligibility inventory

Eligible: 14
Ineligible: 7
Ineligible reason: retained raw evidence fixture missing for 7 packages.

| Campaign | Raw package | Entity | Indicators | Semantic | Expected transformed n | Expected coverage | Eligible | Reason |
| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- |
| 36 | `pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1` | DNK | `NE.EXP.GNFS.ZS` / `NE.IMP.GNFS.ZS` | close | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 37 | `pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1` | NOR | `NE.EXP.GNFS.ZS` / `NE.IMP.GNFS.ZS` | close | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 37 | `pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1` | SWE | `NE.EXP.GNFS.ZS` / `NE.IMP.GNFS.ZS` | close | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 38 | `pkg-object-srcpkg-campaign38-dnk-life-expectancy-fertility-pearson-correlation-v1` | DNK | `SP.DYN.LE00.IN` / `SP.DYN.TFRT.IN` | remote | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 39 | `pkg-object-srcpkg-campaign39-health-system-coverage-pearson-correlation-v1` | DNK | `SH.IMM.IDPT` / `SH.IMM.MEAS` | close | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 39 | `pkg-object-srcpkg-campaign39-infrastructure-digital-access-pearson-correlation-v1` | NOR | `IT.NET.USER.ZS` / `IT.CEL.SETS.P2` | close | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 39 | `pkg-object-srcpkg-campaign39-demographic-rates-pearson-correlation-v1` | SWE | `SP.DYN.CBRT.IN` / `SP.DYN.CDRT.IN` | close | 0 | 0 | no | retained_raw_evidence_fixture_missing |
| 40 | `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1` | DNK | `AG.LND.AGRI.ZS` / `AG.LND.FRST.ZS` | close | 33 | 0.970588235294 | yes | eligible |
| 40 | `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1` | DNK | `FS.AST.PRVT.GD.ZS` / `FM.LBL.BMNY.GD.ZS` | close | 34 | 1 | yes | eligible |
| 40 | `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1` | NOR | `SP.DYN.CBRT.IN` / `SP.DYN.CDRT.IN` | close | 34 | 1 | yes | eligible |
| 40 | `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1` | NOR | `EG.ELC.FOSL.ZS` / `EG.ELC.RNWX.ZS` | close | 31 | 0.911764705882 | yes | eligible |
| 40 | `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1` | NOR | `SP.DYN.LE00.IN` / `SH.DYN.MORT` | close | 34 | 1 | yes | eligible |
| 40 | `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1` | SWE | `IT.NET.USER.ZS` / `IT.CEL.SETS.P2` | close | 34 | 1 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1` | DNK | `AG.LND.AGRI.ZS` / `FM.LBL.BMNY.GD.ZS` | remote | 33 | 0.970588235294 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1` | DNK | `AG.LND.AGRI.ZS` / `FS.AST.PRVT.GD.ZS` | remote | 33 | 0.970588235294 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1` | DNK | `AG.LND.FRST.ZS` / `FM.LBL.BMNY.GD.ZS` | remote | 33 | 0.970588235294 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1` | NOR | `SP.DYN.CBRT.IN` / `EG.ELC.FOSL.ZS` | remote | 33 | 0.970588235294 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1` | NOR | `EG.ELC.FOSL.ZS` / `SH.DYN.MORT` | remote | 33 | 0.970588235294 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1` | NOR | `EG.ELC.RNWX.ZS` / `SH.DYN.MORT` | remote | 31 | 0.911764705882 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1` | SWE | `FS.AST.PRVT.GD.ZS` / `IT.NET.USER.ZS` | moderate | 34 | 1 | yes | eligible |
| 41 | `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1` | SWE | `FS.AST.PRVT.GD.ZS` / `IT.CEL.SETS.P2` | moderate | 34 | 1 | yes | eligible |

## Frozen 8-candidate registry

| Candidate | Raw package | Expected companion package | Entity | Indicators | Semantic | Expected transformed n | Expected coverage | Prior embedded FD diagnostic? |
| --- | --- | --- | --- | --- | --- | ---: | ---: | --- |
| campaign42-fd-pearson-companion-candidate-01 | `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-first-difference-pearson-companion-v1` | DNK | `AG.LND.AGRI.ZS` / `AG.LND.FRST.ZS` | close | 33 | 0.970588235294 | yes |
| campaign42-fd-pearson-companion-candidate-02 | `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-first-difference-pearson-companion-v1` | DNK | `FS.AST.PRVT.GD.ZS` / `FM.LBL.BMNY.GD.ZS` | close | 34 | 1 | yes |
| campaign42-fd-pearson-companion-candidate-03 | `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-first-difference-pearson-companion-v1` | NOR | `SP.DYN.CBRT.IN` / `SP.DYN.CDRT.IN` | close | 34 | 1 | yes |
| campaign42-fd-pearson-companion-candidate-04 | `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-first-difference-pearson-companion-v1` | NOR | `EG.ELC.FOSL.ZS` / `EG.ELC.RNWX.ZS` | close | 31 | 0.911764705882 | yes |
| campaign42-fd-pearson-companion-candidate-05 | `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-first-difference-pearson-companion-v1` | NOR | `SP.DYN.LE00.IN` / `SH.DYN.MORT` | close | 34 | 1 | yes |
| campaign42-fd-pearson-companion-candidate-06 | `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1` | `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-first-difference-pearson-companion-v1` | SWE | `IT.NET.USER.ZS` / `IT.CEL.SETS.P2` | close | 34 | 1 | yes |
| campaign42-fd-pearson-companion-candidate-07 | `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1` | `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-first-difference-pearson-companion-v1` | SWE | `FS.AST.PRVT.GD.ZS` / `IT.NET.USER.ZS` | moderate | 34 | 1 | yes |
| campaign42-fd-pearson-companion-candidate-08 | `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1` | `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-first-difference-pearson-companion-v1` | SWE | `FS.AST.PRVT.GD.ZS` / `IT.CEL.SETS.P2` | moderate | 34 | 1 | yes |

## Semantic/entity/family distribution

entities={'DNK': 2, 'NOR': 3, 'SWE': 3}; semantic={'close': 6, 'moderate': 2}; families={'AG': 1, 'FS': 3, 'SP': 2, 'EG': 1, 'IT': 1}

Selected candidates include multiple entities: DNK, NOR, SWE. The registry includes six close relationships and two moderate relationships. It includes no remote cautionary cases because sufficient close/moderate candidates existed.

## Candidates with/without prior embedded diagnostics

With prior embedded non-promoted first-difference diagnostics: 8
Without prior embedded non-promoted first-difference diagnostics: 0

The values were technically available before selection in existing raw packages, but the registry did not read, compare, threshold, rank, or branch on those numerical values. Used metadata fields were: semantic proximity, diagnostic coverage gap, raw package campaign/order, entity, canonical raw package id, fixture existence, unit transformability, expected transformed overlap/coverage.

## Diagnostic-value independence proof

Proof artifact: `coefficient_independence_proof.json`.

Result: changing or removing stored diagnostic coefficient fields did not alter the selected raw package IDs, expected companion package IDs, registry fingerprint, or specification fingerprint, provided required non-numeric metadata remained unchanged.

## Expected companion package IDs

- campaign42-fd-pearson-companion-candidate-01: `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-02: `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-03: `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-04: `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-05: `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-06: `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-07: `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-first-difference-pearson-companion-v1`
- campaign42-fd-pearson-companion-candidate-08: `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-first-difference-pearson-companion-v1`


## Raw-to-companion links

- `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-first-difference-pearson-companion-v1`
- `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1` -> `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-first-difference-pearson-companion-v1`

## Evidence and transformed-overlap compatibility

All selected candidates have:

- retained evidence fixture identities and fingerprints;
- transformable units under the accepted unit contract;
- no existing canonical first-difference companion;
- expected transformed overlap >= 30;
- expected transformed coverage >= 0.85.

Compatibility details are frozen in `evidence_method_compatibility_report.json`.

## Transformed-unit semantics

- campaign42-fd-pearson-companion-candidate-01: year-to-year percentage-point change in % of land area / year-to-year percentage-point change in % of land area
- campaign42-fd-pearson-companion-candidate-02: year-to-year change in percentage points of GDP / year-to-year change in percentage points of GDP
- campaign42-fd-pearson-companion-candidate-03: absolute year-to-year change in per 1,000 people / absolute year-to-year change in per 1,000 people
- campaign42-fd-pearson-companion-candidate-04: year-to-year percentage-point change in % of total / year-to-year percentage-point change in % of total
- campaign42-fd-pearson-companion-candidate-05: absolute year-to-year change in years / absolute year-to-year change in per 1,000 live births
- campaign42-fd-pearson-companion-candidate-06: year-to-year percentage-point change in % of population / absolute year-to-year change in per 100 people
- campaign42-fd-pearson-companion-candidate-07: year-to-year change in percentage points of GDP / year-to-year percentage-point change in % of population
- campaign42-fd-pearson-companion-candidate-08: year-to-year change in percentage points of GDP / absolute year-to-year change in per 100 people

## Companion identity

The expected companion package identity:

- has its own expected package ID and future package fingerprint;
- references exactly one canonical raw Pearson package;
- retains both raw evidence-series fingerprints;
- identifies the accepted first-difference transformation and method;
- remains independently reproducible and retrievable;
- does not supersede or mutate the raw package.

This requires no package architecture change.

## Architecture/Doctrine classification

Classification: bounded deterministic selection/specification freeze for future companion production.

No Doctrine pressure discovered. No KnowledgeObjectPackage redesign, PostgreSQL schema expansion, general transformation framework, local AI, or repository mutation was required.

## Verification status

Final verification outputs are stored under:

`artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/final-verification/`

Results:

- canonical raw-Pearson enumeration validation: passed; 21 canonical raw Pearson packages enumerated directly from `knowledge_repository/objects`.
- evidence and fingerprint validation: passed.
- transformed-unit compatibility validation: passed for all 8 selected candidates.
- expected-overlap feasibility validation without coefficient calculation: passed; all selected candidates have expected transformed overlap >= 30 and coverage >= 0.85.
- existing-companion exclusion: passed; no existing canonical first-difference companion found for selected candidates.
- package-ID uniqueness validation: passed.
- coefficient-field exclusion: passed for frozen registry.
- diagnostic-value independence test: passed; mutating stored diagnostic coefficient fields did not change selected IDs or registry/specification fingerprints.
- deterministic regeneration: passed.
- registry/specification fingerprint verification: passed.
- targeted Campaign 42 tests: 5 passed.
- complete test suite: 311 passed, 17 subtests passed.
- Python compilation: passed.
- sensitive-material scan: 0 findings.
- coherence check: no blocks; stale generated `context/active_context.md` warning only.
- context-health check: no blocks; stale generated `context/active_context.md` warning only.
- architecture-to-reality audit: no blocks, no warnings.
- git diff --check: passed.

Working-tree note: `git status --short` still includes unrelated pre-existing residue explicitly outside this task boundary, including ArchitectureHarvest deletions, checkpoint payload, historical logs, retained verification databases, and unrelated durability/campaign reports. These were preserved and not cleaned up.

## Final decision

A. Registry frozen and ready for Campaign 42 companion production.

This does not authorize production. Production must be a separate bounded task that reads the frozen registry/specification, calculates first differences and coefficients only then, creates canonical companion packages append-only, and verifies PostgreSQL/export compatibility if publication is authorized.

## Smallest exact next task

Execute Campaign 42 companion production from the frozen coefficient-free registry/specification: calculate first-difference Pearson coefficients for the 8 frozen candidates, create append-only canonical first-difference companion packages, validate package fingerprints/provenance, and verify repository/PostgreSQL/export retrieval — without mutating raw packages.
