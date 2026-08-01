#!/usr/bin/env python3
"""Deterministic publication-authority reconciliation and staging readiness.

This module deliberately does not stage files.  It proves the exact authority
population and returns the mechanically derived parent delta that a separate
strict publication-only operation may stage.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

_AUDIT_SPEC = importlib.util.spec_from_file_location(
    "_publication_authority_architecture_audit",
    Path(__file__).with_name("architecture_reality_audit.py"),
)
_audit = importlib.util.module_from_spec(_AUDIT_SPEC)
assert _AUDIT_SPEC.loader is not None
_AUDIT_SPEC.loader.exec_module(_audit)
canonical_json = _audit.canonical_json
value_fingerprint = _audit.value_fingerprint

AUTHORITY_SCHEMA = "knowledgeforge.publication_authority.v1"
AUTHORITY_VERSION = "1.0"
GATE_SCHEMA = "knowledgeforge.publication_authority.staging_gate.v1"
GATE_VERSION = "1.0"
MIXED_SNAPSHOT_SCHEMA = "knowledgeforge.publication_authority.mixed_live_snapshot.v1"
MIXED_SNAPSHOT_VERSION = "1.0"
REGISTRY_SCHEMA = "knowledgeforge.publication_authority.registry.v1"
REGISTRY_VERSION = "1.0"

REGISTRY_KEYS = {
    "schema_name",
    "schema_version",
    "generation",
    "predecessor_registry_fingerprint",
    "active_authority_fingerprint",
    "superseded_authority_fingerprints",
    "registry_fingerprint",
}
AUTHORITY_KEYS = {
    "schema_name",
    "schema_version",
    "status",
    "parent_head",
    "parent_tree_oid",
    "registry_path",
    "audit_subject_manifest_fingerprint",
    "source_manifests",
    "authority_only_entries",
    "authority_only_path_count",
    "durable_record_path",
    "parent_population_fingerprint",
    "path_count",
    "changed_path_count",
    "parent_identical_path_count",
    "paths",
    "changed_paths",
    "parent_identical_paths",
    "supersedes",
    "authority_fingerprint",
}
COMPLETE_SCHEMA = "knowledgeforge.evidence_portfolio.complete_file_candidate.v1"
MIXED_SCHEMA = "knowledgeforge.evidence_portfolio.mixed_representation_candidate.v1"
LEGACY_SCHEMA = "knowledgeforge.prospective_publication_manifest.v3"
HEX_40 = re.compile(r"[0-9a-f]{40}")
SHA256 = re.compile(r"sha256:[0-9a-f]{64}")
RAW_SHA256 = re.compile(r"[0-9a-f]{64}")
SUPPORTED_MODES = {"100644", "100755"}


class PublicationAuthorityError(ValueError):
    """A publication authority or staging prerequisite failed closed."""


def _fail(message: str) -> None:
    raise PublicationAuthorityError(message)


def _strict_dict(value: Any, message: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(message)
    return value


def _valid_sha256(value: Any, *, prefixed: bool) -> str:
    pattern = SHA256 if prefixed else RAW_SHA256
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        _fail("malformed SHA-256 identity")
    return value


def _valid_mode(value: Any) -> str:
    if value not in SUPPORTED_MODES:
        _fail(f"unsupported publication representation mode: {value!r}")
    return value


def _valid_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        _fail(f"malformed publication path: {value!r}")
    candidate = PurePosixPath(value)
    if (
        candidate.is_absolute()
        or value.startswith("/")
        or value.endswith("/")
        or "//" in value
        or any(part in {"", ".", ".."} for part in candidate.parts)
        or str(candidate) != value
        or candidate.parts[0] == ".git"
    ):
        _fail(f"publication path is not a safe canonical repository-relative path: {value!r}")
    return value


def _valid_reason(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("authority-only declaration requires a non-empty reason")
    return value


def _manifest_fingerprint(value: dict[str, Any], field: str) -> str:
    return value_fingerprint({key: item for key, item in value.items() if key != field})


def authority_fingerprint(authority: dict[str, Any]) -> str:
    return _manifest_fingerprint(authority, "authority_fingerprint")


def gate_fingerprint(gate: dict[str, Any]) -> str:
    return _manifest_fingerprint(gate, "gate_fingerprint")


def _source_manifest(
    manifest: Any, representation_kind: str
) -> tuple[list[dict[str, str]], str, str]:
    manifest = _strict_dict(manifest, f"{representation_kind} source manifest must be an object")
    expected_schema = COMPLETE_SCHEMA if representation_kind == "complete" else MIXED_SCHEMA
    if manifest.get("schema_name") != expected_schema or manifest.get("schema_version") != "1.0":
        _fail(f"{representation_kind} source manifest schema mismatch")
    if manifest.get("manifest_fingerprint") != _manifest_fingerprint(
        manifest, "manifest_fingerprint"
    ):
        _fail(f"{representation_kind} source manifest fingerprint mismatch")
    parent_head = manifest.get("parent_head")
    if not isinstance(parent_head, str) or HEX_40.fullmatch(parent_head) is None:
        _fail(f"{representation_kind} source manifest parent HEAD is malformed")
    rows = manifest.get("paths")
    if not isinstance(rows, list) or isinstance(manifest.get("path_count"), bool) or manifest.get(
        "path_count"
    ) != len(rows):
        _fail(f"{representation_kind} source manifest path count mismatch")
    declarations: list[dict[str, str]] = []
    prior_path = None
    for raw in rows:
        row = _strict_dict(raw, f"{representation_kind} source row must be an object")
        if set(row) != {"path", "mode", "sha256", "size"}:
            _fail(f"{representation_kind} source row schema is not exact")
        path = _valid_path(row.get("path"))
        mode = _valid_mode(row.get("mode"))
        digest = _valid_sha256(row.get("sha256"), prefixed=False)
        size = row.get("size")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            _fail(f"{representation_kind} source size is malformed: {path}")
        if prior_path is not None and path <= prior_path:
            _fail(f"{representation_kind} source paths must be canonical sorted unique")
        prior_path = path
        declarations.append(
            {
                "path": path,
                "mode": mode,
                "blob_sha256": "sha256:" + digest,
                "representation_kind": representation_kind,
            }
        )
    return declarations, parent_head, manifest["manifest_fingerprint"]


def _authority_only(
    entries: Any,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if not isinstance(entries, list):
        _fail("authority-only entries must be a list")
    by_declaration: dict[tuple[str, str, str, str], dict[str, str]] = {}
    by_path: dict[str, tuple[str, str, str, str]] = {}
    for raw in entries:
        row = _strict_dict(raw, "authority-only entry must be an object")
        if set(row) != {"path", "mode", "blob_sha256", "reason"}:
            _fail("authority-only entry schema is not exact")
        normalized = {
            "path": _valid_path(row.get("path")),
            "mode": _valid_mode(row.get("mode")),
            "blob_sha256": _valid_sha256(row.get("blob_sha256"), prefixed=True),
            "reason": _valid_reason(row.get("reason")),
        }
        identity = (
            normalized["path"],
            normalized["mode"],
            normalized["blob_sha256"],
            normalized["reason"],
        )
        previous = by_path.get(normalized["path"])
        if previous is not None and previous != identity:
            _fail(f"conflicting duplicate authority-only declaration: {normalized['path']}")
        by_path[normalized["path"]] = identity
        by_declaration[identity] = normalized
    retained = sorted(by_declaration.values(), key=lambda row: row["path"])
    declarations = [
        {
            "path": row["path"],
            "mode": row["mode"],
            "blob_sha256": row["blob_sha256"],
            "representation_kind": "authority_only",
        }
        for row in retained
    ]
    return declarations, retained


def _assemble_sources(
    complete_manifest: Any, mixed_manifest: Any, authority_only_entries: Any
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    complete, complete_parent, complete_fp = _source_manifest(complete_manifest, "complete")
    mixed, mixed_parent, mixed_fp = _source_manifest(mixed_manifest, "mixed")
    if complete_parent != mixed_parent:
        _fail("complete and mixed source manifests bind different parent HEADs")
    authority_only, retained_extra = _authority_only(authority_only_entries)
    population: dict[str, dict[str, str]] = {}
    for declaration in complete + mixed + authority_only:
        path = declaration["path"]
        previous = population.get(path)
        if previous is not None:
            if previous == declaration:
                continue
            _fail(f"conflicting duplicate representation declaration: {path}")
        population[path] = declaration
    declarations = [population[path] for path in sorted(population)]
    metadata = {
        "parent_head": complete_parent,
        "complete_manifest_fingerprint": complete_fp,
        "mixed_manifest_fingerprint": mixed_fp,
        "complete_path_count": len(complete),
        "mixed_path_count": len(mixed),
        "authority_only_path_count": len(authority_only),
        "authority_only_entries": retained_extra,
    }
    return declarations, metadata


def _reject_symlink_components(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        try:
            if stat.S_ISLNK(current.lstat().st_mode):
                _fail(f"{label} contains a symlink component: {current}")
        except OSError as exc:
            raise PublicationAuthorityError(f"{label} is missing or inaccessible: {current}") from exc
    return absolute


def _git_environment() -> dict[str, str]:
    environment = dict(os.environ)
    for name in (
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_REPLACE_REF_BASE",
    ):
        environment.pop(name, None)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _repository_root(repository_root: Path) -> Path:
    if not isinstance(repository_root, Path):
        _fail("authenticated Git repository root is required")
    try:
        lexical = _reject_symlink_components(repository_root, "authenticated Git repository root")
        resolved = lexical.resolve(strict=True)
        top = subprocess.run(
            ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
            check=True,
            text=True,
            capture_output=True,
            env=_git_environment(),
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PublicationAuthorityError("authenticated Git repository root is invalid") from exc
    if Path(top).resolve() != resolved:
        _fail("authenticated Git repository root must be the exact worktree root")
    return resolved


def _git_parent_entries(
    repository_root: Path, parent_head: str, authority_paths: set[str]
) -> tuple[list[dict[str, str]], str]:
    root = _repository_root(repository_root)
    try:
        current_head = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
            env=_git_environment(),
        ).stdout.strip()
        if current_head != parent_head:
            _fail("source parent HEAD is not the authenticated repository's current publication parent")
        commit_type = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-t", parent_head],
            check=True,
            text=True,
            capture_output=True,
            env=_git_environment(),
        ).stdout.strip()
        if commit_type != "commit":
            _fail("source parent HEAD does not identify a Git commit")
        tree_oid = subprocess.run(
            ["git", "-C", str(root), "rev-parse", f"{parent_head}^{{tree}}"],
            check=True,
            text=True,
            capture_output=True,
            env=_git_environment(),
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise PublicationAuthorityError("source parent HEAD is unavailable in authenticated Git repository") from exc
    entries: list[dict[str, str]] = []
    for relative in sorted(authority_paths):
        try:
            raw = subprocess.run(
                ["git", "-C", str(root), "ls-tree", "-z", parent_head, "--", relative],
                check=True,
                capture_output=True,
                env=_git_environment(),
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise PublicationAuthorityError(f"cannot inspect authenticated parent path: {relative}") from exc
        if not raw:
            continue
        records = [record for record in raw.split(b"\0") if record]
        if len(records) != 1:
            _fail(f"authenticated parent path is ambiguous: {relative}")
        try:
            metadata, encoded_path = records[0].split(b"\t", 1)
            mode, object_type, oid = metadata.decode("ascii").split(" ")
            listed_path = encoded_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise PublicationAuthorityError(f"malformed authenticated parent tree entry: {relative}") from exc
        if listed_path != relative or object_type != "blob" or mode not in SUPPORTED_MODES:
            _fail(f"unsupported authenticated parent representation: {relative}")
        try:
            data = subprocess.run(
                ["git", "-C", str(root), "cat-file", "blob", oid],
                check=True,
                capture_output=True,
                env=_git_environment(),
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise PublicationAuthorityError(f"cannot read authenticated parent blob: {relative}") from exc
        entries.append(
            {
                "path": relative,
                "mode": mode,
                "blob_sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
            }
        )
    if not re.fullmatch(r"[0-9a-f]{40,64}", tree_oid):
        _fail("authenticated parent tree identity is malformed")
    return entries, tree_oid


def _parent_population(
    entries: Any, authority_paths: set[str]
) -> tuple[dict[str, dict[str, str]], list[dict[str, str]], str]:
    if not isinstance(entries, list):
        _fail("parent entries must be a list")
    parent: dict[str, dict[str, str]] = {}
    prior_path = None
    for raw in entries:
        row = _strict_dict(raw, "parent entry must be an object")
        if set(row) != {"path", "mode", "blob_sha256"}:
            _fail("parent entry schema is not exact")
        normalized = {
            "path": _valid_path(row.get("path")),
            "mode": _valid_mode(row.get("mode")),
            "blob_sha256": _valid_sha256(row.get("blob_sha256"), prefixed=True),
        }
        if prior_path is not None and normalized["path"] <= prior_path:
            _fail("parent entries must be canonical sorted unique")
        prior_path = normalized["path"]
        if normalized["path"] not in authority_paths:
            _fail(f"unexpected parent entry outside authority population: {normalized['path']}")
        parent[normalized["path"]] = normalized
    retained = [parent[path] for path in sorted(parent)]
    return parent, retained, value_fingerprint(retained)


def _classify(
    declarations: list[dict[str, str]], parent_entries: Any
) -> tuple[list[dict[str, str]], list[str], list[str], str]:
    parent, retained_parent, parent_fp = _parent_population(
        parent_entries, {row["path"] for row in declarations}
    )
    rows: list[dict[str, str]] = []
    changed: list[str] = []
    identical: list[str] = []
    for declaration in declarations:
        prior = parent.get(declaration["path"])
        if prior is None:
            change_kind = "added"
        elif (
            prior["mode"] == declaration["mode"]
            and prior["blob_sha256"] == declaration["blob_sha256"]
        ):
            change_kind = "parent_identical"
        elif prior["blob_sha256"] == declaration["blob_sha256"]:
            change_kind = "mode_only"
        elif prior["mode"] == declaration["mode"]:
            change_kind = "content"
        else:
            change_kind = "content_and_mode"
        row = dict(declaration)
        row["change_kind"] = change_kind
        rows.append(row)
        (identical if change_kind == "parent_identical" else changed).append(
            declaration["path"]
        )
    return rows, changed, identical, parent_fp


def _legacy_rows(authority: Any) -> tuple[list[dict[str, str]], str]:
    authority = _strict_dict(authority, "legacy publication authority must be an object")
    if authority.get("schema_name") != LEGACY_SCHEMA or authority.get("schema_version") != "1.0":
        _fail("legacy publication authority schema mismatch")
    if authority.get("final_manifest_fingerprint") != _manifest_fingerprint(
        authority, "final_manifest_fingerprint"
    ):
        _fail("legacy publication authority fingerprint mismatch")
    rows = authority.get("paths")
    if not isinstance(rows, list) or isinstance(authority.get("path_count"), bool) or authority.get(
        "path_count"
    ) != len(rows):
        _fail("legacy publication authority path count mismatch")
    normalized: list[dict[str, str]] = []
    prior_path = None
    for raw in rows:
        row = _strict_dict(raw, "legacy publication authority row must be an object")
        if set(row) != {"path", "mode", "blob_sha256"}:
            _fail("legacy publication authority row schema is not exact")
        item = {
            "path": _valid_path(row.get("path")),
            "mode": _valid_mode(row.get("mode")),
            "blob_sha256": _valid_sha256(row.get("blob_sha256"), prefixed=True),
        }
        if prior_path is not None and item["path"] <= prior_path:
            _fail("legacy publication authority paths must be canonical sorted unique")
        prior_path = item["path"]
        normalized.append(item)
    return normalized, authority["final_manifest_fingerprint"]


def validate_legacy_publication_authority(
    authority: Any,
    complete_manifest: Any,
    mixed_manifest: Any,
    authority_only_entries: Any,
    parent_entries: Any,
    *,
    audit_subject_paths: set[str] | None = None,
    superseded_authority_fingerprints: list[str] | None = None,
) -> dict[str, Any]:
    """Reconcile an authenticated v3 flat manifest against declared sources.

    ``audit_subject_paths`` is accepted only to make the conceptual boundary
    explicit; it never contributes publication authority.
    """
    del audit_subject_paths
    declarations, metadata = _assemble_sources(
        complete_manifest, mixed_manifest, authority_only_entries
    )
    rows, fingerprint = _legacy_rows(authority)
    superseded = set(superseded_authority_fingerprints or [])
    if fingerprint in superseded:
        _fail("legacy publication authority is stale or superseded")
    expected = [
        {key: row[key] for key in ("path", "mode", "blob_sha256")}
        for row in declarations
    ]
    if rows != expected:
        actual_paths = {row["path"] for row in rows}
        expected_paths = {row["path"] for row in expected}
        missing = sorted(expected_paths - actual_paths)
        extra = sorted(actual_paths - expected_paths)
        _fail(
            "legacy publication authority is not the exact source union; "
            f"missing={missing}, extra={extra}"
        )
    classified, changed, identical, parent_fp = _classify(
        declarations, parent_entries
    )
    return {
        "valid": True,
        "authority_fingerprint": fingerprint,
        "authority_path_count": len(classified),
        "complete_path_count": metadata["complete_path_count"],
        "mixed_path_count": metadata["mixed_path_count"],
        "authority_only_path_count": metadata["authority_only_path_count"],
        "changed_path_count": len(changed),
        "parent_identical_path_count": len(identical),
        "changed_paths": changed,
        "parent_identical_paths": identical,
        "parent_population_fingerprint": parent_fp,
    }


def _registry_locator(registry_path: Path) -> str:
    if not isinstance(registry_path, Path) or not registry_path.is_absolute():
        _fail("canonical authority registry path must be absolute")
    if registry_path.name != "publication_authority_registry.json":
        _fail("canonical authority registry must use the fixed publication_authority_registry.json name")
    lexical = Path(os.path.abspath(os.fspath(registry_path)))
    if lexical != registry_path:
        _fail("canonical authority registry path must be normalized")
    _reject_symlink_components(registry_path.parent, "authority registry parent")
    if registry_path.exists() or registry_path.is_symlink():
        _reject_symlink_components(registry_path, "authority registry")
        if not registry_path.is_file():
            _fail("canonical authority registry must be a regular file")
    return str(registry_path)


def build_publication_authority(
    complete_manifest: Any,
    mixed_manifest: Any,
    authority_only_entries: Any,
    *,
    repository_root: Path,
    registry_path: Path,
    audit_subject_manifest_fingerprint: str,
    durable_record_path: str,
    supersedes: list[str] | None = None,
) -> dict[str, Any]:
    declarations, metadata = _assemble_sources(
        complete_manifest, mixed_manifest, authority_only_entries
    )
    audit_fp = _valid_sha256(audit_subject_manifest_fingerprint, prefixed=True)
    registry_locator = _registry_locator(registry_path)
    durable_path = _valid_path(durable_record_path)
    durable_patterns = (
        r"^artifacts/tasks/T-[^/]+\.md$",
        r"^artifacts/reports/R-[^/]+\.md$",
        r"^artifacts/decisions/D-[^/]+\.md$",
        r"^context/latest_handoff\.md$",
    )
    if not any(re.fullmatch(pattern, durable_path) for pattern in durable_patterns):
        _fail("durable publication-authority record must be a recognized task, report, decision, or handoff artifact")
    if durable_path not in {row["path"] for row in declarations}:
        _fail("durable publication-authority record must be an authorized repository path")
    supersedes = sorted(set(supersedes or []))
    for fingerprint in supersedes:
        _valid_sha256(fingerprint, prefixed=True)
    parent_entries, parent_tree_oid = _git_parent_entries(
        repository_root, metadata["parent_head"], {row["path"] for row in declarations}
    )
    rows, changed, identical, parent_fp = _classify(declarations, parent_entries)
    durable_row = next(row for row in rows if row["path"] == durable_path)
    if (
        durable_row["representation_kind"] != "complete"
        or durable_row["change_kind"] == "parent_identical"
    ):
        _fail("durable publication-authority record must be a changed complete representation")
    authority: dict[str, Any] = {
        "schema_name": AUTHORITY_SCHEMA,
        "schema_version": AUTHORITY_VERSION,
        "status": "active",
        "parent_head": metadata["parent_head"],
        "parent_tree_oid": parent_tree_oid,
        "registry_path": registry_locator,
        "audit_subject_manifest_fingerprint": audit_fp,
        "source_manifests": {
            "complete": {
                "manifest_fingerprint": metadata["complete_manifest_fingerprint"],
                "path_count": metadata["complete_path_count"],
                "representation_kind": "complete",
            },
            "mixed": {
                "manifest_fingerprint": metadata["mixed_manifest_fingerprint"],
                "path_count": metadata["mixed_path_count"],
                "representation_kind": "mixed",
            },
        },
        "authority_only_entries": metadata["authority_only_entries"],
        "authority_only_path_count": metadata["authority_only_path_count"],
        "durable_record_path": durable_path,
        "parent_population_fingerprint": parent_fp,
        "path_count": len(rows),
        "changed_path_count": len(changed),
        "parent_identical_path_count": len(identical),
        "paths": rows,
        "changed_paths": changed,
        "parent_identical_paths": identical,
        "supersedes": supersedes,
    }
    authority["authority_fingerprint"] = authority_fingerprint(authority)
    return authority


def verify_publication_authority(
    authority: Any,
    complete_manifest: Any,
    mixed_manifest: Any,
    authority_only_entries: Any,
    *,
    repository_root: Path,
) -> dict[str, Any]:
    authority = _strict_dict(authority, "publication authority must be an object")
    if authority.get("schema_name") != AUTHORITY_SCHEMA or authority.get(
        "schema_version"
    ) != AUTHORITY_VERSION:
        _fail("publication authority schema mismatch")
    if authority.get("status") != "active":
        _fail("publication authority is not active; it is stale or superseded")
    supplied_fp = authority.get("authority_fingerprint")
    if supplied_fp != authority_fingerprint(authority):
        _fail("publication authority fingerprint mismatch")
    raw_registry_path = authority.get("registry_path")
    if not isinstance(raw_registry_path, str):
        _fail("publication authority registry locator is missing")
    expected = build_publication_authority(
        complete_manifest,
        mixed_manifest,
        authority_only_entries,
        repository_root=repository_root,
        registry_path=Path(raw_registry_path),
        audit_subject_manifest_fingerprint=authority.get(
            "audit_subject_manifest_fingerprint"
        ),
        durable_record_path=authority.get("durable_record_path"),
        supersedes=authority.get("supersedes"),
    )
    if authority != expected:
        _fail("publication authority does not exactly reconcile current source manifests and authenticated parent tree")
    return {
        "valid": True,
        "authority_fingerprint": supplied_fp,
        "authority_path_count": authority["path_count"],
        "changed_path_count": authority["changed_path_count"],
        "parent_identical_path_count": authority["parent_identical_path_count"],
        "changed_paths": copy.deepcopy(authority["changed_paths"]),
        "parent_identical_paths": copy.deepcopy(authority["parent_identical_paths"]),
    }


def _safe_regular_file(root: Path, relative_path: str) -> Path:
    _valid_path(relative_path)
    if not isinstance(root, Path):
        _fail("source representation root is required")
    try:
        lexical_root = _reject_symlink_components(root, "source representation root")
        root_resolved = lexical_root.resolve(strict=True)
    except OSError as exc:
        raise PublicationAuthorityError(
            f"representation root is missing: {root}"
        ) from exc
    candidate = root / PurePosixPath(relative_path)
    current = root
    for part in PurePosixPath(relative_path).parts:
        current = current / part
        try:
            if stat.S_ISLNK(current.lstat().st_mode):
                _fail(f"unsafe symlink in publication representation: {relative_path}")
        except OSError as exc:
            raise PublicationAuthorityError(
                f"publication representation is missing: {relative_path}"
            ) from exc
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root_resolved)
    except (OSError, ValueError) as exc:
        raise PublicationAuthorityError(
            f"publication representation escapes its root: {relative_path}"
        ) from exc
    if not stat.S_ISREG(resolved.stat().st_mode):
        _fail(f"publication representation is not a regular file: {relative_path}")
    return resolved


def _file_mode(path: Path) -> str:
    return "100755" if path.stat().st_mode & 0o111 else "100644"


def _file_fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def mixed_snapshot_fingerprint(snapshot: dict[str, Any]) -> str:
    return _manifest_fingerprint(snapshot, "snapshot_fingerprint")


def _current_file_identity(root: Path, relative: str, label: str) -> dict[str, Any]:
    path = _safe_regular_file(root, relative)
    permissions = stat.S_IMODE(path.stat().st_mode)
    if permissions & ~0o777:
        _fail(f"{label} unsupported exact filesystem mode: {relative}")
    return {
        "path": relative,
        "filesystem_mode": f"0o{permissions:03o}",
        "size": path.stat().st_size,
        "sha256": _file_fingerprint(path).removeprefix("sha256:"),
    }


def _exact_file_identity(root: Path, row: dict[str, Any], label: str) -> dict[str, Any]:
    path = _safe_regular_file(root, row["path"])
    filesystem_mode = stat.S_IMODE(path.stat().st_mode)
    if "filesystem_mode" in row:
        expected_mode = row["filesystem_mode"]
        if (
            not isinstance(expected_mode, str)
            or re.fullmatch(r"0o[0-7]{3}", expected_mode) is None
            or filesystem_mode != int(expected_mode[2:], 8)
        ):
            _fail(f"{label} exact filesystem mode mismatch: {row['path']}")
        identity_mode = {"filesystem_mode": expected_mode}
    else:
        if _file_mode(path) != row["mode"]:
            _fail(f"{label} Git mode mismatch: {row['path']}")
        identity_mode = {"mode": row["mode"]}
    size = path.stat().st_size
    if size != row["size"]:
        _fail(f"{label} size mismatch: {row['path']}")
    digest = _file_fingerprint(path).removeprefix("sha256:")
    if digest != row["sha256"]:
        _fail(f"{label} identity mismatch: {row['path']}")
    return {"path": row["path"], **identity_mode, "size": size, "sha256": digest}


def _manifest_mixed_rows(mixed_manifest: Any) -> tuple[list[dict[str, Any]], str, str]:
    _declarations, parent_head, manifest_fp = _source_manifest(mixed_manifest, "mixed")
    return copy.deepcopy(mixed_manifest["paths"]), parent_head, manifest_fp


def _current_parent(repository_root: Path, parent_head: str) -> Path:
    root = _repository_root(repository_root)
    try:
        current = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
            text=True, capture_output=True, env=_git_environment(),
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise PublicationAuthorityError("cannot authenticate current repository parent HEAD") from exc
    if current != parent_head:
        _fail("mixed preservation evidence is stale: parent HEAD mismatch")
    return root


def _exact_root_paths(root: Path, expected: set[str], label: str) -> None:
    lexical = _reject_symlink_components(root, label)
    if not lexical.is_dir():
        _fail(f"{label} is not a directory")
    found: set[str] = set()
    for directory, names, files in os.walk(lexical, followlinks=False):
        directory_path = Path(directory)
        for name in names:
            entry = directory_path / name
            if entry.is_symlink():
                _fail(f"{label} contains an unsafe symlink: {entry}")
        for name in files:
            entry = directory_path / name
            if entry.is_symlink() or not stat.S_ISREG(entry.lstat().st_mode):
                _fail(f"{label} contains a non-regular file: {entry}")
            found.add(entry.relative_to(lexical).as_posix())
    if found != expected:
        _fail(f"{label} path population mismatch; missing={sorted(expected-found)}, extra={sorted(found-expected)}")


def capture_mixed_snapshot(
    mixed_manifest: Any,
    *,
    repository_root: Path,
    output_root: Path,
    original_evidence_manifest: Any,
    original_evidence_root: Path,
) -> dict[str, Any]:
    """Copy live mixed bytes only after independent original evidence authenticates them."""
    rows, parent_head, manifest_fp = _manifest_mixed_rows(mixed_manifest)
    repository = _current_parent(repository_root, parent_head)
    _original_snapshot, original_rows = _verified_snapshot_evidence(
        original_evidence_manifest,
        original_evidence_root,
        rows,
        parent_head,
        manifest_fp,
        repository,
        "independent original evidence",
        require_mixed_manifest_fingerprint=False,
    )
    live_before = [
        _exact_file_identity(
            repository, row, "live mixed source before snapshot capture"
        )
        for row in original_evidence_manifest["paths"]
    ]
    if live_before != original_rows:
        _fail(
            "live mixed source does not equal independently authenticated original "
            "evidence; late snapshot or overwrite"
        )
    if not isinstance(output_root, Path):
        _fail("protected mixed snapshot output root is required")
    output = Path(os.path.abspath(os.fspath(output_root)))
    if output.exists() or output.is_symlink():
        _fail("protected mixed snapshot output root already exists")
    _reject_symlink_components(output.parent, "protected mixed snapshot output parent")
    try:
        output.relative_to(repository)
    except ValueError:
        pass
    else:
        _fail("protected mixed snapshot output root must be outside the repository")
    identities = [_current_file_identity(repository, row["path"], "live mixed source") for row in rows]
    snapshot: dict[str, Any] = {
        "schema_name": MIXED_SNAPSHOT_SCHEMA,
        "schema_version": MIXED_SNAPSHOT_VERSION,
        "parent_head": parent_head,
        "mixed_manifest_fingerprint": manifest_fp,
        "path_count": len(identities),
        "paths": identities,
    }
    snapshot["snapshot_fingerprint"] = mixed_snapshot_fingerprint(snapshot)
    try:
        (output / "files").mkdir(parents=True, mode=0o755)
        for row in identities:
            # Copy from independently authenticated evidence, not the mutable live
            # pathname. Live equality is checked immediately before and after the
            # copy, while retained snapshot bytes cannot be redirected by a
            # concurrent live-path replacement.
            source = _safe_regular_file(original_evidence_root / "files", row["path"])
            target = output / "files" / PurePosixPath(row["path"])
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
            with source.open("rb") as source_handle, target.open("xb") as target_handle:
                shutil.copyfileobj(source_handle, target_handle)
            os.chmod(target, int(row["filesystem_mode"][2:], 8))
            _exact_file_identity(output / "files", row, "protected mixed snapshot")
        for row in identities:
            _exact_file_identity(repository, row, "live mixed source after snapshot capture")
        (output / "protected_mixed_manifest.json").write_bytes(_render_json_bytes(snapshot))
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise
    return snapshot


def _validate_mixed_snapshot(
    snapshot: Any,
    rows: list[dict[str, Any]],
    parent_head: str,
    manifest_fp: str,
    *,
    require_mixed_manifest_fingerprint: bool = True,
) -> dict[str, Any]:
    snapshot = _strict_dict(snapshot, "protected mixed snapshot manifest is required")
    expected_keys = {
        "schema_name", "schema_version", "parent_head", "mixed_manifest_fingerprint",
        "path_count", "paths", "snapshot_fingerprint",
    }
    if set(snapshot) != expected_keys:
        _fail("protected mixed snapshot manifest schema is not exact")
    if snapshot.get("schema_name") != MIXED_SNAPSHOT_SCHEMA or snapshot.get("schema_version") != MIXED_SNAPSHOT_VERSION:
        _fail("protected mixed snapshot manifest schema mismatch")
    if snapshot.get("snapshot_fingerprint") != mixed_snapshot_fingerprint(snapshot):
        _fail("protected mixed snapshot fingerprint mismatch")
    if snapshot.get("parent_head") != parent_head:
        _fail("protected mixed snapshot is stale or bound to a different source manifest")
    if (
        require_mixed_manifest_fingerprint
        and snapshot.get("mixed_manifest_fingerprint") != manifest_fp
    ):
        _fail("protected mixed snapshot is bound to a different candidate manifest")
    snapshot_rows = snapshot.get("paths")
    if not isinstance(snapshot_rows, list) or snapshot.get("path_count") != len(rows):
        _fail("protected mixed snapshot path population mismatch")
    prior = None
    normalized_paths = []
    for raw in snapshot_rows:
        row = _strict_dict(raw, "protected mixed snapshot row must be an object")
        if set(row) != {"path", "filesystem_mode", "size", "sha256"}:
            _fail("protected mixed snapshot row schema is not exact")
        path = _valid_path(row.get("path"))
        filesystem_mode = row.get("filesystem_mode")
        if not isinstance(filesystem_mode, str) or re.fullmatch(r"0o[0-7]{3}", filesystem_mode) is None:
            _fail("protected mixed snapshot filesystem mode is malformed")
        _valid_sha256(row.get("sha256"), prefixed=False)
        if isinstance(row.get("size"), bool) or not isinstance(row.get("size"), int) or row["size"] < 0:
            _fail("protected mixed snapshot size is malformed")
        if prior is not None and path <= prior:
            _fail("protected mixed snapshot paths must be canonical sorted unique")
        prior = path
        normalized_paths.append(path)
    if normalized_paths != [row["path"] for row in rows]:
        _fail("protected mixed snapshot path population does not equal mixed manifest")
    return snapshot


def _verified_snapshot_evidence(
    manifest: Any,
    evidence_root: Path,
    rows: list[dict[str, Any]],
    parent_head: str,
    manifest_fp: str,
    repository: Path,
    label: str,
    *,
    require_mixed_manifest_fingerprint: bool = True,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    snapshot = _validate_mixed_snapshot(
        manifest,
        rows,
        parent_head,
        manifest_fp,
        require_mixed_manifest_fingerprint=require_mixed_manifest_fingerprint,
    )
    if not isinstance(evidence_root, Path):
        _fail(f"{label} root is required")
    root = _reject_symlink_components(evidence_root, f"{label} root")
    try:
        root.relative_to(repository)
    except ValueError:
        pass
    else:
        _fail(f"{label} root must be outside the repository")
    try:
        manifest_path = _safe_regular_file(root, "protected_mixed_manifest.json")
        disk_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationAuthorityError(
            f"{label} manifest bytes are missing or malformed"
        ) from exc
    if disk_manifest != snapshot:
        _fail(f"{label} manifest bytes do not match supplied evidence")
    expected = {row["path"] for row in rows}
    _exact_root_paths(root / "files", expected, f"{label} retained bytes")
    identities = [
        _exact_file_identity(root / "files", row, f"{label} retained bytes")
        for row in snapshot["paths"]
    ]
    return snapshot, identities


def verify_mixed_preservation(
    mixed_manifest: Any,
    *,
    repository_root: Path,
    candidate_root: Path,
    protected_manifest: Any,
    protected_root: Path,
    original_evidence_manifest: Any,
    original_evidence_root: Path,
) -> dict[str, Any]:
    """Verify trusted originals, protected snapshot, live files, and candidates separately."""
    rows, parent_head, manifest_fp = _manifest_mixed_rows(mixed_manifest)
    repository = _current_parent(repository_root, parent_head)
    original_snapshot, original_rows = _verified_snapshot_evidence(
        original_evidence_manifest,
        original_evidence_root,
        rows,
        parent_head,
        manifest_fp,
        repository,
        "independent original evidence",
        require_mixed_manifest_fingerprint=False,
    )
    snapshot, protected_rows = _verified_snapshot_evidence(
        protected_manifest,
        protected_root,
        rows,
        parent_head,
        manifest_fp,
        repository,
        "protected mixed snapshot",
    )
    if protected_rows != original_rows:
        _fail("protected mixed snapshot does not equal independent original evidence")
    live_rows = [
        _exact_file_identity(repository, row, "current live mixed source")
        for row in original_snapshot["paths"]
    ]
    candidate_rows = [
        _exact_file_identity(candidate_root, row, "external mixed candidate")
        for row in rows
    ]
    if live_rows != original_rows:
        _fail("current live mixed source does not equal independent original evidence")
    return {
        "valid": True,
        "original_evidence_fingerprint": original_snapshot["snapshot_fingerprint"],
        "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
        "protected_population_fingerprint": value_fingerprint(
            {"role": "live", "paths": protected_rows}
        ),
        "candidate_population_fingerprint": value_fingerprint(
            {"role": "candidate", "paths": candidate_rows}
        ),
        "verified_path_count": len(rows),
    }


def _verify_durable_record_content(
    authority: dict[str, Any], roots: dict[str, Path]
) -> None:
    durable_path = authority["durable_record_path"]
    candidate = _safe_regular_file(roots["complete"], durable_path)
    try:
        content = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise PublicationAuthorityError("durable publication-authority record must be readable UTF-8 text") from exc
    required_lines = {
        "Publication-Authority-Schema: knowledgeforge.publication_authority.v1@1.0",
        f"Publication-Authority-Parent: {authority['parent_head']}",
        f"Publication-Authority-Audit-Subject: {authority['audit_subject_manifest_fingerprint']}",
        (
            "Publication-Authority-Mixed-Manifest: "
            f"{authority['source_manifests']['mixed']['manifest_fingerprint']}"
        ),
        (
            "Publication-Authority-Complete-Path-Count: "
            f"{authority['source_manifests']['complete']['path_count']}"
        ),
        (
            "Publication-Authority-Only-Path-Count: "
            f"{authority['authority_only_path_count']}"
        ),
    }
    actual_lines = set(content.splitlines())
    missing = sorted(required_lines - actual_lines)
    if missing:
        _fail(
            "durable publication-authority record is missing semantic markers: "
            + ", ".join(missing)
        )
    if re.search(
        r"(?m)^Publication-Authority-External-Evidence:\s+\S.*$", content
    ) is None:
        _fail("durable publication-authority record must identify external verification evidence")


def verify_source_representations(
    authority: Any,
    complete_manifest: Any,
    mixed_manifest: Any,
    authority_only_entries: Any,
    *,
    repository_root: Path,
    roots: dict[str, Path] | None,
) -> dict[str, Any]:
    verify_publication_authority(
        authority,
        complete_manifest,
        mixed_manifest,
        authority_only_entries,
        repository_root=repository_root,
    )
    if not isinstance(roots, dict):
        _fail("current source representation roots are required")
    declarations, _ = _assemble_sources(
        complete_manifest, mixed_manifest, authority_only_entries
    )
    declared_sizes = {
        (kind, row["path"]): row["size"]
        for kind, manifest in (
            ("complete", complete_manifest),
            ("mixed", mixed_manifest),
        )
        for row in manifest["paths"]
    }
    verified_rows: list[dict[str, str]] = []
    for row in declarations:
        kind = row["representation_kind"]
        root = roots.get(kind)
        if not isinstance(root, Path):
            _fail(f"missing source representation root: {kind}")
        path = _safe_regular_file(root, row["path"])
        if _file_mode(path) != row["mode"] or _file_fingerprint(path) != row[
            "blob_sha256"
        ]:
            _fail(f"source representation mode or identity mismatch: {row['path']}")
        declared_size = declared_sizes.get((kind, row["path"]))
        if declared_size is not None and path.stat().st_size != declared_size:
            _fail(f"source representation size mismatch: {row['path']}")
        verified_rows.append(dict(row))
    _verify_durable_record_content(authority, roots)
    return {
        "valid": True,
        "authority_fingerprint": authority["authority_fingerprint"],
        "verified_path_count": len(declarations),
        "verified_population_fingerprint": value_fingerprint(verified_rows),
    }


def registry_fingerprint(registry: dict[str, Any]) -> str:
    return _manifest_fingerprint(registry, "registry_fingerprint")


def _validate_authority_document(authority: Any) -> dict[str, Any]:
    authority = _strict_dict(authority, "publication authority must be an object")
    if set(authority) != AUTHORITY_KEYS:
        _fail("publication authority schema fields are not exact")
    if authority.get("schema_name") != AUTHORITY_SCHEMA or authority.get(
        "schema_version"
    ) != AUTHORITY_VERSION:
        _fail("publication authority schema mismatch")
    if authority.get("status") != "active":
        _fail("publication authority status must be active")
    if authority.get("authority_fingerprint") != authority_fingerprint(authority):
        _fail("publication authority fingerprint mismatch")
    supersedes = authority.get("supersedes")
    if not isinstance(supersedes, list) or supersedes != sorted(set(supersedes)):
        _fail("publication authority supersedes population is not canonical")
    for fingerprint in supersedes:
        _valid_sha256(fingerprint, prefixed=True)
    return authority


def _validate_registry_document(registry: Any) -> dict[str, Any]:
    registry = _strict_dict(registry, "publication authority registry must be an object")
    if set(registry) != REGISTRY_KEYS:
        _fail("publication authority registry schema fields are not exact")
    if registry.get("schema_name") != REGISTRY_SCHEMA or registry.get(
        "schema_version"
    ) != REGISTRY_VERSION:
        _fail("publication authority registry schema mismatch")
    generation = registry.get("generation")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
        _fail("publication authority registry generation must be a positive integer")
    predecessor = registry.get("predecessor_registry_fingerprint")
    if generation == 1:
        if predecessor is not None:
            _fail("initial publication authority registry must not name a predecessor")
    else:
        _valid_sha256(predecessor, prefixed=True)
    _valid_sha256(registry.get("active_authority_fingerprint"), prefixed=True)
    superseded = registry.get("superseded_authority_fingerprints")
    if not isinstance(superseded, list) or superseded != sorted(set(superseded)):
        _fail("publication authority registry superseded population is not canonical")
    for fingerprint in superseded:
        _valid_sha256(fingerprint, prefixed=True)
    if registry.get("active_authority_fingerprint") in superseded:
        _fail("active publication authority cannot also be superseded")
    if registry.get("registry_fingerprint") != registry_fingerprint(registry):
        _fail("publication authority registry fingerprint mismatch")
    return registry


def build_authority_registry(
    authority: Any,
    *,
    superseded: list[str] | None = None,
    predecessor_registry: Any | None = None,
) -> dict[str, Any]:
    authority = _validate_authority_document(authority)
    active = _valid_sha256(authority.get("authority_fingerprint"), prefixed=True)
    predecessor = None
    generation = 1
    required_superseded: set[str] = set()
    if predecessor_registry is not None:
        predecessor = _validate_registry_document(predecessor_registry)
        generation = predecessor["generation"] + 1
        required_superseded.update(predecessor["superseded_authority_fingerprints"])
        required_superseded.add(predecessor["active_authority_fingerprint"])
    superseded_values = sorted(set(superseded or []) | required_superseded)
    for fingerprint in superseded_values:
        _valid_sha256(fingerprint, prefixed=True)
    if active in superseded_values:
        _fail("active publication authority cannot also be superseded")
    declared = authority.get("supersedes")
    if predecessor is not None and predecessor[
        "active_authority_fingerprint"
    ] not in declared:
        _fail("successor authority must explicitly supersede the active predecessor")
    if not set(declared).issubset(superseded_values):
        _fail("authority registry must account for every declared predecessor")
    registry: dict[str, Any] = {
        "schema_name": REGISTRY_SCHEMA,
        "schema_version": REGISTRY_VERSION,
        "generation": generation,
        "predecessor_registry_fingerprint": (
            predecessor["registry_fingerprint"] if predecessor is not None else None
        ),
        "active_authority_fingerprint": active,
        "superseded_authority_fingerprints": superseded_values,
    }
    registry["registry_fingerprint"] = registry_fingerprint(registry)
    return registry


def verify_authority_registry(registry: Any, authority: Any) -> dict[str, Any]:
    registry = _validate_registry_document(registry)
    authority = _validate_authority_document(authority)
    active = authority.get("authority_fingerprint")
    superseded = registry["superseded_authority_fingerprints"]
    if active in superseded or registry.get("active_authority_fingerprint") != active:
        _fail("publication authority is stale, superseded, or not the active authority")
    return {
        "valid": True,
        "generation": registry["generation"],
        "registry_fingerprint": registry["registry_fingerprint"],
    }


def _registry_history_directory(registry_path: Path) -> Path:
    return registry_path.parent / "publication_authority_registry.history"


def _render_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def install_authority_registry(
    authority: Any, *, superseded: list[str] | None = None
) -> dict[str, Any]:
    authority = _validate_authority_document(authority)
    raw_path = authority.get("registry_path")
    if not isinstance(raw_path, str):
        _fail("publication authority registry locator is missing")
    path = Path(raw_path)
    _registry_locator(path)
    predecessor = None
    if path.exists():
        try:
            predecessor = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PublicationAuthorityError("canonical publication authority registry is malformed") from exc
        _validate_registry_document(predecessor)
        if predecessor["active_authority_fingerprint"] == authority.get(
            "authority_fingerprint"
        ):
            requested = set(superseded or [])
            existing = set(predecessor["superseded_authority_fingerprints"])
            if not requested.issubset(existing):
                _fail("an active authority registry cannot gain supersession state without a successor authority")
            latest = _load_registry_history(path)[-1]
            if latest["registry_fingerprint"] != predecessor["registry_fingerprint"]:
                _fail("canonical publication authority registry is not latest; rollback detected")
            verify_authority_registry(predecessor, authority)
            return predecessor
    registry = build_authority_registry(
        authority,
        superseded=superseded,
        predecessor_registry=predecessor,
    )
    history = _registry_history_directory(path)
    if history.exists() or history.is_symlink():
        _reject_symlink_components(history, "authority registry history")
        if not history.is_dir():
            _fail("authority registry history must be a directory")
    else:
        history.mkdir(mode=0o755)
    history_name = (
        f"{registry['generation']:08d}-"
        f"{registry['registry_fingerprint'].removeprefix('sha256:')}.json"
    )
    history_path = history / history_name
    rendered = _render_json_bytes(registry)
    try:
        descriptor = os.open(
            history_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o644,
        )
    except FileExistsError:
        if history_path.read_bytes() != rendered:
            _fail("registry history identity collision")
    else:
        try:
            written = 0
            while written < len(rendered):
                count = os.write(descriptor, rendered[written:])
                if count <= 0:
                    _fail("registry history write did not make progress")
                written += count
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=path.parent, prefix=".publication-authority-registry-", delete=False
    ) as temporary:
        temporary.write(rendered)
        temporary.flush()
        os.fsync(temporary.fileno())
        temporary_path = Path(temporary.name)
    os.chmod(temporary_path, 0o644)
    os.replace(temporary_path, path)
    return registry


def _load_registry_history(registry_path: Path) -> list[dict[str, Any]]:
    history = _registry_history_directory(registry_path)
    _reject_symlink_components(history, "authority registry history")
    if not history.is_dir():
        _fail("authority registry history is missing")
    records: list[dict[str, Any]] = []
    for entry in sorted(history.iterdir(), key=lambda item: item.name):
        if entry.is_symlink() or not entry.is_file() or not re.fullmatch(
            r"\d{8}-[0-9a-f]{64}\.json", entry.name
        ):
            _fail("authority registry history contains an unsafe or unexpected entry")
        try:
            record = _validate_registry_document(
                json.loads(entry.read_text(encoding="utf-8"))
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise PublicationAuthorityError("authority registry history is malformed") from exc
        expected_name = (
            f"{record['generation']:08d}-"
            f"{record['registry_fingerprint'].removeprefix('sha256:')}.json"
        )
        if entry.name != expected_name:
            _fail("authority registry history filename does not match its identity")
        records.append(record)
    if not records:
        _fail("authority registry history is empty")
    for index, record in enumerate(records, start=1):
        if record["generation"] != index:
            _fail("authority registry history generations are not contiguous")
        if index == 1:
            if record["predecessor_registry_fingerprint"] is not None:
                _fail("authority registry history initial predecessor is invalid")
        else:
            previous = records[index - 2]
            if record["predecessor_registry_fingerprint"] != previous["registry_fingerprint"]:
                _fail("authority registry history predecessor chain is broken")
            if previous["active_authority_fingerprint"] not in record[
                "superseded_authority_fingerprints"
            ]:
                _fail("authority registry history does not supersede its predecessor")
    return records


def _load_bound_authority_registry(authority: Any) -> dict[str, Any]:
    authority = _strict_dict(authority, "publication authority must be an object")
    raw_path = authority.get("registry_path")
    if not isinstance(raw_path, str):
        _fail("publication authority registry locator is missing")
    path = Path(raw_path)
    _registry_locator(path)
    try:
        registry = _validate_registry_document(
            json.loads(path.read_text(encoding="utf-8"))
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationAuthorityError("canonical publication authority registry is missing or malformed") from exc
    latest = _load_registry_history(path)[-1]
    if registry["registry_fingerprint"] != latest["registry_fingerprint"]:
        _fail("canonical publication authority registry is not the latest history record; rollback detected")
    verify_authority_registry(registry, authority)
    return registry


def build_staging_gate(
    authority: Any,
    complete_manifest: Any,
    mixed_manifest: Any,
    authority_only_entries: Any,
    *,
    repository_root: Path,
    source_roots: dict[str, Path] | None,
    validation_passed: bool,
    protected_mixed_manifest: Any | None = None,
    protected_mixed_root: Path | None = None,
    original_evidence_manifest: Any | None = None,
    original_evidence_root: Path | None = None,
) -> dict[str, Any]:
    if validation_passed is not True:
        _fail("staging validation result must be the strict Boolean true")
    result = verify_publication_authority(
        authority,
        complete_manifest,
        mixed_manifest,
        authority_only_entries,
        repository_root=repository_root,
    )
    registry = _load_bound_authority_registry(authority)
    registry_result = verify_authority_registry(registry, authority)
    source_result = verify_source_representations(
        authority,
        complete_manifest,
        mixed_manifest,
        authority_only_entries,
        repository_root=repository_root,
        roots=source_roots,
    )
    preservation_result = verify_mixed_preservation(
        mixed_manifest,
        repository_root=repository_root,
        candidate_root=source_roots.get("mixed") if isinstance(source_roots, dict) else None,
        protected_manifest=protected_mixed_manifest,
        protected_root=protected_mixed_root,
        original_evidence_manifest=original_evidence_manifest,
        original_evidence_root=original_evidence_root,
    )
    gate: dict[str, Any] = {
        "schema_name": GATE_SCHEMA,
        "schema_version": GATE_VERSION,
        "passed": True,
        "blockers": [],
        "authority_fingerprint": result["authority_fingerprint"],
        "authority_registry_fingerprint": registry_result["registry_fingerprint"],
        "complete_manifest_fingerprint": complete_manifest["manifest_fingerprint"],
        "mixed_manifest_fingerprint": mixed_manifest["manifest_fingerprint"],
        "source_population_fingerprint": source_result["verified_population_fingerprint"],
        "mixed_snapshot_fingerprint": preservation_result["snapshot_fingerprint"],
        "mixed_original_evidence_fingerprint": preservation_result[
            "original_evidence_fingerprint"
        ],
        "mixed_live_population_fingerprint": preservation_result["protected_population_fingerprint"],
        "mixed_candidate_population_fingerprint": preservation_result["candidate_population_fingerprint"],
        "changed_path_count": result["changed_path_count"],
        "parent_identical_path_count": result["parent_identical_path_count"],
        "changed_paths_fingerprint": value_fingerprint(result["changed_paths"]),
    }
    gate["gate_fingerprint"] = gate_fingerprint(gate)
    return gate


def verify_staging_gate(
    gate: Any,
    authority: Any,
    complete_manifest: Any,
    mixed_manifest: Any,
    authority_only_entries: Any,
    *,
    repository_root: Path,
    source_roots: dict[str, Path] | None,
    protected_mixed_manifest: Any | None = None,
    protected_mixed_root: Path | None = None,
    original_evidence_manifest: Any | None = None,
    original_evidence_root: Path | None = None,
) -> dict[str, Any]:
    gate = _strict_dict(gate, "staging gate must be an object")
    if gate.get("schema_name") != GATE_SCHEMA or gate.get("schema_version") != GATE_VERSION:
        _fail("staging gate schema mismatch")
    if gate.get("passed") is not True:
        _fail("staging gate result must be the strict Boolean true")
    if gate.get("blockers") != []:
        _fail("staging gate has blockers")
    if gate.get("gate_fingerprint") != gate_fingerprint(gate):
        _fail("staging gate fingerprint mismatch")
    result = verify_publication_authority(
        authority,
        complete_manifest,
        mixed_manifest,
        authority_only_entries,
        repository_root=repository_root,
    )
    _load_bound_authority_registry(authority)
    expected = build_staging_gate(
        authority,
        complete_manifest,
        mixed_manifest,
        authority_only_entries,
        repository_root=repository_root,
        source_roots=source_roots,
        validation_passed=True,
        protected_mixed_manifest=protected_mixed_manifest,
        protected_mixed_root=protected_mixed_root,
        original_evidence_manifest=original_evidence_manifest,
        original_evidence_root=original_evidence_root,
    )
    if gate != expected:
        _fail("staging gate does not bind current authority, registry, parent tree, and source representations")
    return {
        "staging_authorized": True,
        "authority_fingerprint": result["authority_fingerprint"],
        "changed_path_count": result["changed_path_count"],
        "changed_paths": result["changed_paths"],
        "parent_identical_path_count": result["parent_identical_path_count"],
        "parent_identical_paths": result["parent_identical_paths"],
    }


def _load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str | None, value: Any) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path:
        Path(path).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def _source_inputs(args: argparse.Namespace) -> tuple[Any, Any, Any]:
    return (
        _load_json(args.complete),
        _load_json(args.mixed),
        _load_json(args.authority_only),
    )


def _source_roots(args: argparse.Namespace) -> dict[str, Path]:
    return {
        "complete": Path(args.complete_root),
        "mixed": Path(args.mixed_root),
        "authority_only": Path(args.authority_root),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot-mixed")
    snapshot.add_argument("--mixed", required=True)
    snapshot.add_argument("--repository", required=True)
    snapshot.add_argument("--output-root", required=True)
    snapshot.add_argument("--original-evidence-manifest", required=True)
    snapshot.add_argument("--original-evidence-root", required=True)

    legacy = subparsers.add_parser("check-legacy")
    for name in ("complete", "mixed", "authority-only", "parent-entries", "legacy-authority"):
        legacy.add_argument(f"--{name}", required=True)
    legacy.add_argument("--output")

    build = subparsers.add_parser("build")
    for name in ("complete", "mixed", "authority-only", "repository"):
        build.add_argument(f"--{name}", required=True)
    build.add_argument("--audit-subject-fingerprint", required=True)
    build.add_argument("--durable-record-path", required=True)
    build.add_argument("--registry-path", required=True)
    build.add_argument("--output")

    registry = subparsers.add_parser("registry")
    registry.add_argument("--authority", required=True)
    registry.add_argument("--superseded", action="append", default=[])
    registry.add_argument("--output")

    for command in ("verify-sources", "gate", "verify-gate"):
        child = subparsers.add_parser(command)
        for name in (
            "complete",
            "mixed",
            "authority-only",
            "authority",
            "repository",
            "complete-root",
            "mixed-root",
            "authority-root",
        ):
            child.add_argument(f"--{name}", required=True)
        if command in ("gate", "verify-gate"):
            child.add_argument("--protected-mixed-manifest", required=True)
            child.add_argument("--protected-mixed-root", required=True)
            child.add_argument("--original-evidence-manifest", required=True)
            child.add_argument("--original-evidence-root", required=True)
        if command == "verify-gate":
            child.add_argument("--staging-gate", required=True)
        child.add_argument("--output")

    args = parser.parse_args(argv)
    if args.command == "snapshot-mixed":
        result = capture_mixed_snapshot(
            _load_json(args.mixed),
            repository_root=Path(args.repository),
            output_root=Path(args.output_root),
            original_evidence_manifest=_load_json(args.original_evidence_manifest),
            original_evidence_root=Path(args.original_evidence_root),
        )
        args.output = None
    elif args.command == "check-legacy":
        complete, mixed, extra = _source_inputs(args)
        result = validate_legacy_publication_authority(
            _load_json(args.legacy_authority),
            complete,
            mixed,
            extra,
            _load_json(args.parent_entries),
        )
    elif args.command == "build":
        complete, mixed, extra = _source_inputs(args)
        result = build_publication_authority(
            complete,
            mixed,
            extra,
            repository_root=Path(args.repository),
            registry_path=Path(args.registry_path),
            audit_subject_manifest_fingerprint=args.audit_subject_fingerprint,
            durable_record_path=args.durable_record_path,
        )
    elif args.command == "registry":
        authority = _load_json(args.authority)
        result = install_authority_registry(authority, superseded=args.superseded)
        bound_output = authority.get("registry_path")
        if not isinstance(bound_output, str):
            _fail("publication authority registry locator is missing")
        if args.output is not None and str(Path(args.output).absolute()) != bound_output:
            _fail("registry output must equal the authority-bound canonical registry path")
        args.output = bound_output
    elif args.command == "verify-sources":
        complete, mixed, extra = _source_inputs(args)
        result = verify_source_representations(
            _load_json(args.authority),
            complete,
            mixed,
            extra,
            repository_root=Path(args.repository),
            roots=_source_roots(args),
        )
    elif args.command == "gate":
        complete, mixed, extra = _source_inputs(args)
        result = build_staging_gate(
            _load_json(args.authority),
            complete,
            mixed,
            extra,
            repository_root=Path(args.repository),
            source_roots=_source_roots(args),
            validation_passed=True,
            protected_mixed_manifest=_load_json(args.protected_mixed_manifest),
            protected_mixed_root=Path(args.protected_mixed_root),
            original_evidence_manifest=_load_json(args.original_evidence_manifest),
            original_evidence_root=Path(args.original_evidence_root),
        )
    else:
        complete, mixed, extra = _source_inputs(args)
        result = verify_staging_gate(
            _load_json(args.staging_gate),
            _load_json(args.authority),
            complete,
            mixed,
            extra,
            repository_root=Path(args.repository),
            source_roots=_source_roots(args),
            protected_mixed_manifest=_load_json(args.protected_mixed_manifest),
            protected_mixed_root=Path(args.protected_mixed_root),
            original_evidence_manifest=_load_json(args.original_evidence_manifest),
            original_evidence_root=Path(args.original_evidence_root),
        )
    _write_json(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
