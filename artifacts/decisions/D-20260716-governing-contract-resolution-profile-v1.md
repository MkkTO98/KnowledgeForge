# D-20260716 — Governing Contract Resolution Profile v1

Date: 2026-07-16
Status: accepted normative architecture; not implemented; not production-authorized; machine-readable contracts and conformance gates pending
Decision class: future native-v1 governing-contract resolution, root authority, and technical closure
Normative specification: `docs/governing_contract_resolution_profile_v1.md`
Related specifications:

- `docs/package_content_fingerprint_v1.md`
- `docs/promotion_verification_admission_publication_sequence_v1.md`

Accepted specification identifiers:

- `knowledgeforge_governing_contract_resolution_profile_v1@1.0`
- `knowledgeforge_governing_contract_manifest_v1@1.0`
- `knowledgeforge_resolver_trust_release_v1@1.0`
- `knowledgeforge_contract_closure_identity_v1@1.0`

## Decision

KnowledgeForge accepts exactly this future-native architecture:

> Externally Pinned Governance Checkpoint + Checkpoint-Derived Resolver Trust Release + Package-Rooted Closed Dispatch DAG

The fixed package bootstrap remains `/governing_contracts/package_contract`. A package identifies one exact root package-contract manifest by hash-covered logical identity, version, media type, and exact-byte SHA-256. Exact-byte digest equality proves which root bytes the package selected. It does not prove that KnowledgeForge accepted those bytes as technical authority.

KnowledgeForge therefore accepts `ResolverTrustRelease` as the sole new root-authority artifact class. One exact externally accepted, immutable, Git-backed ResolverTrustRelease authorizes the exact fingerprint-specification artifact, resolver profile, conformance suite, and complete root inventory. Checkpoint-current technical verification derives the one applicable release from an exact externally pinned governance checkpoint and its proven-complete governed Git subtree. The package cannot select, downgrade, replace, extend, or authenticate the checkpoint or release.

The root contains or exact-digest-references one closed dispatch contract. Dispatch maps validated authoritative typed package selectors to exact contract-manifest digests. Selected manifests and mandatory dependencies form a finite typed DAG. Rule-domain authority follows one-way exclusive delegation. Applicability does not arise from ambient scanning, filenames, paths, campaigns, implementation order, producer convention, PostgreSQL, mutable Git state, or network lookup.

No mandatory package-local contract lock is accepted.

## 1. Verified repository reality

The following observations are verified repository reality rather than new architecture:

- `docs/package_content_fingerprint_v1.md` accepts `knowledgeforge_package_content_fingerprint_v1@1.0` as an architectural core and fixes its four-member descriptor, strict package parsing, RFC 8785 canonicalization, SHA-256 digest, exact root `/fingerprints` exclusion, package-ID binding, and fail-closed behavior.
- That specification fixes a hash-covered package-contract bootstrap at `/governing_contracts/package_contract` and requires exact immutable artifact digests, but previously left contract representation, applicability, precedence, and a uniquely bound resolution profile unresolved.
- `docs/promotion_verification_admission_publication_sequence_v1.md` accepts the 15-stage order from candidate identification through later lifecycle events while keeping verification, admission, insertion, Git publication, PostgreSQL projection, export generation, and export verification separate.
- Existing file-backed decisions and Git commits are the repository's current governance and publication evidence. PostgreSQL remains derived and non-authoritative.
- Current `tools/knowledge_repository.py` does not satisfy the future exact-byte-preserving and logically atomic insertion boundary.
- Relationship Export Contract v1 remains a derived representation and does not establish native-v1 package or contract authority.
- No current package implements Package Content Fingerprint v1 or this resolution profile.
- No current machine-readable ResolverTrustRelease, native contract-manifest schema, conformance suite, verification record, or production resolver exists.

The measured 2026-07-15 legacy corpus remains:

- 560 packages;
- 521 packages with populated promotion histories;
- four statistical packages with empty promotion history;
- 35 relationship packages without package-local promotion;
- five invalid historical outer manifests;
- 35 deprecated containing-package mirrors;
- 33 stale mirrors;
- zero native Package Content Fingerprint v1 packages.

## 2. Why package-selected digest equality is insufficient

A digest proves artifact identity, not authority.

Without an external authority boundary, a producer could create:

