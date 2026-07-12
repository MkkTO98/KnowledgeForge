# Relationship Export Contract v1 and Independent Consumer Simulation

## Result

Decision: **A. Read-only export contract validated; independent consumption is operationally proven.**

PostgreSQL indexing decision: **A. Current PostgreSQL v1 is adequate; defer correlation-specific indexing.**

Next strategic direction: **1. Continue operational Pearson production toward 100 objects.**

## Existing commitments inspected

Existing decisions support a KnowledgeForge-owned PostgreSQL operational projection derived from canonical KnowledgeObjectPackages, with canonical package JSON remaining authoritative. Prior commitments also preserve project-independence boundaries and reject PostgreSQL-originated knowledge, schema expansion without evidence, MacroForge/InsightForge coupling, and consumer authority over KnowledgeForge structures.

No contradiction was found. The contract is an owned export interface over KnowledgeForge's projection, not direct consumer database access and not a second canonical representation.

## Recovery lineage

- First attempt generated scenario outputs using invented statement type `statistical_relationship`.
- Canonical inspection proved all 13 current Pearson packages use `derived_relationship`.
- Query specs were corrected to `derived_relationship`.
- Stale first-attempt outputs were preserved at `artifacts/reports/relationship-export-contract-v1-20260711/failed_attempt_wrong_statement_type/`.
- Final outputs were regenerated under `artifacts/reports/relationship-export-contract-v1-20260711/exports/`.

## Contract design

Contract identity: `knowledgeforge_relationship_export_v1@1.0`.

Query identity: `knowledgeforge_relationship_query_v1@1.0`.

The export separates deterministic content from operational metadata. Deterministic content includes query, query fingerprint, repository/projection freshness identity, ordered package identities, package fingerprints, canonical package payloads, and result-set fingerprint. Operational metadata includes export timestamp and measured runtime.

Canonical KnowledgeObjectPackages remain authoritative; the export is a deterministic transfer/snapshot format.

## Implemented capability

- `tools/relationship_export_v1.py` — KnowledgeForge-owned read-only CLI exporter and verifier.
- `tools/relationship_export_consumer_simulator_v1.py` — independent consumer simulator using only export JSON and standard Python libraries.
- `specs/relationship_exports/relationship_export_contract_v1.json`
- `specs/relationship_exports/relationship_query_contract_v1.json`
- `specs/relationship_exports/queries/*.json`
- `tests/test_relationship_export_v1.py`

No HTTP service, shared schema, consumer write path, new Knowledge Object, Campaign 41, schema expansion, or InsightForge implementation was introduced.

## Scenario results

