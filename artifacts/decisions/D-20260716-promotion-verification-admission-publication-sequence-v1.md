# D-20260716 — Promotion–Verification–Admission–Publication Sequence v1

Date: 2026-07-16
Status: Accepted sequencing architecture; not implemented; not production-authorized; dependent contracts pending
Decision class: future native package authority sequencing and publication boundary
Normative specification: `docs/promotion_verification_admission_publication_sequence_v1.md`
Related specification: `docs/package_content_fingerprint_v1.md`

## Decision

KnowledgeForge accepts `knowledgeforge_promotion_verification_admission_publication_sequence_v1@1.0` as the future authority and event sequence for native Package Content Fingerprint v1 packages.

The accepted order is:

1. candidate identification;
2. deterministic candidate validation;
3. final-package construction authorization through existing KnowledgeForge governance and decision machinery;
4. construction of complete final semantic package content;
5. Package Content Fingerprint v1 derivation and descriptor attachment;
6. production of the exact final repository serialization and freezing of those bytes in non-canonical staging;
7. independent verification of the exact final staged artifact;
8. unconditional admission authorization for the exact verified package ID, Package Content Fingerprint v1, and serialized-artifact digest tuple;
9. logically atomic append-only canonical repository transition;
10. read-back verification and deterministic repository reconciliation;
11. Git publication in an immutable commit and verification of the actual resulting commit tree;
12. derived PostgreSQL projection from Git-published canonical state;
13. derived export generation or materialization;
14. independent export verification;
15. later separately governed lifecycle events, when applicable.

Final-package construction authorization permits construction but binds no not-yet-existing fingerprint. Successful verification establishes technical fingerprint validity for exact final bytes. Admission independently authorizes one exact verified artifact for insertion. The logically atomic canonical transition changes local canonical repository state. Git publication gives the publication event an immutable identity; a local commit is not by itself proof of off-host durability. PostgreSQL, export generation, and export verification remain distinct derived consequences.

This decision is architecturally accepted. It does not implement or production-authorize any part of the sequence.

## Ambiguity that triggered this decision

`docs/package_content_fingerprint_v1.md` correctly separated derivation from independent verification and required authoritative post-fingerprint verification and admission results to remain external. Its construction wording nevertheless left the temporal meaning of “persist” and “admission path” open to incompatible interpretations:

- verification requires final persisted descriptor-bearing bytes;
- canonical admission must not occur before final verification;
- post-fingerprint authority cannot be embedded in the package without mutation or an attestation cycle;
- historical campaign language sometimes used promotion, acceptance, persistence, publication, and projection as partially overlapping terms.

Repository history also contains different production sequences:

- coupled candidate-to-object promotion with populated package-local validation history;
- statistical packages with promotion assertions but empty promotion history;
- relationship packages produced under campaign decisions without package-local promotion;
- Campaign 43’s stronger separation of calculation acceptance, package preflight, local canonical publication, PostgreSQL verification, export verification, and Git publication.

Those historical flows remain valid evidence under their original contracts, but they do not provide one unambiguous future native-v1 sequence.

This decision resolves the ambiguity by distinguishing non-canonical staging from canonical insertion and by assigning each later event its own authority and proof boundary.

This decision also records a bounded clarification and amendment of the older orchestration language accepted by `artifacts/decisions/D-20260715-package-content-fingerprint-v1.md`. `docs/package_content_fingerprint_v1.md` remains authoritative for fingerprint calculation, parsing, canonicalization, package binding, contract resolution, and technical verification. The sequence specification governs event ordering and authority boundaries. Where older orchestration language conflicts, the corrected sequence controls. No fingerprint algorithm version, field, descriptor, derivation boundary, technical rule, or legacy measurement changes.

## Why final-package construction authorization is distinct

Final-package construction authorization is candidate-bound and follows candidate identification and validation. It binds an immutable candidate identity, candidate evidence, declared scope, applicable candidate contracts, and authorization identity before complete final package content and its content fingerprint exist. It authorizes construction of a proposed final package but cannot bind unknown final bytes or a not-yet-existing fingerprint.

It therefore does not prove or authorize final package validity, technical fingerprint validity, exact serialized-artifact identity, verification, admission, insertion, Git publication, projection, export generation, or export verification.

