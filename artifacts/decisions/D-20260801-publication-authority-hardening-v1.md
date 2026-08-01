# D-20260801 — Publication Authority Hardening v1

Date: 2026-08-01
Status: Accepted for repository-local implementation, validation and guarded unstaged candidate application; not Git-publication-authorized
Decision class: bounded governance implementation correction
Normative specification: `docs/evidence_portfolio_production_boundary_contract_v1.md`

## Decision

KnowledgeForge accepts one reusable, fail-closed publication-authority mechanism for reconciling complete/new candidate paths, mixed candidate representations and authority-only declarations against an authenticated parent Git tree before any future staging operation.

The mechanism must:

1. derive parent identity and delta from the exact Git object database with replacement refs disabled;
2. bind exact source-manifest bytes, path populations, modes, sizes and SHA-256 identities;
3. classify parent-identical paths separately from real changes;
4. require an active, self-valid authority document and canonical registry with explicit predecessor/supersession history;
5. retain one authorized changed durable report carrying semantic continuity markers and an explicit external verification-evidence locator;
6. verify current source roots again when constructing and verifying a staging gate;
7. emit only a deterministic staging plan; it does not stage, commit or publish.

## Rationale

The previous portfolio-specific publication evidence described correct candidate intent but did not provide one generic executable authority that could reconcile complete, mixed and authority-only populations, derive a trustworthy parent delta, reject stale or rolled-back authority, and prove exact staging scope. The smallest correction is a repository-local validator and CLI, not another portfolio/batching subsystem or a remote authority service.

## Compatibility

This decision does not change Knowledge Object, Evidence Bundle, Calculation Campaign, Evidence-Card view, lifecycle, promotion, repository-fingerprint or PostgreSQL projection semantics. Existing historical portfolio authority artifacts remain evidence of their own executions and are not retroactively rewritten.

## Operational boundary

The registry is a local operational control outside canonical Knowledge Objects. A gate authorizes an exact staging plan only while the authenticated parent and verified source representations remain frozen. The actual publication operator must stage from verified immutable descriptors or immediately reverify after staging; path replacement between verification and Git index insertion remains fail-closed operational work, not a capability silently claimed by this tool.

No staging, commit, push, tag, release or publication is authorized by this decision.
