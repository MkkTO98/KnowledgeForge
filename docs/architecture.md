# KnowledgeForge Foundational Architecture Specification

Date: 2026-06-29
Status: Provisional specification freeze candidate; implementation deferred
Project phase: Specification-only

## 1. Purpose

KnowledgeForge is the canonical reusable knowledge substrate of the Economic Intelligence Platform (EIP). It answers:

> What is known?

KnowledgeForge accumulates, organizes, versions, justifies, and serves reusable knowledge through governed knowledge interfaces while preserving provenance, uncertainty, competing explanations, confidence, evidence, revision history, and lifecycle state. In this specification-only phase, "serves" describes architectural responsibility and interface intent, not runtime infrastructure.

The initial domain is economics. The architecture is deliberately domain-extensible so that future knowledge domains can include companies, industries, products, regulations, supply chains, events, academic knowledge, geography, and other durable knowledge domains.

## 2. Architectural position

```text
Reality
  ↓
Observation systems       What happened?
  ↓
KnowledgeForge             What is known?
  ↓
Reasoning systems          What does this mean?
  ↓
Forecasting systems        What is likely to happen?
  ↓
Decision systems           What should be done?

Navigation systems         Knowledge discovery
Presentation systems       Communication
```

KnowledgeForge is a middle substrate. It consumes evidence references from observational systems and provides governed reusable knowledge interfaces for reasoning, navigation, forecasting, and decision systems without performing those downstream responsibilities itself.

## 3. Current phase boundary

KnowledgeForge currently owns only specification artifacts:

- project purpose;
- scope and non-goals;
- ownership boundaries;
- conceptual architecture;
- future knowledge object model;
- interface contracts;
- governance rules;
- roadmap and deferred implementation decisions;
- ambiguity register.

KnowledgeForge does not currently own:

- databases;
- runtime code;
- graph computation;
- APIs;
- statistical pipelines;
- source ingestion;
- services;
- visualization;
- deployment.

## 4. Scope

KnowledgeForge no longer treats semantic, structural, empirical, contextual, epistemic, and evolutionary knowledge as a flat class hierarchy. The Phase I review found that those terms mix different conceptual dimensions. Phase II preserves their intent by refactoring them into orthogonal components that durable knowledge objects may possess.

The enduring architectural abstraction is a governed, versioned knowledge model. Graphs, ontologies, relational schemas, APIs, and future storage designs are possible representations of this model, but none of them defines KnowledgeForge.

### 4.1 Identity component

Identity establishes what a knowledge object is and how it remains addressable over time. Durable object identity is stable across revisions; revision history belongs to the object rather than replacing it. Identity correction, split, and merge scenarios require governed architectural treatment rather than silent overwrite. Identity includes:

- stable identifier;
- object kind;
- name/title;
- domain;
- canonical description;
- aliases;
- canonical concept identity where applicable;
- source-indicator mapping identity where applicable;
- version identity;
- deprecation-safe historical addressability.

Canonical identity means canonical stewardship and addressability. It does not mean canonical truth. A new identity is expected when an object meaning splits, when multiple objects were incorrectly merged, when a prior identity was materially misidentified, or when a purported revision would change the object into a different knowledge object.

### 4.2 Content component

Content states what the object asserts, defines, relates, maps, limits, or preserves. Content includes the epistemic nature of the knowledge where applicable, such as definition, convention, empirical finding, theory, hypothesis, rejected hypothesis, methodological assumption, historical assertion, evidence evaluation, or limitation. Epistemic nature is distinct from lifecycle state, governance state, confidence, and representation form. Content may be:

- semantic: definitions, concepts, aliases, taxonomies, units, comparability semantics;
- structural: provenance-bearing theory records, dependency records, supply-chain structure, cited causal or structural claims, reusable domain structure;
- empirical: method-scoped reusable statistical claims derived from referenced evidence;
- methodological: reusable knowledge about methods, assumptions, limitations, applicability, biases, transformations, and comparability rules;
- mapping-oriented: source indicator to canonical concept mapping semantics;
- negative: failed, contradicted, unsupported, rejected, incompatible, or not-observed expected knowledge.

Content is not interpretation. KnowledgeForge may preserve a cited theory or empirical result as reusable knowledge, but downstream reasoning systems own applying it to explain current conditions or generate hypotheses.

### 4.3 Applicability component

Applicability states where, when, and under what conditions a knowledge object may be reused. It may include:

- economic regime;
- inflation regime;
- exchange-rate system;
- war, election, pandemic, crisis, regulatory change, or structural break context;
- geography;
- time period;
- institutional arrangement;
- method scope;
- source/evidence scope;
- units, transformations, frequency, sample, lag, or window where applicable.

Contextual knowledge is therefore usually an applicability component of another object rather than a separate peer class. Some contexts may also be durable objects when they have identity and provenance of their own.

