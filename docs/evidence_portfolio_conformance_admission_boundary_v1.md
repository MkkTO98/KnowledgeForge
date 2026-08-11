# Evidence Portfolio Admission Boundary and Admission-Attempt Profile v1

Status: implemented in the unpublished admission-boundary candidate; lifecycle authority is the task and closeout report
Contract identity: `knowledgeforge.evidence_portfolio.admission_boundary.v1@1.0`
Required operational profile: `knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`
Historical adaptation profile retained unchanged: `knowledgeforge.evidence_portfolio.conformance.v1@1.0`
Date: 2026-08-02

## 1. Correction history

The first frozen draft correctly located the operational owner at `tools/evidence_portfolio_production.py:run_portfolio()` and correctly proved that the published historical conformance profile cannot represent the owner's canary surface or package-less runtime outcomes. Its final interpretation was incomplete: it treated every owner result as though it had to be a conforming admitted portfolio and proposed a successor conformance profile without first separating an admission attempt from successful admission.

This correction retains that evidence and changes its interpretation where the code and isolated execution require it:

1. `run_portfolio()` is an invocation and admission-attempt coordinator, not proof that every returned or recorded result is admitted.
2. Null and failed executable outcomes are rejected attempts. Preregistered exclusions are rejected before execution. They are recorded diagnostics and never become admitted packages under the current valid-count gates.
3. A successful canary is not merely a read-only evaluation. The owner calls `persist_packages()`, records `isolated_canary_admitted`, and binds production authorization to the resulting repository state. It canonically admits one package from an explicitly evaluated subset of the complete authoritative manifest.
4. Therefore the incompatibility was not purely a category error. The published historical adaptation profile still cannot describe the real live admission subject, but package-less negative attempts do not themselves need to pass as successful admissions.
5. The required additive artifact is a distinct admission-attempt profile, not an in-place change to published v1 and not a `conformance.v2` successor. Historical analytical adaptation and operational admission attempts are different subjects.
6. Fresh adversarial review of the first implementation found five substantive contract gaps: package identity was not independently tied to the manifest candidate; a direct caller could claim arbitrary manifest bytes; the negative-stage matrix exceeded the owner's actual state machine; explicit result fingerprints were missing; and a clean validator rejection could be converted into a contradictory resealed rejection. The implementation and this contract now correct all five. Exact package identities are owner-derived, file-backed identity hashes the same bytes it decodes, in-memory identity is explicitly classified, only owner-emitted stage transitions are accepted, result fingerprints are explicit, and owner/validator decision disagreement raises before any record or persistence.
7. The next independent review found typed-identity, authorization-context, repository-authentication, output-containment and shared-writer gaps. The corrected owner compares canonical JSON rather than coercive Python equality, requires a complete owner-derived package-identity map for authorization, authenticates repository pre-state and post-state, rejects output/repository overlap and shares one writer lock with compliant lower-level persistence.
8. The next two finding-producing reviews identified seven remaining gaps. The first found that direct portfolio persistence did not always acquire the shared lock and that deterministic output-target failures could occur after canonical persistence. The second found caller-asserted `_lock_held` bypasses on both public persistence APIs, missing independent result/view identity authorization, coercive Python equality across JSON populations, one-directional root containment, and hard-link output aliases. The correction gives public persistence APIs no lock-bypass parameter, routes only the already-locked owner through private locked implementations, requires complete owner-derived package/result/view identity populations, uses canonical typed-JSON equality, requires full output/repository root disjointness, and rejects symlink, type, hard-link and inode-collision defects before calculation or canonical mutation.
9. The following fresh review found that directory writability did not prove an existing regular target was writable. Preflight now rejects targets with no write mode and opens each existing target for write without truncation before any calculation or canonical mutation.

The earlier blocked closeout remains historical evidence. It must be amended by an explicit correction section; it must not be silently erased.

## 2. Precise vocabulary

