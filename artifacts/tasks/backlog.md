# Backlog

## Current next production task

### B-20260712-001 — Campaign 43 coefficient-free first-difference companion registry freeze

Priority: P0 for next production sequencing
Status: pending authorization
Source: `artifacts/decisions/D-20260712-next-production-readiness-before-campaign43.md`

Objective:

- Freeze a coefficient-free first-difference Pearson companion registry for the six remaining Campaign 41 high-shared-time-trend raw Pearson relationships.
- Reuse the existing `wdi_annual_scalar_first_difference_pearson_v1@1.0` method contract.
- Stop before coefficient calculation, package publication, PostgreSQL mutation, or Campaign 43 production execution.

## Completed

### B-20260709-004 — Campaign 2: WDI demographic-structure completeness buckets

Status: completed
Task artifact: `artifacts/tasks/T-20260709-campaign-2-wdi-completeness-buckets.md`
Output: `artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/`

## Next recommended task

### B-20260711-001 — Durability-destination decision and sensitive/local-path remediation

Priority: P0
Status: pending authorization
Source: `artifacts/reports/repository-wide-durability-inventory-supersession-correction-20260711/consolidated_report.md`

Objective:

- Decide durable destinations for recovery-critical untracked KnowledgeForge material before any staging request.
- Classify ordinary Git vs Git LFS vs immutable external artifact storage vs operational backup/checkpointing.
- Remediate sensitive/local-path findings without exposing secret values.

Acceptance criteria:

- canonical packages, repository manifest/indexes/evolution records, method contracts, evidence fixtures, release registries, outbox/inbox state, handoff evidence, and recovery-critical reports have approved durability destinations;
- sensitive scan passes or remaining findings are explicitly classified false-positive/remain-ignored;
- repository-wide durability validator no longer blocks on untracked canonical/recovery-critical state;
- no staging/commit/push until separately authorized.

## Historical next recommended task

### B-20260709-005 — Campaign 3: WDI demographic-structure source freshness and release metadata coverage

Priority: P0
Status: pending
Source: Campaign 2 final recommendation and `docs/production_campaign_roadmap.md`

Objective:

- Characterize source freshness metadata, release-key availability, last-updated availability, null release-date patterns, and freshness-provenance completeness.

Scope:

- WDI annual-scalar demographic-structure release/freshness metadata only;
- provenance;
- evidence quality;
- coverage;
- scoped negative knowledge;
- methodological validation state.

Constraints:

- preserve existing architecture unchanged;
- no interpretation, causal claims, prospective claims, recommendations, policy meaning, investment meaning, or presentation narrative;
- no adapters, APIs, shared schemas, repository coupling, database coupling, runtime infrastructure, or LLM generation.

Acceptance criteria:

- existing architecture reused unchanged;
- SourceEvidencePackages routed through current production pipeline;
- rejected candidates preserved and analysed;
- Production Evolution Log updated with Campaign 3 evidence;
- production-quality report and architectural observations produced;
- final verification passes.

## Investigation candidates after Campaign 2

### I-20260709-001 — Deterministic SourceEvidencePackage authoring helper investigation

Status: pending investigation only
Evidence: PEL-008 moved to investigate after recurring pressure in Campaigns 1 and 2.
Boundary: planning/proof only; must not change architecture or output contracts without separate approval.

### I-20260709-002 — Reusable production-quality metric aggregation helper investigation

Status: pending investigation only
Evidence: PEL-009 moved to investigate after recurring pressure in Campaigns 1 and 2.
Boundary: planning/proof only; must not change architecture or output contracts without separate approval.


## Completed investigations

### B-20260709-006 — Production Evolution Investigation 1: PEL-008 and PEL-009

Status: completed
Task artifact: `artifacts/tasks/T-20260709-production-evolution-investigation-1-pel-008-009.md`
Decision: PEL-008 and PEL-009 both Continue Investigate; do not implement helpers before Campaign 3.


## Completed production campaigns