### 4.4 Evidence component

Evidence explains why a knowledge object exists and how it is justified. It includes:

- provenance;
- evidence references;
- evidence evaluations;
- supporting evidence;
- weakening evidence;
- contradictory evidence;
- assumptions;
- limitations;
- confidence;
- uncertainty;
- derivation method;
- supporting literature.

Evidence references point to evidence owned elsewhere, especially observational evidence systems and source snapshots. Evidence evaluations belong to KnowledgeForge when they describe how the evidence supports, weakens, contradicts, or bounds a reusable knowledge claim.

### 4.5 Evolution component

Evolution describes how a knowledge object changes over time. The provisional lifecycle vocabulary remains:

```text
Observed → Candidate → Supported → Accepted → Questioned → Deprecated → Archived
```

This lifecycle is not a truth scale. Accepted means accepted for reuse under stated evidence and applicability conditions. Evolution also includes revision history, supersession, deprecation rationale, and continued historical addressability.

### 4.6 Governance component

Governance records how a knowledge object is stewarded and reviewed. It includes:

- ownership/stewardship metadata;
- review status;
- review authority or source of acceptance;
- lifecycle-transition rationale;
- dependency declarations;
- boundary constraints;
- downstream-use constraints;
- domain-expansion gate status where applicable.

Governance is distinct from confidence. A knowledge object can be reviewed but uncertain, accepted but narrow in scope, deprecated but still addressable, or candidate but useful for controlled downstream exploration.

### 4.7 First-class claims

KnowledgeForge stores durable knowledge claims as first-class architectural objects. A claim is a provenance-bearing assertion, definition, mapping, negative finding, methodological statement, or relationship statement that can be scoped, evidenced, versioned, reviewed, contradicted, deprecated, and reused.

Claims are classified through governed vocabularies and orthogonal facets, not rigid inheritance hierarchies. The initial architectural facets are:

- assertion function: what the claim is doing, such as defining, identifying, classifying, relating, scoping, measuring, evaluating evidence, limiting, contradicting, or preserving historical/contextual knowledge;
- epistemic nature: what kind of knowledge the claim is, such as definition, convention, empirical finding, theory, hypothesis, competing theory, rejected hypothesis, methodological assumption, historical assertion, evidence evaluation, or limitation;
- polarity: whether the claim asserts, denies, limits, rejects, contradicts, states incompatibility, or records non-observation;
- domain role: what domain structure the claim concerns, such as concept, indicator, mapping, method, event, entity, relationship, context/regime, or evidence source;
- representation form: how the claim may be represented, such as textual assertion, relationship representation, mapping representation, taxonomy placement, evidence evaluation, or dependency declaration.

These are governed vocabularies. They may be extended through KnowledgeForge governance, but they are not object subclasses and must not force KnowledgeForge into an inheritance-first ontology model.

Examples:

- Oil influences inflation.
- GDP measures economic output.
- Transportation costs transmit energy prices.
- A source indicator is only a proxy for a canonical concept.
- A statistical association was not observed under a stated method and evidence scope.

Relationships remain important, but they are one representation of claims rather than the primary abstraction. This prevents KnowledgeForge from becoming edge-centric or graph-defined.

### 4.8 Knowledge dependencies

Knowledge objects may depend on other knowledge objects. Dependencies preserve reasoning structure and support future review propagation without requiring computational implementation in the current phase. Every durable knowledge object must declare its dependency posture: dependencies listed, none known, not applicable, or unresolved.

Where dependencies are listed, they should eventually distinguish:

- dependency type, such as definitional, identity, methodological, evidence, assumption, applicability, derivation, contradiction, mapping, or taxonomic;
- necessity, such as required, supporting, contextual, optional/background, weakening/contradictory, or unresolved;
- strength, meaning reliance strength rather than confidence;
- direction, from dependent object to dependency object;
- scope, such as context, method, version, domain, or evidence scope;
- review-propagation meaning, such as must review, should review, review only if applicability overlaps, or no automatic review implied.

Examples:

- a claim depends on another claim;
- a relationship representation depends on concept identities;
- a theory record depends on assumptions;
- an empirical claim depends on methodological knowledge;
- a mapping depends on source metadata and comparability assumptions.

Dependencies are architectural declarations, not executable graph logic.

### 4.9 Knowledge change

Durable knowledge is rarely created or revised as isolated objects. KnowledgeForge therefore recognizes a conceptual knowledge change: a coherent governed change to one or more knowledge objects, such as adding a claim and its evidence evaluation, revising a mapping and dependent relationship representation, splitting a concept identity, or deprecating a method and marking affected claims for review.

A knowledge change is an architectural audit concept, not an implementation mechanism, transaction protocol, database feature, API, or workflow engine. It exists to preserve coherence, reviewability, and rationale when multiple durable objects change together.

