> Supersession note (2026-07-09 sovereignty correction): This report remains historical evidence. Any recommendation for a project-specific adapter, shared interface, schema coupling, or repository dependency is superseded by the KnowledgeForge-owned Source Evidence Package v1 Real-Fixture Replay Validation Slice.

# Production Gap Analysis

Date: 2026-07-09
Status: complete
Scope: gap analysis only; no production knowledge generated

## Executive conclusion

External WDI evidence can support a first controlled KnowledgeForge production campaign only after a narrow KnowledgeForge-owned real-fixture replay validation slice. The blocker is not evidence availability. The blocker is that audited evidence is source/repository-shaped while KnowledgeForge Validation Framework v1 expects package-shaped evidence references, provenance envelopes, fingerprints, selection/query definitions, validation states, and lifecycle metadata.

No external repository modification is required for the first production campaign. No runtime infrastructure is required. No ontology redesign is justified.

## Gap matrix by knowledge category

| Knowledge category | Immediate production status | Blocking gaps | Effort estimate | Remediation |
|---|---|---|---|---|
| WDI source evidence inventory | Not production-ready yet | No KnowledgeForge SourceEvidencePackage real fixture; no package-level selection/query/package fingerprints; no v1 package fixture from real external WDI evidence. | Small | Build a tiny immutable evidence fixture/snapshot into v1 candidate package JSON; add tests. |
| WDI evidence quality and missingness | Not production-ready yet | Missing deterministic KnowledgeForge missingness-summary generator; validation outputs need scoped selection from source-quality evidence; historical failed task-174 row needs caveat handling. | Small-medium | Add query specs and templates for coverage/missingness/freshness/validation summaries; exclude or caveat stale failed validation rows by run scope. |
| WDI demographic structure coverage | Nearly ready after real-fixture replay validation | Need exact production campaign scope manifest; need cohort-family indicator whitelist; need query fingerprints and package generation templates. | Small-medium | First campaign should start here after real-fixture replay validation. |
| WDI indicator-family classification | Not production-ready | Requires governed mapping table or deterministic classification rules; local AI not needed for first version. | Medium | Create reviewed indicator-family mapping contract; validate no overclaiming. |
| Simple derived metrics | Not production-ready | Requires formula registry, method metadata, input completeness checks, and result fingerprinting. | Medium | Implement only after evidence inventory/missingness packages pass. |
| Statistical characterization | Not production-ready | Requires method registry, boundary-language validators, outlier/missingness policy, and package templates. | Medium | Defer until real-fixture package assembly proves robust. |
| Cross-country descriptive comparisons | Not production-ready | Requires careful vocabulary guardrails to avoid InsightForge interpretation; ranking/percentile package contract. | Medium | Defer behind statistical characterization. |
| Cross-time trend summaries | Not production-ready | Requires deterministic trend descriptor vocabulary and missingness/window policy. | Medium | Defer behind evidence-quality and demographic coverage campaign. |
| Multi-provider/cross-source knowledge | Not production-ready | Only external WDI annual-scalar evidence has been audited as near-term production candidate; cross-provider source compatibility is not audited for KnowledgeForge production. | Large | Separate source-specific readiness audits before use. |
| Revision/vintage-aware knowledge | Not production-ready | The audited WDI annual-scalar evidence does not prove revision/vintage identity at production scale. | Large | Wait for revision-aware time-series stress-class work. |
| Company/entity/event/matrix knowledge | Not production-ready | Outside current external WDI annual-scalar confidence cell; identity and provenance contracts unvalidated. | Large | Separate architecture and evidence audits required. |

## Gap separation

### Architectural gaps

1. No explicit KnowledgeForge `SourceEvidencePackage` real-fixture contract.
2. No production package assembly contract mapping external source evidence/snapshots/manifests to KnowledgeForge Evidence, Evidence Evaluation, Knowledge Candidate, Knowledge Object, and Knowledge Change stages.
3. No selected first production campaign scope manifest.
4. No explicit rule for handling stale/historical validation evidence versus current campaign validation evidence.

