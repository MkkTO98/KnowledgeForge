> Supersession note (2026-07-09 sovereignty correction): This report remains historical evidence. Any recommendation for a project-specific adapter, shared interface, schema coupling, or repository dependency is superseded by the KnowledgeForge-owned Source Evidence Package v1 Real-Fixture Replay Validation Slice.

# MacroForge Compatibility Audit for KnowledgeForge Validation Framework v1

Date: 2026-07-09
Status: complete
Scope: architecture and PostgreSQL repository audit only; no production knowledge generation

## Executive conclusion

MacroForge is compatible enough to support a first controlled KnowledgeForge production campaign, but not directly compatible with the full KnowledgeForge Validation Framework v1 contract.

The current MacroForge PostgreSQL repository is strongest as a source of WDI annual-scalar canonical observation evidence. It provides source identity, canonical observation identities, deterministic load runs, source URLs, raw artifact hashes, raw artifact paths, as-of dates, annual period identity, explicit missing/observed status, and quality-check records.

It does not by itself provide KnowledgeForge-ready package-shaped evidence. KnowledgeForge still needs a repository-independent Source Evidence Package v1 real-fixture replay validation slice that turns external source evidence/snapshots/manifests/selection definitions and validation evidence into explicit Evidence and KnowledgeCandidatePackage structures with package-level fingerprints.

## Audited PostgreSQL state

Read-only query target: PostgreSQL database `macroforge`.

Observed counts:

| Metric | Count |
|---|---:|
| `meta.source` | 1 |
| `meta.dataset_release` | 3 |
| `meta.pipeline_run` | 8 |
| `meta.lineage_event` | 16 |
| `meta.quality_check` | 16 |
| `staging.wdi_observation` | 3,173,661 |
| `curated.fact_observation` | 1,377,595 |
| `curated.dim_indicator` | 182 |
| `curated.dim_territory` | 217 |
| `curated.dim_period` | 35 |
| `curated.dim_unit` | 1 |
| `curated.dim_attribute_set` | 1 |

Repository contents:

- Source: WDI / World Bank World Development Indicators.
- Curated fact coverage: 182 WDI indicators, 217 territories, annual periods 1990-2024.
- Observation status: 1,095,789 observed facts and 281,806 explicit missing facts.
- Current large-scale repository class: WDI annual scalar.

Important limitation: MacroForge artifacts contain broader evidence-only and bounded operational slices across many providers, but the current audited PostgreSQL production repository is WDI-only.

## Contract compatibility matrix

Classification vocabulary:

- Fully supported: MacroForge currently provides this requirement in a form KnowledgeForge can reference with little adaptation.
- Partially supported: MacroForge provides evidence, but KnowledgeForge needs an adapter, normalization, extra fingerprint, or scoping rule.
- Missing: MacroForge does not currently provide the requirement in a usable form.
- Architecturally incompatible: requirement conflicts with MacroForge's constitutional responsibility.

