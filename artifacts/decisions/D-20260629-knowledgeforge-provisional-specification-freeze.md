# Decision: KnowledgeForge Provisional Specification Freeze Consolidation

Date: 2026-06-29
Status: Accepted
Permission level: Specification-only architecture consolidation requested by user
Implementation status: No implementation introduced

## Decision

KnowledgeForge is accepted as a provisional specification-freeze candidate after final architectural consolidation.

The final consolidation adopts a narrow set of refinements from the knowledge model refinement review because they materially improve conceptual clarity and long-term maintainability without redesigning KnowledgeForge:

1. Claims are classified through governed vocabularies and orthogonal facets rather than rigid inheritance hierarchies.
2. Every durable knowledge object has a common durable-object kernel.
3. Durable object identity is stable across revisions.
4. Dependency posture is mandatory for every durable knowledge object.
5. Knowledge change is recognized as an abstract audit/governance concept for coherent multi-object changes.
6. Graphs, ontologies, relational schemas, databases, APIs, and interfaces remain representations of the governed knowledge model, not defining abstractions.

## Adopted refinements

### Claim facets as governed vocabularies

Adopted facets:

- assertion function;
- epistemic nature;
- polarity;
- domain role;
- representation form.

These are governed vocabularies, not subclasses.

### Durable-object kernel

Every durable knowledge object must share:

- stable identity;
- object kind;
- content summary;
- provenance;
- applicability/scope posture;
- evidence state;
- lifecycle state;
- governance/review state;
- revision history;
- dependency posture.

### Stable identity

Object identity remains independent of revision history. Revisions belong to the object unless the meaning splits, objects were incorrectly merged, or the identity was materially misidentified.

### Dependency posture

Every durable knowledge object must declare one dependency posture:

- dependencies listed;
- none known;
- not applicable;
- unresolved.

Where dependencies are listed, they should be classified by type, necessity, strength, direction, scope, and review-propagation meaning.

### Knowledge change

A knowledge change is accepted as an abstract architectural concept for coherent governed changes affecting multiple durable knowledge objects.

It is not an implementation mechanism, transaction protocol, API operation, graph operation, workflow engine, or database feature.

## Explicitly rejected refinements

### Rigid claim inheritance hierarchy

Rejected.

Reason: a claim can be empirical and negative, methodological and limiting, or historical and contextual. Rigid inheritance would force false exclusivity and create brittle domain-specific class trees.

### Representation-first architecture

Rejected.

Reason: KnowledgeForge is not a graph project, ontology project, database project, API project, or graph database. Those may become representations, but the architectural abstraction remains governed, versioned reusable knowledge.

### Implementation-specific transaction model

Rejected.

Reason: the need for coherent multi-object knowledge changes is real, but implementation mechanisms belong to future implementation planning.

### Additional broad architectural review before freeze

Rejected.

Reason: remaining questions are either already constrained by invariants or are expected to emerge from implementation pressure. Further abstract review would likely produce diminishing returns and premature optimization.

## Rationale

The adopted refinements address concrete architectural deficiencies:

- claim facets prevent semantic overload;
- the common kernel preserves cross-domain consistency;
- stable identity protects citations, dependencies, historical review trails, and downstream references;
- dependency posture prevents artificial dependency clutter while preserving review discipline;
- knowledge change acknowledges that durable knowledge often changes coherently across multiple objects;
- representation neutrality prevents premature coupling to graph/database/API choices.

The rejected refinements avoid unnecessary complexity and premature implementation design.

## Specification-freeze recommendation

KnowledgeForge should enter provisional specification freeze after this consolidation.

This freeze is provisional because implementation planning may still refine contracts, vocabulary details, validation mechanisms, storage decisions, and first-slice verification. Those should not reopen the core architecture unless they reveal a boundary violation or contradiction in the durable knowledge model.

## Issues requiring architectural resolution before implementation

Before implementation begins, KnowledgeForge still needs accepted implementation-readiness decisions for:

- concrete claim facet vocabulary governance;
- common durable-object kernel contract;
- stable identity, revision, split, merge, and correction semantics;
- dependency posture/facet contract;
- evidence reference contract with MacroForge;
- evidence evaluation model;
- relationship representation contract;
- lifecycle/governance/confidence/uncertainty contracts;
- first minimal vertical slice;
- storage and representation selection criteria.

## Issues intentionally deferred until implementation pressure

The following should not delay provisional freeze:

- exact storage technology;
- database/schema shape;
- API/interface mechanics;
- graph traversal mechanics;
- implementation validation rules;
- precise confidence scoring method;
- detailed lifecycle transition automation;
- large-scale statistical discovery design;
- performance/scaling engineering;
- UI/navigation representation;
- exact encoding of governed vocabularies.

## Non-changes

This decision does not introduce runtime code, databases, APIs, graph engines, statistical implementations, infrastructure, visualization, deployment, or generalized frameworks.

It does not move responsibilities from MacroForge, InsightForge, AtlasForge, BriefForge, PredictionForge, or DecisionForge into KnowledgeForge.
