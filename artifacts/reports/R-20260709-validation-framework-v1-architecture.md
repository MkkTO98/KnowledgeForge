# Validation Framework v1 Architecture Report

Date: 2026-07-09
Status: completed pre-production vertical slice

## Objective

Implement the first deterministic validation framework for KnowledgeForge, using only synthetic fixtures, to prove that assimilation consolidation contracts are enforceable before MacroForge data is processed.

## Implemented pipeline

```text
Evidence
  -> Evidence Evaluation
  -> Knowledge Candidate
  -> Knowledge Object
  -> Knowledge Change
```

Each stage has an independent validator in `tools/validate_knowledge_pipeline_v1.py`:

- `validate_evidence`
- `validate_evidence_evaluation`
- `validate_knowledge_candidate`
- `validate_knowledge_object`
- `validate_knowledge_change`

The validators return structured JSON-like reports with:

- `ok`
- `stage`
- `validator_version`
- `blockers`
- `warnings`

## Architectural contracts enforced

### Evidence validation

Enforces required metadata, source identity, provenance references, fingerprint presence, evidence classification, and reproducibility handle/state. Blocks LLM-generated text as direct evidence.

### Evidence Evaluation validation

Enforces evidence/evaluation separation, required evaluation dimensions, uncertainty, contradiction records, provenance/fingerprints, and forbidden interpretation-language blocking.

### Knowledge Candidate validation

Enforces package schema, evidence references, provenance envelope, required fingerprints, confidence metadata, generated statement structure, unsupported inference blocking, and candidate lifecycle boundaries.

### Knowledge Object validation

Enforces object promotion requirements, validation history, evidence integrity, lineage continuity, maturity state, and package consistency. Blocks production-governed maturity overclaims.

### Knowledge Change validation

Enforces change report identity, trigger/change justification, previous/new package references, version lineage, evidence/method deltas, fingerprint evolution, validation result, and reproducibility of transition.

## Explicit exclusions preserved

This slice did not:

- access PostgreSQL;
- process MacroForge production data;
- produce production knowledge;
- execute local models;
- execute frontier LLM workflows;
- create schemas, databases, APIs, schedulers, daemons, vector stores, dashboards, or UI infrastructure;
- expand KnowledgeForge into InsightForge.

## RED/GREEN evidence

RED command:

```bash
python3 -m unittest tests.test_validation_framework_v1 -v
```

RED result: failed with `FileNotFoundError` for missing `tools/validate_knowledge_pipeline_v1.py`, proving the tests targeted missing framework behavior.

GREEN command:

```bash
python3 -m unittest tests.test_validation_framework_v1 -v
```

GREEN result: 7 tests passed.

## Architectural assessment

The framework proves that the new contracts are enforceable on fixture-backed examples. It does not prove MacroForge compatibility, production readiness, calibrated confidence, complete ontology coverage, or replay from real upstream packages.
