# D-20260715 — Package Content Fingerprint v1 Architectural Acceptance

Date: 2026-07-15
Status: Accepted architectural core; contract-resolution profile pending; not independently implementable; not implemented; production gate closed
Decision class: package semantic integrity and canonical fingerprint authority
Normative specification: `docs/package_content_fingerprint_v1.md`

## Decision

KnowledgeForge accepts `knowledgeforge_package_content_fingerprint_v1@1.0` as the architectural core of the future package semantic-content fingerprint contract. Independent conformance remains incomplete until a separately accepted contract-resolution profile defines the contract-artifact representation and rule vocabulary required by the normative specification.

The authoritative future field is:

`fingerprints.package_content_fingerprint`

Its value is SHA-256 over the RFC 8785 canonical UTF-8 serialization of the complete final parsed package after removing exactly the root `/fingerprints` member.

Duplicate JSON object keys are rejected. JSON floating-point and non-finite values are prohibited. Integers are limited to the interoperable exact range `-9007199254740991` through `9007199254740991`. Exact non-integer quantities use governed canonical decimal strings. Unicode is not normalized during fingerprinting.

Containing-package self-references outside `/fingerprints` are prohibited. Fingerprints for other packages, source evidence, methods, inputs, registries, calculations, normalized series, and external artifacts remain hash-covered.

For v1, the root `/fingerprints` object is a closed cycle-breaking container whose only permitted persisted member is `package_content_fingerprint`. It cannot contain convenience copies, full-parsed-package fingerprints, exact-file-byte fingerprints over bytes containing the descriptor, PostgreSQL projection hashes, export fingerprints, or substantive upstream/referenced identity. Any future internal descriptor requires a separately versioned explicit non-self-referential derivation boundary.

Purported native v1 packages must carry an exact hash-covered package-contract bootstrap at RFC 6901 JSON Pointer `/governing_contracts/package_contract`, binding contract ID, version, and media type to a SHA-256 digest over exact immutable contract bytes. Contract ID/version alone, mutable `latest` resolution, unpinned network retrieval, ambient search, and producer-private registry state are insufficient. The verifier receives immutable contract artifacts explicitly and fails closed on absence, digest mismatch, unsupported media type/version, ambiguity, conflict, or an ungoverned field requiring a rule.

The bootstrap location and digest binding are accepted, but repository evidence does not yet establish the contract artifact's media type, internal schema, complete rule vocabulary, cross-contract applicability/precedence model, or immutable identity and deterministic binding of exactly one resolution profile to this specification identifier. These remain a separate contract-resolution-profile decision. Ambient choice among multiple profiles is prohibited and fails closed. Until one profile is uniquely and immutably bound, accepted, and supplied, derivation and verification fail closed; this record does not claim an independently implementable conformance contract.

Derivation and verification are separate. Derivation receives complete hash-covered proposed content with `/fingerprints` absent or empty and returns the complete four-member descriptor; it never requires a completed descriptor. The descriptor is attached only after successful derivation, and no placeholder or pending digest may be serialized, persisted, admitted, projected, or exported. Verification receives persisted bytes containing the exact completed descriptor and repeats parsing, contract resolution, content validation, root exclusion, RFC 8785 canonicalization, SHA-256 calculation, and descriptor comparison independently.

A descriptor-bearing package is only `purported_package_content_fingerprint_v1`. `native_package_content_fingerprint_v1_valid` is assigned only after successful independent verification and admission. Internal validation state may contain only completed pre-fingerprint checks. Successful post-fingerprint admission and verification records are external and keyed by validated package ID and Package Content Fingerprint v1 value. If either value fails validation, any external failure record is separately governed and cannot present an untrusted claimed value as a validated key.

## Integrity defect that triggered review

The review was triggered by a concrete mismatch between the repository's claimed deterministic package-manifest identity and the final stored package content.

A read-only corpus recomputation of the historical outer-manifest rule over all 560 canonical package files in the 2026-07-15 corpus found five stored `fingerprints.package_manifest` values that do not recompute from the final package with root `fingerprints` omitted:

### Campaign 35 — `legacy_manifest_invalid_post_hash_mutation`

1. `knowledge_repository/objects/pkg-object-srcpkg-campaign35-dnk-exports-share-statistical-summary-v2.json`
2. `knowledge_repository/objects/pkg-object-srcpkg-campaign35-nor-exports-share-statistical-summary-v2.json`
3. `knowledge_repository/objects/pkg-object-srcpkg-campaign35-swe-exports-share-statistical-summary-v2.json`

These three packages represent the post-hash semantic-mutation defect class: the final stored hash-covered content differs from the content on which the outer legacy manifest was calculated.

### Campaign 37 — `legacy_manifest_invalid_self_reference_order`

4. `knowledge_repository/objects/pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1.json`
5. `knowledge_repository/objects/pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1.json`

These two packages represent the self-reference-order defect class. Their producers calculated an outer manifest, inserted that value into `generated_statements[0].structured_payload.package_fingerprint`, recalculated the outer manifest, then replaced the nested mirror with the new outer value without a final coherent recomputation. The nested value equals the stored outer value, but the stored outer value does not hash the final package content under the historical rule.

The defect is integrity-significant even though repository and PostgreSQL full-payload reconciliation can remain exact: faithful storage or projection can preserve an invalid embedded semantic manifest.

## Containing-package mirror evidence

The read-only corpus scan identified 35 occurrences at:

`/generated_statements/0/structured_payload/package_fingerprint`

that describe the containing package rather than another package.

- 2 occurrences equal the stored outer legacy manifest: the two Campaign 37 packages listed above.
- 33 occurrences are stale relative to the final stored outer legacy manifest.

All 35 are deprecated and non-authoritative. The 33 stale mirrors do not alone require successors when the authoritative legacy outer manifest recomputes under its historical rule. Fingerprints in explicit `raw_package_reference` or equivalent structures that identify another package are not containing-package mirrors and remain substantive hash-covered references.

## Alternatives and rationale

### Candidate A rejected for future packages

For this decision, Candidate A means retaining `fingerprints.package_manifest` and its producer-specific historical construction behavior as the future authoritative package-content identity.

Candidate A is rejected because:

- five committed outer manifests in the measured 2026-07-15 560-package corpus do not recompute from final stored semantic content;
- producer mutation order differs across campaign implementations;
- containing-package mirrors create circularity and stale values;
- the historical serialization profile is Python-specific canonical-like JSON, not a complete cross-language contract;
- the unqualified term `package_manifest` obscures the exact semantic boundary;
- continuing the field would preserve ambiguity between a semantic package hash, a manifest projection, and a producer-stage hash.

The historical field remains preserved as legacy evidence; rejection concerns future authority, not retroactive invalidation of the repository.

### Recursive fingerprint-field deletion rejected

Deleting every field named or resembling a fingerprint recursively is rejected because it would remove substantive provenance and dependency identity. Source evidence, input data, methods, registries, calculations, normalized series, external artifacts, and referenced-other-package fingerprints are part of what the package asserts and therefore must be hash-covered.

Recursive deletion would also make the boundary depend on field names and traversal rules, permit semantic identity to escape coverage by renaming or relocation, and create avoidable cross-language ambiguity.

### Fixed field projection rejected as the default

Hashing a fixed whitelist or projection of selected package fields is rejected as the default because newly added semantic fields would be unhashed until the projection contract changed. That creates an evolution trap and allows complete-package identity to drift from the package's actual semantic content.

A complete-package-minus-one-reserved-root rule covers future semantic additions automatically and requires fewer synchronized authorities.

### RFC 8785 selected

RFC 8785 is selected because it provides a documented, language-independent canonical JSON serialization target with deterministic object ordering and string/number serialization semantics. It supports independent verification better than repository-local `sort_keys` conventions.

Selection does not claim an RFC 8785 implementation currently exists in KnowledgeForge. Implementation and cross-language conformance remain gated.

### Floating-point numbers prohibited

JSON floating-point numbers are prohibited because binary floating-point parsing and rendering can differ across runtimes, can lose source precision, and complicate interoperable RFC 8785 behavior. KnowledgeForge already relies on exact deterministic numeric methods where representation is epistemically material.

