# KnowledgeForge Package Content Fingerprint v1

Date: 2026-07-15
Status: accepted architectural core; Governing Contract Resolution Profile v1 accepted as normative architecture; machine-readable contracts and conformance gates pending; not implemented; not authorized for production package generation
Specification identifier: `knowledgeforge_package_content_fingerprint_v1@1.0`

Normative terms in this document are `MUST`, `MUST NOT`, `SHOULD`, and `MAY`.

## 1. Purpose and authority

This specification defines the future authoritative content fingerprint for a KnowledgeForge package. Its purpose is to identify the complete final parsed semantic package without circularly hashing the descriptor that carries the fingerprint.

For a package that conforms to this specification, the authoritative field is:

`fingerprints.package_content_fingerprint`

This specification is an accepted architectural core. Its content-fingerprint boundary and descriptor are decided. `docs/governing_contract_resolution_profile_v1.md` now defines the normative future resolution, trust-release, dispatch, dependency, and closure architecture required by Section 6.1. Independent conformance remains incomplete until the required machine-readable contracts, artifacts, conformance vectors, implementations, and production gates are separately accepted and completed. Until then, derivation and verification MUST fail closed. This document does not claim that producers, validators, schemas, repository persistence, PostgreSQL projection, exports, or consumers currently enforce it.

### 1.1 Normative orchestration precedence

This specification remains authoritative for fingerprint calculation, strict package parsing, canonicalization, package binding, and technical fingerprint recomputation. `docs/governing_contract_resolution_profile_v1.md` governs contract-manifest interpretation, ResolverTrustRelease validation, external technical trust selection, root authorization, closed dispatch, typed dependency closure, rule-domain delegation, and closure identity. `docs/promotion_verification_admission_publication_sequence_v1.md` governs ordering and authority boundaries among final-package construction authorization, final repository serialization, non-canonical staging, verification, admission, canonical insertion, Git publication, PostgreSQL projection, export generation, and export verification. Each document is authoritative only within its declared domain.

Where older orchestration language in this specification conflicts with that accepted sequence, the corrected sequence controls. This is a bounded clarification and amendment, not a new fingerprint algorithm version. It does not change the field, descriptor, specification identifier, RFC 8785 canonicalization, SHA-256, exact `/fingerprints` exclusion, parsing rules, package-ID binding, semantic roles, or legacy classifications and measurements.

## 2. Applicability and non-retroactivity

This specification applies only to future packages created under a separately authorized implementation that explicitly declares conformance to `knowledgeforge_package_content_fingerprint_v1@1.0`.

It MUST NOT be applied retroactively to existing packages. Existing `fingerprints.package_manifest` values MUST remain immutable legacy values and MUST NOT be reinterpreted as Package Content Fingerprint v1 values.

No current package is classified as native v1-valid. A package carrying the descriptor and claiming the governing contract is only `purported_package_content_fingerprint_v1`; the descriptor is a claim, not proof of technical validity or acceptance. `native_package_content_fingerprint_v1_valid` may be assigned only when an independent verifier successfully establishes that the exact frozen descriptor-bearing artifact conforms to this specification and its complete applicable immutable governing-contract set. Technical validity does not require or imply admission. A production package MUST NOT adopt this contract until the contract-resolution profile, implementation, independent validation, conformance vectors, legacy handling, and the applicable production gate have been separately authorized and completed.

## 3. Typed descriptor schema

The authoritative descriptor MUST appear at `fingerprints.package_content_fingerprint` and MUST have exactly the following member set, member types, and required values. JSON object member order is insignificant:

```json
{
  "specification": "knowledgeforge_package_content_fingerprint_v1@1.0",
  "canonicalization": "RFC8785",
  "digest_algorithm": "sha256",
  "value": "sha256:<64-lowercase-hex>"
}
```

The four members are required strings:

| Member | Required value |
| --- | --- |
| `specification` | `knowledgeforge_package_content_fingerprint_v1@1.0` |
| `canonicalization` | `RFC8785` |
| `digest_algorithm` | `sha256` |
| `value` | `sha256:` followed by exactly 64 lowercase hexadecimal characters |

`<64-lowercase-hex>` is metavariable notation, not a literal descriptor value. The exact canonicalization token is `RFC8785`; prose may refer to the underlying standard as RFC 8785. A v1 descriptor MUST NOT contain additional members. A missing, malformed, unknown, or unsupported descriptor MUST fail closed.

## 4. Exact algorithm identifier and normative formula

Algorithm identifier:

`knowledgeforge_package_content_fingerprint_v1@1.0`

Normative formula:

> Package Content Fingerprint v1 is SHA-256 over the RFC 8785 canonical UTF-8 serialization of the complete final parsed package after removing exactly the root `/fingerprints` member.

Derivation and verification are distinct normative operations. Derivation receives a proposed package whose hash-covered content is finalized and complete; it does not require or accept a completed Package Content Fingerprint v1 descriptor. Verification receives the exact frozen descriptor-bearing final repository serialization from non-canonical staging and requires the exact completed descriptor.

Normative derivation pseudocode:

```text
function derive_package_content_fingerprint_v1(
    serialized_proposed_package_bytes,
    immutable_contract_artifacts,
    accepted_contract_resolution_profile
):
    package = parse_json_strict_reject_bom_duplicates_unicode_and_prohibited_numbers(
        serialized_proposed_package_bytes
    )
    require_root_object(package)
    require_fingerprints_absent_or_empty_object_for_derivation(package)

    bootstrap = require_exact_package_contract_bootstrap(package)
    contracts = resolve_and_digest_verify_contracts(
        bootstrap,
        immutable_contract_artifacts,
        accepted_contract_resolution_profile
    )
    require_complete_unambiguous_nonconflicting_contract_rules(contracts)
    validate_complete_hash_covered_package_content(package, contracts)
    require_valid_package_id_under_contract(package, contracts)
    reject_prohibited_containing_package_self_references(package, contracts)
    enforce_unicode_decimal_identity_role_and_reservation_rules(package, contracts)

    hash_basis = deep_copy(package)
    remove_exact_root_member_if_present(hash_basis, "fingerprints")

    canonical_bytes = UTF8(RFC8785(hash_basis))
    digest = lowercase_hex(SHA256(canonical_bytes))
    return {
        "specification": "knowledgeforge_package_content_fingerprint_v1@1.0",
        "canonicalization": "RFC8785",
        "digest_algorithm": "sha256",
        "value": "sha256:" + digest
    }
```

