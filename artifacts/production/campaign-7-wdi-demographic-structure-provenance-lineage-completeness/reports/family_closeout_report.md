
# WDI Demographic Production Family Closeout Report

Status: Mature
Evidence base: Campaigns 1-7

## Capabilities validated

- deterministic package construction and replay;
- stable package fingerprints;
- provenance completeness;
- rejected-candidate preservation;
- evidence-quality coverage;
- completeness buckets;
- freshness and release metadata;
- indicator-family inventory;
- territorial coverage matrices;
- temporal coverage matrices;
- provenance-lineage completeness;
- scoped negative knowledge.

## Production assumptions confirmed

- The existing KnowledgeForge package hierarchy is sufficient for this evidence family.
- Existing validators reject malformed provenance, missing lineage fingerprints, unsupported categories, and unsafe boundary language.
- Existing categories support the planned WDI demographic evidence-level scopes without taxonomy change.
- Deterministic computation is sufficient; accepted knowledge generation did not require local or frontier LLMs.
- Current campaign-local duplicate checks are sufficient for observed production conditions.

## Assumptions intentionally deferred

- Multi-reference accepted objects: defer to cross-family WDI comparison.
- Partial provenance disagreement: defer until multi-source evidence exists.
- Non-demographic WDI transfer: defer to Campaign 8.
- Local-model-assisted candidate screening: remains unjustified until repeated manual screening pressure exists.

## Production pressures resolved

- Repeated SourceEvidencePackage authoring and common production-quality metric aggregation were resolved by the bounded Production Support layer.
- Family maturity vocabulary is usable as task/report vocabulary without architecture change.

## Production pressures still open

- PEL-012 remains open for multi-reference evidence.
- PEL-017 remains narrowed but open for multi-source and later-stage rejection pressure.
- Cross-family transfer remains untested until Campaign 8.

## Lessons learned

- Mature status should require multiple deterministic campaigns, not a single successful run.
- Rejected candidates are necessary evidence, not noise.
- Missingness and unsupported scope can be valuable negative knowledge when tightly scoped.
- Architecture changes should wait for repeated production pressure.
- Deterministic runners and immutable snapshots are sufficient for early production-family maturation.

## Recommended maturity criteria for future evidence families

Future evidence families should be considered Mature only after they demonstrate:

1. deterministic replay and fingerprint stability across multiple campaign scopes;
2. provenance completeness and lineage/fingerprint validation;
3. rejected-candidate preservation with meaningful failure categories;
4. no required taxonomy, validator, package-model, or architecture change;
5. scoped negative knowledge where missingness or unsupported dimensions exist;
6. at least one inventory/classification scope and one coverage/matrix scope when applicable;
7. explicit classification of assumptions deferred to cross-family or multi-source campaigns.

## Recommended next practice

Before broadening, run a bounded Campaign 8 planning gate to select one non-demographic WDI annual-scalar evidence family and define a narrow deterministic scope.
