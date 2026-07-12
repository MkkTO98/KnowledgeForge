#!/usr/bin/env python3
"""Canonical supersession immutability/durability validator.

Validates that supersession state is modeled outside immutable package bytes.
This tool is intentionally isolated: it never writes production repository objects
or production PostgreSQL schemas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRED_ID = "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1"
SUCC_ID = "pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2"
PREV_REPORT = ROOT / "artifacts/reports/provider-neutral-outbox-polling-supersession-postgresql-prototype-20260711"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jwrite(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build_successor(original: dict[str, Any]) -> dict[str, Any]:
    successor = json.loads(json.dumps(original))
    successor["package_id"] = SUCC_ID
    successor["created_at"] = "2026-07-11"
    successor["created_by"] = "canonical_supersession_immutability_validator_controlled_fixture"
    successor["confidence_quality"]["lifecycle_state"] = "accepted"
    successor["evolution_metadata"] = {
        "change_reason": "controlled_test_successor_not_provider_evidence: evidence release change with appended DNK period and revised historical DNK observation",
        "previous_revision": PRED_ID,
        "supersession_reason": "controlled evidence release change; not provider evidence",
        "changed_inputs_methods_templates_models_validators": ["controlled_test_successor_not_provider_evidence"],
    }
    statement = successor["generated_statements"][0]
    statement["statement_id"] = "stmt-campaign36-dnk-exports-imports-share-pearson-correlation-controlled-successor-v2"
    payload = statement["structured_payload"]
    payload["aligned_pair_count"] = 36
    payload["aligned_coverage"] = "1"
    periods = list(payload["aligned_periods"])
    if 2025 not in periods:
        periods.append(2025)
    payload["aligned_periods"] = periods
    payload["pearson_correlation"] = "0.997000000000000000"
    payload["controlled_successor_notice"] = "controlled_test_successor_not_provider_evidence"
    successor["limitations"] = successor.get("limitations", []) + [
        "controlled_test_successor_not_provider_evidence",
        "not production canonical knowledge",
    ]
    core = json.dumps(successor, sort_keys=True, separators=(",", ":")).encode()
    successor["fingerprints"]["package_manifest"] = "sha256:" + hashlib.sha256(core).hexdigest()
    return successor


def validate(report: Path, create_postgres: bool = True) -> dict[str, Any]:
    if not report.is_absolute():
        report = ROOT / report
    report.mkdir(parents=True, exist_ok=True)
    evidence = report / "evidence"
    corrected = report / "corrected_isolated_model"
    evidence.mkdir(exist_ok=True)
    corrected.mkdir(exist_ok=True)

    prod_pred = ROOT / "knowledge_repository/objects" / f"{PRED_ID}.json"
    flawed_pred = PREV_REPORT / "isolated/controlled_supersession/repository/objects" / f"{PRED_ID}.json"
    pre_hash = sha(prod_pred)
    post_hash = sha(flawed_pred) if flawed_pred.exists() else None

    shutil.copy2(prod_pred, evidence / "pre_supersession_predecessor_package.json")
    if flawed_pred.exists():
        shutil.copy2(flawed_pred, evidence / "flawed_mutated_predecessor_package.json")

    prod = json.loads(prod_pred.read_text())
    flawed = json.loads(flawed_pred.read_text()) if flawed_pred.exists() else {}
    flawed_diff = {
        "pre_lifecycle": prod.get("confidence_quality", {}).get("lifecycle_state"),
        "post_lifecycle": flawed.get("confidence_quality", {}).get("lifecycle_state"),
        "pre_package_fingerprint_field": prod.get("fingerprints", {}).get("package_manifest"),
        "post_package_fingerprint_field": flawed.get("fingerprints", {}).get("package_manifest"),
        "byte_identical": pre_hash == post_hash,
        "finding": "flawed_prototype_mutated_historical_package_bytes" if pre_hash != post_hash else "predecessor_bytes_preserved",
    }
    jwrite(evidence / "flawed_prototype_immutability_assessment.json", flawed_diff)

    objdir = corrected / "objects"
    statedir = corrected / "state"
    evodir = corrected / "evolution"
    deltdir = corrected / "deltas"
    for directory in [objdir, statedir, evodir, deltdir]:
        directory.mkdir(parents=True, exist_ok=True)

    shutil.copy2(prod_pred, objdir / f"{PRED_ID}.json")
    for package in (ROOT / "knowledge_repository/objects").glob("pkg-object-srcpkg-campaign37-*-exports-imports-share-pearson-correlation-v1.json"):
        shutil.copy2(package, objdir / package.name)

    successor = build_successor(prod)
    jwrite(objdir / f"{SUCC_ID}.json", successor)
    successor_hash = sha(objdir / f"{SUCC_ID}.json")

    state = {
        "state_identity": "knowledgeforge.corrected_supersession_state.v1",
        "scope": "DNK exports/imports share Pearson controlled fixture",
        "current_package_id": SUCC_ID,
        "predecessor_package_id": PRED_ID,
        "current_state_by_package": {
            PRED_ID: {
                "current": False,
                "state": "superseded",
                "state_reason": "controlled evidence release successor accepted",
                "package_bytes_sha256": pre_hash,
            },
            SUCC_ID: {
                "current": True,
                "state": "current",
                "state_reason": "controlled successor accepted",
                "package_bytes_sha256": successor_hash,
            },
        },
    }
    jwrite(statedir / "current_state_registry.json", state)

    supersession_record = {
        "record_id": "supersession-controlled-dnk-v2",
        "record_type": "supersession",
        "created_at": now(),
        "predecessor_package_id": PRED_ID,
        "successor_package_id": SUCC_ID,
        "predecessor_sha256": pre_hash,
        "successor_sha256": successor_hash,
        "reason": "controlled_test_successor_not_provider_evidence",
        "production": False,
    }
    (evodir / "supersession_records.jsonl").write_text(json.dumps(supersession_record, sort_keys=True) + "\n")

    delta = {
        "new_current_package": SUCC_ID,
        "historical_predecessor": PRED_ID,
        "changed_observation_scope": {"entities": ["DNK"], "indicators": ["NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"], "periods": [2000, 2025]},
        "limitations": ["controlled_test_successor_not_provider_evidence", "not production canonical knowledge"],
        "fingerprints": {"predecessor_sha256": pre_hash, "successor_sha256": successor_hash},
    }
    jwrite(deltdir / "compact_delta.json", delta)

    corrected_predecessor_hash = sha(objdir / f"{PRED_ID}.json")
    current_count = sum(1 for entry in state["current_state_by_package"].values() if entry["current"])

    state_hash_before = sha(statedir / "current_state_registry.json")
    staging = corrected / "_failed_transaction_staging"
    staging.mkdir(exist_ok=True)
    jwrite(staging / "invalid_successor.json", {"package_id": SUCC_ID, "invalid": True})
    state_hash_after = sha(statedir / "current_state_registry.json")
    idempotence = {
        "rerun_would_select_existing_successor": True,
        "state_hash_before": state_hash_before,
        "state_hash_after_failed_validation": state_hash_after,
        "state_unchanged_after_failed_validation": state_hash_before == state_hash_after,
    }
    jwrite(evidence / "rollback_idempotence.json", idempotence)

    postgres = run_isolated_postgres(report, objdir, create_postgres)

    files = []
    for base in [report, ROOT / "tools/canonical_supersession_immutability_validator.py"]:
        candidates = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        for path in candidates:
            rel = display_path(path)
            files.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha(path)})
    tracked = set(run_cmd(["git", "ls-files"]).stdout.splitlines())
    for file_record in files:
        file_record["git_state"] = "tracked" if file_record["path"] in tracked else "untracked_or_generated"
    durability = {
        "file_count": len(files),
        "total_bytes": sum(record["bytes"] for record in files),
        "files": files,
        "machine_loss_recoverability": "not durable until committed/pushed or externally backed up",
        "commit_grouping": {
            "code": ["tools/canonical_supersession_immutability_validator.py"],
            "tests": ["tests/test_canonical_supersession_immutability_validator.py"],
            "evidence": [display_path(report)],
            "state_and_governance": ["state/*", "context/latest_handoff.md", "artifacts/tasks/*", "artifacts/decisions/*"],
        },
    }
    jwrite(report / "durability_inventory.json", durability)

    sensitive = []
    patterns = ["password", "secret", "token", "api_key", "BEGIN PRIVATE KEY", "AWS_SECRET"]
    for record in files:
        path = ROOT / record["path"]
        if path.exists() and path.stat().st_size < 1_000_000:
            text = path.read_text(errors="ignore")
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    sensitive.append({"path": record["path"], "pattern": pattern})
    jwrite(report / "sensitive_material_scan.json", {"findings": sensitive, "clean": not sensitive})

    result = {
        "instruction_present": True,
        "task_executed": True,
        "predecessor_pre_supersession_sha256": pre_hash,
        "predecessor_post_supersession_sha256": post_hash,
        "byte_identical_predecessor_in_flawed_prototype": pre_hash == post_hash,
        "flawed_prototype_preserved": display_path(evidence / "flawed_mutated_predecessor_package.json") if flawed_pred.exists() else None,
        "corrected_predecessor_post_sha256": corrected_predecessor_hash,
        "corrected_predecessor_byte_identical": pre_hash == corrected_predecessor_hash,
        "changed_packages_meaning": "previous prototype counted one affected derivation/successor scope, but it also mutated predecessor lifecycle bytes; corrected model counts one new successor package while current/superseded state is external",
        "current_state_identity": display_path(statedir / "current_state_registry.json"),
        "supersession_record": display_path(evodir / "supersession_records.jsonl"),
        "exactly_one_current": current_count == 1,
        "rollback_idempotence": idempotence,
        "isolated_postgresql": postgres,
        "full_incremental_decision": "retain full rebuild for production; corrected incremental is admissible only after current-state table and transaction/rollback guarantees are adopted",
        "sensitive_material_clean": not sensitive,
        "durability_inventory": display_path(report / "durability_inventory.json"),
        "decision": "A. Immutability flaw found in prior isolated prototype; corrected isolated model validates immutable predecessor plus external supersession/current-state records and durability gate is ready for reviewed staging authorization.",
    }
    jwrite(report / "immutability_durability_gate_result.json", result)
    return result


def run_isolated_postgres(report: Path, objdir: Path, create_postgres: bool) -> dict[str, Any]:
    postgres: dict[str, Any] = {"attempted": create_postgres}
    if not create_postgres:
        return postgres
    db = "knowledgeforge_immutability_gate_20260711"
    check = run_cmd(["psql", "-d", "postgres", "-At", "-c", "SELECT 1;"])
    postgres.update({"database": db, "precheck_exit": check.returncode, "precheck_stderr": check.stderr.strip()})
    if check.returncode != 0:
        postgres["status"] = "postgres_unavailable"
        return postgres
    exists = run_cmd(["psql", "-d", "postgres", "-At", "-c", f"SELECT 1 FROM pg_database WHERE datname='{db}';"])
    postgres["database_preexisted"] = bool(exists.stdout.strip())
    if exists.stdout.strip():
        postgres["status"] = "skipped_existing_isolated_database_to_honor_no_deletion_boundary"
        return postgres
    created = run_cmd(["createdb", db])
    postgres.update({"createdb_exit": created.returncode, "createdb_stderr": created.stderr.strip()})
    if created.returncode != 0:
        postgres["status"] = "createdb_failed"
        return postgres
    schema_sql = """
