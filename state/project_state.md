# Project State

Updated: 2026-07-13

## Current state

KnowledgeForge is on `main` after the published post-Campaign-43 test-discovery correction. The post-repair production-readiness gate has been adversarially corrected.

Corrected selected path: D — defer/reject the remaining corrected-policy Pearson candidates for immediate priority and select the strongest documented production-enabling alternative.

Selected next task: Phase 2 non-WDI multi-source disagreement planning gate, from backlog item `B-20260709-025`.

## Pearson disposition

- NOR crude birth rate / under-5 mortality: deferred indefinitely.
- NOR crude birth rate / life expectancy: deferred indefinitely.
- NOR crude death rate / under-5 mortality: deferred indefinitely.
- DNK forest area / private credit: rejected for current production priority; preserve only as archived policy residue unless future remote-pair pressure-test work explicitly needs it.

Rationale: Pearson eligibility and residue closure do not establish production priority. The remaining NOR pairs are narrow, clustered, and likely to repeat known time-trend qualification lessons. The DNK pair is remote and mainly cautionary.

## Alternative disposition

The proposed DNK/SWE/NOR `NE.EXP.GNFS.ZS` statistical-summary replication is not selected because Campaign 35 already produced and canonically accepted those exact three statistical-summary v2 packages.

## Production state

- canonical packages: 560
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- PostgreSQL projection: valid at 560 packages
- Relationship Export baseline from prior gate: 35 relationships; 21 raw Pearson; 14 first-difference Pearson
- repository-wide unittest discovery restored: 336 tests OK

No package production, coefficient calculation, summary calculation, registry creation, PostgreSQL mutation, Relationship Export output mutation, doctrine change, architecture change, schema change, staging, commit, push, tag, or release occurred during the correction.

## Active constraints

- Do not begin the non-WDI disagreement planning gate unless separately authorized.
- Planning gate only: no source acquisition, ingestion implementation, package construction/publication, PostgreSQL mutation/rebuild, Relationship Export output mutation, architecture/doctrine/schema change, or other-project modification.
- Preserve protected local residue: six `architecture/architectureharvest/` tracked deletions, eight Campaign 43 Relationship Export verification modifications, stale generated context, local config, caches/dumps/restore material, and unrelated operational/report residue.

## Important artifacts

- Decision: `artifacts/decisions/D-20260713-post-repair-production-readiness-gate.md`
- Task: `artifacts/tasks/T-20260713-non-wdi-multisource-disagreement-planning-gate.md`
- Report: `artifacts/reports/post-repair-production-readiness-gate-20260713/comparison_report.md`
- Roadmap: `docs/production_campaign_roadmap.md`
- Backlog: `artifacts/tasks/backlog.md`
