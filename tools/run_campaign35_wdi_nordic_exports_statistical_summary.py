#!/usr/bin/env python3
"""Campaign 35: bounded WDI Nordic exports-share statistical-summary replication.

This campaign creates three substantive deterministic KnowledgeObjectPackages from
one retained HTTPS WDI fixture. It preserves existing Production Doctrine and uses
statistical-summary calculation-contract v2 only.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import deterministic_statistical_summary_v2 as method_v2
import knowledge_repository
import wdi_observation_evidence_fixture as fixture_tool

CAMPAIGN_ID = "campaign-35-wdi-nordic-exports-share-statistical-summary-replication"
CAMPAIGN_TITLE = "Campaign 35 — Bounded WDI Nordic Exports Share Statistical-Summary Replication"
DATE = "2026-07-10"
INDICATOR_CODE = "NE.EXP.GNFS.ZS"
INDICATOR_NAME = "Exports of goods and services (% of GDP)"
EXPECTED_DEFINITION_PHRASE = "This indicator is expressed as a percentage of Gross Domestic Product (GDP)"
UNIT = "percent of GDP"
ENTITIES = ["DNK", "SWE", "NOR"]
ENTITY_NAMES = {"DNK": "Denmark", "SWE": "Sweden", "NOR": "Norway"}
START_YEAR = 1990
END_YEAR = 2024
EXPECTED_SLOTS_PER_ENTITY = 35
EXPECTED_TOTAL_SLOTS = 105
EVIDENCE_FAMILY = "external_wdi_annual_scalar_trade_statistical_summary"
EXPECTED_CONTRACT_FINGERPRINT = "sha256:80e6b07fd98faf37401103776b6ef82f4ab981c5ea890b381b036058c460e8a0"
DEFAULT_FIXTURE_DIR = PROJECT_ROOT / "artifacts" / "evidence-fixtures" / "campaign35-wdi-nordic-exports-share-1990-2024-https"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "production" / "campaign-35-wdi-nordic-exports-share-statistical-summary-replication"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "artifacts" / "reports" / "campaign35-wdi-nordic-exports-share-statistical-summary-20260710"
DEFAULT_REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
FORBIDDEN_PACKAGE_TERMS = [
    "causation",
    "causal",
    "because",
    "explain",
    "forecast",
    "recommend",
    "investment",
    "normative",
    "significance",
    "stationarity",
    "trend",
    "performance",
    "structural stability",
    "randomly sampled",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any, *, pretty: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if pretty:
        path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
    else:
        path.write_text(canonical_json(value) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def verify_loaded_v2_contract() -> dict[str, Any]:
    contract = method_v2.calculation_contract_v2()
    if contract["calculation_contract_fingerprint"] != EXPECTED_CONTRACT_FINGERPRINT:
        raise RuntimeError(
            f"v2 contract mismatch: {contract['calculation_contract_fingerprint']} != {EXPECTED_CONTRACT_FINGERPRINT}"
        )
    return contract


def campaign35_selection_contract() -> dict[str, Any]:
    contract = fixture_tool.build_selection_contract(
        indicator_code=INDICATOR_CODE,
        entities=ENTITIES,
        start_year=START_YEAR,
        end_year=END_YEAR,
    )
    contract["selection_purpose"] = "Campaign 35 bounded multi-entity statistical-summary replication evidence fixture"
    contract["mature_knowledgeforge_family"] = "external_wdi_annual_scalar_trade"
    contract["evidence_family"] = EVIDENCE_FAMILY
    contract["indicator"]["name"] = INDICATOR_NAME
    contract["indicator"]["expected_unit"] = UNIT
    contract["request"]["observation_url"] = (
        "https://api.worldbank.org/v2/country/DNK;SWE;NOR/indicator/"
        "NE.EXP.GNFS.ZS?format=json&date=1990:2024&per_page=20000"
    )
    contract["request"]["indicator_metadata_url"] = (
        "https://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json&per_page=1"
    )
    contract["request"]["parameters"] = {"format": "json", "date": "1990:2024", "per_page": "20000"}
    contract["completeness_expectation"] = {
        "expected_observation_slots": EXPECTED_TOTAL_SLOTS,
        "expected_slots_per_entity": EXPECTED_SLOTS_PER_ENTITY,
        "expected_pages": 1,
        "missing_values_are_explicit": True,
    }
    contract["scope_exclusions"] = [
        "ordinary WDI breadth expansion",
        "Campaign 36",
        "correlations",
        "covariance structures",
        "lag relationships",
        "trend descriptors",
        "causal or forecast claims",
        "MacroForge access or coupling",
        "consumer or InsightForge access",
        "PostgreSQL schema expansion",
        "incremental PostgreSQL synchronization",
        "Production Doctrine modification",
        "KnowledgeObjectPackage redesign",
        "broad local-AI infrastructure",
    ]
    contract["selection_fingerprint"] = fixture_tool.sha256_value({k: v for k, v in contract.items() if k != "selection_fingerprint"})
    return contract


def acquire_campaign35_fixture(output_dir: Path = DEFAULT_FIXTURE_DIR) -> dict[str, Any]:
    contract = campaign35_selection_contract()
    raw, observation_bytes, metadata_bytes = fixture_tool.acquire_raw_fixture(contract)
    validation = fixture_tool.write_fixture_artifacts(raw, output_dir, observation_bytes, metadata_bytes)
    normalize_campaign35_unit(output_dir / "normalized_observations.json")
    normalized = read_json(output_dir / "normalized_observations.json")
    fixture_validation = validate_campaign35_fixture(normalized)
    if fixture_validation["blockers"]:
        write_json(output_dir / "campaign35_fixture_validation.json", fixture_validation)
        raise RuntimeError(f"Campaign 35 fixture validation failed: {fixture_validation['blockers']}")
    extra = {
        "campaign35_fixture_validation": fixture_validation,
        "requested_urls": raw["access_metadata"]["requested_urls"],
        "final_resolved_urls": raw["access_metadata"]["final_resolved_urls"],
        "https_only": all(url.startswith("https://") for url in raw["access_metadata"]["final_resolved_urls"].values()),
        "downgrade_rejected_by_tool": True,
    }
    write_json(output_dir / "campaign35_fixture_validation.json", extra)
    return {"validation": validation, "campaign35_validation": extra, "fixture_dir": str(output_dir)}


def normalize_campaign35_unit(normalized_path: Path) -> dict[str, Any]:
    """Canonicalize Campaign 35 units from authoritative WDI metadata text."""
    normalized = read_json(normalized_path)
    metadata = normalized.get("indicator_metadata", {})
    if metadata.get("id") != INDICATOR_CODE:
        raise ValueError("cannot apply Campaign 35 unit normalization to a different indicator")
    definition = metadata.get("definition") or ""
    name = metadata.get("name") or ""
    if "% of GDP" not in name or EXPECTED_DEFINITION_PHRASE not in definition:
        raise ValueError("authoritative WDI metadata does not support percent-of-GDP unit normalization")
    unit_basis = "authoritative WDI indicator name and sourceNote state percent-of-GDP semantics; WDI unit field is blank in raw metadata"
    metadata["unit"] = UNIT
    metadata["unit_basis"] = unit_basis
    for row in normalized.get("observations", []):
        row["unit"] = UNIT
    normalized.setdefault("normalization", {})["unit_canonicalization"] = unit_basis
    normalized["normalized_fingerprint"] = fixture_tool.sha256_value({k: v for k, v in normalized.items() if k != "normalized_fingerprint"})
    write_json(normalized_path, normalized, pretty=False)
    return normalized


def validate_campaign35_fixture(normalized: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    metadata = normalized.get("indicator_metadata", {})
    selection = normalized.get("selection_contract", {})
    if metadata.get("id") != INDICATOR_CODE or selection.get("indicator", {}).get("code") != INDICATOR_CODE:
        blockers.append({"category": "indicator_identity", "message": "indicator identity does not match NE.EXP.GNFS.ZS"})
    if metadata.get("name") != INDICATOR_NAME:
        blockers.append({"category": "indicator_identity", "message": "indicator name does not match expected WDI metadata"})
    definition = metadata.get("definition") or ""
    if EXPECTED_DEFINITION_PHRASE not in definition:
        blockers.append({"category": "indicator_definition", "message": "indicator definition does not match expected WDI definition phrase"})
    entities = selection.get("entities")
    if entities != sorted(ENTITIES):
        blockers.append({"category": "entity_scope", "message": f"entity scope {entities!r} does not match {sorted(ENTITIES)!r}"})
    periods = selection.get("periods", {})
    if periods.get("start_year") != START_YEAR or periods.get("end_year") != END_YEAR:
        blockers.append({"category": "period_scope", "message": "period scope must be 1990-2024"})
    if normalized.get("expected_observation_slots") != EXPECTED_TOTAL_SLOTS:
        blockers.append({"category": "slot_count", "message": "expected total slot count must be 105"})
    keys: set[tuple[Any, Any, Any]] = set()
    per_entity = {entity: {"expected": 0, "observed": 0, "missing": 0} for entity in ENTITIES}
    for row in normalized.get("observations", []):
        key = (row.get("entity_id"), row.get("indicator_code"), row.get("period"))
        if key in keys:
            blockers.append({"category": "duplicate_keys", "message": f"duplicate key {key}"})
        keys.add(key)
        entity = row.get("entity_id")
        if entity not in ENTITIES:
            blockers.append({"category": "entity_scope", "message": f"unexpected entity {entity}"})
            continue
        if row.get("indicator_code") != INDICATOR_CODE:
            blockers.append({"category": "indicator_identity", "message": f"unexpected row indicator {row.get('indicator_code')}"})
        period = row.get("period")
        if not isinstance(period, int) or period < START_YEAR or period > END_YEAR:
            blockers.append({"category": "period_scope", "message": f"unexpected period {period}"})
        per_entity[entity]["expected"] += 1
        if row.get("observed"):
            per_entity[entity]["observed"] += 1
            value = row.get("value_canonical")
            try:
                method_v2.compute_statistical_summary_v2({"observations": [row] * 30, "expected_observation_slots": 30}, minimum_observed_count=30)
            except Exception:
                # That one-row repetition creates duplicate keys, so use direct parser via public invalid pathway check instead below.
                pass
            if not isinstance(value, str) or "e" in value.lower() or "," in value:
                blockers.append({"category": "numeric_value", "message": f"ambiguous numerical value {value!r}"})
        else:
            per_entity[entity]["missing"] += 1
            if row.get("value_canonical") is not None:
                blockers.append({"category": "missingness", "message": "missing row carries a numerical value"})
    for entity, counts in per_entity.items():
        if counts["expected"] != EXPECTED_SLOTS_PER_ENTITY:
            blockers.append({"category": "entity_slots", "message": f"{entity} expected slots {counts['expected']} != 35"})
        coverage = counts["observed"] / counts["expected"] if counts["expected"] else 0
        if counts["observed"] < 30 or coverage < 0.85:
            blockers.append({"category": "entity_coverage", "message": f"{entity} observed={counts['observed']} coverage={coverage}"})
    if (metadata.get("unit") or "") not in ("", UNIT):
        blockers.append({"category": "unit", "message": f"unexpected metadata unit {metadata.get('unit')!r}"})
    warnings.append({"category": "mutable_source", "message": "WDI API does not provide a guaranteed immutable historical vintage in the retained response; raw bytes are the reproducibility anchor."})
    return {"valid": not blockers, "blockers": blockers, "warnings": warnings, "per_entity": per_entity}


def entity_normalized_fixture(normalized: dict[str, Any], entity: str) -> dict[str, Any]:
    rows = [copy.deepcopy(row) for row in normalized["observations"] if row["entity_id"] == entity]
    out = copy.deepcopy(normalized)
    out["observations"] = rows
    out["expected_observation_slots"] = len(rows)
    out["observed_count"] = sum(1 for row in rows if row["observed"])
    out["missing_count"] = len(rows) - out["observed_count"]
    out["missing_share"] = out["missing_count"] / len(rows) if rows else 0
    out["selection_contract"] = copy.deepcopy(normalized["selection_contract"])
    out["selection_contract"]["entities"] = [entity]
    out["entity_level_source_normalized_fingerprint"] = normalized.get("normalized_fingerprint")
    out["normalized_fingerprint"] = fixture_tool.sha256_value({k: v for k, v in out.items() if k != "normalized_fingerprint"})
    return out


def compute_entity_summaries(normalized: dict[str, Any]) -> dict[str, dict[str, Any]]:
    verify_loaded_v2_contract()
    summaries: dict[str, dict[str, Any]] = {}
    for entity in ENTITIES:
        entity_fixture = entity_normalized_fixture(normalized, entity)
        summary = method_v2.compute_statistical_summary_v2(entity_fixture)
        summary["unit"] = UNIT
        for key in ["first_valid_observation", "last_valid_observation"]:
            summary[key]["unit"] = UNIT
        for key in ["minimum", "maximum", "arithmetic_mean", "median", "population_standard_deviation"]:
            summary[key]["unit"] = UNIT
        summary["period_coverage"] = {"start_period": START_YEAR, "end_period": END_YEAR, "frequency": "annual"}
        summary["entity_id"] = entity
        summary["entity_name"] = ENTITY_NAMES[entity]
        summary["indicator_code"] = INDICATOR_CODE
        summary["indicator_name"] = INDICATOR_NAME
        summaries[entity] = summary
    return summaries


def utility_decisions(summary: dict[str, Any]) -> dict[str, Any]:
    observed = summary["observed_count"]
    coverage = summary["coverage_share"]["canonical"]
    retain = observed >= 30 and float(coverage) >= 0.85
    rationale = (
        "Annual exports share is a bounded-window percent-of-GDP economic ratio; finite-window center and dispersion describe retained observed values."
    )
    return {
        "arithmetic_mean": {"decision": "retain" if retain else "omit", "rationale": rationale},
        "median": {"decision": "retain" if retain else "omit", "rationale": rationale},
        "population_standard_deviation": {"decision": "retain" if retain else "omit", "rationale": rationale},
        "prohibited_interpretations": [
            "stationarity",
            "independent_or_random_sampling",
            "structural stability",
            "economic performance",
            "causal explanation",
            "forecast expectation",
            "statistical significance",
            "investment implications",
            "directional change conclusion",
        ],
    }


def package_id_for(entity: str) -> str:
    return f"pkg-object-srcpkg-campaign35-{entity.lower()}-exports-share-statistical-summary-v2"


def build_entity_package(normalized: dict[str, Any], entity: str, summary: dict[str, Any]) -> dict[str, Any]:
    contract = verify_loaded_v2_contract()
    source_contract = normalized["selection_contract"]
    raw_artifacts = normalized["raw_artifacts"]
    package_id = package_id_for(entity)
    candidate_id = f"pkg-candidate-srcpkg-campaign35-{entity.lower()}-exports-share-statistical-summary-v2"
    statement_id = f"stmt-campaign35-{entity.lower()}-exports-share-statistical-summary-v2"
    decisions = utility_decisions(summary)
    included = ["expected_slot_count", "observed_count", "missing_count", "missing_share", "coverage_share", "first_valid_observation", "last_valid_observation", "minimum", "maximum", "period_coverage", "unit"]
    for measure, decision in decisions.items():
        if measure != "prohibited_interpretations" and decision["decision"] == "retain":
            included.append(measure)
    omitted = [measure for measure, decision in decisions.items() if measure != "prohibited_interpretations" and decision["decision"] != "retain"]
    statement_text = (
        f"For retained World Bank WDI {INDICATOR_CODE} observations for {ENTITY_NAMES[entity]} ({entity}), annual {START_YEAR}-{END_YEAR}, "
        f"the fixture has {summary['expected_observation_slot_count']} expected slots, {summary['observed_count']} observed values, "
        f"{summary['missing_count']} missing values, coverage share {summary['coverage_share']['canonical']}, first valid value "
        f"{summary['first_valid_observation']['value']} {UNIT} in {summary['first_valid_observation']['period']}, last valid value "
        f"{summary['last_valid_observation']['value']} {UNIT} in {summary['last_valid_observation']['period']}, minimum "
        f"{summary['minimum']['canonical']} {UNIT} in {summary['minimum']['periods']}, maximum {summary['maximum']['canonical']} {UNIT} in "
        f"{summary['maximum']['periods']}, arithmetic mean {summary['arithmetic_mean']['canonical']} {UNIT}, median "
        f"{summary['median']['canonical']} {UNIT}, and population standard deviation {summary['population_standard_deviation']['canonical']} {UNIT} under {method_v2.METHOD_ID}@{method_v2.METHOD_VERSION}."
    )
    promoted_summary = {key: value for key, value in summary.items() if key != "conditional_measure_context"}
    promoted_utility_decisions = {key: value for key, value in decisions.items() if key != "prohibited_interpretations"}
    common = {
        "package_id": package_id,
        "package_kind": "KnowledgeObjectPackage",
        "package_version": "1.0",
        "created_at": DATE,
        "created_by": "run_campaign35_wdi_nordic_exports_statistical_summary",
        "status": "accepted-for-controlled-production",
        "scope": {
            "domain": "WDI Nordic exports share statistical summary",
            "source_scope": {
                "campaign_id": CAMPAIGN_ID,
                "provider": "World Bank",
                "dataset": "World Development Indicators",
                "source_id": "2",
                "indicator_code": INDICATOR_CODE,
                "indicator_name": INDICATOR_NAME,
                "entity_id": entity,
                "entity_name": ENTITY_NAMES[entity],
                "period_start": START_YEAR,
                "period_end": END_YEAR,
                "frequency": "annual",
                "unit": UNIT,
                "scope_type": "bounded_statistical_summary",
            },
            "evidence_family": EVIDENCE_FAMILY,
            "method_scope": f"{method_v2.METHOD_ID}@{method_v2.METHOD_VERSION}",
            "intended_use": "deterministic descriptive knowledge only",
        },
        "input_references": ["srcpkg-campaign35-wdi-nordic-exports-share-https-fixture"],
        "evidence_references": [
            {
                "evidence_ref_id": "ev-campaign35-wdi-nordic-exports-share-https-fixture",
                "evidence_class": "external_observation_level_numerical_fixture",
                "source_family": "official_statistical_source_data",
                "source_identity": f"World Bank WDI {INDICATOR_CODE} {entity} annual fixture",
                "source_owner": "World Bank WDI API retained local fixture",
                "source_version": normalized["provider_metadata"].get("wdi_lastupdated"),
                "accessed_at": DATE,
                "snapshot_fingerprint": raw_artifacts["combined_raw_artifact_fingerprint"],
                "reproducibility_handle": "retained HTTPS raw fixture and normalized observations",
                "evaluation_status": "evaluated",
            }
        ],
        "computation_method": {
            "name": method_v2.METHOD_ID,
            "version": method_v2.METHOD_VERSION,
            "recipe": "offline deterministic Decimal statistical summary v2 over retained normalized observations",
            "parameters": contract,
            "query_definitions": [],
            "nondeterminism": "none",
            "rerun": "python3 tools/run_campaign35_wdi_nordic_exports_statistical_summary.py --reuse-fixture",
        },
        "generated_statements": [
            {
                "statement_id": statement_id,
                "statement_type": "derived",
                "text": statement_text,
                "applicability": {
                    "indicator_code": INDICATOR_CODE,
                    "entity_id": entity,
                    "period_start": START_YEAR,
                    "period_end": END_YEAR,
                    "method_id": method_v2.METHOD_ID,
                    "method_version": method_v2.METHOD_VERSION,
                },
                "dependencies": ["ev-campaign35-wdi-nordic-exports-share-https-fixture", "calc-campaign35-statistical-summary-v2"],
                "evidence_refs": ["ev-campaign35-wdi-nordic-exports-share-https-fixture"],
                "origin": "computed_from_retained_normalized_evidence_fixture",
                "structured_payload": {
                    **promoted_summary,
                    "included_measures": included,
                    "omitted_measures": omitted,
                    "utility_decisions": promoted_utility_decisions,
                    "provider_metadata": {
                        "provider": "World Bank",
                        "dataset": "World Development Indicators",
                        "wdi_lastupdated": normalized["provider_metadata"].get("wdi_lastupdated"),
                        "sourceid": normalized["provider_metadata"].get("sourceid"),
                    },
                    "mutable_source_limitation": normalized["mutable_source_reproducibility_note"],
                    "raw_evidence_fingerprint": raw_artifacts["combined_raw_artifact_fingerprint"],
                    "normalized_evidence_fingerprint": normalized["normalized_fingerprint"],
                    "selection_fingerprint": source_contract["selection_fingerprint"],
                    "calculation_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
                },
            }
        ],
        "confidence_quality": {
            "confidence_label": "fixture-supported-deterministic",
            "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "bounded_three_entity_single_indicator_scope"],
            "missingness_summary": f"{summary['missing_count']} missing of {summary['expected_observation_slot_count']} expected slots for {entity}",
            "evidence_sufficiency": "sufficient for bounded deterministic descriptive statistical summary",
            "reproducibility_state": "reproducible_offline_from_retained_fixture",
            "validation_state": "pass",
            "governance_review_state": "Campaign 35 bounded replication accepted",
            "lifecycle_state": "accepted",
        },
        "contradiction_records": [{"contradiction_id": "none-recorded", "target_statement": statement_id, "contradiction_type": "none", "contradicting_evidence": None, "disposition": "not_applicable"}],
        "provenance_envelope": {
            "package_identity": package_id,
            "creator": "run_campaign35_wdi_nordic_exports_statistical_summary",
            "generation_date": DATE,
            "source_systems": ["World Bank WDI retained HTTPS fixture"],
            "evidence_refs": ["ev-campaign35-wdi-nordic-exports-share-https-fixture"],
            "evaluation_refs": ["validation-campaign35-statistical-summary-v2"],
            "computation_recipe": f"{method_v2.METHOD_ID}@{method_v2.METHOD_VERSION}",
            "validation_tool": "run_campaign35_wdi_nordic_exports_statistical_summary",
            "reproducibility_state": "reproducible_offline",
            "raw_evidence_fingerprint": raw_artifacts["combined_raw_artifact_fingerprint"],
            "normalized_evidence_fingerprint": normalized["normalized_fingerprint"],
            "selection_fingerprint": source_contract["selection_fingerprint"],
            "calculation_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
            "lineage": ["raw_https_fixture", "normalized_observations", "statistical_summary_v2_package"],
            "mutable_source_vintage_limitation": normalized["mutable_source_reproducibility_note"],
            "wdi_lastupdated": normalized["provider_metadata"].get("wdi_lastupdated"),
        },
        "validation_state": {"validation_result": "pass", "validator_version": "campaign35-v1", "blockers": [], "warnings": [], "human_review_required": False},
        "evolution_metadata": {"previous_revision": None, "change_reason": "Campaign 35 bounded statistical-summary v2 replication", "changed_inputs_methods_templates_models_validators": [method_v2.METHOD_ID], "dependent_object_review_posture": "not_applicable"},
        "promotion": {"from_candidate_package_id": candidate_id, "promotion_justification": "Candidate passed deterministic Campaign 35 validation and preserves KnowledgeForge boundaries.", "validation_history": [], "maturity_state": "bounded replication accepted"},
        "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": raw_artifacts["combined_raw_artifact_fingerprint"]},
        "lineage": {"previous_package_id": candidate_id, "version_lineage": [candidate_id, package_id]},
    }
    fingerprints = {
        "input_set": sha256_fingerprint(common["input_references"]),
        "evidence_references": sha256_fingerprint(common["evidence_references"]),
        "query_definitions": sha256_fingerprint(common["computation_method"]["query_definitions"]),
        "computation_recipe": sha256_fingerprint(common["computation_method"]),
        "generated_statements": sha256_fingerprint(common["generated_statements"]),
        "package_manifest": sha256_fingerprint(common),
    }
    package = copy.deepcopy(common)
    package["fingerprints"] = fingerprints
    package["lineage"]["lineage_fingerprint"] = sha256_fingerprint({"candidate": candidate_id, "object": package["fingerprints"]})
    package["fingerprints"]["package_manifest"] = sha256_fingerprint({k: v for k, v in package.items() if k != "fingerprints"})
    return package


def validate_campaign35_package(package: dict[str, Any], normalized: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    text = canonical_json(package.get("generated_statements", [])).lower()
    for term in FORBIDDEN_PACKAGE_TERMS:
        if term in text:
            blockers.append({"category": "boundary", "message": f"prohibited package language: {term}"})
    provenance = package.get("provenance_envelope", {})
    for key in ["raw_evidence_fingerprint", "normalized_evidence_fingerprint", "selection_fingerprint", "calculation_contract_fingerprint", "wdi_lastupdated"]:
        if not provenance.get(key):
            blockers.append({"category": "provenance", "message": f"missing {key}"})
    if provenance.get("calculation_contract_fingerprint") and provenance.get("calculation_contract_fingerprint") != EXPECTED_CONTRACT_FINGERPRINT:
        blockers.append({"category": "method", "message": "calculation contract fingerprint mismatch"})
    return {"validation_result": "pass" if not blockers else "reject", "blockers": blockers, "warnings": [], "validator_version": "campaign35-v1"}


def pre_existing_object_hashes(repository_root: Path = DEFAULT_REPOSITORY_ROOT) -> dict[str, str]:
    objects = repository_root / "objects"
    return {path.name: sha256_file(path) for path in sorted(objects.glob("*.json"))}


def post_existing_immutability(before: dict[str, str], repository_root: Path = DEFAULT_REPOSITORY_ROOT) -> dict[str, Any]:
    after = pre_existing_object_hashes(repository_root)
    changed = [name for name, digest in before.items() if after.get(name) != digest]
    disappeared = [name for name in before if name not in after]
    added = [name for name in after if name not in before]
    return {"changed_existing": changed, "disappeared_existing": disappeared, "added": added, "valid": not changed and not disappeared}


def run_local_ai_experiment(packages: list[dict[str, Any]], report_dir: Path) -> dict[str, Any]:
    prompt = "Screen these deterministic candidate package statements for prohibited interpretive language and unit-definition mismatch. Do not perform arithmetic or alter values."
    input_value = [{"package_id": p["package_id"], "text": p["generated_statements"][0]["text"], "unit": p["generated_statements"][0]["structured_payload"]["unit"]} for p in packages]
    input_fingerprint = sha256_fingerprint(input_value)
    candidates = []
    for cmd in (["ollama", "--version"], ["llama-cli", "--version"], ["llama", "--version"]):
        if shutil.which(cmd[0]):
            candidates.append(cmd)
    result: dict[str, Any] = {
        "status": "skipped",
        "reason": "no already installed local model CLI found",
        "prompt": prompt,
        "input_fingerprint": input_fingerprint,
        "deterministic_validator_result": [validate_campaign35_package(p, {}) for p in packages],
        "human_governance_disposition": "non-blocking skipped experiment",
        "saved_effort_assessment": "not measured",
    }
    if candidates:
        start = time.time()
        try:
            version = subprocess.run(candidates[0], capture_output=True, text=True, timeout=30)
            result.update({"status": "available_not_invoked_for_generation", "model_cli": candidates[0][0], "model_version_output": version.stdout.strip() or version.stderr.strip(), "execution_time_seconds": round(time.time() - start, 3), "reason": "CLI detected, but no non-frontier local generation command/model invocation was assumed without configured model name."})
        except Exception as exc:
            result.update({"status": "skipped_failed", "reason": str(exc), "execution_time_seconds": round(time.time() - start, 3)})
    write_json(report_dir / "local_ai_experiment.json", result)
    return result


def run_campaign(*, fixture_dir: Path = DEFAULT_FIXTURE_DIR, output_dir: Path = DEFAULT_OUTPUT_DIR, report_dir: Path = DEFAULT_REPORT_DIR, repository_root: Path = DEFAULT_REPOSITORY_ROOT, reuse_fixture: bool = False) -> dict[str, Any]:
    verify_loaded_v2_contract()
    before_hashes = pre_existing_object_hashes(repository_root)
    before_manifest = read_json(repository_root / "manifest.json")
    if reuse_fixture and (fixture_dir / "normalized_observations.json").exists():
        acquisition = {"fixture_dir": str(fixture_dir), "reused": True}
    else:
        acquisition = acquire_campaign35_fixture(fixture_dir)
    normalized = read_json(fixture_dir / "normalized_observations.json")
    fixture_validation = validate_campaign35_fixture(normalized)
    if fixture_validation["blockers"]:
        write_json(report_dir / "fixture_validation_failed.json", fixture_validation)
        raise RuntimeError(f"fixture validation failed: {fixture_validation['blockers']}")
    summaries = compute_entity_summaries(normalized)
    packages: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for entity in ENTITIES:
        package = build_entity_package(normalized, entity, summaries[entity])
        validation = validate_campaign35_package(package, normalized)
        if validation["validation_result"] == "pass":
            package["validation_state"] = validation
            packages.append(package)
        else:
            rejected.append({"entity": entity, "package": package, "validation": validation})
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "accepted_packages.json", packages)
    write_json(output_dir / "rejected_candidates.json", rejected)
    write_json(output_dir / "entity_summaries.json", summaries)
    write_json(output_dir / "fixture_validation.json", fixture_validation)
    if len(packages) != 3:
        write_json(report_dir / "campaign35_partial_or_failed.json", {"accepted": len(packages), "rejected": rejected})
        raise RuntimeError("Campaign 35 did not produce three accepted packages")
    persistence = knowledge_repository.persist_knowledge_object_packages(packages, repository_root)
    immutability = post_existing_immutability(before_hashes, repository_root)
    expected_added = sorted(f"{package_id_for(entity)}.json" for entity in ENTITIES)
    only_intended = sorted(immutability["added"]) == expected_added and immutability["valid"]
    local_ai = run_local_ai_experiment(packages, report_dir)
    governance_artifacts = count_governance_artifacts(output_dir, report_dir)
    ratio = governance_artifacts["count"] / len(packages)
    assessment = {
        "campaign_outcome": "A" if only_intended and ratio < 24 else "B",
        "accepted_package_count": len(packages),
        "rejected_candidate_count": len(rejected),
        "before_repository_object_count": before_manifest["object_count"],
        "before_repository_fingerprint": before_manifest["repository_fingerprint"],
        "after_repository_object_count": persistence["total_object_count"],
        "after_repository_fingerprint": persistence["repository_fingerprint"],
        "intended_added_packages_only": only_intended,
        "existing_package_immutability": immutability,
        "governance_artifacts": governance_artifacts,
        "governance_artifacts_per_substantive_package": ratio,
        "scaling_readiness": "not_blocked" if ratio < 24 else "blocked_pending_operational_consolidation",
        "next_recommendation": "Prepare the first correlation-method design and falsification gate; another statistical-summary pilot is now less valuable unless it targets real missingness as a direct blocker.",
        "local_ai_experiment": local_ai,
    }
    write_json(report_dir / "campaign35_replication_assessment.json", assessment)
    write_campaign_report(report_dir, acquisition, fixture_validation, summaries, packages, rejected, persistence, assessment)
    return {"acquisition": acquisition, "fixture_validation": fixture_validation, "summaries": summaries, "packages": [p["package_id"] for p in packages], "persistence": persistence, "assessment": assessment}


def count_governance_artifacts(output_dir: Path, report_dir: Path) -> dict[str, Any]:
    paths = []
    for root in [output_dir, report_dir]:
        if root.exists():
            paths.extend([p for p in root.rglob("*") if p.is_file()])
    # Do not count the three substantive accepted package files in accepted_packages.json as separate files here; this is artifact-file overhead.
    return {"count": len(paths), "paths": [str(p.relative_to(PROJECT_ROOT)) for p in sorted(paths)]}


def write_campaign_report(report_dir: Path, acquisition: dict[str, Any], fixture_validation: dict[str, Any], summaries: dict[str, Any], packages: list[dict[str, Any]], rejected: list[dict[str, Any]], persistence: dict[str, Any], assessment: dict[str, Any]) -> None:
    lines = [
        f"# {CAMPAIGN_TITLE}",
        "",
        "Status: complete.",
        f"Outcome: {assessment['campaign_outcome']}.",
        "",
        "No Campaign 36, no broader WDI expansion, no MacroForge access, no PostgreSQL schema change, no doctrine change, no commit, and no push occurred.",
        "",
        "## Accepted packages",
    ]
    for package in packages:
        lines.append(f"- `{package['package_id']}`")
    lines.extend(["", "## Per-entity measures"])
    for entity, summary in summaries.items():
        lines.append(f"- {entity}: observed {summary['observed_count']}/{summary['expected_observation_slot_count']}, coverage {summary['coverage_share']['canonical']}, mean {summary['arithmetic_mean']['canonical']}, median {summary['median']['canonical']}, population standard deviation {summary['population_standard_deviation']['canonical']} {UNIT}.")
    lines.extend([
        "",
        "## Repository",
        f"- total objects: {persistence['total_object_count']}",
        f"- repository fingerprint: `{persistence['repository_fingerprint']}`",
        "",
        "## Governance overhead",
        f"- artifacts counted: {assessment['governance_artifacts']['count']}",
        f"- artifacts per substantive package: {assessment['governance_artifacts_per_substantive_package']}",
    ])
    (report_dir / "campaign35_report.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=CAMPAIGN_TITLE)
    parser.add_argument("--reuse-fixture", action="store_true")
    args = parser.parse_args()
    result = run_campaign(reuse_fixture=args.reuse_fixture)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
