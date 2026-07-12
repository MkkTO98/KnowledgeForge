# KnowledgeForge Roadmap

Status: Campaign 0 complete; narrow domain-specific deterministic production campaign recommended next

## Phase 0 — Specification-only foundation (completed)

Purpose: establish ownership, boundaries, principles, interfaces, governance, and future responsibilities before implementation.

Allowed work:

- architecture specification;
- principles;
- interface contracts;
- decision artifacts;
- task artifacts;
- open-question capture;
- state/handoff/summaries;
- coherence verification.

Forbidden work:

- runtime code;
- databases;
- APIs;
- graph computation;
- statistical pipelines;
- external services;
- deployment;
- cross-project mutation.

Exit criteria:

- foundational scope accepted;
- observational/reasoning/navigation/presentation/future-project boundaries accepted in repository-independent terms;
- knowledge object component model stable enough for implementation planning;
- claim facets and governed vocabulary posture accepted;
- relationship-representation and dependency posture/facet responsibilities accepted;
- lifecycle, provenance, evidence, governance, stable identity, knowledge-change, and invariant requirements accepted;
- open questions triaged into pre-implementation blockers versus implementation-pressure deferrals.

## Phase 0.5 — Architectural assimilation consolidation (completed)

Purpose: translate the 2026-07-09 architectural assimilation campaign into KnowledgeForge-local contracts before any additional knowledge generation or implementation.

Required artifacts:

- evidence-source and evidence-evaluation architecture;
- reproducible knowledge-generation boundary;
- knowledge candidate/package conceptual contract;
- deterministic validation taxonomy and failure classifications;
- provenance envelope and fingerprinting expectations;
- local-model/frontier-LLM routing policy;
- knowledge-change/evolution report contract;
- pre-implementation blocker triage.

Exit criteria:

- future knowledge artifacts can be produced through a reproducible, provenance-bearing, validator-gated workflow;
- LLM output is clearly candidate material, not accepted knowledge;
- implementation of the next slice can be approved or rejected from explicit evidence and risk.

Primary review artifacts:

- `artifacts/reports/R-20260709-architectural-assimilation-review.md`
- `artifacts/reports/R-20260709-architectural-assimilation-candidate-matrix.md`
- `artifacts/reports/R-20260709-architectural-assimilation-decisions.md`
- `artifacts/reports/R-20260709-architectural-assimilation-roadmap.md`
- `artifacts/reports/R-20260709-architectural-assimilation-risks-prerequisites.md`

## Phase 0.6 — Fixture-backed validator implementation slice (completed)

Purpose: make the new reproducible knowledge-generation contracts enforceable before source-evidence readiness audits or production pilots.

Allowed work:

- non-production fixture KnowledgeCandidatePackage examples;
- deterministic validators for package schema, boundary language, evidence/provenance separation, fingerprint presence, lifecycle/maturity overclaim, and unsupported inference;
- negative fixtures and unit tests;
- documentation updates and closeout artifacts.

Forbidden work:

- production knowledge artifacts;
- external source data pulls unless separately approved after validator baseline;
- database schemas;
- vector databases, dashboards, schedulers, daemons, APIs, or UI infrastructure;
- local-model/frontier-LLM generation pilots.

Exit criteria:

- validators can classify blockers and warnings against at least one fixture package;
- negative fixtures prove boundary/evidence/provenance/fingerprint failures are detected;
- task report states whether external evidence readiness audit is ready next.

## Phase 0.7 — Capability and production readiness audit (completed; recommendations partially superseded)

Purpose: audit a current local external evidence inventory against KnowledgeForge Validation Framework v1 before production knowledge generation.

Primary artifacts:

