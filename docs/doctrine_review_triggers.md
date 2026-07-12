# KnowledgeForge Doctrine Review Trigger Specification

Status: authoritative trigger specification
Classification: preserves agreed architecture

## Purpose

This document defines the only events that interrupt normal KnowledgeForge Operational Expansion.

Ordinary campaigns do not trigger doctrine review. Architecture, production methodology, validators, taxonomy, package hierarchy, provenance, fingerprinting, Production Support, reporting model, and repository model remain preserved unless one of the triggers below occurs with evidence.

## Trigger standard

A doctrine review is justified only when production evidence, repository evidence, or an explicitly listed milestone shows that ordinary roadmap execution may be insufficient.

Speculation, convenience, elegance, anticipated reuse, architectural preference, external-project similarity, or campaign novelty are not triggers.

## Doctrine Review Triggers

### 1. Repeated production evidence against doctrine

Trigger: two or more campaigns expose the same production failure or friction that cannot be resolved inside current doctrine.

Examples:

- repeated accepted-object construction failure caused by package-contract insufficiency;
- repeated inability to express evidence-level knowledge without boundary loss;
- repeated deterministic replay failures not caused by tool/environment issues.

### 2. Repository-quality degradation

Trigger: persisted repository state shows quality degradation.

Examples:

- unresolved duplicate Knowledge Objects;
- unstable repository fingerprints for unchanged inputs;
- missing provenance in accepted persisted objects;
- index inconsistency;
- repository object count or lifecycle-state inconsistency after verified campaign execution.

### 3. Repeated validator insufficiency

Trigger: repeated false positives or false negatives in validators affect valid production candidates or allow unsafe accepted objects.

Expected validator rejections are not a trigger. Rejections are safety evidence unless repeated evidence proves the validator is insufficient.

### 4. Repeated package-model insufficiency

Trigger: repeated production evidence shows accepted knowledge cannot be represented without distorting constitutional boundaries or losing required provenance/applicability/lifecycle/governance state.

### 5. Repeated provenance insufficiency

Trigger: repeated accepted-candidate or repository evidence shows the current provenance envelope cannot preserve source/evidence/reproducibility lineage needed for reuse.

### 6. Repeated fingerprint insufficiency

Trigger: repeated evidence shows current fingerprints cannot detect material input, recipe, validation, generated-statement, or package-manifest changes.

### 7. First non-WDI source

Trigger: the first production family whose evidence source is not WDI.

Required review scope: source-boundary, provenance, source-system identity, raw evidence snapshot, and provider-specific limitations.

This is a bounded doctrine review trigger, not automatic architecture redesign.

### 8. First non-annual evidence shape

Trigger: first production family using non-annual, non-scalar, panel, event, textual, high-frequency, distributional, revision-aware, or otherwise non-current WDI annual-scalar evidence shape.

Required review scope: whether existing evidence-level package construction and applicability fields preserve objectivity and reproducibility.

### 9. First statistically-derived knowledge family

Trigger: first family where accepted knowledge would depend on statistical computation rather than deterministic inventory/coverage/provenance/completeness transforms.

Required review scope: computation provenance, assumptions, reproducibility, uncertainty representation, and boundary against interpretation.

### 10. First correlation or relationship knowledge family

Trigger: first family where accepted knowledge encodes correlations, relationships, associations, mappings, or dependency claims rather than evidence-quality or coverage facts.

Required review scope: claim boundaries, evidence support, non-causality language, uncertainty, applicability, and unsupported-inference rejection.

### 11. First external consumer

Trigger: first external consumer project, such as InsightForge, depends on KnowledgeForge repository artifacts operationally.

Required review scope: representation neutrality, export/serving boundary, non-authority of consumer outputs, and repository provenance expectations.

### 12. Major repository-scale milestone

Trigger: repository reaches a major scale threshold.

Current milestones:

- 500 Knowledge Objects;
- 5,000 Knowledge Objects;
- 50,000 Knowledge Objects.

Required review scope: repository health, index determinism, performance, duplication, provenance completeness, fingerprint stability, and continuity/governance overhead.

## Non-triggers

The following do not interrupt ordinary operations:

- starting the next planned WDI annual-scalar family;
- ordinary rejected candidates;
- ordinary family Stable status;
- ordinary family Mature status;
- ordinary Repository Health or Repository Impact Assessment generation;
- ordinary report wording improvements;
- convenience-based helper ideas;
- preference for a cleaner abstraction;
- the existence of similar machinery in another EIP project.

## Review output if triggered

A doctrine review must classify the evidence as one of:

- preserves agreed architecture;
- refines agreed architecture;
- duplicates an existing concept;
- contradicts an accepted architectural decision;
- introduces architectural drift.

If evidence is insufficient, preserve doctrine unchanged and return to the roadmap.