1. a permissive root contract;
2. a permissive package schema and dispatch DAG;
3. exact digests for every artifact;
4. a package that validates under those self-authored rules;
5. a descriptor that recomputes correctly under those rules.

That system could be internally deterministic and closed while still allowing the package to author the rules that declare itself valid. A trusted parser or resolver executing an unauthorized root does not make the root KnowledgeForge authority.

KnowledgeForge-native technical validity therefore requires both:

- exact root bytes and structural validity; and
- external authorization of that exact root digest for the applicable identity, package kind, and technical scope.

The authorization test occurs before root-authored dispatch or validity rules execute.

## 3. Accepted ResolverTrustRelease authority-family and release-state model

`ResolverTrustRelease` remains the sole new general root-authority artifact class and represents one complete immutable root-authorization snapshot. It is not a registry, service, package field, mutable catalog, or database object.

KnowledgeForge accepts exactly one governed release-authority family for native Package Content Fingerprint v1:

`knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`

This stable identity is fixed by the governing-contract-resolution profile and applicable fingerprint-verification procedure closure. It is a governed selection scope, not a new artifact class, mutable registry, service, database object, package field, invocation-selected namespace, or second root authority. Invocation MUST bind this exact family identity for consistency but cannot choose among alternatives. Missing, unknown, or different family identity fails closed. Multiple authority domains require a separately accepted successor architecture with explicit applicability/non-overlap rules and are outside v1.

Every release binds at least its specification and authority-family identities; release ID and sequence; predecessor digest or explicit genesis; exact fingerprint-specification identity/media type/SHA-256 and required no-semantic-change decision evidence; exact resolver profile and conformance suite; and complete authorized-root snapshot. Every root binds logical identity/version, kind, media type, exact digest, allowed package kinds, and technical scopes.

Every accepted genesis in the family is part of one governed release graph. One genesis cannot hide another. A non-genesis release enters that graph only with exact valid accepted evidence, one exact already-accepted predecessor in the family, sequence increment of one, and predecessor consistency. Invalid, rejected, malformed, or merely proposed releases remain evidence but are not eligible. Sequence is a consistency property, never a selection rule.

Acceptance of a valid successor makes its exact predecessor historical/superseded and non-current-eligible. Withdrawal makes its exact target current-ineligible without erasing acceptance, rewriting prior checkpoints, reactivating a predecessor, selecting a replacement, or implying fallback. Withdrawal of a successor does not reactivate its predecessor. Explicit accepted disposition makes its exact target ineligible according to scope and selects no replacement unless it also provides adequate adjudication. Reactivation/rollback requires separate explicit accepted KnowledgeForge adjudication/reactivation decision evidence binding exact affected releases and evidence; it introduces no new general artifact class.

After complete evidence classification, an eligible terminal candidate is accepted, in this family, completely evidenced, not withdrawn/rejected/dispositioned non-current, not historically superseded without explicit reactivation, on a uniquely adjudicated branch where applicable, and without an accepted successor that keeps it historical.

The accepted deterministic functions are `release_eligible_v1(C, r)`, `eligible_terminal_set_v1(C)`, and `checkpoint_current_head_v1(C)`. The first applies the exact eligibility predicate to complete checkpoint evidence; the second forms the complete eligible-terminal set; the third returns exactly one of:

1. one eligible terminal — checkpoint-current succeeds and lineage is derived from that release's exact predecessor chain;
2. zero eligible terminals — identity-bound `no_current_release`, with checkpoint-current verification failing closed;
3. multiple eligible terminals — identity-bound `conflicting_current_releases`, with checkpoint-current verification failing closed.

No highest sequence, latest, timestamp, commit order, filename, path, digest order, caller, invocation, package, producer, or verifier fallback is accepted.

Adequate accepted adjudication already in checkpoint C may resolve a fork within C only if it binds all applicable competing release and acceptance-evidence digests, dispositions every alternative, and selects exactly one branch/release. If C has no adequate applicable adjudication, C remains unresolved. A later checkpoint may resolve for that later checkpoint without rewriting C's immutable unresolved result. Conflicting accepted-looking adjudications remain unresolved; none wins by ordering.

The accepted examples are:

- G → A → B: G and A are historical; B is the sole terminal candidate if otherwise eligible, based on exact edges rather than highest sequence.
- G → A → B followed by B withdrawal: B is ineligible; A remains historical; no fallback; no current release absent explicit reactivation/adjudication.
- G → A and G → B: A and B compete; unresolved absent adequate adjudication.
- accepted G1 and G2: both are enumerated competing roots; unresolved absent adequate adjudication.
- G → A and G → B with B withdrawn: B is ineligible, G does not reactivate, and A may be unique if no other conflict exists.
- conflicting adjudications selecting different releases: unresolved until adequate later governance resolution.

## 4. External trust selection without genesis pre-partitioning

KnowledgeForge accepts an externally pinned governance checkpoint as the immutable Git verification boundary for checkpoint-current claims. It is composite evidence, not a new general authority-artifact class.

`governance_checkpoint_boundary_identity` binds repository identity, exact Git commit, exact root tree and governed subtrees, exact resolver-profile identity/digest, exact fixed authority-family identity, deterministic namespace/enumeration rules, and mode. It does not bind a preselected genesis or release lineage. The profile/family defines one namespace mapping for each repository/commit/mode tuple. Invocation cannot narrow, replace, partition, or choose it.

The verifier proves complete tree enumeration and classifies every governed release, acceptance, withdrawal, supersession, disposition, adjudication, and reactivation event across every genesis in the family. Paths define discovery only, never release selection.

The accepted-release evidence closure contains all accepted genesis and non-genesis releases, acceptance evidence, predecessor edges, sequence consistency, every governance event and effect, complete predecessor graph, candidate roots/branches/terminals, and either one selected release with derived lineage or an exact unresolved classification and candidate set. Its identity commits to the checkpoint boundary and complete classified evidence/result.

`governance_checkpoint_result_tuple` binds boundary identity, closure identity, authority-family identity, and the same uniquely selected release/derived lineage or unresolved classification/candidate set. The closure commits only to boundary identity, never the result tuple that contains the closure identity; no fixed-point identity arises.

Invocation binds checkpoint, exact family, and mode. It may provide an expected derived result only as a consistency assertion. It cannot preselect genesis or lineage or filter evidence. At checkpoint C containing accepted G1 and G2, invocations expecting G1 and G2 both enumerate both roots and derive the same unresolved result absent adequate adjudication.

The verifier-owned `technical_trust_context` and attestation bind fingerprint specification; resolver profile; conformance suite and implementation evidence; both checkpoint identities and tree identities; fixed authority family; namespace and closure identities; all candidate roots/branches/terminals; one selected release and derived lineage or unresolved classification; every applicable governance event; invocation identity/digest and checkpoint/family/mode binding; and exact mode. They never make an unqualified global-currentness claim.

Historical mode remains authority-family-qualified. It may designate an exact historical release/lineage for reproduction only after matching immutable historical checkpoint evidence. It cannot narrow current-mode evidence, resolve another checkpoint, or establish current authority.

The package does not select fingerprint specification, resolver profile, authority family, governance checkpoint, genesis, release lineage, trust release, governance decisions, sequence, mode, checkpoint currentness, admission currentness, or withdrawal policy. The external checkpoint pin terminates technical trust selection. Technical verification proves checkpoint identity, complete evidence, deterministic graph/current-head derivation, and exact consistency; admission separately judges external-pin legitimacy, applicability, sufficient recency, withdrawal status, and sufficiency.

The fingerprint specification does not contain its own digest. A release externally binds the finalized published specification artifact, and the procedure closure root must match exactly. Accepted no-semantic-change evidence may preserve logical algorithm identity across editorial byte changes only with exact predecessor/successor binding and release/trust-context/attestation evidence. A new exact digest and release are required either way; no fingerprint algorithm rule changes.

## 5. Accepted resolver-profile semantics

The resolver profile owns stable resolution mechanics:

- root and contract-manifest interpretation;
- supported media types;
- trust-release validation;
- closed selector and dispatch grammar;
- typed dependency-edge vocabulary;
- finite DAG traversal and cycle rejection;
- rule-domain ownership and delegation;
- collision and conflict handling;
- closure-identity construction;
- strict failure behavior.

The profile does not enumerate routine authorized roots. Root changes produce new trust releases, not routine profile versions.

