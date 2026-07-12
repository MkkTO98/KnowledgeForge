# KnowledgeForge Assimilation Consolidation Architecture Specification Report

Date: 2026-07-09
Status: completed architecture specification; no runtime implementation
Task: KnowledgeForge Assimilation Consolidation and Reproducible Knowledge-Generation Architecture Specification

## 1. Executive conclusion

KnowledgeForge is now specified as a reproducible knowledge-generation engine bounded by evidence references, deterministic computation, package contracts, provenance/fingerprint envelopes, classified validators, and explicit model-routing policy.

The task did not produce knowledge artifacts, create PostgreSQL schemas, add vector/dashboard/scheduler/UI infrastructure, run local-model pilots, or begin MacroForge/PostgreSQL data consumption.

## 2. Specification deliverables

Created architecture specifications:

- `docs/reproducible_knowledge_generation_architecture.md`
- `docs/evidence_source_evaluation_specification.md`
- `docs/knowledge_package_contract.md`
- `docs/validator_taxonomy.md`
- `docs/provenance_fingerprinting.md`
- `docs/model_routing_policy.md`
- `docs/knowledge_evolution_change_report_contract.md`

Supporting readiness report:

- `artifacts/reports/R-20260709-implementation-readiness-assessment.md`

Task record:

- `artifacts/tasks/T-20260709-assimilation-consolidation-specification.md`

## 3. Architectural decisions encoded

### 3.1 Evidence-source architecture

KnowledgeForge may treat the following as evidence only when properly referenced and scoped:

- MacroForge canonical data, metadata, lineage/provenance, validation reports, and reproducibility handles;
- MetaHarvest external source summaries when applicable to methodology/source/architecture understanding, not as operating authority;
- manually supplied evidence with source identity and capture metadata;
- generated intermediate evidence when upstream references and methods are retained;
- official documentation and literature/source assertions.

KnowledgeForge may not treat unsupported LLM output, downstream consumer usage, repository analogy, or mutable live pages without capture as direct evidence for accepted knowledge.

### 3.2 Evidence-evaluation architecture

Evidence evaluation covers validity, freshness, source family, data lineage, reproducibility, contradiction handling, uncertainty, missingness, and auditability. It records how evidence supports, weakens, contradicts, or bounds reusable knowledge; it must not produce InsightForge-style interpretation.

### 3.3 Reproducible generation boundary

KnowledgeForge may generate factual knowledge, derived knowledge, statistical characterization, classification, candidate knowledge, evidence evaluations, methodological knowledge, and negative knowledge. It must stop before interpretation, hypothesis generation, insight, forecasting, recommendation, presentation, or observational data ownership.

### 3.4 Package contract

The package contract requires package identity, input references, evidence references, computation method, generated statements, quality/confidence metadata, contradiction records, provenance envelope, fingerprints, validation state, and version/evolution metadata.

### 3.5 Validator taxonomy

Validators are classified into constitutional boundary, evidence contract, provenance, reproducibility, unsupported inference, package schema, lineage/fingerprint, maturity-state, advisory, repository/governance, and tooling/environment categories. Constitutional, evidence, provenance, reproducibility, unsupported inference, schema, lineage, and maturity promotion failures are blockers by default for accepted packages.

### 3.6 Provenance and fingerprinting

Fingerprinting targets include input datasets, query definitions, computation recipes, prompts/templates, local/frontier model identifiers, generated packages, and evidence snapshots. Changed inputs, queries, methods, templates, models, or validators require explicit evolution handling.

### 3.7 Model routing

The default route is no model or deterministic computation. Local models may assist candidate generation/extraction only with retained prompts, model identifiers, output references, and deterministic validation. Frontier LLM usage requires explicit justification and is not authority for acceptance.

### 3.8 Knowledge evolution/change reports

Knowledge changes caused by new data, corrected data, changed computation, changed evidence evaluation, changed template/prompt/model, contradiction discovery, validator change, manual governance correction, dependency change, or applicability/scope change must be recorded through a change report contract.

## 4. Roadmap impact

Phase 0.5 is now specified. The next architectural/practical gate should not be knowledge production. The next task should implement or audit readiness for the contracts.

## 5. Final recommendation

The next task should be: **validator implementation slice**.

Reason: before a MacroForge/PostgreSQL capability audit or controlled production pilot can produce useful evidence, KnowledgeForge needs deterministic validators that can enforce the newly specified package, evidence, provenance, boundary, and unsupported-inference contracts on fixture packages. Without validators, a capability audit would identify possible inputs but still leave KnowledgeForge unable to determine whether a knowledge package is acceptable. Without validators, a production pilot design would rely too much on human/frontier-LLM judgment.

Recommended bounded next slice:

```text
Implement fixture-backed package-contract validators for one non-production KnowledgeCandidatePackage.
No MacroForge data pull.
No PostgreSQL schema.
No production knowledge artifact.
Validate schema, boundary language, evidence/provenance separation, required fingerprints, and lifecycle/maturity status.
```

This advances KnowledgeForge from specification toward reproducible generation readiness while preserving the no-production boundary.
