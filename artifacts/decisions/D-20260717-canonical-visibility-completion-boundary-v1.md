# Decision: Canonical visibility completion boundary v1

- Decision ID: `D-20260717-canonical-visibility-completion-boundary-v1`
- Status: Accepted architectural clarification; documentation only; not implementation-authorized, production-authorized, or publication-authorized
- Date: 2026-07-17
- Scope: future native Package Content Fingerprint v1 promotion–verification–admission–insertion–publication sequence

## 1. Decision

KnowledgeForge accepts one narrow successor clarification to the stage-9/stage-10 completion boundary in:

`docs/promotion_verification_admission_publication_sequence_v1.md`

The protected predecessor decision remains immutable and is not edited:

`artifacts/decisions/D-20260716-promotion-verification-admission-publication-sequence-v1.md`

That predecessor correctly established the 15-stage order and logical atomicity requirement, but its wording left materially ambiguous whether stage-9 transition materialization itself made a next state canonical or completed canonical insertion before stage-10 read-back and reconciliation.

The accepted clarification is:

1. stage 9 prepares and materializes the complete admitted transition behind the non-canonical reader-visibility gate;
2. stage 9 does not make the new state canonically visible and does not complete canonical insertion;
3. stage 10 performs read-back verification and deterministic reconciliation while the complete previous state remains the only canonically visible state;
4. only after every stage-10 check succeeds may one logically atomic visibility switch expose the complete next state, retire the previous state as current, and complete canonical insertion;
5. stage-10 failure prohibits the visibility switch and any insertion-success claim; partial materialization remains non-canonical residue governed by future recovery contracts;
6. stage 11 Git publication follows only completed stage-10 canonical insertion.

The stage count and overall order remain unchanged. Stages 1–8 and 11–15 retain their accepted meanings and positions. Verification and admission remain separate; PostgreSQL projection remains after Git publication; export generation remains before independent export verification; later lifecycle events remain separately governed.

## 2. Precise completion semantics

Logical atomicity has one conformance meaning: canonical readers and downstream processes observe either the complete previous canonical repository state or the complete next canonical repository state, never an intermediate state.

Stage 9 MAY materialize, as required by the future repository contract:

- exact admitted package bytes;
- the finalized authority record;
- evolution metadata;
- required deterministic indexes;
- manifest state;
- repository-fingerprint or equivalent reconciliation-identity material;
- other repository-contract-required components.

All such material remains behind the non-canonical reader gate. A directly visible object file does not establish canonical membership. A manifest-last mechanism can conform only if all canonical readers enforce the manifest as the visibility gate.

Stage 10 MUST reconcile exact bytes, authority bindings, manifest state, required indexes and metadata, repository identity, predecessor immutability, and absence of unauthorized paths before the sole visibility switch. If reconciliation fails, the previous state remains the only canonical state. Reconciliation failure cannot occur after canonical completion because successful reconciliation is a prerequisite to the visibility switch.

## 3. Exact affected specification identity

The affected specification is identified by:

- path: `docs/promotion_verification_admission_publication_sequence_v1.md`
- corrected working-tree SHA-256 at this decision's finalization: `1f75e27eb37af830dd7552cf8e8b31eed0609471e673b48b82da456230c5b743`
- protected predecessor decision: `artifacts/decisions/D-20260716-promotion-verification-admission-publication-sequence-v1.md`

The corrected specification and this decision are not Git-published merely because these working-tree bytes exist. Eventual publication evidence MUST be the actual immutable Git commit and verified resulting commit tree containing the exact final specification bytes and exact final decision bytes, with expected parent, allowlisted paths, no missing required paths, and no unauthorized paths. Neither this decision nor the prepublication specification predicts that future commit ID or claims publication success.

If the specification bytes change before the separately authorized publication pass, this decision's digest binding MUST be corrected before publication; no ambient or approximate identity is acceptable.

## 4. Relationship to governing-contract resolution

This clarification is coordinated with:

`artifacts/decisions/D-20260716-governing-contract-resolution-profile-v1.md`

That decision governs the native-v1 release-authority family, cross-genesis checkpoint evidence closure, deterministic release-state/current-head function, trust-context bindings, and construction/verification authority boundary. This decision governs only stage-9 materialization versus stage-10 reconciliation, visibility, and insertion completion.

Neither decision silently overrides the other. Governing-contract resolution does not authorize insertion or visibility; this completion-boundary decision does not alter resolver authority, Package Content Fingerprint v1, or governing-contract resolution.

## 5. Current implementation status

No current repository writer is declared conforming. In particular, this decision does not change or validate `tools/knowledge_repository.py`.

The following remain closed implementation gates:

- authority-record path, naming, identity, canonicality, collision, discovery, manifest/index/fingerprint participation, reconciliation, retention, failed-publication treatment, and recovery;
- exact non-canonical staging and reader-gate mechanism;
- exact atomic visibility-switch mechanism;
- exact repository transaction boundary;
- read-back and deterministic reconciliation implementation;
- quarantine, retention, repair, cleanup, and recovery contracts;
- Git publication allowlisting and actual commit-tree verification;
- independent implementation and conformance validation;
- separate implementation, production, and publication authorization.

Future conformance vectors MUST prove at least:

1. stage-9 materialization followed by stage-10 failure leaves only the previous state canonical and performs no visibility switch;
2. successful stage-10 verification/reconciliation permits exactly one atomic visibility switch and only then completes insertion;
3. attempted visibility before stage-10 success fails closed;
4. attempted stage-11 publication before completed stage-10 insertion fails closed.

## 6. Non-goals and preservation

This is an architectural clarification/correction, not implementation. It does not:

- modify a package or Knowledge Repository object;
- create or modify a PostgreSQL object;
- generate or modify an export;
- stage, insert, reconcile, publish, project, or migrate anything;
- authorize implementation, production, or publication;
- declare any current writer conforming;
- create a service, registry, database, artifact class, task, schema, test, or workflow;
- change the Package Content Fingerprint v1 algorithm, descriptor, RFC 8785 canonicalization, SHA-256, or root `/fingerprints` exclusion;
- change construction authorization, independent technical verification, admission authorization, exact-byte continuity, or combined-record independence;
- design later lifecycle events.

No package, repository object, PostgreSQL object, or export is modified by acceptance of this documentation decision.

## 7. Publication status

This corrected documentation state requires a fresh independent read-only publication-readiness audit. Only a separately authorized bounded publication pass may publish the corrected documentation if that audit returns ready. Publication of this decision does not authorize implementation or production.
