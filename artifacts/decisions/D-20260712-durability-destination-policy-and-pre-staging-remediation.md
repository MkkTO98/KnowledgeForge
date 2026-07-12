# D-20260712 Durability Destination Policy and Pre-Staging Remediation

Date: 2026-07-12
Status: accepted
Decision: B — durability policy complete; operational backup/checkpoint destination still requires approval.

## Context

Repository-wide durability inventory established that current remote Git cannot recover KnowledgeForge's local operational system. The accepted architecture requires preserving substantive knowledge and calculation capability, not merely reports or governance metadata.

## Decision

Primary durability treatment by artifact class:

- canonical KnowledgeObjectPackage JSON: A ordinary Git
- manifest, indexes, fingerprints, and evolution records: A ordinary Git
- method and calculation contracts: A ordinary Git
- correlation/batch specifications: A ordinary Git
- source code and tests: A ordinary Git
- small evidence fixtures: A ordinary Git
- large raw provider responses: C immutable external artifact storage
- release exports and histories: A ordinary Git while small text/audit artifacts fit current scale; C immutable external artifact storage once measured size stops being reviewable in ordinary Git
- accepted source copies: D operational backup/checkpointing
- derivation registries: A ordinary Git when append-only canonical provenance; D operational backup/checkpointing when mutable operational registry
- seen-release registries: D operational backup/checkpointing
- current-state registries: D operational backup/checkpointing
- outbox transport state: D operational backup/checkpointing
- PostgreSQL projection and backups: E projection deterministically rebuildable from durable canonical inputs; D backups for operational recovery only
- reports, logs, generated context: E for generated context/caches; A for compact decision-bearing reports; C for large raw logs/report bundles
- task, decision, doctrine, roadmap, architecture, state, handoff records: A ordinary Git
- sensitive/local configuration: F sensitive/local-only and excluded

## Justification

Current canonical package JSON is small, textual, deterministic, and central to reconstruction. Ordinary Git maximizes auditability, reviewability, reproducibility, and repository independence for canonical packages, methods, source/tests, specifications, governance records, and small deterministic fixtures.

Git LFS or immutable external artifact storage is reserved for measured large raw/binary evidence, full release histories, large logs/report bundles, and future artifacts that no longer fit ordinary Git review. It is not introduced merely for hypothetical scale.

PostgreSQL is an operational projection and retrieval layer only. It can be backed up for operational recovery, but it must never become canonical authority or sole backup.

## Sensitive/local-path disposition

No actual secret blockers remain. Active absolute path dependencies in source/test/config/manifest metadata were parameterized or made portable. Historical local-path references and credential-keyword scanner hits are reviewed false positives or provenance/report references and do not expose secret values.

## Compatibility

This policy protects the 538 canonical objects, all current statistical-summary and Pearson objects, reusable calculation engines/contracts, release-driven recomputation, immutable supersession history, PostgreSQL reconstruction, and future deterministic relationship expansion.

## Required next action

Approve and implement a small operational backup/checkpoint mechanism for mutable registries and PostgreSQL operational backups. After that, rerun the validator and only then request staging authorization for ordinary-Git durability groups.
