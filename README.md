# KnowledgeForge

KnowledgeForge is the canonical reusable knowledge substrate of the Economic Intelligence Platform (EIP).

It answers: **What is known?**

KnowledgeForge is currently a **specification-only** ProjectForge project. It owns architecture, boundaries, governance, and future implementation responsibilities for durable reusable knowledge. It does not yet own runtime infrastructure, databases, graph computation, APIs, pipelines, or services.

## Position in the EIP cognitive stack

```text
Reality
  ↓
MacroForge        What happened?
  ↓
KnowledgeForge    What is known?
  ↓
InsightForge      What does this mean?
  ↓
PredictionForge   What is likely to happen?   (future)
  ↓
DecisionForge     What should be done?        (possible future)

AtlasForge        Navigation
BriefForge        Presentation
```

Every EIP project answers a different question. KnowledgeForge exists to prevent reusable knowledge from being scattered across data, reasoning, navigation, reporting, forecasting, and decision systems.

## Current status

Current phase: specification-only foundation; provisional specification freeze candidate after final architectural consolidation.
- Runtime implementation: explicitly deferred.
- Persistent knowledge store: architecturally expected, technology deferred.
- Graphs, APIs, schemas, and storage: possible future representations/interfaces, not defining architecture; implementation deferred.
- Canonical observational data: owned by external observational systems, not KnowledgeForge.

## Authoritative starting points

- `docs/architecture.md` — full foundational architecture specification.
- `docs/principles.md` — architectural principles and non-negotiables.
- `docs/interfaces.md` — project boundary and interface contracts.
- `docs/roadmap.md` — evolution from specification-only project to implementation project.
- `docs/open_questions.md` — explicit ambiguities and hidden assumptions.
- `docs/invariants.md` — authoritative architectural invariants adopted in Phase II.
- `artifacts/decisions/D-20260629-knowledgeforge-foundational-scope.md` — foundational scope decision.
- `artifacts/tasks/T-001-initial-validation.md` — instantiation task outcome.

## Absolute non-goals

KnowledgeForge shall not:

- own observational datasets;
- duplicate external observational ingestion, validation, canonicalization, lineage, or reproducibility responsibilities;
- generate reports;
- generate hypotheses;
- perform reasoning or interpretation;
- forecast;
- recommend actions;
- implement visualization;
- become a general AI platform or orchestration framework.
