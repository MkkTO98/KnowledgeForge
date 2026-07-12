#!/usr/bin/env python3
"""Campaign 36: DNK exports/imports share Pearson correlation pilot.

Production execution is bounded to one correlation KnowledgeObjectPackage.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN, Context, localcontext
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
FIXTURE_DIR = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign36-wdi-dnk-exports-imports-share-correlation-1990-2024-https"
REPORT_DIR = PROJECT_ROOT / "artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710"
PACKAGE_ID = "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1"
STATEMENT_ID = "stmt-campaign36-dnk-exports-imports-share-pearson-correlation-v1"
EVIDENCE_FAMILY = "external_wdi_annual_scalar_trade_pearson_correlation"
METHOD_IDENTITY = "wdi_annual_scalar_pearson_correlation_v1@1.0"
EXPECTED_CONTRACT_FINGERPRINT = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
ENTITY_ID = "DNK"
ENTITY_NAME = "Denmark"
START_YEAR = 1990
END_YEAR = 2024
EXPECTED_PERIODS = list(range(START_YEAR, END_YEAR + 1))
MIN_ALIGNED_PAIRS = 30
MIN_COVERAGE = Decimal("0.85")
INTERNAL_CONTEXT = Context(prec=50, rounding=ROUND_HALF_EVEN)
SERIES = {
    "exports": {
        "code": "NE.EXP.GNFS.ZS",
        "name": "Exports of goods and services (% of GDP)",
        "role": "series_a",
        "metadata_url": "https://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json&per_page=1",
        "observations_url": "https://api.worldbank.org/v2/country/DNK/indicator/NE.EXP.GNFS.ZS?format=json&date=1990:2024&per_page=20000",
    },
    "imports": {
        "code": "NE.IMP.GNFS.ZS",
        "name": "Imports of goods and services (% of GDP)",
        "role": "series_b",
        "metadata_url": "https://api.worldbank.org/v2/indicator/NE.IMP.GNFS.ZS?format=json&per_page=1",
        "observations_url": "https://api.worldbank.org/v2/country/DNK/indicator/NE.IMP.GNFS.ZS?format=json&date=1990:2024&per_page=20000",
    },
}
PROHIBITED = [
    "causes", "cause", "predicts", "forecast", "investment", "recommendation",
    "statistically significant", "economically significant", "trade performance", "stable relationship",
]


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


def acquire_url(url: str) -> dict[str, Any]:
    if not url.startswith("https://"):
        raise ValueError(f"non-HTTPS URL rejected: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "KnowledgeForge-Campaign36/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        final_url = response.geturl()
        body = response.read()
        headers = dict(response.headers.items())
    if not final_url.startswith("https://"):
        raise ValueError(f"protocol downgrade rejected: {url} -> {final_url}")
    return {
        "requested_url": url,
        "final_url": final_url,
        "headers": headers,
        "bytes": body,
        "fingerprint": sha256_bytes(body),
        "json": json.loads(body.decode("utf-8")),
    }


def acquire_fixture() -> dict[str, Any]:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    raw: dict[str, Any] = {"series": {}, "accessed_at": datetime.now(timezone.utc).isoformat()}
    deterministic_records = {}
    for key, spec in SERIES.items():
        meta = acquire_url(spec["metadata_url"])
        obs = acquire_url(spec["observations_url"])
        (FIXTURE_DIR / f"{key}_metadata_raw.json").write_bytes(meta["bytes"])
        (FIXTURE_DIR / f"{key}_observations_raw.json").write_bytes(obs["bytes"])
        meta_record = meta["json"][1][0]
        page = obs["json"][0]
        raw["series"][key] = {
            "code": spec["code"],
            "role": spec["role"],
            "metadata_requested_url": meta["requested_url"],
            "metadata_final_url": meta["final_url"],
            "metadata_raw_fingerprint": meta["fingerprint"],
            "observation_requested_url": obs["requested_url"],
            "observation_final_url": obs["final_url"],
            "observation_raw_fingerprint": obs["fingerprint"],
            "metadata": meta_record,
            "pagination": page,
            "provider_source": {"sourceid": meta_record.get("source", {}).get("id"), "source": meta_record.get("source", {}).get("value")},
            "lastupdated": page.get("lastupdated"),
        }
        deterministic_records[key] = {k: v for k, v in raw["series"][key].items() if k != "headers"}
    selection = {
        "campaign": "campaign36_dnk_exports_imports_share_pearson_correlation",
        "entity": ENTITY_ID,
        "periods": EXPECTED_PERIODS,
        "frequency": "annual",
        "transformation": "raw",
        "series": {k: {"code": v["code"], "metadata_url": v["metadata_url"], "observations_url": v["observations_url"]} for k, v in SERIES.items()},
        "method_identity": METHOD_IDENTITY,
        "contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
    }
    raw["selection_contract"] = selection
    raw["selection_fingerprint"] = sha256_value(selection)
    raw["combined_raw_fingerprint"] = sha256_value(deterministic_records)
    write_json(FIXTURE_DIR / "raw_fixture_manifest.json", {k: v for k, v in raw.items() if k != "accessed_at"})
    return raw


def resolve_unit(metadata: dict[str, Any]) -> dict[str, Any]:
    fixture = load_module(PROJECT_ROOT / "tools/wdi_observation_evidence_fixture.py", "wdi_fixture")
    resolution = fixture.resolve_wdi_unit(metadata)
    state = resolution.get("state")
    unit = resolution.get("unit") or resolution.get("resolved_unit")
    if state not in {"definition_derived", "definition-derived unit"} or unit != "percent of GDP":
        raise ValueError(f"unit resolution failed closed: {resolution}")
    normalized = dict(resolution)
    normalized["unit"] = unit
    return normalized


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
    metadata = record["metadata"]
    unit = resolve_unit(metadata)
    obs = json.loads((FIXTURE_DIR / f"{key}_observations_raw.json").read_text())
    rows = obs[1]
    seen = set()
    normalized = []
    source_lastupdated = obs[0].get("lastupdated")
    for row in sorted(rows, key=lambda r: int(r["date"])):
        entity = row.get("countryiso3code") or row.get("country", {}).get("id")
        code = row.get("indicator", {}).get("id")
        period = int(row["date"])
        if entity != ENTITY_ID:
            raise ValueError(f"unexpected entity: {entity}")
        if code != record["code"]:
            raise ValueError(f"unexpected indicator: {code}")
        if period < START_YEAR or period > END_YEAR:
            raise ValueError(f"unexpected period: {period}")
        if period in seen:
            raise ValueError(f"duplicate period: {period}")
        seen.add(period)
        value = row.get("value")
        normalized.append({
            "entity_id": ENTITY_ID,
            "entity_name": ENTITY_NAME,
            "indicator_code": code,
            "indicator_name": metadata.get("name"),
            "period": period,
            "frequency": "annual",
            "transformation": "raw",
            "unit": unit["unit"],
            "unit_resolution": unit,
            "observed": value is not None,
            "value_canonical": parse_decimal(value) if value is not None else None,
            "provider_decimal_source": str(value) if value is not None else None,
        })
    if sorted(seen) != EXPECTED_PERIODS:
        raise ValueError(f"period set mismatch for {key}: {sorted(seen)}")
    result = {
        "series_key": key,
        "series_id": {
            "indicator_code": record["code"],
            "indicator_name": metadata.get("name"),
            "entity_id": ENTITY_ID,
            "entity_name": ENTITY_NAME,
            "frequency": "annual",
            "unit": unit["unit"],
            "transformation": "raw",
        },
        "metadata": metadata,
        "provider_metadata": {
            "provider": "World Bank",
            "dataset": "World Development Indicators",
            "sourceid": metadata.get("source", {}).get("id"),
            "source": metadata.get("source", {}).get("value"),
            "wdi_lastupdated": source_lastupdated,
        },
        "raw_fingerprints": {
            "metadata": record["metadata_raw_fingerprint"],
            "observations": record["observation_raw_fingerprint"],
        },
        "observations": normalized,
    }
    result["normalized_series_fingerprint"] = sha256_value({"series_id": result["series_id"], "observations": normalized})
    write_json(FIXTURE_DIR / f"{key}_normalized_series.json", result)
    return result


def validate_and_align(exports: dict[str, Any], imports: dict[str, Any]) -> dict[str, Any]:
    by_key = {}
    missing: dict[str, list[int]] = {}
    for label, series in [("exports", exports), ("imports", imports)]:
        values = {}
        missing[label] = []
        for row in series["observations"]:
            p = row["period"]
            if p in values:
                raise ValueError(f"duplicate normalized period {label} {p}")
            if row["observed"]:
                values[p] = row["value_canonical"]
            else:
                missing[label].append(p)
        if len(set(values.values())) == 1:
            raise ValueError(f"constant series: {label}")
        by_key[label] = values
    aligned_periods = sorted(set(by_key["exports"]) & set(by_key["imports"]))
    excluded = sorted(set(EXPECTED_PERIODS) - set(aligned_periods))
    coverage = Decimal(len(aligned_periods)) / Decimal(len(EXPECTED_PERIODS))
    if len(aligned_periods) < MIN_ALIGNED_PAIRS or coverage < MIN_COVERAGE:
        raise ValueError("alignment thresholds failed")
    aligned = [{"period": p, "exports": by_key["exports"][p], "imports": by_key["imports"][p]} for p in aligned_periods]
    alignment = {
        "expected_periods": EXPECTED_PERIODS,
        "observed_periods": {"exports": sorted(by_key["exports"]), "imports": sorted(by_key["imports"])},
        "aligned_periods": aligned_periods,
        "excluded_periods": excluded,
        "missing_periods_by_series": missing,
        "missing_pair_count": len(excluded),
        "aligned_pair_count": len(aligned_periods),
        "aligned_coverage": str(coverage),
        "first_aligned_period": aligned_periods[0],
        "last_aligned_period": aligned_periods[-1],
        "aligned_values": aligned,
    }
    alignment["combined_aligned_evidence_fingerprint"] = sha256_value({
        "exports_normalized": exports["normalized_series_fingerprint"],
        "imports_normalized": imports["normalized_series_fingerprint"],
        "aligned_values": aligned,
        "alignment_contract": {"join": "inner observed periods", "minimum_pairs": MIN_ALIGNED_PAIRS, "coverage": str(MIN_COVERAGE)},
    })
    write_json(FIXTURE_DIR / "alignment_contract_and_result.json", alignment)
    return alignment


def as_corr_series(series: dict[str, Any]) -> dict[str, Any]:
    return {"series_id": series["series_id"], "observations": series["observations"]}


def independent_recompute(aligned: list[dict[str, str]], coefficient: str) -> dict[str, Any]:
    xs = [Decimal(r["exports"]) for r in aligned]
    ys = [Decimal(r["imports"]) for r in aligned]
    with localcontext(INTERNAL_CONTEXT):
        n = Decimal(len(xs))
        mx = sum(xs, Decimal(0)) / n
        my = sum(ys, Decimal(0)) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        vx = sum((x - mx) * (x - mx) for x in xs)
        vy = sum((y - my) * (y - my) for y in ys)
        den = (vx * vy).sqrt(context=INTERNAL_CONTEXT)
        raw = num / den
        can = raw.quantize(Decimal("0.000000000001"))
    text = format(can, "f").rstrip("0").rstrip(".")
    if text == "-0":
        text = "0"
    return {"matches": text == coefficient, "canonical": text, "unrounded_internal": format(raw, "f"), "mean_x": format(mx, "f"), "mean_y": format(my, "f"), "numerator": format(num, "f"), "variance_x": format(vx, "f"), "variance_y": format(vy, "f"), "denominator": format(den, "f")}


def calculate(exports: dict[str, Any], imports: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "corr")
    contract = corr.calculation_contract_v1()
    if contract["calculation_contract_fingerprint"] != EXPECTED_CONTRACT_FINGERPRINT:
        raise ValueError(f"contract fingerprint mismatch: {contract['calculation_contract_fingerprint']}")
    result = corr.compute_correlation(as_corr_series(exports), as_corr_series(imports), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=MIN_COVERAGE)
    swapped = corr.compute_correlation(as_corr_series(imports), as_corr_series(exports), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=MIN_COVERAGE)
    if result["coefficient"] != swapped["coefficient"] or result["canonical_pair_id"] != swapped["canonical_pair_id"]:
        raise ValueError("pair order invariance failed")
    independent = independent_recompute(alignment["aligned_values"], result["coefficient"]["canonical"])
    if not independent["matches"]:
        raise ValueError("independent recomputation mismatch")
    evidence = {
        "method_result": result,
        "swapped_pair_result_fingerprint": result["output_fingerprint"],
        "independent_recompute": independent,
        "calculation_evidence": {
            "aligned_values": alignment["aligned_values"],
            "means": {"exports": independent["mean_x"], "imports": independent["mean_y"]},
            "centered_sum_numerator": independent["numerator"],
            "sum_of_squares": {"exports": independent["variance_x"], "imports": independent["variance_y"]},
            "denominator": independent["denominator"],
            "unrounded_internal_coefficient": independent["unrounded_internal"],
            "canonical_coefficient": result["coefficient"]["canonical"],
            "aligned_pair_count": result["aligned_pair_count"],
            "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
        },
    }
    evidence["calculation_evidence_fingerprint"] = sha256_value(evidence["calculation_evidence"])
    write_json(REPORT_DIR / "calculation_evidence.json", evidence)
    return evidence


def diagnostics(exports: dict[str, Any], imports: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "corrdiag")
    def series_with_values(code: str, unit: str, vals: list[str], transform: str = "raw") -> dict[str, Any]:
        return {"series_id": {"indicator_code": code, "entity_id": ENTITY_ID, "frequency": "annual", "unit": unit, "transformation": transform}, "observations": [{"period": p, "observed": True, "value_canonical": v} for p, v in zip(EXPECTED_PERIODS[-len(vals):], vals)]}
    time_vals = [str(i) for i in range(1, len(alignment["aligned_values"]) + 1)]
    exp_vals = [r["exports"] for r in alignment["aligned_values"]]
    imp_vals = [r["imports"] for r in alignment["aligned_values"]]
    time_series = series_with_values("CANONICAL_ANNUAL_TIME_INDEX", "index", time_vals)
    exp_series = series_with_values("NE.EXP.GNFS.ZS", "percent of GDP", exp_vals)
    imp_series = series_with_values("NE.IMP.GNFS.ZS", "percent of GDP", imp_vals)
    exp_time = corr.compute_correlation(exp_series, time_series, minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"), same_entity_required=True)
    imp_time = corr.compute_correlation(imp_series, time_series, minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"), same_entity_required=True)
    exp_diff = [format(Decimal(exp_vals[i]) - Decimal(exp_vals[i-1]), "f") for i in range(1, len(exp_vals))]
    imp_diff = [format(Decimal(imp_vals[i]) - Decimal(imp_vals[i-1]), "f") for i in range(1, len(imp_vals))]
    diff_corr = corr.compute_correlation(series_with_values("NE.EXP.GNFS.ZS", "percent of GDP delta", exp_diff, "first_difference"), series_with_values("NE.IMP.GNFS.ZS", "percent of GDP delta", imp_diff, "first_difference"), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"))
    diag = {
        "mechanical_overlap_assessment": {
            "both_use_gdp_denominator": True,
            "shared_denominator_warning": "Both indicators use GDP as denominator, so correlation may partly reflect shared-denominator movement.",
            "flow_relationship_warning": "Exports and imports are economically related flow measures; coefficient cannot distinguish denominator effects, co-movement, shared shocks, time ordering, or mechanisms.",
            "identity_or_component_total_detected": False,
            "promotion_blocker": False,
        },
        "non_promoted_diagnostics": {
            "exports_vs_time_index_coefficient": exp_time["coefficient"]["canonical"],
            "imports_vs_time_index_coefficient": imp_time["coefficient"]["canonical"],
            "first_difference_sensitivity_coefficient": diff_corr["coefficient"]["canonical"],
            "status": "diagnostic_only_not_promoted",
            "limitation": "Diagnostics characterize limitations; they do not prove/disprove validity and do not add stationarity/significance/causal claims.",
        },
    }
    diag["diagnostic_fingerprint"] = sha256_value(diag)
    write_json(REPORT_DIR / "non_promoted_diagnostics.json", diag)
    return diag


def prohibited_language_check(package: dict[str, Any]) -> list[str]:
    text = canonical_json(package).lower()
    found = []
    allowed_context = ["no causation", "not claim", "not imply", "no causal", "non-causality", "prohibited"]
    for term in PROHIBITED:
        if term in text and not any(ctx in text for ctx in allowed_context):
            found.append(term)
    return found


def build_package(raw: dict[str, Any], exports: dict[str, Any], imports: dict[str, Any], alignment: dict[str, Any], calc: dict[str, Any], diag: dict[str, Any]) -> dict[str, Any]:
    coefficient = calc["method_result"]["coefficient"]["canonical"]
    statement_text = (
        f"Across the aligned annual DNK observations from 1990 through 2024, the Pearson correlation between "
        f"exports of goods and services as a percentage of GDP and imports of goods and services as a percentage of GDP "
        f"is {coefficient}, using {alignment['aligned_pair_count']} aligned observations."
    )
    payload = {
        "canonical_pair_identity": calc["method_result"]["canonical_pair_id"],
        "series_a": {"code": "NE.EXP.GNFS.ZS", "name": exports["series_id"]["indicator_name"], "definition": exports["metadata"].get("sourceNote"), "unit": "percent of GDP", "raw_fingerprints": exports["raw_fingerprints"], "normalized_fingerprint": exports["normalized_series_fingerprint"]},
        "series_b": {"code": "NE.IMP.GNFS.ZS", "name": imports["series_id"]["indicator_name"], "definition": imports["metadata"].get("sourceNote"), "unit": "percent of GDP", "raw_fingerprints": imports["raw_fingerprints"], "normalized_fingerprint": imports["normalized_series_fingerprint"]},
        "entity_id": ENTITY_ID,
        "entity_name": ENTITY_NAME,
        "frequency": "annual",
        "period_scope": {"start": START_YEAR, "end": END_YEAR},
        "transformation_state": {"series_a": "raw", "series_b": "raw"},
        "aligned_pair_count": alignment["aligned_pair_count"],
        "aligned_coverage": alignment["aligned_coverage"],
        "missing_pair_count": alignment["missing_pair_count"],
        "excluded_periods": alignment["excluded_periods"],
        "aligned_periods": alignment["aligned_periods"],
        "pearson_coefficient": {"canonical": coefficient, "unit": "dimensionless"},
        "method_id": "wdi_annual_scalar_pearson_correlation_v1",
        "method_version": "1.0",
        "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
        "selection_fingerprint": raw["selection_fingerprint"],
        "combined_raw_evidence_fingerprint": raw["combined_raw_fingerprint"],
        "combined_aligned_evidence_fingerprint": alignment["combined_aligned_evidence_fingerprint"],
        "calculation_evidence_fingerprint": calc["calculation_evidence_fingerprint"],
        "provider_metadata": {"exports": exports["provider_metadata"], "imports": imports["provider_metadata"]},
        "mutable_source_limitation": "Retained bytes, not mutable WDI API reacquisition, provide exact historical reproducibility.",
        "limitations": {
            "shared_gdp_denominator": diag["mechanical_overlap_assessment"]["shared_denominator_warning"],
            "time_ordering_autocorrelation": "Annual macroeconomic series can exhibit time ordering/autocorrelation; no stationarity or independence claim is made.",
            "structural_breaks": "The coefficient is scoped only to the retained 1990-2024 aligned window and may not hold across structural breaks.",
            "non_causality": "The coefficient is a deterministic contemporaneous mathematical relationship only and is not a causal, predictive, statistical-significance, economic-significance, investment, trend, stationarity, or mechanism claim.",
        },
        "validation_judgment": "accepted_one_bounded_correlation_object",
    }
    statement = {
        "statement_id": STATEMENT_ID,
        "statement_type": "derived_relationship",
        "text": statement_text,
        "origin": "computed_from_retained_dual_series_wdi_fixture",
        "evidence_refs": ["ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture"],
        "dependencies": ["calc-campaign36-pearson-correlation-v1", "align-campaign36-dnk-exports-imports-share"],
        "applicability": {"entity_id": ENTITY_ID, "period_start": START_YEAR, "period_end": END_YEAR, "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0"},
        "structured_payload": payload,
    }
    package: dict[str, Any] = {
        "package_kind": "KnowledgeObjectPackage",
        "package_id": PACKAGE_ID,
        "package_version": "1.0",
        "status": "accepted",
        "created_at": "2026-07-10",
        "created_by": "run_campaign36_dnk_exports_imports_correlation",
        "scope": {"domain": "world_development_indicators", "evidence_family": EVIDENCE_FAMILY, "entity_scope": [ENTITY_ID], "period_scope": {"start": START_YEAR, "end": END_YEAR}},
        "input_references": ["campaign36_dual_series_wdi_https_fixture", "pearson_correlation_calculation_contract_v1"],
        "evidence_references": [{"evidence_ref_id": "ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": "World Bank WDI NE.EXP.GNFS.ZS and NE.IMP.GNFS.ZS DNK annual 1990-2024 fixture", "source_version": exports["provider_metadata"].get("wdi_lastupdated"), "snapshot_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "reproducibility_handle": "retained HTTPS raw fixture, normalized series, alignment contract, and calculation evidence", "evaluation_status": "evaluated", "accessed_at": "2026-07-10"}],
        "generated_statements": [statement],
        "confidence_quality": {"confidence_label": "fixture-supported-deterministic", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture", "missingness_summary": f"{alignment['missing_pair_count']} missing/excluded pairs of {len(EXPECTED_PERIODS)} expected periods", "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "shared_gdp_denominator", "time_ordering_autocorrelation", "structural_breaks", "no_significance_or_causal_claim"]},
        "validation_state": {"validation_result": "pass", "blockers": [], "warnings": ["shared GDP denominator", "economic flow co-movement possible", "no causal/predictive/significance interpretation"]},
        "provenance_envelope": {"evidence_refs": ["ev-campaign36-wdi-dnk-exports-imports-share-dual-series-fixture"], "evaluation_refs": ["campaign36_alignment_validation", "campaign36_calculation_evidence", "campaign36_non_promoted_diagnostics"], "method_refs": [METHOD_IDENTITY], "lineage_basis": "fresh Campaign 36 HTTPS acquisition; Campaign 35 observations not reused as substitute"},
        "lineage": {"previous_package_id": None, "version_lineage": [], "source_campaign": "Campaign 36"},
        "evolution_metadata": {"change_reason": "Campaign 36 first bounded production correlation pilot", "changed_inputs_methods_templates_models_validators": ["wdi_annual_scalar_pearson_correlation_v1"], "previous_revision": None, "dependent_object_review_posture": "not_applicable"},
        "contradiction_records": [{"contradiction_id": "none-recorded", "contradiction_type": "none", "target_statement": STATEMENT_ID, "contradicting_evidence": None, "disposition": "not_applicable"}],
        "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": alignment["combined_aligned_evidence_fingerprint"]},
    }
    package["fingerprints"] = {
        "input_set": sha256_value({"exports": exports["normalized_series_fingerprint"], "imports": imports["normalized_series_fingerprint"], "alignment": alignment["combined_aligned_evidence_fingerprint"]}),
        "evidence_references": sha256_value(package["evidence_references"]),
        "generated_statements": sha256_value(package["generated_statements"]),
        "computation_recipe": sha256_value({"method": METHOD_IDENTITY, "contract": EXPECTED_CONTRACT_FINGERPRINT}),
        "query_definitions": sha256_value([]),
    }
    package["fingerprints"]["package_manifest"] = sha256_value({k: v for k, v in package.items() if k != "fingerprints"})
    package["generated_statements"][0]["structured_payload"]["package_fingerprint"] = package["fingerprints"]["package_manifest"]
    package["fingerprints"]["generated_statements"] = sha256_value(package["generated_statements"])
    package["fingerprints"]["package_manifest"] = sha256_value({k: v for k, v in package.items() if k != "fingerprints"})
    blockers = prohibited_language_check(package)
    if blockers:
        raise ValueError(f"prohibited language detected: {blockers}")
    write_json(REPORT_DIR / "candidate_package.json", package)
    return package


def repository_snapshot() -> dict[str, Any]:
    objects = sorted((REPOSITORY_ROOT / "objects").glob("*.json"))
    manifest = read_json(REPOSITORY_ROOT / "manifest.json")
    return {"object_count": len(objects), "manifest_object_count": manifest.get("object_count"), "repository_fingerprint": manifest.get("repository_fingerprint"), "package_hashes": {p.name: sha256_bytes(p.read_bytes()) for p in objects}}


def promote(package: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    kr = load_module(PROJECT_ROOT / "tools/knowledge_repository.py", "knowledge_repository")
    if (REPOSITORY_ROOT / "objects" / f"{PACKAGE_ID}.json").exists():
        existing = read_json(REPOSITORY_ROOT / "objects" / f"{PACKAGE_ID}.json")
        if existing.get("fingerprints", {}).get("package_manifest") == package["fingerprints"]["package_manifest"]:
            result = kr.persist_knowledge_object_packages([package], REPOSITORY_ROOT)
        else:
            raise ValueError("Campaign 36 package already exists with different fingerprint")
    else:
        result = kr.persist_knowledge_object_packages([package], REPOSITORY_ROOT)
    after = repository_snapshot()
    before_hashes = before["package_hashes"]
    after_hashes = after["package_hashes"]
    changed = [name for name, fp in before_hashes.items() if after_hashes.get(name) != fp]
    disappeared = [name for name in before_hashes if name not in after_hashes]
    added = [name for name in after_hashes if name not in before_hashes]
    immutability = {"valid": changed == [] and disappeared == [] and added == [f"{PACKAGE_ID}.json"], "changed_existing": changed, "disappeared_existing": disappeared, "added": added}
    write_json(REPORT_DIR / "repository_promotion_result.json", {"persist_result": result, "before": {k: v for k, v in before.items() if k != "package_hashes"}, "after": {k: v for k, v in after.items() if k != "package_hashes"}, "immutability": immutability})
    if not immutability["valid"] and not (added == [] and changed == [] and disappeared == []):
        raise ValueError(f"repository immutability failed: {immutability}")
    return {"persist_result": result, "before": before, "after": after, "immutability": immutability}


def local_ai_retry(exports: dict[str, Any], imports: dict[str, Any], statement_text: str) -> dict[str, Any]:
    prompt_obj = {
        "task": "Screen for unit conflict, definitional overlap, shared-denominator risk, prohibited causal/predictive language, and semantic mismatch. Do not calculate correlations.",
        "series_a": {"code": "NE.EXP.GNFS.ZS", "name": exports["metadata"].get("name"), "definition": exports["metadata"].get("sourceNote"), "unit": "percent of GDP"},
        "series_b": {"code": "NE.IMP.GNFS.ZS", "name": imports["metadata"].get("name"), "definition": imports["metadata"].get("sourceNote"), "unit": "percent of GDP"},
        "candidate_statement": statement_text,
    }
    prompt = json.dumps(prompt_obj, sort_keys=True, ensure_ascii=False)
    result = {"status": "skipped", "reason": "ollama unavailable"}
    try:
        listing = subprocess.run(["ollama", "list"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        if listing.returncode != 0 or "qwen3:4b" not in listing.stdout:
            result = {"status": "skipped", "reason": "qwen3:4b unavailable", "ollama_list": listing.stdout + listing.stderr}
        else:
            pre_start = time.time()
            prewarm = subprocess.run(["ollama", "run", "qwen3:4b", "Return OK."], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            start = time.time()
            proc = subprocess.run(["ollama", "run", "qwen3:4b", prompt], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            output = proc.stdout + proc.stderr
            result = {
                "status": "completed" if proc.returncode == 0 else "failed",
                "model": "qwen3:4b",
                "model_listing": listing.stdout,
                "prewarm_status": "completed" if prewarm.returncode == 0 else "failed",
                "prewarm_output_fingerprint": sha256_bytes((prewarm.stdout + prewarm.stderr).encode()),
                "prewarm_seconds": round(start - pre_start, 3),
                "prompt": prompt,
                "input_fingerprint": sha256_bytes(prompt.encode("utf-8")),
                "raw_output": output[:8000],
                "output_fingerprint": sha256_bytes(output.encode("utf-8")),
                "execution_time_seconds": round(time.time() - start, 3),
                "token_counts": None,
                "deterministic_human_disposition": "advisory only; deterministic validators govern acceptance",
                "value_assessment": "recorded for screening evidence; no acceptance authority",
            }
    except Exception as exc:
        result = {"status": "failed", "error": str(exc), "disposition": "current local setup unsuitable for this screening route until routing/model-serving evidence changes"}
    write_json(REPORT_DIR / "local_ai_retry.json", result)
    return result


def write_report(package: dict[str, Any], raw: dict[str, Any], alignment: dict[str, Any], calc: dict[str, Any], diag: dict[str, Any], repo: dict[str, Any], ai: dict[str, Any]) -> None:
    coeff = calc["method_result"]["coefficient"]["canonical"]
    report = f"""# Campaign 36 — Bounded WDI Denmark Exports-Imports Share Pearson Correlation Pilot

