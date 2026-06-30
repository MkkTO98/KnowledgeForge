# Report: KnowledgeForge Final Vertical Slice 0 Dependency Refinement

Date: 2026-06-30
Status: Completed; implementation not started
Scope: Final architectural evaluation of whether dependency declarations belong as first-class durable objects in Vertical Slice 0

## 1. Architectural evaluation

The remaining question was whether the dependency declaration in the five-object Slice 0 design deserves to exist as an independent durable knowledge object.

The answer is no for Vertical Slice 0.

Dependency declarations preserve important dependency semantics, but in this slice they do not independently satisfy the criteria for durable reusable knowledge objects.

## 2. Durable-object criteria assessment

| Criterion | Assessment |
|---|---|
| Exist independently | No. The dependency declaration is meaningful only as the claim's dependency posture. |
| Stable identity independent of owner | No. Its identity is derivative of the claim and its current dependencies. |
| Independently citable | Not convincingly. Consumers should cite the claim and inspect its dependency posture. |
| Independent provenance | No. Its provenance belongs with the claim revision/provenance record. |
| Independent lifecycle | No. Its lifecycle follows the claim's lifecycle and review state. |
| Meaningful if detached | No. Detached from the claim, it becomes orphaned metadata. |

## 3. Recommendation

Remove `dependency-claim-gdp-measures-output-to-concepts-and-evidence` as a durable object from Vertical Slice 0.

Keep dependency semantics inside the Claim's durable-object kernel:

- dependency posture: `dependencies listed`;
- dependency entries for both concepts and the evidence reference;
- dependency facets attached to each dependency entry;
- dependency information versioned together with the Claim.

## 4. Rationale

The architecture already requires every durable object to have dependency posture. Creating a separate dependency declaration object would duplicate this kernel responsibility as a new durable object.

This would introduce unnecessary object proliferation and blur the distinction between:

- reusable knowledge objects; and
- structured metadata describing a reusable knowledge object.

A separate dependency object may become justified later if a dependency assertion itself becomes independently reusable, citable, reviewable, and lifecycle-managed. In that case, it may be better modeled as a claim about dependency rather than as generic metadata. That need is not present in Slice 0.

## 5. Consequences of alternatives

### 5.1 Retain dependency declaration as durable object

Benefits:

- dependency semantics are visually explicit;
- future independent review could be imagined.

Costs:

- derivative identity;
- unclear independent lifecycle;
- unclear independent provenance;
- orphaned meaning if detached from claim;
- object proliferation;
- higher implementation effort;
- risk of graph-edge drift.

Conclusion: reject for Slice 0.

### 5.2 Incorporate dependency declarations into the Claim kernel

Benefits:

- preserves dependency posture/facets;
- versions dependencies with the owning claim;
- keeps object identity clean;
- avoids metadata-as-object proliferation;
- remains representation-neutral;
- lowers implementation effort while preserving architectural validation.

Costs:

- dependencies cannot be independently cited in Slice 0;
- future independently reusable dependency assertions may need later promotion.

Conclusion: adopt for Slice 0.

## 6. Updated Vertical Slice 0 object model

Final object ecosystem:

1. `concept-gdp`
2. `concept-aggregate-economic-output`
3. `claim-gdp-measures-aggregate-economic-output`
4. `evidence-ref-gdp-source-documentation`

The Claim owns:

- references to both concepts;
- reference to the evidence object;
- dependency posture;
- dependency entries and facets;
- revision history preserving stable identity.

## 7. Interaction diagram

```text
concept-gdp
  ▲
  │ referenced by / dependency of
  │
claim-gdp-measures-aggregate-economic-output
  ├─ references concept-gdp
  ├─ references concept-aggregate-economic-output
  ├─ supported_by evidence-ref-gdp-source-documentation
  ├─ dependency_posture: dependencies listed
  ├─ dependencies:
  │    - concept-gdp
  │    - concept-aggregate-economic-output
  │    - evidence-ref-gdp-source-documentation
  └─ revision_history: [revision 1, revision 2]
  │
  ▼
concept-aggregate-economic-output

evidence-ref-gdp-source-documentation
```

This remains a representation-neutral diagram, not a graph abstraction.

## 8. Readiness recommendation

Vertical Slice 0 is now implementation-ready after user authorization.

Implementation should be strictly limited to:

- four durable object fixtures;
- embedded dependency posture and dependency entries on the Claim;
- minimal deterministic validation;
- one end-to-end test;
- implementation-evidence report.

Do not add a dependency declaration object, relationship representation, mapping object, empirical/statistical discovery, graph traversal, API, database, ontology manager, lifecycle automation, governance workflow, confidence system, infrastructure, or visualization.

## 9. Files updated

- `docs/vertical_slice_0_implementation_design.md`
- `artifacts/decisions/D-20260630-vertical-slice-0-final-dependency-refinement.md`
- `artifacts/decisions/D-20260630-vertical-slice-0-refined-design.md` marked superseded
