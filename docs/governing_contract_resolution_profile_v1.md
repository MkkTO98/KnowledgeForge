# KnowledgeForge Governing Contract Resolution Profile v1

Date: 2026-07-16
Status: normative architecture for future native-v1 resolution; not implemented; not production-authorized
Specification identifier: `knowledgeforge_governing_contract_resolution_profile_v1@1.0`
Contract manifest format identifier: `knowledgeforge_governing_contract_manifest_v1@1.0`
Resolver trust release identifier: `knowledgeforge_resolver_trust_release_v1@1.0`
Closure identity specification: `knowledgeforge_contract_closure_identity_v1@1.0`
Applicability: future native Package Content Fingerprint v1 packages only

Normative terms in this document are `MUST`, `MUST NOT`, `SHOULD`, and `MAY`.

## 1. Purpose and status

This specification defines the future Governing Contract Resolution Profile v1 for Package Content Fingerprint v1. KnowledgeForge accepts one architecture:

> Externally Pinned Governance Checkpoint + Checkpoint-Derived Resolver Trust Release + Package-Rooted Closed Dispatch DAG

The fingerprint specification supplies a fixed, hash-covered package-contract bootstrap. This profile governs deterministic contract resolution, external root authority, closed dispatch, typed dependency traversal, technical closure identity, and the verifier-owned technical-trust context.

This document is normative architectural documentation. It is not a machine-readable contract, implementation, or production authorization. Native-v1 derivation and verification MUST fail closed until every required machine-readable schema, vocabulary, artifact, conformance vector, implementation, independent-validation gate, and production authorization identified here has been separately accepted and completed.

This specification does not change Package Content Fingerprint v1's authoritative field, four-member descriptor, parser rules, RFC 8785 canonicalization, SHA-256 algorithm, safe-integer boundary, Unicode treatment, exact root `/fingerprints` exclusion, package-ID binding, semantic-role rules, or fingerprint hash boundary.

No current producer, validator, repository writer, PostgreSQL projection, export, package, contract artifact, trust release, or verification record is claimed to implement this profile.

## 2. Authority and precedence

Authority is domain-specific and MUST NOT be generalized beyond these boundaries:

1. `docs/package_content_fingerprint_v1.md` governs the Package Content Fingerprint v1 algorithm, strict package parsing, descriptor, canonicalization, digest, hash boundary, package-ID binding, and technical fingerprint recomputation.
2. This specification governs contract-manifest interpretation, ResolverTrustRelease validation, external technical trust selection, root authorization, closed dispatch, typed dependency closure, rule-domain delegation, and closure identity.
3. `docs/promotion_verification_admission_publication_sequence_v1.md` governs ordering and authority boundaries among construction, staging, verification, admission, insertion, publication, projection, export, and lifecycle events.
4. A separately accepted admission policy governs construction-authorization sufficiency, admission eligibility, stale-authority evaluation, collision/no-overwrite policy, and repository-transition prerequisites. It MUST NOT redefine technical fingerprint validity.
5. Separately accepted projection and export contracts govern derived PostgreSQL and consumer representations. They MUST NOT redefine canonical package identity, technical validity, or earlier authority.

If documents appear to conflict, the document authoritative for the disputed domain controls. No document may silently override another outside its declared domain. Cross-domain changes require an explicit accepted decision identifying every affected specification and whether a new technical identity is required.

This specification narrowly clarifies earlier wording that treated final-package construction authorization as a required input to the technical fingerprint predicate. Construction authorization authorizes only stage 4 construction of complete final semantic package content. Its exact identity is a required binding and process-lineage input to stages 5 through 7, but required identity binding grants no authority over those later events and does not determine deterministic technical fingerprint validity. Admission governance evaluates the authorization's legitimacy, scope, currentness, expiry, withdrawal, and sufficiency.

## 3. Applicability and non-retroactivity

This profile applies only to future packages created under a separately authorized native-v1 implementation that explicitly declares conformance to:

- `knowledgeforge_package_content_fingerprint_v1@1.0` or an explicitly accepted successor bound to this profile;
- `knowledgeforge_governing_contract_resolution_profile_v1@1.0`;
- `knowledgeforge_promotion_verification_admission_publication_sequence_v1@1.0` or an explicitly accepted successor.

It MUST NOT be applied retroactively. Existing package bytes, package-local `promotion` histories, legacy `fingerprints.package_manifest` values, campaign evidence, Git commits, PostgreSQL rows, and export artifacts remain governed by their historical contracts.

The architecture introduces no legacy resolution profile and authorizes no legacy package migration, repair, reserialization, reclassification, successor, or lifecycle change.

## 4. Core architecture and boundaries

A conforming future-native resolver MUST preserve these boundaries:

1. The fingerprint specification defines the fixed package bootstrap.
2. A package hash-covers one root package-contract descriptor.
3. Root digest equality proves exact artifact bytes, not KnowledgeForge authority.
4. One immutable checkpoint-qualified `ResolverTrustRelease`, uniquely selected by the externally pinned governance checkpoint's proven-complete accepted-release evidence closure, authorizes exact root-manifest digests for one verification; unresolved or non-unique selection MUST fail closed.
5. The package cannot select, downgrade, replace, extend, or authenticate its trust release.
6. The resolver profile defines stable resolution semantics and does not enumerate routine authorized roots.
7. Trust releases evolve the authorized root inventory without changing resolver semantics.
8. The root contract contains or digest-references one closed dispatch contract.
9. Dispatch maps validated authoritative typed selectors to exact contract-manifest digests.
10. Selected manifests form a finite typed dependency directed acyclic graph.
11. Applicability is not discovered by ambient scanning.
12. No mandatory package-local contract lock is used.
13. Technical validity remains separate from construction authorization and admission.
14. Verification, admission, insertion, publication, projection, export, and lifecycle remain distinct.
15. No service, network registry, PostgreSQL authority, or mutable-main lookup is introduced.
16. The architecture applies only to future native-v1 packages.

## 5. Fixed hash-covered bootstrap

Every purported native-v1 package MUST carry exactly the bootstrap descriptor defined by `docs/package_content_fingerprint_v1.md` at:

`/governing_contracts/package_contract`

The fingerprint specification remains authoritative for the descriptor's exact member set, types, strict package parsing, and hash boundary. Root `/governing_contracts` remains hash-covered because Package Content Fingerprint v1 excludes exactly root `/fingerprints` and no other root member.

The bootstrap identifies one exact root package-contract manifest by:

- logical contract ID;
- contract version;
- media type;
- exact-byte SHA-256 content digest.

The descriptor does not identify or authorize a ResolverTrustRelease. A package-local field purporting to select fingerprint-specification bytes, a profile, trust release, governance decision, release sequence, currentness policy, or acceptance commit MUST NOT affect trust selection.

Contract ID, version, kind, media type, filename, repository path, Git branch, or matching digest syntax cannot substitute for exact-byte digest verification and external root authorization.

## 6. Normative resolution and verification order

A conforming resolver and verifier MUST perform these technical steps in order:

1. Strictly parse the exact frozen package bytes with duplicate visibility preserved.
2. Reject a UTF-8 BOM, malformed UTF-8, malformed JSON, trailing non-whitespace data, parser recovery, escaped-equivalent duplicate keys, prohibited JSON numbers, non-finite values, out-of-range integers, and malformed Unicode.
3. Validate the exact root package-contract bootstrap under the fingerprint specification.
4. Receive the exact fingerprint-specification artifact, resolver profile, conformance-suite artifact and implementation-conformance evidence, fixed authority-family identity, complete authority-family checkpoint evidence, acceptance evidence, applicable governance-event evidence, externally pinned `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, governed Git-tree material, immutable verifier-invocation authorization, and immutable contract-artifact bundle as external inputs.
5. Before applying any package-selected root rule, verify the exact fingerprint-specification and conformance-suite identities, media types, and digests; require the fingerprint-specification digest to equal the fingerprint-specification explicit-root digest in `fingerprint_verification_procedure_closure`; validate exact implementation-conformance evidence against the release-bound suite; validate accepted same-identity transition evidence; prove complete cross-genesis checkpoint enumeration; derive the accepted-release evidence closure and exactly one checkpoint-current ResolverTrustRelease or an unresolved result; then verify the exact profile, family, checkpoint, release, acceptance, invocation, and applicable governance-event evidence.
6. Locate the package-selected root manifest by exact SHA-256 in the supplied artifact bundle.
7. Verify root exact-byte identity, structural conformance, and external authorization.
8. Evaluate the root's closed dispatch contract against validated authoritative package selectors.
9. Resolve every mandatory typed dependency edge into a finite closed DAG.
10. Validate the complete package under the resulting technical contract closure.
11. Validate the package ID under that closure and require equality with the separately claimed package ID.
12. Recompute Package Content Fingerprint v1 exactly as specified by the fingerprint specification.
13. Require exact equality with the carried four-member descriptor.
14. Produce a verifier-owned technical result bound to the exact artifact, trust context, package closure, and verification-procedure closure.

A root MUST be externally authorized before its dispatch or other root-authored validity rules are executed. A package cannot bootstrap authority by supplying internally consistent rules that authorize itself.

This is the independent technical-verification order for an exact frozen artifact. The earlier construction-time derivation operation MAY use exact profile-governed contract artifacts to calculate and attach a purported descriptor without claiming external root authority or native technical validity. Successful verification still requires every step above. This distinction permits later external root acceptance before verification without retroactively converting an earlier attempted verification into success.

## 7. Cycle and self-reference prohibitions

The following are prohibited:

- a contract rule whose validity depends on the Package Content Fingerprint v1 value it helps calculate;
- a manifest member that claims the manifest's own exact-byte digest;
- a dependency or dispatch edge from a contract artifact to the package artifact;
- a contract edge to verification, admission, insertion, publication, PostgreSQL projection, export, or lifecycle records;
- fixed-point searching, repeated hashing until stability, self-signing authority, or recursive identity removal;
- treating a package-local trust-release reference as external authority.

Manifest and payload digests belong in the parent manifest, dispatch record, trust release, closure description, or external attestation whose hashed boundary does not contain its own stored digest.

The fingerprint specification does not contain or predict its own exact artifact digest. The externally accepted ResolverTrustRelease binds the identity, media type, and exact SHA-256 of the already-finalized and published fingerprint-specification artifact that it authorizes.

## 8. Resolver-profile semantics and identity

The immutable technical semantics identified by `knowledgeforge_governing_contract_resolution_profile_v1@1.0` cover:

- root-manifest and contract-manifest interpretation;
- supported artifact media types;
- ResolverTrustRelease structure and validation;
- closed dispatch grammar;
- authoritative selector grammar;
- dependency-edge vocabulary;
- finite DAG traversal and cycle rejection;
- rule-domain ownership;
- one-way exclusive delegation;
- collision and conflict behavior;
- closure-identity construction;
- strict failure behavior.

The profile MUST NOT enumerate routine authorized roots. Root inventory belongs only to an externally accepted ResolverTrustRelease.

A semantic change to manifest interpretation, media-type behavior, trust-release validation, selector semantics, dispatch, dependency traversal, delegation, conflict handling, or closure identity requires:

- a new resolver-profile identifier or version; and
- under the accepted one-profile-per-fingerprint-conformance rule, a successor fingerprint conformance identity explicitly bound to the new profile.

No technical semantic change may occur silently under an existing identifier/version. Editorial prose changes do not alter technical identity only when an accepted decision explicitly establishes that no technical semantics changed. Every editorially changed artifact nevertheless has a new exact digest and requires a new ResolverTrustRelease before that revised artifact is authorized for verification.

## 9. ResolverTrustRelease

### 9.1 Sole new authority artifact class

KnowledgeForge accepts exactly one new root-authority artifact class:

`ResolverTrustRelease`

Its logical specification identifier is:

`knowledgeforge_resolver_trust_release_v1@1.0`

This profile fixes exactly one governed release-authority family for native Package Content Fingerprint v1:

`knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`

The authority-family identity is a stable governed identity and selection scope fixed by this profile and the applicable `fingerprint_verification_procedure_closure`. It is not an artifact, mutable registry, service, database object, package field, invocation-selected namespace, or second root authority. An invocation MUST bind this exact expected identity for consistency and MUST fail closed on a missing, unknown, or different identity; it cannot choose among families. V1 has no alternative family. Supporting multiple authority domains requires a separately accepted successor architecture with explicit applicability and non-overlap rules.

A ResolverTrustRelease MUST be:

- identified by SHA-256 over its exact bytes;
- immutable;
- Git-backed;
- externally accepted;
- Git-published before any successful technical verification that depends on it;
- retained permanently;
- a complete authorized-root snapshot, not a delta;
- independent of package content;
- selected by the checkpoint-derived closure in checkpoint-current mode, or designated only as an exact consistency assertion against immutable historical evidence in historical mode;
- bound to exactly one resolver profile.

This architecture does not create its machine-readable schema or an actual release.

### 9.2 Required architectural members

A future machine-readable ResolverTrustRelease MUST bind at least:

- specification identifier;
- release-authority-family identity, exactly `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`;
- release ID;
- release sequence;
- predecessor release digest or explicit genesis value;
- fingerprint specification identifier;
- fingerprint specification media type;
- fingerprint specification exact SHA-256;
- whenever that identifier already has an accepted published specification artifact with a different digest, including in a genesis release, accepted no-semantic-change decision identity, exact digest, and Git commit binding the predecessor and successor specification digests;
- resolver-profile identity;
- resolver-profile version;
- resolver-profile media type;
- resolver-profile exact SHA-256;
- conformance-suite identity;
- conformance-suite media type;
- conformance-suite exact SHA-256;
- complete authorized-root array.

Each authorized-root entry MUST bind:

- logical contract ID;
- contract version;
- contract kind;
- media type;
- exact SHA-256;
- allowed package kind or kinds;
- allowed technical scope or scopes.

A release-local `release_lineage_identity` or genesis reference is immutable structural metadata for validating that release's claimed predecessor chain. It has no authority to partition the family, narrow checkpoint evidence, or select currentness. The verifier recomputes graph relations across the complete family closure and records a selected release lineage as technical output only after unique current-head resolution; any mismatch between claimed structural metadata and that derivation fails closed.

The final schema, member names, closed vocabularies, and media types remain implementation gates.

### 9.3 One release-authority family and deterministic release state

All releases for native Package Content Fingerprint v1 belong to the one authority family `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`. The checkpoint namespace MUST enumerate every governed release and governance event in that family before release resolution. A genesis digest or release-lineage identity MUST NOT key, narrow, filter, or pre-partition the checkpoint boundary, governed namespace, evidence closure, or checkpoint-current evaluation. Release-lineage identity is derived only after the complete family graph resolves to one release. When resolution is unresolved, no single lineage identity exists; the result instead binds the complete candidate-genesis, branch, and terminal-release sets.

A release enters the accepted release graph only when exact accepted release evidence is valid at the checkpoint. Invalid, rejected, malformed, or merely proposed releases remain classified evidence but are not eligible. Genesis MUST use sequence `1` and an explicit no-predecessor value. Every accepted non-genesis release MUST bind one exact accepted predecessor digest in this authority family, increment that predecessor's sequence by exactly one, and pass predecessor-consistency rules. Sequence is a consistency property, never a selection rule.

Acceptance of a valid successor makes its exact predecessor historical, superseded, and non-current-eligible from that checkpoint onward. This consequence follows from the accepted predecessor edge, not from sequence comparison, time, or `latest`. Withdrawal makes the exact target current-ineligible from the applicable checkpoint onward but does not erase acceptance history, rewrite earlier checkpoints, reactivate a predecessor, select a replacement, or imply fallback. Once a release is historically superseded, withdrawal or disposition of its successor does not automatically reactivate it. Reactivation or rollback requires a separate explicit accepted KnowledgeForge adjudication/reactivation decision binding the exact affected releases and evidence. That decision uses existing immutable decision evidence and is not a new general artifact class.

An accepted explicit supersession or disposition decision makes its exact target current-ineligible according to its recorded scope. It selects no replacement unless it is also adequate accepted adjudication that binds all relevant competing release and acceptance-evidence digests, dispositions every alternative, and selects exactly one branch and release under this checkpoint and authority family. Contradictory, incomplete, non-exact-bound, or multiple applicable adjudications remain unresolved; none wins by timestamp, commit order, path, filename, sequence, or digest order.

Define `release_eligible_v1(C, r)` over the complete authority-family graph and complete applicable governance-event evidence at exact checkpoint `C`. It returns `true` if and only if release `r` is accepted; belongs to the fixed authority family; is supported by complete checkpoint evidence; is neither withdrawn, rejected, nor dispositioned non-current; is not historically superseded unless explicit accepted reactivation/adjudication restores it; lies on the uniquely selected branch when adequate accepted adjudication applies; and has no accepted successor that makes it historical unless explicit accepted reactivation/adjudication restores it. Every predicate input is exact-identity-bound evidence in `C`; ordering metadata and invocation expectations are not inputs.

Define `eligible_terminal_set_v1(C)` as every `r` for which `release_eligible_v1(C, r)` is `true` after all valid acceptance, predecessor, withdrawal, supersession, disposition, reactivation, and adjudication effects in `C` are applied. Define `checkpoint_current_head_v1(C)` deterministically as exactly one of:

1. if `eligible_terminal_set_v1(C)` contains exactly one release, return that exact release and derive its lineage from its exact predecessor chain;
2. if it is empty, return the identity-bound `no_current_release` unresolved result and checkpoint-current verification fails closed;
3. if it contains more than one release, return the identity-bound `conflicting_current_releases` unresolved result with the complete terminal set and checkpoint-current verification fails closed.

No highest-sequence, latest, timestamp, commit-order, filename, path, digest-order, caller, invocation, package, producer, or verifier fallback is permitted.

The authorized-root array is the complete snapshot for one release. Absence from an accepted successor means the root is not authorized for checkpoint-current verification under that successor. It does not rewrite the predecessor release, an earlier checkpoint, or a historical result. One release MAY temporarily authorize predecessor and successor roots only when package-kind and technical scopes remain non-conflicting or accepted release semantics produce one unambiguous result; ambiguity fails closed.

Within and across accepted releases:

- one logical root ID/version MUST NOT map to different digests;
- one root digest MUST NOT have inconsistent logical identity, kind, media type, or scope;
- byte-identical duplicate entries MUST be rejected rather than silently retained;
- changed root bytes require a new contract version and digest;
- a release is not authority merely because it declares itself accepted;
- roots cannot authenticate themselves or their release.

Every accepted genesis release in this family is a competing graph root. One genesis MUST NOT hide another. Multiple accepted genesis releases remain unresolved unless adequate accepted adjudication binds all candidate genesis and acceptance-evidence digests, dispositions every alternative, and selects exactly one branch and release. If checkpoint C contains accepted genesis releases G1 and G2, invocations expecting G1 and G2 MUST both enumerate G1 and G2, derive the same unresolved result absent adequate adjudication, and reject either expected-release assertion as an override. Neither invocation may preselect a lineage.

Normative release-state examples are:

- **A — linear chain:** for accepted G → A → B, G and A are historical/superseded and B is the sole terminal candidate when otherwise eligible. B is selected from exact predecessor and supersession relations, not highest sequence.
- **B — withdrawal without fallback:** for accepted G → A → B followed by withdrawal of B, B is ineligible, A remains historical/superseded, no fallback occurs, and the result is `no_current_release` unless explicit accepted reactivation/adjudication selects an exact release.
- **C — sibling fork:** for accepted G → A and G → B, G is historical/superseded and A and B are competing terminal candidates. The result is unresolved unless adequate adjudication applies.
- **D — multiple genesis:** accepted G1 and G2 are both enumerated and remain competing roots; invocation cannot exclude either, and resolution is unresolved unless adequate adjudication dispositions all alternatives and selects exactly one branch/release.
- **E — withdrawn fork branch:** for accepted G → A and G → B followed by withdrawal of B, B is ineligible, G does not reactivate, and A may be the unique terminal candidate when no other conflict or disposition applies.
- **F — conflicting adjudications:** two accepted-looking adjudications selecting different releases for the same checkpoint state remain unresolved; neither wins by time, order, path, filename, or digest, and checkpoint-current verification fails closed pending adequate later governance resolution.

Adequate accepted adjudication already contained in checkpoint C MAY resolve a fork within C. It MUST bind every applicable competing release and acceptance-evidence digest, disposition every alternative, select exactly one branch and release where resolution is intended, and be immutable, exact-identity-bound, external to package content, and Git-published inside C's governed evidence subtree. Its identity, digest, and Git commit enter the closure, `technical_trust_context`, and verification attestation. If C contains no adequate applicable accepted adjudication, C remains unresolved. A later checkpoint may contain adjudication that resolves the fork for that later checkpoint without rewriting C's immutable unresolved historical result.

## 10. External acceptance and technical trust context

### 10.1 External acceptance evidence

ResolverTrustRelease acceptance consists of all of:

1. an accepted KnowledgeForge decision that binds the exact release digest;
2. immutable Git publication containing the exact release and acceptance evidence;
3. an externally authorized verifier invocation pinning the exact governance checkpoint, exact authority-family identity `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`, and verification mode. It MAY carry an expected derived release/result only as a consistency assertion. It MUST NOT bind a genesis or lineage in a way that filters checkpoint evidence, choose among alternative families, or select or authorize the checkpoint-current release.

The release and acceptance evidence MUST be published before successful technical verification. A release's self-declaration, a package-local reference, producer configuration, mutable branch name, database row, or ambient file does not prove acceptance.

Before verification, the verifier MUST establish that the exact externally pinned governance checkpoint contains the accepted decision evidence and exact ResolverTrustRelease bytes. The checkpoint commit MUST establish the release as available and accepted before the verification attempt. Git commit timestamps, file modification times, package timestamps, current date, ambient `HEAD`, a mutable branch tip, and a `latest` alias MUST NOT be primary trust evidence. The later Git publication verifier, not the prepublication technical verifier, MUST establish that the resulting package-publication commit contains the exact verification/admission evidence required by the sequence specification. This requirement does not authorize or define a publication workflow in this task.

### 10.2 Externally pinned governance checkpoint and accepted-release evidence closure

A governance checkpoint is a composite immutable Git verification boundary, not a new general authority-artifact class, mutable registry, service, database object, package field, or package hash input. The verifier receives the checkpoint externally. The package, producer, ResolverTrustRelease, ambient repository state, mutable branch name, genesis release, and release lineage MUST NOT select or authenticate it.

A checkpoint has two nonrecursive identities:

1. a `governance_checkpoint_boundary_identity` over the immutable input boundary; and
2. a final `governance_checkpoint_result_tuple` that binds that boundary identity, the derived accepted-release evidence-closure identity, authority-family identity, and the derived selected checkpoint-current release and lineage or exact unresolved result and candidate set.

The externally pinned checkpoint tuple carries both identities and the expected derived result only as a consistency assertion. The verifier MUST independently derive the closure and result, recompute both identities, and require exact equality. The accepted-release evidence closure commits only to `governance_checkpoint_boundary_identity`, never to the final result tuple that contains the closure identity. This ordering prohibits self-reference and fixed-point hashing.

The immutable checkpoint boundary MUST bind at least:

- repository identity;
- exact Git commit;
- exact root-tree identity;
- exact governed evidence-subtree identity or identities;
- this profile's identity and exact digest;
- exact authority-family identity `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`;
- deterministic governed namespace and evidence-enumeration rules;
- verification mode: `checkpoint-current` or `historical`.

It MUST NOT bind a preselected genesis or release-lineage identity as an evidence-filtering input. The exact profile identity/digest and fixed authority-family identity MUST define one deterministic governed namespace and subtree-enumeration mapping for each `(repository identity, exact Git commit, verification mode)` tuple. Invocation authorization MUST bind the one fixed family for consistency but MUST NOT narrow, replace, partition, or choose that mapping. Two purported checkpoints using different governed scopes for the same repository, commit, profile, family, and mode cannot both conform. Any missing, duplicate, unknown, or conflicting mapping fails closed. Applying the unique mapping to the exact root tree yields the governed subtree identities.

The exact Git commit, root tree, and governed subtree identities MUST cryptographically bind the complete checkpoint-relative evidence population. The verifier MUST receive or resolve enough exact Git tree material to enumerate every entry in the governed namespace; verify all relevant tree-object identities; classify every governed release, acceptance, withdrawal, supersession, disposition, adjudication, and reactivation event deterministically; and prove that no governed entry was omitted. A caller-supplied list not proven complete against the subtree is insufficient. Paths and tree traversal define closed discovery only; they MUST NOT select among genesis releases, branches, or releases.

From that proven-complete representation, the verifier MUST deterministically derive one accepted-release evidence closure for the entire authority family. The closure MUST contain and classify:

1. every governed ResolverTrustRelease in the family, including every accepted genesis and accepted non-genesis release;
2. every applicable release-acceptance decision and its exact identity and digest;
3. all exact predecessor edges and sequence-consistency results;
4. every applicable withdrawal, supersession, disposition, adjudication, and reactivation decision and its exact identity, digest, scope, and effect;
5. the complete derived predecessor graph, candidate-genesis set, branch set, terminal-candidate set, and every detected conflict;
6. exactly one selected checkpoint-current release and its derived lineage when the current-head function returns one terminal candidate; otherwise the exact `no_current_release` or `conflicting_current_releases` classification and complete relevant candidate set.

The accepted-release evidence-closure identity MUST commit deterministically to `governance_checkpoint_boundary_identity`, authority-family identity, closed enumeration rules, sorted governed evidence identities and exact digests with evidence types, predecessor edges and sequence consistency, every acceptance/withdrawal/supersession/disposition/adjudication/reactivation effect, derived candidate-genesis/branch/terminal sets, and the selected release/derived lineage or exact unresolved classification and candidate set. The final `governance_checkpoint_result_tuple` MUST commit to the boundary identity, closure identity, authority-family identity, and same resolved or unresolved result. The closure is a derived verification result, not a mutable registry, service, database, package field, contract lock, or second general authority-artifact class.

Derivation MUST fail without producing a closure on missing governed Git-tree material; commit/tree/subtree-object mismatch; unknown governed evidence type; duplicate or conflicting identity; incomplete applicable decision evidence; malformed release; invalid predecessor; unknown/mismatched authority family; contradictory evidence classification; or inability to prove complete enumeration. A complete, consistently classified checkpoint with zero or multiple eligible terminal releases MUST instead produce and identity-bind the applicable explicit unresolved closure/result. Checkpoint-current technical verification MUST fail closed on that recorded unresolved result and MUST NOT suppress it or report a selected release.

For the same exact `governance_checkpoint_boundary_identity`, deterministic conforming verifiers MUST enumerate the same complete authority-family evidence, derive the same closure, candidate sets, selected release/lineage or unresolved classification, and `governance_checkpoint_result_tuple`. An invocation MAY carry an expected result only as a consistency assertion. An expected release, genesis, or lineage inconsistent with the independently derived result fails closed and cannot filter evidence or override the result.

If checkpoint C contains accepted siblings G→A and G→B, complete verification exposes both. If C already contains adequate applicable accepted adjudication binding all competitors and dispositioning every alternative, that adjudication MAY resolve the fork within C. If C contains no adequate applicable accepted adjudication, C remains unresolved. A later checkpoint may contain adjudication that resolves the fork for that later checkpoint without changing C's immutable unresolved result.

If checkpoint C contains accepted genesis releases G1 and G2, every invocation for C MUST enumerate both roots. Invocations expecting G1 and G2 derive the same unresolved result absent adequate adjudication; neither expectation selects a lineage or makes a release current.

For different exact checkpoints, results belong to different technical trust contexts and MUST NOT be silently substituted. Neither checkpoint is selected by timestamp, `latest`, branch state, commit order, sequence alone, or digest order. An offline verifier does not determine whether a later checkpoint exists and does not attest global currentness. Admission governance externally binds exactly one applicable checkpoint for one evaluation and separately evaluates whether that pin is legitimate, applicable, current enough, unwithdrawn, and sufficient. A result under another checkpoint is stale, mismatched, or inapplicable. Multiple incompatible checkpoints for one evaluation fail closed pending governance adjudication. Changing the checkpoint accepted for admission requires an explicit governance event.

The external checkpoint pin terminates technical trust selection. Its legitimacy is not proved by package content, the ResolverTrustRelease, another recursively required checkpoint, or the verifier. The technical verifier proves only exact checkpoint identity, complete governed-subtree representation, deterministic authority-family graph and current-head derivation, and consistency with invocation, trust context, closures, and attestation. Schema, canonical serialization, and implementation remain future gates; the completeness and fail-closed semantics here are normative now.

### 10.3 `technical_trust_context`

`technical_trust_context` is a verifier-owned external binding. It is not:

- package content;
- a fourth package closure;
- a package-local lock;
- another stored registry;
- admission authority;
- lifecycle state.

It MUST bind:

- fingerprint specification identity, media type, and exact SHA-256;
- applicable accepted no-semantic-change decision identity, exact digest, and Git commit whenever an existing fingerprint-specification identity binds bytes different from its previously accepted published artifact;
- resolver-profile identity and exact digest;
- conformance-suite identity, media type, and exact digest, plus exact implementation-conformance-evidence identity and digest;
- exact `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, including repository identity, exact Git commit, exact root-tree identity, and governed evidence-subtree identity or identities;
- exact authority-family identity `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`;
- deterministic governed namespace and evidence-enumeration-rules identity;
- derived accepted-release evidence-closure identity;
- exact checkpoint-current release digest and derived lineage when resolved, or exact unresolved classification plus complete candidate-genesis, branch, and terminal-release sets when unresolved; exact historical release/lineage designation in historical mode;
- ResolverTrustRelease identity and exact digest when selected for the applicable mode;
- every applicable acceptance, withdrawal, supersession, disposition, adjudication, and reactivation decision identity, exact digest, and Git commit;
- externally authorized verifier-invocation identity and immutable digest;
- invocation authorization's exact checkpoint, fixed authority-family, and mode binding;
- exact checkpoint-qualified release designation for the selected verification mode;
- exact derived release-lineage identity, exact genesis release digest, release sequence, and predecessor release digest or genesis marker only when a release is selected after complete resolution;
- verification mode: `checkpoint-current` or `historical`.

