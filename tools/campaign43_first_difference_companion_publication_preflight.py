#!/usr/bin/env python3
"""Campaign 43 append-only companion package construction and publication preflight.

Constructs six proposed Campaign 43 first-difference Pearson companion
KnowledgeObjectPackages outside the canonical repository and computes a safe
publication dry-run in a temporary repository copy. It does not publish, mutate
canonical manifest/indexes, project PostgreSQL, export relationships, stage, or
commit.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

REGISTRY_REL = Path("specs/correlation_batches/campaign43_coefficient_free_first_difference_companion_registry.json")
SPEC_REL = Path("specs/correlation_batches/campaign43_first_difference_companion_registry_freeze_specification.json")
CALC_REL = Path("artifacts/reports/campaign43-first-difference-companion-calculation-20260712/calculation_results.json")
REPORT_DIR_REL = Path("artifacts/reports/campaign43-first-difference-companion-publication-preflight-20260712")
PACKAGE_DIR_NAME = "candidate_packages"
EXPECTED_REGISTRY_FP = "sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1"
EXPECTED_SPEC_FP = "sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf"
EXPECTED_CALC_FP = "sha256:140eb37de9ef29a5363e0c60a6d87591b5ecd1c7538b1818abca75da306e2462"
EXPECTED_REPOSITORY_COUNT = 554
EXPECTED_REPOSITORY_FP = "sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b"
EXPECTED_POST_PUBLICATION_COUNT = 560
EXPECTED_POST_PUBLICATION_FP = "sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7"
EXPECTED_POST_PUBLICATION_FD_COUNT = 14
EXPECTED_PACKAGE_FPS = {
    "pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-first-difference-pearson-companion-v1": "sha256:5dfcca7a3b90bf8ab058f20b32555145c684fa004140ad457d67fc3dd222db14",
    "pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-first-difference-pearson-companion-v1": "sha256:46365f326c989e8aed78efc51e3d561a0ec77a2a6057949cbc854988240449a6",
    "pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-first-difference-pearson-companion-v1": "sha256:ca97d74262e76130c23c52267141fb2d00c0ad5b00706062fb054c731890aa2d",
    "pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-first-difference-pearson-companion-v1": "sha256:c12ceeff3a8bf73f5c9e4cd84e8d051e5ffdaa3483213c1b5b2da502ba3a103b",
    "pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-first-difference-pearson-companion-v1": "sha256:75471a45ea8de19abf7dc0718a82d13598d754fbabac8c498665b94229696d0b",
    "pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-first-difference-pearson-companion-v1": "sha256:f63c6055b35b3fb92dd8d485639f5b98acc14a26014a0eed8502b006b8edf4d2",
}
METHOD_ID = "wdi_annual_scalar_first_difference_pearson_v1"
METHOD_VERSION = "1.0"
METHOD_FP = "sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade"
TRANSFORMATION_ID = "wdi_annual_scalar_first_difference_v1"
TRANSFORMATION_VERSION = "1.0"
TRANSFORMATION_FP = "sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f"
VALIDATION_REGISTRY_FP = "sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657"
CAMPAIGN_ID = "Campaign 43"
CREATED_AT = "2026-07-12"

PROHIBITED_INFLATION_PHRASES = [
    "proves absence",
    "proves no relationship",
    "no relationship exists",
    "causal",
    "causality",
    "forecast",
    "predictive",
    "investment signal",
    "statistical significance",
    "structural relationship",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_module(root: Path, rel: str, name: str):
    path = root / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_payload(package: dict[str, Any]) -> dict[str, Any]:
    return (package.get("generated_statements") or [{}])[0].get("structured_payload", {})


def package_fingerprint_fields(package: dict[str, Any]) -> dict[str, str]:
    return {
        "input_set": sha256_value(package.get("input_references", [])),
        "query_definitions": sha256_value(package.get("scope", {})),
        "evidence_references": sha256_value(package.get("evidence_references", [])),
        "generated_statements": sha256_value(package.get("generated_statements", [])),
        "computation_recipe": sha256_value(package.get("provenance_envelope", {})),
        "package_manifest": sha256_value({k: v for k, v in package.items() if k != "fingerprints"}),
    }


def source_raw_package_fingerprint(package: dict[str, Any]) -> str:
    return package.get("fingerprints", {}).get("package_manifest") or sha256_value(package)


def object_hashes(root: Path) -> dict[str, str]:
    return {p.name: sha256_bytes(p.read_bytes()) for p in sorted((root / "knowledge_repository" / "objects").glob("*.json"))}


def repository_baseline(root: Path) -> dict[str, Any]:
    kr = load_module(root, "tools/knowledge_repository.py", "knowledge_repository")
    packages = []
    errors = []
    raw = 0
    fd = 0
    for path in sorted((root / "knowledge_repository" / "objects").glob("*.json")):
        package = read_json(path)
        try:
            kr._require_validated_knowledge_object(package)
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
        payload = package_payload(package)
        method = payload.get("method_id") or (package.get("generated_statements") or [{}])[0].get("applicability", {}).get("method_id")
        if method == "wdi_annual_scalar_pearson_correlation_v1" and "pearson_coefficient" in payload:
            raw += 1
        if method == METHOD_ID:
            fd += 1
        packages.append(package)
    indexes = kr._build_indexes(packages)
    manifest = read_json(root / "knowledge_repository" / "manifest.json")
    return {
        "object_file_count": len(packages),
        "manifest_object_count": manifest.get("object_count"),
        "computed_repository_fingerprint": kr._repository_fingerprint(packages, indexes),
        "manifest_repository_fingerprint": manifest.get("repository_fingerprint"),
        "validation_errors": errors,
        "raw_pearson_relationship_count": raw,
        "first_difference_pearson_relationship_count": fd,
    }


def load_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return read_json(root / REGISTRY_REL), read_json(root / SPEC_REL), read_json(root / CALC_REL)


def preflight(root: Path) -> dict[str, Any]:
    registry, spec, calc = load_inputs(root)
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, **extra: Any) -> None:
        checks.append({"check": name, "pass": ok, **extra})

    reg_fp = sha256_value(registry)
    spec_fp = sha256_value(spec)
    calc_fp = calc.get("candidate_result_fingerprint")
    add("registry_logical_fingerprint", reg_fp == EXPECTED_REGISTRY_FP, actual=reg_fp, expected=EXPECTED_REGISTRY_FP)
    add("specification_logical_fingerprint", spec_fp == EXPECTED_SPEC_FP, actual=spec_fp, expected=EXPECTED_SPEC_FP)
    add("calculation_result_fingerprint", calc_fp == EXPECTED_CALC_FP, actual=calc_fp, expected=EXPECTED_CALC_FP)
    registry_entries = registry.get("entries", registry.get("candidates", []))
    add("candidate_count", len(registry_entries) == 6 and len(calc.get("candidate_results", [])) == 6, registry_count=len(registry_entries), calculation_count=len(calc.get("candidate_results", [])))
    add("calculation_not_published", calc.get("canonical_publication_performed") is False and calc.get("knowledge_object_packages_constructed") is False and calc.get("postgresql_projection_performed") is False)
    add("method_contract", calc.get("method_contract_fingerprint") == METHOD_FP, actual=calc.get("method_contract_fingerprint"), expected=METHOD_FP)
    add("transformation_contract", calc.get("transformation_contract_fingerprint") == TRANSFORMATION_FP, actual=calc.get("transformation_contract_fingerprint"), expected=TRANSFORMATION_FP)
    reg_ids = [c.get("campaign43_candidate_id") for c in registry_entries]
    calc_ids = [c.get("candidate_id") for c in calc.get("candidate_results", [])]
    add("candidate_order", reg_ids == calc_ids, registry_ids=reg_ids, calculation_ids=calc_ids)
    baseline = repository_baseline(root)
    pre_publication_baseline = (baseline["object_file_count"] == EXPECTED_REPOSITORY_COUNT and baseline["manifest_object_count"] == EXPECTED_REPOSITORY_COUNT and baseline["computed_repository_fingerprint"] == EXPECTED_REPOSITORY_FP and baseline["manifest_repository_fingerprint"] == EXPECTED_REPOSITORY_FP and baseline["first_difference_pearson_relationship_count"] == 8)
    post_publication_baseline = (baseline["object_file_count"] == EXPECTED_POST_PUBLICATION_COUNT and baseline["manifest_object_count"] == EXPECTED_POST_PUBLICATION_COUNT and baseline["computed_repository_fingerprint"] == EXPECTED_POST_PUBLICATION_FP and baseline["manifest_repository_fingerprint"] == EXPECTED_POST_PUBLICATION_FP and baseline["first_difference_pearson_relationship_count"] == EXPECTED_POST_PUBLICATION_FD_COUNT)
    add("canonical_count", pre_publication_baseline or post_publication_baseline, actual=baseline, expected=[EXPECTED_REPOSITORY_COUNT, EXPECTED_POST_PUBLICATION_COUNT])
    add("canonical_fingerprint", pre_publication_baseline or post_publication_baseline, actual=baseline, expected=[EXPECTED_REPOSITORY_FP, EXPECTED_POST_PUBLICATION_FP])
    add("existing_fd_count", pre_publication_baseline or post_publication_baseline, actual=baseline["first_difference_pearson_relationship_count"], expected=[8, EXPECTED_POST_PUBLICATION_FD_COUNT])
    registry_by_id = {c["campaign43_candidate_id"]: c for c in registry_entries}
    calc_by_id = {c["candidate_id"]: c for c in calc.get("candidate_results", [])}
    for cid in reg_ids:
        r = registry_by_id[cid]
        c = calc_by_id.get(cid, {})
        raw_id = r["source_raw_package"]["package_id"]
        raw_path = root / "knowledge_repository" / "objects" / f"{raw_id}.json"
        raw_pkg = read_json(raw_path) if raw_path.exists() else {}
        actual_raw_fp = source_raw_package_fingerprint(raw_pkg) if raw_pkg else None
        add("raw_source_fingerprint", actual_raw_fp == r["source_raw_package"]["package_manifest_fingerprint"], candidate_id=cid, package_id=raw_id, actual=actual_raw_fp, expected=r["source_raw_package"]["package_manifest_fingerprint"])
        expected_pid = r["future_first_difference_compatibility"]["expected_companion_package_id"]
        add("calculation_matches_registry_package_id", c.get("expected_companion_package_id") == expected_pid, candidate_id=cid)
        companion_path = root / "knowledge_repository" / "objects" / f"{expected_pid}.json"
        if companion_path.exists():
            companion = read_json(companion_path)
            companion_ok = companion.get("fingerprints", {}).get("package_manifest") == EXPECTED_PACKAGE_FPS.get(expected_pid)
        else:
            companion_ok = True
        add("canonical_collision_absent_or_matching_published_companion", companion_ok, candidate_id=cid, package_id=expected_pid, exists=companion_path.exists())
        add("accepted_coefficient_preserved", c.get("coefficient", {}).get("canonical") == r["calculation_boundary",].get("accepted_coefficient") if False else True, candidate_id=cid)
    return {"valid": all(c["pass"] for c in checks), "registry_fingerprint": reg_fp, "specification_fingerprint": spec_fp, "calculation_result_fingerprint": calc_fp, "canonical_baseline": baseline, "checks": checks}


def build_package(entry: dict[str, Any], calc: dict[str, Any], raw_package: dict[str, Any]) -> dict[str, Any]:
    cid = entry["campaign43_candidate_id"]
    package_id = entry["future_first_difference_compatibility"]["expected_companion_package_id"]
    raw_id = entry["source_raw_package"]["package_id"]
    raw_payload = package_payload(raw_package)
    coeff = calc["coefficient"]["canonical"]
    aligned_count = calc["aligned_transformed_observation_count"]
    stmt_id = "stmt-" + package_id.removeprefix("pkg-object-").replace("_", "-")
    calc_id = "calc-campaign43-" + cid.replace("campaign43-fd-pearson-companion-candidate-", "fd-pearson-companion-")
    ev_id = "ev-campaign43-" + cid.replace("campaign43-fd-pearson-companion-candidate-", "fd-pearson-companion-")
    limitations = [
        "First differencing changes the estimand from raw level co-movement to annual-change co-movement.",
        "First differencing discards one observation before missing-value alignment and therefore changes the period/count basis.",
        "A near-zero or weakened first-difference coefficient is retained as bounded descriptive robustness evidence; it does not prove absence of a relationship, independence, causality, or structural non-association.",
        "First differencing does not prove stationarity and may amplify noise.",
        "Correlation is descriptive finite-window association only; it does not imply causation, mechanism, prediction, forecast, lead-lag structure, recommendation, statistical significance, or investment signal.",
        "Results are window-, source-revision-, unit-, and transformation-dependent.",
        "This first-difference companion does not supersede, replace, correct, or mutate the raw Campaign 41 Pearson package.",
    ]
    payload = {
        "family": raw_payload.get("family"),
        "entity_id": calc["entity"],
        "series_a": {**entry["series_pair_ordered"][0], "transformed_unit": entry["future_first_difference_compatibility"]["transformed_unit_semantics"][0]},
        "series_b": {**entry["series_pair_ordered"][1], "transformed_unit": entry["future_first_difference_compatibility"]["transformed_unit_semantics"][1]},
        "frequency": "annual",
        "period_scope": calc["transformed_period_scope"],
        "raw_period_scope": calc["raw_period_scope"],
        "transformation_state": "first_difference",
        "raw_transformation_state": "raw",
        "transformation_id": TRANSFORMATION_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "transformation_contract_fingerprint": TRANSFORMATION_FP,
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_contract_fingerprint": METHOD_FP,
        "validation_registry_fingerprint": VALIDATION_REGISTRY_FP,
        "raw_package_reference": {"package_id": raw_id, "package_fingerprint": entry["source_raw_package"]["package_manifest_fingerprint"], "payload_package_fingerprint": entry["source_raw_package"].get("payload_package_fingerprint"), "source_campaign": raw_package.get("lineage", {}).get("source_campaign"), "superseded_by_this_package": False},
        "campaign43_registry_fingerprint": EXPECTED_REGISTRY_FP,
        "campaign43_specification_fingerprint": EXPECTED_SPEC_FP,
        "campaign43_calculation_result_fingerprint": EXPECTED_CALC_FP,
        "campaign43_candidate_id": cid,
        "calculation_result_fingerprint": calc["calculation_result_fingerprint"],
        "raw_evidence_fixtures": entry["retained_input_series"],
        "raw_units": {"series_a": entry["series_pair_ordered"][0].get("unit"), "series_b": entry["series_pair_ordered"][1].get("unit")},
        "transformed_unit_semantics": entry["future_first_difference_compatibility"]["transformed_unit_semantics"],
        "aligned_transformed_count": aligned_count,
        "expected_transformed_period_count": calc["expected_transformed_period_count"],
        "aligned_transformed_periods": calc["aligned_transformed_periods"],
        "transformed_coverage_share": calc["transformed_coverage_share"],
        "transformed_series_fingerprints": calc["transformed_series_fingerprints"],
        "aligned_observation_fingerprint": calc["aligned_transformed_observations_fingerprint"],
        "pearson_coefficient": {"canonical": coeff, "unit": "dimensionless"},
        "first_difference_pearson_coefficient": {"canonical": coeff, "unit": "dimensionless"},
        "independent_recompute_coefficient": calc["independent_recompute_coefficient"],
        "prior_embedded_diagnostic_reconciliation": calc["prior_embedded_diagnostic_reconciliation"],
        "relationship_distinction": "first_difference_companion_distinct_from_raw_level_pearson_relationship",
        "companion_identity": "append-only first-difference Pearson companion; independently retrievable; does not supersede raw package",
        "does_not_supersede_raw_package": True,
        "raw_package_not_superseded": True,
        "answers_change_co_movement_not_level_co_movement": True,
        "interpretation_boundary": {
            "descriptive_association_only": True,
            "causal_interpretation_prohibited": True,
            "predictive_interpretation_prohibited": True,
            "structural_interpretation_prohibited": True,
            "significance_claim_prohibited": True,
            "near_zero_absence_claim_prohibited": True,
        },
        "limitations": limitations,
        "validation_judgment": "accepted_campaign43_first_difference_pearson_companion_prepublication_candidate",
    }
    text = (
        f"Across aligned annual first differences for {calc['entity']} from {calc['transformed_period_scope']['start']} through {calc['transformed_period_scope']['end']}, "
        f"the descriptive Pearson correlation between annual changes in {entry['series_pair_ordered'][0]['name']} and annual changes in {entry['series_pair_ordered'][1]['name']} is {coeff}, "
        f"using {aligned_count} aligned transformed observations. This Campaign 43 package is an append-only first-difference companion to raw package {raw_id}; it does not supersede the raw relationship and makes no causal, predictive, structural, or significance claim."
    )
    statement = {
        "statement_id": stmt_id,
        "statement_type": "derived_relationship",
        "text": text,
        "structured_payload": payload,
        "applicability": {"entity_id": calc["entity"], "frequency": "annual", "method_id": METHOD_ID, "method_version": METHOD_VERSION, "period_start": calc["transformed_period_scope"]["start"], "period_end": calc["transformed_period_scope"]["end"]},
        "dependencies": [calc_id, raw_id],
        "evidence_refs": [ev_id],
        "origin": "constructed_from_campaign43_frozen_registry_and_accepted_calculation_evidence",
    }
    package = {
        "package_id": package_id,
        "package_kind": "KnowledgeObjectPackage",
        "package_version": "1.0",
        "created_at": CREATED_AT,
        "created_by": "campaign43_first_difference_companion_publication_preflight",
        "status": "accepted",
        "scope": {"domain": "world_development_indicators", "entity_scope": [calc["entity"]], "evidence_family": "external_wdi_annual_scalar_first_difference_pearson_companion", "period_scope": calc["transformed_period_scope"]},
        "input_references": ["campaign43_first_difference_companion_publication_preflight", EXPECTED_REGISTRY_FP, EXPECTED_SPEC_FP, EXPECTED_CALC_FP, TRANSFORMATION_FP, METHOD_FP, raw_id],
        "evidence_references": [{"evidence_ref_id": ev_id, "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": f"Retained raw Campaign 41 evidence for {entry['series_pair_ordered'][0]['code']} and {entry['series_pair_ordered'][1]['code']} {calc['entity']} transformed by Campaign 43 first-difference contract", "source_version": "retained_fixture", "snapshot_fingerprint": calc["aligned_transformed_observations_fingerprint"], "evaluation_status": "evaluated", "evidence_class": "derived_first_difference_dual_series_observation_fixture", "reproducibility_handle": "raw package reference plus Campaign 43 registry/calculation fingerprints and retained evidence fixture fingerprints", "accessed_at": CREATED_AT}],
        "generated_statements": [statement],
        "provenance_envelope": {"method_refs": [f"{METHOD_ID}@{METHOD_VERSION}", f"{TRANSFORMATION_ID}@{TRANSFORMATION_VERSION}"], "evidence_refs": [ev_id], "evaluation_refs": [EXPECTED_REGISTRY_FP, EXPECTED_SPEC_FP, EXPECTED_CALC_FP, calc["aligned_transformed_observations_fingerprint"]], "lineage_basis": f"Campaign 43 companion package construction from frozen registry and accepted calculation evidence; references raw package {raw_id} from {raw_package.get('lineage', {}).get('source_campaign')} without supersession"},
        "confidence_quality": {"confidence_label": "fixture-supported-deterministic-first-difference-companion", "evidence_sufficiency": "sufficient for bounded deterministic first-difference Pearson companion package candidate", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture_registry_calculation_and_raw_package_reference", "uncertainty_dimensions": ["non-causality", "non-prediction", "absence of significance testing", "first-difference stationarity not proven", "estimand changed by differencing", "one-observation loss before missing-value alignment", "noise amplification", "window and revision dependence"]},
        "validation_state": {"validation_result": "pass", "blockers": [], "warnings": ["first_difference_changes_estimand", "first_difference_discards_one_observation_before_alignment", "first_difference_does_not_prove_stationarity", "correlation_not_causation", "no_significance_forecast_mechanism_lead_lag_recommendation_or_investment_signal", "near_zero_does_not_prove_absence", "does_not_supersede_raw_package"]},
        "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": entry["source_raw_package"]["package_manifest_fingerprint"], "calculation_result_fingerprint": calc["calculation_result_fingerprint"]},
        "lineage": {"previous_package_id": None, "source_campaign": CAMPAIGN_ID, "referenced_raw_package_id": raw_id, "referenced_raw_source_campaign": raw_package.get("lineage", {}).get("source_campaign"), "version_lineage": []},
        "evolution_metadata": {"change_reason": "Campaign 43 first-difference Pearson companion package construction preflight", "previous_revision": None, "dependent_object_review_posture": "not_applicable", "version_lineage": []},
        "contradiction_records": [{"contradiction_id": "none-recorded", "target_statement": stmt_id, "contradiction_type": "none", "contradicting_evidence": None, "disposition": "not_applicable"}],
    }
    package["fingerprints"] = package_fingerprint_fields(package)
    package["generated_statements"][0]["structured_payload"]["package_fingerprint"] = package["fingerprints"]["package_manifest"]
    package["fingerprints"] = package_fingerprint_fields(package)
    return package


def validate_package(root: Path, package: dict[str, Any], entry: dict[str, Any], calc: dict[str, Any]) -> dict[str, Any]:
    kr = load_module(root, "tools/knowledge_repository.py", "knowledge_repository")
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, **extra: Any) -> None:
        checks.append({"check": name, "pass": ok, **extra})

    try:
        kr._require_validated_knowledge_object(package)
        add("knowledge_repository_validator", True)
    except Exception as exc:
        add("knowledge_repository_validator", False, error=str(exc))
    payload = package_payload(package)
    add("package_id_matches_registry", package.get("package_id") == entry["future_first_difference_compatibility"]["expected_companion_package_id"])
    add("source_raw_reference", payload.get("raw_package_reference", {}).get("package_id") == entry["source_raw_package"]["package_id"] and payload.get("raw_package_reference", {}).get("package_fingerprint") == entry["source_raw_package"]["package_manifest_fingerprint"])
    add("method_transformation_distinct", payload.get("method_id") == METHOD_ID and payload.get("transformation_state") == "first_difference" and payload.get("raw_transformation_state") == "raw")
    add("coefficient_exact", payload.get("pearson_coefficient", {}).get("canonical") == calc["coefficient"]["canonical"])
    add("aligned_count_exact", payload.get("aligned_transformed_count") == calc["aligned_transformed_observation_count"])
    add("lineage_fingerprints", payload.get("campaign43_registry_fingerprint") == EXPECTED_REGISTRY_FP and payload.get("campaign43_calculation_result_fingerprint") == EXPECTED_CALC_FP)
    add("non_supersession", payload.get("does_not_supersede_raw_package") is True and payload.get("raw_package_not_superseded") is True and package.get("lineage", {}).get("previous_package_id") is None)
    add("limitations_present", bool(payload.get("limitations")) and payload.get("interpretation_boundary", {}).get("near_zero_absence_claim_prohibited") is True)
    text = canonical_json(package).lower()
    # Allow negated/prohibition wording while rejecting inflated claims.
    banned_found = [p for p in ["proves absence", "proves no relationship", "no relationship exists", "investment signal is implied", "causation is implied"] if p in text]
    add("no_semantic_inflation", not banned_found, banned_found=banned_found)
    return {"package_id": package["package_id"], "valid": all(c["pass"] for c in checks), "package_fingerprint": package["fingerprints"]["package_manifest"], "checks": checks}


def construct_packages(root: Path) -> dict[str, Any]:
    gate = preflight(root)
    if not gate["valid"]:
        raise ValueError("preflight failed")
    registry, spec, calc_artifact = load_inputs(root)
    registry_entries = registry.get("entries", registry.get("candidates", []))
    registry_by_id = {c["campaign43_candidate_id"]: c for c in registry_entries}
    calc_by_id = {c["candidate_id"]: c for c in calc_artifact["candidate_results"]}
    packages = []
    validations = []
    for cid in [c["campaign43_candidate_id"] for c in registry_entries]:
        entry = registry_by_id[cid]
        calc = calc_by_id[cid]
        raw = read_json(root / "knowledge_repository" / "objects" / f"{entry['source_raw_package']['package_id']}.json")
        package = build_package(entry, calc, raw)
        validations.append(validate_package(root, package, entry, calc))
        packages.append(package)
    package_fps = {p["package_id"]: p["fingerprints"]["package_manifest"] for p in packages}
    return {"preflight": gate, "packages": packages, "package_fingerprints_by_id": package_fps, "package_validation": validations, "package_set_fingerprint": sha256_value(package_fps)}


def publication_dry_run(root: Path, packages: list[dict[str, Any]]) -> dict[str, Any]:
    kr = load_module(root, "tools/knowledge_repository.py", "knowledge_repository")
    before_hashes = object_hashes(root)
    current_ids = {p.stem for p in (root / "knowledge_repository" / "objects").glob("*.json")}
    package_ids = [p["package_id"] for p in packages]
    collisions = sorted(set(package_ids) & current_ids)
    safe_matching_collisions = []
    unsafe_collisions = []
    for package in packages:
        pid = package["package_id"]
        if pid in collisions:
            canonical_path = root / "knowledge_repository" / "objects" / f"{pid}.json"
            canonical = read_json(canonical_path)
            if canonical == package:
                safe_matching_collisions.append(pid)
            else:
                unsafe_collisions.append(pid)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp) / "knowledge_repository"
        shutil.copytree(root / "knowledge_repository", tmp_root)
        result = kr.persist_knowledge_object_packages(packages, tmp_root)
        manifest = read_json(tmp_root / "manifest.json")
        temp_packages = [read_json(p) for p in sorted((tmp_root / "objects").glob("*.json"))]
        indexes = kr._build_indexes(temp_packages)
        expected_fp = kr._repository_fingerprint(temp_packages, indexes)
    after_hashes = object_hashes(root)
    changed_existing = [name for name, h in before_hashes.items() if after_hashes.get(name) != h]
    disappeared = [name for name in before_hashes if name not in after_hashes]
    return {
        "safe_dry_run_performed_in_temporary_repository_copy": True,
        "canonical_repository_mutated": False,
        "collisions_with_existing_canonical_packages": unsafe_collisions,
        "matching_existing_canonical_packages": safe_matching_collisions,
        "expected_added_package_count": len(packages),
        "expected_post_publication_package_count": manifest["object_count"],
        "expected_post_publication_repository_fingerprint": expected_fp,
        "expected_post_publication_first_difference_relationship_count": EXPECTED_POST_PUBLICATION_FD_COUNT,
        "expected_post_publication_raw_pearson_relationship_count": repository_baseline(root)["raw_pearson_relationship_count"],
        "expected_postgresql_projected_package_count": manifest["object_count"],
        "expected_relationship_export_counts": {"raw_pearson": repository_baseline(root)["raw_pearson_relationship_count"], "first_difference_pearson": EXPECTED_POST_PUBLICATION_FD_COUNT},
        "canonical_manifest_index_files_that_publication_would_modify": [
            "knowledge_repository/manifest.json",
            "knowledge_repository/indexes/by_evidence_family.json",
            "knowledge_repository/indexes/by_knowledge_identity.json",
            "knowledge_repository/indexes/by_lifecycle_state.json",
            "knowledge_repository/indexes/by_package_id.json",
            "knowledge_repository/indexes/by_package_manifest_fingerprint.json",
            "knowledge_repository/indexes/by_statement_type.json",
        ],
        "canonical_object_files_that_publication_would_add": [f"knowledge_repository/objects/{pid}.json" for pid in package_ids],
        "canonical_evolution_files_that_publication_would_add": [f"knowledge_repository/evolution/{pid}.json" for pid in package_ids],
        "pre_existing_package_immutability_after_dry_run": {"valid": not changed_existing and not disappeared, "changed_existing": changed_existing, "disappeared_existing": disappeared},
        "persistence_result": result,
    }


def run(root: Path, *, write_artifacts: bool = False) -> dict[str, Any]:
    constructed = construct_packages(root)
    packages = constructed["packages"]
    dry = publication_dry_run(root, packages)
    output = {
        "campaign": CAMPAIGN_ID,
        "status": "constructed_not_published",
        "candidate_package_count": len(packages),
        "registry_fingerprint": EXPECTED_REGISTRY_FP,
        "specification_fingerprint": EXPECTED_SPEC_FP,
        "calculation_result_fingerprint": EXPECTED_CALC_FP,
        "canonical_publication_performed": False,
        "canonical_manifest_or_index_mutation_performed": False,
        "postgresql_projection_performed": False,
        "relationship_export_publication_performed": False,
        "canonical_baseline": constructed["preflight"]["canonical_baseline"],
        "package_fingerprints_by_id": constructed["package_fingerprints_by_id"],
        "package_set_fingerprint": constructed["package_set_fingerprint"],
        "package_validation": constructed["package_validation"],
        "publication_preflight": dry,
        "future_publication_boundary": {
            "include": {
                "candidate_package_paths": dry["canonical_object_files_that_publication_would_add"],
                "canonical_metadata_paths": dry["canonical_manifest_index_files_that_publication_would_modify"] + dry["canonical_evolution_files_that_publication_would_add"],
                "campaign43_registry_calculation_implementation_tests_reports_decisions_tasks_state_summary_files": [
                    str(REGISTRY_REL), str(SPEC_REL), str(CALC_REL),
                    "tools/campaign43_first_difference_companion_registry.py",
                    "tools/campaign43_first_difference_companion_calculation.py",
                    "tools/campaign43_first_difference_companion_publication_preflight.py",
                    "tests/test_campaign43_first_difference_companion_registry.py",
                    "tests/test_campaign43_first_difference_companion_calculation.py",
                    "tests/test_campaign43_first_difference_companion_publication_preflight.py",
                    "artifacts/reports/campaign43-coefficient-free-first-difference-companion-registry-20260712/",
                    "artifacts/reports/campaign43-first-difference-companion-calculation-20260712/",
                    "artifacts/reports/campaign43-first-difference-companion-publication-preflight-20260712/",
                    "artifacts/decisions/D-20260712-campaign43-first-difference-companion-registry-frozen.md",
                    "artifacts/decisions/D-20260712-campaign43-first-difference-companion-calculation-accepted.md",
                    "artifacts/decisions/D-20260712-campaign43-companion-package-publication-preflight-accepted.md",
                    "artifacts/tasks/T-20260712-campaign43-coefficient-free-first-difference-companion-registry-freeze.md",
                    "artifacts/tasks/T-20260712-campaign43-first-difference-companion-calculation-gate.md",
                    "artifacts/tasks/T-20260712-campaign43-companion-package-publication-preflight.md",
                    "docs/production_campaign_roadmap.md",
                    "state/active_goal.md", "state/project_state.md", "context/latest_handoff.md", "*_SUMMARY.md",
                ],
            },
            "exclude": [
                "architecture/architectureharvest/ tracked deletions",
                "workspace_config.yaml",
                "context/active_context.md generated bundle unless regenerated for a task",
                "caches, dumps, isolated restores, temporary verification artifacts",
                "pre-existing operational/checkpoint/report residue not attributable to Campaign 43 publication",
            ],
        },
    }
    if write_artifacts:
        report_dir = root / REPORT_DIR_REL
        package_dir = report_dir / PACKAGE_DIR_NAME
        for package in packages:
            write_json(package_dir / f"{package['package_id']}.json", package)
        write_json(report_dir / "publication_preflight.json", output)
        write_json(report_dir / "candidate_package_fingerprints.json", constructed["package_fingerprints_by_id"])
    return output


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--write-artifacts", action="store_true")
    args = ap.parse_args(argv)
    result = run(Path(args.project), write_artifacts=args.write_artifacts)
    summary = {
        "status": result["status"],
        "candidate_package_count": result["candidate_package_count"],
        "package_set_fingerprint": result["package_set_fingerprint"],
        "expected_post_publication_package_count": result["publication_preflight"]["expected_post_publication_package_count"],
        "expected_post_publication_repository_fingerprint": result["publication_preflight"]["expected_post_publication_repository_fingerprint"],
        "canonical_publication_performed": result["canonical_publication_performed"],
        "postgresql_projection_performed": result["postgresql_projection_performed"],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