- **Portfolio invocation/run**: one call to `run_portfolio()` in `canary` or `production` mode while holding the portfolio writer lock.
- **Candidate evaluation**: one deterministic execution attempt for an entry selected by the run mode, or one outcome record for a selected preregistered exclusion.
- **Canary evaluation**: evaluation of every manifest entry whose literal `canary` field is true; this is a scoped evaluation over the complete authoritative manifest.
- **Admission attempt**: the exact manifest, classified manifest-byte identity (`file_bytes` or `canonical_in_memory_bytes`), run mode, evaluated and unevaluated scopes, outcomes, deterministic reruns, proposed packages, proposed views, blockers and derived decision immediately before persistence could occur.
- **Rejected/failed attempt**: a structurally valid admission-attempt envelope whose derived decision is `reject`; it may be recorded outside canonical storage but authorizes no package write.
- **Admitted portfolio run**: a successful admission attempt whose exact proposed package set was passed to canonical persistence. This phrase describes the coordinated run; it does not make the manifest, attempt envelope, rejected candidates or operational views canonical objects.
- **Admitted package**: a validated `KnowledgeObjectPackage` written or idempotently confirmed by the Knowledge Repository persistence primitive.
- **Canonical mutation**: any write under the Knowledge Repository root that can change canonical object, evolution, index or manifest state.
- **Conformance subject**: for the live boundary, the admission-attempt envelope defined here; for published profile v1, the separate immutable historical analytical adaptation envelope.
- **Admission record**: the deterministic attempt envelope and validator result recorded outside canonical package storage. A rejection record is not an admitted portfolio or package.
- **Historical production surface**: the immutable manifest, execution results, packages, views and governed conclusion adapted by `knowledgeforge.evidence_portfolio.conformance.v1@1.0`.
- **Lower-level persistence**: `persist_packages()` and `knowledge_repository.persist_knowledge_object_packages()`. These accept already proposed packages and lack the complete run subject; they are not Evidence Portfolio admission boundaries.

`admission`, `promotion`, `acceptance` and `successful execution` are not synonyms. A valid candidate execution becomes a proposed package; only a successful run-level admission decision permits persistence; only the package is canonical.

## 3. Operational owner and supported entry points

The sole Evidence Portfolio admission owner is:

`tools/evidence_portfolio_production.py:run_portfolio()`

It acquires the stable repository-adjacent writer lock and delegates to `_run_portfolio_locked()`. The supported entry points are:

1. the Norway/shared CLI in `tools/evidence_portfolio_production.py`;
2. the Sweden Infrastructure CLI in `tools/evidence_portfolio_sweden_infrastructure.py`;
3. direct programmatic calls to `run_portfolio()`.

Both CLIs converge on the same owner. Direct calls cannot bypass the owner-local pinned dispatch. `_run_portfolio_locked()` is an internal implementation detail and is not a supported public entry point.

The generic Knowledge Repository CLI and persistence functions remain lower-level package persistence. Their existence does not constitute Evidence Portfolio admission and they must not claim an admission-attempt record.

## 4. Reconstructed run semantics

### 4.1 Evaluation and outcome scope

- Canary mode retains the complete authoritative manifest and selects every entry with `canary is True`. In the accepted Norway and Sweden manifests this is one executable candidate plus one preregistered exclusion. Exactly those selected entries receive outcomes; the non-canary executable entry is explicitly unevaluated.
- Production mode selects every manifest entry. Both executable entries and the preregistered exclusion receive outcomes.
- Executable entries are evaluated twice for deterministic comparison. A preregistered exclusion receives one `rejected` outcome at `pre_execution` and is not executed.

### 4.2 Package and view rules

- Only a selected executable outcome with disposition `valid`, a matching deterministic rerun, no candidate-limit blocker and a successful package validator can produce a proposed package.
- Null and failed executable outcomes produce no package; the owner emits no runtime-rejected executable transition.
- A preregistered exclusion produces no package.
- Every valid proposed package contains exactly 28 result records under the current production contract and produces exactly 28 operational views.
- Views are non-canonical and each must bind exactly one result record and its proposed canonical package.
- Empty packages, synthetic successful outcomes and reduced/resealed manifests are forbidden.

