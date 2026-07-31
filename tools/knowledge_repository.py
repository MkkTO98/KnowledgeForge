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
import os
import re
import tempfile
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
    payload = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(payload)
        os.replace(temporary_path, path)
    finally:
        if descriptor != -1:
            os.close(descriptor)
        temporary_path.unlink(missing_ok=True)


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


def _validate_package_id(package_id: Any) -> str:
    """Require one portable filename stem, never a path or special component."""
    if not isinstance(package_id, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", package_id) is None:
        raise ValueError("package_id must be a single safe filename stem")
    if "/" in package_id or "\\" in package_id or package_id in {".", ".."}:
        raise ValueError("package_id must be a single safe filename stem")
    return package_id


def _object_path(package_id: str) -> str:
    _validate_package_id(package_id)
    return f"objects/{package_id}.json"


def _contained_path(root: Path, directory: str, package_id: str) -> Path:
    _validate_package_id(package_id)
    resolved_root = root.resolve(strict=False)
    intended = (resolved_root / directory).resolve(strict=False)
    try:
        intended.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"repository {directory} directory escapes repository root") from exc
    candidate = (intended / f"{package_id}.json").resolve(strict=False)
    try:
        candidate.relative_to(intended)
    except ValueError as exc:
        raise ValueError(f"package_id escapes repository {directory} directory") from exc
    return candidate


INDEX_NAMES = (
    "by_package_id",
    "by_knowledge_identity",
    "by_evidence_family",
    "by_statement_type",
    "by_lifecycle_state",
    "by_package_manifest_fingerprint",
)


def _validate_repository_output(root: Path, relative_path: str, *, directory: bool = False) -> Path:
    """Resolve one canonical output without following a repository-internal symlink."""
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"repository output escapes repository root: {relative_path}")
    resolved_root = root.resolve(strict=False)
    lexical = root / relative
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"repository output {relative_path} symlink escapes repository containment")
    resolved = lexical.resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"repository output {relative_path} escapes repository root") from exc
    if lexical.exists() and directory and not lexical.is_dir():
        raise ValueError(f"repository output directory is not a directory: {relative_path}")
    if lexical.exists() and not directory and not lexical.is_file():
        raise ValueError(f"repository output file is not a regular file: {relative_path}")
    if lexical.exists() and not directory and lexical.stat().st_nlink > 1:
        raise ValueError(f"repository output file is hard-linked (multiple links): {relative_path}")
    return lexical


def _validate_repository_structure(root: Path) -> None:
    for directory in ("objects", "indexes", "evolution"):
        _validate_repository_output(root, directory, directory=True)
    for name in INDEX_NAMES:
        _validate_repository_output(root, f"indexes/{name}.json")
    _validate_repository_output(root, "manifest.json")


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
        package_id_from_name = _validate_package_id(path.stem)
        _validate_repository_output(repository_root, f"objects/{package_id_from_name}.json")
        expected_path = _contained_path(repository_root, "objects", package_id_from_name)
        if path.resolve(strict=True) != expected_path:
            raise ValueError("repository object path escapes objects directory")
        value = read_json(path)
        if not isinstance(value, dict):
            raise ValueError("repository object must be a JSON object")
        package_id = _validate_package_id(value.get("package_id"))
        if package_id != package_id_from_name:
            raise ValueError("repository object filename and package_id mismatch")
        _require_validated_knowledge_object(value)
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


def _build_manifest(
    root: Path,
    packages: list[dict[str, Any]],
    indexes: dict[str, Any],
    *,
    repository_root: str | None = None,
) -> dict[str, Any]:
    fingerprint = _repository_fingerprint(packages, indexes)
    return {
        "repository_kind": REPOSITORY_KIND,
        "schema_version": SCHEMA_VERSION,
        "repository_root": _portable_repository_root(root) if repository_root is None else repository_root,
        "object_count": len(packages),
        "package_ids": sorted(package["package_id"] for package in packages),
        "index_files": [f"indexes/{name}.json" for name in sorted(indexes)],
        "object_directory": "objects/",
        "evolution_directory": "evolution/",
        "repository_fingerprint": fingerprint,
        "persistence_policy": "persist validated KnowledgeObjectPackage JSON exactly; repository metadata and indexes remain separate",
    }


def _validate_directory_population(root: Path, directory: str, expected_json_names: set[str]) -> None:
    """Require exactly the canonical JSON files, plus an optional governed summary."""
    entries = {path.name for path in (root / directory).iterdir()}
    allowed = expected_json_names | {"_SUMMARY.md"}
    if not expected_json_names.issubset(entries) or not entries.issubset(allowed):
        population_name = {"objects": "object", "evolution": "evolution", "indexes": "index"}[directory]
        raise ValueError(f"repository {population_name} population mismatch")
    if "_SUMMARY.md" in entries:
        _validate_repository_output(root, f"{directory}/_SUMMARY.md")


