# MetaHarvest Rejected Candidates

Project: KnowledgeForge

Record negative knowledge here so the project does not repeatedly revisit poor-fit patterns.

## Rejected candidates

### 2026-07-09 — PostgreSQL as default KnowledgeForge store by MacroForge analogy

- Candidate: adopt MacroForge PostgreSQL architecture as KnowledgeForge default storage.
- Source project/pattern: MacroForge staging/curated/meta PostgreSQL architecture.
- Rejected date: 2026-07-09.
- Why rejected: MacroForge's PostgreSQL model solves canonical observational data; KnowledgeForge has versioned, provenance-bearing, contradiction-preserving knowledge-object requirements and has not completed storage criteria.
- What was still useful: staging/curated/meta separation, idempotence, run-scoped validation, lineage, and contract checks remain valuable design evidence.
- Future revisit condition: storage-selection task after evidence/evaluation/package contracts exist.
- Status: active.

### 2026-07-09 — Runtime graph/vector/dashboard infrastructure before file-backed failure

- Candidate: add graph DB, vector store, dashboard, UI, scheduler, or service architecture before knowledge generation begins.
- Source project/pattern: rejected/deferred infrastructure in ProjectForge, MacroForge, and MetaHarvest.
- Rejected date: 2026-07-09.
- Why rejected: no evidence that file-backed packages, summaries, indexes, and deterministic validators are insufficient; infrastructure would increase complexity and frontier-LLM pressure.
- What was still useful: representation neutrality remains; future stores may be considered once requirements are evidence-backed.
- Future revisit condition: repeated file-backed limitations demonstrated by real knowledge-generation tasks.
- Status: active.

### 2026-07-09 — Autonomous knowledge-generation daemon

- Candidate: continuously generate knowledge artifacts automatically.
- Source project/pattern: ProjectForge automation doctrine and MetaHarvest negative rules.
- Rejected date: 2026-07-09.
- Why rejected: unacceptable provenance, boundary, quality, and review risk before candidate/evidence/evaluation/lifecycle contracts exist.
- What was still useful: deterministic batch scripts may later be useful after explicit task approval and validation gates.
- Future revisit condition: mature package contracts, validators, idempotent rebuilds, lifecycle governance, and human approval policy.
- Status: active.

## Rejection template

- Candidate:
- Source project/pattern:
- Rejected date:
- Why rejected:
- What was still useful:
- Future revisit condition:
- Status: active | stale | superseded | retired