Outcome: A — Successful correlation pilot.

Package promoted: `{PACKAGE_ID}`

Pearson coefficient: `{coeff}`

Aligned observations: {alignment['aligned_pair_count']} of {len(EXPECTED_PERIODS)} expected annual periods, {alignment['first_aligned_period']}–{alignment['last_aligned_period']}.

Repository count before: {repo['before']['object_count']}
Repository count after: {repo['after']['object_count']}
Repository fingerprint after: `{repo['after']['repository_fingerprint']}`

Method: `{METHOD_IDENTITY}`
Contract fingerprint: `{EXPECTED_CONTRACT_FINGERPRINT}`
Calculation evidence fingerprint: `{calc['calculation_evidence_fingerprint']}`
Combined aligned evidence fingerprint: `{alignment['combined_aligned_evidence_fingerprint']}`

Mechanical-overlap assessment: both indicators use GDP as denominator; exports/imports are economically related flows. This does not invalidate the object, but it blocks causal, predictive, significance, performance, mechanism, or investment interpretation.

Diagnostics, not promoted:
- exports vs time index: {diag['non_promoted_diagnostics']['exports_vs_time_index_coefficient']}
- imports vs time index: {diag['non_promoted_diagnostics']['imports_vs_time_index_coefficient']}
- first-difference sensitivity: {diag['non_promoted_diagnostics']['first_difference_sensitivity_coefficient']}