Normative verification pseudocode:

```text
function verify_package_content_fingerprint_v1(
    serialized_persisted_package_bytes,
    claimed_package_id,
    immutable_contract_artifacts,
    accepted_contract_resolution_profile,
    externally_pinned_technical_trust_context
):
    package = parse_json_strict_reject_bom_duplicates_unicode_and_prohibited_numbers(
        serialized_persisted_package_bytes
    )
    require_root_object(package)
    require_exact_completed_v1_fingerprints_object(package["fingerprints"])
    stored_descriptor = package["fingerprints"]["package_content_fingerprint"]
    require_valid_v1_descriptor_shape_member_types_and_values(stored_descriptor)

    bootstrap = require_exact_package_contract_bootstrap(package)
    contracts = resolve_and_digest_verify_contracts(
        bootstrap,
        immutable_contract_artifacts,
        accepted_contract_resolution_profile,
        externally_pinned_technical_trust_context
    )
    require_complete_unambiguous_nonconflicting_contract_rules(contracts)
    validate_complete_hash_covered_package_content(package, contracts)
    require_valid_package_id_and_exact_claimed_id(package, claimed_package_id, contracts)
    reject_prohibited_containing_package_self_references(package, contracts)
    enforce_unicode_decimal_identity_role_and_reservation_rules(package, contracts)

    hash_basis = deep_copy(package)
    remove_exact_root_member(hash_basis, "fingerprints")
    canonical_bytes = UTF8(RFC8785(hash_basis))
    calculated_descriptor = {
        "specification": "knowledgeforge_package_content_fingerprint_v1@1.0",
        "canonicalization": "RFC8785",
        "digest_algorithm": "sha256",
        "value": "sha256:" + lowercase_hex(SHA256(canonical_bytes))
    }
    require_exact_descriptor_equality(calculated_descriptor, stored_descriptor)
    return verified
```

The accepted contract-resolution profile is a required explicit input to both derivation and verification, not package-selected, ambient, or producer-private knowledge. Derivation may calculate and attach a purported descriptor under the accepted profile and exact contract artifacts without claiming root authority or native technical validity. Verification additionally requires the externally pinned technical trust context, which binds the exact fingerprint-specification identity, media type, and artifact SHA-256 supplied by the ResolverTrustRelease; the exact profile; the release and external acceptance evidence; the authorized invocation; and the verification mode under `docs/governing_contract_resolution_profile_v1.md`. The verified fingerprint-specification digest MUST equal the fingerprint-specification explicit-root digest in `fingerprint_verification_procedure_closure`. The package MUST NOT select or override the fingerprint-specification artifact. Derivation MUST fail closed while its required machine-readable profile, manifest, contract, or conformance dependencies remain pending. Verification MUST additionally fail closed while any fingerprint-specification artifact, trust-release, acceptance, invocation, closure, or verification dependency remains pending.

Only the root member selected by the RFC 6901 JSON Pointer `/fingerprints` is removed. No nested member named `fingerprints`, no recursively discovered fingerprint-like field, and no other root member is removed.

## 5. RFC 8785 canonicalization

The hash basis MUST be serialized using RFC 8785 JSON Canonicalization Scheme semantics and encoded as UTF-8 before hashing.

Object member order, source whitespace, insignificant escape-form differences, and source serialization layout MUST NOT affect the result when they parse to the same permitted JSON value. Array order remains semantically significant and MUST be preserved.

An implementation MUST identify and test a concrete RFC 8785 implementation or conforming implementation strategy before production authorization. Ordinary `json.dumps(sort_keys=True)` behavior MUST NOT be claimed as RFC 8785 conformance without independent proof.

## 6. JSON parsing requirements

The exact frozen staged package bytes presented for verification and later admission evaluation MUST be parsed as one JSON document with a root object. Trailing non-whitespace data, malformed UTF-8, malformed JSON, unsupported values, and parser recovery MUST be rejected.

An initial UTF-8 byte-order mark (BOM) MUST be rejected. A conforming parser MUST NOT silently discard it.

The parser MUST expose duplicate object-member keys as errors rather than silently retaining the first or last value. Duplicate-key comparison occurs after JSON escape decoding but without Unicode normalization; for example, `"a"` and `"\u0061"` are duplicate keys, while distinct NFC and NFD strings remain distinct. Parsing into an ordinary map before duplicate detection is insufficient.

The parsed package used for fingerprinting MUST be the complete final semantic package. Producers MUST NOT fingerprint a projection, selected-field subset, pre-final object, or object that will later receive hash-covered semantic mutations.

### 6.1 Governing-contract bootstrap and resolution status

Every purported native v1 package MUST carry its governing package-contract reference at the fixed hash-covered RFC 6901 JSON Pointer:

`/governing_contracts/package_contract`

The root `/governing_contracts` value MUST be an object. Its `package_contract` member MUST be an object with exactly this member set, member types, and structure; object member order is insignificant:

```json
{
  "contract_id": "<non-empty-string>",
  "contract_version": "<non-empty-string>",
  "media_type": "<non-empty-string>",
  "content_digest": {
    "digest_algorithm": "sha256",
    "value": "sha256:<64-lowercase-hex>"
  }
}
```

