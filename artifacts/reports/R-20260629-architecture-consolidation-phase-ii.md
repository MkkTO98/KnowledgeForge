# Report: KnowledgeForge Architectural Consolidation — Phase II

Date: 2026-06-29
Status: Consolidation completed
Scope: Adopt accepted Phase I architectural review outcomes into specification
Implementation status: No implementation introduced

## Executive summary

Phase II consolidated KnowledgeForge's architecture without introducing runtime code, graph engines, databases, APIs, statistical implementations, visualization, infrastructure, deployment, or generalized frameworks.

The central change is architectural, not operational: KnowledgeForge is now specified as a governed, versioned knowledge model whose durable objects are described through orthogonal components rather than a flat knowledge-class taxonomy.

The consolidated architecture preserves the original purpose:

> KnowledgeForge is the canonical reusable knowledge substrate of the EIP. It answers: "What is known?"

It clarifies that KnowledgeForge serves downstream projects through governed knowledge interfaces, while remaining distinct from implementation-time service/API choices.

## Changes made

### 1. Replaced the flat knowledge-class model

Updated:

- `docs/architecture.md`
- `docs/principles.md`
- `state/architecture.md`

The previous peer list of semantic, structural, empirical, contextual, epistemic, and evolutionary knowledge was replaced by six orthogonal components:

1. Identity.
2. Content.
3. Applicability.
4. Evidence.
5. Evolution.
6. Governance.

The old concepts were not discarded. They were repositioned:

- semantic, structural, empirical, methodological, mapping-oriented, and negative knowledge belong primarily to content;
- contextual knowledge usually becomes applicability;
- epistemic knowledge becomes evidence/provenance/confidence/uncertainty;
- evolutionary knowledge becomes lifecycle/revision history;
- review/stewardship becomes governance.

### 2. Introduced claims as first-class architectural objects

Updated:

- `docs/architecture.md`
- `docs/principles.md`
- `docs/interfaces.md`
- `state/architecture.md`

KnowledgeForge now treats durable knowledge claims as first-class objects.

A claim may express a definition, relationship, mapping judgment, methodological statement, structural assertion, empirical finding, negative finding, limitation, or contradiction.

Relationships remain first-class versioned representations, but they are now explicitly representations of claims rather than the primary architectural abstraction.

### 3. Introduced knowledge dependencies

Updated:

- `docs/architecture.md`
- `docs/principles.md`
- `docs/interfaces.md`
- `docs/roadmap.md`
- `docs/invariants.md`

Knowledge objects may now explicitly depend on other knowledge objects. Dependencies are architectural declarations that preserve reasoning structure and support future review propagation.

No computational graph implementation was introduced.

### 4. Introduced negative knowledge

Updated:

- `docs/architecture.md`
- `docs/principles.md`
- `docs/interfaces.md`
- `docs/roadmap.md`
- `docs/open_questions.md`
- `docs/invariants.md`

KnowledgeForge now explicitly supports durable negative knowledge:

- expected relationships not observed;
- failed empirical relationships;
- rejected mappings;
- disproven or unsupported external hypotheses;
- contradictory literature;
- known limitations.

The specification clarifies that negative knowledge requires explicit evidence scope and method, and that absence of evidence is not evidence of absence unless justified.

### 5. Introduced methodological knowledge

Updated:

- `docs/architecture.md`
- `docs/principles.md`
- `docs/interfaces.md`
- `docs/roadmap.md`
- `docs/open_questions.md`

KnowledgeForge now explicitly supports reusable methodological knowledge:

- assumptions;
- limitations;
- applicability;
- known biases;
- transformation semantics;
- comparability rules;
- methodological relationships.

This is distinct from source ingestion, statistical implementation, MacroForge reproducibility, InsightForge interpretation, PredictionForge forecasting, and DecisionForge recommendation.

### 6. Adopted explicit architectural invariants

Created:

- `docs/invariants.md`

The new invariants document is authoritative and specification-only. It defines rules such as:

- observations remain outside KnowledgeForge;
- every durable knowledge object requires provenance;
- evidence references and evidence evaluations remain distinct;
- claims are first-class;
- relationships require claim linkage and evidence state;
- components are orthogonal;
- applicability is explicit;
- dependencies are explicit;
- contradictions are preserved;
- negative knowledge is admissible;
- empirical knowledge cannot overwrite semantic or structural knowledge;
- association is not causation;
- mappings are typed, reversible, and non-destructive;
- lifecycle state is not truth state;
- downstream use is not evidence;
- representation choices are subordinate.

### 7. Clarified project purpose and interface language

Updated:

- `docs/architecture.md`
- `docs/interfaces.md`
- `docs/principles.md`
- `README.md`

The architecture retains the idea that KnowledgeForge serves downstream projects, but clarifies that this happens through governed knowledge interfaces.

This avoids prematurely implying APIs, services, runtime infrastructure, or deployment while preserving KnowledgeForge's downstream responsibility.

### 8. Updated governance and roadmap expectations

Updated:

- `docs/architecture.md`
- `docs/roadmap.md`
- `state/project_state.md`
- `state/active_goal.md`
- `state/architecture.md`

Future implementation-readiness work must now decide:

- knowledge object component model;
- claim object model;
- evidence reference and evidence evaluation contracts;
- relationship representation contract;
- knowledge dependency contract;
- lifecycle and governance state;
- confidence/uncertainty representation;
- storage and first minimal vertical slice.

