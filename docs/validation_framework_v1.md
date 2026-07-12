# KnowledgeForge Validation Framework v1

Date: 2026-07-09
Status: pre-production vertical slice implemented

## Purpose

Validation Framework v1 is a deterministic, fixture-backed proof that KnowledgeForge's assimilation consolidation contracts are enforceable before processing real external evidence fixtures.

It is not a production implementation. It performs no database access, no model calls, no production knowledge generation, and no runtime service behavior.

## Pipeline boundaries

The framework validates five independent architectural stages:

```text
Evidence
  -> Evidence Evaluation
  -> Knowledge Candidate
  -> Knowledge Object
  -> Knowledge Change
```

Each validator checks one boundary. A later-stage validator does not silently repair or reinterpret a malformed earlier-stage artifact.

## Implementation

- Validator: `tools/validate_knowledge_pipeline_v1.py`
- Tests: `tests/test_validation_framework_v1.py`
- Synthetic fixtures: `tests/fixtures/validation_framework_v1/`

## Stage responsibilities

### Evidence

Checks required metadata, source identity, provenance references, fingerprint presence, evidence classification, and reproducibility handle/state. Blocks malformed evidence and unsupported direct evidence such as LLM output.

### Evidence Evaluation

Checks evidence/evaluation separation, supported evaluation dimensions, uncertainty representation, contradiction records, forbidden interpretation language, provenance, fingerprints, and reproducibility metadata.

### Knowledge Candidate

Checks package schema, constitutional boundary compliance, evidence references, provenance envelope, required fingerprints, confidence/quality metadata, unsupported inference language, and lifecycle/maturity state. Candidate packages cannot claim accepted lifecycle state.

### Knowledge Object

Checks promotion requirements, validation history, evidence integrity, lineage continuity, maturity state, package consistency, and prevention of production-governed maturity overclaim in this pre-production slice.

### Knowledge Change

Checks change justification, previous/new package references, version lineage, fingerprint evolution, evidence/method deltas, contradiction/uncertainty deltas, validation result, and transition reproducibility.

## Finding categories

Framework findings use the consolidation taxonomy categories:

- `constitutional_boundary`
- `evidence_contract`
- `provenance`
- `reproducibility`
- `unsupported_inference`
- `package_schema`
- `lineage_fingerprint`
- `maturity_state`

All implemented v1 findings are blockers because this slice proves rejection behavior before production.

## CLI usage

```bash
python3 tools/validate_knowledge_pipeline_v1.py tests/fixtures/validation_framework_v1/positive_candidate.json
```

The command prints a JSON report and exits 0 on pass, 1 on blockers.
