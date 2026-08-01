# D-20260802 — Evidence Portfolio Conformance Profile v1 Accepted for Isolated Prospective Use

Date: 2026-08-02
Status: accepted; isolated prospective conformance only
Decision class: bounded Evidence Portfolio conformance contract
Task: `T-20260801-evidence-portfolio-accounting-traceability-transformation-identity-dependence-conformance-correction-v1`
Report: `R-20260802-evidence-portfolio-conformance-correction-closeout-v1`

## Decision

Accept `knowledgeforge.evidence_portfolio.conformance.v1@1.0` as the smallest coherent prospective conformance profile that corrects the four defects identified by the published Norway Health / Sweden Infrastructure generalization review:

1. phase-aware, exactly reconciled candidate and result accounting;
2. directional question → candidate → evidence traceability with exact source-candidate and exclusion-reason binding;
3. deterministic transformation identity bound to source-series and historical-result lineage;
4. explicit source-series, provider, acquisition and method dependence bases with deterministically derived cluster identities.

The accepted profile is a conformance layer over the existing Evidence Portfolio composition. It is not a new canonical object, evidence family, calculation method, database, projection schema, portfolio subsystem or general dependence ontology.

## Accepted implementation boundary

The accepted implementation consists of:

- `docs/evidence_portfolio_conformance_profile_v1.md`;
- `tools/evidence_portfolio_conformance.py`;
- `tests/test_evidence_portfolio_conformance.py`.

The implementation builds deterministic, versioned envelopes from parsed immutable historical surfaces. Envelopes embed deep-copied manifest, execution, package and view objects; bind package/result/view/source identities; embed and hash the exact source report; extract the governed conclusion section mechanically; and regenerate candidate ledgers from machine state.

Envelope validation proves deterministic self-consistency. It does not replace repository authentication or digital signatures. Isolated proofs must separately compare embedded sources and report hashes with governed repository inputs.

## Compatibility and authority

Historical Norway Health and Sweden Infrastructure manifests, execution evidence, packages, views, reports, tasks and canonical records remain unchanged. They do not silently conform. They require explicit versioned adaptation.

The two accepted proof envelopes exist only under:

`/tmp/knowledgeforge-evidence-portfolio-conformance-correction-20260801-v2`

They are validation evidence, not canonical Knowledge Objects or production state.

This decision does not authorize:

- mandatory live producer integration;
- rewriting or superseding either historical portfolio;
- canonical or PostgreSQL mutation;
- a third portfolio;
- new evidence acquisition or recalculation;
- publication, staging, commit, push, tag or release.

Any live admission boundary or third portfolio requires a separately governed successor task.

## Validation basis

Accepted evidence at closeout:

- 30 focused conformance tests passed, including coherent resealing attacks;
- 95 combined conformance and historical Evidence Portfolio regression tests passed;
- 518 full repository tests passed;
- Python compilation passed;
- both isolated proof envelopes validated with exact manifest, execution, package, view, report and conclusion preservation;
- Norway fingerprint: `sha256:82e10a666b0aa791e0f84f7e2c84aa3bdc4d9b81a1e0b9c1042cde77a7a3450f`;
- Sweden fingerprint: `sha256:8c854e83657cd2395df4e1dbd705ca416c0095f0c57c6c1f7033bea12b22d33c`;
- canonical repository authenticated at 564 objects, 564 evolution records, six indexes and fingerprint `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`;
- historical tracked-diff check passed and Git index remained empty.

Two independent adversarial review cycles were used, the authorized maximum. Cycle 2 reported no blocker and identified two high-severity binding gaps. Those gaps were corrected by recomputing candidate/package/result/view/transformation and dependence semantics from embedded source artifacts, with new coherent-resealing tests. No third review cycle was opened.

## Remaining limits

The implementation proves conformance for two structurally similar historical portfolios with valid executable candidates and expected pre-execution exclusions. Runtime rejection, null, redundancy and failure taxonomy are adversarially tested but not natural portfolio outcomes. Independent providers, missingness, disagreement, irregular frequency, supersession and a divergent third portfolio remain unproven.

Repository-wide durability remains a separate governance concern: the broad durability validator classified the current mixed uncommitted repository as decision D because recovery-critical and operational-checkpoint artifacts are not machine-loss durable. It found zero actual secret blockers and passed sensitive-material classification. This does not invalidate the isolated conformance implementation, but it prohibits representing the wider repository as durability-ready.

## Consequence

The published two-portfolio classification remains `provisionally generalizable with bounded corrections`. The bounded correction is now implemented and validated as an uncommitted candidate. Universal generality and readiness for portfolio three remain unclaimed and separately gated.
