#!/usr/bin/env python3
"""Deterministic statistical-summary calculation contract v2.

This module is deliberately narrow. It supports the accepted annual-scalar
statistical-summary method family and establishes its own Decimal context for
all calculations so outputs do not depend on process-global Decimal state.
"""
from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, ROUND_HALF_EVEN, Context, InvalidOperation, localcontext
from pathlib import Path
from typing import Any

METHOD_ID = "wdi_annual_scalar_statistical_summary_v2"
METHOD_VERSION = "2.0"
INTERNAL_DECIMAL_PRECISION = 50
INTERNAL_ROUNDING_MODE = ROUND_HALF_EVEN
CANONICAL_STORED_DECIMAL_PLACES = 12
HUMAN_DISPLAY_DECIMAL_PLACES = 4
DEFAULT_MINIMUM_OBSERVED_COUNT = 30
DEFAULT_MINIMUM_COVERAGE_SHARE = "0.85"
_NUMERIC_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _fixed_context() -> Context:
    return Context(prec=INTERNAL_DECIMAL_PRECISION, rounding=INTERNAL_ROUNDING_MODE)


def calculation_contract_v2(
    *,
    minimum_observed_count: int = DEFAULT_MINIMUM_OBSERVED_COUNT,
    minimum_coverage_share: str = DEFAULT_MINIMUM_COVERAGE_SHARE,
) -> dict[str, Any]:
    contract: dict[str, Any] = {
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "internal_decimal_precision": INTERNAL_DECIMAL_PRECISION,
        "internal_rounding_mode": "ROUND_HALF_EVEN",
        "input_numerical_canonicalization": "base-10 plain decimal strings only; scientific notation, commas, locale formatting, NaN, and infinity rejected",
        "observation_ordering": ["entity_id", "indicator_code", "period"],
        "summation_algorithm": "stable-order left-to-right Decimal addition inside local Context(prec=50, rounding=ROUND_HALF_EVEN)",
        "arithmetic_mean_algorithm": "stable-order Decimal sum divided by observed_count inside the pinned local context",
        "median_algorithm": "sort observed Decimal values ascending; odd N uses middle value; even N averages two middle values inside pinned context",
        "population_standard_deviation_formula": "sqrt(sum((x - mean)^2) / N)",
        "population_standard_deviation_denominator": "N observed values",
        "square_root_method": "Decimal.sqrt(context=pinned Context(prec=50, rounding=ROUND_HALF_EVEN))",
        "canonical_stored_decimal_places": CANONICAL_STORED_DECIMAL_PLACES,
        "canonical_rounding_policy": "ROUND_HALF_EVEN",
        "human_display_decimal_places": HUMAN_DISPLAY_DECIMAL_PLACES,
        "trailing_zero_normalization": "strip_fractional_trailing_zeros",
        "negative_zero_handling": "canonicalize_to_zero",
        "scientific_notation_policy": "forbidden_in_canonical_values",
        "missing_value_treatment": "preserve missing rows; missing rows must have value_canonical null; numerical measures use observed rows only",
        "minimum_observed_count": minimum_observed_count,
        "minimum_coverage_share": str(Decimal(minimum_coverage_share)),
        "deterministic_serialization_rules": "canonical JSON sort_keys=True separators=(',', ':') ensure_ascii=False encoded as UTF-8 for fingerprints",
    }
    contract["calculation_contract_fingerprint"] = sha256_fingerprint(
        {k: v for k, v in contract.items() if k != "calculation_contract_fingerprint"}
    )
    return contract


def _parse_decimal(raw: str) -> Decimal:
    if not isinstance(raw, str) or not _NUMERIC_RE.fullmatch(raw):
        raise ValueError(f"non-canonical numeric string: {raw!r}")
    with localcontext(_fixed_context()):
        value = Decimal(raw)
        if not value.is_finite():
            raise ValueError(f"non-finite numeric string: {raw!r}")
        return +value


def _decimal_places_quantum(places: int) -> Decimal:
    return Decimal(1).scaleb(-places)


