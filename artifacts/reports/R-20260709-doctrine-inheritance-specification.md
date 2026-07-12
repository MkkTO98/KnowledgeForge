# Doctrine Inheritance Specification

Date: 2026-07-09
Status: canonical inheritance specification for future production families

## 1. Purpose

This specification defines what every future KnowledgeForge production family inherits automatically from the validated production doctrine.

Future production-family planning should assume these are solved unless production proves otherwise.

## 2. Automatically inherited components

Every future production family inherits:

1. Package model:
   - Source Evidence Package;
   - Evidence Evaluation;
   - KnowledgeCandidatePackage;
   - KnowledgeObjectPackage;
   - KnowledgeChangePackage where evolution/change records are required;
   - GeneratedIntermediatePackage for non-accepted intermediate material.

2. Validator model:
   - deterministic validators;
   - constitutional-boundary checks;
   - evidence-contract checks;
   - provenance checks;
   - reproducibility checks;
   - unsupported-inference checks;
   - package-schema checks;
   - lineage/fingerprint checks;
   - maturity-state checks;
   - repository/governance checks;
   - tooling/environment classification.

3. Production workflow:
   - immutable evidence package construction;
   - evidence validation;
   - evidence evaluation;
   - candidate construction;
   - candidate validation;
   - object construction;
   - object validation;
   - production-quality assessment;
   - rejected-candidate preservation;
   - Production Evolution Log update;
   - maturity/closeout assessment where applicable.

4. Provenance handling:
   - explicit evidence references;
   - source identity/version/access metadata;
   - source family classification;
   - method/query/template/model identifiers when applicable;
   - validation and governance metadata;
   - reproducibility state.

5. Fingerprinting:
   - input/source fingerprints;
   - evidence-reference fingerprints;
   - query fingerprints where applicable;
   - computation-recipe fingerprints;
   - template/model/output fingerprints where applicable;
   - generated-statement fingerprints;
   - package-manifest fingerprints.

6. Reporting:
   - generated object catalogue;
   - rejected candidate catalogue;
   - production quality report;
   - retrospective/architectural observations where appropriate;
   - family maturity assessment;
   - family closeout report before Mature status.

7. Production Evolution Log governance:
   - monitor/investigate/implement/reject lifecycle;
   - production-evidence-only observation updates;
   - no implementation from planning alone;
   - repeated evidence requirement for change.

8. Maturity assessments:
   - Stable for deterministic production families that have not completed provenance-lineage closeout;
   - Mature only after dedicated provenance-lineage completeness and family closeout.

9. Family closeout process:
   - capabilities validated;
   - assumptions confirmed;
   - assumptions deferred;
   - pressures resolved;
   - open questions;
   - lessons learned;
   - evidence supporting maturity;
   - architectural-continuity classification.

## 3. Inheritance default

A future family planning artifact should not re-justify inherited components. It should instead identify:

- family-specific source identity;
- family-specific evidence scope;
- applicable inventory/coverage/provenance dimensions;
- candidate boundary risks;
- expected falsification contribution;
- known deviations, if any, backed by production evidence.

## 4. Deviation rule

Deviation from inherited doctrine requires repeated production evidence that the inherited component is insufficient.

Unsupported reasons for deviation include convenience, anticipated scale, external project resemblance, desire for abstraction, novelty, model availability, or speculative downstream value.

## 5. Classification

This inheritance specification preserves the agreed architecture. It does not refine, duplicate, contradict, or drift.
