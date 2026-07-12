# D-20260711 Provider-Neutral Outbox Polling and Controlled Supersession Prototype

Status: accepted

## Decision

Adopt manual provider-neutral external-outbox polling now, define `artifacts/release-inbox-unified-v1/seen-release-registry.jsonl` as the future production registry authority for real external releases, retain full PostgreSQL projection rebuild for production for now, and defer incremental PostgreSQL publication until a bounded consistency decision establishes transaction/current-state/rollback guarantees.

## Rationale

The real MacroForge closeout-triggered outbox release is discoverable, transferable, hash-validated, adapter-processable, and recognized as the same release already accepted through manual handoff. Controlled supersession works in isolation and compact delta retrieval is feasible, but production incremental projection has higher divergence and recovery risk than full rebuild until stronger transactional semantics are specified.

## Boundaries

No production canonical package mutation, no production PostgreSQL schema expansion, no MacroForge dependency, no scheduler installation, and no Campaign 41.
