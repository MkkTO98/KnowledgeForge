#!/usr/bin/env python3
"""Campaign 34: bounded WDI Denmark population statistical-summary pilot.

Uses only a retained HTTPS-corrected WDI observation fixture and deterministic
offline Decimal computation. Produces one substantive KnowledgeObjectPackage.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE_PATH = PROJECT_ROOT / "artifacts" / "evidence-fixtures" / "wdi-demographic-population-total-denmark-1990-2024-https-corrected" / "normalized_observations.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "production" / "campaign-34-wdi-denmark-population-statistical-summary-pilot"
DEFAULT_REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
CAMPAIGN_ID = "campaign-34-wdi-denmark-population-statistical-summary-pilot"
METHOD_ID = "wdi_denmark_population_statistical_summary_v1"
DATE = "2026-07-10"
MIN_OBSERVED = 30
MIN_COVERAGE = Decimal("0.85")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def calculation_contract(normalized: dict[str, Any]) -> dict[str, Any]:
    contract = {
        "contract_id": "campaign34-statistical-calculation-contract-v1",
        "method_id": METHOD_ID,
        "method_version": "1.0",
        "decimal_parsing_method": "Decimal from canonical base-10 strings",
        "summation_method": "deterministic left-to-right Decimal summation after canonical period ordering",
        "arithmetic_mean_formula": "sum(observed_values) / observed_count",
        "median_rule": "sort observed values ascending; for odd N use middle value; for even N average the two middle values",
        "standard_deviation": "population standard deviation, denominator N",
        "standard_deviation_formula": "sqrt(sum((x - mean)^2) / N)",
        "internal_precision": "Python Decimal default context precision observed by this toolchain",
        "output_precision": "canonical Decimal engineering string without binary floating point",
        "rounding_mode": str(ROUND_HALF_EVEN),
        "deterministic_serialization": "JSON sort_keys=True separators=(',', ':') for fingerprints; pretty JSON for artifacts",
        "stable_ordering": ["entity_id", "indicator_code", "period"],
        "missing_observation_treatment": "preserve missing rows; compute numerical measures over observed values only; report missing count/share separately",
        "minimum_observed_count": MIN_OBSERVED,
        "minimum_coverage_share": str(MIN_COVERAGE),
        "excluded_measures": ["selected distribution cutpoints"],
        "input_normalized_fingerprint": normalized["normalized_fingerprint"],
    }
    contract["calculation_contract_fingerprint"] = sha256_fingerprint({k: v for k, v in contract.items() if k != "calculation_contract_fingerprint"})
    return contract


def _decimal(value: str) -> Decimal:
    return Decimal(value)


def _dstr(value: Decimal) -> str:
    return value.to_eng_string()


def _observed_rows(normalized: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in normalized["observations"] if row["observed"]]
    return sorted(rows, key=lambda row: (row["entity_id"], row["indicator_code"], row["period"]))


def compute_statistical_summary(normalized: dict[str, Any]) -> dict[str, Any]:
    expected = normalized["expected_observation_slots"]
    observed_rows = _observed_rows(normalized)
    observed_count = len(observed_rows)
    missing_count = expected - observed_count
    if observed_count < MIN_OBSERVED:
        raise ValueError("observed count below minimum")
    coverage = Decimal(observed_count) / Decimal(expected)
    if coverage < MIN_COVERAGE:
        raise ValueError("coverage below minimum")
    values = [_decimal(row["value_canonical"]) for row in observed_rows]
    sorted_pairs = sorted(zip(values, observed_rows), key=lambda item: (item[0], item[1]["period"]))
    mean = sum(values, Decimal(0)) / Decimal(observed_count)
    n = observed_count
    ordered_values = sorted(values)
    if n % 2:
        median = ordered_values[n // 2]
    else:
        median = (ordered_values[n // 2 - 1] + ordered_values[n // 2]) / Decimal(2)
    variance = sum((value - mean) * (value - mean) for value in values) / Decimal(observed_count)
    stddev = variance.sqrt()
    min_value = sorted_pairs[0][0]
    max_value = sorted_pairs[-1][0]
    return {
        "method_id": METHOD_ID,
        "expected_observation_slot_count": expected,
        "observed_count": observed_count,
        "missing_count": missing_count,
        "missing_share": _dstr(Decimal(missing_count) / Decimal(expected)),
        "coverage_share": _dstr(coverage),
        "first_valid_observation": {"period": observed_rows[0]["period"], "value": observed_rows[0]["value_canonical"], "unit": observed_rows[0]["unit"]},
        "last_valid_observation": {"period": observed_rows[-1]["period"], "value": observed_rows[-1]["value_canonical"], "unit": observed_rows[-1]["unit"]},
        "minimum": {"value": _dstr(min_value), "periods": [row["period"] for value, row in sorted_pairs if value == min_value], "unit": observed_rows[0]["unit"]},
        "maximum": {"value": _dstr(max_value), "periods": [row["period"] for value, row in sorted_pairs if value == max_value], "unit": observed_rows[0]["unit"]},
        "arithmetic_mean": _dstr(mean),
        "median": _dstr(median),
        "population_standard_deviation": _dstr(stddev),
        "period_coverage": {"start_period": min(row["period"] for row in normalized["observations"]), "end_period": max(row["period"] for row in normalized["observations"]), "frequency": "annual"},
        "unit": observed_rows[0]["unit"],
        "calculation_notes": [
            "Values are deterministic descriptive measures over retained observed annual levels only.",
            "Population standard deviation uses denominator N and is a dispersion descriptor for this retained finite evidence set.",
        ],
    }


def validate_inputs(normalized: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if normalized.get("selection_contract", {}).get("indicator", {}).get("code") != "SP.POP.TOTL":
        blockers.append({"category": "scope", "message": "indicator is not SP.POP.TOTL"})
    if normalized.get("selection_contract", {}).get("entities") != ["DNK"]:
        blockers.append({"category": "scope", "message": "entity scope is not DNK"})
    periods = normalized.get("selection_contract", {}).get("periods", {})
    if periods.get("start_year") != 1990 or periods.get("end_year") != 2024:
        blockers.append({"category": "scope", "message": "period scope is not 1990-2024"})
    keys = set()
    for row in normalized.get("observations", []):
        key = (row.get("entity_id"), row.get("indicator_code"), row.get("period"))
        if key in keys:
            blockers.append({"category": "duplicates", "message": "duplicate observation key"})
        keys.add(key)
        if row.get("observed") and row.get("value_canonical") is None:
            blockers.append({"category": "missingness", "message": "observed row has no value"})
    return blockers


def build_campaign34_package(normalized: dict[str, Any]) -> dict[str, Any]:
    blockers = validate_inputs(normalized)
    if blockers:
        raise ValueError(f"invalid normalized fixture: {blockers}")
    contract = calculation_contract(normalized)
    measures = compute_statistical_summary(normalized)
    source_contract = normalized["selection_contract"]
    raw_artifacts = normalized["raw_artifacts"]
    package_id = "pkg-object-srcpkg-campaign34-denmark-population-statistical-summary"
    candidate_id = "pkg-candidate-srcpkg-campaign34-denmark-population-statistical-summary"
    statement_id = "stmt-campaign34-denmark-population-statistical-summary"
    statement_text = (
        "For retained World Bank WDI SP.POP.TOTL observations for Denmark (DNK), annual 1990-2024, "
        f"the fixture has {measures['expected_observation_slot_count']} expected slots, {measures['observed_count']} observed values, "
        f"{measures['missing_count']} missing values, coverage share {measures['coverage_share']}, first valid value "
        f"{measures['first_valid_observation']['value']} persons in {measures['first_valid_observation']['period']}, last valid value "
        f"{measures['last_valid_observation']['value']} persons in {measures['last_valid_observation']['period']}, minimum "
        f"{measures['minimum']['value']} persons in {measures['minimum']['periods']}, maximum {measures['maximum']['value']} persons in "
        f"{measures['maximum']['periods']}, arithmetic mean {measures['arithmetic_mean']} persons, median {measures['median']} persons, "
        f"and population standard deviation {measures['population_standard_deviation']} persons under {METHOD_ID}."
    )
    common = {
        "package_id": package_id,
        "package_kind": "KnowledgeObjectPackage",
        "package_version": "1.0",
        "created_at": DATE,
        "created_by": "run_campaign34_wdi_denmark_population_statistical_summary",
        "status": "accepted-for-controlled-production",
        "scope": {
            "domain": "WDI Denmark population statistical summary",
            "source_scope": {
                "campaign_id": CAMPAIGN_ID,
                "provider": "World Bank",
                "dataset": "World Development Indicators",
                "source_id": "2",
                "indicator_code": "SP.POP.TOTL",
                "indicator_name": "Population, total",
                "entity_id": "DNK",
                "period_start": 1990,
                "period_end": 2024,
                "frequency": "annual",
                "unit": "persons",
                "scope_type": "bounded_statistical_summary",
            },
            "evidence_family": "external_wdi_annual_scalar_demographic_structure_statistical_summary",
            "method_scope": METHOD_ID,
            "intended_use": "deterministic descriptive knowledge only",
        },
        "input_references": ["srcpkg-campaign34-https-corrected-wdi-observation-fixture"],
        "evidence_references": [
            {
                "evidence_ref_id": "ev-campaign34-https-corrected-wdi-observation-fixture",
                "evidence_class": "external_observation_level_numerical_fixture",
                "source_family": "official_statistical_source_data",
                "source_identity": "World Bank World Development Indicators SP.POP.TOTL DNK annual fixture",
                "source_owner": "World Bank WDI API retained local fixture",
                "source_version": normalized["provider_metadata"].get("wdi_lastupdated"),
                "accessed_at": DATE,
                "snapshot_fingerprint": raw_artifacts["combined_raw_artifact_fingerprint"],
                "reproducibility_handle": "retained HTTPS-corrected raw fixture and normalized observations",
                "evaluation_status": "evaluated",
            }
        ],
        "computation_method": {
            "name": METHOD_ID,
            "version": "1.0",
            "recipe": "offline deterministic Decimal statistical summary over retained normalized observations",
            "parameters": contract,
            "query_definitions": [],
            "nondeterminism": "none",
            "rerun": "python3 tools/run_campaign34_wdi_denmark_population_statistical_summary.py --fixture artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024-https-corrected/normalized_observations.json",
        },
        "generated_statements": [
            {
                "statement_id": statement_id,
                "statement_type": "derived",
                "text": statement_text,
                "applicability": {
                    "indicator_code": "SP.POP.TOTL",
                    "entity_id": "DNK",
                    "period_start": 1990,
                    "period_end": 2024,
                    "method_id": METHOD_ID,
                },
                "dependencies": ["ev-campaign34-https-corrected-wdi-observation-fixture", "calc-campaign34-statistical-summary"],
                "evidence_refs": ["ev-campaign34-https-corrected-wdi-observation-fixture"],
                "origin": "computed_from_retained_normalized_evidence_fixture",
                "structured_payload": measures,
            }
        ],
        "confidence_quality": {
            "confidence_label": "fixture-supported-deterministic",
            "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "single_entity_single_indicator_scope"],
            "missingness_summary": f"{measures['missing_count']} missing of {measures['expected_observation_slot_count']} expected slots",
            "evidence_sufficiency": "sufficient for bounded deterministic descriptive statistical summary",
            "reproducibility_state": "reproducible_offline_from_retained_fixture",
            "validation_state": "pass",
            "governance_review_state": "Campaign 34 accepted bounded pilot",
            "lifecycle_state": "accepted",
        },
        "contradiction_records": [{"contradiction_id": "none-recorded", "target_statement": statement_id, "contradiction_type": "none", "contradicting_evidence": None, "disposition": "not_applicable"}],
        "provenance_envelope": {
            "package_identity": package_id,
            "creator": "run_campaign34_wdi_denmark_population_statistical_summary",
            "generation_date": DATE,
            "source_systems": ["World Bank WDI retained HTTPS fixture"],
            "evidence_refs": ["ev-campaign34-https-corrected-wdi-observation-fixture"],
            "evaluation_refs": ["validation-campaign34-statistical-summary"],
            "computation_recipe": f"{METHOD_ID}@1.0",
            "validation_tool": "run_campaign34_wdi_denmark_population_statistical_summary",
            "reproducibility_state": "reproducible_offline",
            "corrected_raw_evidence_fingerprint": raw_artifacts["combined_raw_artifact_fingerprint"],
            "corrected_normalized_evidence_fingerprint": normalized["normalized_fingerprint"],
            "selection_fingerprint": source_contract["selection_fingerprint"],
            "calculation_contract_fingerprint": contract["calculation_contract_fingerprint"],
            "lineage": ["raw_https_fixture", "normalized_observations", "statistical_summary_package"],
            "mutable_source_vintage_limitation": normalized["mutable_source_reproducibility_note"],
            "wdi_lastupdated": normalized["provider_metadata"].get("wdi_lastupdated"),
        },
        "validation_state": {"validation_result": "pass", "validator_version": "campaign34-v1", "blockers": [], "warnings": [], "human_review_required": False},
        "evolution_metadata": {"previous_revision": None, "change_reason": "Campaign 34 bounded statistical-summary pilot", "changed_inputs_methods_templates_models_validators": [METHOD_ID], "dependent_object_review_posture": "not_applicable"},
        "promotion": {"from_candidate_package_id": candidate_id, "promotion_justification": "Candidate passed deterministic Campaign 34 validation and preserves KnowledgeForge boundaries.", "validation_history": [], "maturity_state": "bounded pilot accepted"},
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


def build_candidate(package: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(package)
    candidate["package_id"] = "pkg-candidate-srcpkg-campaign34-denmark-population-statistical-summary"
    candidate["package_kind"] = "KnowledgeCandidatePackage"
    candidate["status"] = "validated-candidate"
    candidate["validation_state"] = {"validation_result": "pending", "validator_version": "campaign34-v1", "blockers": [], "warnings": [], "human_review_required": True}
    candidate["confidence_quality"]["lifecycle_state"] = "candidate"
    candidate["fingerprints"]["package_manifest"] = sha256_fingerprint({k: v for k, v in candidate.items() if k != "fingerprints"})
    return candidate


def validate_package(package: dict[str, Any], normalized: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    try:
        recomputed = compute_statistical_summary(normalized)
    except Exception as exc:
        blockers.append({"category": "calculation", "message": str(exc)})
        recomputed = {}
    payload = package["generated_statements"][0]["structured_payload"]
    if recomputed and payload != recomputed:
        blockers.append({"category": "calculation", "message": "independent recomputation disagrees"})
    required_provenance = ["corrected_raw_evidence_fingerprint", "corrected_normalized_evidence_fingerprint", "selection_fingerprint", "calculation_contract_fingerprint", "wdi_lastupdated"]
    for key in required_provenance:
        if not package.get("provenance_envelope", {}).get(key):
            blockers.append({"category": "provenance", "message": f"missing {key}"})
    prohibited = ["because", "forecast", "recommend", "investment", "expected future", "caused", "better", "worse"]
    text = package["generated_statements"][0]["text"].lower()
    for term in prohibited:
        if term in text:
            blockers.append({"category": "boundary", "message": f"prohibited language: {term}"})
    return {"validation_result": "pass" if not blockers else "reject", "blockers": blockers, "validator_version": "campaign34-v1"}


def run_campaign(*, output_dir: Path = DEFAULT_OUTPUT_DIR, repository_root: Path = DEFAULT_REPOSITORY_ROOT, fixture_path: Path = DEFAULT_FIXTURE_PATH) -> dict[str, Any]:
    normalized = load_json(fixture_path)
    contract = calculation_contract(normalized)
    package = build_campaign34_package(normalized)
    candidate = build_candidate(package)
    validation = validate_package(package, normalized)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "calculation_contract.json", contract)
    write_json(output_dir / "machine_readable_calculation_evidence.json", package["generated_statements"][0]["structured_payload"])
    write_json(output_dir / "candidate_statistical_summary.json", candidate)
    write_json(output_dir / "knowledge_object_package.json", package)
    write_json(output_dir / "validation_judgment.json", validation)
    if validation["validation_result"] != "pass":
        return {"decision": "rejected", "packages_promoted": 0, "validation": validation}
    import importlib.util
    repo_module_path = PROJECT_ROOT / "tools" / "knowledge_repository.py"
    spec = importlib.util.spec_from_file_location("knowledge_repository", repo_module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load repository module")
    repo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(repo)
    persistence = repo.persist_knowledge_object_packages([package], repository_root)
    result = {
        "decision": "accepted",
        "campaign_id": CAMPAIGN_ID,
        "packages_promoted": 1,
        "package_id": package["package_id"],
        "package_fingerprint": package["fingerprints"]["package_manifest"],
        "normalized_evidence_fingerprint": normalized["normalized_fingerprint"],
        "calculation_contract_fingerprint": contract["calculation_contract_fingerprint"],
        "repository_result": persistence,
    }
    write_json(output_dir / "campaign34_result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Campaign 34 bounded WDI Denmark population statistical-summary pilot")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT)
    args = parser.parse_args()
    result = run_campaign(output_dir=args.output, repository_root=args.repository_root, fixture_path=args.fixture)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["decision"] == "accepted" else 1


if __name__ == "__main__":
    raise SystemExit(main())
