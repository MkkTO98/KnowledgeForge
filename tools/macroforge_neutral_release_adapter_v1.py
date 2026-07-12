#!/usr/bin/env python3
"""KnowledgeForge-owned adapter for MacroForge neutral evidence-release exports v1.

This module consumes transferred serialized files only. It does not import
MacroForge code, query MacroForge PostgreSQL, or depend on MacroForge private
schemas. Producer fingerprints are validated before any transformation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_CONTRACT = "macroforge.neutral_evidence_release_export.v1"
SUPPORTED_VERSION = "1.0"
ADAPTER_ID = "knowledgeforge_macroforge_neutral_release_adapter_v1"
ADAPTER_VERSION = "1.0"
EXPECTED_SELECTION = {
    "provider_dataset_code": "WDI",
    "indicators": ["NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"],
    "entities": ["DNK", "SWE", "NOR"],
    "periods": [str(y) for y in range(1990, 2025)],
    "frequency": "annual",
}
EXPECTED_EXPORT_SHA256 = "1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86"
EXPECTED_RELEASE_FINGERPRINT = "sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67"
EXPECTED_SELECTION_FINGERPRINT = "sha256:2b1a1c3d9e65b182f073e0171c59627c8298740ee9cb7c1418dfbae3ae196e0a"
RELEASE_INBOX = ROOT / "tools" / "release_inbox_v1.py"
CALC_PATHS = {
    "DNK": ROOT / "artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/calculation_evidence.json",
    "SWE": ROOT / "artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/swe_calculation_evidence.json",
    "NOR": ROOT / "artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/nor_calculation_evidence.json",
}
EXPECTED_COEFFICIENTS = {
    "DNK": "0.988873850642",
    "SWE": "0.968490740983",
    "NOR": "-0.477418804478",
}
FORBIDDEN_TERMS = [
    "curated.", "meta.", "staging.", "dataset_release_id", "pipeline_run_id", "source_id",
    "postgres://", "postgresql://", "password", "credential", "srv/EIP/projects/MacroForge",
    "srv/EIP/projects/KnowledgeForge", "InsightForge", "KnowledgeForge private PostgreSQL",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text())


def write_json(path: Path | str, value: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_release_inbox():
    spec = importlib.util.spec_from_file_location("knowledgeforge_release_inbox_v1", RELEASE_INBOX)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load KnowledgeForge release inbox")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def producer_item_without_fingerprint(item: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in item.items() if k != "item_fingerprint"}


def producer_release_without_fingerprint(release: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in release.items() if k not in {"release_fingerprint", "operational_metadata"}}


def leakage_scan_text(text: str) -> dict[str, Any]:
    leaks = [term for term in FORBIDDEN_TERMS if term in text]
    return {"valid": not leaks, "leaks": leaks, "terms_checked": FORBIDDEN_TERMS}


def validate_macroforge_release(export_path: Path | str, manifest_path: Path | str | None = None) -> dict[str, Any]:
    export_path = Path(export_path)
    manifest_path = Path(manifest_path) if manifest_path else None
    errors: list[str] = []
    export_text = export_path.read_text()
    release = json.loads(export_text)
    manifest = read_json(manifest_path) if manifest_path else None
    if release.get("contract_identity") != SUPPORTED_CONTRACT or release.get("contract_version") != SUPPORTED_VERSION:
        errors.append("unsupported_contract_or_version")
    for field in ["release_identity", "selection", "selection_fingerprint", "release_fingerprint", "items", "original_provider", "release_metadata", "producing_system"]:
        if field not in release:
            errors.append(f"missing_release_field:{field}")
    export_sha = sha256_file(export_path)
    if export_sha != EXPECTED_EXPORT_SHA256:
        errors.append("export_sha256_unexpected")
    if manifest:
        if manifest.get("export_sha256") != export_sha:
            errors.append("manifest_export_sha256_mismatch")
        if manifest.get("release_fingerprint") != release.get("release_fingerprint"):
            errors.append("manifest_release_fingerprint_mismatch")
        if manifest.get("selection_fingerprint") != release.get("selection_fingerprint"):
            errors.append("manifest_selection_fingerprint_mismatch")
        if manifest.get("item_count") != len(release.get("items", [])):
            errors.append("manifest_item_count_mismatch")
    if release.get("selection") != EXPECTED_SELECTION:
        errors.append("unexpected_scope")
    selection_fp = sha256_value(release.get("selection"))
    if selection_fp != release.get("selection_fingerprint"):
        errors.append("selection_fingerprint_mismatch")
    if release.get("selection_fingerprint") != EXPECTED_SELECTION_FINGERPRINT:
        errors.append("selection_fingerprint_unexpected")
    seen = set()
    for item in release.get("items", []):
        for field in ["item_id", "entity", "indicator", "period", "frequency", "unit", "definition", "missing", "observation_status", "item_fingerprint", "provenance"]:
            if field not in item:
                errors.append(f"missing_item_field:{field}:{item.get('item_id','unknown')}")
        key = (item.get("entity"), item.get("indicator"), item.get("period"), item.get("frequency"))
        if key in seen:
            errors.append(f"duplicate_observation_key:{key}")
        seen.add(key)
        if item.get("item_fingerprint") != sha256_value(producer_item_without_fingerprint(item)):
            errors.append(f"item_fingerprint_mismatch:{item.get('item_id')}")
        if item.get("frequency") != "annual":
            errors.append(f"invalid_frequency:{item.get('item_id')}")
        if item.get("unit") != "percent of GDP":
            errors.append(f"ambiguous_or_invalid_unit:{item.get('item_id')}:{item.get('unit')}")
        missing = item.get("missing")
        status = item.get("observation_status")
        if missing is False and status != "observed":
            errors.append(f"invalid_missingness:{item.get('item_id')}")
        if missing is True and item.get("value") is not None:
            errors.append(f"missing_item_has_value:{item.get('item_id')}")
    if len(release.get("items", [])) != 210:
        errors.append("unexpected_item_count")
    if release.get("release_fingerprint") != sha256_value(producer_release_without_fingerprint(release)):
        errors.append("release_fingerprint_mismatch")
    if release.get("release_fingerprint") != EXPECTED_RELEASE_FINGERPRINT:
        errors.append("release_fingerprint_unexpected")
    lineage = release.get("release_metadata", {}).get("lineage", {})
    if "WDI:2026-07-01:1990:2024" not in release.get("release_metadata", {}).get("source_release_keys", []):
        errors.append("missing_source_release_key")
    if "task-176-repository-growth-historical-scaling-rerun" not in release.get("release_metadata", {}).get("source_run_keys", []):
        errors.append("missing_source_run_key")
    if "failed" in release.get("release_metadata", {}).get("run_statuses", []):
        errors.append("failed_source_run")
    leakage = leakage_scan_text(export_text)
    if leakage["leaks"]:
        errors.append("forbidden_content_leakage")
    return {
        "valid": not errors,
        "errors": errors,
        "contract_identity": release.get("contract_identity"),
        "contract_version": release.get("contract_version"),
        "release_identity": release.get("release_identity"),
        "item_count": len(release.get("items", [])),
        "selection_fingerprint": release.get("selection_fingerprint"),
        "computed_selection_fingerprint": selection_fp,
        "release_fingerprint": release.get("release_fingerprint"),
        "computed_release_fingerprint": sha256_value(producer_release_without_fingerprint(release)) if isinstance(release, dict) else None,
        "export_sha256": export_sha,
        "leakage": leakage,
        "lineage": lineage,
    }


def adapt_item(item: dict[str, Any]) -> dict[str, Any]:
    observed = not bool(item["missing"])
    out = {
        "item_id": item["item_id"],
        "provider_id": "world_bank",
        "dataset_id": "world_development_indicators",
        "entity_id": item["entity"],
        "entity_name": item.get("entity_label"),
        "indicator_code": item["indicator"],
        "indicator_name": item.get("indicator_label"),
        "definition": item["definition"],
        "period": int(item["period"]),
        "frequency": item["frequency"],
        "value_canonical": None if not observed else str(item["value"]),
        "unit": item["unit"],
        "observed": observed,
        "missing_reason": None if observed else item.get("observation_status"),
        "source_kind": "macroforge_transferred_neutral_release",
        "producer_item_fingerprint": item["item_fingerprint"],
        "producer_provenance": item["provenance"],
    }
    out["item_fingerprint"] = sha256_value({k: v for k, v in out.items() if k != "item_fingerprint"})
    return out


def adapt_macroforge_release(export_path: Path | str, manifest_path: Path | str | None = None) -> dict[str, Any]:
    validation = validate_macroforge_release(export_path, manifest_path)
    if not validation["valid"]:
        raise ValueError("invalid_macroforge_release:" + ";".join(validation["errors"]))
    release = read_json(export_path)
    items = sorted((adapt_item(i) for i in release["items"]), key=lambda x: (x["entity_id"], x["indicator_code"], x["period"]))
    source_release_keys = release["release_metadata"].get("source_release_keys", [])
    source_run_keys = release["release_metadata"].get("source_run_keys", [])
    adapted = {
        "contract_id": "knowledgeforge_neutral_evidence_release_contract_v1",
        "contract_version": "1.0",
        "release_id": release["release_identity"],
        "release_label": "macroforge_transferred_wdi_trade_share_dnk_swe_nor_1990_2024",
        "provider": {"provider_id": "world_bank", "name": release["original_provider"]["provider_identity"]},
        "dataset": {"dataset_id": "world_development_indicators", "name": release["original_provider"]["dataset_identity"]},
        "source_release_vintage": source_release_keys[0] if len(source_release_keys) == 1 else source_release_keys,
        "published_at": release["release_metadata"].get("lineage", {}).get("provider_release", [None])[0],
        "prior_release_id": release.get("predecessor_release_identity"),
        "supersedes_release_id": release.get("predecessor_release_identity"),
        "source_metadata": {
            "producer": release.get("producing_system"),
            "source_release_keys": source_release_keys,
            "source_run_keys": source_run_keys,
            "run_statuses": release["release_metadata"].get("run_statuses", []),
            "selection": release["selection"],
        },
        "producer_metadata": {
            "producer_contract_identity": release["contract_identity"],
            "producer_contract_version": release["contract_version"],
            "producer_release_id": release["release_identity"],
            "producer_release_fingerprint": release["release_fingerprint"],
            "producer_selection_fingerprint": release["selection_fingerprint"],
            "producer_exporter_version": release.get("exporter_version"),
            "adapter_id": ADAPTER_ID,
            "adapter_version": ADAPTER_VERSION,
            "adapter_output_authority": "KnowledgeForge normalized release only; not producer-authored",
        },
        "provenance_note": "Adapted by KnowledgeForge from a manually transferred MacroForge neutral evidence-release export. MacroForge producer fingerprints are preserved; this normalized representation is KnowledgeForge-authored.",
        "evidence_items": items,
    }
    inbox = load_release_inbox()
    inbox.refresh_release_fingerprints(adapted)
    normalized_fp = sha256_value(adapted)
    return {
        "adapter_identity": f"{ADAPTER_ID}@{ADAPTER_VERSION}",
        "producer_validation": validation,
        "producer_release_fingerprint": release["release_fingerprint"],
        "selection_fingerprint": release["selection_fingerprint"],
        "normalized_release_fingerprint": normalized_fp,
        "knowledgeforge_release": adapted,
    }


def process_adapted_release(export_path: Path | str, manifest_path: Path | str | None, state_root: Path | str) -> dict[str, Any]:
    state_root = Path(state_root)
    adapted = adapt_macroforge_release(export_path, manifest_path)
    normalized_path = state_root / "inbox" / f"{adapted['knowledgeforge_release']['release_id']}.knowledgeforge-normalized-release.json"
    write_json(normalized_path, adapted["knowledgeforge_release"])
    inbox = load_release_inbox()
    first = inbox.process_release_path(normalized_path, state_root, no_promote=True)
    result_path = state_root / "processing-evidence" / adapted["knowledgeforge_release"]["release_id"] / "adapter_processing_record.json"
    write_json(result_path, {"adapter_result": {k: v for k, v in adapted.items() if k != "knowledgeforge_release"}, "normalized_release_path": str(normalized_path), "first_processing": first})
    return {"adapter_record_path": str(result_path), "normalized_release_path": str(normalized_path), "first_processing": first, "adapter_result": adapted}


def retained_evidence_items() -> dict[tuple[str, str, str, str], dict[str, Any]]:
    out: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    inbox = load_release_inbox()
    for entity, path in CALC_PATHS.items():
        payload = inbox.package_payload(entity)
        rows = read_json(path)["calculation_evidence"]["aligned_values"]
        for row in rows:
            for indicator, value_key in [("NE.EXP.GNFS.ZS", "exports"), ("NE.IMP.GNFS.ZS", "imports")]:
                item = inbox.evidence_item(entity, indicator, row["period"], row[value_key], payload, "retained_wdi_evidence")
                key = (entity, indicator, str(row["period"]), "annual")
                out[key] = item
    return out


def macroforge_items_by_key(export_path: Path | str) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    release = read_json(export_path)
    return {(i["entity"], i["indicator"], str(i["period"]), i["frequency"]): i for i in release["items"]}


def observation_equivalence_report(export_path: Path | str, out_path: Path | str | None = None) -> dict[str, Any]:
    macro = macroforge_items_by_key(export_path)
    retained = retained_evidence_items()
    macro_keys = set(macro); retained_keys = set(retained)
    common = sorted(macro_keys & retained_keys)
    value_mismatches=[]; missingness_mismatches=[]; unit_mismatches=[]; definition_mismatches=[]
    for key in common:
        m = macro[key]; r = retained[key]
        if Decimal(str(m.get("value"))) != Decimal(str(r.get("value_canonical"))):
            value_mismatches.append({"key": key, "macroforge": m.get("value"), "knowledgeforge": r.get("value_canonical")})
        if (not bool(m.get("missing"))) != bool(r.get("observed")):
            missingness_mismatches.append({"key": key, "macroforge_missing": m.get("missing"), "knowledgeforge_observed": r.get("observed")})
        if m.get("unit") != r.get("unit"):
            unit_mismatches.append({"key": key, "macroforge": m.get("unit"), "knowledgeforge": r.get("unit")})
        if m.get("definition") != r.get("definition"):
            definition_mismatches.append({"key": key, "macroforge": m.get("definition"), "knowledgeforge": r.get("definition")})
    report={
        "macroforge_item_count": len(macro),
        "knowledgeforge_retained_item_count": len(retained),
        "matching_keys": len(common),
        "keys_only_in_macroforge": [list(k) for k in sorted(macro_keys-retained_keys)],
        "keys_only_in_knowledgeforge_retained_evidence": [list(k) for k in sorted(retained_keys-macro_keys)],
        "value_mismatches": value_mismatches,
        "missingness_mismatches": missingness_mismatches,
        "unit_mismatches": unit_mismatches,
        "definition_mismatches": definition_mismatches,
        "semantically_equivalent": not (macro_keys-retained_keys or retained_keys-macro_keys or value_mismatches or missingness_mismatches or unit_mismatches or definition_mismatches),
        "release_metadata_difference": "MacroForge release/run lineage differs from KnowledgeForge retained fixture provenance; observation semantics match only if semantically_equivalent is true.",
    }
    report["report_fingerprint"] = sha256_value(report)
    if out_path:
        write_json(out_path, report)
    return report


def derivation_comparison_from_processing(processing_result: dict[str, Any], out_path: Path | str | None = None) -> dict[str, Any]:
    results = processing_result["first_processing"]["recomputation_summary"]["incremental_results"]
    comparisons=[]
    for r in results:
        entity = r["derivation_id"].split("campaign36-")[-1].split("campaign37-")[-1].split("-")[0].upper()
        if "dnk" in r["derivation_id"]: entity="DNK"
        elif "swe" in r["derivation_id"]: entity="SWE"
        elif "nor" in r["derivation_id"]: entity="NOR"
        expected = EXPECTED_COEFFICIENTS[entity]
        status = "exact_deterministic_match" if Decimal(r["candidate_coefficient"]) == Decimal(expected) else "unexplained_mismatch"
        comparisons.append({"entity": entity, "derivation_id": r["derivation_id"], "expected_existing_coefficient": expected, "candidate_coefficient": r["candidate_coefficient"], "aligned_pair_count": r["aligned_pair_count"], "classification": status, "promotion_status": r["promotion_status"], "candidate_result_fingerprint": r["candidate_result_fingerprint"]})
    report={"comparisons": sorted(comparisons,key=lambda x:x["entity"]), "all_exact_deterministic_match": all(c["classification"]=="exact_deterministic_match" for c in comparisons)}
    report["report_fingerprint"] = sha256_value(report)
    if out_path:
        write_json(out_path, report)
    return report


def main(argv=None) -> int:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("validate"); p.add_argument("export"); p.add_argument("--manifest")
    p=sub.add_parser("adapt"); p.add_argument("export"); p.add_argument("--manifest"); p.add_argument("--output", required=True); p.add_argument("--record")
    p=sub.add_parser("process"); p.add_argument("export"); p.add_argument("--manifest"); p.add_argument("--state-root", required=True)
    p=sub.add_parser("equivalence"); p.add_argument("export"); p.add_argument("--output", required=True)
    args=ap.parse_args(argv)
    if args.cmd=="validate": print(json.dumps(validate_macroforge_release(args.export,args.manifest),indent=2,sort_keys=True)); return 0
    if args.cmd=="adapt":
        result=adapt_macroforge_release(args.export,args.manifest); write_json(args.output,result["knowledgeforge_release"])
        if args.record: write_json(args.record,{k:v for k,v in result.items() if k!="knowledgeforge_release"})
        print(json.dumps({k:v for k,v in result.items() if k!="knowledgeforge_release"},indent=2,sort_keys=True)); return 0
    if args.cmd=="process": print(json.dumps(process_adapted_release(args.export,args.manifest,args.state_root),indent=2,sort_keys=True)); return 0
    if args.cmd=="equivalence": print(json.dumps(observation_equivalence_report(args.export,args.output),indent=2,sort_keys=True)); return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
