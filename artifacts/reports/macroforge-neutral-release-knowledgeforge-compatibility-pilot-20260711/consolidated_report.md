# MacroForge Neutral Evidence Release — KnowledgeForge Compatibility and No-Promote Integration Pilot

Date: 2026-07-11
Status: complete

## Executive result

Integration decision: B — KnowledgeForge adapter validated; real handoff operationally compatible.

Ownership decision: B — KnowledgeForge-owned bounded adapter. The MacroForge export contains sufficient semantics, but its producer contract is not identical to KnowledgeForge release-inbox v1. KnowledgeForge accepts the documented external format through its own adapter, preserving MacroForge producer identity and fingerprints and computing a separate KnowledgeForge normalized-release fingerprint.

No canonical Knowledge Objects were promoted. No KnowledgeForge PostgreSQL update/schema expansion was performed. MacroForge files were not modified by this task.

## 1. Transfer integrity

Transfer byte-for-byte equality: `True`
- macroforge-wdi-trade-share-dnk-swe-nor-1990-2024.neutral-release.json: source sha256 `1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86`, destination sha256 `1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86`, size 207509 bytes, equal `True`
- manifest.json: source sha256 `a8e18d97bf9ff84ce341de648897117a289e14158d6b6d2409ee557b8cfc961b`, destination sha256 `a8e18d97bf9ff84ce341de648897117a289e14158d6b6d2409ee557b8cfc961b`, size 862 bytes, equal `True`

After transfer, all validation used the KnowledgeForge-owned copy under `artifacts/external-release-handoffs/macroforge/task-210-wdi-trade-share-dnk-swe-nor-1990-2024/`.

## 2. Producer-envelope validation

Producer envelope valid: `True`
Item count: `210`
Selection fingerprint: `sha256:2b1a1c3d9e65b182f073e0171c59627c8298740ee9cb7c1418dfbae3ae196e0a`
Release fingerprint: `sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67`
Export SHA-256: `1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86`
Leakage scan leaks: `[]`

Verified independently: manifest consistency, unique observation keys, item fingerprints, producer selection fingerprint, producer release fingerprint, contract/version, provider/dataset, source release key, run lineage, missingness/observed status, unit validity, timestamp exclusion from deterministic producer release identity, and absence of private schema/path/credential leakage.

## 3. Unchanged-validator baseline

Existing KnowledgeForge validator accepted release unchanged: `False`
Exit code: `0`

Failures:
- `missing_release_field:contract_id`
- `missing_release_field:release_id`
- `missing_release_field:provider`
- `missing_release_field:dataset`
- `missing_release_field:source_release_vintage`
- `missing_release_field:evidence_items`
- `missing_release_field:release_content_fingerprint`
- `wrong_contract_version`
- `release_fingerprint_mismatch`

Classification: field-name/contract-identity and fingerprint-shape differences. Not an observation-meaning failure, not a provenance deficiency, and not a sovereignty conflict.

## 4. Compatibility matrix

Field-by-field matrix written to `compatibility_matrix.json` with 22 concepts. Summary: producer identity, provider, dataset, release ID, vintage, predecessor, observation fields, item/release/selection fingerprints, provenance, quality/run status, deterministic metadata, and operational metadata are compatible by adaptation. Definition text differs in granularity and is recorded as a representation difference.

## 5. Adapter result

Adapter identity: `knowledgeforge_macroforge_neutral_release_adapter_v1@1.0`
KnowledgeForge normalized-release fingerprint: `sha256:75a2b2a586df56523e3a5f81435b159f078af767d67de5adbda667e47c755060`

Adapter fail-closed behavior is covered by tests for unsupported/mutated producer fingerprints, duplicates, and idempotent processing. The adapter preserves producer contract identity, producer release ID, producer release fingerprint, selection fingerprint, original provider/dataset, and MacroForge release/run lineage.

## 6. Observation-level equivalence