## Rationale

### R1. Component model improves conceptual scaling

A flat knowledge-class taxonomy would force one object to be categorized as semantic, structural, empirical, contextual, epistemic, or evolutionary even though real knowledge often spans several of these dimensions.

The component model makes the architecture easier to scale conceptually because each object can independently express what it is, what it says, where it applies, why it is believed, how it evolves, and how it is governed.

### R2. Claims prevent edge-centric architecture

If relationships remained the primary abstraction, KnowledgeForge would naturally drift toward graph thinking.

Claims allow the architecture to represent definitions, limitations, mappings, contradictions, methodological statements, and negative findings without forcing them into graph-edge form.

### R3. Dependencies preserve reasoning structure without reasoning

KnowledgeForge must not perform reasoning, but it must preserve enough structure for downstream systems and future reviewers to understand what depends on what.

Dependencies solve this by recording architectural relationships between knowledge objects without introducing computation.

### R4. Negative knowledge prevents repeated rediscovery

A knowledge substrate that only stores positive findings will repeatedly rediscover known failures, contradictions, and limitations.

Negative knowledge is necessary for long-term maintainability and for preventing downstream systems from over-trusting expected relationships that have failed under known conditions.

### R5. Methodological knowledge is necessary for empirical reuse

Empirical claims are not reusable unless their assumptions, limitations, transformations, method scope, and biases are understood.

Methodological knowledge provides that reusable context without making KnowledgeForge a statistical implementation system.

### R6. Invariants reduce future boundary erosion

KnowledgeForge will eventually sit between observational, reasoning, navigation, forecasting, and decision systems. The risk of responsibility drift is high.

Explicit invariants make future implementation and integration decisions easier to audit.

## Architectural consequences

1. KnowledgeForge is now explicitly knowledge-first rather than graph-first, ontology-first, database-first, or API-first.
2. Claims become the primary durable assertion unit.
3. Relationships remain important but are no longer the defining abstraction.
4. Future minimal implementation planning must account for claims, dependencies, evidence evaluation, lifecycle, governance, and invariants before storage selection.
5. Empirical relationship work must preserve method scope, evidence scope, uncertainty, limitations, and negative findings.
6. Methodological knowledge must be separated from statistical implementation and from InsightForge interpretation.
7. Downstream consumers can use governed knowledge interfaces but cannot silently mutate KnowledgeForge state or convert KnowledgeForge citations into reasoning approval.
8. Domain expansion remains possible but must reuse the core model and invariants.

## Compatibility with EIP boundaries

### MacroForge

Compatibility preserved. MacroForge remains the owner of observations, ingestion, validation, canonicalization, lineage, reproducibility, source observational identities, and canonical observational databases.

KnowledgeForge may reference MacroForge evidence and evaluate how evidence supports claims, but it does not duplicate observations.

### InsightForge

Compatibility improved. KnowledgeForge preserves claims and evidence structure. InsightForge owns reasoning, interpretation, hypotheses, analytical understanding, reports, and narrative synthesis.

### AtlasForge

Compatibility preserved. KnowledgeForge stores navigable knowledge, dependency metadata, and relationship metadata. AtlasForge owns navigation UX, visualization, maps, and exploration workflows.

### BriefForge

Compatibility preserved. KnowledgeForge does not generate reports or presentation artifacts. BriefForge may receive KnowledgeForge citations through approved downstream presentation context.

### PredictionForge

Compatibility preserved. KnowledgeForge may provide empirical claims, negative findings, methodological limitations, uncertainty, and structural dependencies. It does not forecast or produce scenario probabilities.

### DecisionForge

Compatibility preserved. KnowledgeForge may provide constraints, uncertainty, competing explanations, negative knowledge, and applicability conditions. It does not recommend actions, trades, policies, portfolio changes, or interventions.

## Remaining open questions

The consolidation intentionally leaves implementation-level decisions open. The main remaining architectural questions are now captured in `docs/open_questions.md`:

1. Boundary between empirical knowledge and analysis.
2. Canonical identity evidence thresholds.
3. Knowledge store technology.
4. Confidence representation.
5. Lifecycle transition gates.
6. Domain-general vs economics-first architecture.
7. Causality claims vs statistical associations.
8. Literature evidence standards.
9. MacroForge reference stability.
10. Safe metadata exposure for future PredictionForge/DecisionForge.
11. Claim granularity.
12. Dependency review propagation.
13. Negative knowledge admission standards.
14. Methodological knowledge boundary.

## Explicit non-changes

No runtime code was created.

No graph engine was introduced.

No database was created or selected.

No API was specified or implemented.

No statistical implementation was introduced.

No visualization, infrastructure, deployment, or generalized framework was introduced.

No responsibilities were moved from MacroForge, InsightForge, AtlasForge, BriefForge, PredictionForge, or DecisionForge into KnowledgeForge.

## Final assessment

Phase II successfully converts the Phase I review into an improved architectural specification while preserving scope discipline.

KnowledgeForge is now better positioned to evolve later into an implementation project without architectural redesign, but it should remain specification-only until the consolidated object, claim, evidence, dependency, lifecycle, governance, confidence, storage, and minimal-slice decisions are explicitly accepted.
