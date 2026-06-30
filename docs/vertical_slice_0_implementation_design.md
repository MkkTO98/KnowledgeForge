# KnowledgeForge Vertical Slice 0 Final Implementation Design

Date: 2026-06-30
Status: Final proposal; implementation not yet started
Scope: Smallest complete object ecosystem for validating the frozen KnowledgeForge architecture
Implementation status: Design only
Supersedes: prior one-object design and five-object dependency-declaration design

## 1. Final refinement decision

Vertical Slice 0 should validate a minimal durable knowledge ecosystem, not merely serialize one object.

However, the separate dependency declaration object from the prior refined design should be removed.

The final Slice 0 object ecosystem is:

```text
Concept
Concept
Claim
Evidence Reference
```

The Claim owns dependency posture and dependency information inside its durable-object kernel. Dependency facets are versioned together with the Claim.

This preserves the architectural validation of dependencies while avoiding a durable object that does not independently satisfy durable reusable knowledge criteria.

## 2. Dependency declaration evaluation

A dependency declaration should not become an independent durable knowledge object in Vertical Slice 0.

Evaluation against durable-object criteria:

| Criterion | Assessment |
|---|---|
| Can it exist independently? | No. The dependency declaration is meaningful only as a dependency posture of the claim that owns it. |
| Can it possess stable identity independent of the owning object? | Not convincingly for Slice 0. Its identity is derivative of the claim and its current dependencies. |
| Can it be cited independently? | Usually no. Downstream consumers should cite the claim and inspect its dependency posture. |
| Can it accumulate independent provenance? | Not in this slice. The provenance for the dependency posture is part of the claim revision/provenance record. |
| Can it possess an independent lifecycle? | No. Its lifecycle follows the owning claim's revision and review state. |
| Does it remain meaningful if detached from the parent object? | No. Detached from the claim, it becomes orphaned metadata rather than reusable knowledge. |

Conclusion: the dependency declaration is metadata with structure, not a first-class durable knowledge object for Vertical Slice 0.

This does not mean dependencies are unimportant. It means dependency posture is part of the durable-object kernel and should be represented inside the object whose reasoning structure it describes unless a later case proves dependency semantics are independently reusable.

## 3. Goal

Implement the smallest end-to-end slice that proves these KnowledgeForge abstractions can work together without violating boundaries or letting representation technology define the architecture:

- concepts;
- claims;
- evidence references;
- dependency posture and dependency facets;
- revision history;
- durable-object kernel;
- stable identity;
- claim facets;
- provenance;
- representation neutrality.

The slice must still avoid:

- ontology management;
- graph traversal;
- generalized vocabularies;
- confidence engines;
- lifecycle automation;
- governance workflows;
- statistical discovery;
- storage technology decisions;
- APIs;
- databases;
- graph engines;
- visualization;
- infrastructure.

## 4. Final minimal object ecosystem

Vertical Slice 0 should contain exactly four durable knowledge objects:

1. Concept A: `concept-gdp`
2. Concept B: `concept-aggregate-economic-output`
3. Claim: `claim-gdp-measures-aggregate-economic-output`
4. Evidence Reference: `evidence-ref-gdp-source-documentation`

Revision history is required, but should be represented inside durable objects rather than as a separate durable object.

Dependency posture is required on every durable object through the durable-object kernel. For Slice 0, the Claim's dependency posture should list dependencies on both concepts and the evidence reference. Dependency facets should remain attached to the Claim and versioned with the Claim.

## 5. Interaction diagram

```text
Concept A
concept-gdp
  ▲
  │ referenced by / dependency of
  │
Claim
claim-gdp-measures-aggregate-economic-output
  │
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
Concept B
concept-aggregate-economic-output

Evidence Reference
evidence-ref-gdp-source-documentation
```

This diagram is not a graph model. It is a human-readable representation of object relationships. The same ecosystem could later be represented as files, tables, documents, graph nodes/edges, or another storage model.

## 6. Complete minimal object ecosystem

### 6.1 Concept A: GDP

Illustrative identity:

```text
concept-gdp
```

Illustrative content:

```text
Gross Domestic Product / GDP
```

Architectural abstraction validated:

- concept identity;
- stable durable identity;
- concept as reusable knowledge object;
- common durable-object kernel;
- concept referenced by claim;
- dependency posture on a non-claim object;
- revision history for non-claim object.

Why this cannot be adequately validated through another object:

A claim can mention text, but text mention does not prove that KnowledgeForge can maintain a reusable concept identity independent of a claim. Concept identity is a core abstraction because future claims, mappings, relationships, evidence evaluations, and downstream systems need stable references to the same concept.

Why necessary for Slice 0:

Without at least one concept object, the slice validates only claim serialization. It does not validate the concept-to-claim interaction that underlies reusable knowledge.

### 6.2 Concept B: Aggregate economic output

Illustrative identity:

```text
concept-aggregate-economic-output
```

Illustrative content:

```text
Aggregate economic output
```

Architectural abstraction validated:

- second concept identity;
- concept-to-concept distinction;
- claim connecting multiple concepts without becoming a graph edge;
- stable references across more than one concept;
- minimal semantic relation surface.

Why this cannot be adequately validated through Concept A:

A one-concept claim can validate that a claim points to a concept, but it does not validate that a claim can relate two durable concept identities while remaining claim-first and representation-neutral.

Why necessary for Slice 0:

The architecture will mostly be useful when claims connect, distinguish, classify, scope, or evaluate multiple reusable objects. Two concepts are the minimum needed to test that interaction without adding relationship representations or graph traversal.

### 6.3 Claim: GDP measures aggregate economic output

Illustrative identity:

```text
claim-gdp-measures-aggregate-economic-output
```

Illustrative statement:

```text
GDP measures aggregate economic output.
```

Required claim facets:

- assertion function: `measurement/comparability` or `definitional`;
- epistemic nature: `definition` or `convention`;
- polarity: `positive assertion`;
- domain role: `concept` or `canonical concept`;
- representation form: `textual assertion`.

Required dependency posture:

```text
dependency_posture: dependencies listed
```

Required dependency information:

```text
dependent object: claim-gdp-measures-aggregate-economic-output

dependencies:
  - object: concept-gdp
    dependency type: identity/definitional
    necessity: required
    direction: dependent object → dependency object
    review-propagation meaning: should review dependent object if dependency changes

  - object: concept-aggregate-economic-output
    dependency type: identity/definitional
    necessity: required
    direction: dependent object → dependency object
    review-propagation meaning: should review dependent object if dependency changes

  - object: evidence-ref-gdp-source-documentation
    dependency type: evidence
    necessity: required
    direction: dependent object → dependency object
    review-propagation meaning: should review dependent object if dependency changes
```

Architectural abstraction validated:

- claim-first architecture;
- governed claim facets;
- claim references to durable concepts;
- provenance-bearing assertion;
- evidence-supported reusable knowledge;
- dependency posture inside the durable-object kernel;
- dependency facets without a separate dependency object;
- stable identity across revision;
- lifecycle/governance state as metadata, not automation.

Why this cannot be adequately validated through concept objects:

Concepts identify reusable meanings. They do not assert the relationship between meanings. KnowledgeForge's central abstraction is durable claims about what is known, so Slice 0 requires at least one claim object.

Why necessary for Slice 0:

Without a claim, the slice would be a concept catalog and would fail to validate KnowledgeForge's claim-first model.

### 6.4 Evidence Reference: GDP source documentation

Illustrative identity:

```text
evidence-ref-gdp-source-documentation
```

Illustrative content:

```text
A pointer to source documentation, standards documentation, or an approved external evidence handle explaining GDP as a measure of economic output.
```

This may be a source-documentation reference rather than a MacroForge observational reference because the example is definitional, not empirical. If an appropriate MacroForge evidence handle already exists, it may be referenced. No observational data may be copied.

Architectural abstraction validated:

- evidence reference as distinct from claim;
- provenance/evidence pointer without data duplication;
- MacroForge boundary discipline where observational evidence would be referenced rather than owned;
- evidence component interaction with a claim;
- common durable-object kernel for evidence reference when treated as durable;
- dependency posture on an evidence object.

Why this cannot be adequately validated through the claim object:

Embedding evidence directly inside the claim would not prove that evidence references can be independently identified, reused, revised, and distinguished from evidence evaluations or observational data.

Why necessary for Slice 0:

KnowledgeForge's boundary with MacroForge depends on storing references, not duplicating observations. A separate evidence reference object is the smallest way to validate that boundary conceptually.

## 7. Revision history design

Revision history should not be a separate durable object in Vertical Slice 0.

Instead, each durable object should include a minimal revision history component. At least the claim object should have two revisions:

1. initial creation;
2. a wording/provenance/dependency-posture refinement that preserves stable identity.

The revised claim should retain the same durable identity.