`content_digest` MUST contain exactly the two shown string members. The metavariables are not literal values. This bootstrap reference is part of the hash-covered package content. Contract ID and version alone are insufficient and MUST NOT be used as authority without the content digest.

The content digest covers the exact immutable bytes of the resolved contract artifact, including their original encoding, whitespace, and member order. No parsing or canonicalization occurs before this digest is checked. The verifier MUST receive an explicitly identified immutable contract-artifact set as an input and select the artifact by the declared SHA-256 content digest. The resolved bytes MUST match the declared digest, and the accepted contract-resolution profile MUST then validate that the artifact's declared contract ID, contract version, and media type exactly match the bootstrap reference. Mutable `latest` resolution, unpinned network retrieval, ambient filesystem search, and producer-private registry state are prohibited. Missing bytes, more than one non-byte-identical artifact for one digest, digest mismatch, unsupported media type, unsupported contract version, or identifier mismatch MUST fail closed.

The resolved package contract MUST deterministically define or immutably reference:

- the package schema and package-ID rule;
- every applicable method, schema, calculation, evidence, or related contract by immutable content digest;
- deterministic applicability for every referenced contract;
- permitted field roles;
- every governed decimal-string location and its lexical, scale, sign, zero, leading-zero, trailing-zero, and exponent rules;
- every permitted fingerprint-reference location and its semantic target relation: containing package, another package, source evidence, method, input, registry, calculation, normalized series, or another external artifact;
- any required identity binding between a reference value and its target identifier;
- deterministic precedence and conflict detection across all applicable contracts.

A contract rule MUST use an exact RFC 6901 JSON Pointer evaluated against the complete final parsed package root unless a future separately versioned contract-resolution profile defines a closed pointer-pattern grammar. Informal `{index}`, wildcard, regular-expression, glob, or implementation-defined path notation is prohibited by this architectural core. Exact pointers MUST use RFC 6901 escape handling (`~0` for `~` and `~1` for `/`). Array tokens MUST be canonical base-10 indices with no leading zero except `0`; `-` is invalid for evaluation against a final package. A malformed pointer, invalid escape, invalid array index, missing target, or target of the wrong type MUST fail closed.

Governing Contract Resolution Profile v1 does not permit pointer patterns or regular expressions. Any future profile that permits patterns MUST define its grammar and version; evaluation root; escaping; array expansion; deterministic expansion order; missing-target behavior; duplicate-target elimination; and uniqueness rules, and requires the successor identities governed by that profile decision. Empty or non-unique expansion MUST fail closed. Under v1, patterns remain unsupported.

For multiple applicable contracts, the accepted profile MUST provide deterministic closed dispatch, one-way exclusive rule-domain delegation, and conflict rules. No delegated child may silently weaken or contradict authority outside its bounded domain; contradictions, overlapping undelegated authority, and ambiguous applicability MUST fail closed. A field whose representation or semantic role requires governance but has no applicable rule MUST fail closed. Field names or digest-shaped values alone MUST NOT be used to guess semantic roles.

This section fixes the hash-covered bootstrap location, reference shape, exact-byte digest binding, immutable-artifact input, and fail-closed resolver requirements. `knowledgeforge_governing_contract_resolution_profile_v1@1.0` defines the accepted future architecture for contract manifests; the one fixed native-v1 release-authority family `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`; authority of the checkpoint-qualified `ResolverTrustRelease` uniquely derived from the externally pinned governance checkpoint's complete cross-genesis accepted-release evidence closure; closed root dispatch; typed dependency closure; rule-domain delegation; and closure identity. The profile is uniquely bound to `knowledgeforge_package_content_fingerprint_v1@1.0`; ambient choice among multiple profiles, authority families, or trust releases is prohibited and MUST fail closed. Root digest equality proves exact bytes but not KnowledgeForge authority. Derivation may use exact root and dependency artifacts to calculate a purported descriptor without asserting that KnowledgeForge has authorized the root. Before root-authored rules may support successful independent verification, the verifier MUST establish that the exact root digest, logical identity, kind, media type, package kind, and technical scope are authorized by the uniquely resolved checkpoint-current trust release. The package MUST NOT select or authenticate that release, its genesis, or its derived lineage. Machine-readable schemas, vocabularies, release artifacts, acceptance evidence, conformance vectors, and implementations remain pending. Therefore this document remains not independently implementable; each operation MUST fail closed until all dependencies required for that operation are supplied, accepted where authority is required, implemented, and supported.

## 7. Duplicate-key rejection

Duplicate keys in any JSON object at any depth MUST be rejected. This applies even when duplicate values are textually or semantically equal.

A package containing duplicate keys has no valid v1 content fingerprint and MUST NOT proceed to successful technical verification, admission authorization, canonical insertion, Git publication, production projection, or export as a v1-conformant package.

## 8. Numeric restrictions

JSON floating-point numbers are prohibited. For this specification, any JSON numeric token that is not an integer token—including a token containing a decimal point or exponent—is prohibited.

Non-finite values such as NaN, positive infinity, and negative infinity are prohibited, whether offered through parser extensions or an in-memory producer API.

JSON integers MUST be within the interoperable exact range:

`-9007199254740991` through `9007199254740991`, inclusive.

Exact non-integer quantities MUST be represented as governed canonical decimal strings, not JSON numbers. The governing package, method, calculation, evidence, or schema contract MUST define the decimal string's scale, sign, zero, leading-zero, trailing-zero, and exponent policy. Such strings remain ordinary hash-covered strings under this specification.

The governing contract for each exact-decimal string MUST be identified and versioned through the hash-covered contract-resolution mechanism in Section 6.1. If no single applicable contract can be resolved, or applicable contracts conflict, verification MUST fail closed.

