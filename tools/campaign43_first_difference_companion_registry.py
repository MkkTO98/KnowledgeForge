#!/usr/bin/env python3
"""Campaign 43 coefficient-free first-difference Pearson companion registry.

This helper freezes a bounded registry for exactly the six authorized Campaign 41
raw Pearson relationships that remain after Campaign 42 produced companions for
the two SWE Campaign 41 relationships. It evaluates package identity, retained
fixture compatibility, non-supersession, and existing-companion absence only.

It must not calculate first differences, Pearson coefficients, p-values,
covariance, or derived sample statistics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
RAW_METHOD_VERSION = "1.0"
RAW_METHOD_FINGERPRINT = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
MIN_EXPECTED_ALIGNED_TRANSFORMED_OBSERVATIONS = 30

FORBIDDEN_REGISTRY_TERMS = [
    "pearson_coefficient",
    "first_difference_pearson\"",
    "series_a_vs_time_index",
    "series_b_vs_time_index",
    "diagnostic_value",
    "p_value",
    "p-value",
    "covariance",
    "calculated_sample_statistic",
    "sample_mean",
    "sample_variance",
]

AUTHORIZED_CANDIDATES: list[dict[str, Any]] = [
    {
        "candidate_slug": "dnk_agricultural_land_broad_money",
        "source_raw_package_id": "pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1",
        "entity": "DNK",
        "series_codes_ordered": ["AG.LND.AGRI.ZS", "FM.LBL.BMNY.GD.ZS"],
        "relationship_label": "DNK agricultural land / broad money",
        "trend_risk_classification": "high_shared_time_trend_risk",
        "trend_risk_evidence": "Campaign 41 registry advisory review classified the relationship as moderate-to-high shared-time-trend/nonstationarity risk for land-share/financial aggregates; post-Campaign-42 readiness evidence records all Campaign 41 raw outputs as high shared-time-trend risk for companion evaluation.",
    },
    {
        "candidate_slug": "dnk_agricultural_land_private_credit",
        "source_raw_package_id": "pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1",
        "entity": "DNK",
        "series_codes_ordered": ["AG.LND.AGRI.ZS", "FS.AST.PRVT.GD.ZS"],
        "relationship_label": "DNK agricultural land / private credit",
        "trend_risk_classification": "high_shared_time_trend_risk",
        "trend_risk_evidence": "Campaign 41 registry advisory review classified the relationship as moderate-to-high shared-time-trend/nonstationarity risk for land-share/financial aggregates; post-Campaign-42 readiness evidence records all Campaign 41 raw outputs as high shared-time-trend risk for companion evaluation.",
    },
    {
        "candidate_slug": "dnk_forest_area_broad_money",
        "source_raw_package_id": "pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1",
        "entity": "DNK",
        "series_codes_ordered": ["AG.LND.FRST.ZS", "FM.LBL.BMNY.GD.ZS"],
        "relationship_label": "DNK forest area / broad money",
        "trend_risk_classification": "high_shared_time_trend_risk",
        "trend_risk_evidence": "Campaign 41 registry advisory review classified the relationship as moderate-to-high shared-time-trend/nonstationarity risk for land-share/financial aggregates; post-Campaign-42 readiness evidence records all Campaign 41 raw outputs as high shared-time-trend risk for companion evaluation.",
    },
    {
        "candidate_slug": "nor_crude_birth_rate_fossil_electricity",
        "source_raw_package_id": "pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1",
        "entity": "NOR",
        "series_codes_ordered": ["SP.DYN.CBRT.IN", "EG.ELC.FOSL.ZS"],
        "relationship_label": "NOR crude birth rate / fossil electricity",
        "trend_risk_classification": "high_shared_time_trend_risk",
        "trend_risk_evidence": "Campaign 41 registry advisory review classified the relationship as high shared-time-trend/nonstationarity risk likely for the demographic/energy pair; post-Campaign-42 readiness evidence records all Campaign 41 raw outputs as high shared-time-trend risk for companion evaluation.",
    },
    {
        "candidate_slug": "nor_fossil_electricity_under5_mortality",
        "source_raw_package_id": "pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1",
        "entity": "NOR",
        "series_codes_ordered": ["EG.ELC.FOSL.ZS", "SH.DYN.MORT"],
        "relationship_label": "NOR fossil electricity / under-5 mortality",
        "trend_risk_classification": "high_shared_time_trend_risk",
        "trend_risk_evidence": "Campaign 41 registry advisory review classified the relationship as high shared-time-trend/nonstationarity risk likely for the energy/health pair; post-Campaign-42 readiness evidence records all Campaign 41 raw outputs as high shared-time-trend risk for companion evaluation.",
    },
    {
        "candidate_slug": "nor_nonhydro_renewable_electricity_under5_mortality",
        "source_raw_package_id": "pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1",
        "entity": "NOR",
        "series_codes_ordered": ["EG.ELC.RNWX.ZS", "SH.DYN.MORT"],
        "relationship_label": "NOR nonhydro renewable electricity / under-5 mortality",
        "trend_risk_classification": "high_shared_time_trend_risk",
        "trend_risk_evidence": "Campaign 41 registry advisory review classified the relationship as high shared-time-trend/nonstationarity risk likely for the energy/health pair; post-Campaign-42 readiness evidence records all Campaign 41 raw outputs as high shared-time-trend risk for companion evaluation.",
    },
]


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


def source_raw_package_fingerprint(package: dict[str, Any]) -> str:
    return package.get("fingerprints", {}).get("package_manifest") or fingerprint(package)


def source_payload_fingerprint(package: dict[str, Any]) -> str | None:
    return package_payload(package).get("package_fingerprint")


def expected_companion_package_id(raw_package_id: str) -> str:
    return raw_package_id.removesuffix("-pearson-correlation-v1") + "-first-difference-pearson-companion-v1"


def observed_periods(root: Path, entity: str, indicator_code: str) -> dict[str, Any]:
    matches: list[Path] = []
    fixtures_root = root / "artifacts" / "evidence-fixtures"
    for path in fixtures_root.glob("**/normalized_observations.json"):
        data = load_json(path)
        obs = data.get("observations") or []
        if any(o.get("entity_id") == entity and o.get("indicator_code") == indicator_code for o in obs):
            matches.append(path)
    if not matches:
        raise ValueError(f"missing retained fixture for {entity} {indicator_code}")
    path = sorted(matches, key=lambda p: ("campaign40-spec-driven-pearson-production" not in str(p), str(p)))[0]
    data = load_json(path)
    obs = [o for o in data.get("observations", []) if o.get("entity_id") == entity and o.get("indicator_code") == indicator_code]
    years = sorted(int(o["period"]) for o in obs if o.get("observed") is True and o.get("value_canonical") not in (None, ""))
    if not years:
        raise ValueError(f"no observed years for {entity} {indicator_code}")
    return {
        "path": str(path.relative_to(root)),
        "normalized_fingerprint": data.get("normalized_fingerprint"),
        "source_raw_fixture_fingerprint": data.get("source_raw_fixture_fingerprint"),
        "selection_fingerprint": data.get("selection_fingerprint"),
        "observed_periods": years,
        "observed_count": len(years),
        "unit": next((o.get("unit") for o in obs if o.get("unit")), ""),
        "indicator_name": obs[0].get("indicator_name") if obs else indicator_code,
    }


def compatible_difference_periods(periods_a: list[int], periods_b: list[int]) -> list[int]:
    # This computes only resolvable period identities; it does not compute first-differenced values.
    set_a, set_b = set(periods_a), set(periods_b)
    if not set_a or not set_b:
        return []
    start = max(min(set_a), min(set_b)) + 1
    end = min(max(set_a), max(set_b))
    return [year for year in range(start, end + 1) if year in set_a and year - 1 in set_a and year in set_b and year - 1 in set_b]


def transformed_unit_semantics(unit: str) -> str:
    normalized = unit.strip().lower()
    if not normalized:
        raise ValueError("unit_missing")
    if "growth" in normalized or "percent change" in normalized or "annual %" in normalized:
        raise ValueError(f"unit_not_absolute_difference_transformable:{unit}")
    if "% of gdp" in normalized or "percent of gdp" in normalized:
        return "year-to-year change in percentage points of GDP"
    if normalized.startswith("% of") or "percent of" in normalized:
        return f"year-to-year percentage-point change in {unit}"
    if "per 1,000" in normalized or "per 100" in normalized:
        return f"absolute year-to-year change in {unit}"
    return f"absolute year-to-year change in {unit}"


def existing_companion_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in (root / "knowledge_repository" / "objects").glob("*.json"):
        package = load_json(path)
        payload = package_payload(package)
        app = package_applicability(package)
        if payload.get("method_id") == METHOD_ID or app.get("method_id") == METHOD_ID:
            ids.add(package["package_id"])
    return ids


def build_entry(root: Path, ordinal: int, candidate: dict[str, Any], existing_companions: set[str]) -> dict[str, Any]:
    package_path = root / "knowledge_repository" / "objects" / f"{candidate['source_raw_package_id']}.json"
    if not package_path.exists():
        raise ValueError(f"missing source raw package: {candidate['source_raw_package_id']}")
    package = load_json(package_path)
    payload = package_payload(package)
    app = package_applicability(package)
    series_a = payload.get("series_a", {})
    series_b = payload.get("series_b", {})
    codes = [series_a.get("code"), series_b.get("code")]
    if package.get("package_id") != candidate["source_raw_package_id"]:
        raise ValueError("source package id mismatch")
    if app.get("method_id") != RAW_METHOD_ID:
        raise ValueError(f"source package is not raw Pearson v1: {candidate['source_raw_package_id']}")
    if app.get("method_version") != RAW_METHOD_VERSION:
        raise ValueError(f"source package raw method version mismatch: {candidate['source_raw_package_id']}")
    if payload.get("entity_id") != candidate["entity"] or app.get("entity_id") != candidate["entity"]:
        raise ValueError(f"source package entity mismatch: {candidate['source_raw_package_id']}")
    if codes != candidate["series_codes_ordered"]:
        raise ValueError(f"source package series order mismatch: {candidate['source_raw_package_id']}: {codes}")

    fa = observed_periods(root, candidate["entity"], codes[0])
    fb = observed_periods(root, candidate["entity"], codes[1])
    periods = compatible_difference_periods(fa["observed_periods"], fb["observed_periods"])
    expected_id = expected_companion_package_id(candidate["source_raw_package_id"])
    exclusion_reasons: list[str] = []
    if len(periods) < MIN_EXPECTED_ALIGNED_TRANSFORMED_OBSERVATIONS:
        exclusion_reasons.append("insufficient_resolvable_periods_for_future_first_difference")
    if expected_id in existing_companions:
        exclusion_reasons.append("equivalent_first_difference_companion_already_exists")
    if package.get("confidence_quality", {}).get("lifecycle_state") != "accepted":
        exclusion_reasons.append("source_raw_package_not_accepted")
    if package.get("evolution_metadata", {}).get("superseded_by"):
        exclusion_reasons.append("source_raw_package_superseded")

    eligibility = "included" if not exclusion_reasons else "excluded"
    rationale = (
        "Included because the authorized Campaign 41 raw package is accepted, not superseded, has the recorded high shared-time-trend risk basis, resolves to retained annual raw fixtures, has enough consecutive aligned periods for future first-difference evaluation, and has no existing equivalent first-difference companion."
        if eligibility == "included"
        else "Excluded because: " + "; ".join(exclusion_reasons)
    )
    return {
        "campaign43_candidate_id": f"campaign43-fd-pearson-companion-candidate-{ordinal:02d}",
        "candidate_slug": candidate["candidate_slug"],
        "relationship_label": candidate["relationship_label"],
        "eligibility_status": eligibility,
        "inclusion_or_exclusion_rationale": rationale,
        "exclusion_reasons": exclusion_reasons,
        "source_raw_package": {
            "package_id": package["package_id"],
            "package_manifest_fingerprint": source_raw_package_fingerprint(package),
            "payload_package_fingerprint": source_payload_fingerprint(package),
            "lifecycle_state": package.get("confidence_quality", {}).get("lifecycle_state"),
            "superseded_by": package.get("evolution_metadata", {}).get("superseded_by"),
            "source_campaign": package.get("lineage", {}).get("source_campaign"),
        },
        "entity": candidate["entity"],
        "frequency": app.get("frequency"),
        "raw_method": {
            "id": app.get("method_id"),
            "version": app.get("method_version"),
            "contract_fingerprint": payload.get("method_contract_fingerprint") or RAW_METHOD_FINGERPRINT,
        },
        "series_pair_ordered": [
            {"code": series_a.get("code"), "name": series_a.get("name"), "unit": series_a.get("unit"), "transformation": series_a.get("transformation")},
            {"code": series_b.get("code"), "name": series_b.get("name"), "unit": series_b.get("unit"), "transformation": series_b.get("transformation")},
        ],
        "raw_period_scope": payload.get("period_scope") or {"start": app.get("period_start"), "end": app.get("period_end")},
        "trend_risk": {
            "classification": candidate["trend_risk_classification"],
            "evidence": candidate["trend_risk_evidence"],
        },
        "retained_input_series": [
            {
                "identity": f"{codes[0]}__{candidate['entity']}__{app.get('period_start')}-{app.get('period_end')}",
                "path": fa["path"],
                "normalized_fingerprint": fa["normalized_fingerprint"],
                "source_raw_fixture_fingerprint": fa["source_raw_fixture_fingerprint"],
                "selection_fingerprint": fa["selection_fingerprint"],
                "observed_count": fa["observed_count"],
            },
            {
                "identity": f"{codes[1]}__{candidate['entity']}__{app.get('period_start')}-{app.get('period_end')}",
                "path": fb["path"],
                "normalized_fingerprint": fb["normalized_fingerprint"],
                "source_raw_fixture_fingerprint": fb["source_raw_fixture_fingerprint"],
                "selection_fingerprint": fb["selection_fingerprint"],
                "observed_count": fb["observed_count"],
            },
        ],
        "future_first_difference_compatibility": {
            "transformation": {"id": TRANSFORMATION_ID, "version": TRANSFORMATION_VERSION, "contract_fingerprint": TRANSFORMATION_FINGERPRINT},
            "method": {"id": METHOD_ID, "version": METHOD_VERSION, "contract_fingerprint": METHOD_FINGERPRINT, "validation_registry_fingerprint": VALIDATION_REGISTRY_FINGERPRINT},
            "expected_companion_package_id": expected_id,
            "equivalent_first_difference_companion_exists": expected_id in existing_companions,
            "minimum_required_resolvable_aligned_periods": MIN_EXPECTED_ALIGNED_TRANSFORMED_OBSERVATIONS,
            "resolvable_aligned_period_count_for_future_differencing": len(periods),
            "resolvable_aligned_period_scope_for_future_differencing": {"start": periods[0] if periods else None, "end": periods[-1] if periods else None},
            "transformed_unit_semantics": [transformed_unit_semantics(series_a.get("unit") or fa.get("unit") or ""), transformed_unit_semantics(series_b.get("unit") or fb.get("unit") or "")],
        },
    }


def build_campaign43_registry(root: Path) -> dict[str, Any]:
    existing = existing_companion_ids(root)
    entries = [build_entry(root, i + 1, c, existing) for i, c in enumerate(AUTHORIZED_CANDIDATES)]
    registry = {
        "registry_id": "campaign43_coefficient_free_first_difference_companion_registry",
        "registry_version": "1.0",
        "campaign": "Campaign 43",
        "purpose": "Freeze the six remaining Campaign 41 high-shared-time-trend raw Pearson relationships for possible later first-difference companion production.",
        "coefficient_free": True,
        "production_authorized": False,
        "calculation_authorized": False,
        "canonical_publication_authorized": False,
        "candidate_boundary": {
            "authorized_relationship_count": 6,
            "source": "post-Campaign-42 next-production readiness decision",
            "excluded_sources": ["Campaign 40", "corrected raw-candidate pool", "other campaigns"],
        },
        "method_contracts": {
            "source_raw_method_id": RAW_METHOD_ID,
            "source_raw_method_version": RAW_METHOD_VERSION,
            "source_raw_method_contract_fingerprint": RAW_METHOD_FINGERPRINT,
            "future_transformation_id": TRANSFORMATION_ID,
            "future_transformation_version": TRANSFORMATION_VERSION,
            "future_transformation_contract_fingerprint": TRANSFORMATION_FINGERPRINT,
            "future_method_id": METHOD_ID,
            "future_method_version": METHOD_VERSION,
            "future_method_contract_fingerprint": METHOD_FINGERPRINT,
            "future_method_validation_registry_fingerprint": VALIDATION_REGISTRY_FINGERPRINT,
        },
        "deterministic_ordering": "authorized readiness-decision order, preserved exactly and assigned ordinal candidate ids 01-06",
        "entries": entries,
    }
    serialized = canonical_json(registry).lower()
    for term in FORBIDDEN_REGISTRY_TERMS:
        if term in serialized:
            raise ValueError(f"forbidden coefficient/result term in registry: {term}")
    spec = {
        "specification_id": "campaign43_first_difference_companion_registry_freeze_specification",
        "specification_version": "1.0",
        "registry_fingerprint": fingerprint(registry),
        "candidate_ids": [e["campaign43_candidate_id"] for e in entries],
        "included_candidate_ids": [e["campaign43_candidate_id"] for e in entries if e["eligibility_status"] == "included"],
        "excluded_candidate_ids": [e["campaign43_candidate_id"] for e in entries if e["eligibility_status"] == "excluded"],
        "raw_to_expected_companion_links": [
            {
                "source_raw_package_id": e["source_raw_package"]["package_id"],
                "expected_companion_package_id": e["future_first_difference_compatibility"]["expected_companion_package_id"],
                "eligibility_status": e["eligibility_status"],
            }
            for e in entries
        ],
        "execution_boundary": "Registry freeze only. Coefficient calculation, first-difference execution, KnowledgeObjectPackage construction, canonical publication, and PostgreSQL mutation require separate authorization.",
        "method_contracts": registry["method_contracts"],
    }
    return {
        "registry": registry,
        "registry_fingerprint": fingerprint(registry),
        "specification": spec,
        "specification_fingerprint": fingerprint(spec),
        "included_count": sum(1 for e in entries if e["eligibility_status"] == "included"),
        "excluded_count": sum(1 for e in entries if e["eligibility_status"] == "excluded"),
    }


def validate_registry(root: Path, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    result = build_campaign43_registry(root)
    expected = result["registry"]
    observed = registry or expected
    errors: list[str] = []
    if observed != expected:
        errors.append("registry_not_equal_to_deterministic_generation")
    if result["registry_fingerprint"] != fingerprint(observed):
        errors.append("registry_fingerprint_mismatch")
    if len(observed.get("entries", [])) != 6:
        errors.append("candidate_boundary_not_six")
    ids = [e.get("campaign43_candidate_id") for e in observed.get("entries", [])]
    if ids != sorted(ids):
        errors.append("candidate_ids_not_deterministically_ordered")
    if len(ids) != len(set(ids)):
        errors.append("duplicate_candidate_ids")
    if canonical_json(observed).lower().find("pearson_coefficient") != -1:
        errors.append("coefficient_field_present")
    return {"valid": not errors, "errors": errors, "registry_fingerprint": result["registry_fingerprint"], "specification_fingerprint": result["specification_fingerprint"], "included_count": result["included_count"], "excluded_count": result["excluded_count"]}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_artifacts(root: Path) -> dict[str, str]:
    result = build_campaign43_registry(root)
    registry_path = root / "specs" / "correlation_batches" / "campaign43_coefficient_free_first_difference_companion_registry.json"
    spec_path = root / "specs" / "correlation_batches" / "campaign43_first_difference_companion_registry_freeze_specification.json"
    report_dir = root / "artifacts" / "reports" / "campaign43-coefficient-free-first-difference-companion-registry-20260712"
    write_json(registry_path, result["registry"])
    write_json(spec_path, result["specification"])
    validation = validate_registry(root, result["registry"])
    write_json(report_dir / "registry_validation.json", validation)
    write_json(report_dir / "registry_freeze_summary.json", {
        "registry_id": result["registry"]["registry_id"],
        "registry_fingerprint": result["registry_fingerprint"],
        "specification_fingerprint": result["specification_fingerprint"],
        "included_candidates": [e["relationship_label"] for e in result["registry"]["entries"] if e["eligibility_status"] == "included"],
        "excluded_candidates": [{"relationship_label": e["relationship_label"], "reasons": e["exclusion_reasons"]} for e in result["registry"]["entries"] if e["eligibility_status"] == "excluded"],
        "coefficient_free": True,
        "canonical_publication_authorized": False,
    })
    return {
        "registry": str(registry_path),
        "specification": str(spec_path),
        "validation": str(report_dir / "registry_validation.json"),
        "summary": str(report_dir / "registry_freeze_summary.json"),
        "registry_fingerprint": result["registry_fingerprint"],
        "specification_fingerprint": result["specification_fingerprint"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if args.write_artifacts:
        print(json.dumps(write_artifacts(root), indent=2, sort_keys=True))
    elif args.validate:
        print(json.dumps(validate_registry(root), indent=2, sort_keys=True))
    else:
        result = build_campaign43_registry(root)
        print(json.dumps({"registry_fingerprint": result["registry_fingerprint"], "specification_fingerprint": result["specification_fingerprint"], "included_count": result["included_count"], "excluded_count": result["excluded_count"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