## 5. Non-scope and forbidden overlap

KnowledgeForge shall not:

- generate reports;
- generate hypotheses;
- perform reasoning or interpretation;
- perform forecasting;
- make recommendations;
- own observational datasets;
- duplicate external observational ingestion, validation, canonicalization, lineage, reproducibility, or observational database responsibilities;
- implement visualization;
- become the EIP controller;
- become a general AI platform;
- own presentation-system concerns;
- own PredictionForge forecasting concerns;
- own DecisionForge action-selection concerns.

## 6. Knowledge object model, conceptual only

This is not a database schema. It is a conceptual contract that future implementation must satisfy.

### 6.1 Knowledge object

A reusable knowledge object is any durable, governed, versioned unit of reusable knowledge. Every durable knowledge object shares a common kernel and should eventually expose the six orthogonal components defined in this specification:

- identity;
- content;
- applicability;
- evidence;
- evolution;
- governance.

Not every component is equally rich for every object, but every durable object must at minimum include the common durable-object kernel: stable identity, object kind, content summary, provenance, applicability/scope posture, evidence state, lifecycle state, governance/review state, revision history, and dependency posture. Type-specific extensions may add richer fields, but no durable object is exempt from the kernel.

### 6.2 Claim object

A claim object is the primary unit of durable knowledge assertion. It may express a definition, relationship, mapping judgment, methodological statement, structural assertion, empirical finding, negative finding, limitation, or contradiction.

A claim should eventually include:

- claim identifier;
- claim facets from governed vocabularies;
- claim statement;
- referenced concepts, mappings, relationships, methods, contexts, or evidence;
- applicability conditions;
- evidence references and evidence evaluations;
- confidence and uncertainty scoped to the claim;
- assumptions and limitations;
- dependency posture and dependency declarations where applicable;
- lifecycle state;
- governance/review state;
- revision history.

Claims are not hypotheses generated by KnowledgeForge. A claim may preserve a hypothesis from literature or another source as reusable knowledge, but KnowledgeForge does not generate new hypotheses.

### 6.3 Concept node

A concept should support both graph and star exploration:

- upstream dependencies;
- downstream dependencies;
- alternative paths;
- supporting evidence;
- contradictions;
- applicable regimes;
- related concepts;
- known literature;
- confidence;
- revision history;
- source indicator mappings;
- units and transformations.

### 6.4 Relationship representation

Relationships are first-class versioned representations of claims. A relationship is not merely an edge between two nodes and should not define the project architecture. A relationship should eventually include:

- relationship identifier;
- relationship type, such as semantic, structural, empirical, methodological, mapping, dependency, contradiction, or applicability;
- source concept(s);
- target concept(s);
- direction;
- reciprocity;
- sign or qualitative effect where applicable;
- confidence;
- uncertainty;
- evidence references;
- statistical methods where applicable;
- derivation method;
- time validity;
- regime validity;
- geographic scope;
- source/provenance;
- revision history;
- lifecycle state;
- limitations;
- contradictions;
- review status;
- claim identifier or claim linkage;
- dependency declarations.

### 6.5 Indicator identity model

KnowledgeForge eventually owns the canonical concept layer and mapping semantics. External evidence systems own source observations and source indicator data.

```text
Source Evidence Indicator
  ↓ reference/mapping, not duplication
KnowledgeForge Canonical Concept
  ↓
KnowledgeForge Mapping Object
```

Mapping types:

- exact;
- equivalent;
- derived;
- proxy;
- incompatible;
- unknown.

Mappings should not erase source methodology differences. A source identity remains distinct even when mapped to a canonical concept.

## 7. Knowledge database posture

KnowledgeForge should eventually own a knowledge database or equivalent persistent knowledge store separate from external observational databases.

The knowledge store should contain reusable knowledge objects, claims, mappings, relationship representations, dependency declarations, methodological knowledge, negative knowledge, and references to evidence. It should not contain duplicated observational datasets.

V1 does not select the storage technology. Candidate storage concerns are deferred until implementation planning:

- graph traversal support;
- star exploration support;
- versioning;
- provenance queries;
- lifecycle queries;
- evidence-reference integrity;
- reproducible statistical relationship computation;
- human auditability;
- migration and export strategy.

## 8. Statistical discovery posture

KnowledgeForge should eventually compute or preserve reusable empirical claims and relationship representations because these are knowledge artifacts, not one-off analysis results.

However, statistical discovery must be governed carefully:

- computations must reference external evidence instead of duplicating observations;
- methods must be recorded;
- parameters/windows/frequencies must be recorded;
- multiple methods may disagree and must be preserved;
- empirical claims may be context-dependent;
- failed or not-observed expected relationships may be preserved as negative knowledge when evidence scope and method are explicit;
- statistical relationships are not causal claims unless separately justified by a structural claim;
- methodological assumptions and limitations must be represented as reusable methodological knowledge where they affect interpretation or reuse;
- downstream reasoning systems may interpret empirical claims, but KnowledgeForge must not generate analytical conclusions.