Remediation:

- Implement a narrow repository-independent real-fixture replay validation slice before production generation.
- Define accepted/rejected source evidence fields and how they map to v1 package fields.

### Repository gaps

1. Current audited evidence inventory is WDI-only.
2. Current audited evidence shape is annual-scalar; broader evidence classes remain unproven for KnowledgeForge production use.
3. `meta.dataset_release.release_date` is null in audited WDI rows, though release/freshness exists through release keys and WDI `lastupdated` metadata.
4. `meta.lineage_event.checksum_sha256` is null in audited lineage rows, though raw artifact hashes exist in manifests.

Remediation:

- Treat external WDI annual-scalar evidence as the only first-campaign production substrate.
- Derive source freshness from WDI source metadata, release key, as-of date, and retained evidence metadata.
- Use raw artifact hashes from manifests as evidence fingerprints; do not rely on lineage-event checksum fields.

### Metadata gaps

1. KnowledgeForge package-level source family and evidence family classifications are not present in source evidence by default.
2. Package-level missingness summaries are not precomputed.
3. Package-level selection/query definitions and computation recipes are not stored as KnowledgeForge artifacts.
4. Indicator-family mappings are not yet governed KnowledgeForge assets.

Remediation:

- Generate package metadata in KnowledgeForge from an immutable external evidence fixture/snapshot.
- Do not mutate external source metadata or other repositories.
- Add a governed mapping artifact only when needed for campaign scope.

### Validation gaps

1. Validation Framework v1 has only synthetic fixtures; it has not validated real external evidence package candidates.
2. Current validators check structure and boundary language but do not recompute all fingerprints from real source manifests/selection specs.
3. No production-readiness test fixture exists for a real WDI Evidence package.

Remediation:

- Next implementation task: repository-independent Source Evidence Package v1 real-fixture replay validation using a tiny immutable WDI evidence fixture/snapshot, still non-production.
- Add negative fixtures for missing raw hashes, missing source URL, missing query fingerprint, overclaim language, and stale validation evidence.

### Provenance gaps

1. Provenance is distributed across source evidence and artifact files rather than package-shaped.
2. No KnowledgeForge provenance envelope for real external WDI evidence exists yet.
3. External lineage details may be too generic to be the only provenance source.

Remediation:

- Assemble provenance envelope from source metadata, release/vintage metadata, artifact manifests, raw artifact metadata, quality/validation evidence, and selection/query spec.

### Automation gaps

1. No command exists to produce a KnowledgeForge candidate package from an external WDI evidence fixture.
2. No command exists to validate real external evidence packages end-to-end.
3. No campaign closeout workflow exists for production package generation.

Remediation:

- Add a small deterministic CLI in KnowledgeForge after explicit implementation approval.
- Avoid daemons, schedulers, APIs, dashboards, and background infrastructure.

### Performance gaps

1. The full WDI evidence universe is large enough that naive all-repository package generation could be wasteful.
2. Production campaign needs query scoping and cached intermediate manifests.
3. Large package text should not duplicate raw data.

Remediation:

- Start with package manifests and aggregate summaries, not one package per observation.
- Fingerprint query outputs and package inputs; store compact summaries and evidence references.

## Production-readiness gates

Before production knowledge generation begins, complete these gates:

1. SourceEvidencePackage real-fixture contract accepted.
2. Tiny real external WDI fixture package generated in non-production mode and validated by v1.
3. Query, input, raw artifact, method, template, and package fingerprints recomputed and tested.
4. Boundary-language validator rejects downstream-interpretation language.
5. Campaign scope manifest selected and reviewed.
6. Freshness, missingness, and validation output handling documented.
7. Handoff/state/backlog updated with no external repository mutation or coupling.

## Gap conclusion

The first production campaign is viable only after a small real-fixture replay validation slice. The highest-leverage prerequisite is not ontology work. It is a deterministic KnowledgeForge-owned Source Evidence Package v1 replay validation with a real external WDI fixture.