An out-of-range integer, floating-point numeric token, non-finite value, or ungoverned exact-decimal representation MUST fail closed.

## 9. Unicode handling

Unicode MUST NOT be normalized before fingerprinting. In particular, canonically equivalent NFC and NFD strings remain distinct input values unless another hash-covered governing contract explicitly prohibited one representation before finalization.

Implementations MUST follow RFC 8785 string serialization requirements and MUST reject malformed Unicode, including unpaired surrogate code points. A producer or verifier MUST NOT apply case folding, compatibility normalization, locale transformation, or Unicode normalization as part of this fingerprint algorithm.

## 10. Exact `/fingerprints` exclusion

The algorithm excludes exactly one member: the root `/fingerprints` object.

The exclusion MUST occur after strict parsing and rule validation and before RFC 8785 serialization. The exclusion MUST NOT:

- recurse into nested structures;
- remove fields merely because their names contain `fingerprint`, `hash`, `digest`, or `manifest`;
- remove a nested `fingerprints` member;
- remove source, input, method, registry, calculation, normalized-series, external-artifact, or referenced-package identity;
- remove validation, evidence, provenance, lifecycle, applicability, evolution, or statement content.

If the root `/fingerprints` member is absent or is not an object in a purported native v1 package, verification MUST fail closed.

## 11. `/fingerprints` closed-member and non-self-reference rule

For Package Content Fingerprint v1, the root `/fingerprints` object is a closed cycle-breaking container. In a persisted purported-native v1 package it MUST contain exactly one member:

- `package_content_fingerprint`

That member is permitted because its derivation boundary removes the complete root `/fingerprints` object before canonicalization and hashing. No other internal descriptor or convenience copy is permitted by v1. During derivation only, `/fingerprints` MAY be absent or MAY be an empty object; the completed four-member descriptor is attached only after derivation succeeds.

No descriptor stored inside an artifact may claim to hash a derivation boundary that contains that descriptor's own stored value. Consequently:

- a fingerprint over the complete parsed package including `/fingerprints` MUST remain external to that parsed package;
- an exact serialized-file fingerprint over bytes containing `/fingerprints` MUST remain external to those bytes;
- PostgreSQL projection hashes and export query, result-set, or content fingerprints remain external derived records;
- any future additional internal descriptor requires a separately versioned contract with an explicit non-self-referential derivation boundary.

The root `/fingerprints` object MUST NOT hold substantive fingerprints of source evidence, input datasets, methods, registries, calculations, normalized series, other referenced packages, or external artifacts. Those fingerprints MUST appear in hash-covered evidence, provenance, method, input, calculation, or reference structures. Producers and schemas MUST NOT move substantive identity data into the excluded root to avoid hash coverage.

## 12. Prohibition of containing-package self-reference

A containing-package self-reference is a value outside root `/fingerprints` whose semantic role under the resolved versioned package contract is to identify, mirror, or equal the Package Content Fingerprint v1 value of the same containing package.

Containing-package self-references outside `/fingerprints` are prohibited and MUST be rejected. This includes differently named fields such as `package_fingerprint`, `package_manifest`, `content_hash`, or equivalent semantic aliases when the resolved contract assigns them the containing-package v1 role. Unknown or ambiguous semantic roles fail closed under Section 6.1.

This rule prevents circular construction and stale mirrors. It does not prohibit ordinary references to the package's stable non-content identifier, such as `package_id`, when allowed by the package contract.

## 13. Inclusion of upstream and referenced-other-package fingerprints

Fingerprints concerning other packages, source evidence, methods, inputs, registries, calculations, normalized series, and external artifacts MUST remain in the hash-covered content when they are part of the package's substantive evidence or provenance.

A referenced-other-package fingerprint MUST carry a contract-declared target relation and a hash-covered target package identifier sufficient to distinguish it from a containing-package self-reference. Such a reference MUST NOT be removed merely because its value happens to resemble or equal another digest.

## 14. Construction, staging, verification, and admission sequence

A conforming future-native flow MUST preserve this order:

1. Following final-package construction authorization, construct the complete final semantic package content, including hash-covered evidence, provenance, methods, inputs, calculations, statements, applicability, governing-contract references, and pre-finalization fields.
2. Represent exact non-integer quantities as governed canonical decimal strings.
3. Ensure root `/fingerprints` is absent or an empty object; no placeholder, pending digest, incomplete descriptor, or completed descriptor may be supplied to derivation.
4. Derive Package Content Fingerprint v1 from the complete proposed semantic content using the exact algorithm, immutable governing-contract artifacts, and accepted contract-resolution profile defined here.
5. Attach the returned complete four-member descriptor as the sole member at `/fingerprints/package_content_fingerprint`.
6. Produce the exact final repository serialization.
7. Freeze and persist those exact bytes in non-canonical staging, identified by a distinct serialized-artifact digest.
8. Have an independent verifier verify that exact frozen descriptor-bearing artifact and record a verifier-owned result.
9. Have a distinct admission authority evaluate the successfully verified exact artifact and issue `authorized`, `denied`, or `deferred`.
10. Permit canonical insertion only after an unconditional successful `authorized` admission attestation.
11. Treat insertion, repository reconciliation, Git publication, PostgreSQL projection, export generation, and export verification as later separate events governed by the sequence specification.

Steps 1 through 7 MAY occur within one bounded operational attempt, but that operational boundary does not define or expand event authority. Final-package construction authorization authorizes only step 1: construction of complete final semantic package content. Its exact identity MUST bind the derivation evidence for steps 4 and 5, the serialization and non-canonical staging evidence for steps 6 and 7, and the later independent-verification process lineage, but required identity binding grants no authority to perform those later events. The authorization does not authorize Package Content Fingerprint derivation, descriptor attachment, final repository serialization, freezing, non-canonical staging, independent verification or any verification result, deterministic technical validity, admission, canonical insertion, read-back or reconciliation, Git publication, PostgreSQL projection, export generation or verification, or lifecycle action. Its legitimacy, scope, currentness, expiry, withdrawal, and sufficiency are evaluated by admission governance and are not part of the deterministic technical-validity predicate. Absence, mismatch, or invalidity of construction authority or its required process-lineage binding may make the production process inadmissible without changing whether the exact artifact is technically valid under its recorded technical trust context.

