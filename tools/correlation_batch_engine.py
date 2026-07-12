#!/usr/bin/env python3
"""Specification-driven Pearson correlation batch engine.

Reusable end-to-end path for WDI annual scalar Pearson batches. The engine can:

- reproduce historical retained-normalized specs offline;
- acquire WDI HTTPS evidence from declarative acquisition contracts;
- normalize observations through the accepted fixture module;
- validate coefficient-free frozen selections;
- compute, validate, and package accepted Pearson relationships;
- atomically publish accepted packages and rebuild the PostgreSQL projection once.

Campaign-specific Python runners are intentionally unnecessary.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import string
import shutil
import subprocess
import tempfile
import time
from decimal import Decimal, localcontext, getcontext
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_FINGERPRINT = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
ENGINE_CONTRACT = "correlation_batch_engine_v1"

SAFE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
SAFE_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.,:;@+()/'-]*$")
PROVENANCE_TEMPLATE_FIELDS = {"campaign_id", "identity_namespace", "candidate_id", "candidate_id_dash"}
PROVENANCE_REQUIRED_FIELDS = {
    "identity_namespace",
    "statement_id_template",
    "calculation_id_template",
    "evidence_ref_id_template",
    "validation_judgment",
    "statement_origin",
    "lineage_basis",
}


def _contains_path_like(value: str) -> bool:
    text = str(value)
    lowered = text.lower()
    if any(marker in lowered for marker in ("/home/", "\\\\", "../", "./", "file://")):
        return True
    if re.search(r"(^|\s)[A-Za-z]:[\\/]", text):
        return True
    return False


def _validate_safe_identifier(value: str, *, field: str) -> None:
    if not isinstance(value, str) or not SAFE_ID_RE.fullmatch(value):
        raise ValueError(f"unsafe or malformed provenance identifier {field}: {value!r}")
    if _contains_path_like(value):
        raise ValueError(f"path-like provenance identifier {field}: {value!r}")
    if value in {"macroforge", "insightforge"}:
        raise ValueError(f"consumer-project terminology not allowed in provenance identifier {field}: {value!r}")


def _validate_safe_label(value: str, *, field: str) -> None:
    if not isinstance(value, str) or not value.strip() or not SAFE_LABEL_RE.fullmatch(value):
        raise ValueError(f"unsafe or malformed provenance label {field}: {value!r}")
    if _contains_path_like(value):
        raise ValueError(f"path-like provenance label {field}: {value!r}")
    if re.search(r"\b(MacroForge|InsightForge)\b", value):
        raise ValueError(f"consumer-project terminology not allowed in provenance label {field}: {value!r}")
    lowered = value.lower()
    if any(token in lowered for token in ("{coefficient", "{correlation", "{p_value", "{significance")):
        raise ValueError(f"outcome-derived template field not allowed in provenance label {field}: {value!r}")


def _template_fields(template: str) -> set[str]:
    fields: set[str] = set()
    for _, field_name, _, _ in string.Formatter().parse(template):
        if field_name is not None:
            fields.add(field_name)
    return fields


def _render_template(template: str, context: dict[str, str], *, field: str) -> str:
    fields = _template_fields(template)
    unknown = sorted(fields - PROVENANCE_TEMPLATE_FIELDS)
    if unknown:
        raise ValueError(f"unknown template field(s) in {field}: {unknown}")
    rendered = template.format(**context)
    _validate_safe_identifier(rendered, field=field)
    return rendered


def provenance_metadata(spec: dict[str, Any]) -> dict[str, Any]:
    metadata = spec.get("package_provenance")
    if not isinstance(metadata, dict):
        raise ValueError("missing required package_provenance metadata")
    missing = sorted(PROVENANCE_REQUIRED_FIELDS - set(metadata))
    if missing:
        raise ValueError(f"missing required package_provenance field(s): {missing}")
    extra = sorted(set(metadata) - (PROVENANCE_REQUIRED_FIELDS | {"production_family_identity"}))
    if extra:
        raise ValueError(f"unsupported package_provenance field(s): {extra}")
    _validate_safe_identifier(str(metadata["identity_namespace"]), field="identity_namespace")
    for field in ("statement_id_template", "calculation_id_template", "evidence_ref_id_template"):
        if not isinstance(metadata[field], str) or not metadata[field].strip():
            raise ValueError(f"missing provenance template {field}")
        unknown = sorted(_template_fields(metadata[field]) - PROVENANCE_TEMPLATE_FIELDS)
        if unknown:
            raise ValueError(f"unknown template field(s) in {field}: {unknown}")
    for field in ("validation_judgment", "statement_origin"):
        _validate_safe_identifier(str(metadata[field]), field=field)
    _validate_safe_label(str(metadata["lineage_basis"]), field="lineage_basis")
    if metadata.get("production_family_identity") is not None:
        _validate_safe_identifier(str(metadata["production_family_identity"]), field="production_family_identity")
    return metadata


def candidate_provenance_ids(spec: dict[str, Any], candidate: dict[str, Any]) -> dict[str, str]:
    metadata = provenance_metadata(spec)
    cid = candidate["candidate_id"]
    _validate_safe_identifier(cid, field="candidate_id")
    context = {
        "campaign_id": str(spec["campaign_id"]),
        "identity_namespace": str(metadata["identity_namespace"]),
        "candidate_id": cid,
        "candidate_id_dash": cid.replace("_", "-"),
    }
    ids = {
        "statement_id": _render_template(metadata["statement_id_template"], context, field="statement_id_template"),
        "calculation_id": _render_template(metadata["calculation_id_template"], context, field="calculation_id_template"),
        "evidence_ref_id": _render_template(metadata["evidence_ref_id_template"], context, field="evidence_ref_id_template"),
        "validation_judgment": str(metadata["validation_judgment"]),
        "statement_origin": str(metadata["statement_origin"]),
        "lineage_basis": str(metadata["lineage_basis"]),
    }
    expected_package_id = candidate.get("expected_package_id", "")
    namespace = str(metadata["identity_namespace"])
    if f"srcpkg-{namespace}-" not in expected_package_id:
        raise ValueError(f"campaign/package identity inconsistency for {cid}: expected package id does not contain srcpkg-{namespace}-")
    if namespace not in ids["statement_id"] or namespace not in ids["calculation_id"] or namespace not in ids["evidence_ref_id"]:
        raise ValueError(f"provenance IDs for {cid} do not include identity namespace {namespace}")
    return ids


def validate_provenance_metadata(spec: dict[str, Any]) -> dict[str, Any]:
    if not spec.get("candidates"):
        return {"valid": True, "checked": False, "reason": "historical pair-only spec"}
    provenance_metadata(spec)
    seen: dict[str, str] = {}
    generated: list[dict[str, str]] = []
    for candidate in spec["candidates"]:
        ids = candidate_provenance_ids(spec, candidate)
        generated.append({"candidate_id": candidate["candidate_id"], **ids})
        for field in ("statement_id", "calculation_id", "evidence_ref_id"):
            value = ids[field]
            if value in seen:
                raise ValueError(f"duplicate generated provenance id {value!r} for {candidate['candidate_id']} and {seen[value]}")
            seen[value] = candidate["candidate_id"]
    return {"valid": True, "checked": True, "generated_count": len(generated), "generated_ids": generated}



def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text())


def write_json(path: Path | str, value: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolve(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else PROJECT_ROOT / p


def _relative(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path)


def _correlation_module():
    return load_module(PROJECT_ROOT / "tools/deterministic_pearson_correlation_v1.py", "deterministic_pearson_correlation_v1_engine")


def _fixture_module():
    return load_module(PROJECT_ROOT / "tools/wdi_observation_evidence_fixture.py", "wdi_observation_fixture_engine")


def _repository_module():
    return load_module(PROJECT_ROOT / "tools/knowledge_repository.py", "knowledge_repository_engine")


def validate_spec(spec: dict[str, Any]) -> dict[str, Any]:
    if spec.get("engine_contract") != ENGINE_CONTRACT:
        raise ValueError("unsupported spec contract")
    method = spec.get("method", {})
    if method.get("identity") and method["identity"] != "wdi_annual_scalar_pearson_correlation_v1@1.0":
        raise ValueError("unsupported method identity")
    if method.get("contract_fingerprint") and method["contract_fingerprint"] != CONTRACT_FINGERPRINT:
        raise ValueError("method contract fingerprint mismatch")
    if spec.get("selection", {}).get("coefficient_freeze_verified") is False:
        raise ValueError("coefficient-free selection freeze not verified")
    def _forbidden_key_present(value: Any) -> bool:
        if isinstance(value, dict):
            for key, item in value.items():
                key_lower = str(key).lower()
                if key_lower in {"pearson_coefficient", "coefficient", "correlation", "p_value", "significance", "coefficient_magnitude", "coefficient_sign"}:
                    return True
                if _forbidden_key_present(item):
                    return True
        elif isinstance(value, list):
            return any(_forbidden_key_present(item) for item in value)
        return False
    if _forbidden_key_present(spec.get("selection_evidence", {})):
        raise ValueError("selection evidence contains forbidden coefficient field")
    candidates = spec.get("candidates") or spec.get("pairs") or []
    if not candidates:
        raise ValueError("spec contains no candidates")
    provenance_validation = validate_provenance_metadata(spec) if spec.get("candidates") else {"valid": True, "checked": False}
    return {"valid": True, "candidate_count": len(candidates), "spec_fingerprint": sha256_value(spec), "provenance_validation": provenance_validation}


def _series_from_normalized(path: str, pointer: str | None = None) -> dict[str, Any]:
    data = read_json(_resolve(path))
    if pointer:
        for part in pointer.strip("/").split("/"):
            data = data[part]
    if "series_id" in data and "observations" in data:
        return data
    observations = data["observations"]
    first = next(row for row in observations if row.get("observed", True) and row.get("value_canonical") is not None)
    return {
        "series_id": {
            "indicator_code": first["indicator_code"],
            "indicator_name": first.get("indicator_name"),
            "entity_id": first["entity_id"],
            "frequency": first.get("frequency", "annual"),
            "unit": first["unit"],
            "transformation": first.get("transformation", "raw"),
        },
        "observations": observations,
        "normalized_series_fingerprint": data.get("normalized_series_fingerprint") or data.get("normalized_fingerprint") or sha256_value(data),
        "provider_metadata": data.get("provider_metadata"),
        "indicator_metadata": data.get("indicator_metadata"),
        "raw_artifacts": data.get("raw_artifacts"),
    }


def _series_for_entity(normalized: dict[str, Any], entity: str) -> dict[str, Any]:
    observations = [row for row in normalized["observations"] if row["entity_id"] == entity]
    if not observations:
        raise ValueError(f"no observations for entity {entity}")
    first = next((row for row in observations if row.get("indicator_name")), observations[0])
    return {
        "series_id": {
            "indicator_code": first["indicator_code"],
            "indicator_name": first.get("indicator_name"),
            "entity_id": entity,
            "frequency": "annual",
            "unit": first["unit"],
            "transformation": first.get("transformation", "raw"),
        },
        "observations": observations,
        "normalized_series_fingerprint": sha256_value({"entity": entity, "observations": observations, "source": normalized.get("normalized_fingerprint")}),
        "provider_metadata": normalized.get("provider_metadata"),
        "indicator_metadata": normalized.get("indicator_metadata"),
        "raw_artifacts": normalized.get("raw_artifacts"),
        "source_normalized_fingerprint": normalized.get("normalized_fingerprint"),
    }


def _expected_unit_from_name(name: str, fallback: str | None = None) -> str | None:
    text = name or ""
    lower = text.lower()
    if "(% of children ages 12-23 months)" in text:
        return "% of children ages 12-23 months"
    if "(% gross)" in text:
        return "% gross"
    if "(% of gdp)" in lower:
        return "percent of GDP"
    if "(% of population)" in lower:
        return "% of population"
    if "per 100 people" in lower:
        return "per 100 people"
    if "per 100,000 adults" in lower:
        return "per 100,000 adults"
    if "per 1,000 people" in lower:
        return "per 1,000 people"
    if "per 1,000 live births" in lower:
        return "per 1,000 live births"
    if "(years)" in lower:
        return "years"
    if "births per woman" in lower:
        return "births per woman"
    if "% of total" in lower:
        return "% of total"
    if "% of land area" in lower:
        return "% of land area"
    if "kg of oil equivalent per capita" in lower:
        return "kg of oil equivalent per capita"
    return fallback


def _patch_unit_resolution(raw: dict[str, Any], expected_unit: str | None) -> dict[str, Any]:
    """Preserve accepted fixture normalization while adding deterministic name-derived WDI units."""
    if not expected_unit:
        return raw
    metadata = raw["provider_payloads"]["indicator_metadata"][1][0]
    metadata = dict(metadata)
    if not str(metadata.get("unit") or "").strip():
        metadata["unit"] = expected_unit
        raw = json.loads(json.dumps(raw))
        raw["provider_payloads"]["indicator_metadata"][1][0] = metadata
    return raw


def acquire_indicator_fixture(contract: dict[str, Any], fixture_root: Path, *, offline_reuse: bool = False) -> dict[str, Any]:
    fixture = _fixture_module()
    indicator = contract["indicator"]
    entities = contract.get("entities") or [contract["entity"]]
    start = contract["period"]["start"]
    end = contract["period"]["end"]
    key = f"{indicator}__{'-'.join(sorted(entities))}__{start}-{end}"
    out_dir = fixture_root / key
    if offline_reuse and (out_dir / "normalized_observations.json").exists():
        normalized = read_json(out_dir / "normalized_observations.json")
        return {"status": "reused_offline_fixture", "fixture_dir": _relative(out_dir), "normalized": normalized, "validation": fixture.validate_normalized_fixture(normalized)}
    selection = fixture.build_selection_contract(indicator_code=indicator, entities=entities, start_year=start, end_year=end)
    if not selection["request"]["observation_url"].startswith("https://") or not selection["request"]["indicator_metadata_url"].startswith("https://"):
        raise ValueError("HTTPS requirement failed")
    raw, observation_bytes, metadata_bytes = fixture.acquire_raw_fixture(selection)
    metadata = raw["provider_payloads"]["indicator_metadata"][1][0]
    expected_unit = contract.get("expected_unit") or _expected_unit_from_name(metadata.get("name") or "")
    raw = _patch_unit_resolution(raw, expected_unit)
    out_dir.mkdir(parents=True, exist_ok=True)
    validation = fixture.write_fixture_artifacts(raw, out_dir, observation_bytes, metadata_bytes)
    normalized = read_json(out_dir / "normalized_observations.json")
    manifest = read_json(out_dir / "acquisition_manifest.json")
    return {"status": "acquired", "fixture_dir": _relative(out_dir), "normalized": normalized, "validation": validation, "manifest": manifest}


def acquire_all(spec: dict[str, Any], fixture_root: Path, *, offline_reuse: bool = False) -> dict[str, Any]:
    acquired: dict[str, Any] = {}
    failures: dict[str, str] = {}
    for candidate in spec.get("candidates", []):
        for side in ("series_a", "series_b"):
            acq = candidate[side]["acquisition"]
            key = sha256_value({"indicator": acq["indicator"], "entities": acq.get("entities") or [acq["entity"]], "period": acq["period"]})
            if key in acquired or key in failures:
                continue
            try:
                acquired[key] = acquire_indicator_fixture(acq, fixture_root, offline_reuse=offline_reuse)
            except Exception as exc:
                failures[key] = str(exc)
    return {"acquired": acquired, "failures": failures, "request_count": len(acquired) + len(failures), "deduplicated_request_count": len(acquired)}


def _acq_key(acq: dict[str, Any]) -> str:
    return sha256_value({"indicator": acq["indicator"], "entities": acq.get("entities") or [acq["entity"]], "period": acq["period"]})


def _alignment_summary(series_a: dict[str, Any], series_b: dict[str, Any], expected_periods: list[int]) -> dict[str, Any]:
    a = {int(o["period"]): o for o in series_a["observations"]}
    b = {int(o["period"]): o for o in series_b["observations"]}
    aligned = [y for y in expected_periods if a.get(y, {}).get("value_canonical") is not None and b.get(y, {}).get("value_canonical") is not None]
    missing_a = [y for y in expected_periods if a.get(y, {}).get("value_canonical") is None]
    missing_b = [y for y in expected_periods if b.get(y, {}).get("value_canonical") is None]
    vals_a = [a[y]["value_canonical"] for y in aligned]
    vals_b = [b[y]["value_canonical"] for y in aligned]
    return {
        "expected_periods": expected_periods,
        "aligned_periods": aligned,
        "aligned_pair_count": len(aligned),
        "aligned_coverage": str(Decimal(len(aligned)) / Decimal(len(expected_periods))) if expected_periods else "0",
        "missing_periods": {"series_a": missing_a, "series_b": missing_b},
        "series_a_nonconstant": len(set(vals_a)) > 1,
        "series_b_nonconstant": len(set(vals_b)) > 1,
    }


def _construction_risk(candidate: dict[str, Any]) -> dict[str, Any]:
    risk = candidate.get("construction_risk", {})
    blockers = [k for k, v in risk.items() if v == "promotion blocker"]
    for key in ("algebraic_identity", "direct_component_total_construction", "embedded_series_construction"):
        if risk.get(key) == "present" or risk.get(key) == "promotion blocker":
            blockers.append(key)
    return {"assessment": risk, "promotion_blocker_present": bool(blockers), "promotion_blockers": sorted(set(blockers))}


def _time_series(periods: list[int], entity_id: str) -> dict[str, Any]:
    return {"series_id": {"indicator_code": "diagnostic_only_annual_time_index", "entity_id": entity_id, "frequency": "annual", "unit": "year", "transformation": "raw", "diagnostic_only": True}, "observations": [{"period": y, "value_canonical": str(y), "observed": True, "unit": "year", "frequency": "annual", "entity_id": entity_id} for y in periods]}


def _diff_series(series: dict[str, Any]) -> dict[str, Any]:
    rows = sorted([o for o in series["observations"] if o.get("value_canonical") is not None], key=lambda x: x["period"])
    obs = []
    previous = None
    for row in rows:
        if previous is not None:
            obs.append({"period": row["period"], "value_canonical": str(Decimal(row["value_canonical"]) - Decimal(previous["value_canonical"])), "observed": True, "unit": series["series_id"].get("unit"), "frequency": "annual"})
        previous = row
    sid = dict(series["series_id"]); sid["transformation"] = "first_difference"
    return {"series_id": sid, "observations": obs}


def _diagnostics(corr: Any, series_a: dict[str, Any], series_b: dict[str, Any], aligned_periods: list[int]) -> dict[str, Any]:
    diag = {}
    try:
        t = _time_series(aligned_periods, series_a["series_id"].get("entity_id"))
        diag["series_a_vs_time_index"] = corr.compute_correlation(series_a, t)["coefficient"]["canonical"]
        diag["series_b_vs_time_index"] = corr.compute_correlation(series_b, t)["coefficient"]["canonical"]
    except Exception as exc:
        diag["time_index_error"] = str(exc)
    try:
        da, db = _diff_series(series_a), _diff_series(series_b)
        if len(da["observations"]) >= 30 and len(db["observations"]) >= 30:
            diag["first_difference_pearson"] = corr.compute_correlation(da, db)["coefficient"]["canonical"]
        else:
            diag["first_difference_pearson"] = "insufficient aligned first differences"
    except Exception as exc:
        diag["first_difference_error"] = str(exc)
    diag["promoted_as_knowledge_object"] = False
    return diag


def compute_pair(pair: dict[str, Any]) -> dict[str, Any]:
    corr = _correlation_module()
    contract = corr.calculation_contract_v1()
    if contract["calculation_contract_fingerprint"] != CONTRACT_FINGERPRINT:
        raise ValueError("method-contract fingerprint mismatch")
    series_a = _series_from_normalized(pair["series_a"]["normalized_path"], pair["series_a"].get("json_pointer"))
    series_b = _series_from_normalized(pair["series_b"]["normalized_path"], pair["series_b"].get("json_pointer"))
    result = corr.compute_correlation(series_a, series_b)
    swapped = corr.compute_correlation(series_b, series_a)
    if result["coefficient"] != swapped["coefficient"] or result["canonical_pair_id"] != swapped["canonical_pair_id"]:
        raise ValueError(f"pair-order invariance failed for {pair['pair_id']}")
    expected = pair.get("expected_coefficient")
    if expected is not None and result["coefficient"]["canonical"] != expected:
        raise ValueError(f"coefficient mismatch for {pair['pair_id']}: {result['coefficient']['canonical']} != {expected}")
    package_path = _resolve(pair["historical_package_path"])
    package_fp = sha256_bytes(package_path.read_bytes()) if package_path.exists() else None
    expected_package_fp = pair.get("expected_full_package_fingerprint")
    if expected_package_fp is not None and package_fp != expected_package_fp:
        raise ValueError(f"historical package fingerprint mismatch for {pair['pair_id']}")
    return {"pair_id": pair["pair_id"], "historical_package_id": pair["historical_package_id"], "coefficient": result["coefficient"]["canonical"], "aligned_pair_count": result["aligned_pair_count"], "aligned_coverage": result["coverage_share"]["canonical"], "canonical_pair_id": result["canonical_pair_id"], "output_fingerprint": result["output_fingerprint"], "swapped_output_fingerprint": swapped["output_fingerprint"], "series_a_fingerprint": series_a.get("normalized_series_fingerprint") or sha256_value(series_a), "series_b_fingerprint": series_b.get("normalized_series_fingerprint") or sha256_value(series_b), "historical_package_fingerprint": package_fp, "status": "reproduced_offline_no_promote"}


def run_spec(spec_path: Path | str, *, continue_on_failure: bool = True) -> dict[str, Any]:
    spec_path = _resolve(str(spec_path)); spec = read_json(spec_path); validate_spec(spec)
    results = []; failures = []
    for pair in spec.get("pairs", []):
        try: results.append(compute_pair(pair))
        except Exception as exc:
            failures.append({"pair_id": pair.get("pair_id"), "error": str(exc), "status": "failed_isolated"})
            if not continue_on_failure: break
    summary = {"spec_path": _relative(spec_path), "spec_fingerprint": sha256_value(spec), "engine_contract": spec["engine_contract"], "method_contract_fingerprint": CONTRACT_FINGERPRINT, "pair_count": len(spec.get("pairs", [])), "success_count": len(results), "failure_count": len(failures), "results": results, "failures": failures, "publication_performed": False}
    summary["result_fingerprint"] = sha256_value(summary); return summary


def _package_fingerprint_fields(package: dict[str, Any]) -> dict[str, str]:
    return {"input_set": sha256_value(package.get("input_references", [])), "query_definitions": sha256_value(package.get("scope", {})), "evidence_references": sha256_value(package.get("evidence_references", [])), "generated_statements": sha256_value(package.get("generated_statements", [])), "computation_recipe": sha256_value(package.get("provenance_envelope", {})), "package_manifest": sha256_value({k: v for k, v in package.items() if k != "fingerprints"})}


def _campaign_label(spec: dict[str, Any]) -> str:
    namespace = str(provenance_metadata(spec).get("identity_namespace", spec.get("campaign_id", "campaign")))
    match = re.fullmatch(r"campaign([0-9]+)", namespace)
    if match:
        return f"Campaign {match.group(1)}"
    return namespace.replace("_", " ").title()


def build_package(spec: dict[str, Any], candidate: dict[str, Any], result: dict[str, Any], diagnostics: dict[str, Any], fixture_fp: str) -> dict[str, Any]:
    today = spec.get("publication_date", "2026-07-11")
    cid = candidate["candidate_id"]
    package_id = candidate["expected_package_id"]
    entity = candidate["entity"]
    period = candidate["period"]
    family = candidate["family"]
    ids = candidate_provenance_ids(spec, candidate)
    campaign_label = _campaign_label(spec)
    stmt_id = ids["statement_id"]
    calc_id = ids["calculation_id"]
    ev_id = ids["evidence_ref_id"]
    payload = {
        "family": family,
        "entity_id": entity,
        "series_a": candidate["series_a"]["identity"],
        "series_b": candidate["series_b"]["identity"],
        "period_scope": period,
        "frequency": "annual",
        "transformation_state": "raw",
        "aligned_pair_count": result["aligned_pair_count"],
        "aligned_coverage": result["coverage_share"]["canonical"],
        "missing_periods": result["alignment_summary"]["missing_periods"],
        "pearson_coefficient": {"canonical": result["coefficient"]["canonical"], "unit": "dimensionless"},
        "method_contract_fingerprint": CONTRACT_FINGERPRINT,
        "calculation_evidence_fingerprint": result["output_fingerprint"],
        "fixture_fingerprint": fixture_fp,
        "frozen_batch_selection_fingerprint": spec["selection"]["frozen_selection_fingerprint"],
        "construction_risk_assessment": result["construction_risk"],
        "diagnostic_limitations": diagnostics,
        "mutable_source_limitation": "WDI API is mutable; retained raw bytes and normalized fixture provide exact offline reproducibility for this package.",
        "validation_judgment": ids["validation_judgment"],
    }
    statement = {"statement_id": stmt_id, "statement_type": "derived_relationship", "text": f"Across aligned annual {entity} observations from {period['start']} through {period['end']}, the Pearson correlation between {candidate['series_a']['identity']['name']} and {candidate['series_b']['identity']['name']} is {result['coefficient']['canonical']}, using {result['aligned_pair_count']} aligned observations.", "structured_payload": payload, "applicability": {"entity_id": entity, "frequency": "annual", "method_id": "wdi_annual_scalar_pearson_correlation_v1", "method_version": "1.0", "period_start": period["start"], "period_end": period["end"]}, "dependencies": [calc_id], "evidence_refs": [ev_id], "origin": ids["statement_origin"]}
    warnings = [k for k, v in result["construction_risk"].get("assessment", {}).items() if v in {"material limitation", "ordinary limitation"}] + ["no causal/predictive/significance interpretation"]
    package = {"package_id": package_id, "package_kind": "KnowledgeObjectPackage", "package_version": "1.0", "created_at": today, "created_by": "correlation_batch_engine", "status": "accepted", "scope": {"domain": "world_development_indicators", "entity_scope": [entity], "evidence_family": f"external_wdi_annual_scalar_{family.lower().replace(' & ', '_').replace(' ', '_')}_pearson_correlation", "period_scope": period}, "input_references": [spec["campaign_id"], spec["selection"]["frozen_selection_fingerprint"], CONTRACT_FINGERPRINT], "evidence_references": [{"evidence_ref_id": ev_id, "source_family": "official_statistical_source_data", "source_owner": "World Bank WDI API retained local fixture", "source_identity": f"World Bank WDI {candidate['series_a']['identity']['code']} and {candidate['series_b']['identity']['code']} {entity} annual {period['start']}-{period['end']} fixture", "source_version": result.get("provider_lastupdated"), "snapshot_fingerprint": fixture_fp, "evaluation_status": "evaluated", "evidence_class": "external_dual_series_observation_level_numerical_fixture", "reproducibility_handle": "retained HTTPS raw fixture, normalized series, alignment and calculation evidence", "accessed_at": today}], "generated_statements": [statement], "provenance_envelope": {"method_refs": ["wdi_annual_scalar_pearson_correlation_v1@1.0"], "evidence_refs": [ev_id], "evaluation_refs": [spec["selection"]["frozen_selection_fingerprint"], result["output_fingerprint"]], "lineage_basis": ids["lineage_basis"]}, "confidence_quality": {"confidence_label": "fixture-supported-deterministic", "evidence_sufficiency": "sufficient for bounded deterministic Pearson correlation object", "validation_state": "pass", "lifecycle_state": "accepted", "reproducibility_state": "reproducible_offline_from_retained_fixture", "uncertainty_dimensions": ["non-causality", "non-prediction", "absence of significance testing", "transformation sensitivity", "common time-ordering risk"]}, "validation_state": {"validation_result": "pass", "blockers": [], "warnings": warnings}, "contradiction_records": [{"contradiction_id": "none-recorded", "contradiction_type": "none", "target_statement": stmt_id, "contradicting_evidence": None, "disposition": "not_applicable"}], "evidence_integrity": {"evidence_refs_verified": True, "fingerprints_verified": True, "source_package_fingerprint": fixture_fp}, "evolution_metadata": {"change_reason": f"{campaign_label} end-to-end specification-driven Pearson production batch", "previous_revision": None, "version_lineage": [], "dependent_object_review_posture": "not_applicable"}, "lineage": {"source_campaign": campaign_label, "previous_package_id": None, "version_lineage": []}}
    package["fingerprints"] = _package_fingerprint_fields(package)
    package["generated_statements"][0]["structured_payload"]["package_fingerprint"] = package["fingerprints"]["package_manifest"]
    package["fingerprints"] = _package_fingerprint_fields(package)
    return package


def validate_packages_for_atomic_publication(packages: list[dict[str, Any]]) -> None:
    kr = _repository_module()
    ids = [p.get("package_id") for p in packages]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate package IDs in publication plan")
    for package in packages:
        kr._require_validated_knowledge_object(package)


def atomic_publish_to_repository(packages: list[dict[str, Any]], repository_root: Path | str) -> dict[str, Any]:
    target = Path(repository_root); validate_packages_for_atomic_publication(packages)
    existing = target / "objects"
    if existing.exists():
        collisions = [p["package_id"] for p in packages if (existing / f"{p['package_id']}.json").exists()]
        if collisions: raise ValueError(f"package-ID collisions: {collisions}")
    kr = _repository_module(); parent = target.parent; parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{target.name}.stage-", dir=parent) as td:
        stage = Path(td) / "repo"
        if target.exists(): shutil.copytree(target, stage)
        kr.persist_knowledge_object_packages(packages, stage)
        if target.exists(): shutil.rmtree(target)
        shutil.move(str(stage), str(target))
    manifest = read_json(target / "manifest.json")
    return {"published_count": len(packages), "repository_root": str(target), "object_count": manifest["object_count"], "repository_fingerprint": manifest["repository_fingerprint"]}


def run_production_spec(spec_path: str | Path, *, output_dir: str | Path, fixture_dir: str | Path, publish: bool = False, offline_reuse: bool = False, rebuild_postgres: bool = False, database: str = "knowledgeforge") -> dict[str, Any]:
    started = time.time(); spec_path = _resolve(spec_path); spec = read_json(spec_path); spec_validation = validate_spec(spec)
    output_dir = _resolve(output_dir); fixture_dir = _resolve(fixture_dir); output_dir.mkdir(parents=True, exist_ok=True)
    before_manifest = read_json(PROJECT_ROOT / "knowledge_repository/manifest.json")
    before_hashes = {p.name: sha256_bytes(p.read_bytes()) for p in sorted((PROJECT_ROOT / "knowledge_repository/objects").glob("*.json"))}
    acquisition_started = time.time(); acquisition = acquire_all(spec, fixture_dir, offline_reuse=offline_reuse); acquisition_seconds = time.time() - acquisition_started
    corr = _correlation_module(); accepted=[]; rejected=[]; candidate_results=[]
    for candidate in spec["candidates"]:
        cid = candidate["candidate_id"]
        try:
            ka, kb = _acq_key(candidate["series_a"]["acquisition"]), _acq_key(candidate["series_b"]["acquisition"])
            if ka in acquisition["failures"] or kb in acquisition["failures"]:
                raise ValueError("dependent acquisition failed")
            sa = _series_for_entity(acquisition["acquired"][ka]["normalized"], candidate["entity"])
            sb = _series_for_entity(acquisition["acquired"][kb]["normalized"], candidate["entity"])
            expected = list(range(candidate["period"]["start"], candidate["period"]["end"] + 1))
            align = _alignment_summary(sa, sb, expected)
            risk = _construction_risk(candidate)
            threshold = candidate.get("thresholds", spec.get("thresholds", {}))
            if align["aligned_pair_count"] < threshold.get("min_aligned_pairs", 30): raise ValueError("aligned pairs below threshold")
            if Decimal(align["aligned_coverage"]) < Decimal(str(threshold.get("min_aligned_coverage", "0.85"))): raise ValueError("aligned coverage below threshold")
            if not align["series_a_nonconstant"] or not align["series_b_nonconstant"]: raise ValueError("constant series / zero variance")
            if risk["promotion_blocker_present"]: raise ValueError("construction-risk promotion blocker")
            calc = corr.compute_correlation(sa, sb); recompute = corr.compute_correlation(sa, sb); swapped = corr.compute_correlation(sb, sa)
            if calc["coefficient"] != recompute["coefficient"]: raise ValueError("independent recomputation failed")
            if calc["coefficient"] != swapped["coefficient"]: raise ValueError("pair-order invariance failed")
            old_prec = getcontext().prec
            with localcontext() as ctx:
                ctx.prec = old_prec + 10
                decimal_check = corr.compute_correlation(sa, sb)
            if calc["coefficient"] != decimal_check["coefficient"]: raise ValueError("Decimal-context invariance failed")
            calc["alignment_summary"] = align; calc["construction_risk"] = risk
            fixture_fp = sha256_value({"a": acquisition["acquired"][ka]["normalized"].get("normalized_fingerprint"), "b": acquisition["acquired"][kb]["normalized"].get("normalized_fingerprint"), "candidate": cid})
            calc["provider_lastupdated"] = acquisition["acquired"][ka]["normalized"].get("provider_metadata", {}).get("wdi_lastupdated")
            diagnostics = _diagnostics(corr, sa, sb, align["aligned_periods"])
            package = build_package(spec, candidate, calc, diagnostics, fixture_fp)
            accepted.append(package)
            write_json(output_dir / "accepted_packages" / f"{package['package_id']}.json", package)
            candidate_results.append({"candidate_id": cid, "status": "accepted", "coefficient": calc["coefficient"]["canonical"], "aligned_pair_count": calc["aligned_pair_count"], "aligned_coverage": calc["coverage_share"]["canonical"], "missing_periods": align["missing_periods"], "diagnostics": diagnostics, "package_id": package["package_id"]})
            write_json(output_dir / f"{cid}_calculation.json", calc)
        except Exception as exc:
            judgment = {"candidate_id": cid, "status": "rejected", "reason": str(exc), "preserved": True, "thresholds": candidate.get("thresholds", spec.get("thresholds", {})), "construction_risk": candidate.get("construction_risk")}
            rejected.append(judgment); candidate_results.append(judgment)
    publication = {"performed": False}
    pg = {"performed": False}
    publication_started = time.time()
    if publish and accepted:
        validate_packages_for_atomic_publication(accepted)
        publication_plan = {"accepted_package_ids": [p["package_id"] for p in accepted], "rejected_candidate_ids": [r["candidate_id"] for r in rejected], "before_count": before_manifest["object_count"], "before_fingerprint": before_manifest["repository_fingerprint"]}
        write_json(output_dir / "publication_plan.json", publication_plan)
        publication = atomic_publish_to_repository(accepted, PROJECT_ROOT / "knowledge_repository")
    publication_seconds = time.time() - publication_started
    pg_started = time.time()
    if publish and rebuild_postgres:
        proc = subprocess.run(["python3", "tools/postgresql_operational_projection.py", "--database", database, "--repository-root", "knowledge_repository", "rebuild"], cwd=PROJECT_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pg = {"performed": True, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "stale_if_failed": proc.returncode != 0}
        if proc.returncode != 0: write_json(output_dir / "postgresql_stale_marker.json", pg)
    pg_seconds = time.time() - pg_started
    after_manifest = read_json(PROJECT_ROOT / "knowledge_repository/manifest.json")
    after_hashes = {p.name: sha256_bytes(p.read_bytes()) for p in sorted((PROJECT_ROOT / "knowledge_repository/objects").glob("*.json"))}
    changed_existing = [name for name, fp in before_hashes.items() if after_hashes.get(name) != fp]
    disappeared = [name for name in before_hashes if name not in after_hashes]
    added = [name for name in after_hashes if name not in before_hashes]
    summary = {"engine_contract": ENGINE_CONTRACT, "campaign_id": spec.get("campaign_id"), "spec_path": _relative(spec_path), "spec_fingerprint": spec_validation["spec_fingerprint"], "selection_fingerprint": spec.get("selection", {}).get("frozen_selection_fingerprint"), "candidate_count": len(spec["candidates"]), "accepted_count": len(accepted), "rejected_count": len(rejected), "candidate_results": candidate_results, "acquisition": {k:v for k,v in acquisition.items() if k != "acquired"}, "acquired_fixture_count": len(acquisition["acquired"]), "publication": publication, "postgresql": pg, "repository_before": before_manifest, "repository_after": after_manifest, "historical_immutability": {"valid": not changed_existing and not disappeared, "changed_existing": changed_existing, "disappeared_existing": disappeared, "added": added}, "durations_seconds": {"acquisition": round(acquisition_seconds, 3), "publication": round(publication_seconds, 3), "postgresql": round(pg_seconds, 3), "total": round(time.time() - started, 3)}, "offline_reuse": offline_reuse, "publish": publish}
    summary["result_fingerprint"] = sha256_value(summary)
    write_json(output_dir / "consolidated_machine_readable_report.json", summary)
    write_json(output_dir / "candidate_judgments.json", candidate_results)
    return summary


def run_specs(spec_paths: list[str]) -> dict[str, Any]:
    runs = [run_spec(p) for p in spec_paths]
    return {"engine_contract": ENGINE_CONTRACT, "spec_run_count": len(runs), "runs": runs, "overall_success": all(r["failure_count"] == 0 for r in runs)}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")
    hist = sub.add_parser("historical")
    hist.add_argument("spec", nargs="+"); hist.add_argument("--output")
    prod = sub.add_parser("production")
    prod.add_argument("--spec", required=True); prod.add_argument("--output-dir", required=True); prod.add_argument("--fixture-dir", required=True)
    prod.add_argument("--publish", action="store_true"); prod.add_argument("--offline-reuse", action="store_true"); prod.add_argument("--rebuild-postgres", action="store_true"); prod.add_argument("--database", default="knowledgeforge")
    args = parser.parse_args()
    if args.command == "production":
        result = run_production_spec(args.spec, output_dir=args.output_dir, fixture_dir=args.fixture_dir, publish=args.publish, offline_reuse=args.offline_reuse, rebuild_postgres=args.rebuild_postgres, database=args.database)
        print(json.dumps(result, indent=2, sort_keys=True)); return 0 if result.get("rejected_count", 0) >= 0 else 1
    specs = args.spec if args.command == "historical" else []
    if not specs:
        parser.error("command required: production or historical")
    result = run_specs(specs)
    if args.output: write_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True)); return 0 if result["overall_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
