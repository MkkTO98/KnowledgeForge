#!/usr/bin/env python3
"""Campaign 43 first-difference Pearson companion calculation gate.

Bounded helper for the six frozen Campaign 43 candidates. It verifies frozen
registry/spec identities and computes first-difference Pearson coefficients from
retained fixtures only. It intentionally does not construct, publish, or project
KnowledgeObjectPackages.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from decimal import Decimal, Context, ROUND_HALF_EVEN, localcontext, getcontext
from pathlib import Path
from typing import Any

REGISTRY_REL = Path("specs/correlation_batches/campaign43_coefficient_free_first_difference_companion_registry.json")
SPEC_REL = Path("specs/correlation_batches/campaign43_first_difference_companion_registry_freeze_specification.json")
REPORT_DIR_REL = Path("artifacts/reports/campaign43-first-difference-companion-calculation-20260712")
EXPECTED_REGISTRY_FP = "sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1"
EXPECTED_SPEC_FP = "sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf"
EXPECTED_REPOSITORY_COUNT = 554
EXPECTED_REPOSITORY_FP = "sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b"
POST_PUBLICATION_REPOSITORY_COUNT = 560
POST_PUBLICATION_REPOSITORY_FP = "sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7"
POST_EVIDENCE_PORTFOLIO_PILOT_COUNT = 562
POST_EVIDENCE_PORTFOLIO_PILOT_FP = "sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff"
EXPECTED_COMPANION_MANIFEST_FINGERPRINTS = {
    "pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-first-difference-pearson-companion-v1": "sha256:5dfcca7a3b90bf8ab058f20b32555145c684fa004140ad457d67fc3dd222db14",
    "pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-first-difference-pearson-companion-v1": "sha256:46365f326c989e8aed78efc51e3d561a0ec77a2a6057949cbc854988240449a6",
    "pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-first-difference-pearson-companion-v1": "sha256:ca97d74262e76130c23c52267141fb2d00c0ad5b00706062fb054c731890aa2d",
    "pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-first-difference-pearson-companion-v1": "sha256:c12ceeff3a8bf73f5c9e4cd84e8d051e5ffdaa3483213c1b5b2da502ba3a103b",
    "pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-first-difference-pearson-companion-v1": "sha256:75471a45ea8de19abf7dc0718a82d13598d754fbabac8c498665b94229696d0b",
    "pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-first-difference-pearson-companion-v1": "sha256:f63c6055b35b3fb92dd8d485639f5b98acc14a26014a0eed8502b006b8edf4d2",
}
METHOD_ID = "wdi_annual_scalar_first_difference_pearson_v1"
METHOD_VERSION = "1.0"
METHOD_FP = "sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade"
TRANSFORMATION_ID = "wdi_annual_scalar_first_difference_v1"
TRANSFORMATION_VERSION = "1.0"
TRANSFORMATION_FP = "sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f"
VALIDATION_REGISTRY_FP = "sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657"
INTERNAL_CONTEXT = Context(prec=50, rounding=ROUND_HALF_EVEN)
Q12 = Decimal("0.000000000001")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


ANALYTICAL_COMPARISON_PROFILE = "campaign43_analytical_comparison_v1"
# The accepted Campaign 43 broad candidate fingerprint includes these fields.
# Their transformed-series preimages contain the operational normalized-file
# path, so they preserve historical execution context but are not portable
# analytical comparison keys across clean checkout roots.
_CONTEXTUAL_CANDIDATE_FIELDS = frozenset({
    "transformed_series_fingerprints",
    "calculation_result_fingerprint",
    "calculation_summary_fingerprint",
})


def analytical_candidate_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    """Return stable Campaign 43 analytical content without path-context hashes.

    This is a new compatibility projection. It does not reinterpret or replace
    the accepted historical candidate_result_fingerprint.
    """
    return {
        key: value
        for key, value in candidate.items()
        if key not in _CONTEXTUAL_CANDIDATE_FIELDS
    }


def analytical_result_projection(result: dict[str, Any]) -> dict[str, Any]:
    """Separate analytical identity from repository/execution context."""
    return {
        "profile": ANALYTICAL_COMPARISON_PROFILE,
        "campaign": result.get("campaign"),
        "registry_fingerprint": result.get("registry_fingerprint"),
        "specification_fingerprint": result.get("specification_fingerprint"),
        "candidate_count": result.get("candidate_count"),
        "accepted_calculation_count": result.get("accepted_calculation_count"),
        "rejected_calculation_count": result.get("rejected_calculation_count"),
        "method_contract_fingerprint": result.get("method_contract_fingerprint"),
        "transformation_contract_fingerprint": result.get("transformation_contract_fingerprint"),
        "validation_registry_fingerprint": result.get("validation_registry_fingerprint"),
        "expected_companion_package_ids": result.get("expected_companion_package_ids"),
        "candidate_results": [
            analytical_candidate_projection(candidate)
            for candidate in result.get("candidate_results", [])
        ],
    }


def analytical_result_fingerprint(result: dict[str, Any]) -> str:
    return sha256_value(analytical_result_projection(result))


def repository_context_projection(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "repository_before": result.get("repository_before"),
        "repository_after": result.get("repository_after"),
        "pre_existing_package_immutability": result.get("pre_existing_package_immutability"),
    }


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_method_module(root: Path):
    path = root / "tools" / "first_difference_pearson_method_v1.py"
    spec = importlib.util.spec_from_file_location("first_difference_pearson_method_v1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load first_difference_pearson_method_v1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_repository_module(root: Path):
    path = root / "tools" / "knowledge_repository.py"
    spec = importlib.util.spec_from_file_location("knowledge_repository", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load knowledge_repository")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_payload(package: dict[str, Any]) -> dict[str, Any]:
    return (package.get("generated_statements") or [{}])[0].get("structured_payload", {})


def source_raw_package_fingerprint(package: dict[str, Any]) -> str:
    return package.get("fingerprints", {}).get("package_manifest") or sha256_value(package)


def repository_baseline(root: Path) -> dict[str, Any]:
    kr = load_repository_module(root)
    packages = []
    errors = []
    raw = 0
    fd = 0
    for path in sorted((root / "knowledge_repository" / "objects").glob("*.json")):
        package = read_json(path)
        try:
            kr._require_validated_knowledge_object(package)
        except Exception as exc:  # pragma: no cover - surfaced in report/tests
            errors.append(f"{path.name}: {exc}")
        payload = package_payload(package)
        method = payload.get("method_id") or (package.get("generated_statements") or [{}])[0].get("applicability", {}).get("method_id")
        if method == "wdi_annual_scalar_pearson_correlation_v1" and "pearson_coefficient" in payload:
            raw += 1
        if method == METHOD_ID:
            fd += 1
        packages.append(package)
    indexes = kr._build_indexes(packages)
    computed = kr._repository_fingerprint(packages, indexes)
    manifest = read_json(root / "knowledge_repository" / "manifest.json")
    return {
        "object_file_count": len(packages),
        "manifest_object_count": manifest.get("object_count"),
        "computed_repository_fingerprint": computed,
        "manifest_repository_fingerprint": manifest.get("repository_fingerprint"),
        "validation_errors": errors,
        "raw_pearson_objects": raw,
        "first_difference_pearson_companions": fd,
    }


def object_hashes(root: Path) -> dict[str, str]:
    return {p.name: sha256_bytes(p.read_bytes()) for p in sorted((root / "knowledge_repository" / "objects").glob("*.json"))}


def load_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    return read_json(root / REGISTRY_REL), read_json(root / SPEC_REL)


def pre_execution_gate(root: Path) -> dict[str, Any]:
    registry, spec = load_inputs(root)
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, **extra: Any) -> None:
        checks.append({"check": name, "pass": ok, **extra})

    registry_fp = sha256_value(registry)
    spec_fp = sha256_value(spec)
    entries = registry.get("entries", [])
    included = [e for e in entries if e.get("eligibility_status") == "included"]
    baseline = repository_baseline(root)
    add("registry_fingerprint", registry_fp == EXPECTED_REGISTRY_FP, actual=registry_fp, expected=EXPECTED_REGISTRY_FP)
    add("specification_fingerprint", spec_fp == EXPECTED_SPEC_FP, actual=spec_fp, expected=EXPECTED_SPEC_FP)
    add("candidate_count", len(entries) == 6 and len(included) == 6, actual={"entries": len(entries), "included": len(included)}, expected=6)
    add("candidate_order", [e["campaign43_candidate_id"] for e in entries] == spec.get("candidate_ids"), actual=[e.get("campaign43_candidate_id") for e in entries], expected=spec.get("candidate_ids"))
    pre_publication_baseline = (baseline["object_file_count"] == EXPECTED_REPOSITORY_COUNT and baseline["manifest_object_count"] == EXPECTED_REPOSITORY_COUNT and baseline["computed_repository_fingerprint"] == EXPECTED_REPOSITORY_FP and baseline["manifest_repository_fingerprint"] == EXPECTED_REPOSITORY_FP)
    post_publication_baseline = (baseline["object_file_count"] == POST_PUBLICATION_REPOSITORY_COUNT and baseline["manifest_object_count"] == POST_PUBLICATION_REPOSITORY_COUNT and baseline["computed_repository_fingerprint"] == POST_PUBLICATION_REPOSITORY_FP and baseline["manifest_repository_fingerprint"] == POST_PUBLICATION_REPOSITORY_FP)
    post_portfolio_pilot_baseline = (baseline["object_file_count"] == POST_EVIDENCE_PORTFOLIO_PILOT_COUNT and baseline["manifest_object_count"] == POST_EVIDENCE_PORTFOLIO_PILOT_COUNT and baseline["computed_repository_fingerprint"] == POST_EVIDENCE_PORTFOLIO_PILOT_FP and baseline["manifest_repository_fingerprint"] == POST_EVIDENCE_PORTFOLIO_PILOT_FP)
    add("repository_count", pre_publication_baseline or post_publication_baseline or post_portfolio_pilot_baseline, actual=baseline, expected=[EXPECTED_REPOSITORY_COUNT, POST_PUBLICATION_REPOSITORY_COUNT, POST_EVIDENCE_PORTFOLIO_PILOT_COUNT])
    add("repository_fingerprint", pre_publication_baseline or post_publication_baseline or post_portfolio_pilot_baseline, actual=baseline, expected=[EXPECTED_REPOSITORY_FP, POST_PUBLICATION_REPOSITORY_FP, POST_EVIDENCE_PORTFOLIO_PILOT_FP])
    add("repository_validation", not baseline["validation_errors"], errors=baseline["validation_errors"])
    add("method_contract_fingerprint", spec.get("method_contracts", {}).get("future_method_contract_fingerprint") == METHOD_FP, actual=spec.get("method_contracts", {}).get("future_method_contract_fingerprint"), expected=METHOD_FP)
    add("transformation_contract_fingerprint", spec.get("method_contracts", {}).get("future_transformation_contract_fingerprint") == TRANSFORMATION_FP, actual=spec.get("method_contracts", {}).get("future_transformation_contract_fingerprint"), expected=TRANSFORMATION_FP)
    add("validation_registry_fingerprint", spec.get("method_contracts", {}).get("future_method_validation_registry_fingerprint") == VALIDATION_REGISTRY_FP, actual=spec.get("method_contracts", {}).get("future_method_validation_registry_fingerprint"), expected=VALIDATION_REGISTRY_FP)
    for entry in entries:
        cid = entry["campaign43_candidate_id"]
        raw_id = entry["source_raw_package"]["package_id"]
        raw_path = root / "knowledge_repository" / "objects" / f"{raw_id}.json"
        raw_pkg = read_json(raw_path) if raw_path.exists() else None
        add("source_raw_package_exists", raw_pkg is not None, candidate_id=cid, package_id=raw_id)
        if raw_pkg is not None:
            add("source_raw_package_fingerprint", source_raw_package_fingerprint(raw_pkg) == entry["source_raw_package"]["package_manifest_fingerprint"], candidate_id=cid, actual=source_raw_package_fingerprint(raw_pkg), expected=entry["source_raw_package"]["package_manifest_fingerprint"])
            payload = package_payload(raw_pkg)
            app = (raw_pkg.get("generated_statements") or [{}])[0].get("applicability", {})
            raw_method_id = payload.get("method_id") or app.get("method_id")
            add("source_raw_package_method", raw_method_id == "wdi_annual_scalar_pearson_correlation_v1", candidate_id=cid, actual=raw_method_id)
            add("source_raw_not_superseded", entry["source_raw_package"].get("superseded_by") is None and raw_pkg.get("confidence_quality", {}).get("lifecycle_state") == "accepted", candidate_id=cid)
        companion_id = entry["future_first_difference_compatibility"]["expected_companion_package_id"]
        companion_path = root / "knowledge_repository" / "objects" / f"{companion_id}.json"
        if companion_path.exists():
            companion = read_json(companion_path)
            companion_fp = companion.get("fingerprints", {}).get("package_manifest")
            companion_ok = companion_fp == EXPECTED_COMPANION_MANIFEST_FINGERPRINTS.get(companion_id)
        else:
            companion_fp = None
            companion_ok = True
        add("expected_companion_absent_or_matching_canonical", companion_ok, candidate_id=cid, package_id=companion_id, exists=companion_path.exists(), actual=companion_fp, expected=EXPECTED_COMPANION_MANIFEST_FINGERPRINTS.get(companion_id))
        for fixture in entry.get("retained_input_series", []):
            fpath = root / fixture["path"]
            data = read_json(fpath) if fpath.exists() else None
            add("retained_fixture_exists", data is not None, candidate_id=cid, fixture=fixture["identity"])
            if data is not None:
                add("retained_fixture_normalized_fingerprint", data.get("normalized_fingerprint") == fixture["normalized_fingerprint"], candidate_id=cid, fixture=fixture["identity"], actual=data.get("normalized_fingerprint"), expected=fixture["normalized_fingerprint"])
    result_dependent_keys = {"pearson_coefficient", "first_difference_pearson_coefficient", "p_value", "covariance", "significance"}

    def find_forbidden_keys(value: Any, path: str = "") -> list[str]:
        found: list[str] = []
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else str(key)
                if str(key).lower() in result_dependent_keys:
                    found.append(child_path)
                found.extend(find_forbidden_keys(child, child_path))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                found.extend(find_forbidden_keys(child, f"{path}[{index}]"))
        return found

    found = find_forbidden_keys({"registry": registry, "spec": spec})
    add("frozen_inputs_no_calculated_result_fields", not found, forbidden_found=found)
    return {"valid": all(c["pass"] for c in checks), "registry_fingerprint": registry_fp, "specification_fingerprint": spec_fp, "repository_baseline": baseline, "checks": checks}


def canonical_decimal_12(value: Decimal) -> str:
    with localcontext(INTERNAL_CONTEXT):
        rounded = value.quantize(Q12)
    if rounded.is_zero():
        return "0"
    text = format(rounded, "f")
    if "E" in text.upper():
        raise ValueError("scientific notation forbidden")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def prior_precision_match(prior: Any, new: str) -> tuple[bool, str]:
    prior_dec = Decimal(str(prior))
    new_dec = Decimal(str(new))
    if prior_dec == new_dec:
        return True, "exact_decimal_match"
    exponent = prior_dec.as_tuple().exponent
    prior_places = abs(int(exponent)) if isinstance(exponent, int) and exponent < 0 else 0
    with localcontext(INTERNAL_CONTEXT):
        q = Decimal(1).scaleb(-prior_places)
        if new_dec.quantize(q) == prior_dec:
            return True, f"new_value_matches_when_quantized_to_prior_{prior_places}_decimal_places"
    return False, "canonical_value_differs"


def recompute_reference_from_aligned_pairs(aligned: list[dict[str, Any]]) -> str:
    xs = [Decimal(str(row["series_a"])) for row in aligned]
    ys = [Decimal(str(row["series_b"])) for row in aligned]
    with localcontext(INTERNAL_CONTEXT):
        n = Decimal(len(xs))
        sx = sum(xs, Decimal(0)); sy = sum(ys, Decimal(0))
        sxy = sum(x * y for x, y in zip(xs, ys))
        sx2 = sum(x * x for x in xs); sy2 = sum(y * y for y in ys)
        numerator = sxy - (sx * sy / n)
        var_x = sx2 - (sx * sx / n)
        var_y = sy2 - (sy * sy / n)
        if var_x.is_zero() or var_y.is_zero():
            raise ValueError("zero variance transformed series")
        coeff = numerator / (var_x * var_y).sqrt(context=INTERNAL_CONTEXT)
    return canonical_decimal_12(coeff)


def candidate_series(entry: dict[str, Any], method_module: Any, root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    series = []
    for fixture in entry["retained_input_series"]:
        series.append(method_module.load_series_from_normalized(root / fixture["path"]))
    if len(series) != 2:
        raise ValueError("expected exactly two retained input series")
    return series[0], series[1]


def compute_candidate(root: Path, entry: dict[str, Any], *, weird_decimal_context: bool = False) -> dict[str, Any]:
    method_module = load_method_module(root)
    series_a, series_b = candidate_series(entry, method_module, root)
    if weird_decimal_context:
        with localcontext() as ctx:
            ctx.prec = 17
            result = method_module.compute_first_difference_pearson(series_a, series_b)
    else:
        result = method_module.compute_first_difference_pearson(series_a, series_b)
    reference = recompute_reference_from_aligned_pairs(result["aligned_transformed_observations"])
    if result["coefficient"]["canonical"] != reference:
        raise ValueError("independent recomputation mismatch")
    with localcontext() as ctx:
        ctx.prec = 17
        adversarial = method_module.compute_first_difference_pearson(series_a, series_b)["coefficient"]["canonical"]
    if adversarial != result["coefficient"]["canonical"]:
        raise ValueError("ambient Decimal context affected result")
    raw_id = entry["source_raw_package"]["package_id"]
    raw_package = read_json(root / "knowledge_repository" / "objects" / f"{raw_id}.json")
    prior = package_payload(raw_package).get("diagnostic_limitations", {})
    prior_coeff = prior.get("first_difference_pearson")
    prior_match = None
    prior_match_basis = "not_present"
    if prior_coeff is not None:
        prior_match, prior_match_basis = prior_precision_match(prior_coeff, result["coefficient"]["canonical"])
    aligned_count = result["aligned_transformed_observation_count"]
    expected_aligned = entry["future_first_difference_compatibility"]["resolvable_aligned_period_count_for_future_differencing"]
    reconciliation = {
        "prior_embedded_diagnostic_present": prior_coeff is not None,
        "prior_embedded_first_difference_coefficient": prior_coeff,
        "new_companion_coefficient": result["coefficient"]["canonical"],
        "coefficient_matches_prior_diagnostic_at_recorded_precision": prior_match,
        "coefficient_match_basis": prior_match_basis,
        "aligned_count_matches_registry": aligned_count == expected_aligned,
        "expected_registry_aligned_count": expected_aligned,
    }
    if not reconciliation["aligned_count_matches_registry"]:
        raise ValueError(f"aligned count mismatch for {entry['campaign43_candidate_id']}")
    aligned_payload = result["aligned_transformed_observations"]
    calc = {
        "candidate_id": entry["campaign43_candidate_id"],
        "relationship_label": entry["relationship_label"],
        "entity": entry["entity"],
        "source_raw_package_id": raw_id,
        "expected_companion_package_id": entry["future_first_difference_compatibility"]["expected_companion_package_id"],
        "status": "calculated_not_published",
        "method_id": METHOD_ID,
        "method_version": METHOD_VERSION,
        "method_contract_fingerprint": result["method_contract_fingerprint"],
        "transformation_id": TRANSFORMATION_ID,
        "transformation_version": TRANSFORMATION_VERSION,
        "transformation_contract_fingerprint": result["transformation_contract_fingerprint"],
        "coefficient": result["coefficient"],
        "independent_recompute_coefficient": {"canonical": reference, "unit": "dimensionless"},
        "raw_period_scope": result["raw_period_scope"],
        "transformed_period_scope": result["transformed_period_scope"],
        "aligned_transformed_observation_count": aligned_count,
        "expected_transformed_period_count": result["expected_transformed_period_count"],
        "transformed_coverage_share": result["transformed_coverage_share"],
        "aligned_transformed_periods": result["aligned_periods"],
        "transformed_series_fingerprints": result["transformed_series_fingerprints"],
        "aligned_transformed_observations_fingerprint": result["aligned_transformed_observations_fingerprint"],
        "calculation_terms": result["calculation_terms"],
        "calculation_result_fingerprint": result["result_fingerprint"],
        "prior_embedded_diagnostic_reconciliation": reconciliation,
        "limitations": result["limitations"],
    }
    calc["calculation_summary_fingerprint"] = sha256_value(calc)
    return calc


def calculate_campaign43(root: Path, *, write_artifacts: bool = False, weird_decimal_context: bool = False) -> dict[str, Any]:
    before_hashes = object_hashes(root)
    gate = pre_execution_gate(root)
    if not gate["valid"]:
        failed = [c for c in gate["checks"] if not c["pass"]]
        raise ValueError(f"pre-execution gate failed: {failed}")
    registry, spec = load_inputs(root)
    entries = registry["entries"]
    results = [compute_candidate(root, entry, weird_decimal_context=weird_decimal_context) for entry in entries]
    after_hashes = object_hashes(root)
    repository_after = repository_baseline(root)
    immutability = {
        "valid": before_hashes == after_hashes,
        "before_count": len(before_hashes),
        "after_count": len(after_hashes),
        "changed_object_files": sorted(name for name in set(before_hashes) | set(after_hashes) if before_hashes.get(name) != after_hashes.get(name)),
    }
    prior_diagnostic_mismatches = [
        r for r in results
        if r["prior_embedded_diagnostic_reconciliation"]["prior_embedded_diagnostic_present"]
        and r["prior_embedded_diagnostic_reconciliation"]["coefficient_matches_prior_diagnostic_at_recorded_precision"] is False
    ]
    output = {
        "campaign": "Campaign 43",
        "execution_status": "calculated_not_published_prior_diagnostic_review_required" if prior_diagnostic_mismatches else "calculated_not_published",
        "publication_readiness": "blocked_pending_prior_embedded_diagnostic_mismatch_review" if prior_diagnostic_mismatches else "ready_for_separately_authorized_publication_preflight",
        "prior_embedded_diagnostic_mismatch_count": len(prior_diagnostic_mismatches),
        "prior_embedded_diagnostic_mismatches": [
            {
                "candidate_id": r["candidate_id"],
                "relationship_label": r["relationship_label"],
                "source_raw_package_id": r["source_raw_package_id"],
                "prior_embedded_first_difference_coefficient": r["prior_embedded_diagnostic_reconciliation"]["prior_embedded_first_difference_coefficient"],
                "new_companion_coefficient": r["coefficient"]["canonical"],
            }
            for r in prior_diagnostic_mismatches
        ],
        "canonical_publication_performed": False,
        "postgresql_projection_performed": False,
        "knowledge_object_packages_constructed": False,
        "registry_fingerprint": gate["registry_fingerprint"],
        "specification_fingerprint": gate["specification_fingerprint"],
        "candidate_count": len(results),
        "accepted_calculation_count": len(results),
        "rejected_calculation_count": 0,
        "candidate_results": results,
        "candidate_result_fingerprint": sha256_value(results),
        "repository_before": gate["repository_baseline"],
        "repository_after": repository_after,
        "pre_existing_package_immutability": immutability,
        "expected_companion_package_ids": [r["expected_companion_package_id"] for r in results],
        "method_contract_fingerprint": METHOD_FP,
        "transformation_contract_fingerprint": TRANSFORMATION_FP,
        "validation_registry_fingerprint": VALIDATION_REGISTRY_FP,
    }
    if write_artifacts:
        outdir = root / REPORT_DIR_REL
        write_json(outdir / "calculation_results.json", output)
        write_json(outdir / "pre_execution_gate.json", gate)
        write_json(outdir / "candidate_result_fingerprints.json", {r["candidate_id"]: r["calculation_summary_fingerprint"] for r in results})
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--weird-decimal-context", action="store_true")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    result = calculate_campaign43(root, write_artifacts=args.write_artifacts, weird_decimal_context=args.weird_decimal_context)
    print(json.dumps({
        "execution_status": result["execution_status"],
        "candidate_count": result["candidate_count"],
        "candidate_result_fingerprint": result["candidate_result_fingerprint"],
        "repository_fingerprint": result["repository_after"]["computed_repository_fingerprint"],
        "pre_existing_package_immutability": result["pre_existing_package_immutability"],
        "canonical_publication_performed": result["canonical_publication_performed"],
        "postgresql_projection_performed": result["postgresql_projection_performed"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
