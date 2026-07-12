# PEL-009 Investigation Report — Reusable Production-Quality Metric Aggregation Helper

Date: 2026-07-09
Status: completed investigation
Scope: PEL-009 only

## Investigation question

Does repeated production evidence from Campaigns 0-2 justify implementing a reusable production-quality metric aggregation helper before Campaign 3?

## Evidence base

Evidence consulted:

- Campaign 0 production-quality report and runner.
- Campaign 1 production-quality report, retrospective, and runner.
- Campaign 2 production-quality report, cross-campaign assessment, and runner.
- `docs/production_evolution_log.md` after Campaign 2.

No evidence outside Campaigns 0-2 was used.

## Observed pattern

PEL-009 states:

> Production-quality metric aggregation is recurring manual work in domain campaigns.

Observed evidence:

- Campaign 0 established the production-quality report pattern.
- Campaign 1 retrospective records that production-quality metric aggregation repeated the Campaign 0 pattern.
- Campaign 2 production-quality/cross-campaign evidence records the same aggregation pressure again.
- Campaign 1 and Campaign 2 both compute category counts, rejected-category counts, validator failure counts, acceptance/rejection rates, average evidence references, provenance completeness, duplicate detection, fingerprint stability, and deterministic replay checks.
- Campaign 2 additionally compares metrics against Campaigns 0 and 1.

## Required evaluation

### How many times has the pattern occurred?

Formally: 2 domain campaigns after Campaign 0 established the pattern.

Contextually: 3 campaigns have produced production-quality reporting, but the repeated manual aggregation pressure was explicitly recorded starting in Campaign 1.

### Is the repetition structural or coincidental?

Structural.

The metrics are required by the production campaign discipline and recur because every campaign must preserve accepted objects, rejected candidates, validation failures, provenance/fingerprint/determinism checks, and category counts.

### Is the repeated work deterministic?

Yes.

The metrics are pure reductions over existing campaign artifacts: accepted object packages, rejected records, validation reports, fingerprints, and replay outputs.

### Is it sufficiently stable across campaigns?

Mostly.

Stable metrics across Campaigns 1-2:

- accepted object count;
- rejected candidate count;
- acceptance/rejection rate;
- validator failures by category;
- knowledge categories produced/rejected;
- average evidence references;
- provenance completeness;
- fingerprint stability;
- determinism verification;
- duplicate detection;
- processing statistics;
- report serialization.

Campaign 2 added cross-campaign comparison. That addition is likely durable, but it has only one campaign of evidence as a metric feature.

### Does it reduce readability or maintainability?

Manual aggregation increases repeated code and makes metric definitions vulnerable to small naming inconsistencies across campaigns.

A helper could improve maintainability by centralizing metric formulas and report field names.

Risk: centralizing too early could obscure campaign-specific metrics or force a rigid reporting schema before enough campaign variety exists.

### Does it introduce unnecessary manual work?

Yes.

Counting categories, failure categories, average evidence references, duplicate fingerprints, and acceptance rates is mechanical work repeated across campaigns.

### Would a helper preserve or weaken auditability?

It could preserve auditability if it emits transparent JSON plus markdown summaries from explicit campaign records, with no hidden filtering.

It would weaken auditability if it normalized away campaign-specific evidence, silently dropped rejected candidates, or made it hard to trace metric values back to objects and validation reports.

### Would a helper preserve or weaken reproducibility?

It could strengthen reproducibility because pure reductions over deterministic artifacts should produce stable metrics.

It would weaken reproducibility only if it read mutable global state, current time, live files outside the explicit campaign bundle, or inconsistent historical report schemas.

### Would a helper reduce validator clarity?

It should not affect validators.

Metric aggregation must report validator output, not reinterpret or repair it. The helper must preserve raw failure categories and stage reports.

### Would implementation introduce premature abstraction?

Implementation before Campaign 3 is still premature.

The core metric set is stable across Campaigns 1-2, but Campaign 2 only just introduced cross-campaign comparison. Campaign 3 will stress freshness/provenance metrics and should test whether the metric helper should remain a general campaign summarizer or split into base metrics plus campaign-specific metric sections.

### Could future campaigns invalidate the proposed helper?

Partially.

Future campaigns may require additional metrics such as multi-evidence-reference counts, lineage-depth metrics, object-volume distributions, or cross-family comparison metrics. A rigid helper could become a constraint. A minimal helper limited to base metrics would be safer, but Campaign 3 can clarify the boundary.

## Conceptual design if later justified

This is conceptual only. No code is authorized.

### Responsibility

A reusable production-quality metric aggregation helper would compute standard base production metrics from explicit campaign outputs.

It would not define campaign scope, generate knowledge, validate objects, or decide architecture.

### Boundaries

The helper must not:

- replace validators;
- alter accepted/rejected records;
- infer missing metrics from unrelated files;
- hide rejected candidates;
- impose a new campaign schema;
- redesign production reports;
- create runtime infrastructure;
- access databases/APIs/models;
- generate interpretation or recommendations.

### Inputs

Explicit inputs only:

- accepted KnowledgeObjectPackage records;
- rejected candidate records;
- validation stage reports;
- replay/fingerprint comparison result;
- optional campaign-specific processing statistics;
- optional prior campaign metrics when cross-campaign comparison is explicitly requested.

### Outputs

Existing output shapes only:

- production-quality JSON object;
- markdown production-quality summary;
- optional cross-campaign comparison section;
- no new canonical runtime type.

### Invariants

- every accepted/rejected count traces to concrete files or records;
- validator failures remain raw categories from validators;
- deterministic output for identical inputs;
- no silent dropping of rejected candidates;
- no hidden interpretation of quality beyond measured counts/booleans;
- campaign-specific metrics remain attachable without changing the base helper.

### Constitutional constraints

The helper must produce only production-quality metadata and audit metrics. It must not produce demographic, macroeconomic, policy, investment, causal, prospective, or recommendation meaning.

### Why deterministic

Metric aggregation is a pure computation over existing deterministic campaign outputs. Determinism is the primary reason a helper may eventually be justified.

## Decision

Classification: Continue Investigate

Justification:

- The repeated work is structural and deterministic.
- The repeated base metric set is stronger than PEL-008, because Campaign 0-2 all produced production-quality reporting.
- Still, implementation before Campaign 3 is not necessary: Campaign 3 will add freshness/provenance pressure and can clarify whether the base metric set remains stable under a new metadata emphasis.

## Recommendation for PEL-009

Do not implement before Campaign 3.

Continue investigation through Campaign 3 evidence. If Campaign 3 repeats the same base metric aggregation pattern without meaningful variation, a minimal helper proof may become ready after Campaign 3, constrained to base metrics and existing output shapes.