A semantic change to those mechanics requires a new resolver-profile identity and, under the accepted one-profile-per-fingerprint-conformance rule, a successor fingerprint conformance identity. No semantic change may occur silently under an existing identifier or version.

## 6. Accepted closed dispatch and typed DAG

The root package contract owns or digest-references one closed dispatch contract. It maps authoritative typed selector tuples to exact contract-manifest digests.

Permitted selector domains are profile-governed package fields such as package kind, schema/version, statement type, method ID/version, transformation ID/version, calculation-contract ID/version, evidence/reference role, numeric-rule family, and fingerprint semantic role.

Dispatch is deterministic, offline, side-effect-free, non-Turing-complete, and limited in v1 to typed equality or closed set membership. Arbitrary code and regular expressions are not accepted v1 dispatch mechanisms.

After dispatch, dependencies are mandatory exact-digest typed edges. Resolution rejects missing nodes, cycles, unsupported artifacts, identity collisions, ambiguous dispatch, ungoverned domains, and incomplete closure. Unreachable supplied artifacts do not enter the technical closure.

No mandatory package-local contract lock is needed because exact root dispatch plus exact mandatory dependency edges already determine the closure. A package-local lock would duplicate the graph and still would not establish external root authority.

## 7. Accepted manifest and payload identity

One future exact-byte typed manifest represents each technical contract node under:

`knowledgeforge_governing_contract_manifest_v1@1.0`

Manifest identity is SHA-256 over exact bytes. Optional external payloads may carry JSON Schema, large vocabularies, governed tables, or other format-specific technical rules when each payload is bound by media type and exact SHA-256. A normative payload digest is a closure member and its manifest reference is a typed closure edge; unreachable supplied payloads are excluded.

No second semantic contract fingerprint is accepted. For JSON, UTF-8, BOM rejection, strict duplicate-key detection, no Unicode normalization, and exact-byte identity apply. Whitespace or line-ending changes create new artifact identities.

Historical `*_contract_fingerprint` values remain legacy semantic evidence. Markdown prose and implementation code do not become machine-executable contract authority by description alone.

## 8. Accepted one-way exclusive delegation

KnowledgeForge accepts one-way exclusive rule-domain delegation:

1. the resolver profile owns resolution mechanics;
2. the root owns package-wide technical rule domains;
3. a parent may delegate one bounded named domain to one child;
4. the child governs only that domain;
5. the parent may not retain conflicting rules in the delegated domain;
6. overlap without explicit delegation fails;
7. no generic override or load-order precedence exists.

Filename, path, digest order, implementation order, and “most specific wins” cannot create authority.

## 9. Accepted closure boundaries

KnowledgeForge accepts exactly three closure names.

### `package_technical_contract_closure`

Contains only package-conformance authority reached from exactly one authorized root. It excludes construction authorization, admission, insertion, publication, PostgreSQL, exports, and lifecycle outcomes.

### `fingerprint_verification_procedure_closure`

Contains stable verification semantics such as the fingerprint specification, resolver profile, trust-release validation rules, parser/RFC 8785 requirements, serialized-artifact digest contract, closure-identity contract, and verification-record contract. Its explicit roots are exactly the fingerprint specification and resolver profile. The fingerprint-specification root digest must equal the release-bound and trust-context digest exactly; logical identity alone is insufficient. It excludes a producer-specific implementation binary. Implementation identity belongs in the attestation.

### `admission_policy_closure`

Contains construction-authorization policy, admission policy, collision/no-overwrite rules, stale-authority evaluation, and repository-transition prerequisites, reached from exactly one admission-policy root. It cannot redefine technical fingerprint validity.

Closure identity uses:

`knowledgeforge_contract_closure_identity_v1@1.0`

It is SHA-256 over RFC 8785 canonical UTF-8 JSON with domain-separated closure type, profile identity/digest, explicit roots, sorted member digests, and sorted typed edges including rule domain. Graph structure is committed; member-set equality alone is insufficient. No Merkle tree is accepted for v1.

## 10. Accepted qualified technical validity

The complete proposition is:

> Exact artifact A is `native_package_content_fingerprint_v1_valid` under exact fingerprint-specification artifact X, resolver profile P, conformance suite S with exact implementation-conformance evidence I, externally pinned governance checkpoint Q, checkpoint-qualified ResolverTrustRelease R, accepted-release evidence closure E, package technical contract closure C, and fingerprint-verification procedure closure V whose fingerprint-specification root equals X by exact digest.

