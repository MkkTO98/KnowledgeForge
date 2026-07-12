#!/usr/bin/env python3
"""Deterministic first-difference Pearson method contract validation tooling.

Bounded method validation only: no canonical package promotion, no PostgreSQL
writes, no production campaign execution.
"""
from __future__ import annotations

import hashlib
import json
from decimal import Context, Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRANSFORMATION_ID = "wdi_annual_scalar_first_difference_v1"
TRANSFORMATION_VERSION = "1.0"
METHOD_ID = "wdi_annual_scalar_first_difference_pearson_v1"
METHOD_VERSION = "1.0"
PEARSON_BASE_METHOD_ID = "wdi_annual_scalar_pearson_correlation_v1"
PEARSON_BASE_METHOD_VERSION = "1.0"
INTERNAL_PRECISION = 50
CANONICAL_DECIMAL_PLACES = 12
ROUNDING = ROUND_HALF_EVEN
MINIMUM_ALIGNED_TRANSFORMED_OBSERVATIONS = 30
MINIMUM_TRANSFORMED_COVERAGE = Decimal("0.85")
_CTX = Context(prec=INTERNAL_PRECISION, rounding=ROUNDING)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: str | Path) -> Any:
    p = Path(path)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    return json.loads(p.read_text())


def write_json(path: str | Path, value: Any) -> None:
    p = Path(path)
    if not p.is_absolute():
        p = PROJECT_ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def _canonical_decimal(value: Decimal) -> str:
    with localcontext(_CTX):
        q = Decimal(1).scaleb(-CANONICAL_DECIMAL_PLACES)
        rounded = value.quantize(q)
    if rounded.is_zero():
        return "0"
    text = format(rounded, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if "E" in text.upper():
        raise ValueError("scientific notation forbidden")
    return text or "0"


def _parse_decimal(value: Any) -> Decimal:
    if value is None:
        raise ValueError("missing numeric value")
    text = str(value)
    if "e" in text.lower():
        raise ValueError("scientific notation forbidden")
    try:
        dec = Decimal(text)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal value: {value!r}") from exc
    if not dec.is_finite():
        raise ValueError("non-finite decimal value")
    return dec


def transformed_unit(raw_unit: str) -> str:
    unit = (raw_unit or "").strip()
    if not unit:
        raise ValueError("unresolved unit")
    lowered = unit.lower()
    if lowered in {"% of gdp", "percent of gdp"}:
        return "year-to-year change in percentage points of GDP"
    if "%" in unit or "percent" in lowered or "percentage" in lowered:
        return "year-to-year percentage-point change"
    if "per 1,000" in lowered or "per 1000" in lowered:
        return f"absolute year-to-year change in {unit}"
    if "per 100" in lowered:
        return f"absolute year-to-year change in {unit}"
    if "$" in unit or "currency" in lowered or "us$" in lowered:
        return f"year-to-year change in {unit}"
    if lowered in {"count", "number"} or "people" in lowered:
        return f"year-to-year change in {unit}"
    if unit:
        return f"year-to-year change in {unit}"
    raise ValueError("unresolved unit")


def _series_identity(series: dict[str, Any]) -> dict[str, Any]:
    sid = dict(series.get("series_id") or {})
    sid.setdefault("transformation", "raw")
    return sid


def load_series_from_normalized(path: str | Path) -> dict[str, Any]:
    data = read_json(path)
    observations = data["observations"]
    first = next(row for row in observations if row.get("indicator_code") and row.get("entity_id"))
    meta = data.get("indicator_metadata", {})
    return {
        "series_id": {
            "indicator_code": first["indicator_code"],
            "indicator_name": first.get("indicator_name") or meta.get("name"),
            "indicator_definition": meta.get("definition"),
            "entity_id": first["entity_id"],
            "frequency": first.get("frequency", "annual"),
            "unit": first.get("unit") or meta.get("unit"),
            "transformation": "raw",
        },
        "evidence_identity": {
            "normalized_path": str(Path(path)),
            "normalized_fingerprint": data.get("normalized_fingerprint"),
            "raw_fixture_fingerprint": data.get("source_raw_fixture_fingerprint"),
            "selection_fingerprint": data.get("selection_fingerprint"),
        },
        "observations": [
            {
                "period": int(row["period"]),
                "observed": bool(row.get("observed")),
                "value_canonical": row.get("value_canonical"),
            }
            for row in observations
        ],
    }


def _observed_map(series: dict[str, Any]) -> tuple[dict[int, Decimal], list[int]]:
    out: dict[int, Decimal] = {}
    all_periods: list[int] = []
    for row in series.get("observations", []):
        period = int(row["period"])
        if period in all_periods:
            raise ValueError("duplicate entity-indicator-period key")
        all_periods.append(period)
        if row.get("observed", row.get("value_canonical") is not None) and row.get("value_canonical") is not None:
            out[period] = _parse_decimal(row["value_canonical"])
    return out, sorted(all_periods)


def first_difference_series(series: dict[str, Any]) -> dict[str, Any]:
    sid = _series_identity(series)
    if sid.get("frequency") != "annual":
        raise ValueError("first-difference v1 requires annual frequency")
    if sid.get("transformation", "raw") != "raw":
        raise ValueError("first-difference v1 input must be raw")
    raw_unit = sid.get("unit") or ""
    new_unit = transformed_unit(raw_unit)
    values, all_periods = _observed_map(series)
    observations = []
    for period in sorted(p for p in all_periods if p - 1 in all_periods):
        if period in values and (period - 1) in values:
            with localcontext(_CTX):
                delta = values[period] - values[period - 1]
            if not delta.is_finite():
                raise ValueError("non-finite first difference")
            observations.append({"period": period, "observed": True, "value_canonical": _canonical_decimal(delta)})
        else:
            observations.append({"period": period, "observed": False, "value_canonical": None, "missing_reason": "non_consecutive_or_missing_endpoint"})
    transformed_id = dict(sid)
    transformed_id["transformation"] = "first_difference"
    transformed_id["unit"] = new_unit
    transformed_id["transformation_contract"] = f"{TRANSFORMATION_ID}@{TRANSFORMATION_VERSION}"
    result = {
        "series_id": transformed_id,
        "source_series_id": sid,
        "transformation": {
            "id": TRANSFORMATION_ID,
            "version": TRANSFORMATION_VERSION,
            "formula": "delta_x_t = x_t - x_(t-1)",
            "period_label": "ending period t",
            "gap_behavior": "do not bridge gaps; t and t-1 must be consecutive annual periods with valid observations",
            "unit_semantics": new_unit,
        },
        "evidence_identity": series.get("evidence_identity", {}),
        "observations": observations,
    }
    result["transformed_series_fingerprint"] = sha256_value(result)
    return result


def transformation_contract_v1() -> dict[str, Any]:
    contract = {
        "transformation_id": TRANSFORMATION_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "formula": "delta_x_t = x_t - x_(t-1)",
        "input_frequency": "annual",
        "input_transformation": "raw",
        "period_label_semantics": "transformed observation is labeled by ending period t and represents change from t-1 to t",
        "gap_behavior": "t and t-1 must be consecutive annual periods; do not bridge gaps using previous available observation",
        "missingness_behavior": "missing when either endpoint is missing or invalid",
        "duplicate_key_behavior": "duplicate entity-indicator-period keys fail closed",
        "non_finite_behavior": "non-finite inputs or outputs fail closed",
        "unit_semantics": "absolute year-to-year first differences; never percent growth, percent change, growth rate, or elasticity",
    }
    contract["transformation_contract_fingerprint"] = sha256_value(contract)
    return contract


def method_contract_v1() -> dict[str, Any]:
    contract = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_identity": f"{METHOD_ID}@{METHOD_VERSION}",
        "transformation_contract": transformation_contract_v1(),
        "base_pearson_method": f"{PEARSON_BASE_METHOD_ID}@{PEARSON_BASE_METHOD_VERSION}",
        "decimal_context": {"precision": INTERNAL_PRECISION, "rounding": "ROUND_HALF_EVEN", "local_context_required": True},
        "canonical_decimal_places": CANONICAL_DECIMAL_PLACES,
        "minimum_aligned_transformed_observations": MINIMUM_ALIGNED_TRANSFORMED_OBSERVATIONS,
        "minimum_transformed_coverage": str(MINIMUM_TRANSFORMED_COVERAGE),
        "threshold_justification": "Retained 1990-2024 annual fixtures have at most 34 first differences; 30 preserves raw Pearson v1's minimum evidentiary intent while allowing one-period transformation loss and limited retained missingness. This validation accepts the threshold for bounded companion production; future broader source classes may require revalidation.",
        "population_sample_convention": "Pearson coefficient uses sums of deviations; population/sample covariance scaling cancels in r",
        "zero_variance_handling": "fail closed",
        "non_finite_result_handling": "fail closed",
        "deterministic_ordering": "sort periods and canonicalize pair identity by series identity",
        "prohibited_claims": ["causation", "stationarity", "statistical significance", "prediction", "forecast", "investment signal", "lead-lag structure"],
    }
    contract["method_contract_fingerprint"] = sha256_value({k: v for k, v in contract.items() if k != "method_contract_fingerprint"})
    return contract


