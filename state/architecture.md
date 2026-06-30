# Architecture

Project: KnowledgeForge
Status: Provisional specification freeze; Vertical Slice 0 implemented, verified, and validator-hardened

## Architecture posture

KnowledgeForge is the canonical reusable knowledge substrate of the Economic Intelligence Platform. It answers: "What is known?"

The enduring architectural abstraction is a governed, versioned, provenance-bearing knowledge model. Graphs, ontologies, relational schemas, document stores, APIs, databases, and future interfaces are representations of that model, not defining abstractions.

KnowledgeForge now has a minimal Vertical Slice 0 implementation: four file-backed durable knowledge object fixtures, a deterministic invariant validator, and standard-library unittest coverage for valid and invalid invariant cases. It still does not own databases, graph computation, APIs, statistical pipelines, visualization, infrastructure, deployment, executable services, generalized frameworks, or MacroForge observational datasets.

## Core model

Durable knowledge objects are component-based:

1. Identity.
2. Content.
3. Applicability.
4. Evidence.
5. Evolution.
6. Governance.

Every durable knowledge object has a common kernel:

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

## Stable identity

Durable object identity is stable across revisions. Revisions belong to the object unless the object meaning splits, multiple objects were incorrectly merged, or the identity was materially misidentified.

Identity correction, split, and merge scenarios require governed treatment and historical traceability.

## Claims

Claims are first-class durable knowledge objects. Relationships are representations of claims, not the primary architectural abstraction.

Claims are classified through governed vocabularies and orthogonal facets rather than rigid subclasses:

- assertion function;
- epistemic nature;
- polarity;
- domain role;
- representation form.

## Dependencies

Every durable knowledge object declares dependency posture:

- dependencies listed;
- none known;
- not applicable;
- unresolved.

Where dependencies are listed, they should distinguish type, necessity, strength, direction, scope, and review-propagation meaning. Dependencies are architectural declarations, not executable graph logic.

## Knowledge change

KnowledgeForge recognizes knowledge change as an abstract audit concept for coherent governed changes affecting one or more durable knowledge objects. This is not a database transaction, API operation, workflow engine, graph operation, or implementation mechanism.

## Boundaries

KnowledgeForge owns reusable knowledge.

It does not own:

- observational data;
- ingestion;
- validation;
- canonical observational databases;
- reasoning;
- interpretation;
- report generation;
- visualization;
- forecasting;
- recommendations;
- downstream action selection.

## Authoritative architecture artifacts

- `docs/architecture.md`
- `docs/principles.md`
- `docs/invariants.md`
- `docs/governed_vocabularies.md`
- `docs/interfaces.md`
- `docs/roadmap.md`
- `docs/open_questions.md`
- `artifacts/decisions/D-20260629-knowledgeforge-provisional-specification-freeze.md`
- `artifacts/reports/R-20260629-final-architectural-consolidation-spec-freeze.md`
- `docs/vertical_slice_0_implementation_design.md`
- `artifacts/reports/R-20260630-vertical-slice-0-implementation-evidence.md`
- `artifacts/reports/R-20260630-vertical-slice-0-validator-hardening.md`

## Freeze posture

KnowledgeForge has entered provisional specification freeze and completed Vertical Slice 0. Future implementation planning may refine concrete contracts and representation choices, but should not reopen purpose, boundaries, representation neutrality, claim-first architecture, common durable-object kernel, stable identity, dependency posture, knowledge-change concept, or invariants unless implementation evidence reveals a real contradiction.
