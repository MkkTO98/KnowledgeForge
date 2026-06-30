# Report: KnowledgeForge Vertical Slice 0 Design Refinement

Date: 2026-06-30
Status: Superseded by `R-20260630-final-vertical-slice-0-dependency-refinement.md`; implementation not started
Scope: Refine Vertical Slice 0 to validate architectural interactions rather than isolated serialization

## 1. Architectural evaluation

The prior one-claim Vertical Slice 0 design was too narrow.

It validated:

- object serialization;
- portions of the durable-object kernel;
- claim facets;
- basic stable identity;
- basic evidence reference posture.

It did not adequately validate:

- concepts as durable reusable identities;
- claims referencing durable concept objects rather than inline text;
- evidence references as separately addressable durable objects;
- dependency semantics beyond ordinary references;
- revision history across an interacting object ecosystem.

Therefore refinement is justified.

## 2. Refined Vertical Slice 0 design

Vertical Slice 0 should validate a minimal durable knowledge object ecosystem containing exactly five durable objects:

1. `concept-gdp`
2. `concept-aggregate-economic-output`
3. `claim-gdp-measures-aggregate-economic-output`
4. `evidence-ref-gdp-source-documentation`
5. `dependency-claim-gdp-measures-output-to-concepts-and-evidence`

Revision history should be embedded inside objects rather than implemented as a separate durable object.

## 3. Interaction diagram

```text
concept-gdp
  │
  │ referenced by
  ▼
claim-gdp-measures-aggregate-economic-output
  ▲            │             ▲
  │            │ supported by│
  │            ▼             │
concept-aggregate-economic-output
evidence-ref-gdp-source-documentation
  ▲
  │ dependency declaration records required dependencies
  │
dependency-claim-gdp-measures-output-to-concepts-and-evidence

revision_history is embedded in durable objects and preserves stable identity.
```

This is not a graph architecture. It is a representation-neutral interaction diagram.

## 4. Architectural abstraction validated by each object

| Object | Validated abstraction | Why it cannot be validated elsewhere | Why necessary |
|---|---|---|---|
| `concept-gdp` | Durable concept identity | Claim text is not reusable identity | Required to prove concepts are first-class reusable references |
| `concept-aggregate-economic-output` | Multi-concept claim interaction | One concept cannot validate relation over multiple durable meanings | Required to test claims connecting concepts without graph-first drift |
| `claim-gdp-measures-aggregate-economic-output` | Claim-first architecture, facets, provenance-bearing assertion | Concepts do not assert knowledge | Required because KnowledgeForge stores reusable claims |
| `evidence-ref-gdp-source-documentation` | Evidence reference distinct from claim and observational data | Embedded evidence would not validate independent evidence reference or boundary discipline | Required to test provenance/reference boundary |
| `dependency-claim-gdp-measures-output-to-concepts-and-evidence` | Dependency posture/facets and dependency direction | Ordinary references do not express dependency type, necessity, direction, or review meaning | Required to test dependency semantics without graph traversal |

## 5. Rationale for included objects

The five objects are the smallest set that validates the revised objective:

- two concepts: minimum needed for a claim connecting durable meanings;
- one claim: minimum assertion unit;
- one evidence reference: minimum evidence/provenance boundary test;
- one dependency declaration: minimum semantic dependency test;
- embedded revision history: minimum stable identity/revision test.

## 6. Rationale for excluded objects

Excluded from Vertical Slice 0:

- relationship representation: would prematurely test a second representation of a claim and risk graph-first drift;
- mapping object: would introduce source-indicator/MacroForge comparability complexity too early;
- evidence evaluation object: useful later, but evidence reference is the required first boundary test;
- methodology object: not needed for a definition-style claim;
- context/regime object: not needed for the GDP definition example;
- knowledge change object: would prematurely imply event/transaction infrastructure;
- separate revision object: would prematurely imply event sourcing;
- confidence object/engine: explicitly out of scope;
- lifecycle automation: state can be represented without automation;
- ontology/vocabulary manager: governed vocabularies already exist as documents;
- graph/database/API/infrastructure: representation choices remain subordinate.

## 7. Recommendation

The refined Vertical Slice 0 is ready for implementation after user acceptance.

The implementation should be strictly limited to:

- five object fixtures;
- minimal deterministic validation;
- one end-to-end test;
- an implementation-evidence report.

Do not add relationship representations, mappings, empirical claims, graph traversal, APIs, databases, ontology management, governance workflows, lifecycle automation, confidence systems, statistical discovery, infrastructure, or visualization.

## 8. Files updated

- `docs/vertical_slice_0_implementation_design.md`
- `artifacts/decisions/D-20260630-vertical-slice-0-refined-design.md`
- `artifacts/decisions/D-20260630-vertical-slice-0-design.md` marked superseded