def _canonical_series_key(identity: dict[str, Any]) -> str:
    return canonical_json({k: identity.get(k) for k in ["indicator_code", "entity_id", "frequency", "unit", "transformation"]})


def _pearson_from_maps(map_a: dict[int, Decimal], map_b: dict[int, Decimal], expected_periods: list[int], *, minimum: int, coverage_threshold: Decimal) -> dict[str, Any]:
    aligned_periods = sorted(set(map_a) & set(map_b))
    if len(aligned_periods) < minimum:
        raise ValueError("insufficient aligned transformed observations")
    coverage = Decimal(len(aligned_periods)) / Decimal(len(expected_periods) or 1)
    if coverage < coverage_threshold:
        raise ValueError("insufficient transformed coverage")
    xs = [map_a[p] for p in aligned_periods]
    ys = [map_b[p] for p in aligned_periods]
    if len(set(xs)) == 1 or len(set(ys)) == 1:
        raise ValueError("zero variance transformed series")
    with localcontext(_CTX):
        n = Decimal(len(aligned_periods))
        mean_x = sum(xs, Decimal(0)) / n
        mean_y = sum(ys, Decimal(0)) / n
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        var_x = sum((x - mean_x) * (x - mean_x) for x in xs)
        var_y = sum((y - mean_y) * (y - mean_y) for y in ys)
        if var_x.is_zero() or var_y.is_zero():
            raise ValueError("zero variance transformed series")
        coefficient = numerator / (var_x * var_y).sqrt(context=_CTX)
    if coefficient < Decimal("-1") or coefficient > Decimal("1"):
        tolerance = Decimal("1e-40")
        if coefficient < Decimal("-1") and coefficient >= Decimal("-1") - tolerance:
            coefficient = Decimal("-1")
        elif coefficient > Decimal("1") and coefficient <= Decimal("1") + tolerance:
            coefficient = Decimal("1")
        else:
            raise ValueError("coefficient outside [-1, 1]")
    return {
        "aligned_periods": aligned_periods,
        "aligned_transformed_observation_count": len(aligned_periods),
        "expected_transformed_period_count": len(expected_periods),
        "transformed_coverage_share": {"canonical": _canonical_decimal(coverage)},
        "coefficient": {"canonical": _canonical_decimal(coefficient), "unit": "dimensionless"},
        "calculation_terms": {"covariance_numerator": _canonical_decimal(numerator), "variance_x": _canonical_decimal(var_x), "variance_y": _canonical_decimal(var_y)},
    }


