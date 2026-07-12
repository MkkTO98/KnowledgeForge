# Phase 2 Production Expansion Strategy

Date: 2026-07-09
Status: completed planning artifact
Scope: KnowledgeForge Phase 2 production-family expansion strategy after Campaigns 0-12

## 1. Authoritative design reviewed

This strategy treats the following as authoritative design:

- `CONSTITUTION.md`
- `docs/architecture.md`
- `state/architecture.md`
- accepted architectural decisions under `artifacts/decisions/`
- `docs/knowledge_package_contract.md`
- `docs/validation_framework_v1.md`
- `docs/validator_taxonomy.md`
- `docs/provenance_fingerprinting.md`
- `docs/production_quality_assessment.md`
- `artifacts/production/campaign-7-wdi-demographic-structure-provenance-lineage-completeness/reports/family_closeout_report.md`
- `artifacts/production/campaign-12-wdi-environment-provenance-lineage-closeout/reports/environment_family_closeout_report.md`
- `artifacts/production/campaign-12-wdi-environment-provenance-lineage-closeout/reports/production_methodology_closeout_report.md`
- `docs/production_evolution_log.md`
- `docs/production_campaign_roadmap.md`
- accepted production doctrine from the Production Methodology Closeout Report

Default posture: preserve the agreed architecture.

## 2. Phase 2 objective

Phase 2 transitions KnowledgeForge from production-methodology validation into systematic long-term knowledge expansion.

The goal is not to invent a new production method. The goal is to mature additional evidence families using the validated method, while progressively exercising remaining assumptions in an order that maximizes reusable objective knowledge and minimizes architectural drift.

## 3. Strategic recommendation

Phase 2 should use balanced expansion with WDI annual-scalar breadth first, followed by targeted depth and then deliberate non-WDI falsification.

Balanced means:

1. broaden across additional WDI annual-scalar families to prove repeatability at larger family count;
2. deepen only where family maturity criteria require inventory, coverage, provenance-lineage, rejected-candidate, and closeout evidence;
3. postpone non-WDI multi-source disagreement until there is enough WDI-family breadth to make disagreement tests meaningful rather than confounded by an immature internal methodology.

## 4. Recommended family order

1. WDI Infrastructure annual-scalar evidence.
2. WDI Energy & Mining annual-scalar evidence.
3. WDI Agriculture & Rural Development annual-scalar evidence.
4. Cross-family WDI annual-scalar comparison across Mature families.
5. WDI Trade annual-scalar evidence.
6. WDI Financial Sector annual-scalar evidence.
7. WDI Education or Health annual-scalar evidence, only after scale behaviour is understood.
8. Deliberate non-WDI multi-source disagreement workstream.

This is a production-family order, not a campaign list. Each family should mature through the established family criteria before being classified Mature.

## 5. Why this order maximizes reusable objective knowledge

Infrastructure is first because it was already identified as the strongest fallback during second-family selection and remains highly compatible with the validated WDI annual-scalar method. It adds objective structural and coverage knowledge without immediately increasing semantic boundary risk.

Energy & Mining follows because it increases non-demographic/non-environmental heterogeneity while remaining modest in size and annual-scalar compatible. It gives another test of technical-domain labels without policy or investment interpretation.

Agriculture & Rural Development follows because it is narrower and useful as a lower-scale contrast. Its value is methodological: it tests whether the method remains efficient for smaller families and whether family closeout criteria overfit to broad families.

A cross-family WDI comparison should follow once at least three or four families have Mature or near-Mature evidence. This naturally exercises multi-reference objects, duplicate pressure, partial provenance differences, and transferable structural knowledge without leaving the WDI source family.

Trade and Financial Sector are deferred until after additional controlled WDI breadth because they have higher interpretation-risk surfaces. They are valuable, but should be approached after validator boundary behaviour is repeatedly confirmed across less interpretation-prone families.

Education or Health should come later because scale is the main pressure. Their indicator counts are large enough to test practical scalability, catalogue management, and object-volume behaviour after smaller/mid-sized families establish baseline scaling expectations.

Non-WDI multi-source disagreement should be deliberate and later. It is the major remaining falsification gap, but doing it too early risks mixing source-family novelty, disagreement semantics, and production-family maturity in one step.

## 6. Expansion posture

Phase 2 should emphasize balanced expansion.

Breadth alone would create many partially characterized families without closeout evidence. Depth alone would over-optimize WDI annual-scalar internals and postpone the known non-WDI falsification gap too long. Balanced expansion retains the proven family maturity doctrine: each selected family moves through evidence-quality, inventory, coverage, provenance-lineage, rejection preservation, and closeout, while the selected sequence increases family heterogeneity over time.

## 7. Recommendation classification

| Recommendation | Classification | Justification |
| --- | --- | --- |
| Use balanced Phase 2 expansion | preserves agreed architecture | It applies the Production Methodology Closeout doctrine unchanged. |
| Mature Infrastructure next | preserves agreed architecture | It continues WDI annual-scalar family broadening as recommended after Campaign 12. |
| Mature Energy & Mining after Infrastructure | preserves agreed architecture | It adds controlled heterogeneity without new contracts. |
| Mature Agriculture after Energy | preserves agreed architecture | It tests smaller-family closeout behaviour inside existing contracts. |
| Run cross-family WDI comparison after additional family maturity | preserves agreed architecture | Campaign 9 proved multi-reference WDI comparison works without package change. |
| Defer Trade/Financial until boundary behaviour is further confirmed | preserves agreed architecture | It respects constitutional boundary risk without redesign. |
| Defer Education/Health scale stress until smaller families establish scaling baseline | preserves agreed architecture | It avoids premature scale pressure and does not change architecture. |
| Defer non-WDI multi-source disagreement to a deliberate later workstream | preserves agreed architecture | PEL-017 identifies this as a falsification gap, but not a blocker for WDI third-family broadening. |

No Phase 2 recommendation refines the architecture, duplicates an existing concept, contradicts an accepted decision, or introduces architectural drift.

## 8. Explicit non-recommendations

Phase 2 does not support:

- architecture redesign;
- taxonomy redesign;
- validator redesign;
- package-contract redesign;
- cross-campaign duplicate registry;
- additional helper extraction;
- runtime infrastructure;
- repository coupling;
- adapters/APIs/shared schemas;
- database coupling;
- local or frontier LLM generation;
- replacing family maturity with a new maturity vocabulary.

## 9. When to broaden beyond WDI annual-scalar evidence

KnowledgeForge should broaden beyond WDI annual-scalar evidence after Phase 2 has achieved at least:

1. three or four Mature WDI annual-scalar families;
2. at least one post-Campaign-12 cross-family comparison across more than two families;
3. continued absence of package/validator/taxonomy/provenance/fingerprint pressure;
4. an explicit planning gate for non-WDI multi-source disagreement that isolates source disagreement from immature family methodology.

The first non-WDI broadening should be a deliberate falsification workstream, not a domain-importance-driven expansion.
