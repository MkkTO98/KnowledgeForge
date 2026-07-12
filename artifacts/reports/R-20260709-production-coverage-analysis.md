# Production Coverage Analysis Before Campaign 4

Date: 2026-07-09
Status: completed
Scope: Campaigns 0-3 accepted/rejected Knowledge Objects and production quality reports

## Production corpus summary

| Campaign | Accepted | Rejected | Acceptance rate | Determinism | Fingerprint stability | Duplicates |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Campaign 0 | 10 | 3 | n/a | true | true | false |
| Campaign 1 | 12 | 4 | 0.75 | true | true | false |
| Campaign 2 | 14 | 4 | 0.777778 | true | true | false |
| Campaign 3 | 12 | 4 | 0.75 | true | true | false |

Total accepted Knowledge Objects reviewed: 48.

## Accepted knowledge category coverage

Aggregate accepted category counts across Campaigns 0-3:

| Category | Accepted count | Coverage assessment |
| --- | ---: | --- |
| methodological | 12 | Strong current coverage; repeated across campaigns. |
| coverage | 12 | Strong current coverage; mostly WDI evidence-family scoped. |
| negative | 6 | Moderate coverage; missingness/release-null patterns exercised. |
| evidence_quality | 6 | Moderate coverage; WDI evidence quality exercised. |
| provenance | 4 | Low-moderate coverage; every campaign has at least one provenance object. |
| derived | 3 | Low coverage; deterministic derived transformations not yet volume-stressed. |
| classified | 3 | Low coverage; Campaign 4 naturally expands classification pressure. |
| factual | 2 | Low coverage; repository/WDI factual inventory statements only. |

## Evidence-reference coverage

All 48 accepted Knowledge Objects use exactly one evidence reference.

Implication:

- Single-source evidence handling is production-proven.
- Multi-source-package evidence references are not production-proven.
- This is a known gap, not a blocker before Campaign 4.

Roadmap coverage:

- Campaign 9 explicitly stresses multi-source-package evidence references.
- Campaign 10 stresses multi-campaign evidence references.

## Evidence family coverage

Covered:

- repository evidence snapshot;
- WDI annual-scalar demographic evidence quality/coverage;
- WDI demographic completeness buckets;
- WDI freshness/release metadata.

Not yet covered:

- second WDI annual-scalar non-demographic family;
- cross-family WDI comparison;
- production artifacts as first-class production evidence;
- local-model-assisted candidate drafts.

Roadmap coverage:

- Campaign 8 covers a second WDI family.
- Campaign 9 covers cross-family comparison.
- Campaign 10 covers production artifacts as evidence.
- Campaign 11 conditionally covers local-model-assisted screening.

## Production behavior coverage

Well covered:

- deterministic replay;
- canonical fingerprint stability;
- accepted provenance envelope presence;
- rejected source package preservation;
- basic constitutional-boundary rejection;
- missing provenance/fingerprint rejection;
- evidence-level freshness metadata;
- scoped negative knowledge.

Weakly covered:

- multi-reference accepted objects;
- later-stage malformed candidate/object rejection in production;
- valid near-duplicate or overlapping objects;
- partial provenance disagreement rather than absent provenance;
- large matrix-generated object sets;
- cross-family deterministic comparison.

## Coverage conclusion

Coverage is sufficient to proceed to Campaign 4. The key gaps are real, but Campaign 4 is a logical next falsification step for classification, inventory richness, and duplicate pressure. Later roadmap campaigns cover the heavier multi-reference, cross-family, provenance-lineage, and production-artifact gaps.
