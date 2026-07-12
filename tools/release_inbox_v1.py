#!/usr/bin/env python3
"""Provider-neutral release inbox and real-evidence impact pilot v1.

KnowledgeForge-owned operational slice. It never imports MacroForge code, queries
MacroForge tables, mutates canonical packages, writes PostgreSQL, creates Campaign
41, or promotes Knowledge Objects.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ID = "knowledgeforge_neutral_evidence_release_contract_v1"
CONTRACT_VERSION = "1.0"
FULL_CONTRACT = f"{CONTRACT_ID}@{CONTRACT_VERSION}"
DEFAULT_STATE = ROOT / "artifacts/release-inbox-v1"
DEFAULT_REPORT = ROOT / "artifacts/reports/provider-neutral-release-inbox-real-evidence-impact-pilot-v1-20260711"
DERIVATION_REGISTRY_PATH = ROOT / "specs/release_automation/real_derivation_applicability_registry_v1.json"
METHOD_TOOL = ROOT / "tools/deterministic_pearson_correlation_v1.py"

ENTITY_NAMES = {"DNK": "Denmark", "SWE": "Sweden", "NOR": "Norway"}
PKG_IDS = {
    "DNK": "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1",
    "SWE": "pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1",
    "NOR": "pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1",
}
CALC_PATHS = {
    "DNK": ROOT / "artifacts/reports/campaign36-dnk-exports-imports-share-pearson-correlation-20260710/calculation_evidence.json",
    "SWE": ROOT / "artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/swe_calculation_evidence.json",
    "NOR": ROOT / "artifacts/reports/campaign37-swe-nor-exports-imports-share-pearson-correlation-20260710/nor_calculation_evidence.json",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text())


def write_json(path: Path | str, value: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def release_content_without_fingerprint(release: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in release.items() if k not in {"release_content_fingerprint", "received_at", "operational_notes"}}


def item_without_fingerprint(item: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in item.items() if k != "item_fingerprint"}


def refresh_release_fingerprints(release: dict[str, Any], *, keep_release_id: bool = True) -> dict[str, Any]:
    for item in release.get("evidence_items", []):
        item["item_fingerprint"] = sha256_value(item_without_fingerprint(item))
    release["release_content_fingerprint"] = sha256_value(release_content_without_fingerprint(release))
    return release


def initialize_operational_state(state_root: Path = DEFAULT_STATE) -> dict[str, str]:
    paths = {
        "inbox": state_root / "inbox",
        "accepted": state_root / "accepted-releases",
        "quarantine": state_root / "quarantined-releases",
        "processing": state_root / "processing-evidence",
    }
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    registry = state_root / "seen-release-registry.jsonl"
    if not registry.exists():
        registry.write_text("")
    return {k: str(v) for k, v in paths.items()} | {"registry": str(registry)}


def load_registry(state_root: Path = DEFAULT_STATE) -> dict[str, Any]:
    initialize_operational_state(state_root)
    entries = []
    registry = state_root / "seen-release-registry.jsonl"
    for line in registry.read_text().splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return {"registry_path": str(registry), "entries": entries}


def append_registry(state_root: Path, entry: dict[str, Any]) -> None:
    initialize_operational_state(state_root)
    with (state_root / "seen-release-registry.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")


def package_payload(entity: str) -> dict[str, Any]:
    pkg = read_json(ROOT / "knowledge_repository/objects" / f"{PKG_IDS[entity]}.json")
    return pkg["generated_statements"][0]["structured_payload"]


def load_aligned_values(entity: str) -> list[dict[str, Any]]:
    return read_json(CALC_PATHS[entity])["calculation_evidence"]["aligned_values"]


def evidence_item(entity: str, indicator: str, period: int, value: str, payload: dict[str, Any], source_kind: str) -> dict[str, Any]:
    series = payload["series_a"] if indicator == "NE.EXP.GNFS.ZS" else payload["series_b"]
    item = {
        "item_id": f"wdi:{entity}:{indicator}:{period}",
        "provider_id": "world_bank",
        "dataset_id": "world_development_indicators",
        "entity_id": entity,
        "entity_name": ENTITY_NAMES[entity],
        "indicator_code": indicator,
        "indicator_name": series["name"],
        "definition": series["definition"],
        "period": int(period),
        "frequency": "annual",
        "value_canonical": str(value),
        "unit": "percent of GDP",
        "observed": True,
        "missing_reason": None,
        "source_kind": source_kind,
    }
    item["item_fingerprint"] = sha256_value(item_without_fingerprint(item))
    return item


def build_release(release_id: str, version: str, prior_release_id: str | None, label: str, controlled: bool = False) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    source_versions = {}
    for entity in ["DNK", "SWE", "NOR"]:
        payload = package_payload(entity)
        source_versions[entity] = payload["provider_metadata"]["exports"].get("wdi_lastupdated")
        for row in load_aligned_values(entity):
            exp = row["exports"]
            imp = row["imports"]
            exp_source = "retained_wdi_evidence"
            imp_source = "retained_wdi_evidence"
            if controlled and entity == "DNK" and int(row["period"]) == 2020:
                exp = format(Decimal(exp) + Decimal("0.125"), "f")
                exp_source = "controlled_test_successor_release"
            items.append(evidence_item(entity, "NE.EXP.GNFS.ZS", row["period"], exp, payload, exp_source))
            items.append(evidence_item(entity, "NE.IMP.GNFS.ZS", row["period"], imp, payload, imp_source))
        if controlled and entity == "DNK":
            items.append(evidence_item(entity, "NE.EXP.GNFS.ZS", 2025, "72.000000000000", payload, "controlled_test_successor_release"))
            items.append(evidence_item(entity, "NE.IMP.GNFS.ZS", 2025, "67.000000000000", payload, "controlled_test_successor_release"))
    release = {
        "contract_id": CONTRACT_ID,
        "contract_version": CONTRACT_VERSION,
        "release_id": release_id,
        "release_label": label,
        "provider": {"provider_id": "world_bank", "name": "World Bank"},
        "dataset": {"dataset_id": "world_development_indicators", "name": "World Development Indicators"},
        "source_release_vintage": "2026-07-01" if not controlled else "controlled_test_successor_release",
        "published_at": "2026-07-01T00:00:00Z" if not controlled else "2026-07-08T00:00:00Z",
        "prior_release_id": prior_release_id,
        "supersedes_release_id": prior_release_id,
        "source_metadata": {"wdi_lastupdated_by_entity": source_versions, "indicators": ["NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"], "entities": ["DNK", "SWE", "NOR"], "periods": {"start": 1990, "end": 2024 if not controlled else 2025}},
        "provenance_note": "KnowledgeForge conformance fixture derived from retained provider evidence, not a genuine MacroForge export." if not controlled else "controlled_test_successor_release; test-only values do not come from WDI or MacroForge.",
        "evidence_items": sorted(items, key=lambda x: (x["entity_id"], x["indicator_code"], x["period"])),
    }
    return refresh_release_fingerprints(release)


def write_real_evidence_pilot_fixtures(out_dir: Path = DEFAULT_REPORT / "fixtures") -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    v1 = build_release("wdi-trade-exports-imports-retained-evidence-v1", "v1", None, "retained_wdi_evidence_v1", controlled=False)
    v2 = build_release("wdi-trade-exports-imports-controlled-test-v2", "v2", v1["release_id"], "controlled_test_successor_release", controlled=True)
    write_json(out_dir / "real_wdi_exports_imports_release_v1.json", v1)
    write_json(out_dir / "controlled_successor_release_v2.json", v2)
    return {"v1": str(out_dir / "real_wdi_exports_imports_release_v1.json"), "v2": str(out_dir / "controlled_successor_release_v2.json")}


def validate_release(release: dict[str, Any]) -> dict[str, Any]:
    errors = []
    for k in ["contract_id", "contract_version", "release_id", "provider", "dataset", "source_release_vintage", "evidence_items", "release_content_fingerprint"]:
        if k not in release:
            errors.append(f"missing_release_field:{k}")
    if release.get("contract_id") != CONTRACT_ID or release.get("contract_version") != CONTRACT_VERSION:
        errors.append("wrong_contract_version")
    ids = set()
    for item in release.get("evidence_items", []):
        for k in ["item_id", "entity_id", "indicator_code", "period", "frequency", "value_canonical", "unit", "observed", "item_fingerprint"]:
            if k not in item:
                errors.append(f"missing_item_field:{k}:{item.get('item_id','unknown')}")
        if item.get("item_id") in ids:
            errors.append(f"duplicate_item_id:{item.get('item_id')}")
        ids.add(item.get("item_id"))
        if item.get("item_fingerprint") != sha256_value(item_without_fingerprint(item)):
            errors.append(f"item_fingerprint_mismatch:{item.get('item_id')}")
    expected = sha256_value(release_content_without_fingerprint(release)) if isinstance(release, dict) else None
    if release.get("release_content_fingerprint") != expected:
        errors.append("release_fingerprint_mismatch")
    return {"valid": not errors, "errors": errors, "release_id": release.get("release_id"), "release_content_fingerprint": release.get("release_content_fingerprint")}


def load_derivation_registry() -> dict[str, Any]:
    if DERIVATION_REGISTRY_PATH.exists():
        return read_json(DERIVATION_REGISTRY_PATH)
    corr = load_module(METHOD_TOOL, "pearson_contract_for_registry")
    contract = corr.calculation_contract_v1()
    derivations = []
    for entity in ["DNK", "SWE", "NOR"]:
        pkg = read_json(ROOT / "knowledge_repository/objects" / f"{PKG_IDS[entity]}.json")
        payload = pkg["generated_statements"][0]["structured_payload"]
        derivations.append({
            "derivation_id": PKG_IDS[entity],
            "canonical_output_package_id": PKG_IDS[entity],
            "pair_identity": payload["canonical_pair_identity"],
            "series_dependencies": ["NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"],
            "entity": entity,
            "frequency": "annual",
            "period_scope": payload["period_scope"],
            "transformation_scope": payload["transformation_state"],
            "method_identity": contract["method_identity"],
            "method_contract_fingerprint": contract["calculation_contract_fingerprint"],
            "evidence_requirements": {"required_indicators": ["NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"], "minimum_aligned_pairs": 30, "observed_values_only": True},
            "recomputation_strategy": "no_promote_recompute_when_dependency_scope_changes",
            "automatic_execution_class": "deterministic_local_no_promote_allowed",
            "promotion_requirement": "separate explicit promotion task required",
            "prior_coefficient": payload["pearson_coefficient"]["canonical"],
            "prior_package_fingerprint": pkg["fingerprints"]["package_manifest"],
        })
    return {"registry_id": "knowledgeforge_real_derivation_applicability_registry_v1@1.0", "derivations": derivations}


def write_derivation_registry() -> dict[str, Any]:
    reg = load_derivation_registry()
    write_json(DERIVATION_REGISTRY_PATH, reg)
    return reg


def items_by_id(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {i["item_id"]: i for i in release.get("evidence_items", [])}


def detect_change(old: dict[str, Any] | None, new: dict[str, Any]) -> dict[str, Any]:
    if old is None:
        added = sorted(items_by_id(new))
        result = {"predecessor_release_id": None, "processed_release_id": new["release_id"], "added_item_ids": added, "removed_item_ids": [], "changed_item_ids": [], "unchanged_item_ids": []}
    else:
        a, b = items_by_id(old), items_by_id(new)
        added = sorted(set(b) - set(a)); removed = sorted(set(a) - set(b)); common = sorted(set(a) & set(b))
        changed = [i for i in common if a[i]["item_fingerprint"] != b[i]["item_fingerprint"]]
        unchanged = [i for i in common if i not in changed]
        result = {"predecessor_release_id": old["release_id"], "processed_release_id": new["release_id"], "added_item_ids": added, "removed_item_ids": removed, "changed_item_ids": changed, "unchanged_item_ids": unchanged}
    result["change_set_fingerprint"] = sha256_value(result)
    return result


def changed_scopes(change: dict[str, Any], release: dict[str, Any], predecessor: dict[str, Any] | None = None) -> dict[str, Any]:
    sources = []
    ids = set(change["added_item_ids"] + change["changed_item_ids"] + change["removed_item_ids"])
    maps = [items_by_id(release)]
    if predecessor:
        maps.append(items_by_id(predecessor))
    for m in maps:
        for item_id in ids:
            if item_id in m:
                sources.append(m[item_id])
    return {"entities": sorted({i["entity_id"] for i in sources}), "indicators": sorted({i["indicator_code"] for i in sources}), "periods": sorted({i["period"] for i in sources})}


def impact_analysis(change: dict[str, Any], release: dict[str, Any], predecessor: dict[str, Any] | None, registry: dict[str, Any]) -> dict[str, Any]:
    scopes = changed_scopes(change, release, predecessor)
    affected, unaffected = [], []
    for d in registry["derivations"]:
        hit = d["entity"] in scopes["entities"] and bool(set(d["series_dependencies"]) & set(scopes["indicators"]))
        (affected if hit else unaffected).append(d)
    result = {"changed_scopes": scopes, "affected_derivation_ids": [d["derivation_id"] for d in affected], "unaffected_derivation_ids": [d["derivation_id"] for d in unaffected], "affected_derivations": affected, "unaffected_derivations": unaffected}
    result["affected_derivation_fingerprint"] = sha256_value({"affected": result["affected_derivation_ids"], "unaffected": result["unaffected_derivation_ids"], "scopes": scopes})
    return result


def release_series(release: dict[str, Any], entity: str, indicator: str) -> dict[str, Any]:
    observations = []
    meta = None
    for item in release["evidence_items"]:
        if item["entity_id"] == entity and item["indicator_code"] == indicator:
            observations.append({"period": item["period"], "observed": item.get("observed", True), "value_canonical": item.get("value_canonical")})
            meta = item
    if not observations:
        raise ValueError(f"missing series {entity} {indicator}")
    return {"series_id": {"indicator_code": indicator, "entity_id": entity, "frequency": "annual", "unit": meta["unit"], "transformation": "raw"}, "observations": sorted(observations, key=lambda x: x["period"])}


def recompute_derivation(release: dict[str, Any], derivation: dict[str, Any]) -> dict[str, Any]:
    corr = load_module(METHOD_TOOL, "pearson_recompute")
    a = release_series(release, derivation["entity"], "NE.EXP.GNFS.ZS")
    b = release_series(release, derivation["entity"], "NE.IMP.GNFS.ZS")
    result = corr.compute_correlation(a, b, minimum_aligned_pairs=30, coverage_threshold=Decimal("0"))
    out = {"derivation_id": derivation["derivation_id"], "prior_coefficient": derivation["prior_coefficient"], "prior_fingerprint": derivation["prior_package_fingerprint"], "candidate_coefficient": result["coefficient"]["canonical"], "candidate_result_fingerprint": result["output_fingerprint"], "aligned_pair_count": result["aligned_pair_count"], "promotion_status": "not_promoted"}
    return out


def recomputation_plan(release: dict[str, Any], impact: dict[str, Any], registry: dict[str, Any], *, simulate_recompute_failure: bool = False) -> dict[str, Any]:
    if simulate_recompute_failure:
        raise RuntimeError("simulated recomputation failure")
    incremental = [recompute_derivation(release, d) for d in impact["affected_derivations"]]
    full = [recompute_derivation(release, d) for d in registry["derivations"]]
    full_for_affected = [r for r in full if r["derivation_id"] in impact["affected_derivation_ids"]]
    return {"incremental_results": incremental, "full_comparison_results_for_affected": full_for_affected, "full_recompute_count_for_verification": len(full), "incremental_recompute_count": len(incremental), "avoided_recompute_count": len(registry["derivations"]) - len(incremental), "unchanged_derivation_identities": impact["unaffected_derivation_ids"]}


def latest_successful_by_release(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for e in entries:
        if e.get("processing_status") == "successfully_processed_no_promote":
            out[e.get("release_id")] = e
    return out


def accepted_release_path(state_root: Path, release_id: str) -> Path:
    return state_root / "accepted-releases" / f"{release_id}.json"


def classify_release(release: dict[str, Any], validation: dict[str, Any], state_root: Path) -> tuple[str, str | None]:
    entries = load_registry(state_root)["entries"]
    successes = latest_successful_by_release(entries)
    rid, rfp = release.get("release_id"), release.get("release_content_fingerprint")
    if not validation["valid"]:
        return "invalid_release", ";".join(validation["errors"])
    successful_ids = list(successes)
    latest_id = successful_ids[-1] if successful_ids else None
    if rid in successes:
        if successes[rid].get("release_content_fingerprint") != rfp:
            return "conflicting_reuse_of_release_id", "release_id reused with different content fingerprint"
        if latest_id and latest_id != rid:
            return "out_of_order_release", "release already processed before current registry head"
        return "already_processed_identical_release", None
    predecessor = release.get("prior_release_id")
    if predecessor:
        if predecessor not in successes:
            return "out_of_order_release", "missing predecessor release"
        if latest_id != predecessor:
            return "out_of_order_release", "predecessor is not current registry head"
        return "valid_successor_release", None
    if successes:
        return "out_of_order_release", "root release arrived after accepted successor chain"
    return "unseen", None


def make_entry(release: dict[str, Any] | None, validation: dict[str, Any], received_status: str, processing_status: str, **extra) -> dict[str, Any]:
    return {
        "registry_entry_id": sha256_value({"release": release.get("release_id") if release else None, "fingerprint": release.get("release_content_fingerprint") if release else None, "status": received_status, "extra": extra, "timestamp_source": "excluded_from_deterministic_id"}),
        "operational_timestamp": now_utc(),
        "release_id": release.get("release_id") if release else None,
        "contract_identity": f"{release.get('contract_id')}@{release.get('contract_version')}" if release else None,
        "provider_identity": release.get("provider", {}).get("provider_id") if release else None,
        "dataset_identity": release.get("dataset", {}).get("dataset_id") if release else None,
        "source_release_vintage": release.get("source_release_vintage") if release else None,
        "release_content_fingerprint": release.get("release_content_fingerprint") if release else None,
        "prior_release_id": release.get("prior_release_id") if release else None,
        "received_status": received_status,
        "validation_result": validation,
        "processing_status": processing_status,
        "change_set_fingerprint": extra.get("change_set_fingerprint"),
        "affected_derivation_fingerprint": extra.get("affected_derivation_fingerprint"),
        "downstream_delta_fingerprint": extra.get("downstream_delta_fingerprint"),
        "failure_rejection_reason": extra.get("failure_rejection_reason"),
        "supersession_state": extra.get("supersession_state", "not_evaluated"),
    }


def emit_delta(state_root: Path, release: dict[str, Any], predecessor: dict[str, Any] | None, change: dict[str, Any], impact: dict[str, Any], recompute: dict[str, Any]) -> Path:
    delta = {"delta_contract_id": "knowledgeforge_provider_neutral_release_delta_v1@1.0", "processed_release_id": release["release_id"], "predecessor_release_id": predecessor.get("release_id") if predecessor else None, "release_fingerprint": release["release_content_fingerprint"], "change_set_fingerprint": change["change_set_fingerprint"], "changed_scopes": impact["changed_scopes"], "affected_derivations": impact["affected_derivation_ids"], "unaffected_derivations": impact["unaffected_derivation_ids"], "recomputed_candidates": [r["derivation_id"] for r in recompute["incremental_results"]], "candidate_results": recompute["incremental_results"], "promotion_status": "not_promoted", "supersession_plan": {"supersedes": predecessor.get("release_id") if predecessor else None, "canonical_supersession_implemented": False}, "compact_impact_cards": [{"release_id": release["release_id"], "changed_scopes": impact["changed_scopes"], "affected": impact["affected_derivation_ids"], "unaffected": impact["unaffected_derivation_ids"], "promotion_status": "not_promoted"}]}
    delta["downstream_export_fingerprint"] = sha256_value(delta)
    path = state_root / "processing-evidence" / release["release_id"] / "downstream_delta.json"
    write_json(path, delta)
    return path


def consumer_assess_delta(delta: dict[str, Any]) -> dict[str, Any]:
    return {"can_determine_what_changed": bool(delta.get("changed_scopes")), "can_determine_which_relationship_would_change": bool(delta.get("affected_derivations")), "can_determine_which_relationships_remain_valid": "unaffected_derivations" in delta, "canonical_promotion_occurred": delta.get("promotion_status") != "not_promoted", "evidence_release_id": delta.get("processed_release_id")}


def process_release_path(path: Path | str, state_root: Path = DEFAULT_STATE, *, no_promote: bool = True, simulate_recompute_failure: bool = False) -> dict[str, Any]:
    initialize_operational_state(state_root)
    p = Path(path)
    try:
        release = read_json(p)
    except Exception as exc:
        validation = {"valid": False, "errors": [f"malformed_json:{type(exc).__name__}"], "release_id": None, "release_content_fingerprint": None}
        entry = make_entry(None, validation, "invalid_release", "quarantined_release", failure_rejection_reason=validation["errors"][0])
        append_registry(state_root, entry)
        q = state_root / "quarantined-releases" / f"malformed-{sha256_bytes(p.read_bytes() if p.exists() else b'')[-16:]}.json"
        if p.exists(): shutil.copy2(p, q)
        return entry | {"recomputation_summary": {"incremental_recompute_count": 0}}
    validation = validate_release(release)
    received, reason = classify_release(release, validation, state_root)
    if received in {"invalid_release", "conflicting_reuse_of_release_id", "out_of_order_release"}:
        entry = make_entry(release, validation, received, "quarantined_release", failure_rejection_reason=reason)
        append_registry(state_root, entry)
        shutil.copy2(p, state_root / "quarantined-releases" / p.name)
        return entry | {"recomputation_summary": {"incremental_recompute_count": 0}}
    if received == "already_processed_identical_release":
        entry = make_entry(release, validation, received, "successfully_processed_no_promote", supersession_state="unchanged_duplicate")
        append_registry(state_root, entry)
        return entry | {"recomputation_summary": {"incremental_recompute_count": 0}}
    predecessor = read_json(accepted_release_path(state_root, release["prior_release_id"])) if release.get("prior_release_id") else None
    registry = load_derivation_registry()
    change = detect_change(predecessor, release)
    impact = impact_analysis(change, release, predecessor, registry)
    try:
        recompute = recomputation_plan(release, impact, registry, simulate_recompute_failure=simulate_recompute_failure)
    except Exception as exc:
        entry = make_entry(release, validation, received, "processing_failed", change_set_fingerprint=change["change_set_fingerprint"], affected_derivation_fingerprint=impact["affected_derivation_fingerprint"], failure_rejection_reason=str(exc), supersession_state="not_applied_failure")
        append_registry(state_root, entry)
        write_json(state_root / "processing-evidence" / release["release_id"] / "failure.json", entry)
        return entry | {"change": change, "impact": impact, "recomputation_summary": {"incremental_recompute_count": 0, "failure": str(exc)}}
    delta_path = emit_delta(state_root, release, predecessor, change, impact, recompute)
    delta = read_json(delta_path)
    shutil.copy2(p, accepted_release_path(state_root, release["release_id"]))
    processing_status = "accepted_but_not_promoted" if not no_promote else "successfully_processed_no_promote"
    entry = make_entry(release, validation, received if received != "unseen" else "unseen", processing_status, change_set_fingerprint=change["change_set_fingerprint"], affected_derivation_fingerprint=impact["affected_derivation_fingerprint"], downstream_delta_fingerprint=delta["downstream_export_fingerprint"], supersession_state="supersedes_prior_release" if predecessor else "root_release_accepted")
    append_registry(state_root, entry)
    write_json(state_root / "processing-evidence" / release["release_id"] / "processing_result.json", {"entry": entry, "change": change, "impact": impact, "recomputation_summary": recompute, "downstream_delta_path": str(delta_path)})
    return entry | {"change": change, "impact": impact, "recomputation_summary": recompute, "downstream_delta_path": str(delta_path)}


def scan_inbox(state_root: Path = DEFAULT_STATE) -> dict[str, Any]:
    initialize_operational_state(state_root)
    pending = sorted(str(p) for p in (state_root / "inbox").glob("*.json"))
    return {"inbox": str(state_root / "inbox"), "pending_count": len(pending), "pending": pending}


def verify_registry(state_root: Path = DEFAULT_STATE) -> dict[str, Any]:
    reg = load_registry(state_root)
    ok = True; errors = []
    for i, e in enumerate(reg["entries"]):
        for k in ["release_id", "received_status", "processing_status", "validation_result"]:
            if k not in e:
                ok = False; errors.append(f"entry_{i}_missing_{k}")
    return {"valid": ok, "errors": errors, "entry_count": len(reg["entries"]), "registry_path": reg["registry_path"]}


def write_producer_conformance_package(out_dir: Path = DEFAULT_REPORT / "producer_conformance") -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    examples = write_real_evidence_pilot_fixtures(out_dir)
    valid = read_json(examples["v1"])
    wrong_contract = dict(valid); wrong_contract["contract_version"] = "9.9"; refresh_release_fingerprints(wrong_contract)
    missing = dict(valid); missing.pop("provider", None); refresh_release_fingerprints(missing)
    mismatch = dict(valid); mismatch["release_content_fingerprint"] = "sha256:" + "0" * 64
    invalids = {"wrong_contract_version.json": wrong_contract, "missing_provider.json": missing, "fingerprint_mismatch.json": mismatch}
    for name, obj in invalids.items(): write_json(out_dir / name, obj)
    package = {"package_id": "knowledgeforge-provider-neutral-release-conformance-v1", "contract_identity": FULL_CONTRACT, "neutral_release_contract_specification": {"required_release_fields": ["contract_id", "contract_version", "release_id", "provider", "dataset", "source_release_vintage", "evidence_items", "release_content_fingerprint"], "required_item_fields": ["item_id", "entity_id", "indicator_code", "period", "value_canonical", "unit", "item_fingerprint"]}, "minimal_valid_example": "real_wdi_exports_imports_release_v1.json", "controlled_invalid_examples": sorted(invalids), "fingerprint_rules": "sha256 over canonical JSON excluding the fingerprint field itself; operational timestamps excluded from deterministic release identity", "unit_missingness_requirements": "unit required for every item; observed false requires missing_reason and null value", "predecessor_supersession_rules": "successor releases must name prior_release_id; missing predecessors fail closed", "validation_command": "python3 tools/release_inbox_v1.py validate-release <path>", "forbidden_dependencies": ["producer-specific storage identifiers", "producer runtime classes", "credential material", "consumer-private relational schema"]}
    write_json(out_dir / "conformance_package.json", package)
    return package


def verify_conformance_package(out_dir: Path) -> dict[str, Any]:
    pkg = read_json(out_dir / "conformance_package.json")
    valid_result = validate_release(read_json(out_dir / pkg["minimal_valid_example"]))
    invalid_results = {}
    for name in pkg["controlled_invalid_examples"]:
        invalid_results[name] = validate_release(read_json(out_dir / name))
    return {"valid": valid_result["valid"] and all(not r["valid"] for r in invalid_results.values()), "valid_example_result": valid_result, "controlled_invalid_results": invalid_results}


def recovery_inventory(paths: list[Path]) -> dict[str, Any]:
    files = []
    for base in paths:
        if base.exists():
            for p in sorted(x for x in base.rglob("*") if x.is_file()):
                files.append({"path": str(p), "bytes": p.stat().st_size, "sha256": sha256_bytes(p.read_bytes())})
    return {"file_count": len(files), "files": files, "durability_note": "Release registry and accepted release packages are recovery-critical operational state; without commit/push or external backup they survive only on this machine."}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("scan-inbox")
    p = sub.add_parser("inspect-release"); p.add_argument("path")
    p = sub.add_parser("validate-release"); p.add_argument("path")
    p = sub.add_parser("process-one"); p.add_argument("path"); p.add_argument("--simulate-recompute-failure", action="store_true")
    sub.add_parser("process-all")
    sub.add_parser("verify-registry")
    sub.add_parser("write-fixtures")
    sub.add_parser("write-derivation-registry")
    sub.add_parser("write-conformance")
    sub.add_parser("verify-conformance")
    sub.add_parser("recovery-inventory")
    ap.add_argument("--state-root", default=str(DEFAULT_STATE))
    ap.add_argument("--report-dir", default=str(DEFAULT_REPORT))
    args = ap.parse_args(argv)
    state = Path(args.state_root); report = Path(args.report_dir)
    if args.cmd == "init": print(json.dumps(initialize_operational_state(state), indent=2)); return 0
    if args.cmd == "scan-inbox": print(json.dumps(scan_inbox(state), indent=2)); return 0
    if args.cmd == "inspect-release": print(json.dumps(read_json(args.path), indent=2, sort_keys=True)); return 0
    if args.cmd == "validate-release": print(json.dumps(validate_release(read_json(args.path)), indent=2, sort_keys=True)); return 0
    if args.cmd == "process-one": print(json.dumps(process_release_path(Path(args.path), state, simulate_recompute_failure=args.simulate_recompute_failure), indent=2, sort_keys=True)); return 0
    if args.cmd == "process-all":
        results = [process_release_path(Path(p), state) for p in scan_inbox(state)["pending"]]
        print(json.dumps({"processed": results}, indent=2, sort_keys=True)); return 0
    if args.cmd == "verify-registry": print(json.dumps(verify_registry(state), indent=2, sort_keys=True)); return 0
    if args.cmd == "write-fixtures": print(json.dumps(write_real_evidence_pilot_fixtures(report / "fixtures"), indent=2)); return 0
    if args.cmd == "write-derivation-registry": print(json.dumps(write_derivation_registry(), indent=2, sort_keys=True)); return 0
    if args.cmd == "write-conformance": print(json.dumps(write_producer_conformance_package(report / "producer_conformance"), indent=2, sort_keys=True)); return 0
    if args.cmd == "verify-conformance": print(json.dumps(verify_conformance_package(report / "producer_conformance"), indent=2, sort_keys=True)); return 0
    if args.cmd == "recovery-inventory": print(json.dumps(recovery_inventory([state, report / "fixtures", report / "producer_conformance", DERIVATION_REGISTRY_PATH.parent]), indent=2, sort_keys=True)); return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
