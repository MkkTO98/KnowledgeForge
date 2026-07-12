
# Production Quality Report

Campaign: campaign-7-wdi-demographic-structure-provenance-lineage-completeness

## Metrics

- Source Evidence Packages processed: 16
- KnowledgeCandidatePackages generated: 16
- KnowledgeObjectPackages accepted: 16
- Rejected candidates: 4
- Acceptance rate: 0.8
- Rejection rate: 0.2
- Average evidence references per Knowledge Object: 1.0
- Provenance completeness: True
- Fingerprint stability: True
- Determinism verification: True
- Duplicate Knowledge Objects detected: False

## Cross-campaign comparison

| Campaign | Accepted | Rejected | Determinism | Fingerprint stability | Duplicates |
| --- | --- | --- | --- | --- | --- |
| campaign_0 | 10 | 3 | True | True | False |
| campaign_1 | 12 | 4 | True | True | False |
| campaign_2 | 14 | 4 | True | True | False |
| campaign_3 | 12 | 4 | True | True | False |
| campaign_4 | 14 | 4 | True | True | False |
| campaign_5 | 20 | 4 | True | True | False |
| campaign_6 | 18 | 4 | True | True | False |
| campaign_7 | 16 | 4 | True | True | False |

## Knowledge categories produced

| Category | Count |
| --- | --- |
| classified | 1 |
| coverage | 6 |
| derived | 1 |
| evidence_quality | 1 |
| factual | 1 |
| methodological | 4 |
| negative | 1 |
| provenance | 1 |

## Validator failures by category

| Failure category | Count |
| --- | --- |
| constitutional_boundary | 1 |
| evidence_contract | 2 |
| lineage_fingerprint | 2 |
| provenance | 1 |
| unsupported_inference | 1 |

## Lineage completeness observations

| Observation | Value |
| --- | --- |
| raw_artifact_hashes | exercised |
| raw_artifact_urls | exercised |
| release_keys | exercised |
| source_urls | exercised |
| license_notes | exercised |
| provenance_envelopes | exercised |
| lineage_fingerprint_validation | exercised |
| malformed_provenance_rejection | exercised |
| duplicate_pressure | not_observed |

Campaigns 0-7 preserve determinism, fingerprint stability, rejected-candidate preservation, and zero observed duplicate pressure. Campaign 7 validates provenance-lineage completeness for the planned WDI demographic production family.
