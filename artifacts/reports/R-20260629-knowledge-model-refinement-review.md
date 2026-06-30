# Report: KnowledgeForge Knowledge Model Refinement Review

Date: 2026-06-29
Status: Review completed; recommendations not yet adopted
Scope: Claim ontology, stable identity, epistemic nature, knowledge object uniformity, dependency refinement
Implementation status: No implementation introduced

## Executive judgment

KnowledgeForge's Phase II architecture is strong enough to preserve, but the knowledge model needs one more ontology-level refinement before specification freeze.

The current architecture correctly makes claims first-class and defines common object components: identity, content, applicability, evidence, evolution, and governance. The main remaining risk is semantic overloading: a single generic claim object could end up carrying definitions, empirical findings, identity mappings, methodological assumptions, historical facts, theory statements, contradictions, and negative findings without enough internal ontology to keep them distinguishable at tens of millions of objects.

The review does not recommend a redesign. It recommends a small set of stabilizing refinements:

1. Treat claim classification as multi-dimensional, not a long subtype hierarchy.
2. Make stable identity independent from revisions for all durable knowledge objects.
3. Add epistemic nature as a distinct architectural facet, separate from lifecycle and confidence.
4. Preserve a common knowledge-object kernel while allowing type-specific extensions.
5. Refine dependencies by type, necessity, strength, direction, scope, and review-propagation meaning.

These refinements preserve KnowledgeForge's existing philosophy and avoid implementation commitments.

## 1. Architectural evaluation

### 1.1 Claim ontology

#### Current architecture

Phase II defines claims as first-class objects. A claim may express a definition, relationship, mapping judgment, methodological statement, structural assertion, empirical finding, negative finding, limitation, or contradiction.

This is directionally correct. It prevents relationships from becoming the primary abstraction and keeps KnowledgeForge knowledge-first rather than graph-first.

#### Evaluation

A single generic claim object is necessary but insufficient. If every durable assertion is only a claim with free-form content, KnowledgeForge will eventually lose semantic precision.

However, the right solution is not a large rigid hierarchy of claim subclasses. At multi-domain scale, a deep subtype tree would become brittle and domain-specific. The better decomposition is a small set of orthogonal claim facets.

Recommended claim facets:

1. Assertion function.
   What the claim is doing.

   Examples:
   - definitional;
   - identity/equivalence;
   - classification/taxonomy;
   - relationship;
   - applicability/scope;
   - methodological;
   - measurement/comparability;
   - historical/event;
   - structural/theoretical;
   - empirical/statistical;
   - evaluative-of-evidence;
   - limitation/constraint;
   - contradiction/incompatibility.

2. Polarity.
   Whether the claim asserts, denies, limits, or fails to find something.

   Examples:
   - positive assertion;
   - negative assertion;
   - non-observation;
   - rejection;
   - incompatibility;
   - limitation;
   - contradiction.

3. Epistemic nature.
   What kind of knowledge the claim is epistemically.

   Examples:
   - definition;
   - convention;
   - empirical finding;
   - theory;
   - hypothesis;
   - competing theory;
   - rejected hypothesis;
   - methodological assumption;
   - historical assertion.

4. Domain role.
   What domain structure the claim concerns.

   Examples:
   - concept;
   - indicator;
   - mapping;
   - method;
   - event;
   - entity;
   - relationship;
   - context/regime;
   - evidence source.

5. Representation form.
   How the claim may be represented without defining the claim.

   Examples:
   - textual assertion;
   - relationship representation;
   - mapping representation;
   - taxonomy placement;
   - evidence evaluation;
   - dependency declaration.

This decomposition avoids semantic overloading while preserving generality.

#### Current architecture sufficient?

Partially sufficient. Claims are correctly first-class, but the architecture should not freeze until it distinguishes claim facets at the ontology level.

### 1.2 Stable identity

#### Current architecture

The architecture already includes stable identifiers, version identity, revision history, and deprecation-safe historical addressability.

#### Evaluation

Stable identity independent of revisions should become explicit for every durable knowledge object:

- concepts;
- claims;
- mappings;
- methodologies;
- relationship representations;
- contexts/regimes where represented as objects;
- evidence evaluations;
- dependency declarations when they become durable reviewable objects.

The stable object identity should represent continuity of the object across revisions. Revisions should belong to the object rather than replace it.

