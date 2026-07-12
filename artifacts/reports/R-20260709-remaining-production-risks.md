# Remaining Production Risks

Date: 2026-07-09
Status: completed

## Summary

The final pre-production construction validation slice removes the remaining architectural blocker to a first controlled production campaign. The remaining risks are production-operation risks, not reasons for another architecture campaign.

## Risks

### 1. Source Evidence Package selection risk

Risk: the first production Source Evidence Package may be too broad, include ambiguous evidence, or include source fields not covered by the final validation slice.

Mitigation:

- keep the first campaign narrow;
- use one source family;
- use descriptive evidence-quality and coverage packages only;
- require immutable package input and recomputed fingerprints before construction.

### 2. Scope creep into interpretation

Risk: production package wording may drift into interpretation, hypotheses, forecasts, causal claims, recommendations, policy meaning, or investment meaning.

Mitigation:

- apply `docs/knowledge_acceptance_criteria.md` as a mandatory gate;
- keep first campaign package themes factual/evidence-quality/coverage/provenance/negative only;
- reject or defer ambiguous trend/comparison language unless explicitly contracted.

### 3. Fingerprint drift

Risk: production construction may include timestamps, ordering differences, implicit environment state, or unpinned methods.

Mitigation:

- use canonical JSON fingerprints;
- fingerprint source package, method, generated statements, and package manifest;
- rerun construction and compare outputs before promotion.

### 4. Lifecycle overclaim

Risk: production packages may incorrectly claim absolute truth, broad maturity, or unrestricted reuse.

Mitigation:

- lifecycle state must remain scoped;
- governance state must remain distinct from confidence;
- validation must reject production-governed maturity overclaim in pre-production paths.

### 5. Operational closeout risk

Risk: production campaign may generate correct packages but fail to update task/state/handoff/report artifacts.

Mitigation:

- treat file-backed audit trail as part of the production campaign acceptance criteria;
- require construction report, validation report, package inventory, and handoff before campaign completion.

## Non-risks after this slice

The following are not remaining blockers for a first controlled production campaign:

- need for another architecture campaign;
- need for runtime infrastructure;
- need for APIs;
- need for database coupling;
- need for cross-repository adapters;
- need for local or frontier LLM execution;
- need for ontology redesign.

## Conclusion

Proceed to the first controlled production campaign with narrow scope and strict acceptance gates.