This event is not historical KnowledgeForge `promotion` or the current candidate-to-`KnowledgeObjectPackage` promotion convention. Existing package-local `promotion` fields, acceptance criteria, construction behavior, and historical decisions remain immutable historical evidence and are not retroactively redefined. Final native-v1 canonical acceptance depends on verification, admission, insertion, and publication rather than a historical package-local promotion block alone.

Existing file-backed decision machinery is suitable to carry future construction authority in principle, so no new registry or service is justified. The standardized final-package construction-authorization contract remains a closed implementation prerequisite; existing machinery is not claimed to supply that complete contract today.

## Why final verification is distinct and external

Independent final verification must inspect the exact complete descriptor-bearing artifact. It cannot occur before Package Content Fingerprint v1 derivation and descriptor attachment.

A successful final verification claim cannot be inserted into the package after derivation because doing so would mutate hash-covered content or create an attestation cycle. It therefore remains external and binds:

- validated package ID;
- Package Content Fingerprint v1;
- exact serialized-artifact digest;
- governing contracts and contract-resolution profile;
- verifier identity, implementation, checks, result, and attestation identity.

Verification establishes whether exact bytes satisfy the governing contracts. It is evidentiary, not admission authority. The verifier MUST NOT authorize admission merely by reporting success.

Successful independent verification establishes `native_package_content_fingerprint_v1_valid` for that exact frozen descriptor-bearing artifact and complete applicable immutable governing-contract set. Technical validity remains distinct from admission, insertion, Git publication, projection, export generation, export verification, and later lifecycle status. A fingerprint-valid artifact may still be denied or deferred admission; denial or deferral does not make its correctly computed fingerprint technically invalid.

Producer self-checking is insufficient because it does not provide an independent authority boundary over persisted final bytes.

## Why admission is distinct

Admission evaluates a successfully verified artifact in its final-package construction-authorization, constitutional, package-kind, governing-contract, collision, and no-overwrite context. It binds one exact tuple:

```text
package_id
+ Package Content Fingerprint v1
+ serialized-artifact digest
```

Admission outcomes are `authorized`, `denied`, and `deferred`. Only unconditional `authorized`, with no outstanding conditions, is insertion-ready. A condition must be satisfied before a final `authorized` attestation is issued. A fingerprint-invalid or incompletely verified artifact cannot receive successful authorization.

Admission occurs before canonical insertion. Successful verification does not compel admission, and admission status does not determine technical fingerprint validity. Immediately before insertion, changed, unavailable, superseded, withdrawn, expired, non-resolving, or artifact-inconsistent authority or evidence requires fail-closed renewal of verification or admission as applicable.

Admission permits an insertion attempt for the exact artifact but does not claim that insertion, reconciliation, Git publication, projection, export generation, or export verification later succeeds.

## Accepted combined external record

KnowledgeForge accepts one future external record class, provisionally named:

`FinalPackageVerificationAndAdmissionAuthorizationRecord`

One physical record is accepted because both attestations bind the same exact artifact and governing-contract set. No new service or registry is required. The record remains external to the fingerprinted package and contains two semantically, logically, and authoritatively identifiable attestations:

1. independent verification attestation;
2. admission authorization attestation.

Their identities, authorities, inputs, outcomes, completion times, and content digests remain independently distinguishable. The successful record is finalized only after verification completes and the admission authority issues an unconditional `authorized` outcome. Denied, deferred, failed, and incomplete attempts remain separate decision or failure evidence and are not successful authorization records.

The successful record exists before canonical insertion and must not contain or predict insertion success, reconciliation success, Git commit identity, publication success, PostgreSQL success, export-generation success, or export-verification success.

## Minimum future record content and role rules

The shared immutable binding includes:

- record kind and version;
- a content-bound record identity or an identity with immutable deterministic resolution;
- package ID and complete Package Content Fingerprint v1 descriptor/value;
- serialized-artifact digest;
- final-package construction-authorization identity;
- complete applicable immutable governing-contract set;
- fingerprint specification and accepted contract-resolution-profile identity;
- admission-policy identity/version;
- record status.

The independent verification attestation includes verifier identity, verifier authority/role identity, verification implementation identity/version, outcome, completion time, attestation identity/content digest, shared artifact and contract binding, exact checks, and failure reason where unsuccessful.

The admission attestation includes admission-authority identity, admission role/authority identity, admission-policy identity/version, outcome, authorization time, attestation identity/content digest, explicit reference to the completed successful verification attestation, the same artifact and contract binding, and denial/deferral reasons where applicable.

