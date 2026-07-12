> Supersession note (2026-07-09 sovereignty correction): This report remains historical evidence. Any recommendation for a project-specific adapter, shared interface, schema coupling, or repository dependency is superseded by the KnowledgeForge-owned Source Evidence Package v1 Real-Fixture Replay Validation Slice.

# First Production Campaign Recommendation

Date: 2026-07-09
Status: complete
Scope: recommendation only; no production knowledge generated

## Single recommendation

The first KnowledgeForge production campaign should be:

```text
WDI Annual-Scalar Demographic Structure Evidence-Quality and Coverage Knowledge
```

This campaign should generate governed KnowledgeForge packages about:

- External WDI demographic-structure source scope;
- age-sex cohort indicator-family membership;
- country/year/indicator coverage;
- observed versus missing evidence status;
- source freshness and raw artifact provenance;
- validation-state summaries;
- deterministic descriptive metadata for the evidence slice;
- negative knowledge about what the audited repository slice does not support.

It must not generate demographic interpretation, forecasts, hypotheses, investment meaning, country recommendations, policy conclusions, or causal claims.

## Why this campaign

This campaign maximizes the requested criteria:

| Criterion | Assessment |
|---|---|
| Reproducibility | Strong. External WDI evidence fixtures/snapshots include source URLs, raw artifact hashes, run parameters, as-of dates, and observed/missing fact status. |
| Determinism | Strong. Coverage, missingness, freshness, cohort-family membership, and source/provenance summaries are deterministic computations. |
| Validator coverage | Strong. Existing Validation Framework v1 can validate evidence references, provenance, fingerprints, maturity state, boundary language, and package structure after an real-fixture validation is added. |
| Architectural stability | Strong. Stays inside WDI annual-scalar data, the audited external WDI annual-scalar confidence cell. |
| Future downstream reuse | Strong. Downstream reasoning systems can later use demographic evidence-quality and coverage packages as safe context without duplicating observation/provenance logic. |
| Minimal frontier-model dependence | Strong. No frontier LLM is required; deterministic computation plus templates is sufficient. |

## Evidence supporting recommendation

Audit evidence:

- The audited evidence inventory contains WDI-only annual-scalar facts.
- The audited inventory contains 1,377,595 curated facts, 182 indicators, 217 territories, annual periods 1990-2024.
- Observation status is explicit: 1,095,789 observed and 281,806 missing facts.
- TASK-180 demographic structure closure added 68 five-year female/male age-band count/share indicators and 516,460 rows.
- WDI raw artifact manifests include URLs, SHA-256 hashes, bytes, row counts, content type, WDI `lastupdated`, and non-null observation counts.
- The audited evidence inventory records demographic structure as operationally complete within WDI annual-scalar scope for national annual historical five-year age-sex cohort analysis.

## What the campaign should produce

After prerequisite real-fixture replay validation, the campaign may produce packages in these families:

1. Evidence inventory package
   - WDI demographic-structure source slice scope.
   - Included indicators, territories, periods, fact counts, observed/missing counts.

2. Indicator-family structure package
   - Female/male five-year cohort indicator families.
   - Count/share family separation.
   - Age-band boundaries and 80+ open-ended class where source indicator names/codes support it.

3. Coverage and missingness packages
   - Completeness by indicator, territory, year, and indicator family.
   - Missingness summaries with explicit observation-status definitions.

4. Provenance/freshness package
   - Source URL, WDI release metadata, run key, raw artifact URLs/hashes, as-of date, and relevant validation outputs.

5. Negative knowledge package
   - This audited slice does not support forecasts, causal demographic explanations, policy/investment conclusions, non-WDI source comparison, or revision/vintage claims.

6. Methodological package
   - How external WDI annual-scalar evidence maps into KnowledgeForge EvidenceReference and package provenance.

## Required prerequisite task before this campaign

Do not start production generation immediately. First implement:

```text
Source Evidence Package v1 Real-Fixture Replay Validation Slice
```

This prerequisite should:

- remain non-production;
- use only a tiny immutable read-only external WDI evidence fixture/snapshot;
- assemble v1-shaped Evidence and KnowledgeCandidatePackage fixtures;
- compute/fingerprint selection/query specs, method specs, template specs, evidence manifests, and package content;
- validate the fixtures with `tools/validate_knowledge_pipeline_v1.py`;
- add negative fixtures for missing evidence/provenance/fingerprint and downstream-interpretation boundary language;
- avoid cross-repository mutation, adapters, shared schemas, APIs, daemons, schedulers, dashboards, database coupling, and production package generation.

## Campaign non-goals

The first production campaign should not include:

- GDP/macroeconomic interpretation;
- demographic burden or policy narratives;
- ranking countries by attractiveness or economic quality;
- forecasting population structure;
- causal relationships;
- multi-source reconciliation;
- non-WDI providers;
- local or frontier LLM generation;
- graph/database/runtime infrastructure;
- consumer-facing reports or visualizations.

## Deferred campaign candidates

Defer these until after the first campaign proves package generation/review/change mechanics:

1. WDI trade balance derived-metric packages.
2. WDI indicator-family classification across all 182 indicators.
3. Cross-country/cross-time statistical characterization packages.
4. Correlation/relationship packages with negative-knowledge support.
5. Multi-provider source packages.
6. Revision/vintage-aware packages.

## Final recommendation statement

Proceed next with the non-production Source Evidence Package v1 Real-Fixture Replay Validation Slice. After that slice passes validation, the first controlled production campaign should be External WDI Annual-Scalar Demographic Structure Evidence-Quality and Coverage Knowledge.

Do not begin production knowledge generation before repository-independent real-fixture replay validation passes.
