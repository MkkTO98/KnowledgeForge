# D-20260801 — Mixed-Live Restoration Hardening v1

Date: 2026-08-01
Status: Accepted for repository-local implementation and validation; not publication-authorized
Decision class: bounded correction to the accepted Publication Authority Contract v1
Normative specification: `docs/evidence_portfolio_production_boundary_contract_v1.md`

## Decision

A mixed-path preservation snapshot may authorize later staging only when it is anchored to separately retained, independently authenticated original evidence. Current live bytes alone are not temporal proof of originality.

The snapshot and staging-gate path must therefore:

1. require an external original-evidence manifest and retained-byte root;
2. bind that evidence to the same authenticated parent HEAD and exact mixed path population;
3. prove current live identities equal the independent originals before capture;
4. copy protected snapshot bytes from the retained original-evidence source, not mutable live pathnames;
5. prove current live identities still equal the originals after capture;
6. verify original evidence, protected snapshot, current live files, and candidate representations separately at gate construction and verification;
7. bind the original-evidence fingerprint into the staging gate;
8. fail closed on late capture, M=1 overwrite, mutation, missing bytes, population drift, mode drift, stale parent state, and evidence/candidate substitution.

## Rationale

The previous mechanism could preserve candidate bytes as if they were originals when capture occurred after candidate application. A hash-only or live-derived snapshot cannot establish temporal provenance. The smallest coherent correction is to add a separately authenticated original-evidence input to the existing authority mechanism, not create another publication subsystem.

## Boundary

The external recovery package remains a governed trust input. The tool proves byte, mode, path-population and parent consistency; it cannot independently prove when an operator created fraudulent evidence. Ordinary path-based filesystem checks are not an atomic transaction, so uncooperative mutate-and-restore races remain outside this local tool's guarantee. Publication still requires exclusive ownership, frozen inputs, immediate verification and explicit human authorization.

No staging, commit, push, tag, release or publication is authorized by this decision.
