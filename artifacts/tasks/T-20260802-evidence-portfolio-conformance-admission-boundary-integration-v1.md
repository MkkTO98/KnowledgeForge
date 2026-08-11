# Task: Evidence Portfolio conformance admission-boundary integration v1

ID: `T-20260802-evidence-portfolio-conformance-admission-boundary-integration-v1`
Status: complete; renewed closeout at the unstaged publication boundary
Date: 2026-08-02
Decision: `D-20260802-evidence-portfolio-admission-attempt-profile-v1.md`
Closeout: `R-20260802-evidence-portfolio-conformance-admission-boundary-integration-review-closeout.md`

## Objective

Adjudicate whether the two-Evidence-Portfolio generalization could be connected to the live producer without changing published historical conformance v1, and, if justified, implement the smallest fail-closed admission boundary.

## Final adjudication

Implementation was authorized only after correcting the initial category error:

- historical `knowledgeforge.evidence_portfolio.conformance.v1@1.0` remains immutable and describes historical analytical adaptations;
- the live owner needs the separate exact profile `knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0`;
- null/rejected/failed outcomes are authenticated rejected attempts, never package-less admitted portfolios;
- a successful canary is a scoped admission over the complete manifest and may canonically persist only the exact validated package population.

## Implemented boundary

The candidate:

- routes Norway/shared CLI, Sweden CLI and direct supported calls through `run_portfolio()`;
- binds exact profile, manifest source bytes or classified canonical in-memory bytes, selected scope, outcomes, reruns, blockers, packages and views;
- requires complete independently owner-derived package, result and view identities for authorization;
- compares cross-population JSON semantics without Python bool/int/float coercion;
- permits only owner-emitted negative stage/disposition combinations;
- separates structural validity from admission authorization;
- rejects owner/profile decision disagreement before persistence or attempt-record output;
- authenticates repository pre-state, rechecks it after calculation, binds it under one shared writer lock and authenticates post-state;
- exposes no public caller-asserted lock bypass;
- requires full output/repository root disjointness and preflights target type, symlink, hard-link, inode collision, mode and non-truncating write-open before execution;
- preserves generic lower-level repository persistence as a non-admission package API.

## Correction history

1. Initial review blocked implementation because historical conformance v1 could not represent canary scope and negative outcomes.
2. Adjudication corrected the category error and selected a distinct admission-attempt profile.
3. RED-GREEN implementation added the exact dispatcher and owner integration.
4. Independent review found package-identity, manifest-byte, stage-matrix, result-fingerprint and validator-disagreement gaps; all were corrected.
5. Further review found typed-manifest, authorization-context, repository-authentication, output-containment and shared-lock gaps; all were corrected.
6. Further review found direct helper locking and post-persistence output-destination defects; all were corrected.
7. Final adversarial cycles found public `_lock_held` bypasses, missing result/view identity authority, coercive cross-population equality, inverse root containment, hard-link aliases and existing-target writability. RED tests reproduced each defect; implementations and contracts were corrected.
8. A final fresh independent review returned PASS with no remaining supported-entry-point release blocker.
9. Publication review later found stale lifecycle wording, pre-authentication output preflight, and an unrelated summary deletion. RED-GREEN correction moved output preflight after manifest/source-byte authentication; lifecycle wording and the exact historical summary entry were restored.
10. Renewed review found coercive interpretation of a validator's `admission_authorized` field. RED reproduced truthy non-Boolean authorization reaching persistence; GREEN now requires exact `valid is true`, Boolean authorization, exact `admit`/`reject`, and owner/validator agreement before persistence.

## Verification

Renewed post-correction results from the cache-isolated 2026-08-11 verification:

- focused owner/profile/repository compatibility: `147 tests`, PASS;
- admission + historical conformance profile: `83 passed, 47 subtests passed`;
- exact historical 95 selection: `95 passed, 98 subtests passed`;
- exact frozen integration selection: `147 passed, 1 deselected, 109 subtests passed` (the one deselection is the later target-writability regression, separately included in focused/full runs);
- repository suite excluding the separately owned deterministic-funnel test file: `556 passed, 217 subtests passed`;
- canonical repository authentication: `564` objects, fingerprint `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`;
- independent adversarial review: initial BLOCK on coercive validator-response handling; RED-GREEN remediation complete; three renewed near-final reviews returned PASS, and exact final-byte verdicts are bound by the external current-session authority evidence.

Governance, security, coherence and final preservation evidence are recorded in the closeout report.

## Publication boundary

The exact candidate is intentionally unstaged. No commit, push, tag, release, PostgreSQL mutation, production portfolio run, third portfolio, or canonical project-repository mutation was authorized.

## Post-publication-review correction and renewed closeout — 2026-08-11

A publication-only review stopped without staging after identifying three release blockers:

1. stale `pending final closeout` lifecycle wording in the admission-boundary document;
2. side-effecting output preflight occurring before manifest/source-byte authentication;
3. task-extraneous removal of `post-campaign42-production-alignment-git-durability-20260712/` from `artifacts/reports/_SUMMARY.md`.

The ordering defect retains its RED-GREEN correction. The regression proved invalid manifest bytes could create the output directory (`1 failed`); moving `preflight_output_destination()` under the repository lock and after manifest/source-byte authentication made it pass (`1 passed`). Lifecycle wording and the historical summary entry are aligned, complete isolated verification passed, and renewed review drove the strict validator-response correction above.

Two earlier continuation attempts stopped at the concurrency gate rather than modifying overlapping work. The current session began only after quiescence was established. Fresh current-session authority authenticates exactly 22 admission-candidate paths and freezes every currently visible excluded path plus the seven named caches at current identities. Eight excluded paths have established deterministic-funnel provenance and non-overlap; the remaining excluded population is preserved without converting old totals into acceptance criteria.

### Renewed acceptance

- Quiescence, branch/parent/upstream, empty index, no Git operation/lock, and exact 22-path scope were freshly authenticated.
- Blockers A and C and the ordering correction are reflected in current contract and summary bytes.
- Cache-isolated focused, selected, and repository verification passed; the separately owned funnel test file was not run.
- All excluded visible paths and all seven caches remained unchanged from the fresh current-session snapshot.
- Historical conformance v1 and its accepted surfaces remain unchanged from `HEAD`.
- Historical bytes unavailable from the lost earlier external artifact remain unauthenticated; current authority proves only current-session non-interference.
- Keep the index empty. No publication, funnel continuation, or successor activation is authorized.

### Terminal boundary

The bounded correction is complete and re-closed. A later publication request must establish its own fresh authority over exactly the renewed 22-path candidate and must not absorb excluded work.