def _validated_manifest_repository_root(root: Path, manifest: dict[str, Any]) -> str:
    """Validate a stored root locator without rebasing a portable relative value."""
    value = manifest.get("repository_root")
    if not isinstance(value, str) or not value:
        raise ValueError("repository manifest repository_root is not a non-empty string")
    stored = Path(value)
    if stored.is_absolute():
        if stored.resolve(strict=False) != root.resolve(strict=True):
            raise ValueError("repository manifest absolute repository_root mismatch")
        return value
    if value != stored.as_posix() or value == "." or any(part in {"", ".", ".."} for part in stored.parts):
        raise ValueError("repository manifest repository_root is not a normalized portable path")
    return value


def authenticate_repository(repository_root: Path | str) -> dict[str, Any]:
    """Read-only authentication of every canonical v1 repository component."""
    root = Path(repository_root)
    try:
        if root.is_symlink():
            raise ValueError("repository root must not be a symlink")
        _validate_repository_structure(root)
        if not root.is_dir():
            raise ValueError("repository root is missing or not a directory")
        packages = _load_existing_packages(root)
        package_ids = [package["package_id"] for package in packages]
        expected_object_names = {f"{package_id}.json" for package_id in package_ids}
        expected_index_names = {f"{name}.json" for name in INDEX_NAMES}
        _validate_directory_population(root, "objects", expected_object_names)
        _validate_directory_population(root, "evolution", expected_object_names)
        _validate_directory_population(root, "indexes", expected_index_names)
        indexes = _build_indexes(packages)
        for package in packages:
            package_id = package["package_id"]
            evolution_path = _validate_repository_output(root, f"evolution/{package_id}.json")
            if read_json(evolution_path) != _evolution_record(package):
                raise ValueError(f"repository evolution record mismatch: {package_id}")
        for name, expected in indexes.items():
            if read_json(_validate_repository_output(root, f"indexes/{name}.json")) != expected:
                raise ValueError(f"repository index mismatch: {name}")
        manifest = read_json(_validate_repository_output(root, "manifest.json"))
        if not isinstance(manifest, dict):
            raise ValueError("repository manifest must be a JSON object")
        stored_repository_root = _validated_manifest_repository_root(root, manifest)
        expected_manifest = _build_manifest(
            root,
            packages,
            indexes,
            repository_root=stored_repository_root,
        )
        if manifest != expected_manifest:
            raise ValueError("repository manifest mismatch")
        return {
            "object_count": len(packages),
            "repository_fingerprint": expected_manifest["repository_fingerprint"],
        }
    except (OSError, json.JSONDecodeError, TypeError, KeyError, ValueError) as exc:
        raise ValueError(f"repository authentication failed: {exc}") from exc


def persist_knowledge_object_packages(packages: list[dict[str, Any]], repository_root: Path | str = DEFAULT_REPOSITORY_ROOT) -> dict[str, Any]:
    """Persist validated packages only after a complete canonical-output preflight."""
    root = Path(repository_root)
    if root.is_symlink():
        raise ValueError("repository root must not be a symlink")
    _validate_repository_structure(root)
    for package in packages:
        if not isinstance(package, dict):
            raise ValueError("package must be a JSON object with a safe package_id")
        _validate_package_id(package.get("package_id"))
        _require_validated_knowledge_object(package)

    existing_packages = _load_existing_packages(root) if root.exists() else []
    existing_by_id = {package["package_id"]: package for package in existing_packages}
    incoming_by_id: dict[str, dict[str, Any]] = {}
    for package in packages:
        package_id = package["package_id"]
        existing = existing_by_id.get(package_id)
        if existing is not None and sha256_fingerprint(existing) != sha256_fingerprint(package):
            raise ValueError(
                f"{package_id} already exists with different bytes; canonical package overwrite is forbidden. "
                "Publish a distinct successor package and append evolution/current-state records instead."
            )
        incoming_by_id[package_id] = package

    all_by_id = dict(existing_by_id)
    all_by_id.update(incoming_by_id)
    all_packages = [all_by_id[key] for key in sorted(all_by_id)]
    indexes = _build_indexes(all_packages)
    manifest = _build_manifest(root, all_packages, indexes)

    # Validate every dynamic output as well as the static metadata outputs before
    # creating directories or writing one byte.
    for package_id in all_by_id:
        _validate_repository_output(root, f"objects/{package_id}.json")
        _validate_repository_output(root, f"evolution/{package_id}.json")

    root.mkdir(parents=True, exist_ok=True)
    for directory in ("objects", "indexes", "evolution"):
        (root / directory).mkdir(exist_ok=True)
    for package_id, package in incoming_by_id.items():
        write_json(root / "objects" / f"{package_id}.json", package)
        write_json(root / "evolution" / f"{package_id}.json", _evolution_record(package))
    for name, index in indexes.items():
        write_json(root / "indexes" / f"{name}.json", index)
    write_json(root / "manifest.json", manifest)

    return {
        "repository_root": str(root),
        "persisted_count": len(incoming_by_id),
        "rejected_count": 0,
        "total_object_count": len(all_packages),
        "repository_fingerprint": manifest["repository_fingerprint"],
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
