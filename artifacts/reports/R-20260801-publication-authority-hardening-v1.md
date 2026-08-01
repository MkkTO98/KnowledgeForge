# R-20260801 — Publication Authority Hardening v1

Date: 2026-08-01
Status: Validated unstaged candidate; Git publication not authorized
Task: `artifacts/tasks/T-20260801-publication-authority-hardening-v1.md`
Decision: `artifacts/decisions/D-20260801-publication-authority-hardening-v1.md`

## Outcome and classification

KnowledgeForge now has one reusable repository-local publication-authority validator for exact candidate reconciliation and deterministic staging-plan authorization. This is a bounded governance/tooling correction, not a new Evidence Portfolio, batching subsystem, canonical ontology, database architecture or production campaign.

## Root cause

Earlier portfolio publication evidence was population-specific and could establish candidate intent, but no single executable mechanism authenticated the parent Git tree, reconciled complete, mixed and authority-only sources, separated parent-identical representations from real changes, preserved canonical authority history, and bound a future staging plan to current source bytes. That gap made exact publication scope dependent on operator procedure.

## Implemented correction

`tools/publication_authority.py` now validates strict canonical source manifests; resolves the exact current parent and tree with Git replacement refs disabled; verifies regular-file ancestry, modes, declared sizes and content hashes; detects duplicate/conflicting semantics; derives the true parent delta from Git objects; constructs deterministic authority and registry documents; preserves hash-chained predecessor history; rejects rollback and stale authorities; and builds/verifies exact staging gates against current source roots.

The CLI supports source verification, authority construction, registry installation, gate construction and gate verification. It emits a staging plan only. It never invokes `git add`, changes the index, commits or publishes.

## Adversarial coverage

The tests cover deterministic identity, exact parent delta, stale HEAD, source mutation after authority/gate construction, omitted and undeclared paths, duplicate/conflicting declarations, malformed/traversal/absolute/backslash paths, symlinked paths and ancestors, unsupported modes, declared-size drift, replacement refs, non-Boolean gates, parent-identical classification, durable-record constraints, registry schema/rollback/successor rules, inactive/self-invalid authority rejection, CLI end-to-end behavior and the corrected Sweden Infrastructure 64-path/58-change regression.

## Verification

- Focused authority/audit suite: 48/48 passed.
- Full repository suite: 473/473 passed in 38.137 seconds after supplying the repository-required sibling MacroForge durable-export fixture read-only; the initial isolated-topology run had six environment fixture errors and 467 passes, with no KnowledgeForge code failure.
- Compileall: passed.
- Security-pattern scan: passed; no subprocess shell execution, dynamic execution, pickle, network client or secret-like token was introduced in the new authority implementation.
- Coherence: zero blocks/warnings.
- Context health: passed.
- Architecture-to-Reality Audit after recording `R-20260801-architecture-reality-audit.md`: zero blocks/warnings.
- Independent review: one explicit-predecessor blocker and two cheap integrity findings were accepted, fixed and regression-tested; no unresolved correctness blocker remains.

## Durable continuity markers

- parent HEAD: `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3`
- exact audit-subject, final-candidate, source-manifest, authority, registry and gate identities are retained under `/tmp/knowledgeforge-publication-authority-hardening-4de0fcc/final/`;
- those external identities are intentionally not embedded here because this report is part of the frozen audit subject and embedding its own subject identity would create a self-hash cycle;
- `R-20260801-architecture-reality-audit.md`, which is excluded from the audit subject by contract, is the designated changed complete durable authority record and carries the required exact semantic markers.

## Residual boundary

The remaining risk is the conventional path-based time-of-check/time-of-use gap between a successful gate and a later Git index write. The accepted operating procedure therefore requires frozen verified source roots and immediate post-staging identity verification, or a future descriptor-based staging implementation. This task does not claim that filesystem path names alone are immutable.

No live PostgreSQL instance, other EIP project, admitted evidence, canonical Knowledge Object, Git index, commit, remote, tag or release was mutated. No follow-on task was activated.
