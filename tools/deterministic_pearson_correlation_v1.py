#!/usr/bin/env python3
"""Deterministic contemporaneous Pearson correlation v1.

Bounded method tooling only: no production promotion, no p-values, no
regression, no lagged relationships, and no causal/forecast semantics.
"""
from __future__ import annotations

import hashlib
import json
from decimal import Context, Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext
from typing import Any

METHOD_ID = "wdi_annual_scalar_pearson_correlation_v1"
METHOD_VERSION = "1.0"
INTERNAL_PRECISION = 50
CANONICAL_DECIMAL_PLACES = 12
ROUNDING = ROUND_HALF_EVEN
MINIMUM_ALIGNED_PAIRS = 30
COVERAGE_THRESHOLD = Decimal("0.85")
_ALLOWED_TRANSFORMATIONS = {"raw", "first_difference", "percentage_change", "log_difference"}
_CTX = Context(prec=INTERNAL_PRECISION, rounding=ROUNDING)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


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


def calculation_contract_v1() -> dict[str, Any]:
    contract = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_identity": f"{METHOD_ID}@{METHOD_VERSION}",
        "accepted_numeric_representation": "base-10 decimal strings; scientific notation forbidden",
        "decimal_context": {"precision": INTERNAL_PRECISION, "rounding": "ROUND_HALF_EVEN", "local_context_required": True},
        "canonical_stored_decimal_places": CANONICAL_DECIMAL_PLACES,
        "canonical_serialization": "JSON sort_keys=True compact separators UTF-8",
        "series_identity": ["indicator_code", "entity_id", "frequency", "unit", "transformation"],
        "entity_scope": "same entity by default for first pilot; cross-entity allowed only if explicitly requested",
        "frequency": "annual scalar observations for this method family",
        "period_scope": "intersection of observed periods after explicit missing-pair exclusion",
        "transformation_state": ["raw", "first_difference", "percentage_change", "log_difference", "other explicit derived transformation"],
        "observation_key_alignment": "period equality after series identity validation",
        "join_semantics": "inner join on observed periods",
        "missing_pair_exclusion": "exclude pairs where either value is missing; record missing/excluded periods",
        "minimum_pair_threshold": MINIMUM_ALIGNED_PAIRS,
        "coverage_threshold": str(COVERAGE_THRESHOLD),
        "duplicate_handling": "duplicate period keys fail closed",
        "constant_series_rejection": True,
        "zero_variance_rejection": True,
        "covariance_numerator": "sum((x_i - mean_x) * (y_i - mean_y))",
        "variance_terms": "sum((x_i - mean_x)^2), sum((y_i - mean_y)^2)",
        "pearson_formula": "covariance numerator / sqrt(variance_x * variance_y)",
        "coefficient_bounds_validation": "accepted coefficients must lie in [-1, 1]; tiny Decimal overrun is clamped only if within 1e-40",
        "negative_zero_handling": "canonicalize to 0",
        "scientific_notation_policy": "forbidden in inputs and canonical outputs",
        "output_fingerprint": "sha256 of canonical result excluding no fields",
        "prohibited_outputs": ["p-values", "confidence intervals", "hypothesis tests", "regression coefficients", "Spearman", "partial correlation", "rolling correlation", "lagged correlation", "multiple-testing correction"],
    }
    contract["calculation_contract_fingerprint"] = sha256_value({k: v for k, v in contract.items() if k != "calculation_contract_fingerprint"})
    return contract


def _series_identity(series: dict[str, Any]) -> dict[str, Any]:
    sid = dict(series.get("series_id") or {})
    sid.setdefault("transformation", "raw")
    return sid


def _canonical_series_key(identity: dict[str, Any]) -> str:
    return canonical_json({k: identity.get(k) for k in ["indicator_code", "entity_id", "frequency", "unit", "transformation"]})


def _observed_map(series: dict[str, Any]) -> dict[int, Decimal]:
    out: dict[int, Decimal] = {}
    for row in series.get("observations", []):
        period = int(row["period"])
        if period in out:
            raise ValueError("duplicate observation key")
        if row.get("observed", row.get("value_canonical") is not None) and row.get("value_canonical") is not None:
            out[period] = _parse_decimal(row["value_canonical"])
    return out


def _strong_time_ordering(values: list[Decimal]) -> bool:
    if len(values) < 4:
        return False
    inc = all(values[i] <= values[i + 1] for i in range(len(values) - 1))
    dec = all(values[i] >= values[i + 1] for i in range(len(values) - 1))
    return inc or dec


def _validate_scope(id_a: dict[str, Any], id_b: dict[str, Any], same_entity_required: bool) -> None:
    if same_entity_required and id_a.get("entity_id") != id_b.get("entity_id"):
        raise ValueError("mismatched entities")
    if id_a.get("frequency") != id_b.get("frequency"):
        raise ValueError("mismatched frequencies")
    if id_a.get("transformation", "raw") not in _ALLOWED_TRANSFORMATIONS or id_b.get("transformation", "raw") not in _ALLOWED_TRANSFORMATIONS:
        raise ValueError("unsupported transformation")
    if id_a.get("transformation", "raw") != id_b.get("transformation", "raw"):
        raise ValueError("mismatched transformations")


