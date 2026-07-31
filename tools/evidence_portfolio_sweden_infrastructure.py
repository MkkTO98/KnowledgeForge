#!/usr/bin/env python3
"""Sweden Infrastructure Evidence Portfolio v1 preregistration and runner.

This producer supplies family-specific, outcome-blind configuration to the shared
Evidence Portfolio implementation.  It reads only the retained Campaign 40 WDI
fixtures and does not alter the canonical contract or repository schema.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import evidence_portfolio_production as portfolio

CAMPAIGN_ID = "evidence-portfolio-infrastructure-sweden-baseline-20260731"
MANIFEST_ID = "manifest-evidence-portfolio-infrastructure-sweden-baseline-v1"
BUNDLE_ID = "bundle-infrastructure-sweden-annual-1990-2024-v1"
DATE = "2026-07-31"
SUBSTANTIVE_EQUIVALENCE_LIMITATION = "Shared population scaling or denominator conventions do not make Internet users and mobile cellular subscriptions substantively equivalent."
ACROSS_YEARS_LIMITATION = "Level-distribution statistics are unweighted summaries across retained annual observations; they are not population-weighted pooled-period estimates and do not describe a cross-sectional distribution among people, users or subscriptions."
PREDECESSOR_MANIFEST_FINGERPRINT = "sha256:8e82a5859402f3ded40e739a0ee82525118a224d6031c4a7dbde6ae1b533a5c1"
FIXTURE_ROOT = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https"
CANDIDATE_REGISTRY = PROJECT_ROOT / "artifacts/reports/campaign40-spec-driven-pearson-production-20260711/selection/candidate_registry.json"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / f"artifacts/production/{CAMPAIGN_ID}"
DEFAULT_REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"

SERIES = [
    {
        "code": "IT.NET.USER.ZS",
        "name": "Individuals using the Internet (% of population)",
        "definition": "Internet users are individuals who have used the Internet (from any location) in the last 3 months. The Internet can be used via a computer, mobile phone, personal digital assistant, games machine, digital TV etc.",
        "unit": "% of population",
        "denominator_basis": "resident_population_scaled_as_percent",
        "measure_kind": "individual_people_using_internet_share",
        "canary": True,
        "applicability_limitations": [
            "The measure concerns people using the Internet, not subscriptions, devices, connection quality, intensity of use or digital skills.",
            "Technology definitions and survey or modeled-estimation practices can change across the retained window.",
            "Adoption and saturation dynamics can be nonlinear and are not represented by a structural model.",
            "Structural breaks, policy changes and technology transitions are not identified or explained by these descriptors.",
        ],
    },
    {
        "code": "IT.CEL.SETS.P2",
        "name": "Mobile cellular subscriptions (per 100 people)",
        "definition": "Mobile cellular telephone subscriptions are subscriptions to a public mobile telephone service that provide access to the PSTN using cellular technology. The indicator includes (and is split into) the number of postpaid subscriptions, and the number of active prepaid accounts (i.e. that have been used during the last three months). The indicator applies to all mobile cellular subscriptions that offer voice communications. It excludes subscriptions via data cards or USB modems, subscriptions to public mobile data services, private trunked mobile radio, telepoint, radio paging and telemetry services.",
        "unit": "per 100 people",
        "denominator_basis": "resident_population_scaled_per_100_people",
        "measure_kind": "mobile_cellular_subscriptions_per_100_people",
        "canary": False,
        "applicability_limitations": [
            "The measure counts mobile cellular subscriptions, not unique people, devices, service quality, usage or affordability; one person may hold multiple subscriptions.",
            "Technology definitions, active-account rules and administrative reporting practices can change across the retained window.",
            "Adoption and saturation dynamics can be nonlinear and are not represented by a structural model.",
            "Structural breaks, policy changes and technology transitions are not identified or explained by these descriptors.",
        ],
    },
]


def _family_configuration(series: dict[str, Any]) -> dict[str, Any]:
    return {
        "family": "Infrastructure",
        "family_slug": "infrastructure",
        "domain": "WDI Infrastructure baseline characterization",
        "evidence_family": "external_wdi_annual_scalar_infrastructure_baseline_characterization",
        "result_limitations": [
            "finite retained ordered annual sequence",
            "descriptive only",
            "no causal predictive significance stationarity saturation permanence or technology-adoption claim",
            ACROSS_YEARS_LIMITATION,
        ],
        "package_limitations": [
            "No cross-series comparison or relationship is calculated.",
            SUBSTANTIVE_EQUIVALENCE_LIMITATION,
            f"The indicator is interpreted only as {series['measure_kind']}; it is not a general measure of infrastructure quality or welfare.",
            "Slope sign is a finite-window time-index descriptor, not evidence of structural trend, stationarity, saturation or forecastability.",
            "First differences summarize consecutive retained annual values only and do not identify technology transitions or structural breaks.",
            "WDI reacquisition may change; retained local bytes are the replay anchor.",
            "Canonical decimal precision is not measurement precision.",
            ACROSS_YEARS_LIMITATION,
        ],
        "applicability_limitations": [
            *copy.deepcopy(series["applicability_limitations"]),
            SUBSTANTIVE_EQUIVALENCE_LIMITATION,
        ],
        "uncertainty_dimensions": [
            "mutable_source_reacquisition_limit",
            "survey_modeled_or_administrative_measurement_process",
            "technology_definition_and_adoption_change",
            "bounded_single_territory_window",
        ],
        "governance_review_state": "bounded Infrastructure portfolio promotion contract passed",
        "evolution_change_reason": "first bounded Sweden Infrastructure Evidence Portfolio production pilot",
        "promotion_maturity_state": "bounded Infrastructure portfolio pilot accepted",
        "generation_date": DATE,
    }


def _entry_for_series(series: dict[str, Any]) -> dict[str, Any]:
    path = FIXTURE_ROOT / f"{series['code']}__SWE__1990-2024" / "normalized_observations.json"
    normalized = portfolio.read_json(path)
    identity_inputs = {
        "indicator_code": series["code"],
        "territory_id": "SWE",
        "period_start": 1990,
        "period_end": 2024,
        "method_id": portfolio.METHOD_ID,
        "method_version": portfolio.METHOD_VERSION,
    }
    return {
        "candidate_id": f"candidate-infrastructure-{portfolio._slug(series['code'])}-swe-1990-2024-baseline-v1",
        "disposition": "execute",
        "canary": series["canary"],
        "input": {
            "path": str(path.relative_to(PROJECT_ROOT)),
            "sha256": portfolio.file_fingerprint(path),
            "normalized_fingerprint": normalized["normalized_fingerprint"],
            "admission_basis": "retained Campaign 40 HTTPS fixture selected by the frozen coefficient-free candidate registry",
        },
        "indicator": {
            "code": series["code"],
            "name": series["name"],
            "definition": series["definition"],
            "family": "Infrastructure",
        },
        "territory": {
            "id": "SWE",
            "name": "Sweden",
            "observational_population": "retained observed annual Sweden values for the indicator within 1990-2024",
        },
        "applicability": {
            "denominator_basis": series["denominator_basis"],
            "unit": series["unit"],
            "period_start": 1990,
            "period_end": 2024,
            "frequency": "annual",
            "observation_grain": "territory_indicator_year",
            "population_basis": "finite retained sequence; not a random sample",
            "measure_kind": series["measure_kind"],
        },
        "transformation": ["level", "adjacent_first_difference", "linear_time_index_slope"],
        "method": {
            "id": portfolio.METHOD_ID,
            "version": portfolio.METHOD_VERSION,
            "parameters": {
                "summary_method": "wdi_annual_scalar_statistical_summary_v2@2.0",
                "summary_contract_fingerprint": portfolio.SUMMARY_CONTRACT_FINGERPRINT,
                "minimum_observed_count": 30,
                "minimum_coverage_share": "0.85",
                "decimal_precision": 50,
                "rounding": "ROUND_HALF_EVEN",
                "difference_rule": "only consecutive observed annual periods",
                "quartile_rule": "median of lower and upper halves excluding the overall median for odd N",
                "slope_rule": "ordinary least-squares slope against integer calendar year; descriptor only",
            },
        },
        "expected_output_class": "baseline_characterization",
        "dependencies": ["retained_campaign40_fixture", "wdi_annual_scalar_statistical_summary_v2@2.0"],
        "bundle_id": BUNDLE_ID,
        "campaign_id": CAMPAIGN_ID,
        "computational_budget": copy.deepcopy(portfolio.REQUIRED_ENTRY_LIMITS),
        "validation_requirements": ["input_hash", "coverage", "stable_identity", "exact_lineage", "applicability", "schema", "nonredundancy", "input_immutability"],
        "promotion_conditions": ["all_28_required_results_valid", "no_identity_collision", "no_redundancy", "knowledge_object_validation_pass"],
        "exclusion_and_stopping_rules": ["stop_on_input_hash_mismatch", "stop_on_manifest_fingerprint_mismatch", "exclude_nonconsecutive_differences", "exclude_growth_rates", "exclude_relationship_claims"],
        "identity_inputs": identity_inputs,
        "family_configuration": _family_configuration(series),
    }


def build_preregistration() -> tuple[dict[str, Any], dict[str, Any]]:
    registry = portfolio.read_json(CANDIDATE_REGISTRY)
    selected = next(
        record for record in registry["records"]
        if record["candidate_id"] == "infrastructure_internet_mobile_swe"
    )
    entries = [_entry_for_series(series) for series in SERIES]
    exclusion = copy.deepcopy(entries[0])
    exclusion.update({
        "candidate_id": "candidate-infrastructure-internet-users-cagr-excluded-v1",
        "disposition": "excluded_pre_execution",
        "canary": True,
        "expected_output_class": "excluded_inapplicable_method",
        "exclusion_reason": "CAGR and percentage-growth summaries are not semantically justified for this bounded infrastructure adoption-share level series and could imply a compound accumulation process.",
    })
    exclusion["method"] = {"id": "compound_annual_growth_rate", "version": "not_registered", "parameters": {}}
    exclusion["identity_inputs"] = {
        **exclusion["identity_inputs"],
        "method_id": "compound_annual_growth_rate",
        "method_version": "not_registered",
    }
    entries.append(exclusion)

    rubric = {
        "rubric_id": "selection-rubric-infrastructure-sweden-baseline-portfolio-v1",
        "recorded_before_new_outcome_calculation": True,
        "eligible_universe": [{
            "registry_id": registry["registry_id"],
            "registry_fingerprint": registry["registry_fingerprint"],
            "candidate_ids": [record["candidate_id"] for record in registry["records"]],
        }],
        "criteria": [
            "authoritative Mature WDI Infrastructure family and admitted retained HTTPS evidence",
            "complete two-series registry pair with coefficient-free admission metadata",
            "same Sweden territory, annual frequency and 1990-2024 window",
            "durable local raw and normalized inputs with exact hashes",
            "clear units, definitions, observational population and denominator/applicability bases",
            "35 retained observations and complete coverage in frozen admission metadata",
            "low bounded computational and review cost",
            "descriptive downstream utility without relationship calculation or technology-adoption interpretation",
            "no selection based on newly calculated level, difference, slope or variability outcomes",
        ],
        "selected_family": "Infrastructure",
        "selected_candidate_id": selected["candidate_id"],
        "selection_reason": "The complete retained Sweden Infrastructure pair is mature, semantically distinguishable, territory/period consistent, fully covered in admitted metadata and useful for bounded baseline characterization without calculating a cross-series relationship.",
        "known_limitations": [
            "WDI mutable-source vintage limitation; retained bytes are the replay anchor",
            "Internet users measure people while mobile cellular subscriptions may count multiple subscriptions per person",
            SUBSTANTIVE_EQUIVALENCE_LIMITATION,
            "technology definitions, reporting methods, adoption, saturation and structural breaks can vary over time",
            "finite ordered annual values are not random or independent samples",
            "linear slope and first-difference descriptors do not establish persistence, explanation or forecastability",
            "canonical decimal precision is representation policy, not source measurement precision",
        ],
        "excluded_universe": [
            {"candidate_id": record["candidate_id"], "reason": "different WDI topical family; excluded before portfolio outcomes"}
            for record in registry["records"] if record["candidate_id"] != selected["candidate_id"]
        ],
        "selection_registry_file_sha256": portfolio.file_fingerprint(CANDIDATE_REGISTRY),
    }
    rubric["rubric_fingerprint"] = portfolio.fingerprint({key: value for key, value in rubric.items() if key != "rubric_fingerprint"})

    manifest = {
        "manifest_id": MANIFEST_ID,
        "manifest_version": "1.1",
        "amendment": {
            "predecessor_manifest_fingerprint": PREDECESSOR_MANIFEST_FINGERPRINT,
            "reason": "Independent pre-closeout semantic review required quantity-aware derived units and an explicit across-years statistical-population limitation.",
            "scope": ["derived_result_unit_labels", "statistical_population_limitation"],
            "candidate_universe_changed": False,
            "calculation_methods_changed": False,
            "outcome_replacement_or_padding": False,
        },
        "campaign_id": CAMPAIGN_ID,
        "portfolio_kind": "bounded_baseline_characterization_execution_manifest",
        "canonical_ontology_change": False,
        "evidence_card_equivalent_definition": "one operational result-record view; canonical authority remains the KnowledgeObjectPackage",
        "bundle_definition": "bounded campaign grouping only; not a new canonical object type",
        "selection_rubric_fingerprint": rubric["rubric_fingerprint"],
        "entries": entries,
        "candidate_order": [entry["candidate_id"] for entry in entries],
        "computational_budget": copy.deepcopy(portfolio.REQUIRED_PORTFOLIO_LIMITS),
        "validation_requirements": ["manifest_schema", "outcome_blind_fields", "input_hashes", "stable_identities", "complete_accounting", "deterministic_rerun"],
        "promotion_conditions": ["canary_gate_pass", "all_required_records_valid", "canonical_package_validator_pass", "no_duplicate_promotion"],
        "stopping_rules": ["no candidate substitution after outcomes", "stop_on_canary_material_failure", "do_not_exceed_budget"],
        "forbidden_outcome_fields": copy.deepcopy(portfolio.FORBIDDEN_OUTCOME_FIELDS),
    }
    manifest["manifest_fingerprint"] = portfolio.fingerprint({key: value for key, value in manifest.items() if key != "manifest_fingerprint"})
    portfolio.validate_manifest(manifest)
    return rubric, manifest


def command_preregister(args: argparse.Namespace) -> None:
    rubric, manifest = build_preregistration()
    output = Path(args.output_root)
    portfolio.write_json(output / "selection_rubric.json", rubric)
    portfolio.write_json(output / "portfolio_manifest.json", manifest)
    print(json.dumps({
        "selection_rubric": str(output / "selection_rubric.json"),
        "manifest": str(output / "portfolio_manifest.json"),
        "manifest_fingerprint": manifest["manifest_fingerprint"],
        "entries": len(manifest["entries"]),
    }, sort_keys=True))


def command_run(args: argparse.Namespace) -> None:
    manifest_path = Path(args.manifest)
    manifest = portfolio.read_json(manifest_path)
    gate = portfolio.run_portfolio(
        manifest,
        args.mode,
        Path(args.output_root),
        Path(args.repository_root),
        Path(args.canary_gate) if args.canary_gate else None,
        manifest_file_fingerprint=portfolio.file_fingerprint(manifest_path),
        project_root=PROJECT_ROOT,
    )
    print(json.dumps(gate, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    preregister = subparsers.add_parser("preregister")
    preregister.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    preregister.set_defaults(func=command_preregister)
    run = subparsers.add_parser("run")
    run.add_argument("--manifest", required=True)
    run.add_argument("--mode", choices=["canary", "production"], required=True)
    run.add_argument("--output-root", required=True)
    run.add_argument("--repository-root", required=True)
    run.add_argument("--canary-gate")
    run.set_defaults(func=command_run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
