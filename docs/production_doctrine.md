# KnowledgeForge Production Doctrine

Date: 2026-07-09
Status: canonical operational production doctrine
Scope: KnowledgeForge production families, Phase 2 and beyond

## 1. Authority

This document freezes the validated KnowledgeForge production methodology as operational doctrine.

This is a doctrine freeze, not an architecture freeze. Future production remains evidence-driven. The burden of proof has shifted: the validated methodology is now the default, and deviations must justify themselves with repeated production evidence.

Authoritative basis reviewed:

- `CONSTITUTION.md`
- `docs/architecture.md`
- `state/architecture.md`
- accepted decisions under `artifacts/decisions/`
- `docs/knowledge_package_contract.md`
- `docs/validation_framework_v1.md`
- `docs/validator_taxonomy.md`
- `docs/provenance_fingerprinting.md`
- WDI Demographic Family Closeout Report
- WDI Environment Family Closeout Report
- Production Methodology Closeout Report
- `docs/production_evolution_log.md`
- `artifacts/reports/R-20260709-phase-2-production-expansion-strategy.md`

## 2. Evidence base

Doctrine status is supported by:

- two independently Mature production families: WDI demographic and WDI Environment;
- deterministic replay and fingerprint stability across Campaigns 0-12;
- validator stability across malformed provenance, missing lineage/fingerprint, evidence-contract, unsupported-inference, constitutional-boundary, and maturity-state failures;
- package stability across repository-level evidence, family evidence, cross-family comparison, recurrence audit, family maturation, family closeout, and methodology closeout;
- provenance and fingerprint stability across two family closeouts;
- Production Support layer stability after bounded implementation;
- Production Evolution Log governance stability through Campaigns 0-12 and Phase 2 planning.

## 3. Validated production methodology

KnowledgeForge production follows this invariant chain:

```text
Immutable Source Evidence Package
        ↓
Evidence Validation
        ↓
Evidence Evaluation
        ↓
KnowledgeCandidatePackage
        ↓
Candidate Validation
        ↓
KnowledgeObjectPackage
        ↓
Object Validation
        ↓
Production Quality Assessment
        ↓
Production Evolution Log update
        ↓
Family Maturity / Closeout where applicable
```

Production may use deterministic Production Support helpers to construct source packages and aggregate common quality metrics, but helpers do not redefine package contracts, validators, provenance, fingerprints, taxonomy, or architecture.

Validated KnowledgeObjectPackages may be persisted into the operational Knowledge Repository after object validation passes. Repository population is an additional operational output, not a replacement for packages, reports, validators, provenance, fingerprints, or Production Evolution Log governance.

## 4. Mandatory production invariants

Every production family inherits these invariants:

1. KnowledgeForge accumulates objective, reproducible, evidence-backed knowledge. It does not seek completeness, sophistication, or abstraction for their own sake; every addition should measurably improve repository objective knowledge while preserving reproducibility, auditability, and constitutional boundaries.
2. KnowledgeForge produces reusable evidence-level knowledge, not observations, ingestion outputs, interpretation, forecasts, recommendations, reports-as-products, visualizations, or downstream reasoning.
3. Evidence references and evidence evaluations remain distinct.
4. External observational systems remain systems of record for observations.
5. Knowledge objects require stable identity, provenance, evidence state, applicability/scope, lifecycle state, governance/review state, revision history, and dependency posture.
6. Representation neutrality is mandatory; files, tables, graphs, APIs, or databases are representations, not the defining abstraction.
7. Accepted means accepted for reuse under stated evidence and applicability conditions, not proven true.
8. Deterministic production is the default. Local or frontier LLM output is candidate/intermediate material only unless separately governed and fully fingerprinted; it is not direct evidence.
9. Rejected candidates are production evidence and must be preserved when they expose validation or boundary behaviour.
10. Architecture, taxonomy, validator, package, provenance, fingerprint, and workflow changes require repeated production evidence proving current doctrine insufficient.
11. Convenience, abstraction preference, novelty, or anticipated reuse are not sufficient reasons to deviate.

## 5. Required production stages

Every production family must use the validated stage pattern unless production evidence proves a stage is inapplicable for that family.

1. Evidence-quality transfer or source-evidence preflight.
2. Inventory/classification production where applicable.
3. Coverage/matrix production where applicable.
4. Rejected-candidate preservation and catalogue reporting.
5. Deterministic replay and fingerprint-stability verification.
6. Dedicated provenance-lineage completeness.
7. Family maturity assessment.
8. Family closeout report before Mature status.
9. Production Evolution Log update after each production campaign or family closeout.
10. Production-quality reporting before outputs are treated as accepted production knowledge.
11. Knowledge Repository population for validated KnowledgeObjectPackages when production outputs are materialized operationally.
12. Knowledge Repository Impact Assessment documenting repository value added, reusable knowledge introduced, composition changes, recomputation avoided, and repository-quality concerns/improvements.

## 6. Required validation behaviour

Validators must remain deterministic, narrow, explainable, and tied to constitutional or package contracts.

Required validation behaviour includes:

- constitutional-boundary rejection;
- evidence-contract validation;
- evidence/evaluation separation validation;
- provenance validation;
- reproducibility validation;
- package-schema validation;
- unsupported-inference rejection;
- lineage/fingerprint consistency validation;
- maturity/lifecycle-state validation;
- repository/governance consistency checks during closeout;
- tooling/environment issue classification separate from repository or governance inconsistency.

