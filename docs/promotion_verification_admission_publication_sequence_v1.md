# KnowledgeForge Promotion–Verification–Admission–Publication Sequence v1

Date: 2026-07-16
Status: architecturally accepted; Governing Contract Resolution Profile v1 accepted as normative architecture; not implemented; not production-authorized; machine-readable profile artifacts and record contract pending
Specification identifier: `knowledgeforge_promotion_verification_admission_publication_sequence_v1@1.0`
Applicability: future native Package Content Fingerprint v1 flows only

Normative terms in this document are `MUST`, `MUST NOT`, `SHOULD`, and `MAY`.

## 1. Scope and status

This document defines the future ordering, authority boundaries, identities, and failure behavior connecting final-package construction authorization, final-package verification, admission authorization, canonical insertion, Git publication, PostgreSQL projection, export generation, and export verification for native Package Content Fingerprint v1 packages.

This sequence is architecturally accepted. It is not implemented and is not production-authorized. It depends on:

- the accepted normative architecture in `docs/governing_contract_resolution_profile_v1.md`, with its machine-readable contracts, ResolverTrustRelease evidence, conformance vectors, and implementation still pending;
- a future contract for `FinalPackageVerificationAndAdmissionAuthorizationRecord` or an equivalently clear successor name;
- separately authorized implementation, conformance, production, and publication gates.

Until those prerequisites are accepted and implemented, native-v1 derivation, verification, admission, insertion, projection, and export MUST fail closed.

This document does not claim that the current package producer, validator, repository writer, PostgreSQL projection, or export implementation satisfies the future sequence.

## 2. Applicability to future native Package Content Fingerprint v1 flows

This sequence applies only to a future package flow that explicitly declares conformance to:

- `knowledgeforge_package_content_fingerprint_v1@1.0`; and
- this sequencing specification or an explicitly accepted successor.

A package that merely carries a v1-shaped descriptor MUST NOT be treated as `native_package_content_fingerprint_v1_valid` until independent verification succeeds. Successful technical verification does not make the artifact admitted, inserted, published, projected, exported, or current; those statuses require their own later events and authorities.

Current production paths MAY continue to be described by their historical contracts until a separately authorized migration or successor flow exists. They MUST NOT be represented as implementing this sequence.

### 2.1 Normative relationship to Package Content Fingerprint v1

`docs/package_content_fingerprint_v1.md` remains authoritative for fingerprint calculation, strict package parsing, canonicalization, package binding, and technical fingerprint recomputation. `docs/governing_contract_resolution_profile_v1.md` governs contract-manifest interpretation, ResolverTrustRelease validation, external technical trust selection, root authorization, closed dispatch, typed dependency closure, rule-domain delegation, and closure identity. This specification governs ordering and authority boundaries among final-package construction authorization, final repository serialization, non-canonical staging, verification, admission, canonical insertion, Git publication, PostgreSQL projection, export generation, and export verification. Each document is authoritative only within its declared domain.

Where older orchestration language in `docs/package_content_fingerprint_v1.md` conflicts with this accepted sequence, this corrected sequence controls. The corresponding bounded correction to that document is an orchestration clarification and amendment, not a new fingerprint algorithm version. It does not change the fingerprint field, descriptor, specification identifier, derivation boundary, RFC 8785 canonicalization, SHA-256 algorithm, parsing rules, package-ID binding, self-reference rules, or legacy classifications.

## 3. Non-retroactivity

This sequence MUST NOT be applied retroactively to existing package bytes, campaign records, Git commits, PostgreSQL rows, or export artifacts.

Existing package bytes MUST remain unchanged. KnowledgeForge MUST NOT:

- backfill historical promotion records;
- create retroactive final-package verification or admission authorizations;
- reinterpret historical Git publication as native-v1 admission;
- rewrite invalid legacy manifests;
- recompute or replace historical package identities merely for uniformity;
- create successor packages solely to make legacy representation match this sequence.

Legacy compatibility MUST remain descriptive and external.

## 4. Correct unit vocabulary

The following units are distinct and MUST NOT be collapsed:

| Unit | Normative meaning |
| --- | --- |
| Candidate | A bounded proposed knowledge package or proposition identified for deterministic evaluation; it is not canonical knowledge. |
| Candidate validation | Deterministic evaluation of candidate eligibility and prerequisites before final-package construction authorization. It does not establish final-package validity. |
| Final-package construction authorization | External governance authorization to construct a proposed final package from one immutable validated-candidate identity and scope. It is not historical package-local promotion, verification, admission, insertion, publication, projection, or export. |
| Proposed package | Complete pre-fingerprint semantic content presented for Package Content Fingerprint v1 derivation. |
| Package Content Fingerprint v1 | The semantic-content identity defined by `docs/package_content_fingerprint_v1.md`; it does not identify exact source serialization bytes. |
| Frozen staged artifact | The complete descriptor-bearing final package in its exact final repository serialization, frozen as immutable bytes outside the canonical Knowledge Repository. |
| Independent verification | Independent evaluation of the exact frozen staged artifact and its complete applicable immutable governing-contract set. Successful verification establishes technical fingerprint validity; it does not authorize admission. |
| Admission authorization | Unconditional authority to attempt insertion of one exact successfully verified artifact tuple into the canonical repository. Denied or deferred outcomes are not insertion-ready. |
| Canonical insertion | One logically atomic append-only repository transition whose materialization remains behind the non-canonical reader gate until successful read-back/reconciliation and whose single visibility switch then makes the exact admitted bytes and required authority/repository metadata canonically visible together. |
| Repository reconciliation | Read-back and deterministic reconciliation of the package, authority record, manifest, indexes, required evolution metadata, and resulting repository identity. |
| Git publication | An immutable Git commit containing the complete authorized repository transition and authority evidence. A local commit is not by itself proof of off-host durability. |
| Distribution | Transfer or exposure of the publication commit, normally through a verified remote ref. Distribution is not admission. |
| PostgreSQL projection | Derived operational materialization reconstructed from Git-published canonical repository state for conforming production. |
| Export generation | Materialization of a versioned derived consumer representation from the applicable published canonical and projected state. |
| Export verification | Independent verification of a generated export against its governing contract. |
| Later lifecycle event | A separately governed contradiction, weakening, withdrawal, currentness, succession, or supersession event that never mutates an immutable predecessor. |

For future native-v1 flows, only successful stage-10 reconciliation followed by the one atomic visibility switch may be called `canonical insertion complete`. Stage-9 local materialization is non-canonical preparation. An uncommitted completed insertion MUST NOT be called `Git-published` or off-host durable.

## 5. Complete event order

A conforming future native-v1 flow MUST use this order:

1. Candidate identification.
2. Deterministic candidate validation.
3. Final-package construction authorization through existing KnowledgeForge governance and decision machinery.
4. Construction of complete final semantic package content.
5. Package Content Fingerprint v1 derivation and descriptor attachment.
6. Production of the exact final repository serialization and freezing of those bytes in non-canonical staging.
7. Independent verification of the exact final staged artifact.
8. Unconditional admission authorization for the exact verified tuple:
   - package ID;
   - Package Content Fingerprint v1;
   - serialized-artifact digest.
9. Complete canonical-transition preparation and materialization behind the non-canonical reader gate.
10. Read-back verification, deterministic reconciliation, and logically atomic visibility switch completing canonical insertion.
11. Git publication in an immutable commit, followed by verification of the actual resulting commit tree.
12. Derived PostgreSQL projection from Git-published canonical state.
13. Derived export generation or materialization.
14. Independent export verification.
15. Later separately governed lifecycle events, when applicable.

The ordering is normative. A later event MUST NOT be used as retroactive authority for an earlier event. PostgreSQL agreement, export success, or Git storage MUST NOT make an invalid or unauthorized package valid.

## 6. Candidate identity and validation

A candidate MUST have a stable identity before validation and final-package construction authorization. Its identity MUST bind the bounded candidate scope and SHOULD bind all material candidate inputs, specifications, evidence references, and governing method or selection artifacts by immutable identity or content digest.

Candidate validation MUST be deterministic under its governing contract. It MAY record pass, failure, blockers, warnings requiring governance review, or ineligibility. Candidate validation MUST NOT claim:

- final package construction success;
- final Package Content Fingerprint v1 validity;
- exact serialized-artifact identity;
- admission;
- insertion;
- publication;
- projection or export success.

A candidate that changes materially after validation MUST be revalidated under the candidate identity rules. A future candidate contract MUST define whether the change requires a new candidate identity.

## 7. Final-package construction authorization

KnowledgeForge MUST reuse its existing file-backed governance and decision machinery as the carrier for final-package construction authorization in principle. It MUST NOT create a construction-authorization registry or service for this architecture. A standardized future construction-authorization contract remains a closed implementation prerequisite; existing machinery is not claimed to provide that complete contract today.

A final-package construction authorization MUST:

- bind one immutable candidate identity, the candidate evidence, declared scope, applicable candidate contracts, and authorization identity;
- occur after candidate identification and validation and before complete final package construction;
- be immutable or bound by an immutable content digest;
- be referenceable from hash-covered package lineage established before package finalization;
- record authorization, denial, deferral, withdrawal, or expiration;
- identify the governing authority and decision basis;
- state the construction scope it authorizes.

Final-package construction authorization authorizes only stage 4: construction of complete final semantic package content. Its identity is a required binding and process-lineage input to stages 5 through 7, but required identity binding grants no authority to perform those later events. Stages 4 through 7 MAY occur within one bounded operational attempt; that operational boundary does not define or expand stage-3 authority. The authorization does not bind a Package Content Fingerprint or exact serialized-artifact digest that does not yet exist. It MUST NOT authorize Package Content Fingerprint derivation, descriptor attachment, final repository serialization, freezing, non-canonical staging, or:

- final package or technical fingerprint validity;
- independent technical verification;
- any verification result;
- admission;
- canonical insertion;
- read-back or reconciliation;
- Git publication;
- PostgreSQL projection;
- export generation or verification;
- lifecycle action.

