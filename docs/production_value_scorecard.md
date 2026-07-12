# Production-Value Scorecard

```json
{
  "after_campaign": "Campaign 35",
  "campaign35_accepted_candidates": 3,
  "campaign35_evidence_fixture": "campaign35-wdi-nordic-exports-share-1990-2024-https",
  "campaign35_rejected_candidates": 0,
  "campaign35_substantive_numerical_objects_produced": 3,
  "date": "2026-07-10",
  "deterministic_calculations_executed_campaign35": 3,
  "downstream_retrieval_readiness": "validated through PostgreSQL lookup, family filter, statement-type filter, lifecycle filter, and provenance lineage retrieval for Campaign 35 packages",
  "frontier_model_usage": "none for numerical production; local model experiment attempted and failed non-blockingly",
  "governance_artifact_count_policy": "campaign-specific non-substantive artifact files excluding raw provider response byte files, canonical package JSONs, repository indexes, and final verification logs",
  "governance_artifacts_per_substantive_object_campaign35": 5.333333333333333,
  "local_ai_experiment": {
    "disposition": "No model finding is authoritative; deterministic package validators passed. Treat model output as advisory screen only.",
    "model": "qwen3:4b",
    "saved_effort_assessment": "low; useful as a quick wording screen but added operational overhead for three short packages",
    "status": "failed"
  },
  "metadata_heavy_drift_assessment": "improved: Campaign 35 added three substantive numerical packages and no metadata KnowledgeObjects merely to inflate count",
  "offline_reproducibility": "validated by retained raw fixture and normalized fixture; final verification reruns offline regeneration",
  "postgresql_projected_object_count": 525,
  "postgresql_projection_id": "sha256:fcb0cbdea757746fae8e7d9884f24b64af5f1599f6074554f3b97299ff8187bd",
  "postgresql_publication_result": "valid",
  "repository_fingerprint": "sha256:257d003fba6800cecef6f7d4750875ce79811955d892e13c176d79316f94c9fd",
  "statistical_summary_evidence_fixtures_covered_total": 2,
  "substantive_numerical_statistical_summary_objects_total": 4,
  "total_canonical_objects": 525
}
```


## Campaign 36 — DNK exports/imports share Pearson correlation

- outcome: A — Successful correlation pilot
- total repository objects: 526
- substantive statistical-summary objects: 4
- substantive correlation objects: 1
- Campaign 36 substantive objects produced: 1
- Pearson coefficient: 0.988873850642
- aligned pairs: 35
- evidence fixture: `artifacts/evidence-fixtures/campaign36-wdi-dnk-exports-imports-share-correlation-1990-2024-https/`
- deterministic calculations: raw Pearson, independent recomputation, two time-index diagnostics, first-difference sensitivity diagnostic
- PostgreSQL publication: valid; canonical/projected count 526 and required retrieval checks passed
- governance artifacts per substantive object: 13.0
- offline reproducibility: validated by `python3 tools/run_campaign36_dnk_exports_imports_correlation.py --reuse-fixture --no-promote`
- local-AI result: failed; qwen3:4b timed out under bounded route and is classified unsuitable for this screening task until routing/model-serving evidence changes
- downstream retrieval readiness: PostgreSQL v1 JSONB projection and required retrieval checks passed
- metadata-heavy drift: improved relative to metadata-heavy phases; one substantive relationship object promoted, diagnostics not promoted


## Campaign 37 — SWE/NOR exports/imports share Pearson correlation replication

- outcome: A — Successful controlled replication
- total repository objects: 528
- substantive statistical-summary objects: 4
- substantive correlation objects: 3
- Campaign 37 accepted candidates: 2
- Campaign 37 rejected candidates: 0
- coefficients: SWE `0.968490740983`, NOR `-0.477418804478`
- evidence fixture: `artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/`
- deterministic calculations: per entity raw Pearson, independent recomputation, two time-index diagnostics, first-difference sensitivity diagnostic
- governance/support artifacts per substantive object: 18 / 2 = 9.0
- Campaign 36 governance baseline: 13 / 1 = 13.0
- PostgreSQL publication: valid; canonical/projected count 528; family query returns Campaign 36 plus Campaign 37 packages
- offline reproducibility: validated by no-promote Campaign 37 rerun from retained fixture
- downstream retrieval readiness: validated through PostgreSQL v1 package/family/statement/lifecycle/fingerprint/provenance retrieval
- local-AI status: deferred; 45-second and 120-second qwen3:4b attempts previously failed and were not retried
- metadata-heavy drift: improved; two substantive relationship objects promoted from one consolidated fixture/report path, diagnostics not promoted


## Campaign 38 — semantically distinct WDI Pearson correlation pilot

- outcome: B — Successful with bounded operational pressure
- repository objects: 529
- statistical-summary objects: 4
- correlation objects: 4
- correlation pairs: exports/imports share; life expectancy/fertility
- domains represented: trade/external sector; demographic
- entities represented in correlation objects: DNK, SWE, NOR
- Campaign 38 accepted candidates: 1
- Campaign 38 rejected candidates: 0 after frozen selection; shortlist rejected/deferred alternatives recorded in selection decision
- coefficient: `-0.40932912178` (`-0.409329121780` fixed 12-decimal rendering)
- evidence fixture: `artifacts/evidence-fixtures/campaign38-wdi-dnk-life-expectancy-fertility-correlation-1990-2024-https/`
- deterministic calculations: raw Pearson, independent recomputation, time-index diagnostics, first-difference diagnostic
- governance/support artifacts per substantive object: 15 / 1 = 15.0
- Campaign 37 baseline: 9.0
- PostgreSQL status: valid; canonical/projected count 529; Campaign 36-37 correlation objects remain retrievable
- offline reproducibility: validated by no-promote rerun from retained fixture
- downstream retrieval readiness: validated through PostgreSQL v1 package/family/statement/lifecycle/fingerprint/provenance retrieval
- metadata-heavy drift: bounded; one object from one frozen selection/report/fixture path
- local-AI status: deferred; no retry


## Campaign 39 — small heterogeneous WDI Pearson correlation batch

- outcome: A — Successful heterogeneous batch
- repository objects: 532
- statistical-summary objects: 4
- correlation objects: 7
- distinct pairs: exports/imports share; life expectancy/fertility; DPT/measles immunization; birth/death rates; internet users/mobile subscriptions
- domains: trade/external sector, demographic, health, infrastructure
- entities: DNK, SWE, NOR
- accepted/rejected candidates: 3 accepted, 0 rejected after frozen selection
- governance ratio: 7.67:1
- PostgreSQL status: valid
- offline reproducibility: retained fixture/no-promote rerun
- downstream readiness: generic PostgreSQL retrieval valid
- local-AI status: deferred; no retry