The package and producer MUST NOT select, substitute, weaken, or authenticate any of these values. The verification attestation MUST record the complete exact trust-context tuple.

## 11. Root authorization before rule execution

Before applying any root-authored technical rule, the verifier MUST establish:

1. the exact ResolverTrustRelease digest;
2. the fingerprint-specification bytes resolved from the supplied immutable artifact set, with exact identity, media-type, and SHA-256 equality to the release-bound descriptor;
3. equality between that verified fingerprint-specification digest and the fingerprint-specification explicit-root digest in `fingerprint_verification_procedure_closure`;
4. whenever an existing fingerprint-specification identity binds bytes different from its previously accepted published artifact, exact accepted no-semantic-change decision evidence binding the predecessor and successor specification digests and its Git commit, including for a genesis release;
5. exact equality between the release-bound and externally pinned resolver profile;
6. accepted decision evidence binding every applicable release digest and applicable lineage adjudication or disposition evidence;
7. exact `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, complete governed-subtree enumeration, derived accepted-release evidence-closure identity, invocation authorization, checkpoint-qualified release consistency, and pre-verification ordering;
8. the package-selected root's exact bytes and digest;
9. root structural conformance to `knowledgeforge_governing_contract_manifest_v1@1.0` when implemented;
10. one exact release entry matching all of:
   - root digest;
   - logical contract ID;
   - contract version;
   - contract kind;
   - media type;
   - package kind;
   - technical scope.

A structurally valid but unauthorized root MUST fail KnowledgeForge-native technical verification before dispatch. Evidence may state only:

- exact root bytes verified;
- root structure valid;
- fingerprint recomputation possibly self-consistent under self-selected rules;
- KnowledgeForge-native technical validity not established.

Root authorization is part of technical trust. It is not admission authorization.

## 12. Closed root dispatch

The root package contract MUST contain or exact-digest-reference one closed dispatch contract. Dispatch maps validated authoritative selector tuples from the complete parsed package to exact contract-manifest digests.

Profile-governed selector domains MAY include only closed typed fields such as:

- package kind;
- package schema/version;
- statement type;
- method ID/version;
- transformation ID/version;
- calculation-contract ID/version;
- evidence/reference role;
- numeric-rule family;
- fingerprint semantic role.

The root contract MUST define each authoritative selector's exact RFC 6901 pointer, type, closed value vocabulary or exact comparison domain, and combination rule.

The resolver MUST reject:

- a missing authoritative selector;
- an unknown selector value;
- duplicate authoritative selectors;
- conflicting selectors;
- a value outside a closed vocabulary;
- an inconsistent convenience mirror;
- a missing dispatched artifact;
- zero dispatch results where one is required;
- more than one dispatch result where one is required;
- any ambiguous dispatch result.

Dispatch MUST be deterministic, side-effect-free, offline, closed, non-Turing-complete, and limited in v1 to typed equality or closed set-membership operations. It MUST NOT execute arbitrary code. Regular expressions are prohibited in v1 unless a later accepted semantic-profile decision proves necessity and creates the required successor identities.

Applicability MUST NOT be discovered by scanning manifests, artifact filenames, repository paths, campaign names, producer identity, PostgreSQL, Git branches, mutable repository state, or any supplied artifact not reached by authorized dispatch and dependency edges.

## 13. Contract manifests and payloads

### 13.1 Manifest format

Each technical contract node MUST have one typed exact-byte manifest governed by:

`knowledgeforge_governing_contract_manifest_v1@1.0`

At the architectural level, each manifest MUST bind:

- logical contract ID;
- contract version;
- contract kind;
- manifest-schema version;
- mandatory typed dependency edges;
- rule-domain ownership;
- normative technical rules when directly representable;
- optional exact payload references.

The root package-contract manifest additionally owns or digest-references the closed dispatch contract.

### 13.2 Optional external payloads

An external payload MAY be used only when useful for a format-specific technical authority such as:

- JSON Schema;
- a large closed vocabulary;
- a governed table;
- a format-specific technical specification.

Every payload reference MUST bind its media type and exact SHA-256. Payload applicability arises only through an authorized manifest edge. When a payload carries normative technical authority, its digest is a closure member and its manifest-to-payload reference is a typed closure edge. A supplied payload not reached through a selected manifest reference is unreachable and excluded from the closure.

### 13.3 Identity rules

Exact-byte SHA-256 is the authority identity for manifests and payloads. No second semantic contract fingerprint is introduced.

For JSON manifests and payloads:

- bytes MUST be UTF-8;
- an initial BOM MUST be rejected;
- parsing MUST reject duplicate keys after escape decoding;
- Unicode MUST NOT be normalized;
- exact bytes, including whitespace, member order, escapes, and line endings, determine identity.

Any byte change creates a new artifact identity. A manifest MUST NOT contain its own exact-byte digest.

Historical `*_contract_fingerprint` values remain legacy semantic evidence and MUST NOT be reinterpreted as native exact-byte manifest or payload digests. Markdown prose and implementation code are not machine-executable contract authority merely because they describe accepted behavior.

## 14. Typed dependency DAG and delegation

After dispatch, every dependency MUST be a mandatory exact-digest typed edge. V1 has no optional dependency edges.

Resolution MUST enforce:

- finite closure;
- missing-node rejection;
- self-cycle rejection;
- multi-node-cycle rejection;
- unsupported schema, version, kind, or media-type rejection;
- logical identity collision rejection;
- shared dependency deduplication by exact digest;
- explicit multiple-method roots or edges where applicable;
- exclusion of unreachable supplied artifacts from technical closure.

Supplying an artifact does not make it applicable or authoritative.

### 14.1 One-way exclusive rule-domain delegation

Rule authority follows one-way exclusive delegation:

1. The resolver profile owns resolution mechanics.
2. The root package contract owns package-wide technical rule domains.
3. A parent manifest MAY delegate one bounded named domain to one child dependency.
4. The child may govern only that delegated domain and any subdomain it explicitly and validly delegates.
5. The parent MUST NOT retain conflicting rules inside a delegated domain.
6. Overlap without explicit delegation MUST fail closed.
7. No generic override, fallback authority, or warning-based conflict resolution exists in v1.

No authority or precedence may arise from load order, filename, path, digest order, “most specific wins,” implementation order, or producer convention.

## 15. Closure boundaries

This profile defines exactly three closure names.

### 15.1 `package_technical_contract_closure`

This closure contains only technical package-conformance contracts reached from exactly one authorized package-contract root through closed dispatch and mandatory dependency edges.

It MAY contain package schema, package-ID, method, transformation, calculation, evidence-role, numeric-representation, fingerprint-semantic-role, and related technical contracts.

It MUST exclude:

- final-package construction authorization;
- admission policy or outcome;
- insertion or repository-transition authority;
- Git publication;
- PostgreSQL projection;
- export generation or verification;
- later lifecycle outcomes.

### 15.2 `fingerprint_verification_procedure_closure`

This closure contains stable verification semantics, including as applicable:

- Package Content Fingerprint specification;
- resolver profile;
- ResolverTrustRelease validation rules, but not a package-selected release;
- strict parser and RFC 8785 requirements;
- serialized-artifact digest contract;
- closure-identity contract;
- verification-record contract.

Its explicit root set contains exactly the fingerprint specification and resolver profile under the accepted v1 closure model. The fingerprint-specification explicit root MUST use the same exact SHA-256 as the release-bound fingerprint-specification descriptor and the verifier-owned `technical_trust_context`; logical identity equality without exact artifact-digest equality is insufficient. Every other normative verification-procedure artifact, including any normative payload, MUST be reached through typed exact-digest edges from those roots.

It MUST NOT contain a producer-specific or verifier-specific implementation binary. Verifier implementation identity and version belong in the verification attestation.

### 15.3 `admission_policy_closure`

This closure contains governance and process-policy authority, including as applicable:

- final-package construction-authorization contract;
- admission policy;
- collision and no-overwrite rules;
- stale-authority evaluation;
- repository-transition prerequisites.

Its explicit root set contains exactly one admission-policy root. Construction-authorization, collision/no-overwrite, stale-authority, repository-transition, and any normative payload authority MUST be reached through typed exact-digest edges from that root.

It MUST NOT redefine Package Content Fingerprint v1, root structural validity, root technical authority under a recorded trust release, or technical recomputation results.

## 16. Closure identity

The closure identity specification is:

`knowledgeforge_contract_closure_identity_v1@1.0`

A closure identity is SHA-256 over RFC 8785 canonical UTF-8 JSON representing:

- closure identity specification;
- closure type;
- resolver-profile identity and exact digest;
- explicit root digests;
- sorted member digests;
- sorted typed edges including rule domain.

The representation MUST provide explicit domain separation among the three closure types. It MUST:

- reject duplicate roots, members, and edges;
- sort roots by digest;
- sort members by digest;
- sort edges lexicographically by `(from, edge_type, rule_domain, to)`;
- commit graph structure, direction, edge type, and rule domain, not merely the member set;
- use exactly one package-contract root for `package_technical_contract_closure`;
- use exactly the explicit roots fixed for each closure in Section 15;
- include normative payload digests as members and typed payload-reference edges in graph identity;
- exclude unreachable supplied artifacts;
- avoid a Merkle tree in v1.

This document does not create the machine-readable closure schema, canonical examples, or conformance vectors.

## 17. Qualified technical validity

The complete technical proposition is:

> Exact artifact A is `native_package_content_fingerprint_v1_valid` under exact fingerprint-specification artifact X, resolver profile P, exact release-bound conformance suite S and implementation-conformance evidence I, externally pinned governance checkpoint Q, checkpoint-qualified ResolverTrustRelease R, accepted-release evidence closure E, package technical contract closure C, and fingerprint-verification procedure closure V whose fingerprint-specification root equals X by exact digest.

Successful native-v1 technical verification requires:

- exact fingerprint-specification bytes whose identity, media type, and SHA-256 match the checkpoint-qualified ResolverTrustRelease and whose digest equals the procedure closure's fingerprint-specification explicit root;
- exact conformance-suite bytes whose identity, media type, and SHA-256 match the checkpoint-qualified ResolverTrustRelease, plus exact evidence that the verifier implementation conforms to that suite;
- an exact externally pinned governance checkpoint with a proven-complete governed subtree and deterministic accepted-release evidence closure;
- in checkpoint-current mode, an externally accepted ResolverTrustRelease uniquely selected as checkpoint-current by that closure; in historical mode, the exact historical release designated by the immutable historical evidence without a currentness claim;
- an authorized exact root with matching identity, kind, media type, package kind, and scope;
- a complete, finite, unambiguous technical contract closure;
- strict validation of the exact frozen descriptor-bearing artifact;
- successful Package Content Fingerprint v1 recomputation and exact descriptor comparison.

The attestation MUST bind at least:

- fingerprint specification identity, media type, and exact SHA-256;
- applicable accepted no-semantic-change decision identity, exact digest, and Git commit when required;
- resolver-profile identity and exact digest;
- conformance-suite identity, media type, and exact digest, plus exact implementation-conformance-evidence identity and digest;
- exact `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, commit, root-tree identity, and governed evidence-subtree identity or identities;
- exact authority-family identity `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`;
- governed namespace and enumeration-rules identity;
- accepted-release evidence-closure identity and checkpoint-current, historical, or unresolved designation;
- exact selected checkpoint-current release and derived lineage when unique, or exact unresolved classification with candidate-genesis, branch, and terminal-release sets; exact historical designation when applicable;
- ResolverTrustRelease identity and exact digest when selected for the applicable mode;
- every applicable acceptance, withdrawal, supersession, disposition, adjudication, and reactivation decision identity and digest;
- verifier-invocation authorization identity and immutable digest;
- invocation authorization's exact checkpoint, fixed authority-family, and mode binding;
- any expected derived result, identified only as a consistency assertion that cannot narrow evidence or override derivation;
- exact derived release-lineage identity, exact genesis release digest, release sequence, and predecessor release digest or genesis marker only when resolution selects a release;
- authorized root-manifest identity and digest;
- `package_technical_contract_closure` identity;
- `fingerprint_verification_procedure_closure` identity;
- validated package ID;
- complete Package Content Fingerprint v1 descriptor;
- serialized-artifact digest;
- verifier identity and authority role;
- implementation identity and version;
- verification mode, outcome, completion time or equivalent ordering proof, and failure reason where applicable.

