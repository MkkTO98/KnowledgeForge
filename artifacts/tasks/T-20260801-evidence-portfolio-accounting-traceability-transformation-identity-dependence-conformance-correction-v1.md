# T-20260801 — Evidence Portfolio Accounting, Traceability, Transformation-Identity, and Dependence Conformance Correction v1

Status: complete; fully validated uncommitted candidate
Owner: Hermes
Classification: prospective Evidence Portfolio conformance correction; no production or canonical mutation

## Objective

Implement the smallest coherent prospective Evidence Portfolio conformance profile that corrects the four defects published by the two-portfolio generalization review, then prove Norway Health and Sweden Infrastructure can be represented under it in isolated temporary storage without changing their evidence, calculations, conclusions, historical artifacts, canonical packages, or canonical repository.

## Authority and immutable baseline

- Activation authority: explicit user instruction on 2026-08-01.
- Branch/HEAD/fetched `origin/main`: `main` at `3076f191040fbf4a44beea2d41602bf6e2371ebe`, ahead/behind `0/0`, empty index.
- Published predecessor review: task, decision and report `T/D/R-20260801-two-evidence-portfolio-generalization-review-v1` plus `docs/roadmap.md`.
- Canonical baseline: 564 objects, 564 evolution records, six indexes, fingerprint `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`.
- Preserved unrelated baseline: 493 Git-visible records and 313 ignored records; 806 authenticated identities with zero mismatches.
- External pre-edit evidence: `/tmp/knowledgeforge-evidence-portfolio-conformance-correction-v1-20260801/preflight.json` and `pre_edit_identities.json`.

## Publication discrepancy adjudication

The published commit subject is `Record two-Evidence-Portfolio generalization review`; the earlier publication prompt prescribed `Review Evidence Portfolio generalization`. The accepted commit is not amended or rewritten.

For the published report:

- Git blob object ID: `2b20991ef1dc0dff7839306bf2589150bedd16c3`;
- filesystem and committed-blob SHA-256: `sha256:5a33c83321cc3f5d023080b7f8da162bee2a36e35b7fdc11a5b7363958555318`;
- externally reported 40-hex value: `5a33c83321dc0dff7839306bf2589150bedd16c3`.

The reported value is neither identity. It is a chimera formed from the first ten hex characters of the SHA-256 and the final thirty characters of the Git blob ID. It occurs in no tracked repository artifact at the published commit. The discrepancy is confined to the external completion message, so successor activation may proceed.

## Published correction matrix

| Area | Observed defect | Required invariant | Enforcement owner | Positive proof | Negative proof |
|---|---|---|---|---|---|
| Accounting | `excluded_pre_execution` became machine `rejected_candidates`; narrative and machine dispositions drifted. | Every candidate has exactly one phase-aware terminal disposition; manifest candidates reconcile exactly to excluded plus executed, and executed reconcile exactly to valid, execution rejection, null, redundant or failed. Record counts reconcile separately from evidence/support counts. | Prospective conformance profile validator and accounting builder. | Exact Norway/Sweden reconciliation. | Missing, duplicate, contradictory and unknown dispositions. |
| Traceability | Neither portfolio binds candidates to a substantive bounded analytical question; Sweden prose described all-pairs exclusion while the manifest excluded Internet-user CAGR. | Every governed question resolves directionally through a candidate relation to admitted, excluded or absent evidence units; candidate IDs and exact exclusion reasons are machine-rendered, and orphan questions/evidence/claims fail. | Prospective conformance profile plus deterministic candidate-ledger renderer. | Complete resolvable question→candidate→transformed evidence→historical result/source chain. | Orphan evidence, unsupported question link, changed candidate/reason and broken intermediate reference. |
| Transformation identity | Manifests use `linear_time_index_slope`; records use `linear_time_index`; views omit transformation; result identity does not bind transformation. | A transformation definition and required parameters produce one deterministic identity bound to source-series lineage; every transformed evidence unit carries it; different analytical forms cannot collide or substitute. | Prospective transformation registry/identity validator; projection remains payload-preserving, not owner. | Level, adjacent difference and linear-time-index identities are distinct and stable for the same source. | Alias, missing parameters, collision, substitution and contradictory identity. |
| Dependence | Per-series `dependency_clusters` obscure shared WDI provider, Campaign 40 acquisition and one method family, permitting false corroboration. | Source-series diversity is reported separately from provider, acquisition and method dependence; known shared lineage and unresolved dependence are explicit; record diversity cannot inflate independent support. | Prospective dependence declarations and dimension-specific accounting/reporting. | Two distinct series remain distinct while shared provider/acquisition/method grouping is explicit. | Different IDs over shared lineage cannot masquerade as independent; unknown never becomes independent; one shared attribute does not collapse distinct evidence. |

## Frozen implementation scope

