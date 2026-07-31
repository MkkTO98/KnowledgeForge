# Evidence Portfolio Production Boundary Contract v1

Status: Accepted and implementation-authorized for the first unpublished Evidence Portfolio pilot
Contract identity: `knowledgeforge.evidence_portfolio.production_boundary.v1@1.0`
Date: 2026-07-31

## Purpose and boundaries

This bounded operating-procedure contract closes pre-publication authorization and audit-attestation defects found in the first Evidence Portfolio pilot. It does not alter the canonical `KnowledgeObjectPackage`, Evidence Bundle, Calculation Campaign, Evidence-Card-equivalent view, repository fingerprint, PostgreSQL projection, production doctrine, Campaign 43 analytical identity, or KnowledgeForge's independence from MacroForge.

The boundary contains two coordinated but semantically distinct subcontracts:

1. Production Authorization Contract v1 controls whether one exact canary result authorizes one content-identical bounded production invocation.
2. Architecture-to-Reality Candidate Attestation Contract v1 records what substantive candidate was audited without recursively hashing the audit output.

Authorization is not audit attestation. Audit attestation is not production authorization. Neither is Git publication authority.

## 1. Production Authorization Contract v1

Schema identity: `knowledgeforge.evidence_portfolio.production_authorization.v1`
Schema version: `1.0`

A successful authorization is a JSON object containing:

- `schema_name` and `schema_version`;
- `campaign_id` and `manifest_id`;
- `execution_manifest_byte_fingerprint`, the SHA-256 of the exact manifest file bytes supplied to the CLI invocation, or of the explicitly supplied deterministic in-memory serialization for a programmatic invocation;
- `manifest_fingerprint`, independently verified under the manifest's existing self-field exclusion;
- `candidate_population`, in manifest order, containing candidate ID, disposition, canary flag and the available input path, file SHA-256 and normalized fingerprint;
- `candidate_population_fingerprint`, computed from that ordered population;
- `production_limits`, containing the complete portfolio budget and the ordered per-entry budgets;
- `execution_mode`, which is exactly `canary`;
- `passed`, which is exactly the JSON Boolean `true`;
- `blockers`, which is exactly empty;
- complete canary `accounting`;
- deterministic `reruns`, whose executable canary entries use an exact row schema, contain two syntactically valid SHA-256 result fingerprints and report exact match;
- `publication`, recording the isolated canary admission disposition, the count admitted by this invocation, the resulting total repository object count and repository fingerprint; these two repository-state values authorize only a production target in that exact canary-admitted pre-state;
- `gate_fingerprint`.

The gate fingerprint is `sha256:` plus SHA-256 over UTF-8 canonical JSON (`sort_keys=true`, separators `,` and `:`, no ASCII coercion) of the complete gate object after removing only `gate_fingerprint`. The consumer recomputes it independently.

Before any production evidence read, calculation, package construction, promotion or canonical write, the consumer validates the top-level object, exact schema/version, literal Boolean success, empty blockers, canary mode, fingerprint, campaign, manifest ID, exact manifest-byte fingerprint, semantic manifest fingerprint, ordered candidate/input population, complete limits, expected canary accounting, exact successful-rerun rows and the production repository's exact object count and fingerprint against the canary-admitted state. Reading the target repository manifest for this precondition is part of authorization validation, not production calculation.

The production path holds an exclusive advisory lock on a stable operational lock file adjacent to the canonical repository from pre-state validation through persistence. The lock is outside canonical repository identity and compliant portfolio writers share it. The consumer also revalidates exact repository state immediately before persistence, so an uncooperative intervening mutation blocks canonical writes rather than being absorbed.

A malformed, incomplete, false, non-Boolean, tampered, differently bound, repository-state-mismatched, stale-content or legacy weak gate fails through a controlled validation error. Content-bound reuse is permitted only for the byte-identical campaign, manifest, candidate/input population, limits and canary-admitted repository pre-state. No wall-clock expiry, signature, remote authority or secret is introduced.

The historical weak `canary_gate.json` remains immutable historical execution evidence. It is not retroactively represented as v1 authorization and is never grandfathered.

## 2. Normative limit semantics

The fingerprinted pilot manifest limits remain normative:

- `maximum_executed_candidates = 2`: count selected executable candidates before calculation; excess fails before calculation.
- `maximum_promoted_objects = 2`: count proposed packages before canonical persistence; excess fails before canonical writes.
- `maximum_raw_result_records = 56`: compare aggregate produced records after calculation and before admission/persistence/promotion; excess output is not admitted or persisted.
- entry `maximum_result_records = 28`: compare each candidate's raw and valid result counts before package construction/admission/promotion. The existing exact-28 domain invariant remains a separate stronger rule.
- entry `maximum_wall_seconds = 5`: measure each candidate rerun calculation interval with a monotonic clock. Excess blocks package construction, admission, promotion and persistence; this contract does not claim calculation cancellation.
- `stop_on_canary_failure = true`: the configured value itself must be the literal Boolean `true`, and production requires a fully valid v1 gate.

Diagnostics may be written to an explicitly non-canonical output directory after failure. Persistent/default PostgreSQL and canonical repository mutation remain forbidden on every failed gate.

## 3. Manifest-path containment

Every manifest-controlled evidence path must be repository-relative. Before bytes are read or hashed, the consumer:

1. rejects absolute paths;
2. resolves the permitted repository root canonically;
3. resolves the candidate canonically;
4. proves component-aware containment with `Path.relative_to()`;
5. rejects parent or normalized escape and symlink escape;
6. requires an existing regular file;
7. reports missing, directory and unsupported-file failures as controlled validation errors.

String-prefix containment is forbidden. No external bytes may reach the read/hash boundary.

## 4. Architecture-to-Reality Candidate Attestation Contract v1

Schema identity: `knowledgeforge.architecture_reality.audit_subject_manifest.v1`
Schema version: `1.0`

An Audit Subject Manifest freezes the substantive candidate before audit generation. It contains parent HEAD, relevant canonical repository fingerprint, exact sorted repository-relative subject paths, Git-compatible modes and SHA-256 byte hashes, exact exclusions, subject path count and a deterministic subject-manifest fingerprint. Its fingerprint removes only its own fingerprint field before canonical serialization.

The subject identity is workspace-independent. The manifest is validation evidence external to the publication candidate; the final publication manifest includes every path enumerated by it, not the subject-manifest file itself. This avoids a self-hash cycle while retaining complete verification evidence.

The only subject exclusions are:

- the architecture-audit output, because its bytes depend on running the audit;
- `artifacts/reports/_SUMMARY.md`, because its generated inventory must list the resulting audit.

No other candidate path may be silently excluded.

The audit report durably records parent HEAD, subject-manifest fingerprint, subject path count, exact exclusions, repository fingerprint, audit-tool byte fingerprint, result and optional informational workspace location. It describes itself as attesting the frozen audit subject; it does not claim to hash itself, predict a commit or recursively attest the final candidate.

Predecessor discovery excludes the current output destination and selects the lexically latest genuinely preceding audit deterministically.

## 5. Acyclic generation and publication-preflight sequence

1. Freeze substantive authorized candidate blobs.
2. Build and verify the external Audit Subject Manifest, excluding only audit output and reports summary.
3. Run the architecture audit against that subject and write the audit report.
4. Regenerate `artifacts/reports/_SUMMARY.md` so it lists the audit.
5. Freeze all candidate blobs.
6. Build the external prospective publication manifest containing every subject path, the exact audit report, exact regenerated summary and all other authorized candidate paths.
7. Verify that the audit binds the subject manifest, every subject mode/hash still matches, the summary lists the audit, and the final path/mode/hash set is exact.
8. Publication remains separately prohibited until an explicit publication-only task.

## 6. Current unpublished pilot compatibility

The same pilot may be replayed under v1 only by reconstructing the exact 560-package pre-pilot repository in disposable storage, running the same campaign/manifest/candidates/inputs/limits through a fresh v1 canary, and then running the same bounded wave under that gate. It must reproduce the retained two packages, 56 records, identities, values, precision and final 562-package repository fingerprint exactly wherever existing contracts require equality.

This replay is validation of the same unpublished pilot, not a second portfolio, new campaign, new evidence population, new knowledge claim or retroactive authorization. Historical calculation and weak-gate artifacts remain byte-identical. A distinct v1 authorization artifact and replay evidence may be retained for prospective publication proof.

## 7. Unchanged architecture

Unchanged:

- canonical Knowledge Object and package schemas;
- Evidence Bundle and Calculation Campaign meanings;
- operational-view status;
- production doctrine and ontology;
- Campaign 43 historical and analytical fingerprints;
- canonical repository fingerprint algorithm;
- PostgreSQL projection schema;
- provider and cross-project boundaries.

This contract is a bounded operating-procedure correction only.
