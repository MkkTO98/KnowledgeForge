#!/usr/bin/env python3
"""Create, validate, and restore KnowledgeForge operational-state checkpoints.

This tool is intentionally generic and deterministic over file content. It does
not mutate canonical packages, does not write production PostgreSQL, and does not
claim machine-loss durability for same-host checkpoints.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_VERSION = "knowledgeforge.operational_state_checkpoint.v1"
DEFAULT_CONFIG = ROOT / "config/protected_state_v1.json"
DEFAULT_DESTINATION = ROOT / "artifacts/operational-state-checkpoints"


class CheckpointError(RuntimeError):
    pass


def rel(path: Path, root: Path = ROOT) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def display_path(path: Path, root: Path = ROOT) -> str:
    try:
        return rel(path, root)
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, separators=(",", ": ")) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(data))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)


@dataclass(frozen=True)
class ExclusionRules:
    path_globs: tuple[str, ...]
    content_regexes: tuple[re.Pattern[str], ...]

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "ExclusionRules":
        raw = config.get("sensitive_exclusions", {})
        return cls(
            path_globs=tuple(raw.get("path_globs", [])),
            content_regexes=tuple(re.compile(p, re.I) for p in raw.get("content_regexes", [])),
        )

    def path_excluded(self, rel_path: str) -> bool:
        name = Path(rel_path).name
        return any(fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(name, pat) for pat in self.path_globs)

    def content_excluded(self, path: Path) -> bool:
        if path.stat().st_size > 5_000_000:
            return False
        text = path.read_text(errors="ignore")
        return any(rx.search(text) for rx in self.content_regexes)


def protected_entries(config: dict[str, Any]) -> list[dict[str, Any]]:
    entries = config.get("protected_paths", [])
    if not isinstance(entries, list):
        raise CheckpointError("protected_paths must be a list")
    return entries


def iter_protected_files(config: dict[str, Any], root: Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = root or ROOT
    exclusions = ExclusionRules.from_config(config)
    files: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for entry in protected_entries(config):
        rel_base = entry["path"].rstrip("/")
        base = root / rel_base
        if not base.exists():
            if entry.get("required"):
                raise CheckpointError(f"required protected path missing: {rel_base}")
            skipped.append({"path": rel_base, "reason": "missing_optional_path", "class": entry.get("class")})
            continue
        paths = [base] if base.is_file() else sorted(p for p in base.rglob("*") if p.is_file())
        for path in paths:
            rp = rel(path, root)
            if exclusions.path_excluded(rp):
                skipped.append({"path": rp, "reason": "sensitive_path_exclusion", "class": entry.get("class")})
                continue
            if exclusions.content_excluded(path):
                skipped.append({"path": rp, "reason": "sensitive_content_exclusion", "class": entry.get("class")})
                continue
            st = path.stat()
            files.append({
                "path": rp,
                "bytes": st.st_size,
                "sha256": sha256_file(path),
                "class": entry.get("class"),
                "source_protected_path": rel_base,
            })
    files.sort(key=lambda x: x["path"])
    skipped.sort(key=lambda x: x["path"])
    return files, skipped


def postgresql_reconstruction_evidence(config: dict[str, Any]) -> dict[str, Any]:
    pg = config.get("postgresql_operational_recovery", {})
    tool = ROOT / pg.get("projection_tool", "tools/postgresql_operational_projection.py")
    cfg = ROOT / pg.get("projection_config_example", "docs/postgresql_projection_config.example")
    canonical = ROOT / pg.get("canonical_source", "knowledge_repository")
    psql = shutil.which("psql")
    pg_dump = shutil.which("pg_dump")
    package_count = len(list((canonical / "objects").glob("*.json"))) if (canonical / "objects").exists() else 0
    manifest = canonical / "manifest.json"
    return {
        "mode": pg.get("mode", "reconstruction_evidence"),
        "production_database_write_allowed": bool(pg.get("production_database_write_allowed", False)),
        "backup_dump_destination_configured": bool(pg.get("backup_dump_destination_configured", False)),
        "same_host_only": True,
        "tested_local_only": True,
        "machine_loss_durable": False,
        "projection_tool": str(tool.relative_to(ROOT)) if tool.exists() else pg.get("projection_tool"),
        "projection_tool_exists": tool.exists(),
        "projection_tool_sha256": sha256_file(tool) if tool.exists() else None,
        "projection_config_example_exists": cfg.exists(),
        "projection_config_example_sha256": sha256_file(cfg) if cfg.exists() else None,
        "canonical_manifest_exists": manifest.exists(),
        "canonical_manifest_sha256": sha256_file(manifest) if manifest.exists() else None,
        "canonical_package_count": package_count,
        "psql_available": bool(psql),
        "pg_dump_available": bool(pg_dump),
        "evidence_statement": "PostgreSQL is recoverable as a projection from durable canonical packages plus projection code/config; no production database backup destination outside the host failure domain is configured by this checkpoint.",
    }


def checkpoint_dir(destination: Path, checkpoint_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "-", checkpoint_id)
    if not safe:
        raise CheckpointError("empty checkpoint id")
    return destination / safe


def create_checkpoint(config_path: Path, destination: Path, checkpoint_id: str | None = None) -> dict[str, Any]:
    config = load_json(config_path)
    if config.get("contract_version") != "knowledgeforge.protected_state.v1":
        raise CheckpointError("unsupported protected-state config contract_version")
    checkpoint_id = checkpoint_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = checkpoint_dir(destination, checkpoint_id)
    if out.exists():
        raise CheckpointError(f"checkpoint already exists: {out}")
    files, skipped = iter_protected_files(config)
    file_root = out / "files"
    for rec in files:
        src = ROOT / rec["path"]
        dst = file_root / rec["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    copied_records = []
    for rec in files:
        dst = file_root / rec["path"]
        copied = dict(rec)
        copied["checkpoint_sha256"] = sha256_file(dst)
        if copied["checkpoint_sha256"] != rec["sha256"]:
            raise CheckpointError(f"copy hash mismatch: {rec['path']}")
        copied_records.append(copied)
    git_head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    manifest: dict[str, Any] = {
        "contract_version": CONTRACT_VERSION,
        "checkpoint_id": checkpoint_id,
        "source_project": "KnowledgeForge",
        "source_root_name": ROOT.name,
        "git_head": git_head,
        "protected_config_path": display_path(config_path),
        "protected_config_sha256": sha256_file(config_path),
        "protected_state_contract_version": config["contract_version"],
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "tested_local_only": True,
        "machine_loss_durable": False,
        "external_destination_configured": False,
        "files": copied_records,
        "skipped": skipped,
        "file_count": len(copied_records),
        "total_bytes": sum(r["bytes"] for r in copied_records),
        "postgresql_operational_recovery": postgresql_reconstruction_evidence(config),
    }
    stable_projection = {k: v for k, v in manifest.items() if k not in {"created_at_utc"}}
    manifest["content_fingerprint_excluding_created_at"] = sha256_text(canonical_json(stable_projection))
    write_json(out / "manifest.json", manifest)
    validation = validate_checkpoint(out)
    write_json(out / "validation.json", validation)
    if not validation["valid"]:
        raise CheckpointError("created checkpoint failed validation")
    return {"checkpoint_path": display_path(out), "manifest": manifest, "validation": validation}


def validate_checkpoint(checkpoint: Path) -> dict[str, Any]:
    manifest_path = checkpoint / "manifest.json"
    if not manifest_path.exists():
        return {"valid": False, "errors": ["manifest_missing"], "checkpoint": str(checkpoint)}
    manifest = load_json(manifest_path)
    errors: list[dict[str, Any] | str] = []
    if manifest.get("contract_version") != CONTRACT_VERSION:
        errors.append("unsupported_checkpoint_contract_version")
    file_root = checkpoint / "files"
    for rec in manifest.get("files", []):
        path = file_root / rec["path"]
        if not path.exists():
            errors.append({"path": rec["path"], "error": "checkpoint_file_missing"})
            continue
        actual = sha256_file(path)
        if actual != rec.get("sha256") or actual != rec.get("checkpoint_sha256"):
            errors.append({"path": rec["path"], "error": "sha256_mismatch", "actual_sha256": actual})
    pg = manifest.get("postgresql_operational_recovery", {})
    if pg.get("production_database_write_allowed"):
        errors.append("production_postgresql_write_not_allowed")
    if manifest.get("machine_loss_durable") is not False:
        errors.append("same_host_checkpoint_must_not_claim_machine_loss_durable")
    if manifest.get("tested_local_only") is not True:
        errors.append("same_host_checkpoint_must_report_tested_local_only")
    return {
        "valid": not errors,
        "errors": errors,
        "contract_version": manifest.get("contract_version"),
        "checkpoint_id": manifest.get("checkpoint_id"),
        "file_count": len(manifest.get("files", [])),
        "total_bytes": sum(r.get("bytes", 0) for r in manifest.get("files", [])),
        "tested_local_only": manifest.get("tested_local_only"),
        "machine_loss_durable": manifest.get("machine_loss_durable"),
        "postgresql_reconstruction_evidence_present": bool(pg),
    }


def restore_checkpoint(checkpoint: Path, restore_root: Path) -> dict[str, Any]:
    validation = validate_checkpoint(checkpoint)
    if not validation["valid"]:
        raise CheckpointError("cannot restore invalid checkpoint")
    manifest = load_json(checkpoint / "manifest.json")
    restore_root.mkdir(parents=True, exist_ok=True)
    restored: list[dict[str, Any]] = []
    for rec in manifest.get("files", []):
        src = checkpoint / "files" / rec["path"]
        dst = restore_root / rec["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        actual = sha256_file(dst)
        if actual != rec["sha256"]:
            raise CheckpointError(f"restore hash mismatch: {rec['path']}")
        restored.append({"path": rec["path"], "bytes": rec["bytes"], "sha256": actual})
    report = {
        "valid": True,
        "checkpoint_id": manifest.get("checkpoint_id"),
        "restore_root": str(restore_root),
        "restored_file_count": len(restored),
        "restored_bytes": sum(r["bytes"] for r in restored),
        "restored": restored,
        "tested_local_only": True,
        "machine_loss_durable": False,
    }
    write_json(restore_root / "restore_validation.json", report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_create = sub.add_parser("create")
    p_create.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p_create.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    p_create.add_argument("--checkpoint-id")
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--checkpoint", type=Path, required=True)
    p_restore = sub.add_parser("restore")
    p_restore.add_argument("--checkpoint", type=Path, required=True)
    p_restore.add_argument("--restore-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "create":
            result = create_checkpoint(args.config, args.destination, args.checkpoint_id)
        elif args.command == "validate":
            result = validate_checkpoint(args.checkpoint)
        elif args.command == "restore":
            result = restore_checkpoint(args.checkpoint, args.restore_root)
        else:  # pragma: no cover
            raise CheckpointError(f"unknown command: {args.command}")
        print(canonical_json(result), end="")
        return 0 if result.get("valid", True) else 1
    except CheckpointError as exc:
        print(canonical_json({"valid": False, "error": str(exc)}), end="", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
