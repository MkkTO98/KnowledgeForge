# Provider-Neutral Release Inbox, Seen-Release Registry, and Real-Evidence Impact Pilot v1

## Decision

A. Real-evidence release ingestion and incremental impact processing validated.

Next task: Ask MacroForge, in a separate project-owned task, to implement the neutral evidence-release exporter.

## Previous prototype classification

Accepted classification: B. Existing architecture supports release-driven automation, but operational components are missing.

- synthetic release/change detection: proven
- real provider release ingestion before this task: not proven
- real existing-derivation impact mapping before this task: not proven
- canonical supersession: not implemented
- incremental PostgreSQL updating: not implemented
- automatic scheduling: not implemented
- MacroForge-compatible producer output: not implemented
- local-AI contribution: zero

The overall release-driven loop is not described as fully operational. This slice validates the KnowledgeForge-side manual inbox/registry/no-promote impact path against retained WDI evidence fixtures and existing derivations.

## Inbox implementation

Implementation: `tools/release_inbox_v1.py`.

Operational state root: `artifacts/release-inbox-v1/`.

Subpaths:

- inbox: `artifacts/release-inbox-v1/inbox/`
- accepted releases: `artifacts/release-inbox-v1/accepted-releases/`
- quarantine: `artifacts/release-inbox-v1/quarantined-releases/`
- processing evidence: `artifacts/release-inbox-v1/processing-evidence/`
- seen-release registry: `artifacts/release-inbox-v1/seen-release-registry.jsonl`

CLI supports init, scan-inbox, inspect-release, validate-release, process-one, process-all, verify-registry, fixture generation, derivation-registry writing, conformance package generation/verification, and recovery inventory.

## Registry model and durability

Registry is append-only JSONL. Operational timestamps are recorded but excluded from deterministic release identities/fingerprints.

Canonical operational records:

- `seen-release-registry.jsonl`
- `accepted-releases/*.json`
- `quarantined-releases/*.json`
- `processing-evidence/*/processing_result.json`
- `processing-evidence/*/downstream_delta.json`

Derived/rebuildable:

- generated conformance examples
- generated report summaries
- verification logs

Durability gap: these files are local and recovery-critical. They do not survive machine loss until committed/pushed after review or backed up externally. This report uses explicit inventory/hashes rather than relying on `git diff` for untracked operational records.

## Real v1 fixture

Path: `artifacts/reports/provider-neutral-release-inbox-real-evidence-impact-pilot-v1-20260711/fixtures/real_wdi_exports_imports_release_v1.json`

- release ID: `wdi-trade-exports-imports-retained-evidence-v1`
- provider/dataset: World Bank / World Development Indicators
- indicators: NE.EXP.GNFS.ZS and NE.IMP.GNFS.ZS
- entities: DNK, SWE, NOR
- periods: 1990-2024
- item count: 210
- release fingerprint: `sha256:b2ee86039a991528a8e88c845a7aa9652562e2be9cce1e0f6ef3bca633a3f014`
- provenance: KnowledgeForge conformance fixture derived from retained provider evidence; not a genuine MacroForge export

## Controlled v2 fixture

Path: `artifacts/reports/provider-neutral-release-inbox-real-evidence-impact-pilot-v1-20260711/fixtures/controlled_successor_release_v2.json`

- release ID: `wdi-trade-exports-imports-controlled-test-v2`
- label: controlled_test_successor_release
- changed item: `wdi:DNK:NE.EXP.GNFS.ZS:2020`
- appended items: `wdi:DNK:NE.EXP.GNFS.ZS:2025, wdi:DNK:NE.IMP.GNFS.ZS:2025`
- removed items: none
- change-set fingerprint: `sha256:72ac330164359dc2413a8c2bd7667eef60d0bfe883b515a45a9970ef0a7d349c`

The v2 controlled values are test evidence only and are not claimed to come from WDI or MacroForge.

## Actual derivation registry entries

Registry: `specs/release_automation/real_derivation_applicability_registry_v1.json`

Entries:

- `pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1`

Each entry records canonical output package identity, pair identity, series dependencies, entity, frequency, period/transformation scope, method identity/version, method-contract fingerprint, evidence requirements, recomputation strategy, automatic-execution class, and promotion requirement.

## Affected/unaffected outputs

Changed scopes:

```json
{
  "entities": [
    "DNK"
  ],
  "indicators": [
    "NE.EXP.GNFS.ZS",
    "NE.IMP.GNFS.ZS"
  ],
  "periods": [
    2020,
    2025
  ]
}
```

Affected:

- `pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1`

Unaffected:

- `pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1`

Affected-derivation fingerprint: `sha256:3b1bac1e7b6715e548b2e16b524a81e85810732be51d07d68af5d2db93ab5131`

## No-promote recomputation

