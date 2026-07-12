--
-- PostgreSQL database dump
--

\restrict EOIQsECOe3SrhmrR8gXcxgcW8wkedUxW2LelBiGgIhTjYp4NAgK5TPWsicDXtcV

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: immutability_gate; Type: SCHEMA; Schema: -; Owner: mkkto
--

CREATE SCHEMA immutability_gate;


ALTER SCHEMA immutability_gate OWNER TO mkkto;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: immutable_packages; Type: TABLE; Schema: immutability_gate; Owner: mkkto
--

CREATE TABLE immutability_gate.immutable_packages (
    package_id text NOT NULL,
    package_sha256 text NOT NULL,
    payload jsonb NOT NULL
);


ALTER TABLE immutability_gate.immutable_packages OWNER TO mkkto;

--
-- Name: package_current_state; Type: TABLE; Schema: immutability_gate; Owner: mkkto
--

CREATE TABLE immutability_gate.package_current_state (
    package_id text NOT NULL,
    lifecycle_state text NOT NULL,
    is_current boolean NOT NULL,
    superseded_by text
);


ALTER TABLE immutability_gate.package_current_state OWNER TO mkkto;

--
-- Data for Name: immutable_packages; Type: TABLE DATA; Schema: immutability_gate; Owner: mkkto
--

