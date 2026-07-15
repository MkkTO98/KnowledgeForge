# KnowledgeForge Package Content Fingerprint v1

Date: 2026-07-15
Status: accepted architectural core; not independently implementable; contract-resolution profile pending; not implemented; not authorized for production package generation
Specification identifier: `knowledgeforge_package_content_fingerprint_v1@1.0`

Normative terms in this document are `MUST`, `MUST NOT`, `SHOULD`, and `MAY`.

## 1. Purpose and authority

This specification defines the future authoritative content fingerprint for a KnowledgeForge package. Its purpose is to identify the complete final parsed semantic package without circularly hashing the descriptor that carries the fingerprint.

For a package that conforms to this specification, the authoritative field is:

`fingerprints.package_content_fingerprint`

This specification is an accepted architectural core. Its content-fingerprint boundary and descriptor are decided, but independent conformance remains incomplete until a separately accepted, versioned contract-resolution profile defines the contract-artifact representation and rule vocabulary required by Section 6.1. Until then, derivation and verification MUST fail closed. This document does not claim that producers, validators, schemas, repository persistence, PostgreSQL projection, exports, or consumers currently enforce it.

## 2. Applicability and non-retroactivity

This specification applies only to future packages created under a separately authorized implementation that explicitly declares conformance to `knowledgeforge_package_content_fingerprint_v1@1.0`.

It MUST NOT be applied retroactively to existing packages. Existing `fingerprints.package_manifest` values MUST remain immutable legacy values and MUST NOT be reinterpreted as Package Content Fingerprint v1 values.

No current package is classified as native v1-valid. A package carrying the descriptor and claiming the governing contract is only `purported_package_content_fingerprint_v1`; the descriptor is a claim, not proof of acceptance. `native_package_content_fingerprint_v1_valid` may be assigned only by an independently implemented verifier after successful verification and admission. A production package MUST NOT adopt this contract until the contract-resolution profile, implementation, independent validation, conformance vectors, legacy handling, and the applicable production gate have been separately authorized and completed.

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

Derivation and verification are distinct normative operations. Derivation receives a proposed package whose hash-covered content is finalized and complete; it does not require or accept a completed Package Content Fingerprint v1 descriptor. Verification receives a persisted purported-native package and requires the exact completed descriptor.

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
    accepted_contract_resolution_profile
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
        accepted_contract_resolution_profile
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

The accepted contract-resolution profile is a required explicit input, not ambient or producer-private knowledge. While that profile remains pending under Section 6.1, both operations MUST fail closed before claiming conformance.

Only the root member selected by the RFC 6901 JSON Pointer `/fingerprints` is removed. No nested member named `fingerprints`, no recursively discovered fingerprint-like field, and no other root member is removed.

## 5. RFC 8785 canonicalization

The hash basis MUST be serialized using RFC 8785 JSON Canonicalization Scheme semantics and encoded as UTF-8 before hashing.

Object member order, source whitespace, insignificant escape-form differences, and source serialization layout MUST NOT affect the result when they parse to the same permitted JSON value. Array order remains semantically significant and MUST be preserved.

An implementation MUST identify and test a concrete RFC 8785 implementation or conforming implementation strategy before production authorization. Ordinary `json.dumps(sort_keys=True)` behavior MUST NOT be claimed as RFC 8785 conformance without independent proof.

## 6. JSON parsing requirements

The exact package bytes presented for admission or verification MUST be parsed as one JSON document with a root object. Trailing non-whitespace data, malformed UTF-8, malformed JSON, unsupported values, and parser recovery MUST be rejected.

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

If a future profile permits pointer patterns, that profile MUST define its grammar and version; evaluation root; escaping; array expansion; deterministic expansion order; missing-target behavior; duplicate-target elimination; and uniqueness rules. Empty or non-unique expansion MUST fail closed. Until that profile is accepted, patterns are unsupported.