| KnowledgeForge v1 requirement | Status | Evidence | Architectural justification | Recommended remediation |
|---|---|---|---|---|
| Canonical identities | Partially supported | `curated.fact_observation` UUIDs; source, indicator, territory, period, unit, attribute-set dimensions; WDI source codes; annual periods; canonical territory codes. | MacroForge owns observational identity, not reusable semantic identity. This is the correct boundary. KnowledgeForge can reference MacroForge observational identities but must own claim/concept/package identities itself. | Create a read-only EvidenceRef convention: source_code + dataset_release_id + pipeline_run_id + indicator_id + territory_id + period_id + unit_id + attribute_set_id + as_of_date, plus fact row id when needed. |
| Evidence references | Partially supported | `meta.dataset_release.raw_artifact_path`, `raw_sha256`, `source_url`; `meta.pipeline_run.artifact_manifest`; normalized artifact paths in load reports. | Evidence exists, but not as KnowledgeForge `evidence_ref_id` objects with source family, evaluation status, and package-scoped reproducibility handles. | Superseded by sovereignty correction: build a KnowledgeForge-owned Source Evidence Package v1 real-fixture replay validation slice before production generation. |
| Source identities | Fully supported for current PostgreSQL scope | `meta.source` contains WDI source code/name/home URL/license note. | WDI source identity is explicit and stable enough for WDI-backed packages. | Preserve MacroForge source IDs and source code in every KnowledgeForge evidence reference. |
| Lineage | Partially supported | `meta.pipeline_run`, `meta.dataset_release`, `meta.lineage_event`; load reports; raw-to-staging and staging-to-curated event types. | MacroForge has lineage structure, but lineage events have null `checksum_sha256` in current audited rows, details are generic, and revision/vintage lineage remains unvalidated at repository scale. | Evidence adapter should combine `pipeline_run`, dataset release, raw artifact manifest hashes, normalized artifact path, load report, and quality checks into a KnowledgeForge lineage envelope. |
| Provenance | Partially supported | Source table, dataset releases, pipeline runs, input parameters, artifact manifests, raw artifact hashes, load reports, source metadata with WDI `lastupdated`. | MacroForge provenance is operational rather than KnowledgeForge-package-shaped. This is not a flaw; KnowledgeForge must not force MacroForge to own KnowledgeForge package envelopes. | Assemble KnowledgeForge provenance envelopes downstream without mutating MacroForge. |
| Fingerprints | Partially supported | Raw artifact SHA-256 values, `raw_sha256`, observed package fingerprinting code, `package_fingerprint` in the WDI trade-balance capability package. | MacroForge fingerprints inputs/artifacts in several places, but not all v1 targets: query definitions, computation recipes, generated statements, package manifests, and validation reports. | Add KnowledgeForge-side manifest/query/recipe/package fingerprinting in the production adapter. Do not require MacroForge schema changes. |
| Query definitions | Partially supported | Pipeline `input_parameters` include countries, indicators, date ranges; artifact manifests include exact WDI URLs. | Query evidence exists for WDI API retrieval, but downstream PostgreSQL query definitions for KnowledgeForge extraction are not separately normalized or fingerprinted. | Store read-only query specs as KnowledgeForge package inputs and fingerprint normalized SQL/query parameters. |
| Reproducibility metadata | Partially supported | Raw paths, raw hashes, artifact manifests, load reports, input parameters, source URLs, normalized paths. | Current data is replayable/auditable, but replay commands and package-level reproducibility states are not standardized for KnowledgeForge. | Create per-package replay instructions and classify reproducibility state (`reproducible` or `replayable-with-external-dependency`). |
| Freshness metadata | Partially supported | `as_of_date`; WDI `source_metadata.lastupdated`; release keys like `WDI:2026-07-01:1990:2024`; pipeline run dates. | Freshness is present but distributed. `meta.dataset_release.release_date` is null in current rows. | Derive freshness from WDI `lastupdated`, release key, pipeline run date, and as-of date; mark missing release_date as an adapter warning, not a blocker for WDI if source metadata is present. |
| Missingness metadata | Partially supported | `curated.fact_observation.observation_status` has `observed` and `missing`; load reports record observed/missing counts; WDI trade balance package records missing indicators per country-year. | Missingness is explicit at observation level and stronger than many upstream systems, but KnowledgeForge requires package-level missingness summaries and method-scoped missingness interpretation. | Generate deterministic missingness profiles per evidence slice/package. |
| Update/version history | Partially supported | 8 pipeline runs, rerun keys, as-of dates, release keys, load reports. | Good enough for WDI load history. Not yet enough for revision-aware knowledge evolution or multiple valid vintages of the same period at scale. | Use current WDI as single-current-release evidence. Defer revision-aware production packages until MacroForge TASK-182-style evidence exists. |
| Evidence family classification | Partially supported | Source code WDI and artifact/run context identify official statistical source data and MacroForge canonical observation packages. | MacroForge does not use KnowledgeForge's evidence-family vocabulary because it should not own KnowledgeForge semantics. | Map MacroForge evidence to KnowledgeForge classes downstream: `macroforge_canonical_data`, `macroforge_metadata`, `macroforge_lineage_provenance`, and official statistical metadata where present. |
| Dataset contracts | Partially supported | `ObservedIngestionPackage` v1; PostgreSQL schema constraints; WDI loader/load reports; source-specific raw artifact manifests. | Strong for WDI annual-scalar observed/canonical facts. Not proven for all repository classes. | First production campaign should stay inside WDI annual-scalar confidence cell. |
| Schema stability | Partially supported | Current schema supports meta/staging/curated, annual periods, canonical territory, source/provider mappings, attributes JSON, fact grain uniqueness. | Stable for WDI annual-scalar and scalar numeric facts; unvalidated for revision/vintage, relationship/matrix roles, event identity, and company/entity contexts. | Do not choose first campaign requiring revision/vintage, relationship, event, company, matrix, or non-scalar identity. |
| Validation outputs | Partially supported | `meta.quality_check`; load reports; idempotent rerun reports; ProjectForge task reports. | Validation exists but is MacroForge-operational, not KnowledgeForge-package validation. One historical `task-174` quality row remains failed due overlapping-load semantics, while later campaigns and state show corrected run-scoped validation. | Production adapter should include only latest relevant passing run-scoped validation outputs and explicitly record known historical validation caveats. |

## Compatibility implications

### What is production-ready enough

KnowledgeForge can safely use MacroForge as evidence for bounded WDI annual-scalar knowledge if it first implements a read-only adapter/exporter that creates v1-shaped evidence references, query fingerprints, missingness summaries, package fingerprints, and validation-state records.

### What is not production-ready

KnowledgeForge should not begin with:

- revision/vintage-aware claims;
- non-WDI cross-provider comparison claims;
- company/entity claims;
- matrix/input-output claims;
- event claims;
- broad relationship/causal/interpretive claims;
- knowledge requiring source ontology not already represented in MacroForge.

### Boundary conclusion

No architectural incompatibility was found between MacroForge and KnowledgeForge. The correct architecture is adapter-mediated: MacroForge remains the source-of-record for observations and observational lineage; KnowledgeForge owns evidence references, evaluations, packages, confidence, uncertainty, contradictions, lifecycle, and reusable knowledge statements.
