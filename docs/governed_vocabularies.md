# KnowledgeForge Governed Vocabularies

Status: Provisional specification vocabulary
Date: 2026-06-29
Implementation status: Specification-only; no schema, database, API, or runtime mechanism implied

This document defines the initial governed vocabulary posture for KnowledgeForge claim facets and dependency posture. These vocabularies are architectural controls, not object subclasses and not implementation enums.

The purpose is to prevent semantic overload while preserving representation neutrality. Future implementation may encode these vocabularies in files, schemas, tables, documents, graph labels, or another representation, but the vocabulary governance remains part of the knowledge model.

## 1. Governance rules

1. Vocabularies are extensible through KnowledgeForge governance.
2. Vocabulary extension must preserve EIP boundaries.
3. Vocabulary values should describe knowledge semantics, not implementation mechanics.
4. New values should be added only when existing values cannot represent a materially different knowledge meaning.
5. Vocabulary values do not create inheritance hierarchies.
6. Vocabulary values may combine across facets.

## 2. Claim facets

Claims are classified through orthogonal facets. A claim may require multiple facet values or an explicit unknown/unresolved value during early lifecycle states.

### 2.1 Assertion function

What the claim is doing.

Initial values:

- definitional;
- identity/equivalence;
- classification/taxonomy;
- relationship;
- applicability/scope;
- methodological;
- measurement/comparability;
- historical/contextual;
- structural/theoretical;
- empirical/statistical;
- evidence-evaluative;
- limitation/constraint;
- contradiction/incompatibility.

### 2.2 Epistemic nature

What kind of knowledge the claim is.

Initial values:

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
- limitation;
- contradiction;
- unknown/unresolved.

Epistemic nature is distinct from lifecycle state. A rejected hypothesis may be accepted as durable negative knowledge without being accepted as true.

### 2.3 Polarity

Whether the claim asserts, denies, limits, or records failure/absence.

Initial values:

- positive assertion;
- negative assertion;
- non-observation;
- rejection;
- incompatibility;
- limitation;
- contradiction;
- mixed/conditional;
- unknown/unresolved.

### 2.4 Domain role

What domain structure the claim concerns.

Initial values:

- concept;
- source indicator;
- canonical concept;
- mapping;
- method;
- event/context;
- entity;
- relationship;
- regime;
- evidence source;
- assumption;
- limitation;
- cross-domain object.

### 2.5 Representation form

How the claim may be represented without defining the claim.

Initial values:

- textual assertion;
- relationship representation;
- mapping representation;
- taxonomy placement;
- evidence evaluation;
- dependency declaration;
- method note;
- applicability condition;
- lifecycle/governance record.

Representation form does not determine truth, lifecycle state, or storage technology.

## 3. Dependency posture

Every durable knowledge object must declare one dependency posture.

Initial values:

- dependencies listed: known dependencies are declared;
- none known: no dependencies are currently known under the object's evidence and review state;
- not applicable: dependencies are not meaningful for this object type or object state;
- unresolved: dependencies are expected or suspected but not yet sufficiently identified.

## 4. Dependency facets

Where dependencies are listed, they should be classified by facets rather than treated as generic edges.

### 4.1 Dependency type

Initial values:

- definitional;
- identity;
- methodological;
- evidence;
- assumption;
- applicability;
- derivation;
- contradiction;
- mapping;
- taxonomic;
- historical/contextual;
- governance/review.

### 4.2 Dependency necessity

Initial values:

- required;
- supporting;
- contextual;
- optional/background;
- weakening/contradictory;
- unresolved.

### 4.3 Dependency strength

Initial values:

- strong;
- moderate;
- weak;
- unknown.

Dependency strength means reliance strength. It is distinct from confidence in the dependent object.

### 4.4 Dependency direction

Direction means:

```text
dependent object → dependency object
```

It does not mean causal direction, traversal direction, data-flow direction, or downstream consumer direction.

### 4.5 Dependency scope

Scope may include:

- context;
- method;
- version;
- domain;
- evidence scope;
- geography;
- time period;
- regime;
- applicability condition.

### 4.6 Review-propagation meaning

Initial values:

- must review dependent object;
- should review dependent object;
- review only if applicability overlaps;
- no automatic review implied;
- unresolved.

This is a conceptual governance signal. It does not imply automated graph computation or workflow execution.

## 5. Explicitly rejected vocabulary designs

KnowledgeForge rejects rigid claim inheritance hierarchies as the primary ontology design.

Rejected pattern:

```text
Claim
  DefinitionClaim
  EmpiricalClaim
  TheoryClaim
  NegativeClaim
  HistoricalClaim
```

Reason: a single claim may be both empirical and negative, methodological and limiting, or historical and contextual. Orthogonal facets preserve meaning without forcing premature subtype selection.