def _canonical_decimal(value: Decimal, *, places: int = CANONICAL_STORED_DECIMAL_PLACES) -> str:
    with localcontext(_fixed_context()) as ctx:
        quantized = value.quantize(_decimal_places_quantum(places), context=ctx)
        if quantized.is_zero():
            return "0"
        text = format(quantized, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        if text == "-0":
            return "0"
        if "E" in text or "e" in text:
            raise ValueError("scientific notation not allowed in canonical values")
        return text


def _display_decimal(value: Decimal) -> str:
    return _canonical_decimal(value, places=HUMAN_DISPLAY_DECIMAL_PLACES)


def _measure(value: Decimal, unit: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"canonical": _canonical_decimal(value), "display": _display_decimal(value)}
    if unit is not None:
        out["unit"] = unit
    return out


def _observed_rows(normalized: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, Any, Any]] = set()
    rows: list[dict[str, Any]] = []
    for row in normalized.get("observations", []):
        key = (row.get("entity_id"), row.get("indicator_code"), row.get("period"))
        if key in seen:
            raise ValueError(f"duplicate observation key: {key}")
        seen.add(key)
        observed = bool(row.get("observed"))
        value = row.get("value_canonical")
        if observed and value is None:
            raise ValueError(f"observed row missing value: {key}")
        if not observed and value is not None:
            raise ValueError(f"missing row must not carry value: {key}")
        if observed:
            rows.append(row)
    return sorted(rows, key=lambda row: (row["entity_id"], row["indicator_code"], row["period"]))


