# Campaign 41 — Coefficient-Free Pearson Candidate Registry and Batch Specification

Decision: B — 8 structurally valid candidates are frozen; a bounded reusable Pearson-engine extension is required before calculation.

Important qualification: all 8 candidates are suitable only with strong non-promoted time-index diagnostics and explicit limitations. None is classified unsuitable, so no registry revision is required before the engine-extension task; but execution must not promote raw-level Pearson beyond bounded descriptive relationship objects.

## 1. Eligible retained evidence pool
- Root: `artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https`
- Retained validated series: 16
- Result-independent proposals after filters: 18
- Frozen candidates: 8
- Boundary: retained validated KnowledgeForge WDI annual-scalar fixture evidence only; no MacroForge runtime/private DB, no new acquisition, no coefficient/result cache.

## 2. Existing candidate-construction design found
- Campaigns 36–39 compatibility specs showed prior Pearson compatibility-gate structure.
- Campaign 40 registry/spec provided the reusable candidate metadata pattern, retained fixture layout, expected package-ID pattern, and spec-driven engine contract.
- `docs/pearson_correlation_method_v1.md` provided the accepted method family.
- `specs/release_automation/real_derivation_applicability_registry_v1.json` provided derivation applicability boundaries.

## 3. New reusable tooling necessity
- Necessary: yes, limited helper only.
- Added `tools/coefficient_free_pearson_candidate_registry.py` because existing tooling could validate/run specs but did not enumerate retained eligible series, exclude prior pairs, freeze deterministic candidates, emit fingerprints, and prove coefficient-free construction without calculation.
- Added `tests/test_coefficient_free_pearson_candidate_registry.py`.

## 4. Deterministic selection policy
- canonical_ordering_rules:
  - group by entity order DNK, NOR, SWE
  - within entity sort by canonical series order: family, indicator code, indicator name
  - canonicalize pair side ordering by family, indicator code, indicator name
- compatibility_filters:
  - same entity
  - annual frequency
  - raw transformation
  - resolved units
  - at least 30 aligned observed annual pairs
  - at least 0.85 aligned coverage
- diversity_rules:
  - round-robin across DNK/NOR/SWE
  - maximum three candidates per entity
  - maximum two uses of the same indicator per entity before deterministic relaxation
  - prefer cross-family retained pairs when available
- duplicate_removal: remove self-pairs and duplicate/reversed entity-indicator pairs before selection
- eligible_evidence_pool: artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https
- maximum_candidate_count: 8
- outcome_values_used: False
- pool_rule: retained validated Campaign 40 WDI annual-scalar individual-series fixtures only
- prior_relationship_exclusion: exclude relationships already canonicalized or frozen/rejected in Campaigns 36-40 with same entity/scope/transformation
- semantic_risk_filters:
  - exclude direct arithmetic identities
  - exclude direct component-total relationships
  - exclude near-duplicate indicator definitions
  - exclude candidates requiring interpretive/causal/forecast/investment justification
- tie_breaking_rules:
  - entity order
  - series_a indicator code
  - series_b indicator code
  - candidate_id lexical order

## 5. Frozen registry
1. `dnk_agricultural_land_broad_money`
   - expected package: `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1`
   - entity/period: DNK 1990-2024; aligned pairs 34/35; coverage 0.9714285714285714
   - A: AG.LND.AGRI.ZS — Agricultural land (% of land area); unit `% of land area`; transformation `raw`
   - B: FM.LBL.BMNY.GD.ZS — Broad money (% of GDP); unit `percent of GDP`; transformation `raw`
2. `nor_fossil_electricity_under5_mortality`
   - expected package: `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1`
   - entity/period: NOR 1990-2024; aligned pairs 34/35; coverage 0.9714285714285714
   - A: EG.ELC.FOSL.ZS — Electricity production from oil, gas and coal sources (% of total); unit `% of total`; transformation `raw`
   - B: SH.DYN.MORT — Mortality rate, under-5 (per 1,000 live births); unit `per 1,000 live births`; transformation `raw`
3. `swe_private_credit_mobile_cellular`
   - expected package: `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1`
   - entity/period: SWE 1990-2024; aligned pairs 35/35; coverage 1
   - A: FS.AST.PRVT.GD.ZS — Domestic credit to private sector (% of GDP); unit `percent of GDP`; transformation `raw`
   - B: IT.CEL.SETS.P2 — Mobile cellular subscriptions (per 100 people); unit `per 100 people`; transformation `raw`
