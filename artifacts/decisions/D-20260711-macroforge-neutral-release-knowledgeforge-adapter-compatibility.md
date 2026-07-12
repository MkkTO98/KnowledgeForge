# Decision — MacroForge Neutral Release Compatibility Ownership

Date: 2026-07-11
Status: accepted

## Decision

B. KnowledgeForge-owned bounded adapter.

MacroForge owns its external producer export representation. KnowledgeForge owns ingestion, validation, and internal normalized release representation. The MacroForge export contains sufficient semantics for KnowledgeForge to ingest it through a documented external-contract adapter, while preserving MacroForge producer identity and fingerprints.

## Rationale

- The unchanged KnowledgeForge validator rejected the MacroForge export because of contract identity, field-name, and fingerprint-shape differences, not because of observation meaning or missing provenance.
- Producer fingerprints validated independently: selection `sha256:2b1a1c3d9e65b182f073e0171c59627c8298740ee9cb7c1418dfbae3ae196e0a`, release `sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67`.
- All 210 canonical observation keys matched retained KnowledgeForge WDI evidence by value, unit, period, frequency, entity, indicator, and missingness.
- Definition text differed in granularity and is recorded as a representation difference rather than silently normalized away.
- No-promote recomputation reproduced DNK/SWE/NOR existing Pearson coefficients exactly.

## Consequences

- KnowledgeForge may support `macroforge.neutral_evidence_release_export.v1` through `knowledgeforge_macroforge_neutral_release_adapter_v1@1.0`.
- Producer release ID, producer release fingerprint, selection fingerprint, original provider/dataset, and MacroForge release/run lineage must be preserved.
- KnowledgeForge may compute an additional normalized-release fingerprint for its own deterministic representation.
- Unsupported MacroForge contract versions, fingerprint failures, duplicate keys, invalid missingness, ambiguous units, or unexpected scope fail closed.
- This does not authorize shared runtime code, MacroForge database access, canonical promotion, scheduling, PostgreSQL mutation, or KnowledgeObjectPackage redesign.

## Next step

1. Ask MacroForge to connect exporter execution to successful canonical release closeout.
