# Evidence Portfolio Conformance Profile v1

Status: implementation candidate; validated for isolated adaptation only
Contract identity: `knowledgeforge.evidence_portfolio.conformance.v1@1.0`
Date: 2026-08-01

## Purpose

This prospective profile corrects four bounded defects found by the published Norway Health / Sweden Infrastructure generalization review:

1. pre-execution exclusion was collapsed into runtime rejection;
2. governed analytical questions were not mechanically bound to candidates and evidence;
3. transformation labels and identities drifted across manifest, result and view surfaces;
4. source-series record diversity obscured shared provider, acquisition and method dependence.

The profile is one conformance layer over the existing Evidence Portfolio composition. It is not a new canonical object, evidence family, calculation method, portfolio subsystem, projection schema, database or universal dependence ontology.

## Compatibility boundary

Historical Norway Health and Sweden Infrastructure manifests, execution evidence, packages, views, reports, tasks and canonical records are immutable. They do not silently satisfy this profile. `validate_conformance_envelope()` rejects an unadapted historical manifest with a clear schema/version error.

`build_historical_conformance_envelope()` creates a separate versioned representation that embeds deep-copied parsed source manifest, execution, package and view objects and binds their canonical semantic fingerprints and package/result/view/source identities. It does not preserve or claim the original JSON file bytes. It also embeds the exact source report text and extracts the governed conclusion section mechanically. It performs no acquisition or recalculation and rewrites no historical identifier or conclusion. The adapter records every structural correction explicitly.

Envelope validation proves deterministic self-consistency and exact binding to the embedded source artifacts. It is not a digital-signature scheme: provenance authentication still requires the isolated proof to compare those embedded artifacts and report hashes with the governed repository inputs.

This task validates isolated envelopes only. Applying the profile as a mandatory live production boundary requires a separate governed task.

## Deterministic identity

Canonical serialization is UTF-8 JSON with sorted keys, compact separators and no ASCII coercion. A fingerprint is `sha256:` plus SHA-256 of those bytes. The envelope fingerprint excludes only its own `conformance_fingerprint` field.

Transformation identity is the fingerprint of:

```json
{
  "base_series_identity": "source-series:sha256:...",
  "definition": {
    "transformation_id": "...",
    "operation": "...",
    "parameters": {}
  }
}
```

The profile currently admits only transformations already present in both reviewed portfolios:

- `level`: identity operation, no parameters;
- `adjacent_first_difference`: first-order difference over consecutive retained annual periods;
- `linear_time_index_slope`: ordinary-least-squares slope against integer calendar year, descriptor only.

The historical result label `linear_time_index` is retained in historical records but adapted to the declared `linear_time_index_slope` identity in the new envelope. This is an explicit versioned mapping, not a historical rewrite.

## Accounting invariant

Every manifest candidate has exactly one terminal disposition from:

- `excluded_pre_execution`;
- `valid`;
- `rejected_execution`;
- `null`;
- `redundant_candidate`;
- `execution_failure`.

The required equations are:

```text
manifest_candidates
  = excluded_pre_execution + executed_candidates

executed_candidates
  = valid + rejected_execution + null
    + redundant_candidate + execution_failure

raw_result_records
  = valid_result_records + redundant_result_records
```

Candidate identities must cover the manifest, outcome and traceability populations exactly once. Missing, duplicate, unknown or contradictory dispositions fail. Excluded candidates never count as executed or rejected. Runtime rejection or failure requires an explicit `execution` or `post_execution_validation` stage; a pre-execution stage cannot be relabeled as runtime failure.

Record diversity and support diversity are separate. Transformed result variants and operational views do not create additional source-series or independent-support claims.

## Question-to-evidence traceability invariant

Every envelope contains at least one governed analytical question with:

- stable `question_id`;
- bounded question text;
- intended use;
- explicit prohibited uses;
- an ordered machine binding to each exact source-manifest candidate, including candidate semantic fingerprint, indicator, method and planned disposition;
- deterministic scope fingerprint.

