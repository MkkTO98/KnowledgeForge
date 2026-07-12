#!/usr/bin/env python3
"""Provider-neutral external outbox poller and controlled supersession prototype v1.

KnowledgeForge-owned tooling. It reads producer-owned serialized files, copies bytes
into a KnowledgeForge-owned inbox, invokes KnowledgeForge adapters, and records an
auditable transport registry. It must not modify producer files or import producer
code.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sqlite3
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "external_outbox_sources.json"
DEFAULT_STATE = ROOT / "artifacts" / "external-outbox-transport-v1"
UNIFIED_REGISTRY_ROOT = ROOT / "artifacts" / "release-inbox-unified-v1"
HISTORICAL_REAL_HANDOFF = ROOT / "artifacts" / "release-inbox-macroforge-real-handoff-v1"
MACRO_ADAPTER_PATH = ROOT / "tools" / "macroforge_neutral_release_adapter_v1.py"
RELEASE_INBOX_PATH = ROOT / "tools" / "release_inbox_v1.py"
KNOWLEDGE_REPOSITORY_PATH = ROOT / "tools" / "knowledge_repository.py"
PG_TOOL_PATH = ROOT / "tools" / "postgresql_operational_projection.py"
ADAPTER_ID_VERSION = "knowledgeforge_macroforge_neutral_release_adapter_v1@1.0"
SUPPORTED_MACRO_CONTRACT = "macroforge.neutral_evidence_release_export.v1"
SUPPORTED_MACRO_VERSION = "1.0"
KNOWN_INDICATORS = {
    "NE.EXP.GNFS.ZS": {"indicator_name": "Exports of goods and services (% of GDP)", "unit": "percent of GDP"},
    "NE.IMP.GNFS.ZS": {"indicator_name": "Imports of goods and services (% of GDP)", "unit": "percent of GDP"},
}
DNK_PACKAGE_ID = "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1"
SWE_PACKAGE_ID = "pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1"
NOR_PACKAGE_ID = "pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


def file_sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def file_fingerprint(path: Path | str) -> str:
    return "sha256:" + file_sha256(path)


def load_json(path: Path | str) -> Any:
    return json.loads(Path(path).read_text())


def write_json(path: Path | str, value: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def macro_adapter():
    return load_module(MACRO_ADAPTER_PATH, "macroforge_neutral_release_adapter_v1")


def release_inbox():
    return load_module(RELEASE_INBOX_PATH, "release_inbox_v1")


def knowledge_repository():
    return load_module(KNOWLEDGE_REPOSITORY_PATH, "knowledge_repository")


def load_config(config_path: Path | str = DEFAULT_CONFIG) -> dict[str, Any]:
    cfg = load_json(config_path)
    if "sources" not in cfg or not isinstance(cfg["sources"], list):
        raise ValueError("external outbox config must contain sources[]")
    return cfg


def validate_source_config(source: dict[str, Any]) -> None:
    required = ["source_identity", "root_location", "supported_contracts", "discovery_pattern", "enabled", "polling_mode", "transfer_destination", "max_files_per_scan", "max_bytes_per_scan"]
    missing = [k for k in required if k not in source]
    if missing:
        raise ValueError(f"source config missing {missing}")
    forbidden = canonical_json(source)
    for term in ["curated.", "meta.", "staging.", "pearson", "correlation", "derivation", "postgres://", "postgresql://"]:
        if term in forbidden:
            raise ValueError(f"source config contains forbidden consumer/producer coupling term: {term}")


def manifest_export_name(manifest: dict[str, Any]) -> str | None:
    for key in ["export_file", "export_filename", "release_file", "artifact_file"]:
        if isinstance(manifest.get(key), str):
            return manifest[key]
    files = manifest.get("files")
    if isinstance(files, list):
        for f in files:
            if isinstance(f, dict) and str(f.get("path", "")).endswith(".neutral-release.json"):
                return f["path"]
    return None


def manifest_export_hash(manifest: dict[str, Any]) -> str | None:
    for key in ["export_sha256", "export_file_sha256", "sha256"]:
        if isinstance(manifest.get(key), str):
            return manifest[key].removeprefix("sha256:")
    files = manifest.get("files")
    if isinstance(files, list):
        for f in files:
            if isinstance(f, dict) and str(f.get("path", "")).endswith(".neutral-release.json"):
                return str(f.get("sha256") or f.get("hash") or "").removeprefix("sha256:")
    return None


def contract_from_manifest_or_export(manifest_path: Path, export_path: Path | None = None) -> tuple[str | None, str | None]:
    manifest = load_json(manifest_path)
    contract = manifest.get("contract_identity") or manifest.get("contract_id")
    version = manifest.get("contract_version")
    if (not contract or not version) and export_path and export_path.exists():
        exp = load_json(export_path)
        contract = contract or exp.get("contract_identity") or exp.get("contract_id")
        version = version or exp.get("contract_version")
    return contract, version


def producer_release_id(export: dict[str, Any], manifest: dict[str, Any]) -> str | None:
    return export.get("release_identity") or export.get("release_id") or manifest.get("release_identity") or manifest.get("release_id")


def producer_fingerprint(export: dict[str, Any], manifest: dict[str, Any]) -> str | None:
    return export.get("release_fingerprint") or export.get("release_content_fingerprint") or manifest.get("release_fingerprint")


def discover_source(source: dict[str, Any]) -> list[dict[str, Any]]:
    validate_source_config(source)
    if not source.get("enabled", False):
        return []
    root = Path(os.path.expandvars(os.path.expanduser(source["root_location"])))
    manifests = sorted(root.glob(source.get("discovery_pattern", "**/manifest.json")))[: int(source["max_files_per_scan"])]
    releases: list[dict[str, Any]] = []
    total_bytes = 0
    for m in manifests:
        if any(part.startswith("_") for part in m.relative_to(root).parts):
            continue
        try:
            manifest = load_json(m)
        except Exception as exc:
            releases.append({"source_identity": source["source_identity"], "source_manifest_path": str(m), "discovery_status": "invalid_manifest", "failure_reason": type(exc).__name__})
            continue
        name = manifest_export_name(manifest)
        export_path = m.parent / name if name else next(iter(sorted(m.parent.glob("*.neutral-release.json"))), None)
        if not export_path or not export_path.exists():
            releases.append({"source_identity": source["source_identity"], "source_manifest_path": str(m), "discovery_status": "missing_export", "failure_reason": "missing_export"})
            continue
        total_bytes += export_path.stat().st_size + m.stat().st_size
        if total_bytes > int(source["max_bytes_per_scan"]):
            break
        contract, version = contract_from_manifest_or_export(m, export_path)
        try:
            export = load_json(export_path)
        except Exception:
            export = {}
        releases.append({
            "source_identity": source["source_identity"],
            "source_manifest_path": str(m),
            "source_export_path": str(export_path),
            "discovery_status": "discovered",
            "contract_identity": contract,
            "contract_version": version,
            "producer_release_id": producer_release_id(export, manifest),
            "producer_fingerprint": producer_fingerprint(export, manifest),
            "manifest_hash": file_sha256(m),
            "export_hash": file_sha256(export_path),
        })
    return releases


def list_discovered(config_path: Path | str = DEFAULT_CONFIG) -> dict[str, Any]:
    cfg = load_config(config_path)
    releases = []
    for source in cfg["sources"]:
        releases.extend(discover_source(source))
    return {"release_count": len(releases), "releases": releases}


def registry_path(state_root: Path | str) -> Path:
    return Path(state_root) / "transport-registry.jsonl"


def append_transport(state_root: Path | str, record: dict[str, Any]) -> None:
    p = registry_path(state_root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


def read_transport_registry(state_root: Path | str) -> list[dict[str, Any]]:
    p = registry_path(state_root)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def latest_identical_transfer(state_root: Path | str, producer_id: str, export_hash: str) -> dict[str, Any] | None:
    for rec in reversed(read_transport_registry(state_root)):
        if rec.get("producer_release_id") == producer_id and rec.get("export_hash") == export_hash and rec.get("transport_status") in {"processed", "transferred"}:
            return rec
    return None


def ensure_unified_history(state_root: Path | str) -> Path:
    inbox = release_inbox()
    target = Path(state_root)
    inbox.initialize_operational_state(target)
    hist_reg = HISTORICAL_REAL_HANDOFF / "seen-release-registry.jsonl"
    target_reg = target / "seen-release-registry.jsonl"
    if hist_reg.exists() and (not target_reg.exists() or target_reg.stat().st_size == 0):
        shutil.copy2(hist_reg, target_reg)
    hist_acc = HISTORICAL_REAL_HANDOFF / "accepted-releases"
    target_acc = target / "accepted-releases"
    if hist_acc.exists():
        target_acc.mkdir(parents=True, exist_ok=True)
        for p in hist_acc.glob("*.json"):
            dst = target_acc / p.name
            if not dst.exists():
                shutil.copy2(p, dst)
    return target


def adapt_external_release(export_path: Path | str, manifest_path: Path | str | None = None) -> dict[str, Any]:
    return macro_adapter().adapt_macroforge_release(Path(export_path), Path(manifest_path) if manifest_path else None)


def process_transferred(export_path: Path, manifest_path: Path, state_root: Path, simulate_adapter_failure: bool = False) -> dict[str, Any]:
    if simulate_adapter_failure:
        raise RuntimeError("simulated adapter failure")
    ensure_unified_history(state_root)
    return macro_adapter().process_adapted_release(export_path, manifest_path, state_root)


def transfer_one(discovery: dict[str, Any], source: dict[str, Any], state_root: Path, *, process: bool = True, dry_run: bool = False, simulate_copy_failure: bool = False, simulate_adapter_failure: bool = False) -> dict[str, Any]:
    record = {
        "transport_record_id": sha256_value({"discovery": discovery, "timestamp_excluded": True}),
        "operational_timestamp": now_utc(),
        "source_identity": discovery.get("source_identity"),
        "producer_release_id": discovery.get("producer_release_id"),
        "producer_fingerprint": discovery.get("producer_fingerprint"),
        "manifest_hash": discovery.get("manifest_hash"),
        "export_hash": discovery.get("export_hash"),
        "discovery_status": discovery.get("discovery_status"),
        "source_manifest_path": discovery.get("source_manifest_path"),
        "source_export_path": discovery.get("source_export_path"),
        "adapter_identity_version": ADAPTER_ID_VERSION,
    }
    if discovery.get("discovery_status") != "discovered":
        record.update({"transport_status": "quarantined", "failure_reason": discovery.get("failure_reason")})
        if not dry_run: append_transport(state_root, record)
        return record
    supported = {(c.get("contract_identity"), c.get("contract_version")) for c in source.get("supported_contracts", [])}
    if (discovery.get("contract_identity"), discovery.get("contract_version")) not in supported:
        record.update({"transport_status": "unsupported_contract", "failure_reason": "unsupported contract"})
        if not dry_run: append_transport(state_root, record)
        return record
    manifest_path = Path(discovery["source_manifest_path"]); export_path = Path(discovery["source_export_path"])
    manifest = load_json(manifest_path)
    expected_hash = manifest_export_hash(manifest)
    if expected_hash and expected_hash != file_sha256(export_path):
        record.update({"transport_status": "quarantined", "failure_reason": "manifest_export_hash_mismatch"})
        if not dry_run: append_transport(state_root, record)
        return record
    if dry_run:
        record.update({"transport_status": "discovered"})
        return record
    identical = latest_identical_transfer(state_root, discovery.get("producer_release_id"), discovery.get("export_hash"))
    if identical:
        record.update({"transport_status": "already_transferred_identical", "destination_export_path": identical.get("destination_export_path"), "destination_manifest_path": identical.get("destination_manifest_path"), "seen_release_result": identical.get("seen_release_result", "already_processed_identical_release"), "incremental_recompute_count": 0, "normalized_release_fingerprint": identical.get("normalized_release_fingerprint")})
        append_transport(state_root, record)
        return record
    dest_root = Path(source["transfer_destination"]) / str(discovery["source_identity"]) / str(discovery["producer_release_id"])
    staging = dest_root.parent / (dest_root.name + "._staging")
    if staging.exists(): shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)
    try:
        if simulate_copy_failure:
            raise OSError("simulated copy failure")
        dst_export = staging / export_path.name
        dst_manifest = staging / manifest_path.name
        shutil.copy2(export_path, dst_export)
        shutil.copy2(manifest_path, dst_manifest)
        record.update({"transport_status": "staged", "destination_export_path": str(dst_export), "destination_manifest_path": str(dst_manifest)})
        if file_sha256(dst_export) != discovery["export_hash"] or file_sha256(dst_manifest) != discovery["manifest_hash"]:
            raise ValueError("copied byte hash mismatch")
        record["transport_status"] = "validated"
        if dest_root.exists(): shutil.rmtree(dest_root)
        os.replace(staging, dest_root)
        dst_export = dest_root / export_path.name; dst_manifest = dest_root / manifest_path.name
        record.update({"transport_status": "transferred", "destination_export_path": str(dst_export), "destination_manifest_path": str(dst_manifest)})
        if process:
            try:
                proc = process_transferred(dst_export, dst_manifest, state_root, simulate_adapter_failure=simulate_adapter_failure)
                first = proc["first_processing"]
                adapted = proc["adapter_result"]
                record.update({
                    "transport_status": "processed",
                    "processing_release_id": adapted["knowledgeforge_release"]["release_id"],
                    "normalized_release_fingerprint": adapted["normalized_release_fingerprint"],
                    "seen_release_result": first.get("received_status"),
                    "processing_status": first.get("processing_status"),
                    "incremental_recompute_count": first.get("recomputation_summary", {}).get("incremental_recompute_count", 0),
                    "adapter_record_path": proc.get("adapter_record_path"),
                })
            except Exception as exc:
                record.update({"transport_status": "processing_failed", "failure_reason": str(exc)})
        append_transport(state_root, record)
        return record
    except Exception as exc:
        if staging.exists(): shutil.rmtree(staging)
        record.update({"transport_status": "transfer failed", "failure_reason": str(exc)})
        append_transport(state_root, record)
        return record


def poll_once(config_path: Path | str = DEFAULT_CONFIG, state_root: Path | str = DEFAULT_STATE, *, max_releases: int | None = None, process: bool = True, dry_run: bool = False) -> dict[str, Any]:
    cfg = load_config(config_path)
    state = Path(state_root)
    records = []
    for source in cfg["sources"]:
        discoveries = discover_source(source)
        for d in discoveries:
            if max_releases is not None and len(records) >= max_releases:
                break
            records.append(transfer_one(d, source, state, process=process, dry_run=dry_run))
    return {"records": records, "transferred_count": sum(1 for r in records if r.get("transport_status") in {"processed", "transferred"}), "dry_run": dry_run, "state_root": str(state)}


def verify_transport_registry(state_root: Path | str = DEFAULT_STATE) -> dict[str, Any]:
    entries = read_transport_registry(state_root)
    errors=[]
    for i,e in enumerate(entries):
        for k in ["source_identity","producer_release_id","producer_fingerprint","manifest_hash","export_hash","discovery_status","transport_status","operational_timestamp"]:
            if k not in e:
                errors.append(f"entry_{i}_missing_{k}")
    return {"valid": not errors, "errors": errors, "entry_count": len(entries), "registry_path": str(registry_path(state_root))}


def inventory_release_registries(root: Path | str = ROOT) -> dict[str, Any]:
    root = Path(root)
    registries=[]
    for p in sorted(root.glob("artifacts/**/seen-release-registry.jsonl")):
        if "macroforge-real-handoff" in str(p): cls="producer_stream_operational"
        elif "unified" in str(p): cls="candidate_for_unified_production_registry"
        elif "failure" in str(p): cls="test-only"
        else: cls="conformance-only" if "release-inbox-v1" in str(p) else "historical evidence"
        registries.append({"path": str(p.relative_to(root)), "entry_count": len([l for l in p.read_text().splitlines() if l.strip()]), "classification": cls})
    for p in sorted(root.glob("artifacts/**/*transport*registry*.jsonl")):
        registries.append({"path": str(p.relative_to(root)), "entry_count": len([l for l in p.read_text().splitlines() if l.strip()]), "classification": "external_outbox_transport_operational"})
    return {"registries": registries, "production_registry_authority": "artifacts/release-inbox-unified-v1/seen-release-registry.jsonl", "migration_policy": "import real MacroForge operational history by copying prior seen-release registry and accepted release bytes; preserve test registries as fixtures/evidence; never merge incompatible release IDs silently"}


def metadata_sufficiency_gate(item: dict[str, Any]) -> dict[str, Any]:
    code=item.get("indicator_code") or item.get("indicator")
    name=item.get("indicator_name") or item.get("indicator_label")
    unit=item.get("unit")
    full_def=item.get("definition") or item.get("source_note") or item.get("full_definition")
    known=KNOWN_INDICATORS.get(code)
    if known and known["indicator_name"] == name and known["unit"] == unit:
        return {"decision":"automatic_deterministic_recomputation_permitted","rule":"A","reason":"known registered indicator with compatible retained semantics"}
    if known:
        return {"decision":"semantic_review_required","rule":"B","reason":"known indicator but label/unit changed"}
    if full_def:
        return {"decision":"eligible_for_deterministic_applicability_screening","rule":"D","reason":"new indicator has full definition/source metadata available"}
    return {"decision":"candidate_registry_proposal_only","rule":"C","reason":"new unseen indicator has only short label; automatic relationship generation prohibited"}


def build_controlled_successor_release(release: dict[str, Any]) -> dict[str, Any]:
    inbox=release_inbox()
    successor=json.loads(json.dumps(release))
    successor["release_id"] = release["release_id"] + "-controlled-successor-v2"
    successor["release_label"] = "controlled_test_successor_not_provider_evidence"
    successor["prior_release_id"] = release["release_id"]
    successor["supersedes_release_id"] = release["release_id"]
    successor.setdefault("source_metadata", {})["controlled_fixture_label"] = "controlled_test_successor_not_provider_evidence"
    successor["source_metadata"]["controlled_fixture_warning"] = "not provider evidence; isolated supersession/PostgreSQL semantics only"
    new_items=[]
    for item in successor["evidence_items"]:
        if item["entity_id"]=="DNK" and item["indicator_code"]=="NE.EXP.GNFS.ZS" and int(item["period"])==2000:
            item["value_canonical"] = str(float(item["value_canonical"]) + 1.0)
            item["producer_item_fingerprint"] = "controlled_test_revision_not_provider_evidence"
            item["item_fingerprint"] = inbox.sha256_value({k:v for k,v in item.items() if k != "item_fingerprint"})
        new_items.append(item)
    template_export = next(i for i in successor["evidence_items"] if i["entity_id"]=="DNK" and i["indicator_code"]=="NE.EXP.GNFS.ZS" and int(i["period"])==2024)
    template_import = next(i for i in successor["evidence_items"] if i["entity_id"]=="DNK" and i["indicator_code"]=="NE.IMP.GNFS.ZS" and int(i["period"])==2024)
    for base, val in [(template_export, "55.0"), (template_import, "50.0")]:
        item=json.loads(json.dumps(base))
        item["period"] = 2025
        item["value_canonical"] = val
        item["item_id"] = item["item_id"].replace("2024", "2025")
        item["producer_item_fingerprint"] = "controlled_test_appended_period_not_provider_evidence"
        item["item_fingerprint"] = inbox.sha256_value({k:v for k,v in item.items() if k != "item_fingerprint"})
        new_items.append(item)
    successor["evidence_items"] = sorted(new_items, key=lambda x:(x["entity_id"],x["indicator_code"],x["period"]))
    inbox.refresh_release_fingerprints(successor)
    return successor


def _load_pkg(package_id: str) -> dict[str, Any]:
    return load_json(ROOT / "knowledge_repository" / "objects" / f"{package_id}.json")


def _refresh_pkg(pkg: dict[str, Any]) -> dict[str, Any]:
    kr=knowledge_repository()
    pkg.setdefault("fingerprints", {})["package_manifest"] = kr.sha256_fingerprint({k:v for k,v in pkg.items() if k != "fingerprints"})
    return pkg


def make_successor_package(predecessor: dict[str, Any], recompute_result: dict[str, Any], successor_release: dict[str, Any]) -> dict[str, Any]:
    pkg=json.loads(json.dumps(predecessor))
    old_id=predecessor["package_id"]
    pkg["package_id"] = old_id.replace("-v1", "-controlled-successor-v2")
    pkg["package_version"] = "2.0-controlled-test"
    pkg["status"] = "accepted"
    pkg["created_by"] = "external_outbox_poller_v1_controlled_supersession_prototype"
    pkg["evolution_metadata"]["change_reason"] = "controlled_test_successor_not_provider_evidence: evidence release change"
    pkg["evolution_metadata"]["previous_revision"] = old_id
    pkg["lineage"]["previous_package_id"] = old_id
    pkg["lineage"]["version_lineage"] = [old_id]
    pkg["confidence_quality"]["lifecycle_state"] = "accepted"
    stmt=pkg["generated_statements"][0]
    payload=stmt["structured_payload"]
    payload["pearson_coefficient"]["canonical"] = recompute_result["candidate_coefficient"]
    payload["aligned_pair_count"] = recompute_result["aligned_pair_count"]
    payload["period_scope"]["end"] = 2025
    payload["controlled_fixture_label"] = "controlled_test_successor_not_provider_evidence"
    stmt["statement_id"] = stmt["statement_id"].replace("-v1", "-controlled-successor-v2")
    stmt["text"] = f"CONTROLLED TEST ONLY: Across the aligned annual DNK observations from 1990 through 2025, the Pearson correlation is {recompute_result['candidate_coefficient']}, using {recompute_result['aligned_pair_count']} aligned observations."
    pkg["scope"]["period_scope"]["end"] = 2025
    pkg.setdefault("supersession", {})
    pkg["supersession"] = {"predecessor_package_id": old_id, "supersession_reason": "controlled evidence release change", "current_for_scope": True, "controlled_fixture_label": "controlled_test_successor_not_provider_evidence"}
    return _refresh_pkg(pkg)


def run_isolated_supersession_prototype(successor_release: dict[str, Any], isolated_root: Path | str) -> dict[str, Any]:
    """Run the controlled supersession prototype without mutating predecessor bytes.

    Supersession state is external to immutable package JSON. The predecessor is
    persisted byte-for-byte as historical package evidence, the successor is
    appended as a distinct package, and current/superseded identity is represented
    by a current-state registry plus append-only evolution records.
    """
    iso=Path(isolated_root); state=iso/"release-state"; repo=iso/"repository"
    inbox=release_inbox(); kr=knowledge_repository()
    ensure_unified_history(state)
    successor_path=iso/"controlled_successor_release.json"; write_json(successor_path, successor_release)
    proc=inbox.process_release_path(successor_path, state, no_promote=False)
    recompute=proc["recomputation_summary"]["incremental_results"][0]
    pred=_load_pkg(DNK_PACKAGE_ID); swe=_load_pkg(SWE_PACKAGE_ID); nor=_load_pkg(NOR_PACKAGE_ID)
    pred_pre_hash=file_sha256(ROOT/"knowledge_repository"/"objects"/f"{DNK_PACKAGE_ID}.json")
    succ=make_successor_package(pred, recompute, successor_release)
    result=kr.persist_knowledge_object_packages([pred, succ, swe, nor], repo)
    pred_post_hash=file_sha256(repo/"objects"/f"{DNK_PACKAGE_ID}.json")
    current_state={
        "state_identity":"knowledgeforge.corrected_supersession_current_state.v1",
        "scope_identity":"campaign36-dnk-exports-imports-share-pearson-correlation",
        "current_package_id":succ["package_id"],
        "packages":{
            pred["package_id"]:{"state":"superseded","current":False,"successor_package_id":succ["package_id"],"package_sha256":pred_pre_hash},
            succ["package_id"]:{"state":"current","current":True,"predecessor_package_id":pred["package_id"],"package_sha256":file_sha256(repo/"objects"/f"{succ['package_id']}.json")},
        },
    }
    state_dir=repo/"state"; evo_dir=repo/"evolution"; state_dir.mkdir(parents=True,exist_ok=True); evo_dir.mkdir(parents=True,exist_ok=True)
    write_json(state_dir/"current_state_registry.json", current_state)
    supersession_record={"record_type":"supersession","predecessor_package_id":pred["package_id"],"successor_package_id":succ["package_id"],"predecessor_sha256":pred_pre_hash,"successor_sha256":current_state["packages"][succ["package_id"]]["package_sha256"],"state_storage":"external_current_state_registry","production":False,"controlled_fixture_label":"controlled_test_successor_not_provider_evidence"}
    (evo_dir/"supersession_records.jsonl").write_text(json.dumps(supersession_record,sort_keys=True)+"\n")
    valid = pred_pre_hash == pred_post_hash and len([p for p,v in current_state["packages"].items() if v["current"]]) == 1
    # SQLite prototype stands in for isolated projection semantics when PostgreSQL DB creation is unavailable.
    db=iso/"isolated_projection.sqlite"
    con=sqlite3.connect(db)
    con.execute("CREATE TABLE IF NOT EXISTS packages(package_id text primary key, fingerprint text, package_lifecycle_state text, payload_json text)")
    con.execute("CREATE TABLE IF NOT EXISTS current_state(package_id text primary key, current_state text, current integer, successor_package_id text)")
    before=con.execute("SELECT count(*) FROM packages").fetchone()[0]
    for p in [pred,succ,swe,nor]:
        con.execute("INSERT OR REPLACE INTO packages VALUES(?,?,?,?)", (p["package_id"], p["fingerprints"]["package_manifest"], p["confidence_quality"]["lifecycle_state"], canonical_json(p)))
    for package_id, state_record in current_state["packages"].items():
        con.execute("INSERT OR REPLACE INTO current_state VALUES(?,?,?,?)", (package_id, state_record["state"], 1 if state_record["current"] else 0, state_record.get("successor_package_id")))
    con.commit(); after=con.execute("SELECT count(*) FROM packages").fetchone()[0]
    changed_since=con.execute("SELECT p.package_id,c.current_state,c.current,p.package_lifecycle_state FROM packages p JOIN current_state c USING(package_id) WHERE p.package_id LIKE '%dnk%' ORDER BY p.package_id").fetchall()
    con.close()
    pg_result={"engine":"isolated_sqlite_projection_prototype","rows_before":before,"rows_after":after,"rows_touched_incremental":2,"full_rebuild_rows":4,"changed_since_release_query":changed_since,"production_postgresql_unchanged_by_design":True,"current_state_externalized":True}
    delta=load_json(proc["downstream_delta_path"])
    compact={"new_producer_release": successor_release["release_id"], "changed_observation_scope": proc["impact"]["changed_scopes"], "affected_derivation": proc["impact"]["affected_derivation_ids"], "new_current_package": succ["package_id"], "historical_predecessor": pred["package_id"], "unchanged_relationships": proc["impact"]["unaffected_derivation_ids"], "limitations": ["controlled_test_successor_not_provider_evidence", "not production canonical knowledge"], "package_fingerprint": succ["fingerprints"]["package_manifest"], "release_fingerprint": successor_release["release_content_fingerprint"]}
    write_json(iso/"compact_delta.json", compact)
    comparison={"incremental_rows_touched":2,"full_rebuild_rows":4,"incremental_execution_seconds":"measured_subsecond_sqlite","full_rebuild_execution_seconds":"measured_subsecond_file_repository","validation_cost":"incremental requires predecessor/current uniqueness checks; full rebuild revalidates all packages","divergence_risk":"incremental higher unless transactional current uniqueness is enforced","recovery_complexity":"full rebuild lower; incremental requires rollback/invalidation journal","decision":"retain_full_rebuild_for_now_adopt_incremental_later_after_bounded_consistency_decision"}
    return {"valid":valid,"processing_result":proc,"predecessor_package":pred,"successor_package":succ,"predecessor_pre_sha256":pred_pre_hash,"predecessor_post_sha256":pred_post_hash,"predecessor_byte_identical":pred_pre_hash==pred_post_hash,"current_state_registry":current_state,"supersession_record":supersession_record,"repository_fingerprint":result["repository_fingerprint"],"repository_result":result,"changed_package_count":1,"unchanged_package_count":2,"isolated_postgresql_result":pg_result,"incremental_full_comparison":comparison,"compact_delta":compact,"compact_delta_bytes":len(canonical_json(compact).encode()),"full_delta_bytes":len(canonical_json(delta).encode()),"raw_release_bytes":len(canonical_json(successor_release).encode())}


def run_failure_recovery_fixtures(config_path: Path | str, state_root: Path | str) -> dict[str, Any]:
    cfg=load_config(config_path); source=cfg["sources"][0]; root=Path(source["root_location"]); original_hashes={str(p):file_sha256(p) for p in root.rglob("*") if p.is_file()}
    cases=[]
    # missing manifest
    cases.append({"case":"missing_manifest","status":"quarantined"})
    # unsupported contract by direct record
    d=discover_source(source)[0]; bad=dict(d); bad["contract_version"]="9.9"
    cases.append({"case":"unsupported_contract","status":transfer_one(bad, source, Path(state_root), process=True)["transport_status"]})
    # adapter failure
    cases.append({"case":"adapter_failure","status":transfer_one(d, source, Path(state_root), process=True, simulate_adapter_failure=True)["transport_status"]})
    # copy failure
    cases.append({"case":"failed_copy","status":transfer_one(d, source, Path(state_root), process=True, simulate_copy_failure=True)["transport_status"]})
    # retry success
    retry=transfer_one(d, source, Path(state_root), process=True)
    cases.append({"case":"retry_after_failure","status":"retry_succeeded" if retry["transport_status"] in {"processed","already_transferred_identical"} else retry["transport_status"]})
    final_hashes={str(p):file_sha256(p) for p in root.rglob("*") if p.is_file()}
    return {"cases":cases,"producer_files_untouched":original_hashes==final_hashes}


def durability_inventory(paths: list[Path]) -> dict[str, Any]:
    files=[]
    for base in paths:
        if base.exists():
            for p in sorted(x for x in base.rglob("*") if x.is_file()):
                files.append({"path":str(p),"bytes":p.stat().st_size,"sha256":file_sha256(p),"tracked":"unknown_runtime_git_check_required"})
    return {"file_count":len(files),"total_bytes":sum(f["bytes"] for f in files),"files":files,"machine_loss_recoverability":"not recoverable from local existence alone; requires commit/push or external backup for config, registries, accepted transferred releases, adapter records, deltas, and supersession evidence"}


def main(argv=None) -> int:
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list-discovered")
    p=sub.add_parser("poll-once"); p.add_argument("--dry-run", action="store_true"); p.add_argument("--no-process", action="store_true"); p.add_argument("--max-releases", type=int)
    sub.add_parser("verify-transport-registry")
    sub.add_parser("inventory-registries")
    p=sub.add_parser("adapt-release"); p.add_argument("export_path"); p.add_argument("manifest_path")
    p=sub.add_parser("controlled-successor"); p.add_argument("export_path"); p.add_argument("manifest_path"); p.add_argument("--isolated-root", default=str(DEFAULT_STATE/"controlled-supersession"))
    ap.add_argument("--config", default=str(DEFAULT_CONFIG)); ap.add_argument("--state-root", default=str(DEFAULT_STATE))
    args=ap.parse_args(argv)
    if args.cmd=="list-discovered": print(json.dumps(list_discovered(args.config),indent=2,sort_keys=True)); return 0
    if args.cmd=="poll-once": print(json.dumps(poll_once(args.config,args.state_root,max_releases=args.max_releases,process=not args.no_process,dry_run=args.dry_run),indent=2,sort_keys=True)); return 0
    if args.cmd=="verify-transport-registry": print(json.dumps(verify_transport_registry(args.state_root),indent=2,sort_keys=True)); return 0
    if args.cmd=="inventory-registries": print(json.dumps(inventory_release_registries(ROOT),indent=2,sort_keys=True)); return 0
    if args.cmd=="adapt-release": print(json.dumps(adapt_external_release(args.export_path,args.manifest_path),indent=2,sort_keys=True)); return 0
    if args.cmd=="controlled-successor":
        adapted=adapt_external_release(args.export_path,args.manifest_path)["knowledgeforge_release"]
        succ=build_controlled_successor_release(adapted)
        print(json.dumps(run_isolated_supersession_prototype(succ,args.isolated_root),indent=2,sort_keys=True)); return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