A package-local reference to the final-package construction authorization MAY be hash-covered lineage, but the authoritative authorization remains the external governance artifact, not a package-local assertion. The exact external construction-authorization identity MUST bind stage-5 derivation evidence, MUST bind stage-6 serialization and non-canonical staging evidence, MUST accompany the frozen artifact and stage-7 verification as required process lineage, and MUST be preserved by the verification evidence or combined authority record. The technical verifier MUST check and record exact equality of that identity across those bindings as a process-conformance observation. Required presence and exact binding do not grant authority, do not establish governance validity, and do not determine deterministic technical-fingerprint validity. The technical verifier MUST NOT evaluate the authorization's legitimacy, scope, currentness, expiry, withdrawal, or sufficiency as part of technical validity. Admission governance MUST evaluate those properties and MAY deny or defer an otherwise technically valid artifact when the construction process or required lineage binding was unauthorized or nonconforming.

This event is distinct from historical KnowledgeForge `promotion` and the current candidate-to-`KnowledgeObjectPackage` promotion convention. Existing package-local `promotion` fields remain immutable historical evidence. Existing acceptance criteria, historical decisions, and construction behavior are not retroactively redefined or renamed. Final native-v1 canonical acceptance is governed by independent verification, admission, logically atomic insertion, and Git publication—not by a historical package-local promotion block alone.

## 8. Final package construction

After final-package construction authorization, a producer MAY construct the complete final semantic package. Before fingerprint derivation, the producer MUST complete all hash-covered content required by the governing package, evidence, method, calculation, lineage, and applicability contracts.

The proposed package MUST satisfy the derivation prerequisites in `docs/package_content_fingerprint_v1.md`. Root `/fingerprints` MUST be absent or an empty object at derivation time. No placeholder or pending descriptor MAY be serialized as a final artifact.

Completed pre-fingerprint validation results and lineage facts MAY be hash-covered when their truth is established before derivation. The package MUST NOT contain claims whose truth can arise only after independent final verification, admission, canonical insertion, or publication.

After successful Package Content Fingerprint v1 derivation, the complete descriptor MUST be attached as the sole root `/fingerprints` member permitted by v1. The package MUST then be frozen. Any subsequent hash-covered semantic mutation invalidates that artifact’s descriptor and requires a separately governed construction attempt.

## 9. Final repository serialization and non-canonical staging

After descriptor attachment, the complete package MUST be serialized into the exact bytes intended for canonical repository installation. Those exact bytes MUST be frozen and persisted in non-canonical staging before independent verification.

Non-canonical staging is pre-admission persistence. It is not canonical repository membership, publication, or an admission result and does not violate the fingerprint specification's prohibition on premature canonical persistence.

Staging MUST:

- exist outside the canonical Knowledge Repository;
- remain immutable throughout verification and admission evaluation;
- bind the exact serialized bytes with a serialized-artifact digest;
- distinguish semantic Package Content Fingerprint v1 from physical exact-byte identity;
- contain the exact final repository serialization, including every byte of whitespace, escaping, member order, and newline treatment;
- remain non-canonical even though the bytes are in final package form;
- fail closed on mutation, disappearance, ambiguous identity, or digest mismatch.

Verification MUST operate on those exact bytes. Admission MUST bind those exact bytes. Canonical insertion MUST install those exact admitted bytes unchanged. Insertion code MUST NOT parse and reserialize, normalize, alter whitespace, alter escaping, alter member order, change a newline, or otherwise change any byte before insertion.

If any byte changes after verification or admission, the former serialized-artifact digest, verification result, and admission authorization do not authorize the changed artifact. The changed bytes MUST be frozen as a new staged artifact and receive a new exact digest, independent verification, and admission decision. Semantic Package Content Fingerprint v1 equality does not waive exact-byte reauthorization.

Staged material MAY be discarded only under a later accepted retention and failure-evidence contract. The current repository writer MUST NOT be claimed to satisfy future byte-preservation or logical-atomicity requirements merely because it can persist parsed package content.

## 10. Independent final-package verification

Independent verification MUST operate on the exact frozen staged bytes, not producer in-memory state, a selected-field projection, a pre-descriptor object, a PostgreSQL row, or an export payload.

The verifier MUST receive, at minimum:

- the exact staged artifact;
- the separately claimed package ID;
- the Package Content Fingerprint v1 descriptor carried by the artifact;
- the serialized-artifact digest;
- the exact fingerprint-specification artifact identified by media type and SHA-256 in the checkpoint-qualified `ResolverTrustRelease` uniquely selected by the accepted-release evidence closure derived from the externally pinned governance checkpoint;
- explicitly identified immutable governing contract artifacts;
- the accepted resolution profile;
- the exact fixed release-authority-family identity `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`, exact externally pinned `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, governed Git-tree material, complete cross-genesis checkpoint-derived accepted-release evidence closure, uniquely selected checkpoint-qualified ResolverTrustRelease and derived lineage when resolved, all applicable acceptance/withdrawal/supersession/disposition/adjudication/reactivation evidence, exact release-bound conformance-suite artifact and implementation-conformance evidence, and exact `technical_trust_context` tuple required by `docs/governing_contract_resolution_profile_v1.md`.

The exact final-package construction-authorization identity MUST accompany the artifact and the stage-5 derivation and stage-6 serialization/staging evidence as required stage-7 process lineage. The verifier MUST check and record exact equality of the identity across those bindings, but required presence and exact binding grant no authority, do not prove governance validity, and MUST NOT determine the deterministic technical result. Admission separately evaluates legitimacy, scope, currentness, expiry, withdrawal, and sufficiency.

The verifier MUST independently perform all checks required by `docs/package_content_fingerprint_v1.md`, including strict parsing, duplicate-key rejection, numeric and Unicode constraints, governing-contract resolution and digest validation, package validation, package-ID validation, containing-package self-reference rejection, RFC 8785 canonicalization, SHA-256 derivation, and exact descriptor comparison.

Verification establishes properties of the exact final bytes. It MUST NOT authorize admission merely by reporting success. Producer self-checking MAY supplement but MUST NOT replace independent verification.

A successful independent verification assigns technical status `native_package_content_fingerprint_v1_valid` to the exact frozen descriptor-bearing artifact when the verifier establishes conformance under the exact externally bound fingerprint-specification identity, media type, and SHA-256; exact resolver profile; fixed release-authority family; complete checkpoint identities and cross-genesis accepted-release evidence closure; exactly one eligible checkpoint-current ResolverTrustRelease and derived lineage in current mode or matching immutable historical evidence in historical mode; exact release-bound conformance-suite artifact and implementation-conformance evidence; authorized root; package technical contract closure; and verification-procedure closure. Zero or multiple eligible terminal releases cannot produce checkpoint-current technical validity. The verified fingerprint-specification digest MUST equal the fingerprint-specification explicit-root digest in the procedure closure. The result MUST be labelled `checkpoint-current` or `historical` with the exact checkpoint and MUST NOT claim unqualified global currentness. This qualified technical status is separate from construction-authorization validity, admission, canonical insertion, Git publication, PostgreSQL projection, export generation, export verification, and later lifecycle status. A fingerprint-valid artifact MAY still be denied or deferred admission. Denial, deferral, or a construction-authorization defect does not make a correctly computed fingerprint technically invalid.

Verification failure MUST prevent successful admission. Failed verification evidence MUST NOT present unvalidated claimed package IDs or fingerprints as validated identities.

## 11. Admission authorization and stale authority

Admission evaluation MUST occur after successful independent verification and before canonical insertion. A fingerprint-invalid or incompletely verified artifact MUST NOT receive successful admission authorization.

Admission binds exactly one artifact tuple:

```text
validated package_id
+ validated Package Content Fingerprint v1
+ exact serialized-artifact digest
```

Admission policy MUST bind exactly one externally authorized governance checkpoint for the evaluation and evaluate that checkpoint pin's legitimacy, applicability, sufficient recency, withdrawal status, and sufficiency; final-package construction-authorization legitimacy, scope, currentness, expiry, withdrawal, and sufficiency; the `admission_policy_closure`; current eligibility and stale-authority status of the already verified technical-trust-context, authorized root, and named technical closures; package-kind and constitutional boundaries; and collision/no-overwrite preconditions. A verification result under a different checkpoint is stale, mismatched, or inapplicable. Multiple incompatible checkpoints presented as applicable to one evaluation MUST fail closed pending governance adjudication. Admission MUST NOT rerun, redefine, or silently replace the verifier-owned checkpoint-relative technical-conformance result.

Admission outcomes are:

- `authorized`: successful, unconditional, and insertion-ready, with no outstanding conditions;
- `denied`: insertion prohibited;
- `deferred`: insertion prohibited pending new or completed evidence.

A conditional decision with unresolved conditions is not successful authorization. If conditions are used operationally, they MUST be satisfied before a final `authorized` attestation is issued.

The admission authority MUST NOT manufacture, alter, suppress, or rewrite the independent verifier's result. Successful verification MUST NOT compel admission. Admission status does not determine technical fingerprint validity.

Immediately before insertion, the gate MUST fail closed if the exact admission-bound checkpoint or admission policy, or an explicit governance event recognized by that policy, establishes that any bound authority, contract, evidence, or identity has become unavailable, been superseded, been withdrawn, expired under its governing contract, ceased to resolve immutably, or become inconsistent with the staged artifact. Ambient branch movement, timestamps, or an unpinned later checkpoint MUST NOT silently redefine this evaluation. Renewed verification or admission MUST occur as applicable.

An `authorized` result permits an insertion attempt for the exact verified artifact. It does not prove that insertion, repository reconciliation, Git publication, PostgreSQL projection, export generation, or export verification later succeeds. After canonical insertion or publication, later contradiction, weakening, withdrawal, currentness, or supersession MUST remain a separately governed lifecycle event and MUST NOT rewrite the immutable predecessor.

## 12. Combined record structure and authority separation

KnowledgeForge accepts one future external record class, provisionally named:

`FinalPackageVerificationAndAdmissionAuthorizationRecord`

The name MAY be refined only if existing terminology supplies a clearer name without collapsing verification and admission. One physical record MAY contain both attestations; no new service or registry is required by this decision.

The record MUST remain outside the fingerprinted package. A successful record MUST exist in finalized form before canonical insertion and MUST contain two semantically, logically, and authoritatively distinct attestations:

1. independent verification attestation;
2. admission authorization attestation.

Their identities, authorities, inputs, outcomes, completion times, and content digests MUST remain independently distinguishable.

### 12.1 Shared immutable binding

The future record contract MUST bind:

- record kind and version;
- a content-bound record identity or an identity with immutable deterministic resolution;
- package ID;
- complete Package Content Fingerprint v1 descriptor and value;
- serialized-artifact digest;
- final-package construction-authorization identity and its admission-policy evaluation;
- fingerprint-specification identity, media type, and exact SHA-256, plus any required accepted no-semantic-change decision identity, digest, and Git commit, and accepted resolution-profile identity and exact digest;
- exact `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, including repository identity, commit, root-tree identity, governed evidence-subtree identities, profile identity/digest, fixed release-authority-family identity, governed namespace/enumeration identity, accepted-release evidence-closure identity, complete candidate sets, checkpoint-current release and derived lineage or exact unresolved designation, and verification mode; checkpoint-qualified ResolverTrustRelease identity/digest when resolved; exact conformance-suite identity/media type/digest and implementation-conformance-evidence identity/digest; all applicable acceptance, withdrawal, supersession, disposition, adjudication, and reactivation decision identities/digests; verifier-invocation authorization identity/digest and exact checkpoint/family/mode binding; selected release lineage, genesis, sequence, predecessor, and authorized root only when derived after complete resolution;
- `package_technical_contract_closure` identity;
- `fingerprint_verification_procedure_closure` identity;
- `admission_policy_closure` identity;
- admission-policy identity and version;
- record status.

