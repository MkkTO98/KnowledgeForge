# Validator Coverage Analysis Before Campaign 4

Date: 2026-07-09
Status: completed
Scope: production validator behavior across Campaigns 0-3

## Production validator evidence

Accepted production paths:

- 48 accepted Knowledge Objects passed all applicable validator stages.
- Accepted validation records show all stages passing for accepted production packages.

Rejected production paths:

- 15 rejected package files were preserved across Campaigns 0-3.
- The repeated rejected categories were:
  - evidence_contract;
  - lineage_fingerprint;
  - provenance;
  - unsupported_inference;
  - constitutional_boundary.

## Validator paths exercised by production

Strongly exercised:

- valid source evidence package acceptance;
- valid evidence evaluation acceptance;
- valid candidate acceptance;
- valid knowledge object acceptance;
- source-level rejection for missing provenance;
- source-level rejection for missing/invalid fingerprints;
- source-level rejection for unsupported inference/boundary language;
- source-level rejection for unsupported category.

Weakly or not production-exercised:

| Validator area | Production coverage | Existing non-production coverage | Roadmap coverage |
| --- | --- | --- | --- |
| malformed KnowledgeCandidatePackage after valid source | Little/no production coverage | Fixture/unit coverage exists | Partially Campaign 9/11 |
| malformed KnowledgeObjectPackage after valid candidate | Little/no production coverage | Fixture/unit coverage exists | Partially Campaign 9/11 |
| multi-evidence-reference validation | No accepted production coverage | Contract-level coverage only | Campaign 9/10 |
| evolution/change validation | No production campaign coverage | Validation Framework v1 tests | Not central before Campaign 10+ |
| duplicate object pressure | No observed duplicates | Campaign-local checks run | Campaign 4/5/10 |
| partial provenance inconsistency | Only missing provenance/fingerprint cases | Fixture-level validation | Campaign 7/9 |
| temporal language boundary tension | Campaign 3 freshness wording accepted safely | Boundary tests exist | Campaign 6/9 |

## Important distinction

The validator framework has broader test coverage than production coverage. This review concerns production falsification only.

The fact that malformed later-stage packages are not production-observed is not currently a blocker because Campaigns 0-3 use deterministic construction from source packages. It becomes more important when future campaigns introduce multi-source comparisons, local-model-assisted draft screening, or more complex candidate assembly.

## Validator falsification conclusion

The production validator evidence is strong for accepted deterministic construction and source-boundary rejection. It is weak for later-stage production rejection, multi-reference objects, partial provenance inconsistency, and duplicate/overlap resolution.

This does not justify a pre-Campaign-4 stress campaign. Campaign 4 naturally exercises duplicate and category consistency pressure. Campaigns 7, 9, 10, and 11 address the heavier remaining validator gaps.