Each candidate has one directional `question_to_candidate_to_evidence` link that repeats the source candidate semantic fingerprint. The relation vocabulary reserves `supports`, `weakens`, `qualifies`, `excludes` and `absence`; profile v1 admits only the terminal-state mapping justified by the source artifacts: `valid -> supports`, `excluded_pre_execution -> excludes`, and non-result execution outcomes -> `absence`. A later profile version is required before `weakens` or `qualifies` can be admitted.

For these two historical portfolios:

- executed candidates use `supports` and resolve to their transformed result evidence units;
- the preregistered CAGR candidate uses `excludes`, resolves to no calculated evidence unit and must retain its exact manifest exclusion reason.

Every evidence unit resolves through candidate and question IDs to the historical package, result, operational view, source-series identity and transformation identity. Orphan questions, candidates or evidence units; duplicate evidence links; changed exclusion reasons; unsupported question links; and drifted generated ledgers fail validation.

The profile does not claim general natural-language semantic inference. Semantic governance is bounded to the exact question scope, machine relation, candidate identity, source/result identities and exact exclusion reason. The validator prevents syntactic relabeling from changing those admitted semantics unnoticed.

## Transformation invariant

Each executable candidate declares exactly the three bounded transformations supported by the reviewed portfolios. Every transformation registry row includes:

- candidate identity;
- base source-series identity;
- stable transformation ID;
- exact operation;
- complete parameters;
- deterministic transformation identity.

Every evidence unit repeats the resolved transformation ID and identity. Aliases, missing parameters, collisions, substitutions, contradictory source lineage, duplicate definitions and unsupported transformation IDs fail closed. The identity function itself is generic enough to distinguish parameterized forms such as lag 1 versus lag 2, but profile admission remains closed to the three reviewed transformations.

## Dependence invariant

Every executable evidence candidate declares these currently justified dimensions separately:

- source-series cluster, bound directly to normalized source-series identity;
- provider semantic basis and deterministically derived provider cluster;
- acquisition/fixture-lineage semantic basis and deterministically derived acquisition cluster;
- method semantic basis and one deterministically derived cluster per method;
- dependence status: `known` or `unresolved`.

The profile reports source-series diversity separately from shared provider, acquisition and method grouping. It records zero fully independent support claims because neither reviewed portfolio establishes independence. Unknown or unresolved dependence therefore cannot silently become independence.

Sharing one attribute does not collapse otherwise distinct evidence: Norway's two source series remain two source-series clusters, while their WDI provider, retained Campaign 40 acquisition lineage and method family remain explicitly shared. The same invariant applies to Sweden.

## Generated candidate ledger

The envelope contains a marker-delimited Markdown table generated only from the machine candidate, outcome and traceability populations. Validation regenerates it and requires exact equality. Free-form task/report prose may add context but cannot replace this authoritative ledger.

## Isolated adaptation API

```python
from tools import evidence_portfolio_conformance as conformance

envelope = conformance.build_historical_conformance_envelope(
    manifest=manifest,
    execution_results=execution_results,
    packages=packages,
    views=views,
    portfolio_label="Norway Health",
    question="What deterministic baseline characteristics are present ...?",
    intended_use="bounded descriptive baseline characterization",
    prohibited_uses=["causal inference", "forecasting", "independent corroboration claim"],
    source_report_path="artifacts/reports/R-...md",
    source_report_text=source_report_text,
    conclusion_heading="## Production conclusion",
)
result = conformance.validate_conformance_envelope(envelope)
```

Use only external temporary output paths for the current correction task. Do not pass the live canonical repository to this module; it has no persistence API.

## Explicit non-claims

Two successful historical conformance envelopes demonstrate that the correction is coherent for Norway Health and Sweden Infrastructure. They do not establish:

- universal Evidence Portfolio generality;
- a third portfolio's admissibility;
- source or method independence;
- causal, predictive or investment conclusions;
- authorization to recalculate, migrate, publish or mutate canonical state;
- PostgreSQL or cross-project integration readiness.