COPY immutability_gate.immutable_packages (package_id, package_sha256, payload) FROM stdin;
pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1	8330693f4aa639f4bc8e38a6409679b44f41c40ac6a5e11a0c07a1ab61e8467e	{"scope": {"domain": "world_development_indicators", "entity_scope": ["DNK"], "period_scope": {"end": 2024, "start": 1990}, "evidence_family": "external_wdi_annual_scalar_trade_pearson_correlation"}, "status": "accepted", "lineage": {"source_campaign": "Campaign 36", "version_lineage": [], "previous_package_id": null}, "created_at": "2026-07-10", "created_by": "run_campaign36_dnk_exports_imports_correlation", "package_id": "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1", "fingerprints": {"input_set": "sha256:dd9a2ab5863ae2a70ec411e7e0e0cb012748524e705f5e4d7e507436397055bf", "package_manifest": "sha256:6a42d69696af4682113f790a065aa9bed22b181f21fbf728e40a0d5285d45842", "query_definitions": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945", "computation_recipe": "sha256:eec09fa6d2efbda5500c16e058d16f8ac83aa802a008b48e619697ad569bcc5e", "evidence_references": "sha256:51d3ae190d5facc9a6006d7038b3d4722517632f64c55937abe9a32f6369aff5", "generated_statements": "sha256:cb13eafc26ab41643a306fbc3e8d1e7e4dfe20314dc7a3f01258d7785ab1b63c"}, "package_kind": "KnowledgeObjectPackage", "package_version": "1.0", "input_references": ["campaign36_dual_series_wdi_https_fixture", "pearson_correlation_calculation_contract_v1"], "validation_state": {"blockers": [], "warnings": ["shared GDP denominator", "economic flow co-movement possible", "no causal/predictive/significance interpretation"], "validation_result": "pass"}, "confidence_quality": {"lifecycle_state": "accepted", "confidence_label": "fixture-supported-deterministic", "validation_state": "pass", "missingness_summary": "0 missing/excluded pairs of 35 expected periods", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation", "reproducibility_state": "reproducible_offline_from_retained_fixture", "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "shared_gdp_denominator", "time_ordering_autocorrelation", "structural_breaks", "no_significance_or_causal_claim"]}, "evidence_integrity": {"fingerprints_verified": true, "evidence_refs_verified": true, "source_package_fingerprint": "sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f"}, "evolution_metadata": {"change_reason": "Campaign 36 first bounded production correlation pilot", "previous_revision": null, "dependent_object_review_posture": "not_applicable", "changed_inputs_methods_templates_models_validators": ["wdi_annual_scalar_pearson_correlation_v1"]}, "evidence_references": [{"accessed_at": "2026-07-10", "source_owner": "World Bank WDI API retained local fixture", "source_family": "official_statistical_source_data", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "source_version": "2026-07-01", "evidence_ref_id": "ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture", "source_identity": "World Bank WDI NE.EXP.GNFS.ZS and NE.IMP.GNFS.ZS DNK annual 1990-2024 fixture", "evaluation_status": "evaluated", "snapshot_fingerprint": "sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f", "reproducibility_handle": "retained HTTPS raw fixture, normalized series, alignment contract, and calculation evidence"}], "provenance_envelope": {"method_refs": ["wdi_annual_scalar_pearson_correlation_v1@1.0"], "evidence_refs": ["ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture"], "lineage_basis": "fresh Campaign 36 HTTPS acquisition; Campaign 35 observations not reused as substitute", "evaluation_refs": ["campaign36_alignment_validation", "campaign36_calculation_evidence", "campaign36_non_promoted_diagnostics"]}, "generated_statements": [{"text": "Across the aligned annual DNK observations from 1990 through 2024, the Pearson correlation between exports of goods and services as a percentage of GDP and imports of goods and services as a percentage of GDP is 0.988873850642, using 35 aligned observations.", "origin": "computed_from_retained_dual_series_wdi_fixture", "dependencies": ["calc-campaign36-pearson-correlation-v1", "align-campaign36-dnk-exports-imports-share"], "statement_id": "stmt-campaign36-dnk-exports-imports-share-pearson-correlation-v1", "applicability": {"entity_id": "DNK", "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "period_end": 2024, "period_start": 1990, "method_version": "1.0"}, "evidence_refs": ["ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture"], "statement_type": "derived_relationship", "structured_payload": {"series_a": {"code": "NE.EXP.GNFS.ZS", "name": "Exports of goods and services (% of GDP)", "unit": "percent of GDP", "definition": "Exports of goods includes changes in the economic ownership of goods from residents of the compiling economy to non-residents, irrespective of physical movement of goods across national borders. Exports of services includes services provided by residents to non-residents. This indicator is expressed as a percentage of Gross Domestic Product (GDP) which is the total income earned through the production of goods and services in an economic territory during an accounting period.", "raw_fingerprints": {"metadata": "sha256:57dae5fa8dbd577b2cff50f9cfe581b3273ecdaa1125c4188164ef9a3cdddff4", "observations": "sha256:1217c3b6dbd7656137cf76cf7f39746e8fffd293315e4cf42ee5554214d76f3a"}, "normalized_fingerprint": "sha256:afbc4de1619498ee6716c48f1d53b4591971c54f9cd9b7b0162dee951ac9986b"}, "series_b": {"code": "NE.IMP.GNFS.ZS", "name": "Imports of goods and services (% of GDP)", "unit": "percent of GDP", "definition": "Imports of goods includes change in the economic ownership of goods from non-residents to\\n\\n\\n\\n\\nresidents of the compiling economy, irrespective of physical movement of goods across national borders. Imports of services includes services provided by non-residents to residents. This indicator is expressed as a percentage of Gross Domestic Product (GDP) which is the total income earned through the production of goods and services in an economic territory during an accounting period.", "raw_fingerprints": {"metadata": "sha256:a6e803f45b0ecfabb89dfa448350c47e4994f543f62f46d2060362b91853eb75", "observations": "sha256:e5700dd43c368020283a03b72146e998303e1111d71441b4610a815619ed4a67"}, "normalized_fingerprint": "sha256:aa45c162c20c317dd183018ff190fab402270c5b41b3f38dfad7dc953d54a0a3"}, "entity_id": "DNK", "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "entity_name": "Denmark", "limitations": {"non_causality": "The coefficient is a deterministic contemporaneous mathematical relationship only and is not a causal, predictive, statistical-significance, economic-significance, investment, trend, stationarity, or mechanism claim.", "structural_breaks": "The coefficient is scoped only to the retained 1990-2024 aligned window and may not hold across structural breaks.", "shared_gdp_denominator": "Both indicators use GDP as denominator, so correlation may partly reflect shared-denominator movement.", "time_ordering_autocorrelation": "Annual macroeconomic series can exhibit time ordering/autocorrelation; no stationarity or independence claim is made."}, "period_scope": {"end": 2024, "start": 1990}, "method_version": "1.0", "aligned_periods": [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], "aligned_coverage": "1", "excluded_periods": [], "provider_metadata": {"exports": {"source": "World Development Indicators", "dataset": "World Development Indicators", "provider": "World Bank", "sourceid": "2", "wdi_lastupdated": "2026-07-01"}, "imports": {"source": "World Development Indicators", "dataset": "World Development Indicators", "provider": "World Bank", "sourceid": "2", "wdi_lastupdated": "2026-07-01"}}, "aligned_pair_count": 35, "missing_pair_count": 0, "package_fingerprint": "sha256:d717f394fe4998adb3b0abd3639c6d6ae9fafc6c3fbe850b8f1719d71d81f8b5", "pearson_coefficient": {"unit": "dimensionless", "canonical": "0.988873850642"}, "validation_judgment": "accepted_one_bounded_correlation_object", "transformation_state": {"series_a": "raw", "series_b": "raw"}, "selection_fingerprint": "sha256:83b19470d2c7dfde5a17d66ce32f6867285539afeae9bd4bf30fe9d9ec5648a4", "canonical_pair_identity": "sha256:4f132f3e9cbe36737d994c12257610b20b4e1b13b7da2d9bc1fae8da4ffee6d5", "mutable_source_limitation": "Retained bytes, not mutable WDI API reacquisition, provide exact historical reproducibility.", "method_contract_fingerprint": "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476", "calculation_evidence_fingerprint": "sha256:e43f4350e99e73e0557cba370bcd35e4ea3d22d88211d125a37695dafac67033", "combined_raw_evidence_fingerprint": "sha256:bd1fffa81ce48a306ea3ed0a0493ae08ce0a41064e21397241beefe1d7b9a560", "combined_aligned_evidence_fingerprint": "sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f"}}], "contradiction_records": [{"disposition": "not_applicable", "contradiction_id": "none-recorded", "target_statement": "stmt-campaign36-dnk-exports-imports-share-pearson-correlation-v1", "contradiction_type": "none", "contradicting_evidence": null}]}
pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2	93bcdacb16e02ee3ba4c9fcd10c4c802fb735c1ddeba0de65371381c21c66d7d	{"scope": {"domain": "world_development_indicators", "entity_scope": ["DNK"], "period_scope": {"end": 2024, "start": 1990}, "evidence_family": "external_wdi_annual_scalar_trade_pearson_correlation"}, "status": "accepted", "lineage": {"source_campaign": "Campaign 36", "version_lineage": [], "previous_package_id": null}, "created_at": "2026-07-11", "created_by": "canonical_supersession_immutability_validator_controlled_fixture", "package_id": "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2", "limitations": ["controlled_test_successor_not_provider_evidence", "not production canonical knowledge"], "fingerprints": {"input_set": "sha256:dd9a2ab5863ae2a70ec411e7e0e0cb012748524e705f5e4d7e507436397055bf", "package_manifest": "sha256:275ff652fd5f067268378a701bea9f477b45b3ac4c654deb64996b95e740bf90", "query_definitions": "sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945", "computation_recipe": "sha256:eec09fa6d2efbda5500c16e058d16f8ac83aa802a008b48e619697ad569bcc5e", "evidence_references": "sha256:51d3ae190d5facc9a6006d7038b3d4722517632f64c55937abe9a32f6369aff5", "generated_statements": "sha256:cb13eafc26ab41643a306fbc3e8d1e7e4dfe20314dc7a3f01258d7785ab1b63c"}, "package_kind": "KnowledgeObjectPackage", "package_version": "1.0", "input_references": ["campaign36_dual_series_wdi_https_fixture", "pearson_correlation_calculation_contract_v1"], "validation_state": {"blockers": [], "warnings": ["shared GDP denominator", "economic flow co-movement possible", "no causal/predictive/significance interpretation"], "validation_result": "pass"}, "confidence_quality": {"lifecycle_state": "accepted", "confidence_label": "fixture-supported-deterministic", "validation_state": "pass", "missingness_summary": "0 missing/excluded pairs of 35 expected periods", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation", "reproducibility_state": "reproducible_offline_from_retained_fixture", "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "shared_gdp_denominator", "time_ordering_autocorrelation", "structural_breaks", "no_significance_or_causal_claim"]}, "evidence_integrity": {"fingerprints_verified": true, "evidence_refs_verified": true, "source_package_fingerprint": "sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f"}, "evolution_metadata": {"change_reason": "controlled_test_successor_not_provider_evidence: evidence release change with appended DNK period and revised historical DNK observation", "previous_revision": "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1", "supersession_reason": "controlled evidence release change; not provider evidence", "changed_inputs_methods_templates_models_validators": ["controlled_test_successor_not_provider_evidence"]}, "evidence_references": [{"accessed_at": "2026-07-10", "source_owner": "World Bank WDI API retained local fixture", "source_family": "official_statistical_source_data", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "source_version": "2026-07-01", "evidence_ref_id": "ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture", "source_identity": "World Bank WDI NE.EXP.GNFS.ZS and NE.IMP.GNFS.ZS DNK annual 1990-2024 fixture", "evaluation_status": "evaluated", "snapshot_fingerprint": "sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f", "reproducibility_handle": "retained HTTPS raw fixture, normalized series, alignment contract, and calculation evidence"}], "provenance_envelope": {"method_refs": ["wdi_annual_scalar_pearson_correlation_v1@1.0"], "evidence_refs": ["ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture"], "lineage_basis": "fresh Campaign 36 HTTPS acquisition; Campaign 35 observations not reused as substitute", "evaluation_refs": ["campaign36_alignment_validation", "campaign36_calculation_evidence", "campaign36_non_promoted_diagnostics"]}, "generated_statements": [{"text": "Across the aligned annual DNK observations from 1990 through 2024, the Pearson correlation between exports of goods and services as a percentage of GDP and imports of goods and services as a percentage of GDP is 0.988873850642, using 35 aligned observations.", "origin": "computed_from_retained_dual_series_wdi_fixture", "dependencies": ["calc-campaign36-pearson-correlation-v1", "align-campaign36-dnk-exports-imports-share"], "statement_id": "stmt-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2", "applicability": {"entity_id": "DNK", "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "period_end": 2024, "period_start": 1990, "method_version": "1.0"}, "evidence_refs": ["ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture"], "statement_type": "derived_relationship", "structured_payload": {"series_a": {"code": "NE.EXP.GNFS.ZS", "name": "Exports of goods and services (% of GDP)", "unit": "percent of GDP", "definition": "Exports of goods includes changes in the economic ownership of goods from residents of the compiling economy to non-residents, irrespective of physical movement of goods across national borders. Exports of services includes services provided by residents to non-residents. This indicator is expressed as a percentage of Gross Domestic Product (GDP) which is the total income earned through the production of goods and services in an economic territory during an accounting period.", "raw_fingerprints": {"metadata": "sha256:57dae5fa8dbd577b2cff50f9cfe581b3273ecdaa1125c4188164ef9a3cdddff4", "observations": "sha256:1217c3b6dbd7656137cf76cf7f39746e8fffd293315e4cf42ee5554214d76f3a"}, "normalized_fingerprint": "sha256:afbc4de1619498ee6716c48f1d53b4591971c54f9cd9b7b0162dee951ac9986b"}, "series_b": {"code": "NE.IMP.GNFS.ZS", "name": "Imports of goods and services (% of GDP)", "unit": "percent of GDP", "definition": "Imports of goods includes change in the economic ownership of goods from non-residents to\\n\\n\\n\\n\\nresidents of the compiling economy, irrespective of physical movement of goods across national borders. Imports of services includes services provided by non-residents to residents. This indicator is expressed as a percentage of Gross Domestic Product (GDP) which is the total income earned through the production of goods and services in an economic territory during an accounting period.", "raw_fingerprints": {"metadata": "sha256:a6e803f45b0ecfabb89dfa448350c47e4994f543f62f46d2060362b91853eb75", "observations": "sha256:e5700dd43c368020283a03b72146e998303e1111d71441b4610a815619ed4a67"}, "normalized_fingerprint": "sha256:aa45c162c20c317dd183018ff190fab402270c5b41b3f38dfad7dc953d54a0a3"}, "entity_id": "DNK", "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "entity_name": "Denmark", "limitations": {"non_causality": "The coefficient is a deterministic contemporaneous mathematical relationship only and is not a causal, predictive, statistical-significance, economic-significance, investment, trend, stationarity, or mechanism claim.", "structural_breaks": "The coefficient is scoped only to the retained 1990-2024 aligned window and may not hold across structural breaks.", "shared_gdp_denominator": "Both indicators use GDP as denominator, so correlation may partly reflect shared-denominator movement.", "time_ordering_autocorrelation": "Annual macroeconomic series can exhibit time ordering/autocorrelation; no stationarity or independence claim is made."}, "period_scope": {"end": 2024, "start": 1990}, "method_version": "1.0", "aligned_periods": [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025], "aligned_coverage": "1", "excluded_periods": [], "provider_metadata": {"exports": {"source": "World Development Indicators", "dataset": "World Development Indicators", "provider": "World Bank", "sourceid": "2", "wdi_lastupdated": "2026-07-01"}, "imports": {"source": "World Development Indicators", "dataset": "World Development Indicators", "provider": "World Bank", "sourceid": "2", "wdi_lastupdated": "2026-07-01"}}, "aligned_pair_count": 36, "missing_pair_count": 0, "package_fingerprint": "sha256:d717f394fe4998adb3b0abd3639c6d6ae9fafc6c3fbe850b8f1719d71d81f8b5", "pearson_coefficient": {"unit": "dimensionless", "canonical": "0.988873850642"}, "pearson_correlation": "0.997000000000000000", "validation_judgment": "accepted_one_bounded_correlation_object", "transformation_state": {"series_a": "raw", "series_b": "raw"}, "selection_fingerprint": "sha256:83b19470d2c7dfde5a17d66ce32f6867285539afeae9bd4bf30fe9d9ec5648a4", "canonical_pair_identity": "sha256:4f132f3e9cbe36737d994c12257610b20b4e1b13b7da2d9bc1fae8da4ffee6d5", "mutable_source_limitation": "Retained bytes, not mutable WDI API reacquisition, provide exact historical reproducibility.", "controlled_successor_notice": "controlled_test_successor_not_provider_evidence", "method_contract_fingerprint": "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476", "calculation_evidence_fingerprint": "sha256:e43f4350e99e73e0557cba370bcd35e4ea3d22d88211d125a37695dafac67033", "combined_raw_evidence_fingerprint": "sha256:bd1fffa81ce48a306ea3ed0a0493ae08ce0a41064e21397241beefe1d7b9a560", "combined_aligned_evidence_fingerprint": "sha256:a12b78bbfb39d38c4316a5b9bcc74bb1899cecb71134a1200fb851c62b1e8b0f"}}], "contradiction_records": [{"disposition": "not_applicable", "contradiction_id": "none-recorded", "target_statement": "stmt-campaign36-dnk-exports-imports-share-pearson-correlation-v1", "contradiction_type": "none", "contradicting_evidence": null}]}
\.


--
-- Data for Name: package_current_state; Type: TABLE DATA; Schema: immutability_gate; Owner: mkkto
--

COPY immutability_gate.package_current_state (package_id, lifecycle_state, is_current, superseded_by) FROM stdin;
pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1	superseded	f	pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2
pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2	current	t	\N
\.


--
-- Name: immutable_packages immutable_packages_pkey; Type: CONSTRAINT; Schema: immutability_gate; Owner: mkkto
--

ALTER TABLE ONLY immutability_gate.immutable_packages
    ADD CONSTRAINT immutable_packages_pkey PRIMARY KEY (package_id);


--
-- Name: package_current_state package_current_state_pkey; Type: CONSTRAINT; Schema: immutability_gate; Owner: mkkto
--

ALTER TABLE ONLY immutability_gate.package_current_state
    ADD CONSTRAINT package_current_state_pkey PRIMARY KEY (package_id);


--
-- Name: one_current_dnk; Type: INDEX; Schema: immutability_gate; Owner: mkkto
--

CREATE UNIQUE INDEX one_current_dnk ON immutability_gate.package_current_state USING btree (is_current) WHERE is_current;


--
-- Name: package_current_state package_current_state_package_id_fkey; Type: FK CONSTRAINT; Schema: immutability_gate; Owner: mkkto
--

ALTER TABLE ONLY immutability_gate.package_current_state
    ADD CONSTRAINT package_current_state_package_id_fkey FOREIGN KEY (package_id) REFERENCES immutability_gate.immutable_packages(package_id);


--
-- PostgreSQL database dump complete
--

\unrestrict EOIQsECOe3SrhmrR8gXcxgcW8wkedUxW2LelBiGgIhTjYp4NAgK5TPWsicDXtcV
