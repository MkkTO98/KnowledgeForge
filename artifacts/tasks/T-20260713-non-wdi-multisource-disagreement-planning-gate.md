# T-20260713 Non-WDI Multi-Source Disagreement Planning Gate

Status: selected; not started
Date: 2026-07-13
Decision: `artifacts/decisions/D-20260713-post-repair-production-readiness-gate.md`
Backlog source: `B-20260709-025 — Phase 2 non-WDI multi-source disagreement planning gate`

## Objective

Open a bounded production-enabling planning gate for non-WDI multi-source disagreement.

The task is to determine whether KnowledgeForge can support a later objective production campaign around source disagreement without architecture redesign, doctrine amendment, schema change, or interpretive leakage.

## Why selected

The prior Campaign 44 Pearson registry-freeze proposal was rejected under stricter marginal-value review. Corrected-policy Pearson eligibility does not obligate production. Campaigns 42-43 already proved raw/first-difference coexistence and retrieval. The remaining Pearson candidates are low-to-medium marginal value and concentrated in one demographic/health cluster.

The non-WDI disagreement gate targets a documented falsification gap, PEL-017, that remains after repeated WDI family maturation.

## Required scope

The planning gate must:

1. identify candidate non-WDI or multi-source evidence families suitable for objective disagreement production;
2. compare source readiness, reproducibility, licensing/retention feasibility, and deterministic fixture requirements;
3. distinguish objective source-disagreement knowledge from interpretation, causal claims, policy meaning, or investment meaning;
4. decide whether a later production campaign is justified;
5. if justified, define the smallest later production boundary;
6. if not justified, record why and select no production campaign.

## Stop before

- source acquisition;
- ingestion implementation;
- package construction;
- package publication;
- PostgreSQL mutation or rebuild;
- Relationship Export output mutation;
- architecture/doctrine/schema changes;
- MacroForge/InsightForge/other-project modification;
- staging, commit, push, tag, or release;
- protected residue cleanup.

## Verification expected when implemented

- documented evidence-source candidates and explicit rejection/selection basis;
- architecture/doctrine non-expansion check;
- objective-knowledge boundary check;
- reproducibility/retention prerequisites;
- no production mutation;
- repository-wide tests and canonical/PostgreSQL unchanged checks.