Technical validity requires externally bound exact fingerprint-specification bytes, equality with the procedure-closure fingerprint-specification root, exact release-bound conformance-suite bytes and implementation-conformance evidence, a proven-complete checkpoint evidence boundary, deterministic checkpoint-qualified external root authority, complete technical closure, strict verification of exact frozen bytes, and successful descriptor recomputation. The attestation binds both nonrecursive checkpoint identities and exact tree identities, accepted-release evidence-closure identity, checkpoint-current or historical designation, selected release and applicable adjudications, fingerprint-specification and conformance-suite identities/media types/digests, implementation-conformance-evidence identity/digest, technical trust context, and procedure closure. It never claims unqualified global currentness and does not require a valid construction authorization or successful admission.

Construction authorization authorizes only stage 4 construction of complete final semantic package content. Its exact identity is a required binding and process-lineage input to stages 5 through 7, but required identity binding grants no authority over those later events and does not determine deterministic technical fingerprint validity. Admission evaluates its legitimacy, scope, currentness, expiry, withdrawal, and sufficiency. A technically valid artifact may still be denied, deferred, ineligible, not evaluated, prohibited from insertion, unpublished, or non-current.

This decision narrowly amends earlier wording that treated construction-authorization identity or validity as part of the deterministic technical fingerprint predicate. It does not change the fingerprint algorithm or the 15-stage order.

## 11. Accepted checkpoint-current and historical verification modes

Checkpoint-current mode receives exactly one externally pinned checkpoint, the fixed authority-family identity, and mode through immutable verifier-invocation authorization. It proves complete cross-genesis enumeration, derives the entire-family closure and terminal set, applies the deterministic current-head function, derives lineage only after one unique result, and rejects partial evidence, invocation preselection, zero/multiple candidates, conflicting adjudication, absent authority, and order-based fallback.

Same-checkpoint deterministic invocations derive the same complete evidence population, candidate sets, and selected release/derived lineage or unresolved result. Invocations expecting different genesis releases cannot narrow evidence. Adequate accepted adjudication already inside checkpoint C may resolve C; if C contains none, C remains unresolved and later adjudication changes only a later checkpoint.

Different-checkpoint results are distinct technical trust contexts, never unqualified global-current claims. Admission binds exactly one checkpoint; another result is stale, mismatched, or inapplicable, and incompatible checkpoints fail closed. Admission currentness remains separate.

Historical mode is authority-family-qualified and may designate a release/lineage for reproduction only after exact matching immutable historical checkpoint evidence. It cannot narrow current-mode evidence, resolve current authority, or authorize current insertion. Missing historical artifacts/tree material produce an indeterminate result; later adjudication never rewrites earlier unresolved history.

A root accepted after package freezing but before verification may support technical verification because derivation can calculate a purported descriptor under exact contract artifacts without claiming external root authority. Admission may still reject the nonconforming production process. Root acceptance after an attempted verification does not make that attempt successful retroactively; new independent verification is required.

## 12. Accepted evolution, withdrawal, and contradiction rules

- New root under unchanged resolver semantics: new trust release.
- New dispatch entry: successor root and new release.
- Corrected dependency: successor dependency, changed ancestors, root, and release.
- New package schema expressible under existing semantics: new root and release.
- Resolver semantic change: new profile and successor fingerprint conformance identity.
- Fingerprint algorithm/bootstrap change: new fingerprint specification identity.
- Editorial fingerprint-specification revision accepted as technically unchanged: same logical identity may remain, but a new exact artifact digest and new ResolverTrustRelease are required before verification.
- Admission eligibility change only: new admission-policy version.

Withdrawal makes the exact target release current-ineligible at applicable checkpoints. It preserves acceptance history, never reactivates a predecessor, selects no replacement, and permits no automatic fallback. Zero eligible terminals produce `no_current_release`. Explicit accepted KnowledgeForge adjudication/reactivation evidence is required to restore an exact predecessor. Admission policy may reject stale prior-release attestations for new insertion.

A technically unsound historical root requires immutable contradiction or withdrawal evidence, a successor release, corrected successor contracts if possible, and a new verification result if re-evaluated. Historical release bytes and attestations are never rewritten.

