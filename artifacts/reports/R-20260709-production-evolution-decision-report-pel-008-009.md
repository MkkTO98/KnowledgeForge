# Production Evolution Decision Report — PEL-008 and PEL-009

Date: 2026-07-09
Status: completed
Scope: investigation decisions for PEL-008 and PEL-009 only

## Decision summary

| Item | Decision | Evidence basis | Implementation before Campaign 3? |
| --- | --- | --- | --- |
| PEL-008 | Continue Investigate | Repeated in Campaigns 1-2; structural package-contract construction pressure but only across one domain/evidence family. | No |
| PEL-009 | Continue Investigate | Repeated in Campaigns 0-2 as production-quality reporting; base metric formulas stable, but Campaign 3 should test freshness/provenance pressure before extraction. | No |

No investigated item is Ready for Implementation.

## Decision rule applied

The Production Evolution Log says `implement` requires repeated evidence plus investigation showing that a minimal change preserves current architecture and reduces repeated production friction.

This investigation confirms repeated friction, but does not yet confirm the minimal safe helper boundary strongly enough to implement before Campaign 3.

## PEL-008 decision details

Decision: Continue Investigate

Evidence supporting investigation:

- Campaign 1 explicitly observed repeated SourceEvidencePackage field construction across accepted and rejected packages.
- Campaign 2 repeated that pressure.
- Campaign runners show repeated construction of the same SourceEvidencePackage contract regions.

Evidence against implementation now:

- Formal recurrence count is only two domain campaigns.
- Both are WDI demographic-structure campaigns.
- Campaign 3 will stress source freshness/provenance metadata, which may materially clarify the helper boundary.
- A helper implemented now could overfit the Campaign 1-2 evidence-payload/provenance shape.

Required next evidence:

- Campaign 3 should record whether SourceEvidencePackage scaffolding repeats unchanged.
- Campaign 3 should identify whether rejected-candidate authoring benefits from or should remain outside any future helper.
- Campaign 3 should record whether a future helper can stay source-family-neutral.

## PEL-009 decision details

Decision: Continue Investigate

Evidence supporting investigation:

- Campaign 0 established production-quality reporting.
- Campaign 1 repeated production-quality aggregation and recorded it as friction.
- Campaign 2 repeated aggregation again and added cross-campaign comparison.
- Metric formulas are deterministic reductions over accepted objects, rejected records, validator failure categories, evidence references, provenance envelopes, fingerprints, and replay outputs.

Evidence against implementation now:

- Cross-campaign comparison has only one campaign of evidence as an explicit metric extension.
- Campaign 3 freshness/provenance emphasis may add or reshape base metric needs.
- A helper implemented now might accidentally freeze a rigid reporting schema before enough campaign variation exists.

Required next evidence:

- Campaign 3 should record whether the same base metrics recur unchanged.
- Campaign 3 should record whether freshness/provenance metrics are campaign-specific extensions or belong in the base metric set.
- Campaign 3 should confirm whether cross-campaign comparison stabilizes as a standard feature.

## Architectural decision

Preserve the architecture unchanged.

No evidence supports:

- new package model;
- new taxonomy;
- validator redesign;
- production workflow redesign;
- runtime infrastructure;
- APIs;
- adapters;
- shared schemas;
- repository coupling;
- database coupling;
- model generation.

## Implementation decision

Do not implement either helper before Campaign 3.

Both items remain investigation candidates. The next evidence should come from Campaign 3 production, not pre-campaign implementation.

## Final recommendation

Proceed directly to Campaign 3 unchanged.

Rationale:

- PEL-008 and PEL-009 are real recurring pressures.
- They are not production blockers.
- Existing Campaign 3 is precisely the right next evidence source because it stresses source freshness/provenance metadata inside the same architecture.
- Implementing now would reduce short-term manual work but increase the risk of premature abstraction.
