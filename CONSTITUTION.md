# KnowledgeForge Constitution

KnowledgeForge is the canonical reusable knowledge substrate of the Economic Intelligence Platform. It answers: "What is known?"

KnowledgeForge accumulates, organizes, versions, justifies, and serves reusable knowledge while preserving provenance, uncertainty, competing explanations, confidence, evidence, revision history, lifecycle state, applicability, and governance state.

## Knowledge accumulation principle

KnowledgeForge exists to accumulate objective, reproducible, evidence-backed knowledge. It does not seek completeness, sophistication, or abstraction for their own sake. Every addition should measurably improve the repository's objective knowledge while preserving reproducibility, auditability, and constitutional boundaries.

## Non-negotiable rules

1. KnowledgeForge owns reusable knowledge, not observations, ingestion, canonical observational databases, reasoning, interpretation, forecasting, recommendations, report generation, visualization, or presentation.
2. External observational systems remain the systems of record for observations, ingestion, validation, canonicalization, observational lineage, reproducibility handles, and observational databases. KnowledgeForge may reference or snapshot evidence from such systems, but it does not expose, consume, or require project-specific runtime interfaces.
3. Durable KnowledgeForge objects require stable identity, provenance, evidence state, applicability/scope posture, lifecycle state, governance/review state, revision history, and dependency posture.
4. Claims are first-class durable knowledge objects. Relationships, mappings, tables, graphs, database schemas, APIs, and documents are representations of the knowledge model, not the defining abstraction.
5. Evidence references and evidence evaluations are distinct. KnowledgeForge may evaluate how evidence supports, weakens, contradicts, or bounds reusable knowledge claims, but it must not duplicate external observational evidence.
6. Contradictory evidence, competing explanations, rejected hypotheses, incompatible mappings, and negative findings must remain discoverable when evidence scope and method are explicit.
7. Lifecycle state is not truth state. Accepted means accepted for reuse under stated evidence and applicability conditions, not proven true.
8. Governance state is distinct from confidence. Review status, stewardship status, and lifecycle state do not equal epistemic confidence.
9. Representation neutrality is mandatory. A graph, ontology, relational database, document store, API, or file-backed model may implement KnowledgeForge, but none may redefine its purpose or boundaries.
10. Domain expansion cannot bypass invariants or cause KnowledgeForge to own observations, reasoning, prediction, recommendation, presentation, or domain operations.
11. Implementation must proceed through bounded, evidence-backed slices. Do not generalize Slice 0 into infrastructure without an approved architectural task and verification plan.
12. Project state, decisions, reports, tasks, and handoffs must remain explicit on disk in ordinary files.
13. Cloud/frontier LLM use must be minimized through deterministic validation, local-first tooling, cached artifacts, reusable templates, and explicit context discipline.
14. GitHub pushes require human approval.

## Default operating posture

The default is documentation/governance work inside approved scope, deterministic local verification, and conservative implementation. Implementation/runtime changes require an explicit task artifact, architectural justification, and real validation.

## Current authoritative architecture

The authoritative KnowledgeForge model is defined by:

- `docs/architecture.md`
- `docs/principles.md`
- `docs/invariants.md`
- `docs/governed_vocabularies.md`
- `docs/interfaces.md`
- `docs/roadmap.md`
- `docs/production_doctrine.md` for operational production doctrine
- `docs/knowledge_repository_architecture.md` for operational Knowledge Repository persistence
- current decision and report artifacts under `artifacts/decisions/` and `artifacts/reports/`
