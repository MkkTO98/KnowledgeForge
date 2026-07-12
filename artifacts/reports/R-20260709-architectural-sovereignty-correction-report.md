# Sovereignty Correction Report

Date: 2026-07-09
Status: completed

## Objective

Remove current architectural wording that made KnowledgeForge appear dependent on, integrated with, or formally coupled to another EIP repository, while preserving useful architectural lessons from the assimilation/readiness work.

## Correction summary

### Corrected authoritative/current files

| File | Correction |
| --- | --- |
| `CONSTITUTION.md` | Replaced named observational-system authority with repository-independent external observational-system authority. Added explicit rule that KnowledgeForge may reference/snapshot evidence but does not expose, consume, or require project-specific runtime interfaces. |
| `state/active_goal.md` | Replaced project-specific adapter next task with KnowledgeForge Source Evidence Package v1 Real-Fixture Replay Validation Slice. Reframed production campaign as external WDI evidence rather than repository-derived evidence. |
| `state/project_state.md` | Replaced compatibility/adapter phase with sovereignty-corrected production-readiness posture. Marked historical audit recommendations as superseded where they imply adapters. |
| `state/architecture.md` | Replaced compatibility architecture with sovereign evidence boundary. Added KnowledgeForge-owned EvidenceReference, SourceEvidencePackage, EvidenceEvaluation, ProvenanceEnvelope, and package-contract definitions. |
| `docs/architecture.md` | Replaced named EIP project layering and interface language with role-based observational/reasoning/navigation/forecasting/decision/presentation systems. Removed named project evidence/interface contract phrasing from current architecture. |
| `docs/evidence_source_evaluation_specification.md` | Replaced named project evidence classes with external observational data, external source metadata, external lineage/provenance, and external source summaries. Removed origin-project explanation from source-family-specific handling. |
| `docs/provenance_fingerprinting.md` | Replaced named package/run ID requirement with source package/export/snapshot/run identifier. |
| `docs/knowledge_package_contract.md` | Replaced named package/run/query references with source package/export/snapshot/query references. |
| `docs/roadmap.md` | Rewrote current/recommended phases around repository-independent Source Evidence Package v1 real-fixture validation. Removed project-specific adapter, database coupling, and named consumer interface language from future phases. |
| `artifacts/tasks/backlog.md` | Replaced next task with repository-independent real-fixture replay validation. Rejected cross-repository adapters/shared schemas/runtime APIs/database coupling/shared implementation packages. |
| `context/latest_handoff.md` | Updated handoff to reflect sovereignty correction and new next task. |
| `_SUMMARY.md`, `state/_SUMMARY.md`, `artifacts/tasks/_SUMMARY.md`, `artifacts/reports/_SUMMARY.md` | Updated current summaries to prevent stale project-specific adapter recommendations from guiding future agents. |

### Superseded historical report recommendations

The following reports were preserved as historical audit/evidence artifacts but received supersession notes where their recommendations implied project-specific adapters or repository coupling:

- `artifacts/reports/R-20260709-macroforge-compatibility-audit.md`
- `artifacts/reports/R-20260709-production-gap-analysis.md`
- `artifacts/reports/R-20260709-first-production-campaign-recommendation.md`

Reason for preserving rather than rewriting fully:

- They document what was actually audited.
- Historical evidence should remain traceable.
- The problem was current architectural authority and next-task direction, not the fact that a historical audit inspected another repository.

## Concepts retained under KnowledgeForge ownership

| Prior blurred wording | Corrected KnowledgeForge-owned concept | Reason |
| --- | --- | --- |
| project-specific `EvidenceRef Adapter` | `SourceEvidencePackage` + `EvidenceReference` fixture assembly | Keeps reproducible package assembly without implying cross-repository interface. |
| project-derived fixture | real external evidence fixture/snapshot | Keeps real-evidence validation without tying it to another repository. |
| adapter/export slice | real-fixture replay validation slice | Focuses on deterministic replay and validation, not integration. |
| package/run/query references from a named project | source package/export/snapshot/query references | Generalizes provenance to any external evidence source. |
| compatibility architecture | sovereign evidence boundary | Makes KnowledgeForge's architecture independent from source implementation details. |
| named downstream project interfaces | role-based downstream export/use discipline | Keeps boundary clarity without embedding fixed inter-repository architecture. |

## Corrections not made

Some project names remain in historical, scaffold, or advisory contexts:

- completed assimilation and audit reports;
- generated-project scaffold instructions;
- local advisory paths and review history;
- foundational historical decisions;
- source-of-review statements identifying which repositories were inspected.

These are not current architecture or production integration requirements. Removing them wholesale would reduce traceability and falsify audit history.

## Compatibility with constraints

The correction introduced no:

- shared libraries;
- adapters between repositories;
- runtime integrations;
- APIs;
- database coupling;
- shared schemas;
- shared implementation packages;
- new infrastructure;
- modifications outside KnowledgeForge.

All changes are documentation, state, backlog, and report changes within KnowledgeForge.

## Architectural result

The finished current architecture now reads as if KnowledgeForge's evidence/package/provenance/validation model was designed independently:

- evidence enters as external evidence references or snapshots;
- source-specific handling terminates at KnowledgeForge-owned package contracts;
- KnowledgeForge owns all package identity, provenance, fingerprints, validation state, lifecycle state, governance state, and knowledge-change reports;
- downstream systems consume KnowledgeForge-owned exports/references but do not define KnowledgeForge acceptance;
- production remains blocked until real-fixture replay validation proves deterministic package assembly and validation.
