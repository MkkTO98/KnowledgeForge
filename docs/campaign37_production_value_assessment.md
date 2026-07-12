# Campaign 37 Production-Value Assessment

Outcome: A.

Campaign 37 accepted both entity candidates and promoted two correlation KnowledgeObjectPackages from one consolidated fixture and one consolidated campaign report.

- repository objects: 528
- statistical-summary objects: 4
- correlation objects: 3
- accepted candidates: 2
- rejected candidates: 0
- governance/support artifacts counted: 18
- governance/support artifacts per accepted package: 9.0
- Campaign 36 baseline: 13.0
- PostgreSQL: valid, no schema/index pressure
- local AI: deferred, not retried

Counted support/governance artifacts:
- artifacts/decisions/D-20260710-campaign37-swe-nor-exports-imports-share-correlation-replication.md
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/nor_alignment_contract_and_result.json
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/nor_exports_normalized_series.json
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/nor_imports_normalized_series.json
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/raw_fixture_manifest.json
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/swe_alignment_contract_and_result.json
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/swe_exports_normalized_series.json
- artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https/swe_imports_normalized_series.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/campaign37_report.md
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/candidate_judgments.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/nor_calculation_evidence.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/nor_candidate_package.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/nor_non_promoted_diagnostics.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/repository_promotion_result.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/swe_calculation_evidence.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/swe_candidate_package.json
- artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/swe_non_promoted_diagnostics.json
- artifacts/tasks/T-20260710-campaign37-swe-nor-exports-imports-share-correlation-replication.md

Assessment: governance overhead fell below Campaign 36's first-method baseline if both packages are accepted. Scaling is not operationally blocked by this measured ratio, but the next step should vary semantic pair rather than repeat exports/imports across more countries.
