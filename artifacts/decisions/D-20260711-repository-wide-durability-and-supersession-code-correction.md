# D-20260711 Repository-Wide Durability and Supersession-Code Correction

Status: accepted
Decision: D — canonical/recovery-critical state remains locally vulnerable.

## Context

The prior durability inventory was too narrow. KnowledgeForge contains 538 canonical packages and a broad dirty/untracked operational system that would not be recoverable from the current remote repository.

## Decision

Do not stage. Do not commit. Do not push.

Accept the supersession immutability correction, but treat the repository as not durability-ready until recovery-critical material has an approved durable destination and sensitive/local-path review is complete.

## Rationale

- Full repository inventory found 3922 untracked files / 48094254 bytes.
- Machine-loss analysis found 3597 recovery-critical/historical files / 46137234 bytes would be lost if only the current remote remained.
- All 538 canonical packages are present locally but not recoverable from current remote Git.
- Production supersession mutation risks were corrected/disabled, but staging is still blocked by durability and sensitive/local-path review.

## Consequences

- Use a hybrid storage policy: ordinary Git for canonical/small text state, immutable external storage or Git LFS for large raw evidence/release histories/logs, database backups for operational PostgreSQL only.
- Keep temporary DB `knowledgeforge_immutability_gate_20260711` unless explicit deletion authorization is given.
- Request only the smallest remediation: durability-destination decision and sensitive/local-path remediation before staging.