Technical validity does not require valid final-package construction authorization or successful admission. Construction authorization cannot make an invalid fingerprint valid and cannot make a technically correct fingerprint incorrect.

A technically valid artifact may be denied, deferred, ineligible, unevaluated for admission, prohibited from insertion, unpublished, unprojected, unexported, contradicted later, or non-current.

## 18. Construction authorization and admission boundary

Final-package construction authorization authorizes only stage 4: construction of complete final semantic package content. Its exact identity MUST bind stage-5 derivation evidence, MUST bind stage-6 serialization and non-canonical staging evidence, and MUST accompany stage-7 verification as required process lineage. Required presence and exact identity binding grant no authority to perform Package Content Fingerprint derivation or descriptor attachment, final repository serialization, freezing or non-canonical staging, independent verification or any verification result, deterministic technical validity, admission, canonical insertion, read-back or reconciliation, Git publication, PostgreSQL projection, export generation or verification, or lifecycle action.

Stages 4 through 7 MAY occur within one bounded operational attempt, but that operational boundary does not define or expand stage-3 authority. The technical verifier MUST check and record exact equality of the construction-authorization identity across derivation evidence, serialization/staging evidence, and verification process lineage as a separate process-conformance observation. The technical verifier MUST NOT infer technical validity from the identity or evaluate construction-authorization legitimacy, scope, currentness, expiry, withdrawal, or sufficiency as part of the deterministic technical-fingerprint predicate. Admission governance MUST evaluate those properties and may deny or defer a technically valid artifact because the construction process or required lineage binding was unauthorized or nonconforming. The verification evidence or combined authority record MUST preserve the exact cross-stage process-lineage binding.

