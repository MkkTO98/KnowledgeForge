#!/usr/bin/env python3
"""Prospective Evidence Portfolio conformance profile v1.

This module adapts immutable historical portfolio surfaces into a separate,
version-governed conformance envelope.  It never writes canonical state and it
does not reinterpret or recalculate evidence values.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

SCHEMA_NAME = "knowledgeforge.evidence_portfolio.conformance.v1"
SCHEMA_VERSION = "1.0"
PROFILE_ID = f"{SCHEMA_NAME}@{SCHEMA_VERSION}"
TERMINAL_DISPOSITIONS = {
    "valid",
    "excluded_pre_execution",
    "rejected_execution",
    "null",
    "redundant_candidate",
    "execution_failure",
}
RELATIONS = {"supports", "weakens", "qualifies", "excludes", "absence"}
DEPENDENCE_STATUSES = {"known", "unresolved"}
TRANSFORMATION_DEFINITIONS = {
    "level": {
        "transformation_id": "level",
        "operation": "identity",
        "parameters": {},
    },
    "adjacent_first_difference": {
        "transformation_id": "adjacent_first_difference",
        "operation": "difference",
        "parameters": {
            "adjacency": "consecutive_retained_periods",
            "frequency": "annual",
            "order": 1,
        },
    },
    "linear_time_index_slope": {
        "transformation_id": "linear_time_index_slope",
        "operation": "ordinary_least_squares_slope",
        "parameters": {
            "independent_variable": "integer_calendar_year",
            "role": "descriptor_only",
        },
    },
}
_REQUIRED_TRANSFORMATIONS = tuple(TRANSFORMATION_DEFINITIONS)
_DEPENDENCE_FIELDS = {
    "candidate_id",
    "source_series_cluster_id",
    "provider_basis",
    "provider_cluster_id",
    "acquisition_basis",
    "acquisition_cluster_id",
    "method_basis",
    "method_cluster_ids",
    "dependence_status",
}
_ENVELOPE_FIELDS = {
    "schema_name", "schema_version", "profile_id", "portfolio_id", "portfolio_label", "adaptation_kind",
    "historical_representation", "questions", "candidates", "candidate_outcomes", "candidate_links",
    "transformations", "evidence_units", "dependence_declarations", "preserved_conclusion",
    "preserved_conclusion_fingerprint", "structural_differences", "generality_boundary", "accounting",
    "candidate_ledger_markdown", "conformance_fingerprint",
}
_CANDIDATE_FIELDS = {"candidate_id", "planned_disposition", "source_series_identity", "method_identity", "declared_transformations", "exclusion_reason"}
_OUTCOME_FIELDS = {"candidate_id", "planned_disposition", "historical_disposition", "terminal_disposition", "raw_result_count", "valid_result_count", "redundant_result_count"}
_LINK_FIELDS = {"question_id", "question_scope_fingerprint", "candidate_id", "source_candidate_fingerprint", "direction", "relation", "reason", "evidence_unit_ids"}
_TRANSFORMATION_FIELDS = {"candidate_id", "base_series_identity", "transformation_id", "operation", "parameters", "transformation_identity"}
_EVIDENCE_FIELDS = {
    "evidence_unit_id", "candidate_id", "question_id", "historical_package_id", "historical_package_fingerprint",
    "historical_result_id", "historical_result_fingerprint", "historical_result_semantic_fingerprint",
    "historical_view_id", "historical_view_fingerprint", "source_series_identity", "transformation_id",
    "transformation_identity", "provenance_fingerprint",
}
_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9._:-]*")
_RELATION_BY_TERMINAL = {
    "valid": "supports",
    "excluded_pre_execution": "excludes",
    "null": "absence",
    "rejected_execution": "absence",
    "execution_failure": "absence",
    "redundant_candidate": "absence",
}
_REASON_BY_TERMINAL = {
    "valid": "candidate admitted and produced retained bounded descriptive result records",
    "null": "candidate executed but produced no retained result",
    "rejected_execution": "candidate was rejected during or after execution",
    "execution_failure": "candidate execution failed",
    "redundant_candidate": "candidate produced no distinct retained evidence",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def pretty_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("portfolio label does not produce a stable identifier")
    return slug


def text_sha256(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("text identity input must be a string")
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def extract_report_section(source_report_text: str, heading: str) -> str:
    if not isinstance(source_report_text, str) or not isinstance(heading, str) or not heading.startswith("## "):
        raise ValueError("source report text and level-two conclusion heading are required")
    marker = heading + "\n"
    if source_report_text.count(marker) != 1:
        raise ValueError("conclusion heading must resolve exactly once in source report")
    body = source_report_text.split(marker, 1)[1]
    next_heading = body.find("\n## ")
    if next_heading >= 0:
        body = body[:next_heading]
    section = body.strip()
    if not section:
        raise ValueError("published conclusion section is empty")
    return section


def transformation_identity(base_series_identity: str, definition: dict[str, Any]) -> str:
    if not isinstance(base_series_identity, str) or not base_series_identity:
        raise ValueError("transformation base-series identity must be nonempty")
    _validate_transformation_shape(definition)
    return fingerprint({"base_series_identity": base_series_identity, "definition": definition})


def _validate_transformation_shape(definition: Any) -> None:
    if not isinstance(definition, dict) or set(definition) != {"transformation_id", "operation", "parameters"}:
        raise ValueError("transformation definition must contain exact identity, operation and parameters")
    if not isinstance(definition.get("transformation_id"), str) or not definition["transformation_id"]:
        raise ValueError("transformation identifier must be nonempty")
    if not isinstance(definition.get("operation"), str) or not definition["operation"]:
        raise ValueError("transformation operation must be nonempty")
    if not isinstance(definition.get("parameters"), dict):
        raise ValueError("transformation parameters must be an object")


def _validate_transformation_definition(definition: Any) -> None:
    _validate_transformation_shape(definition)
    transformation_id = definition.get("transformation_id")
    expected = TRANSFORMATION_DEFINITIONS.get(transformation_id)
    if expected is None:
        raise ValueError("transformation alias or unsupported transformation identity")
    if definition != expected:
        raise ValueError("transformation definition or required parameters are incomplete or contradictory")


def _record_transformation(record: Any) -> str:
    if not isinstance(record, dict):
        raise ValueError("historical result record must be an object")
    historical = record.get("transformation")
    mapping = {
        "level": "level",
        "adjacent_first_difference": "adjacent_first_difference",
        "linear_time_index": "linear_time_index_slope",
    }
    if historical not in mapping:
        raise ValueError("historical result transformation is unknown or unsupported")
    metric = record.get("metric")
    if not isinstance(metric, str) or not metric:
        raise ValueError("historical result metric is missing")
    if historical == "level" and ("difference" in metric or metric.startswith("linear_time_index")):
        raise ValueError("historical result metric contradicts level transformation")
    if historical == "adjacent_first_difference" and "difference" not in metric:
        raise ValueError("historical result metric contradicts difference transformation")
    if historical == "linear_time_index" and not metric.startswith("linear_time_index_slope"):
        raise ValueError("historical result metric contradicts slope transformation")
    return mapping[historical]


def _manifest_semantic_fingerprint(manifest: dict[str, Any]) -> str:
    return fingerprint({key: value for key, value in manifest.items() if key != "manifest_fingerprint"})


def _question_scope_fingerprint(question: dict[str, Any]) -> str:
    return fingerprint({key: value for key, value in question.items() if key != "scope_fingerprint"})


def _cluster(prefix: str, value: Any) -> str:
    return f"{prefix}-" + fingerprint(value).split(":", 1)[1][:24]


def classify_terminal_disposition(entry: dict[str, Any], outcome: dict[str, Any]) -> str:
    planned = entry.get("disposition")
    historical = outcome.get("disposition")
    if planned == "excluded_pre_execution":
        if outcome.get("stage") != "pre_execution" or historical != "rejected":
            raise ValueError("historical exclusion is contradictory or incomplete")
        return "excluded_pre_execution"
    if planned != "execute":
        raise ValueError("historical planned disposition is unsupported")
    mapping = {
        "valid": "valid",
        "null": "null",
        "rejected": "rejected_execution",
        "failed": "execution_failure",
        "redundant": "redundant_candidate",
    }
    if historical not in mapping:
        raise ValueError("historical execution disposition is unsupported")
    terminal = mapping[historical]
    if terminal in {"rejected_execution", "execution_failure"} and outcome.get("stage") not in {"execution", "post_execution_validation"}:
        raise ValueError("runtime negative outcome must identify an execution or post-execution stage")
    if terminal in {"valid", "null", "redundant_candidate"} and outcome.get("stage") == "pre_execution":
        raise ValueError("executed candidate cannot carry a pre-execution stage")
    return terminal


def _source_series_identity(entry: dict[str, Any]) -> str:
    normalized = entry.get("input", {}).get("normalized_fingerprint")
    if not isinstance(normalized, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", normalized) is None:
        raise ValueError("candidate source-series normalized fingerprint is invalid")
    return f"source-series:{normalized}"


def _entry_package(entry: dict[str, Any], packages: list[dict[str, Any]]) -> dict[str, Any] | None:
    code = entry.get("indicator", {}).get("code")
    matches = [package for package in packages if package.get("scope", {}).get("source_scope", {}).get("indicator_code") == code]
    if entry.get("disposition") == "execute" and len(matches) != 1:
        raise ValueError("executable historical candidate must resolve to exactly one package")
    if entry.get("disposition") != "execute" and matches:
        return None
    return matches[0] if matches else None


def _ledger_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", "<br>")


def _render_candidate_ledger(envelope: dict[str, Any]) -> str:
    links = {row["candidate_id"]: row for row in envelope["candidate_links"]}
    outcomes = {row["candidate_id"]: row for row in envelope["candidate_outcomes"]}
    lines = [
        "<!-- KNOWLEDGEFORGE:EVIDENCE-PORTFOLIO-CONFORMANCE-V1:BEGIN -->",
        "| Candidate | Planned | Terminal | Relation | Question | Evidence units | Reason |",
        "| --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for candidate in envelope["candidates"]:
        candidate_id = candidate["candidate_id"]
        link = links[candidate_id]
        outcome = outcomes[candidate_id]
        reason = _ledger_cell(link["reason"])
        lines.append(
            f"| `{_ledger_cell(candidate_id)}` | `{_ledger_cell(candidate['planned_disposition'])}` | "
            f"`{_ledger_cell(outcome['terminal_disposition'])}` | `{_ledger_cell(link['relation'])}` | "
            f"`{_ledger_cell(link['question_id'])}` | {len(link['evidence_unit_ids'])} | {reason} |"
        )
    lines.append("<!-- KNOWLEDGEFORGE:EVIDENCE-PORTFOLIO-CONFORMANCE-V1:END -->")
    return "\n".join(lines) + "\n"


def derive_accounting(envelope: dict[str, Any]) -> dict[str, Any]:
    outcomes = envelope["candidate_outcomes"]
    dispositions = [row["terminal_disposition"] for row in outcomes]
    executed = [row for row in outcomes if row["terminal_disposition"] != "excluded_pre_execution"]
    dependence = envelope["dependence_declarations"]
    shared_groups = {
        (
            row["provider_cluster_id"],
            row["acquisition_cluster_id"],
            tuple(row["method_cluster_ids"]),
        )
        for row in dependence
    }
    raw = sum(row["raw_result_count"] for row in outcomes)
    valid = sum(row["valid_result_count"] for row in outcomes)
    redundant_records = sum(row["redundant_result_count"] for row in outcomes)
    return {
        "manifest_candidates": len(outcomes),
        "excluded_pre_execution": dispositions.count("excluded_pre_execution"),
        "executed_candidates": len(executed),
        "valid_candidates": dispositions.count("valid"),
        "rejected_execution": dispositions.count("rejected_execution"),
        "null_candidates": dispositions.count("null"),
        "redundant_candidates": dispositions.count("redundant_candidate"),
        "execution_failures": dispositions.count("execution_failure"),
        "raw_result_records": raw,
        "valid_result_records": valid,
        "redundant_result_records": redundant_records,
        "referenced_historical_packages": len(envelope["historical_representation"]["package_fingerprints"]),
        "referenced_operational_views": len(envelope["historical_representation"]["view_fingerprints"]),
        "record_diversity": {
            "valid_result_records": len(envelope["evidence_units"]),
            "transformation_definitions": len({row["transformation_id"] for row in envelope["transformations"]}),
            "transformed_series_variants": len({row["transformation_identity"] for row in envelope["evidence_units"]}),
        },
        "support_diversity": {
            "distinct_evidence_candidates": len(dependence),
            "source_series_clusters": len({row["source_series_cluster_id"] for row in dependence}),
            "provider_clusters": len({row["provider_cluster_id"] for row in dependence}),
            "acquisition_clusters": len({row["acquisition_cluster_id"] for row in dependence}),
            "method_clusters": len({item for row in dependence for item in row["method_cluster_ids"]}),
            "shared_support_groups": len(shared_groups),
            "fully_independent_support_claims": 0,
        },
        "reconciliation": {
            "manifest_equals_excluded_plus_executed": len(outcomes) == dispositions.count("excluded_pre_execution") + len(executed),
            "executed_equals_terminal_execution_categories": len(executed) == sum(dispositions.count(value) for value in TERMINAL_DISPOSITIONS - {"excluded_pre_execution"}),
            "raw_equals_valid_plus_redundant": raw == valid + redundant_records,
        },
    }


def build_historical_conformance_envelope(
    *,
    manifest: dict[str, Any],
    execution_results: dict[str, Any],
    packages: list[dict[str, Any]],
    views: list[dict[str, Any]],
    portfolio_label: str,
    question: str,
    intended_use: str,
    prohibited_uses: list[str],
    source_report_path: str,
    source_report_text: str,
    conclusion_heading: str,
) -> dict[str, Any]:
    """Build a corrected representation without changing historical inputs."""
    if not isinstance(manifest, dict) or manifest.get("manifest_fingerprint") != _manifest_semantic_fingerprint(manifest):
        raise ValueError("historical manifest fingerprint mismatch")
    if not isinstance(execution_results, dict) or not isinstance(execution_results.get("outcomes"), list):
        raise ValueError("historical execution results are incomplete")
    if not isinstance(packages, list) or not isinstance(views, list):
        raise ValueError("historical packages and views must be lists")
    if not all(isinstance(value, str) and value for value in [portfolio_label, question, intended_use]):
        raise ValueError("portfolio label and question scope must be nonempty")
    if not isinstance(prohibited_uses, list) or not prohibited_uses or any(not isinstance(value, str) or not value for value in prohibited_uses):
        raise ValueError("question prohibited uses must be a nonempty string list")
    if not isinstance(source_report_path, str) or not source_report_path or source_report_path.startswith("/") or ".." in source_report_path.split("/"):
        raise ValueError("source report path must be a nonempty repository-relative path")
    conclusion_text = extract_report_section(source_report_text, conclusion_heading)
    conclusion = {
        "source_report": source_report_path,
        "source_report_text": source_report_text,
        "source_report_sha256": text_sha256(source_report_text),
        "conclusion_heading": conclusion_heading,
        "text": conclusion_text,
        "text_sha256": text_sha256(conclusion_text),
    }

    entries = manifest.get("entries")
    order = manifest.get("candidate_order")
    if not isinstance(entries, list) or order != [entry.get("candidate_id") for entry in entries]:
        raise ValueError("historical manifest candidate population is inconsistent")
    historical_outcomes = execution_results["outcomes"]
    outcome_ids = [row.get("candidate_id") for row in historical_outcomes if isinstance(row, dict)]
    if len(outcome_ids) != len(set(outcome_ids)) or set(outcome_ids) != set(order):
        raise ValueError("historical outcome population does not reconcile to manifest")
    outcome_by_id = {row["candidate_id"]: row for row in historical_outcomes}

    executable_entries = [entry for entry in entries if entry.get("disposition") == "execute"]
    executable_codes = [entry.get("indicator", {}).get("code") for entry in executable_entries]
    package_ids = [package.get("package_id") for package in packages if isinstance(package, dict)]
    package_codes = [package.get("scope", {}).get("source_scope", {}).get("indicator_code") for package in packages if isinstance(package, dict)]
    if len(package_ids) != len(packages) or len(package_ids) != len(set(package_ids)) or sorted(package_codes) != sorted(executable_codes):
        raise ValueError("historical package population must cover executable candidates exactly once")
    view_ids = [view.get("view_id") for view in views if isinstance(view, dict)]
    view_result_ids = [view.get("result_record_id") for view in views if isinstance(view, dict)]
    if len(view_ids) != len(views) or len(view_ids) != len(set(view_ids)) or len(view_result_ids) != len(set(view_result_ids)):
        raise ValueError("historical operational views must have unique view and result identities")
    expected_result_ids: set[str] = set()
    for entry in executable_entries:
        outcome = outcome_by_id[entry["candidate_id"]]
        result_records = outcome.get("result_records")
        if outcome.get("disposition") == "valid" and not isinstance(result_records, list):
            raise ValueError("valid historical outcome must include exact result records")
        if isinstance(result_records, list):
            ids = [record.get("result_id") for record in result_records if isinstance(record, dict)]
            if len(ids) != len(result_records) or len(ids) != len(set(ids)):
                raise ValueError("historical result record identities must be complete and unique")
            expected_result_ids.update(ids)
    if set(view_result_ids) != expected_result_ids:
        raise ValueError("historical operational-view population does not match result records exactly")

    question_id = f"question-{_slug(portfolio_label)}-baseline-v1"
    source_candidates = [
        {
            "candidate_id": entry["candidate_id"],
            "candidate_semantic_fingerprint": fingerprint(entry),
            "indicator_code": entry.get("indicator", {}).get("code"),
            "method_identity": f"{entry.get('method', {}).get('id')}@{entry.get('method', {}).get('version')}",
            "planned_disposition": entry.get("disposition"),
        }
        for entry in entries
    ]
    question_row = {
        "question_id": question_id,
        "question": question,
        "intended_use": intended_use,
        "prohibited_uses": copy.deepcopy(prohibited_uses),
        "source_candidates": source_candidates,
    }
    question_row["scope_fingerprint"] = _question_scope_fingerprint(question_row)

    candidates: list[dict[str, Any]] = []
    outcomes: list[dict[str, Any]] = []
    transformations: list[dict[str, Any]] = []
    evidence_units: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    dependence: list[dict[str, Any]] = []
    view_by_result = {view.get("result_record_id"): view for view in views if isinstance(view, dict)}

    for entry in entries:
        candidate_id = entry["candidate_id"]
        source_identity = _source_series_identity(entry)
        historical_outcome = outcome_by_id[candidate_id]
        terminal = classify_terminal_disposition(entry, historical_outcome)
        is_excluded = terminal == "excluded_pre_execution"
        declared_transformations = [] if is_excluded else list(_REQUIRED_TRANSFORMATIONS)
        candidate = {
            "candidate_id": candidate_id,
            "planned_disposition": entry["disposition"],
            "source_series_identity": source_identity,
            "method_identity": f"{entry['method']['id']}@{entry['method']['version']}",
            "declared_transformations": declared_transformations,
            "exclusion_reason": entry.get("exclusion_reason") if is_excluded else None,
        }
        candidates.append(candidate)
        outcomes.append({
            "candidate_id": candidate_id,
            "planned_disposition": entry["disposition"],
            "historical_disposition": historical_outcome.get("disposition"),
            "terminal_disposition": terminal,
            "raw_result_count": int(historical_outcome.get("raw_result_count", 0)),
            "valid_result_count": int(historical_outcome.get("valid_result_count", 0)),
            "redundant_result_count": int(historical_outcome.get("raw_result_count", 0)) - int(historical_outcome.get("valid_result_count", 0)),
        })

        unit_ids: list[str] = []
        if not is_excluded:
            for transformation_id in _REQUIRED_TRANSFORMATIONS:
                definition = copy.deepcopy(TRANSFORMATION_DEFINITIONS[transformation_id])
                transformations.append({
                    "candidate_id": candidate_id,
                    "base_series_identity": source_identity,
                    **definition,
                    "transformation_identity": transformation_identity(source_identity, definition),
                })
            package = _entry_package(entry, packages)
            assert package is not None
            records = package.get("generated_statements", [{}])[0].get("structured_payload", {}).get("result_records")
            if not isinstance(records, list) or records != historical_outcome.get("result_records"):
                raise ValueError("historical package records do not exactly match execution outcome records")
            if any(record.get("input_normalized_fingerprint") != entry["input"]["normalized_fingerprint"] for record in records):
                raise ValueError("historical package result source lineage mismatch")
            registry = {
                row["transformation_id"]: row
                for row in transformations
                if row["candidate_id"] == candidate_id
            }
            for record in records:
                transformation_id = _record_transformation(record)
                transformation = registry[transformation_id]
                result_id = record.get("result_id")
                view = view_by_result.get(result_id)
                if view is None:
                    raise ValueError("historical result does not resolve to an operational view")
                expected_view_fingerprint = fingerprint({key: value for key, value in view.items() if key != "view_fingerprint"})
                if view.get("view_fingerprint") != expected_view_fingerprint or view.get("canonical_package_id") != package.get("package_id"):
                    raise ValueError("historical operational view identity or package binding mismatch")
                if view.get("metric") != record.get("metric") or view.get("class") != record.get("class") or view.get("value") != record.get("value"):
                    raise ValueError("historical operational view semantics differ from result record")
                unit_id = "evidence-unit-" + fingerprint({"candidate_id": candidate_id, "historical_result_id": result_id}).split(":", 1)[1][:24]
                unit_ids.append(unit_id)
                evidence_units.append({
                    "evidence_unit_id": unit_id,
                    "candidate_id": candidate_id,
                    "question_id": question_id,
                    "historical_package_id": package["package_id"],
                    "historical_package_fingerprint": fingerprint(package),
                    "historical_result_id": result_id,
                    "historical_result_fingerprint": fingerprint(record),
                    "historical_result_semantic_fingerprint": record.get("semantic_fingerprint"),
                    "historical_view_id": view.get("view_id"),
                    "historical_view_fingerprint": view.get("view_fingerprint"),
                    "source_series_identity": source_identity,
                    "transformation_id": transformation_id,
                    "transformation_identity": transformation["transformation_identity"],
                    "provenance_fingerprint": fingerprint({
                        "input_normalized_fingerprint": entry["input"]["normalized_fingerprint"],
                        "package_id": package["package_id"],
                        "result_id": result_id,
                        "semantic_fingerprint": record.get("semantic_fingerprint"),
                    }),
                })
            source_scope = package.get("scope", {}).get("source_scope", {})
            dependencies = entry.get("dependencies", [])
            provider_basis = {"provider": source_scope.get("provider"), "dataset": source_scope.get("dataset")}
            acquisition_basis = sorted(value for value in dependencies if str(value).endswith("_fixture"))
            method_basis = sorted({candidate["method_identity"], *[dependency for dependency in dependencies if not str(dependency).endswith("_fixture")]})
            if any(not isinstance(value, str) or not value for value in provider_basis.values()) or not acquisition_basis or not method_basis:
                raise ValueError("dependence basis is incomplete")
            dependence.append({
                "candidate_id": candidate_id,
                "source_series_cluster_id": source_identity,
                "provider_basis": provider_basis,
                "provider_cluster_id": _cluster("provider-cluster", provider_basis),
                "acquisition_basis": acquisition_basis,
                "acquisition_cluster_id": _cluster("acquisition-cluster", acquisition_basis),
                "method_basis": method_basis,
                "method_cluster_ids": [_cluster("method-cluster", value) for value in method_basis],
                "dependence_status": "known",
            })

        relation = _RELATION_BY_TERMINAL[terminal]
        reason = candidate["exclusion_reason"] if terminal == "excluded_pre_execution" else _REASON_BY_TERMINAL[terminal]
        links.append({
            "question_id": question_id,
            "question_scope_fingerprint": question_row["scope_fingerprint"],
            "candidate_id": candidate_id,
            "source_candidate_fingerprint": fingerprint(entry),
            "direction": "question_to_candidate_to_evidence",
            "relation": relation,
            "reason": reason,
            "evidence_unit_ids": unit_ids,
        })

    envelope: dict[str, Any] = {
        "schema_name": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "profile_id": PROFILE_ID,
        "portfolio_id": f"portfolio-conformance-{_slug(portfolio_label)}-v1",
        "portfolio_label": portfolio_label,
        "adaptation_kind": "versioned_prospective_representation_of_immutable_historical_portfolio",
        "historical_representation": {
            "manifest_id": manifest["manifest_id"],
            "manifest_version": manifest.get("manifest_version"),
            "manifest_fingerprint": manifest["manifest_fingerprint"],
            "manifest_semantic_fingerprint_verified": True,
            "source_manifest": copy.deepcopy(manifest),
            "source_execution_results": copy.deepcopy(execution_results),
            "source_packages": copy.deepcopy(packages),
            "source_views": copy.deepcopy(views),
            "package_ids": [package["package_id"] for package in packages],
            "package_fingerprints": [fingerprint(package) for package in packages],
            "package_bindings": [
                {
                    "package_id": package["package_id"],
                    "package_fingerprint": fingerprint(package),
                    "indicator_code": package["scope"]["source_scope"]["indicator_code"],
                    "result_bindings": [
                        {
                            "result_id": record["result_id"],
                            "result_fingerprint": fingerprint(record),
                            "semantic_fingerprint": record["semantic_fingerprint"],
                        }
                        for record in package["generated_statements"][0]["structured_payload"]["result_records"]
                    ],
                }
                for package in packages
            ],
            "view_fingerprints": [view["view_fingerprint"] for view in views],
            "view_bindings": [
                {
                    "view_id": view["view_id"],
                    "view_fingerprint": view["view_fingerprint"],
                    "result_id": view["result_record_id"],
                    "package_id": view["canonical_package_id"],
                }
                for view in views
            ],
            "historical_outcome_fingerprint": fingerprint(execution_results),
        },
        "questions": [question_row],
        "candidates": candidates,
        "candidate_outcomes": outcomes,
        "candidate_links": links,
        "transformations": transformations,
        "evidence_units": evidence_units,
        "dependence_declarations": dependence,
        "preserved_conclusion": copy.deepcopy(conclusion),
        "preserved_conclusion_fingerprint": fingerprint(conclusion),
        "structural_differences": [
            "pre-execution exclusions remain excluded rather than being collapsed into rejection",
            "question, candidate relation and exact exclusion reason are machine-bound",
            "historical linear_time_index output labels are adapted to the declared linear_time_index_slope identity without rewriting historical records",
            "transformation definitions and parameters are bound to source-series lineage",
            "source-series diversity is separated from provider, acquisition and method dependence",
            "historical packages and views are referenced by identity and are not rewritten",
        ],
        "generality_boundary": "isolated conformance of two historical portfolios does not establish universal Evidence Portfolio generality",
    }
    envelope["accounting"] = derive_accounting(envelope)
    envelope["candidate_ledger_markdown"] = _render_candidate_ledger(envelope)
    envelope["conformance_fingerprint"] = fingerprint(envelope)
    validate_conformance_envelope(envelope)
    return envelope


def validate_conformance_envelope(envelope: Any) -> dict[str, Any]:
    if not isinstance(envelope, dict) or set(envelope) != _ENVELOPE_FIELDS or envelope.get("schema_name") != SCHEMA_NAME or envelope.get("schema_version") != SCHEMA_VERSION or envelope.get("profile_id") != PROFILE_ID:
        raise ValueError("prospective Evidence Portfolio conformance schema/version is required; historical artifacts require explicit adaptation")
    expected_fingerprint = fingerprint({key: value for key, value in envelope.items() if key != "conformance_fingerprint"})
    if envelope.get("conformance_fingerprint") != expected_fingerprint:
        raise ValueError("conformance fingerprint mismatch")
    if envelope.get("adaptation_kind") != "versioned_prospective_representation_of_immutable_historical_portfolio":
        raise ValueError("historical compatibility adaptation kind mismatch")
    historical = envelope.get("historical_representation")
    historical_fields = {
        "manifest_id", "manifest_version", "manifest_fingerprint", "manifest_semantic_fingerprint_verified",
        "source_manifest", "source_execution_results", "source_packages", "source_views",
        "package_ids", "package_fingerprints", "package_bindings", "view_fingerprints", "view_bindings",
        "historical_outcome_fingerprint",
    }
    if not isinstance(historical, dict) or set(historical) != historical_fields or historical.get("manifest_semantic_fingerprint_verified") is not True:
        raise ValueError("historical representation identity is incomplete")
    source_manifest = historical.get("source_manifest")
    source_execution = historical.get("source_execution_results")
    source_packages = historical.get("source_packages")
    source_views = historical.get("source_views")
    if not isinstance(source_manifest, dict) or source_manifest.get("manifest_fingerprint") != _manifest_semantic_fingerprint(source_manifest):
        raise ValueError("embedded source manifest identity is invalid")
    if historical.get("manifest_id") != source_manifest.get("manifest_id") or historical.get("manifest_version") != source_manifest.get("manifest_version") or historical.get("manifest_fingerprint") != source_manifest.get("manifest_fingerprint"):
        raise ValueError("historical manifest pointer contradicts embedded source manifest")
    if not isinstance(source_execution, dict) or historical.get("historical_outcome_fingerprint") != fingerprint(source_execution):
        raise ValueError("embedded source execution identity is invalid")
    if not isinstance(source_packages, list) or not isinstance(source_views, list):
        raise ValueError("embedded source package/view populations must be lists")
    expected_package_ids = [package.get("package_id") for package in source_packages if isinstance(package, dict)]
    expected_package_fingerprints = [fingerprint(package) for package in source_packages if isinstance(package, dict)]
    if len(expected_package_ids) != len(source_packages) or expected_package_ids != historical.get("package_ids") or expected_package_fingerprints != historical.get("package_fingerprints"):
        raise ValueError("embedded package population does not match historical identities")
    expected_view_fingerprints = [view.get("view_fingerprint") for view in source_views if isinstance(view, dict)]
    if len(expected_view_fingerprints) != len(source_views) or expected_view_fingerprints != historical.get("view_fingerprints"):
        raise ValueError("embedded operational-view population does not match historical identities")
    for view in source_views:
        if view.get("view_fingerprint") != fingerprint({key: value for key, value in view.items() if key != "view_fingerprint"}):
            raise ValueError("embedded operational-view fingerprint is invalid")
    package_bindings = historical.get("package_bindings")
    view_bindings = historical.get("view_bindings")
    if not isinstance(package_bindings, list) or not isinstance(view_bindings, list):
        raise ValueError("historical package/view bindings must be lists")
    expected_package_bindings = [
        {
            "package_id": package["package_id"],
            "package_fingerprint": fingerprint(package),
            "indicator_code": package["scope"]["source_scope"]["indicator_code"],
            "result_bindings": [
                {
                    "result_id": record["result_id"],
                    "result_fingerprint": fingerprint(record),
                    "semantic_fingerprint": record["semantic_fingerprint"],
                }
                for record in package["generated_statements"][0]["structured_payload"]["result_records"]
            ],
        }
        for package in source_packages
    ]
    expected_view_bindings = [
        {
            "view_id": view["view_id"],
            "view_fingerprint": view["view_fingerprint"],
            "result_id": view["result_record_id"],
            "package_id": view["canonical_package_id"],
        }
        for view in source_views
    ]
    if package_bindings != expected_package_bindings or view_bindings != expected_view_bindings:
        raise ValueError("historical package/result/view bindings contradict embedded source artifacts")
    package_binding_ids = [row.get("package_id") for row in package_bindings if isinstance(row, dict)]
    if len(package_binding_ids) != len(package_bindings) or len(package_binding_ids) != len(set(package_binding_ids)):
        raise ValueError("historical package binding identities must be unique")
    if package_binding_ids != historical.get("package_ids") or [row.get("package_fingerprint") for row in package_bindings] != historical.get("package_fingerprints"):
        raise ValueError("historical package identity lists contradict bindings")
    result_bindings: dict[str, dict[str, Any]] = {}
    for package_binding in package_bindings:
        if set(package_binding) != {"package_id", "package_fingerprint", "indicator_code", "result_bindings"} or not isinstance(package_binding["result_bindings"], list):
            raise ValueError("historical package binding shape is invalid")
        for result_binding in package_binding["result_bindings"]:
            if not isinstance(result_binding, dict) or set(result_binding) != {"result_id", "result_fingerprint", "semantic_fingerprint"}:
                raise ValueError("historical result binding shape is invalid")
            result_id = result_binding.get("result_id")
            if not isinstance(result_id, str) or not result_id or result_id in result_bindings:
                raise ValueError("historical result binding identities must be unique")
            result_bindings[result_id] = {**result_binding, "package_id": package_binding["package_id"], "package_fingerprint": package_binding["package_fingerprint"]}
    view_binding_ids = [row.get("view_id") for row in view_bindings if isinstance(row, dict)]
    view_result_ids = [row.get("result_id") for row in view_bindings if isinstance(row, dict)]
    if len(view_binding_ids) != len(view_bindings) or len(view_binding_ids) != len(set(view_binding_ids)) or len(view_result_ids) != len(set(view_result_ids)):
        raise ValueError("historical view binding identities must be unique")
    if [row.get("view_fingerprint") for row in view_bindings] != historical.get("view_fingerprints") or set(view_result_ids) != set(result_bindings):
        raise ValueError("historical view/result populations contradict bindings")
    for row in view_bindings:
        if set(row) != {"view_id", "view_fingerprint", "result_id", "package_id"} or result_bindings[row["result_id"]]["package_id"] != row["package_id"]:
            raise ValueError("historical view binding shape or package lineage mismatch")
    view_by_result_binding = {row["result_id"]: row for row in view_bindings}

    conclusion = envelope.get("preserved_conclusion")
    if not isinstance(conclusion, dict) or set(conclusion) != {"source_report", "source_report_text", "source_report_sha256", "conclusion_heading", "text", "text_sha256"}:
        raise ValueError("preserved conclusion contract is incomplete")
    source_report = conclusion.get("source_report")
    if not isinstance(source_report, str) or not source_report or source_report.startswith("/") or ".." in source_report.split("/"):
        raise ValueError("preserved conclusion source-report path must be repository-relative")
    if not isinstance(conclusion.get("source_report_text"), str) or conclusion.get("source_report_sha256") != text_sha256(conclusion["source_report_text"]):
        raise ValueError("source report content identity mismatch")
    if not isinstance(conclusion.get("conclusion_heading"), str) or conclusion.get("text") != extract_report_section(conclusion["source_report_text"], conclusion["conclusion_heading"]):
        raise ValueError("preserved conclusion is not the exact governed source-report section")
    if not isinstance(conclusion.get("text"), str) or conclusion.get("text_sha256") != text_sha256(conclusion["text"]):
        raise ValueError("preserved conclusion text identity mismatch")
    if not isinstance(conclusion.get("source_report_sha256"), str) or re.fullmatch(r"sha256:[0-9a-f]{64}", conclusion["source_report_sha256"]) is None:
        raise ValueError("source report identity is invalid")
    if envelope.get("preserved_conclusion_fingerprint") != fingerprint(conclusion):
        raise ValueError("preserved conclusion identity mismatch")

    questions = envelope.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("at least one governed analytical question is required")
    question_ids = [row.get("question_id") for row in questions if isinstance(row, dict)]
    if len(question_ids) != len(questions) or len(question_ids) != len(set(question_ids)):
        raise ValueError("question identities must be complete and unique")
    for question in questions:
        if set(question) != {"question_id", "question", "intended_use", "prohibited_uses", "source_candidates", "scope_fingerprint"}:
            raise ValueError("question contract fields are incomplete")
        if any(not isinstance(question.get(key), str) or not question[key] for key in ["question_id", "question", "intended_use"]):
            raise ValueError("question scalar fields must be nonempty")
        if not isinstance(question["prohibited_uses"], list) or not question["prohibited_uses"] or not all(isinstance(item, str) and item.strip() for item in question["prohibited_uses"]):
            raise ValueError("question prohibited-use boundary is required")
        manifest_entries_for_question = source_manifest.get("entries")
        if not isinstance(manifest_entries_for_question, list):
            raise ValueError("embedded source manifest entries are missing")
        expected_source_candidates = [
            {
                "candidate_id": entry.get("candidate_id"),
                "candidate_semantic_fingerprint": fingerprint(entry),
                "indicator_code": entry.get("indicator", {}).get("code"),
                "method_identity": f"{entry.get('method', {}).get('id')}@{entry.get('method', {}).get('version')}",
                "planned_disposition": entry.get("disposition"),
            }
            for entry in manifest_entries_for_question
        ]
        if question.get("source_candidates") != expected_source_candidates:
            raise ValueError("analytical question is not bound to exact source candidate semantics")
        if question["scope_fingerprint"] != _question_scope_fingerprint(question):
            raise ValueError("question scope fingerprint mismatch")
    question_map = {row["question_id"]: row for row in questions}

    candidates = envelope.get("candidates")
    outcomes = envelope.get("candidate_outcomes")
    links = envelope.get("candidate_links")
    if not all(isinstance(value, list) for value in [candidates, outcomes, links]):
        raise ValueError("candidate, outcome and traceability populations must be lists")
    candidate_ids = [row.get("candidate_id") for row in candidates if isinstance(row, dict)]
    outcome_ids = [row.get("candidate_id") for row in outcomes if isinstance(row, dict)]
    link_ids = [row.get("candidate_id") for row in links if isinstance(row, dict)]
    if any(set(row) != _CANDIDATE_FIELDS for row in candidates if isinstance(row, dict)) or any(set(row) != _OUTCOME_FIELDS for row in outcomes if isinstance(row, dict)) or any(set(row) != _LINK_FIELDS for row in links if isinstance(row, dict)):
        raise ValueError("candidate, outcome or traceability row shape contains missing or hidden semantics")
    if len(candidate_ids) != len(candidates) or any(not isinstance(value, str) or _ID_PATTERN.fullmatch(value) is None for value in candidate_ids) or len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate identities must be complete, safe and unique")
    if len(outcome_ids) != len(set(outcome_ids)) or set(outcome_ids) != set(candidate_ids):
        raise ValueError("candidate outcomes are missing, duplicated or orphaned")
    if len(link_ids) != len(set(link_ids)) or set(link_ids) != set(candidate_ids):
        raise ValueError("candidate traceability links are missing, duplicated or orphaned")
    candidate_map = {row["candidate_id"]: row for row in candidates}
    outcome_map = {row["candidate_id"]: row for row in outcomes}
    source_entries = source_manifest.get("entries")
    source_order = source_manifest.get("candidate_order")
    source_outcomes = source_execution.get("outcomes")
    if not isinstance(source_entries, list) or not isinstance(source_order, list) or not isinstance(source_outcomes, list) or source_order != candidate_ids:
        raise ValueError("candidate population does not preserve source-manifest order")
    source_entry_map = {entry.get("candidate_id"): entry for entry in source_entries if isinstance(entry, dict)}
    source_outcome_map = {row.get("candidate_id"): row for row in source_outcomes if isinstance(row, dict)}
    if set(source_entry_map) != set(candidate_ids) or set(source_outcome_map) != set(candidate_ids) or len(source_entry_map) != len(source_entries) or len(source_outcome_map) != len(source_outcomes):
        raise ValueError("embedded manifest/execution candidate populations do not reconcile")
    for candidate_id in candidate_ids:
        entry = source_entry_map[candidate_id]
        historical_outcome = source_outcome_map[candidate_id]
        is_excluded = entry.get("disposition") == "excluded_pre_execution"
        expected_candidate = {
            "candidate_id": candidate_id,
            "planned_disposition": "excluded_pre_execution" if is_excluded else "execute",
            "source_series_identity": _source_series_identity(entry),
            "method_identity": f"{entry.get('method', {}).get('id')}@{entry.get('method', {}).get('version')}",
            "declared_transformations": [] if is_excluded else list(_REQUIRED_TRANSFORMATIONS),
            "exclusion_reason": entry.get("exclusion_reason") if is_excluded else None,
        }
        if candidate_map[candidate_id] != expected_candidate:
            raise ValueError("candidate semantics contradict embedded source manifest")
        terminal = classify_terminal_disposition(entry, historical_outcome)
        records = historical_outcome.get("result_records") if isinstance(historical_outcome.get("result_records"), list) else []
        expected_outcome = {
            "candidate_id": candidate_id,
            "planned_disposition": expected_candidate["planned_disposition"],
            "historical_disposition": historical_outcome.get("disposition"),
            "terminal_disposition": terminal,
            "raw_result_count": len(records),
            "valid_result_count": len(records) if terminal == "valid" else 0,
            "redundant_result_count": len(records) if terminal == "redundant_candidate" else 0,
        }
        if outcome_map[candidate_id] != expected_outcome:
            raise ValueError("candidate outcome semantics contradict embedded execution result")

    source_package_by_candidate: dict[str, dict[str, Any]] = {}
    source_result_by_id: dict[str, dict[str, Any]] = {}
    source_result_candidate: dict[str, str] = {}
    consumed_package_ids: list[str] = []
    for candidate_id_value in candidate_ids:
        candidate_id = str(candidate_id_value)
        entry = source_entry_map[candidate_id]
        historical_outcome = source_outcome_map[candidate_id]
        package = _entry_package(entry, source_packages)
        records = historical_outcome.get("result_records")
        if entry.get("disposition") != "execute":
            if records not in (None, []):
                raise ValueError("non-executable candidate cannot retain historical result records")
            continue
        if package is None:
            raise ValueError("executable candidate has no exact embedded package")
        source_package_by_candidate[candidate_id] = package
        consumed_package_ids.append(package["package_id"])
        package_records = package.get("generated_statements", [{}])[0].get("structured_payload", {}).get("result_records")
        if not isinstance(records, list) or not isinstance(package_records, list) or package_records != records:
            raise ValueError("embedded package records do not exactly match embedded execution outcome")
        for record in records:
            result_id = record.get("result_id") if isinstance(record, dict) else None
            if not isinstance(result_id, str) or result_id in source_result_by_id:
                raise ValueError("embedded historical result identities must be complete and unique")
            if record.get("input_normalized_fingerprint") != entry.get("input", {}).get("normalized_fingerprint"):
                raise ValueError("embedded historical result is detached from candidate source series")
            _record_transformation(record)
            source_result_by_id[result_id] = record
            source_result_candidate[result_id] = candidate_id
    if len(consumed_package_ids) != len(source_packages) or set(consumed_package_ids) != set(historical["package_ids"]):
        raise ValueError("embedded package population is not exactly consumed by executable candidates")

    source_view_by_result: dict[str, dict[str, Any]] = {}
    for view in source_views:
        result_id = view.get("result_record_id")
        if not isinstance(result_id, str):
            raise ValueError("embedded operational view result identity is invalid")
        result = source_result_by_id.get(result_id)
        if result is None or result_id in source_view_by_result:
            raise ValueError("embedded operational view is orphaned or duplicated")
        candidate_id = source_result_candidate[result_id]
        package = source_package_by_candidate[candidate_id]
        if view.get("canonical_package_id") != package.get("package_id"):
            raise ValueError("embedded operational view package lineage mismatch")
        if any(view.get(key) != result.get(key) for key in ["metric_id", "evidence_class", "value"]):
            raise ValueError("embedded operational view semantics contradict historical result")
        source_view_by_result[result_id] = view
    if set(source_view_by_result) != set(source_result_by_id):
        raise ValueError("embedded operational views do not cover historical results exactly")

    evidence_units = envelope.get("evidence_units")
    if not isinstance(evidence_units, list):
        raise ValueError("evidence-unit population must be a list")
    evidence_ids = [row.get("evidence_unit_id") for row in evidence_units if isinstance(row, dict)]
    if any(set(row) != _EVIDENCE_FIELDS for row in evidence_units if isinstance(row, dict)):
        raise ValueError("evidence-unit row shape contains missing or hidden semantics")
    if len(evidence_ids) != len(evidence_units) or any(not isinstance(value, str) or _ID_PATTERN.fullmatch(value) is None for value in evidence_ids) or len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("evidence-unit identities must be complete, safe and unique")
    evidence_map = {row["evidence_unit_id"]: row for row in evidence_units}
    for unit in evidence_units:
        result_binding = result_bindings.get(unit.get("historical_result_id"))
        view_binding = view_by_result_binding.get(unit.get("historical_result_id"))
        if result_binding is None or view_binding is None:
            raise ValueError("evidence unit is not bound to the exact historical result/view population")
        result_id = unit.get("historical_result_id")
        source_record = source_result_by_id.get(result_id)
        if source_record is None or source_result_candidate.get(result_id) != unit.get("candidate_id"):
            raise ValueError("evidence unit historical result is cross-assigned between candidates")
        candidate_id = unit["candidate_id"]
        source_package = source_package_by_candidate.get(candidate_id)
        source_view = source_view_by_result.get(result_id)
        if source_package is None or source_view is None:
            raise ValueError("evidence unit source package/view lineage is incomplete")
        if unit.get("source_series_identity") != candidate_map[candidate_id]["source_series_identity"] or unit.get("transformation_id") != _record_transformation(source_record):
            raise ValueError("evidence unit source-series or transformation lineage contradicts historical result")
        expected_historical = {
            "historical_package_id": result_binding["package_id"],
            "historical_package_fingerprint": result_binding["package_fingerprint"],
            "historical_result_fingerprint": result_binding["result_fingerprint"],
            "historical_result_semantic_fingerprint": result_binding["semantic_fingerprint"],
            "historical_view_id": view_binding["view_id"],
            "historical_view_fingerprint": view_binding["view_fingerprint"],
        }
        if any(unit.get(key) != value for key, value in expected_historical.items()):
            raise ValueError("evidence unit historical package/result/view identity mismatch")
        source_fingerprint = source_record.get("input_normalized_fingerprint")
        expected_provenance = fingerprint({
            "input_normalized_fingerprint": source_fingerprint,
            "package_id": unit["historical_package_id"],
            "result_id": unit["historical_result_id"],
            "semantic_fingerprint": unit["historical_result_semantic_fingerprint"],
        })
        if unit.get("provenance_fingerprint") != expected_provenance:
            raise ValueError("evidence-unit provenance identity mismatch")
    if {unit["historical_result_id"] for unit in evidence_units} != set(result_bindings):
        raise ValueError("evidence-unit population does not cover historical results exactly")

    for outcome in outcomes:
        if outcome.get("terminal_disposition") not in TERMINAL_DISPOSITIONS:
            raise ValueError("unknown candidate terminal disposition")
        candidate = candidate_map[outcome["candidate_id"]]
        terminal = outcome["terminal_disposition"]
        if outcome.get("planned_disposition") != candidate.get("planned_disposition"):
            raise ValueError("candidate planned disposition is contradictory")
        if candidate.get("planned_disposition") == "excluded_pre_execution":
            if terminal != "excluded_pre_execution" or not candidate.get("exclusion_reason"):
                raise ValueError("excluded candidate accounting is contradictory or incomplete")
        elif candidate.get("planned_disposition") == "execute":
            if terminal == "excluded_pre_execution":
                raise ValueError("executed candidate cannot be counted as pre-execution exclusion")
        else:
            raise ValueError("candidate planned disposition is unsupported")
        for key in ["raw_result_count", "valid_result_count", "redundant_result_count"]:
            if type(outcome.get(key)) is not int or outcome[key] < 0:
                raise ValueError("candidate result accounting must use nonnegative integers")
        if outcome["raw_result_count"] != outcome["valid_result_count"] + outcome["redundant_result_count"]:
            raise ValueError("candidate result accounting does not reconcile")
        candidate_evidence_count = sum(1 for unit in evidence_units if unit.get("candidate_id") == outcome["candidate_id"])
        historical_to_terminal = {
            "valid": "valid", "null": "null", "rejected": "rejected_execution",
            "failed": "execution_failure", "redundant": "redundant_candidate",
        }
        if candidate["planned_disposition"] == "excluded_pre_execution":
            expected_terminal = "excluded_pre_execution" if outcome.get("historical_disposition") == "rejected" else None
        else:
            expected_terminal = historical_to_terminal.get(outcome.get("historical_disposition"))
        if terminal != expected_terminal:
            raise ValueError("historical and terminal dispositions are contradictory")
        if terminal == "valid":
            if outcome["valid_result_count"] <= 0 or candidate_evidence_count != outcome["valid_result_count"]:
                raise ValueError("valid outcome evidence count does not reconcile")
        elif terminal == "redundant_candidate":
            if outcome["valid_result_count"] != 0 or outcome["raw_result_count"] == 0 or candidate_evidence_count != 0:
                raise ValueError("redundant candidate accounting is contradictory")
        elif any(outcome[key] != 0 for key in ["raw_result_count", "valid_result_count", "redundant_result_count"]) or candidate_evidence_count != 0:
            raise ValueError("non-result disposition cannot carry result records or evidence units")

    linked_units: set[str] = set()
    support_by_question = {question_id: 0 for question_id in question_ids}
    for link in links:
        if link.get("direction") != "question_to_candidate_to_evidence" or link.get("relation") not in RELATIONS:
            raise ValueError("traceability direction or relation is invalid")
        question = question_map.get(link.get("question_id"))
        candidate = candidate_map[link["candidate_id"]]
        if question is None or link.get("question_scope_fingerprint") != question["scope_fingerprint"]:
            raise ValueError("unsupported question link")
        if link.get("source_candidate_fingerprint") != fingerprint(source_entry_map[link["candidate_id"]]):
            raise ValueError("candidate traceability link is detached from its source semantics")
        units = link.get("evidence_unit_ids")
        if not isinstance(units, list) or len(units) != len(set(units)) or any(unit not in evidence_map for unit in units):
            raise ValueError("traceability contains orphaned or duplicate evidence")
        terminal = outcome_map[link["candidate_id"]]["terminal_disposition"]
        expected_relation = _RELATION_BY_TERMINAL[terminal]
        expected_reason = candidate.get("exclusion_reason") if terminal == "excluded_pre_execution" else _REASON_BY_TERMINAL[terminal]
        if link["relation"] != expected_relation or link.get("reason") != expected_reason:
            raise ValueError("candidate relation or exact exclusion/terminal reason contradicts terminal disposition")
        if terminal == "valid":
            if not units or len(units) != outcome_map[link["candidate_id"]]["valid_result_count"]:
                raise ValueError("valid evidentiary relation lacks exact evidence-unit coverage")
            support_by_question[link["question_id"]] += 1
        elif units:
            raise ValueError("non-valid candidate relation cannot carry evidence units")
        for unit_id in units:
            unit = evidence_map[unit_id]
            if unit.get("candidate_id") != link["candidate_id"] or unit.get("question_id") != link["question_id"]:
                raise ValueError("evidence unit is orphaned from its directional chain")
            if unit_id in linked_units:
                raise ValueError("evidence unit is linked more than once")
            linked_units.add(unit_id)
    if linked_units != set(evidence_ids):
        raise ValueError("orphaned evidence units are present")
    if any(count == 0 for count in support_by_question.values()):
        raise ValueError("unsupported question has no admitted evidentiary support")

    transformations = envelope.get("transformations")
    if not isinstance(transformations, list):
        raise ValueError("transformation registry must be a list")
    transformation_by_identity: dict[str, dict[str, Any]] = {}
    transformation_keys: set[tuple[str, str]] = set()
    for row in transformations:
        if not isinstance(row, dict) or set(row) != _TRANSFORMATION_FIELDS:
            raise ValueError("transformation registry row shape contains missing or hidden semantics")
        candidate = candidate_map.get(row.get("candidate_id"))
        if candidate is None or row.get("base_series_identity") != candidate.get("source_series_identity"):
            raise ValueError("transformation registry row is orphaned or detached from candidate source lineage")
        definition = {key: row.get(key) for key in ["transformation_id", "operation", "parameters"]}
        _validate_transformation_definition(definition)
        base = row.get("base_series_identity")
        identity = row.get("transformation_identity")
        if identity != transformation_identity(base, definition):
            raise ValueError("transformation identity collision, substitution or incomplete binding")
        key = (base, row["transformation_id"])
        if key in transformation_keys or identity in transformation_by_identity:
            raise ValueError("transformation identity collision or duplicate definition")
        transformation_keys.add(key)
        transformation_by_identity[identity] = row
    for candidate in candidates:
        expected = [] if candidate["planned_disposition"] == "excluded_pre_execution" else list(_REQUIRED_TRANSFORMATIONS)
        if candidate.get("declared_transformations") != expected:
            raise ValueError("candidate transformation declarations are incomplete or contradictory")
        base = candidate.get("source_series_identity")
        actual = {
            row["transformation_id"]
            for row in transformations
            if row.get("candidate_id") == candidate["candidate_id"]
        }
        if actual != set(expected):
            raise ValueError("candidate transformation registry coverage mismatch")
    for unit in evidence_units:
        row = transformation_by_identity.get(unit.get("transformation_identity"))
        candidate = candidate_map.get(unit.get("candidate_id"))
        if row is None or candidate is None:
            raise ValueError("evidence transformation identity is unresolved")
        if row["candidate_id"] != unit.get("candidate_id") or row["transformation_id"] != unit.get("transformation_id") or row["base_series_identity"] != unit.get("source_series_identity") or candidate["source_series_identity"] != unit["source_series_identity"]:
            raise ValueError("evidence transformation identity was substituted or detached from source lineage")

    dependence = envelope.get("dependence_declarations")
    if not isinstance(dependence, list):
        raise ValueError("dependence declarations must be a list")
    dependence_ids = [row.get("candidate_id") for row in dependence if isinstance(row, dict)]
    executable_ids = {row["candidate_id"] for row in candidates if row["planned_disposition"] == "execute"}
    if len(dependence_ids) != len(set(dependence_ids)) or set(dependence_ids) != executable_ids:
        raise ValueError("dependence declarations do not cover executable evidence candidates exactly")
    for row in dependence:
        if set(row) != _DEPENDENCE_FIELDS:
            raise ValueError("dependence declaration dimensions are incomplete")
        if row["dependence_status"] not in DEPENDENCE_STATUSES:
            raise ValueError("dependence status must be known or unresolved")
        for key in ["source_series_cluster_id", "provider_cluster_id", "acquisition_cluster_id"]:
            if not isinstance(row[key], str) or not row[key]:
                raise ValueError("dependence cluster identity is missing")
        provider_basis = row["provider_basis"]
        acquisition_basis = row["acquisition_basis"]
        method_basis = row["method_basis"]
        if not isinstance(provider_basis, dict) or set(provider_basis) != {"provider", "dataset"} or any(not isinstance(value, str) or not value for value in provider_basis.values()):
            raise ValueError("provider dependence basis is incomplete")
        if not isinstance(acquisition_basis, list) or not acquisition_basis or acquisition_basis != sorted(set(acquisition_basis)) or any(not isinstance(value, str) or not value for value in acquisition_basis):
            raise ValueError("acquisition dependence basis is incomplete or duplicated")
        if not isinstance(method_basis, list) or not method_basis or method_basis != sorted(set(method_basis)) or any(not isinstance(value, str) or not value for value in method_basis):
            raise ValueError("method dependence basis is incomplete or duplicated")
        expected_method_clusters = [_cluster("method-cluster", value) for value in method_basis]
        candidate_id = row["candidate_id"]
        source_entry = source_entry_map[candidate_id]
        source_package = source_package_by_candidate[candidate_id]
        source_scope = source_package.get("scope", {}).get("source_scope", {})
        dependencies = source_entry.get("dependencies", [])
        expected_provider_basis = {"provider": source_scope.get("provider"), "dataset": source_scope.get("dataset")}
        expected_acquisition_basis = sorted(dependency for dependency in dependencies if str(dependency).endswith("_fixture")) or [str(source_entry.get("input", {}).get("source_path"))]
        expected_method_basis = sorted({candidate_map[candidate_id]["method_identity"], *[dependency for dependency in dependencies if not str(dependency).endswith("_fixture")]})
        if provider_basis != expected_provider_basis or acquisition_basis != expected_acquisition_basis or method_basis != expected_method_basis:
            raise ValueError("dependence semantic basis contradicts embedded package or manifest source")
        if row["provider_cluster_id"] != _cluster("provider-cluster", provider_basis) or row["acquisition_cluster_id"] != _cluster("acquisition-cluster", acquisition_basis) or row["method_cluster_ids"] != expected_method_clusters:
            raise ValueError("dependence cluster identity does not match its explicit semantic basis")
        if not isinstance(row["method_cluster_ids"], list) or not row["method_cluster_ids"] or len(row["method_cluster_ids"]) != len(set(row["method_cluster_ids"])):
            raise ValueError("method dependence clusters are incomplete or duplicated")
        if row["source_series_cluster_id"] != candidate_map[row["candidate_id"]]["source_series_identity"]:
            raise ValueError("dependence source-series lineage mismatch")

    expected_accounting = derive_accounting(envelope)
    if envelope.get("accounting") != expected_accounting:
        raise ValueError("portfolio accounting is incomplete, contradictory or conceals support dependence")
    if not all(expected_accounting["reconciliation"].values()):
        raise ValueError("portfolio accounting reconciliation failed closed")
    if any(row["dependence_status"] == "unresolved" for row in dependence) and expected_accounting["support_diversity"]["fully_independent_support_claims"] != 0:
        raise ValueError("unresolved dependence cannot become independence")
    if envelope.get("candidate_ledger_markdown") != _render_candidate_ledger(envelope):
        raise ValueError("generated candidate ledger drifted from machine traceability")
    if envelope.get("generality_boundary") != "isolated conformance of two historical portfolios does not establish universal Evidence Portfolio generality":
        raise ValueError("conformance proof overclaims Evidence Portfolio generality")
    return {
        "valid": True,
        "profile_id": PROFILE_ID,
        "portfolio_id": envelope.get("portfolio_id"),
        "conformance_fingerprint": envelope["conformance_fingerprint"],
        "accounting": copy.deepcopy(expected_accounting),
    }


def resolve_question_evidence_chain(envelope: dict[str, Any], question_id: str) -> dict[str, Any]:
    validate_conformance_envelope(envelope)
    questions = [row for row in envelope["questions"] if row["question_id"] == question_id]
    if len(questions) != 1:
        raise ValueError("question identity does not resolve exactly once")
    links = [row for row in envelope["candidate_links"] if row["question_id"] == question_id]
    candidate_ids = {row["candidate_id"] for row in links}
    unit_ids = {unit_id for row in links for unit_id in row["evidence_unit_ids"]}
    return {
        "question": copy.deepcopy(questions[0]),
        "candidate_links": copy.deepcopy(links),
        "candidates": [copy.deepcopy(row) for row in envelope["candidates"] if row["candidate_id"] in candidate_ids],
        "evidence_units": [copy.deepcopy(row) for row in envelope["evidence_units"] if row["evidence_unit_id"] in unit_ids],
    }