def _transformed_observed_map(t: dict[str, Any]) -> tuple[dict[int, Decimal], list[int]]:
    m: dict[int, Decimal] = {}
    periods = []
    for row in t.get("observations", []):
        p = int(row["period"]); periods.append(p)
        if row.get("observed") and row.get("value_canonical") is not None:
            m[p] = _parse_decimal(row["value_canonical"])
    return m, sorted(periods)


def compute_first_difference_pearson(series_a: dict[str, Any], series_b: dict[str, Any], *, minimum_aligned_transformed_observations: int = MINIMUM_ALIGNED_TRANSFORMED_OBSERVATIONS, coverage_threshold: Decimal = MINIMUM_TRANSFORMED_COVERAGE) -> dict[str, Any]:
    id_a = _series_identity(series_a); id_b = _series_identity(series_b)
    if id_a.get("entity_id") != id_b.get("entity_id"):
        raise ValueError("mismatched entities")
    if id_a.get("frequency") != id_b.get("frequency"):
        raise ValueError("mismatched frequencies")
    ta = first_difference_series(series_a); tb = first_difference_series(series_b)
    ma, pa = _transformed_observed_map(ta); mb, pb = _transformed_observed_map(tb)
    expected = sorted(set(pa) | set(pb))
    terms = _pearson_from_maps(ma, mb, expected, minimum=minimum_aligned_transformed_observations, coverage_threshold=coverage_threshold)
    ordered_ids = sorted([ta["series_id"], tb["series_id"]], key=_canonical_series_key)
    aligned_payload = [{"period": p, "series_a": _canonical_decimal(ma[p]), "series_b": _canonical_decimal(mb[p])} for p in terms["aligned_periods"]]
    result = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_identity": f"{METHOD_ID}@{METHOD_VERSION}",
        "method_contract_fingerprint": method_contract_v1()["method_contract_fingerprint"],
        "transformation_id": TRANSFORMATION_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "transformation_contract_fingerprint": transformation_contract_v1()["transformation_contract_fingerprint"],
        "series_a_identity": ordered_ids[0],
        "series_b_identity": ordered_ids[1],
        "input_series_designation_preserved": {"input_a": id_a, "input_b": id_b},
        "raw_period_scope": {"start": min(set(_observed_map(series_a)[1]) | set(_observed_map(series_b)[1])), "end": max(set(_observed_map(series_a)[1]) | set(_observed_map(series_b)[1]))},
        "transformed_period_scope": {"start": min(expected), "end": max(expected)},
        "transformed_series_fingerprints": {"input_a": ta["transformed_series_fingerprint"], "input_b": tb["transformed_series_fingerprint"]},
        "aligned_transformed_observations_fingerprint": sha256_value(aligned_payload),
        "aligned_transformed_observations": aligned_payload,
        **terms,
        "limitations": statistical_limitations(),
    }
    result["canonical_pair_id"] = sha256_value(ordered_ids)
    result["result_fingerprint"] = sha256_value(result)
    return result