Admission remains downstream of successful technical verification. Only an unconditional `authorized` admission attestation is insertion-ready.

## 19. Checkpoint-current and historical verification modes

### 19.1 Checkpoint-current mode

Checkpoint-current verification MUST:

- receive exactly one externally pinned governance checkpoint through an immutable verifier-invocation authorization binding its exact tuple, the fixed authority-family identity, and checkpoint-current mode;
- prove complete cross-genesis enumeration of that checkpoint's governed evidence subtree and derive the entire authority-family accepted-release evidence closure;
- apply the deterministic release-state and current-head function and require exactly one eligible terminal ResolverTrustRelease;
- derive release-lineage identity only after unique release resolution;
- reject an older, package-supplied, producer-selected, unaccepted, or invocation-selected release inconsistent with the closure;
- reject zero or multiple terminal candidates, contradictory adjudication, incomplete checkpoint representation, or unqualified currentness;
- reject any invocation attempt to preselect genesis or lineage, filter the authority-family evidence, or bind an unknown/mismatched family identity;
- never discover or choose `latest`, ambient `HEAD`, a branch tip, timestamp order, commit order, sequence alone, or digest order implicitly;
- reject an invocation whose immutable identity, exact digest, shape, mode, checkpoint/family binding, or internal consistency cannot be validated technically; the verifier does not establish governance legitimacy of the external checkpoint pin;
- record the exact technical trust context, including both nonrecursive checkpoint identities, governed tree identities, authority-family and closure identities, complete candidate sets, selected release/derived lineage or unresolved classification, invocation authorization, and applicable governance-event evidence.