Validators may reject unsafe or malformed candidates. Rejections are expected safety behaviour, not evidence of validator insufficiency unless repeated false positives or false negatives appear in production.

## 7. Required provenance guarantees

Accepted production packages must retain or reference a provenance envelope with:

- package identity and version;
- generation date/timestamp;
- creator/tool/process;
- source system and source owner;
- evidence references and source-family classification;
- input dataset/query/template/model identifiers where applicable;
- computation recipe and parameters;
- generated intermediate identifiers where applicable;
- validation tool/version and results;
- governance/review actor or status;
- environment/toolchain notes where material;
- known nondeterminism and mitigation;
- reproducibility state.

Missing provenance for accepted objects is a blocker unless explicitly scoped as non-accepted candidate material.

## 8. Required fingerprint guarantees

Accepted production packages must record fingerprints for applicable:

- input datasets or source snapshots;
- evidence references;
- query definitions;
- computation recipes;
- prompts/templates if used;
- model identifiers and outputs if used;
- generated statements;
- package manifests;
- validation results and evolution metadata where applicable.

Changed inputs, queries, recipes, templates, models, validators, or generated statements require fingerprint change visibility and, where applicable, an evolution/change record.

## 9. Family maturation requirements

A production family may be classified Mature only after it demonstrates:

1. deterministic replay and fingerprint stability across multiple production scopes;
2. provenance completeness and lineage/fingerprint validation;
3. rejected-candidate preservation with meaningful failure categories;
4. no required architecture, taxonomy, validator, package-model, provenance, or fingerprint change;
5. scoped negative knowledge where missingness or unsupported dimensions exist;
6. inventory/classification and coverage/matrix production where applicable;
7. dedicated provenance-lineage completeness;
8. explicit classification of assumptions deferred to cross-family or multi-source campaigns;
9. family closeout report.

Stable remains available for families that have meaningful deterministic production evidence but have not yet completed provenance-lineage completeness and closeout.

## 10. Closeout requirements

Family Closeout Reports must document:

- validated capabilities;
- production assumptions confirmed;
- assumptions intentionally deferred;
- production pressures resolved;
- remaining open questions;
- lessons learned;
- evidence supporting maturity state;
- architectural continuity classification.

Production Methodology Closeout Reports are exceptional artifacts. They are justified only when multiple production families have reached Mature status and the methodology itself can be evaluated across families.

Knowledge Repository Impact Assessments are required at the conclusion of every production campaign. They are complementary to Production Quality Reports: Production Quality Reports evaluate how production performed; Knowledge Repository Impact Assessments evaluate the long-term value added to KnowledgeForge's operational repository. Each assessment must cover repository object counts before/after, new Knowledge Objects, new reusable knowledge, category and evidence-family expansion, repository breadth/depth gained, confidence gained, downstream recomputation avoided, composition changes, repository-quality concerns, and repository-quality improvements. This is an operational reporting refinement and does not authorize production-methodology, package, validator, provenance, fingerprint, Production Support, or architecture changes.

## 11. Production-governance expectations

The Production Evolution Log remains the canonical governance mechanism for production-driven evolution.

PEL rules:

1. Record observations only from production outputs, validation reports, rejected catalogues, production-quality reports, retrospectives, architecture observations, closeout reports, or planning artifacts explicitly grounded in production evidence.
2. Keep observations in `monitor` until repeated production evidence justifies investigation.
3. Move to `investigate` only for bounded planning/proof work.
4. Move to `implement` only after investigation plus later campaign evidence proves a minimal change preserves the architecture and reduces repeated production friction.
5. Move to `reject` when later evidence disproves or neutralizes the pressure.
6. Planning alone does not authorize implementation.

## 12. Burden of proof for future deviation

Future production families inherit this doctrine by default.

Deviation requires repeated production evidence demonstrating that the inherited methodology is insufficient.

The following are not sufficient reasons to deviate:

- architectural preference;
- convenience;
- elegance;
- abstraction opportunity;
- desire for reuse;
- novelty;
- similarity to another project;
- expectation that a future family might need different machinery;
- model availability;
- dashboard/API/database convenience.

Production evidence is the only accepted justification for methodological evolution.

## 13. Architectural continuity classification

Doctrine freeze classification: preserves agreed architecture.

This doctrine does not refine, duplicate, contradict, rename, or drift from the existing KnowledgeForge architecture. It canonizes the already validated production methodology as operational default.
## 14. Operational autonomy

KnowledgeForge is operationally autonomous for ordinary Operational Expansion campaigns. Campaign-by-campaign external prompting is complete. Future production progression derives from `docs/production_campaign_roadmap.md` and this doctrine.

The default operating cycle is defined in `docs/standard_operational_loop.md`. Doctrine review is interrupted only by the triggers defined in `docs/doctrine_review_triggers.md`. Normal campaigns, ordinary rejected candidates, family Stable/Mature transitions, and routine Repository Health or Knowledge Repository Impact Assessment generation do not trigger doctrine review.

Current autonomous next step after Campaign 15 is Campaign 16 — WDI Energy & Mining annual-scalar evidence-quality/source-evidence transfer.

Operational autonomy preserves agreed architecture. It does not redesign production methodology, validators, taxonomy, package hierarchy, provenance, fingerprints, Production Support, reporting, family maturation, or repository persistence.
