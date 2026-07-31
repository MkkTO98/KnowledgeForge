#!/usr/bin/env python3
"""Bounded Evidence Portfolio production pilot.

This module composes existing KnowledgeForge contracts. It does not define a new
canonical ontology: one accepted KnowledgeObjectPackage remains canonical per
source series, while result records are operational Evidence-Card-equivalent
views. Inputs are retained Campaign 40 WDI fixtures and are always read-only.
"""
from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import date
from decimal import Decimal, Context, ROUND_HALF_EVEN, localcontext
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

import deterministic_statistical_summary_v2 as summary_v2
import knowledge_repository
from validate_knowledge_pipeline_v1 import validate_knowledge_object

CAMPAIGN_ID = "evidence-portfolio-pilot-health-baseline-20260730"
MANIFEST_ID = "manifest-evidence-portfolio-pilot-health-baseline-v1"
BUNDLE_ID = "bundle-health-norway-annual-1990-2024-v1"
METHOD_ID = "baseline_characterization_portfolio_v1"
METHOD_VERSION = "1.0"
DATE = "2026-07-30"
EXPECTED_RESULT_RECORDS = 28
SUMMARY_CONTRACT_FINGERPRINT = "sha256:80e6b07fd98faf37401103776b6ef82f4ab981c5ea890b381b036058c460e8a0"
FIXTURE_ROOT = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "artifacts/production/evidence-portfolio-pilot-health-baseline-20260730"
DEFAULT_REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
CANDIDATE_REGISTRY = PROJECT_ROOT / "artifacts/reports/campaign40-spec-driven-pearson-production-20260711/selection/candidate_registry.json"
FORBIDDEN_OUTCOME_FIELDS = ["calculated_value", "interesting", "attractive", "coefficient", "significance", "result_rank"]
FORBIDDEN_CLAIM_TERMS = ["causes", "because", "predicts", "forecast", "recommend", "investment implication", "statistically significant"]
AUTHORIZATION_SCHEMA = "knowledgeforge.evidence_portfolio.production_authorization.v1"
AUTHORIZATION_VERSION = "1.0"
REQUIRED_PORTFOLIO_LIMITS = {
    "maximum_executed_candidates": 2,
    "maximum_raw_result_records": 56,
    "maximum_promoted_objects": 2,
    "stop_on_canary_failure": True,
}
REQUIRED_ENTRY_LIMITS = {"maximum_result_records": 28, "maximum_wall_seconds": 5}

SERIES = [
    {
        "code": "SP.DYN.LE00.IN",
        "name": "Life expectancy at birth, total (years)",
        "unit": "years",
        "denominator_basis": "not_applicable_duration_measure_years",
        "definition": "Expected years of life at birth under the period mortality schedule represented by the retained WDI series.",
        "canary": True,
    },
    {
        "code": "SH.DYN.MORT",
        "name": "Mortality rate, under-5 (per 1,000 live births)",
        "unit": "per 1,000 live births",
        "denominator_basis": "live_births_scaled_per_1000",
        "definition": "Probability per 1,000 live births of dying before age five under the retained WDI series definition.",
        "canary": False,
    },
]