Smallest coherent architectural unit: `knowledgeforge.evidence_portfolio.conformance.v1@1.0`, a prospective, deterministic conformance profile over the existing Evidence Portfolio composition. It is not a new canonical object, portfolio subsystem, database, ontology, calculation method or evidence family.

Intended additions:

- `docs/evidence_portfolio_conformance_profile_v1.md`;
- `tools/evidence_portfolio_conformance.py`;
- `tests/test_evidence_portfolio_conformance.py`;
- this task, one decision, and one final report.

Intended modifications:

- `tools/evidence_portfolio_production.py` only for a narrow prospective conformance-validation seam if tests prove it is required;
- `state/active_goal.md`, `state/project_state.md`, `context/latest_handoff.md` and affected `_SUMMARY.md` files required by lifecycle closeout;
- `docs/roadmap.md` only if the established lifecycle requires recording completion/readiness.

Compatibility strategy:

- Historical Norway and Sweden manifests, results, packages, views, tasks, reports and canonical objects remain byte-identical.
- Corrected representations are versioned prospective conformance envelopes built only in external temporary storage during this task.
- Each corrected envelope retains exact historical manifest/result/source identities and states that it adapts, rather than rewrites or supersedes, historical representation.
- Legacy artifacts do not silently pass the prospective profile; they require explicit adaptation.

Prohibited paths and actions:

- both historical portfolio production roots and their task/report artifacts;
- `knowledge_repository/**` and all live manifests/indexes/evolution records;
- PostgreSQL and projection code/schema/state;
- evidence fixtures and calculations;
- third-portfolio files or selection;
- sibling projects, publication authority, staging, commit, push, tag, release, cleanup, amend, revert or force-push.

## Isolated conformance procedure

For each historical portfolio, load only its retained manifest, execution results, accounting, views and canonical package references; construct a versioned conformance envelope in a fresh external temporary workspace; validate accounting, traceability, transformation identities, dependence, deterministic serialization/fingerprint and exact retained conclusion text; replay construction and compare bytes/fingerprints. Compare the conformance envelope structurally with the immutable historical surfaces. Authenticate the live canonical repository before and after.

## Acceptance criteria

- [x] RED tests prove all four missing conformance behaviors and adversarial failures.
- [x] Prospective profile and deterministic builders/validators pass all focused tests.
- [x] Historical formats remain immutable and require explicit versioned adaptation.
- [x] Norway Health isolated conformance passes without conclusion change.
- [x] Sweden Infrastructure isolated conformance passes without conclusion change.
- [x] Focused, Evidence Portfolio regression and full repository tests pass above the existing 488-test baseline.
- [x] Compilation, diff, coherence, context health, no-write architecture audit, security/hygiene and preservation gates pass, with the broad durability decision and one command-authorization denial classified separately below.
- [x] Canonical repository remains exactly 564/564/6 with the same fingerprint.
- [x] Candidate remains fully validated and uncommitted with an empty Git index.

## Outcome

Accepted prospective profile: `knowledgeforge.evidence_portfolio.conformance.v1@1.0`.

Delivered implementation, tests and contract:

- `tools/evidence_portfolio_conformance.py`;
- `tests/test_evidence_portfolio_conformance.py`;
- `docs/evidence_portfolio_conformance_profile_v1.md`.

Accepted decision and closeout report:

- `artifacts/decisions/D-20260802-evidence-portfolio-conformance-profile-v1-accepted.md`;
- `artifacts/reports/R-20260802-evidence-portfolio-conformance-correction-closeout-v1.md`.

Both historical portfolios validated in `/tmp/knowledgeforge-evidence-portfolio-conformance-correction-20260801-v2`. Exact manifest, execution, package, view, source-report and conclusion preservation passed. Final boundary accounting returned 504/504 expected visible records, 313/313 ignored records, 797 unrelated identities with zero mismatch, six exact new paths and no unexpected/missing path. The Git index is empty; no canonical, PostgreSQL, historical-portfolio or sibling-project mutation occurred.

Verification: 30 focused tests, 95 combined Evidence Portfolio tests and 518 full-suite tests passed; compilation passed; coherence/context health/architecture audit had zero blocks; canonical authentication returned 564 objects, 564 evolution records, six indexes and the unchanged fingerprint. Two independent adversarial cycles were exhausted. Cycle 2 found no blocker; its two high-severity source-binding findings were remediated and covered by coherent-resealing tests.

Repository-wide durability remains decision D because the pre-existing mixed uncommitted tree includes recovery-critical and operational-checkpoint material that is not machine-loss durable. The same validator reported zero actual secret blockers and passed sensitive-material classification. This is a repository/governance limitation, not a conformance implementation failure, and publication remains prohibited.

## Current next action

Stop. Any staging/publication, live conformance admission seam, third-portfolio selection or production requires separate authority.
