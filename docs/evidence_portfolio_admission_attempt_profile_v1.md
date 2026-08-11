# Evidence Portfolio Admission-Attempt Profile v1

Status: implemented in unpublished corrective candidate
Profile identity: `knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`
Schema name: `knowledgeforge.evidence_portfolio.admission_attempt.v1`
Schema version: `1.0`
Date: 2026-08-02

## Purpose

This profile governs one live operational Evidence Portfolio admission attempt immediately before the existing owner may call canonical package persistence. It is distinct from published `knowledgeforge.evidence_portfolio.conformance.v1@1.0`, which remains an immutable historical analytical adaptation profile.

A profile-valid attempt is not necessarily an admitted run. The validator independently returns `admission_authorized`; only `true` authorizes persistence. Null and failed executable attempts, plus preregistered pre-execution exclusions, can be represented and authenticated while remaining non-admissions.

## Exact subject

The envelope binds:

- the complete authoritative manifest and its semantic fingerprint;
- the invocation's exact manifest-byte fingerprint and identity kind: `file_bytes` or `canonical_in_memory_bytes`;
- run mode: `canary` or `production`;
- evaluated candidate IDs in authoritative manifest order;
- unevaluated candidate IDs in authoritative manifest order;
- one outcome for every and only evaluated candidate;
- one normalized deterministic rerun binding for every and only evaluated executable candidate;
- owner-derived blockers;
- proposal state: `constructed` or `withheld`;
- proposed packages and package fingerprints;
- explicit fingerprints for every outcome;
- proposed operational views and view fingerprints;
- mechanically derived decision: `admit` or `reject`;
- deterministic attempt fingerprint.

Elapsed wall-clock telemetry is deliberately excluded from rerun identity. The owner's limit decision is retained through deterministic blocker text; volatile timing cannot make identical semantic attempts fingerprint-different.

## Scope rules

Canary mode selects every manifest entry whose literal `canary` field is true. Entries not selected remain explicit in `unevaluated_candidate_ids` and receive no invented outcome, rerun, package or view.

Production mode selects all manifest entries and therefore has an empty unevaluated population.

A preregistered exclusion must be `rejected` at `pre_execution` and cannot carry result records. The owner-emitted executable transitions are exactly:

- `valid`, with exactly 28 result records and no stage;
- `failed` at `input_validation`;
- `null` at `calculation`;
- `failed` at `calculation`.

Runtime `rejected`, `execution` and `post_execution_validation` transitions are not emitted by the current owner. The profile rejects them rather than admitting invented future behavior.

## Proposal and decision rules

A constructed proposal contains packages for every and only valid evaluated executable outcome, in evaluated order. Each package must:

- pass the canonical Knowledge Object package validator;
- bind the exact manifest fingerprint;
- match the complete owner-derived package-identity population for evaluated executable candidates;
- bind exact candidate scope, inputs, method, evidence, provenance and result lineage from its manifest entry;
- bind result records byte-for-byte to its outcome;
- carry a deterministic package fingerprint.

Operational views must cover package result records exactly and in package/result order. Each view must bind its package ID, result ID, class, metric and value and must authenticate its own fingerprint.

A withheld proposal contains no packages, views or related fingerprints. This is the owner's state when an early blocker prevents proposal construction.

`admit` is derived only when:

- blockers are empty;
- every evaluated executable outcome is valid;
- deterministic reruns match;
- canary has exactly one valid executable package and 28 views; or
- production has exactly two valid executable packages and 56 views;
- the proposal is constructed and semantically valid.

Every other structurally authenticated attempt derives `reject`. A caller cannot set or spoof `admit`.

## Dispatch

The only accepted identity is:

`knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`

The dispatcher rejects omission, schema-only identity, alias, `latest`, ranges, unsupported versions and unknown profiles. There is no fallback, discovery mechanism, compatibility inference or silent upgrade.

The owner constructs and validates the current envelope itself. It accepts no caller-supplied validation result or caller-claimed manifest hash. File-backed calls hash the same bytes they decode; direct calls are explicitly bound to deterministic canonical in-memory bytes. It persists the exact package objects copied into the freshly validated envelope. The validator response must have exact `valid is true`, exact Boolean `admission_authorized`, exact `admit`/`reject`, and agreement with the owner's independently derived decision; truthy coercion is forbidden. Any owner/profile authorization disagreement raises as an internal contradiction before persistence or attempt-record output.

## Mutation boundary

Owner ordering is:

manifest/authentication → output-destination preflight → authenticated repository pre-state → deterministic evaluation → blockers → package/view proposal → repository reauthentication → admission-attempt build and validation → canonical persistence → complete repository post-authentication.

The owner and compliant lower-level writers use one repository-adjacent lock. Public persistence APIs always acquire it and expose no caller-asserted bypass; the already-locked owner alone uses private locked implementations. Admission persistence binds the exact authenticated pre-state again under that lock. Authorization requires complete owner-derived package, result and view identity populations, and cross-population semantic bindings use canonical typed-JSON equality. Output and repository roots must be fully disjoint in both ancestor directions, and every required output target is preflighted for symlink/type safety, single-link/inode uniqueness, write-mode presence and a non-truncating write-open before calculation or mutation.

A validation exception or derived rejection occurs before the first persistence call. Rejected attempts may be recorded outside canonical package storage. Lower-level `persist_packages()` and `knowledge_repository.persist_knowledge_object_packages()` remain package-persistence primitives, not admission-attempt APIs. Per-file atomic replacement still does not provide whole-portfolio crash atomicity.

## Compatibility

This profile does not modify, supersede, reinterpret or migrate:

- `knowledgeforge.evidence_portfolio.conformance.v1@1.0`;
- historical Norway Health artifacts;
- historical Sweden Infrastructure artifacts;
- canonical Knowledge Object schema v1;
- existing repository or PostgreSQL state.

Historical Norway and Sweden conformance proofs show two concrete historical adaptations. They do not prove universal generality and they do not claim that those historical runs used this live profile.

## Limits

A pass proves deterministic structural and fingerprint consistency, exact scope reconciliation, package/outcome/view lineage and correct admission classification for this owner. It does not prove source truth, external authenticity, analytical usefulness, independence, causal meaning, future reproducibility, whole-portfolio crash-transactional persistence, Git publication, database projection or authorization for another portfolio.
