# Decision: KnowledgeForge Vertical Slice 0 Final Dependency Refinement

Date: 2026-06-30
Status: Proposed; awaiting acceptance before implementation
Implementation status: Design only; no runtime implementation introduced
Supersedes: `D-20260630-vertical-slice-0-refined-design.md` five-object proposal

## Decision

Do not retain dependency declarations as independent durable knowledge objects in Vertical Slice 0.

Instead, dependency posture and dependency information should live inside the owning durable object's common kernel. For Slice 0, the Claim owns its dependency posture and dependency entries.

The final Vertical Slice 0 ecosystem should contain exactly four durable objects:

1. `concept-gdp`
2. `concept-aggregate-economic-output`
3. `claim-gdp-measures-aggregate-economic-output`
4. `evidence-ref-gdp-source-documentation`

Revision history remains embedded inside durable objects.

## Architectural evaluation

Dependency declarations do not satisfy the durable-object criteria in Slice 0:

- they do not exist independently of the owning claim;
- their identity is derivative of the owning claim and current dependencies;
- they are not meaningfully cited independently;
- their provenance belongs to the claim revision/provenance record;
- their lifecycle follows the claim lifecycle;
- detached from the claim, they become orphaned metadata rather than reusable knowledge.

Therefore, dependency declarations are structured metadata with architectural importance, not first-class durable knowledge objects for this slice.

## Rationale

The durable-object kernel already requires dependency posture. Placing dependency information inside the Claim preserves the architectural abstraction while reducing object proliferation.

This keeps Slice 0 focused on the real architectural interaction:

```text
Concept + Concept + Claim + Evidence Reference
```

where the Claim records dependencies on both concepts and the evidence reference.

## Consequences

### Consequences of removing the dependency declaration object

Benefits:

- smaller implementation slice;
- fewer durable objects with derivative identity;
- dependencies remain versioned with the object whose reasoning structure they describe;
- less risk of graph-edge drift;
- clearer durable-object boundary.

Costs:

- dependency declarations cannot be independently cited in Slice 0;
- future independently reusable dependency assertions may need promotion to claims or another durable object type;
- the claim object carries richer dependency metadata.

### Consequences if it had been retained

Benefits:

- explicit standalone dependency record;
- possible future independent review of dependency assertions.

Costs:

- unnecessary object proliferation;
- unclear independent identity;
- unclear independent lifecycle;
- risk of treating dependency metadata as graph-edge objects;
- increased implementation effort without improved Slice 0 architectural validation.

## Implementation boundary

This decision does not authorize implementation by itself. It records the final design refinement.

Implementation may begin only after this final design is accepted and should remain limited to the four-object ecosystem, minimal deterministic validation, one end-to-end test, and an implementation-evidence report.

## Reference

Detailed final design:

- `docs/vertical_slice_0_implementation_design.md`