Immutable ordering evidence must prove verification completed before admission authorization. Separate timestamps are mandatory unless a later accepted contract supplies an equally deterministic immutable ordering mechanism. Record and attestation identities must be content-bound or immutably and deterministically resolvable; opaque mutable identifiers alone are insufficient.

For one artifact, the producer/finalizer may not be its independent verifier; the verifier may not issue its admission authorization; the admission authority may not alter, replace, manufacture, or suppress verifier-owned evidence; verification success does not compel admission; and admission may not convert failed or incomplete verification into success. Different services, organizations, or cryptographic signatures are not required and remain implementation choices.

## Authority-record placement remains closed

This decision does not select an authority-record path. Operational admission remains blocked until a future record/repository contract settles path and naming, canonicality class, collision/no-overwrite behavior, content identity, repository-fingerprint/manifest/index participation, deterministic discovery, reconciliation, retention, failed-publication treatment, and recovery.

The final successful record must be included in the same logically atomic canonical transition and later Git publication boundary as governed by that future contract. No package may be admitted operationally before this dependency is closed.

## Non-canonical staging and exact-byte continuity decision

After descriptor attachment, the exact final repository serialization must be produced and frozen in non-canonical staging. Staging is pre-admission persistence outside the canonical repository; it is not canonical membership, publication, or an admission result.

The serialized-artifact digest identifies those exact bytes. Verification operates on them, admission binds them, and canonical insertion installs them unchanged. Insertion may not parse and reserialize, normalize, change whitespace, escaping, member order, a newline, or any other byte. Any byte change requires a new staged artifact, exact digest, independent verification, and admission decision even when semantic Package Content Fingerprint v1 remains equal.

Staged-artifact retention and failure-evidence handling remain closed contracts. The current repository writer does not satisfy the future exact-byte or logical-atomicity boundary and remains unchanged.

## Logically atomic canonical transition and reconciliation decision

Only unconditional `authorized` admission may enter the insertion gate. The complete transition includes, as applicable, exact admitted package bytes, the finalized authority record, evolution metadata, deterministic indexes, deterministic manifest state, and expected repository fingerprint or equivalent reconciliation identity.

Logical atomicity means readers and downstream processes observe either the complete previous canonical state or the complete next canonical state. A visible package object alone is not canonical membership. One explicit repository transition boundary or commit marker controls canonical visibility.

Staging plus atomic replacement and manifest-last transactional visibility are permissible future options, but no mechanism is selected. Arbitrary sequential writes followed by best-effort rollback are not atomic. Partial files remain non-canonical residue; readers cannot consume them, and a separate recovery procedure must quarantine, recover, or remove them.

Collision, overwrite, same-ID/different-content, unexpected pre-existence, stale-authority, and identity/digest mismatch fail closed. Read-back and reconciliation must cover package bytes, authority record, evolution, indexes, manifest, repository identity, predecessor immutability, and unauthorized paths before the next state becomes canonical.

The transaction mechanism, reader gate, recovery protocol, authority-record placement, and reconciliation implementation remain closed implementation dependencies.

## Git publication and commit-tree proof

Git publication remains distinct from canonical insertion. Publication proof is the immutable commit and independently verified actual commit tree; pre-commit working-tree inspection alone is insufficient.

The publication verifier must establish the expected parent, exact allowlisted paths, exact admitted package bytes, exact finalized authority record, expected repository-transition metadata and manifest/repository identity, no unauthorized paths, and no missing required paths.

The commit ID is the publication-event identity and cannot be predicted or embedded in the pre-insertion authority record. No duplicate publication-receipt record is accepted.

Remote push is distribution, not admission or Git publication. Off-host and machine-loss durability remain separate. A local-only commit is not proof of off-host durability.

## PostgreSQL projection and export ordering

PostgreSQL remains a derived operational projection and cannot own admission or canonical authority. For a conforming future-native production flow, successful Git publication and commit-tree verification precede PostgreSQL projection; projection precedes export generation/materialization; independent export verification follows generation.

A separately authorized prepublication test projection must be labelled non-authoritative, non-production, preview-only, and nonconforming with the completed native-v1 production sequence. It cannot establish admission, insertion, publication, consumer export publication, or retroactive proof of any earlier stage.

PostgreSQL schema, data, loader, and authority remain unchanged. Projection failure cannot rewrite canonical packages.

