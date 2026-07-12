
# Cross-Campaign Assessment Report

Scope: Campaigns 0-4

## Production stability

All five campaigns completed with deterministic execution and accepted KnowledgeObjectPackages through the existing pipeline.

| Campaign | Accepted | Rejected | Determinism | Fingerprint stability | Duplicates |
| --- | --- | --- | --- | --- | --- |
| campaign_0 | 10 | 3 | True | True | False |
| campaign_1 | 12 | 4 | True | True | False |
| campaign_2 | 14 | 4 | True | True | False |
| campaign_3 | 12 | 4 | True | True | False |
| campaign_4 | 14 | 4 | True | True | False |

## Validator behavior

Validator failures again involved evidence-contract, provenance, lineage-fingerprint, unsupported-inference, and boundary-language categories. Campaign 4 did not naturally exercise later-stage candidate/object rejection; PEL-017 should remain monitor.

## Falsification evidence

Campaign 4 exercised classification consistency, object similarity, factual/classified coverage, supported dimensions, unsupported dimensions, and scoped overlapping valid objects. It did not produce duplicates, multi-reference objects, partial provenance disagreement, or later-stage validator rejection.

## Duplicate pressure

No duplicate Knowledge Objects were detected in Campaigns 0, 1, 2, 3, or 4. A cross-campaign duplicate registry remains unjustified.

## Roadmap assessment

Campaign 4 does not justify resequencing the production roadmap. Campaign 5 remains the next production campaign.