A release transition requiring simultaneous predecessor and successor roots MUST place both roots in one complete, non-ambiguous release snapshot rather than supply two releases to one verification.

For same-checkpoint invocations, partial evidence cannot produce competing valid answers: each invocation MUST prove the same subtree completeness and derive the same result. For different-checkpoint invocations, each result MUST be labelled with its exact checkpoint and MUST NOT be reported as globally current or substituted into an admission evaluation bound to another checkpoint. Checkpoint currentness is technical and checkpoint-relative; admission currentness is a separate governance judgment.

### 19.2 Historical mode

Historical verification MUST:

- receive an immutable verifier-invocation authorization binding historical mode, the exact historical checkpoint, and the one authority-family identity;
- prove that the designated historical release/lineage matches immutable historical checkpoint evidence before using it for reproduction;
- use the exact historical checkpoint, profile, release, contract artifacts, package bytes, and closures;
- label its output historical, checkpoint-qualified, and authority-family-qualified;
- remain incapable of narrowing current-mode evidence or establishing checkpoint-current, current admission, or insertion authority;
- return indeterminate if required historical artifacts, checkpoint tree material, or trust evidence are unavailable.

Current reliance or admission eligibility, if needed, is a separate evaluation under one externally admission-authorized governance checkpoint and admission policy. Historical authority MUST NOT be reconstructed from mutable current state.

