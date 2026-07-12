# D-20260712 Campaign 41 Pearson Production Accepted

Date: 2026-07-12
Status: accepted

## Decision
Accept Campaign 41 as a successful end-to-end Pearson production campaign using the existing Pearson v1 package architecture, existing canonical repository publication path, existing PostgreSQL full-rebuild projection, and Relationship Export Contract v1.

## Basis
- The authorized ready specification fingerprint matched the recorded readiness artifact.
- The frozen candidate-registry logical fingerprint remained `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`.
- Candidate identities/order and expected package IDs remained unchanged.
- Evidence paths and fingerprints resolved from retained validated fixtures.
- No coefficients or outcome-dependent fields were present in frozen inputs.
- The generic engine contained no Campaign 41-specific runtime branch.
- All eight coefficients independently recomputed exactly to canonical precision.
- Time-index diagnostics were exposed through existing package payload/export structures without promoting them as separate Knowledge Objects.
- Pre-existing canonical package bytes remained unchanged; publication was append-only.
- PostgreSQL full rebuild verified payload/fingerprint fidelity and repository-fingerprint agreement.
- Consumer-neutral export/simulation verified retrieval without private table access, runtime import, coefficient recomputation, or campaign-report dependency.

## Architectural classification
This is operational production within existing architecture. It does not amend Production Doctrine, redesign KnowledgeObjectPackage, expand PostgreSQL schema, introduce a new methodology, or require a Doctrine Review Trigger.

## Consequences
- Canonical object count increased from 538 to 546.
- Pearson-object count increased from 13 to 21.
- Statistical-summary count remained 4.
- Repository fingerprint became `sha256:c89c25ede69ec88a12f4791dba94b6199f2927721d0028420a65a74dd6ee735c`.
- PostgreSQL projection was rebuilt to 546 objects.

## Follow-up
Smallest next task: Campaign 41 post-publication repository assimilation closeout. Inspect whether accepted Campaign 41 relationship packages require only documentation/index summary updates for downstream discovery, then stop before any new campaign or methodology work.
