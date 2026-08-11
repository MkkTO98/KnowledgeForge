#!/usr/bin/env python3
"""Pinned Evidence Portfolio admission-attempt profile v1.

This module describes the complete operational subject immediately before the
existing Evidence Portfolio owner may call canonical package persistence.  It
has no persistence API and does not modify historical conformance profile v1.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

from validate_knowledge_pipeline_v1 import validate_knowledge_object

SCHEMA_NAME = "knowledgeforge.evidence_portfolio.admission_attempt.v1"
SCHEMA_VERSION = "1.0"
PROFILE_ID = f"{SCHEMA_NAME}@{SCHEMA_VERSION}"
MODES = {"canary", "production"}
NEGATIVE_STAGE_BY_DISPOSITION = {
    "null": {"calculation"},
    "rejected": set(),
    "failed": {"input_validation", "calculation"},
}
MANIFEST_IDENTITY_KINDS = {"file_bytes", "canonical_in_memory_bytes"}
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}")
_FIELDS = {
    "schema_name",
    "schema_version",
    "profile_id",
    "mode",
    "manifest",
    "manifest_fingerprint",
    "manifest_byte_fingerprint",
    "manifest_identity_kind",
    "evaluated_candidate_ids",
    "unevaluated_candidate_ids",
    "outcomes",
    "reruns",
    "blockers",
    "proposal_state",
    "packages",
    "package_fingerprints",
    "result_fingerprints",
    "views",
    "view_fingerprints",
    "decision",
    "attempt_fingerprint",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _json_equal(left: Any, right: Any) -> bool:
    """Compare JSON semantics without Python's bool/int/float coercions."""
    return canonical_json(left) == canonical_json(right)


def fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_profile(profile_id: Any) -> None:
    if profile_id != PROFILE_ID:
        raise ValueError(f"exact admission-attempt profile {PROFILE_ID} is required")


def _manifest_fingerprint(manifest: dict[str, Any]) -> str:
    return fingerprint({key: value for key, value in manifest.items() if key != "manifest_fingerprint"})


def _selected_entries(manifest: dict[str, Any], mode: str) -> list[dict[str, Any]]:
    if mode not in MODES:
        raise ValueError("admission-attempt mode must be canary or production")
    entries = manifest.get("entries")
    order = manifest.get("candidate_order")
    if not isinstance(entries, list) or order != [entry.get("candidate_id") for entry in entries if isinstance(entry, dict)]:
        raise ValueError("authoritative manifest candidate population is invalid")
    return [entry for entry in entries if mode == "production" or entry.get("canary") is True]