Opaque mutable identifiers alone are insufficient.

### 12.2 Independent verification attestation

The verification section MUST include:

- verifier identity;
- verifier authority or role identity;
- verification implementation identity and version;
- verification outcome;
- verification-completion time;
- verification-attestation identity or content digest;
- binding to the shared artifact tuple; fingerprint-specification identity, media type, and exact SHA-256; exact `technical_trust_context`; authorized root; `package_technical_contract_closure`; and `fingerprint_verification_procedure_closure`, including equality between the recorded fingerprint-specification digest and that closure's fingerprint-specification explicit root;
- exact checks performed;
- blockers and failure reason where not successful.

### 12.3 Admission authorization attestation

The admission section MUST include:

- admission-authority identity;
- admission role or authority identity;
- admission-policy identity and version;
- admission outcome;
- admission-authorization time;
- admission-attestation identity or content digest;
- explicit reference to the completed successful verification attestation;
- binding to the same artifact tuple and exact technical-trust-context tuple, including the fingerprint-specification descriptor, exact governance checkpoint, accepted-release evidence closure, checkpoint-qualified designation, and applicable lineage evidence; explicit reference to the verifier-owned technical closures without redefining them; and binding to the exact `admission_policy_closure`;
- denial or deferral reasons where applicable.

The record MUST contain immutable ordering evidence proving verification completed before admission authorization. Separate attestation timestamps are mandatory unless a later accepted contract provides an equally deterministic immutable ordering mechanism.

### 12.4 Minimum role and authority rules

For the same artifact:

- the artifact producer or finalizer MUST NOT serve as its independent verifier;
- the verifier MUST NOT issue its admission authorization;
- the admission authority MUST NOT alter, replace, manufacture, or suppress verifier-owned evidence;
- verification success MUST NOT compel admission;
- admission MUST NOT convert failed or incomplete verification into success.

Different services, organizations, and cryptographic signatures are not required by this architecture; they remain implementation choices.

Only an `authorized` admission attestation may finalize the successful combined record used for insertion. Denied, deferred, failed, or incomplete attempts MUST remain distinguishable failure or decision evidence and MUST NOT be represented as successful authorization records.

The successful pre-insertion record MUST NOT claim insertion success, repository reconciliation success, Git commit identity, publication success, PostgreSQL projection success, export-generation success, or export-verification success.

### 12.5 Authority-record placement remains closed

This specification does not invent the final authority-record path. Operational admission remains blocked until a future record/repository contract settles:

- path and naming;
- whether the record is canonical repository metadata or adjacent immutable governance evidence;
- collision and no-overwrite behavior;
- content identity and deterministic resolution;
- repository-fingerprint, manifest, and index participation;
- deterministic discovery and reconciliation validation;
- retention, failed-publication treatment, and recovery treatment.

Under that future contract, the finalized successful record MUST participate in the same logically atomic canonical transition and later Git publication boundary as the admitted package. No package may be admitted operationally under this architecture before this dependency is closed.

## 13. Stage-9 canonical-transition preparation and materialization

Stage 9 may begin only after unconditional `authorized` admission and a final stale-authority check. It MUST prepare and materialize the complete admitted transition behind a non-canonical reader-visibility gate. Stage 9 does not make the next state canonically visible and does not complete canonical insertion.

