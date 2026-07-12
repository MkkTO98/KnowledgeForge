# KnowledgeForge Knowledge Acceptance Criteria

Status: authoritative architectural standard
Date: 2026-07-09
Scope: KnowledgeForge-owned knowledge objects and package promotion decisions

## Purpose

This document defines what qualifies as a valid KnowledgeForge knowledge object.

KnowledgeForge answers: "What is known?" It does not answer what should be done, what will happen, what a situation means for investors or policy makers, or how knowledge should be presented to an audience.

A KnowledgeForge knowledge object is acceptable only when it is reusable, evidence-backed, provenance-bearing, reproducible, validation-gated, lifecycle-scoped, and constitutionally permitted.

## Universal acceptance criteria

Every accepted KnowledgeForge knowledge object must satisfy all criteria below.

1. Stable identity
   - Has a durable package/object identifier.
   - Has version and lineage metadata.
   - Can be referenced without depending on a representation format.

2. Evidence grounding
   - References evidence through KnowledgeForge-owned EvidenceReference structures.
   - Does not embed or duplicate external observational datasets as owned KnowledgeForge data.
   - Distinguishes source evidence from KnowledgeForge evidence evaluation.

3. Provenance
   - Includes a ProvenanceEnvelope identifying inputs, methods, templates, validators, review state, and source evidence references.
   - Retains enough information to audit why the object exists.

4. Reproducibility
   - Includes fingerprints for input set, evidence references, selection/query definitions where applicable, computation recipe, generated statements, and package manifest.
   - Can be reconstructed from retained immutable source evidence packages or explicit references.
   - Contains no hidden model, time, network, database, or repository dependency unless explicitly represented as evidence and accepted by governance.

5. Validation
   - Passes deterministic stage validation.
   - Records validation result, validator version, blockers, warnings, and review requirement.
   - Does not rely on an LLM as acceptance authority.

6. Constitutional boundary
   - Contains no interpretation, hypotheses, forecasts, causal claims, recommendations, presentation narrative, investment meaning, policy meaning, or action selection.
   - Does not create dependency on another repository, shared runtime interface, shared schema, adapter, API, database, or shared codebase.

7. Lifecycle and governance
   - Separates lifecycle state from truth state.
   - Separates governance/review state from confidence.
   - States applicability, scope, limitations, uncertainty, and contradiction posture.

## Supported knowledge categories

### 1. Factual knowledge

Definition: A scoped statement that preserves or summarizes factual content from accepted evidence without adding interpretation.

Accepted examples:

- "The source evidence package records complete coverage for the specified fixture scope."
- "The retained source snapshot identifies the indicator family as age-sex cohort coverage."
- "The package contains one source snapshot, one evidence reference, and one validation result."

Rejected examples:

- "The country is economically attractive because coverage is complete."
- "This means demographic quality is strong."
- "Investors should prefer this country."

Reason: rejected examples add interpretation, investment meaning, or recommendation.

### 2. Derived knowledge

Definition: A deterministic computation from accepted evidence using an explicit method.

Accepted examples:

- "Coverage completeness equals observed required fields divided by required fields under method M."
- "The fixture has zero missing required evidence fields under validator v1."

Rejected examples:

- "The complete coverage causes better economic outcomes."
- "The derived trend implies future growth."

Reason: rejected examples add causality or forecasting.

### 3. Classified knowledge

Definition: A deterministic or governed classification under an explicit vocabulary.

Accepted examples:

- "This statement is classified as factual knowledge."
- "This evidence is classified as a SourceEvidencePackage."
- "This package belongs to the coverage knowledge family."

Rejected examples:

- "This classification proves the source is reliable for all future uses."
- "This country is high quality."

Reason: rejected examples overclaim beyond the classification rule.

### 4. Methodological knowledge

Definition: Knowledge about methods, validation rules, construction procedures, reproducibility, or limitations.

Accepted examples:

- "The construction method uses canonical JSON and SHA-256 fingerprints."
- "The validation slice rejects unsupported inference language before object promotion."

Rejected examples:

- "This methodology should be used for investment decisions."
- "This method forecasts demographic change."

Reason: rejected examples turn method description into recommendation or prediction.

### 5. Evidence-quality knowledge