Historical mode MAY reproduce either branch's exact recorded context when all required evidence is available. Historical acceptance or reproduction does not resolve checkpoint-current lineage at another checkpoint and cannot authorize current insertion by itself.

When a checkpoint conflict arises, each attestation remains immutable evidence of its exact recorded checkpoint-qualified result. If that checkpoint contained no adequate applicable accepted adjudication, it remains historically unresolved. Adequate adjudication in a later checkpoint can govern only that later checkpoint and fresh stale-authority evaluation; it does not rewrite the predecessor checkpoint.

### 19.3 Acceptance timing

If a root is externally accepted after package freezing but before independent technical verification, technical verification MAY succeed under the later accepted release. The construction/finalization process may remain nonconforming, and admission MUST evaluate that defect.

If root acceptance occurs after an attempted verification, the earlier attempt does not become successful retroactively. New independent verification under the accepted release is required.

## 20. Evolution, withdrawal, and contradiction

Identity consequences are:

- new root under existing resolver semantics: new ResolverTrustRelease;
- new dispatch entry: successor root plus new release;
- corrected dependency: successor dependency, every changed ancestor, successor root, and new release;
- new package schema expressible under existing semantics: new root plus new release;
- resolver semantic change: new resolver profile and successor fingerprint conformance identity;
- fingerprint algorithm or bootstrap change: new fingerprint specification identity;
- editorial fingerprint-specification artifact change with an accepted no-semantic-change decision: same logical identity MAY remain, but the changed bytes require a new exact digest and a new ResolverTrustRelease before use;
- admission eligibility or accepted-checkpoint change without fingerprint-algorithm change: explicit admission-governance event and, where policy semantics change, a new admission-policy version.

A successor root or dependency MUST use a new logical version and exact digest. Existing artifact bytes and historical closures remain unchanged.

Withdrawal for checkpoint-current verification requires governed withdrawal evidence binding the exact target and visible in the applicable checkpoint. It makes that target current-ineligible without erasing acceptance, rewriting earlier checkpoints, reactivating a predecessor, selecting a replacement, or implying fallback. If no eligible terminal remains, the result is `no_current_release` and checkpoint-current verification fails closed. Reactivation or rollback requires separate explicit accepted KnowledgeForge adjudication/reactivation evidence binding exact releases and evidence; no new general artifact class is introduced. Admission policy MUST be updated when necessary to reject stale prior-checkpoint or prior-release attestations for new insertion.

If an accepted historical root is later found technically unsound, KnowledgeForge MUST:

- preserve the historical release and verification attestation;
- append immutable contradiction or withdrawal evidence;
- publish a successor release;
- publish corrected successor contracts if possible and separately authorized;
- produce a new verification result if the package is re-evaluated;
- never rewrite predecessor bytes, attestations, or outcomes.

A later contradiction may change admission reliance or eligibility under its lifecycle and admission authority. It does not change an earlier checkpoint-derived result or falsify the historical fact that a specific verifier produced a result under a specific recorded trust context.

A later checkpoint containing valid lineage adjudication may resolve checkpoint-current selection at that later checkpoint only. It MUST preserve the earlier checkpoint's unresolved result and every competing release, acceptance decision, Git commit, and historical attestation unchanged.

## 21. Failure semantics

Resolution and trust validation are fail-closed. Failure includes at least:

- missing fingerprint-specification artifact, wrong or unsupported fingerprint-specification media type, specification-identity mismatch, release-bound specification-digest mismatch, or missing release-bound exact specification digest;
- mismatch between the verified fingerprint-specification digest and the procedure closure's fingerprint-specification explicit root;
- same-identity changed fingerprint-specification bytes without applicable immutable, accepted, exact-bound no-semantic-change evidence;
- package or producer attempt to select or override fingerprint-specification bytes;
- missing, malformed, unsupported, or digest-mismatched profile, release, manifest, or payload;
- missing, unknown, or mismatched authority-family identity, or invocation attempting to choose an alternative family;
- absent or invalid external acceptance evidence;
- release not published before verification;
- profile/release/family mismatch;
- package-selected or ambiguous release or governance checkpoint;
- invocation-selected genesis or lineage used to narrow the checkpoint boundary, namespace, evidence closure, or current-head result;
- incomplete governed subtree representation, missing Git tree material, or inability to prove complete cross-genesis enumeration;
- checkpoint commit, root-tree, or governed-subtree identity mismatch;
- omitted accepted genesis, non-genesis release, acceptance decision, adjudication, disposition, withdrawal, supersession, or reactivation evidence;
- same checkpoint supplied through partial invocations that do not each prove the same complete governed evidence population;
- contradictory invocation assertions for one checkpoint or an expected release/genesis/lineage inconsistent with the checkpoint-derived closure;
- invalid release sequence or predecessor, including a non-genesis predecessor outside the same accepted authority-family graph;
- zero or multiple eligible terminal releases presented as one checkpoint-current release;
- missing, incomplete, contradictory, mutable, or non-exact-identity-bound adjudication; adjudication that omits a competitor, fails to disposition every alternative, or selects multiple releases;
- timestamp, commit order, `latest`, highest sequence, digest order, filename, path, caller, invocation, package, producer, or verifier preference used to select a genesis, branch, or terminal release;
- automatic fallback to a historically superseded predecessor after withdrawal or disposition of its successor;
- conflicting accepted-looking adjudications treated as resolved by ordering;
- complete checkpoint with an unresolved fork or competing roots presented as having a checkpoint-current release;
- different-checkpoint verification results presented as interchangeable, or a C2 result presented to admission bound to C1;
- multiple incompatible checkpoints presented as applicable to one admission evaluation;
- historical checkpoint evidence presented as unqualified current or current insertion authority;
- unknown governed evidence type or duplicate/conflicting governed identity in the closed namespace;
- lower-sequence or earlier-checkpoint material treated as a downgrade solely from order rather than evaluated under the exact admission-bound checkpoint;
- unauthorized, wrong-scope, or wrong-package-kind root;
- root logical identity, version, kind, media-type, or digest mismatch;
- same logical ID/version with different digests;
- identical digest with inconsistent identity or scope;
- missing, unknown, conflicting, or ambiguous selector;
- zero or multiple dispatch results where exactly one is required;
- missing dependency, unsupported node, cycle, identity collision, or unauthorized domain overlap;
- optional, ambient, scanned, mutable, or network-resolved dependency;
- incomplete closure or ungoverned required rule domain;
- closure identity mismatch;
- package validation, package-ID, or descriptor failure.

