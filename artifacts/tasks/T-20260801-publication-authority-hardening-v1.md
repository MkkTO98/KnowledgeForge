# T-20260801 — Publication Authority Hardening v1

Status: Completed as an unstaged working-tree candidate
Owner: exclusive Hermes session
Classification: bounded governance/tooling correction; no production, schema or architecture redesign
Decision: `artifacts/decisions/D-20260801-publication-authority-hardening-v1.md`
Specification: `docs/evidence_portfolio_production_boundary_contract_v1.md`
Final report: `artifacts/reports/R-20260801-publication-authority-hardening-v1.md`

## Objective

Implement and prove the smallest reusable publication-authority mechanism that authenticates parent state, reconciles exact complete/mixed/authority-only source populations, preserves authority history, and emits a deterministic fail-closed staging plan without staging or publishing.

## Pre-mutation recovery

- Authoritative branch/HEAD/origin: `main` / `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3` / aligned; ahead/behind 0/0.
- Staged paths: zero.
- Frozen live baseline: 493 Git-visible dirty identities plus ignored-state inventory in `/tmp/knowledgeforge-publication-authority-hardening-4de0fcc/live_baseline.json`.
- No overlapping live KnowledgeForge owner or material task collision was accepted.
- Prospective path authority: `/tmp/knowledgeforge-publication-authority-hardening-4de0fcc/candidate_allowlist_v2.json`.
- Implementation occurred only in `/tmp/knowledgeforge-publication-authority-hardening-4de0fcc/workspace` before guarded application.

## Completed work

1. Added `tools/publication_authority.py` with strict source-manifest validation, authenticated Git parent/tree reads, exact mode/size/hash checking, complete/mixed/authority-only reconciliation, parent-delta classification, deterministic authority identity, canonical registry history, staging-gate construction/verification and CLI commands.
2. Added generic and Sweden Infrastructure regression fixtures/tests plus an independent adversarial test module.
3. Corrected findings from independent review: explicit predecessor naming, registry rollback detection, exact registry/authority schemas, source-size verification, invalid-authority installation rejection, durable-report semantic markers, symlink-ancestor rejection, replacement-ref immunity and source-root/current-HEAD binding.
4. Updated the accepted production-boundary contract rather than creating a parallel publication architecture.
5. Recorded the scheduled Architecture-to-Reality Audit and completed file-backed closeout.

## Verification

- Focused publication-authority plus architecture-audit suite: 48/48 pass.
- Full repository discovery with the required read-only sibling durable-export fixture: 473/473 pass.
- Python compileall and security-pattern scan: pass.
- Coherence and context health: pass using an ignored validation-only workspace linkage.
- Formal Architecture-to-Reality Audit after report write: zero blocks, zero warnings.
- Independent adversarial review: final blocker and integrity findings corrected and regression-tested.

## Outcome

The reusable authority mechanism is validated as an unstaged candidate. It narrows future publication scope and fails closed on stale identity, malformed manifests, unbound source state, duplicate/conflicting declarations, invalid lifecycle/history, rollback and source mutation. It does not itself stage or publish.

No follow-on task was activated.