Definition: Knowledge about evidence completeness, validity, freshness, lineage, uncertainty, contradiction posture, or auditability.

Accepted examples:

- "The source package includes provenance and reproducibility metadata."
- "The evidence evaluation records no contradiction inside the fixture scope."

Rejected examples:

- "High evidence quality means the situation is bullish."
- "Coverage quality implies policy success."

Reason: rejected examples add investment or policy meaning.

### 6. Coverage and missingness knowledge

Definition: Knowledge about what evidence is present, absent, scoped, excluded, or unsupported.

Accepted examples:

- "The fixture scope contains one territory and one period."
- "No missingness is declared for the fixture scope."
- "The package does not support claims outside the fixture scope."

Rejected examples:

- "Complete coverage proves the source captures the full economy."
- "Missing data means a country is weak."

Reason: rejected examples overgeneralize or interpret.

### 7. Negative knowledge

Definition: Explicitly retained knowledge about unsupported claims, failed validation, missing evidence, rejected mappings, contradictions, or out-of-scope uses.

Accepted examples:

- "The package does not support forecasts."
- "The package does not support causal claims."
- "The package is invalid when provenance is missing."

Rejected examples:

- "Because forecasts are unsupported, the future outcome is unknowable."
- "Because policy claims are rejected, no policy conclusion is possible."

Reason: rejected examples turn negative knowledge into broad interpretation.

### 8. Provenance knowledge

Definition: Knowledge about source identity, retained snapshots, fingerprints, validation history, lineage, and construction method.

Accepted examples:

- "The package manifest fingerprint is SHA-256 over canonical package content."
- "The object was promoted from candidate package X after deterministic validation."

Rejected examples:

- "This lineage makes the claim true."
- "This provenance is sufficient for production in every domain."

Reason: provenance supports auditability, not truth overclaim or universal scope.

## Ambiguous cases

### Descriptive trend language

Example: "The series increased over the selected period."

Decision: defer unless a deterministic trend descriptor method, window policy, missingness policy, and boundary-language validator are approved.

Reason: trend language can remain descriptive, but it often drifts into interpretation or forecasting.

### Rankings and comparisons

Example: "Country A has higher coverage than Country B."

Decision: defer unless a comparison/ranking package contract defines scope, denominator, tie handling, missingness, and vocabulary.

Reason: comparisons are deterministic but can easily become evaluative or decision-oriented.

### Source reliability language

Example: "The source is reliable."

Decision: reject in this generic form.

Acceptable replacement: "The evidence evaluation found required provenance and reproducibility fields present for this fixture scope."

Reason: reliability is too broad unless decomposed into explicit evidence-quality dimensions.

### Causal mechanism language

Example: "Coverage completeness causes better demographic analysis."

Decision: reject.

Reason: causality is outside current KnowledgeForge acceptance scope unless a future causal-evidence contract is explicitly approved.

### Policy or investment implications

Example: "This supports a policy intervention" or "investors should monitor this."

Decision: reject.

Reason: KnowledgeForge does not own recommendation, policy meaning, investment meaning, or action selection.

## Promotion criteria from candidate to object

A KnowledgeCandidatePackage may become a KnowledgeObjectPackage only when:

1. the source evidence package validates;
2. Evidence validates independently;
3. Evidence Evaluation validates independently;
4. KnowledgeCandidatePackage validates independently;
5. boundary verification passes;
6. package fingerprints are recomputed and stable across replay;
7. lineage from candidate to object is explicit;
8. evidence integrity verifies references and fingerprints;
9. lifecycle state remains scoped and does not claim absolute truth;
10. governance/review state is recorded.

## Rejection triggers

A candidate or object must be rejected or blocked if it contains:

- malformed evidence;
- missing provenance;
- invalid or unrecomputable fingerprints;
- unsupported inference language;
- constitutional boundary violations;
- incomplete package construction;
- invalid lifecycle or maturity state;
- broken reproducibility;
- interpretation;
- hypotheses;
- forecasts;
- causal claims;
- recommendations;
- presentation narrative;
- investment meaning;
- policy meaning;
- hidden runtime/database/repository dependencies.

## Production-campaign use

Before any production campaign, this acceptance standard must be used as the minimum object-promotion gate. A production campaign may narrow the accepted categories further, but it must not weaken these criteria.
