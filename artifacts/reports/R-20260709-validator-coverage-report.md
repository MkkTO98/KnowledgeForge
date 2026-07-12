# Validator Coverage Report

Date: 2026-07-09
Status: completed

## Coverage summary

| Stage | Positive fixture | Negative cases | Validator |
| --- | --- | --- | --- |
| Evidence | `positive_evidence.json` | missing source identity, missing fingerprint, LLM direct evidence | `validate_evidence` |
| Evidence Evaluation | `positive_evidence_evaluation.json` | collapsed evidence/evaluation, forbidden interpretation, missing uncertainty | `validate_evidence_evaluation` |
| Knowledge Candidate | `positive_candidate.json` | unsupported inference, missing fingerprints, maturity overclaim | `validate_knowledge_candidate` |
| Knowledge Object | `positive_knowledge_object.json` | missing validation history, invalid lineage, production maturity overclaim | `validate_knowledge_object` |
| Knowledge Change | `positive_knowledge_change.json` | missing previous reference, missing fingerprint evolution, malformed version history | `validate_knowledge_change` |

## Contract coverage

Implemented checks cover:

- required metadata;
- source identity;
- provenance references;
- fingerprint presence;
- evidence classification;
- reproducibility requirements;
- evidence/evaluation separation;
- supported evidence-evaluation dimensions;
- uncertainty representation;
- contradiction recording;
- forbidden interpretation language;
- package schema;
- constitutional boundary compliance;
- evidence references;
- provenance envelope;
- confidence metadata;
- lifecycle state;
- promotion requirements;
- validation history;
- evidence integrity;
- lineage continuity;
- maturity state;
- package consistency;
- change justification fields;
- previous/new package references;
- version lineage;
- fingerprint evolution;
- reproducibility of transition.

## Finding categories exercised

- `constitutional_boundary`
- `evidence_contract`
- `provenance`
- `reproducibility`
- `unsupported_inference`
- `package_schema`
- `lineage_fingerprint`
- `maturity_state`

## Not yet covered

- Real MacroForge evidence handles.
- Real PostgreSQL query fingerprints.
- Real package-manifest hash recomputation.
- Cross-file fixture directories and dependency resolution across multiple package files.
- Calibrated confidence/uncertainty semantics.
- Complete governed vocabulary validation.
- Validator version migration across accepted package revisions.
- Revalidation of prior accepted packages after validator changes.