For multiple applicable contracts, the pending profile MUST provide deterministic applicability, precedence, and conflict rules. No lower-precedence rule may silently weaken or contradict a higher-precedence rule; contradictions and ambiguous applicability MUST fail closed. A field whose representation or semantic role requires governance but has no applicable rule MUST fail closed. Field names or digest-shaped values alone MUST NOT be used to guess semantic roles.

This section fixes the hash-covered bootstrap location, reference shape, exact-byte digest binding, immutable-artifact input, and fail-closed resolver requirements. Repository evidence does not yet establish the contract-artifact media type, internal contract-document schema, complete rule vocabulary, cross-contract applicability/precedence model, or immutable identity and deterministic binding of exactly one resolution profile to this specification identifier. Those choices require a separately accepted, versioned contract-resolution profile. The profile MUST be uniquely and immutably bound to `knowledgeforge_package_content_fingerprint_v1@1.0` or a successor specification identifier; ambient choice among multiple profiles is prohibited and MUST fail closed. Therefore this document is an accepted architectural core, not an independently implementable conformance contract; derivation and verification MUST fail closed until that profile and binding are supplied and supported.

## 7. Duplicate-key rejection

Duplicate keys in any JSON object at any depth MUST be rejected. This applies even when duplicate values are textually or semantically equal.

A package containing duplicate keys has no valid v1 content fingerprint and MUST NOT proceed to v1 admission, promotion, repository insertion, projection activation, or export as a v1-conformant package.

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

## 14. Construction and finalization sequence

A conforming future producer MUST use this sequence:

1. Construct the complete semantic package, including all hash-covered evidence, provenance, methods, inputs, calculations, statements, applicability, contract references, and fields classified as pre-finalization content in Section 14.1.
2. Represent exact non-integer quantities as governed canonical decimal strings.
3. Ensure root `/fingerprints` is absent or is an empty object. A placeholder, pending digest, incomplete descriptor, or completed descriptor MUST NOT be supplied to derivation.
4. Invoke `derive_package_content_fingerprint_v1` with the exact proposed serialized package bytes, immutable contract artifacts, and the accepted contract-resolution profile.
5. Derivation independently performs strict parsing, bootstrap and contract resolution, complete hash-covered content validation, package-ID validation, self-reference checks, exact root exclusion, RFC 8785 canonicalization, and SHA-256 calculation.
6. Only after derivation succeeds, attach the returned complete four-member descriptor as the sole member at `/fingerprints/package_content_fingerprint`.
7. Freeze the complete package. No hash-covered field may change after this point.
8. Serialize and persist only through a separately authorized admission path.
9. Independently verify the persisted bytes under Section 15.
10. Record authoritative post-fingerprint admission and verification results externally.

No placeholder or pending digest may be serialized, persisted, admitted, projected, or exported. A producer MAY self-check the result, but producer self-checking is not independent verification.

### 14.1 Lifecycle and validation-state classification for future native packages

This table governs only future v1-native package design and does not operationally reclassify legacy packages or resolve the deferred promotion policy.