Non-canonical staging is pre-admission persistence outside the canonical Knowledge Repository. It is not canonical repository membership, publication, an admission result, or a violation of the prohibition on premature canonical persistence. A producer MAY self-check, but producer self-checking is not independent verification.

The semantic Package Content Fingerprint v1 and serialized-artifact digest are distinct. The former identifies parsed semantic content under this specification; the latter identifies every exact byte of the final repository serialization. Exact digest descriptor details remain a closed record-contract dependency.

The verifier records verification results only. The admission authority records admission results only. No combined “admission/verification result” is owned by the verifier.

### 14.1 Lifecycle and validation-state classification for future native packages

This table governs only future v1-native package design and does not operationally reclassify legacy packages or resolve deferred lifecycle and construction-authorization contracts.

| Information class | v1 classification | Normative treatment |
| --- | --- | --- |
| `status` | deferred pending lifecycle-contract reconciliation | A later authorized reconciliation MUST decide whether each status is fixed pre-finalization content or external lifecycle state. v1 MUST NOT infer that answer. |
| Governance or review state | deferred pending lifecycle-contract reconciliation | Review and governance timing relative to admission remains a separate lifecycle decision. |
| Lifecycle state | deferred pending lifecycle-contract reconciliation | Mutable lifecycle state MUST NOT be inserted after fingerprinting; exact representation remains undecided. |
| Historical promotion metadata | immutable legacy evidence; future contract unresolved | Existing candidate-to-`KnowledgeObjectPackage` promotion semantics and package-local fields remain unchanged. Future final-package construction authorization is external and distinct. |
| Completed pre-fingerprint validation results | hash-covered pre-finalization content | They may attest only to checks completed before derivation and MUST NOT claim successful final-fingerprint verification or admission. |
| Successful post-fingerprint verification and admission results | external post-fingerprint attestations | Verification and admission remain distinct. The verification attestation binds validated package ID, Package Content Fingerprint v1, exact serialized-artifact digest, governing-contract closures, technical trust context, and the exact construction-authorization identity as required process lineage; the verifier checks that this identity is the same identity bound by derivation and serialization/staging evidence but does not evaluate that authority or infer technical validity from it. Admission separately binds the artifact and completed verification and evaluates construction-authorization legitimacy, scope, currentness, expiry, withdrawal, and sufficiency. The combined authority record MUST preserve the exact cross-stage process-lineage binding. Neither attestation is inserted into the package. |
| Failed verification or admission attempts | external non-canonical failure or decision evidence | A separately governed failure-evidence contract MAY bind exact artifact identity and untrusted claimed values but MUST NOT represent an unvalidated package ID or descriptor as validated or use failure evidence as proof of admission. |
| Evidence-integrity assertions | deferred pending lifecycle-contract reconciliation | Substantive evidence/provenance remains hash-covered, but existing assertions such as fingerprint-verification flags require explicit timing and authority reconciliation. |
| Lineage | hash-covered pre-finalization content | Lineage known when the proposed package is finalized is substantive package content; later lineage events require an external record or a separately governed immutable successor. |
| Evolution and supersession assertions | hash-covered pre-finalization content | A package may contain only assertions complete before derivation. Later successor/supersession events require an external record or separately governed immutable successor and MUST NOT mutate the predecessor. |
| Package-local claim that the completed descriptor has already passed independent verification or admission | prohibited package-local claim | The claim can arise only after the descriptor and persisted bytes exist and therefore would create a post-fingerprint mutation or attestation cycle. |

## 15. Independent technical verification and external status separation

An independent verifier MUST:

1. Receive the exact frozen descriptor-bearing staged artifact, separately claimed package ID, serialized-artifact digest, explicitly identified immutable governing-contract artifacts, exact fingerprint-specification artifact, accepted resolution profile, fixed authority-family identity `knowledgeforge_native_package_content_fingerprint_v1_release_authority_family@1.0`, exact externally pinned `governance_checkpoint_boundary_identity` and `governance_checkpoint_result_tuple`, governed Git-tree material, complete cross-genesis checkpoint-derived accepted-release evidence closure, checkpoint-qualified ResolverTrustRelease and all applicable acceptance/withdrawal/supersession/disposition/adjudication/reactivation evidence, exact release-bound conformance-suite artifact and implementation-conformance evidence, any required accepted no-semantic-change decision evidence, the exact technical-trust-context tuple, the derivation and serialization/staging evidence binding the exact final-package construction-authorization identity, and that same exact identity as required verification process lineage, without relying on producer in-memory or ambient state. The checkpoint, authority family, uniquely selected release and derived lineage when resolved, and trust context MUST bind the fingerprint-specification and conformance-suite identities, media types, exact SHA-256 values, implementation-conformance-evidence identity/digest, and any required no-semantic-change decision identity, digest, and Git commit. Invocation may assert an expected derived result only for consistency; it MUST NOT preselect genesis/lineage or narrow checkpoint evidence. The verifier MUST check and record exact equality of the construction-authorization identity across stage-5 derivation evidence, stage-6 serialization/staging evidence, and stage-7 process lineage as a separate process-conformance observation. Required presence and exact binding grant no authority, do not establish the authorization's governance validity, and are not inputs to the deterministic technical-validity predicate.
2. Recalculate the serialized-artifact digest over those exact staged bytes and require equality with the supplied exact-byte identity.
3. Parse the artifact with strict duplicate-key, numeric, Unicode, UTF-8, BOM, and JSON rules.
4. Require root `/fingerprints` to contain exactly `package_content_fingerprint`, and validate the descriptor's exact four-member set, types, and required values.
5. Resolve the fingerprint-specification and conformance-suite bytes from the supplied immutable artifact set; require exact identity, media-type, and SHA-256 equality with the checkpoint-qualified release descriptors; require the fingerprint-specification digest to equal the fingerprint-specification explicit-root digest in `fingerprint_verification_procedure_closure`; validate exact implementation-conformance evidence against the release-bound suite; prove both nonrecursive governance-checkpoint identities, exact commit/tree identities, fixed authority-family identity, and complete cross-genesis governed evidence enumeration; derive the entire-family accepted-release evidence closure, deterministic terminal-candidate set, and unique checkpoint-current release plus derived lineage or exact unresolved classification; and then validate the exact bootstrap reference, resolver profile, uniquely selected trust release and external governance-event evidence, root authorization before root-authored rule execution, governing-contract artifact digests, and complete applicable immutable technical contract closure under `docs/governing_contract_resolution_profile_v1.md`.
6. Repeat package schema, complete hash-covered content, package-ID, decimal, semantic-role, target-relation, reservation, and containing-package self-reference validation independently.
7. Require the validated parsed package ID to equal the separately claimed package ID exactly.
8. Remove exactly root `/fingerprints` from a deep copy, produce RFC 8785 canonical UTF-8 bytes, calculate SHA-256, construct the expected descriptor, and require exact descriptor equality.
9. Fail closed on any missing fingerprint-specification or conformance-suite artifact, unsupported or wrong media type, identity or digest mismatch, absent/mismatched implementation-conformance evidence, procedure-closure-root mismatch, package attempt to select specification bytes, same-identity changed bytes without applicable immutable accepted exact-bound no-semantic-change evidence, missing/unknown/mismatched authority-family identity, invocation attempt to preselect genesis or lineage, incomplete cross-genesis or mismatched governance-checkpoint tree material, omitted or conflicting governed release/event evidence, zero or multiple eligible terminal releases in checkpoint-current mode, conflicting adjudication, other difference, or unresolved dependency.
10. Record a verifier-owned result with the fingerprint-specification identity, media type, and exact SHA-256; conformance-suite identity, media type, and exact SHA-256 plus implementation-conformance-evidence identity/digest; any required no-semantic-change decision identity, digest, and Git commit; exact authority-family identity; exact `governance_checkpoint_boundary_identity`, `governance_checkpoint_result_tuple`, and tree identities; complete accepted-release evidence-closure identity; verification mode; selected checkpoint-current release and derived lineage when unique or exact unresolved classification and candidate-genesis/branch/terminal sets; exact historical designation when applicable; all applicable disposition/adjudication evidence; exact artifact; technical-trust-context; authorized root; package technical closure; and verification-procedure closure bindings; verifier identity/role; implementation identity/version; outcome; completion time; attestation identity/content digest; and failure reason where applicable. The result MUST NOT claim unqualified global currentness. It MUST record the exact construction-authorization identity and result of checking its cross-stage binding as required process lineage, separately from the deterministic technical outcome. It MUST NOT infer technical validity from that identity or adjudicate its legitimacy, scope, currentness, expiry, withdrawal, or sufficiency.
11. Assign `native_package_content_fingerprint_v1_valid` upon successful independent technical verification of the exact artifact. Before success, it is merely `purported_package_content_fingerprint_v1`.

This specification does not contain or predict its own exact artifact digest. A future externally accepted ResolverTrustRelease supplies the digest of the already-finalized and published fingerprint-specification artifact that it authorizes. This external exact-artifact binding does not change the Package Content Fingerprint v1 algorithm. An editorially revised artifact may retain the same logical algorithm identity only when an accepted decision explicitly establishes that technical semantics did not change; it still has a new exact digest and requires a new ResolverTrustRelease before it may be used for verification. A technical semantic change requires the applicable successor specification or profile identities.

Technical fingerprint verification status, admission-authorization status, canonical-insertion status, Git-publication status, PostgreSQL-projection status, export-generation status, export-verification status, and later lifecycle status are separate dimensions.

A fingerprint-valid artifact may be denied or deferred admission. Denial or deferral does not make its correctly computed fingerprint invalid. Technical validity alone does not make an artifact admitted, insertion-ready, canonical, inserted, Git-published, projected, exported, or current. A fingerprint-invalid or incompletely verified artifact cannot receive successful admission authorization.

The verifier MUST NOT issue admission authorization or evaluate construction-authorization legitimacy, scope, currentness, expiry, withdrawal, or sufficiency as part of the deterministic technical predicate. The admission authority MUST explicitly reference the completed successful verification attestation, bind the same artifact and technical-trust-context tuple, and separately evaluate construction authorization and admission policy. The independent verifier SHOULD be implemented or tested across more than one runtime or language before production authorization.

## 16. Cycle-breaking rule

Cycle freedom is obtained by exactly three rules used together:

1. root `/fingerprints` is excluded from the hash basis; and
2. persisted v1 packages permit only `package_content_fingerprint` inside `/fingerprints`, with the root-exclusion derivation boundary defined here; and
3. containing-package content-fingerprint self-references outside `/fingerprints` are prohibited.

No fixed-point search, repeated rehashing until stability, recursive fingerprint-field deletion, or producer-order convention is part of v1. A package that requires any such procedure is non-conformant.

## 17. Failure semantics