def reference_first_difference_pearson(series_a: dict[str, Any], series_b: dict[str, Any]) -> dict[str, Any]:
    # Independent oracle: derives deltas directly from raw maps, not via first_difference_series.
    id_a = _series_identity(series_a); id_b = _series_identity(series_b)
    va, pa = _observed_map(series_a); vb, pb = _observed_map(series_b)
    da: dict[int, Decimal] = {}; db: dict[int, Decimal] = {}
    for p in sorted(pa):
        if p - 1 in pa and p in va and p - 1 in va:
            with localcontext(_CTX): da[p] = va[p] - va[p - 1]
    for p in sorted(pb):
        if p - 1 in pb and p in vb and p - 1 in vb:
            with localcontext(_CTX): db[p] = vb[p] - vb[p - 1]
    expected = sorted((set(p for p in pa if p - 1 in pa)) | (set(p for p in pb if p - 1 in pb)))
    terms = _pearson_from_maps(da, db, expected, minimum=MINIMUM_ALIGNED_TRANSFORMED_OBSERVATIONS, coverage_threshold=MINIMUM_TRANSFORMED_COVERAGE)
    return {"method_id": METHOD_ID, **terms}


def statistical_limitations() -> list[str]:
    return [
        "First differencing does not prove stationarity.",
        "First differencing does not remove every trend or structural break.",
        "Correlation is not causation.",
        "No statistical significance is implied.",
        "No forecast, recommendation, or investment signal is implied.",
        "Results remain finite-window dependent.",
        "Measurement revisions can change results.",
        "Differencing can amplify noise.",
        "Differencing changes the question from level co-movement to change co-movement.",
        "Contemporaneous first-difference correlation does not establish lead-lag structure.",
    ]


def _fixture_path(code: str, entity: str) -> Path | None:
    root = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https"
    matches = sorted(root.glob(f"{code}__{entity}__*/normalized_observations.json"))
    return matches[0] if matches else None


def build_validation_registry() -> dict[str, Any]:
    cases = [
        {"case_id": "close_complete_nor_birth_under5", "entity": "NOR", "series_a": "SP.DYN.CBRT.IN", "series_b": "SH.DYN.MORT", "semantic": "close", "expected_pressure": "complete coverage"},
        {"case_id": "remote_missing_dnk_forest_broad_money", "entity": "DNK", "series_a": "AG.LND.FRST.ZS", "series_b": "FM.LBL.BMNY.GD.ZS", "semantic": "remote", "expected_pressure": "missing raw periods"},
        {"case_id": "strong_raw_weak_diff_swe_credit_internet", "entity": "SWE", "series_a": "FS.AST.PRVT.GD.ZS", "series_b": "IT.NET.USER.ZS", "semantic": "moderate", "expected_pressure": "strong raw weak first-difference diagnostic"},
        {"case_id": "close_nor_birth_life", "entity": "NOR", "series_a": "SP.DYN.CBRT.IN", "series_b": "SP.DYN.LE00.IN", "semantic": "close", "expected_pressure": "candidate-policy future pool"},
        {"case_id": "negative_zero_variance", "synthetic": True, "negative_case": "zero_variance_transformed_series"},
        {"case_id": "negative_insufficient_overlap", "synthetic": True, "negative_case": "insufficient_transformed_overlap"},
        {"case_id": "negative_non_consecutive_gap", "synthetic": True, "negative_case": "non_consecutive_gap_no_bridge"},
        {"case_id": "negative_duplicate_period", "synthetic": True, "negative_case": "duplicate_period"},
        {"case_id": "negative_unresolved_unit", "synthetic": True, "negative_case": "unresolved_unit"},
    ]
    registry = {
        "registry_id": "first_difference_pearson_method_validation_registry_20260712",
        "coefficient_free": True,
        "method_under_validation": f"{METHOD_ID}@{METHOD_VERSION}",
        "evidence_boundary": "retained validated KnowledgeForge Campaign 40/41 evidence only; synthetic negatives for fail-closed semantics",
        "cases": cases,
        "validation_case_count": len(cases),
        "forbidden_selection_inputs": ["post-calculation numeric outcomes", "statistical-test outputs", "post-calculation acceptance outcome"],
    }
    registry["registry_fingerprint"] = sha256_value({k: v for k, v in registry.items() if k != "registry_fingerprint"})
    return registry


