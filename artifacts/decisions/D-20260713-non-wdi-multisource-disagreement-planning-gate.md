# Decision: Reject Concrete Non-WDI Multi-Source Disagreement Candidate

Date: 2026-07-13
Status: accepted
Task: `artifacts/tasks/T-20260713-non-wdi-multisource-disagreement-planning-gate.md`
Report: `artifacts/reports/non-wdi-multisource-disagreement-planning-gate-20260713/report.md`
Backlog authority: `B-20260709-025`

## Decision

Reject the only concrete repository-supported source-pair candidate for this gate:

`world_bank_wdi_retained_trade_share_vs_macroforge_neutral_wdi_release_trade_share_dnk_swe_nor_1990_2024`.

No disagreement-production candidate is selected.

## Rationale

The candidate has retained evidence, metadata, deterministic fingerprints and a bounded DNK/SWE/NOR annual 1990-2024 trade-share scope, but it fails the source-independence requirement. The MacroForge neutral release is a producer export of WDI evidence into KnowledgeForge, not an independent source estimate.

A numerical difference between the two would indicate release, adapter, provenance, normalization, controlled-successor, or vintage/revision behavior. It would not be source disagreement.

## Rejected alternatives

Broad MacroForge-documented non-WDI capabilities are not concrete KnowledgeForge candidates yet because this repository does not retain a bounded two-source evidence bundle with sufficient source definitions, units, territorial scope, frequency, vintage/release metadata, revision policy, missing-value semantics, and licensing/retention evidence.

WDI release-vintage or controlled-successor comparisons remain useful for provenance/revision knowledge, but they are not non-WDI multi-source disagreement candidates.

## Required prerequisite before reopening

Reopen this workstream only after KnowledgeForge has, or has admitted through an existing producer-neutral handoff boundary, one immutable two-source evidence bundle that is:

- genuinely source-independent;
- bounded to one concept, one or a few entities, one frequency, and one time window;
- metadata-complete for equivalence testing;
- licensing/retention-cleared;
- deterministic and fingerprinted;
- usable without runtime imports, database access, shared code, or private schema dependence on MacroForge or another project.

## Architecture classification

No architecture, doctrine, schema, package-type, PostgreSQL, or Relationship Export change is required or justified. Existing SourceEvidencePackage, KnowledgeObjectPackage, provenance, evidence-quality, methodological, negative-knowledge and deterministic-fingerprinting structures are sufficient for both this rejection and any later properly bounded objective candidate.

## Boundaries preserved

This decision did not authorize source acquisition, API calls, ingestion, normalization, comparison calculation, disagreement registry creation, package construction/publication, PostgreSQL mutation, Relationship Export output mutation, other-project modification, staging, commit or push.