Conformance is fail-closed. Any parse error, BOM, duplicate key, malformed Unicode, prohibited numeric value, absent or malformed bootstrap reference, unavailable or digest-mismatched contract artifact, unsupported or unresolvable contract/algorithm/media-type/version, ambiguous applicability, conflicting rules, ungoverned field requiring governance, malformed descriptor, package-ID mismatch, digest mismatch, containing-package self-reference, additional root `/fingerprints` member, or closed-member-rule violation MUST cause v1 verification failure.

Any hash-covered mutation after finalization produces a different artifact for which the prior Package Content Fingerprint v1 value is invalid. It does not invalidate, alter, or diminish the preserved predecessor artifact or the correctness of that predecessor's fingerprint for its original bytes and content. If the changed artifact retains the old descriptor, independent verification detects a digest mismatch. If its content and descriptor are both recomputed, a separately persisted changed artifact MUST receive the identity and version required by the applicable package and lifecycle contracts and MUST enter a separately authorized lifecycle-permitted finalization. Where canonical overwrite prohibition applies, one package ID MUST NOT identify different canonical bytes. Successor and supersession treatment remains separately governed; this rule neither authorizes a successor nor retroactively makes any legacy defect valid. Artifact-only verification does not claim to reconstruct unrecorded producer history; repository immutability and external records keyed by package ID plus fingerprint provide the cross-artifact detection boundary.

If any byte changes after verification or admission, the former serialized-artifact digest no longer identifies the artifact, and the former verification and admission evidence cannot authorize it. The changed bytes MUST be frozen as a new staged artifact and receive a new exact digest, independent verification, and admission decision. Semantic fingerprint equality does not waive exact-byte reauthorization. Canonical insertion MUST install the exact admitted bytes unchanged; parsing and reserialization, normalization, whitespace or escaping changes, member-order changes, newline changes, and every other byte change are prohibited before insertion.

Failure MUST NOT be rewritten as a warning merely because full-file persistence, repository indexing, PostgreSQL projection, or export payload fidelity succeeds.

A failed package MUST NOT be represented as `native_package_content_fingerprint_v1_valid`. Its preservation, rejection, quarantine, successor, or lifecycle disposition requires the separately governed stage applicable to that package.

## 18. Distinction from other fingerprints

| Identity | Boundary | Relationship to v1 |
| --- | --- | --- |
| Package Content Fingerprint v1 | Complete final parsed semantic package minus exactly root `/fingerprints`, RFC 8785 UTF-8 | The future authoritative semantic content identity defined here. |
| Full parsed-package fingerprint | Complete parsed package including `/fingerprints` | Different boundary; MUST remain external to that parsed package and MUST NOT be called v1. |
| Serialized-file fingerprint | Exact stored bytes, including whitespace and formatting | Physical artifact identity; when its boundary contains `/fingerprints`, it MUST remain external to those bytes and MUST NOT be called v1. |
| Repository fingerprint | Aggregate repository manifest, package set, indexes, and/or package identities under a repository contract | Repository reconciliation identity; not package semantic identity. |
| Projection payload hash | Exact or canonicalized payload persisted in a derived projection | Projection fidelity identity; does not prove v1 validity. |
| Source-evidence fingerprint | Exact source payload, snapshot, release, query result, or SourceEvidencePackage identity | Substantive upstream identity; MUST remain in hash-covered evidence/provenance structures when used. |

Unqualified terms such as `package_fingerprint` SHOULD NOT be introduced in new contracts because they obscure the hashed boundary.

## 19. Legacy classifications

Legacy classification is external compatibility and lifecycle metadata. It MUST NOT rewrite existing package bytes or stored `fingerprints.package_manifest` values.

The following categories are governed:

1. `legacy_manifest_recomputed_valid`
   - The stored legacy outer `fingerprints.package_manifest` recomputes under its historical rule and no deprecated containing-package mirror is present.
2. `legacy_manifest_valid_with_deprecated_self_mirror`
   - The stored legacy outer value recomputes under its historical rule, but the package contains a deprecated containing-package mirror.
3. `legacy_manifest_invalid_post_hash_mutation`
   - The stored legacy outer value does not recompute because hash-covered content was mutated after the historical hash; this is the Campaign 35 defect class.
4. `legacy_manifest_invalid_self_reference_order`
   - The stored legacy outer value does not recompute because containing-package mirror insertion/update and outer hashing occurred in an incoherent order; this is the Campaign 37 defect class.
5. `native_package_content_fingerprint_v1_valid`
   - Reserved exclusively for future packages whose exact frozen descriptor-bearing artifact passes implemented independent v1 technical verification under the complete applicable immutable governing-contract set. Admission is a separate status.

The five invalid legacy outer manifests measured in the 2026-07-15 560-package corpus MUST remain preserved and require later lifecycle adjudication before any successor is created. This corpus-scoped count does not preclude future audits from discovering additional defects. The 35 deprecated containing-package mirror occurrences measured in that corpus, including 33 stale mirrors, are non-authoritative legacy fields. A stale mirror alone does not require a successor when the authoritative legacy outer manifest remains valid.

No current package MAY be classified as `native_package_content_fingerprint_v1_valid`.

The five anomalous packages may remain historically accepted under their original governance while not being technically valid under this future native-v1 contract. Historical acceptance and native-v1 technical validity are separate classifications. This amendment does not alter the measured zero-current-native-v1 result.

## 20. PostgreSQL implications

PostgreSQL remains a derived operational projection. This specification does not change its schema, data, authority, loader, verifier, rebuild process, or publication state.

A future separately authorized projection MAY expose the v1 descriptor, package ID, full payload, serialized/payload hash, and external verification status. It MUST preserve the distinction between:

- exact payload fidelity;
- projection payload hash validity;
- legacy manifest status; and
- Package Content Fingerprint v1 validity.

PostgreSQL MUST NOT originate or mutate a canonical v1 package, and database agreement MUST NOT be treated as proof that the package content fingerprint is valid.