Interoperable-range integers remain JSON numbers. Exact non-integer quantities are governed canonical decimal strings, allowing the owning method or evidence contract to preserve exact scale and representation without binary conversion.

### Structured descriptor selected

A structured descriptor is selected instead of a bare digest because the package must state the specification identity, canonicalization contract, digest algorithm, and value independently. The structure makes algorithm/version negotiation explicit and permits fail-closed verification without inferring semantics from a field name.

JSON object member order is insignificant. “Exact structure” in the normative specification means the exact required member set, member types, and required values. `<64-lowercase-hex>` is metavariable notation rather than literal text. The exact descriptor token is `RFC8785`; prose may refer to RFC 8785.

### Derivation and verification separated

Derivation cannot require a completed descriptor because the descriptor value is what derivation computes. The accepted producer sequence therefore supplies finalized hash-covered content with `/fingerprints` absent or empty, derives and returns the complete descriptor, and attaches it only after success. Verification is a separate operation over persisted bytes and requires the exact completed descriptor before independently repeating all checks and comparing the recomputed result.

Pending or placeholder descriptor values are prohibited from every serialized, persisted, admitted, projected, or exported representation.

### Deterministic contract bootstrap fixed; resolution profile deferred

The package-contract bootstrap is fixed at hash-covered RFC 6901 pointer `/governing_contracts/package_contract`. It binds `contract_id`, `contract_version`, and `media_type` to an exact-byte SHA-256 `content_digest`. Verifiers receive immutable contract artifacts explicitly; mutable or unpinned resolution is prohibited.

Exact RFC 6901 pointers are the only field-location form accepted by the architectural core. They are evaluated against the complete final parsed root with RFC 6901 escaping and strict array-index semantics. Missing or malformed targets fail closed. Pointer patterns are unsupported until a separate versioned profile defines a closed grammar, deterministic expansion order, and empty/non-unique expansion failure.

The remaining contract-artifact representation and multi-contract rule semantics are not evidenced sufficiently to decide here. The separately accepted profile must define supported media types/versions, the internal contract-document schema, applicable schemas/methods, field roles, governed decimals, fingerprint target relations, applicability, precedence, conflict detection, and an immutable identity that binds exactly one profile to this specification identifier. Until then, both derivation and verification fail closed.

### `/fingerprints` is the only excluded root and is closed in v1

The root `/fingerprints` object is the only excluded root because it is the narrow cycle-breaking container for `package_content_fingerprint`. In persisted v1 packages that is its only permitted member. Excluding additional roots would weaken semantic coverage. Excluding fingerprint-like fields recursively would erase substantive provenance.

The closed-member rule prevents this narrow exclusion from becoming an escape hatch: substantive source, input, method, registry, calculation, normalized-series, other-package, and external-artifact identity must remain inside hash-covered structures. A full-parsed-package fingerprint that includes `/fingerprints`, and an exact serialized-file fingerprint over bytes containing `/fingerprints`, must remain external. PostgreSQL projection and export fingerprints also remain external derived records. No stored descriptor may claim to hash a boundary containing its own value.

### Post-fingerprint admission results are external

Authoritative admission and verification results are external because inserting them into the package after fingerprinting would mutate hash-covered semantic content, while including a result about the final fingerprint before the fingerprint exists would create a cycle.

Internal validation state may therefore record only pre-fingerprint checks. A successful authoritative post-fingerprint record is keyed by both validated package ID and content fingerprint, preserving auditability without mutating canonical package bytes. Failure records produced before both values validate are separately governed and must not misrepresent claimed values as validated.

## Legacy treatment

All existing `fingerprints.package_manifest` values remain immutable legacy values. The new contract is not retroactive. Existing packages are not rewritten, normalized, repaired, or silently reclassified by this decision.

The following external classification vocabulary is accepted:

1. `legacy_manifest_recomputed_valid`
   - stored legacy outer manifest recomputes under its historical rule and no deprecated containing-package mirror is present;
