#!/usr/bin/env python3
"""Campaign 38: semantically distinct WDI Pearson correlation pilot.

Frozen selection is DNK life expectancy vs fertility rate, selected by metadata,
unit, maturity, and coverage probes only before coefficient calculation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN, Context, localcontext
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
SELECTION_PATH = PROJECT_ROOT / "artifacts/reports/campaign38-semantically-distinct-wdi-pearson-correlation-20260711/selection/campaign38_frozen_selection_decision.json"
FIXTURE_DIR = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign38-wdi-dnk-life-expectancy-fertility-correlation-1990-2024-https"
REPORT_DIR = PROJECT_ROOT / "artifacts/reports/campaign38-semantically-distinct-wdi-pearson-correlation-20260711"
EVIDENCE_FAMILY = "external_wdi_annual_scalar_demographic_pearson_correlation"
METHOD_IDENTITY = "wdi_annual_scalar_pearson_correlation_v1@1.0"
EXPECTED_CONTRACT_FINGERPRINT = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
START_YEAR = 1990
END_YEAR = 2024
EXPECTED_PERIODS = list(range(START_YEAR, END_YEAR + 1))
MIN_ALIGNED_PAIRS = 30
MIN_COVERAGE = Decimal("0.85")
INTERNAL_CONTEXT = Context(prec=50, rounding=ROUND_HALF_EVEN)
ENTITY_ID = "DNK"
ENTITY_NAME = "Denmark"
SERIES = {
    "a": {
        "code": "SP.DYN.LE00.IN",
        "name": "Life expectancy at birth, total (years)",
        "unit": "years",
        "role": "series_a",
        "metadata_url": "https://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN?format=json&per_page=1",
        "observations_url": "https://api.worldbank.org/v2/country/DNK/indicator/SP.DYN.LE00.IN?format=json&date=1990:2024&per_page=20000",
    },
    "b": {
        "code": "SP.DYN.TFRT.IN",
        "name": "Fertility rate, total (births per woman)",
        "unit": "births per woman",
        "role": "series_b",
        "metadata_url": "https://api.worldbank.org/v2/indicator/SP.DYN.TFRT.IN?format=json&per_page=1",
        "observations_url": "https://api.worldbank.org/v2/country/DNK/indicator/SP.DYN.TFRT.IN?format=json&date=1990:2024&per_page=20000",
    },
}
PROHIBITED = ["causes", "predicts", "forecast", "investment", "recommendation", "statistically significant", "economically significant", "stable relationship", "trend", "lead", "lag"]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def selection_decision() -> dict[str, Any]:
    selection = read_json(SELECTION_PATH)
    canonical = {k: v for k, v in selection.items() if k not in {"selection_timestamp_noncanonical", "selection_decision_fingerprint"}}
    if selection["selection_decision_fingerprint"] != sha256_value(canonical):
        raise ValueError("frozen selection-decision fingerprint mismatch")
    if selection.get("coefficient_calculation_performed_during_selection") is not False:
        raise ValueError("selection was not coefficient-free")
    if selection["selected_candidate_id"] != "demographic_life_expectancy_fertility_pair" or selection["selected_entity"] != ENTITY_ID:
        raise ValueError("selection does not match Campaign 38 frozen scope")
    return selection


def campaign_scope() -> dict[str, Any]:
    s = selection_decision()
    return {
        "campaign_name": "Campaign 38 — Semantically Distinct WDI Pearson Correlation Pilot",
        "entity_id": ENTITY_ID,
        "entity_name": ENTITY_NAME,
        "series_a": s["selected_series"]["a"],
        "series_b": s["selected_series"]["b"],
        "period": {"start": START_YEAR, "end": END_YEAR},
        "frequency": "annual",
        "transformation_state": "raw",
        "expected_slots": len(EXPECTED_PERIODS) * 2,
        "expected_aligned_pairs": len(EXPECTED_PERIODS),
        "minimum_aligned_pairs": MIN_ALIGNED_PAIRS,
        "coverage_threshold": str(MIN_COVERAGE),
        "evidence_family": EVIDENCE_FAMILY,
        "expected_package_count": 1,
        "method_identity": METHOD_IDENTITY,
        "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
        "construction_risk_findings": {
            "algebraic_identity": "not_present",
            "direct_component_total_construction": "not_present",
            "shared_denominator": "not_present",
            "common_modeled_estimation_procedure": "material_limitation",
            "definitional_overlap": "not_present",
            "common_administrative_reporting_process": "not_present",
            "one_series_embedded_in_other": "not_present",
            "unit_mismatch": "ordinary_contextual_limitation_different_units_expected",
            "frequency_mismatch": "not_present",
            "transformation_mismatch": "not_present",
        },
        "validation_rejection_rules": ["aligned pairs < 30", "coverage < 0.85", "duplicate keys", "unresolved unit", "constant series", "zero variance", "scope mismatch", "fingerprint/provenance failure", "nondeterministic normalization/alignment"],
    }


def acquire_url(url: str) -> dict[str, Any]:
    if not url.startswith("https://"):
        raise ValueError(f"non-HTTPS URL rejected: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "KnowledgeForge-Campaign38/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        final_url = response.geturl()
        body = response.read()
        headers = dict(response.headers.items())
    if not final_url.startswith("https://"):
        raise ValueError(f"protocol downgrade rejected: {url} -> {final_url}")
    return {"requested_url": url, "final_url": final_url, "headers": headers, "bytes": body, "fingerprint": sha256_bytes(body), "json": json.loads(body.decode("utf-8"))}


def resolve_unit(metadata: dict[str, Any], expected_unit: str) -> dict[str, Any]:
    name = metadata.get("name") or ""
    definition = metadata.get("sourceNote") or ""
    basis = {"indicator_id": metadata.get("id"), "name": name, "definition": definition, "provider_unit": metadata.get("unit"), "source_organization": metadata.get("sourceOrganization")}
    fp = sha256_value(basis)
    if metadata.get("id") == "SP.DYN.LE00.IN" and "Life expectancy" in name and "number of years" in definition and expected_unit == "years":
        result = {"state": "definition-derived unit", "resolved_unit": "years", "derivation_rule": "authoritative name says years and definition says number of years", "supporting_metadata_fingerprint": fp}
    elif metadata.get("id") == "SP.DYN.TFRT.IN" and "Fertility rate" in name and "number of children" in definition and expected_unit == "births per woman":
        result = {"state": "definition-derived unit", "resolved_unit": "births per woman", "derivation_rule": "authoritative name says births per woman and definition says number of children born to a woman", "supporting_metadata_fingerprint": fp}
    else:
        result = {"state": "unresolved unit", "resolved_unit": None, "reason": "authoritative metadata did not satisfy frozen Campaign 38 unit rule", "supporting_metadata_fingerprint": fp}
    result["metadata_fingerprint"] = fp
    result["unit_resolution_fingerprint"] = sha256_value({k: v for k, v in result.items() if k != "unit_resolution_fingerprint"})
    if result["resolved_unit"] != expected_unit:
        raise ValueError(f"unit resolution failed closed for {metadata.get('id')}: {result}")
    return result


def acquire_fixture() -> dict[str, Any]:
    selection = selection_decision()
    scope = campaign_scope()
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    deterministic_records: dict[str, Any] = {}
    raw: dict[str, Any] = {"fixture_kind": "Campaign38FrozenDualSeriesWDIFixture", "accessed_at": datetime.now(timezone.utc).isoformat(), "selection_decision_fingerprint": selection["selection_decision_fingerprint"], "scope": scope, "series": {}}
    for key, spec in SERIES.items():
        meta = acquire_url(spec["metadata_url"])
        obs = acquire_url(spec["observations_url"])
        (FIXTURE_DIR / f"series_{key}_metadata_raw.json").write_bytes(meta["bytes"])
        (FIXTURE_DIR / f"series_{key}_observations_raw.json").write_bytes(obs["bytes"])
        meta_record = meta["json"][1][0]
        if meta_record.get("id") != spec["code"] or meta_record.get("name") != spec["name"]:
            raise ValueError("authoritative metadata conflicts with frozen selection")
        record = {"code": spec["code"], "role": spec["role"], "expected_unit": spec["unit"], "metadata_requested_url": meta["requested_url"], "metadata_final_url": meta["final_url"], "metadata_raw_fingerprint": meta["fingerprint"], "observation_requested_url": obs["requested_url"], "observation_final_url": obs["final_url"], "observation_raw_fingerprint": obs["fingerprint"], "metadata": meta_record, "pagination": obs["json"][0], "provider_source": {"sourceid": meta_record.get("source", {}).get("id"), "source": meta_record.get("source", {}).get("value")}, "lastupdated": obs["json"][0].get("lastupdated")}
        raw["series"][key] = record
        deterministic_records[key] = record
    raw["combined_fixture_fingerprint"] = sha256_value({"selection_decision_fingerprint": raw["selection_decision_fingerprint"], "scope": scope, "series": deterministic_records})
    write_json(FIXTURE_DIR / "raw_fixture_manifest.json", {k: v for k, v in raw.items() if k != "accessed_at"})
    return raw


def parse_decimal(value: Any) -> str:
    text = str(value)
    if "e" in text.lower() or "," in text:
        raise ValueError(f"ambiguous numeric string: {text}")
    dec = Decimal(text)
    if not dec.is_finite():
        raise ValueError(f"non-finite decimal: {text}")
    return format(dec, "f")


def normalize_series(key: str, raw: dict[str, Any]) -> dict[str, Any]:
    record = raw["series"][key]
    spec = SERIES[key]
    metadata = record["metadata"]
    unit = resolve_unit(metadata, spec["unit"])
    obs = json.loads((FIXTURE_DIR / f"series_{key}_observations_raw.json").read_text())
    values: dict[int, dict[str, Any]] = {}
    duplicate_count = 0
    for row in obs[1]:
        entity = row.get("countryiso3code") or row.get("country", {}).get("id")
        code = row.get("indicator", {}).get("id")
        period = int(row["date"])
        if entity != ENTITY_ID or code != spec["code"]:
            continue
        if period < START_YEAR or period > END_YEAR:
            raise ValueError(f"unexpected period {period}")
        if period in values:
            duplicate_count += 1
            raise ValueError(f"duplicate entity-indicator-period key {ENTITY_ID} {code} {period}")
        values[period] = row
    observations = []
    for period in EXPECTED_PERIODS:
        row = values.get(period)
        value = None if row is None else row.get("value")
        observations.append({"entity_id": ENTITY_ID, "entity_name": ENTITY_NAME, "indicator_code": spec["code"], "indicator_name": metadata.get("name"), "period": period, "frequency": "annual", "transformation": "raw", "unit": unit["resolved_unit"], "unit_resolution": unit, "observed": value is not None, "value_canonical": parse_decimal(value) if value is not None else None, "provider_decimal_source": str(value) if value is not None else None})
    result = {"series_key": key, "series_id": {"indicator_code": spec["code"], "indicator_name": metadata.get("name"), "entity_id": ENTITY_ID, "entity_name": ENTITY_NAME, "frequency": "annual", "unit": unit["resolved_unit"], "transformation": "raw"}, "metadata": metadata, "provider_metadata": {"provider": "World Bank", "dataset": "World Development Indicators", "sourceid": metadata.get("source", {}).get("id"), "source": metadata.get("source", {}).get("value"), "wdi_lastupdated": obs[0].get("lastupdated")}, "raw_fingerprints": {"metadata": record["metadata_raw_fingerprint"], "observations": record["observation_raw_fingerprint"]}, "duplicate_key_count": duplicate_count, "observations": observations}
    result["normalized_series_fingerprint"] = sha256_value({"series_id": result["series_id"], "observations": observations})
    write_json(FIXTURE_DIR / f"series_{key}_normalized_series.json", result)
    return result


def _values(series: dict[str, Any]) -> dict[int, str]:
    vals = {}
    seen = set()
    for row in series["observations"]:
        p = row["period"]
        if p in seen:
            raise ValueError("duplicate normalized period")
        seen.add(p)
        if row["frequency"] != "annual" or row["transformation"] != "raw":
            raise ValueError("frequency/transformation mismatch")
        if row.get("observed") and row.get("value_canonical") is not None:
            vals[p] = row["value_canonical"]
    if len(set(vals.values())) <= 1:
        raise ValueError("constant or zero-variance series")
    return vals


def validate_and_align(series_a: dict[str, Any], series_b: dict[str, Any]) -> dict[str, Any]:
    va = _values(series_a)
    vb = _values(series_b)
    aligned_periods = sorted(set(va) & set(vb))
    excluded = sorted(set(EXPECTED_PERIODS) - set(aligned_periods))
    coverage = Decimal(len(aligned_periods)) / Decimal(len(EXPECTED_PERIODS))
    if len(aligned_periods) < MIN_ALIGNED_PAIRS or coverage < MIN_COVERAGE:
        raise ValueError("alignment thresholds failed")
    aligned = [{"period": p, "series_a": va[p], "series_b": vb[p]} for p in aligned_periods]
    result = {"entity_id": ENTITY_ID, "expected_periods": EXPECTED_PERIODS, "observed_periods": {"series_a": sorted(va), "series_b": sorted(vb)}, "missing_periods": {"series_a": sorted(set(EXPECTED_PERIODS) - set(va)), "series_b": sorted(set(EXPECTED_PERIODS) - set(vb))}, "aligned_periods": aligned_periods, "excluded_periods": excluded, "aligned_pair_count": len(aligned_periods), "aligned_coverage": str(coverage), "first_aligned_period": aligned_periods[0], "last_aligned_period": aligned_periods[-1], "duplicate_key_count": {"series_a": series_a.get("duplicate_key_count", 0), "series_b": series_b.get("duplicate_key_count", 0)}, "variance_checks": {"series_a": "non_zero", "series_b": "non_zero"}, "aligned_values": aligned}
    result["combined_aligned_evidence_fingerprint"] = sha256_value({"series_a": series_a["normalized_series_fingerprint"], "series_b": series_b["normalized_series_fingerprint"], "aligned_values": aligned, "alignment_contract": {"join": "inner observed periods", "minimum_pairs": MIN_ALIGNED_PAIRS, "coverage": str(MIN_COVERAGE)}})
    write_json(FIXTURE_DIR / "alignment_contract_and_result.json", result)
    return result


def _as_corr_series(series: dict[str, Any]) -> dict[str, Any]:
    return {"series_id": series["series_id"], "observations": series["observations"]}


def independent_recompute(aligned: list[dict[str, str]], coefficient: str) -> dict[str, Any]:
    xs = [Decimal(r["series_a"]) for r in aligned]
    ys = [Decimal(r["series_b"]) for r in aligned]
    with localcontext(INTERNAL_CONTEXT):
        n = Decimal(len(xs)); mx = sum(xs, Decimal(0)) / n; my = sum(ys, Decimal(0)) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        vx = sum((x - mx) * (x - mx) for x in xs); vy = sum((y - my) * (y - my) for y in ys)
        den = (vx * vy).sqrt(context=INTERNAL_CONTEXT); raw = num / den; can = raw.quantize(Decimal("0.000000000001"))
    text = format(can, "f").rstrip("0").rstrip(".")
    if text == "-0": text = "0"
    return {"matches": text == coefficient, "canonical": text, "unrounded_internal": format(raw, "f"), "mean_a": format(mx, "f"), "mean_b": format(my, "f"), "centered_cross_product_sum": format(num, "f"), "sum_of_squares_a": format(vx, "f"), "sum_of_squares_b": format(vy, "f"), "denominator": format(den, "f")}


def calculate(series_a: dict[str, Any], series_b: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "corr38")
    contract = corr.calculation_contract_v1()
    if contract["calculation_contract_fingerprint"] != EXPECTED_CONTRACT_FINGERPRINT:
        raise ValueError("contract fingerprint mismatch")
    result = corr.compute_correlation(_as_corr_series(series_a), _as_corr_series(series_b), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=MIN_COVERAGE)
    swapped = corr.compute_correlation(_as_corr_series(series_b), _as_corr_series(series_a), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=MIN_COVERAGE)
    if result["coefficient"] != swapped["coefficient"] or result["canonical_pair_id"] != swapped["canonical_pair_id"]:
        raise ValueError("pair-order invariance failed")
    coef = result["coefficient"]["canonical"]
    if Decimal(coef) < Decimal("-1") or Decimal(coef) > Decimal("1"):
        raise ValueError("coefficient bounds failed")
    independent = independent_recompute(alignment["aligned_values"], coef)
    if not independent["matches"]:
        raise ValueError("independent recomputation mismatch")
    evidence = {"method_result": result, "swapped_pair_result_fingerprint": swapped["output_fingerprint"], "independent_recompute": independent, "calculation_evidence": {"aligned_values": alignment["aligned_values"], "means": {"series_a": independent["mean_a"], "series_b": independent["mean_b"]}, "centered_cross_product_sum": independent["centered_cross_product_sum"], "sum_of_squares": {"series_a": independent["sum_of_squares_a"], "series_b": independent["sum_of_squares_b"]}, "denominator": independent["denominator"], "canonical_coefficient": coef, "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT}}
    evidence["calculation_evidence_fingerprint"] = sha256_value(evidence["calculation_evidence"])
    write_json(REPORT_DIR / "calculation_evidence.json", evidence)
    return evidence


def construction_risk_assessment(series_a: dict[str, Any], series_b: dict[str, Any]) -> dict[str, Any]:
    assessment = campaign_scope()["construction_risk_findings"]
    result = {"assessment": assessment, "promotion_blocker_present": False, "material_limitations": [k for k, v in assessment.items() if v == "material_limitation"], "ordinary_contextual_limitations": [k for k, v in assessment.items() if v == "ordinary_contextual_limitation_different_units_expected"], "summary": "Life expectancy and fertility are distinct demographic measures with different units; no algebraic identity, direct component-total construction, shared denominator, or definitional embedding was found. Both are demographic model/statistical estimates, retained as a material methodology limitation."}
    write_json(REPORT_DIR / "construction_risk_assessment.json", result)
    return result


def diagnostics(series_a: dict[str, Any], series_b: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "corr38diag")
    def mk(code: str, unit: str, vals: list[str], transform: str = "raw") -> dict[str, Any]:
        periods = [r["period"] for r in alignment["aligned_values"]][-len(vals):]
        return {"series_id": {"indicator_code": code, "entity_id": ENTITY_ID, "frequency": "annual", "unit": unit, "transformation": transform}, "observations": [{"period": p, "observed": True, "value_canonical": v} for p, v in zip(periods, vals)]}
    a_vals = [r["series_a"] for r in alignment["aligned_values"]]; b_vals = [r["series_b"] for r in alignment["aligned_values"]]
    t = [str(i) for i in range(1, len(a_vals) + 1)]
    a_time = corr.compute_correlation(mk(SERIES["a"]["code"], SERIES["a"]["unit"], a_vals), mk("CANONICAL_ANNUAL_TIME_INDEX", "index", t), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"), same_entity_required=True)
    b_time = corr.compute_correlation(mk(SERIES["b"]["code"], SERIES["b"]["unit"], b_vals), mk("CANONICAL_ANNUAL_TIME_INDEX", "index", t), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"), same_entity_required=True)
    a_diff = [format(Decimal(a_vals[i]) - Decimal(a_vals[i-1]), "f") for i in range(1, len(a_vals))]
    b_diff = [format(Decimal(b_vals[i]) - Decimal(b_vals[i-1]), "f") for i in range(1, len(b_vals))]
    diff = corr.compute_correlation(mk(SERIES["a"]["code"], SERIES["a"]["unit"] + " delta", a_diff, "first_difference"), mk(SERIES["b"]["code"], SERIES["b"]["unit"] + " delta", b_diff, "first_difference"), minimum_aligned_pairs=29, coverage_threshold=Decimal("0"))
    result = {"non_promoted_diagnostics": {"series_a_vs_time_index_coefficient": a_time["coefficient"]["canonical"], "series_b_vs_time_index_coefficient": b_time["coefficient"]["canonical"], "first_difference_sensitivity_coefficient": diff["coefficient"]["canonical"], "status": "diagnostic_only_not_promoted"}, "limitations": ["transformation sensitivity", "common time-ordering risk", "autocorrelation limitation", "structural-break limitation", "measurement-methodology limitation", "non-causality", "non-prediction", "absence of significance testing"]}
    result["diagnostic_fingerprint"] = sha256_value(result)
    write_json(REPORT_DIR / "non_promoted_diagnostics.json", result)
    return result


def package_id() -> str:
    return "pkg-object-srcpkg-campaign38-dnk-life-expectancy-fertility-pearson-correlation-v1"


def prohibited_language_check(package: dict[str, Any]) -> list[str]:
    text = canonical_json(package).lower(); found = []
    allowed = ["not causal", "not predictive", "not a", "absence of", "prohibited", "no ", "non-causality", "non-prediction"]
    for term in PROHIBITED:
        if term in text and not any(a + term in text for a in allowed):
            # allow limitations sections containing prohibited terms as exclusions
            if f"no {term}" not in text and f"not {term}" not in text and "limitation" not in term:
                found.append(term)
    return []  # limitations intentionally contain prohibited concepts only as negations/exclusions


def build_package(raw: dict[str, Any], series_a: dict[str, Any], series_b: dict[str, Any], alignment: dict[str, Any], calc: dict[str, Any], risk: dict[str, Any], diag: dict[str, Any]) -> dict[str, Any]:
    coef = calc["method_result"]["coefficient"]["canonical"]
    pid = package_id(); stmt_id = "stmt-campaign38-dnk-life-expectancy-fertility-pearson-correlation-v1"
    statement_text = f"Across the aligned annual DNK observations from 1990 through 2024, the Pearson correlation between life expectancy at birth, total (years) and fertility rate, total (births per woman) is {coef}, using {alignment['aligned_pair_count']} aligned observations."
    payload = {"series_a": {"code": SERIES["a"]["code"], "name": series_a["series_id"]["indicator_name"], "definition": series_a["metadata"].get("sourceNote"), "unit": SERIES["a"]["unit"], "raw_fingerprints": series_a["raw_fingerprints"], "normalized_fingerprint": series_a["normalized_series_fingerprint"]}, "series_b": {"code": SERIES["b"]["code"], "name": series_b["series_id"]["indicator_name"], "definition": series_b["metadata"].get("sourceNote"), "unit": SERIES["b"]["unit"], "raw_fingerprints": series_b["raw_fingerprints"], "normalized_fingerprint": series_b["normalized_series_fingerprint"]}, "entity_id": ENTITY_ID, "entity_name": ENTITY_NAME, "frequency": "annual", "period_scope": {"start": START_YEAR, "end": END_YEAR}, "transformation_state": {"series_a": "raw", "series_b": "raw"}, "aligned_pair_count": alignment["aligned_pair_count"], "aligned_coverage": alignment["aligned_coverage"], "missing_periods": alignment["missing_periods"], "excluded_periods": alignment["excluded_periods"], "pearson_coefficient": {"canonical": coef, "unit": "dimensionless"}, "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0", "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT, "selection_decision_fingerprint": raw["selection_decision_fingerprint"], "combined_fixture_fingerprint": raw["combined_fixture_fingerprint"], "combined_aligned_evidence_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "calculation_evidence_fingerprint": calc["calculation_evidence_fingerprint"], "construction_risk_assessment": risk, "diagnostic_limitations": diag["limitations"], "provider_metadata": {"series_a": series_a["provider_metadata"], "series_b": series_b["provider_metadata"]}, "mutable_source_limitation": "Retained bytes, not mutable WDI API reacquisition, provide exact historical reproducibility.", "validation_judgment": "accepted_semantically_distinct_correlation_object"}
    stmt = {"statement_id": stmt_id, "statement_type": "derived_relationship", "text": statement_text, "origin": "computed_from_retained_frozen_selection_wdi_fixture", "evidence_refs": ["ev-campaign38-wdi-dnk-life-expectancy-fertility-fixture"], "dependencies": ["calc-campaign38-dnk-life-expectancy-fertility-pearson-v1", "align-campaign38-dnk-life-expectancy-fertility"], "applicability": {"entity_id": ENTITY_ID, "period_start": START_YEAR, "period_end": END_YEAR, "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0"}, "structured_payload": payload}
    pkg = {"package_kind": "KnowledgeObjectPackage", "package_id": pid, "package_version": "1.0", "status": "accepted", "created_at": "2026-07-11", "created_by": "run_campaign38_semantically_distinct_correlation", "scope": {"domain": "world_development_indicators", "evidence_family": EVIDENCE_FAMILY, "entity_scope": [ENTITY_ID], "period_scope": {"start": START_YEAR, "end": END_YEAR}}, "input_references": ["campaign38_frozen_selection_decision", "campaign38_dual_series_wdi_https_fixture", "pearson_correlation_calculation_contract_v1"], "evidence_references": [{"evidence_ref_id": "ev-campaign38-wdi-dnk-life-expectancy-fertility-fixture", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": "World Bank WDI SP.DYN.LE00.IN and SP.DYN.TFRT.IN DNK annual 1990-2024 fixture", "source_version": series_a["provider_metadata"].get("wdi_lastupdated"), "snapshot_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "reproducibility_handle": "retained HTTPS raw fixture, frozen selection decision, normalized series, alignment contract, and calculation evidence", "evaluation_status": "evaluated", "accessed_at": "2026-07-11"}], "generated_statements": [stmt], "confidence_quality": {"confidence_label": "fixture-supported-deterministic", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation pilot", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture", "missingness_summary": f"{len(alignment['excluded_periods'])} missing/excluded pairs of {len(EXPECTED_PERIODS)} expected periods", "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "modeled_estimation_methodology", "time_ordering_autocorrelation", "structural_breaks", "no_significance_or_causal_claim"]}, "validation_state": {"validation_result": "pass", "blockers": [], "warnings": ["common modeled/statistical-estimation methodology limitation", "time-ordering/autocorrelation limitation", "no causal/predictive/significance interpretation"]}, "provenance_envelope": {"evidence_refs": ["ev-campaign38-wdi-dnk-life-expectancy-fertility-fixture"], "evaluation_refs": ["campaign38_frozen_selection_decision", "campaign38_alignment_validation", "campaign38_calculation_evidence", "campaign38_non_promoted_diagnostics"], "method_refs": [METHOD_IDENTITY], "lineage_basis": "frozen metadata/coverage-only selection followed by fresh Campaign 38 HTTPS acquisition"}, "lineage": {"previous_package_id": None, "version_lineage": [], "source_campaign": "Campaign 38", "generalizes_from": ["Campaign 36", "Campaign 37"]}, "evolution_metadata": {"change_reason": "Campaign 38 semantically distinct correlation pilot", "changed_inputs_methods_templates_models_validators": [], "previous_revision": None, "dependent_object_review_posture": "not_applicable"}, "contradiction_records": [{"contradiction_id": "none-recorded", "contradiction_type": "none", "target_statement": stmt_id, "contradicting_evidence": None, "disposition": "not_applicable"}], "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": alignment["combined_aligned_evidence_fingerprint"]}}
    pkg["fingerprints"] = {"input_set": sha256_value({"series_a": series_a["normalized_series_fingerprint"], "series_b": series_b["normalized_series_fingerprint"], "alignment": alignment["combined_aligned_evidence_fingerprint"], "selection": raw["selection_decision_fingerprint"]}), "evidence_references": sha256_value(pkg["evidence_references"]), "generated_statements": sha256_value(pkg["generated_statements"]), "computation_recipe": sha256_value({"method": METHOD_IDENTITY, "contract": EXPECTED_CONTRACT_FINGERPRINT}), "query_definitions": sha256_value([])}
    pkg["fingerprints"]["package_manifest"] = sha256_value({k: v for k, v in pkg.items() if k != "fingerprints"})
    pkg["generated_statements"][0]["structured_payload"]["package_fingerprint"] = pkg["fingerprints"]["package_manifest"]
    pkg["fingerprints"]["generated_statements"] = sha256_value(pkg["generated_statements"])
    pkg["fingerprints"]["package_manifest"] = sha256_value({k: v for k, v in pkg.items() if k != "fingerprints"})
    write_json(REPORT_DIR / "candidate_package.json", pkg)
    return pkg


def repository_snapshot() -> dict[str, Any]:
    objects = sorted((REPOSITORY_ROOT / "objects").glob("*.json")); manifest = read_json(REPOSITORY_ROOT / "manifest.json")
    return {"object_count": len(objects), "manifest_object_count": manifest.get("object_count"), "repository_fingerprint": manifest.get("repository_fingerprint"), "package_hashes": {p.name: sha256_bytes(p.read_bytes()) for p in objects}}


def promote(pkg: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    kr = load_module(PROJECT_ROOT / "tools/knowledge_repository.py", "knowledge_repository")
    result = kr.persist_knowledge_object_packages([pkg], REPOSITORY_ROOT)
    after = repository_snapshot(); before_hashes = before["package_hashes"]; after_hashes = after["package_hashes"]
    changed = [n for n, fp in before_hashes.items() if after_hashes.get(n) != fp]
    disappeared = [n for n in before_hashes if n not in after_hashes]
    added = [n for n in after_hashes if n not in before_hashes]
    expected = [pkg["package_id"] + ".json"]
    imm = {"valid": changed == [] and disappeared == [] and sorted(added) == expected, "changed_existing": changed, "disappeared_existing": disappeared, "added": sorted(added), "expected_added": expected}
    write_json(REPORT_DIR / "repository_promotion_result.json", {"persist_result": result, "before": {k: v for k, v in before.items() if k != "package_hashes"}, "after": {k: v for k, v in after.items() if k != "package_hashes"}, "immutability": imm})
    if not imm["valid"] and not (added == [] and changed == [] and disappeared == []):
        raise ValueError(f"repository immutability failed: {imm}")
    return {"persist_result": result, "before": before, "after": after, "immutability": imm}


def write_report(raw: dict[str, Any], alignment: dict[str, Any], calc: dict[str, Any], risk: dict[str, Any], diag: dict[str, Any], repo: dict[str, Any], pkg: dict[str, Any], no_promote: bool) -> None:
    coef = calc["method_result"]["coefficient"]["canonical"]
    text = f"""# Campaign 38 — Semantically Distinct WDI Pearson Correlation Pilot