Incremental recomputation count: 1.
Avoided recomputation count: 2.
Full comparison count: 3.

Prior DNK coefficient: `0.988873850642`.
Controlled-test recomputed DNK coefficient: `0.989755588995`.
Candidate result fingerprint: `sha256:5398faa672dab1fffa352d9e075fe7490349a0df205d68b04bcc6778f6df49de`.

Incremental result equals the independently executed full no-promote recomputation result for the affected derivation.

No canonical packages were promoted or mutated. PostgreSQL was not updated.

## Idempotence and failure handling

Statuses:

```json
{
  "process_fingerprint_mismatch": {
    "failure_rejection_reason": "release_fingerprint_mismatch",
    "processing_status": "quarantined_release",
    "received_status": "invalid_release"
  },
  "process_identical_v1_again": {
    "failure_rejection_reason": null,
    "processing_status": "successfully_processed_no_promote",
    "received_status": "already_processed_identical_release"
  },
  "process_malformed_release": {
    "failure_rejection_reason": "malformed_json:JSONDecodeError",
    "processing_status": "quarantined_release",
    "received_status": "invalid_release"
  },
  "process_missing_predecessor": {
    "failure_rejection_reason": "missing predecessor release",
    "processing_status": "quarantined_release",
    "received_status": "out_of_order_release"
  },
  "process_out_of_order_v1_after_v2": {
    "failure_rejection_reason": "release already processed before current registry head",
    "processing_status": "quarantined_release",
    "received_status": "out_of_order_release"
  },
  "process_v1_once": {
    "failure_rejection_reason": null,
    "processing_status": "successfully_processed_no_promote",
    "received_status": "unseen"
  },
  "process_v2_again": {
    "failure_rejection_reason": null,
    "processing_status": "successfully_processed_no_promote",
    "received_status": "already_processed_identical_release"
  },
  "process_valid_successor_v2": {
    "failure_rejection_reason": null,
    "processing_status": "successfully_processed_no_promote",
    "received_status": "valid_successor_release"
  },
  "process_wrong_contract_version": {
    "failure_rejection_reason": "wrong_contract_version",
    "processing_status": "quarantined_release",
    "received_status": "invalid_release"
  },
  "reuse_v1_release_id_altered_content": {
    "failure_rejection_reason": "release_id reused with different content fingerprint",
    "processing_status": "quarantined_release",
    "received_status": "conflicting_reuse_of_release_id"
  }
}
```

Failure/resume statuses:

```json
{
  "process_v1_once": {
    "failure_rejection_reason": null,
    "processing_status": "successfully_processed_no_promote",
    "received_status": "unseen"
  },
  "process_v2_simulated_failure": {
    "failure_rejection_reason": "simulated recomputation failure",
    "processing_status": "processing_failed",
    "received_status": "valid_successor_release"
  },
  "resume_v2_after_failure": {
    "failure_rejection_reason": null,
    "processing_status": "successfully_processed_no_promote",
    "received_status": "valid_successor_release"
  }
}
```

## Downstream delta export

Path: `/home/mkkto/srv/EIP/projects/KnowledgeForge/artifacts/release-inbox-v1/processing-evidence/wdi-trade-exports-imports-controlled-test-v2/downstream_delta.json`

The delta contains processed release ID, predecessor release ID, release fingerprint, change-set fingerprint, changed scopes, affected derivations, unaffected derivations, recomputed candidates, candidate results, promotion status `not_promoted`, supersession plan, downstream export fingerprint, and compact impact cards.

Consumer check: a consumer can determine what changed, which relationship would change, which relationships remain valid, whether canonical promotion occurred, and which release caused the change.

## Producer conformance package

Path: `artifacts/reports/provider-neutral-release-inbox-real-evidence-impact-pilot-v1-20260711/producer_conformance/`

Contains neutral release-contract specification, minimal valid example, controlled invalid examples, fingerprint rules, unit/missingness requirements, predecessor/supersession rules, validation command, and expected validation results.

It does not reference MacroForge table names, MacroForge Python classes, MacroForge credentials, or KnowledgeForge private PostgreSQL schema.

## Eventing and local AI

Eventing decision: manual CLI and bounded inbox scan only. No daemon, cron installation, systemd, webhook, event bus, database notification, or scheduler.

Local AI used: zero. Future local-AI candidates remain proposal-only and must be validated by deterministic rules or review.

## Doctrine and architecture classification

- Repository inconsistency: none found for this slice.
- Governance inconsistency: none; no Production Doctrine or KnowledgeObjectPackage redesign was performed.
- Tooling/environment issue: none blocking; stale generated `context/active_context.md` warnings may appear in context-health/coherence checks.

## Verification summary source

Detailed verification outputs are under `artifacts/reports/provider-neutral-release-inbox-real-evidence-impact-pilot-v1-20260711/verification/` after final verification.
