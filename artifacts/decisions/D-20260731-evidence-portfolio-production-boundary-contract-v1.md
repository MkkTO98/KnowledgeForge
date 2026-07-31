# D-20260731 — Evidence Portfolio Production Boundary Contract v1

Date: 2026-07-31
Status: Accepted, implementation-authorized and validation-authorized for the first unpublished Evidence Portfolio pilot; not publication-authorized
Decision class: bounded production operating-procedure authorization and audit-attestation correction
Normative specification: `docs/evidence_portfolio_production_boundary_contract_v1.md`

## Decision

KnowledgeForge accepts `knowledgeforge.evidence_portfolio.production_boundary.v1@1.0` with two distinct coordinated subcontracts:

1. `knowledgeforge.evidence_portfolio.production_authorization.v1@1.0` binds a successful canary to one exact campaign, execution-manifest byte identity, manifest semantic identity, ordered candidate/input population, complete limits, canary accounting, exact deterministic-rerun rows, blocker state, isolated admission disposition and exact canary-admitted repository pre-state before a bounded production wave can read evidence, calculate or mutate canonical state.
2. `knowledgeforge.architecture_reality.audit_subject_manifest.v1@1.0` freezes an exact substantive candidate and permits an acyclic audit → report-summary → final-publication-manifest attestation chain.

Authorization and audit attestation remain different evidence and authority classes. Neither authorizes Git publication.

## Rationale

Independent pre-publication review reproduced generic-truthiness authorization, missing campaign/manifest/population binding, unenforced normative budgets, repository-root path escape, audit predecessor self-selection, unstable candidate scope and stale reports-summary generation. The prior contracts contained the production intent but lacked the narrow executable gate and acyclic durable-attestation procedure required to prove it.

The accepted correction is deterministic and repository-local. It requires neither digital signatures nor a service, secret, authentication system or new canonical ontology.

## Compatibility and migration

The legacy canary gate remains historical execution evidence and is explicitly non-authoritative under v1. It is not rewritten or represented as retroactive v1 authorization.

The unpublished pilot must be validated by reconstructing the exact 560-package state, issuing a fresh v1 canary authorization for the unchanged campaign/manifest/candidates/inputs/limits, replaying the same wave in disposable storage, and comparing the resulting 562-package state with the retained candidate.

The replay does not create another portfolio, campaign or knowledge claim. Historical calculation artifacts remain immutable.

## Explicitly unchanged

This decision does not change canonical Knowledge Object schemas, package fingerprints, repository fingerprint semantics, Campaign 43 analytical identity, Production Doctrine, PostgreSQL projection schema, Evidence-Card-equivalent view status, provider admission or KnowledgeForge's independence from MacroForge.

## Scope and authority

Authorized now:

- contract documentation and this decision;
- strict production-gate implementation;
- normative budget enforcement;
- manifest path containment;
- audit-subject manifest and final-candidate verification support;
- audit predecessor correction;
- isolated v1 replay and validation;
- correction of the unpublished prospective publication candidate.

Not authorized:

- staging, commit, push or publication;
- another Evidence Portfolio or Sweden Infrastructure work;
- new evidence, campaign or knowledge claim;
- canonical schema, projection schema or Campaign 43 reinterpretation;
- persistent/default PostgreSQL mutation.