def _all_rows_sorted(normalized: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(normalized.get("observations", []), key=lambda row: (row["entity_id"], row["indicator_code"], row["period"]))


def compute_statistical_summary_v2(
    normalized: dict[str, Any],
    *,
    minimum_observed_count: int = DEFAULT_MINIMUM_OBSERVED_COUNT,
    minimum_coverage_share: str = DEFAULT_MINIMUM_COVERAGE_SHARE,
) -> dict[str, Any]:
    expected = int(normalized.get("expected_observation_slots", len(normalized.get("observations", []))))
    if expected <= 0:
        raise ValueError("expected observation slots must be positive")
    observed_rows = _observed_rows(normalized)
    observed_count = len(observed_rows)
    if observed_count < minimum_observed_count:
        raise ValueError("observed count below minimum")
    with localcontext(_fixed_context()) as ctx:
        min_coverage = Decimal(minimum_coverage_share)
        coverage = ctx.divide(Decimal(observed_count), Decimal(expected))
        if coverage < min_coverage:
            raise ValueError("coverage below minimum")
        missing_count = expected - observed_count
        missing_share = ctx.divide(Decimal(missing_count), Decimal(expected))
        values = [_parse_decimal(row["value_canonical"]) for row in observed_rows]
        total = Decimal(0)
        for value in values:
            total = ctx.add(total, value)
        mean = ctx.divide(total, Decimal(observed_count))
        ordered_values = sorted(values)
        if observed_count % 2:
            median = ordered_values[observed_count // 2]
        else:
            median = ctx.divide(ctx.add(ordered_values[observed_count // 2 - 1], ordered_values[observed_count // 2]), Decimal(2))
        variance_sum = Decimal(0)
        for value in values:
            diff = ctx.subtract(value, mean)
            variance_sum = ctx.add(variance_sum, ctx.multiply(diff, diff))
        variance = ctx.divide(variance_sum, Decimal(observed_count))
        stddev = variance.sqrt(context=ctx)
        sorted_pairs = sorted(zip(values, observed_rows), key=lambda item: (item[0], item[1]["period"]))
        min_value = sorted_pairs[0][0]
        max_value = sorted_pairs[-1][0]
        unit = observed_rows[0].get("unit")
        all_rows = _all_rows_sorted(normalized)
        return {
            "method_id": METHOD_ID,
            "method_version": METHOD_VERSION,
            "expected_observation_slot_count": expected,
            "observed_count": observed_count,
            "missing_count": missing_count,
            "missing_share": _measure(missing_share),
            "coverage_share": _measure(coverage),
            "first_valid_observation": {
                "period": observed_rows[0]["period"],
                "value": _canonical_decimal(values[0]),
                "unit": unit,
            },
            "last_valid_observation": {
                "period": observed_rows[-1]["period"],
                "value": _canonical_decimal(values[-1]),
                "unit": unit,
            },
            "minimum": {
                **_measure(min_value, unit),
                "periods": [row["period"] for value, row in sorted_pairs if value == min_value],
            },
            "maximum": {
                **_measure(max_value, unit),
                "periods": [row["period"] for value, row in sorted_pairs if value == max_value],
            },
            "arithmetic_mean": _measure(mean, unit),
            "median": _measure(median, unit),
            "population_standard_deviation": _measure(stddev, unit),
            "period_coverage": {
                "start_period": min(row["period"] for row in all_rows),
                "end_period": max(row["period"] for row in all_rows),
                "frequency": "annual",
            },
            "unit": unit,
            "conditional_measure_context": {
                "summarized_population": "retained observed annual scalar values in the stated entity/indicator/window scope",
                "prohibited_interpretations": [
                    "causation",
                    "forecasting",
                    "statistical significance",
                    "stationarity",
                    "randomness_or_independence_of_ordered_annual_observations",
                    "normative_judgment",
                    "investment_implication",
                    "trend_conclusion",
                ],
            },
        }


def _normalized_input_summary(normalized: dict[str, Any]) -> dict[str, Any]:
    selection = normalized.get("selection_contract", {})
    return {
        "input_normalized_fingerprint": normalized.get("normalized_fingerprint"),
        "indicator_code": selection.get("indicator", {}).get("code"),
        "indicator_name": selection.get("indicator", {}).get("name"),
        "entities": selection.get("entities"),
        "periods": selection.get("periods"),
        "expected_observation_slots": normalized.get("expected_observation_slots"),
    }


def build_candidate_payload_v2(
    normalized: dict[str, Any],
    *,
    package_id: str,
    minimum_observed_count: int = DEFAULT_MINIMUM_OBSERVED_COUNT,
    minimum_coverage_share: str = DEFAULT_MINIMUM_COVERAGE_SHARE,
) -> dict[str, Any]:
    contract = calculation_contract_v2(
        minimum_observed_count=minimum_observed_count,
        minimum_coverage_share=minimum_coverage_share,
    )
    measures = compute_statistical_summary_v2(
        normalized,
        minimum_observed_count=minimum_observed_count,
        minimum_coverage_share=minimum_coverage_share,
    )
    payload = {
        "candidate_kind": "statistical_summary_v2_candidate_payload",
        "package_id": package_id,
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "calculation_contract": contract,
        "input_summary": _normalized_input_summary(normalized),
        "structured_payload": measures,
        "promotion_status": "candidate_only",
    }
    payload["candidate_payload_fingerprint"] = sha256_fingerprint(
        {k: v for k, v in payload.items() if k not in {"candidate_payload_fingerprint", "package_manifest_fingerprint"}}
    )
    payload["package_manifest_fingerprint"] = sha256_fingerprint(
        {
            "package_id": package_id,
            "method_id": METHOD_ID,
            "method_version": METHOD_VERSION,
            "candidate_payload_fingerprint": payload["candidate_payload_fingerprint"],
            "promotion_status": payload["promotion_status"],
        }
    )
    return payload


def build_campaign34_v2_comparison(normalized: dict[str, Any]) -> dict[str, Any]:
    payload = build_candidate_payload_v2(
        normalized,
        package_id="non-promoted-comparison-campaign34-statistical-summary-v2",
    )
    return {
        "comparison_id": "campaign34-input-v2-non-promoted-comparison",
        "promotion_status": "non_promoted_comparison_only",
        "historical_method_id": "wdi_denmark_population_statistical_summary_v1",
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "calculation_contract_fingerprint": payload["calculation_contract"]["calculation_contract_fingerprint"],
        "candidate_payload_fingerprint": payload["candidate_payload_fingerprint"],
        "package_manifest_fingerprint_if_promoted": payload["package_manifest_fingerprint"],
        "measures": payload["structured_payload"],
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