def _normalized_reruns(reruns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(reruns, list):
        raise ValueError("deterministic reruns must be a list")
    keys = ("candidate_id", "matched", "first_fingerprint", "second_fingerprint")
    rows = []
    for row in reruns:
        if not isinstance(row, dict) or any(key not in row for key in keys):
            raise ValueError("deterministic rerun binding is incomplete")
        rows.append({key: copy.deepcopy(row[key]) for key in keys})
    return rows


def _preliminary_decision(
    mode: str,
    selected: list[dict[str, Any]],
    outcomes: list[dict[str, Any]],
    reruns: list[dict[str, Any]],
    blockers: list[str],
    packages: list[dict[str, Any]],
    views: list[dict[str, Any]],
) -> str:
    outcome_by_id = {row.get("candidate_id"): row for row in outcomes if isinstance(row, dict)}
    executable = [entry for entry in selected if entry.get("disposition") == "execute"]
    valid_count = sum(outcome_by_id.get(entry.get("candidate_id"), {}).get("disposition") == "valid" for entry in executable)
    required_valid = 1 if mode == "canary" else 2
    rerun_ok = len(reruns) == len(executable) and all(row.get("matched") is True for row in reruns)
    proposal_ok = len(packages) == required_valid and len(views) == required_valid * 28
    return "admit" if not blockers and valid_count == required_valid and len(executable) == required_valid and rerun_ok and proposal_ok else "reject"


def build_admission_attempt(
    *,
    manifest: dict[str, Any],
    manifest_byte_fingerprint: str,
    manifest_identity_kind: str,
    mode: str,
    outcomes: list[dict[str, Any]],
    reruns: list[dict[str, Any]],
    blockers: list[str],
    packages: list[dict[str, Any]],
    views: list[dict[str, Any]],
    profile_id: Any = PROFILE_ID,
) -> dict[str, Any]:
    """Build and validate one deterministic live admission-attempt envelope."""
    _require_profile(profile_id)
    if not isinstance(manifest, dict):
        raise ValueError("admission-attempt manifest must be an object")
    if manifest_identity_kind not in MANIFEST_IDENTITY_KINDS:
        raise ValueError("admission-attempt manifest identity kind is unsupported")
    selected = _selected_entries(manifest, mode)
    if not isinstance(outcomes, list) or not isinstance(blockers, list) or not isinstance(packages, list) or not isinstance(views, list):
        raise ValueError("admission-attempt populations must be lists")
    normalized_reruns = _normalized_reruns(reruns)
    selected_ids = [entry["candidate_id"] for entry in selected]
    selected_set = set(selected_ids)
    unevaluated_ids = [entry["candidate_id"] for entry in manifest["entries"] if entry["candidate_id"] not in selected_set]
    proposal_state = "constructed" if packages or views else "withheld"
    envelope: dict[str, Any] = {
        "schema_name": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "profile_id": PROFILE_ID,
        "mode": mode,
        "manifest": copy.deepcopy(manifest),
        "manifest_fingerprint": manifest.get("manifest_fingerprint"),
        "manifest_byte_fingerprint": manifest_byte_fingerprint,
        "manifest_identity_kind": manifest_identity_kind,
        "evaluated_candidate_ids": selected_ids,
        "unevaluated_candidate_ids": unevaluated_ids,
        "outcomes": copy.deepcopy(outcomes),
        "reruns": normalized_reruns,
        "blockers": copy.deepcopy(blockers),
        "proposal_state": proposal_state,
        "packages": copy.deepcopy(packages),
        "package_fingerprints": [fingerprint(package) for package in packages],
        "result_fingerprints": [fingerprint(outcome) for outcome in outcomes],
        "views": copy.deepcopy(views),
        "view_fingerprints": [view.get("view_fingerprint") for view in views],
        "decision": _preliminary_decision(mode, selected, outcomes, normalized_reruns, blockers, packages, views),
    }
    envelope["attempt_fingerprint"] = fingerprint(envelope)
    validate_admission_attempt(
        envelope,
        expected_manifest=manifest,
        expected_manifest_byte_fingerprint=manifest_byte_fingerprint,
        expected_manifest_identity_kind=manifest_identity_kind,
    )
    return envelope


def _validate_outcomes(
    envelope: dict[str, Any],
    selected: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    outcomes = envelope["outcomes"]
    if not isinstance(outcomes, list):
        raise ValueError("admission-attempt outcomes must be a list")
    selected_ids = [entry["candidate_id"] for entry in selected]
    outcome_ids = [row.get("candidate_id") for row in outcomes if isinstance(row, dict)]
    if len(outcome_ids) != len(outcomes) or outcome_ids != selected_ids or len(outcome_ids) != len(set(outcome_ids)):
        raise ValueError("admission-attempt outcome population does not equal evaluated scope")
    outcome_by_id = {row["candidate_id"]: row for row in outcomes}
    executable: list[dict[str, Any]] = []
    for entry in selected:
        outcome = outcome_by_id[entry["candidate_id"]]
        if entry.get("disposition") != "execute":
            if outcome.get("disposition") != "rejected" or outcome.get("stage") != "pre_execution":
                raise ValueError("pre-execution exclusion outcome is contradictory")
            if outcome.get("result_records") not in (None, []) or int(outcome.get("raw_result_count", 0)) != 0:
                raise ValueError("pre-execution exclusion cannot carry results")
            continue
        executable.append(entry)
        disposition = outcome.get("disposition")
        if disposition not in {"valid", "null", "rejected", "failed"}:
            raise ValueError("executable outcome disposition is unsupported")
        records = outcome.get("result_records")
        if disposition == "valid":
            if not isinstance(records, list) or len(records) != 28:
                raise ValueError("valid outcome must contain exactly 28 result records")
            if outcome.get("stage") is not None:
                raise ValueError("valid outcome cannot carry a failure stage")
            if outcome.get("raw_result_count") != len(records) or outcome.get("valid_result_count") != len(records):
                raise ValueError("valid outcome result cardinality mismatch")
        else:
            if outcome.get("stage") not in NEGATIVE_STAGE_BY_DISPOSITION[disposition]:
                raise ValueError("negative executable outcome disposition/stage transition is not emitted by this owner")
            if records not in (None, []) or int(outcome.get("raw_result_count", 0)) != 0 or int(outcome.get("valid_result_count", 0)) != 0:
                raise ValueError("negative executable outcome cannot carry result records")
    return outcome_by_id, executable


def _validate_reruns(envelope: dict[str, Any], executable: list[dict[str, Any]], outcome_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    reruns = envelope["reruns"]
    if not isinstance(reruns, list):
        raise ValueError("deterministic rerun population must be a list")
    expected_ids = [entry["candidate_id"] for entry in executable]
    ids = [row.get("candidate_id") for row in reruns if isinstance(row, dict)]
    exact_fields = {"candidate_id", "matched", "first_fingerprint", "second_fingerprint"}
    if ids != expected_ids or len(ids) != len(set(ids)) or any(not isinstance(row, dict) or set(row) != exact_fields for row in reruns):
        raise ValueError("deterministic rerun population does not equal evaluated executable scope")
    for row in reruns:
        first = row["first_fingerprint"]
        second = row["second_fingerprint"]
        if type(row["matched"]) is not bool or not isinstance(first, str) or not isinstance(second, str) or _SHA256.fullmatch(first) is None or _SHA256.fullmatch(second) is None:
            raise ValueError("deterministic rerun fingerprint binding is malformed")
        if row["matched"] != (first == second) or first != fingerprint(outcome_by_id[row["candidate_id"]]):
            raise ValueError("deterministic rerun fingerprint binding is stale or contradictory")
    return reruns


def _package_result_records(package: dict[str, Any]) -> list[dict[str, Any]]:
    records = package.get("generated_statements", [{}])[0].get("structured_payload", {}).get("result_records")
    if not isinstance(records, list):
        raise ValueError("package result population is missing")
    return records


def _validate_package_entry_binding(
    entry: dict[str, Any],
    outcome: dict[str, Any],
    package: dict[str, Any],
    manifest_fingerprint: str,
    expected_package_id: str | None,
) -> None:
    if expected_package_id is not None and package.get("package_id") != expected_package_id:
        raise ValueError("package identity does not match manifest candidate")
    identity = entry.get("identity_inputs", {})
    territory = entry.get("territory", {})
    applicability = entry.get("applicability", {})
    indicator = entry.get("indicator", {})
    source_scope = package.get("scope", {}).get("source_scope", {})
    expected_source = {
        "campaign_id": entry.get("campaign_id"),
        "indicator_code": indicator.get("code"),
        "indicator_name": indicator.get("name"),
        "entity_id": territory.get("id"),
        "entity_name": territory.get("name"),
        "period_start": identity.get("period_start"),
        "period_end": identity.get("period_end"),
        "frequency": applicability.get("frequency"),
        "unit": applicability.get("unit"),
        "denominator_basis": applicability.get("denominator_basis"),
        "observational_population": territory.get("observational_population"),
    }
    if any(not _json_equal(source_scope.get(key), value) for key, value in expected_source.items()):
        raise ValueError("package source scope does not match manifest candidate")
    method = entry.get("method", {})
    if package.get("scope", {}).get("method_scope") != f"{method.get('id')}@{method.get('version')}":
        raise ValueError("package method scope does not match manifest candidate")
    input_binding = entry.get("input", {})
    if not _json_equal(package.get("input_references"), [input_binding.get("normalized_fingerprint")]):
        raise ValueError("package input reference does not match manifest candidate")
    computation = package.get("computation_method", {})
    if not _json_equal(computation.get("name"), method.get("id")) or not _json_equal(computation.get("version"), method.get("version")) or not _json_equal(computation.get("parameters"), method.get("parameters")):
        raise ValueError("package computation method does not match manifest candidate")
    evidence = package.get("evidence_references")
    if not isinstance(evidence, list) or len(evidence) != 1 or evidence[0].get("snapshot_fingerprint") != input_binding.get("sha256") or evidence[0].get("reproducibility_handle") != input_binding.get("path"):
        raise ValueError("package evidence reference does not match manifest candidate")
    statements = package.get("generated_statements")
    if not isinstance(statements, list) or len(statements) != 1:
        raise ValueError("package statement population does not match manifest candidate")
    statement = statements[0]
    payload = statement.get("structured_payload", {})
    if not _json_equal(statement.get("applicability"), applicability) or not _json_equal(payload.get("calculation_fingerprint"), outcome.get("calculation_fingerprint")) or not _json_equal(payload.get("manifest_fingerprint"), manifest_fingerprint) or not _json_equal(payload.get("indicator_definition"), indicator.get("definition")):
        raise ValueError("package statement binding does not match manifest candidate")
    provenance = package.get("provenance_envelope", {})
    if provenance.get("package_identity") != package.get("package_id") or provenance.get("input_file_sha256") != input_binding.get("sha256") or provenance.get("normalized_evidence_fingerprint") != input_binding.get("normalized_fingerprint") or provenance.get("selection_manifest_fingerprint") != manifest_fingerprint:
        raise ValueError("package provenance does not match manifest candidate")
    if expected_package_id is not None:
        candidate_package_id = expected_package_id.replace("pkg-object-", "pkg-candidate-")
        if package.get("promotion", {}).get("from_candidate_package_id") != candidate_package_id or package.get("lineage", {}).get("previous_package_id") != candidate_package_id:
            raise ValueError("package promotion lineage does not match manifest candidate")


def _validate_proposal(
    envelope: dict[str, Any],
    selected: list[dict[str, Any]],
    outcome_by_id: dict[str, dict[str, Any]],
    expected_package_ids: dict[str, str] | None,
    expected_result_ids: dict[str, list[str]] | None,
    expected_view_ids: dict[str, str] | None,
) -> None:
    packages = envelope["packages"]
    views = envelope["views"]
    if not isinstance(packages, list) or not isinstance(views, list):
        raise ValueError("package and view populations must be lists")
    proposal_state = envelope.get("proposal_state")
    if proposal_state not in {"constructed", "withheld"}:
        raise ValueError("proposal state must be constructed or withheld")
    if proposal_state == "withheld":
        if packages or views:
            raise ValueError("rejected attempt with withheld proposal cannot carry packages or views")
        if envelope["package_fingerprints"] != [] or envelope["view_fingerprints"] != []:
            raise ValueError("withheld proposal cannot carry package or view fingerprints")
        return
    if not packages:
        raise ValueError("constructed proposal must contain packages")
    expected_entries = [entry for entry in selected if outcome_by_id[entry["candidate_id"]].get("disposition") == "valid"]
    expected_codes = [entry.get("indicator", {}).get("code") for entry in expected_entries]
    package_codes = [package.get("scope", {}).get("source_scope", {}).get("indicator_code") for package in packages if isinstance(package, dict)]
    package_ids = [package.get("package_id") for package in packages if isinstance(package, dict)]
    if len(package_ids) != len(packages) or package_codes != expected_codes:
        raise ValueError("package population does not equal valid evaluated outcomes")
    if not envelope["blockers"] and len(package_ids) != len(set(package_ids)):
        raise ValueError("admissible package population contains duplicate identities")
    expected_package_fingerprints = [fingerprint(package) for package in packages]
    if envelope.get("package_fingerprints") != expected_package_fingerprints:
        raise ValueError("package fingerprint population is stale or tampered")
    expected_view_rows: list[tuple[dict[str, Any], str]] = []
    for entry, package in zip(expected_entries, packages):
        expected_package_id = expected_package_ids.get(entry["candidate_id"]) if expected_package_ids is not None else None
        _validate_package_entry_binding(
            entry, outcome_by_id[entry["candidate_id"]], package,
            envelope["manifest_fingerprint"], expected_package_id,
        )
        validation = validate_knowledge_object(package)
        if validation.get("blockers"):
            raise ValueError("package validation failed inside admission attempt")
        outcome_records = outcome_by_id[entry["candidate_id"]]["result_records"]
        package_records = _package_result_records(package)
        if not _json_equal(package_records, outcome_records):
            raise ValueError("package records do not exactly match valid outcome")
        if package.get("provenance_envelope", {}).get("selection_manifest_fingerprint") != envelope["manifest_fingerprint"]:
            raise ValueError("package manifest lineage does not match admission attempt")
        observed_result_ids: list[str] = []
        for record in package_records:
            result_id = record.get("result_id") if isinstance(record, dict) else None
            if not isinstance(result_id, str):
                raise ValueError("package result identity is missing")
            observed_result_ids.append(result_id)
            expected_view_rows.append((record, package["package_id"]))
        if expected_result_ids is not None and observed_result_ids != expected_result_ids[entry["candidate_id"]]:
            raise ValueError("package result identity population does not match owner-derived identities")
    view_ids = [view.get("view_id") for view in views if isinstance(view, dict)]
    view_result_ids = [view.get("result_record_id") for view in views if isinstance(view, dict)]
    if len(view_ids) != len(views) or len(views) != len(expected_view_rows):
        raise ValueError("view population does not exactly cover package result records")
    if not envelope["blockers"] and (len(view_ids) != len(set(view_ids)) or len(view_result_ids) != len(set(view_result_ids))):
        raise ValueError("admissible view population contains duplicate identities")
    expected_view_fingerprints = []
    for view, (record, package_id) in zip(views, expected_view_rows):
        expected = fingerprint({key: value for key, value in view.items() if key != "view_fingerprint"})
        if view.get("view_fingerprint") != expected:
            raise ValueError("view fingerprint is stale or tampered")
        result_id = record.get("result_id")
        if not isinstance(result_id, str):
            raise ValueError("package result identity is missing")
        if expected_view_ids is not None and view.get("view_id") != expected_view_ids[result_id]:
            raise ValueError("view identity does not match owner-derived identity")
        if not _json_equal(view.get("result_record_id"), result_id) or not _json_equal(view.get("canonical_package_id"), package_id) or any(not _json_equal(view.get(key), record.get(key)) for key in ("class", "metric", "value")):
            raise ValueError("view population is detached from package result semantics")
        expected_view_fingerprints.append(expected)
    if envelope.get("view_fingerprints") != expected_view_fingerprints:
        raise ValueError("view fingerprint population is stale or tampered")


def validate_admission_attempt(
    envelope: Any,
    *,
    expected_manifest: dict[str, Any] | None = None,
    expected_manifest_byte_fingerprint: str | None = None,
    expected_manifest_identity_kind: str | None = None,
    expected_package_ids: dict[str, str] | None = None,
    expected_result_ids: dict[str, list[str]] | None = None,
    expected_view_ids: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Validate structure and derive admission authorization independently."""
    if not isinstance(envelope, dict) or set(envelope) != _FIELDS:
        raise ValueError("admission-attempt envelope fields are incomplete or unexpected")
    if envelope.get("schema_name") != SCHEMA_NAME or envelope.get("schema_version") != SCHEMA_VERSION or envelope.get("profile_id") != PROFILE_ID:
        raise ValueError("admission-attempt schema/version/profile identity mismatch")
    expected_attempt_fingerprint = fingerprint({key: value for key, value in envelope.items() if key != "attempt_fingerprint"})
    if envelope.get("attempt_fingerprint") != expected_attempt_fingerprint:
        raise ValueError("admission-attempt fingerprint mismatch")
    manifest = envelope.get("manifest")
    if not isinstance(manifest, dict) or manifest.get("manifest_fingerprint") != _manifest_fingerprint(manifest):
        raise ValueError("admission-attempt manifest fingerprint mismatch")
    if envelope.get("manifest_fingerprint") != manifest["manifest_fingerprint"]:
        raise ValueError("admission-attempt manifest identity binding mismatch")
    byte_fingerprint = envelope.get("manifest_byte_fingerprint")
    if not isinstance(byte_fingerprint, str) or _SHA256.fullmatch(byte_fingerprint) is None:
        raise ValueError("admission-attempt manifest byte fingerprint is malformed")
    identity_kind = envelope.get("manifest_identity_kind")
    if identity_kind not in MANIFEST_IDENTITY_KINDS:
        raise ValueError("admission-attempt manifest identity kind is unsupported")
    if expected_manifest_identity_kind is not None and identity_kind != expected_manifest_identity_kind:
        raise ValueError("admission-attempt manifest identity kind does not match invocation")
    if expected_manifest is not None and not _json_equal(manifest, expected_manifest):
        raise ValueError("admission-attempt does not match expected manifest")
    if expected_manifest_byte_fingerprint is not None and byte_fingerprint != expected_manifest_byte_fingerprint:
        raise ValueError("admission-attempt manifest byte fingerprint does not match invocation")
    mode = envelope.get("mode")
    selected = _selected_entries(manifest, mode)
    selected_ids = [entry["candidate_id"] for entry in selected]
    selected_set = set(selected_ids)
    unevaluated_ids = [entry["candidate_id"] for entry in manifest["entries"] if entry["candidate_id"] not in selected_set]
    if envelope.get("evaluated_candidate_ids") != selected_ids or envelope.get("unevaluated_candidate_ids") != unevaluated_ids:
        raise ValueError("evaluated candidate scope does not match manifest and mode")
    outcome_by_id, executable = _validate_outcomes(envelope, selected)
    if expected_package_ids is not None:
        expected_identity_keys = {entry["candidate_id"] for entry in executable}
        if set(expected_package_ids) != expected_identity_keys or any(not isinstance(value, str) or not value for value in expected_package_ids.values()):
            raise ValueError("owner-derived package identity population is incomplete or malformed")
    if (expected_result_ids is None) != (expected_view_ids is None):
        raise ValueError("owner-derived result and view identity contexts must be supplied together")
    if expected_result_ids is not None and expected_view_ids is not None:
        executable_keys = {entry["candidate_id"] for entry in executable}
        if set(expected_result_ids) != executable_keys or any(not isinstance(values, list) or any(not isinstance(value, str) or not value for value in values) for values in expected_result_ids.values()):
            raise ValueError("owner-derived result identity population is incomplete or malformed")
        flattened_result_ids = [value for entry in executable for value in expected_result_ids[entry["candidate_id"]]]
        if len(flattened_result_ids) != len(set(flattened_result_ids)) or set(expected_view_ids) != set(flattened_result_ids) or any(not isinstance(value, str) or not value for value in expected_view_ids.values()):
            raise ValueError("owner-derived view identity population is incomplete or malformed")
    expected_result_fingerprints = [fingerprint(outcome) for outcome in envelope["outcomes"]]
    if envelope.get("result_fingerprints") != expected_result_fingerprints:
        raise ValueError("result fingerprint population is stale or tampered")
    reruns = _validate_reruns(envelope, executable, outcome_by_id)
    blockers = envelope.get("blockers")
    if not isinstance(blockers, list) or any(not isinstance(value, str) or not value for value in blockers):
        raise ValueError("admission-attempt blockers must be nonempty strings")
    _validate_proposal(envelope, selected, outcome_by_id, expected_package_ids, expected_result_ids, expected_view_ids)
    expected_decision = _preliminary_decision(mode, selected, envelope["outcomes"], reruns, blockers, envelope["packages"], envelope["views"])
    if envelope.get("decision") != expected_decision:
        raise ValueError("admission-attempt derived decision mismatch")
    if expected_decision == "admit" and envelope.get("proposal_state") != "constructed":
        raise ValueError("admitted attempt requires a constructed proposal")
    return {
        "valid": True,
        "profile_id": PROFILE_ID,
        "attempt_fingerprint": envelope["attempt_fingerprint"],
        "decision": expected_decision,
        "admission_authorized": expected_decision == "admit" and expected_package_ids is not None and expected_result_ids is not None and expected_view_ids is not None,
        "package_fingerprints": copy.deepcopy(envelope["package_fingerprints"]),
    }


def dispatch_validate_admission_attempt(
    profile_id: Any,
    envelope: Any,
    *,
    expected_manifest: dict[str, Any] | None = None,
    expected_manifest_byte_fingerprint: str | None = None,
    expected_manifest_identity_kind: str | None = None,
    expected_package_ids: dict[str, str] | None = None,
    expected_result_ids: dict[str, list[str]] | None = None,
    expected_view_ids: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Closed exact-version dispatcher; no aliases, ranges or fallbacks."""
    _require_profile(profile_id)
    if expected_package_ids is None:
        raise ValueError("owner-derived package identity context is required for admission authorization")
    return validate_admission_attempt(
        envelope,
        expected_manifest=expected_manifest,
        expected_manifest_byte_fingerprint=expected_manifest_byte_fingerprint,
        expected_manifest_identity_kind=expected_manifest_identity_kind,
        expected_package_ids=expected_package_ids,
        expected_result_ids=expected_result_ids,
        expected_view_ids=expected_view_ids,
    )