2. `legacy_manifest_valid_with_deprecated_self_mirror`
   - outer legacy value recomputes, but the package contains a deprecated containing-package mirror;
3. `legacy_manifest_invalid_post_hash_mutation`
   - Campaign 35 defect class;
4. `legacy_manifest_invalid_self_reference_order`
   - Campaign 37 defect class;
5. `native_package_content_fingerprint_v1_valid`
   - reserved for future packages that pass separately implemented independent verification and admission.

No current package is classified as native v1-valid.

The five invalid legacy outer manifests measured in the 2026-07-15 560-package corpus remain preserved and require later lifecycle adjudication before successor creation. This corpus-scoped finding does not imply that future audits cannot discover additional defects. This decision does not determine whether successors are required, current, accepted, deprecated, or superseding.

The 35 containing-package mirror occurrences are deprecated and non-authoritative. The 33 stale mirrors do not by themselves require successors.

## Existing packages are not rewritten

Rewriting current package bytes would violate the canonical supersession immutability model, erase historical production evidence, alter repository and projection fingerprints, and conflate architectural acceptance with legacy remediation. If lifecycle adjudication later requires corrected current objects, immutable successors must be separately authorized and created under the then-applicable contract.

Any hash-covered mutation after finalization produces a different artifact for which the prior Package Content Fingerprint v1 value is invalid. It does not invalidate, alter, or diminish the preserved predecessor or the correctness of that predecessor's fingerprint for its original bytes and content. A separately persisted changed artifact must receive the identity/version required by package and lifecycle contracts. Where canonical overwrite prohibition applies, one package ID cannot identify different canonical bytes. Successor and supersession treatment remains separately governed. This wording does not retroactively make the five measured legacy defects valid.

This decision is not a fix to existing packages.

## PostgreSQL remains unchanged

PostgreSQL remains a derived operational projection of canonical repository packages. It neither originates nor mutates canonical knowledge and does not become authoritative because it can query or faithfully retain a payload.

No PostgreSQL schema, table, row, view, materialized view, function, grant, loader, projection, or verification record is changed by this decision. Future projection of v1 descriptors or external verification state requires separate authorization.

## Relationship Export Contract v1 remains unchanged

Relationship Export Contract v1 remains unchanged because this decision defines future package semantic identity, not relationship query or export semantics. Current export query fingerprints, result fingerprints, payload fidelity checks, and independent consumer simulation are unchanged by this decision and remain governed exclusively by their existing contract.

No export is regenerated and no export field is added. Any future export exposure of v1 identity requires a separately versioned compatibility decision.

## Promotion-policy reconciliation deferred

Current candidate-to-object promotion and validation machinery includes producer-specific validation histories and fingerprint-verification assertions. Reconciliation is deferred because this decision does not authorize code, schema, validator, lifecycle, or production-flow changes.

For future native packages, this decision classifies completed pre-fingerprint validation results and pre-finalization lineage/evolution assertions as hash-covered content; authoritative post-fingerprint verification/admission results as external; and package-local claims of completed independent fingerprint verification/admission as prohibited. The following remain explicitly deferred pending promotion-policy reconciliation: `status`, governance/review state, lifecycle state, promotion metadata, and evidence-integrity assertions whose timing or authority is not already unambiguous.

A later implementation task must determine the exact treatment of those deferred fields and preserve candidate-to-object and lifecycle semantics. It may not infer a promotion-policy answer from this fingerprint decision alone. Later lineage or evolution events must not mutate a preserved predecessor; they require an external record or a separately governed immutable successor.

## Distinct gates

This record distinguishes four gates:

1. **Architectural acceptance — OPEN/COMPLETE.**
   - The field, descriptor, formula, strict JSON profile, separate derivation/verification operations, fixed contract-reference bootstrap, closed `/fingerprints` rule, cycle-breaking rule, legacy posture, and external-verification boundary are accepted. The contract-resolution profile required for independent conformance is explicitly not yet accepted.
2. **Operational implementation — CLOSED.**
   - No RFC 8785 implementation, parser, producer, validator, schema, projection, export, consumer, or conformance suite is authorized by this record.
