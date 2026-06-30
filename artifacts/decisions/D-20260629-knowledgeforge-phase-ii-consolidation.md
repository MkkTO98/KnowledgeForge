# Decision: KnowledgeForge Phase II Architectural Consolidation

Date: 2026-06-29
Status: Accepted
Permission level: Specification-only architecture consolidation requested by user
Implementation status: No implementation introduced

## Decision

Adopt the accepted Phase I architectural review outcomes into the KnowledgeForge specification.

KnowledgeForge remains the canonical reusable knowledge substrate of the EIP. It organizes, preserves, versions, justifies, and provides governed knowledge interfaces for reusable knowledge.

KnowledgeForge does not own observational data, perform reasoning, generate hypotheses, perform prediction, recommend decisions, implement visualization, or define itself by any particular runtime representation.

## Consolidated architectural model

The previous flat knowledge-class model is replaced by orthogonal components of durable knowledge objects:

- identity;
- content;
- applicability;
- evidence;
- evolution;
- governance.

Semantic, structural, empirical, contextual, epistemic, and evolutionary concerns remain valid, but they are no longer treated as mutually exclusive peer classes.

## First-class claims

Durable claims are now first-class KnowledgeForge objects.

Relationships remain important, but they are relationship representations of claims rather than the primary architectural abstraction.

## Additional accepted concepts

KnowledgeForge explicitly supports, at the architectural level:

- knowledge dependencies;
- negative knowledge;
- methodological knowledge;
- evidence references distinct from evidence evaluations;
- explicit architectural invariants.

These are conceptual responsibilities, not implementation artifacts.

## Representation boundary

KnowledgeForge is not a graph project, ontology project, database project, API project, or generalized framework.

Graphs, ontologies, relational schemas, document stores, APIs, and file-backed representations may later be derived from the governed knowledge model, but none defines the architecture.

## Consequences

Future implementation-readiness work must use the consolidated model as its starting point.

Before implementation, KnowledgeForge still requires accepted decisions for claim model, dependency model, evidence contracts, lifecycle/governance state, confidence/uncertainty representation, storage, versioning, and first minimal vertical slice.
