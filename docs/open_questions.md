# KnowledgeForge Open Questions and Architectural Ambiguities

Status: Active ambiguity register

This file exists because architectural criticism is preferred over silently resolving foundational ambiguity.

## A1. Boundary between empirical knowledge and analysis

KnowledgeForge should own reusable empirical claims and relationship representations. InsightForge should own interpretation.

Ambiguity: when does an empirical claim or statistical relationship representation become an analytical conclusion?

Proposed boundary: KnowledgeForge may state method, evidence, effect estimate, uncertainty, applicability, limitations, dependencies, negative findings, and lifecycle state. It must not state investment meaning, macro interpretation, narrative implication, or recommendation.

## A2. Canonical identity risk

KnowledgeForge should solve canonical identity, but premature canonicalization can erase source methodology differences.

Open question: what evidence is required before two indicators can be mapped as exact or equivalent rather than proxy or unknown?

## A3. Knowledge store technology

A graph database may be tempting, but the architecture needs provenance, versioning, lifecycle, evidence references, and human auditability as much as traversal.

Open question: should the first implementation use a file-backed model, relational model, graph model, document model, or hybrid?

Decision deferred.

## A4. Confidence representation

KnowledgeForge must preserve confidence and uncertainty.

Open question: should confidence be numeric, categorical, method-specific, evidence-weighted, or multi-dimensional?

Decision deferred.

## A5. Lifecycle state transitions

Initial lifecycle vocabulary:

Observed → Candidate → Supported → Accepted → Questioned → Deprecated → Archived

Open question: what gates, evidence thresholds, review roles, and automated checks are required for transitions?

## A6. Domain-general vs economics-first architecture

KnowledgeForge should initially focus on economics but later support many domains.

Risk: designing too generally could create a vague ontology project. Designing too narrowly could require redesign later.

Proposed stance: specify economics-first objects using domain-extensible primitives: concept, claim, relationship representation, evidence reference, evidence evaluation, applicability condition, lifecycle, governance, dependency, provenance, mapping, methodological knowledge, and negative knowledge.

## A7. Relationship causality

Structural relationships may be causal, empirical relationships may be correlational, and contextual relationships may condition validity.

Open question: what evidence and dependency structure is required before an empirical association can support a separate causal or structural claim without KnowledgeForge becoming InsightForge?

## A8. Literature-derived knowledge

KnowledgeForge should preserve literature-derived reusable knowledge.

Open question: what counts as acceptable literature evidence, and how should conflicting academic findings be represented?

## A9. MacroForge reference stability

KnowledgeForge should reference MacroForge evidence, not duplicate observations.

Open question: what reference contract guarantees that old KnowledgeForge evidence pointers remain reproducible after MacroForge schema or storage evolution?

## A10. Future project pressure

PredictionForge and DecisionForge are future projects. KnowledgeForge must not absorb their responsibilities prematurely.

Open question: what metadata is safe to expose for future prediction/decision systems without doing prediction or recommendation itself?

## A11. Claim granularity

Claims are now first-class architectural objects.

Open question: what is the correct granularity for a claim so that claims are neither too coarse to review nor too fragmented to maintain?

## A12. Dependency review propagation

Knowledge dependencies are architectural declarations intended to preserve reasoning structure and support future review propagation.

Open question: what governance rule should determine when a changed dependency requires review of dependent claims, mappings, methods, or relationships?

## A13. Negative knowledge admission

Negative findings are reusable knowledge only when evidence scope and method are explicit.

Open question: what standards prevent weak absence-of-evidence claims from being misrepresented as evidence of absence?

## A14. Methodological knowledge boundary

KnowledgeForge may preserve reusable methodological assumptions, limitations, and applicability.

Open question: how much method detail belongs in KnowledgeForge before it becomes statistical implementation, MacroForge reproducibility metadata, or InsightForge interpretation?

## Specification-freeze triage

The final architectural consolidation accepts the following as architectural commitments before provisional freeze:

- claim facets are governed vocabularies rather than object subclasses;
- every durable knowledge object has a common kernel;
- stable identity is independent of revision history;
- dependency posture is mandatory;
- knowledge change is an abstract audit concept;
- graphs, ontologies, relational schemas, databases, APIs, and interfaces are representations of the knowledge model, not defining abstractions.

The remaining questions above are intentionally deferred until implementation planning unless they threaten ownership boundaries, representation neutrality, the common durable-object kernel, stable identity, or the claim/dependency facet model.