3. **Legacy remediation — CLOSED.**
   - No package rewrite, successor, lifecycle adjudication, migration, reclassification, repository rebuild, or PostgreSQL change is authorized.
4. **Publication — CLOSED.**
   - No implementation, package, schema, projection, export, migration, successor, lifecycle, or production-activation artifact may be staged, committed, pushed, published, or described as production-active under v1 without separate authorization. This gate does not prohibit review and later publication of this decision record and its normative documentation through the normal human-authorized documentation workflow.

## Exact implementation gate that remains closed

No production package may populate `fingerprints.package_content_fingerprint` until a separately authorized implementation task has, at minimum:

1. separately accepted the versioned contract-resolution profile, including its immutable identity and unique binding to this specification identifier, supported media type/version, immutable contract-document schema, rule vocabulary, exact-pointer semantics, applicability, precedence, and conflict handling;
2. implemented strict duplicate-key-aware JSON parsing and the numeric/Unicode restrictions;
3. implemented and independently verified RFC 8785 canonicalization;
4. implemented the exact bootstrap, contract digest binding, package-ID binding, exact-decimal validation, fingerprint-field semantic roles, target relations, containing-package self-reference enforcement, and closed `/fingerprints` member rule;
5. implemented separate derivation and verification operations without placeholders, descriptor precondition cycles, post-hash mutation, or internal physical-fingerprint self-reference;
6. implemented independent verification, successful external results keyed by validated package ID plus content fingerprint, and separately governed failure records that do not misrepresent unvalidated claims;
7. published and passed the required positive, negative, boundary, mutation, resolver, pointer, and cross-language conformance vectors;
8. reconciled producer, candidate admission, promotion, repository insertion, PostgreSQL projection, export, and consumer verification responsibilities;
9. defined legacy compatibility behavior without rewriting current packages;
10. completed explicit lifecycle adjudication for the five invalid legacy outer manifests measured in the 2026-07-15 corpus before any successor creation;
11. received separate authorization for production package generation and publication.

Until all applicable gates are accepted, implementations MUST fail closed and v1 remains documentation-only.

## Evidence basis

Primary repository evidence:

- `CONSTITUTION.md`
- `docs/knowledge_package_contract.md`
- `docs/provenance_fingerprinting.md`
- `docs/knowledge_repository_architecture.md`
- `docs/knowledge_repository_persistence_specification.md`
- `docs/postgresql_operational_repository.md`
- `artifacts/decisions/D-20260710-bounded-postgresql-knowledge-repository-realization.md`
- `artifacts/decisions/D-20260711-relationship-export-contract-v1.md`
- `artifacts/decisions/D-20260711-canonical-supersession-immutability-model.md`
- `tools/construct_knowledge_package_v1.py`
- `tools/knowledge_repository.py`
- `tools/postgresql_operational_projection.py`
- `tools/relationship_export_v1.py`
- `tools/run_campaign35_wdi_nordic_exports_statistical_summary.py`
- `tools/run_campaign37_swe_nor_exports_imports_correlation.py`
- all 560 JSON packages under `knowledge_repository/objects/`, inspected by read-only corpus recomputation

Measured read-only findings formalized here:

- canonical package files scanned: 560;
- invalid historical outer manifests: 5;
- Campaign 35 invalid-post-hash-mutation packages: 3;
- Campaign 37 invalid-self-reference-order packages: 2;
- deprecated containing-package mirror occurrences: 35;
- stale containing-package mirrors: 33;
- current packages classified as native v1-valid: 0.

## Consequences and non-authorizations

This decision improves future semantic identity by making the byte/value boundary explicit, non-circular, and versioned. It is designed for independent verification after the separately required contract-resolution profile and implementation gates are completed. It preserves source and dependency fingerprints as substantive content and prevents use of excluded root metadata as an identity escape hatch.

It does not authorize code, tests, schemas, migrations, package changes, repository-index changes, PostgreSQL changes, export changes, production calculations, successor creation, lifecycle changes, promotion-policy reconciliation, or publication of implementation or production artifacts. Publication of these two documentation artifacts remains subject to the normal separate human-authorized Git workflow.
