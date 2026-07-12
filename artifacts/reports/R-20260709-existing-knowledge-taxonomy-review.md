# Existing Knowledge Taxonomy Review

Date: 2026-07-09
Status: completed
Task: Campaign 1 planning — taxonomy verification and structural production design

## Purpose

Verify whether KnowledgeForge already contains the knowledge taxonomy needed for the first domain-specific production campaign, without redesigning or replacing established concepts.

## Sources reviewed

- `CONSTITUTION.md`
- `docs/architecture.md`
- `docs/governed_vocabularies.md`
- `docs/knowledge_acceptance_criteria.md`
- `docs/knowledge_package_contract.md`
- `docs/interfaces.md`
- `tools/construct_knowledge_package_v1.py`
- `tools/validate_knowledge_pipeline_v1.py`
- Campaign 0 production quality and architectural observation reports

## Current authoritative taxonomy

KnowledgeForge already has two compatible taxonomy layers.

### 1. Foundational component model

`docs/architecture.md` defines durable knowledge objects through orthogonal components rather than a flat inheritance hierarchy:

- identity;
- content;
- applicability;
- evidence;
- evolution;
- governance.

This is the higher-level architecture. It remains authoritative for durable knowledge-object design.

### 2. Claim-facet governed vocabularies

`docs/governed_vocabularies.md` defines claim classification through governed facets:

- assertion function;
- epistemic nature;
- polarity;
- domain role;
- representation form;
- dependency posture and dependency facets.

The architecture explicitly rejects rigid claim inheritance hierarchies as the primary ontology design. Campaign 1 must therefore classify knowledge using existing orthogonal facets rather than inventing new object subclasses.

### 3. Production knowledge categories

`docs/knowledge_acceptance_criteria.md` and `tools/construct_knowledge_package_v1.py` define the current production-safe accepted categories:

- factual;
- derived;
- classified;
- methodological;
- evidence_quality;
- coverage;
- negative;
- provenance.

Campaign 0 used six of these categories successfully: factual, derived, methodological, coverage, negative, and provenance. It did not require new categories.

## Finding

The existing KnowledgeForge architecture already contains an adequate knowledge taxonomy for Campaign 1.

Campaign 1 should not introduce a competing taxonomy. It should use:

- component model for object completeness;
- governed facets for classification semantics;
- production categories for validator-gated statements.

## Non-changes recommended

- Do not replace the component model.
- Do not replace claim facets with card types or subclasses.
- Do not add a new demographic taxonomy.
- Do not promote trend, ranking, comparison, or statistical characterization categories until production evidence requires them.