A revision may change content, evidence, applicability, confidence, lifecycle, governance, or dependency state. It should not silently create a new identity unless the object's meaning has split or the old identity was mistaken.

#### Architectural consistency effect

This strengthens the existing component model:

- Identity is the stable anchor.
- Evolution contains revisions of that identity.
- Governance records why revisions were accepted.
- Evidence records what supports or weakens the current and prior versions.
- Applicability can narrow or expand across revisions without destroying identity.

#### Current architecture sufficient?

Mostly sufficient but under-specified. Stable identity exists implicitly; it should become an explicit invariant before freeze.

### 1.3 Epistemic nature

#### Current architecture

Phase II distinguishes lifecycle, governance, confidence, uncertainty, evidence, and negative knowledge. It does not yet explicitly separate epistemic nature from lifecycle state.

#### Evaluation

KnowledgeForge should explicitly distinguish epistemic nature.

Lifecycle answers: what governance/reuse state is this object in?

Examples:
- Candidate;
- Supported;
- Accepted;
- Questioned;
- Deprecated.

Epistemic nature answers: what kind of knowledge is this object?

Examples:
- definition;
- convention;
- empirical finding;
- theory;
- hypothesis;
- competing theory;
- rejected hypothesis;
- methodological assumption;
- historical assertion.

These are not the same. A definition can be Accepted. A hypothesis can be Accepted as a preserved hypothesis while not accepted as true. A rejected hypothesis can be Accepted as durable negative knowledge. A theory can be Supported but contested. A convention can be Accepted with low empirical content because conventions are not empirical findings.

Without this distinction, lifecycle states will be misread as epistemic judgments.

#### Interaction with existing model

Epistemic nature should be part of the content/evidence boundary:

- content states the claim;
- epistemic nature classifies what kind of knowledge the claim is;
- evidence explains why it is held or preserved;
- lifecycle says its governance/reuse status;
- confidence/uncertainty qualify belief under scope;
- applicability scopes when/where/methodologically it applies.

This does not require a new top-level component. It can be a required facet within the content/evidence model, or a subfacet of content with evidence implications. The architecture should explicitly state that it is distinct from lifecycle and confidence.

#### Current architecture sufficient?

Not sufficient for specification freeze. Epistemic nature should be added as a conceptual facet.

### 1.4 Knowledge object uniformity

#### Current architecture

Every durable knowledge object may possess identity, content, applicability, evidence, evolution, and governance.

#### Evaluation

A common model is correct and should be preserved.

At tens of millions of knowledge objects, the architecture needs a uniform kernel so all objects remain discoverable, reviewable, versionable, and governable. Without a common kernel, each domain and object type will invent its own lifecycle, provenance, identity, and evidence conventions.

Recommended common kernel:

1. Identity.
2. Object kind.
3. Content summary.
4. Provenance.
5. Applicability/scope, even if universal or not-applicable.
6. Evidence state, including explicit unsupported/candidate state where relevant.
7. Lifecycle state.
8. Governance/review state.
9. Revision history.
10. Dependency declarations, including explicit none/not-applicable where appropriate.

The phrase "every durable knowledge object explicitly references its dependencies" should be refined to avoid fake dependencies. Better invariant:

> Every durable knowledge object must explicitly declare its dependency posture: dependencies listed, none known, not applicable, or unresolved.

This prevents meaningless dependency fields while preserving review discipline.

#### Exceptions

No durable object should be exempt from identity, provenance, lifecycle/evolution, and governance.

However, object types may legitimately differ in richness:

- A concept may have aliases, units, taxonomic placement, and mappings.
- A claim may have assertion function, epistemic nature, polarity, evidence, and applicability.
- A method may have assumptions, limitations, applicable domains, and known biases.
- A mapping may have source/target identities, mapping type, comparability judgment, and lossiness.
- A relationship representation may have direction, reciprocity, sign, and endpoints.
- An evidence evaluation may have evidence reference, support/weakening/contradiction role, and evaluation rationale.

#### Current architecture sufficient?

Sufficient in principle, but the common kernel should be made explicit and dependency posture should be refined.

### 1.5 Knowledge dependencies

#### Current architecture

Dependencies preserve reasoning structure and support future review propagation. They are architectural declarations, not executable graph logic.

#### Evaluation

