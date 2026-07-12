# Production Quality Report

## Counts

- Source Evidence Packages processed: 10
- KnowledgeCandidatePackages created: 10
- KnowledgeObjectPackages accepted: 10
- Packages rejected: 3
- Constitutional boundary violations: 1
- Duplicate knowledge detected: False
- Missing provenance failures: 1
- Missing fingerprint failures: 2
- Ambiguous classifications: 0
- Determinism verified: True
- Fingerprint stability: True

## Validator failures by category

| category | count |
| --- | --- |
| evidence_contract | 1 |
| lineage_fingerprint | 2 |
| provenance | 1 |
| unsupported_inference | 1 |

## Architectural observations

- Existing deterministic construction and validation contracts handled repository-level evidence objects without widening scope.
- Rejected objects were preserved for analysis without promotion.
- No new architecture was required during Campaign 0 execution.

## Candidate improvements discovered

- Future campaigns would benefit from a production-specific maturity vocabulary that does not reuse pre-production wording in construction internals.
- Duplicate detection is currently campaign-local and fingerprint-based; this was sufficient for Campaign 0 but may need a governed registry after repeated production pressure.