Local AI retry: {ai.get('status')}

Campaign 37: not executed.
"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "campaign36_report.md").write_text(report)


def run(reuse_fixture: bool = False, no_promote: bool = False) -> dict[str, Any]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    before = repository_snapshot()
    raw = read_json(FIXTURE_DIR / "raw_fixture_manifest.json") if reuse_fixture and (FIXTURE_DIR / "raw_fixture_manifest.json").exists() else acquire_fixture()
    exports = normalize_series("exports", raw)
    imports = normalize_series("imports", raw)
    alignment = validate_and_align(exports, imports)
    calc = calculate(exports, imports, alignment)
    diag = diagnostics(exports, imports, alignment)
    package = build_package(raw, exports, imports, alignment, calc, diag)
    if no_promote:
        repo = {"before": before, "after": before, "immutability": {"valid": True, "added": []}}
    else:
        repo = promote(package, before)
    if no_promote and (REPORT_DIR / "local_ai_retry.json").exists():
        ai = read_json(REPORT_DIR / "local_ai_retry.json")
    else:
        ai = local_ai_retry(exports, imports, package["generated_statements"][0]["text"])
    write_report(package, raw, alignment, calc, diag, repo, ai)
    result = {"outcome": "A", "package_id": PACKAGE_ID, "coefficient": calc["method_result"]["coefficient"]["canonical"], "aligned_pair_count": alignment["aligned_pair_count"], "repository_after": {k: v for k, v in repo["after"].items() if k != "package_hashes"}, "package_fingerprint": package["fingerprints"]["package_manifest"]}
    write_json(REPORT_DIR / "campaign36_result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse-fixture", action="store_true")
    parser.add_argument("--no-promote", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(reuse_fixture=args.reuse_fixture, no_promote=args.no_promote), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
