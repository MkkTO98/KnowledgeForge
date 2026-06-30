# KnowledgeForge Architectural Principles

## 1. Knowledge is not observation

MacroForge owns observations: what was measured, where it came from, how it was canonicalized, and how it can be reproduced.

KnowledgeForge owns reusable knowledge: concepts, definitions, claims, relationship representations, mappings, dependencies, evidence evaluations, uncertainty, provenance, lifecycle, governance state, methodological knowledge, and negative knowledge.

Knowledge objects may reference MacroForge evidence. They must not duplicate MacroForge datasets.

## 2. KnowledgeForge does not determine truth

KnowledgeForge is not a truth oracle. It preserves epistemic structure:

- why a knowledge object exists;
- where it came from;
- how it was derived;
- what supports it;
- what weakens it;
- what contradicts it;
- what assumptions it depends on;
- how confident the project is;
- when and where it is valid;
- what lifecycle state it currently holds.

Canonical means canonical stewardship, identity, and addressability. It does not mean canonical truth.

## 3. Knowledge objects are component-based, not single-class

The previous semantic/structural/empirical/contextual/epistemic/evolutionary class list is replaced by orthogonal components that durable knowledge objects may possess:

- identity;
- content;
- applicability;
- evidence;
- evolution;
- governance.

This preserves the intent of the original classes while avoiding forced classification. A single empirical claim can have semantic dependencies, contextual applicability, epistemic evidence, lifecycle state, and governance state.

## 4. Claims are first-class knowledge objects

KnowledgeForge primarily preserves durable knowledge claims. A claim is a scoped, provenance-bearing assertion that can be evidenced, contradicted, versioned, reviewed, deprecated, and reused.

Claims may express definitions, relationships, mappings, methodological statements, empirical findings, structural assertions, limitations, contradictions, or negative findings. Claims are classified by governed vocabularies and orthogonal facets rather than rigid object subclasses. Initial facets are assertion function, epistemic nature, polarity, domain role, and representation form.

KnowledgeForge may preserve claims from evidence and literature. It must not generate hypotheses, perform reasoning, or decide what those claims imply for current analysis.

## 5. Relationships are representations of claims

A relationship is not merely an edge between two nodes and KnowledgeForge is not a graph project. A relationship is a versioned representation of one or more claims with identity, type, direction, confidence, evidence, uncertainty, provenance, applicability conditions, revisions, dependencies, and lifecycle state.

Graphs, ontologies, relational schemas, APIs, and future interfaces may be derived from the governed knowledge model. No representation choice defines the architecture.

## 6. Canonical concepts are separated from source indicators

Source indicators are not collapsed into canonical concepts prematurely.

```text
Source Indicator
  ↓
Canonical Concept
  ↓
Mappings
```

Mappings must support at least: exact, equivalent, derived, proxy, incompatible, and unknown.

Mappings are typed and reversible. Source identity, methodology, and lossiness must remain inspectable.

## 7. Applicability is mandatory

Reusable knowledge is frequently regime-, time-, geography-, method-, source-, or context-dependent. KnowledgeForge must model applicability conditions rather than forcing universal claims.

Contextual information is usually an applicability component of a claim, relationship, mapping, method, or concept. It may become a standalone knowledge object only when it has its own identity, provenance, and lifecycle.

## 8. Evidence references and evidence evaluations are distinct

Evidence references identify source material, observations, literature, or reproducibility handles. Evidence evaluations describe how that evidence supports, weakens, contradicts, bounds, or fails to support a knowledge object.

MacroForge may own observational evidence references. KnowledgeForge owns reusable evaluations of how evidence relates to knowledge claims, without duplicating observational datasets.

## 9. Dependencies are explicit

Every durable knowledge object must explicitly declare its dependency posture: dependencies listed, none known, not applicable, or unresolved. This avoids artificial dependencies while preserving review discipline.

Dependencies may connect claims, concepts, mappings, methods, assumptions, evidence evaluations, contexts, and relationship representations. Where dependencies are listed, they should distinguish type, necessity, strength, direction, scope, and review-propagation meaning. They preserve reasoning structure and support future review propagation without requiring current computational implementation.

## 10. Durable identity is stable across revisions

Every durable knowledge object has stable identity independent of revision history. Revisions belong to the object unless the object meaning splits, multiple objects were incorrectly merged, or the identity was materially misidentified. Deprecated or corrected objects remain historically addressable.

## 11. Negative knowledge is reusable knowledge

Expected relationships that fail, rejected mappings, contradicted claims, unsupported hypotheses from literature, known limitations, and failed empirical relationships should be preserved when evidence scope and method are explicit.

Negative knowledge prevents rediscovery, preserves uncertainty, and protects downstream systems from repeatedly treating absence, contradiction, or incompatibility as unexplored territory.

## 12. Methodological knowledge is distinct from domain knowledge

KnowledgeForge may preserve reusable methodological knowledge: assumptions, limitations, biases, comparability rules, transformation semantics, applicability constraints, and methodological relationships.

Methodological knowledge supports reuse and evaluation. It is not source ingestion, statistical implementation, analysis, prediction, or recommendation.

## 13. Knowledge changes are coherent audit concepts

Durable knowledge is often created or revised through coherent multi-object changes. KnowledgeForge recognizes knowledge change as an abstract governance/audit concept for grouped conceptual revisions. It is not a database transaction, API operation, workflow engine, or implementation mechanism.

## 14. Specification precedes implementation

KnowledgeForge begins as an architectural specification project because premature runtime decisions would create hard-to-remove coupling across the EIP.

No runtime implementation, database, API, graph engine, statistical pipeline, or visualization system should be introduced until the ownership model, knowledge object model, lifecycle model, invariants, and project interfaces have stabilized.

## 15. Future implementation must not require architectural redesign

Although implementation is deferred, the architecture must be implementation-ready. The project should be able to evolve into a persistent knowledge store, relationship computation system, and downstream knowledge provider without changing its purpose or boundaries.

## 16. Human exploration and graph algorithms both matter

Knowledge should support graph traversal, but KnowledgeForge must not be reduced to a graph database mental model. Each concept should also support star exploration: upstream dependencies, downstream dependencies, alternatives, evidence, contradictions, regimes, literature, confidence, and revision history.

## 17. Downstream consumers do not govern KnowledgeForge

InsightForge, AtlasForge, BriefForge, PredictionForge, DecisionForge, and future projects may consume KnowledgeForge through governed knowledge interfaces. They do not own its durable knowledge structures, lifecycle rules, evidence evaluation rules, or invariants.

## 18. KnowledgeForge does not govern downstream interpretation

KnowledgeForge can provide reusable knowledge and uncertainty. It must not decide what it means, what will happen next, or what should be done.

Citation or use of KnowledgeForge objects does not imply that KnowledgeForge approves downstream reasoning, forecasts, reports, or decisions.