RESULT_SPEC = [
    ("coverage_missingness", "expected_observation_slot_count"),
    ("coverage_missingness", "observed_count"),
    ("coverage_missingness", "missing_count"),
    ("coverage_missingness", "coverage_share"),
    ("coverage_missingness", "missing_share"),
    ("sample_period", "period_start"),
    ("sample_period", "period_end"),
    ("sample_period", "first_valid_observation"),
    ("sample_period", "last_valid_observation"),
    ("sample_period", "observed_period_span_years"),
    ("level_distribution", "minimum"),
    ("level_distribution", "maximum"),
    ("level_distribution", "arithmetic_mean"),
    ("level_distribution", "median"),
    ("level_distribution", "population_standard_deviation"),
    ("level_distribution", "first_quartile"),
    ("level_distribution", "third_quartile"),
    ("level_distribution", "interquartile_range"),
    ("differences", "adjacent_first_difference_count"),
    ("differences", "first_difference_mean"),
    ("differences", "first_difference_median"),
    ("differences", "first_difference_minimum"),
    ("differences", "first_difference_maximum"),
    ("differences", "net_level_difference"),
    ("trend_descriptor", "linear_time_index_slope_per_year"),
    ("trend_descriptor", "linear_time_index_slope_sign"),
    ("variability_stability", "first_difference_population_standard_deviation"),
    ("variability_stability", "mean_absolute_first_difference"),
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_fingerprint(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def manifest_bytes_fingerprint(manifest: dict[str, Any]) -> str:
    """Fingerprint the deterministic bytes used by an explicit in-memory invocation."""
    return "sha256:" + hashlib.sha256(canonical_json(manifest).encode("utf-8")).hexdigest()


def resolve_manifest_input(project_root: Path, raw_path: Any) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError("manifest input path must be a nonempty repository-relative string")
    relative = Path(raw_path)
    if relative.is_absolute():
        raise ValueError("manifest input path must not be absolute")
    if ".." in relative.parts:
        raise ValueError("manifest input path must not contain parent traversal")
    root = project_root.resolve(strict=True)
    try:
        resolved = (root / relative).resolve(strict=True)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        raise ValueError(f"manifest input path does not resolve to an existing file: {raw_path}") from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("manifest input path escapes repository root") from exc
    if not resolved.is_file():
        raise ValueError("manifest input path must resolve to a regular file")
    return resolved


def resolve_and_fingerprint_manifest_input(project_root: Path, raw_path: Any) -> tuple[Path, str]:
    path = resolve_manifest_input(project_root, raw_path)
    return path, file_fingerprint(path)


def candidate_population(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    population = []
    for entry in manifest["entries"]:
        input_ref = entry.get("input", {})
        population.append({
            "candidate_id": entry["candidate_id"],
            "disposition": entry["disposition"],
            "canary": entry.get("canary") is True,
            "input_path": input_ref.get("path"),
            "input_sha256": input_ref.get("sha256"),
            "input_normalized_fingerprint": input_ref.get("normalized_fingerprint"),
        })
    return population


def production_limits(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "portfolio": copy.deepcopy(manifest["computational_budget"]),
        "entries": [{"candidate_id": entry["candidate_id"], "limits": copy.deepcopy(entry["computational_budget"])} for entry in manifest["entries"]],
    }


def expected_canary_accounting(manifest: dict[str, Any]) -> dict[str, Any]:
    selected = [entry for entry in manifest["entries"] if entry.get("canary") is True]
    executable = [entry for entry in selected if entry.get("disposition") == "execute"]
    rejected = len(selected) - len(executable)
    result_count = sum(entry["computational_budget"]["maximum_result_records"] for entry in executable)
    return {
        "manifest_candidates": len(selected), "executed_candidates": len(executable),
        "valid_candidates": len(executable), "null_candidates": 0, "rejected_candidates": rejected,
        "execution_failures": 0, "raw_calculation_results": result_count, "valid_result_records": result_count,
        "promoted_canonical_objects": len(executable), "operational_views": result_count,
        "distinct_source_series": len(executable), "distinct_transformations": 3 if executable else 0,
        "evidence_bundles": len({entry["bundle_id"] for entry in executable}),
        "dependency_clusters": len(executable), "redundant_candidates": 0, "redundant_result_records": 0,
    }


def authorization_fingerprint(gate: dict[str, Any]) -> str:
    return fingerprint({key: value for key, value in gate.items() if key != "gate_fingerprint"})


def build_production_authorization(
    manifest: dict[str, Any], execution_manifest_byte_fingerprint: str, *, accounting: dict[str, Any],
    reruns: list[dict[str, Any]], publication: dict[str, Any] | None, passed: bool = True,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    population = candidate_population(manifest)
    gate = {
        "schema_name": AUTHORIZATION_SCHEMA, "schema_version": AUTHORIZATION_VERSION,
        "campaign_id": manifest["campaign_id"], "manifest_id": manifest["manifest_id"],
        "execution_manifest_byte_fingerprint": execution_manifest_byte_fingerprint,
        "manifest_fingerprint": manifest["manifest_fingerprint"],
        "candidate_population": population, "candidate_population_fingerprint": fingerprint(population),
        "production_limits": production_limits(manifest), "execution_mode": "canary",
        "passed": passed, "blockers": list(blockers or []), "accounting": copy.deepcopy(accounting),
        "reruns": copy.deepcopy(reruns), "publication": copy.deepcopy(publication),
    }
    gate["gate_fingerprint"] = authorization_fingerprint(gate)
    return gate


def validate_production_authorization(
    gate: Any, manifest: dict[str, Any], execution_manifest_byte_fingerprint: str,
    current_repository_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(gate, dict):
        raise ValueError("production authorization top-level value must be a JSON object")
    required = {"schema_name", "schema_version", "campaign_id", "manifest_id", "execution_manifest_byte_fingerprint", "manifest_fingerprint", "candidate_population", "candidate_population_fingerprint", "production_limits", "execution_mode", "passed", "blockers", "accounting", "reruns", "publication", "gate_fingerprint"}
    missing = sorted(required - set(gate))
    if missing:
        raise ValueError(f"production authorization missing fields: {missing}")
    if gate["schema_name"] != AUTHORIZATION_SCHEMA or gate["schema_version"] != AUTHORIZATION_VERSION:
        raise ValueError("production authorization schema or version mismatch")
    if type(gate["passed"]) is not bool or gate["passed"] is not True:
        raise ValueError("production authorization passed must be the JSON Boolean true")
    if gate["execution_mode"] != "canary":
        raise ValueError("production authorization execution mode must be literal canary")
    if gate["gate_fingerprint"] != authorization_fingerprint(gate):
        raise ValueError("production authorization gate fingerprint mismatch")
    expected = {
        "campaign_id": manifest["campaign_id"], "manifest_id": manifest["manifest_id"],
        "execution_manifest_byte_fingerprint": execution_manifest_byte_fingerprint,
        "manifest_fingerprint": manifest["manifest_fingerprint"],
        "candidate_population": candidate_population(manifest), "production_limits": production_limits(manifest),
    }
    for key, value in expected.items():
        if gate[key] != value:
            raise ValueError(f"production authorization {key} binding mismatch")
    if gate["candidate_population_fingerprint"] != fingerprint(gate["candidate_population"]):
        raise ValueError("production authorization candidate population fingerprint mismatch")
    if gate["blockers"] != []:
        raise ValueError("production authorization blockers must be empty")
    if gate["accounting"] != expected_canary_accounting(manifest):
        raise ValueError("production authorization canary accounting mismatch")
    expected_rerun_ids = [entry["candidate_id"] for entry in manifest["entries"] if entry.get("canary") is True and entry.get("disposition") == "execute"]
    reruns = gate["reruns"]
    if not isinstance(reruns, list) or [row.get("candidate_id") for row in reruns if isinstance(row, dict)] != expected_rerun_ids:
        raise ValueError("production authorization deterministic rerun population mismatch")
    rerun_keys = {"candidate_id", "matched", "first_fingerprint", "second_fingerprint"}
    sha256_pattern = re.compile(r"^sha256:[0-9a-f]{64}$")
    if any(
        not isinstance(row, dict)
        or set(row) != rerun_keys
        or type(row.get("matched")) is not bool
        or row["matched"] is not True
        or not isinstance(row.get("first_fingerprint"), str)
        or not isinstance(row.get("second_fingerprint"), str)
        or sha256_pattern.fullmatch(row["first_fingerprint"]) is None
        or row["first_fingerprint"] != row["second_fingerprint"]
        for row in reruns
    ):
        raise ValueError("production authorization deterministic rerun accounting invalid")
    if (
        not isinstance(gate["publication"], dict)
        or gate["publication"].get("disposition") != "isolated_canary_admitted"
        or gate["publication"].get("admitted_object_count") != len(expected_rerun_ids)
        or type(gate["publication"].get("object_count")) is not int
        or gate["publication"]["object_count"] < len(expected_rerun_ids)
        or not isinstance(gate["publication"].get("repository_fingerprint"), str)
        or sha256_pattern.fullmatch(gate["publication"]["repository_fingerprint"]) is None
    ):
        raise ValueError("production authorization publication disposition invalid")
    expected_repository_state = {
        "object_count": gate["publication"]["object_count"],
        "repository_fingerprint": gate["publication"]["repository_fingerprint"],
    }
    if current_repository_state != expected_repository_state:
        raise ValueError("production authorization repository state does not match canary-admitted state")
    return {"valid": True, "schema_name": AUTHORIZATION_SCHEMA, "campaign_id": manifest["campaign_id"], "repository_state": expected_repository_state}


def enforce_preexecution_limits(manifest: dict[str, Any], selected: list[dict[str, Any]]) -> None:
    count = sum(1 for entry in selected if entry.get("disposition") == "execute")
    maximum = manifest["computational_budget"]["maximum_executed_candidates"]
    if count > maximum:
        raise ValueError(f"executed candidate limit exceeded before calculation: {count} > {maximum}")


def enforce_candidate_result_limits(entry: dict[str, Any], result: dict[str, Any], elapsed_wall_seconds: float) -> None:
    maximum_records = entry["computational_budget"]["maximum_result_records"]
    if int(result.get("raw_result_count", 0)) > maximum_records or int(result.get("valid_result_count", 0)) > maximum_records:
        raise ValueError("candidate result record limit exceeded before admission or promotion")
    maximum_seconds = entry["computational_budget"]["maximum_wall_seconds"]
    if elapsed_wall_seconds > maximum_seconds:
        raise ValueError(f"candidate wall time exceeded after calculation; admission and promotion blocked: {elapsed_wall_seconds:.6f} > {maximum_seconds}")


def enforce_aggregate_result_limit(manifest: dict[str, Any], outcomes: list[dict[str, Any]]) -> None:
    produced = sum(int(outcome.get("raw_result_count", 0)) for outcome in outcomes)
    maximum = manifest["computational_budget"]["maximum_raw_result_records"]
    if produced > maximum:
        raise ValueError(f"aggregate raw result record limit exceeded before admission or persistence: {produced} > {maximum}")


def enforce_promotion_limit(manifest: dict[str, Any], packages: list[dict[str, Any]]) -> None:
    maximum = manifest["computational_budget"]["maximum_promoted_objects"]
    if len(packages) > maximum:
        raise ValueError(f"promoted object limit exceeded before canonical writes: {len(packages)} > {maximum}")


def _slug(code: str) -> str:
    return code.lower().replace(".", "-")


LEGACY_HEALTH_FAMILY_CONFIGURATION = {
    "family": "Health",
    "family_slug": "health",
    "domain": "WDI Health baseline characterization",
    "evidence_family": "external_wdi_annual_scalar_health_baseline_characterization",
    "result_limitations": ["finite retained ordered annual sequence", "descriptive only", "no causal predictive significance stationarity or permanence claim"],
    "package_limitations": ["No cross-series comparison or relationship is calculated.", "Slope sign is a finite-window time-index descriptor, not evidence of structural trend, stationarity or forecastability.", "First differences summarize consecutive retained annual values only.", "WDI reacquisition may change; retained local bytes are the replay anchor.", "Canonical decimal precision is not measurement precision."],
    "applicability_limitations": [],
    "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "modeled_estimation_process", "bounded_single_territory_window"],
    "governance_review_state": "bounded pilot promotion contract passed",
    "evolution_change_reason": "first bounded Evidence Portfolio production pilot",
    "promotion_maturity_state": "bounded portfolio pilot accepted",
    "generation_date": "2026-07-30",
}
LEGACY_HEALTH_ENTRY_IDENTITIES = {
    (
        "candidate-health-sp-dyn-le00-in-nor-1990-2024-baseline-v1",
        "execute",
        "SP.DYN.LE00.IN",
        METHOD_ID,
        METHOD_VERSION,
    ),
    (
        "candidate-health-sh-dyn-mort-nor-1990-2024-baseline-v1",
        "execute",
        "SH.DYN.MORT",
        METHOD_ID,
        METHOD_VERSION,
    ),
    (
        "candidate-health-life-expectancy-cagr-excluded-v1",
        "excluded_pre_execution",
        "SP.DYN.LE00.IN",
        "compound_annual_growth_rate",
        "not_registered",
    ),
}
LEGACY_HEALTH_ENTRY_FINGERPRINTS = {
    "candidate-health-sp-dyn-le00-in-nor-1990-2024-baseline-v1": "sha256:75c18911c501467c4f4d5d89e791adff4afc5768b24d033ac9401ac71a47062c",
    "candidate-health-sh-dyn-mort-nor-1990-2024-baseline-v1": "sha256:f542c10af16cc139a5eeac659c9b7fa2d2e3b56369067221340cc8bb3b8e24eb",
    "candidate-health-life-expectancy-cagr-excluded-v1": "sha256:9d04cce19c8728e0e07e8ec57c8e8a85109ba92713aa078e11121bf34f8d30e8",
}
LEGACY_HEALTH_INPUTS = {
    "SP.DYN.LE00.IN": {
        "path": "artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https/SP.DYN.LE00.IN__NOR__1990-2024/normalized_observations.json",
        "sha256": "sha256:bcbed15f37c0208fd80641ac280e9279f38968b2229fa9a7cdf3efbb685d5728",
        "normalized_fingerprint": "sha256:83d74ce0f508ec88a4a841fdea817725e1c022ee71ac42a6a5895d3b775e2f27",
    },
    "SH.DYN.MORT": {
        "path": "artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https/SH.DYN.MORT__NOR__1990-2024/normalized_observations.json",
        "sha256": "sha256:6e3ca56274f18bf710383d5c438fa89d15680e3405f8d1045456855c67a5b411",
        "normalized_fingerprint": "sha256:15a09202c1263ed917c780d7557bb353f9183271b4840b25b2a4c368a1df922e",
    },
}
LEGACY_HEALTH_DEFINITIONS = {series["code"]: series["definition"] for series in SERIES}
LEGACY_HEALTH_METADATA_DEFINITIONS = {
    "SP.DYN.LE00.IN": "Life expectancy at birth indicates the number of years a newborn infant would live if prevailing patterns of mortality at the time of its birth were to stay the same throughout its life.",
    "SH.DYN.MORT": "Under-five mortality rate is the probability per 1,000 that a newborn baby will die before reaching age five, if subject to age-specific mortality rates of the specified year.",
}
FAMILY_CONFIGURATION_FIELDS = set(LEGACY_HEALTH_FAMILY_CONFIGURATION)


def _is_published_legacy_health_entry(entry: dict[str, Any]) -> bool:
    """Match one immutable, field-complete published Norway entry identity."""
    if not isinstance(entry, dict):
        return False
    candidate_id = entry.get("candidate_id")
    expected_fingerprint = LEGACY_HEALTH_ENTRY_FINGERPRINTS.get(candidate_id)
    identity = (
        candidate_id,
        entry.get("disposition"),
        entry.get("indicator", {}).get("code"),
        entry.get("method", {}).get("id"),
        entry.get("method", {}).get("version"),
    )
    return (
        expected_fingerprint is not None
        and identity in LEGACY_HEALTH_ENTRY_IDENTITIES
        and fingerprint(entry) == expected_fingerprint
    )


def _safe_family_slug(family: str) -> str:
    if not isinstance(family, str) or re.fullmatch(r"[A-Z][A-Za-z0-9]*(?: [A-Z][A-Za-z0-9]*)*", family) is None:
        raise ValueError("family configuration family must use the closed family-name grammar")
    return family.lower().replace(" ", "-")


def _validate_entry_identifiers(entry: dict[str, Any], config: dict[str, Any]) -> str:
    indicator_code = entry.get("indicator", {}).get("code")
    territory_id = entry.get("territory", {}).get("id")
    if not isinstance(indicator_code, str) or re.fullmatch(r"[A-Z0-9]+(?:\.[A-Z0-9]+)*", indicator_code) is None:
        raise ValueError("indicator identifier does not use the accepted grammar")
    indicator_slug = _slug(indicator_code)
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", indicator_slug) is None:
        raise ValueError("indicator-derived slug does not use the accepted grammar")
    if not isinstance(territory_id, str) or re.fullmatch(r"[A-Z0-9][A-Z0-9_-]*", territory_id) is None:
        raise ValueError("territory identifier does not use the accepted grammar")
    identity = entry.get("identity_inputs", {})
    package_id = (
        f"pkg-object-eppilot-{config['family_slug']}-{indicator_slug}-"
        f"{territory_id.lower()}-{identity.get('period_start')}-{identity.get('period_end')}-baseline-v1"
    )
    if re.fullmatch(r"[a-z0-9][a-z0-9_-]*", package_id) is None:
        raise ValueError("final package identifier does not use the accepted grammar")
    return package_id


def family_configuration(entry: dict[str, Any]) -> dict[str, Any]:
    """Return closed rendering configuration; only published Health v1 may omit it."""
    configured = entry.get("family_configuration")
    if configured is None:
        if _is_published_legacy_health_entry(entry):
            return copy.deepcopy(LEGACY_HEALTH_FAMILY_CONFIGURATION)
        raise ValueError("family configuration is required outside the exact published Norway Health portfolio")
    if not isinstance(configured, dict) or set(configured) != FAMILY_CONFIGURATION_FIELDS:
        raise ValueError("family configuration must contain the complete normative field set")
    if configured.get("family") != entry.get("indicator", {}).get("family"):
        raise ValueError("family configuration family is inconsistent with indicator family")
    list_fields = {"result_limitations", "package_limitations", "applicability_limitations", "uncertainty_dimensions"}
    if any(not isinstance(configured.get(key), str) or not configured[key] for key in FAMILY_CONFIGURATION_FIELDS - list_fields):
        raise ValueError("family configuration scalar fields must be nonempty strings")
    for key in list_fields:
        if not isinstance(configured.get(key), list) or not configured[key] or any(not isinstance(value, str) or not value for value in configured[key]):
            raise ValueError(f"family configuration {key} must be a nonempty string list")
    family = configured["family"]
    family_slug = _safe_family_slug(family)
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", configured["family_slug"]) is None:
        raise ValueError("family configuration family_slug does not use the accepted safe grammar")
    if configured["family_slug"] != family_slug:
        raise ValueError("family configuration family_slug is not deterministically bound to family")
    expected = {
        "domain": f"WDI {family} baseline characterization",
        "evidence_family": f"external_wdi_annual_scalar_{family_slug.replace('-', '_')}_baseline_characterization",
        "governance_review_state": "bounded pilot promotion contract passed" if family == "Health" else f"bounded {family} portfolio promotion contract passed",
        "promotion_maturity_state": "bounded portfolio pilot accepted" if family == "Health" else f"bounded {family} portfolio pilot accepted",
    }
    if any(configured[key] != value for key, value in expected.items()):
        raise ValueError("family configuration is not semantically bound to its declared family")
    try:
        parsed_date = date.fromisoformat(configured["generation_date"])
    except ValueError as exc:
        raise ValueError("family configuration generation_date must be a valid ISO date") from exc
    if parsed_date.isoformat() != configured["generation_date"]:
        raise ValueError("family configuration generation_date must be a valid ISO date")
    return copy.deepcopy(configured)


def campaign_generation_date(campaign_id: Any) -> str:
    """Derive the immutable portfolio date from the authorized campaign identity."""
    if not isinstance(campaign_id, str):
        raise ValueError("campaign_id must end in an authorized YYYYMMDD generation date")
    match = re.search(r"-(\d{4})(\d{2})(\d{2})$", campaign_id)
    if match is None:
        raise ValueError("campaign_id must end in an authorized YYYYMMDD generation date")
    try:
        return date(*(int(value) for value in match.groups())).isoformat()
    except ValueError as exc:
        raise ValueError("campaign_id generation date is invalid") from exc


def stable_object_id(entry: dict[str, Any]) -> str:
    return _validate_entry_identifiers(entry, family_configuration(entry))


def stable_result_id(entry: dict[str, Any], result_class: str, metric: str) -> str:
    return f"result-{fingerprint({'identity_inputs': entry['identity_inputs'], 'class': result_class, 'metric': metric}).split(':', 1)[1][:24]}"


def _entry_for_series(series: dict[str, Any]) -> dict[str, Any]:
    path = FIXTURE_ROOT / f"{series['code']}__NOR__1990-2024" / "normalized_observations.json"
    normalized = read_json(path)
    identity_inputs = {
        "indicator_code": series["code"], "territory_id": "NOR", "period_start": 1990, "period_end": 2024,
        "method_id": METHOD_ID, "method_version": METHOD_VERSION,
    }
    return {
        "candidate_id": f"candidate-health-{_slug(series['code'])}-nor-1990-2024-baseline-v1",
        "disposition": "execute", "canary": series["canary"],
        "input": {
            "path": str(path.relative_to(PROJECT_ROOT)), "sha256": file_fingerprint(path),
            "normalized_fingerprint": normalized["normalized_fingerprint"],
            "admission_basis": "retained Campaign 40 HTTPS fixture selected by the frozen coefficient-free candidate registry",
        },
        "indicator": {"code": series["code"], "name": series["name"], "definition": series["definition"], "family": "Health"},
        "territory": {"id": "NOR", "name": "Norway", "observational_population": "retained observed annual Norway values for the indicator within 1990-2024"},
        "applicability": {
            "denominator_basis": series["denominator_basis"], "unit": series["unit"], "period_start": 1990,
            "period_end": 2024, "frequency": "annual", "observation_grain": "territory_indicator_year",
            "population_basis": "finite retained sequence; not a random sample",
        },
        "transformation": ["level", "adjacent_first_difference", "linear_time_index_slope"],
        "method": {
            "id": METHOD_ID, "version": METHOD_VERSION,
            "parameters": {
                "summary_method": "wdi_annual_scalar_statistical_summary_v2@2.0",
                "summary_contract_fingerprint": SUMMARY_CONTRACT_FINGERPRINT,
                "minimum_observed_count": 30, "minimum_coverage_share": "0.85",
                "decimal_precision": 50, "rounding": "ROUND_HALF_EVEN",
                "difference_rule": "only consecutive observed annual periods",
                "quartile_rule": "median of lower and upper halves excluding the overall median for odd N",
                "slope_rule": "ordinary least-squares slope against integer calendar year; descriptor only",
            },
        },
        "expected_output_class": "baseline_characterization", "dependencies": ["retained_campaign40_fixture", "wdi_annual_scalar_statistical_summary_v2@2.0"],
        "bundle_id": BUNDLE_ID, "campaign_id": CAMPAIGN_ID,
        "computational_budget": {"maximum_result_records": EXPECTED_RESULT_RECORDS, "maximum_wall_seconds": 5},
        "validation_requirements": ["input_hash", "coverage", "stable_identity", "exact_lineage", "applicability", "schema", "nonredundancy", "input_immutability"],
        "promotion_conditions": ["all_28_required_results_valid", "no_identity_collision", "no_redundancy", "knowledge_object_validation_pass"],
        "exclusion_and_stopping_rules": ["stop_on_input_hash_mismatch", "stop_on_manifest_fingerprint_mismatch", "exclude_nonconsecutive_differences", "exclude_growth_rates", "exclude_relationship_claims"],
        "identity_inputs": identity_inputs,
    }


def build_preregistration() -> tuple[dict[str, Any], dict[str, Any]]:
    registry = read_json(CANDIDATE_REGISTRY)
    health = next(record for record in registry["records"] if record["candidate_id"] == "health_life_expectancy_under5_mortality_nor")
    entries = [_entry_for_series(series) for series in SERIES]
    exclusion = copy.deepcopy(entries[0])
    exclusion.update({
        "candidate_id": "candidate-health-life-expectancy-cagr-excluded-v1",
        "disposition": "excluded_pre_execution", "canary": True,
        "expected_output_class": "excluded_inapplicable_method",
        "exclusion_reason": "Compound annual growth and percentage-growth summaries are not semantically justified for this bounded health-state level series and could imply an accumulation process.",
    })
    exclusion["method"] = {"id": "compound_annual_growth_rate", "version": "not_registered", "parameters": {}}
    exclusion["identity_inputs"] = {**exclusion["identity_inputs"], "method_id": "compound_annual_growth_rate", "method_version": "not_registered"}
    entries.append(exclusion)
    rubric = {
        "rubric_id": "selection-rubric-health-baseline-portfolio-v1", "recorded_before_new_outcome_calculation": True,
        "eligible_universe": [{
            "registry_id": registry["registry_id"], "registry_fingerprint": registry["registry_fingerprint"],
            "candidate_ids": [record["candidate_id"] for record in registry["records"]],
        }],
        "criteria": [
            "authoritative Mature WDI family and admitted retained HTTPS evidence",
            "two-series semantic coherence within one registered family",
            "same territory, annual frequency and 1990-2024 window",
            "durable local raw and normalized inputs with hashes",
            "clear units, definitions, observational population and denominator/applicability bases",
            "at least 30 retained observations and 0.85 coverage under existing admission metadata",
            "low bounded computational and review cost",
            "descriptive downstream utility without requiring comparison or interpretation",
            "no selection based on newly calculated level, difference, slope or variability outcomes",
        ],
        "selected_family": "Health", "selected_candidate_id": health["candidate_id"],
        "selection_reason": "The complete retained Health pair is mature, semantically coherent, territory/period consistent, fully covered in admitted metadata, denominator-explicit and useful for baseline characterization without relationship calculation.",
        "known_limitations": [
            "WDI mutable-source vintage limitation; retained bytes are the replay anchor",
            "shared modeled-estimation processes can create dependence but no cross-series relationship is calculated",
            "finite ordered annual values are not random or independent samples",
            "linear slope and first-difference descriptors do not establish stationarity, persistence, explanation or forecastability",
            "canonical decimal precision is representation policy, not source measurement precision",
        ],
        "excluded_universe": [
            {"candidate_id": r["candidate_id"], "reason": "different WDI topical family; excluded before portfolio outcomes"}
            for r in registry["records"] if r["candidate_id"] != health["candidate_id"]
        ],
        "selection_registry_file_sha256": file_fingerprint(CANDIDATE_REGISTRY),
    }
    rubric["rubric_fingerprint"] = fingerprint({k: v for k, v in rubric.items() if k != "rubric_fingerprint"})
    manifest = {
        "manifest_id": MANIFEST_ID, "manifest_version": "1.0", "campaign_id": CAMPAIGN_ID,
        "portfolio_kind": "bounded_baseline_characterization_execution_manifest", "canonical_ontology_change": False,
        "evidence_card_equivalent_definition": "one operational result-record view; canonical authority remains the KnowledgeObjectPackage",
        "bundle_definition": "bounded campaign grouping only; not a new canonical object type",
        "selection_rubric_fingerprint": rubric["rubric_fingerprint"], "entries": entries,
        "candidate_order": [entry["candidate_id"] for entry in entries],
        "computational_budget": {"maximum_executed_candidates": 2, "maximum_raw_result_records": 56, "maximum_promoted_objects": 2, "stop_on_canary_failure": True},
        "validation_requirements": ["manifest_schema", "outcome_blind_fields", "input_hashes", "stable_identities", "complete_accounting", "deterministic_rerun"],
        "promotion_conditions": ["canary_gate_pass", "all_required_records_valid", "canonical_package_validator_pass", "no_duplicate_promotion"],
        "stopping_rules": ["no candidate substitution after outcomes", "stop_on_canary_material_failure", "do_not_exceed_budget"],
        "forbidden_outcome_fields": FORBIDDEN_OUTCOME_FIELDS,
    }
    manifest["manifest_fingerprint"] = fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
    validate_manifest(manifest)
    return rubric, manifest


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    required = {"manifest_id", "campaign_id", "entries", "candidate_order", "computational_budget", "selection_rubric_fingerprint"}
    missing = sorted(required - set(manifest))
    if missing:
        raise ValueError(f"manifest missing fields: {missing}")
    if manifest.get("candidate_order") != [entry.get("candidate_id") for entry in manifest["entries"]]:
        raise ValueError("manifest candidate order mismatch")
    limits = manifest.get("computational_budget")
    if not isinstance(limits, dict) or set(limits) != set(REQUIRED_PORTFOLIO_LIMITS):
        raise ValueError("manifest computational budget must contain the complete normative limit set")
    for key, expected_value in REQUIRED_PORTFOLIO_LIMITS.items():
        value = limits.get(key)
        if key == "stop_on_canary_failure":
            if type(value) is not bool or value is not True:
                raise ValueError("stop_on_canary_failure must be the literal Boolean true")
        elif type(value) is not int or value != expected_value:
            raise ValueError(f"normative portfolio limit mismatch: {key}")
    authorized_generation_date = campaign_generation_date(manifest["campaign_id"])
    forbidden = set(manifest.get("forbidden_outcome_fields", FORBIDDEN_OUTCOME_FIELDS))
    for entry in manifest["entries"]:
        overlap = forbidden.intersection(entry)
        if overlap:
            raise ValueError(f"manifest contains outcome field: {sorted(overlap)}")
        for key in ["candidate_id", "disposition", "input", "indicator", "territory", "applicability", "method", "bundle_id", "campaign_id", "computational_budget", "validation_requirements", "promotion_conditions", "exclusion_and_stopping_rules", "identity_inputs"]:
            if key not in entry:
                raise ValueError(f"manifest entry missing {key}")
        if type(entry.get("canary")) is not bool:
            raise ValueError(f"{entry.get('candidate_id')} canary must be a JSON Boolean")
        if entry["campaign_id"] != manifest["campaign_id"]:
            raise ValueError("manifest entry campaign must match top-level campaign")
        entry_limits = entry["computational_budget"]
        if not isinstance(entry_limits, dict) or set(entry_limits) != set(REQUIRED_ENTRY_LIMITS):
            raise ValueError("manifest entry must contain the complete normative limit set")
        if any(type(entry_limits[key]) is not int or entry_limits[key] != expected for key, expected in REQUIRED_ENTRY_LIMITS.items()):
            raise ValueError("normative manifest entry limit mismatch")
        config = family_configuration(entry)
        if config["generation_date"] != authorized_generation_date:
            raise ValueError("family configuration generation_date does not match authorized campaign generation date")
        identity = entry["identity_inputs"]
        if (
            identity.get("indicator_code") != entry["indicator"].get("code")
            or identity.get("territory_id") != entry["territory"].get("id")
            or identity.get("period_start") != entry["applicability"].get("period_start")
            or identity.get("period_end") != entry["applicability"].get("period_end")
            or identity.get("method_id") != entry["method"].get("id")
            or identity.get("method_version") != entry["method"].get("version")
        ):
            raise ValueError("manifest entry identity inputs are inconsistent with structured entry")
        _validate_entry_identifiers(entry, config)
    expected = manifest.get("manifest_fingerprint")
    if expected and expected != fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"}):
        raise ValueError("manifest fingerprint mismatch")
    return {"valid": True, "entry_count": len(manifest["entries"])}


def _ctx() -> Context:
    return Context(prec=50, rounding=ROUND_HALF_EVEN)


def _dec(value: Any) -> Decimal:
    if isinstance(value, dict):
        value = value.get("canonical", value.get("value"))
    return Decimal(str(value))


def _canon(value: Decimal) -> str:
    with localcontext(_ctx()) as ctx:
        out = value.quantize(Decimal("0.000000000001"), context=ctx)
        if out.is_zero():
            return "0"
        return format(out, "f").rstrip("0").rstrip(".")


def _median(values: list[Decimal]) -> Decimal:
    values = sorted(values); n = len(values)
    with localcontext(_ctx()) as ctx:
        return values[n // 2] if n % 2 else ctx.divide(ctx.add(values[n // 2 - 1], values[n // 2]), Decimal(2))


def _pop_std(values: list[Decimal]) -> Decimal:
    with localcontext(_ctx()) as ctx:
        mean = sum(values, Decimal(0)) / Decimal(len(values))
        variance = sum((value - mean) * (value - mean) for value in values) / Decimal(len(values))
        return variance.sqrt(context=ctx)


def _quartiles(values: list[Decimal]) -> tuple[Decimal, Decimal]:
    ordered = sorted(values); n = len(ordered); half = n // 2
    return _median(ordered[:half]), _median(ordered[-half:])


def _metric_value(summary: dict[str, Any], extras: dict[str, Any], metric: str) -> Any:
    direct = {
        "expected_observation_slot_count": summary["expected_observation_slot_count"], "observed_count": summary["observed_count"],
        "missing_count": summary["missing_count"], "coverage_share": summary["coverage_share"]["canonical"],
        "missing_share": summary["missing_share"]["canonical"], "period_start": summary["period_coverage"]["start_period"],
        "period_end": summary["period_coverage"]["end_period"], "first_valid_observation": summary["first_valid_observation"],
        "last_valid_observation": summary["last_valid_observation"], "minimum": summary["minimum"], "maximum": summary["maximum"],
        "arithmetic_mean": summary["arithmetic_mean"], "median": summary["median"],
        "population_standard_deviation": summary["population_standard_deviation"],
    }
    return direct[metric] if metric in direct else extras[metric]


_RATE_METRICS = {
    "first_difference_mean", "first_difference_median", "first_difference_minimum",
    "first_difference_maximum", "linear_time_index_slope_per_year",
    "first_difference_population_standard_deviation", "mean_absolute_first_difference",
}
_ABSOLUTE_DELTA_METRICS = {
    "population_standard_deviation", "interquartile_range", "net_level_difference",
}


def _semantic_result_value(entry: dict[str, Any], metric: str, value: Any) -> Any:
    """Give derived values quantity-aware units without changing source applicability.

    The admitted provider unit remains in applicability/source scope. Result-level
    units distinguish percentage levels from percentage-point distances and make
    subscription quantities explicit in standalone operational views. Families
    without an explicit supported measure_kind retain their historical rendering.
    """
    if not isinstance(value, dict) or "unit" not in value:
        return value
    rendered = copy.deepcopy(value)
    measure_kind = entry["applicability"].get("measure_kind")
    if measure_kind == "individual_people_using_internet_share":
        if metric in _RATE_METRICS:
            rendered["unit"] = "percentage points per year"
        elif metric in _ABSOLUTE_DELTA_METRICS:
            rendered["unit"] = "percentage points"
    elif measure_kind == "mobile_cellular_subscriptions_per_100_people":
        rendered["unit"] = "mobile cellular subscriptions per 100 people"
        if metric in _RATE_METRICS:
            rendered["unit"] += " per year"
    return rendered


def calculate_candidate(entry: dict[str, Any], normalized: dict[str, Any]) -> dict[str, Any]:
    if entry.get("disposition") != "execute":
        raise ValueError("candidate is not executable")
    contract = summary_v2.calculation_contract_v2()
    if contract["calculation_contract_fingerprint"] != SUMMARY_CONTRACT_FINGERPRINT:
        raise ValueError("summary calculation contract fingerprint mismatch")
    summary = summary_v2.compute_statistical_summary_v2(normalized)
    observed = sorted((row for row in normalized["observations"] if row["observed"]), key=lambda row: row["period"])
    values = [Decimal(row["value_canonical"]) for row in observed]
    adjacent = [(b["period"], Decimal(b["value_canonical"]) - Decimal(a["value_canonical"])) for a, b in zip(observed, observed[1:]) if b["period"] == a["period"] + 1]
    diffs = [value for _, value in adjacent]
    if not diffs:
        raise ValueError("null first-difference population")
    with localcontext(_ctx()):
        q1, q3 = _quartiles(values)
        diff_mean = sum(diffs, Decimal(0)) / Decimal(len(diffs))
        x = [Decimal(row["period"]) for row in observed]
        x_mean = sum(x, Decimal(0)) / Decimal(len(x)); y_mean = sum(values, Decimal(0)) / Decimal(len(values))
        denom = sum((xi - x_mean) * (xi - x_mean) for xi in x)
        slope = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, values)) / denom
        extras = {
            "observed_period_span_years": observed[-1]["period"] - observed[0]["period"],
            "first_quartile": {"canonical": _canon(q1), "unit": entry["applicability"]["unit"]},
            "third_quartile": {"canonical": _canon(q3), "unit": entry["applicability"]["unit"]},
            "interquartile_range": {"canonical": _canon(q3 - q1), "unit": entry["applicability"]["unit"]},
            "adjacent_first_difference_count": len(diffs),
            "first_difference_mean": {"canonical": _canon(diff_mean), "unit": f"{entry['applicability']['unit']} per year"},
            "first_difference_median": {"canonical": _canon(_median(diffs)), "unit": f"{entry['applicability']['unit']} per year"},
            "first_difference_minimum": {"canonical": _canon(min(diffs)), "unit": f"{entry['applicability']['unit']} per year"},
            "first_difference_maximum": {"canonical": _canon(max(diffs)), "unit": f"{entry['applicability']['unit']} per year"},
            "net_level_difference": {"canonical": _canon(values[-1] - values[0]), "unit": entry["applicability"]["unit"]},
            "linear_time_index_slope_per_year": {"canonical": _canon(slope), "unit": f"{entry['applicability']['unit']} per year"},
            "linear_time_index_slope_sign": "positive" if slope > 0 else "negative" if slope < 0 else "zero",
            "first_difference_population_standard_deviation": {"canonical": _canon(_pop_std(diffs)), "unit": f"{entry['applicability']['unit']} per year"},
            "mean_absolute_first_difference": {"canonical": _canon(sum(abs(v) for v in diffs) / Decimal(len(diffs))), "unit": f"{entry['applicability']['unit']} per year"},
        }
    records = []
    config = family_configuration(entry)
    record_limitations = config["result_limitations"] + config["applicability_limitations"]
    for result_class, metric in RESULT_SPEC:
        value = _semantic_result_value(entry, metric, _metric_value(summary, extras, metric))
        record = {
            "result_id": stable_result_id(entry, result_class, metric), "class": result_class, "metric": metric, "value": value,
            "applicability": copy.deepcopy(entry["applicability"]), "input_normalized_fingerprint": normalized["normalized_fingerprint"],
            "method_id": entry["method"]["id"], "method_version": entry["method"]["version"], "transformation": "adjacent_first_difference" if "difference" in metric else "linear_time_index" if metric.startswith("linear_") else "level",
            "limitations": record_limitations,
        }
        record["semantic_fingerprint"] = fingerprint({k: v for k, v in record.items() if k not in {"result_id", "semantic_fingerprint"}})
        records.append(record)
    unique, redundant = detect_redundancy(records)
    if redundant or len(unique) != EXPECTED_RESULT_RECORDS:
        raise ValueError("required result record set is incomplete or redundant")
    return {
        "candidate_id": entry["candidate_id"], "disposition": "valid", "input_normalized_fingerprint": normalized["normalized_fingerprint"],
        "raw_result_count": len(records), "valid_result_count": len(unique), "result_records": unique,
        "calculation_fingerprint": fingerprint(unique), "null_result_count": 0, "failure_count": 0,
    }


def detect_redundancy(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_id: dict[str, dict[str, Any]] = {}; unique = []; redundant = []
    for record in records:
        identity = record["result_id"]
        if identity in by_id:
            if canonical_json(by_id[identity]) != canonical_json(record):
                raise ValueError(f"identity collision for {identity}")
            redundant.append({"result_id": identity, "reason": "exact duplicate semantics, input, parameters and value"})
        else:
            by_id[identity] = record; unique.append(record)
    return unique, redundant


def build_knowledge_object(entry: dict[str, Any], result: dict[str, Any], manifest_fingerprint: str) -> dict[str, Any]:
    if len(result.get("result_records", [])) != EXPECTED_RESULT_RECORDS or result.get("valid_result_count") != EXPECTED_RESULT_RECORDS:
        raise ValueError("required result records are incomplete")
    package_id = stable_object_id(entry)
    config = family_configuration(entry)
    identity = entry["identity_inputs"]
    applicability = entry["applicability"]
    territory = entry["territory"]
    method_id, method_version = entry["method"]["id"], entry["method"]["version"]
    campaign_id = entry["campaign_id"]
    evidence_ref_id = f"ev-eppilot-{_slug(entry['indicator']['code'])}-{territory['id'].lower()}-{identity['period_start']}-{identity['period_end']}"
    candidate_id = package_id.replace("pkg-object-", "pkg-candidate-")
    statement_id = package_id.replace("pkg-object-", "stmt-")
    result_classes = sorted({record["class"] for record in result["result_records"]})
    common = {
        "package_id": package_id, "package_kind": "KnowledgeObjectPackage", "package_version": "1.0", "created_at": config["generation_date"],
        "created_by": "evidence_portfolio_production", "status": "accepted-for-controlled-production",
        "scope": {
            "domain": config["domain"], "evidence_family": config["evidence_family"],
            "source_scope": {"campaign_id": campaign_id, "provider": "World Bank", "dataset": "World Development Indicators", "source_id": "2", "indicator_code": entry["indicator"]["code"], "indicator_name": entry["indicator"]["name"], "entity_id": territory["id"], "entity_name": territory["name"], "period_start": identity["period_start"], "period_end": identity["period_end"], "frequency": applicability["frequency"], "unit": applicability["unit"], "denominator_basis": applicability["denominator_basis"], "observational_population": territory["observational_population"], "scope_type": "bounded_baseline_characterization"},
            "method_scope": f"{method_id}@{method_version}", "intended_use": "deterministic descriptive baseline knowledge only",
        },
        "input_references": [entry["input"]["normalized_fingerprint"]],
        "evidence_references": [{
            "evidence_ref_id": evidence_ref_id, "evidence_class": "external_observation_level_numerical_fixture",
            "source_family": "official_statistical_source_data", "source_identity": f"World Bank WDI {entry['indicator']['code']} {territory['id']} {applicability['frequency']} retained Campaign 40 fixture",
            "source_owner": "World Bank WDI API retained local fixture", "source_version": "2026-07-01", "accessed_at": "2026-07-11",
            "snapshot_fingerprint": entry["input"]["sha256"], "reproducibility_handle": entry["input"]["path"], "evaluation_status": "evaluated",
        }],
        "computation_method": {"name": method_id, "version": method_version, "recipe": "summary v2 plus deterministic adjacent first-difference, quartile and calendar-year OLS slope descriptors", "parameters": entry["method"]["parameters"], "query_definitions": [], "nondeterminism": "none", "rerun": f"python3 tools/evidence_portfolio_production.py run --manifest artifacts/production/{campaign_id}/portfolio_manifest.json --mode production --canary-gate artifacts/production/{campaign_id}/canary_gate.json"},
        "generated_statements": [{
            "statement_id": statement_id, "statement_type": "derived",
            "text": f"The retained World Bank WDI {entry['indicator']['code']} series for {territory['name']}, {applicability['frequency']} {identity['period_start']}-{identity['period_end']}, has a deterministic baseline characterization containing {EXPECTED_RESULT_RECORDS} coverage, period, level, adjacent-difference, linear time-index slope and variability result records. These descriptors apply only to the finite retained sequence and do not explain, predict or establish persistence.",
            "applicability": copy.deepcopy(entry["applicability"]),
            "dependencies": [entry["input"]["normalized_fingerprint"], SUMMARY_CONTRACT_FINGERPRINT, manifest_fingerprint],
            "evidence_refs": [evidence_ref_id], "origin": "computed_offline_from_retained_admitted_evidence",
            "structured_payload": {"result_records": result["result_records"], "result_classes": result_classes, "result_count": EXPECTED_RESULT_RECORDS, "calculation_fingerprint": result["calculation_fingerprint"], "manifest_fingerprint": manifest_fingerprint, "indicator_definition": entry["indicator"]["definition"], "limitations": config["package_limitations"]},
        }],
        "confidence_quality": {"confidence_label": "retained-fixture-supported-deterministic", "uncertainty_dimensions": config["uncertainty_dimensions"], "missingness_summary": "encoded in result records", "evidence_sufficiency": "sufficient for bounded descriptive baseline characterization", "reproducibility_state": "reproducible_offline_from_retained_fixture", "validation_state": "pass", "governance_review_state": config["governance_review_state"], "lifecycle_state": "accepted"},
        "contradiction_records": [{"contradiction_id": "none-recorded", "target_statement": statement_id, "contradiction_type": "none", "contradicting_evidence": None, "disposition": "not_applicable"}],
        "provenance_envelope": {"package_identity": package_id, "creator": "evidence_portfolio_production", "generation_date": config["generation_date"], "source_systems": ["World Bank WDI retained Campaign 40 HTTPS fixture"], "evidence_refs": [evidence_ref_id], "evaluation_refs": [f"validation-{campaign_id}"], "computation_recipe": f"{method_id}@{method_version}", "validation_tool": "evidence_portfolio_production", "reproducibility_state": "reproducible_offline", "input_file_sha256": entry["input"]["sha256"], "normalized_evidence_fingerprint": entry["input"]["normalized_fingerprint"], "selection_manifest_fingerprint": manifest_fingerprint, "calculation_contract_fingerprint": SUMMARY_CONTRACT_FINGERPRINT, "lineage": ["retained_https_fixture", "normalized_observations", "preregistered_calculation", "validated_result_records", "knowledge_object_package"]},
        "validation_state": {"validation_result": "pass", "validator_version": "evidence-portfolio-pilot-v1", "blockers": [], "warnings": [], "human_review_required": False},
        "evolution_metadata": {"previous_revision": None, "change_reason": config["evolution_change_reason"], "changed_inputs_methods_templates_models_validators": [method_id], "dependent_object_review_posture": "review_on_source_or_method_supersession", "supersession_dependencies": [entry["input"]["normalized_fingerprint"], SUMMARY_CONTRACT_FINGERPRINT, manifest_fingerprint]},
        "promotion": {"from_candidate_package_id": candidate_id, "promotion_justification": "Pre-registered candidate passed deterministic calculation, applicability, lineage, nonredundancy and package validation gates.", "validation_history": ["manifest_validation_pass", "calculation_validation_pass", "package_validation_pass"], "maturity_state": config["promotion_maturity_state"]},
        "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": entry["input"]["sha256"]},
        "lineage": {"previous_package_id": candidate_id, "version_lineage": [candidate_id, package_id]},
    }
    for term in FORBIDDEN_CLAIM_TERMS:
        if term in common["generated_statements"][0]["text"].lower():
            raise ValueError(f"prohibited claim term: {term}")
    package = copy.deepcopy(common)
    package["fingerprints"] = {
        "input_set": fingerprint(common["input_references"]), "evidence_references": fingerprint(common["evidence_references"]),
        "query_definitions": fingerprint(common["computation_method"]["query_definitions"]), "computation_recipe": fingerprint(common["computation_method"]),
        "generated_statements": fingerprint(common["generated_statements"]), "package_manifest": fingerprint(common),
    }
    package["lineage"]["lineage_fingerprint"] = fingerprint({"candidate": candidate_id, "object": package["fingerprints"]})
    package["fingerprints"]["package_manifest"] = fingerprint({k: v for k, v in package.items() if k != "fingerprints"})
    validation = validate_knowledge_object(package)
    if validation.get("blockers"):
        raise ValueError(f"knowledge object validation failed: {validation['blockers']}")
    return package


def render_operational_views(entry: dict[str, Any], result: dict[str, Any]) -> list[dict[str, Any]]:
    package_id = stable_object_id(entry)
    views = []
    for record in result["result_records"]:
        view = {
            "view_id": record["result_id"].replace("result-", "view-"), "view_kind": "EvidenceCardEquivalentView",
            "canonical_package_id": package_id, "result_record_id": record["result_id"], "class": record["class"], "metric": record["metric"],
            "value": record["value"], "applicability": record["applicability"], "limitations": record["limitations"],
            "authority": "operational_view_only_canonical_authority_is_knowledge_object_package",
        }
        view["view_fingerprint"] = fingerprint({k: v for k, v in view.items() if k != "view_fingerprint"})
        views.append(view)
    return views


def repository_state(repository_root: Path) -> dict[str, Any]:
    try:
        return knowledge_repository.authenticate_repository(repository_root)
    except ValueError as exc:
        raise ValueError("production repository authentication failed") from exc


def persist_packages(packages: list[dict[str, Any]], repository_root: Path) -> dict[str, Any]:
    ids = [package["package_id"] for package in packages]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate package IDs in publication set")
    knowledge_repository.persist_knowledge_object_packages(packages, repository_root)
    manifest = read_json(repository_root / "manifest.json")
    return {"repository_fingerprint": manifest["repository_fingerprint"], "object_count": manifest["object_count"]}


def validate_normalized_input_binding(entry: dict[str, Any], normalized: dict[str, Any]) -> None:
    """Bind authorized structured identity and applicability to normalized evidence."""
    identity = entry["identity_inputs"]
    indicator = entry["indicator"]
    territory = entry["territory"]
    applicability = entry["applicability"]
    method = entry["method"]
    if normalized.get("normalized_fingerprint") != entry["input"]["normalized_fingerprint"]:
        raise ValueError("normalized fingerprint mismatch")
    actual_fingerprint = fingerprint({key: value for key, value in normalized.items() if key != "normalized_fingerprint"})
    if actual_fingerprint != normalized.get("normalized_fingerprint"):
        raise ValueError("normalized fingerprint does not authenticate normalized fixture semantics")
    if (
        identity.get("indicator_code") != indicator.get("code")
        or identity.get("territory_id") != territory.get("id")
        or identity.get("period_start") != applicability.get("period_start")
        or identity.get("period_end") != applicability.get("period_end")
        or identity.get("method_id") != method.get("id")
        or identity.get("method_version") != method.get("version")
    ):
        raise ValueError("registered method or identity inputs mismatch")
    selection = normalized.get("selection_contract", {})
    periods = selection.get("periods", {})
    metadata = normalized.get("indicator_metadata", {})
    observations = normalized.get("observations")
    if not isinstance(observations, list) or not observations:
        raise ValueError("normalized observations missing")
    if selection.get("indicator", {}).get("code") != indicator.get("code") or metadata.get("id") != indicator.get("code"):
        raise ValueError("normalized indicator binding mismatch")
    if indicator.get("name") != metadata.get("name"):
        raise ValueError("normalized indicator metadata name binding mismatch")
    definition_matches = indicator.get("definition") == metadata.get("definition")
    if _is_published_legacy_health_entry(entry):
        code = indicator.get("code")
        definition_matches = (
            indicator.get("definition") == LEGACY_HEALTH_DEFINITIONS.get(code)
            and metadata.get("definition") == LEGACY_HEALTH_METADATA_DEFINITIONS.get(code)
        )
    if not definition_matches:
        raise ValueError("normalized indicator metadata definition binding mismatch")
    config = family_configuration(entry)
    topic_families = {
        topic.get("value", "").strip()
        for topic in metadata.get("topics", [])
        if isinstance(topic, dict) and isinstance(topic.get("value"), str)
    }
    if config["family"] not in topic_families:
        raise ValueError("normalized indicator metadata family binding mismatch")
    if selection.get("entities") != [territory.get("id")]:
        raise ValueError("normalized territory binding mismatch")
    if periods.get("start_year") != identity.get("period_start") or periods.get("end_year") != identity.get("period_end"):
        raise ValueError("normalized period binding mismatch")
    if periods.get("frequency") != applicability.get("frequency"):
        raise ValueError("normalized frequency binding mismatch")
    expected_periods = list(range(identity["period_start"], identity["period_end"] + 1))
    if [row.get("period") for row in observations] != expected_periods:
        raise ValueError("normalized observation period population mismatch")
    if any(row.get("indicator_code") != indicator["code"] for row in observations):
        raise ValueError("normalized observation indicator mismatch")
    if any(row.get("entity_id") != territory["id"] or row.get("entity_name") != territory["name"] for row in observations):
        raise ValueError("normalized observation territory mismatch")
    provider_unit = metadata.get("unit")
    if provider_unit and (provider_unit != applicability.get("unit") or any(row.get("unit") != provider_unit for row in observations)):
        raise ValueError("normalized provider-explicit unit binding mismatch")
    if any(row.get("frequency") not in (None, applicability["frequency"]) for row in observations):
        raise ValueError("normalized observation frequency mismatch")


def execute_entry(entry: dict[str, Any], project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    if entry.get("disposition") != "execute":
        return {"candidate_id": entry["candidate_id"], "disposition": "rejected", "stage": "pre_execution", "reason": entry.get("exclusion_reason", "pre-registered exclusion"), "raw_result_count": 0}
    try:
        path, before = resolve_and_fingerprint_manifest_input(project_root, entry["input"]["path"])
    except ValueError as exc:
        return {"candidate_id": entry["candidate_id"], "disposition": "failed", "stage": "input_validation", "reason": str(exc), "raw_result_count": 0}
    if before != entry["input"]["sha256"]:
        return {"candidate_id": entry["candidate_id"], "disposition": "failed", "stage": "input_validation", "reason": "input hash mismatch", "raw_result_count": 0}
    try:
        normalized = read_json(path)
        validate_normalized_input_binding(entry, normalized)
    except (ValueError, json.JSONDecodeError, OSError, TypeError, KeyError) as exc:
        return {"candidate_id": entry["candidate_id"], "disposition": "failed", "stage": "input_validation", "reason": str(exc), "raw_result_count": 0}
    try:
        result = calculate_candidate(entry, normalized)
    except ValueError as exc:
        disposition = "null" if "null" in str(exc).lower() else "failed"
        return {"candidate_id": entry["candidate_id"], "disposition": disposition, "stage": "calculation", "reason": str(exc), "raw_result_count": 0}
    after = file_fingerprint(path)
    if before != after:
        raise RuntimeError("canonical admitted input mutated")
    result["input_hash_before"] = before; result["input_hash_after"] = after
    return result


def account_outcomes(outcomes: list[dict[str, Any]], packages: list[dict[str, Any]], views: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {name: sum(1 for outcome in outcomes if outcome.get("disposition") == disposition) for name, disposition in [
        ("valid_candidates", "valid"), ("null_candidates", "null"), ("rejected_candidates", "rejected"), ("execution_failures", "failed")
    ]}
    raw = sum(int(outcome.get("raw_result_count", 0)) for outcome in outcomes)
    valid_results = sum(int(outcome.get("valid_result_count", 0)) for outcome in outcomes)
    return {
        "manifest_candidates": len(outcomes), "executed_candidates": sum(1 for outcome in outcomes if outcome.get("disposition") in {"valid", "null", "failed"}),
        **counts, "raw_calculation_results": raw, "valid_result_records": valid_results,
        "promoted_canonical_objects": len(packages), "operational_views": len(views),
        "distinct_source_series": len({package["scope"]["source_scope"]["indicator_code"] for package in packages}),
        "distinct_transformations": 3 if packages else 0, "evidence_bundles": 1 if packages else 0,
        "dependency_clusters": len(packages), "redundant_candidates": 0, "redundant_result_records": raw - valid_results,
    }


def verify_unrelated_identity_preservation(
    baseline: dict[str, dict[str, Any]], current: dict[str, dict[str, Any]], allowlist: set[str]
) -> dict[str, Any]:
    """Compare path-level raw identities while excluding declared task-owned paths."""
    paths = sorted((set(baseline) | set(current)) - allowlist)
    changed = [path for path in paths if baseline.get(path) != current.get(path)]
    return {"valid": not changed, "changed_unrelated_paths": changed, "compared_unrelated_paths": len(paths)}


def _rerun_match(entry: dict[str, Any], project_root: Path) -> tuple[dict[str, Any], dict[str, Any], bool]:
    first = execute_entry(entry, project_root); second = execute_entry(entry, project_root)
    return first, second, fingerprint(first) == fingerprint(second)


@contextmanager
def production_repository_lock(repository_root: Path):
    """Serialize compliant portfolio writers without changing canonical repository bytes."""
    lock_path = repository_root.parent / f".{repository_root.name}.evidence_portfolio_production.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield lock_path
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def run_portfolio(
    manifest: dict[str, Any], mode: str, output_root: Path, repository_root: Path,
    canary_gate_path: Path | None = None, *, manifest_file_fingerprint: str | None = None,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    with production_repository_lock(repository_root):
        return _run_portfolio_locked(
            manifest, mode, output_root, repository_root, canary_gate_path,
            manifest_file_fingerprint=manifest_file_fingerprint, project_root=project_root,
        )


def _run_portfolio_locked(
    manifest: dict[str, Any], mode: str, output_root: Path, repository_root: Path,
    canary_gate_path: Path | None = None, *, manifest_file_fingerprint: str | None = None,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    validate_manifest(manifest)
    manifest_file_fingerprint = manifest_file_fingerprint or manifest_bytes_fingerprint(manifest)
    authorized_repository_state: dict[str, Any] | None = None
    if mode == "production":
        if canary_gate_path is None:
            raise ValueError("production wave requires v1 canary authorization")
        try:
            gate = read_json(canary_gate_path)
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError("production wave requires readable v1 canary authorization") from exc
        authorization_result = validate_production_authorization(gate, manifest, manifest_file_fingerprint, repository_state(repository_root))
        authorized_repository_state = authorization_result["repository_state"]
    selected = [entry for entry in manifest["entries"] if mode == "production" or entry.get("canary") is True]
    enforce_preexecution_limits(manifest, selected)
    outcomes: list[dict[str, Any]] = []
    reruns: list[dict[str, Any]] = []
    promotable: list[tuple[dict[str, Any], dict[str, Any]]] = []
    blockers: list[str] = []
    for entry in selected:
        if entry.get("disposition") != "execute":
            outcomes.append(execute_entry(entry, project_root))
            continue
        started = time.monotonic()
        first, second, matches = _rerun_match(entry, project_root)
        elapsed = time.monotonic() - started
        reruns.append({
            "candidate_id": entry["candidate_id"], "matched": matches,
            "first_fingerprint": fingerprint(first), "second_fingerprint": fingerprint(second),
            "elapsed_wall_seconds": format(elapsed, ".9f"),
        })
        outcomes.append(first)
        try:
            enforce_candidate_result_limits(entry, first, elapsed)
        except ValueError as exc:
            blockers.append(str(exc))
            continue
        if first.get("disposition") == "valid" and matches:
            promotable.append((entry, first))
    if any(not row["matched"] for row in reruns):
        blockers.append("deterministic rerun mismatch")
    if any(outcome["disposition"] == "failed" for outcome in outcomes):
        blockers.append("execution failure")
    if mode == "canary" and sum(1 for outcome in outcomes if outcome["disposition"] == "valid") != 1:
        blockers.append("canary valid-candidate count mismatch")
    if mode == "production" and sum(1 for outcome in outcomes if outcome["disposition"] == "valid") != 2:
        blockers.append("production valid-candidate count mismatch")
    try:
        enforce_aggregate_result_limit(manifest, outcomes)
    except ValueError as exc:
        blockers.append(str(exc))
    packages: list[dict[str, Any]] = []
    views: list[dict[str, Any]] = []
    if not blockers:
        for entry, result in promotable:
            package = build_knowledge_object(entry, result, manifest["manifest_fingerprint"])
            packages.append(package)
            views.extend(render_operational_views(entry, result))
        try:
            enforce_promotion_limit(manifest, packages)
        except ValueError as exc:
            blockers.append(str(exc))
    accounting = account_outcomes(outcomes, packages, views)
    publication = None
    if not blockers and mode == "production":
        try:
            current_repository_state = repository_state(repository_root)
        except ValueError:
            blockers.append("production repository state changed after authorization; persistence blocked")
        else:
            if current_repository_state != authorized_repository_state:
                blockers.append("production repository state changed after authorization; persistence blocked")
    if not blockers:
        publication = persist_packages(packages, repository_root)
        publication = {"disposition": "isolated_canary_admitted" if mode == "canary" else "isolated_production_admitted", "admitted_object_count": len(packages), **publication}
    output_root.mkdir(parents=True, exist_ok=True)
    write_json(output_root / f"{mode}_execution_results.json", {"outcomes": outcomes, "reruns": reruns})
    write_json(output_root / f"{mode}_accounting.json", accounting)
    write_json(output_root / f"{mode}_packages.json", packages)
    write_json(output_root / f"{mode}_views.json", views)
    if mode == "canary":
        authorization_reruns = [{key: value for key, value in row.items() if key != "elapsed_wall_seconds"} for row in reruns]
        result_gate = build_production_authorization(
            manifest, manifest_file_fingerprint, accounting=accounting, reruns=authorization_reruns,
            publication=publication, passed=not blockers, blockers=blockers,
        )
        write_json(output_root / "canary_gate.json", result_gate)
        write_json(output_root / "canary_authorization_v1.json", result_gate)
    else:
        deterministic_reruns = [{key: value for key, value in row.items() if key != "elapsed_wall_seconds"} for row in reruns]
        result_gate = {"mode": mode, "passed": not blockers, "blockers": blockers, "accounting": accounting, "reruns": deterministic_reruns, "publication": publication}
        result_gate["gate_fingerprint"] = fingerprint({key: value for key, value in result_gate.items() if key != "gate_fingerprint"})
    write_json(output_root / f"{mode}_gate.json", result_gate)
    if blockers:
        raise RuntimeError(f"{mode} gate failed: {blockers}")
    return result_gate


def command_preregister(args: argparse.Namespace) -> None:
    rubric, manifest = build_preregistration(); output = Path(args.output_root)
    write_json(output / "selection_rubric.json", rubric); write_json(output / "portfolio_manifest.json", manifest)
    print(json.dumps({"selection_rubric": str(output / "selection_rubric.json"), "manifest": str(output / "portfolio_manifest.json"), "manifest_fingerprint": manifest["manifest_fingerprint"], "entries": len(manifest["entries"])}, sort_keys=True))


def command_run(args: argparse.Namespace) -> None:
    manifest_path = Path(args.manifest)
    manifest = read_json(manifest_path)
    gate = run_portfolio(
        manifest, args.mode, Path(args.output_root), Path(args.repository_root),
        Path(args.canary_gate) if args.canary_gate else None,
        manifest_file_fingerprint=file_fingerprint(manifest_path), project_root=PROJECT_ROOT,
    )
    print(json.dumps(gate, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    prereg = sub.add_parser("preregister"); prereg.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT)); prereg.set_defaults(func=command_preregister)
    run = sub.add_parser("run"); run.add_argument("--manifest", required=True); run.add_argument("--mode", choices=["canary", "production"], required=True)
    run.add_argument("--output-root", required=True); run.add_argument("--repository-root", required=True); run.add_argument("--canary-gate"); run.set_defaults(func=command_run)
    args = parser.parse_args(); args.func(args)


if __name__ == "__main__":
    main()
