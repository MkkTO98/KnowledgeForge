# Validation Framework v1 Fixture Catalogue

Date: 2026-07-09
Status: completed
Fixture root: `tests/fixtures/validation_framework_v1/`

## Positive fixtures

- `positive_evidence.json` — valid synthetic evidence reference.
- `positive_evidence_evaluation.json` — valid synthetic evidence evaluation.
- `positive_candidate.json` — valid synthetic KnowledgeCandidatePackage.
- `positive_knowledge_object.json` — valid synthetic promoted KnowledgeObjectPackage.
- `positive_knowledge_change.json` — valid synthetic Knowledge Change report.

## Negative evidence fixtures

- `negative_evidence_missing_source_identity.json` — violates source identity requirement.
- `negative_evidence_missing_fingerprint.json` — violates fingerprint/provenance requirement.
- `negative_evidence_llm_direct_evidence.json` — violates constitutional rule that LLM output cannot be direct evidence.

## Negative evidence evaluation fixtures

- `negative_evaluation_collapsed_evidence.json` — violates evidence/evaluation separation.
- `negative_evaluation_forbidden_interpretation.json` — crosses into interpretation/InsightForge language.
- `negative_evaluation_missing_uncertainty.json` — omits uncertainty representation.

## Negative candidate fixtures

- `negative_candidate_unsupported_inference.json` — generated statement crosses into interpretation/recommendation language.
- `negative_candidate_missing_fingerprints.json` — omits required package fingerprints.
- `negative_candidate_maturity_overclaim.json` — candidate claims accepted lifecycle state.

## Negative object fixtures

- `negative_object_missing_validation_history.json` — promotion lacks validation history.
- `negative_object_invalid_lineage.json` — object lineage points to a missing previous package.
- `negative_object_maturity_overclaim.json` — fixture claims production-governed maturity.

## Negative change fixtures

- `negative_change_missing_previous_ref.json` — change lacks previous package reference.
- `negative_change_missing_fingerprint_evolution.json` — change lacks fingerprint evolution.
- `negative_change_malformed_history.json` — version lineage omits previous package.

## Fixture policy

All fixtures are synthetic and non-production. They do not reference real PostgreSQL data, real MacroForge packages, local model output, or frontier LLM output.
