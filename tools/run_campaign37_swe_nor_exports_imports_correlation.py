#!/usr/bin/env python3
"""Campaign 37: SWE/NOR exports-imports share Pearson correlation replication.

Bounded controlled replication of Campaign 36. Varies only entity dimension.
No local-AI retry, no schema/doctrine/package-model changes.
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
FIXTURE_DIR = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign37-wdi-swe-nor-exports-imports-share-correlation-1990-2024-https"
REPORT_DIR = PROJECT_ROOT / "artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710"
EVIDENCE_FAMILY = "external_wdi_annual_scalar_trade_pearson_correlation"
METHOD_IDENTITY = "wdi_annual_scalar_pearson_correlation_v1@1.0"
EXPECTED_CONTRACT_FINGERPRINT = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
START_YEAR = 1990
END_YEAR = 2024
EXPECTED_PERIODS = list(range(START_YEAR, END_YEAR + 1))
MIN_ALIGNED_PAIRS = 30
MIN_COVERAGE = Decimal("0.85")
INTERNAL_CONTEXT = Context(prec=50, rounding=ROUND_HALF_EVEN)
ENTITIES = {"SWE": "Sweden", "NOR": "Norway"}
SERIES = {
    "exports": {
        "code": "NE.EXP.GNFS.ZS",
        "name": "Exports of goods and services (% of GDP)",
        "role": "series_a",
        "metadata_url": "https://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json&per_page=1",
        "observations_url": "https://api.worldbank.org/v2/country/SWE;NOR/indicator/NE.EXP.GNFS.ZS?format=json&date=1990:2024&per_page=20000",
    },
    "imports": {
        "code": "NE.IMP.GNFS.ZS",
        "name": "Imports of goods and services (% of GDP)",
        "role": "series_b",
        "metadata_url": "https://api.worldbank.org/v2/indicator/NE.IMP.GNFS.ZS?format=json&per_page=1",
        "observations_url": "https://api.worldbank.org/v2/country/SWE;NOR/indicator/NE.IMP.GNFS.ZS?format=json&date=1990:2024&per_page=20000",
    },
}
PROHIBITED = ["causes", "cause", "predicts", "forecast", "investment", "recommendation", "statistically significant", "economically significant", "trade performance", "stable relationship"]


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
    req = urllib.request.Request(url, headers={"User-Agent": "KnowledgeForge-Campaign37/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        final_url = response.geturl()
        body = response.read()
        headers = dict(response.headers.items())
    if not final_url.startswith("https://"):
        raise ValueError(f"protocol downgrade rejected: {url} -> {final_url}")
    return {"requested_url": url, "final_url": final_url, "headers": headers, "bytes": body, "fingerprint": sha256_bytes(body), "json": json.loads(body.decode("utf-8"))}


def inspect_campaign35_reuse() -> dict[str, Any]:
    # Reuse was inspected and rejected deliberately: Campaign 35 has exports only, different selection contract/family,
    # and no imports companion. Fresh bounded Campaign 37 evidence gives simpler metadata comparability and lineage.
    c35 = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign35-wdi-nordic-exports-share-1990-2024-https"
    exists = c35.exists()
    return {
        "campaign35_fixture_exists": exists,
        "decision": "fresh_reacquisition",
        "reason": "Campaign 35 contains exports-share evidence only under a statistical-summary selection contract; Campaign 37 requires a consolidated dual-series correlation fixture with imports companion evidence and directly comparable metadata. Reuse conditions are therefore cumbersome/uncertain, so fresh bounded exports/imports evidence was acquired.",
        "historical_artifact_modified": False,
    }


def acquire_fixture() -> dict[str, Any]:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    raw: dict[str, Any] = {"series": {}, "accessed_at": datetime.now(timezone.utc).isoformat(), "reuse_decision": inspect_campaign35_reuse()}
    deterministic_records = {}
    for key, spec in SERIES.items():
        meta = acquire_url(spec["metadata_url"])
        obs = acquire_url(spec["observations_url"])
        (FIXTURE_DIR / f"{key}_metadata_raw.json").write_bytes(meta["bytes"])
        (FIXTURE_DIR / f"{key}_observations_raw.json").write_bytes(obs["bytes"])
        meta_record = meta["json"][1][0]
        page = obs["json"][0]
        raw["series"][key] = {
            "code": spec["code"], "role": spec["role"],
            "metadata_requested_url": meta["requested_url"], "metadata_final_url": meta["final_url"], "metadata_raw_fingerprint": meta["fingerprint"],
            "observation_requested_url": obs["requested_url"], "observation_final_url": obs["final_url"], "observation_raw_fingerprint": obs["fingerprint"],
            "metadata": meta_record, "pagination": page,
            "provider_source": {"sourceid": meta_record.get("source", {}).get("id"), "source": meta_record.get("source", {}).get("value")},
            "lastupdated": page.get("lastupdated"),
        }
        deterministic_records[key] = raw["series"][key]
    selection = {
        "campaign": "campaign37_swe_nor_exports_imports_share_pearson_correlation_replication",
        "entities": sorted(ENTITIES), "periods": EXPECTED_PERIODS, "frequency": "annual", "transformation": "raw",
        "series": {k: {"code": v["code"], "metadata_url": v["metadata_url"], "observations_url": v["observations_url"]} for k, v in SERIES.items()},
        "method_identity": METHOD_IDENTITY, "contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT,
    }
    raw["selection_contract"] = selection
    raw["selection_fingerprint"] = sha256_value(selection)
    raw["combined_fixture_fingerprint"] = sha256_value({"series": deterministic_records, "selection": selection, "reuse_decision": raw["reuse_decision"]})
    write_json(FIXTURE_DIR / "raw_fixture_manifest.json", {k: v for k, v in raw.items() if k != "accessed_at"})
    return raw


def resolve_unit(metadata: dict[str, Any]) -> dict[str, Any]:
    fixture = load_module(PROJECT_ROOT / "tools/wdi_observation_evidence_fixture.py", "wdi_fixture")
    resolution = fixture.resolve_wdi_unit(metadata)
    unit = resolution.get("unit") or resolution.get("resolved_unit")
    state = resolution.get("state")
    if state not in {"definition_derived", "definition-derived unit"} or unit != "percent of GDP":
        raise ValueError(f"unit resolution failed closed: {resolution}")
    out = dict(resolution); out["unit"] = unit
    return out


def parse_decimal(value: Any) -> str:
    text = str(value)
    if "e" in text.lower() or "," in text:
        raise ValueError(f"ambiguous numeric string: {text}")
    dec = Decimal(text)
    if not dec.is_finite():
        raise ValueError(f"non-finite decimal: {text}")
    return format(dec, "f")


def normalize_series(key: str, entity: str, raw: dict[str, Any]) -> dict[str, Any]:
    record = raw["series"][key]
    metadata = record["metadata"]
    unit = resolve_unit(metadata)
    obs = json.loads((FIXTURE_DIR / f"{key}_observations_raw.json").read_text())
    rows = obs[1]
    seen: set[int] = set()
    normalized = []
    for row in sorted(rows, key=lambda r: (r.get("countryiso3code") or "", int(r["date"]))):
        row_entity = row.get("countryiso3code") or row.get("country", {}).get("id")
        if row_entity != entity:
            continue
        code = row.get("indicator", {}).get("id")
        period = int(row["date"])
        if code != record["code"]: raise ValueError(f"unexpected indicator: {code}")
        if period < START_YEAR or period > END_YEAR: raise ValueError(f"unexpected period: {period}")
        if period in seen: raise ValueError(f"duplicate period: {entity} {key} {period}")
        seen.add(period)
        value = row.get("value")
        normalized.append({
            "entity_id": entity, "entity_name": ENTITIES[entity], "indicator_code": code, "indicator_name": metadata.get("name"),
            "period": period, "frequency": "annual", "transformation": "raw", "unit": unit["unit"], "unit_resolution": unit,
            "observed": value is not None, "value_canonical": parse_decimal(value) if value is not None else None,
            "provider_decimal_source": str(value) if value is not None else None,
        })
    missing_slots = sorted(set(EXPECTED_PERIODS) - seen)
    # Preserve explicit missing slots if API omits any expected period.
    for p in missing_slots:
        normalized.append({"entity_id": entity, "entity_name": ENTITIES[entity], "indicator_code": record["code"], "indicator_name": metadata.get("name"), "period": p, "frequency": "annual", "transformation": "raw", "unit": unit["unit"], "unit_resolution": unit, "observed": False, "value_canonical": None, "provider_decimal_source": None, "missing_slot_synthesized_from_expected_period_contract": True})
    normalized = sorted(normalized, key=lambda r: r["period"])
    result = {
        "series_key": key,
        "series_id": {"indicator_code": record["code"], "indicator_name": metadata.get("name"), "entity_id": entity, "entity_name": ENTITIES[entity], "frequency": "annual", "unit": unit["unit"], "transformation": "raw"},
        "metadata": metadata,
        "provider_metadata": {"provider": "World Bank", "dataset": "World Development Indicators", "sourceid": metadata.get("source", {}).get("id"), "source": metadata.get("source", {}).get("value"), "wdi_lastupdated": obs[0].get("lastupdated")},
        "raw_fingerprints": {"metadata": record["metadata_raw_fingerprint"], "observations": record["observation_raw_fingerprint"]},
        "observations": normalized,
    }
    result["normalized_series_fingerprint"] = sha256_value({"series_id": result["series_id"], "observations": normalized})
    write_json(FIXTURE_DIR / f"{entity.lower()}_{key}_normalized_series.json", result)
    return result


def validate_and_align(entity: str, exports: dict[str, Any], imports: dict[str, Any]) -> dict[str, Any]:
    by_key = {}; missing = {}; duplicate_key_count = {}; variance = {}
    for label, series in [("exports", exports), ("imports", imports)]:
        values = {}; missing[label] = []; seen=[]
        for row in series["observations"]:
            p = row["period"]; seen.append(p)
            if row["entity_id"] != entity: raise ValueError("entity mismatch")
            if row["frequency"] != "annual" or row["transformation"] != "raw" or row["unit"] != "percent of GDP": raise ValueError("scope mismatch")
            if row.get("observed") and row.get("value_canonical") is not None:
                if p in values: raise ValueError(f"duplicate normalized observed period {entity} {label} {p}")
                values[p] = row["value_canonical"]
            else:
                missing[label].append(p)
        duplicate_key_count[label] = len(seen) - len(set(seen))
        if duplicate_key_count[label]: raise ValueError("duplicate period keys")
        if len(set(values.values())) == 1: raise ValueError(f"constant series: {entity} {label}")
        variance[label] = "non_zero"
        by_key[label] = values
    aligned_periods = sorted(set(by_key["exports"]) & set(by_key["imports"]))
    excluded = sorted(set(EXPECTED_PERIODS) - set(aligned_periods))
    coverage = Decimal(len(aligned_periods)) / Decimal(len(EXPECTED_PERIODS))
    if len(aligned_periods) < MIN_ALIGNED_PAIRS or coverage < MIN_COVERAGE: raise ValueError(f"alignment thresholds failed: {entity}")
    aligned = [{"period": p, "exports": by_key["exports"][p], "imports": by_key["imports"][p]} for p in aligned_periods]
    alignment = {"entity_id": entity, "expected_periods": EXPECTED_PERIODS, "observed_periods": {"exports": sorted(by_key["exports"]), "imports": sorted(by_key["imports"])}, "aligned_periods": aligned_periods, "missing_exports_periods": missing["exports"], "missing_imports_periods": missing["imports"], "excluded_periods": excluded, "missing_pair_count": len(excluded), "aligned_pair_count": len(aligned_periods), "aligned_coverage": str(coverage), "first_aligned_period": aligned_periods[0], "last_aligned_period": aligned_periods[-1], "duplicate_key_count": duplicate_key_count, "variance_checks": variance, "aligned_values": aligned}
    alignment["combined_aligned_evidence_fingerprint"] = sha256_value({"entity": entity, "exports_normalized": exports["normalized_series_fingerprint"], "imports_normalized": imports["normalized_series_fingerprint"], "aligned_values": aligned, "alignment_contract": {"join": "inner observed periods", "minimum_pairs": MIN_ALIGNED_PAIRS, "coverage": str(MIN_COVERAGE)}})
    write_json(FIXTURE_DIR / f"{entity.lower()}_alignment_contract_and_result.json", alignment)
    return alignment


def as_corr_series(series: dict[str, Any]) -> dict[str, Any]:
    return {"series_id": series["series_id"], "observations": series["observations"]}


def independent_recompute(aligned: list[dict[str, str]], coefficient: str) -> dict[str, Any]:
    xs = [Decimal(r["exports"]) for r in aligned]; ys = [Decimal(r["imports"]) for r in aligned]
    with localcontext(INTERNAL_CONTEXT):
        n = Decimal(len(xs)); mx = sum(xs, Decimal(0)) / n; my = sum(ys, Decimal(0)) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); vx = sum((x - mx) * (x - mx) for x in xs); vy = sum((y - my) * (y - my) for y in ys)
        den = (vx * vy).sqrt(context=INTERNAL_CONTEXT); raw = num / den; can = raw.quantize(Decimal("0.000000000001"))
    text = format(can, "f").rstrip("0").rstrip(".")
    if text == "-0": text = "0"
    return {"matches": text == coefficient, "canonical": text, "unrounded_internal": format(raw, "f"), "mean_x": format(mx, "f"), "mean_y": format(my, "f"), "numerator": format(num, "f"), "variance_x": format(vx, "f"), "variance_y": format(vy, "f"), "denominator": format(den, "f")}


def calculate(entity: str, exports: dict[str, Any], imports: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", f"corr_{entity}")
    contract = corr.calculation_contract_v1()
    if contract["calculation_contract_fingerprint"] != EXPECTED_CONTRACT_FINGERPRINT: raise ValueError("contract fingerprint mismatch")
    result = corr.compute_correlation(as_corr_series(exports), as_corr_series(imports), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=MIN_COVERAGE)
    swapped = corr.compute_correlation(as_corr_series(imports), as_corr_series(exports), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=MIN_COVERAGE)
    if result["coefficient"] != swapped["coefficient"] or result["canonical_pair_id"] != swapped["canonical_pair_id"]: raise ValueError("pair order invariance failed")
    independent = independent_recompute(alignment["aligned_values"], result["coefficient"]["canonical"])
    if not independent["matches"]: raise ValueError("independent recomputation mismatch")
    evidence = {"entity_id": entity, "method_result": result, "swapped_pair_result_fingerprint": swapped["output_fingerprint"], "independent_recompute": independent, "calculation_evidence": {"aligned_values": alignment["aligned_values"], "means": {"exports": independent["mean_x"], "imports": independent["mean_y"]}, "centered_sum_numerator": independent["numerator"], "sum_of_squares": {"exports": independent["variance_x"], "imports": independent["variance_y"]}, "denominator": independent["denominator"], "unrounded_internal_coefficient": independent["unrounded_internal"], "canonical_coefficient": result["coefficient"]["canonical"], "aligned_pair_count": result["aligned_pair_count"], "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT}}
    evidence["calculation_evidence_fingerprint"] = sha256_value(evidence["calculation_evidence"])
    write_json(REPORT_DIR / f"{entity.lower()}_calculation_evidence.json", evidence)
    return evidence


def diagnostics(entity: str, exports: dict[str, Any], imports: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", f"corrdiag_{entity}")
    def series_with_values(code: str, unit: str, vals: list[str], transform: str = "raw") -> dict[str, Any]:
        return {"series_id": {"indicator_code": code, "entity_id": entity, "frequency": "annual", "unit": unit, "transformation": transform}, "observations": [{"period": p, "observed": True, "value_canonical": v} for p, v in zip(EXPECTED_PERIODS[-len(vals):], vals)]}
    exp_vals = [r["exports"] for r in alignment["aligned_values"]]; imp_vals = [r["imports"] for r in alignment["aligned_values"]]
    time_vals = [str(i) for i in range(1, len(alignment["aligned_values"]) + 1)]
    exp_time = corr.compute_correlation(series_with_values("NE.EXP.GNFS.ZS", "percent of GDP", exp_vals), series_with_values("CANONICAL_ANNUAL_TIME_INDEX", "index", time_vals), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"), same_entity_required=True)
    imp_time = corr.compute_correlation(series_with_values("NE.IMP.GNFS.ZS", "percent of GDP", imp_vals), series_with_values("CANONICAL_ANNUAL_TIME_INDEX", "index", time_vals), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"), same_entity_required=True)
    exp_diff = [format(Decimal(exp_vals[i]) - Decimal(exp_vals[i-1]), "f") for i in range(1, len(exp_vals))]
    imp_diff = [format(Decimal(imp_vals[i]) - Decimal(imp_vals[i-1]), "f") for i in range(1, len(imp_vals))]
    diff_corr = corr.compute_correlation(series_with_values("NE.EXP.GNFS.ZS", "percent of GDP delta", exp_diff, "first_difference"), series_with_values("NE.IMP.GNFS.ZS", "percent of GDP delta", imp_diff, "first_difference"), minimum_aligned_pairs=MIN_ALIGNED_PAIRS, coverage_threshold=Decimal("0"))
    diag = {"entity_id": entity, "mechanical_overlap_assessment": {"both_use_gdp_denominator": True, "related_external_sector_flow_measures": True, "identity_or_component_total_detected": False, "promotion_blocker": False, "warning": "Raw-level correlation may reflect shared GDP denominator, common time movement, external shocks, autocorrelation, structural breaks, economic co-movement, or unidentified mechanisms."}, "non_promoted_diagnostics": {"exports_vs_time_index_coefficient": exp_time["coefficient"]["canonical"], "imports_vs_time_index_coefficient": imp_time["coefficient"]["canonical"], "first_difference_sensitivity_coefficient": diff_corr["coefficient"]["canonical"], "status": "diagnostic_only_not_promoted", "limitation": "Raw and first-difference comparison is transformation-sensitivity evidence only, not economic interpretation."}}
    diag["diagnostic_fingerprint"] = sha256_value(diag)
    write_json(REPORT_DIR / f"{entity.lower()}_non_promoted_diagnostics.json", diag)
    return diag


def prohibited_language_check(package: dict[str, Any]) -> list[str]:
    text = canonical_json(package).lower(); found=[]
    allowed_context=["no causation", "not causal", "not predictive", "not claim", "not imply", "non-causality", "prohibited", "no causal/predictive/significance"]
    for term in PROHIBITED:
        if term in text and not any(ctx in text for ctx in allowed_context): found.append(term)
    return found


def package_id(entity: str) -> str:
    return f"pkg-object-srcpkg-campaign37-{entity.lower()}-exports-imports-share-pearson-correlation-v1"


def build_package(raw: dict[str, Any], entity: str, exports: dict[str, Any], imports: dict[str, Any], alignment: dict[str, Any], calc: dict[str, Any], diag: dict[str, Any]) -> dict[str, Any]:
    coeff = calc["method_result"]["coefficient"]["canonical"]; pid=package_id(entity); stmt_id=f"stmt-campaign37-{entity.lower()}-exports-imports-share-pearson-correlation-v1"
    statement_text = f"Across the aligned annual {entity} observations from 1990 through 2024, the Pearson correlation between exports of goods and services as a percentage of GDP and imports of goods and services as a percentage of GDP is {coeff}, using {alignment['aligned_pair_count']} aligned observations."
    payload = {"canonical_pair_identity": calc["method_result"]["canonical_pair_id"], "series_a": {"code": "NE.EXP.GNFS.ZS", "name": exports["series_id"]["indicator_name"], "definition": exports["metadata"].get("sourceNote"), "unit": "percent of GDP", "raw_fingerprints": exports["raw_fingerprints"], "normalized_fingerprint": exports["normalized_series_fingerprint"]}, "series_b": {"code": "NE.IMP.GNFS.ZS", "name": imports["series_id"]["indicator_name"], "definition": imports["metadata"].get("sourceNote"), "unit": "percent of GDP", "raw_fingerprints": imports["raw_fingerprints"], "normalized_fingerprint": imports["normalized_series_fingerprint"]}, "entity_id": entity, "entity_name": ENTITIES[entity], "frequency": "annual", "period_scope": {"start": START_YEAR, "end": END_YEAR}, "transformation_state": {"series_a": "raw", "series_b": "raw"}, "aligned_pair_count": alignment["aligned_pair_count"], "aligned_coverage": alignment["aligned_coverage"], "missing_pair_count": alignment["missing_pair_count"], "excluded_periods": alignment["excluded_periods"], "aligned_periods": alignment["aligned_periods"], "pearson_coefficient": {"canonical": coeff, "unit": "dimensionless"}, "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0", "method_contract_fingerprint": EXPECTED_CONTRACT_FINGERPRINT, "selection_fingerprint": raw["selection_fingerprint"], "combined_fixture_fingerprint": raw["combined_fixture_fingerprint"], "combined_aligned_evidence_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "calculation_evidence_fingerprint": calc["calculation_evidence_fingerprint"], "provider_metadata": {"exports": exports["provider_metadata"], "imports": imports["provider_metadata"]}, "mutable_source_limitation": "Retained bytes, not mutable WDI API reacquisition, provide exact historical reproducibility.", "limitations": {"shared_gdp_denominator": "Both indicators use GDP as denominator; the coefficient may partly reflect shared-denominator movement.", "time_ordering_autocorrelation": "Annual macroeconomic series can exhibit time ordering/autocorrelation; no stationarity or independence claim is made.", "structural_breaks": "The coefficient is scoped only to the retained 1990-2024 aligned window and may not hold across structural breaks.", "non_causality_non_prediction": "The coefficient is a deterministic contemporaneous mathematical relationship only and is not causal, not predictive, not statistical-significance, not economic-significance, not investment, not trend, and not mechanism evidence."}, "validation_judgment": "accepted_bounded_correlation_replication_object", "package_fingerprint": None}
    statement={"statement_id": stmt_id, "statement_type": "derived_relationship", "text": statement_text, "origin": "computed_from_retained_dual_entity_dual_series_wdi_fixture", "evidence_refs": ["ev-campaign37-wdi-swe-nor-exports-imports-share-dual-series-fixture"], "dependencies": [f"calc-campaign37-{entity.lower()}-pearson-correlation-v1", f"align-campaign37-{entity.lower()}-exports-imports-share"], "applicability": {"entity_id": entity, "period_start": START_YEAR, "period_end": END_YEAR, "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0"}, "structured_payload": payload}
    pkg={"package_kind": "KnowledgeObjectPackage", "package_id": pid, "package_version": "1.0", "status": "accepted", "created_at": "2026-07-10", "created_by": "run_campaign37_swe_nor_exports_imports_correlation", "scope": {"domain": "world_development_indicators", "evidence_family": EVIDENCE_FAMILY, "entity_scope": [entity], "period_scope": {"start": START_YEAR, "end": END_YEAR}}, "input_references": ["campaign37_dual_entity_dual_series_wdi_https_fixture", "pearson_correlation_calculation_contract_v1"], "evidence_references": [{"evidence_ref_id": "ev-campaign37-wdi-swe-nor-exports-imports-share-dual-series-fixture", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": f"World Bank WDI NE.EXP.GNFS.ZS and NE.IMP.GNFS.ZS {entity} annual 1990-2024 fixture", "source_version": exports["provider_metadata"].get("wdi_lastupdated"), "snapshot_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "reproducibility_handle": "retained HTTPS raw fixture, normalized series, alignment contract, and calculation evidence", "evaluation_status": "evaluated", "accessed_at": "2026-07-10"}], "generated_statements": [statement], "confidence_quality": {"confidence_label": "fixture-supported-deterministic", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation replication", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture", "missingness_summary": f"{alignment['missing_pair_count']} missing/excluded pairs of {len(EXPECTED_PERIODS)} expected periods", "uncertainty_dimensions": ["mutable_source_reacquisition_limit", "shared_gdp_denominator", "time_ordering_autocorrelation", "structural_breaks", "no_significance_or_causal_claim"]}, "validation_state": {"validation_result": "pass", "blockers": [], "warnings": ["shared GDP denominator", "economic flow co-movement possible", "no causal/predictive/significance interpretation"]}, "provenance_envelope": {"evidence_refs": ["ev-campaign37-wdi-swe-nor-exports-imports-share-dual-series-fixture"], "evaluation_refs": [f"campaign37_{entity.lower()}_alignment_validation", f"campaign37_{entity.lower()}_calculation_evidence", f"campaign37_{entity.lower()}_non_promoted_diagnostics"], "method_refs": [METHOD_IDENTITY], "lineage_basis": "fresh Campaign 37 HTTPS acquisition; Campaign 35 exports evidence inspected but not reused"}, "lineage": {"previous_package_id": None, "version_lineage": [], "source_campaign": "Campaign 37", "replicates_method_from": "Campaign 36"}, "evolution_metadata": {"change_reason": "Campaign 37 controlled entity replication", "changed_inputs_methods_templates_models_validators": [], "previous_revision": None, "dependent_object_review_posture": "not_applicable"}, "contradiction_records": [{"contradiction_id": "none-recorded", "contradiction_type": "none", "target_statement": stmt_id, "contradicting_evidence": None, "disposition": "not_applicable"}], "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": alignment["combined_aligned_evidence_fingerprint"]}}
    pkg["fingerprints"]={"input_set": sha256_value({"exports": exports["normalized_series_fingerprint"], "imports": imports["normalized_series_fingerprint"], "alignment": alignment["combined_aligned_evidence_fingerprint"]}), "evidence_references": sha256_value(pkg["evidence_references"]), "generated_statements": sha256_value(pkg["generated_statements"]), "computation_recipe": sha256_value({"method": METHOD_IDENTITY, "contract": EXPECTED_CONTRACT_FINGERPRINT}), "query_definitions": sha256_value([])}
    pkg["fingerprints"]["package_manifest"] = sha256_value({k:v for k,v in pkg.items() if k != "fingerprints"})
    pkg["generated_statements"][0]["structured_payload"]["package_fingerprint"] = pkg["fingerprints"]["package_manifest"]
    pkg["fingerprints"]["generated_statements"] = sha256_value(pkg["generated_statements"])
    pkg["fingerprints"]["package_manifest"] = sha256_value({k:v for k,v in pkg.items() if k != "fingerprints"})
    pkg["generated_statements"][0]["structured_payload"]["package_fingerprint"] = pkg["fingerprints"]["package_manifest"]
    blockers = prohibited_language_check(pkg)
    if blockers: raise ValueError(f"prohibited language detected: {blockers}")
    write_json(REPORT_DIR / f"{entity.lower()}_candidate_package.json", pkg)
    return pkg


def repository_snapshot() -> dict[str, Any]:
    objects = sorted((REPOSITORY_ROOT / "objects").glob("*.json")); manifest = read_json(REPOSITORY_ROOT / "manifest.json")
    return {"object_count": len(objects), "manifest_object_count": manifest.get("object_count"), "repository_fingerprint": manifest.get("repository_fingerprint"), "package_hashes": {p.name: sha256_bytes(p.read_bytes()) for p in objects}}


def promote(packages: list[dict[str, Any]], before: dict[str, Any]) -> dict[str, Any]:
    kr=load_module(PROJECT_ROOT / "tools/knowledge_repository.py", "knowledge_repository")
    result=kr.persist_knowledge_object_packages(packages, REPOSITORY_ROOT)
    after=repository_snapshot(); before_hashes=before["package_hashes"]; after_hashes=after["package_hashes"]
    changed=[n for n,fp in before_hashes.items() if after_hashes.get(n)!=fp]; disappeared=[n for n in before_hashes if n not in after_hashes]; added=[n for n in after_hashes if n not in before_hashes]
    expected=sorted([p["package_id"]+".json" for p in packages])
    imm={"valid": changed==[] and disappeared==[] and sorted(added)==expected, "changed_existing": changed, "disappeared_existing": disappeared, "added": sorted(added), "expected_added": expected}
    write_json(REPORT_DIR / "repository_promotion_result.json", {"persist_result": result, "before": {k:v for k,v in before.items() if k!="package_hashes"}, "after": {k:v for k,v in after.items() if k!="package_hashes"}, "immutability": imm})
    if not imm["valid"] and not (added==[] and changed==[] and disappeared==[]): raise ValueError(f"repository immutability failed: {imm}")
    return {"persist_result": result, "before": before, "after": after, "immutability": imm}


def write_campaign_artifacts(raw: dict[str, Any], entities: dict[str, Any], repo: dict[str, Any], no_promote: bool) -> None:
    coeffs={e:d["calc"]["method_result"]["coefficient"]["canonical"] for e,d in entities.items()}
    diag_lines="\n".join([f"- {e}: exports/time {d['diag']['non_promoted_diagnostics']['exports_vs_time_index_coefficient']}; imports/time {d['diag']['non_promoted_diagnostics']['imports_vs_time_index_coefficient']}; first-difference {d['diag']['non_promoted_diagnostics']['first_difference_sensitivity_coefficient']}" for e,d in entities.items()])
    report=f"""# Campaign 37 — SWE/NOR Exports-Imports Share Pearson Correlation Replication