### B-20260709-007 — Campaign 3 WDI source freshness and release metadata coverage

Status: completed
Task artifact: `artifacts/tasks/T-20260709-campaign-3-wdi-freshness-release-metadata.md`
Output bundle: `artifacts/production/campaign-3-wdi-demographic-structure-source-freshness-release-metadata/`
Decision: PEL-008 and PEL-009 ready for bounded implementation proof before Campaign 4.


## Ready implementation proofs

### B-20260709-008 — PEL-008/PEL-009 bounded helper proof

Status: completed
Evidence basis: Campaigns 0-3 plus Production Evolution Investigation 1.
Scope: implement deterministic operational helpers only if they emit existing SourceEvidencePackage/report shapes, preserve validator clarity, preserve auditability/reproducibility, and introduce no architecture change.


## Ready production campaigns

### B-20260709-009 — Campaign 4 WDI indicator-family inventory expansion

Status: ready
Prerequisite satisfied: bounded PEL-008/PEL-009 Production Support proof completed.
Scope: proceed using refined deterministic Production Support implementation without further architecture change or helper extraction.


### B-20260709-010 — Campaign 4 after falsification review

Status: ready
Prerequisite satisfied: production falsification review completed.
Scope: proceed to Campaign 4 unchanged; monitor PEL-017 gaps but do not insert a pre-Campaign-4 stress campaign.


### B-20260709-011 — Campaign 5 territorial coverage matrix

Status: ready
Prerequisite satisfied: Campaign 4 completed without blocker.
Scope: execute approved Campaign 5 unchanged; stress larger deterministic object sets, territorial applicability scopes, repeated missingness statements, and fingerprint stability under more object volume.


### B-20260709-012 — Campaign 6 temporal coverage matrix

Status: ready
Prerequisite satisfied: Campaign 5 completed without blocker.
Scope: execute approved Campaign 6 unchanged; stress period applicability, deterministic temporal bucket construction, recurring negative knowledge about missing periods, and boundary wording for historical time coverage without forecasting.


### B-20260709-013 — Campaign 7 provenance lineage completeness

Status: ready
Prerequisite satisfied: Campaign 6 completed without blocker.
Scope: execute approved Campaign 7 unchanged; stress provenance envelope completeness, lineage/fingerprint validation, raw artifact hashes/URLs/release keys/source URLs/license notes, malformed provenance rejection, and post-Campaign-7 family maturity assessment.


### B-20260709-014 — Campaign 8 planning gate

Status: completed
Outcome: selected WDI Environment annual-scalar evidence as the second production family. Campaign 8 should be a narrow evidence-quality and coverage transfer campaign.


### B-20260709-015 — Campaign 8 WDI Environment evidence-quality and coverage transfer

Status: completed
Prerequisite satisfied: Campaign 8 planning gate selected WDI Environment annual-scalar evidence.
Scope: execute a narrow deterministic Environment evidence-quality and coverage transfer campaign using existing architecture, package model, validators, Production Support layer, provenance/fingerprints, rejected-candidate preservation, and production-quality reporting.
Non-goals: no interpretation, architecture redesign, validator/taxonomy change, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local model generation, or frontier model generation.


### B-20260709-016 — Campaign 9 cross-family WDI annual-scalar coverage comparison

Status: completed
Prerequisite satisfied: Campaign 8 completed and methodology transfer to WDI Environment was successful.
Scope: compare WDI demographic and WDI Environment annual-scalar coverage at evidence-inventory level, produce valid multi-reference Knowledge Objects where supported, preserve existing architecture, and avoid interpretation or significance claims.
Non-goals: no architecture redesign, validator/taxonomy change, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local model generation, or frontier model generation.


### B-20260709-017 — Campaign 10 cross-campaign duplicate and recurrence audit

