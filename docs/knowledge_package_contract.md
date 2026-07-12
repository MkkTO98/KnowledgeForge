# Knowledge Candidate and Package Contract Specification

Date: 2026-07-09
Status: architecture specification; implementation not authorized

## 1. Purpose

A KnowledgeForge package is a reproducible, provenance-bearing bundle that contains candidate or durable knowledge statements plus the evidence, methods, validation state, contradictions, and evolution metadata required to audit or regenerate them.

This is a conceptual contract, not a database schema.

## 2. Package kinds

| Package kind | Purpose | Accepted as durable knowledge? |
| --- | --- | --- |
| KnowledgeCandidatePackage | Holds proposed statements before full validation/review. | No. |
| KnowledgeObjectPackage | Holds one or more accepted or supported durable knowledge objects/revisions. | Yes if validation and governance gates pass. |
| KnowledgeChangePackage | Holds a coherent governed change across one or more objects. | Yes as audit/evolution record. |
| EvidenceEvaluationPackage | Holds reusable evaluations of evidence against claims or candidate statements. | Yes if scoped and validated. |
| GeneratedIntermediatePackage | Holds parsed/extracted/model-assisted intermediate material. | No direct acceptance; supports candidates only. |

## 3. Required structure

Every package must include these sections.

### 3.1 Package identity

- `package_id`: stable package identifier.
- `package_kind`: candidate, object, change, evaluation, or intermediate.
- `package_version`: version of the package contract.
- `created_at`: timestamp or date.
- `created_by`: human, tool, or process.
- `status`: draft, candidate, validated, blocked, accepted, rejected, deprecated, archived.
- `scope`: domain, evidence family, source scope, method scope, and intended use.

### 3.2 Input references

- source package/export/snapshot/query references where applicable.
- Source documentation references.
- Manual evidence references.
- Prior KnowledgeForge object/revision references.
- Template/prompt references.
- Model references if a model was used.
- Generated intermediate references.

### 3.3 Evidence references

Each evidence reference must include:

- `evidence_ref_id`;
- evidence class and source family;
- source owner/system;
- source identity/version/vintage/access date;
- snapshot/fingerprint when available;
- reproducibility handle;
- license/access constraints if relevant;
- evaluation status.

### 3.4 Computation method

- method name and version;
- deterministic algorithm or computation recipe;
- parameters;
- query definitions;
- data filters/window/frequency/units;
- transformation steps;
- software/tool versions when material;
- random seeds or nondeterminism declaration;
- rerun instructions or replay command when available.

### 3.5 Generated statements

Each generated statement must include:

- statement identifier;
- statement text or structured content;
- statement type: factual, derived, statistical characterization, classification, evidence evaluation, methodological, negative, candidate;
- claim facets if claim-like;
- applicability/scope;
- dependencies;
- supporting/weakening/contradicting evidence references;
- whether statement is generated, preserved from source, or deterministically derived.

### 3.6 Confidence and quality metadata

- confidence label or quality state;
- uncertainty dimensions;
- missingness summary;
- evidence sufficiency summary;
- reproducibility state;
- validation state;
- governance/review state;
- lifecycle state when promoted to durable object.

Do not confuse confidence, lifecycle, and governance. A reviewed package can be low confidence; a candidate can be high apparent confidence but unaccepted.

### 3.7 Contradiction records

- contradiction identifier;
- target statement/object;
- contradicting evidence or object;
- contradiction type;
- scope/method differences;
- disposition: unresolved, resolved by scope, accepted competing claim, blocks acceptance, requires review, or deprecated.

### 3.8 Provenance envelope

The package must embed or reference the provenance envelope defined in `docs/provenance_fingerprinting.md`.

### 3.9 Fingerprint

The package must include fingerprints for:

- input set;
- evidence references/snapshots;
- query definitions;
- computation recipe;
- prompts/templates if used;
- model identifiers if used;
- generated statements;
- package manifest.

### 3.10 Validation state

- validator version;
- validation timestamp;
- validation result: pass, warnings, blocked;
- blocker list;
- advisory warning list;
- intentionally deferred checks;
- human review requirement.

### 3.11 Version and evolution metadata

- previous package/object revision;
- supersedes/superseded-by links;
- change reason;
- changed inputs/methods/templates/models/validators;
- migration/compatibility note;
- dependent object review posture.

## 4. Minimal package acceptance gate

A package cannot become accepted durable knowledge unless:

1. evidence references are explicit;
2. provenance envelope is complete for the package kind;
3. computation method or source-preservation method is explicit;
4. generated statements have scope and dependencies;
5. contradiction handling is present or explicitly not applicable;
6. required fingerprints are present;
7. deterministic validators pass without blockers;
8. governance/review state is recorded.

## 5. Package anti-patterns

Reject or block packages that:

- contain LLM-generated statements without upstream evidence;
- merge evidence references and evidence evaluations into one opaque field;
- omit query/method/template/model versions;
- treat downstream usage as truth evidence;
- include insight, forecast, or recommendation language;
- contain observational datasets as owned KnowledgeForge data rather than references/snapshots;
- cannot be audited because intermediate outputs were discarded.