### 4.3 Decision and mutation ordering

The corrected order is:

1. resolve the output and repository roots and reject containment in either direction before acquiring the writer lock;
2. snapshot the caller-supplied manifest and acquire the shared repository-adjacent writer lock;
3. validate the complete authoritative manifest and exact manifest-byte identity; a CLI/file-backed invocation decodes and fingerprints one observed byte string, while a direct in-memory invocation uses deterministic canonical JSON bytes and cannot supply a claimed hash;
4. preflight the output destination and every deterministic output target, after manifest/source-byte authentication but before repository authentication, calculation or canonical mutation;
5. authenticate repository pre-state and, in production mode, validate the exact canary authorization against that state;
6. derive evaluated and unevaluated scopes from mode and manifest;
7. execute selected entries and deterministic reruns;
8. enforce candidate, aggregate and valid-count gates;
9. construct proposed packages and views only when prior blockers are empty;
10. enforce package limits and reauthenticate the repository state against the pre-state;
11. build and freshly validate the exact pinned admission-attempt envelope;
12. derive `admit` or `reject` from envelope semantics, never from a caller-supplied success claim;
13. only if the derived decision is `admit`, call the private already-locked persistence implementation with the exact package population bound into the validated envelope;
14. write non-canonical attempt/result/accounting/package/view/gate records;
15. raise on rejection.

No canonical write may precede step 13. Profile validation failure or a derived rejection must leave the repository root unchanged.

### 4.4 Existing admission and storage unit

At the operational decision layer, one run admits an exact set of packages:

- successful canary: one package from the evaluated canary scope;
- successful production: the exact two-package production proposal, one of which may already exist identically from canary admission.

The canonical unit is the `KnowledgeObjectPackage`, not the manifest, run envelope, outcome or view. `knowledge_repository.persist_knowledge_object_packages()` performs a complete semantic/output-path preflight, then writes package, evolution, index and manifest files sequentially using per-file atomic replacement. It is not a transactionally atomic whole-portfolio commit. Consequently:

- semantic rejection before persistence produces no partial canonical admission;
- valid packages are never admitted alongside an executable null or failure under the current exact valid-count gates;
- an operating-system failure during the lower-level sequential write remains a crash-atomicity limitation and must not be described as whole-portfolio atomicity.

This limitation does not make the admission subject ambiguous and does not authorize a permissive profile. It is outside this bounded conformance integration correction.

## 5. Hypothesis adjudication

### Hypothesis A — rejected as a complete explanation

A is partly true: negative executable outcomes are rejected attempts, not admitted negative portfolios. Profile failure on them is not evidence that such subjects should be declared successfully admitted.

A is insufficient because successful canary runs do mutate canonical state and are explicitly recorded as `isolated_canary_admitted`. Published conformance v1 requires outcomes for the entire manifest and packages for every executable manifest entry, so it cannot represent the actual admitted canary scope.

### Hypothesis B — selected

The owner legitimately admits a scoped canary package from a complete authoritative manifest while leaving one executable candidate explicitly unevaluated. The live subject also needs to represent rejected attempts without inventing packages. Those are operational run/admission-attempt semantics, not the historical analytical-question adaptation governed by conformance v1.

The narrow additive artifact is therefore:

`knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`

It is a distinct profile, not `knowledgeforge.evidence_portfolio.conformance.v2`, because it governs a different conceptual subject and lifecycle moment.

### Hypothesis C — rejected for this task

The owner completes its semantic admission decision before calling persistence; supported portfolio entry points converge on that ordering; and the exact admission-attempt subject is unambiguous. The current gates prevent successful packages from being persisted alongside an executable null or failure.

The lower-level repository writer is only per-file atomic, not whole-portfolio transactional. That limitation is recorded, but it does not show mutation-before-decision, inconsistent entry points, or an undefined admission unit. This task therefore does not redesign the owner or disguise a defect with a permissive schema.

## 6. Admission-attempt profile v1

