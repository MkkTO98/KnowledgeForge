# D-20260712 Next Production Readiness Before Campaign 43

Date: 2026-07-12
Status: accepted

## Decision

Select path A: expand first-difference Pearson companions.

This decision does not authorize Campaign 43 execution, coefficient calculation, package publication, PostgreSQL mutation, schema change, doctrine amendment, or export redesign.

## Basis

- Relationship Export Contract v1 can retrieve raw and first-difference relationships separately.
- Independent consumer simulation passed for raw method, first-difference method, first-difference transformation, and all-relationship discovery queries without package IDs or campaign numbers.
- Exported records expose method, transformation, source package identity/fingerprint, provenance, temporal scope, frequency, entity, series metadata, coefficient, limitations, and lifecycle state.
- Corrected raw Pearson policy leaves only four additional raw candidates in the retained pool; all were previously classified as high time-risk and insufficient as a useful raw registry before first-difference validation.
- Campaign 41 recorded high shared-time-trend risk for its raw outputs. Campaign 42 produced companions for two SWE Campaign 41 relationships; six specific Campaign 41 high-risk raw relationships remain without companion treatment.

## Rejected alternatives

B. Resume raw Pearson candidate production is rejected for the next immediate task because the corrected candidate pool is small and high-risk, while higher-value robustness knowledge remains available for already-canonical high-risk relationships.

C. Pause production for retrieval/export improvements is rejected because adversarial export and consumer checks did not show a retrieval/export blocker. Broader query/API/schema work would be premature.

## Architecture classification

Bounded sequencing decision inside existing architecture. No Production Doctrine amendment, KnowledgeObjectPackage redesign, PostgreSQL schema expansion, Relationship Export Contract redesign, broad transformation framework, generalized query platform, or cross-project dependency is required or authorized.

## Consequence

The smallest next task is a coefficient-free Campaign 43 first-difference companion registry freeze for the six remaining Campaign 41 high-shared-time-trend raw Pearson relationships, stopping before calculation/publication.

## Resume closeout verification

Interrupted closeout was resumed and re-verified under current `HEAD` / `origin/main` `78b29b5b7ffb92a7a065e36d520ab4d51ff93a5e`. Path A remains accepted. The re-check used the repository-supported `python3 -m unittest` path rather than unsupported pytest/uv pytest execution; pytest is not installed for `/usr/bin/python3` and the repository declares no pytest/uv dependency environment. Canonical state remained 554 packages with fingerprint `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`; no packages or PostgreSQL production state were mutated. Detailed evidence: `artifacts/reports/next-production-readiness-decision-20260712/final_verification/resume_closeout_20260712.json`.
