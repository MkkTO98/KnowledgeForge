#!/usr/bin/env python3
"""Deterministic pre-production validation framework for KnowledgeForge synthetic fixtures.

This validator enforces the architecture contracts for the fixture-backed pipeline:
Evidence -> Evidence Evaluation -> Knowledge Candidate -> Knowledge Object -> Knowledge Change.
It performs no PostgreSQL access, no model calls, and no production knowledge generation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALIDATOR_VERSION = "v1"

FORBIDDEN_INTERPRETATION_PHRASES = [
    "this means",
    "investors should",
    "economy is likely",
    "key takeaway",
    "bullish",
    "bearish",
    "policy implication",
    "therefore",
    "recommend",
]

ALLOWED_EVIDENCE_CLASSES = {
    "source_evidence_package",
    "external_observational_metadata",
    "external_lineage_provenance",
    "external_source_summary",
    "manually_supplied_evidence",
    "generated_intermediate_evidence",
    "official_source_documentation",
    "literature_source_assertion",
}

DISALLOWED_DIRECT_EVIDENCE_CLASSES = {"llm_generated_text", "consumer_usage", "live_web_without_snapshot"}

REPRODUCIBLE_STATES = {"reproducible", "replayable-with-external-dependency", "audit-only"}

PACKAGE_KINDS = {
    "KnowledgeCandidatePackage",
    "KnowledgeObjectPackage",
    "KnowledgeChangePackage",
    "EvidenceEvaluationPackage",
    "GeneratedIntermediatePackage",
}

REQUIRED_PACKAGE_FINGERPRINTS = {
    "input_set",
    "evidence_references",
    "query_definitions",
    "computation_recipe",
    "generated_statements",
    "package_manifest",
}


Finding = dict[str, Any]
Report = dict[str, Any]


def _finding(category: str, message: str, severity: str = "blocker", location: str = "") -> Finding:
    return {
        "category": category,
        "severity": severity,
        "message": message,
        "location": location,
        "blocks_acceptance": severity == "blocker",
    }


def _report(stage: str, blockers: list[Finding], warnings: list[Finding] | None = None) -> Report:
    return {
        "ok": not blockers,
        "stage": stage,
        "validator_version": VALIDATOR_VERSION,
        "blockers": blockers,
        "warnings": warnings or [],
    }


def _missing(data: dict[str, Any], fields: list[str], category: str, location: str = "") -> list[Finding]:
    return [
        _finding(category, f"missing required field: {field}", location=location or field)
        for field in fields
        if field not in data or data[field] in (None, "", [], {})
    ]


def _contains_forbidden_language(value: Any) -> bool:
    texts: list[str] = []
    if isinstance(value, str):
        texts.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            if isinstance(item, (str, dict, list)):
                texts.append(json.dumps(item) if not isinstance(item, str) else item)
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (str, dict, list)):
                texts.append(json.dumps(item) if not isinstance(item, str) else item)
    combined = "\n".join(texts).lower()
    return any(phrase in combined for phrase in FORBIDDEN_INTERPRETATION_PHRASES)


def validate_evidence(evidence: dict[str, Any]) -> Report:
    blockers: list[Finding] = []
    blockers.extend(
        _missing(
            evidence,
            [
                "evidence_ref_id",
                "evidence_class",
                "source_family",
                "source_identity",
                "provenance_refs",
                "fingerprints",
                "classification",
                "reproducibility",
            ],
            "evidence_contract",
        )
    )

    fingerprints = evidence.get("fingerprints")
    if not isinstance(fingerprints, dict) or not fingerprints:
        blockers.append(_finding("provenance", "missing required fingerprint presence for evidence", location="fingerprints"))

    evidence_class = evidence.get("evidence_class")
    classification = evidence.get("classification", {}) if isinstance(evidence.get("classification"), dict) else {}
    direct = bool(classification.get("direct_evidence"))
    if evidence_class in DISALLOWED_DIRECT_EVIDENCE_CLASSES and direct:
        blockers.append(
            _finding(
                "constitutional_boundary",
                "LLM output cannot be direct evidence; disallowed evidence classes cannot support accepted knowledge directly",
                location="evidence_class",
            )
        )
    if evidence_class and evidence_class not in ALLOWED_EVIDENCE_CLASSES and evidence_class not in DISALLOWED_DIRECT_EVIDENCE_CLASSES:
        blockers.append(_finding("evidence_contract", f"unsupported evidence_class: {evidence_class}", location="evidence_class"))

    repro = evidence.get("reproducibility")
    if not isinstance(repro, dict) or repro.get("state") not in REPRODUCIBLE_STATES:
        blockers.append(_finding("reproducibility", "reproducibility state must be explicit and replayable/auditable", location="reproducibility"))
    elif not repro.get("handle"):
        blockers.append(_finding("reproducibility", "reproducibility handle is required", location="reproducibility.handle"))

    return _report("evidence", blockers)


def validate_evidence_evaluation(evaluation: dict[str, Any]) -> Report:
    blockers: list[Finding] = []
    blockers.extend(
        _missing(
            evaluation,
            [
                "evaluation_id",
                "evidence_ref_id",
                "evaluation_type",
                "evaluation_statement",
                "dimensions",
                "uncertainty",
                "contradictions",
                "evidence_references",
                "provenance",
                "fingerprints",
                "reproducibility",
            ],
            "evidence_contract",
        )
    )
    if "embedded_evidence" in evaluation or "evidence" in evaluation:
        blockers.append(_finding("evidence_contract", "evidence evaluation must not embed evidence; keep evidence/evaluation separation", location="embedded_evidence"))

    required_dimensions = {
        "validity",
        "freshness",
        "source_family",
        "data_lineage",
        "reproducibility",
        "contradiction_handling",
        "uncertainty",
        "missingness",
        "auditability",
    }
    dimensions = evaluation.get("dimensions")
    if not isinstance(dimensions, dict) or not required_dimensions.issubset(dimensions):
        blockers.append(_finding("evidence_contract", "supported evaluation fields/dimensions are incomplete", location="dimensions"))

    if "uncertainty" not in evaluation or not evaluation.get("uncertainty"):
        blockers.append(_finding("evidence_contract", "uncertainty representation is required", location="uncertainty"))
    if "contradictions" not in evaluation or not isinstance(evaluation.get("contradictions"), list):
        blockers.append(_finding("evidence_contract", "contradiction recording is required", location="contradictions"))
    if not isinstance(evaluation.get("fingerprints"), dict) or not evaluation.get("fingerprints"):
        blockers.append(_finding("provenance", "reproducibility metadata/fingerprints are required", location="fingerprints"))
    if _contains_forbidden_language(evaluation.get("evaluation_statement", "")):
        blockers.append(_finding("unsupported_inference", "forbidden interpretation language in evidence evaluation", location="evaluation_statement"))

    return _report("evidence_evaluation", blockers)


def _validate_common_package(package: dict[str, Any], expected_kind: str | None = None) -> list[Finding]:
    blockers: list[Finding] = []
    blockers.extend(
        _missing(
            package,
            [
                "package_id",
                "package_kind",
                "package_version",
                "created_at",
                "created_by",
                "status",
                "scope",
                "input_references",
                "evidence_references",
                "computation_method",
                "generated_statements",
                "confidence_quality",
                "contradiction_records",
                "provenance_envelope",
                "fingerprints",
                "validation_state",
                "evolution_metadata",
            ],
            "package_schema",
        )
    )
    kind = package.get("package_kind")
    if kind not in PACKAGE_KINDS:
        blockers.append(_finding("package_schema", f"invalid package_kind: {kind}", location="package_kind"))
    if expected_kind and kind != expected_kind:
        blockers.append(_finding("package_schema", f"expected package_kind {expected_kind}, got {kind}", location="package_kind"))

    fingerprints = package.get("fingerprints")
    if not isinstance(fingerprints, dict) or not REQUIRED_PACKAGE_FINGERPRINTS.issubset(set(fingerprints)):
        blockers.append(_finding("lineage_fingerprint", "required package fingerprints are missing", location="fingerprints"))

    provenance = package.get("provenance_envelope")
    if not isinstance(provenance, dict) or not provenance.get("reproducibility_state"):
        blockers.append(_finding("provenance", "provenance envelope with reproducibility state is required", location="provenance_envelope"))

    if not isinstance(package.get("evidence_references"), list) or not package.get("evidence_references"):
        blockers.append(_finding("evidence_contract", "evidence references are required", location="evidence_references"))
    if "embedded_evaluation" in package:
        blockers.append(_finding("evidence_contract", "candidate must not collapse evidence and evaluation into one field", location="embedded_evaluation"))

    statements = package.get("generated_statements", [])
    if not isinstance(statements, list) or not statements:
        blockers.append(_finding("package_schema", "generated statements are required", location="generated_statements"))
    else:
        for idx, statement in enumerate(statements):
            if not isinstance(statement, dict):
                blockers.append(_finding("package_schema", "generated statement must be an object", location=f"generated_statements[{idx}]"))
                continue
            blockers.extend(_missing(statement, ["statement_id", "statement_type", "text", "applicability", "dependencies", "evidence_refs", "origin"], "package_schema", location=f"generated_statements[{idx}]"))
            if _contains_forbidden_language(statement.get("text", "")):
                blockers.append(_finding("unsupported_inference", "forbidden interpretation language in generated statement", location=f"generated_statements[{idx}].text"))

    cq = package.get("confidence_quality")
    if not isinstance(cq, dict):
        blockers.append(_finding("package_schema", "confidence metadata is required", location="confidence_quality"))
    else:
        blockers.extend(_missing(cq, ["confidence_label", "uncertainty_dimensions", "missingness_summary", "evidence_sufficiency", "reproducibility_state", "validation_state", "governance_review_state", "lifecycle_state"], "package_schema", location="confidence_quality"))

    return blockers


def validate_knowledge_candidate(candidate: dict[str, Any]) -> Report:
    blockers = _validate_common_package(candidate, "KnowledgeCandidatePackage")
    if candidate.get("status") == "accepted" or (isinstance(candidate.get("confidence_quality"), dict) and candidate["confidence_quality"].get("lifecycle_state") == "accepted"):
        blockers.append(_finding("maturity_state", "candidate package cannot be accepted or claim accepted lifecycle state", location="status"))
    if candidate.get("package_kind") == "KnowledgeCandidatePackage" and candidate.get("status") not in {"draft", "candidate", "validated", "blocked", "rejected"}:
        blockers.append(_finding("maturity_state", "candidate package has invalid pre-production status", location="status"))
    return _report("knowledge_candidate", blockers)


def validate_knowledge_object(obj: dict[str, Any]) -> Report:
    blockers = _validate_common_package(obj, "KnowledgeObjectPackage")
    promotion = obj.get("promotion")
    if not isinstance(promotion, dict):
        blockers.append(_finding("maturity_state", "promotion requirements are missing", location="promotion"))
    else:
        blockers.extend(_missing(promotion, ["from_candidate_package_id", "promotion_justification", "validation_history", "maturity_state"], "maturity_state", location="promotion"))
        maturity = promotion.get("maturity_state", "")
        if "M5" in maturity or "production" in maturity.lower():
            blockers.append(_finding("maturity_state", "production-governed maturity cannot be claimed by pre-production fixture", location="promotion.maturity_state"))

    validation_state = obj.get("validation_state")
    if not isinstance(validation_state, dict) or validation_state.get("validation_result") != "pass" or validation_state.get("blockers"):
        blockers.append(_finding("maturity_state", "knowledge object promotion requires passing validation history", location="validation_state"))

    evidence_integrity = obj.get("evidence_integrity")
    if not isinstance(evidence_integrity, dict) or not evidence_integrity.get("evidence_refs_verified") or not evidence_integrity.get("fingerprints_verified"):
        blockers.append(_finding("evidence_contract", "evidence integrity must verify references and fingerprints", location="evidence_integrity"))

    lineage = obj.get("lineage")
    candidate_id = promotion.get("from_candidate_package_id") if isinstance(promotion, dict) else None
    if not isinstance(lineage, dict):
        blockers.append(_finding("lineage_fingerprint", "lineage continuity is required", location="lineage"))
    else:
        if lineage.get("previous_package_id") != candidate_id:
            blockers.append(_finding("lineage_fingerprint", "previous package lineage does not match promotion candidate", location="lineage.previous_package_id"))
        version_lineage = lineage.get("version_lineage")
        if not isinstance(version_lineage, list) or candidate_id not in version_lineage or obj.get("package_id") not in version_lineage:
            blockers.append(_finding("lineage_fingerprint", "version lineage must include candidate and object package", location="lineage.version_lineage"))

    return _report("knowledge_object", blockers)


def validate_knowledge_change(change: dict[str, Any]) -> Report:
    blockers: list[Finding] = []
    blockers.extend(
        _missing(
            change,
            [
                "change_report_id",
                "date",
                "author",
                "status",
                "related_package_ids",
                "trigger_categories",
                "previous_package_ref",
                "new_package_ref",
                "version_lineage",
                "before_after",
                "evidence_method_delta",
                "fingerprint_evolution",
                "contradiction_uncertainty_delta",
                "validation_result",
                "reproducibility_note",
            ],
            "package_schema",
        )
    )
    if "fingerprint_evolution" not in change or not isinstance(change.get("fingerprint_evolution"), dict):
        blockers.append(_finding("lineage_fingerprint", "fingerprint_evolution is required", location="fingerprint_evolution"))
    else:
        blockers.extend(_missing(change["fingerprint_evolution"], ["previous_package_manifest", "new_package_manifest", "changed_fingerprints"], "lineage_fingerprint", location="fingerprint_evolution"))

    version_lineage = change.get("version_lineage")
    previous_ref = change.get("previous_package_ref")
    new_ref = change.get("new_package_ref")
    if not isinstance(version_lineage, list) or previous_ref not in version_lineage or new_ref not in version_lineage:
        blockers.append(_finding("lineage_fingerprint", "version lineage must include previous and new package references", location="version_lineage"))

    repro = change.get("reproducibility_note")
    if not isinstance(repro, dict) or not all(repro.get(key) for key in ["prior_state_reconstructable", "new_state_reconstructable", "changed_inputs_methods_fingerprinted", "rerun_expected_to_reproduce"]):
        blockers.append(_finding("reproducibility", "transition reproducibility note must prove prior/new reconstruction and fingerprinting", location="reproducibility_note"))

    return _report("knowledge_change", blockers)


def validate_by_stage(data: dict[str, Any]) -> Report:
    stage = data.get("stage")
    kind = data.get("package_kind")
    if stage == "evidence":
        return validate_evidence(data)
    if stage == "evidence_evaluation" or kind == "EvidenceEvaluationPackage":
        return validate_evidence_evaluation(data)
    if kind == "KnowledgeCandidatePackage":
        return validate_knowledge_candidate(data)
    if kind == "KnowledgeObjectPackage":
        return validate_knowledge_object(data)
    if stage == "knowledge_change" or kind == "KnowledgeChangePackage":
        return validate_knowledge_change(data)
    return _report("unknown", [_finding("package_schema", "cannot determine validation stage", location="stage")])


def validate_file(path: Path) -> Report:
    return validate_by_stage(json.loads(path.read_text(encoding="utf-8")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a KnowledgeForge pre-production pipeline fixture")
    parser.add_argument("path", type=Path, help="JSON fixture path")
    args = parser.parse_args(argv)
    report = validate_file(args.path)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