- `artifacts/reports/R-20260709-macroforge-compatibility-audit.md` (historical evidence audit; adapter recommendations superseded)
- `artifacts/reports/R-20260709-knowledge-capability-inventory.md` (historical inventory; not an architectural dependency)
- `artifacts/reports/R-20260709-knowledge-opportunity-catalogue.md`
- `artifacts/reports/R-20260709-intelligence-routing-assessment.md`
- `artifacts/reports/R-20260709-production-gap-analysis.md` (superseded where it recommends project-specific adapters)
- `artifacts/reports/R-20260709-first-production-campaign-recommendation.md` (superseded where it recommends project-specific adapters)

Sovereign conclusion:

- External WDI annual-scalar evidence is viable for a first controlled production campaign after a KnowledgeForge-owned real-fixture replay validation slice.
- The first production campaign should be External WDI Annual-Scalar Demographic Structure Evidence-Quality and Coverage Knowledge.
- Production generation must not start until a non-production KnowledgeForge Source Evidence Package v1 Real-Fixture Replay Validation Slice passes v1 validation.
- No project-specific adapter, shared schema, runtime interface, database coupling, or cross-repository dependency is approved.

## Phase 0.8 — Architectural sovereignty correction (completed)

Purpose: remove project-specific adapter/interface/coupling language introduced by the previous assimilation/readiness tasks while preserving useful KnowledgeForge-owned architectural lessons.

Primary artifacts:

- `artifacts/reports/R-20260709-architectural-sovereignty-occurrence-catalogue.md`
- `artifacts/reports/R-20260709-architectural-sovereignty-review.md`
- `artifacts/reports/R-20260709-architectural-sovereignty-correction-report.md`
- `artifacts/reports/R-20260709-production-readiness-sovereignty-assessment.md`

Exit criteria:

- current architecture/state/backlog/roadmap use KnowledgeForge-owned evidence, provenance, package, fingerprint, and validation terminology;
- historical project-specific audit artifacts are clearly treated as evidence history, not current architecture;
- next production prerequisite is repository-independent and non-production;
- no implementation or cross-repository integration is introduced.

## Phase 0.9 — Knowledge Package Construction Validation Slice (completed)

Purpose: prove deterministic end-to-end construction from immutable Source Evidence Package input into KnowledgeForge-owned Evidence, Evidence Evaluation, KnowledgeCandidatePackage, and KnowledgeObjectPackage without producing production knowledge.

Primary artifacts:

- `tools/construct_knowledge_package_v1.py`
- `tests/test_package_construction_validation_v1.py`
- `tests/fixtures/package_construction_v1/valid_source_evidence_package.json`
- `docs/knowledge_acceptance_criteria.md`
- `artifacts/reports/R-20260709-construction-validation-report.md`
- `artifacts/reports/R-20260709-determinism-verification-report.md`
- `artifacts/reports/R-20260709-construction-validation-coverage-report.md`
- `artifacts/reports/R-20260709-remaining-production-risks.md`
- `artifacts/reports/R-20260709-final-production-readiness-assessment.md`

Exit criteria met:

- immutable Source Evidence Package validates;
- Evidence validates independently;
- Evidence Evaluation validates independently;
- KnowledgeCandidatePackage validates independently;
- KnowledgeObjectPackage validates independently;
- replay is deterministic and fingerprint-stable;
- required negative cases fail for intended reasons;
- knowledge acceptance criteria define accepted, rejected, and deferred object categories;
- no repository dependency, adapter, shared schema, shared code, API, database coupling, runtime infrastructure, or LLM execution was introduced.

## Phase 1 — First controlled production campaign (approved next)

Purpose: validate KnowledgeForge production workflow under real operating conditions with the narrowest possible constitutionally safe campaign.

Approved campaign:

External WDI Annual-Scalar Demographic Structure Evidence-Quality and Coverage Knowledge.

Allowed themes:

- source scope;
- age-sex cohort indicator-family membership;
- coverage;
- missingness;
- source freshness;
- provenance;
- validation state;
- scoped negative knowledge.

Forbidden themes:

- demographic interpretation;
- forecasts;
- hypotheses;
- causal claims;
- investment meaning;
- policy meaning;
- recommendations;
- presentation narrative.

Mandatory gates:

- immutable Source Evidence Package input;
- deterministic construction;
- independent validation of every stage;
- recomputed fingerprints;
- `docs/knowledge_acceptance_criteria.md` object-promotion gate;
- complete production report, package inventory, task artifact, state update, and handoff.

Exit criteria:

- at least one controlled production KnowledgeObjectPackage passes all gates;
- generated packages remain within accepted knowledge categories;
- no boundary-language, provenance, reproducibility, lifecycle, or fingerprint blocker remains;
- production workflow can be repeated from source package input.


## Phase 1.1 — Campaign 0: Repository Evidence Characterization (completed)

Purpose: validate the complete production architecture under real operating conditions using only repository/evidence-level knowledge.

Primary artifacts:

- `tools/run_campaign0_repository_evidence.py`
- `tests/test_campaign0_repository_evidence.py`
- `docs/production_quality_assessment.md`
- `artifacts/production/campaign-0-repository-evidence-characterization/`

Observed result:

- 10 Source Evidence Packages processed;
- 10 KnowledgeCandidatePackages created;
- 10 KnowledgeObjectPackages accepted;
- 3 rejected candidates preserved;
- determinism verified;
- fingerprint stability verified;
- no interpretive knowledge generated;
- no architecture redesign required.

## Phase 1.2 — Narrow domain-specific deterministic production campaign (recommended next)

Purpose: increase architectural confidence by applying the proven production pipeline to a narrow external evidence domain while remaining deterministic and constitutionally compliant.

Recommended campaign:

External WDI Annual-Scalar Demographic Structure Evidence-Quality and Coverage Knowledge.

Allowed: evidence quality, coverage, missingness, source freshness, provenance, validation state, scoped negative knowledge.

Forbidden: interpretation, hypotheses, forecasts, causal claims, recommendations, presentation narrative, investment meaning, policy meaning, adapters, APIs, shared schemas, database coupling, runtime infrastructure, and LLM generation.

## Phase 2 — Conceptual model hardening

Purpose: convert the foundational architecture into implementation-ready contracts without building runtime systems.

Likely artifacts:

- knowledge object component specification;
- claim facet vocabulary and claim object specification;
- stable identity/revision/split/merge semantics;
- relationship representation specification;
- knowledge dependency posture/facet specification;
- canonical concept and source-indicator mapping specification;
- source evidence reference contract;
- evidence evaluation contract;
- lifecycle state machine specification;
- governance/review state specification;
- confidence/uncertainty representation decision;
- provenance model specification;
- methodological knowledge specification;
- negative knowledge specification;
- knowledge-change audit concept specification;
- storage selection criteria.

Exit criteria:

- a future implementer can build a minimal vertical slice without redefining ownership boundaries;
- no unresolved L3/L4 boundary questions remain for the first slice.

## Phase 3 — Minimal implementation planning

Purpose: choose one narrow vertical slice that proves the architecture without turning KnowledgeForge into a platform too early.

Candidate first slice:

```text
One external source evidence fixture
  ↓ reference/snapshot only
One canonical concept
  ↓
One mapping object
  ↓
One claim object
  ↓
One relationship representation or negative finding
  ↓
One dependency declaration
  ↓
One evidence/provenance/lifecycle/governance record
  ↓
One read-only KnowledgeForge-owned export artifact
```

The slice should be deterministic, fixture-backed where possible, and explicitly non-production.

Exit criteria:

- task artifact for implementation exists;
- storage decision exists;
- tests and verification plan exist;
- rollback/migration plan exists;
- no external credentials, cross-repository adapters, shared schemas, or production data required.

## Phase 3 — Minimal implementation

Purpose: implement the smallest end-to-end reusable knowledge path.

Allowed only after explicit approval.

Likely implementation concerns:

- schemas or equivalent contracts;
- persistent knowledge store or file-backed prototype;
- evidence reference validation;
- lifecycle state validation;
- claim object creation;
- relationship representation or negative-knowledge object creation;
- dependency declaration validation;
- deterministic tests;
- export/read artifact.