Exports remain versioned derived consumer representations. Export generation and independent export verification are distinct events. Relationship Export Contract v1 remains unchanged, and native-v1 identity exposure still requires separate compatibility authorization. A preview projection cannot be used for consumer export publication.

## Failure-evidence decision

Failed verification, denied/deferred admission, repository-transition failure, reconciliation failure, and Git-publication failure must produce or preserve evidence sufficient for diagnosis and governance. Unvalidated package IDs or fingerprints remain labelled claimed identities, not validated keys. Failed staged artifacts do not become Knowledge Objects, and failure evidence is not proof of canonical admission.

The successful combined authority record, failed-verification evidence, denied/deferred-admission evidence, repository-transition failure evidence, and publication-failure evidence are distinct classes and need not use one schema. Their storage location, retention period, immutable identity, and recovery handling remain a closed failure-evidence contract dependency. No storage service or database design is selected.

Failures before successful canonical insertion create no new canonical knowledge. Partial repository files remain non-canonical residue. Projection, export, distribution, and publication failure cannot rewrite canonical content. Operational failure is not automatically substantive negative knowledge and becomes reusable negative knowledge only through a separate applicable package and admission path.

Changed bytes require a new staged-artifact digest, verification, and admission decision. Later contradiction, weakening, withdrawal, currentness, and supersession remain separately governed and do not mutate predecessors.

## Lifecycle and status boundary

For future native-v1 packages, claims whose truth arises only after technical fingerprint verification, admission, insertion, Git publication, projection, export generation, or export verification remain external to immutable package content.

Future packages must not contain package-local claims that any of those later events has already succeeded.

This decision does not settle the complete lifecycle model. The successor native-v1 package contract must resolve package-local:

- maturity;
- governance review state;
- truth state;
- confidence;
- lifecycle and currentness;
- evidence-integrity assertions whose timing remains ambiguous.

Later contradiction, weakening, withdrawal, currentness, and supersession must not mutate preserved predecessors.

## Legacy treatment

The measured 2026-07-15 corpus remains:

- 521 packages with populated promotion history;
- four statistical packages with empty promotion history;
- 35 relationship packages without package-local promotion;
- five invalid legacy manifests;
- 35 containing-package mirrors;
- 33 stale containing-package mirrors;
- zero native Package Content Fingerprint v1 packages.

All existing bytes remain preserved. This decision does not:

- backfill promotion histories;
- create retroactive verification/admission records;
- reinterpret Git publication as native-v1 admission;
- rewrite invalid manifests;
- require successors merely for representational uniformity;
- operationally reclassify any current package as native-v1-valid.

Legacy compatibility remains descriptive and external. Historical package, campaign, and publication evidence remains governed by its original contracts.

The five anomalous packages may remain historically accepted under original governance while not being technically valid under the future native-v1 fingerprint contract. Historical acceptance and native-v1 technical validity are separate classifications. Stale containing-package mirrors remain non-authoritative.

## Explicitly rejected alternatives

### Embedded post-fingerprint verification

Rejected because inserting successful final verification or admission claims into the package after derivation would mutate hash-covered content or create an attestation cycle.

### Final-package construction authorization as admission

Rejected because final-package construction authorization is candidate-bound and occurs before exact final content, fingerprint, and bytes exist.

### Canonical insertion before verification

Rejected because canonical knowledge must not be created from an independently unverified final artifact. Final-form bytes needed for verification belong in non-canonical staging.

### Verification as automatic admission

Rejected because independent technical verification and governance admission have different authorities and outcomes. Admission denial must remain possible after verification success.

### PostgreSQL admission authority

Rejected because PostgreSQL is derived, rebuildable operational state and cannot become a competing source of canonical authority.

### Campaign prose alone as exact final-byte verification

Rejected because a campaign decision or report can document governance and production evidence but does not independently verify the exact descriptor-bearing serialized artifact under the governing contracts.

### Separate new construction-authorization, verification, admission, insertion, and publication registries or services

Rejected because existing file-backed governance can carry future construction authority in principle, while one combined external verification/admission record, deterministic repository materialization, and Git history provide the selected authority boundaries with less coordination and no competing canonical system. Standardized contracts remain prerequisites.

### Retroactive uniformity

Rejected because rewriting or backfilling legacy packages would erase production history, alter canonical bytes and fingerprints, and falsely claim historical conformance to a future architecture.

## Consequences

