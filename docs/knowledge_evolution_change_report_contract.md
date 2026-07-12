# Knowledge Evolution and Change Report Contract

Date: 2026-07-09
Status: architecture specification; implementation not authorized

## 1. Purpose

KnowledgeForge must record why knowledge changes. A change report is the audit artifact that explains how new data, corrected data, changed computation, changed evidence evaluation, templates/models, contradictions, or validators affected a package or durable knowledge object.

A knowledge-change report is not a database transaction, workflow engine, or runtime scheduler.

## 2. Required report structure

### 2.1 Identity

- `change_report_id`;
- date/time;
- author/tool;
- related package IDs;
- related knowledge object IDs/revisions;
- change status: proposed, accepted, blocked, rejected, superseded.

### 2.2 Trigger category

At least one trigger must be specified:

- new data;
- corrected data;
- changed computation;
- changed evidence evaluation;
- changed template/prompt/model;
- contradiction discovery;
- validator change;
- manual governance correction;
- dependency change;
- scope/applicability change.

### 2.3 Before/after state

- prior package/object revision;
- new package/object revision;
- statements added/changed/removed;
- lifecycle/governance/confidence changes;
- dependencies affected;
- downstream review posture.

### 2.4 Evidence and method delta

- changed evidence references;
- changed input fingerprints;
- changed query fingerprints;
- changed computation recipe fingerprints;
- changed prompt/template/model fingerprints;
- changed validator version or result;
- explanation of whether the knowledge changed materially or only reproducibility metadata changed.

### 2.5 Contradiction and uncertainty delta

- new contradictions;
- resolved contradictions;
- unresolved contradictions;
- uncertainty/missingness changes;
- applicability narrowing or broadening.

### 2.6 Validation result

- validators run;
- blockers;
- warnings;
- environment issues;
- human/governance review requirement;
- acceptance decision or next action.

### 2.7 Reproducibility note

- can the prior state be reconstructed?
- can the new state be reconstructed?
- are all changed inputs/methods fingerprinted?
- is a rerun expected to reproduce the new result?

## 3. Trigger-specific requirements

### New data

Must record source/version/vintage, source evidence handle if applicable, and whether statements changed or only confidence/freshness changed.

### Corrected data

Must identify correction source, affected input fingerprint, affected package/object revisions, and whether previous knowledge is deprecated, questioned, or superseded.

### Changed computation

Must record recipe version, parameter changes, output delta, and whether previous outputs remain valid under old method.

### Changed evidence evaluation

Must record evaluation rationale, evidence dimension changed, contradiction/uncertainty impact, and lifecycle implications.

### Changed template/prompt/model

Must record old/new template or model fingerprints and determine whether wording only changed or generated statements materially changed.

### Contradiction discovery

Must record contradiction type, target statement, contradicting evidence, disposition, and required review propagation.

### Validator change

Must record validator version, new/removed checks, packages affected, and whether prior accepted packages require revalidation.

## 4. Change disposition

A change report should result in one of:

- no material knowledge change;
- candidate revision created;
- supported/accepted revision created;
- object questioned;
- object deprecated;
- contradiction retained without resolution;
- scope narrowed;
- dependency review required;
- package blocked pending evidence or validation.

## 5. Anti-patterns

Reject change reports that:

- say "updated due to new data" without identifying data fingerprints;
- change generated statements without package version evolution;
- hide contradictions by overwriting old statements;
- treat validator failure as editorial preference;
- collapse lifecycle, confidence, and governance into a single status.