4. `dnk_agricultural_land_private_credit`
   - expected package: `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1`
   - entity/period: DNK 1990-2024; aligned pairs 34/35; coverage 0.9714285714285714
   - A: AG.LND.AGRI.ZS — Agricultural land (% of land area); unit `% of land area`; transformation `raw`
   - B: FS.AST.PRVT.GD.ZS — Domestic credit to private sector (% of GDP); unit `percent of GDP`; transformation `raw`
5. `nor_nonhydro_renewable_electricity_under5_mortality`
   - expected package: `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1`
   - entity/period: NOR 1990-2024; aligned pairs 32/35; coverage 0.9142857142857143
   - A: EG.ELC.RNWX.ZS — Electricity production from renewable sources, excluding hydroelectric (% of total); unit `% of total`; transformation `raw`
   - B: SH.DYN.MORT — Mortality rate, under-5 (per 1,000 live births); unit `per 1,000 live births`; transformation `raw`
6. `swe_private_credit_internet_users`
   - expected package: `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1`
   - entity/period: SWE 1990-2024; aligned pairs 35/35; coverage 1
   - A: FS.AST.PRVT.GD.ZS — Domestic credit to private sector (% of GDP); unit `percent of GDP`; transformation `raw`
   - B: IT.NET.USER.ZS — Individuals using the Internet (% of population); unit `% of population`; transformation `raw`
7. `dnk_forest_area_broad_money`
   - expected package: `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1`
   - entity/period: DNK 1990-2024; aligned pairs 34/35; coverage 0.9714285714285714
   - A: AG.LND.FRST.ZS — Forest area (% of land area); unit `% of land area`; transformation `raw`
   - B: FM.LBL.BMNY.GD.ZS — Broad money (% of GDP); unit `percent of GDP`; transformation `raw`
8. `nor_crude_birth_rate_fossil_electricity`
   - expected package: `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1`
   - entity/period: NOR 1990-2024; aligned pairs 34/35; coverage 0.9714285714285714
   - A: SP.DYN.CBRT.IN — Birth rate, crude (per 1,000 people); unit `per 1,000 people`; transformation `raw`
   - B: EG.ELC.FOSL.ZS — Electricity production from oil, gas and coal sources (% of total); unit `% of total`; transformation `raw`

## 6. Fingerprints
- Registry fingerprint: `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`
- Batch spec fingerprint: `sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2`
- Registry byte SHA-256 during verification: `sha256:23375a97271273c3fadaf8b42434257d471c0f904922a76e052e032abf634383`
- Spec byte SHA-256 during verification: `sha256:941c9a504f0925f44088ae51f6111a7e9469c86aa4e4d6eafc85dc6460ed9350`

## 7. Batch specification
- Path: `specs/correlation_batches/campaign41_coefficient_free_pearson_batch_spec.json`
- Engine validation: {'candidate_count': 8, 'spec_fingerprint': 'sha256:83b3597116b7937fa3e673b18315f1e6ac57a509434f4de747b59f60d91af4d5', 'valid': True}

## 8. Expected package IDs
- `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1`
- `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1`

## 9. Compatibility proof per candidate
- `dnk_agricultural_land_broad_money`: same entity, annual frequency, raw transformations, resolved units, 34 aligned observations, coverage 0.9714285714285714, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `nor_fossil_electricity_under5_mortality`: same entity, annual frequency, raw transformations, resolved units, 34 aligned observations, coverage 0.9714285714285714, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `swe_private_credit_mobile_cellular`: same entity, annual frequency, raw transformations, resolved units, 35 aligned observations, coverage 1, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `dnk_agricultural_land_private_credit`: same entity, annual frequency, raw transformations, resolved units, 34 aligned observations, coverage 0.9714285714285714, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `nor_nonhydro_renewable_electricity_under5_mortality`: same entity, annual frequency, raw transformations, resolved units, 32 aligned observations, coverage 0.9142857142857143, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `swe_private_credit_internet_users`: same entity, annual frequency, raw transformations, resolved units, 35 aligned observations, coverage 1, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `dnk_forest_area_broad_money`: same entity, annual frequency, raw transformations, resolved units, 34 aligned observations, coverage 0.9714285714285714, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.
- `nor_crude_birth_rate_fossil_electricity`: same entity, annual frequency, raw transformations, resolved units, 34 aligned observations, coverage 0.9714285714285714, no self-pair/duplicate/reversed/prior canonical pair collision, no direct arithmetic/component-total risk recorded.

