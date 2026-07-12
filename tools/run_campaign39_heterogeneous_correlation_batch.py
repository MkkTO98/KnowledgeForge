#!/usr/bin/env python3
"""Campaign 39: small heterogeneous WDI Pearson correlation batch."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN, Context, localcontext
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
REPORT_DIR = PROJECT_ROOT / "artifacts/reports/campaign39-heterogeneous-wdi-pearson-batch-20260711"
SELECTION_PATH = REPORT_DIR / "selection/campaign39_frozen_batch_selection_decision.json"
FIXTURE_DIR = PROJECT_ROOT / "artifacts/evidence-fixtures/campaign39-heterogeneous-wdi-pearson-batch-1990-2024-https"
METHOD_IDENTITY = "wdi_annual_scalar_pearson_correlation_v1@1.0"
CONTRACT_FP = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
YEARS = list(range(1990, 2025))
MIN_PAIRS = 30
MIN_COVERAGE = Decimal("0.85")
CTX = Context(prec=50, rounding=ROUND_HALF_EVEN)


def canonical_json(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def sha256_value(v: Any) -> str:
    return sha256_bytes(canonical_json(v).encode())


def write_json(path: Path, v: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(v, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def maturity_registry() -> dict[str, Any]:
    registry = load_module(PROJECT_ROOT / "tools/wdi_family_maturity_registry.py", "wdi_family_maturity_registry_campaign39")
    return registry.mature_wdi_family_registry(PROJECT_ROOT)


def batch_scope() -> dict[str, Any]:
    return {
        "campaign_name": "Campaign 39 — Small Heterogeneous WDI Pearson Correlation Batch",
        "expected_package_count_max": 3,
        "method_identity": METHOD_IDENTITY,
        "method_contract_fingerprint": CONTRACT_FP,
        "verified_mature_families": maturity_registry(),
        "period": {"start": 1990, "end": 2024},
        "frequency": "annual",
        "transformation_state": "raw",
        "minimum_aligned_pairs": MIN_PAIRS,
        "minimum_coverage": str(MIN_COVERAGE),
    }


def selection_decision() -> dict[str, Any]:
    selection = read_json(SELECTION_PATH)
    canonical = {k: v for k, v in selection.items() if k not in {"selection_timestamp_noncanonical", "selection_decision_fingerprint"}}
    if sha256_value(canonical) != selection["selection_decision_fingerprint"]:
        raise ValueError("batch-selection fingerprint mismatch")
    if selection["coefficient_calculation_performed_during_selection"] is not False:
        raise ValueError("selection was not coefficient-free")
    if len(selection["selected_pairs"]) != 3:
        raise ValueError("Campaign 39 requires exactly three selected pairs")
    return selection


def acquire_url(url: str) -> dict[str, Any]:
    if not url.startswith("https://"):
        raise ValueError(f"non-HTTPS URL rejected: {url}")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "KnowledgeForge-Campaign39/1.0"}), timeout=120) as response:
        final_url = response.geturl()
        data = response.read()
        headers = dict(response.headers.items())
    if not final_url.startswith("https://"):
        raise ValueError(f"protocol downgrade rejected: {url} -> {final_url}")
    return {"requested_url": url, "final_url": final_url, "headers": headers, "bytes": data, "fingerprint": sha256_bytes(data), "json": json.loads(data.decode())}


def unit_from_metadata(code: str, metadata: dict[str, Any], expected: str) -> dict[str, Any]:
    name = metadata.get("name", "")
    definition = metadata.get("sourceNote", "")
    basis = {"code": code, "name": name, "definition": definition, "provider_unit": metadata.get("unit"), "sourceOrganization": metadata.get("sourceOrganization")}
    basis_fp = sha256_value(basis)
    rules = {
        "SH.IMM.IDPT": ("% of children ages 12-23 months", ["percentage of children", "DPT"]),
        "SH.IMM.MEAS": ("% of children ages 12-23 months", ["percentage of children", "measles"]),
        "SP.DYN.CBRT.IN": ("per 1,000 people", ["per 1,000 population", "birth"]),
        "SP.DYN.CDRT.IN": ("per 1,000 people", ["per 1,000 population", "death"]),
        "IT.NET.USER.ZS": ("% of population", ["Internet users", "individuals"]),
        "IT.CEL.SETS.P2": ("per 100 people", ["per 100 people", "subscriptions"]),
    }
    if code not in rules:
        raise ValueError(f"no fail-closed unit rule for {code}")
    resolved, tokens = rules[code]
    text = name + "\n" + definition
    if resolved != expected or not all(t.lower() in text.lower() for t in tokens):
        raise ValueError(f"unit resolution failed for {code}: expected {expected}")
    result = {"state": "definition-derived unit", "resolved_unit": resolved, "supporting_metadata_fingerprint": basis_fp, "derivation_rule": "Campaign 39 fail-closed authoritative metadata token rule"}
    result["unit_resolution_fingerprint"] = sha256_value(result)
    return result


def acquire_fixture() -> dict[str, Any]:
    selection = selection_decision()
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {"fixture_kind": "Campaign39HeterogeneousBatchWDIFixture", "accessed_at_noncanonical": datetime.now(timezone.utc).isoformat(), "selection_decision_fingerprint": selection["selection_decision_fingerprint"], "pairs": []}
    for pair in selection["selected_pairs"]:
        pair_id = pair["candidate_id"]
        record = {"candidate_id": pair_id, "entity": pair["entity"], "family": pair["family"], "series": {}}
        for role in ["a", "b"]:
            code = pair[f"series_{role}_code"]
            meta_url = f"https://api.worldbank.org/v2/indicator/{code}?format=json&per_page=1"
            obs_url = f"https://api.worldbank.org/v2/country/{pair['entity']}/indicator/{code}?format=json&date=1990:2024&per_page=20000"
            meta = acquire_url(meta_url)
            obs = acquire_url(obs_url)
            (FIXTURE_DIR / f"{pair_id}_series_{role}_metadata_raw.json").write_bytes(meta["bytes"])
            (FIXTURE_DIR / f"{pair_id}_series_{role}_observations_raw.json").write_bytes(obs["bytes"])
            meta_record = meta["json"][1][0]
            if meta_record["id"] != code or meta_record["name"] != pair[f"series_{role}_name"]:
                raise ValueError(f"metadata conflict for {pair_id} {role}")
            record["series"][role] = {"code": code, "expected_unit": pair[f"series_{role}_unit"], "metadata_raw_fingerprint": meta["fingerprint"], "observation_raw_fingerprint": obs["fingerprint"], "metadata_requested_url": meta["requested_url"], "metadata_final_url": meta["final_url"], "observation_requested_url": obs["requested_url"], "observation_final_url": obs["final_url"], "lastupdated": obs["json"][0].get("lastupdated"), "pagination": obs["json"][0], "metadata": meta_record}
        manifest["pairs"].append(record)
    stable_manifest = {k: v for k, v in manifest.items() if k != "accessed_at_noncanonical"}
    stable_manifest["fixture_fingerprint"] = sha256_value(stable_manifest)
    write_json(FIXTURE_DIR / "batch_raw_fixture_manifest.json", stable_manifest)
    return stable_manifest


def parse_decimal(v: Any) -> str:
    text = str(v)
    if "e" in text.lower() or "," in text:
        raise ValueError(f"ambiguous numeric value: {text}")
    dec = Decimal(text)
    if not dec.is_finite():
        raise ValueError(f"non-finite numeric value: {text}")
    return format(dec, "f")


def normalize_pair(pair_record: dict[str, Any]) -> dict[str, Any]:
    pair_id = pair_record["candidate_id"]
    selection_pair = next(p for p in selection_decision()["selected_pairs"] if p["candidate_id"] == pair_id)
    normalized = {"candidate_id": pair_id, "entity": pair_record["entity"], "family": pair_record["family"], "series": {}}
    for role in ["a", "b"]:
        s = pair_record["series"][role]
        obs = json.loads((FIXTURE_DIR / f"{pair_id}_series_{role}_observations_raw.json").read_text())
        unit = unit_from_metadata(s["code"], s["metadata"], s["expected_unit"])
        values: dict[int, Any] = {}
        for row in obs[1]:
            if (row.get("countryiso3code") or row.get("country", {}).get("id")) != pair_record["entity"]:
                continue
            if row.get("indicator", {}).get("id") != s["code"]:
                continue
            year = int(row["date"])
            if year in values:
                raise ValueError(f"duplicate key for {pair_id} {role} {year}")
            if year in YEARS:
                values[year] = row.get("value")
        observations = [{"period": y, "observed": values.get(y) is not None, "value_canonical": parse_decimal(values[y]) if values.get(y) is not None else None, "frequency": "annual", "transformation": "raw", "entity_id": pair_record["entity"], "indicator_code": s["code"], "unit": unit["resolved_unit"], "unit_resolution": unit} for y in YEARS]
        series = {"series_id": {"indicator_code": s["code"], "indicator_name": s["metadata"]["name"], "entity_id": pair_record["entity"], "frequency": "annual", "unit": unit["resolved_unit"], "transformation": "raw"}, "metadata": s["metadata"], "raw_fingerprints": {"metadata": s["metadata_raw_fingerprint"], "observations": s["observation_raw_fingerprint"]}, "provider_metadata": {"provider": "World Bank", "dataset": "World Development Indicators", "source": s["metadata"].get("source", {}).get("value"), "wdi_lastupdated": s["lastupdated"]}, "observations": observations}
        series["normalized_series_fingerprint"] = sha256_value({"series_id": series["series_id"], "observations": observations})
        normalized["series"][role] = series
    write_json(FIXTURE_DIR / f"{pair_id}_normalized_pair.json", normalized)
    return normalized


def align_pair(normalized: dict[str, Any]) -> dict[str, Any]:
    def vals(role: str) -> dict[int, str]:
        out = {r["period"]: r["value_canonical"] for r in normalized["series"][role]["observations"] if r["observed"]}
        if len(set(out.values())) <= 1:
            raise ValueError(f"constant series {normalized['candidate_id']} {role}")
        return out
    va, vb = vals("a"), vals("b")
    aligned_periods = sorted(set(va) & set(vb))
    coverage = Decimal(len(aligned_periods)) / Decimal(len(YEARS))
    if len(aligned_periods) < MIN_PAIRS or coverage < MIN_COVERAGE:
        raise ValueError(f"alignment threshold failure {normalized['candidate_id']}")
    aligned = [{"period": y, "series_a": va[y], "series_b": vb[y]} for y in aligned_periods]
    result = {"candidate_id": normalized["candidate_id"], "entity": normalized["entity"], "family": normalized["family"], "expected_periods": YEARS, "observed_periods": {"series_a": sorted(va), "series_b": sorted(vb)}, "missing_periods": {"series_a": sorted(set(YEARS)-set(va)), "series_b": sorted(set(YEARS)-set(vb))}, "aligned_periods": aligned_periods, "excluded_periods": sorted(set(YEARS)-set(aligned_periods)), "aligned_pair_count": len(aligned_periods), "aligned_coverage": str(coverage), "first_aligned_period": aligned_periods[0], "last_aligned_period": aligned_periods[-1], "aligned_values": aligned}
    result["combined_aligned_evidence_fingerprint"] = sha256_value({"a": normalized["series"]["a"]["normalized_series_fingerprint"], "b": normalized["series"]["b"]["normalized_series_fingerprint"], "aligned_values": aligned})
    return result


def construction_risk(pair: dict[str, Any]) -> dict[str, Any]:
    cid = pair["candidate_id"]
    base = {"algebraic_identity": "not present", "direct_component_total_construction": "not present", "definitional_overlap": "not present", "embedded_series_construction": "not present", "frequency_mismatch": "not present", "transformation_mismatch": "not present", "unit_incompatibility": "not present", "promotion_blocker_present": False}
    if cid == "health_system_coverage":
        base.update({"shared_denominator": "material limitation", "common_modeled_estimation_process": "ordinary limitation", "common_administrative_reporting": "material limitation"})
    elif cid == "demographic_rates":
        base.update({"shared_denominator": "material limitation", "common_modeled_estimation_process": "material limitation", "common_administrative_reporting": "ordinary limitation"})
    else:
        base.update({"shared_denominator": "ordinary limitation", "common_modeled_estimation_process": "ordinary limitation", "common_administrative_reporting": "ordinary limitation"})
    return {"candidate_id": cid, "assessment": base, "promotion_blocker_present": False, "material_limitations": [k for k, v in base.items() if v == "material limitation"], "ordinary_limitations": [k for k, v in base.items() if v == "ordinary limitation"]}


def _corr_series(series: dict[str, Any]) -> dict[str, Any]:
    return {"series_id": series["series_id"], "observations": series["observations"]}


def independent(aligned: list[dict[str, str]], coefficient: str) -> dict[str, Any]:
    xs = [Decimal(r["series_a"]) for r in aligned]
    ys = [Decimal(r["series_b"]) for r in aligned]
    with localcontext(CTX):
        n = Decimal(len(xs)); mx = sum(xs, Decimal(0)) / n; my = sum(ys, Decimal(0)) / n
        num = sum((x-mx)*(y-my) for x, y in zip(xs, ys)); vx = sum((x-mx)*(x-mx) for x in xs); vy = sum((y-my)*(y-my) for y in ys)
        den = (vx*vy).sqrt(context=CTX); raw = num/den; can = raw.quantize(Decimal("0.000000000001"))
    text = format(can, "f").rstrip("0").rstrip(".")
    if text == "-0": text = "0"
    return {"matches": text == coefficient, "canonical": text, "mean_a": format(mx,"f"), "mean_b": format(my,"f"), "centered_cross_product_sum": format(num,"f"), "sum_of_squares_a": format(vx,"f"), "sum_of_squares_b": format(vy,"f"), "denominator": format(den,"f")}


def diagnostics(normalized: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "corr39diag")
    def mk(code: str, unit: str, vals: list[str], transform: str = "raw") -> dict[str, Any]:
        periods = [r["period"] for r in alignment["aligned_values"]][-len(vals):]
        return {"series_id": {"indicator_code": code, "entity_id": normalized["entity"], "frequency": "annual", "unit": unit, "transformation": transform}, "observations": [{"period": p, "observed": True, "value_canonical": v} for p, v in zip(periods, vals)]}
    a_vals = [r["series_a"] for r in alignment["aligned_values"]]; b_vals = [r["series_b"] for r in alignment["aligned_values"]]; t = [str(i) for i in range(1, len(a_vals)+1)]
    a = normalized["series"]["a"]["series_id"]; b = normalized["series"]["b"]["series_id"]
    a_time = corr.compute_correlation(mk(a["indicator_code"], a["unit"], a_vals), mk("CANONICAL_ANNUAL_TIME_INDEX", "index", t), minimum_aligned_pairs=30, coverage_threshold=Decimal("0"), same_entity_required=True)
    b_time = corr.compute_correlation(mk(b["indicator_code"], b["unit"], b_vals), mk("CANONICAL_ANNUAL_TIME_INDEX", "index", t), minimum_aligned_pairs=30, coverage_threshold=Decimal("0"), same_entity_required=True)
    a_diff = [format(Decimal(a_vals[i])-Decimal(a_vals[i-1]), "f") for i in range(1, len(a_vals))]
    b_diff = [format(Decimal(b_vals[i])-Decimal(b_vals[i-1]), "f") for i in range(1, len(b_vals))]
    diff = corr.compute_correlation(mk(a["indicator_code"], a["unit"]+" delta", a_diff, "first_difference"), mk(b["indicator_code"], b["unit"]+" delta", b_diff, "first_difference"), minimum_aligned_pairs=29, coverage_threshold=Decimal("0"))
    return {"candidate_id": normalized["candidate_id"], "series_a_vs_time_index_coefficient": a_time["coefficient"]["canonical"], "series_b_vs_time_index_coefficient": b_time["coefficient"]["canonical"], "first_difference_sensitivity_coefficient": diff["coefficient"]["canonical"], "status": "diagnostic_only_not_promoted", "limitations": ["transformation sensitivity", "common time-ordering risk", "autocorrelation limitation", "structural-break limitation", "measurement-methodology limitation", "non-causality", "non-prediction", "absence of significance testing"]}


def calculate(normalized: dict[str, Any], alignment: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "corr39")
    contract = corr.calculation_contract_v1()
    if contract["calculation_contract_fingerprint"] != CONTRACT_FP:
        raise ValueError("contract fingerprint mismatch")
    result = corr.compute_correlation(_corr_series(normalized["series"]["a"]), _corr_series(normalized["series"]["b"]), minimum_aligned_pairs=MIN_PAIRS, coverage_threshold=MIN_COVERAGE)
    swapped = corr.compute_correlation(_corr_series(normalized["series"]["b"]), _corr_series(normalized["series"]["a"]), minimum_aligned_pairs=MIN_PAIRS, coverage_threshold=MIN_COVERAGE)
    if result["coefficient"] != swapped["coefficient"] or result["canonical_pair_id"] != swapped["canonical_pair_id"]:
        raise ValueError("pair-order invariance failed")
    coef = result["coefficient"]["canonical"]
    if not (Decimal("-1") <= Decimal(coef) <= Decimal("1")):
        raise ValueError("coefficient bounds failed")
    ind = independent(alignment["aligned_values"], coef)
    if not ind["matches"]:
        raise ValueError("independent recomputation mismatch")
    calc = {"candidate_id": normalized["candidate_id"], "method_result": result, "swapped_pair_result_fingerprint": swapped["output_fingerprint"], "independent_recompute": ind, "calculation_evidence": {"aligned_values": alignment["aligned_values"], "means": {"series_a": ind["mean_a"], "series_b": ind["mean_b"]}, "centered_cross_product_sum": ind["centered_cross_product_sum"], "sum_of_squares": {"series_a": ind["sum_of_squares_a"], "series_b": ind["sum_of_squares_b"]}, "denominator": ind["denominator"], "canonical_coefficient": coef, "method_contract_fingerprint": CONTRACT_FP}}
    calc["calculation_evidence_fingerprint"] = sha256_value(calc["calculation_evidence"])
    return calc


def package_id(candidate_id: str) -> str:
    return f"pkg-object-srcpkg-campaign39-{candidate_id.replace('_','-')}-pearson-correlation-v1"


def build_package(selection: dict[str, Any], normalized: dict[str, Any], alignment: dict[str, Any], risk: dict[str, Any], calc: dict[str, Any], diag: dict[str, Any]) -> dict[str, Any]:
    cid = normalized["candidate_id"]; sp = next(p for p in selection["selected_pairs"] if p["candidate_id"] == cid); coef = calc["method_result"]["coefficient"]["canonical"]
    pid = package_id(cid); stmt_id = f"stmt-campaign39-{cid.replace('_','-')}-pearson-v1"
    payload = {"family": sp["family"], "series_a": {"code": sp["series_a_code"], "name": sp["series_a_name"], "definition": sp["series_a_definition"], "unit": sp["series_a_unit"], "fingerprints": normalized["series"]["a"]["raw_fingerprints"]}, "series_b": {"code": sp["series_b_code"], "name": sp["series_b_name"], "definition": sp["series_b_definition"], "unit": sp["series_b_unit"], "fingerprints": normalized["series"]["b"]["raw_fingerprints"]}, "entity_id": sp["entity"], "period_scope": sp["period"], "frequency": "annual", "transformation_state": "raw", "aligned_pair_count": alignment["aligned_pair_count"], "aligned_coverage": alignment["aligned_coverage"], "missing_periods": alignment["missing_periods"], "excluded_periods": alignment["excluded_periods"], "pearson_coefficient": {"canonical": coef, "unit": "dimensionless"}, "method_contract_fingerprint": CONTRACT_FP, "frozen_batch_selection_fingerprint": selection["selection_decision_fingerprint"], "combined_aligned_evidence_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "calculation_evidence_fingerprint": calc["calculation_evidence_fingerprint"], "construction_risk_assessment": risk, "diagnostic_limitations": diag["limitations"], "mutable_source_limitation": "Retained bytes, not mutable WDI API reacquisition, provide exact historical reproducibility.", "validation_judgment": "accepted_campaign39_batch_correlation_object"}
    stmt = {"statement_id": stmt_id, "statement_type": "derived_relationship", "text": f"Across the aligned annual {sp['entity']} observations from 1990 through 2024, the Pearson correlation between {sp['series_a_name']} and {sp['series_b_name']} is {coef}, using {alignment['aligned_pair_count']} aligned observations.", "origin": "computed_from_retained_campaign39_frozen_selection_wdi_fixture", "evidence_refs": [f"ev-campaign39-{cid}-fixture"], "dependencies": [f"calc-campaign39-{cid}-pearson-v1"], "applicability": {"entity_id": sp["entity"], "period_start": 1990, "period_end": 2024, "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0"}, "structured_payload": payload}
    pkg = {"package_kind": "KnowledgeObjectPackage", "package_id": pid, "package_version": "1.0", "status": "accepted", "created_at": "2026-07-11", "created_by": "run_campaign39_heterogeneous_correlation_batch", "scope": {"domain": "world_development_indicators", "evidence_family": f"external_wdi_annual_scalar_{sp['family'].lower().replace(' & ', '_').replace(' ', '_')}_pearson_correlation", "entity_scope": [sp["entity"]], "period_scope": sp["period"]}, "input_references": ["campaign39_frozen_batch_selection_decision", "campaign39_batch_wdi_https_fixture", "pearson_correlation_calculation_contract_v1"], "evidence_references": [{"evidence_ref_id": f"ev-campaign39-{cid}-fixture", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": f"World Bank WDI {sp['series_a_code']} and {sp['series_b_code']} {sp['entity']} annual 1990-2024 fixture", "source_version": normalized["series"]["a"]["provider_metadata"].get("wdi_lastupdated"), "snapshot_fingerprint": alignment["combined_aligned_evidence_fingerprint"], "reproducibility_handle": "retained HTTPS raw fixture, frozen batch selection, normalized series, alignment and calculation evidence", "evaluation_status": "evaluated", "accessed_at": "2026-07-11"}], "generated_statements": [stmt], "confidence_quality": {"confidence_label": "fixture-supported-deterministic", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation batch object", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture", "uncertainty_dimensions": diag["limitations"]}, "validation_state": {"validation_result": "pass", "blockers": [], "warnings": risk["material_limitations"] + risk["ordinary_limitations"] + ["no causal/predictive/significance interpretation"]}, "provenance_envelope": {"evidence_refs": [f"ev-campaign39-{cid}-fixture"], "evaluation_refs": ["campaign39_frozen_batch_selection_decision", f"campaign39_{cid}_alignment", f"campaign39_{cid}_calculation", f"campaign39_{cid}_diagnostics"], "method_refs": [METHOD_IDENTITY], "lineage_basis": "frozen coefficient-free batch selection followed by Campaign 39 HTTPS acquisition"}, "lineage": {"previous_package_id": None, "version_lineage": [], "source_campaign": "Campaign 39"}, "evolution_metadata": {"change_reason": "Campaign 39 heterogeneous correlation batch", "changed_inputs_methods_templates_models_validators": [], "previous_revision": None, "dependent_object_review_posture": "not_applicable"}, "contradiction_records": [{"contradiction_id": "none-recorded", "contradiction_type": "none", "target_statement": stmt_id, "contradicting_evidence": None, "disposition": "not_applicable"}], "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": alignment["combined_aligned_evidence_fingerprint"]}}
    pkg["fingerprints"] = {"input_set": sha256_value({"selection": selection["selection_decision_fingerprint"], "alignment": alignment["combined_aligned_evidence_fingerprint"]}), "evidence_references": sha256_value(pkg["evidence_references"]), "generated_statements": sha256_value(pkg["generated_statements"]), "computation_recipe": sha256_value({"method": METHOD_IDENTITY, "contract": CONTRACT_FP}), "query_definitions": sha256_value([])}
    pkg["fingerprints"]["package_manifest"] = sha256_value({k: v for k, v in pkg.items() if k != "fingerprints"})
    pkg["generated_statements"][0]["structured_payload"]["package_fingerprint"] = pkg["fingerprints"]["package_manifest"]
    pkg["fingerprints"]["generated_statements"] = sha256_value(pkg["generated_statements"])
    pkg["fingerprints"]["package_manifest"] = sha256_value({k: v for k, v in pkg.items() if k != "fingerprints"})
    return pkg


def repository_snapshot() -> dict[str, Any]:
    files = sorted((REPOSITORY_ROOT / "objects").glob("*.json")); manifest = read_json(REPOSITORY_ROOT / "manifest.json")
    return {"object_count": len(files), "manifest_object_count": manifest["object_count"], "repository_fingerprint": manifest["repository_fingerprint"], "package_hashes": {f.name: sha256_bytes(f.read_bytes()) for f in files}}


def promote(packages: list[dict[str, Any]], before: dict[str, Any]) -> dict[str, Any]:
    kr = load_module(PROJECT_ROOT / "tools/knowledge_repository.py", "knowledge_repository_campaign39")
    persist = kr.persist_knowledge_object_packages(packages, REPOSITORY_ROOT)
    after = repository_snapshot(); before_hashes = before["package_hashes"]; after_hashes = after["package_hashes"]
    changed = [n for n, fp in before_hashes.items() if after_hashes.get(n) != fp]; disappeared = [n for n in before_hashes if n not in after_hashes]; added = [n for n in after_hashes if n not in before_hashes]
    expected = sorted([p["package_id"] + ".json" for p in packages])
    imm = {"valid": changed == [] and disappeared == [] and sorted(added) == expected, "changed_existing": changed, "disappeared_existing": disappeared, "added": sorted(added), "expected_added": expected}
    if not imm["valid"] and not (added == [] and changed == [] and disappeared == []):
        raise ValueError(f"immutability failed {imm}")
    return {"persist_result": persist, "before": before, "after": after, "immutability": imm}


def run(reuse_fixture: bool = False, no_promote: bool = False) -> dict[str, Any]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True); FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    selection = selection_decision(); before = repository_snapshot()
    fixture = read_json(FIXTURE_DIR / "batch_raw_fixture_manifest.json") if reuse_fixture and (FIXTURE_DIR / "batch_raw_fixture_manifest.json").exists() else acquire_fixture()
    normalized = [normalize_pair(p) for p in fixture["pairs"]]
    alignments = [align_pair(n) for n in normalized]
    write_json(FIXTURE_DIR / "batch_alignment_results.json", alignments)
    risks = [construction_risk(n) for n in normalized]
    calculations = [calculate(n, a) for n, a in zip(normalized, alignments)]
    diagnostics_results = [diagnostics(n, a) for n, a in zip(normalized, alignments)]
    packages = [build_package(selection, n, a, r, c, d) for n, a, r, c, d in zip(normalized, alignments, risks, calculations, diagnostics_results)]
    write_json(REPORT_DIR / "batch_calculation_evidence.json", calculations)
    write_json(REPORT_DIR / "batch_construction_risk_assessment.json", risks)
    write_json(REPORT_DIR / "batch_non_promoted_diagnostics.json", diagnostics_results)
    write_json(REPORT_DIR / "candidate_packages.json", packages)
    if no_promote:
        result = {"outcome": "rerun_no_promote", "accepted_package_ids": [p["package_id"] for p in packages], "coefficients": {p["package_id"]: p["generated_statements"][0]["structured_payload"]["pearson_coefficient"]["canonical"] for p in packages}, "repository_after": {k: v for k, v in before.items() if k != "package_hashes"}}
        write_json(REPORT_DIR / "campaign39_no_promote_rerun_result.json", result)
        return result
    repo = promote(packages, before)
    write_json(REPORT_DIR / "repository_promotion_result.json", {"persist_result": repo["persist_result"], "before": {k:v for k,v in before.items() if k != "package_hashes"}, "after": {k:v for k,v in repo["after"].items() if k != "package_hashes"}, "immutability": repo["immutability"]})
    result = {"outcome": "A", "accepted_package_ids": [p["package_id"] for p in packages], "coefficients": {p["package_id"]: p["generated_statements"][0]["structured_payload"]["pearson_coefficient"]["canonical"] for p in packages}, "package_fingerprints": {p["package_id"]: p["fingerprints"]["package_manifest"] for p in packages}, "repository_after": {k: v for k, v in repo["after"].items() if k != "package_hashes"}}
    write_json(REPORT_DIR / "campaign39_result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--reuse-fixture", action="store_true"); parser.add_argument("--no-promote", action="store_true")
    args = parser.parse_args(); print(json.dumps(run(args.reuse_fixture, args.no_promote), indent=2, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