Status: completed
Prerequisite satisfied: Campaign 9 completed and validated multi-reference cross-family Knowledge Objects without architecture change.
Scope: production-artifact-as-evidence audit of duplicate pressure, repeated metadata patterns, repeated validator failures, recurring deterministic transformations, and recurrence-count derived knowledge across Campaigns 0-9.
Non-goals: no architecture redesign, validator/taxonomy change, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local model generation, or frontier model generation.


### B-20260709-018 — Campaign 11 WDI Environment indicator-family inventory and coverage matrix maturation

Status: completed
Prerequisite satisfied: Campaign 10 completed and found no duplicate-registry, helper-extraction, architecture, taxonomy, validator, or workflow pressure.
Scope: deterministic WDI Environment indicator-family inventory and coverage matrix maturation using existing package model, validators, Production Support, provenance/fingerprint model, and reporting.
Non-goals: environmental interpretation, causal/significance claims, forecasts, recommendations, architecture redesign, taxonomy/validator change, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local model generation, or frontier model generation.


### B-20260709-019 — Campaign 12 WDI Environment provenance-lineage completeness and family closeout

Status: completed
Prerequisite satisfied: Campaign 11 completed and classified WDI Environment as Stable without architecture/taxonomy/validator/workflow pressure.
Scope: deterministic Environment provenance-lineage completeness and family closeout using existing package model, validators, Production Support, provenance/fingerprint model, and reporting.
Non-goals: environmental interpretation, causal/significance claims, forecasts, recommendations, policy/investment meaning, architecture redesign, taxonomy/validator change, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local model generation, or frontier model generation.


### B-20260709-020 — Campaign 13 third WDI annual-scalar evidence-family selection and transfer

Status: ready
Prerequisite satisfied: Campaign 12 completed; WDI demographic and WDI Environment families are Mature; Production Methodology Closeout Report exists.
Scope: select and begin a third WDI annual-scalar evidence family using the established methodology unchanged.
Non-goals: architecture redesign, taxonomy/validator changes, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local/frontier LLM generation, environmental/economic/policy interpretation, forecasts, recommendations, or presentation narrative.


### B-20260709-021 — Phase 2 WDI Infrastructure production-family maturation

Status: ready
Basis: Phase 2 Production Expansion Strategy selected WDI Infrastructure as the first Phase 2 family.
Scope: mature WDI Infrastructure annual-scalar evidence using the established Production Methodology Closeout criteria unchanged.
Non-goals: architecture redesign, taxonomy/validator/package changes, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local/frontier LLM generation, economic interpretation, policy meaning, investment meaning, forecasts, recommendations, or presentation narrative.

### B-20260709-022 — Phase 2 WDI Energy & Mining production-family maturation

Status: deferred until Infrastructure transfer evidence exists
Basis: Phase 2 ordering.
Scope: second Phase 2 family after Infrastructure, using established methodology unchanged.

### B-20260709-023 — Phase 2 WDI Agriculture & Rural Development production-family maturation

Status: deferred until Infrastructure and Energy evidence exist
Basis: Phase 2 ordering.
Scope: smaller-family contrast using established methodology unchanged.

### B-20260709-024 — Phase 2 broader WDI cross-family comparison

Status: deferred until at least three Mature/near-Mature WDI annual-scalar families exist
Basis: Phase 2 dependency map.
Scope: multi-family comparison to exercise multi-reference, overlap, duplicate-pressure, and provenance-difference behaviour.

### B-20260709-025 — Phase 2 non-WDI multi-source disagreement planning gate

Status: intentionally deferred
Basis: PEL-017 remains the major falsification gap, but Phase 2 strategy recommends additional WDI breadth first.
Scope: later deliberate planning gate for source disagreement without architecture redesign.


### B-20260709-026 — Operational Expansion: WDI Infrastructure under frozen doctrine

Status: ready
Basis: Production Doctrine Freeze and Phase 2 Production Expansion Strategy.
Scope: mature WDI Infrastructure annual-scalar evidence as the first Operational Expansion family using `docs/production_doctrine.md` unchanged.
Inherited doctrine: package model, validator model, production workflow, provenance handling, fingerprinting, reporting, Production Evolution Log governance, maturity assessments, and family closeout process.
Non-goals: architecture redesign, methodology redesign, taxonomy/validator/package changes, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local/frontier LLM generation, interpretation, forecast, recommendation, policy meaning, investment meaning, or presentation narrative.