The prepared transition MUST include, as applicable under the future repository contract:

- the exact admitted package bytes;
- the finalized successful verification/admission authority record;
- required evolution metadata;
- deterministic indexes;
- deterministic manifest state;
- expected repository-fingerprint or equivalent reconciliation-identity material;
- every other repository-contract-required component.

The prepared transition MUST be append-only, preserve existing predecessors without mutation, reject same-package-ID/different-content and unexpected-pre-existence collisions, and fail closed on overwrite, stale authority, identity, digest, contract, or authorization mismatch. It MUST install the exact admitted staged bytes unchanged. No parsing and reserialization, normalization, repair, overwrite, or implicit successor creation is authorized.

Future implementations MAY use staging plus atomic replacement or a transactionally enforced reader gate, but this specification does not select the mechanism. A manifest-last protocol conforms only if every canonical reader enforces that manifest as the visibility gate. Arbitrary sequential writes followed by best-effort rollback MUST NOT be called atomic. Materialized files remain non-canonical until successful stage 10; canonical readers and downstream processes MUST be unable to consume them as canonical.

The current `tools/knowledge_repository.py` implementation does not satisfy this future non-canonical preparation, exact-byte, or logical-atomicity boundary and remains unchanged and nonconforming.

## 14. Stage-10 read-back, reconciliation, and canonical visibility completion

While the complete previous state remains the only canonically visible state, stage 10 MUST read back and reconcile the prepared next state:

- exact prepared package bytes against the admitted serialized-artifact digest and admitted staged bytes;
- finalized authority record and its bindings;
- prepared `knowledge_repository/manifest.json` state;
- applicable deterministic indexes;
- required evolution metadata;
- resulting repository fingerprint or equivalent reconciliation identity and package set;
- predecessor immutability and absence of unauthorized paths.

Only after every stage-10 check succeeds under the accepted repository contract may one logically atomic visibility switch expose the complete next state, retire the previous state as current, and complete canonical insertion. Logical atomicity has one conformance meaning: readers and downstream processes observe either the complete previous canonical state or the complete next canonical state, never an intermediate state. A materialized or otherwise directly visible object file before this switch does not establish canonical membership.

If any stage-10 check fails, the visibility switch MUST NOT occur, canonical insertion MUST NOT be claimed complete, and the previous state MUST remain the only canonical state. Partial materialization remains non-canonical residue. Retention, quarantine, repair, or cleanup follows separately governed future recovery contracts. Reconciliation failure cannot occur after the transition is considered canonical because successful reconciliation is a prerequisite to the sole canonical-visibility switch.

The exact transaction mechanism, repository reader gate, visibility switch, recovery protocol, authority-record location, and reconciliation implementation remain closed implementation-contract dependencies. Stage 11 Git publication MUST NOT begin before successful stage-10 completion.

Future conformance vectors MUST include at least: stage-9 materialization followed by stage-10 failure, proving no visibility switch and only the previous canonical state; successful stage-10 reconciliation followed by exactly one atomic visibility switch; attempted canonical visibility before all stage-10 checks succeed, which MUST fail closed; and attempted stage-11 publication before stage-10 canonical insertion completion, which MUST fail closed.

## 15. Git publication and commit-tree proof

Git publication occurs only when the complete authorized repository transition is committed to Git and the actual resulting commit tree is independently checked. Pre-commit working-tree inspection alone is insufficient.

The publication verifier MUST establish at minimum:

- the expected parent commit;
- the exact allowlisted path set;
- the exact admitted package bytes;
- the exact finalized authority record;
- expected repository-transition metadata;
- expected manifest and repository identity;
- no unauthorized paths;
- no missing required paths.

The immutable commit and verified commit-tree contents provide publication proof. The commit ID is the external publication-event identity. It MUST NOT be embedded in or predicted by the pre-insertion authority record because the commit does not yet exist. That record also MUST NOT claim future insertion, reconciliation, publication, PostgreSQL, export-generation, or export-verification success.

Commit creation MUST NOT make invalid, unverified, unauthorized, or inconsistently inserted content valid. No separate publication-receipt record is accepted; it would duplicate Git identity.

Remote push is distribution, not admission or Git publication. A verified remote ref MAY prove distribution. Off-host durability and machine-loss durability remain separate from Git publication. A local-only commit MUST NOT be represented as off-host durable when the host remains the only copy.

## 16. PostgreSQL projection

PostgreSQL MUST remain a derived operational projection of canonical repository state. It MUST NOT originate admission, mutate canonical knowledge, replace the verification/admission record, or become authoritative merely because its payload reconciles with repository files.

For a conforming future-native production flow, projection MUST occur only after successful Git publication and commit-tree verification. A separately authorized prepublication projection used for testing MUST be labelled non-authoritative, non-production, preview-only, and nonconforming with the completed native-v1 production sequence. It MUST NOT establish admission, insertion, publication, consumer export publication, or retroactive proof of any earlier stage.