For conforming future-native production, successful Git publication precedes PostgreSQL projection. A separately authorized prepublication test projection is non-authoritative, non-production, preview-only, and nonconforming with the completed production sequence; it proves no earlier stage and cannot support consumer export publication.

## 21. Relationship Export Contract v1 implications

Relationship Export Contract v1 remains unchanged. This specification does not alter export fields, query semantics, result-set fingerprints, consumer simulations, or relationship package publication.

A future export-contract revision MAY carry Package Content Fingerprint v1 only after separate authorization and compatibility analysis. Export fidelity MUST remain distinct from package-content-fingerprint validity.

Export generation or materialization occurs after the applicable production projection. Independent export verification is a distinct later event. Neither may rewrite canonical packages or establish earlier authority.

## 22. Required future conformance vectors

Before implementation may be authorized for production, conformance vectors MUST cover at least:

- object member reordering;
- insignificant whitespace and permitted escape-form differences;
- array-order sensitivity;
- empty and nested objects/arrays;
- exact root `/fingerprints` exclusion;
- nested `fingerprints` inclusion;
- mutation of every representative hash-covered section;
- descriptor value replacement without hash-basis change;
- duplicate keys at root and nested depths;
- duplicate keys expressed with escaped-equivalent names, including `"a"` and `"\u0061"`;
- initial UTF-8 BOM rejection;
- minimum and maximum permitted integers;
- integers immediately outside the permitted range;
- decimal-point and exponent JSON numeric tokens;
- parser-extension NaN and infinities;
- canonical decimal strings and rejected non-canonical decimal strings under a governing contract;
- absent or malformed `/governing_contracts/package_contract` bootstrap references;
- correct release/specification/procedure-root equality, missing fingerprint-specification bytes, unsupported or wrong fingerprint-specification media type, specification-identity mismatch, release-bound digest mismatch including same-ID/different-byte material, and procedure-closure-root mismatch;
- package- or producer-selected fingerprint-specification bytes and same-ID changed bytes with absent, invalid, or non-exact-bound no-semantic-change evidence;
- all eighteen authority-family/checkpoint conformance cases in `docs/governing_contract_resolution_profile_v1.md` Section 21, including complete cross-genesis enumeration, invocation non-selection, deterministic linear-chain head resolution, zero/one/multiple terminal candidates, withdrawal without fallback, explicit reactivation, sibling forks, conflicting and adequate same-checkpoint adjudication, later-checkpoint historical preservation, unknown/mismatched authority family, nonrecursive checkpoint identities, different-checkpoint non-interchangeability, admission checkpoint mismatch, historical/unqualified-current misuse, unknown governed evidence, and incomplete Git tree material;
- missing, digest-mismatched, mutable, ambiguously selected, and unknown governing-contract artifacts;
- unauthorized roots, wrong-scope roots, package-selected or ambiguous trust releases, release/profile mismatch, invalid acceptance evidence, release downgrade, and root identity/digest collisions;
- unsupported contract-artifact media types and versions;
- exact RFC 6901 pointer escaping, array indices, missing targets, and malformed-pointer rejection;
- prohibited pointer patterns and, for any future accepted pattern profile, deterministic expansion plus empty/non-unique expansion rejection;
- ambiguous applicability, precedence conflicts, contradictory rules, and fields requiring governance without a governing rule;
- Unicode composed/decomposed distinction;
- Unicode escaping and malformed surrogate rejection;
- containing-package self-reference rejection under multiple field names;
- referenced-other-package fingerprint inclusion;
- source, input, method, registry, calculation, normalized-series, and external-artifact fingerprint inclusion;
- additional root `/fingerprints` members and internal physical/full-package descriptors whose boundary contains their own stored value;
- external full-parsed-package, exact-file-byte, PostgreSQL-projection, and export fingerprints that remain outside their hashed artifact;
- claimed package-ID mismatch with the parsed package ID;
- post-fingerprint semantic mutation;
- malformed, unknown, and future descriptor versions;
- cross-language canonical-byte and digest equality.

Vectors MUST include positive and negative cases and MUST publish the exact input bytes, expected parse disposition, expected canonical bytes where valid, expected digest where valid, and expected failure reason where invalid.

## 23. Versioning and fail-closed behavior

The specification identifier and descriptor shape are versioned together. A semantic change to the hash boundary, digest algorithm or encoding, fixed descriptor member values or semantics, canonicalization, parsing restrictions, number policy, Unicode policy, closed `/fingerprints` member rule, or self-reference rule requires a new specification identifier.

Implementations MUST NOT silently treat an unknown future identifier as v1. Producers, validators, projections, and consumers MUST fail closed or explicitly classify the package as unsupported until the version is implemented and authorized.

Compatibility mappings MUST be external and MUST NOT mutate historical package bytes.

## 24. Explicit non-goals

This accepted architectural core does not:

- implement RFC 8785;
- implement the accepted Governing Contract Resolution Profile v1, its machine-readable trust-release, governance-checkpoint, governed-namespace/enumeration, Git-tree completeness-proof, accepted-release evidence-closure, manifest, technical closure, vocabulary, selector, acceptance-evidence, conformance, or verifier-invocation contracts;
- implement or modify a producer, parser, validator, schema, migration, registry, repository index, projection, export, or consumer;
- repair, rewrite, normalize, or reclassify current packages operationally;
- create successors or alter lifecycle state;
- redefine historical candidate-to-object promotion or settle the future standardized construction-authorization contract;
- make PostgreSQL canonical;
- change Relationship Export Contract v1;
- define a universal decimal ontology for all methods;
- define a serialized-file or repository fingerprint;
- authorize production package generation;
- authorize publication;
- implement staging, admission, insertion, Git publication, PostgreSQL projection, export generation, export verification, authority-record placement, failure-evidence storage, or lifecycle handling.
