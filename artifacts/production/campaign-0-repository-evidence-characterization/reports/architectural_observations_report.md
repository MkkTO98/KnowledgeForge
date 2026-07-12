# Architectural Observations Report

## Observed behavior

- Every accepted object passed deterministic construction and stage validation.
- Rejected objects were preserved and not promoted.
- Fingerprints remained stable across replay.
- No additional metadata field was required to complete Campaign 0.
- Existing validators were restrictive enough to catch malformed provenance and forbidden boundary language.
- Existing validators were not too restrictive for repository/evidence-level factual, coverage, methodological, provenance, and negative knowledge.

## Evidence-backed improvements

- Introduce a production-specific maturity vocabulary only if repeated campaigns show confusion from pre-production internal wording.
- Defer repository-wide duplicate registry until repeated production campaigns demonstrate cross-campaign duplicate pressure.

## Recommendation basis

Campaign 0 supports moving to the narrowest domain-specific deterministic campaign. It does not support broad architecture redesign.
