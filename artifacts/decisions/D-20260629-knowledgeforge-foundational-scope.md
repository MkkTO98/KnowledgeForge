# Decision: KnowledgeForge Foundational Scope

Date: 2026-06-29
Status: Accepted
Permission level: L4 foundational, approved by explicit user request to instantiate KnowledgeForge

## Decision

Instantiate KnowledgeForge as an autonomous EIP sibling project using ProjectForge, initially as a specification-only project.

KnowledgeForge is the canonical reusable knowledge substrate of the EIP. It answers: "What is known?"

## Scope accepted

Phase II note: this foundational scope has been refined by `D-20260629-knowledgeforge-phase-ii-consolidation.md`. The terms below remain historically accepted, but the authoritative current model treats them as concerns within identity, content, applicability, evidence, evolution, and governance components rather than as a flat peer taxonomy.

KnowledgeForge will eventually own reusable knowledge structures, including:

- semantic knowledge;
- structural knowledge;
- empirical reusable statistical relationships;
- contextual knowledge;
- epistemic knowledge;
- evolutionary/lifecycle knowledge;
- canonical concepts and source-indicator mappings;
- relationship objects as first-class versioned entities.

## Boundary accepted

KnowledgeForge does not own observations. MacroForge remains the system of record for observational data, ingestion, validation, canonicalization, lineage, reproducibility, and the canonical economic database.

KnowledgeForge stores knowledge and evidence references, not duplicated observational datasets.

## Specification-only constraint

The initial project phase explicitly forbids runtime implementation, graph computation, APIs, databases, statistical pipelines, visualization, deployment, external services, secrets, or cross-project mutation.

## Relationship to EIP projects

- MacroForge: upstream observational evidence provider.
- InsightForge: downstream reasoning and interpretation consumer.
- AtlasForge: downstream navigation consumer.
- BriefForge: presentation layer, primarily consuming InsightForge outputs.
- PredictionForge: future downstream forecasting consumer.
- DecisionForge: possible future downstream recommendation/action consumer.

## Rationale

The EIP is becoming a layered cognitive architecture. Without a separate KnowledgeForge, durable knowledge structures would be duplicated across MacroForge, InsightForge, AtlasForge, and future projects, causing unclear ownership and architectural overlap.

## Consequences

Future work must preserve the distinction between:

- observations vs knowledge;
- knowledge vs interpretation;
- knowledge vs navigation;
- knowledge vs presentation;
- knowledge vs prediction;
- knowledge vs decision.

Any implementation task must first pass through KnowledgeForge governance and accepted implementation-readiness decisions.
