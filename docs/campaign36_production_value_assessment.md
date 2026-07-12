# Campaign 36 Production-Value Assessment

Outcome: A — Successful correlation pilot.

- total repository objects: 526
- substantive statistical-summary objects: 4
- substantive correlation objects: 1
- Campaign 36 substantive objects produced: 1
- evidence fixtures: Campaign 34 population fixture, Campaign 35 Nordic exports-share fixture, Campaign 36 dual-series exports/imports correlation fixture
- deterministic calculations in Campaign 36: raw Pearson correlation, exports-vs-time diagnostic, imports-vs-time diagnostic, first-difference diagnostic, independent recomputation
- PostgreSQL publication result: valid; canonical/projected count 526; retrieval by package ID, evidence family, statement type, lifecycle, package fingerprint, and provenance lineage passed
- governance artifacts counted for Campaign 36 before final verification: 13
- governance artifacts per substantive Campaign 36 object: 13.0
- offline reproducibility: validated from retained raw bytes/normalized fixture by Campaign 36 rerun
- local-AI result: failed — current qwen3:4b local route unsuitable for this screening task under bounded timeout
- downstream retrieval readiness: validated through PostgreSQL v1 package/family/statement/lifecycle/fingerprint/provenance retrieval
- metadata-heavy drift: improved; one substantive object promoted, diagnostics/reports not promoted as Knowledge Objects

Counted governance/support artifacts:
- artifacts/decisions/D-20260710-campaign36-dnk-exports-imports-share-pearson-correlation.md
- artifacts/evidence-fixtures/campaign36-wdi-dnk-exports-imports-share-correlation-1990-2024-https/alignment_contract_and_result.json
- artifacts/evidence-fixtures/campaign36-wdi-dnk-exports-imports-share-correlation-1990-2024-https/exports_normalized_series.json
- artifacts/evidence-fixtures/campaign36-wdi-dnk-exports-imports-share-correlation-1990-2024-https/imports_normalized_series.json
- artifacts/evidence-fixtures/campaign36-wdi-dnk-exports-imports-share-correlation-1990-2024-https/raw_fixture_manifest.json
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/calculation_evidence.json
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/campaign36_report.md
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/candidate_package.json
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/local_ai_retry.json
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/non_promoted_diagnostics.json
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/ollama_list_after_retry.txt
- artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/repository_promotion_result.json
- artifacts/tasks/T-20260710-campaign36-dnk-exports-imports-share-pearson-correlation.md