Non-goals:

- broad ontology;
- generalized graph platform;
- large-scale statistical discovery;
- dashboards;
- reasoning;
- forecasting;
- decision automation;
- cross-project runtime integration.

## Phase 4 — Empirical relationship subsystem

Purpose: compute or preserve reusable empirical claims and relationship representations as governed knowledge objects, including negative empirical findings when method and evidence scope are explicit.

Preconditions:

- source evidence reference contract stable;
- method metadata model stable;
- uncertainty/confidence model stable;
- lifecycle gates defined;
- spurious discovery safeguards defined.

Initial method candidates:

- Pearson;
- Spearman;
- Kendall;
- cross-correlation;
- rolling correlations.

More complex methods such as mutual information, cointegration, and regime-dependent models should wait until simpler relationship governance has proven reliable.

## Phase 5 — Consumer export/use discipline

Purpose: let downstream systems consume KnowledgeForge knowledge artifacts without duplicating or mutating its responsibilities.

Likely export/use posture:

- downstream systems consume concepts, claims, relationship representations, dependencies, evidence, uncertainty, contradictions, negative knowledge, methodological knowledge, and lifecycle state through KnowledgeForge-owned export artifacts or approved references;
- downstream use does not validate, mutate, or raise confidence in KnowledgeForge objects;
- KnowledgeForge still does not generate reports or visualization.

## Phase 6 — Domain expansion

Purpose: expand beyond economics only after the economics substrate proves stable.

Candidate domains:

- companies;
- industries;
- products;
- regulations;
- supply chains;
- events;
- academic knowledge;
- geographic entities.


## Phase 1.1 — Campaign 1 WDI evidence-quality production (completed)

Purpose: validate repeatable domain-specific controlled production using the existing architecture unchanged.

Primary artifacts:

- `tools/run_campaign1_wdi_demographic_evidence.py`
- `tests/test_campaign1_wdi_demographic_evidence.py`
- `artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/`
- `artifacts/tasks/T-20260709-campaign-1-wdi-demographic-evidence-quality-coverage.md`

Exit criteria met:

- 12 KnowledgeObjectPackages accepted;
- 4 rejected candidates preserved;
- determinism verified;
- fingerprint stability verified;
- no duplicate Knowledge Objects detected;
- no architecture redesign required.

## Phase 1.2 — Next recommended production campaign

Recommended from Campaign 1 evidence: WDI annual-scalar demographic-structure completeness by indicator family and period/territory completeness buckets.

The campaign must preserve existing architecture unchanged and remain evidence-level, deterministic, and non-interpretive.


## Phase 1.15 — Production campaign roadmap and evolution log (completed)

Purpose: govern production-driven evolution before Campaign 2 by sequencing approximately the next 10 campaigns and accumulating production observations before any architecture or implementation change.

Primary artifacts:

- `docs/production_campaign_roadmap.md`
- `docs/production_evolution_log.md`
- `artifacts/tasks/T-20260709-production-campaign-roadmap-evolution-log.md`

Conclusion:

- Campaign 2 should proceed exactly as planned.
- Campaigns 0 and 1 support preserving the existing architecture unchanged.
- Helper candidates remain monitored, not approved for implementation.


## Phase 1.3 — Campaign 2 completed

Campaign 2 — WDI Annual-Scalar Demographic Structure Completeness Buckets — completed.

Primary output:

- `artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/`

Conclusion:

- Existing architecture remains sufficient.
- Deterministic SourceEvidencePackage authoring helper and production-quality metric aggregation helper are now investigation candidates only.
- Campaign 3 should proceed next as sequenced: WDI demographic-structure source freshness and release metadata coverage.


## 2026-07-11 — Release-driven automation next step

KnowledgeForge consumer-side release inbox/registry/no-promote impact processing is validated against retained WDI evidence and existing Pearson derivations. Do not keep simulating indefinitely; next recommended slice is a separate MacroForge-owned neutral evidence-release exporter task.
