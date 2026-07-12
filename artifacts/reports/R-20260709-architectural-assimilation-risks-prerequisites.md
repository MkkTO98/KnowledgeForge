# KnowledgeForge Architectural Risks, Compatibility Analysis, and Prerequisites

Date: 2026-07-09
Status: completed

## Architectural risks

### R1. Premature infrastructure selection

Risk: selecting PostgreSQL, graph database, vector store, or service architecture before object/evidence/revision contracts are stable.

Mitigation: keep storage deferred; use file-backed packages and validators until real scaling pressure exists.

### R2. LLM-generated knowledge mistaken for accepted knowledge

Risk: plausible generated statements become durable knowledge without evidence cycle completion.

Mitigation: LLM output is candidate material only; acceptance requires evidence evaluation, contradiction search, applicability, dependencies, lifecycle/governance state, and deterministic validation.

### R3. KnowledgeForge absorbs MacroForge responsibilities

Risk: evidence reproduction or empirical computation becomes observational ingestion/canonicalization.

Mitigation: reference MacroForge evidence handles; do not duplicate observational datasets; keep empirical findings scoped to reusable knowledge claims.

### R4. KnowledgeForge absorbs InsightForge responsibilities

Risk: evidence evaluations become interpretation or macro analysis.

Mitigation: KnowledgeForge records what evidence supports/weakens/contradicts and under what scope; InsightForge owns meaning, implication, and narrative interpretation.

### R5. Over-general ontology expansion

Risk: terminology governance turns into universal ontology construction.

Mitigation: extend terms only when existing values cannot represent materially different knowledge meaning under current evidence.

### R6. Abstraction before repeated evidence

Risk: creating generic knowledge pipelines or object families from one or two examples.

Mitigation: use MetaHarvest/MacroForge discipline: evidence-only slices first, abstraction only after repeated convergence and measured benefit.

### R7. Evidence-source freshness mistaken for reproducibility

Risk: live/current source freshness weakens reconstructability.

Mitigation: prefer immutable references, snapshots, commits, methodology version, access date, and explicit staleness state.

### R8. Validator sprawl

Risk: validators become overlapping frameworks or hard-to-debug policy engines.

Mitigation: keep validators narrow, deterministic, classified, and tied to explicit invariants.

### R9. Local-model false confidence

Risk: local model output looks cheap and repeatable but is not deterministic enough for acceptance.

Mitigation: local models may assist extraction/classification only inside bounded templates with deterministic validation and retained outputs.

### R10. Existing dirty repository state

Risk: pre-existing uncommitted ProjectForge/MetaHarvest compatibility changes obscure this task's changes.

Mitigation: final report distinguishes this task's intended files; review git diff before commit.

## Compatibility analysis

### ProjectForge compatibility

KnowledgeForge should retain ProjectForge's file-backed operating system, context policy, handoff discipline, task/report/decision artifacts, and validation/coherence checks. Assimilation strengthens, not replaces, ProjectForge compatibility.

### MacroForge compatibility

KnowledgeForge must remain downstream of MacroForge evidence, not a mirror. MacroForge evidence handles, reproducibility metadata, source identities, and canonical observation keys are inputs to KnowledgeForge evidence references/evaluations. PostgreSQL patterns are useful evidence, not a storage mandate.

### MetaHarvest compatibility

MetaHarvest remains advisory. Its evidence-source architecture and scientific-cycle discipline are useful, but KnowledgeForge must not become an architecture-harvesting or recommendation system. Local `architecture/metaharvest/` surfaces should record assimilation review outcomes as advisory history.

### Existing KnowledgeForge architecture compatibility

The adopted/adapted candidates are compatible with current commitments: claim-first model, common kernel, representation neutrality, dependency posture, stable identity, contradiction preservation, negative knowledge, and knowledge-change audit concept.

## Required prerequisites before implementation begins

1. Complete assimilation consolidation specification.
2. Define KnowledgeForge evidence-source and evidence-evaluation architecture.
3. Define a conceptual knowledge candidate/package boundary.
4. Define deterministic validation taxonomy and failure classes.
5. Define local-model/frontier-LLM routing and audit policy for knowledge generation.
6. Define provenance envelope and fingerprinting expectations.
7. Define knowledge-change lineage/evolution report contract.
8. Update open questions with pre-implementation blockers vs implementation-pressure deferrals.
9. Select a single narrow reproducible pilot and write an implementation task artifact.
10. Run coherence, context health, architecture-reality audit, and relevant unit tests before implementation approval.

## Next architectural task recommendation

Before producing knowledge artifacts, run: `KnowledgeForge Assimilation Consolidation and Reproducible Knowledge-Generation Architecture Specification`.

Purpose: convert this campaign's Adopt/Adapt decisions into KnowledgeForge-local contracts for evidence/evaluation, candidate package boundaries, deterministic validation, provenance/fingerprints, lifecycle/change reporting, and local/frontier model routing.
