# Existing Card and Output Architecture Review

Date: 2026-07-09
Status: completed
Task: Campaign 1 planning — taxonomy verification and structural production design

## Purpose

Determine whether the existing card/output model and package hierarchy are already formally specified and adequate for Campaign 1.

## Existing package hierarchy

`docs/knowledge_package_contract.md` defines the authoritative package hierarchy:

| Package kind | Current role |
| --- | --- |
| KnowledgeCandidatePackage | Proposed statements before full validation/review. |
| KnowledgeObjectPackage | Accepted/supported durable knowledge objects or revisions. |
| KnowledgeChangePackage | Governed coherent change across objects. |
| EvidenceEvaluationPackage | Reusable scoped evidence evaluations. |
| GeneratedIntermediatePackage | Parsed/extracted/model-assisted intermediate material with no direct acceptance. |

The production pipeline proven in Campaign 0 uses the relevant subset:

```text
SourceEvidencePackage → Evidence → EvidenceEvaluation → KnowledgeCandidatePackage → KnowledgeObjectPackage
```

## Existing output model

The current output model is package-first and file-backed:

- immutable source package JSON;
- candidate package JSON;
- accepted object package JSON;
- rejected candidate JSON;
- campaign summary JSON;
- production quality report JSON/Markdown;
- human-readable campaign reports and catalogues.

This is adequate for Campaign 1 because it preserves determinism, provenance, replay, rejection evidence, and auditability without introducing runtime infrastructure.

## Existing card-equivalent architecture

The repository does not currently define an independent production "card system" as a separate runtime or schema. Historical assimilation artifacts adapted MetaHarvest component-card lessons into compact object/evidence/evaluation cards, but the formal current architecture expresses that role through:

- `EvidenceReference`;
- `EvidenceEvaluation`;
- `KnowledgeCandidatePackage`;
- `KnowledgeObjectPackage`;
- package catalogues and production reports.

Therefore the correct continuity-preserving interpretation is:

- package records and catalogues are the current card-equivalent output form;
- cards are not a separate object type;
- Campaign 1 must not introduce a competing card system.

## Finding

The existing package/output model remains appropriate. Campaign 0 did not reveal a card/output deficiency.

## Non-changes recommended

- Do not introduce a separate card schema.
- Do not rename packages as cards.
- Do not create dashboard, API, database, renderer, or presentation outputs.
- Continue using file-backed package JSON plus catalogues/reports for controlled production campaigns.
