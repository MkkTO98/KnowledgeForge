#!/usr/bin/env python3
"""Deterministic KnowledgeForge Knowledge Repository persistence.

This module persists existing validated KnowledgeObjectPackage dictionaries exactly as
produced by the validated production methodology. It adds file-backed repository
layout, indexes, manifest, and evolution records around the existing package model;
it does not redefine package contracts, validators, taxonomy, APIs, services, or
source-project interfaces.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
REPOSITORY_KIND = "KnowledgeForgeKnowledgeRepository"
DEFAULT_REPOSITORY_ROOT = Path("knowledge_repository")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _require_validated_knowledge_object(package: dict[str, Any]) -> None:
    package_id = package.get("package_id", "<missing-package-id>")
    if package.get("package_kind") != "KnowledgeObjectPackage":
        raise ValueError(f"{package_id} is not a KnowledgeObjectPackage")
    validation = package.get("validation_state")
    if not isinstance(validation, dict):
        raise ValueError(f"{package_id} is missing validation_state")
    blockers = validation.get("blockers") or []
    if validation.get("validation_result") != "pass" or blockers:
        raise ValueError(f"{package_id} has validation blockers or did not pass validation")
    if not package.get("provenance_envelope"):
        raise ValueError(f"{package_id} is missing provenance_envelope")
    if not package.get("fingerprints"):
        raise ValueError(f"{package_id} is missing fingerprints")
    quality = package.get("confidence_quality")
    if not isinstance(quality, dict):
        raise ValueError(f"{package_id} is missing confidence_quality")
    if not quality.get("lifecycle_state"):
        raise ValueError(f"{package_id} is missing lifecycle_state")
    if not quality.get("reproducibility_state"):
        raise ValueError(f"{package_id} is missing reproducibility_state")
    statements = package.get("generated_statements")
    if not isinstance(statements, list) or not statements:
        raise ValueError(f"{package_id} is missing generated_statements")
    for statement in statements:
        if not isinstance(statement, dict) or not statement.get("statement_id"):
            raise ValueError(f"{package_id} contains a statement without statement_id")


def _object_path(package_id: str) -> str:
    return f"objects/{package_id}.json"


def _sorted_unique(values: list[str]) -> list[str]:
    return sorted(set(values))


def _build_indexes(packages: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_package_id: dict[str, str] = {}
    by_knowledge_identity: dict[str, list[str]] = {}
    by_evidence_family: dict[str, list[str]] = {}
    by_statement_type: dict[str, list[str]] = {}
    by_lifecycle_state: dict[str, list[str]] = {}
    by_package_manifest_fingerprint: dict[str, list[str]] = {}

    for package in sorted(packages, key=lambda p: p["package_id"]):
        package_id = package["package_id"]
        by_package_id[package_id] = _object_path(package_id)
        evidence_family = package.get("scope", {}).get("evidence_family", "unspecified")
        by_evidence_family.setdefault(evidence_family, []).append(package_id)
        lifecycle = package.get("confidence_quality", {}).get("lifecycle_state", "unspecified")
        by_lifecycle_state.setdefault(lifecycle, []).append(package_id)
        manifest_fingerprint = package.get("fingerprints", {}).get("package_manifest", "missing")
        by_package_manifest_fingerprint.setdefault(manifest_fingerprint, []).append(package_id)
        for statement in package.get("generated_statements", []):
            statement_id = statement["statement_id"]
            by_knowledge_identity.setdefault(statement_id, []).append(package_id)
            statement_type = statement.get("statement_type", "unspecified")
            by_statement_type.setdefault(statement_type, []).append(package_id)

    def sorted_index(index: dict[str, list[str]]) -> dict[str, list[str]]:
        return {key: _sorted_unique(values) for key, values in sorted(index.items())}

    return {
        "by_package_id": dict(sorted(by_package_id.items())),
        "by_knowledge_identity": sorted_index(by_knowledge_identity),
        "by_evidence_family": sorted_index(by_evidence_family),
        "by_statement_type": sorted_index(by_statement_type),
        "by_lifecycle_state": sorted_index(by_lifecycle_state),
        "by_package_manifest_fingerprint": sorted_index(by_package_manifest_fingerprint),
    }


def _evolution_record(package: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": package["package_id"],
        "package_version": package.get("package_version"),
        "status": package.get("status"),
        "lineage": package.get("lineage"),
        "evolution_metadata": package.get("evolution_metadata"),
        "provenance_envelope": package.get("provenance_envelope"),
        "fingerprints": package.get("fingerprints"),
        "validation_state": package.get("validation_state"),
        "lifecycle_state": package.get("confidence_quality", {}).get("lifecycle_state"),
        "reproducibility_state": package.get("confidence_quality", {}).get("reproducibility_state"),
    }


def _load_existing_packages(repository_root: Path) -> list[dict[str, Any]]:
    objects_dir = repository_root / "objects"
    if not objects_dir.exists():
        return []
    packages = []
    for path in sorted(objects_dir.glob("*.json")):
        value = read_json(path)
        if isinstance(value, dict):
            packages.append(value)
    return packages


def _repository_fingerprint(packages: list[dict[str, Any]], indexes: dict[str, Any]) -> str:
    manifest_basis = {
        "repository_kind": REPOSITORY_KIND,
        "schema_version": SCHEMA_VERSION,
        "package_ids": sorted(package["package_id"] for package in packages),
        "object_package_fingerprints": {
            package["package_id"]: sha256_fingerprint(package)
            for package in sorted(packages, key=lambda p: p["package_id"])
        },
        "indexes": indexes,
    }
    return sha256_fingerprint(manifest_basis)


def _portable_repository_root(root: Path) -> str:
    try:
        return str(root.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(root)


def persist_knowledge_object_packages(packages: list[dict[str, Any]], repository_root: Path | str = DEFAULT_REPOSITORY_ROOT) -> dict[str, Any]:
    """Persist validated KnowledgeObjectPackages into a file-backed repository.

    Existing packages are read and included in indexes so repeated calls are
    deterministic and idempotent. Incoming packages overwrite the same package_id
    only when their content is explicitly supplied again.
    """
    root = Path(repository_root)
    root.mkdir(parents=True, exist_ok=True)
    (root / "objects").mkdir(exist_ok=True)
    (root / "indexes").mkdir(exist_ok=True)
    (root / "evolution").mkdir(exist_ok=True)

    existing_by_id = {package["package_id"]: package for package in _load_existing_packages(root)}
    incoming_by_id: dict[str, dict[str, Any]] = {}
    for package in packages:
        _require_validated_knowledge_object(package)
        package_id = package["package_id"]
        existing = existing_by_id.get(package_id)
        if existing is not None and sha256_fingerprint(existing) != sha256_fingerprint(package):
            raise ValueError(
                f"{package_id} already exists with different bytes; canonical package overwrite is forbidden. "
                "Publish a distinct successor package and append evolution/current-state records instead."
            )
        incoming_by_id[package_id] = package
        write_json(root / _object_path(package_id), package)
        write_json(root / "evolution" / f"{package_id}.json", _evolution_record(package))

    all_by_id = dict(existing_by_id)
    all_by_id.update(incoming_by_id)
    all_packages = [all_by_id[key] for key in sorted(all_by_id)]

    indexes = _build_indexes(all_packages)
    for name, index in indexes.items():
        write_json(root / "indexes" / f"{name}.json", index)

    fingerprint = _repository_fingerprint(all_packages, indexes)
    manifest = {
        "repository_kind": REPOSITORY_KIND,
        "schema_version": SCHEMA_VERSION,
        "repository_root": _portable_repository_root(root),
        "object_count": len(all_packages),
        "package_ids": sorted(package["package_id"] for package in all_packages),
        "index_files": [f"indexes/{name}.json" for name in sorted(indexes)],
        "object_directory": "objects/",
        "evolution_directory": "evolution/",
        "repository_fingerprint": fingerprint,
        "persistence_policy": "persist validated KnowledgeObjectPackage JSON exactly; repository metadata and indexes remain separate",
    }
    write_json(root / "manifest.json", manifest)

    return {
        "repository_root": str(root),
        "persisted_count": len(incoming_by_id),
        "rejected_count": 0,
        "total_object_count": len(all_packages),
        "repository_fingerprint": fingerprint,
        "manifest_path": str(root / "manifest.json"),
    }


def load_packages_from_file(path: Path) -> list[dict[str, Any]]:
    value = read_json(path)
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    raise ValueError(f"unsupported package file shape: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Persist validated KnowledgeObjectPackages into the KnowledgeForge Knowledge Repository.")
    parser.add_argument("package_file", type=Path, help="JSON file containing one KnowledgeObjectPackage or a list of packages")
    parser.add_argument("--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT)
    args = parser.parse_args()
    result = persist_knowledge_object_packages(load_packages_from_file(args.package_file), args.repository_root)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