The current dependency model is directionally correct but too broad for specification freeze. Dependencies need conceptual facets so that a future knowledge object can distinguish "this cannot stand without X" from "X is helpful background."

Recommended dependency facets:

1. Dependency type.

   Examples:
   - definitional dependency;
   - identity dependency;
   - methodological dependency;
   - evidence dependency;
   - assumption dependency;
   - applicability dependency;
   - derivation dependency;
   - contradiction dependency;
   - mapping dependency;
   - taxonomic dependency.

2. Dependency necessity.

   Examples:
   - required;
   - supporting;
   - contextual;
   - optional/background;
   - weakening/contradictory;
   - unresolved.

3. Dependency strength.

   Examples:
   - strong;
   - moderate;
   - weak;
   - unknown.

Strength should not be confused with confidence. Strength describes how much the dependent object relies on the dependency. Confidence describes belief in a claim under scope.

4. Dependency direction.

   Direction should be explicit:

   ```text
   dependent object → dependency object
   ```

   This means "the first object relies on the second." It does not mean causal direction, graph traversal direction, or downstream consumer direction.

5. Dependency scope.

   A dependency may apply only under certain contexts, methods, versions, domains, or evidence scopes.

6. Review propagation meaning.

   A dependency should indicate what kind of review may be needed if the dependency changes.

   Examples:
   - must review dependent object;
   - should review dependent object;
   - review only if applicability overlaps;
   - no automatic review implied, dependency is background/contextual.

This remains conceptual. It does not require implementation mechanisms.

#### Current architecture sufficient?

Partially sufficient. Dependencies are correctly introduced, but they should be refined before freeze to avoid becoming untyped edges.

## 2. Recommended refinements

### Recommendation 1 — Add claim facets instead of a rigid claim subtype hierarchy

Adopt claim facets:

- assertion function;
- polarity;
- epistemic nature;
- domain role;
- representation form.

Rationale: prevents a generic claim object from becoming semantically overloaded while avoiding a brittle ontology tree.

### Recommendation 2 — Make stable identity independent of revision explicit

Add an invariant:

> Every durable knowledge object has stable identity independent of revision history. Revisions belong to the object unless the object's meaning splits, merges, or is found to have been misidentified.

Rationale: at scale, citations, dependencies, lifecycle, and governance require stable anchors.

### Recommendation 3 — Add epistemic nature as an explicit knowledge facet

Add epistemic nature distinct from lifecycle, governance, and confidence.

Recommended initial values should be small and extensible:

- definition;
- convention;
- empirical finding;
- theory;
- hypothesis;
- competing theory;
- rejected hypothesis;
- methodological assumption;
- historical assertion;
- evidence evaluation;
- limitation.

Rationale: KnowledgeForge must distinguish what kind of knowledge an object is, not only whether it is Accepted or Questioned.

### Recommendation 4 — Define a common durable-object kernel

Every durable object should share:

- identity;
- object kind;
- content summary;
- provenance;
- applicability/scope posture;
- evidence state;
- lifecycle state;
- governance/review state;
- revision history;
- dependency posture.

Rationale: uniformity is necessary for conceptual scaling and cross-domain consistency.

### Recommendation 5 — Replace mandatory dependencies with mandatory dependency posture

Refine the dependency invariant from:

> every durable knowledge object explicitly references its dependencies

To:

> every durable knowledge object explicitly declares its dependency posture: dependencies listed, none known, not applicable, or unresolved.

Rationale: prevents artificial dependency clutter while preserving epistemic discipline.

### Recommendation 6 — Refine dependency facets

Add conceptual dependency facets:

- type;
- necessity;
- strength;
- direction;
- scope;
- review-propagation meaning.

Rationale: untyped dependencies will become indistinguishable graph edges. Typed dependencies preserve review structure without introducing graph computation.

### Recommendation 7 — Clarify identity split/merge semantics architecturally

Before implementation planning, specify when a new object identity is required rather than a revision.

Examples requiring new identity or identity split:

- two concepts were incorrectly merged;
- a claim actually contains two separable assertions;
- a mapping was proxy rather than equivalent;
- a method name refers to materially different methodological variants;
- a historical entity changes legal/semantic identity.

Rationale: stable identity only works if split/merge semantics are governed.

### Recommendation 8 — Keep historical claims inside KnowledgeForge only when reusable