| Information class | v1 classification | Normative treatment |
| --- | --- | --- |
| `status` | deferred pending promotion-policy reconciliation | A later authorized reconciliation MUST decide whether each status is fixed pre-finalization content or external lifecycle state. v1 MUST NOT infer that answer. |
| Governance or review state | deferred pending promotion-policy reconciliation | Review and governance timing relative to admission remains a separate lifecycle decision. |
| Lifecycle state | deferred pending promotion-policy reconciliation | Mutable lifecycle state MUST NOT be inserted after fingerprinting; exact representation remains undecided. |
| Promotion metadata | deferred pending promotion-policy reconciliation | Existing candidate-to-object semantics remain unchanged until separately reconciled. |
| Completed pre-fingerprint validation results | hash-covered pre-finalization content | They may attest only to checks completed before derivation and MUST NOT claim successful final-fingerprint verification or admission. |
| Successful post-fingerprint verification or admission results | external post-fingerprint record | They MUST be keyed externally by validated package ID and Package Content Fingerprint v1 value and MUST NOT be inserted into the package. |
| Failed verification or admission attempts | external post-fingerprint record | This specification does not define their external identity when package ID or descriptor validation fails. A separately governed admission contract MAY record an exact external artifact identity and untrusted claimed values, but MUST NOT represent an unvalidated package ID or descriptor as validated. |
| Evidence-integrity assertions | deferred pending promotion-policy reconciliation | Substantive evidence/provenance remains hash-covered, but existing assertions such as fingerprint-verification flags require explicit timing and authority reconciliation. |
| Lineage | hash-covered pre-finalization content | Lineage known when the proposed package is finalized is substantive package content; later lineage events require an external record or a separately governed immutable successor. |
| Evolution and supersession assertions | hash-covered pre-finalization content | A package may contain only assertions complete before derivation. Later successor/supersession events require an external record or separately governed immutable successor and MUST NOT mutate the predecessor. |
| Package-local claim that the completed descriptor has already passed independent verification or admission | prohibited package-local claim | The claim can arise only after the descriptor and persisted bytes exist and therefore would create a post-fingerprint mutation or attestation cycle. |

## 15. Independent verification sequence

An independent verifier MUST:

1. Receive the exact serialized persisted package artifact, its claimed package ID, an explicitly identified immutable contract-artifact set, and an accepted contract-resolution profile without relying on producer in-memory or ambient state.
2. Parse it with strict duplicate-key, numeric, Unicode, UTF-8, BOM, and JSON rules.
3. Require root `/fingerprints` to contain exactly `package_content_fingerprint`, and validate the descriptor's exact four-member set, types, and required values.
4. Validate the exact bootstrap reference at `/governing_contracts/package_contract`, verify the contract artifact's exact-byte SHA-256 digest, and resolve every applicable contract under the accepted profile.
5. Repeat package schema, complete hash-covered content, package-ID, decimal, semantic-role, target-relation, reservation, and containing-package self-reference validation independently.
6. Require the validated parsed package ID to equal the separately claimed package ID exactly.
7. Deep-copy the complete final parsed package and remove exactly root `/fingerprints`.
8. Independently produce the RFC 8785 canonical UTF-8 bytes and calculate SHA-256.
9. Construct the expected complete four-member descriptor and compare it with the stored descriptor using exact member, type, token, and value equality.
10. Fail closed on any difference or unresolved dependency.
11. Record a successful admission/verification result externally, keyed by the validated package ID and stored Package Content Fingerprint v1 value. If verification fails before both values validate, any external failure record is governed separately and MUST NOT present untrusted claimed values as validated keys.
12. Assign `native_package_content_fingerprint_v1_valid` only after successful verification and admission; before that, the artifact is merely `purported_package_content_fingerprint_v1`.

The independent verifier SHOULD be implemented or tested across more than one runtime or language before production authorization.

## 16. Cycle-breaking rule

Cycle freedom is obtained by exactly three rules used together:

1. root `/fingerprints` is excluded from the hash basis; and
2. persisted v1 packages permit only `package_content_fingerprint` inside `/fingerprints`, with the root-exclusion derivation boundary defined here; and
3. containing-package content-fingerprint self-references outside `/fingerprints` are prohibited.

No fixed-point search, repeated rehashing until stability, recursive fingerprint-field deletion, or producer-order convention is part of v1. A package that requires any such procedure is non-conformant.

## 17. Failure semantics

Conformance is fail-closed. Any parse error, BOM, duplicate key, malformed Unicode, prohibited numeric value, absent or malformed bootstrap reference, unavailable or digest-mismatched contract artifact, unsupported or unresolvable contract/algorithm/media-type/version, ambiguous applicability, conflicting rules, ungoverned field requiring governance, malformed descriptor, package-ID mismatch, digest mismatch, containing-package self-reference, additional root `/fingerprints` member, or closed-member-rule violation MUST cause v1 verification failure.