## 13. Rejected alternatives

### Profile-embedded routine root inventory

Rejected because every routine root addition or withdrawal would change resolver-profile identity and could force unnecessary successor fingerprint conformance identities. Stable semantics and evolving root inventory remain separate.

### Individual root-authorization records as the general model

Rejected because the verifier would need another catalog, snapshot, registry, or scan to prove that the record set is complete and non-conflicting. One complete release snapshot is smaller and more deterministic.

### Package-local contract lock

Rejected because it duplicates the package-rooted dependency graph, adds package complexity, and still cannot prove external authority. Exact root dispatch and mandatory digest edges already determine the closure.

### Root binding embedded in the fingerprint specification

Rejected because routine schema, method, and root evolution would become coupled to fingerprint algorithm identity. This does not reject the accepted external ResolverTrustRelease binding of the exact already-finalized fingerprint-specification artifact; the specification does not embed its own digest.

### Network registry, service, or database authority

Rejected because native verification must remain offline and reproducible. Mutable network, PostgreSQL, producer-private registry, branch, or filesystem state cannot establish authority.

### Arbitrary executable dispatch or precedence

Rejected because it weakens deterministic cross-language conformance and introduces hidden behavior. V1 uses closed typed selectors and exclusive delegation.

## 14. Narrow amendment and predecessor preservation

This decision records four bounded documentation corrections:

1. it integrates accepted governing-contract resolution into both normative specifications;
2. it preserves the construction-authorization boundary: stage 3 authorizes stage 4 only, while the exact identity remains non-authorizing process-lineage evidence for stages 5–7;
3. it fixes one native-v1 release-authority family, removes genesis/lineage as invocation-selectable checkpoint inputs, makes lineage derived output, requires complete cross-genesis evidence enumeration, and accepts the deterministic release-state/current-head rules; and
4. it records coordination with `artifacts/decisions/D-20260717-canonical-visibility-completion-boundary-v1.md`, which separately clarifies that stage-9 materialization remains non-canonical and stage-10 success plus one visibility switch completes insertion.

The amendment preserves the accepted construction authority boundary:

- final-package construction authorization authorizes only stage 4 construction of complete final semantic package content;
- its exact identity is required binding/process-lineage evidence for stages 5–7 but grants no authority over those stages;
- stage 3 does not authorize fingerprint derivation, descriptor attachment, serialization, freezing, staging, verification/result, validity, admission, insertion, reconciliation, publication, projection, export, or lifecycle action;
- admission, not the technical verifier, evaluates construction-authorization legitimacy, scope, currentness, expiry, withdrawal, and sufficiency.

The bytes of these protected predecessor decisions remain unchanged historical evidence:

- `artifacts/decisions/D-20260715-package-content-fingerprint-v1.md`
- `artifacts/decisions/D-20260716-promotion-verification-admission-publication-sequence-v1.md`

The successor visibility decision does not edit the predecessor sequence decision. It clarifies only the completion boundary between stage-9 materialization and stage-10 reconciliation/visibility. The 15-stage count and order remain unchanged, but the amended sequence specification's stage-9/10 block is intentionally not byte-identical to the protected predecessor wording.

For the same-identity editorial transition accepted here, the predecessor published `knowledgeforge_package_content_fingerprint_v1@1.0` artifact remains SHA-256 `4585c44556c28e738e0a7f5ae326677e9676baead4a53dc4a978637b790335ae`, and the final corrected artifact is SHA-256 `8e3a01eadfa0d6de2a94ebd5ef934f21acbd3dba59755beee1de8bd4d88c1dc8`. The corrected bytes change authority resolution, family/closure/trust evidence, conformance vectors, versioning clarity, and construction-authorization boundary clarity only. They do not change the Package Content Fingerprint v1 hash boundary, four-member descriptor, RFC 8785 canonicalization, SHA-256, root `/fingerprints` exclusion, parsing, numeric, Unicode, package-ID, mirror, or self-reference semantics. A future ResolverTrustRelease authorizing the corrected artifact MUST bind this decision's exact identity, digest, and eventual Git publication commit even if that release is genesis.

