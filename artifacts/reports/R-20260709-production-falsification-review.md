# Production Falsification Review Before Campaign 4

Date: 2026-07-09
Status: completed
Scope: Campaigns 0-3, Production Evolution Log, production quality reports, cross-campaign assessments, validator behavior, accepted/rejected Knowledge Objects

## Objective

Identify KnowledgeForge production-methodology assumptions that have not yet been challenged by Campaigns 0-3 and determine whether the roadmap should deliberately exercise them before continuing production.

This review does not redesign architecture, modify code, modify validators, implement functionality, or change ontology.

## Evidence base

Observed production evidence:

- Campaign 0: 10 accepted, 3 rejected, deterministic replay true, fingerprint stability true.
- Campaign 1: 12 accepted, 4 rejected, deterministic replay true, fingerprint stability true, duplicate pressure false.
- Campaign 2: 14 accepted, 4 rejected, deterministic replay true, fingerprint stability true, duplicate pressure false.
- Campaign 3: 12 accepted, 4 rejected, deterministic replay true, fingerprint stability true, duplicate pressure false.
- Total accepted Knowledge Objects reviewed: 48.
- Accepted evidence references per object: all 48 accepted objects use exactly 1 evidence reference.
- Accepted provenance envelopes: 48/48 present.
- Rejected production examples: 15 rejected package files across Campaigns 0-3.

## Assumptions not yet falsified by production

| Assumption | Current evidence | Falsification gap | Roadmap coverage | Severity |
| --- | --- | --- | --- | --- |
| Single-evidence-reference objects are sufficient for current production. | Campaigns 1-3 average evidence references = 1.0; all 48 accepted objects have one evidence reference. | Multi-source-package objects have not been produced. Dependency/evidence-reference behavior is accepted by tests but not production-stressed. | Partially covered by Campaign 9 and Campaign 10. | Medium |
| Campaign-local duplicate checks are enough. | Campaigns 0-3 report no duplicate Knowledge Objects. | No valid production path has generated near-duplicate or conflicting valid objects. | Partially covered by Campaign 4/5/10. | Medium |
| Existing taxonomy covers future evidence-level knowledge. | Campaigns 0-3 used methodological, coverage, negative, factual, derived, classified, evidence_quality, provenance. | Factual/derived/classified remain low-count; no cross-family comparison pressure yet. | Covered by Campaign 4 and Campaign 9. | Low-medium |
| Rejected production cases primarily fail at source-evidence boundary. | Rejected production examples are source-level malformed packages; accepted constructed candidates/objects pass all stages. | Later-stage candidate/object validator rejection is fixture-tested but not production-stressed. | Partially covered by Campaign 9/11; not covered before Campaign 4. | Medium |
| Provenance completeness is simple binary presence. | Accepted objects all have complete provenance envelopes; rejected cases cover missing provenance. | Partial provenance, inconsistent source identities, conflicting release metadata, and multi-source provenance disagreement have not been production-stressed. | Covered by Campaign 7; partially by Campaign 9/10. | Medium |
| Fingerprint stability holds under current small object volumes. | Determinism and fingerprint stability hold across Campaigns 0-3. | Larger object volumes, similar object clusters, and multi-reference fingerprints have not been stressed. | Covered by Campaign 5/6/9. | Medium |
| Deterministic transformations remain transparent at current complexity. | Bucket construction, freshness metadata, and support-layer mechanics are deterministic. | Larger matrices, cross-family comparisons, and recurrence-count transformations are not yet stressed. | Covered by Campaign 5/6/9/10. | Medium |
| Missingness/negative knowledge remains scoped and non-interpretive. | Negative objects accepted in Campaigns 1-3; missing release-date values accepted as negative knowledge. | Dense territorial/temporal missingness may create repetitive statements or implicit interpretation pressure. | Covered by Campaign 5/6/7. | Medium |
| Local/frontier AI is unnecessary for accepted production. | Campaigns 0-3 accepted outputs were deterministic. | Candidate-screening pressure has not been tested because manual deterministic production remains manageable. | Covered only conditionally by Campaign 11. | Low |

## Realistic conflicting-object scenarios not yet encountered

The following are realistic but not yet observed:

1. Two valid source packages produce overlapping coverage claims with different scope granularity.
   - Example shape: one object says an indicator family is broadly covered; another says a territory/period sub-scope is missing.
   - This is not a contradiction if scopes differ, but it tests object identity, applicability, and reader interpretation.
   - Roadmap coverage: Campaigns 5, 6, and 9.

2. Two valid metadata packages report different freshness or release metadata for the same source family and scope.
   - This could arise from release-date versus last-updated fields, or from refreshed WDI snapshots later.
   - Roadmap coverage: Campaign 7 partially; future live/updated-source campaigns would cover more directly.

3. Two valid deterministic transformations produce near-duplicate methodological objects.
   - Example shape: one campaign records method from inventory construction; another records method from provenance lineage construction.
   - Roadmap coverage: Campaigns 4 and 10.

4. A cross-family comparison produces a valid object whose plain-language statement could be mistaken for domain interpretation.
   - Roadmap coverage: Campaign 9.

## Falsification judgment

The current roadmap deliberately exercises most identified gaps, but not immediately before Campaign 4.

Campaign 4 is itself a useful falsification step because it stresses:

- richer classified inventory knowledge;
- supported/unsupported dimensions;
- object similarity and duplicate pressure;
- category assignment consistency.

No gap identified here is severe enough to require a new stress campaign before Campaign 4.

The largest untested assumptions are multi-evidence-reference behavior, partial/conflicting provenance, and later-stage validator rejection under production conditions. These are real but are already partially or fully covered later in the roadmap.

## Recommendation

Proceed directly to Campaign 4 unchanged.

Do not insert a targeted stress campaign before Campaign 4.

Do record a falsification-watch item in the Production Evolution Log so future campaigns deliberately report whether they exercised:

- multi-reference objects;
- conflicting or overlapping valid objects;
- later-stage candidate/object validator failures;
- partial provenance and release-metadata disagreement;
- larger deterministic transformations.
