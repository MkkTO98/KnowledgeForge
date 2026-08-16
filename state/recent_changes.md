# Recent Changes

## 2026-07-09 — Operational Autonomy and repository-first expansion

- Declared KnowledgeForge operationally autonomous for ordinary Operational Expansion.
- Added operational autonomy, standard loop, and doctrine-review trigger docs.
- Completed WDI Infrastructure closeout through Campaign 15; repository reached 89 accepted objects.
- Completed WDI Energy & Mining Campaigns 16-18; family became Mature; repository reached 161 objects.
- Completed WDI Agriculture & Rural Development Campaigns 19-21; family became Mature; repository reached 233 objects.
- Completed WDI Health Campaigns 22-24; family became Mature; repository reached 305 objects.
- Production Doctrine mechanics remained unchanged through all campaigns.

## 2026-07-10 — Campaigns 25-32 and 500-object trigger

- Completed WDI Education Campaigns 25-27; family became Mature.
- Completed WDI Trade Campaigns 28-30; family became Mature.
- Completed WDI Financial Sector Campaigns 31-32; family became Stable.
- Repository object count reached 504; fingerprint `sha256:d9edfd69ca2718e407614856cddf9503e12f436ed522c5acd5f995a6ceb2148c`.
- Campaign 32 reached the 500-object repository-scale Doctrine Review Trigger.

## 2026-07-10 — Repository-scale doctrine review completed

- Completed mandatory 500-object Repository-Scale Doctrine Review.
- Decision: Recommendation B — Production Doctrine remains sufficient; revise/annotate roadmap or sequencing.
- Campaign 33 disposition: proceed immediately after the review gate closes.
- PostgreSQL disposition: schedule separate bounded repository-realization decision; no implementation authorized.

## 2026-07-10 — Campaign 33 WDI Financial Sector closeout

- Accepted the 500-object Repository-Scale Doctrine Review with Recommendation B.
- Completed Campaign 33 WDI Financial Sector provenance-lineage closeout.
- Accepted 17 KnowledgeObjectPackages and preserved 4 rejected candidates.
- WDI Financial Sector reached Mature status.
- Repository count: 521; fingerprint `sha256:9c7ebb9cc47f3dc58a06828fa334e53473b59f563845b1c64343840ee7a9479c`.
- Production stopped before Campaign 34. Next task: Bounded PostgreSQL Knowledge Repository Realization Decision.

## 2026-07-10 — Bounded PostgreSQL realization decision

- Completed the PostgreSQL realization decision gate.
- Selected Option B: durable KnowledgeForge-owned PostgreSQL operational repository derived and rebuildable from canonical packages.
- Confirmed PostgreSQL is not required for current raw performance at 521 objects, but is justified for operational realization and future retrieval/discovery needs.
- Preserved full KnowledgeObjectPackage JSON as canonical and filesystem-backed packages as the authoritative artifact layer.
- Performed no implementation, schema/API/service/loader work, Campaign 34, doctrine modification, or cross-project coupling.

## 2026-07-10 — PostgreSQL operational projection implementation

- Implemented the first local KnowledgeForge-owned PostgreSQL operational projection slice.
- Created/used database `knowledgeforge`, schema `knowledgeforge_projection`.
- Loaded 521 canonical KnowledgeObjectPackages with repository fingerprint `sha256:9c7ebb9cc47f3dc58a06828fa334e53473b59f563845b1c64343840ee7a9479c`.
- Verified payload fidelity, package fingerprints, deterministic/idempotent rebuilds, stale-state fail-closed behavior, and no canonical package byte changes.
- Did not start Campaign 34, add consumer access, implement an API/service, introduce incremental sync, modify doctrine/packages, or add cross-project coupling.

- 2026-07-10: Removed generic WDI unit fallback; implemented Pearson correlation method v1; selected Campaign 36 specification without execution.
- 2026-07-11: Completed MacroForge neutral evidence release compatibility pilot; validated bounded KnowledgeForge adapter, no-promote Pearson recomputation, downstream delta, and integration decision B.

## 2026-08-08/16 — Deterministic candidate-funnel pilot and re-closeout

- Reused the Pearson registry for 40 candidates: 30 excluded, 4 selected, 6 deprioritized, 0 unresolved/escalated; no production or publication occurred.
- Re-closeout disclosed premature execution and non-isolated cache mutation. `c4e3e2a…` satisfies the dependency prospectively; RED-GREEN corrected elapsed evidence, output paths, and malformed containers. Independent review passed; candidate remains unstaged/unpublished.