def validate_registry_and_compute_cases() -> dict[str, Any]:
    registry = build_validation_registry()
    results = []
    for case in registry["cases"]:
        if case.get("synthetic"):
            continue
        pa = _fixture_path(case["series_a"], case["entity"]); pb = _fixture_path(case["series_b"], case["entity"])
        if not pa or not pb:
            results.append({"case_id": case["case_id"], "status": "missing_fixture"}); continue
        res = compute_first_difference_pearson(load_series_from_normalized(pa), load_series_from_normalized(pb))
        results.append({"case_id": case["case_id"], "status": "pass", "coefficient": res["coefficient"], "aligned_periods": res["aligned_periods"], "aligned_count": res["aligned_transformed_observation_count"], "result_fingerprint": res["result_fingerprint"]})
    return {"registry": registry, "case_results": results, "case_results_fingerprint": sha256_value(results)}


def _pearson_packages() -> list[dict[str, Any]]:
    out = []
    for path in sorted((PROJECT_ROOT / "knowledge_repository/objects").glob("*.json")):
        pkg = read_json(path)
        pl = (pkg.get("generated_statements") or [{}])[0].get("structured_payload") or {}
        diag = pl.get("diagnostic_limitations") or {}
        if isinstance(diag, dict) and diag.get("first_difference_pearson") is not None:
            out.append(pkg)
    return out


def _canonical_precision_match(prior: str, new: str) -> tuple[bool, str]:
    prior_dec = _parse_decimal(prior)
    new_dec = _parse_decimal(new)
    if prior_dec == new_dec:
        return True, "exact_decimal_match"
    exponent = prior_dec.as_tuple().exponent
    prior_places = abs(int(exponent)) if isinstance(exponent, int) and exponent < 0 else 0
    with localcontext(_CTX):
        q = Decimal(1).scaleb(-prior_places)
        if new_dec.quantize(q) == prior_dec:
            return True, f"new_value_matches_when_quantized_to_prior_{prior_places}_decimal_places"
    return False, "canonical value differs"


def reconcile_existing_first_difference_diagnostics() -> dict[str, Any]:
    comparisons = []
    mismatches = []
    for pkg in _pearson_packages():
        pl = pkg["generated_statements"][0]["structured_payload"]
        a = pl["series_a"]; b = pl["series_b"]; entity = pl["entity_id"]
        pa = _fixture_path(a["code"], entity); pb = _fixture_path(b["code"], entity)
        if not pa or not pb:
            continue
        try:
            res = compute_first_difference_pearson(load_series_from_normalized(pa), load_series_from_normalized(pb))
            prior = str(pl["diagnostic_limitations"]["first_difference_pearson"])
            new = res["coefficient"]["canonical"]
            match, match_basis = _canonical_precision_match(prior, new)
            comp = {"package_id": pkg["package_id"], "series_a": a["code"], "series_b": b["code"], "entity": entity, "prior_diagnostic_value": prior, "newly_recomputed_value": new, "canonical_precision_match": match, "match_basis": match_basis, "aligned_transformed_periods": res["aligned_periods"], "aligned_transformed_observation_count": res["aligned_transformed_observation_count"], "result_fingerprint": res["result_fingerprint"]}
            comparisons.append(comp)
            if not match:
                mismatches.append({**comp, "mismatch_reason": match_basis})
        except Exception as exc:
            mismatches.append({"package_id": pkg.get("package_id"), "mismatch_reason": str(exc)})
    report = {"compared_count": len(comparisons), "mismatch_count": len(mismatches), "comparisons": comparisons, "mismatches": mismatches}
    report["reconciliation_fingerprint"] = sha256_value(report)
    return report


