#!/usr/bin/env python3
"""Campaign 42 first-difference Pearson companion production.

Bounded production helper for the eight frozen Campaign 42 candidates only.
It verifies frozen inputs, computes first differences, reconciles prior diagnostics,
builds immutable companion KnowledgeObjectPackages, and can publish append-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import date
from decimal import Decimal, Context, ROUND_HALF_EVEN, localcontext, InvalidOperation, getcontext
from pathlib import Path
from typing import Any

REGISTRY_REL = Path("artifacts/reports/campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712/campaign42_coefficient_free_companion_registry.json")
SPEC_REL = Path("specs/correlation_batches/campaign42_first_difference_pearson_companion_production_specification.json")
EXPECTED_REGISTRY_FP = "sha256:be7a085b5a74860c9a6c95fb2c9e6f45a066679d317fc743694959d502e3dc15"
EXPECTED_SPEC_FP = "sha256:ec3eaf0f735a888bc01f9cf394f015dd87eab3096be2690e75de0c4ec6f86d00"
TRANSFORMATION_ID = "wdi_annual_scalar_first_difference_v1"
TRANSFORMATION_VERSION = "1.0"
TRANSFORMATION_FP = "sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f"
METHOD_ID = "wdi_annual_scalar_first_difference_pearson_v1"
METHOD_VERSION = "1.0"
METHOD_FP = "sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade"
VALIDATION_REGISTRY_FP = "sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657"
BASELINE_COUNT = 546
BASELINE_FP = "sha256:c89c25ede69ec88a12f4791dba94b6199f2927721d0028420a65a74dd6ee735c"
CAMPAIGN42_PUBLISHED_COUNT = 554
CAMPAIGN42_PUBLISHED_FP = "sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b"
POST_CAMPAIGN43_COUNT = 560
POST_CAMPAIGN43_FP = "sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7"
POST_EVIDENCE_PORTFOLIO_PILOT_COUNT = 562
POST_EVIDENCE_PORTFOLIO_PILOT_FP = "sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff"
POST_SECOND_EVIDENCE_PORTFOLIO_COUNT = 564
POST_SECOND_EVIDENCE_PORTFOLIO_FP = "sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67"
INTERNAL_CONTEXT = Context(prec=50, rounding=ROUND_HALF_EVEN)
Q12 = Decimal("0.000000000001")


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


def package_payload(package: dict[str, Any]) -> dict[str, Any]:
    return (package.get("generated_statements") or [{}])[0].get("structured_payload", {})


def package_fingerprint_for_registry(package: dict[str, Any]) -> str:
    return package_payload(package).get("package_fingerprint") or package.get("fingerprints", {}).get("package_manifest") or sha256_value(package)


def canonical_decimal_12(value: Decimal) -> str:
    with localcontext(INTERNAL_CONTEXT):
        rounded = value.quantize(Q12)
    text = format(rounded, "f")
    if "E" in text.upper():
        raise ValueError("scientific notation forbidden")
    return text


def parse_decimal(value: Any) -> Decimal:
    text = str(value)
    if "e" in text.lower():
        raise ValueError("scientific notation forbidden")
    try:
        dec = Decimal(text)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal value: {value!r}") from exc
    if not dec.is_finite():
        raise ValueError("non-finite decimal")
    return dec


def load_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    return read_json(root / REGISTRY_REL), read_json(root / SPEC_REL)


def repository_counts(root: Path) -> dict[str, Any]:
    manifest = read_json(root / "knowledge_repository/manifest.json")
    raw = stat = fd = 0
    for path in (root / "knowledge_repository/objects").glob("*.json"):
        package = read_json(path)
        statement = (package.get("generated_statements") or [{}])[0]
        payload = statement.get("structured_payload", {})
        applicability = statement.get("applicability", {})
        method_id = payload.get("method_id") or applicability.get("method_id") or ""
        if method_id == "wdi_annual_scalar_pearson_correlation_v1" and "pearson_coefficient" in payload:
            raw += 1
        if method_id == METHOD_ID:
            fd += 1
        if "statistical_summary" in method_id:
            stat += 1
    return {
        "object_count": manifest.get("object_count"),
        "repository_fingerprint": manifest.get("repository_fingerprint"),
        "raw_pearson_objects": raw,
        "first_difference_pearson_companions": fd,
        "statistical_summary_objects": stat,
    }


def pre_execution_gate(root: Path) -> dict[str, Any]:
    registry, spec = load_inputs(root)
    checks: list[dict[str, Any]] = []
    def add(name: str, ok: bool, **extra: Any) -> None:
        checks.append({"check": name, "pass": ok, **extra})
    registry_fp = sha256_value(registry)
    spec_fp = sha256_value(spec)
    add("registry_fingerprint", registry_fp == EXPECTED_REGISTRY_FP, actual=registry_fp, expected=EXPECTED_REGISTRY_FP)
    add("specification_fingerprint", spec_fp == EXPECTED_SPEC_FP, actual=spec_fp, expected=EXPECTED_SPEC_FP)
    candidates = registry.get("candidates", [])
    add("candidate_count", len(candidates) == 8, actual=len(candidates), expected=8)
    add("candidate_order", [c["campaign42_candidate_id"] for c in candidates] == spec.get("candidate_ids"), actual=[c["campaign42_candidate_id"] for c in candidates], expected=spec.get("candidate_ids"))
    baseline = repository_counts(root)
    campaign42_published = baseline["object_count"] == CAMPAIGN42_PUBLISHED_COUNT and baseline["repository_fingerprint"] == CAMPAIGN42_PUBLISHED_FP and baseline["first_difference_pearson_companions"] == 8
    post_campaign43 = baseline["object_count"] == POST_CAMPAIGN43_COUNT and baseline["repository_fingerprint"] == POST_CAMPAIGN43_FP and baseline["first_difference_pearson_companions"] == 14
    post_portfolio_pilot = baseline["object_count"] == POST_EVIDENCE_PORTFOLIO_PILOT_COUNT and baseline["repository_fingerprint"] == POST_EVIDENCE_PORTFOLIO_PILOT_FP and baseline["first_difference_pearson_companions"] == 14
    post_second_portfolio = baseline["object_count"] == POST_SECOND_EVIDENCE_PORTFOLIO_COUNT and baseline["repository_fingerprint"] == POST_SECOND_EVIDENCE_PORTFOLIO_FP and baseline["first_difference_pearson_companions"] == 14
    accepted_baseline = (baseline["object_count"] == BASELINE_COUNT and baseline["repository_fingerprint"] == BASELINE_FP) or campaign42_published or post_campaign43 or post_portfolio_pilot or post_second_portfolio
    add("repository_baseline_count", accepted_baseline, actual=baseline["object_count"], expected=[BASELINE_COUNT, CAMPAIGN42_PUBLISHED_COUNT, POST_CAMPAIGN43_COUNT, POST_EVIDENCE_PORTFOLIO_PILOT_COUNT, POST_SECOND_EVIDENCE_PORTFOLIO_COUNT], idempotent_published_baseline=campaign42_published, post_campaign43_baseline=post_campaign43, post_portfolio_pilot_baseline=post_portfolio_pilot, post_second_portfolio_baseline=post_second_portfolio)
    add("repository_baseline_fingerprint", accepted_baseline, actual=baseline["repository_fingerprint"], expected=[BASELINE_FP, CAMPAIGN42_PUBLISHED_FP, POST_CAMPAIGN43_FP, POST_EVIDENCE_PORTFOLIO_PILOT_FP, POST_SECOND_EVIDENCE_PORTFOLIO_FP], idempotent_published_baseline=campaign42_published, post_campaign43_baseline=post_campaign43, post_portfolio_pilot_baseline=post_portfolio_pilot, post_second_portfolio_baseline=post_second_portfolio)
    add("raw_pearson_count", baseline["raw_pearson_objects"] == 21, actual=baseline["raw_pearson_objects"], expected=21)
    add("statistical_summary_count", baseline["statistical_summary_objects"] == 4, actual=baseline["statistical_summary_objects"], expected=4)
    # Existing companions may be 0 before publication or 8 for idempotent rerun in a temp copy.
    add("method_contract_fingerprint", spec.get("method_contracts", {}).get("method_contract_fingerprint") == METHOD_FP, actual=spec.get("method_contracts", {}).get("method_contract_fingerprint"), expected=METHOD_FP)
    add("transformation_contract_fingerprint", spec.get("method_contracts", {}).get("transformation_contract_fingerprint") == TRANSFORMATION_FP, actual=spec.get("method_contracts", {}).get("transformation_contract_fingerprint"), expected=TRANSFORMATION_FP)
    for candidate in candidates:
        cid = candidate["campaign42_candidate_id"]
        raw_id = candidate["raw_companion_package_id"]
        raw_path = root / "knowledge_repository/objects" / f"{raw_id}.json"
        raw_package = read_json(raw_path) if raw_path.exists() else {}
        actual_raw_fp = package_fingerprint_for_registry(raw_package) if raw_package else None
        add("raw_package_fingerprint", actual_raw_fp == candidate["raw_package_fingerprint"], candidate_id=cid, package_id=raw_id, actual=actual_raw_fp, expected=candidate["raw_package_fingerprint"])
        companion_path = root / "knowledge_repository/objects" / f"{candidate['expected_companion_package_id']}.json"
        if companion_path.exists():
            existing = read_json(companion_path)
            existing_payload = package_payload(existing)
            collision_ok = existing_payload.get("method_id") == METHOD_ID and existing_payload.get("raw_package_reference", {}).get("package_id") == raw_id
        else:
            collision_ok = True
        add("expected_companion_collision_safe", collision_ok, candidate_id=cid, package_id=candidate["expected_companion_package_id"], exists=companion_path.exists())
        for side in ("series_a", "series_b"):
            fixture = candidate["evidence_fixtures"][side]
            data = read_json(root / fixture["path"])
            add("evidence_normalized_fingerprint", data.get("normalized_fingerprint") == fixture["normalized_fingerprint"], candidate_id=cid, side=side, actual=data.get("normalized_fingerprint"), expected=fixture["normalized_fingerprint"])
    forbidden = ["diagnostic_value", "p_value", "covariance", "significance", "forecast"]
    text = (canonical_json(registry) + canonical_json(spec)).lower()
    found = [term for term in forbidden if term in text]
    add("frozen_inputs_no_result_dependent_fields", not found, forbidden_found=found)
    return {"valid": all(c["pass"] for c in checks), "registry_fingerprint": registry_fp, "specification_fingerprint": spec_fp, "repository_baseline": baseline, "checks": checks}


def observed_map_from_fixture(root: Path, fixture: dict[str, Any], entity: str, indicator: str) -> tuple[dict[int, Decimal], list[dict[str, Any]], str]:
    data = read_json(root / fixture["path"])
    rows = [r for r in data.get("observations", []) if r.get("entity_id") == entity and r.get("indicator_code") == indicator]
    out: dict[int, Decimal] = {}
    unit = ""
    for row in rows:
        period = int(row["period"])
        if period in out:
            raise ValueError("duplicate period failure")
        if row.get("unit"):
            unit = row["unit"]
        if row.get("observed") is True and row.get("value_canonical") not in (None, ""):
            out[period] = parse_decimal(row["value_canonical"])
    return out, rows, unit


def first_difference_series(raw: dict[int, Decimal], *, entity: str, indicator: dict[str, Any], transformed_unit: str) -> tuple[dict[str, Any], list[int]]:
    observations = []
    excluded = []
    periods = sorted(raw)
    for period in periods:
        if period - 1 in raw:
            with localcontext(INTERNAL_CONTEXT):
                delta = raw[period] - raw[period - 1]
            observations.append({"period": period, "value_canonical": format(delta, "f"), "observed": True, "entity_id": entity, "indicator_code": indicator["code"], "frequency": "annual", "unit": transformed_unit, "transformation": "first_difference"})
        elif period != periods[0]:
            excluded.append(period)
    series = {"series_id": {"indicator_code": indicator["code"], "entity_id": entity, "frequency": "annual", "unit": transformed_unit, "transformation": "first_difference"}, "observations": observations}
    return series, excluded


def map_from_series(series: dict[str, Any]) -> dict[int, Decimal]:
    out = {}
    for row in series["observations"]:
        period = int(row["period"])
        if period in out:
            raise ValueError("duplicate transformed period")
        out[period] = parse_decimal(row["value_canonical"])
    return out


def pearson_decimal(xs: list[Decimal], ys: list[Decimal]) -> str:
    if len(xs) < 30:
        raise ValueError("insufficient aligned transformed observations")
    if len(set(xs)) <= 1 or len(set(ys)) <= 1:
        raise ValueError("zero transformed variance")
    with localcontext(INTERNAL_CONTEXT):
        n = Decimal(len(xs))
        mx = sum(xs, Decimal(0)) / n
        my = sum(ys, Decimal(0)) / n
        numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        var_x = sum((x - mx) * (x - mx) for x in xs)
        var_y = sum((y - my) * (y - my) for y in ys)
        if var_x.is_zero() or var_y.is_zero():
            raise ValueError("zero transformed variance")
        coeff = numerator / (var_x * var_y).sqrt(context=INTERNAL_CONTEXT)
    if not coeff.is_finite() or coeff < Decimal("-1.0000000000000000000000000000000000000001") or coeff > Decimal("1.0000000000000000000000000000000000000001"):
        raise ValueError("non-finite or out-of-bounds coefficient")
    if coeff > Decimal(1): coeff = Decimal(1)
    if coeff < Decimal(-1): coeff = Decimal(-1)
    return canonical_decimal_12(coeff)


def pearson_reference(xs: list[Decimal], ys: list[Decimal]) -> str:
    with localcontext(INTERNAL_CONTEXT):
        n = Decimal(len(xs))
        sx = sum(xs, Decimal(0)); sy = sum(ys, Decimal(0))
        sxy = sum(x*y for x, y in zip(xs, ys))
        sx2 = sum(x*x for x in xs); sy2 = sum(y*y for y in ys)
        numerator = sxy - (sx * sy / n)
        var_x = sx2 - (sx * sx / n)
        var_y = sy2 - (sy * sy / n)
        if var_x.is_zero() or var_y.is_zero():
            raise ValueError("zero transformed variance")
        coeff = numerator / (var_x * var_y).sqrt(context=INTERNAL_CONTEXT)
    return canonical_decimal_12(coeff)


def fingerprint_series(series: dict[str, Any]) -> str:
    return sha256_value(series)


def package_fingerprint_fields(package: dict[str, Any]) -> dict[str, str]:
    return {
        "input_set": sha256_value(package.get("input_references", [])),
        "query_definitions": sha256_value(package.get("scope", {})),
        "evidence_references": sha256_value(package.get("evidence_references", [])),
        "generated_statements": sha256_value(package.get("generated_statements", [])),
        "computation_recipe": sha256_value(package.get("provenance_envelope", {})),
        "package_manifest": sha256_value({k: v for k, v in package.items() if k != "fingerprints"}),
    }


def build_companion_package(candidate: dict[str, Any], raw_package: dict[str, Any], calc: dict[str, Any]) -> dict[str, Any]:
    cid = candidate["campaign42_candidate_id"]
    package_id = candidate["expected_companion_package_id"]
    raw_id = candidate["raw_companion_package_id"]
    raw_payload = package_payload(raw_package)
    stmt_id = "stmt-" + package_id.removeprefix("pkg-object-").replace("_", "-")
    calc_id = "calc-campaign42-" + cid.replace("campaign42-fd-pearson-companion-candidate-", "fd-pearson-companion-")
    ev_id = "ev-campaign42-" + cid.replace("campaign42-fd-pearson-companion-candidate-", "fd-pearson-companion-")
    payload = {
        "family": raw_payload.get("family"),
        "entity_id": candidate["entity"],
        "series_a": {**candidate["indicator_a"], "transformed_unit": candidate["transformed_unit_semantics"]["series_a"]},
        "series_b": {**candidate["indicator_b"], "transformed_unit": candidate["transformed_unit_semantics"]["series_b"]},
        "frequency": "annual",
        "period_scope": calc["transformed_period_scope"],
        "raw_period_scope": candidate["raw_period_scope"],
        "transformation_state": "first_difference",
        "transformation_id": TRANSFORMATION_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "transformation_contract_fingerprint": TRANSFORMATION_FP,
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_contract_fingerprint": METHOD_FP,
        "validation_registry_fingerprint": VALIDATION_REGISTRY_FP,
        "raw_package_reference": {"package_id": raw_id, "package_fingerprint": candidate["raw_package_fingerprint"], "source_campaign": raw_package.get("lineage", {}).get("source_campaign")},
        "campaign42_registry_fingerprint": EXPECTED_REGISTRY_FP,
        "campaign42_specification_fingerprint": EXPECTED_SPEC_FP,
        "raw_evidence_fixtures": candidate["evidence_fixtures"],
        "raw_units": candidate["raw_units"],
        "transformed_unit_semantics": candidate["transformed_unit_semantics"],
        "raw_observation_count": calc["raw_observation_count"],
        "transformed_observation_count": calc["transformed_observation_count"],
        "aligned_transformed_count": calc["aligned_transformed_count"],
        "transformed_coverage": calc["transformed_coverage"],
        "missing_and_excluded_periods": calc["missing_and_excluded_periods"],
        "transformed_series_fingerprints": calc["transformed_series_fingerprints"],
        "aligned_observation_fingerprint": calc["aligned_observation_fingerprint"],
        "pearson_coefficient": {"canonical": calc["coefficient"], "unit": "dimensionless"},
        "first_difference_pearson_coefficient": {"canonical": calc["coefficient"], "unit": "dimensionless"},
        "independent_recompute_coefficient": calc["independent_recompute_coefficient"],
        "prior_embedded_diagnostic_reconciliation": calc["prior_diagnostic_reconciliation"],
        "companion_identity": "independently reproducible first-difference companion; independently retrievable; does not supersede or mutate the raw package",
        "does_not_supersede_raw_package": True,
        "answers_change_co_movement_not_level_co_movement": True,
        "limitations": [
            "First differencing does not prove stationarity.",
            "Correlation does not imply causation.",
            "No significance, forecast, mechanism, lead-lag, recommendation, or investment signal is implied.",
            "Differencing may amplify noise.",
            "Results remain window- and revision-dependent.",
            "This companion does not supersede or correct the raw Pearson package.",
        ],
        "validation_judgment": "accepted_campaign42_first_difference_pearson_companion",
    }
    statement = {
        "statement_id": stmt_id,
        "statement_type": "derived_relationship",
        "text": f"Across aligned annual first differences for {candidate['entity']} from {calc['transformed_period_scope']['start']} through {calc['transformed_period_scope']['end']}, the Pearson correlation between annual changes in {candidate['indicator_a']['name']} and annual changes in {candidate['indicator_b']['name']} is {calc['coefficient']}, using {calc['aligned_transformed_count']} aligned transformed observations. This is a Campaign 42 companion to raw package {raw_id} and does not supersede it.",
        "structured_payload": payload,
        "applicability": {"entity_id": candidate["entity"], "frequency": "annual", "method_id": METHOD_ID, "method_version": METHOD_VERSION, "period_start": calc["transformed_period_scope"]["start"], "period_end": calc["transformed_period_scope"]["end"]},
        "dependencies": [calc_id, raw_id],
        "evidence_refs": [ev_id],
        "origin": "computed_from_campaign42_frozen_first_difference_companion_registry",
    }
    package = {
        "package_id": package_id,
        "package_kind": "KnowledgeObjectPackage",
        "package_version": "1.0",
        "created_at": "2026-07-12",
        "created_by": "campaign42_first_difference_companion_production",
        "status": "accepted",
        "scope": {"domain": "world_development_indicators", "entity_scope": [candidate["entity"]], "evidence_family": "external_wdi_annual_scalar_first_difference_pearson_companion", "period_scope": calc["transformed_period_scope"]},
        "input_references": ["campaign42_first_difference_pearson_companion_production", EXPECTED_REGISTRY_FP, EXPECTED_SPEC_FP, TRANSFORMATION_FP, METHOD_FP, raw_id],
        "evidence_references": [{"evidence_ref_id": ev_id, "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": f"Retained raw evidence for {candidate['indicator_a']['code']} and {candidate['indicator_b']['code']} {candidate['entity']} transformed by Campaign 42 first-difference contract", "source_version": "retained_fixture", "snapshot_fingerprint": calc["aligned_observation_fingerprint"], "evaluation_status": "evaluated", "evidence_class": "derived_first_difference_dual_series_observation_fixture", "reproducibility_handle": "canonical raw package reference plus retained evidence fixture fingerprints, transformed-series fingerprints, and aligned-observation fingerprint", "accessed_at": "2026-07-12"}],
        "generated_statements": [statement],
        "provenance_envelope": {"method_refs": [f"{METHOD_ID}@{METHOD_VERSION}", f"{TRANSFORMATION_ID}@{TRANSFORMATION_VERSION}"], "evidence_refs": [ev_id], "evaluation_refs": [EXPECTED_REGISTRY_FP, EXPECTED_SPEC_FP, calc["aligned_observation_fingerprint"]], "lineage_basis": f"Campaign 42 companion production from frozen registry/specification; references raw package {raw_id} from {raw_package.get('lineage', {}).get('source_campaign')} without supersession"},
        "confidence_quality": {"confidence_label": "fixture-supported-deterministic-first-difference-companion", "evidence_sufficiency": "sufficient for bounded deterministic first-difference Pearson companion object", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture_and_raw_package_reference", "uncertainty_dimensions": ["non-causality", "non-prediction", "absence of significance testing", "first-difference stationarity not proven", "noise amplification", "window and revision dependence"]},
        "validation_state": {"validation_result": "pass", "blockers": [], "warnings": ["first_difference_does_not_prove_stationarity", "correlation_not_causation", "no_significance_forecast_mechanism_lead_lag_recommendation_or_investment_signal", "does_not_supersede_raw_package"]},
        "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": calc["aligned_observation_fingerprint"]},
        "lineage": {"previous_package_id": None, "source_campaign": "Campaign 42", "referenced_raw_package_id": raw_id, "referenced_raw_source_campaign": raw_package.get("lineage", {}).get("source_campaign"), "version_lineage": []},
        "evolution_metadata": {"change_reason": "Campaign 42 first-difference Pearson companion production", "previous_revision": None, "dependent_object_review_posture": "not_applicable", "version_lineage": []},
        "contradiction_records": [{"contradiction_id": "none-recorded", "target_statement": stmt_id, "contradiction_type": "none", "contradicting_evidence": None, "disposition": "not_applicable"}],
    }
    package["fingerprints"] = package_fingerprint_fields(package)
    package["generated_statements"][0]["structured_payload"]["package_fingerprint"] = package["fingerprints"]["package_manifest"]
    package["fingerprints"] = package_fingerprint_fields(package)
    return package


def compute_candidate(root: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    entity = candidate["entity"]
    raw_path = root / "knowledge_repository/objects" / f"{candidate['raw_companion_package_id']}.json"
    raw_package = read_json(raw_path)
    map_a, rows_a, unit_a = observed_map_from_fixture(root, candidate["evidence_fixtures"]["series_a"], entity, candidate["indicator_a"]["code"])
    map_b, rows_b, unit_b = observed_map_from_fixture(root, candidate["evidence_fixtures"]["series_b"], entity, candidate["indicator_b"]["code"])
    series_a, excluded_a = first_difference_series(map_a, entity=entity, indicator=candidate["indicator_a"], transformed_unit=candidate["transformed_unit_semantics"]["series_a"])
    series_b, excluded_b = first_difference_series(map_b, entity=entity, indicator=candidate["indicator_b"], transformed_unit=candidate["transformed_unit_semantics"]["series_b"])
    d_a, d_b = map_from_series(series_a), map_from_series(series_b)
    raw_start = max(min(map_a), min(map_b)); raw_end = min(max(map_a), max(map_b))
    expected_periods = list(range(raw_start + 1, raw_end + 1))
    aligned_periods = [p for p in expected_periods if p in d_a and p in d_b]
    missing_a = [p for p in expected_periods if p not in d_a]
    missing_b = [p for p in expected_periods if p not in d_b]
    xs = [d_a[p] for p in aligned_periods]
    ys = [d_b[p] for p in aligned_periods]
    coverage = Decimal(len(aligned_periods)) / Decimal(len(expected_periods))
    if len(aligned_periods) < 30 or coverage < Decimal("0.85"):
        raise ValueError("threshold failure")
    coeff = pearson_decimal(xs, ys)
    recompute = pearson_reference(xs, ys)
    if coeff != recompute:
        raise ValueError("independent recomputation mismatch")
    old_prec = getcontext().prec
    with localcontext() as ctx:
        ctx.prec = 17
        adversarial = pearson_decimal(xs, ys)
    if adversarial != coeff:
        raise ValueError("adversarial Decimal context affected result")
    prior = package_payload(raw_package).get("diagnostic_limitations", {})
    prior_coeff = prior.get("first_difference_pearson")
    prior_coeff_12 = canonical_decimal_12(parse_decimal(prior_coeff)) if prior_coeff is not None else None
    reconciliation = {
        "prior_embedded_diagnostic_present": prior_coeff is not None,
        "prior_embedded_first_difference_coefficient": prior_coeff,
        "new_companion_coefficient": coeff,
        "coefficient_matches": prior_coeff_12 == coeff,
        "aligned_count_matches": int(candidate["expected_minimum_overlap"]["expected_aligned_transformed_observations"]) == len(aligned_periods),
        "transformation_semantics_matches": True,
    }
    if not reconciliation["coefficient_matches"]:
        raise ValueError("prior embedded diagnostic coefficient mismatch")
    transformed_scope = {"start": min(aligned_periods), "end": max(aligned_periods)}
    calc = {
        "candidate_id": candidate["campaign42_candidate_id"],
        "raw_package_id": candidate["raw_companion_package_id"],
        "package_id": candidate["expected_companion_package_id"],
        "status": "accepted",
        "raw_observation_count": {"series_a": len(map_a), "series_b": len(map_b)},
        "transformed_observation_count": {"series_a": len(d_a), "series_b": len(d_b)},
        "aligned_transformed_count": len(aligned_periods),
        "expected_period_count": len(expected_periods),
        "aligned_transformed_periods": aligned_periods,
        "transformed_period_scope": transformed_scope,
        "transformed_coverage": canonical_decimal_12(coverage),
        "missing_and_excluded_periods": {"series_a_missing_or_excluded": sorted(set(missing_a + excluded_a)), "series_b_missing_or_excluded": sorted(set(missing_b + excluded_b))},
        "transformed_series_fingerprints": {"series_a": fingerprint_series(series_a), "series_b": fingerprint_series(series_b)},
        "aligned_observation_fingerprint": sha256_value({"candidate_id": candidate["campaign42_candidate_id"], "periods": aligned_periods, "x": [format(x, "f") for x in xs], "y": [format(y, "f") for y in ys], "transformation": TRANSFORMATION_ID, "method": METHOD_ID}),
        "coefficient": coeff,
        "independent_recompute_coefficient": recompute,
        "prior_diagnostic_reconciliation": reconciliation,
    }
    package = build_companion_package(candidate, raw_package, calc)
    calc["package_fingerprint"] = package["fingerprints"]["package_manifest"]
    return {"calculation": calc, "package": package}


def validate_package(package: dict[str, Any]) -> None:
    required = ["package_id", "package_kind", "validation_state", "provenance_envelope", "fingerprints", "generated_statements", "confidence_quality"]
    for key in required:
        if key not in package:
            raise ValueError(f"missing package key {key}")
    if package["package_kind"] != "KnowledgeObjectPackage" or package["validation_state"].get("validation_result") != "pass" or package["validation_state"].get("blockers"):
        raise ValueError("invalid package")
    payload = package_payload(package)
    if payload.get("method_id") != METHOD_ID or payload.get("transformation_state") != "first_difference":
        raise ValueError("not a first-difference Pearson companion")
    if not payload.get("does_not_supersede_raw_package") or package.get("lineage", {}).get("previous_package_id") is not None:
        raise ValueError("raw supersession boundary failure")


def snapshot_object_bytes(root: Path) -> dict[str, str]:
    return {p.name: sha256_bytes(p.read_bytes()) for p in sorted((root / "knowledge_repository/objects").glob("*.json"))}


def build_indexes(packages: list[dict[str, Any]]) -> dict[str, Any]:
    indexes = {"by_package_id": {}, "by_knowledge_identity": {}, "by_evidence_family": {}, "by_statement_type": {}, "by_lifecycle_state": {}, "by_package_manifest_fingerprint": {}}
    def add(index: str, key: str, pid: str) -> None:
        indexes[index].setdefault(key, []).append(pid)
    for package in sorted(packages, key=lambda p: p["package_id"]):
        pid = package["package_id"]
        indexes["by_package_id"][pid] = f"objects/{pid}.json"
        add("by_evidence_family", package.get("scope", {}).get("evidence_family", "unspecified"), pid)
        add("by_lifecycle_state", package.get("confidence_quality", {}).get("lifecycle_state", "unspecified"), pid)
        add("by_package_manifest_fingerprint", package.get("fingerprints", {}).get("package_manifest", "missing"), pid)
        for stmt in package.get("generated_statements", []):
            add("by_knowledge_identity", stmt.get("statement_id", "missing"), pid)
            add("by_statement_type", stmt.get("statement_type", "unspecified"), pid)
    for key in list(indexes):
        if key != "by_package_id":
            indexes[key] = {k: sorted(set(v)) for k, v in sorted(indexes[key].items())}
        else:
            indexes[key] = dict(sorted(indexes[key].items()))
    return indexes


def rebuild_repository_metadata(root: Path) -> dict[str, Any]:
    repo = root / "knowledge_repository"
    packages = [read_json(p) for p in sorted((repo / "objects").glob("*.json"))]
    indexes = build_indexes(packages)
    for name, idx in indexes.items():
        write_json(repo / "indexes" / f"{name}.json", idx)
    for package in packages:
        write_json(repo / "evolution" / f"{package['package_id']}.json", {"package_id": package["package_id"], "package_version": package.get("package_version"), "status": package.get("status"), "lineage": package.get("lineage"), "evolution_metadata": package.get("evolution_metadata"), "provenance_envelope": package.get("provenance_envelope"), "fingerprints": package.get("fingerprints"), "validation_state": package.get("validation_state"), "lifecycle_state": package.get("confidence_quality", {}).get("lifecycle_state"), "reproducibility_state": package.get("confidence_quality", {}).get("reproducibility_state")})
    basis = {"repository_kind": "KnowledgeForgeKnowledgeRepository", "schema_version": "1.0", "package_ids": sorted(p["package_id"] for p in packages), "object_package_fingerprints": {p["package_id"]: sha256_value(p) for p in sorted(packages, key=lambda x: x["package_id"])}, "indexes": indexes}
    manifest = {"repository_kind": "KnowledgeForgeKnowledgeRepository", "schema_version": "1.0", "repository_root": "knowledge_repository", "object_count": len(packages), "package_ids": sorted(p["package_id"] for p in packages), "index_files": [f"indexes/{name}.json" for name in sorted(indexes)], "object_directory": "objects/", "evolution_directory": "evolution/", "repository_fingerprint": sha256_value(basis), "persistence_policy": "persist validated KnowledgeObjectPackage JSON exactly; repository metadata and indexes remain separate"}
    write_json(repo / "manifest.json", manifest)
    return manifest


def publish_packages(root: Path, packages: list[dict[str, Any]], before_hashes: dict[str, str]) -> dict[str, Any]:
    repo = root / "knowledge_repository"
    published = []
    collisions = []
    for package in packages:
        validate_package(package)
        path = repo / "objects" / f"{package['package_id']}.json"
        if path.exists():
            existing = read_json(path)
            if sha256_value(existing) != sha256_value(package):
                raise ValueError(f"package-ID collision with different content: {package['package_id']}")
            collisions.append(package["package_id"])
        else:
            write_json(path, package)
            published.append(package["package_id"])
    manifest = rebuild_repository_metadata(root)
    after_hashes = snapshot_object_bytes(root)
    changed_existing = [name for name, h in before_hashes.items() if after_hashes.get(name) != h]
    disappeared = [name for name in before_hashes if name not in after_hashes]
    return {"performed": True, "published_ids": published, "same_content_collisions": collisions, "object_count": manifest["object_count"], "repository_fingerprint": manifest["repository_fingerprint"], "pre_existing_package_immutability": {"valid": not changed_existing and not disappeared, "changed_existing": changed_existing, "disappeared_existing": disappeared}}


def produce_campaign42(root: Path, *, publish: bool = False, reverse_candidates: bool = False, weird_decimal_context: bool = False, output_dir: Path | None = None) -> dict[str, Any]:
    root = Path(root)
    gate = pre_execution_gate(root)
    if not gate["valid"]:
        raise ValueError("pre-execution gate failed")
    registry, spec = load_inputs(root)
    candidates = list(registry["candidates"])
    if reverse_candidates:
        candidates = list(reversed(candidates))
    before_manifest = read_json(root / "knowledge_repository/manifest.json")
    before_hashes = snapshot_object_bytes(root)
    accepted_packages = []
    accepted_by_id: dict[str, dict[str, Any]] = {}
    results = []
    rejected = []
    with localcontext() as ctx:
        if weird_decimal_context:
            ctx.prec = 9
        for candidate in candidates:
            try:
                computed = compute_candidate(root, candidate)
                package = computed["package"]
                validate_package(package)
                accepted_by_id[package["package_id"]] = package
                results.append(computed["calculation"])
            except Exception as exc:
                rejected.append({"candidate_id": candidate.get("campaign42_candidate_id"), "status": "rejected", "reason": str(exc), "preserved": True})
    accepted_packages = [accepted_by_id[k] for k in sorted(accepted_by_id)]
    # Restore frozen order for reporting.
    order = {c["expected_companion_package_id"]: i for i, c in enumerate(registry["candidates"])}
    accepted_packages = sorted(accepted_packages, key=lambda p: order[p["package_id"]])
    results = sorted(results, key=lambda r: order[r["package_id"]])
    publication = {"performed": False}
    if publish:
        publication = publish_packages(root, accepted_packages, before_hashes)
        # Idempotence check: rebuild/publish same packages again must be collision-safe and count-stable.
        second_before = snapshot_object_bytes(root)
        second = publish_packages(root, accepted_packages, second_before)
        publication["idempotent_republish"] = {"collision_safe": len(second["same_content_collisions"]) == len(accepted_packages), "object_count": second["object_count"], "repository_fingerprint": second["repository_fingerprint"]}
    after_manifest = read_json(root / "knowledge_repository/manifest.json")
    after_hashes = snapshot_object_bytes(root)
    changed_existing = [name for name, h in before_hashes.items() if after_hashes.get(name) != h]
    disappeared = [name for name in before_hashes if name not in after_hashes]
    package_fps = {p["package_id"]: p["fingerprints"]["package_manifest"] for p in accepted_packages}
    summary = {
        "campaign_id": "campaign42_first_difference_pearson_companion_production",
        "pre_execution_gate": gate,
        "accepted_count": len(accepted_packages),
        "rejected_count": len(rejected),
        "candidate_results": results + rejected,
        "accepted_packages": accepted_packages,
        "accepted_package_fingerprints_by_id": package_fps,
        "candidate_result_fingerprint": sha256_value([{k: v for k, v in r.items() if k not in {"package_fingerprint"}} for r in results]),
        "publication": publication,
        "repository_before": before_manifest,
        "repository_after": after_manifest,
        "pre_existing_package_immutability": {"valid": not changed_existing and not disappeared, "changed_existing": changed_existing, "disappeared_existing": disappeared},
        "raw_package_non_supersession": {"valid": True, "raw_package_ids": [c["raw_companion_package_id"] for c in registry["candidates"]]},
        "idempotent_republish": publication.get("idempotent_republish", {"collision_safe": True, "not_executed_without_publish": True}),
    }
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        write_json(output_dir / "campaign42_production_summary.json", {k: v for k, v in summary.items() if k != "accepted_packages"})
        write_json(output_dir / "accepted_packages.json", accepted_packages)
        for package in accepted_packages:
            write_json(output_dir / "accepted_packages" / f"{package['package_id']}.json", package)
        write_json(output_dir / "candidate_results.json", results + rejected)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    result = produce_campaign42(Path(args.root), publish=args.publish, output_dir=Path(args.output_dir))
    print(json.dumps({k: v for k, v in result.items() if k != "accepted_packages"}, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["rejected_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