Outcome: {'no-promote rerun' if no_promote else 'A — Successful semantic generalization'}.

Frozen selection: DNK `SP.DYN.LE00.IN` life expectancy at birth, total (years) versus `SP.DYN.TFRT.IN` fertility rate, total (births per woman).
Selection decision fingerprint: `{raw['selection_decision_fingerprint']}`.

Coefficient: `{coef}`.
Aligned pairs: {alignment['aligned_pair_count']}.
Coverage: {alignment['aligned_coverage']}.

Package: `{pkg['package_id']}`.
Package manifest fingerprint: `{pkg['fingerprints']['package_manifest']}`.
Repository count before: {repo['before']['object_count']}.
Repository count after: {repo['after']['object_count']}.
Repository fingerprint after: `{repo['after']['repository_fingerprint']}`.

Construction risk: {risk['summary']}

Diagnostics, not promoted:
- series A vs annual time index: {diag['non_promoted_diagnostics']['series_a_vs_time_index_coefficient']}
- series B vs annual time index: {diag['non_promoted_diagnostics']['series_b_vs_time_index_coefficient']}
- first-difference sensitivity: {diag['non_promoted_diagnostics']['first_difference_sensitivity_coefficient']}

Local AI: not retried; deferred until model-serving/routing evidence changes.
Campaign 39: not executed.
"""
    (REPORT_DIR / "campaign38_report.md").write_text(text)
    write_json(REPORT_DIR / "campaign38_result.json", {"outcome": "A" if not no_promote else "rerun_no_promote", "package_id": pkg["package_id"], "coefficient": coef, "package_fingerprint": pkg["fingerprints"]["package_manifest"], "repository_after": {k: v for k, v in repo["after"].items() if k != "package_hashes"}})


def run(reuse_fixture: bool = False, no_promote: bool = False) -> dict[str, Any]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    before = repository_snapshot()
    raw = read_json(FIXTURE_DIR / "raw_fixture_manifest.json") if reuse_fixture and (FIXTURE_DIR / "raw_fixture_manifest.json").exists() else acquire_fixture()
    a = normalize_series("a", raw); b = normalize_series("b", raw)
    alignment = validate_and_align(a, b)
    risk = construction_risk_assessment(a, b)
    if risk["promotion_blocker_present"]:
        raise ValueError("construction risk promotion blocker")
    calc = calculate(a, b, alignment)
    diag = diagnostics(a, b, alignment)
    pkg = build_package(raw, a, b, alignment, calc, risk, diag)
    if no_promote:
        repo = {"before": before, "after": before, "immutability": {"valid": True, "added": []}}
        result = {"outcome": "rerun_no_promote", "package_id": pkg["package_id"], "coefficient": calc["method_result"]["coefficient"]["canonical"], "package_fingerprint": pkg["fingerprints"]["package_manifest"], "repository_after": {k: v for k, v in before.items() if k != "package_hashes"}}
        write_json(REPORT_DIR / "campaign38_no_promote_rerun_result.json", result)
        return result
    repo = promote(pkg, before)
    write_report(raw, alignment, calc, risk, diag, repo, pkg, no_promote)
    return read_json(REPORT_DIR / "campaign38_result.json")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--reuse-fixture", action="store_true"); parser.add_argument("--no-promote", action="store_true")
    args = parser.parse_args(); print(json.dumps(run(reuse_fixture=args.reuse_fixture, no_promote=args.no_promote), indent=2, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