## 9. Interfaces

Detailed interfaces are in `docs/interfaces.md`. The high-level model is:

- Observation/evidence systems → KnowledgeForge: evidence references, observational identifiers, source metadata, reproducibility handles, or immutable source snapshots.
- KnowledgeForge → downstream reasoning/navigation/forecasting/decision systems: reusable concepts, claims, relationships, dependencies, evidence, uncertainty, contradictions, negative knowledge, methodological knowledge, lifecycle state.
- KnowledgeForge → AtlasForge: navigable knowledge structures, concept neighborhoods, relationship metadata, dependency metadata, evidence pointers.
- Downstream reasoning systems → presentation systems: reports and presentation-ready outputs; KnowledgeForge does not directly own presentation.
- KnowledgeForge → PredictionForge: reusable knowledge, empirical claims, relationship representations, methodological limitations, and negative knowledge; no forecasts.
- KnowledgeForge → DecisionForge: applicability conditions, contextual knowledge, uncertainty, constraints, and negative knowledge; no recommendations.

## 10. Governance

### 10.1 Specification-only governance

During the current phase, permitted work is limited to:

- architecture documents;
- decision artifacts;
- task artifacts;
- state and handoff updates;
- folder summaries;
- open-question capture;
- verification of file-backed coherence.

Forbidden work without explicit approval:

- runtime code;
- API implementation;
- database creation;
- graph engine setup;
- statistical computation pipelines;
- ingestion systems;
- external services;
- cross-project mutation;
- secrets or credentials;
- deployment.

### 10.2 Future implementation governance

Before implementation begins, KnowledgeForge must have accepted decisions for:

- knowledge object component and common-kernel model;
- claim facet governed vocabularies and claim object model;
- stable identity, revision, split, merge, and identity-correction semantics;
- source evidence reference contract;
- evidence evaluation model;
- canonical concept and source-indicator mapping contract;
- relationship representation contract;
- knowledge dependency posture and facet model;
- lifecycle state machine;
- confidence/uncertainty representation;
- governance/review state model;
- knowledge change audit concept;
- architectural invariants;
- storage selection;
- versioning model;
- statistical discovery boundary;
- first minimal vertical slice;
- verification strategy;
- migration/export strategy.

## 11. Artifact structure

The initial artifact structure is intentionally file-backed and specification-oriented:

```text
KnowledgeForge/
  README.md
  docs/
    architecture.md
    principles.md
    interfaces.md
    roadmap.md
    open_questions.md
    invariants.md
    governed_vocabularies.md
  artifacts/
    decisions/
      D-20260629-knowledgeforge-foundational-scope.md
    tasks/
      T-001-initial-validation.md
    reports/
      R-20260629-knowledgeforge-instantiation.md
  state/
    active_goal.md
    project_state.md
    architecture.md
  context/
    latest_handoff.md
  knowledge/
    _SUMMARY.md
```

Future implementation may add `src/`, `tests/`, `schemas/`, `db/`, `pipelines/`, or equivalent only after explicit implementation approval.

## 12. Architecture criticism and hidden assumptions

Important unresolved issues are intentionally captured in `docs/open_questions.md`. The largest architectural risks are:

1. The boundary between reusable empirical knowledge and analytical interpretation may become blurry.
2. Canonical identity is powerful but dangerous; premature merging could destroy source methodology distinctions.
3. A graph, ontology, database, or API representation could bias the architecture away from governed knowledge objects, claims, evidence, lifecycle, and human auditability.
4. Statistical discovery could produce spurious reusable objects unless lifecycle, evidence, methodological, and negative-knowledge gates are strong.
5. KnowledgeForge must support future domains without becoming a vague universal ontology project.
6. Claim granularity and dependency declarations may become inconsistent without explicit review guidance.

## 13. Exit criteria for specification phase

KnowledgeForge should remain specification-only until the following are stable:

- project boundaries are accepted;
- source-evidence and downstream-consumer contracts are accepted;
- knowledge object common-kernel model, claim facet model, dependency posture/facet model, stable identity semantics, and relationship representation model are specified enough for a minimal implementation;
- lifecycle, evidence, epistemic, and governance invariants are specified;
- first implementation slice is narrowly chosen;
- storage decision has an evidence-backed decision artifact;
- implementation tests/verification strategy is defined.

With the final consolidation applied, KnowledgeForge is mature enough for provisional specification freeze. Remaining implementation-pressure questions may be deferred if they do not change ownership boundaries, the common kernel, claim facets, stable identity, dependency posture, invariants, or representation neutrality.