## 10. Excluded proposals
- 14: insufficient aligned overlap under Pearson v1 threshold
- 1: campaign40 canonicalized agriculture/agricultural-forest land relationship
- 1: campaign40 canonicalized birth/death rates relationship
- 1: campaign40 canonicalized finance credit/broad money relationship
- 1: campaign40 canonicalized fossil/nonhydro renewables relationship
- 1: campaign40 canonicalized health life-expectancy/under-5 mortality relationship
- 1: campaign40 canonicalized internet/mobile relationship
- 1: campaign40 frozen/rejected ATM/private credit relationship
- 1: campaign40 frozen/rejected primary/secondary enrollment relationship

## 11. Coefficient-free proof
- no_campaign41_coefficient_calculated: True
- no_candidate_ranked_by_numerical_association: True
- no_covariance_calculated: True
- no_outcome_cache_consulted: True
- no_p_value_or_significance_calculated: True
- proof_basis: helper uses retained metadata, fingerprints, observed/missing period overlap, units, transformation, duplicate/existing-pair exclusion, and deterministic ordering only
- registry_contains_result_field: False
- Forbidden result fields in registry/spec candidate payloads: []
- Helper references `compute_correlation`: False
- No covariance, p-value, significance, coefficient, result-ranking, or outcome-cache operation was used.

## 12. Deterministic regeneration
- batch_spec_fingerprint_before: sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2
- batch_spec_fingerprint_regenerated: sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2
- frozen_registry_byte_identity_during_verification: True
- frozen_spec_byte_identity_during_verification: True
- logical_identity: True
- registry_fingerprint_before: sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc
- registry_fingerprint_regenerated: sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc
- returncode: 0
- stderr:

## 13. Local AI
- Not used.

## 14. Additional advisory review
- `dnk_agricultural_land_broad_money`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: moderate-to-high shared-time-trend/nonstationarity risk likely for land-share/financial aggregates; raw-level Pearson should be non-promoted with explicit limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `nor_fossil_electricity_under5_mortality`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: high shared-time-trend/nonstationarity risk likely; raw-level Pearson should be non-promoted with strong time-index diagnostics and limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `swe_private_credit_mobile_cellular`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: high shared-time-trend/nonstationarity risk likely; raw-level Pearson should be non-promoted with strong time-index diagnostics and limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `dnk_agricultural_land_private_credit`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: moderate-to-high shared-time-trend/nonstationarity risk likely for land-share/financial aggregates; raw-level Pearson should be non-promoted with explicit limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `nor_nonhydro_renewable_electricity_under5_mortality`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: high shared-time-trend/nonstationarity risk likely; raw-level Pearson should be non-promoted with strong time-index diagnostics and limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `swe_private_credit_internet_users`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: high shared-time-trend/nonstationarity risk likely; raw-level Pearson should be non-promoted with strong time-index diagnostics and limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `dnk_forest_area_broad_money`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: moderate-to-high shared-time-trend/nonstationarity risk likely for land-share/financial aggregates; raw-level Pearson should be non-promoted with explicit limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.
- `nor_crude_birth_rate_fossil_electricity`: suitable only with strong non-promoted time-index diagnostics and explicit limitations. Usefulness: minimum descriptive usefulness present because it adds a bounded same-entity cross-indicator relationship over retained annual evidence. Trend risk: high shared-time-trend/nonstationarity risk likely; raw-level Pearson should be non-promoted with strong time-index diagnostics and limitations Mechanical/common-denominator risk: low. Semantic remoteness: moderate. Reusable knowledge: reusable as an auditable, bounded relationship candidate with retained evidence/provenance; not reusable as explanation or signal. Raw Pearson adequacy: raw-level Pearson structurally adequate for finite-window descriptive object only; withhold promotion beyond non-causal descriptive package until time-index diagnostics are attached.

