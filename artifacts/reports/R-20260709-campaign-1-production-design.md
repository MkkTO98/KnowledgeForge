# Campaign 1 Production Design

Date: 2026-07-09
Status: recommended design
Task: Campaign 1 planning — Knowledge Taxonomy Verification and Structural Production Design

## Campaign name

Campaign 1 — External WDI Annual-Scalar Demographic Structure Evidence-Quality and Coverage Knowledge

## Objective

Use the existing KnowledgeForge production architecture to generate only deterministic, constitutionally compliant evidence-level knowledge from an immutable Source Evidence Package representing a narrow WDI annual-scalar demographic-structure evidence scope.

The campaign is not intended to generate demographic interpretation or macroeconomic conclusions. It exists to increase production confidence by applying the proven package pipeline to a first external evidence domain.

## Architecture reused unchanged

Campaign 1 must reuse:

- existing component model: identity, content, applicability, evidence, evolution, governance;
- existing governed vocabularies and claim facets;
- existing production categories: factual, derived, classified, methodological, evidence_quality, coverage, negative, provenance;
- existing package hierarchy: SourceEvidencePackage, Evidence, EvidenceEvaluation, KnowledgeCandidatePackage, KnowledgeObjectPackage;
- existing validation pipeline;
- existing file-backed campaign output model;
- existing production-quality assessment standard.

## Proposed campaign organization

```text
artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/
  campaign_summary.json
  source_evidence_package.json or source_packages/
  knowledge_candidates/
  knowledge_objects/
  rejected/
  production_quality_report.json
  reports/
    campaign_1_final_report.md
    evidence_characterization_report.md
    generated_knowledge_object_catalogue.md
    rejected_knowledge_object_catalogue.md
    production_quality_report.md
    architectural_observations_report.md
```

## Input boundary

Input should be one small immutable Source Evidence Package. It may represent a WDI annual-scalar demographic-structure evidence scope, but KnowledgeForge must treat it only as evidence.

The package should contain enough information to support:

- source identity;
- dataset/evidence-family identity;
- indicator-family or source-indicator membership;
- territory scope;
- period scope;
- metadata availability;
- provenance;
- fingerprints;
- reproducibility metadata;
- validation metadata.

It must not imply dependency on another EIP repository, shared schema, API, adapter, database, runtime process, or shared code.

## Allowed output categories

Campaign 1 may produce only existing-category knowledge:

- factual: source/package facts inside the retained scope;
- coverage: territories, periods, indicators, dimensions present or absent;
- evidence_quality: provenance, metadata, freshness, validation state, missingness, lineage quality;
- provenance: source identity, snapshot fingerprints, construction/replay records;
- methodological: construction method, validation method, reproducibility procedure;
- negative: unsupported dimensions, unavailable observations, missing metadata, unsupported claims;
- classified: deterministic classification under existing vocabularies if required;
- derived: simple deterministic counts/ratios only if method, denominator, and missingness handling are explicit.

## Explicitly forbidden outputs

Reject any candidate containing:

- demographic interpretation;
- macroeconomic interpretation;
- causal claim;
- hypothesis;
- forecast;
- recommendation;
- explanation of significance;
- investment meaning;
- policy meaning;
- presentation narrative;
- broad source reliability claim not decomposed into objective evidence-quality dimensions.

## Minimal expected knowledge objects

The campaign should start with the smallest useful object set, for example:

1. source evidence package identity/provenance object;
2. indicator-family membership or source-indicator classification object;
3. territory coverage object;
4. temporal coverage object;
5. metadata/provenance completeness object;
6. reproducibility/fingerprint availability object;
7. scoped negative object for unsupported interpretive claims or unsupported dimensions.

This list is a design target, not a new taxonomy.

## Validation requirements

Every accepted object must pass:

```text
Source Evidence Package validation
Evidence validation
Evidence Evaluation validation
KnowledgeCandidatePackage validation
KnowledgeObjectPackage validation
Final constitutional boundary validation
Replay/fingerprint stability verification
```

Rejected candidates must be preserved with validator evidence.

## Non-goals

- no ontology redesign;
- no new card system;
- no new taxonomy;
- no local/frontier LLM generation;
- no database access or coupling;
- no adapters or APIs;
- no shared schema or shared code;
- no interpretation or presentation layer.

## Final design recommendation

Proceed with Campaign 1 using the existing architecture unchanged. The campaign should be organized by evidence family/scope while using existing package stages and knowledge categories internally.