The concepts and evidence reference may each have one initial revision entry unless implementation effort remains low enough to demonstrate one non-claim revision as well.

Architectural abstraction validated:

- revision history belongs to the durable object;
- stable identity persists across revisions;
- dependencies are versioned together with the object whose reasoning structure they describe;
- revisions do not replace object identity;
- object revision does not imply graph/database transaction machinery.

## 8. Object inclusion rationale summary

| Object | Validates | Why necessary |
|---|---|---|
| Concept A: GDP | Stable concept identity | A claim text cannot validate reusable concept identity |
| Concept B: aggregate economic output | Multi-concept claim interaction | One concept does not validate claim relations between durable meanings |
| Claim | Claim-first architecture, facets, and dependency posture | Concepts alone do not assert reusable knowledge or dependency semantics |
| Evidence Reference | Evidence boundary and provenance reference | Embedded evidence would not validate independent evidence references or MacroForge boundary discipline |

## 9. Object exclusions and rationale

### 9.1 Dependency declaration object

Excluded from Vertical Slice 0.

Reason: dependency declarations do not satisfy the durable-object criteria in this slice. They do not exist independently, do not have stable identity independent of the owning object, are not meaningfully cited outside the claim, do not accumulate independent provenance, do not have independent lifecycle, and become orphaned metadata if detached from the parent object.

Dependency semantics remain fully represented through the Claim's dependency posture and dependency information inside the durable-object kernel.

### 9.2 Relationship representation

Excluded.

Reason: the claim already connects two concepts. Adding a relationship representation would test a second representation of the claim and risk graph-first drift. Relationship representation should be Slice 1 or Slice 2 after the claim/concept/evidence/dependency-posture ecosystem works.

### 9.3 Mapping object

Excluded.

Reason: source-indicator mapping would introduce MacroForge source identity, comparability, methodology, and mapping-type semantics. That is important, but it is not necessary to validate the first ecosystem.

### 9.4 Evidence evaluation object

Excluded as a separate object.

Reason: Slice 0 needs an evidence reference. A minimal support/limitation note may exist inside the claim's evidence component, but a durable evidence evaluation object would introduce a richer epistemic model too early. It should follow once evidence references are proven.

### 9.5 Methodology object

Excluded.

Reason: the GDP definition example does not require a reusable method. Methodological claims are a good next-slice candidate.

### 9.6 Context/regime object

Excluded.

Reason: the example is not regime-conditioned. Adding a context object would validate applicability but broaden the slice beyond the revised objective.

### 9.7 Knowledge change object

Excluded.

Reason: knowledge change remains an architectural audit concept. Implementing it as a durable object in Slice 0 would prematurely choose an event/transaction representation. The implementation report can record that the coherent ecosystem was introduced together without creating a knowledge-change mechanism.

### 9.8 Revision object

Excluded.

Reason: revision history should be embedded in the durable object for Slice 0. Separate revision objects would prematurely imply event sourcing or transaction infrastructure.

### 9.9 Confidence object or engine

Excluded.

Reason: confidence can be a scoped field or posture. A confidence system is explicitly out of scope.

### 9.10 Lifecycle automation

Excluded.

Reason: lifecycle state should be represented, not automated.

### 9.11 Ontology or vocabulary manager

Excluded.

Reason: governed vocabularies already exist as specification documents. Slice 0 should read/use them conceptually, not implement a manager.

## 10. Consequences of alternatives

### Alternative A: retain dependency declaration as durable object

Benefits:

- makes dependency semantics highly explicit;
- could support independent review of dependency assertions in a future richer model;
- visually separates references from dependencies.

Costs:

- creates an object whose identity is derivative of the claim;
- risks object proliferation for metadata;
- implies dependency declarations may be independently citable/lifecycle-managed before that need is proven;
- complicates Slice 0 without increasing architectural validation;
- risks drifting toward graph-edge objects despite representation neutrality.

Assessment: reject for Slice 0.

### Alternative B: dependency posture lives in the Claim kernel

Benefits:

- preserves dependency semantics without object proliferation;
- keeps dependencies versioned with the object whose reasoning structure they describe;
- aligns with the durable-object kernel already requiring dependency posture;
- keeps Slice 0 smaller and more coherent;
- avoids graph-edge drift.

Costs:

- dependency declarations cannot be cited independently in Slice 0;
- future independently reusable dependency assertions may require later promotion to claims or another durable object type;
- claim object becomes slightly richer.

Assessment: adopt for Slice 0.