A future authorized projection MAY expose package identity, Package Content Fingerprint v1, exact payload fidelity, projection payload hashes, legacy classification, admission status, insertion status, Git-publication status, and external verification state. These status dimensions MUST remain distinct.

Projection failure MUST NOT mutate or invalidate an otherwise valid canonical package. It MUST survive as derived operational failure evidence and MAY be retried without a new package identity when canonical content is unchanged.

## 17. Export generation and independent verification

Exports MUST remain versioned derived consumer representations. Export generation or materialization MUST occur after the applicable Git-published canonical state and required production projection are available. Independent export verification MUST then evaluate the generated export against its governing export contract as a distinct later event.

An export MUST NOT authorize admission, redefine canonical package identity, mutate package content, treat query/result/content fingerprints as Package Content Fingerprint v1, or make failed verification, admission, insertion, publication, or projection valid.

Relationship Export Contract v1 remains unchanged. Exposure of native-v1 identity requires a separately authorized compatibility decision or successor export contract. A preview projection MUST NOT be used for consumer export publication.

Export-generation or verification failure MUST preserve canonical state, MUST be recorded as a derived-interface failure, and MAY be retried without a new package identity when canonical content is unchanged.

## 18. Failure and rejection paths

Operational failure MUST NOT automatically be classified as substantive negative knowledge.

| Failure state | Final package exists? | Canonical knowledge exists? | Evidence that MUST survive | Retry and identity rule |
| --- | --- | --- | --- | --- |
| Candidate ineligible | No final package | No | Candidate assessment, scope, reasons, validator/policy identity | MAY retry only after prerequisites or scope change; new candidate identity is required when candidate identity inputs materially change. |
| Candidate validation failed | No final package | No | Candidate identity, checks, failures, blockers | MAY retry unchanged candidate after deterministic defect correction or blocker resolution; new identity follows candidate contract if inputs change. |
| Construction authorization denied, deferred, withdrawn, or expired | No authorized final package | No | Immutable construction-authorization decision and rationale | MAY be reconsidered by a new decision; a changed candidate requires a new candidate identity. Expired authorization requires renewed authority. |
| Construction failed | No complete final package | No | Construction-attempt evidence sufficient for audit | MAY retry; new package identity is required only when governing package identity rules say the constructed content/scope changed materially. |
| Fingerprint derivation failed | No valid final native-v1 package | No | Failure class, governing inputs, and safe artifact-attempt identity | MAY retry after correction; a materially changed proposed package follows package identity rules. Failed claimed values MUST remain untrusted. |
| Final verification failed | A frozen purported package exists, but no valid/admitted package | No | Exact staged-artifact digest, checks, verifier identity, blockers, and untrusted claims clearly marked | MAY retry the identical bytes with corrected verifier dependencies; changed bytes require a new artifact digest and re-verification, and may require a new package identity. |
| Admission denied or deferred | A successfully verified artifact may exist | No | Verification attestation, admission attestation, policy, reasons, and limitations | MAY seek a new admission decision after policy/context changes; changed bytes require new verification and authorization. |
| Insertion collision | An admitted staged artifact exists | Existing canonical knowledge remains; the new artifact is not inserted | Admission record, existing/new identities, collision evidence | Retry is permitted only after resolving identity/content conflict without overwriting; same ID/different content normally requires a new valid package identity or rejection. |
| Stage-9 materialization or stage-10 reconciliation failure | An admitted staged artifact exists; local partial materialization may exist as non-canonical residue, but no visibility switch or completed insertion exists | The complete previous repository state remains the only canonical state | Exact attempted transition, affected paths, read-back/reconciliation results, quarantine/recovery state | MUST NOT switch visibility or attempt stage 11; MAY retry only after repository consistency is restored and exact admission remains valid; changed bytes require new verification/admission. |
| Git publication failed | Canonical insertion may be complete locally | Local canonical materialization may exist, but Git publication is incomplete | Repository transition, admission evidence, Git failure, intended allowlist | MAY retry publication of the unchanged complete transition without a new package identity or admission; changed package bytes require new verification/admission. |
| Remote push failed | Immutable local publication commit exists | Canonical package and local Git publication may exist; off-host distribution/durability is incomplete | Commit ID, remote/ref target, push failure | MAY retry distribution of the same commit; no new package identity or admission is required. |
| PostgreSQL projection failed | Yes, if prior gates succeeded | Yes | Projection identity, source repository fingerprint, failure and reconciliation evidence | MAY retry projection; no new package identity or admission is required when canonical content is unchanged. |
| Export generation or verification failed | Yes, if prior gates succeeded | Yes | Export contract/query identity, source projection/repository identity, failure evidence | MAY retry export; no new package identity or admission is required when canonical content is unchanged. |
| Later contradiction or supersession | Yes | Predecessor remains immutable canonical knowledge under its historical scope; currentness may change externally | Contradiction/supersession evidence, predecessor identity, successor/event identity and authority | MUST NOT mutate the predecessor. A changed package requires the separately governed successor identity and admission flow. |

