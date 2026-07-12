# D-20260711 Canonical Supersession Immutability and Durability Gate

Status: accepted

## Decision

Correct KnowledgeForge supersession architecture so canonical package bytes remain immutable. Current/superseded state must be stored outside package JSON bytes in a current-state registry or projection table, with append-only supersession/evolution records linking predecessor and successor packages.

## Finding

The previous isolated supersession prototype mutated predecessor package bytes by changing `confidence_quality.lifecycle_state` from `accepted` to `superseded`. The package fingerprint field stayed the same, but the JSON byte hash changed, so the model violated canonical immutability.

## Correction

Use this model:

1. Immutable package object remains byte-identical forever.
2. Successor package is appended as a distinct package identity/version.
3. Supersession is recorded in append-only evolution records.
4. Current-state identity is represented by an external current-state registry/projection.
5. PostgreSQL stores immutable package payload separately from package_current_state.

## Production posture

Do not authorize production supersession until the corrected model is reviewed, staged, committed, and backed up. Retain full projection rebuild for production until incremental current-state publication has an explicit consistency/rollback decision.
