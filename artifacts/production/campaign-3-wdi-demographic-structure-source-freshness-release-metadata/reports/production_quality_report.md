
# Production Quality Report

Campaign: campaign-3-wdi-demographic-structure-source-freshness-release-metadata

## Metrics

- Source Evidence Packages processed: 12
- KnowledgeCandidatePackages generated: 12
- KnowledgeObjectPackages accepted: 12
- Rejected candidates: 4
- Acceptance rate: 0.75
- Rejection rate: 0.25
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

## Knowledge categories produced

| Category | Count |
| --- | --- |
| classified | 1 |
| coverage | 1 |
| evidence_quality | 2 |
| methodological | 5 |
| negative | 2 |
| provenance | 1 |

## Validator failures by category

| Failure category | Count |
| --- | --- |
| constitutional_boundary | 1 |
| evidence_contract | 2 |
| lineage_fingerprint | 2 |
| provenance | 1 |
| unsupported_inference | 1 |

## Production quality assessment

Campaigns 0-3 all preserve determinism, fingerprint stability, rejected-candidate preservation, and zero observed duplicate pressure. Campaign 3 adds one more successful freshness/provenance metadata campaign without architecture modification.
