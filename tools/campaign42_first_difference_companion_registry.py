#!/usr/bin/env python3
"""Campaign 42 coefficient-free first-difference Pearson companion registry.

This helper freezes selection metadata only. It enumerates canonical raw Pearson
packages and retained evidence fixtures, validates first-difference method
compatibility using period availability/units/fingerprints, and emits a
deterministic coefficient-free companion-production registry.

It must not calculate first differences or Pearson coefficients.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

TRANSFORMATION_ID = "wdi_annual_scalar_first_difference_v1"
TRANSFORMATION_VERSION = "1.0"
TRANSFORMATION_FINGERPRINT = "sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f"
METHOD_ID = "wdi_annual_scalar_first_difference_pearson_v1"
METHOD_VERSION = "1.0"
METHOD_FINGERPRINT = "sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade"
VALIDATION_REGISTRY_FINGERPRINT = "sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657"
RAW_METHOD_ID = "wdi_annual_scalar_pearson_correlation_v1"
MIN_TRANSFORMED_OBSERVATIONS = 30
MIN_TRANSFORMED_COVERAGE = 0.85

FORBIDDEN_REGISTRY_TERMS = [
    "pearson_coefficient",
    "diagnostic_limitations.first_difference_pearson",
    "diagnostic_value",
    "p_value",
    "covariance",
    "significance",
    "forecast",
]

SEMANTIC_OVERRIDES = {
    ("NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"): ("close", "national-account external trade flow shares"),
    ("SP.DYN.CBRT.IN", "SP.DYN.CDRT.IN"): ("close", "demographic vital-rate pair"),
    ("IT.NET.USER.ZS", "IT.CEL.SETS.P2"): ("close", "digital access/infrastructure pair"),
    ("AG.LND.AGRI.ZS", "AG.LND.FRST.ZS"): ("close", "land-use share pair"),
    ("EG.ELC.FOSL.ZS", "EG.ELC.RNWX.ZS"): ("close", "electricity-generation share pair"),
    ("FS.AST.PRVT.GD.ZS", "FM.LBL.BMNY.GD.ZS"): ("close", "financial-depth percent-of-GDP pair"),
    ("SP.DYN.LE00.IN", "SH.DYN.MORT"): ("close", "health outcome pair"),
    ("FS.AST.PRVT.GD.ZS", "IT.NET.USER.ZS"): ("moderate", "financial-depth and digital-adoption modernization pair"),
    ("FS.AST.PRVT.GD.ZS", "IT.CEL.SETS.P2"): ("moderate", "financial-depth and mobile-access modernization pair"),
}

FAMILY_FALLBACKS = {
    "AG.LND.AGRI.ZS": "Agriculture & Rural Development",
    "AG.LND.FRST.ZS": "Agriculture & Rural Development",
    "EG.ELC.FOSL.ZS": "Energy & Mining",
    "EG.ELC.RNWX.ZS": "Energy & Mining",
    "FM.LBL.BMNY.GD.ZS": "Financial Sector",
    "FS.AST.PRVT.GD.ZS": "Financial Sector",
    "IT.CEL.SETS.P2": "Infrastructure",
    "IT.NET.USER.ZS": "Infrastructure",
    "NE.EXP.GNFS.ZS": "Trade",
    "NE.IMP.GNFS.ZS": "Trade",
    "SH.DYN.MORT": "Health",
    "SP.DYN.CBRT.IN": "Demographic",
    "SP.DYN.CDRT.IN": "Demographic",
    "SP.DYN.LE00.IN": "Health",
}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def package_payload(package: dict[str, Any]) -> dict[str, Any]:
    return package.get("generated_statements", [{}])[0].get("structured_payload", {})


def package_applicability(package: dict[str, Any]) -> dict[str, Any]:
    return package.get("generated_statements", [{}])[0].get("applicability", {})


def is_raw_pearson_package(package: dict[str, Any]) -> bool:
    payload = package_payload(package)
    applicability = package_applicability(package)
    has_method = payload.get("method_id") == RAW_METHOD_ID or applicability.get("method_id") == RAW_METHOD_ID
    has_raw_coeff = "pearson_coefficient" in payload
    return bool(has_method and has_raw_coeff)


def package_fingerprint(package: dict[str, Any]) -> str:
    payload = package_payload(package)
    return payload.get("package_fingerprint") or package.get("fingerprints", {}).get("package_manifest") or fingerprint(package)


def campaign_order(package_id: str) -> int:
    m = re.search(r"campaign(\d+)", package_id)
    return int(m.group(1)) if m else 999


def pair_key(code_a: str, code_b: str) -> tuple[str, str]:
    return tuple(sorted([code_a, code_b]))  # type: ignore[return-value]


def semantic_classification(code_a: str, code_b: str, family: str | None) -> tuple[str, str]:
    key = pair_key(code_a, code_b)
    if key in SEMANTIC_OVERRIDES:
        return SEMANTIC_OVERRIDES[key]
    fam_a = FAMILY_FALLBACKS.get(code_a)
    fam_b = FAMILY_FALLBACKS.get(code_b)
    if fam_a and fam_b and fam_a == fam_b:
        return "close", f"same WDI family: {fam_a}"
    if family and " x " not in family:
        return "close", f"same package family: {family}"
    return "remote", "cross-family cautionary companion case"


def transformed_unit(unit: str) -> str:
    normalized = unit.strip().lower()
    if not normalized:
        raise ValueError("unresolved unit")
    if "growth" in normalized or "percent change" in normalized or "annual %" in normalized:
        raise ValueError(f"unit not unambiguously absolute-difference transformable: {unit}")
    if "% of gdp" in normalized or "percent of gdp" in normalized:
        return "year-to-year change in percentage points of GDP"
    if normalized.startswith("% of") or "percent of" in normalized:
        return f"year-to-year percentage-point change in {unit}"
    if "per 1,000" in normalized or "per 100" in normalized:
        return f"absolute year-to-year change in {unit}"
    if "current" in normalized or "$" in normalized or "currency" in normalized:
        return f"year-to-year change in {unit}"
    return f"absolute year-to-year change in {unit}"


def find_fixture(root: Path, entity: str, indicator_code: str) -> dict[str, Any] | None:
    candidates: list[Path] = []
    fixtures_root = root / "artifacts" / "evidence-fixtures"
    if fixtures_root.exists():
        for p in fixtures_root.glob("**/normalized_observations.json"):
            try:
                data = load_json(p)
            except Exception:
                continue
            obs = data.get("observations") or []
            if not obs:
                continue
            if any(o.get("entity_id") == entity and o.get("indicator_code") == indicator_code for o in obs):
                candidates.append(p)
    if not candidates:
        return None
    # Prefer the retained Campaign 40 fixture pool for Campaign 42 compatibility; otherwise deterministic path order.
    candidates = sorted(candidates, key=lambda p: ("campaign40-spec-driven-pearson-production" not in str(p), str(p)))
    path = candidates[0]
    data = load_json(path)
    obs = [o for o in data.get("observations", []) if o.get("entity_id") == entity and o.get("indicator_code") == indicator_code]
    periods = sorted(int(o["period"]) for o in obs if o.get("observed") is True and o.get("value_canonical") not in (None, ""))
    unit = next((o.get("unit") for o in obs if o.get("unit")), "")
    return {
        "path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path),
        "normalized_fingerprint": data.get("normalized_fingerprint"),
        "source_raw_fixture_fingerprint": data.get("source_raw_fixture_fingerprint"),
        "selection_fingerprint": data.get("selection_fingerprint"),
        "observed_periods": periods,
        "unit": unit,
        "indicator_name": obs[0].get("indicator_name") if obs else indicator_code,
        "observed_count": len(periods),
    }


def expected_transformed_periods(periods_a: list[int], periods_b: list[int]) -> list[int]:
    set_a, set_b = set(periods_a), set(periods_b)
    raw_start = max(min(set_a), min(set_b)) if set_a and set_b else 0
    raw_end = min(max(set_a), max(set_b)) if set_a and set_b else -1
    out = []
    for year in range(raw_start + 1, raw_end + 1):
        if year in set_a and year - 1 in set_a and year in set_b and year - 1 in set_b:
            out.append(year)
    return out


def existing_companion_package_ids(root: Path) -> set[str]:
    out = set()
    for p in (root / "knowledge_repository" / "objects").glob("*.json"):
        package = load_json(p)
        payload = package_payload(package)
        app = package_applicability(package)
        if payload.get("method_id") == METHOD_ID or app.get("method_id") == METHOD_ID:
            out.add(package.get("package_id", p.stem))
    return out


def enumerate_raw_pearson_packages(root: Path) -> list[dict[str, Any]]:
    objects = []
    for p in (root / "knowledge_repository" / "objects").glob("*.json"):
        package = load_json(p)
        if not is_raw_pearson_package(package):
            continue
        payload = package_payload(package)
        app = package_applicability(package)
        series_a = payload.get("series_a", {})
        series_b = payload.get("series_b", {})
        entity = payload.get("entity_id") or app.get("entity_id") or (package.get("scope", {}).get("entity_scope") or [None])[0]
        diag = payload.get("diagnostic_limitations")
        has_modern_diagnostic = isinstance(diag, dict) and "first_difference_pearson" in diag
        sem, sem_reason = semantic_classification(series_a.get("code"), series_b.get("code"), payload.get("family"))
        objects.append({
            "raw_package_id": package["package_id"],
            "raw_package_path": str(p),
            "raw_package_fingerprint": package_fingerprint(package),
            "campaign_order": campaign_order(package["package_id"]),
            "entity": entity,
            "indicator_a": {"code": series_a.get("code"), "name": series_a.get("name"), "unit": series_a.get("unit"), "transformation": series_a.get("transformation", "raw")},
            "indicator_b": {"code": series_b.get("code"), "name": series_b.get("name"), "unit": series_b.get("unit"), "transformation": series_b.get("transformation", "raw")},
            "family": payload.get("family") or " x ".join(sorted({FAMILY_FALLBACKS.get(series_a.get("code"), "unknown"), FAMILY_FALLBACKS.get(series_b.get("code"), "unknown")})),
            "raw_period_scope": payload.get("period_scope") or {"start": app.get("period_start"), "end": app.get("period_end")},
            "raw_aligned_pair_count": payload.get("aligned_pair_count"),
            "raw_aligned_coverage_present": payload.get("aligned_coverage") is not None,
            "semantic_proximity": sem,
            "semantic_proximity_reason": sem_reason,
            "embedded_first_difference_diagnostic_present": has_modern_diagnostic,
            "embedded_time_index_diagnostics_present": isinstance(diag, dict) and "series_a_vs_time_index" in diag and "series_b_vs_time_index" in diag,
        })
    return sorted(objects, key=lambda o: (o["campaign_order"], o["entity"] or "", o["raw_package_id"]))


def enrich_eligibility(root: Path, raw: dict[str, Any], companions: set[str]) -> dict[str, Any]:
    item = copy.deepcopy(raw)
    entity = item["entity"]
    fa = find_fixture(root, entity, item["indicator_a"]["code"])
    fb = find_fixture(root, entity, item["indicator_b"]["code"])
    reasons = []
    eligible = True
    if not fa or not fb:
        eligible = False
        reasons.append("retained_raw_evidence_fixture_missing")
    if fa and fb:
        transformed_periods = expected_transformed_periods(fa["observed_periods"], fb["observed_periods"])
        raw_scope = item["raw_period_scope"]
        raw_start, raw_end = int(raw_scope["start"]), int(raw_scope["end"])
        max_possible = raw_end - raw_start
        coverage = len(transformed_periods) / max_possible if max_possible > 0 else 0
        if len(transformed_periods) < MIN_TRANSFORMED_OBSERVATIONS:
            eligible = False
            reasons.append("insufficient_expected_transformed_overlap")
        if coverage < MIN_TRANSFORMED_COVERAGE:
            eligible = False
            reasons.append("insufficient_expected_transformed_coverage")
        try:
            unit_a = transformed_unit(item["indicator_a"].get("unit") or fa.get("unit") or "")
            unit_b = transformed_unit(item["indicator_b"].get("unit") or fb.get("unit") or "")
        except ValueError as exc:
            eligible = False
            reasons.append(f"unit_not_transformable:{exc}")
            unit_a = unit_b = None
        item.update({
            "evidence_fixtures": {
                "series_a": {"identity": f"{item['indicator_a']['code']}__{entity}__{raw_start}-{raw_end}", "path": fa["path"], "normalized_fingerprint": fa["normalized_fingerprint"], "source_raw_fixture_fingerprint": fa["source_raw_fixture_fingerprint"], "selection_fingerprint": fa["selection_fingerprint"]},
                "series_b": {"identity": f"{item['indicator_b']['code']}__{entity}__{raw_start}-{raw_end}", "path": fb["path"], "normalized_fingerprint": fb["normalized_fingerprint"], "source_raw_fixture_fingerprint": fb["source_raw_fixture_fingerprint"], "selection_fingerprint": fb["selection_fingerprint"]},
            },
            "expected_transformed_period_scope": {"start": transformed_periods[0] if transformed_periods else None, "end": transformed_periods[-1] if transformed_periods else None},
            "expected_transformed_observation_count": len(transformed_periods),
            "expected_transformed_coverage": format(coverage, ".12f").rstrip("0").rstrip("."),
            "transformed_unit_semantics": {"series_a": unit_a, "series_b": unit_b},
        })
    else:
        item.update({"evidence_fixtures": {}, "expected_transformed_period_scope": None, "expected_transformed_observation_count": 0, "expected_transformed_coverage": "0", "transformed_unit_semantics": {}})
    expected_id = expected_companion_package_id(item["raw_package_id"])
    if expected_id in companions:
        eligible = False
        reasons.append("existing_canonical_first_difference_companion")
    item["expected_companion_package_id"] = expected_id
    item["existing_canonical_first_difference_companion_found"] = expected_id in companions
    item["eligible"] = eligible
    item["eligibility_reasons"] = [] if eligible else reasons
    return item


def expected_companion_package_id(raw_package_id: str) -> str:
    prefix = raw_package_id.removesuffix("-pearson-correlation-v1")
    return f"{prefix}-first-difference-pearson-companion-v1"


def selected_candidates(eligible: list[dict[str, Any]], count: int = 8) -> list[dict[str, Any]]:
    sem_priority = {"close": 0, "moderate": 1, "remote": 2}
    def key(x: dict[str, Any]) -> tuple[Any, ...]:
        diagnostic_gap_priority = 0 if not x["embedded_first_difference_diagnostic_present"] else 1
        return (sem_priority.get(x["semantic_proximity"], 9), diagnostic_gap_priority, x["campaign_order"], x["entity"], x["raw_package_id"])
    ordered = sorted(eligible, key=key)
    chosen: list[dict[str, Any]] = []
    remote_count = 0
    for item in ordered:
        if item["semantic_proximity"] == "remote" and remote_count >= 2:
            continue
        chosen.append(item)
        if item["semantic_proximity"] == "remote":
            remote_count += 1
        if len(chosen) == count:
            break
    return chosen


def candidate_id(n: int) -> str:
    return f"campaign42-fd-pearson-companion-candidate-{n:02d}"


def registry_entry(n: int, item: dict[str, Any]) -> dict[str, Any]:
    return {
        "campaign42_candidate_id": candidate_id(n),
        "expected_companion_package_id": item["expected_companion_package_id"],
        "raw_companion_package_id": item["raw_package_id"],
        "raw_package_fingerprint": item["raw_package_fingerprint"],
        "entity": item["entity"],
        "indicator_a": item["indicator_a"],
        "indicator_b": item["indicator_b"],
        "evidence_fixtures": item["evidence_fixtures"],
        "raw_period_scope": item["raw_period_scope"],
        "expected_transformed_period_scope": item["expected_transformed_period_scope"],
        "transformation": {"id": TRANSFORMATION_ID, "version": TRANSFORMATION_VERSION, "contract_fingerprint": TRANSFORMATION_FINGERPRINT},
        "method": {"id": METHOD_ID, "version": METHOD_VERSION, "contract_fingerprint": METHOD_FINGERPRINT, "validation_registry_fingerprint": VALIDATION_REGISTRY_FINGERPRINT},
        "raw_units": {"series_a": item["indicator_a"].get("unit"), "series_b": item["indicator_b"].get("unit")},
        "transformed_unit_semantics": item["transformed_unit_semantics"],
        "expected_minimum_overlap": {"required_aligned_transformed_observations": MIN_TRANSFORMED_OBSERVATIONS, "expected_aligned_transformed_observations": item["expected_transformed_observation_count"]},
        "expected_minimum_coverage": {"required_transformed_coverage": "0.85", "expected_transformed_coverage": item["expected_transformed_coverage"]},
        "semantic_proximity": item["semantic_proximity"],
        "semantic_proximity_reason": item["semantic_proximity_reason"],
        "companion_production_justification": "Create independently retrievable annual-change co-movement knowledge for an existing raw-level Pearson relationship without mutating or superseding the raw package.",
        "expected_consumer_use": "Compare raw level co-movement with annual-change co-movement and retrieve transformation-aware limitations/provenance independently.",
        "limitations": [
            "first differencing does not prove stationarity",
            "correlation is not causation",
            "no inferential acceptance claim is implied",
            "no forward-looking signal is implied",
            "results remain finite-window dependent",
            "differencing can amplify noise",
            "companion does not supersede the raw package",
        ],
        "deterministic_selection_provenance": {
            "allowed_metadata_used": ["canonical raw package id", "entity", "indicator identities", "package campaign/order", "semantic proximity class", "diagnostic metadata presence flag", "fixture paths/fingerprints", "units", "period availability counts"],
            "disallowed_values_not_used": ["raw Pearson magnitude", "first-difference diagnostic magnitude", "sign", "p-value", "inferential acceptance claim", "forward-looking result", "consumer result surprise"],
            "embedded_first_difference_diagnostic_present": item["embedded_first_difference_diagnostic_present"],
            "embedded_time_index_diagnostics_present": item["embedded_time_index_diagnostics_present"],
        },
        "existing_canonical_first_difference_companion_found": item["existing_canonical_first_difference_companion_found"],
    }


def strip_diagnostic_values_for_proof(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: ("<diagnostic-value-ignored>" if k in {"first_difference_pearson", "series_a_vs_time_index", "series_b_vs_time_index"} else strip_diagnostic_values_for_proof(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_diagnostic_values_for_proof(v) for v in obj]
    return obj


def build_campaign42_registry(root: Path) -> dict[str, Any]:
    raw_inventory = enumerate_raw_pearson_packages(root)
    companions = existing_companion_package_ids(root)
    eligibility = [enrich_eligibility(root, p, companions) for p in raw_inventory]
    eligible = [e for e in eligibility if e["eligible"]]
    chosen = selected_candidates(eligible, 8)
    entries = [registry_entry(i + 1, e) for i, e in enumerate(chosen)]
    registry = {
        "registry_id": "campaign42_coefficient_free_first_difference_pearson_companion_registry",
        "registry_version": "1.0",
        "campaign": "Campaign 42",
        "purpose": "Freeze 6-8 existing raw Pearson packages for later first-difference Pearson companion production.",
        "coefficient_free": True,
        "production_authorized": False,
        "selection_policy": {
            "priority_order": ["semantic proximity", "diagnostic coverage gap", "raw package campaign/order", "entity", "canonical raw package id"],
            "stored_diagnostic_policy": "stored diagnostic coefficient fields are inventoried only for post-freeze audit and are not read, compared, thresholded, ranked, or branched on",
            "maximum_remote_candidates": 2,
            "target_candidate_count": "6-8, selecting 8 if compatibility allows",
        },
        "accepted_method_contracts": {
            "transformation_id": TRANSFORMATION_ID,
            "transformation_version": TRANSFORMATION_VERSION,
            "transformation_contract_fingerprint": TRANSFORMATION_FINGERPRINT,
            "method_id": METHOD_ID,
            "method_version": METHOD_VERSION,
            "method_contract_fingerprint": METHOD_FINGERPRINT,
            "validation_registry_fingerprint": VALIDATION_REGISTRY_FINGERPRINT,
        },
        "candidates": entries,
    }
    serialized = canonical_json(registry).lower()
    for term in FORBIDDEN_REGISTRY_TERMS:
        if term in serialized:
            raise ValueError(f"forbidden coefficient/result field in registry: {term}")
    reg_fp = fingerprint(registry)
    spec = {
        "specification_id": "campaign42_first_difference_pearson_companion_production_spec",
        "specification_version": "1.0",
        "registry_fingerprint": reg_fp,
        "method_contracts": registry["accepted_method_contracts"],
        "production_boundary": "declarative frozen selection only; coefficient calculation and canonical publication require separate authorization",
        "candidate_ids": [e["campaign42_candidate_id"] for e in entries],
        "expected_companion_package_ids": [e["expected_companion_package_id"] for e in entries],
        "raw_to_companion_links": [{"raw_package_id": e["raw_companion_package_id"], "expected_companion_package_id": e["expected_companion_package_id"]} for e in entries],
        "execution_requirements_before_future_production": ["verify registry fingerprint", "verify raw package fingerprints", "verify retained evidence fixture fingerprints", "calculate only after separate authorization"],
    }
    spec_fp = fingerprint(spec)
    return {
        "inventory": raw_inventory,
        "eligibility_inventory": eligibility,
        "eligible_count": len(eligible),
        "ineligible_count": len(eligibility) - len(eligible),
        "registry": registry,
        "registry_fingerprint": reg_fp,
        "specification": spec,
        "specification_fingerprint": spec_fp,
        "expected_package_id_manifest": {e["campaign42_candidate_id"]: e["expected_companion_package_id"] for e in entries},
        "raw_to_companion_link_manifest": spec["raw_to_companion_links"],
        "diagnostic_honesty_audit": {
            "values_technically_available_before_selection": True,
            "value_fields_excluded_from_registry": ["diagnostic_limitations.first_difference_pearson", "diagnostic_limitations.series_a_vs_time_index", "diagnostic_limitations.series_b_vs_time_index", "pearson_coefficient.canonical"],
            "used_fields": registry["selection_policy"]["priority_order"] + ["fixture existence", "unit transformability", "expected transformed overlap/coverage"],
            "selected_candidates_with_embedded_first_difference_diagnostic": [e["raw_companion_package_id"] for e in entries if e["deterministic_selection_provenance"]["embedded_first_difference_diagnostic_present"]],
            "selected_candidates_without_embedded_first_difference_diagnostic": [e["raw_companion_package_id"] for e in entries if not e["deterministic_selection_provenance"]["embedded_first_difference_diagnostic_present"]],
        },
        "coefficient_independence_proof": {
            "selection_ignores_diagnostic_values": True,
            "implementation_uses_diagnostic_presence_flag_only": True,
            "fingerprint_excludes_stored_diagnostic_values": True,
        },
    }


def write_artifacts(root: Path, out: Path) -> dict[str, str]:
    result = build_campaign42_registry(root)
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "eligibility_inventory": out / "complete_21_package_eligibility_inventory.json",
        "registry": out / "campaign42_coefficient_free_companion_registry.json",
        "specification": out / "campaign42_declarative_companion_production_specification.json",
        "expected_package_id_manifest": out / "expected_package_id_manifest.json",
        "raw_to_companion_link_manifest": out / "raw_to_companion_link_manifest.json",
        "evidence_method_compatibility_report": out / "evidence_method_compatibility_report.json",
        "coefficient_independence_proof": out / "coefficient_independence_proof.json",
        "diagnostic_honesty_audit": out / "post_freeze_diagnostic_honesty_audit.json",
        "deterministic_regeneration_proof": out / "deterministic_regeneration_proof.json",
    }
    files["eligibility_inventory"].write_text(json.dumps(result["eligibility_inventory"], indent=2, sort_keys=True))
    files["registry"].write_text(json.dumps(result["registry"], indent=2, sort_keys=True))
    files["specification"].write_text(json.dumps(result["specification"], indent=2, sort_keys=True))
    files["expected_package_id_manifest"].write_text(json.dumps(result["expected_package_id_manifest"], indent=2, sort_keys=True))
    files["raw_to_companion_link_manifest"].write_text(json.dumps(result["raw_to_companion_link_manifest"], indent=2, sort_keys=True))
    compat = {
        "eligible_count": result["eligible_count"],
        "ineligible_count": result["ineligible_count"],
        "selected_count": len(result["registry"]["candidates"]),
        "minimum_overlap": MIN_TRANSFORMED_OBSERVATIONS,
        "minimum_coverage": "0.85",
        "candidate_compatibility": [
            {"candidate_id": e["campaign42_candidate_id"], "raw_package_id": e["raw_companion_package_id"], "expected_transformed_period_scope": e["expected_transformed_period_scope"], "expected_overlap": e["expected_minimum_overlap"], "expected_coverage": e["expected_minimum_coverage"], "unit_semantics": e["transformed_unit_semantics"]}
            for e in result["registry"]["candidates"]
        ],
    }
    files["evidence_method_compatibility_report"].write_text(json.dumps(compat, indent=2, sort_keys=True))
    files["coefficient_independence_proof"].write_text(json.dumps(result["coefficient_independence_proof"], indent=2, sort_keys=True))
    files["diagnostic_honesty_audit"].write_text(json.dumps(result["diagnostic_honesty_audit"], indent=2, sort_keys=True))
    rerun = build_campaign42_registry(root)
    regen = {"registry_fingerprint_first": result["registry_fingerprint"], "registry_fingerprint_second": rerun["registry_fingerprint"], "specification_fingerprint_first": result["specification_fingerprint"], "specification_fingerprint_second": rerun["specification_fingerprint"], "deterministic": result["registry_fingerprint"] == rerun["registry_fingerprint"] and result["specification_fingerprint"] == rerun["specification_fingerprint"]}
    files["deterministic_regeneration_proof"].write_text(json.dumps(regen, indent=2, sort_keys=True))
    return {k: str(v) for k, v in files.items()} | {"registry_fingerprint": result["registry_fingerprint"], "specification_fingerprint": result["specification_fingerprint"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--write-artifacts")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if args.write_artifacts:
        print(json.dumps(write_artifacts(root, Path(args.write_artifacts)), indent=2, sort_keys=True))
    else:
        result = build_campaign42_registry(root)
        print(json.dumps({"registry_fingerprint": result["registry_fingerprint"], "specification_fingerprint": result["specification_fingerprint"], "selected_count": len(result["registry"]["candidates"]), "eligible_count": result["eligible_count"], "ineligible_count": result["ineligible_count"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