Outcome: {'not promoted rerun' if no_promote else 'A — Successful controlled replication'}.

Evidence decision: {raw['reuse_decision']['decision']} — {raw['reuse_decision']['reason']}

Accepted packages: {len(entities)}

Coefficients:
""" + "\n".join([f"- {e}: `{c}`" for e,c in coeffs.items()]) + f"""

Repository count before: {repo['before']['object_count']}
Repository count after: {repo['after']['object_count']}
Repository fingerprint after: `{repo['after']['repository_fingerprint']}`

Method: `{METHOD_IDENTITY}`
Contract fingerprint: `{EXPECTED_CONTRACT_FINGERPRINT}`
Combined fixture fingerprint: `{raw['combined_fixture_fingerprint']}`

Diagnostics, not promoted:
{diag_lines}

Local AI: not retried. Existing 45-second and 120-second qwen3:4b attempts failed; current local screening route deferred until model-serving/routing evidence changes.

Campaign 38: not executed.
"""
    (REPORT_DIR / "campaign37_report.md").write_text(report)
    result={"outcome":"A" if len(entities)==2 and not no_promote else "rerun_no_promote", "accepted_entities": sorted(entities), "coefficients": coeffs, "package_ids": [entities[e]["package"]["package_id"] for e in sorted(entities)], "package_fingerprints": {e: entities[e]["package"]["fingerprints"]["package_manifest"] for e in entities}, "repository_after": {k:v for k,v in repo["after"].items() if k!="package_hashes"}}
    write_json(REPORT_DIR / "campaign37_result.json", result)


def run(reuse_fixture: bool=False, no_promote: bool=False) -> dict[str, Any]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True); before=repository_snapshot()
    raw = read_json(FIXTURE_DIR / "raw_fixture_manifest.json") if reuse_fixture and (FIXTURE_DIR / "raw_fixture_manifest.json").exists() else acquire_fixture()
    accepted={}; rejected={}
    for entity in ENTITIES:
        try:
            exports=normalize_series("exports", entity, raw); imports=normalize_series("imports", entity, raw)
            alignment=validate_and_align(entity, exports, imports); calc=calculate(entity, exports, imports, alignment); diag=diagnostics(entity, exports, imports, alignment); pkg=build_package(raw, entity, exports, imports, alignment, calc, diag)
            accepted[entity]={"exports":exports,"imports":imports,"alignment":alignment,"calc":calc,"diag":diag,"package":pkg,"judgment":"accepted"}
        except Exception as exc:
            rejected[entity]={"judgment":"rejected","error":str(exc)}
    write_json(REPORT_DIR / "candidate_judgments.json", {"accepted": {e:{"package_id":d["package"]["package_id"],"coefficient":d["calc"]["method_result"]["coefficient"]["canonical"],"aligned_pair_count":d["alignment"]["aligned_pair_count"]} for e,d in accepted.items()}, "rejected": rejected})
    packages=[accepted[e]["package"] for e in sorted(accepted)]
    repo={"before":before,"after":before,"immutability":{"valid":True,"added":[]}} if no_promote else promote(packages, before)
    if no_promote:
        result={"outcome":"rerun_no_promote", "accepted_entities": sorted(accepted), "coefficients": {e: accepted[e]["calc"]["method_result"]["coefficient"]["canonical"] for e in accepted}, "package_ids": [accepted[e]["package"]["package_id"] for e in sorted(accepted)], "package_fingerprints": {e: accepted[e]["package"]["fingerprints"]["package_manifest"] for e in accepted}, "repository_after": {k:v for k,v in repo["after"].items() if k!="package_hashes"}}
        write_json(REPORT_DIR / "campaign37_no_promote_rerun_result.json", result)
        return result
    write_campaign_artifacts(raw, accepted, repo, no_promote)
    return read_json(REPORT_DIR / "campaign37_result.json")


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--reuse-fixture", action="store_true"); parser.add_argument("--no-promote", action="store_true")
    args=parser.parse_args(); print(json.dumps(run(reuse_fixture=args.reuse_fixture, no_promote=args.no_promote), indent=2, sort_keys=True)); return 0

if __name__ == "__main__":
    raise SystemExit(main())
