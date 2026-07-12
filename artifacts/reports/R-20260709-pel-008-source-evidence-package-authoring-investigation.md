# PEL-008 Investigation Report — Deterministic SourceEvidencePackage Authoring Helper

Date: 2026-07-09
Status: completed investigation
Scope: PEL-008 only

## Investigation question

Does repeated production evidence from Campaigns 0-2 justify implementing a deterministic SourceEvidencePackage authoring helper before Campaign 3?

## Evidence base

Evidence consulted:

- Campaign 0 production reports and runner.
- Campaign 1 production retrospective and runner.
- Campaign 2 production-quality, cross-campaign, architectural-observation reports, and runner.
- `docs/production_evolution_log.md` after Campaign 2.

No evidence outside Campaigns 0-2 was used.

## Observed pattern

PEL-008 states:

> SourceEvidencePackage field construction is recurring manual work in domain campaigns.

Observed evidence:

- Campaign 1 retrospective records that SourceEvidencePackage field construction was repeated across accepted and rejected packages.
- Campaign 2 production-quality/cross-campaign evidence records the same pressure again.
- The current production runners contain campaign-local `source_package(...)` functions that populate the same broad contract regions: identity, package kind/version, immutability, source identity, evidence payload, evidence metadata, provenance, reproducibility, and fingerprints.
- Campaign 0 also used a campaign-local `source_package(...)` function, but PEL-008 was only formally observed as domain-campaign pressure beginning in Campaign 1.

## Required evaluation

### How many times has the pattern occurred?

Formally: 2 completed domain campaigns, Campaigns 1 and 2.

Contextually: Campaign 0 also had a similar construction shape, but the evidence log treats Campaign 1 as the first explicit observation because Campaign 0 was repository/evidence characterization rather than domain evidence production.

### Is the repetition structural or coincidental?

Likely structural.

Reason: the repeated work follows the existing SourceEvidencePackage contract, not arbitrary campaign prose. The same contract regions must be populated for any package that enters the existing construction and validation pipeline.

However, the exact payload metadata differs by campaign. That means the structural pressure is real, but the stable helper boundary is not yet fully proven.

### Is the repeated work deterministic?

Yes.

The repeated construction uses deterministic field assignment, deterministic canonical fingerprinting, immutable snapshots, and no model execution.

### Is it sufficiently stable across campaigns?

Partially.

Stable across Campaigns 1-2:

- required SourceEvidencePackage contract regions;
- deterministic fingerprint insertion;
- source identity/provenance/reproducibility structure;
- accepted/rejected package construction path.

Not yet fully stable:

- exact evidence payload metadata shape;
- campaign-specific source identity wording;
- campaign-specific provenance basis;
- degree to which malformed/rejected candidates should be easier to construct or deliberately remain explicit.

### Does it reduce readability or maintainability?

The current manual construction increases file length and repetition. It also makes it easier to accidentally drift field names or omit required contract fields.

But the explicit form is currently readable and audit-friendly. A helper could improve maintainability only if it remains transparent and emits the exact existing package dictionary without hiding campaign-specific evidence.

### Does it introduce unnecessary manual work?

Yes, repeated contract scaffolding is unnecessary once the package contract is stable.

The campaign-specific payload itself remains necessary manual/evidence work.

### Would a helper preserve or weaken auditability?

It could preserve auditability if it is a thin deterministic constructor that emits ordinary SourceEvidencePackage dictionaries and leaves all evidence payload/provenance inputs explicit.

It would weaken auditability if it introduced defaults, inferred missing evidence, hid provenance construction, auto-generated campaign meaning, or made rejected candidates harder to inspect.

### Would a helper preserve or weaken reproducibility?

It could preserve reproducibility if it uses canonical deterministic inputs and existing fingerprinting.

It would weaken reproducibility if it used clocks, random values, environment state, external data reads, or implicit repository scans.

### Would a helper reduce validator clarity?

It should not touch validators.

Risk: if a helper silently prevents invalid packages from being expressible, tests may lose clear rejected-candidate examples. The helper must not replace negative fixture/candidate construction unless it can deliberately construct malformed cases for testing without masking failures.

### Would implementation introduce premature abstraction?

Implementation before Campaign 3 would probably be premature.

Evidence shows repeated pressure, but only two domain campaigns have exercised it, both in the same WDI demographic evidence family. Campaign 3 will test freshness/provenance metadata within the same family and should clarify whether helper responsibility is source-package contract construction generally or WDI-specific metadata convenience. Implementing now risks overfitting to Campaigns 1-2.

### Could future campaigns invalidate the proposed helper?

Yes.

Campaign 3 may show that provenance/freshness packages need a slightly different authoring pattern. Campaigns 8-9 may show that a helper designed from WDI demographic evidence overfits one evidence family. This argues against implementation now.

## Conceptual design if later justified

This is conceptual only. No code is authorized.

### Responsibility

A deterministic SourceEvidencePackage authoring helper would construct an ordinary existing SourceEvidencePackage object from explicit caller-provided evidence fields.

It would reduce repeated contract scaffolding while preserving the existing package hierarchy.

### Boundaries

The helper must not:

- define a new package model;
- modify validators;
- infer evidence meaning;
- create new knowledge categories;
- access databases, APIs, repositories, or model systems;
- generate interpretation, forecasts, recommendations, policy meaning, investment meaning, or narrative;
- become WDI-specific unless separately justified;
- replace rejected-candidate preservation.

### Inputs

Explicit inputs only:

- package id;
- statement text;
- existing knowledge category;
- campaign id/date;
- immutable source identity;
- evidence payload metadata;
- provenance basis;
- reproducibility handle;
- source snapshot fingerprint or explicit source-version value.

### Outputs

One existing SourceEvidencePackage dictionary that validates under the current construction pipeline.

Optional future proof task may also require that manually authored packages and helper-authored packages produce identical canonical fingerprints for the same semantic input.

### Invariants

- deterministic output for identical input;
- no implicit defaults that alter evidence meaning;
- no hidden provenance;
- existing fingerprint method preserved;
- existing validator behavior unchanged;
- package remains serializable as existing JSON artifact;
- rejected candidates remain preservable and inspectable.

### Constitutional constraints

The helper must reject or pass through only evidence-level statements. It must not generate interpretation, causal claims, hypotheses, forecasts, recommendations, policy/investment meaning, or presentation narrative.

### Why deterministic

The helper exists only to remove repeated mechanical package-contract construction. Its purpose would be reproducible package construction, not knowledge generation.

## Decision

Classification: Continue Investigate

Justification:

- Repetition is real and structural enough to investigate.
- Evidence is not yet broad enough for implementation because Campaigns 1-2 are both WDI demographic-family campaigns.
- Campaign 3 should provide more evidence about freshness/provenance package construction before a helper proof is designed.

## Recommendation for PEL-008

Do not implement before Campaign 3.

Preserve the current architecture and production pipeline. Continue collecting evidence during Campaign 3, with special attention to whether package scaffolding repeats unchanged or whether provenance/freshness packages expose a different helper boundary.