Historical claims should be supported, but carefully scoped.

KnowledgeForge may preserve durable historical claims when they serve reusable knowledge:

- regime dates;
- event occurrence claims;
- institutional changes;
- policy framework changes;
- structural breaks;
- domain-defining historical facts.

KnowledgeForge should not become a general event database or observational timeline. MacroForge/domain observational systems own observations; future reasoning systems interpret events.

Rationale: historical claims are needed for applicability and context, but they are a scope-creep risk.

## 3. Rationale summary

The recommendations are conservative. They do not change KnowledgeForge's purpose, boundaries, or representation-neutral posture.

They strengthen the model by separating:

- claim kind from claim object;
- object identity from object revision;
- epistemic nature from lifecycle state;
- common object kernel from type-specific extensions;
- dependency existence from dependency type/necessity/strength;
- relationship representation from claim semantics.

These distinctions matter more as KnowledgeForge grows across domains. A model that works for hundreds of economic concepts can fail at tens of millions of cross-domain objects if claim semantics, identities, epistemic nature, and dependencies are underspecified.

## 4. Potential risks if refinements are not adopted

### Risk 1 — Generic claim overload

Without claim facets, the claim object may become a catch-all container for unrelated semantics. Future agents may encode definitions, hypotheses, empirical findings, conventions, and contradictions inconsistently.

### Risk 2 — Lifecycle misread as truth

Without epistemic nature, lifecycle states such as Accepted or Deprecated may be mistaken for truth judgments. A rejected hypothesis accepted as durable negative knowledge could be misread as an accepted true claim.

### Risk 3 — Identity churn

Without stable identity independent of revision, citations, dependencies, downstream references, and historical review trails will become brittle.

### Risk 4 — Artificial dependency clutter

If every object must list dependencies without a dependency posture, future authors may create meaningless dependencies just to satisfy the rule.

### Risk 5 — Untyped dependency graph drift

Without dependency facets, dependencies become generic edges. This recreates the graph-first risk that Phase II intentionally avoided.

### Risk 6 — Cross-domain inconsistency

Without a common durable-object kernel, future domains will invent incompatible identity, provenance, evidence, lifecycle, and governance structures.

### Risk 7 — Historical scope creep

Without a boundary for historical claims, KnowledgeForge could drift into an event database or timeline system rather than preserving reusable historical knowledge.

## 5. Remaining unresolved architectural questions

These questions should be resolved or explicitly deferred before specification freeze.

1. Claim facet vocabulary.
   What is the minimal accepted list of assertion functions, polarities, epistemic natures, domain roles, and representation forms?

2. Claim granularity.
   When should a statement be one claim versus multiple claims?

3. Identity split/merge rules.
   When does a revision preserve identity, and when must a new identity be created?

4. Epistemic nature vocabulary.
   What initial vocabulary is stable enough across domains without becoming too abstract?

5. Historical claim boundary.
   Which historical/event claims belong in KnowledgeForge, and which belong to observational/event systems or InsightForge?

6. Dependency posture vocabulary.
   What are the accepted values for dependencies listed, none known, not applicable, and unresolved?

7. Review propagation semantics.
   What conceptual review obligation follows when a required dependency is deprecated, contradicted, split, or narrowed in applicability?

8. Confidence interaction.
   How should confidence interact with epistemic nature? For example, how should confidence apply to definitions, conventions, theories, and rejected hypotheses differently?

9. Evidence evaluation identity.
   Should evidence evaluations be first-class durable objects with stable identity, or always subordinate components of claims?

10. Taxonomy placement claims.
    Should taxonomic membership be modeled as claims, concept metadata, relationship representations, or all three depending on context?

## 6. Final assessment

The current architecture is stable enough to avoid major redesign. It is not yet precise enough for specification freeze.

The most important refinement is to prevent the first-class claim model from becoming a generic assertion bucket. The best path is a component-compatible claim-facet model, not a rigid inheritance hierarchy.

The second most important refinement is to make stable identity independent of revisions explicit for all durable knowledge objects.

The third is to introduce epistemic nature as a separate facet from lifecycle, governance, and confidence.

If these refinements are adopted, KnowledgeForge's knowledge model should remain conceptually valid at tens of millions of objects and across domains beyond economics without becoming graph-first, ontology-first, database-first, or implementation-driven.