Failed verification, denied or deferred admission, repository-transition failure, reconciliation failure, and Git-publication failure MUST produce or preserve evidence sufficient for diagnosis and governance. Unvalidated package IDs or fingerprints MUST be labelled as claimed identities, not validated keys. Failed staged artifacts do not become Knowledge Objects, and failure evidence MUST NOT be used as proof of canonical admission.

The successful combined authority record, failed-verification evidence, denied/deferred-admission evidence, repository-transition failure evidence, and publication-failure evidence are distinct evidence classes and need not share one schema. Failure evidence remains non-canonical unless admitted through a separate applicable path. Its storage location, retention period, immutable identity, and recovery handling remain a closed failure-evidence contract dependency; this specification does not select a storage service or database design. A rejected or failed attempt becomes reusable negative knowledge only through a separately applicable knowledge-package and admission path.

## 19. Legacy compatibility

The measured 2026-07-15 corpus contains:

- 521 packages with populated promotion history;
- four statistical packages with empty promotion history;
- 35 relationship packages without package-local promotion;
- five invalid legacy manifests;
- 35 containing-package mirrors;
- 33 stale containing-package mirrors;
- zero native Package Content Fingerprint v1 packages.

These counts describe the measured legacy corpus and do not transform it.

All existing bytes MUST be preserved. KnowledgeForge MUST NOT:

- backfill promotion histories;
- create retroactive verification/admission records;
- reinterpret Git publication as native-v1 admission;
- rewrite invalid manifests;
- create successors merely for representational uniformity;
- treat stale containing-package mirrors as authoritative;
- reclassify a current package as native-v1-valid without the future native flow.

Existing campaign decisions, package-local promotion histories, legacy manifests, and publication records remain historical evidence under their original contracts. Compatibility classifications MUST remain external and descriptive.

The five anomalous packages may remain historically accepted under their original governance while not being technically valid under the future native-v1 fingerprint contract. Historical acceptance and native-v1 technical validity are separate classifications.

## 20. Implementation prerequisites

This specification does not authorize implementation. Before implementation work begins, KnowledgeForge MUST issue separate bounded implementation authorization. Before any implementation may claim native-v1 conformance or receive production authorization, KnowledgeForge MUST separately:

1. implement and independently validate the accepted Governing Contract Resolution Profile v1 through exact machine-readable trust-release, governance-checkpoint, governed-namespace/enumeration, Git-tree completeness-proof, accepted-release evidence-closure, contract-manifest, technical closure, vocabulary, selector, verifier-invocation, and conformance contracts uniquely bound to the fingerprint specification;
2. standardize the final-package construction-authorization contract;
3. define the `FinalPackageVerificationAndAdmissionAuthorizationRecord` contract with shared artifact and complete governing-contract bindings, independently identifiable attestations, timestamps, ordering proof, and minimum role rules;
4. define content-bound or immutable deterministic record and attestation resolution;
5. settle authority-record path, naming, canonicality class, collision behavior, fingerprint/manifest/index participation, discovery, reconciliation, retention, failed-publication treatment, and recovery;
6. define separate failure-evidence identity, storage, retention, and recovery rules without treating unvalidated claims as validated keys;
7. implement and independently validate strict parsing, RFC 8785 conformance, and the complete required conformance vectors;
8. implement exact-byte-digest-bound non-canonical staging and exact-byte-preserving insertion;
9. define and implement one logical repository transition boundary, canonical-reader gate, transaction mechanism, quarantine/recovery protocol, and deterministic reconciliation;
10. implement Git publication allowlisting and verification of the actual resulting commit tree;
11. reconcile the successor native-v1 package contract with external post-fingerprint status and lifecycle truth;
12. prove no-overwrite, collision handling, stale-authority rejection, predecessor immutability, read-back, projection derivation, export-generation separation, and independent export verification;
13. receive separate implementation, production, and publication authorization.

The successor native-v1 package contract MUST resolve package-local fields whose timing and authority remain ambiguous, including maturity, governance review state, truth state, confidence, lifecycle/currentness, and evidence-integrity assertions whose timing remains ambiguous.

Claims whose truth arises after technical fingerprint verification, admission, insertion, Git publication, projection, export generation, or export verification MUST remain external to the immutable package. Future packages MUST NOT contain package-local claims that those later events have already succeeded. Later contradiction, weakening, withdrawal, currentness, and supersession MUST NOT mutate predecessors.

This document does not settle the complete lifecycle model.

## 21. Explicit non-goals

This accepted architecture does not:

- implement candidate validation, final-package construction authorization, fingerprinting, staging, verification, admission, insertion, reconciliation, Git publication, projection, export generation, export verification, or later lifecycle handling;
- create an executable schema, registry, service, database object, admission record, or publication receipt;
- select cryptographic signing or attestation infrastructure;
- authorize production package generation or Git publication;
- modify current package, repository, PostgreSQL, or export state;
- redesign the Knowledge Repository;
- make PostgreSQL canonical or writable by consumers;
- change Relationship Export Contract v1;
- settle the complete package lifecycle, truth, maturity, confidence, governance, or currentness model;
- repair or normalize legacy packages;
- redesign another EIP project;
- require a graph database or new orchestration subsystem.