### B-20260709-027 — Phase 2 start: WDI Infrastructure production-family maturation

Status: ready
Basis: Foundation Era closeout, Operational Expansion Declaration, Production Doctrine Freeze, and Phase 2 Production Expansion Strategy.
Scope: begin Phase 2 by maturing WDI Infrastructure annual-scalar evidence under `docs/production_doctrine.md` unchanged.
Inherited doctrine: package model, validator model, production workflow, provenance handling, fingerprinting, reporting, Production Evolution Log governance, maturity assessments, rejected-candidate preservation, and family closeout process.
Non-goals: architecture redesign, methodology redesign, taxonomy/validator/package changes, runtime infrastructure, adapters/APIs/shared schemas, database coupling, repository coupling, local/frontier LLM generation, interpretation, forecasting, recommendations, policy/investment meaning, completeness for its own sake, sophistication for its own sake, or abstraction for its own sake.


### B-20260709-028 — Populate Knowledge Repository during WDI Infrastructure production

Status: ready
Basis: Knowledge Repository Operationalization completed.
Scope: when maturing WDI Infrastructure annual-scalar production family, persist validated KnowledgeObjectPackages into `knowledge_repository/` using `tools/knowledge_repository.py` after validation passes. Continue producing reports as governance artifacts.
Non-goals: package redesign, repository coupling, API/adapter/shared schema, runtime synchronization, cache layer, database coupling, local/frontier LLM generation.


### B-20260709-029 — Continue WDI Infrastructure family maturation

Status: ready
Basis: Campaign 13 completed first WDI Infrastructure evidence-quality and coverage transfer.
Scope: run the next bounded Infrastructure-family production campaign under `docs/production_doctrine.md` unchanged, preserving validators/package contracts/provenance/fingerprints and populating `knowledge_repository/` after validation.
Non-goals: architecture redesign, taxonomy redesign, validator redesign, repository coupling, adapters/APIs/shared schemas, runtime synchronization, cache/database layers, local/frontier LLM generation.

## Completed — Campaign 14 WDI Infrastructure maturation

- Task artifact: `artifacts/tasks/T-20260709-campaign-14-wdi-infrastructure-maturation.md`
- Campaign output: `artifacts/production/campaign-14-wdi-infrastructure-indicator-family-coverage-maturation/`
- Knowledge Repository objects added: 36
- Repository object count: 72

## Next — Campaign 15 WDI Infrastructure provenance-lineage completeness

Execute Infrastructure provenance-lineage completeness under the existing Production Doctrine unchanged. Populate the Knowledge Repository, produce Repository Health, and close out the WDI Infrastructure family if Mature criteria are satisfied.

## Next operational task — Campaign 16 WDI Energy & Mining evidence-quality transfer

Status: pending

Execute the next Phase 2 production family: WDI Energy & Mining annual-scalar evidence. Use the Production Doctrine unchanged. Begin with evidence-quality/source-evidence transfer, validate all KnowledgeObjectPackages, populate the Knowledge Repository, and produce Repository Health plus Knowledge Repository Impact Assessment.

## Next recommended integration task

### B-20260711-MF-001 — Connect MacroForge exporter execution to successful canonical release closeout

Priority: P0
Status: pending
Source: MacroForge real handoff compatibility pilot integration decision B.

Objective: ask MacroForge to trigger its neutral evidence-release exporter from successful canonical release closeout, preserving producer-side release/run lineage and avoiding scheduler/canonical-mutation work until handoff generation is reliable.

Constraints: no KnowledgeForge canonical promotion, no inbox scheduling, no PostgreSQL incremental mutation, no shared runtime code, and no MacroForge private-schema dependency.
