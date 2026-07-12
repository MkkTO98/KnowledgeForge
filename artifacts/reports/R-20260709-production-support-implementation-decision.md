# Implementation Decision Report — Minimal Production Support Layer

Date: 2026-07-09
Status: completed
Scope: PEL-008 and PEL-009 only

## Decision

Implement a minimal deterministic Production Support layer.

Implemented file:

- `tools/production_support.py`

Integrated into:

- `tools/run_campaign0_repository_evidence.py` for SourceEvidencePackage construction;
- `tools/run_campaign1_wdi_demographic_evidence.py` for SourceEvidencePackage construction and common quality metrics;
- `tools/run_campaign2_wdi_completeness_buckets.py` for SourceEvidencePackage construction and common quality metrics;
- `tools/run_campaign3_wdi_freshness_metadata.py` for SourceEvidencePackage construction and common quality metrics.

## Implemented responsibilities

### SourceEvidencePackage construction

`build_source_evidence_package(...)` assembles the existing package dictionary and calls the existing fingerprint builder.

It does not decide campaign metadata. All campaign-specific values remain explicit at each campaign call site.

### Common production-quality aggregation

`aggregate_common_quality_metrics(...)` computes only the common metrics repeated by Campaigns 1-3:

- source package count;
- candidate count;
- accepted object count;
- rejected record count;
- acceptance/rejection rate;
- produced category counts;
- rejected category counts;
- validator failure category counts;
- average evidence references;
- provenance completeness;
- fingerprint stability flag;
- determinism flag;
- duplicate-pressure flag.

Campaign-specific processing statistics, cross-campaign comparisons, architectural observations, and report prose remain in campaign scripts.

## Contracts preserved

Preserved:

- every existing production artifact shape;
- every Knowledge Object package structure;
- every SourceEvidencePackage structure;
- every validator;
- every report format;
- fingerprint stability for Campaigns 1-3;
- determinism for Campaigns 0-3;
- rejected-candidate preservation;
- campaign-specific auditability.

Campaign 0 note:

Campaign 0 is repository-snapshot-based and therefore its snapshot fingerprint changed after adding/refactoring production code and tests. This is expected repository-evidence behavior, not a behavior change. Campaign 0 regression tests and rerun still verified accepted/rejected counts, validator behavior, determinism, and fingerprint stability for the new repository state.

## Why this is not architectural redesign

The support layer is not canonical architecture. It is operational support for repeated deterministic mechanics.

It introduces no:

- package model;
- validator framework;
- taxonomy;
- workflow engine;
- registry;
- schema;
- adapter;
- API;
- persistence;
- runtime infrastructure;
- local or frontier model behavior.

## Decision outcome

The implementation satisfied PEL-008 and PEL-009 without introducing new implementation pressure requiring immediate extraction.

Further helper extraction is rejected for now because no repeated production evidence beyond PEL-008 and PEL-009 justifies it.
