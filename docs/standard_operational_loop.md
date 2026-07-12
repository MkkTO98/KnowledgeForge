# KnowledgeForge Standard Operational Loop

Status: authoritative operational loop
Classification: preserves agreed architecture

## Purpose

This document defines the default operating cycle for KnowledgeForge Operational Expansion.

It does not redesign production. It makes explicit the campaign loop already established by the Production Doctrine, Phase 2 roadmap, repository-first operational addendum, and family maturation methodology.

## Default loop

For ordinary production work, execute the following loop automatically:

1. Select the next production family according to the approved roadmap.
2. Execute the next campaign using the Production Doctrine unchanged.
3. Validate every KnowledgeObjectPackage.
4. Populate the Knowledge Repository with validated packages only.
5. Produce governance artifacts.
6. Produce Repository Health Summary.
7. Produce Knowledge Repository Impact Assessment.
8. Update the Production Evolution Log.
9. Evaluate family maturity.
10. Continue automatically unless a Doctrine Review Trigger occurs.

## Family progression rule

Each production family should normally progress through:

1. evidence-quality/source-evidence transfer;
2. inventory/classification production where applicable;
3. territorial and temporal coverage/matrix production where applicable;
4. provenance-lineage completeness;
5. family maturity assessment;
6. Family Closeout Report when Mature criteria are satisfied.

If a family reaches Stable but not Mature, continue the family rather than switching families.

If a family reaches Mature, produce or confirm the Family Closeout Report, then move to the next family in the roadmap.

## Repository-first closeout rule

A campaign is not operationally complete until the Knowledge Repository has been updated and the campaign reports repository value.

Required closeout artifacts:

- Production Quality Report;
- Repository Health Summary;
- Knowledge Repository Impact Assessment;
- rejected candidate catalogue/report where applicable;
- family maturity assessment where applicable;
- Production Evolution Log update;
- task/state/handoff continuity updates.

## Roadmap authority

`docs/production_campaign_roadmap.md` is the authoritative sequencing artifact for ordinary production progression.

External prompts are no longer required for ordinary campaign selection. Prompts may still request a stop, audit, review, or deviation, but absent such instruction the roadmap governs the next campaign.

## Doctrine preservation rule

Normal campaign execution must not modify:

- production workflow;
- package hierarchy;
- validator framework;
- taxonomy;
- provenance model;
- fingerprint model;
- Production Support;
- reporting model;
- family maturation methodology;
- repository model.

Changes require a Doctrine Review Trigger and repeated production evidence.
