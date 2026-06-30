# Project State

Project: KnowledgeForge
Template: default_project
Created by: ProjectForge
Current phase: Vertical Slice 0 implemented and verified

## Purpose

KnowledgeForge is the canonical reusable knowledge substrate of the Economic Intelligence Platform. It answers: "What is known?"

## Operating context

- Project type: architecture specification / future data-knowledge infrastructure.
- Primary users: Mikkel and Hermes agents operating the EIP.
- Future consumers: InsightForge, AtlasForge, PredictionForge, DecisionForge, BriefForge indirectly, and future domain projects.
- Agent autonomy: conservative; documentation/governance work allowed inside approved task scope; implementation/runtime changes require explicit approval and task artifact.
- Command policy: layered default with specification-only constraint.
- Secrets policy: no secrets or credentials in V1.
- Logging standard: ProjectForge file-backed governance logs only.
- Testing standard: `python3 -m unittest discover -s tests -v`, targeted validator checks, compile checks for touched Python, and ProjectForge coherence/context checks.
- Documentation standard: rigorous, boundary-explicit, provenance-aware, future-agent-readable.

## Current architecture status

Foundational specification created, Phase I architectural review completed, Phase II architectural consolidation applied, ontology-focused knowledge model refinement review completed, and final architectural consolidation for provisional specification freeze completed. The authoritative model now treats durable knowledge objects as component-based objects with a common durable-object kernel. Claims are first-class and classified through governed vocabularies/facets rather than subclasses. Relationships are representations of claims. Stable identity is independent of revisions. Every durable object declares dependency posture. Dependencies, negative knowledge, methodological knowledge, knowledge change, and explicit invariants are part of the architecture. Vertical Slice 0 has been implemented as a minimal file-backed object ecosystem and validator without introducing databases, APIs, graph engines, ontology managers, statistical discovery, lifecycle automation, governance workflow automation, infrastructure, visualization, or generalized frameworks.

Authoritative architecture files:

- `docs/architecture.md`
- `docs/principles.md`
- `docs/interfaces.md`
- `docs/roadmap.md`
- `docs/open_questions.md`
- `docs/invariants.md`
- `docs/governed_vocabularies.md`
- `docs/vertical_slice_0_implementation_design.md`

Current review/consolidation artifacts:

- `artifacts/reports/R-20260629-architecture-review-phase-i.md`
- `artifacts/reports/R-20260629-architecture-consolidation-phase-ii.md`
- `artifacts/reports/R-20260629-knowledge-model-refinement-review.md`
- `artifacts/reports/R-20260629-final-architectural-consolidation-spec-freeze.md`
- `artifacts/reports/R-20260630-final-vertical-slice-0-dependency-refinement.md`
- `artifacts/reports/R-20260630-vertical-slice-0-implementation-evidence.md`
- `artifacts/reports/R-20260630-vertical-slice-0-validator-hardening.md`

## Boundary summary

KnowledgeForge owns reusable knowledge. MacroForge owns observations. InsightForge owns reasoning/interpretation. AtlasForge owns navigation. BriefForge owns presentation. PredictionForge will own forecasting. DecisionForge may own recommendations/actions.

## Vertical Slice 0 implementation planning

Vertical Slice 0 is implemented, verified, and validator-hardened. It contains exactly four durable object fixtures under `knowledge/objects/`, a deterministic invariant validator at `tools/validate_vertical_slice_0.py`, end-to-end and negative invariant tests at `tests/test_vertical_slice_0.py`, implementation evidence at `artifacts/reports/R-20260630-vertical-slice-0-implementation-evidence.md`, and validator-hardening evidence at `artifacts/reports/R-20260630-vertical-slice-0-validator-hardening.md`. Dependency posture and dependency entries live inside the Claim kernel and are versioned with the Claim.

## Source of truth

Setup answers and foundational decisions are under `artifacts/decisions/`. Future agents must update decision artifacts when durable policy changes.