- `calculation_observation_equivalent`: `True`
- `definition_mismatch_classification`: `representation_granularity_difference_macroforge_short_indicator_label_vs_knowledgeforge_retained_full_wdi_definition; nonblocking for no-promote Pearson recomputation because indicator code/unit/value/frequency/entity/period match`
- `definition_mismatch_count`: `210`
- `knowledgeforge_retained_item_count`: `210`
- `macroforge_item_count`: `210`
- `matching_keys`: `210`
- `report_fingerprint`: `sha256:af3dd06de856762352ea990187474856dd8d00836cd32bf1d6e7d257cf1b7715`
- `semantically_equivalent_for_no_promote_derivation_comparison`: `True`

Value, unit, period, frequency, key, and missingness semantics match for all 210 observations. Definition text differs for 210/210 observations because MacroForge exposes the short indicator label while KnowledgeForge retained fuller WDI definitions. This is nonblocking for no-promote Pearson recomputation and is recorded as a representation-granularity difference, not silently erased.

## 7. Inbox/idempotence

First processing: `{'received_status': 'unseen', 'processing_status': 'successfully_processed_no_promote', 'acceptance_status': None, 'initial_release': None, 'downstream_delta_path': 'artifacts/release-inbox-macroforge-real-handoff-v1/processing-evidence/macroforge-wdi-1990-2024-2b1a1c3d9e65b182/downstream_delta.json', 'incremental_recompute_count': 3, 'applicable_derivations': None}`
Second processing: `{'received_status': 'already_processed_identical_release', 'processing_status': 'successfully_processed_no_promote', 'acceptance_status': None, 'initial_release': None, 'downstream_delta_path': None, 'incremental_recompute_count': 0, 'applicable_derivations': None}`

The first real MacroForge release was treated as an initial external producer release. The second processing detected an identical already-seen release and performed zero incremental recomputations.

## 8. Derivation comparison

- DNK: candidate `0.988873850642`, existing `0.988873850642`, aligned pairs `35`, classification `exact_deterministic_match`, promotion `not_promoted`
- NOR: candidate `-0.477418804478`, existing `-0.477418804478`, aligned pairs `35`, classification `exact_deterministic_match`, promotion `not_promoted`
- SWE: candidate `0.968490740983`, existing `0.968490740983`, aligned pairs `35`, classification `exact_deterministic_match`, promotion `not_promoted`

All exact deterministic match: `True`

## 9. Downstream delta

- `external_release_accepted`: `True`
- `promotion_status`: `not_promoted`
- `canonical_knowledge_status`: `canonical_equivalent_no_promotion`
- `later_supersession_required`: `False`
- `downstream_delta_fingerprint`: `sha256:deaa8bc1628b1138f6996d588cc28fe40006c9a4b9d8a9f3454ebafaead38cbd`

Result: `canonical_equivalent_no_promotion`; no duplicate packages were created.

## 10. Independence proof

Processing used the transferred serialized files, `tools/macroforge_neutral_release_adapter_v1.py`, `tools/release_inbox_v1.py`, the existing derivation registry/calculation logic, and KnowledgeForge-owned state under `artifacts/release-inbox-macroforge-real-handoff-v1/`. It did not import MacroForge Python, query MacroForge PostgreSQL, access MacroForge private schemas/tables, use live MacroForge paths after the transfer, or use shared runtime modules.

## 11. Durability

Recovery-critical file count inventoried: `61`
Durability status: not durable until committed/pushed or externally backed up; untracked files and modified tracked files are at risk until a reviewed commit/backup exists

The handoff copy, adapter, registry state, processing evidence, delta, reports, task, and decision artifacts require later commit/backup. This task intentionally did not commit or push.

## 12. Doctrine and architecture classification

Classification: preserves Production Doctrine and KnowledgeObjectPackage boundaries. Adds a bounded external-contract adapter and handoff-processing proof; does not redesign KnowledgeObjectPackage, does not create Campaign 41, does not mutate canonical packages, does not expand PostgreSQL schema, and does not install scheduling.

## 13. Next operational step

1. Ask MacroForge to connect exporter execution to successful canonical release closeout.

Rationale: manual real transfer and KnowledgeForge-side semantics are now proven. The next bottleneck is producer-side trigger reliability; scheduling and canonical mutation should wait until release generation and handoff semantics remain stable through producer closeout.