Any hash-covered mutation after finalization produces a different artifact for which the prior Package Content Fingerprint v1 value is invalid. It does not invalidate, alter, or diminish the preserved predecessor artifact or the correctness of that predecessor's fingerprint for its original bytes and content. If the changed artifact retains the old descriptor, independent verification detects a digest mismatch. If its content and descriptor are both recomputed, a separately persisted changed artifact MUST receive the identity and version required by the applicable package and lifecycle contracts and MUST enter a separately authorized lifecycle-permitted finalization. Where canonical overwrite prohibition applies, one package ID MUST NOT identify different canonical bytes. Successor and supersession treatment remains separately governed; this rule neither authorizes a successor nor retroactively makes any legacy defect valid. Artifact-only verification does not claim to reconstruct unrecorded producer history; repository immutability and external records keyed by package ID plus fingerprint provide the cross-artifact detection boundary.

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
   - Reserved exclusively for future packages that pass implemented independent v1 verification and admission.

The five invalid legacy outer manifests measured in the 2026-07-15 560-package corpus MUST remain preserved and require later lifecycle adjudication before any successor is created. This corpus-scoped count does not preclude future audits from discovering additional defects. The 35 deprecated containing-package mirror occurrences measured in that corpus, including 33 stale mirrors, are non-authoritative legacy fields. A stale mirror alone does not require a successor when the authoritative legacy outer manifest remains valid.

No current package MAY be classified as `native_package_content_fingerprint_v1_valid`.

## 20. PostgreSQL implications

PostgreSQL remains a derived operational projection. This specification does not change its schema, data, authority, loader, verifier, rebuild process, or publication state.

A future separately authorized projection MAY expose the v1 descriptor, package ID, full payload, serialized/payload hash, and external verification status. It MUST preserve the distinction between:

- exact payload fidelity;
- projection payload hash validity;
- legacy manifest status; and
- Package Content Fingerprint v1 validity.

PostgreSQL MUST NOT originate or mutate a canonical v1 package, and database agreement MUST NOT be treated as proof that the package content fingerprint is valid.

## 21. Relationship Export Contract v1 implications

Relationship Export Contract v1 remains unchanged. This specification does not alter export fields, query semantics, result-set fingerprints, consumer simulations, or relationship package publication.

A future export-contract revision MAY carry Package Content Fingerprint v1 only after separate authorization and compatibility analysis. Export fidelity MUST remain distinct from package-content-fingerprint validity.

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
- missing, digest-mismatched, mutable, ambiguously selected, and unknown governing-contract artifacts;
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

The specification identifier and descriptor shape are versioned together. A semantic change to the hash boundary, canonicalization, parsing restrictions, number policy, Unicode policy, closed `/fingerprints` member rule, or self-reference rule requires a new specification identifier.

Implementations MUST NOT silently treat an unknown future identifier as v1. Producers, validators, projections, and consumers MUST fail closed or explicitly classify the package as unsupported until the version is implemented and authorized.

Compatibility mappings MUST be external and MUST NOT mutate historical package bytes.

## 24. Explicit non-goals

This accepted architectural core does not:

- implement RFC 8785;
- define or accept the pending contract-resolution profile, its immutable identity/binding, media type, contract-document schema, rule vocabulary, applicability model, or precedence model;
- implement or modify a producer, parser, validator, schema, migration, registry, repository index, projection, export, or consumer;
- repair, rewrite, normalize, or reclassify current packages operationally;
- create successors or alter lifecycle state;
- reconcile candidate-to-object promotion policy;
- make PostgreSQL canonical;
- change Relationship Export Contract v1;
- define a universal decimal ontology for all methods;
- define a serialized-file or repository fingerprint;
- authorize production package generation;
- authorize publication.