## 15. Engine limitation audit
- line 363, generated_statements[0].statement_id prefix: `stmt-campaign40-...-pearson-v1`; affects statement identity, statement dependency graph readability, provenance/reproducibility labels; fix: derive from spec campaign_id/campaign_label.
- line 364, calculation dependency id: `calc-campaign40-...-pearson-v1`; affects calculation identity, statement dependencies, provenance; fix: derive from spec campaign_id/campaign_label.
- line 365, evidence_ref_id: `ev-campaign40-...-fixture`; affects evidence identity, evidence_refs, provenance; fix: derive from spec campaign_id/campaign_label.
- line 385, structured_payload.validation_judgment: `accepted_campaign40_spec_driven_correlation_object`; affects validation classification, provenance semantics; fix: derive from spec validation_judgment or campaign label.
- line 387, generated_statements[0].origin: `computed_from_campaign40_declarative_spec_wdi_fixture`; affects origin text, provenance, auditability; fix: derive from spec origin/provenance label.
- line 389, provenance_envelope.lineage_basis: `frozen coefficient-free declarative Campaign 40 specification followed by reusable engine acquisition and calculation`; affects lineage text, provenance, reproducibility narrative; fix: derive from spec lineage_basis/campaign_label.
- Smallest reusable parameterization: Add optional package_template/provenance_template fields to production spec or derive labels from campaign_id; use them in build_package for statement_id, calc_id, evidence_ref_id, validation_judgment, origin, and lineage_basis; preserve Campaign 40 output semantics via regression tests; then run Campaign 41 exactly from frozen spec.
- KnowledgeObjectPackage redesign required: no.
- Doctrine redesign required: no.

## 16. Verification results
- python_compile: passed: python3 -m compileall -q tools tests
- targeted_tests: passed: 13 passed in 0.17s
- full_tests: passed: 278 passed in 17.89s
- registry_spec_schema_validation: {'candidate_count': 8, 'errors': [], 'schema_note': 'Spec uses existing correlation_batch_engine_v1 field name method, not method_contract; engine.validate_spec accepted it.', 'valid': True}
- engine_spec_validation: {'result': {'candidate_count': 8, 'spec_fingerprint': 'sha256:83b3597116b7937fa3e673b18315f1e6ac57a509434f4de747b59f60d91af4d5', 'valid': True}, 'valid': True}
- coefficient_free_validation: {'forbidden_result_field_paths': [], 'helper_references_compute_correlation': False, 'proof': {'no_campaign41_coefficient_calculated': True, 'no_candidate_ranked_by_numerical_association': True, 'no_covariance_calculated': True, 'no_outcome_cache_consulted': True, 'no_p_value_or_significance_calculated': True, 'proof_basis': 'helper uses retained metadata, fingerprints, observed/missing period overlap, units, transformation, duplicate/existing-pair exclusion, and deterministic ordering only', 'registry_contains_result_field': False}, 'valid': True}
- evidence_path_and_fingerprint_validation: {'errors': [], 'valid': True}
- package_id_duplicate_existing_exclusion: {'duplicate_or_reversed_pairs': [], 'existing_package_id_collisions': [], 'existing_relationship_pair_collisions': [], 'package_id_unique': True, 'self_pairs': [], 'valid': True}
- deterministic_regeneration: {'batch_spec_fingerprint_before': 'sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2', 'batch_spec_fingerprint_regenerated': 'sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2', 'frozen_registry_byte_identity_during_verification': True, 'frozen_spec_byte_identity_during_verification': True, 'logical_identity': True, 'registry_fingerprint_before': 'sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc', 'registry_fingerprint_regenerated': 'sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc', 'returncode': 0, 'stderr': ''}
- sensitive_material_scan: passed for sensitive content: actual_secret_blockers=0; unsafe_absolute_path_dependencies=0; repository durability validator decision remains D due unrelated untracked recovery-critical implementation/durability residuals
- context_health: passed with warning only: stale generated context/active_context.md
- coherence: passed with warning only: stale generated context/active_context.md
- architecture_reality_audit: passed: 0 blocks, 0 warnings
- git_diff_checks: passed: git diff --check and git diff --cached --check exit 0
- frozen_registry_byte_identical: True
- frozen_spec_byte_identical: True

## 17. Doctrine/architecture classification
- Doctrine Review Trigger: not reached.
- Architecture pressure: not discovered.
- The required extension is bounded reusable parameterization of existing engine package internals, not a KnowledgeObjectPackage redesign.

## 18. Decision
B. 8 valid candidates frozen; bounded reusable engine extension is required before calculation.

## 19. Smallest exact next task
Patch `tools/correlation_batch_engine.py` to parameterize Campaign 40 hardcoded statement/calculation/evidence IDs, validation judgment, origin, and lineage text from spec-level metadata; add regression tests preserving Campaign 40 compatibility and proving Campaign 41 spec readiness. Stop before coefficient calculation unless explicitly authorized.

## 20. Hard boundaries preserved
- No Campaign 41 coefficients/covariance/p-values/significance calculated.
- No canonical packages created or published.
- No PostgreSQL rebuild/write.
- No relationship export execution.
- No Campaign 42.
- No commit or push.
