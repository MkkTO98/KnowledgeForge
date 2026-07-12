# Project State

Status: operational repository with completed real external-release handoff compatibility pilot.

Current repository authority remains file-backed `knowledge_repository/`; PostgreSQL remains a rebuildable operational projection only.

Latest completed integration slice:
- Task: `artifacts/tasks/T-20260711-macroforge-neutral-release-knowledgeforge-compatibility-pilot.md`
- Decision: `artifacts/decisions/D-20260711-macroforge-neutral-release-knowledgeforge-adapter-compatibility.md`
- Report: `artifacts/reports/macroforge-neutral-release-knowledgeforge-compatibility-pilot-20260711/consolidated_report.md`
- Result: B. KnowledgeForge-owned bounded adapter validated for MacroForge neutral evidence release v1.
- No canonical Knowledge Objects promoted; no PostgreSQL mutation/schema expansion; no Campaign 41.

Next recommended task: ask MacroForge to connect exporter execution to successful canonical release closeout.

## 2026-07-11 Provider-neutral outbox polling prototype

Completed manual provider-neutral MacroForge outbox polling prototype with unified release-registry authority, duplicate no-promote recognition, metadata sufficiency gate, controlled isolated supersession, isolated PostgreSQL projection evidence, and failure/recovery tests. No production canonical or production PostgreSQL mutation.

## 2026-07-11 Repository-wide durability inventory and supersession-code correction

Completed repository-wide durability inventory after rejecting the prior narrow staging grouping. Production-risk supersession paths were corrected: the outbox isolated prototype no longer mutates predecessor bytes, and repository persistence refuses non-identical overwrites of existing package ids. Full inventory found 538 local canonical packages, 3,920 untracked files / 48,094,254 bytes, 1,083 canonical files, and 3,597 recovery-critical/historical files / 46,137,234 bytes that would be lost if only the current remote remained. Decision: D — canonical/recovery-critical state remains locally vulnerable; no staging authorization requested. Next step is a durability-destination decision plus sensitive/local-path remediation before staging.

## 2026-07-12 Durability-destination decision and pre-staging remediation

Completed artifact-class durability destination policy and pre-staging remediation plan. Decision: B — policy complete and sensitive/local-path review clean; operational backup/checkpoint destination still requires approval. Validator now distinguishes actual secrets, reviewed false positives, unsafe absolute-path dependencies, untracked canonical state, untracked recovery-critical implementation, and operational state lacking backup. Current staged state is empty; prior staged-count reports were caused by treating `??` untracked files as staged. Latest validator remains invalid because canonical/recovery-critical implementation files are untracked/local-only and mutable operational state lacks backup/checkpointing.

## 2026-07-12 Operational state backup, restore, and durability gate

Implemented versioned local operational-state checkpoint/restore tooling, declarative protected-state configuration, sensitive-material exclusions, PostgreSQL reconstruction evidence, isolated restore validation, failure-mode tests, and validator semantics that distinguish local checkpoint coverage from machine-loss durability. Decision: D — local checkpoint covers current operational state and restore is verified, but it is same-host only (`tested_local_only = true`, `machine_loss_durable = false`); canonical/recovery-critical implementation files also remain untracked/local-only. No staging/commit/push, canonical mutation, production PostgreSQL write, scheduling, Campaign 41, MacroForge modification, or InsightForge modification.
