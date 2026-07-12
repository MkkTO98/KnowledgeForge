# Remaining Falsification Roadmap — Phase 2

Date: 2026-07-09
Status: completed planning artifact

## Purpose

This roadmap identifies important assumptions not yet tested after Campaigns 0-12 and classifies how Phase 2 should address them.

## Falsification matrix

| Assumption | Current evidence | Classification | Phase 2 handling | Recommendation classification |
| --- | --- | --- | --- | --- |
| Method transfers beyond two WDI families | Demographic and Environment Mature | Naturally covered by planned production | Infrastructure, Energy, Agriculture | preserves agreed architecture |
| Existing taxonomy covers additional WDI families | PEL-011 across Campaigns 0-12 | Naturally covered by planned production | Monitor in each new family | preserves agreed architecture |
| Validators remain sufficient under higher-risk domain vocabulary | Boundary rejection active across campaigns | Naturally covered, then deliberately stressed | Trade/Financial after lower-risk families | preserves agreed architecture |
| Package contracts scale to larger object counts | Campaigns handled up to current family sizes; no duplicate pressure | Naturally covered by planned production | Education/Health later as scale test | preserves agreed architecture |
| Multi-reference objects remain stable beyond two-family comparison | Campaign 9 and Campaign 10 successful | Requiring deliberate future campaign | WDI multi-family comparison after more families | preserves agreed architecture |
| Non-WDI multi-source disagreement fits existing model | Still major gap in PEL-017 | Requiring deliberate future campaigns | Later non-WDI disagreement workstream | preserves agreed architecture |
| Local-model-assisted candidate screening is needed | Campaigns 0-12 accepted deterministic outputs | Intentionally deferred | Revisit only after repeated manual screening pressure | preserves agreed architecture |
| Cross-campaign duplicate registry is needed | No duplicates across Campaigns 0-12 | Intentionally deferred/rejected for now | Monitor only; do not implement | preserves agreed architecture |
| Additional helper extraction is needed | PEL-008/009 satisfied by Production Support; no new pressure | Intentionally deferred/rejected for now | Monitor only | preserves agreed architecture |
| Runtime infrastructure is needed | No production evidence of need | Intentionally deferred | Not part of Phase 2 | preserves agreed architecture |

## Deliberate future falsification workstreams

1. WDI multi-family comparison after three or four families.
2. Higher-boundary-risk WDI family maturation through Trade/Financial Sector.
3. Scale-family maturation through Education or Health.
4. Non-WDI multi-source disagreement after WDI breadth stabilizes.

## Intentionally deferred assumptions

- Local/frontier LLM generation for accepted knowledge.
- Runtime service/API/database behaviour.
- Generic adapter or shared schema infrastructure.
- Cross-campaign duplicate registry.
- Additional helper extraction.

These are deferred because Campaigns 0-12 show no repeated production evidence proving current design insufficient.

## Architectural continuity conclusion

The falsification roadmap preserves the existing architecture. It treats unanswered assumptions as monitoring and sequencing inputs, not architecture-change authorization.
