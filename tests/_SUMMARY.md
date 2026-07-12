# Folder Summary: tests

## Purpose
Project tests, including Vertical Slice 0 invariant coverage and Validation Framework v1 synthetic fixture coverage.

## Contains
<!-- PROJECTFORGE:BEGIN-CONTAINS -->
- `fixtures/`
- `invariants/`
- `test_campaign0_repository_evidence.py`
- `test_campaign10_cross_campaign_recurrence_audit.py`
- `test_campaign11_wdi_environment_maturation.py`
- `test_campaign12_wdi_environment_provenance_lineage_closeout.py`
- `test_campaign13_wdi_infrastructure_transfer.py`
- `test_campaign14_wdi_infrastructure_maturation.py`
- `test_campaign15_wdi_infrastructure_provenance_lineage_closeout.py`
- `test_campaign16_wdi_energy_mining_transfer.py`
- `test_campaign17_wdi_energy_mining_maturation.py`
- `test_campaign18_wdi_energy_mining_provenance_lineage_closeout.py`
- `test_campaign19_wdi_agriculture_rural_development_transfer.py`
- `test_campaign1_wdi_demographic_evidence.py`
- `test_campaign20_wdi_agriculture_rural_development_maturation.py`
- `test_campaign21_wdi_agriculture_rural_development_provenance_lineage_closeout.py`
- `test_campaign22_wdi_health_transfer.py`
- `test_campaign23_wdi_health_maturation.py`
- `test_campaign24_wdi_health_provenance_lineage_closeout.py`
- `test_campaign25_wdi_education_transfer.py`
- `test_campaign26_wdi_education_maturation.py`
- `test_campaign27_wdi_education_provenance_lineage_closeout.py`
- `test_campaign28_wdi_trade_transfer.py`
- `test_campaign29_wdi_trade_maturation.py`
- `test_campaign2_wdi_completeness_buckets.py`
- `test_campaign30_wdi_trade_provenance_lineage_closeout.py`
- `test_campaign31_wdi_financial_sector_transfer.py`
- `test_campaign32_wdi_financial_sector_maturation.py`
- `test_campaign33_wdi_financial_sector_provenance_lineage_closeout.py`
- `test_campaign34_decimal_context_evaluation.py`
- `test_campaign34_wdi_denmark_population_statistical_summary.py`
- `test_campaign35_wdi_nordic_exports_statistical_summary.py`
- `test_campaign36_dnk_exports_imports_correlation.py`
- `test_campaign37_swe_nor_exports_imports_correlation.py`
- `test_campaign38_semantically_distinct_correlation.py`
- `test_campaign39_heterogeneous_correlation_batch.py`
- `test_campaign3_wdi_freshness_metadata.py`
- `test_campaign42_first_difference_companion_production.py`
- `test_campaign42_first_difference_companion_registry.py`
- `test_campaign43_first_difference_companion_registry.py`
- `test_campaign4_wdi_indicator_inventory.py`
- `test_campaign5_wdi_territorial_coverage.py`
- `test_campaign6_wdi_temporal_coverage.py`
- `test_campaign7_wdi_provenance_lineage.py`
- `test_campaign8_wdi_environment_transfer.py`
- `test_campaign9_wdi_cross_family_comparison.py`
- `test_canonical_supersession_immutability_validator.py`
- `test_coefficient_free_pearson_candidate_registry.py`
- `test_correlation_batch_engine.py`
- `test_correlation_engine_provenance_parameterization.py`
- `test_external_outbox_polling_supersession_v1.py`
- `test_first_difference_pearson_method.py`
- `test_knowledge_repository.py`
- `test_macroforge_neutral_release_adapter_v1.py`
- `test_operational_state_checkpoint.py`
- `test_package_construction_validation_v1.py`
- `test_pearson_correlation_v1.py`
- `test_postgresql_operational_projection.py`
- `test_postgresql_realization_decision.py`
- `test_production_support.py`
- `test_relationship_export_v1.py`
- `test_release_automation_alignment_v1.py`
- `test_release_inbox_real_evidence_v1.py`
- `test_repository_scale_doctrine_review.py`
- `test_statistical_summary_v2.py`
- `test_validation_framework_v1.py`
- `test_vertical_slice_0.py`
- `test_wdi_family_maturity_registry.py`
- `test_wdi_observation_evidence_fixture.py`
- `test_wdi_unit_resolution.py`
<!-- PROJECTFORGE:END-CONTAINS -->

## Active Work
- `test_validation_framework_v1.py` verifies positive and negative synthetic fixtures for all five pre-production validation stages.
- `test_vertical_slice_0.py` verifies the approved four-object ecosystem plus negative invariant cases.

## Needs Attention
- Future MacroForge compatibility tests should remain audit/fixture-backed until production generation is explicitly approved.

- `test_correlation_batch_engine.py` — historical spec reproduction plus Campaign 40 freeze, acquisition contract, rejection isolation, atomic publication, and stale-PostgreSQL safeguards.
- `test_relationship_export_v1.py` — export contract validation, consumer independence, tamper detection, stale-projection failure, malformed-query rejection, SQL-injection literal handling, and bounded-result enforcement.
- `test_release_automation_alignment_v1.py` — synthetic release contract, exact change detection, derivation-impact, and boundary-preservation tests.
- `test_campaign43_first_difference_companion_registry.py` — verifies the six-candidate Campaign 43 boundary, raw package/fingerprint resolution, non-supersession, no existing companion, method/transformation references, coefficient-free enforcement, deterministic/idempotent generation, and unchanged canonical count/fingerprint.
