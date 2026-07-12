#!/usr/bin/env python3
"""KnowledgeForge PostgreSQL operational projection.

This module implements the first bounded PostgreSQL projection slice approved by
D-20260710-bounded-postgresql-knowledge-repository-realization.

Canonical authority remains exclusively with `knowledge_repository/objects/*.json`.
PostgreSQL is a KnowledgeForge-owned operational projection for discovery and
retrieval. It may not originate or mutate canonical knowledge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
DEFAULT_DATABASE = os.environ.get("KNOWLEDGEFORGE_PG_DATABASE", "knowledgeforge")
SCHEMA_NAME = "knowledgeforge_projection"
TOOL_VERSION = "postgresql_operational_projection_v1"
EXPECTED_CAMPAIGN33_REPOSITORY_FINGERPRINT = "sha256:9c7ebb9cc47f3dc58a06828fa334e53473b59f563845b1c64343840ee7a9479c"


class ProjectionError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def psql(database: str, sql: str, *, tuples_only: bool = False) -> str:
    args = ["psql", "-X", "-v", "ON_ERROR_STOP=1", "-d", database]
    if tuples_only:
        args.extend(["-At"])
    proc = subprocess.run(args, input=sql, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise ProjectionError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout


def psql_json(database: str, sql: str) -> Any:
    output = psql(database, sql, tuples_only=True).strip()
    if not output:
        return None
    return json.loads(output)


def database_exists(database: str) -> bool:
    try:
        out = psql("postgres", f"SELECT 1 FROM pg_database WHERE datname = {sql_literal(database)};", tuples_only=True).strip()
        return out == "1"
    except ProjectionError:
        return False


def ensure_database(database: str, *, create: bool = False) -> dict[str, Any]:
    if database_exists(database):
        owner = psql(
            "postgres",
            f"SELECT pg_catalog.pg_get_userbyid(datdba) FROM pg_database WHERE datname = {sql_literal(database)};",
            tuples_only=True,
        ).strip()
        return {"database": database, "exists": True, "created": False, "owner": owner}
    if not create:
        raise ProjectionError(f"KnowledgeForge PostgreSQL database does not exist: {database}")
    proc = subprocess.run(["createdb", database], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise ProjectionError(proc.stderr.strip() or proc.stdout.strip())
    owner = psql(
        "postgres",
        f"SELECT pg_catalog.pg_get_userbyid(datdba) FROM pg_database WHERE datname = {sql_literal(database)};",
        tuples_only=True,
    ).strip()
    return {"database": database, "exists": True, "created": True, "owner": owner}


def load_manifest(repository_root: Path) -> dict[str, Any]:
    return json.loads((repository_root / "manifest.json").read_text())


def load_canonical_packages(repository_root: Path, *, traversal_order: str = "sorted") -> list[dict[str, Any]]:
    object_paths = list((repository_root / "objects").glob("*.json"))
    if traversal_order == "reverse":
        object_paths = sorted(object_paths, reverse=True)
    elif traversal_order == "filesystem":
        object_paths = object_paths
    else:
        object_paths = sorted(object_paths)
    packages = []
    for path in object_paths:
        value = json.loads(path.read_text())
        if not isinstance(value, dict):
            raise ProjectionError(f"canonical package file is not an object: {path}")
        packages.append(value)
    return packages


def validate_canonical_package(package: dict[str, Any]) -> None:
    package_id = package.get("package_id", "<missing-package-id>")
    if package.get("package_kind") != "KnowledgeObjectPackage":
        raise ProjectionError(f"{package_id} is not a KnowledgeObjectPackage")
    validation = package.get("validation_state")
    if not isinstance(validation, dict) or validation.get("validation_result") != "pass" or validation.get("blockers"):
        raise ProjectionError(f"{package_id} is not a passing validated package")
    if not isinstance(package.get("provenance_envelope"), dict):
        raise ProjectionError(f"{package_id} is missing provenance_envelope")
    if not isinstance(package.get("fingerprints"), dict):
        raise ProjectionError(f"{package_id} is missing fingerprints")
    if not package.get("fingerprints", {}).get("package_manifest"):
        raise ProjectionError(f"{package_id} is missing package_manifest fingerprint")
    if not isinstance(package.get("generated_statements"), list) or not package["generated_statements"]:
        raise ProjectionError(f"{package_id} is missing generated_statements")
    quality = package.get("confidence_quality")
    if not isinstance(quality, dict) or not quality.get("lifecycle_state"):
        raise ProjectionError(f"{package_id} is missing lifecycle_state")


def validate_canonical_repository(repository_root: Path, packages: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = load_manifest(repository_root)
    manifest_ids = manifest.get("package_ids") or []
    package_ids = sorted(package["package_id"] for package in packages)
    if len(package_ids) != len(set(package_ids)):
        raise ProjectionError("duplicate canonical package IDs detected")
    if package_ids != sorted(manifest_ids):
        raise ProjectionError("canonical object package IDs do not match manifest package_ids")
    if manifest.get("object_count") != len(packages):
        raise ProjectionError("canonical object count does not match manifest object_count")
    for package in packages:
        validate_canonical_package(package)
    return manifest


def snapshot_canonical_package_bytes(repository_root: Path) -> dict[str, str]:
    return {
        path.name: sha256_bytes(path.read_bytes())
        for path in sorted((repository_root / "objects").glob("*.json"))
    }


def package_rows(repository_root: Path, packages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for package in sorted(packages, key=lambda item: item["package_id"]):
        package_id = package["package_id"]
        payload = canonical_json(package)
        rows.append(
            {
                "package_id": package_id,
                "package_fingerprint": sha256_fingerprint(package),
                "package_manifest_fingerprint": package.get("fingerprints", {}).get("package_manifest", ""),
                "canonical_path": f"objects/{package_id}.json",
                "evidence_family": package.get("scope", {}).get("evidence_family", "unspecified"),
                "lifecycle_state": package.get("confidence_quality", {}).get("lifecycle_state", "unspecified"),
                "payload_sha256": sha256_bytes(payload.encode("utf-8")),
                "payload_json": payload,
            }
        )
    return rows


def statement_type_rows(packages: list[dict[str, Any]]) -> list[tuple[str, str]]:
    rows: set[tuple[str, str]] = set()
    for package in packages:
        package_id = package["package_id"]
        for statement in package.get("generated_statements", []):
            rows.add((package_id, statement.get("statement_type", "unspecified")))
    return sorted(rows)


def _add_relation(rows: set[tuple[str, str, str]], package_id: str, relation_type: str, target: Any) -> None:
    if isinstance(target, str) and target:
        rows.add((package_id, relation_type, target))


def provenance_lineage_rows(packages: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    rows: set[tuple[str, str, str]] = set()
    for package in packages:
        package_id = package["package_id"]
        envelope = package.get("provenance_envelope", {}) or {}
        for value in envelope.get("evidence_refs", []) or []:
            _add_relation(rows, package_id, "evidence_ref", value)
        for value in envelope.get("evaluation_refs", []) or []:
            _add_relation(rows, package_id, "evaluation_ref", value)
        for value in package.get("input_references", []) or []:
            _add_relation(rows, package_id, "input_reference", value)
        for ref in package.get("evidence_references", []) or []:
            if isinstance(ref, dict):
                _add_relation(rows, package_id, "evidence_reference_record", ref.get("evidence_ref_id"))
        for statement in package.get("generated_statements", []) or []:
            if isinstance(statement, dict):
                for value in statement.get("evidence_refs", []) or []:
                    _add_relation(rows, package_id, "statement_evidence_ref", value)
                for value in statement.get("dependencies", []) or []:
                    _add_relation(rows, package_id, "statement_dependency", value)
        lineage = package.get("lineage", {}) or {}
        _add_relation(rows, package_id, "previous_package_id", lineage.get("previous_package_id"))
        for value in lineage.get("version_lineage", []) or []:
            _add_relation(rows, package_id, "version_lineage", value)
    return sorted(rows)


def logical_projection_fingerprint(rows: list[dict[str, Any]]) -> str:
    basis = [
        {
            "package_id": row["package_id"],
            "package_fingerprint": row["package_fingerprint"],
            "package_manifest_fingerprint": row["package_manifest_fingerprint"],
            "canonical_path": row["canonical_path"],
            "payload_sha256": row["payload_sha256"],
        }
        for row in sorted(rows, key=lambda item: item["package_id"])
    ]
    return sha256_fingerprint(basis)


def create_schema_sql() -> str:
    return f"""
CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.projection_state (
    projection_id text PRIMARY KEY,
    repository_fingerprint text NOT NULL,
    object_count integer NOT NULL,
    logical_projection_fingerprint text NOT NULL,
    tool_version text NOT NULL,
    status text NOT NULL CHECK (status IN ('building','valid','failed','invalid')),
    validity_message text NOT NULL,
    build_started_at timestamptz NOT NULL,
    build_finished_at timestamptz,
    active boolean NOT NULL DEFAULT false
);
CREATE UNIQUE INDEX IF NOT EXISTS projection_state_single_active_valid
    ON {SCHEMA_NAME}.projection_state(active)
    WHERE active AND status = 'valid';
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.projected_packages (
    projection_id text NOT NULL REFERENCES {SCHEMA_NAME}.projection_state(projection_id) ON DELETE CASCADE,
    package_id text NOT NULL,
    package_fingerprint text NOT NULL,
    package_manifest_fingerprint text NOT NULL,
    canonical_path text NOT NULL,
    evidence_family text NOT NULL,
    lifecycle_state text NOT NULL,
    payload_sha256 text NOT NULL,
    payload_json jsonb NOT NULL,
    PRIMARY KEY (projection_id, package_id)
);
CREATE INDEX IF NOT EXISTS projected_packages_package_id_idx ON {SCHEMA_NAME}.projected_packages(package_id);
CREATE INDEX IF NOT EXISTS projected_packages_evidence_family_idx ON {SCHEMA_NAME}.projected_packages(evidence_family, package_id);
CREATE INDEX IF NOT EXISTS projected_packages_lifecycle_state_idx ON {SCHEMA_NAME}.projected_packages(lifecycle_state, package_id);
CREATE INDEX IF NOT EXISTS projected_packages_package_fingerprint_idx ON {SCHEMA_NAME}.projected_packages(package_fingerprint, package_id);
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.package_statement_types (
    projection_id text NOT NULL,
    package_id text NOT NULL,
    statement_type text NOT NULL,
    PRIMARY KEY (projection_id, package_id, statement_type),
    FOREIGN KEY (projection_id, package_id) REFERENCES {SCHEMA_NAME}.projected_packages(projection_id, package_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS package_statement_types_statement_type_idx ON {SCHEMA_NAME}.package_statement_types(statement_type, package_id);
CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.provenance_lineage_edges (
    projection_id text NOT NULL,
    package_id text NOT NULL,
    relation_type text NOT NULL,
    target_id text NOT NULL,
    PRIMARY KEY (projection_id, package_id, relation_type, target_id),
    FOREIGN KEY (projection_id, package_id) REFERENCES {SCHEMA_NAME}.projected_packages(projection_id, package_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS provenance_lineage_edges_package_idx ON {SCHEMA_NAME}.provenance_lineage_edges(package_id, relation_type, target_id);
"""


def rebuild_projection(repository_root: Path | str = DEFAULT_REPOSITORY_ROOT, database: str = DEFAULT_DATABASE, *, traversal_order: str = "sorted") -> dict[str, Any]:
    root = Path(repository_root)
    packages = load_canonical_packages(root, traversal_order=traversal_order)
    manifest = validate_canonical_repository(root, packages)
    rows = package_rows(root, packages)
    statement_rows = statement_type_rows(packages)
    lineage_rows = provenance_lineage_rows(packages)
    projection_id = sha256_fingerprint(
        {
            "tool_version": TOOL_VERSION,
            "repository_fingerprint": manifest["repository_fingerprint"],
            "object_count": len(rows),
            "logical_projection_fingerprint": logical_projection_fingerprint(rows),
        }
    )
    logical_fp = logical_projection_fingerprint(rows)
    started_at = datetime.now(timezone.utc).isoformat()

    statements = ["BEGIN;", create_schema_sql()]
    statements.append(f"DELETE FROM {SCHEMA_NAME}.projection_state;")
    statements.append(
        f"INSERT INTO {SCHEMA_NAME}.projection_state "
        "(projection_id, repository_fingerprint, object_count, logical_projection_fingerprint, tool_version, status, validity_message, build_started_at, active) VALUES ("
        f"{sql_literal(projection_id)}, {sql_literal(manifest['repository_fingerprint'])}, {len(rows)}, {sql_literal(logical_fp)}, "
        f"{sql_literal(TOOL_VERSION)}, 'building', 'full rebuild in progress', {sql_literal(started_at)}::timestamptz, false);"
    )
    for row in rows:
        statements.append(
            f"INSERT INTO {SCHEMA_NAME}.projected_packages "
            "(projection_id, package_id, package_fingerprint, package_manifest_fingerprint, canonical_path, evidence_family, lifecycle_state, payload_sha256, payload_json) VALUES ("
            f"{sql_literal(projection_id)}, {sql_literal(row['package_id'])}, {sql_literal(row['package_fingerprint'])}, "
            f"{sql_literal(row['package_manifest_fingerprint'])}, {sql_literal(row['canonical_path'])}, {sql_literal(row['evidence_family'])}, "
            f"{sql_literal(row['lifecycle_state'])}, {sql_literal(row['payload_sha256'])}, {sql_literal(row['payload_json'])}::jsonb);"
        )
    for package_id, statement_type in statement_rows:
        statements.append(
            f"INSERT INTO {SCHEMA_NAME}.package_statement_types (projection_id, package_id, statement_type) VALUES "
            f"({sql_literal(projection_id)}, {sql_literal(package_id)}, {sql_literal(statement_type)});"
        )
    for package_id, relation_type, target_id in lineage_rows:
        statements.append(
            f"INSERT INTO {SCHEMA_NAME}.provenance_lineage_edges (projection_id, package_id, relation_type, target_id) VALUES "
            f"({sql_literal(projection_id)}, {sql_literal(package_id)}, {sql_literal(relation_type)}, {sql_literal(target_id)});"
        )
    statements.append(
        f"UPDATE {SCHEMA_NAME}.projection_state SET status='valid', validity_message='full rebuild complete and verified', "
        f"build_finished_at=now(), active=true WHERE projection_id={sql_literal(projection_id)};"
    )
    statements.append("COMMIT;")
    psql(database, "\n".join(statements))
    verification = verify_projection(root, database)
    if not verification["valid"]:
        raise ProjectionError("post-rebuild verification failed: " + json.dumps(verification, sort_keys=True))
    return {
        "valid": True,
        "projection_id": projection_id,
        "repository_fingerprint": manifest["repository_fingerprint"],
        "object_count": len(rows),
        "logical_projection_fingerprint": logical_fp,
        "statement_type_rows": len(statement_rows),
        "provenance_lineage_rows": len(lineage_rows),
        "database": database,
        "schema": SCHEMA_NAME,
        "tool_version": TOOL_VERSION,
    }


def active_state(database: str) -> dict[str, Any] | None:
    return psql_json(
        database,
        f"""
SELECT row_to_json(s)::text
FROM (
  SELECT projection_id, repository_fingerprint, object_count, logical_projection_fingerprint,
         tool_version, status, validity_message, active
  FROM {SCHEMA_NAME}.projection_state
  WHERE active AND status='valid'
  ORDER BY build_finished_at DESC NULLS LAST
  LIMIT 1
) s;
""",
    )


def db_logical_fingerprint(database: str, projection_id: str) -> str:
    rows = psql_json(
        database,
        f"""
SELECT COALESCE(json_agg(row_to_json(t) ORDER BY package_id), '[]'::json)::text
FROM (
  SELECT package_id, package_fingerprint, package_manifest_fingerprint, canonical_path, payload_sha256
  FROM {SCHEMA_NAME}.projected_packages
  WHERE projection_id = {sql_literal(projection_id)}
  ORDER BY package_id
) t;
""",
    )
    return sha256_fingerprint(rows or [])


def validate_projection_freshness(repository_root: Path | str, database: str) -> dict[str, Any]:
    root = Path(repository_root)
    manifest = load_manifest(root)
    try:
        state = active_state(database)
    except ProjectionError as exc:
        return {"valid": False, "error": "stale_or_invalid_projection", "detail": str(exc)}
    if not state:
        return {"valid": False, "error": "stale_or_invalid_projection", "detail": "no active valid projection state"}
    reasons: list[str] = []
    if state.get("repository_fingerprint") != manifest.get("repository_fingerprint"):
        reasons.append("repository_fingerprint_mismatch")
    if state.get("object_count") != manifest.get("object_count"):
        reasons.append("object_count_mismatch")
    count = psql_json(database, f"SELECT count(*)::int FROM {SCHEMA_NAME}.projected_packages WHERE projection_id={sql_literal(state['projection_id'])};")
    if count != manifest.get("object_count"):
        reasons.append("projected_count_mismatch")
    logical = db_logical_fingerprint(database, state["projection_id"])
    if logical != state.get("logical_projection_fingerprint"):
        reasons.append("logical_projection_fingerprint_mismatch")
    if reasons:
        return {"valid": False, "error": "stale_or_invalid_projection", "reasons": sorted(reasons), "state": state}
    return {"valid": True, "state": state, "projected_count": count, "logical_projection_fingerprint": logical}


def verify_projection(repository_root: Path | str = DEFAULT_REPOSITORY_ROOT, database: str = DEFAULT_DATABASE) -> dict[str, Any]:
    root = Path(repository_root)
    packages = load_canonical_packages(root)
    manifest = validate_canonical_repository(root, packages)
    canonical_by_id = {package["package_id"]: package for package in packages}
    fresh = validate_projection_freshness(root, database)
    if not fresh["valid"]:
        return fresh
    projection_id = fresh["state"]["projection_id"]
    projected = psql_json(
        database,
        f"""
SELECT COALESCE(json_agg(row_to_json(t) ORDER BY package_id), '[]'::json)::text
FROM (
  SELECT package_id, package_fingerprint, package_manifest_fingerprint, canonical_path, payload_sha256, payload_json
  FROM {SCHEMA_NAME}.projected_packages
  WHERE projection_id = {sql_literal(projection_id)}
  ORDER BY package_id
) t;
""",
    ) or []
    projected_ids = [row["package_id"] for row in projected]
    canonical_ids = sorted(canonical_by_id)
    missing = sorted(set(canonical_ids) - set(projected_ids))
    extra = sorted(set(projected_ids) - set(canonical_ids))
    payload_failures = []
    fingerprint_failures = []
    for row in projected:
        package = canonical_by_id.get(row["package_id"])
        if package is None:
            continue
        canonical_payload = canonical_json(package)
        if canonical_json(row["payload_json"]) != canonical_payload:
            payload_failures.append(row["package_id"])
        if row["package_fingerprint"] != sha256_fingerprint(package):
            fingerprint_failures.append(row["package_id"])
        if row["payload_sha256"] != sha256_bytes(canonical_payload.encode("utf-8")):
            payload_failures.append(row["package_id"] + ":payload_sha")
    return {
        "valid": not missing and not extra and not payload_failures and not fingerprint_failures,
        "repository_fingerprint": manifest["repository_fingerprint"],
        "state_repository_fingerprint": fresh["state"]["repository_fingerprint"],
        "projected_object_count": len(projected),
        "canonical_object_count": len(canonical_ids),
        "missing_package_ids": missing,
        "extra_package_ids": extra,
        "payload_fidelity_failures": len(payload_failures),
        "payload_fidelity_failure_ids": payload_failures[:10],
        "package_fingerprint_failures": len(fingerprint_failures),
        "package_fingerprint_failure_ids": fingerprint_failures[:10],
        "logical_projection_fingerprint": fresh["logical_projection_fingerprint"],
        "projection_id": projection_id,
    }


def lookup_package(repository_root: Path | str, database: str, package_id: str) -> dict[str, Any]:
    fresh = validate_projection_freshness(repository_root, database)
    if not fresh["valid"]:
        return fresh
    projection_id = fresh["state"]["projection_id"]
    row = psql_json(
        database,
        f"""
SELECT row_to_json(t)::text
FROM (
  SELECT package_id, package_fingerprint, package_manifest_fingerprint, canonical_path, evidence_family, lifecycle_state, payload_json AS payload
  FROM {SCHEMA_NAME}.projected_packages
  WHERE projection_id={sql_literal(projection_id)} AND package_id={sql_literal(package_id)}
) t;
""",
    )
    return {"valid": True, "package": row}


def filter_packages(repository_root: Path | str, database: str, *, evidence_family: str | None = None, statement_type: str | None = None, lifecycle_state: str | None = None, package_fingerprint: str | None = None) -> dict[str, Any]:
    fresh = validate_projection_freshness(repository_root, database)
    if not fresh["valid"]:
        return fresh
    projection_id = fresh["state"]["projection_id"]
    where = [f"p.projection_id={sql_literal(projection_id)}"]
    join = ""
    if evidence_family is not None:
        where.append(f"p.evidence_family={sql_literal(evidence_family)}")
    if lifecycle_state is not None:
        where.append(f"p.lifecycle_state={sql_literal(lifecycle_state)}")
    if package_fingerprint is not None:
        where.append(f"p.package_fingerprint={sql_literal(package_fingerprint)}")
    if statement_type is not None:
        join = f"JOIN {SCHEMA_NAME}.package_statement_types st ON st.projection_id=p.projection_id AND st.package_id=p.package_id"
        where.append(f"st.statement_type={sql_literal(statement_type)}")
    package_ids = psql_json(
        database,
        f"""
SELECT COALESCE(json_agg(package_id ORDER BY package_id), '[]'::json)::text
FROM (
  SELECT DISTINCT p.package_id
  FROM {SCHEMA_NAME}.projected_packages p
  {join}
  WHERE {' AND '.join(where)}
  ORDER BY p.package_id
) q;
""",
    ) or []
    return {"valid": True, "package_ids": package_ids, "count": len(package_ids)}


def provenance_lineage(repository_root: Path | str, database: str, package_id: str) -> dict[str, Any]:
    fresh = validate_projection_freshness(repository_root, database)
    if not fresh["valid"]:
        return fresh
    projection_id = fresh["state"]["projection_id"]
    relationships = psql_json(
        database,
        f"""
SELECT COALESCE(json_agg(row_to_json(t) ORDER BY relation_type, target_id), '[]'::json)::text
FROM (
  SELECT relation_type, target_id
  FROM {SCHEMA_NAME}.provenance_lineage_edges
  WHERE projection_id={sql_literal(projection_id)} AND package_id={sql_literal(package_id)}
  ORDER BY relation_type, target_id
) t;
""",
    ) or []
    return {"valid": True, "package_id": package_id, "relationships": relationships, "count": len(relationships)}


def inject_stale_test_row(database: str, package_id: str) -> None:
    state = active_state(database)
    if not state:
        raise ProjectionError("no active state for stale row injection")
    payload = canonical_json({"package_id": package_id, "test_only": True})
    psql(
        database,
        f"""
INSERT INTO {SCHEMA_NAME}.projected_packages
(projection_id, package_id, package_fingerprint, package_manifest_fingerprint, canonical_path, evidence_family, lifecycle_state, payload_sha256, payload_json)
VALUES ({sql_literal(state['projection_id'])}, {sql_literal(package_id)}, 'sha256:test', 'sha256:test', 'objects/stale.json', 'test', 'accepted', {sql_literal(sha256_bytes(payload.encode('utf-8')))}, {sql_literal(payload)}::jsonb);
""",
    )


def package_exists_in_projection(database: str, package_id: str) -> bool:
    count = psql_json(database, f"SELECT count(*)::int FROM {SCHEMA_NAME}.projected_packages WHERE package_id={sql_literal(package_id)};")
    return bool(count)


def mark_projection_invalid_for_test(database: str, *, repository_fingerprint: str) -> None:
    psql(database, f"UPDATE {SCHEMA_NAME}.projection_state SET repository_fingerprint={sql_literal(repository_fingerprint)} WHERE active=true;")


def create_failed_build_marker_for_test(database: str) -> None:
    psql(database, create_schema_sql())
    psql(
        database,
        f"""
DELETE FROM {SCHEMA_NAME}.projection_state;
INSERT INTO {SCHEMA_NAME}.projection_state
(projection_id, repository_fingerprint, object_count, logical_projection_fingerprint, tool_version, status, validity_message, build_started_at, active)
VALUES ('test-failed-build', 'sha256:failed', 0, 'sha256:failed', {sql_literal(TOOL_VERSION)}, 'failed', 'test failed rebuild marker', now(), false);
""",
    )


def inspect_database_isolation(database: str) -> dict[str, Any]:
    owner = psql("postgres", f"SELECT pg_catalog.pg_get_userbyid(datdba) FROM pg_database WHERE datname={sql_literal(database)};", tuples_only=True).strip()
    rows = psql_json(
        database,
        f"""
SELECT COALESCE(json_agg(row_to_json(t) ORDER BY table_schema, table_name), '[]'::json)::text
FROM (
  SELECT table_schema, table_name
  FROM information_schema.tables
  WHERE table_name IN ('projection_state','projected_packages','package_statement_types','provenance_lineage_edges')
    AND table_schema <> {sql_literal(SCHEMA_NAME)}
  ORDER BY table_schema, table_name
) t;
""",
    ) or []
    table_counts = psql_json(
        database,
        f"""
SELECT row_to_json(t)::text
FROM (
  SELECT
    (SELECT count(*)::int FROM {SCHEMA_NAME}.projection_state) AS projection_state,
    (SELECT count(*)::int FROM {SCHEMA_NAME}.projected_packages) AS projected_packages,
    (SELECT count(*)::int FROM {SCHEMA_NAME}.package_statement_types) AS package_statement_types,
    (SELECT count(*)::int FROM {SCHEMA_NAME}.provenance_lineage_edges) AS provenance_lineage_edges
) t;
""",
    )
    return {
        "database": database,
        "database_owner": owner,
        "schema": SCHEMA_NAME,
        "non_knowledgeforge_schemas_with_projection_tables": rows,
        "table_counts": table_counts,
    }


def query_evidence(database: str) -> dict[str, Any]:
    return {
        "database": database,
        "isolation": inspect_database_isolation(database),
        "state": active_state(database),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="KnowledgeForge PostgreSQL operational projection")
    parser.add_argument("--repository-root", type=Path, default=DEFAULT_REPOSITORY_ROOT)
    parser.add_argument("--database", default=DEFAULT_DATABASE)
    parser.add_argument("--create-database", action="store_true")
    parser.add_argument("--output", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("ensure-database")
    rebuild = sub.add_parser("rebuild")
    rebuild.add_argument("--traversal-order", choices=["sorted", "reverse", "filesystem"], default="sorted")
    sub.add_parser("verify")
    lookup = sub.add_parser("lookup")
    lookup.add_argument("package_id")
    filt = sub.add_parser("filter")
    filt.add_argument("--evidence-family")
    filt.add_argument("--statement-type")
    filt.add_argument("--lifecycle-state")
    filt.add_argument("--package-fingerprint")
    lineage = sub.add_parser("lineage")
    lineage.add_argument("package_id")
    sub.add_parser("evidence")
    sub.add_parser("failed-marker-test")
    args = parser.parse_args()

    if args.command == "ensure-database":
        result = ensure_database(args.database, create=args.create_database)
    else:
        if not database_exists(args.database):
            if args.create_database:
                ensure_database(args.database, create=True)
            else:
                raise ProjectionError(f"database does not exist: {args.database}")
        if args.command == "rebuild":
            result = rebuild_projection(args.repository_root, args.database, traversal_order=args.traversal_order)
        elif args.command == "verify":
            result = verify_projection(args.repository_root, args.database)
        elif args.command == "lookup":
            result = lookup_package(args.repository_root, args.database, args.package_id)
        elif args.command == "filter":
            result = filter_packages(
                args.repository_root,
                args.database,
                evidence_family=args.evidence_family,
                statement_type=args.statement_type,
                lifecycle_state=args.lifecycle_state,
                package_fingerprint=args.package_fingerprint,
            )
        elif args.command == "lineage":
            result = provenance_lineage(args.repository_root, args.database, args.package_id)
        elif args.command == "evidence":
            result = query_evidence(args.database)
        elif args.command == "failed-marker-test":
            create_failed_build_marker_for_test(args.database)
            result = validate_projection_freshness(args.repository_root, args.database)
        else:
            raise AssertionError(args.command)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
    if isinstance(result, dict) and result.get("valid") is False and args.command in {"lookup", "filter", "lineage"}:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