This decision also binds the final corrected resolver-profile artifact `knowledgeforge_governing_contract_resolution_profile_v1@1.0` at `docs/governing_contract_resolution_profile_v1.md`, SHA-256 `fe21e147ec2ee289cffde4fea82ab8c11f567c457b107a95af5d2ff03407d472`. Working-tree presence does not publish either artifact or this decision. Eventual publication evidence MUST be an immutable Git commit and verified actual commit tree containing the exact final bytes under the separately authorized allowlist; no future commit ID or publication success is predicted here.

## 15. Legacy preservation

This decision applies only to future native-v1 packages. It does not:

- introduce a legacy resolver profile;
- add `/governing_contracts` to existing packages;
- add native-v1 descriptors;
- reinterpret historical contract fingerprints;
- repair invalid manifests or stale mirrors;
- synthesize missing method versions;
- reserialize packages;
- manufacture promotion histories;
- assign native-v1 validity;
- create successors automatically;
- change lifecycle state.

All 560 existing packages remain legacy. Historical governance acceptance and native-v1 technical validity remain separate.

## 16. Future implementation dependencies

This accepted architecture is not independently implementable. Future implementation requires separate acceptance of at least:

- exact machine-readable trust-release, contract-manifest, and closure schemas;
- media types and closed vocabularies;
- root selector pointers, types, and dispatch representation;
- exact dependency-edge and rule-domain vocabularies;
- exact failure codes;
- positive, negative, adversarial, and exact-byte conformance vectors covering all eighteen authority-family/checkpoint cases normatively listed in the profile and all four stage-9/10 visibility cases in the sequence specification;
- cross-language parsing, dispatch, DAG, closure, RFC 8785, release-state, identity, and failure agreement;
- trust-release acceptance, one-family cross-genesis enumeration, deterministic terminal-head resolution, withdrawal/reactivation, checkpoint-relative adjudication, and Git-publication workflow;
- exact machine-readable fixed authority-family binding, `governance_checkpoint_boundary_identity`, `governance_checkpoint_result_tuple`, namespace/enumeration representation, accepted-release evidence-closure identity, Git tree completeness proof, and externally authorized verifier-invocation contract implementing the accepted semantics;
- serialized-artifact digest contract;
- verification/admission record and attestation schemas;
- authority-record placement and retention;
- long-term profile, release, manifest, payload, decision, and conformance-artifact retention;
- construction-authorization and admission-policy contracts;
- exact stage-9 non-canonical materialization, reader-gate, stage-10 reconciliation, one-switch canonical-visibility, and logical-atomicity mechanism;
- repository transition, reconciliation, quarantine, retention, cleanup, and recovery;
- lifecycle contradiction, withdrawal, currentness, and supersession contracts;
- separate implementation, production, and publication authorization.

## 17. Non-goals

This decision does not create:

- a resolver implementation;
- JSON Schemas;
- a manifest namespace;
- an actual ResolverTrustRelease;
- an accepted root contract;
- contract manifests or payloads;
- a conformance suite;
- a verification-record implementation;
- an admission-policy implementation;
- a mutable checkpoint registry, checkpoint service, second general authority-artifact class, or alternative native-v1 authority family;
- a contract bundle;
- a repository transition;
- package migration;
- PostgreSQL objects;
- exports;
- production authorization.

It does not make a governance checkpoint package content or fingerprint input, authorize ambient branch state as authority, or authorize package construction, derivation, verification, admission, insertion, publication, projection, export, migration, repair, or lifecycle mutation.

## 18. Decision consequences

### Accepted decision

The architectural trust gap is closed at the documentation level by separating exact root identity from external root authority, retaining ResolverTrustRelease as the sole new general authority-artifact class, fixing one native-v1 authority family, proving complete cross-genesis checkpoint evidence, and deriving exactly one terminal current release/lineage or an identity-bound unresolved result without invocation preselection.

### Future implementation dependency

All machine-readable forms, workflows, vectors, implementations, and operational boundaries remain closed. Native-v1 derivation continues to fail closed while its profile, manifest, contract, and conformance dependencies are absent; verification additionally fails closed without accepted trust-release, invocation, acceptance, and closure dependencies.

### Non-goal

This decision is not evidence that any current component conforms, and it is not authority to implement or produce native-v1 packages.

### Publication status

This documentation has not passed independent publication-readiness review and is not publication-authorized by this decision alone.