A failure MUST NOT be weakened to a warning because fingerprint bytes happen to recompute, a package is stored, PostgreSQL agrees, or an export succeeds. Failed or untrusted claimed identities MUST remain clearly labelled claims.

Future conformance suites MUST include exact positive and negative vectors proving at least:

1. two accepted genesis releases in one authority family — both enumerated and unresolved absent adequate adjudication;
2. two invocations expecting different genesis releases at one checkpoint — same complete evidence and same unresolved result; neither narrows the family;
3. accepted linear G → A → B — B is the unique terminal candidate by predecessor/supersession relations, not sequence ranking;
4. withdrawal of B in G → A → B — B ineligible, A remains historical, and no automatic fallback;
5. explicit accepted reactivation of an exact predecessor — restored only according to exact adjudication scope;
6. accepted sibling fork G → A and G → B — multiple eligible terminals and unresolved absent adequate adjudication;
7. withdrawal of sibling B — A may remain the unique eligible terminal and G does not reactivate;
8. zero eligible terminal candidates — identity-bound `no_current_release` and checkpoint-current failure;
9. multiple eligible terminal candidates — identity-bound `conflicting_current_releases` and checkpoint-current failure;
10. conflicting accepted-looking adjudications — unresolved without order-based winner;
11. adequate accepted same-checkpoint adjudication binding all competitors and dispositioning all alternatives — exactly one result within that checkpoint;
12. later-checkpoint adjudication — later result may resolve while earlier unresolved history remains immutable;
13. invocation attempting to preselect genesis or lineage — cannot filter evidence and fails if inconsistent with derivation;
14. unknown or mismatched authority-family identity — fail closed;
15. complete checkpoint result/closure identity construction — nonrecursive boundary → closure → result ordering with no fixed-point identity;
16. partial governed subtree or omitted governed event — fail completeness;
17. two results bound to different checkpoints or admission expecting C1 but receiving C2 — distinct and non-interchangeable;
18. historical designation — accepted only after matching immutable historical checkpoint evidence and never usable to narrow current-mode evidence or claim current authority.

## 22. Legacy preservation

The measured 2026-07-15 corpus remains exactly:

- 560 existing packages;
- 521 packages with populated promotion histories;
- four statistical packages with empty promotion history;
- 35 relationship packages without package-local promotion;
- five invalid historical outer manifests;
- 35 deprecated containing-package mirrors;
- 33 stale mirrors;
- zero native Package Content Fingerprint v1 packages.

This architecture MUST NOT:

- add `/governing_contracts` retroactively;
- add native-v1 descriptors;
- reinterpret historical contract fingerprints;
- repair invalid manifests or stale mirrors;
- synthesize missing method versions;
- reserialize packages;
- manufacture promotion histories;
- assign native-v1 validity;
- create successors automatically;
- change lifecycle state.

Historical governance acceptance and native-v1 technical validity remain separate. Existing `*_contract_fingerprint` values remain legacy semantic evidence and are not native exact-byte manifest identities.

PostgreSQL remains a derived non-authoritative projection. Relationship Export Contract v1 remains unchanged and is evidenced by `specs/relationship_exports/relationship_export_contract_v1.json`, `artifacts/decisions/D-20260711-relationship-export-contract-v1.md`, and `tools/relationship_export_v1.py`; its query, result-set, content, package, and legacy manifest fingerprints MUST NOT be reinterpreted as Package Content Fingerprint v1 or native governing-contract identities.

## 23. Non-goals

This specification and its acceptance decision do not create or authorize:

- a resolver implementation;
- JSON Schemas;
- a machine-readable manifest namespace;
- an actual ResolverTrustRelease;
- an accepted root contract;
- contract manifests or payloads;
- a conformance suite;
- a verification-record implementation;
- an admission-policy implementation;
- a contract bundle;
- non-canonical staging;
- a repository transition;
- canonical insertion or publication;
- package migration or successors;
- package construction or verification;
- PostgreSQL objects or mutations;
- exports or export changes;
- production authorization.

It does not introduce a package-local contract lock, mutable registry, service, network lookup, database authority, graph database, arbitrary executable policy language, cryptographic signing system, Merkle tree, or new orchestration subsystem. The governance checkpoint is a composite externally pinned Git verification boundary and the accepted-release evidence closure is derived; neither is a second general authority-artifact class. The checkpoint is not package content and does not enter the Package Content Fingerprint v1 hash input.

## 24. Remaining gates

This documentation does not authorize implementation. Before any implementation work begins, item 21 requires separate implementation authorization. Before any implementation may claim native-v1 conformance or receive production authorization, KnowledgeForge MUST separately close all applicable gates below:

1. exact machine-readable ResolverTrustRelease schema and media type;
2. exact machine-readable contract-manifest schema and media type;
3. exact closure-identity representation schema;
4. closed contract-kind, package-kind, technical-scope, edge-type, rule-domain, selector, and media-type vocabularies;
5. exact root selector pointers, types, combination rules, and dispatch representation;
6. exact manifest and payload parsing behavior;
7. exact failure codes and severity mapping;
8. positive, negative, adversarial, and exact-byte conformance vectors;
9. cross-language agreement for strict parsing, dispatch, DAG traversal, RFC 8785 bytes, identities, and failures;
10. ResolverTrustRelease acceptance, one-family cross-genesis release-state resolution, withdrawal/reactivation, checkpoint-relative adjudication, and Git-publication workflow;
11. exact machine-readable `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, governed-namespace and evidence-enumeration representation, accepted-release evidence-closure identity, Git tree-material proof, and externally authorized verifier-invocation contract implementing the normative completeness semantics in Section 10.2;
12. serialized-artifact digest contract;
13. verification/admission record and attestation schemas;
14. authority-record placement, identity, canonicality, indexing, reconciliation, retention, failed-publication, and recovery rules;
15. historical profile, release, manifest, payload, decision, and conformance-artifact retention;
16. final-package construction-authorization contract;
17. admission-policy contract and stale-authority behavior;
18. exact canonical-visibility and logical-atomicity mechanism;
19. repository read-back, quarantine, recovery, and commit-tree verification mechanisms;
20. lifecycle, currentness, contradiction, withdrawal, and supersession contracts;
21. separate implementation authorization;
22. independent implementation and conformance validation;
23. separate production authorization;
24. separate publication authorization.

Closing this architectural profile does not close those gates.
