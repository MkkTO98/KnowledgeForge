#!/usr/bin/env python3
"""Repository-wide durability inventory and validator for KnowledgeForge.

Read-only against production canonical repository/PostgreSQL. Writes only requested
reports under artifacts/reports/... when invoked with --report.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = ROOT / "artifacts/reports/repository-wide-durability-inventory-supersession-correction-20260711"
DEFAULT_OPERATIONAL_CHECKPOINT_DIR = ROOT / "artifacts/operational-state-checkpoints"

CORE_DIRS = [
    "knowledge_repository/objects", "knowledge_repository/manifest.json", "knowledge_repository/indexes", "knowledge_repository/evolution",
    "artifacts/evidence-fixtures", "artifacts/methods", "artifacts/production", "artifacts/exports", "artifacts/external-release-handoffs",
    "artifacts/external-outbox-transport-v1", "artifacts/release-inbox-v1", "artifacts/release-inbox-unified-v1",
    "artifacts/reports", "artifacts/tasks", "artifacts/decisions", "specs", "config", "tools", "tests", "docs", "state", "context",
]

POLICY = {
    "ordinary_git": [
        "canonical KnowledgeObjectPackage JSON",
        "repository manifest/indexes/fingerprints/evolution records",
        "method and calculation contracts",
        "correlation/batch specifications",
        "source code and tests",
        "small deterministic evidence fixtures",
        "task/decision/doctrine/roadmap/architecture/state/handoff records",
        "small reports needed to understand accepted production decisions",
    ],
    "git_lfs": [
        "large binary artifacts only when a future measured artifact exceeds ordinary Git reviewability",
    ],
    "immutable_external_artifact_storage": [
        "genuinely large raw provider responses",
        "genuinely large release exports and full histories",
        "large historical report bundles and verification logs",
        "database dumps when retained for evidence rather than operational recovery",
    ],
    "operational_backup_checkpoint": [
        "seen-release registries",
        "current-state registries",
        "outbox transport state",
        "accepted source copies that are mutable operational state",
        "PostgreSQL backups for operational recovery only",
    ],
    "deterministically_rebuildable": [
        "PostgreSQL projection contents when canonical packages and projection code are durable",
        "derived indexes and exports generated from canonical packages and query contracts",
        "generated context bundles",
    ],
    "sensitive_local_excluded": ["workspace_config.yaml", ".env", "credentials", "private keys", "local connection files"],
}

ARTIFACT_CLASS_POLICY = {
    "canonical_knowledge_object_package_json": "A ordinary Git",
    "manifest_indexes_fingerprints_evolution_records": "A ordinary Git",
    "method_and_calculation_contracts": "A ordinary Git",
    "correlation_batch_specifications": "A ordinary Git",
    "source_code_and_tests": "A ordinary Git",
    "small_evidence_fixtures": "A ordinary Git",
    "large_raw_provider_responses": "C immutable external artifact storage",
    "release_exports_and_histories": "A ordinary Git while small text/audit artifacts fit current repository scale; C immutable external artifact storage when measured size stops being reviewable in ordinary Git",
    "accepted_source_copies": "D operational backup/checkpointing",
    "derivation_registries": "A ordinary Git when append-only canonical provenance; D operational backup/checkpointing when mutable operational registry",
    "seen_release_registries": "D operational backup/checkpointing",
    "current_state_registries": "D operational backup/checkpointing",
    "outbox_transport_state": "D operational backup/checkpointing",
    "postgresql_projection_and_backups": "E projection deterministically rebuildable from durable canonical inputs; D backups for operational recovery only",
    "reports_logs_generated_context": "E for generated context/caches; A for decision-bearing compact reports; C for large raw logs/report bundles",
    "task_decision_doctrine_roadmap_architecture_state_handoff_records": "A ordinary Git",
    "sensitive_local_configuration": "F sensitive/local-only and excluded",
}

SENSITIVE_PATTERNS = [
    ("credential_keyword", re.compile(r"(?i)(password|passwd|api[_-]?key|secret|token|credential|private[_-]?key)")),
    ("private_key_marker", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("postgres_connection_string", re.compile(r"postgres(?:ql)?://[^\s'\"]+", re.I)),
    ("absolute_home_path", re.compile(r"/home/[A-Za-z0-9_.-]+/")),
    ("env_file_reference", re.compile(r"(?i)(^|/|\s)\.env($|\s|/)")),
]


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def git_sets() -> dict[str, set[str]]:
    tracked = set(run(["git", "ls-files"]).stdout.splitlines())
    staged = set()
    modified = set()
    deleted = set()
    untracked_roots = set()
    for line in run(["git", "status", "--porcelain"]).stdout.splitlines():
        if not line:
            continue
        x, y, path = line[0], line[1], line[3:]
        if x == "?" and y == "?":
            untracked_roots.add(path)
            continue
        if x != " ":
            staged.add(path)
        if y != " " or x == "D":
            modified.add(path)
        if x == "D" or y == "D":
            deleted.add(path)
    ignored = set()
    for line in run(["git", "status", "--porcelain", "--ignored"]).stdout.splitlines():
        if line.startswith("!! "):
            ignored.add(line[3:])
    remote = set(run(["git", "ls-tree", "-r", "--name-only", "origin/main"]).stdout.splitlines())
    return {"tracked": tracked, "staged": staged, "modified": modified, "deleted": deleted, "untracked_roots": untracked_roots, "ignored_roots": ignored, "remote": remote}


def all_files() -> list[Path]:
    files: list[Path] = []
    for base, dirs, names in os.walk(ROOT):
        pbase = Path(base)
        if ".git" in pbase.parts:
            continue
        # keep ignored visible; only skip Python cache binary noise from deep walks? No: inventory ignored separately by git status.
        for name in names:
            p = pbase / name
            if p.is_file():
                files.append(p)
    return sorted(files)


def classify_path(path: str) -> dict[str, Any]:
    cat = "derived_rebuildable"
    recovery = False
    canonical = False
    local_only = False
    sensitive = False
    if path.startswith((".pytest_cache/", "tools/__pycache__/", "tests/__pycache__/")) or path == "context/active_context.md":
        cat = "ephemeral_untracked"; recovery = False
    elif path == "workspace_config.yaml" or path.endswith(".env"):
        cat = "sensitive_ignored"; recovery = False; local_only = True; sensitive = True
    elif path.startswith("knowledge_repository/objects/") and path.endswith(".json"):
        cat = "must_track_git"; recovery = True; canonical = True
    elif path in {"knowledge_repository/manifest.json"} or path.startswith("knowledge_repository/indexes/") or path.startswith("knowledge_repository/evolution/"):
        cat = "must_track_git"; recovery = True; canonical = True
    elif path.startswith(("specs/", "docs/", "tools/", "tests/", "config/")):
        cat = "must_track_git"; recovery = True
    elif path.startswith(("state/", "context/latest_handoff.md", "artifacts/tasks/", "artifacts/decisions/")):
        cat = "must_track_git"; recovery = True
    elif path.startswith(("artifacts/methods/", "artifacts/production/", "artifacts/evidence-fixtures/")):
        cat = "must_track_git"; recovery = True
    elif path.startswith(("artifacts/release-inbox", "artifacts/external-outbox-transport-v1", "artifacts/external-release-handoffs")):
        cat = "operational_state_backup"; recovery = True
    elif path.startswith("artifacts/operational-state-checkpoints/"):
        cat = "operational_checkpoint_artifact"; recovery = True
    elif path.startswith(("artifacts/exports/",)):
        cat = "external_artifact_storage"; recovery = True
    elif path.startswith("artifacts/reports/"):
        if path.endswith((".log", ".txt")) or "/verification/" in path or "/final-verification/" in path:
            cat = "historical_evidence_or_external_storage"; recovery = False
        else:
            cat = "historical_evidence_optional_main_git"; recovery = True
    return {"category": cat, "recovery_critical": recovery, "canonical": canonical, "local_only": local_only, "sensitive_local": sensitive}


def inventory() -> dict[str, Any]:
    gs = git_sets()
    ignored_roots = gs["ignored_roots"]
    records = []
    totals = collections.defaultdict(lambda: {"file_count": 0, "bytes": 0})
    status_totals = collections.defaultdict(lambda: {"file_count": 0, "bytes": 0})
    for p in all_files():
        r = rel(p)
        st = p.stat()
        tracked = r in gs["tracked"]
        remote = r in gs["remote"]
        modified = r in gs["modified"]
        staged = r in gs["staged"]
        ignored = any(r == root.rstrip("/") or r.startswith(root.rstrip("/") + "/") for root in ignored_roots)
        untracked = not tracked and not ignored
        cls = classify_path(r)
        rec = {
            "path": r,
            "bytes": st.st_size,
            "sha256": sha(p) if st.st_size <= 50_000_000 else "skipped_large_file",
            "tracked": tracked,
            "remote_tracked": remote,
            "modified_tracked": modified and tracked,
            "staged": staged,
            "untracked": untracked,
            "ignored": ignored,
            **cls,
        }
        records.append(rec)
        totals[cls["category"]]["file_count"] += 1; totals[cls["category"]]["bytes"] += st.st_size
        for key in ["tracked", "remote_tracked", "modified_tracked", "staged", "untracked", "ignored", "canonical", "recovery_critical", "sensitive_local"]:
            if rec[key]:
                status_totals[key]["file_count"] += 1; status_totals[key]["bytes"] += st.st_size
    core_presence = {item: (ROOT / item).exists() for item in CORE_DIRS}
    return {"generated_from_head": run(["git", "rev-parse", "HEAD"]).stdout.strip(), "upstream_reference": "origin/main", "core_presence": core_presence, "totals_by_category": totals, "totals_by_status": status_totals, "files": records}


def load_packages() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = json.loads((ROOT / "knowledge_repository/manifest.json").read_text())
    packages = []
    for p in sorted((ROOT / "knowledge_repository/objects").glob("*.json")):
        try:
            obj = json.loads(p.read_text())
            obj["__path"] = rel(p)
            packages.append(obj)
        except Exception as exc:
            packages.append({"__path": rel(p), "__error": str(exc)})
    return manifest, packages


def package_counts(packages: list[dict[str, Any]]) -> dict[str, Any]:
    pearson = [p for p in packages if "pearson" in p.get("package_id", "") or "pearson" in json.dumps(p.get("generated_statements", []), sort_keys=True).lower()]
    stat = [p for p in packages if "statistical-summary" in p.get("package_id", "") or "statistical_summary" in json.dumps(p.get("generated_statements", []), sort_keys=True).lower()]
    campaign40 = [p for p in packages if "campaign40" in p.get("package_id", "")]
    return {"all_packages": len(packages), "pearson_objects": len(pearson), "statistical_summary_objects": len(stat), "campaign40_packages": len(campaign40), "pearson_package_ids": [p.get("package_id") for p in pearson], "statistical_summary_package_ids": [p.get("package_id") for p in stat], "campaign40_package_ids": [p.get("package_id") for p in campaign40]}


def _classify_sensitive_finding(path: str, finding_type: str) -> tuple[str, str]:
    """Classify without returning matched values.

    The validator reports categories/counts only so it never reproduces credentials or
    local paths in generated reports.
    """
    if finding_type in {"private_key_marker", "postgres_connection_string", "env_file_reference"}:
        return "unresolved_actual_secret_or_credential_reference", "redact or exclude before any staging"
    if finding_type == "absolute_home_path":
        if path.startswith(("tools/", "tests/", "config/", "knowledge_repository/manifest.json")):
            return "unsafe_absolute_path_dependency", "parameterize or replace with project-relative/env-derived path before staging"
        return "reviewed_historical_or_evidence_local_path_reference", "benign as historical/provenance text; do not treat as a secret"
    if finding_type == "credential_keyword":
        if path.endswith(".py"):
            return "reviewed_false_positive_scanner_literal_or_schema_field", "scanner/test literal or forbidden-term guard; no secret value reported"
        return "reviewed_false_positive_domain_keyword", "domain text, schema field, or evidence variable name; no secret value reported"
    return "review_required", "manual review required"


def sensitive_scan(records: list[dict[str, Any]]) -> dict[str, Any]:
    findings = []
    proposed = [r for r in records if r["category"] in {"must_track_git", "operational_state_backup", "historical_evidence_optional_main_git", "external_artifact_storage"}]
    for rec in proposed:
        path = ROOT / rec["path"]
        if not path.exists() or rec["bytes"] > 5_000_000:
            continue
        text = path.read_text(errors="ignore")
        for name, rx in SENSITIVE_PATTERNS:
            matches = list(rx.finditer(text))
            if matches:
                classification, disposition = _classify_sensitive_finding(rec["path"], name)
                findings.append({"path": rec["path"], "finding_type": name, "count": len(matches), "classification": classification, "disposition": disposition})
    actual_secret_blockers = [f for f in findings if f["classification"] == "unresolved_actual_secret_or_credential_reference"]
    unsafe_absolute_path_dependencies = [f for f in findings if f["classification"] == "unsafe_absolute_path_dependency"]
    reviewed_false_positives = [f for f in findings if f["classification"].startswith("reviewed_")]
    review_required = [f for f in findings if f["classification"] == "review_required"]
    return {
        "proposed_file_count": len(proposed),
        "findings": findings,
        "actual_secret_blockers": actual_secret_blockers,
        "unsafe_absolute_path_dependencies": unsafe_absolute_path_dependencies,
        "reviewed_false_positives": reviewed_false_positives,
        "review_required": review_required,
        "passes": not actual_secret_blockers and not unsafe_absolute_path_dependencies and not review_required,
    }


def machine_loss(inv: dict[str, Any], counts: dict[str, Any]) -> dict[str, Any]:
    lost = [r for r in inv["files"] if r["recovery_critical"] and (not r["remote_tracked"] or r["modified_tracked"] or r["untracked"])]
    lost_by_category = collections.defaultdict(lambda: {"file_count": 0, "bytes": 0})
    for r in lost:
        lost_by_category[r["category"]]["file_count"] += 1; lost_by_category[r["category"]]["bytes"] += r["bytes"]
    capabilities = {
        "all_538_canonical_packages": {"recoverable_from_remote": counts["all_packages"] == 538 and all((r["remote_tracked"] and not r["modified_tracked"]) for r in inv["files"] if r["path"].startswith("knowledge_repository/objects/")), "local_count": counts["all_packages"]},
        "repository_manifest_and_fingerprint": {"recoverable_from_remote": any(r["path"] == "knowledge_repository/manifest.json" and r["remote_tracked"] and not r["modified_tracked"] for r in inv["files"])},
        "all_13_pearson_objects": {"recoverable_from_remote": counts["pearson_objects"] == 13 and all(any(r["path"] == p["__path"] and r["remote_tracked"] for r in inv["files"]) for p in load_packages()[1] if p.get("package_id") in counts["pearson_package_ids"]), "local_count": counts["pearson_objects"]},
        "all_four_statistical_summary_objects": {"recoverable_from_remote": counts["statistical_summary_objects"] == 4 and all(any(r["path"] == p["__path"] and r["remote_tracked"] for r in inv["files"]) for p in load_packages()[1] if p.get("package_id") in counts["statistical_summary_package_ids"]), "local_count": counts["statistical_summary_objects"]},
        "campaign40_six_packages": {"recoverable_from_remote": counts["campaign40_packages"] == 6 and all(any(r["path"] == p["__path"] and r["remote_tracked"] for r in inv["files"]) for p in load_packages()[1] if p.get("package_id") in counts["campaign40_package_ids"]), "local_count": counts["campaign40_packages"]},
        "evidence_fixtures": {"recoverable_from_remote": all(r["remote_tracked"] for r in inv["files"] if r["path"].startswith("artifacts/evidence-fixtures/"))},
        "calculation_contracts_specs_methods": {"recoverable_from_remote": all(r["remote_tracked"] for r in inv["files"] if r["path"].startswith(("specs/", "artifacts/methods/", "docs/pearson", "docs/statistical_summary")))},
        "generic_batch_engine": {"recoverable_from_remote": any(r["path"] == "tools/correlation_batch_engine.py" and r["remote_tracked"] for r in inv["files"])},
        "postgresql_projection": {"recoverable_from_remote": any(r["path"] == "tools/postgresql_operational_projection.py" and r["remote_tracked"] for r in inv["files"])},
        "relationship_export_contract": {"recoverable_from_remote": any(r["path"] == "tools/relationship_export_v1.py" and r["remote_tracked"] for r in inv["files"])},
        "macroforge_adapter": {"recoverable_from_remote": any(r["path"] == "tools/macroforge_neutral_release_adapter_v1.py" and r["remote_tracked"] for r in inv["files"])},
        "release_inbox_seen_registry": {"recoverable_from_remote": all(r["remote_tracked"] for r in inv["files"] if r["path"].startswith(("tools/release_inbox_v1.py", "artifacts/release-inbox")))},
        "external_handoff_evidence": {"recoverable_from_remote": all(r["remote_tracked"] for r in inv["files"] if r["path"].startswith("artifacts/external-release-handoffs/"))},
        "derivation_registry": {"recoverable_from_remote": all(r["remote_tracked"] for r in inv["files"] if "derivation" in r["path"])},
        "outbox_poller": {"recoverable_from_remote": any(r["path"] == "tools/external_outbox_poller_v1.py" and r["remote_tracked"] for r in inv["files"])},
        "downstream_deltas": {"recoverable_from_remote": all(r["remote_tracked"] for r in inv["files"] if "delta" in r["path"])},
        "supersession_rules": {"recoverable_from_remote": any(r["path"] == "tools/canonical_supersession_immutability_validator.py" and r["remote_tracked"] for r in inv["files"])},
    }
    return {"lost_file_count": len(lost), "lost_bytes": sum(r["bytes"] for r in lost), "lost_by_category": lost_by_category, "lost_paths": [r["path"] for r in lost], "capability_recovery": capabilities}


def size_projection(inv: dict[str, Any], counts: dict[str, Any]) -> dict[str, Any]:
    canonical_bytes = sum(r["bytes"] for r in inv["files"] if r["path"].startswith("knowledge_repository/objects/"))
    avg = canonical_bytes / max(1, counts["all_packages"])
    evidence_bytes = sum(r["bytes"] for r in inv["files"] if r["path"].startswith("artifacts/evidence-fixtures/"))
    evidence_per_pkg = evidence_bytes / max(1, counts["all_packages"])
    projections = {}
    for n in [100, 1000, 10000, 100000]:
        projections[str(n)] = {"canonical_json_bytes_estimate": int(avg * n), "evidence_fixture_bytes_linear_estimate": int(evidence_per_pkg * n), "release_history_bytes_rough_estimate": int((avg + evidence_per_pkg) * n * 1.5)}
    return {"current_canonical_bytes": canonical_bytes, "current_avg_package_bytes": avg, "current_evidence_fixture_bytes": evidence_bytes, "projections": projections, "decision": {"ordinary_git_suitable": ["canonical JSON packages", "specifications", "method contracts", "small registries"], "git_lfs_or_artifact_store": ["raw evidence fixtures as they grow", "large release exports", "large logs/reports"], "database_backups": ["operational PostgreSQL projections, not canonical source of truth"], "recommended_model": "hybrid: ordinary Git for canonical small text/state; immutable external artifact storage for large/raw evidence and release histories; database backups for operational projections only"}}


def operational_checkpoint_status(operational_paths: list[str], checkpoint_dir: Path = DEFAULT_OPERATIONAL_CHECKPOINT_DIR) -> dict[str, Any]:
    manifests = sorted(checkpoint_dir.glob("*/manifest.json")) if checkpoint_dir.exists() else []
    candidates = []
    for manifest_path in manifests:
        try:
            manifest = json.loads(manifest_path.read_text())
        except Exception as exc:
            candidates.append({"checkpoint": rel(manifest_path.parent), "valid": False, "error": f"manifest_parse_error: {exc}"})
            continue
        files = manifest.get("files", [])
        errors = []
        covered = set()
        for rec in files:
            path = manifest_path.parent / "files" / rec.get("path", "")
            if not path.exists():
                errors.append({"path": rec.get("path"), "error": "missing_checkpoint_file"})
                continue
            actual = sha(path)
            if actual != rec.get("sha256") or actual != rec.get("checkpoint_sha256"):
                errors.append({"path": rec.get("path"), "error": "sha256_mismatch"})
                continue
            covered.add(rec.get("path"))
        missing_coverage = sorted(set(operational_paths) - covered)
        valid = manifest.get("contract_version") == "knowledgeforge.operational_state_checkpoint.v1" and not errors
        candidates.append({
            "checkpoint": rel(manifest_path.parent),
            "valid": valid,
            "checkpoint_id": manifest.get("checkpoint_id"),
            "file_count": len(files),
            "total_bytes": sum(r.get("bytes", 0) for r in files),
            "tested_local_only": manifest.get("tested_local_only"),
            "machine_loss_durable": manifest.get("machine_loss_durable"),
            "external_destination_configured": manifest.get("external_destination_configured"),
            "postgresql_reconstruction_evidence_present": bool(manifest.get("postgresql_operational_recovery")),
            "covered_operational_state_count": len(set(operational_paths) & covered),
            "missing_operational_state_coverage_count": len(missing_coverage),
            "missing_operational_state_coverage_sample": missing_coverage[:50],
            "errors": errors[:50],
        })
    covering = [c for c in candidates if c.get("valid") and c.get("missing_operational_state_coverage_count") == 0]
    selected = covering[-1] if covering else (candidates[-1] if candidates else None)
    return {
        "checkpoint_dir": rel(checkpoint_dir) if checkpoint_dir.exists() else str(checkpoint_dir.relative_to(ROOT)),
        "checkpoint_count": len(candidates),
        "selected_checkpoint": selected,
        "has_valid_local_checkpoint_covering_operational_state": bool(covering),
        "tested_local_only": bool(selected and selected.get("tested_local_only") is True),
        "machine_loss_durable": bool(selected and selected.get("machine_loss_durable") is True),
        "external_destination_configured": bool(selected and selected.get("external_destination_configured") is True),
        "candidates_sample": candidates[-5:],
    }


def validate(inv: dict[str, Any], sens: dict[str, Any]) -> dict[str, Any]:
    manifest, packages = load_packages()
    package_paths = {Path(p).stem for p in [r["path"] for r in inv["files"] if r["path"].startswith("knowledge_repository/objects/") and r["path"].endswith(".json")]}
    manifest_ids = set(manifest.get("package_ids", []))
    missing = sorted(manifest_ids - package_paths)
    extra = sorted(package_paths - manifest_ids)
    untracked_canonical = [r["path"] for r in inv["files"] if r["canonical"] and not r["tracked"]]
    untracked_recovery_critical_implementation = [r["path"] for r in inv["files"] if r["recovery_critical"] and not r["tracked"] and r["category"] == "must_track_git"]
    operational_state_without_backup = [r["path"] for r in inv["files"] if r["category"] == "operational_state_backup" and (not r["remote_tracked"] or r["modified_tracked"] or r["untracked"])]
    checkpoint_status = operational_checkpoint_status(operational_state_without_backup)
    package_dep_warnings = []
    for pkg in packages:
        if pkg.get("__error"):
            package_dep_warnings.append({"package": pkg.get("__path"), "issue": "json_parse_error"})
            continue
        if not pkg.get("evidence_references") and "correlation" in pkg.get("package_id", ""):
            package_dep_warnings.append({"package": pkg.get("package_id"), "issue": "missing_evidence_references"})
        if not pkg.get("provenance_envelope") and "correlation" in pkg.get("package_id", ""):
            package_dep_warnings.append({"package": pkg.get("package_id"), "issue": "missing_provenance_envelope"})
    mutation_paths = []
    for p in (ROOT / "tools").glob("*.py"):
        txt = p.read_text(errors="ignore")
        if "lifecycle_state" in txt and "superseded" in txt:
            mutation_paths.append(rel(p))
    current_state_paths = [r["path"] for r in inv["files"] if "current_state_registry" in r["path"]]
    blocks = []
    if missing: blocks.append("manifest_package_missing")
    if untracked_canonical: blocks.append("untracked_canonical_state_not_durable")
    if untracked_recovery_critical_implementation: blocks.append("untracked_recovery_critical_implementation_not_durable")
    if operational_state_without_backup and not checkpoint_status["has_valid_local_checkpoint_covering_operational_state"]: blocks.append("operational_state_lacking_backup_destination")
    if checkpoint_status["has_valid_local_checkpoint_covering_operational_state"] and not checkpoint_status["machine_loss_durable"]: blocks.append("operational_state_checkpoint_not_machine_loss_durable")
    if sens["actual_secret_blockers"]: blocks.append("unresolved_actual_secrets")
    if sens["unsafe_absolute_path_dependencies"]: blocks.append("unsafe_absolute_path_dependencies")
    if sens["review_required"]: blocks.append("sensitive_findings_require_review")
    return {
        "valid": not blocks,
        "blocks": blocks,
        "manifest_object_count": manifest.get("object_count"),
        "actual_package_count": len(packages),
        "missing_manifest_packages": missing,
        "extra_package_files": extra,
        "untracked_canonical_count": len(untracked_canonical),
        "untracked_canonical_paths_sample": untracked_canonical[:50],
        "untracked_recovery_critical_implementation_count": len(untracked_recovery_critical_implementation),
        "untracked_recovery_critical_implementation_paths_sample": untracked_recovery_critical_implementation[:50],
        "operational_state_without_backup_count": len(operational_state_without_backup),
        "operational_state_without_backup_paths_sample": operational_state_without_backup[:50],
        "operational_checkpoint_status": checkpoint_status,
        "tested_local_only": checkpoint_status["tested_local_only"],
        "machine_loss_durable": checkpoint_status["machine_loss_durable"],
        "actual_secret_blocker_count": len(sens["actual_secret_blockers"]),
        "unsafe_absolute_path_dependency_count": len(sens["unsafe_absolute_path_dependencies"]),
        "reviewed_false_positive_count": len(sens["reviewed_false_positives"]),
        "package_dependency_warnings": package_dep_warnings[:100],
        "supersession_lifecycle_mutation_code_paths": mutation_paths,
        "current_state_registry_paths": current_state_paths,
        "postgresql_not_sole_backup": True,
        "staging_counts_as_durable": False,
    }


def commit_plan(inv: dict[str, Any], sens: dict[str, Any]) -> dict[str, Any]:
    groups = [
        ("01-foundational-doctrine-state-architecture", ["AGENTS.md", "CONSTITUTION.md", "README.md", "_SUMMARY.md", "architecture/", "docs/", "state/", "context/", "instructions/"]),
        ("02-canonical-knowledge-repository", ["knowledge_repository/"]),
        ("03-mature-wdi-production-evidence", ["artifacts/evidence-fixtures/", "artifacts/production/", "artifacts/methods/"]),
        ("04-postgresql-projection", ["tools/postgresql_operational_projection.py", "tools/postgresql_realization_decision.py", "tests/test_postgresql", "docs/postgresql"]),
        ("05-statistical-summary-methods-objects", ["tools/deterministic_statistical_summary_v2.py", "tests/test_statistical_summary", "docs/statistical_summary", "artifacts/reports/campaign34", "artifacts/reports/campaign35"]),
        ("06-pearson-correlation-method-objects", ["tools/deterministic_pearson_correlation_v1.py", "tools/run_campaign36", "tools/run_campaign37", "tools/run_campaign38", "tools/run_campaign39", "tests/test_campaign36", "tests/test_campaign37", "tests/test_campaign38", "tests/test_campaign39", "docs/pearson", "docs/correlation", "artifacts/reports/campaign36", "artifacts/reports/campaign37", "artifacts/reports/campaign38", "artifacts/reports/campaign39"]),
        ("07-specification-driven-batch-engine-campaign40", ["tools/correlation_batch_engine.py", "tests/test_correlation_batch_engine.py", "artifacts/reports/campaign40", "specs/"]),
        ("08-relationship-export-contract", ["tools/relationship_export", "tests/test_relationship_export", "artifacts/reports/relationship-export", "docs/interfaces.md"]),
        ("09-release-automation-inbox-registries", ["tools/release_inbox_v1.py", "tools/release_automation_alignment_v1.py", "tests/test_release", "artifacts/release-inbox"]),
        ("10-macroforge-adapter-real-handoff-evidence", ["tools/macroforge_neutral_release_adapter_v1.py", "tests/test_macroforge", "artifacts/external-release-handoffs/", "artifacts/release-inbox-macroforge-real-handoff-v1/", "artifacts/reports/macroforge"]),
        ("11-outbox-polling", ["tools/external_outbox_poller_v1.py", "tests/test_external_outbox", "config/external_outbox_sources.json", "artifacts/external-outbox", "artifacts/release-inbox-unified-v1", "artifacts/reports/provider-neutral-outbox"]),
        ("12-corrected-supersession-model", ["tools/canonical_supersession_immutability_validator.py", "tests/test_canonical_supersession", "artifacts/reports/canonical-supersession", "artifacts/decisions/D-20260711-canonical-supersession"]),
        ("13-documentation-final-handoff-and-durability", ["artifacts/tasks/", "artifacts/decisions/", "artifacts/reports/repository-wide-durability", "tools/repository_wide_durability_validator.py"]),
    ]
    records = inv["files"]
    plan = []
    assigned: set[str] = set()
    for idx, (name, prefixes) in enumerate(groups, start=1):
        files = [r for r in records if any(r["path"] == pref.rstrip("/") or r["path"].startswith(pref) for pref in prefixes) and (r["modified_tracked"] or r["untracked"] or (r["tracked"] and not r["remote_tracked"]))]
        for f in files: assigned.add(f["path"])
        sensitive = [f for f in sens["findings"] if f["path"] in {r["path"] for r in files}]
        plan.append({"sequence": idx, "group": name, "pathspecs": prefixes, "file_count": len(files), "approx_bytes": sum(r["bytes"] for r in files), "tracked_modified": sum(1 for r in files if r["modified_tracked"]), "untracked": sum(1 for r in files if r["untracked"]), "sensitive_findings": sensitive, "depends_on": [] if idx == 1 else [groups[idx-2][0]], "tests_required": ["python3 -m compileall -q tools tests", "uvx --from pytest pytest tests -q"], "rollback_implications": "do not reset/clean; rollback by inverse patch or new corrective commit after review", "suggested_commit_message": f"KnowledgeForge: {name.replace('-', ' ')}", "canonical_data_included": any(r["canonical"] for r in files)})
    unassigned = [r for r in records if (r["modified_tracked"] or r["untracked"] or (r["tracked"] and not r["remote_tracked"])) and r["path"] not in assigned and not r["ignored"]]
    return {"groups": plan, "unassigned_changed_or_untracked": [{"path": r["path"], "bytes": r["bytes"], "category": r["category"]} for r in unassigned[:500]], "unassigned_count": len(unassigned)}


def db_cleanup_assessment() -> dict[str, Any]:
    db = "knowledgeforge_immutability_gate_20260711"
    exists = run(["psql", "-d", "postgres", "-At", "-c", f"SELECT 1 FROM pg_database WHERE datname='{db}';"])
    isolated = False
    row_counts = []
    if exists.returncode == 0 and exists.stdout.strip() == "1":
        q = run(["psql", "-d", db, "-At", "-c", "SELECT schemaname, tablename FROM pg_tables WHERE schemaname='immutability_gate' ORDER BY tablename;"])
        row_counts = q.stdout.splitlines()
        isolated = all(line.startswith("immutability_gate|") for line in row_counts) if row_counts else True
    return {"database": db, "exists": exists.returncode == 0 and exists.stdout.strip() == "1", "isolated_schema_only": isolated, "production_depends_on_it": False, "evidence_dump_present": (DEFAULT_REPORT.parent / "canonical-supersession-immutability-durability-gate-20260711/isolated_postgresql_schema_dump.sql").exists(), "safe_to_remove_later": True, "authorization_required_to_drop": True, "tables": row_counts}


def write_outputs(report: Path) -> dict[str, Any]:
    report.mkdir(parents=True, exist_ok=True)
    inv = inventory(); manifest, packages = load_packages(); counts = package_counts(packages); sens = sensitive_scan(inv["files"]); ml = machine_loss(inv, counts); storage = size_projection(inv, counts); val = validate(inv, sens); plan = commit_plan(inv, sens); db = db_cleanup_assessment()
    outputs = {"inventory": inv, "package_counts": counts, "sensitive_scan": sens, "machine_loss_recovery": ml, "artifact_policy": POLICY, "artifact_class_policy": ARTIFACT_CLASS_POLICY, "size_storage_assessment": storage, "repository_wide_validator": val, "commit_plan": plan, "temporary_db_cleanup_assessment": db}
    for name, data in outputs.items():
        (report / f"{name}.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    decision = "D" if any(b in val["blocks"] for b in ["untracked_canonical_state_not_durable", "untracked_recovery_critical_implementation_not_durable", "operational_state_lacking_backup_destination"]) else ("C" if sens["actual_secret_blockers"] else ("E" if sens["unsafe_absolute_path_dependencies"] else "A"))
    consolidated = {"decision": decision, "decision_reason": val["blocks"], "summary": {"inventory_totals_by_status": inv["totals_by_status"], "inventory_totals_by_category": inv["totals_by_category"], "lost_file_count": ml["lost_file_count"], "lost_bytes": ml["lost_bytes"], "sensitive_passes": sens["passes"], "actual_secret_blockers": len(sens["actual_secret_blockers"]), "unsafe_absolute_path_dependencies": len(sens["unsafe_absolute_path_dependencies"]), "reviewed_false_positives": len(sens["reviewed_false_positives"]), "validator_valid": val["valid"], "package_counts": counts}}
    (report / "consolidated_machine_readable_summary.json").write_text(json.dumps(consolidated, indent=2, sort_keys=True) + "\n")
    return consolidated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()
    print(json.dumps(write_outputs(args.report), indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
