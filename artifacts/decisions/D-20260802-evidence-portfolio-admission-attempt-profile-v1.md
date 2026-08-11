# D-20260802 — Use a distinct Evidence Portfolio admission-attempt profile

Status: accepted for the current unpublished corrective candidate
Date: 2026-08-02
Decision identity: `knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`

## Context

Published `knowledgeforge.evidence_portfolio.conformance.v1@1.0` is an immutable historical analytical adaptation profile. It requires full-manifest outcomes, one package per executable manifest entry, exact view coverage, governed question/conclusion binding and dependence declarations.

The live owner `tools/evidence_portfolio_production.py:run_portfolio()` coordinates both canary and production attempts. Isolated execution proved that a successful canary canonically admits one package from an evaluated subset of the complete authoritative manifest, while null and failed executable outcomes are recorded rejections with no persistence and preregistered exclusions remain pre-execution rejections.

## Decision

Add the distinct operational profile:

`knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`

Use it as the exact pinned pre-persistence subject at the existing owner. It binds complete manifest identity and identity kind, mode, evaluated and unevaluated scopes, outcomes and explicit result fingerprints, reruns, blockers, proposed packages, proposed views, derived admission decision and deterministic fingerprint. Exact package identities are independently supplied by the owner from manifest candidates at dispatch.

A structurally valid rejected attempt is not a successful admission. Only a freshly validated envelope whose response has exact `valid is true`, exact Boolean `admission_authorized`, exact `admit`/`reject`, and complete agreement with the owner's independently derived decision may pass its exact bound package set to lower-level persistence. Truthy coercion is not authorization.

Published conformance v1 remains byte-for-byte unchanged. This is not `conformance.v2` because historical analytical adaptation and live operational admission attempt are different subjects and lifecycle moments.

## Rejected alternatives

1. Integrate conformance v1 directly: rejected because it cannot represent the real admitted canary subject.
2. Treat canary as non-admitting evaluation: rejected by the actual persistence call, `isolated_canary_admitted` record and production pre-state binding.
3. Make negative attempts conforming admitted portfolios: rejected because current gates call persistence zero times for executable null and failure.
4. Modify conformance v1 in place: rejected by publication immutability and changed subject semantics.
5. Create `conformance.v2`: rejected because version succession would imply a broader version of the same historical analytical subject.
6. Move enforcement to `persist_packages()` or the generic Knowledge Repository writer: rejected because those primitives lack the complete run subject.
7. Redesign the owner for whole-portfolio transactional persistence: rejected as outside this bounded correction; current semantic decision ordering is unambiguous, while crash-atomicity remains an explicit limitation.

## Consequences

- Every supported Evidence Portfolio path inherits one owner-local exact dispatch.
- Conformance occurs after package/view proposal construction and before the first canonical write.
- Rejection leaves canonical state unchanged.
- Canary admission remains explicit partial-scope package admission; unevaluated candidates receive no invented outcomes.
- Historical Norway and Sweden artifacts are not migrated and do not retroactively claim the new profile.
- CLI/file-backed calls bind one decoded byte string and its hash; direct calls bind deterministic canonical in-memory bytes and cannot claim an external hash.
- Only owner-emitted outcome/stage transitions are valid; invented runtime rejection, execution or post-execution transitions fail closed.
- Any owner/profile authorization disagreement raises before persistence or attempt-record output.
- Owner and compliant lower-level writers serialize on one repository-adjacent lock; public helpers always acquire it and expose no caller-asserted bypass, while the owner uses private locked implementations only while already holding the lock.
- Admission authenticates repository state before execution, rechecks and binds it under the lock before persistence, and fully authenticates the resulting repository.
- Authorization requires complete independently owner-derived package, result and view identity populations; cross-population semantics use canonical typed-JSON equality.
- Output/repository roots are disjoint in both ancestor directions, and symlink, type, hard-link, inode-collision, write-mode and non-truncating write-open defects are preflighted before calculation or canonical mutation.
- A profile pass proves structural/fingerprint consistency and correct decision derivation, not source truth, whole-portfolio crash atomicity, publication, projection or universal generality.