def compute_correlation(
    series_a: dict[str, Any],
    series_b: dict[str, Any],
    *,
    minimum_aligned_pairs: int = MINIMUM_ALIGNED_PAIRS,
    coverage_threshold: Decimal = COVERAGE_THRESHOLD,
    same_entity_required: bool = True,
) -> dict[str, Any]:
    id_a = _series_identity(series_a)
    id_b = _series_identity(series_b)
    _validate_scope(id_a, id_b, same_entity_required)
    map_a = _observed_map(series_a)
    map_b = _observed_map(series_b)
    periods_a, periods_b = set(map_a), set(map_b)
    aligned_periods = sorted(periods_a & periods_b)
    if not aligned_periods:
        raise ValueError("no overlapping periods")
    expected_periods = sorted({int(row["period"]) for row in series_a.get("observations", [])} | {int(row["period"]) for row in series_b.get("observations", [])})
    if len(aligned_periods) < minimum_aligned_pairs:
        raise ValueError("insufficient aligned pairs")
    coverage = Decimal(len(aligned_periods)) / Decimal(len(expected_periods) or 1)
    if coverage < coverage_threshold:
        raise ValueError("insufficient aligned coverage")
    xs = [map_a[p] for p in aligned_periods]
    ys = [map_b[p] for p in aligned_periods]
    if len(set(xs)) == 1 or len(set(ys)) == 1:
        raise ValueError("constant series / zero variance")
    with localcontext(_CTX):
        n = Decimal(len(aligned_periods))
        mean_x = sum(xs, Decimal(0)) / n
        mean_y = sum(ys, Decimal(0)) / n
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        var_x = sum((x - mean_x) * (x - mean_x) for x in xs)
        var_y = sum((y - mean_y) * (y - mean_y) for y in ys)
        if var_x.is_zero() or var_y.is_zero():
            raise ValueError("constant series / zero variance")
        denominator = (var_x * var_y).sqrt(context=_CTX)
        coeff = numerator / denominator
    if coeff < Decimal("-1") or coeff > Decimal("1"):
        tolerance = Decimal("1e-40")
        if coeff < Decimal("-1") and coeff >= Decimal("-1") - tolerance:
            coeff = Decimal("-1")
        elif coeff > Decimal("1") and coeff <= Decimal("1") + tolerance:
            coeff = Decimal("1")
        else:
            raise ValueError("coefficient outside [-1, 1]")
    identity_a = _canonical_series_key(id_a)
    identity_b = _canonical_series_key(id_b)
    ordered_ids = sorted([id_a, id_b], key=_canonical_series_key)
    result = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_identity": f"{METHOD_ID}@{METHOD_VERSION}",
        "calculation_contract_fingerprint": calculation_contract_v1()["calculation_contract_fingerprint"],
        "canonical_pair_id": sha256_value(ordered_ids),
        "series_a_identity": ordered_ids[0],
        "series_b_identity": ordered_ids[1],
        "input_series_designation_preserved": {"input_a": id_a, "input_b": id_b},
        "aligned_periods": aligned_periods,
        "aligned_pair_count": len(aligned_periods),
        "expected_period_count": len(expected_periods),
        "missing_pair_count": len(expected_periods) - len(aligned_periods),
        "coverage_share": {"canonical": _canonical_decimal(coverage)},
        "coefficient": {"canonical": _canonical_decimal(coeff)},
        "calculation_terms": {"covariance_numerator": _canonical_decimal(numerator), "variance_x": _canonical_decimal(var_x), "variance_y": _canonical_decimal(var_y)},
        "transformation_state": {"series_a": id_a.get("transformation", "raw"), "series_b": id_b.get("transformation", "raw")},
        "diagnostics": {
            "series_a_strong_time_ordering": _strong_time_ordering(xs),
            "series_b_strong_time_ordering": _strong_time_ordering(ys),
            "spurious_correlation_warning": "correlation may be spurious due to common trends, structural breaks, autocorrelation, shared construction, or common external factors",
            "causal_interpretation_allowed": False,
        },
        "limitations": [
            "No causation, explanation, mechanism, predictive power, economic significance, statistical significance, stationarity, independence, investment relevance, recommendation, lead/lag, or trend claim is implied.",
        ],
    }
    result["output_fingerprint"] = sha256_value(result)
    return result


def screen_candidate_pair(candidate: dict[str, Any]) -> dict[str, Any]:
    risks = []
    if candidate.get("series_a_code") == candidate.get("series_b_code"):
        risks.append("identical_series")
    if candidate.get("relationship_risk") in {"component_vs_total", "mechanical_identity", "algebraic_overlap"}:
        risks.append(candidate["relationship_risk"])
    if candidate.get("unit_a") and candidate.get("unit_b") and candidate.get("unit_a") != candidate.get("unit_b"):
        risks.append("unit_mismatch")
    decision = "reject" if risks else "candidate"
    return {"decision": decision, "risks": risks, "candidate": candidate}
