# MetaHarvest Recommendation Proposals

Project: KnowledgeForge

Advisory recommendation proposals only. MetaHarvest may recommend that this project consider opening a task, but it may not create tasks here. Do not implement anything from this file without normal project decision, dry-run, tests, and coherence gates.

## Active recommendation proposals

### KF-MH-20260709-001 — Evidence-source/evidence-evaluation architecture

- Source project/pattern: MetaHarvest evidence-source architecture; MacroForge evidence handles.
- Target area: KnowledgeForge provenance and evidence model.
- Recommendation type: adoption/adaptation.
- Minimum useful extraction: define KnowledgeForge-local evidence-source taxonomy, evidence reference contract, evidence evaluation contract, snapshot/reference policy, and contradiction handling.
- Expected benefit: stronger provenance, reproducibility, and lower LLM reliance.
- Risks: overbuilding an evidence subsystem before object packages exist.
- Required gates: architecture task, decision/report artifact, validator design, no runtime infrastructure.
- Status: active.

### KF-MH-20260709-002 — Reproducible knowledge package boundary

- Source project/pattern: MacroForge ObservedIngestionPackage, fingerprinting, idempotent reruns; MetaHarvest portable records.
- Target area: future KnowledgeForge knowledge-generation workflow.
- Recommendation type: adaptation.
- Minimum useful extraction: conceptual candidate/package boundary with stable identity, claim facets, evidence references/evaluations, applicability, dependencies, lifecycle proposal, provenance, and fingerprint expectations.
- Expected benefit: deterministic rebuildability and auditability.
- Risks: premature implementation if treated as code before contract design.
- Required gates: specification-first task and tests before implementation.
- Status: active.

### KF-MH-20260709-003 — Deterministic validator and scientific-cycle gates

- Source project/pattern: ProjectForge validator classification, MacroForge run-scoped validation, MetaHarvest knowledge evolution cycle.
- Target area: validator roadmap and object acceptance governance.
- Recommendation type: adoption/adaptation.
- Minimum useful extraction: classify validator failures and require candidate/evidence/contradiction/applicability/dependency/lifecycle completion before acceptance.
- Expected benefit: prevents LLM-generated statements from becoming accepted knowledge without evidence.
- Risks: validator sprawl if too broad.
- Required gates: small validator slices with negative tests.
- Status: active.

## Proposal template

- Recommendation proposal:
- Source project/pattern:
- Target area:
- Recommendation type: adoption | simplification | replacement | deletion | rejection
- Minimum useful extraction:
- Expected benefit:
- Risks:
- Required gates:
- Status: active | stale | superseded | retired