The envelope must bind exactly:

- `schema_name = knowledgeforge.evidence_portfolio.admission_attempt.v1`;
- `schema_version = 1.0`;
- `profile_id = knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`;
- run mode (`canary` or `production`);
- the complete authoritative manifest object, semantic fingerprint and invocation byte fingerprint;
- exact evaluated-candidate IDs in manifest order;
- exact unevaluated/not-selected IDs in manifest order, without invented outcomes;
- one outcome for every and only evaluated candidate;
- deterministic rerun bindings for every and only evaluated executable candidate;
- blockers;
- proposed packages only for valid deterministic executable outcomes;
- proposed views covering proposed package result records exactly once;
- package, result and view fingerprints;
- derived decision (`admit` or `reject`);
- deterministic envelope fingerprint.

The exact owner-emitted disposition/stage matrix is:

- a preregistered exclusion: `rejected` at `pre_execution`;
- an executable input-validation failure: `failed` at `input_validation`;
- an executable calculation null: `null` at `calculation`;
- an executable calculation exception: `failed` at `calculation`;
- a valid executable result: `valid` with no stage.

`rejected` at `execution` and failures at `execution` or `post_execution_validation` are not emitted by this owner and are rejected as invented transitions. An unevaluated candidate has no outcome, rerun, package or view. A negative evaluated candidate has an outcome but no package or view. A valid evaluated candidate has exactly one package and exact view coverage.

The validator derives the decision. It rejects spoofed caller claims, malformed populations, stale or tampered fingerprints, package/outcome mismatch, view/package mismatch and unsupported stages. The owner accepts only a response with exact `valid is true`, exact Boolean `admission_authorized`, exact `admit`/`reject`, and agreement with the owner's independently derived decision; truthy coercion is forbidden. A structurally valid negative attempt may validate as an attempt while returning `admission_authorized = false`; structural validity must never be reported as successful admission.

## 7. Exact dispatch and anti-spoofing

The live owner supports exactly `knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`. It accepts no omitted identity, schema without version, alias, fallback, `latest`, range, compatibility inference or silent upgrade.

Dispatch is one closed explicit branch, not a registry, plugin system or discovery layer. The owner constructs the envelope from current local manifest, outcomes, reruns, proposed packages and views and validates it immediately before persistence. It does not accept a caller-supplied conformance result. Persistence uses the exact package objects embedded in the freshly validated envelope.

The envelope fingerprint is necessary but not sufficient: validation recomputes manifest, package, result, view, population and decision semantics. It also compares every executable candidate to a complete owner-derived package-identity map and verifies package scope, inputs, method, evidence, provenance and result lineage against that manifest entry. Resealing a tampered envelope does not make it admissible. Any disagreement between the owner's blocker-derived authorization and the profile result is an internal contradiction and raises before persistence or attempt-record output.

## 8. Historical compatibility and non-migration

Published `tools/evidence_portfolio_conformance.py`, its tests, profile documentation and Norway/Sweden historical envelope proofs remain byte-for-byte unchanged. They retain their accepted meaning: two isolated historical analytical adaptations conform to `knowledgeforge.evidence_portfolio.conformance.v1@1.0`.

No historical manifest, outcome, package, view, canonical record or report is migrated or rewritten. No third portfolio is created. The new live profile does not retroactively claim that historical runs used it.

## 9. Meaning and limits of a pass

A successful admission-attempt validation proves only that:

- the exact run subject is structurally and fingerprint-consistent;
- evaluated and unevaluated scopes match the authoritative manifest and mode;
- outcomes, reruns, packages and views obey this owner's bounded cardinality and lineage rules;
- the derived decision is correctly classified;
- when `admission_authorized` is true, the exact proposed package set may reach the existing lower-level persistence call.

It does not prove source truth, external authenticity, analytical usefulness, independence, causal or predictive meaning, future reproducibility, crash-transactional whole-portfolio storage, Git publication, PostgreSQL projection, universal Evidence Portfolio generality or authorization for another portfolio.
