# Validation Framework v1 Remaining Validation Gaps

Date: 2026-07-09
Status: completed

## Remaining gaps

1. Real MacroForge handle compatibility is untested.
   - The framework validates synthetic evidence handles only.
2. Real PostgreSQL query fingerprinting is untested.
   - No database access was allowed or performed.
3. Fingerprint values are presence-checked, not recomputed from canonical serialization.
   - This is acceptable for v1 fixture proof but insufficient for production.
4. Cross-package dependency resolution is minimal.
   - Current tests validate individual fixture objects rather than a package graph/directory.
5. Governed vocabulary validation is incomplete.
   - v1 validates broad status/kind categories, not all vocabularies from `docs/governed_vocabularies.md`.
6. Confidence and uncertainty are structurally validated, not semantically calibrated.
7. Contradiction handling is structurally validated, not semantically adjudicated.
8. Validator migration/revalidation policy is not implemented.
9. Local/frontier model routing is validated only indirectly through no-direct-evidence and no-unsupported-inference checks.
10. No production lifecycle acceptance workflow exists.

## Recommendations before first MacroForge capability audit

Before auditing MacroForge/PostgreSQL capability, use this framework as the contract checklist. The audit should ask whether MacroForge can provide:

- stable evidence references;
- source identity/version/vintage/access dates;
- reproducibility handles;
- data/package fingerprints;
- query-definition fingerprints;
- lineage/provenance reports;
- validation/drift reports;
- metadata sufficient for source-family classification;
- enough missingness/freshness/lineage metadata for KnowledgeForge evidence evaluation.

Do not start a production pilot until the audit maps real MacroForge outputs into the v1 package/evidence fields and identifies missing compatibility requirements.

## Next-step recommendation

KnowledgeForge is now ready for a MacroForge/PostgreSQL capability audit, but not for ontology freeze or production pilot.