## 11. Minimal validation contract

The future implementation should include the smallest deterministic validation needed to test the ecosystem.

The validator should check only:

1. each object has the common durable-object kernel;
2. object identities are stable and unique within the slice;
3. concept objects can be referenced by the claim;
4. claim facets use governed values;
5. evidence reference is separate from the claim and does not embed observational data;
6. the claim declares dependency posture as `dependencies listed`;
7. the claim's dependency entries point from the claim to both concepts and the evidence reference;
8. dependency facets are present for listed dependencies;
9. dependency posture is declared on every durable object;
10. revision history exists and preserves stable identity;
11. no object declares graph/database/API representation as authoritative.

The validator should not implement:

- graph traversal;
- ontology management;
- dependency propagation;
- confidence scoring;
- lifecycle automation;
- governance workflow automation;
- statistical discovery;
- persistence abstraction layers.

## 12. Proposed future implementation shape

These files are proposed only. They should not be created until implementation is explicitly approved.

```text
knowledge/
  objects/
    concept-gdp.json
    concept-aggregate-economic-output.json
    claim-gdp-measures-aggregate-economic-output.json
    evidence-ref-gdp-source-documentation.json

src/ or tools/
  minimal validator for the four-object ecosystem

tests/
  one end-to-end Vertical Slice 0 test
```

A single `tools/validate_vertical_slice_0.py` script may be preferable to a package layout if it minimizes infrastructure. The implementation choice should be based on the lowest-cost way to validate the architecture, not on anticipated future packaging.

## 13. Phased implementation plan

Implementation should proceed only after this final design is accepted.

### Phase 0.1: Confirm object ecosystem

Acceptance criteria:

- four objects are accepted as the Slice 0 ecosystem;
- no dependency declaration object, relationship, mapping, methodology, context, revision, or knowledge-change object is added.

### Phase 0.2: Create four object fixtures

Acceptance criteria:

- all four objects have stable identities;
- all four objects include the durable-object kernel;
- the claim references both concepts and the evidence reference;
- the claim owns dependency posture and dependency entries for the concepts/evidence reference;
- evidence reference does not duplicate observational data.

### Phase 0.3: Demonstrate revision history

Acceptance criteria:

- the claim object has at least two revision entries;
- the claim's durable identity remains stable across revision;
- dependency posture changes are versioned with the claim;
- revision changes do not require new object identity unless meaning changes.

### Phase 0.4: Add minimal deterministic validation

Acceptance criteria:

- validator checks object kernels, references, dependency posture, dependency direction, vocabulary values, evidence-reference boundary, revision identity stability, and representation neutrality;
- validator does not introduce generalized infrastructure.

### Phase 0.5: Add one end-to-end test

Acceptance criteria:

- test loads all four objects;
- test validates interactions among concepts, claim, evidence reference, dependencies, and revisions;
- test proves the ecosystem requires no graph/database/API assumptions.

### Phase 0.6: Record implementation evidence

Acceptance criteria:

- implementation report states what architectural uncertainty was reduced;
- report identifies any friction in the frozen architecture;
- report lists next-slice candidates without generalizing prematurely.

## 14. Why the final slice is sufficient

The final slice is sufficient because it validates the interaction among the core primitives:

- concepts are durable identities, not inline claim text;
- claims assert reusable knowledge over durable concepts;
- evidence references remain separate from claims and outside observational ownership;
- dependency posture carries dependency semantics beyond generic links;
- revision history preserves stable identity;
- the ecosystem can be represented without graph/database/API assumptions.

This removes more architectural uncertainty than a single claim object while avoiding an unnecessary dependency-declaration object.

## 15. Why the final slice remains minimal

The slice uses exactly the objects needed to validate the revised objective:

- two concepts are the minimum for a claim connecting durable meanings;
- one claim is the minimum assertion and dependency owner;
- one evidence reference is the minimum evidence boundary test;
- embedded dependency posture is the minimum dependency semantics test;
- embedded revision history is the minimum revision test.

Anything else validates a later architectural concern.

## 16. Readiness recommendation

The final Vertical Slice 0 design is ready for implementation after user acceptance.

Implementation should be strictly limited to this four-object ecosystem, minimal validation, one end-to-end test, and an implementation-evidence report.

Do not begin dependency declaration objects, relationship representations, mappings, empirical/statistical claims, graph traversal, APIs, databases, ontology management, lifecycle automation, governance workflow automation, or confidence systems in Vertical Slice 0.