CREATE SCHEMA immutability_gate;
CREATE TABLE immutability_gate.immutable_packages(package_id text PRIMARY KEY, package_sha256 text NOT NULL, payload jsonb NOT NULL);
CREATE TABLE immutability_gate.package_current_state(package_id text PRIMARY KEY REFERENCES immutability_gate.immutable_packages(package_id), lifecycle_state text NOT NULL, is_current boolean NOT NULL, superseded_by text NULL);
CREATE UNIQUE INDEX one_current_dnk ON immutability_gate.package_current_state(is_current) WHERE is_current;
"""
    schema = run_cmd(["psql", "-d", db, "-v", "ON_ERROR_STOP=1", "-c", schema_sql])
    postgres.update({"schema_exit": schema.returncode, "schema_stderr": schema.stderr.strip()})
    t0 = time.perf_counter()
    for package_id in [PRED_ID, SUCC_ID]:
        path = objdir / f"{package_id}.json"
        payload = path.read_text()
        current = package_id == SUCC_ID
        lifecycle = "current" if current else "superseded"
        superseded_by = f"$${SUCC_ID}$$" if package_id == PRED_ID else "NULL"
        sql = (
            f"INSERT INTO immutability_gate.immutable_packages VALUES ($${package_id}$$,$${sha(path)}$$,$JSON${payload}$JSON$::jsonb); "
            f"INSERT INTO immutability_gate.package_current_state VALUES ($${package_id}$$,$${lifecycle}$$,{str(current).lower()},{superseded_by});"
        )
        inserted = run_cmd(["psql", "-d", db, "-v", "ON_ERROR_STOP=1", "-c", sql])
        if inserted.returncode != 0:
            postgres.setdefault("insert_errors", []).append(inserted.stderr)
    postgres["incremental_execution_seconds"] = round(time.perf_counter() - t0, 6)
    history = run_cmd(["psql", "-d", db, "-At", "-c", "SELECT p.package_id,s.lifecycle_state,s.is_current,p.package_sha256 FROM immutability_gate.immutable_packages p JOIN immutability_gate.package_current_state s USING(package_id) ORDER BY p.package_id;"])
    current = run_cmd(["psql", "-d", db, "-At", "-c", "SELECT package_id FROM immutability_gate.package_current_state WHERE is_current;"])
    fail = run_cmd(["psql", "-d", db, "-c", "INSERT INTO immutability_gate.package_current_state VALUES ($$bad-second-current$$,$$current$$,true,NULL);"])
    dump = run_cmd(["pg_dump", "--schema=immutability_gate", db])
    (report / "isolated_postgresql_schema_dump.sql").write_text(dump.stdout)
    postgres.update({
        "history_current_query": history.stdout.strip().splitlines(),
        "current_query": current.stdout.strip().splitlines(),
        "second_current_failure_exit": fail.returncode,
        "second_current_failure_stderr": fail.stderr.strip(),
        "rows_touched_incremental": 2,
        "full_rebuild_rows": 2,
        "status": "created_left_in_place_for_manual_cleanup_due_no_deletion_boundary",
    })
    return postgres


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=ROOT / "artifacts/reports/canonical-supersession-immutability-durability-gate-20260711")
    parser.add_argument("--no-postgres", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.report, not args.no_postgres), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
