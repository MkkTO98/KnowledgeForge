# KnowledgeForge Assimilation Implementation Roadmap

Date: 2026-07-09
Status: recommendation only; implementation not yet approved

## Roadmap principle

Do not begin producing knowledge artifacts until KnowledgeForge has a local, reproducible, evidence-backed generation architecture. The roadmap below is architectural preparation, not implementation authorization.

## Priority 0 — Constitution and state alignment (completed in this campaign)

- Correct `CONSTITUTION.md` to match KnowledgeForge.
- Record assimilation review artifacts.
- Update state/handoff/backlog surfaces.

## Priority 1 — Assimilation consolidation specification

Goal: translate accepted/adapted candidates into KnowledgeForge-local architecture contracts.

Deliverables:

- Knowledge-generation boundary specification.
- Evidence-source/evidence-evaluation architecture for KnowledgeForge.
- Knowledge candidate package / knowledge object package conceptual contract.
- Deterministic validation taxonomy and failure classification.
- Local-model/frontier-LLM routing policy for knowledge generation.
- Updated open-question triage.

Exit criteria:

- No ambiguity about what is deterministic, local-model-assisted, frontier-LLM-assisted, or human-reviewed.
- No ambiguity about evidence reference vs evidence evaluation.
- No ambiguity about package/object/change boundaries.

## Priority 2 — Reproducibility and provenance architecture

Goal: make future knowledge artifacts rebuildable and auditable before production generation.

Deliverables:

- Provenance envelope specification.
- Object/revision/package fingerprinting design.
- Knowledge-change lineage report structure.
- Idempotent rebuild expectation.
- Evidence snapshot/reference policy.
- Compatibility rules for MacroForge evidence handles.

Exit criteria:

- A future object can state exactly what evidence and process generated it.
- A future rerun can determine same/different result explicitly.

## Priority 3 — Deterministic validator expansion design

Goal: specify the next validator capability before code changes.

Candidate validation domains:

- common-kernel completeness;
- claim facet vocabulary validity;
- evidence-reference/evidence-evaluation distinction;
- dependency posture/facet validity;
- applicability declaration presence;
- lifecycle transition requirements;
- contradiction/negative-knowledge admissibility;
- knowledge-change coherence;
- report/state/handoff consistency.

Exit criteria:

- Validator changes can be implemented as a bounded slice with tests.

## Priority 4 — Knowledge generation workflow templates

Goal: reduce frontier LLM usage by making knowledge work template-driven and validator-gated.

Deliverables:

- Evidence evaluation template.
- Claim candidate template.
- Contradiction search template.
- Applicability/dependency review template.
- Lifecycle transition proposal template.
- Knowledge-change report template.

Exit criteria:

- LLM/local-model outputs are candidates only and have clear validation gates.

## Priority 5 — Narrow reproducible pilot design

Goal: design, but not yet implement, one reproducible knowledge-generation pilot.

Recommended pilot shape:

```text
One MacroForge evidence handle or official methodology source
-> one canonical concept or claim candidate
-> one evidence evaluation
-> one dependency/applicability declaration
-> one lifecycle proposal
-> deterministic validation plan
```

Exit criteria:

- Implementation task can be approved or rejected with known risk, scope, and verification.

## Priority 6 — Implementation slice only after approval

Only after priorities 1-5 are complete should KnowledgeForge implement additional functionality beyond Slice 0.

Likely first implementation after approval:

- file-backed package/object/evidence-evaluation fixture;
- deterministic validator extension;
- unit tests including negative cases;
- no database/API/graph service;
- no autonomous generation.