| Scenario | Count | Query fingerprint | Result-set fingerprint | Query shape | Time seconds |
|---|---:|---|---|---|---:|
| `all_pearson_relationships` | 13 | `sha256:7ee0faa2b7951d3680b3e4a963c864365c92eb208fdeb87bc1ee4f4e2314a324` | `sha256:7cafe3558ecad1230c110f590642ed12b900f0cf6ae3e30a6c13b02f7cd8a377` | indexed=1, jsonb=1 | 0.112429 |
| `involving_ne_exp_gnfs_zs` | 3 | `sha256:a91d1b9643cae59436f9431b6c0c93573021c9970ee94dc0e2bbdeb3ab585f1a` | `sha256:2b7a5df256fa08d56113fa10ed6229ec642dd523301d0507645c9421e0fa7f0b` | indexed=1, jsonb=1 | 0.103457 |
| `entity_nor` | 5 | `sha256:aa9c9c4d054962e615ff4eb9d4505253c5457db9510dd31e3af0aeff6d55c495` | `sha256:e4e6a1e5708091026509bdc8784f43e48e46e49e81612214efebfb342a4c4e25` | indexed=1, jsonb=1 | 0.098482 |
| `method_wdi_annual_scalar_pearson_v1` | 13 | `sha256:343e9eb5403dc988d51095722e6d55d62fb8d18e415787886a97c2fce770e6cf` | `sha256:7cafe3558ecad1230c110f590642ed12b900f0cf6ae3e30a6c13b02f7cd8a377` | indexed=1, jsonb=2 | 0.109639 |
| `raw_transformation_pearson` | 13 | `sha256:21eb908be20410b46da8a47797a1acb63684f62d206d086e842e92fbeebdd9e6` | `sha256:7cafe3558ecad1230c110f590642ed12b900f0cf6ae3e30a6c13b02f7cd8a377` | indexed=1, jsonb=2 | 0.103164 |
| `absolute_coefficient_at_least_0_8` | 7 | `sha256:34b465a75d61a0a9a39881660815ea0b6447554a5ab3fd26bbe79eec13345795` | `sha256:74bbf9bd373289d3426e56620cc9bf60a64213e478e9812ae22ba8f6cdd33ac4` | indexed=1, jsonb=1 | 0.102108 |
| `exact_package_id` | 1 | `sha256:637ef064f0aaa0e9d917b43674fc810fc1bd20f885fa3dd6e841dfaa3a5b5fef` | `sha256:bb32bc112647095808e0239fe6c9ac3dac3f8de60ae13154954465e4fe67a847` | indexed=1, jsonb=0 | 0.111240 |
| `zero_results` | 0 | `sha256:3cbf9d1f1f1f3f5c8ca7581c37e2e1c45a91214c2584e0fa3e50bc8f975256ef` | `sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | indexed=1, jsonb=1 | 0.100657 |


Repository fingerprint: `sha256:958c88d4be0bce735adcaaf3f236a7643aa80fd79846db23f4b521d05459771b`.

PostgreSQL projection identity: `sha256:f18f617896489d63662faa1911dedc9c8af177e0e732216df5564d8ee00c8334`.

Logical projection fingerprint: `sha256:bf6538b4610919e5fde1c6c5d12f6535b25886afbcb5604af5590d40d3771757`.

## Independent consumer result

The simulator verified contract version, query fingerprint, result-set fingerprint, package fingerprints, stable ordering, counts, provenance, limitations, and duplicate absence. It built local indexes by series, entity, and method without PostgreSQL access, KnowledgeForge runtime imports, canonical repository access, private schema knowledge, or mutation rights.

## Usefulness assessment

Using exported data only:

- Relationships involving `NE.EXP.GNFS.ZS`: 3
- Relationships for `NOR`: 5
- Method families exported: 1
- Packages with absolute coefficient >= 0.8: 7

The export eliminated the need for the simulated consumer to recompute correlations, query WDI, understand KnowledgeForge filesystem layout, or access PostgreSQL internals. It did not interpret economic importance, causality, prediction, or actionability.

## Determinism and change semantics

- Identical rerun deterministic content unchanged: True
- Identical rerun result-set fingerprint unchanged: True
- Operational timestamps differ while deterministic content stays unchanged: True
- Changed query fingerprint changed: True
- Changed query result fingerprint changed: True
- Stale projection simulation failed closed.

Consumers detect identical exports through deterministic content/result-set fingerprints; changed queries through query fingerprint; changed repository/projection through freshness identity; changed packages through package fingerprints; and contract changes through contract identity.

## Security and independence

Safeguards implemented:

- no consumer database credential path;
- no network service;
- read-only SELECT-based export;
- fail-closed projection freshness;
- repository/projection fingerprint validation;
- package fingerprint validation;
- deterministic result limits with `max_result_count <= 1000`;
- unsupported/interpretive filter rejection;
- SQL literal escaping for user filters;
- tamper detection through deterministic content and package fingerprints;
- no arbitrary input file reads except explicit query file;
- bounded local CLI scope.

Remaining risks are local-operator risks: large payload exports at future scale and JSONB scan latency if relationship objects grow substantially.

## PostgreSQL discovery-index decision

Decision: **A. Current PostgreSQL v1 is adequate; defer correlation-specific indexing.**

Evidence: current corrected scenario timings are sub-second, with query execution around tens of milliseconds and total export dominated by validation/serialization for small result sets. At 13 relationship objects, indexing is unjustified. At projected 100 objects, JSONB scans should remain acceptable. At 1,000 objects, this should be remeasured before schema/index work. No representation problem was found.

## Governance/artifact efficiency

One consolidated report, one contract spec, one query-contract spec, one reusable export CLI, one consumer simulator, one test file, and scenario exports were produced. No new Knowledge Objects were created, so substantive-object ratio is not applicable.

## Doctrine and architecture classification

- Doctrine: no Production Doctrine modification.
- Architecture: read-only export contract validated as a boundary-preserving operational interface.
- Repository inconsistency: none.
- Governance inconsistency: first attempt used non-canonical statement terminology; corrected and archived.
- Tooling/environment issue: none blocking.

## Verification references

Final verification logs live under `artifacts/reports/relationship-export-contract-v1-20260711/verification/`.