Future native-v1 production has an explicit non-circular sequence and a testable authority boundary for every stage.

The selected architecture:

- reuses existing decision machinery;
- adds only one future record class;
- keeps final verification and admission external;
- preserves role separation inside one physical record;
- keeps canonical package authority file-backed;
- uses Git as publication proof;
- leaves PostgreSQL and exports derived;
- preserves all legacy bytes and classifications;
- prevents local insertion from being mislabeled Git publication or off-host durability.

Implementation must fail closed until all required contracts and gates exist.

## Unresolved questions and closed gates

The following remain closed implementation or production dependencies:

1. accepted immutable Package Content Fingerprint v1 contract-resolution profile and binding;
2. standardized final-package construction-authorization contract;
3. final authority-record serialization, media type, content-bound identity, complete governing-contract binding, attestation identities, timestamps, and ordering mechanism;
4. authority-record path, canonicality class, collision behavior, repository-fingerprint/manifest/index participation, discovery, reconciliation, retention, failed-publication treatment, and recovery;
5. failure-evidence identity, storage, retention, and recovery;
6. verifier and admission-authority assignment that satisfies the accepted minimum role rules;
7. exact serialized-artifact digest descriptor contract;
8. exact-byte staging and insertion implementation;
9. logical repository transaction mechanism, reader gate, quarantine/recovery protocol, and reconciliation implementation;
10. Git publication allowlisting and actual commit-tree verification;
11. successor native-v1 package treatment of maturity, governance, truth, confidence, lifecycle/currentness, and ambiguous evidence-integrity fields;
12. any future PostgreSQL or export exposure of native-v1 identities and external authority status;
13. lifecycle adjudication of the five invalid legacy manifests before successor creation;
14. separate implementation, production-package-generation, and publication authorization.

Cryptographic signing and separate organizations or services remain optional implementation choices, not accepted prerequisites.

Operational implementation, production activation, legacy remediation, package mutation, PostgreSQL change, export change, and Git publication remain closed.

## Non-authorizations

This decision does not authorize:

- code or test changes;
- executable schemas;
- record instances;
- staging implementation;
- atomic insertion implementation;
- Package Content Fingerprint v1 implementation;
- package generation or mutation;
- repository manifest/index/evolution mutation;
- PostgreSQL mutation;
- export mutation;
- legacy repair or successor creation;
- task, state, handoff, report, or summary changes;
- staging, commit, fetch, pull, push, or publication.

## Evidence basis

Primary repository evidence:

- `CONSTITUTION.md`
- `docs/knowledge_package_contract.md`
- `docs/knowledge_acceptance_criteria.md`
- `docs/provenance_fingerprinting.md`
- `docs/knowledge_repository_architecture.md`
- `docs/knowledge_repository_persistence_specification.md`
- `docs/package_content_fingerprint_v1.md`
- `artifacts/decisions/D-20260715-package-content-fingerprint-v1.md`
- `artifacts/decisions/D-20260712-durability-destination-policy-and-pre-staging-remediation.md`
- `artifacts/decisions/D-20260712-campaign41-candidate-registry-freeze.md`
- `artifacts/decisions/D-20260712-campaign43-first-difference-companion-calculation-accepted.md`
- `artifacts/decisions/D-20260712-campaign43-companion-package-publication-preflight-accepted.md`
- `artifacts/decisions/D-20260712-campaign43-canonical-publication-accepted.md`
- `tools/construct_knowledge_package_v1.py`
- `tools/run_campaign35_wdi_nordic_exports_statistical_summary.py`
- `tools/correlation_batch_engine.py`
- `tools/knowledge_repository.py`
- `tools/postgresql_operational_projection.py`
- `tools/relationship_export_v1.py`
- the measured 560-package legacy corpus summarized in the Package Content Fingerprint v1 acceptance decision.

Campaign 43 evidence establishes the bounded local operations stated in its own decisions, including local canonical publication, PostgreSQL verification, and export verification. Because `artifacts/decisions/D-20260712-campaign43-canonical-publication-accepted.md` says Git push remained pending, it is not used alone as proof of the future Git-publication boundary. The durability decision supports the distinction among local commit identity, distribution, and off-host durability.

The normative authority for this decision is `docs/promotion_verification_admission_publication_sequence_v1.md`. If summary prose here conflicts with that specification, the normative specification controls until a separately accepted successor decision says otherwise.