def simulate_companion_package_payload(comparison: dict[str, Any]) -> dict[str, Any]:
    package_id = "pkg-object-method-validation-first-difference-companion-" + comparison["package_id"].replace("pkg-object-", "")
    package = {
        "package_id": package_id,
        "package_kind": "KnowledgeObjectPackage",
        "status": "validation_simulation_only_not_canonical",
        "scope": {"evidence_family": "WDI annual scalar relationship"},
        "confidence_quality": {"lifecycle_state": "simulated"},
        "generated_statements": [{
            "statement_id": package_id.replace("pkg-object-", "stmt-"),
            "statement_type": "derived_relationship",
            "structured_payload": {
                "method_id": METHOD_ID,
                "method_version": METHOD_VERSION,
                "method_contract_fingerprint": method_contract_v1()["method_contract_fingerprint"],
                "entity_id": comparison["entity"],
                "frequency": "annual",
                "transformation_state": "first_difference",
                "raw_period_scope": {"start": 1990, "end": 2024},
                "transformed_period_scope": {"start": min(comparison["aligned_transformed_periods"]), "end": max(comparison["aligned_transformed_periods"])},
                "pearson_coefficient": {"canonical": comparison["newly_recomputed_value"], "unit": "dimensionless"},
                "companion_raw_package_id": comparison["package_id"],
                "series_a": {"code": comparison["series_a"], "transformation": "first_difference"},
                "series_b": {"code": comparison["series_b"], "transformation": "first_difference"},
                "limitations": statistical_limitations(),
            },
        }],
        "provenance_envelope": {"evidence_refs": ["validation_simulation_existing_retained_fixtures"], "method_contract": method_contract_v1()["method_contract_fingerprint"]},
        "fingerprints": {},
    }
    package["fingerprints"]["package_payload"] = sha256_value(package)
    package["fingerprints"]["package_manifest"] = sha256_value({"package_id": package_id, "payload": package["fingerprints"]["package_payload"]})
    return package


def validate_representation_compatibility(package: dict[str, Any]) -> dict[str, Any]:
    pl = package["generated_statements"][0]["structured_payload"]
    required = ["method_id", "method_version", "method_contract_fingerprint", "raw_period_scope", "transformed_period_scope", "pearson_coefficient", "companion_raw_package_id", "limitations"]
    missing = [k for k in required if k not in pl]
    return {
        "package_representation_valid": not missing and package.get("package_kind") == "KnowledgeObjectPackage",
        "postgresql_projection_compatible": not missing and "generated_statements" in package and "provenance_envelope" in package and "fingerprints" in package,
        "relationship_export_compatible": not missing and pl.get("method_id") == METHOD_ID and pl.get("transformation_state") == "first_difference",
        "missing_fields": missing,
        "schema_change_required": False,
        "new_package_field_required": False,
    }


def write_validation_artifacts(base: str | Path) -> dict[str, str]:
    base = Path(base)
    if not base.is_absolute(): base = PROJECT_ROOT / base
    base.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "transformation_contract": transformation_contract_v1(),
        "method_contract": method_contract_v1(),
        "validation_registry": build_validation_registry(),
        "validation_results": validate_registry_and_compute_cases(),
        "diagnostic_reconciliation": reconcile_existing_first_difference_diagnostics(),
    }
    paths = {}
    for name, obj in artifacts.items():
        path = base / f"{name}.json"
        write_json(path, obj)
        paths[name] = str(path.relative_to(PROJECT_ROOT))
    # Representation proof based on first available comparison.
    rec = artifacts["diagnostic_reconciliation"]
    if rec["comparisons"]:
        pkg = simulate_companion_package_payload(rec["comparisons"][0])
        proof = {"simulated_package": pkg, "compatibility": validate_representation_compatibility(pkg)}
        path = base / "representation_compatibility_proof.json"
        write_json(path, proof); paths["representation_compatibility_proof"] = str(path.relative_to(PROJECT_ROOT))
    return paths


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-artifacts")
    args = ap.parse_args()
    if args.write_artifacts:
        print(json.dumps(write_validation_artifacts(args.write_artifacts), indent=2, sort_keys=True))
    else:
        print(json.dumps(method_contract_v1(), indent=2, sort_keys=True))
