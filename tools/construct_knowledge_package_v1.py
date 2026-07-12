#!/usr/bin/env python3
"""Deterministically construct KnowledgeForge package fixtures from a Source Evidence Package.

This is a pre-production validation slice. It performs no repository integration,
no database access, no model calls, and no production knowledge generation.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

VALIDATOR_VERSION = "construction-v1"
DATE = "2026-07-09"

FORBIDDEN_BOUNDARY_TERMS = [
    "this means",
    "investors should",
    "economy is likely",
    "key takeaway",
    "bullish",
    "bearish",
    "policy implication",
    "recommend",
    "hypothesis",
    "forecast",
    "causal claim",
    "presentation narrative",
    "investment meaning",
    "policy meaning",
]

SUPPORTED_KNOWLEDGE_CATEGORIES = {
    "factual",
    "derived",
    "classified",
    "methodological",
    "negative",
    "evidence_quality",
    "coverage",
    "provenance",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def finding(category: str, message: str, location: str = "", severity: str = "blocker") -> dict[str, Any]:
    return {
        "category": category,
        "severity": severity,
        "message": message,
        "location": location,
        "blocks_acceptance": severity == "blocker",
    }


def report(stage: str, blockers: list[dict[str, Any]], warnings: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "ok": not blockers,
        "stage": stage,
        "validator_version": VALIDATOR_VERSION,
        "blockers": blockers,
        "warnings": warnings or [],
    }


def _missing(data: dict[str, Any], fields: list[str], category: str, location_prefix: str = "") -> list[dict[str, Any]]:
    out = []
    for field in fields:
        if field not in data or data[field] in (None, "", [], {}):
            loc = f"{location_prefix}.{field}" if location_prefix else field
            out.append(finding(category, f"missing required field: {field}", loc))
    return out


def _source_manifest(package: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_evidence_package_id": package.get("source_evidence_package_id"),
        "package_kind": package.get("package_kind"),
        "package_version": package.get("package_version"),
        "created_at": package.get("created_at"),
        "immutability": package.get("immutability"),
        "source_identity": package.get("source_identity"),
        "evidence_payload": package.get("evidence_payload"),
        "evidence_metadata": package.get("evidence_metadata"),
        "provenance": package.get("provenance"),
        "reproducibility": package.get("reproducibility"),
    }


def expected_source_fingerprints(package: dict[str, Any]) -> dict[str, str]:
    return {
        "source_payload": sha256_fingerprint(package.get("evidence_payload")),
        "provenance": sha256_fingerprint(package.get("provenance")),
        "reproducibility": sha256_fingerprint(package.get("reproducibility")),
        "package_manifest": sha256_fingerprint(_source_manifest(package)),
    }


def validate_source_evidence_package(package: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    blockers.extend(_missing(package, [
        "source_evidence_package_id",
        "package_kind",
        "package_version",
        "created_at",
        "immutability",
        "source_identity",
        "evidence_payload",
        "evidence_metadata",
        "provenance",
        "reproducibility",
        "fingerprints",
    ], "evidence_contract"))

    if package.get("package_kind") != "SourceEvidencePackage":
        blockers.append(finding("evidence_contract", "package_kind must be SourceEvidencePackage", "package_kind"))

    immutability = package.get("immutability")
    if not isinstance(immutability, dict) or immutability.get("state") != "immutable_fixture" or immutability.get("mutation_policy") != "read_only":
        blockers.append(finding("evidence_contract", "source package must be immutable and read-only", "immutability"))

    if not isinstance(package.get("provenance"), dict) or not package.get("provenance", {}).get("source_snapshot_id"):
        blockers.append(finding("provenance", "provenance must include a source_snapshot_id", "provenance"))

    repro = package.get("reproducibility")
    if not isinstance(repro, dict) or repro.get("state") != "reproducible" or repro.get("nondeterminism") != "none":
        blockers.append(finding("reproducibility", "reproducibility must prove deterministic replay with no nondeterminism", "reproducibility"))
    elif "deterministic" not in str(repro.get("rerun_method", "")).lower():
        blockers.append(finding("reproducibility", "rerun_method must describe deterministic replay", "reproducibility.rerun_method"))

    metadata = package.get("evidence_metadata")
    if not isinstance(metadata, dict):
        blockers.append(finding("evidence_contract", "evidence_metadata is required", "evidence_metadata"))
    else:
        classification = metadata.get("classification", {})
        if classification.get("generated_by_llm"):
            blockers.append(finding("constitutional_boundary", "LLM generated evidence is not valid for this slice", "evidence_metadata.classification"))
        if classification.get("contains_observational_values"):
            blockers.append(finding("constitutional_boundary", "source package fixture must not make KnowledgeForge own observations", "evidence_metadata.classification"))

    payload = package.get("evidence_payload")
    if isinstance(payload, dict):
        statement = payload.get("factual_statement", "")
        category = payload.get("knowledge_category")
        if category not in SUPPORTED_KNOWLEDGE_CATEGORIES:
            blockers.append(finding("constitutional_boundary", f"unsupported knowledge category: {category}", "evidence_payload.knowledge_category"))
        if contains_forbidden_boundary_language(statement):
            blockers.append(finding("unsupported_inference", "source factual statement contains forbidden boundary language", "evidence_payload.factual_statement"))
    else:
        blockers.append(finding("evidence_contract", "evidence_payload must be an object", "evidence_payload"))

    fingerprints = package.get("fingerprints")
    if not isinstance(fingerprints, dict):
        blockers.append(finding("lineage_fingerprint", "fingerprints must be an object", "fingerprints"))
    else:
        for key, expected in expected_source_fingerprints(package).items():
            if fingerprints.get(key) != expected:
                blockers.append(finding("lineage_fingerprint", f"{key} fingerprint does not match canonical source package content", f"fingerprints.{key}"))

    return report("source_evidence_package", blockers)


def contains_forbidden_boundary_language(value: Any) -> bool:
    text = canonical_json(value).lower() if not isinstance(value, str) else value.lower()
    return any(term in text for term in FORBIDDEN_BOUNDARY_TERMS)


def _evidence_ref_id(source_package: dict[str, Any]) -> str:
    return "ev-" + source_package["source_evidence_package_id"].replace("srcpkg-", "srcpkg-")


def construct_evidence(source_package: dict[str, Any]) -> dict[str, Any]:
    metadata = source_package["evidence_metadata"]
    source_identity = source_package["source_identity"]
    return {
        "stage": "evidence",
        "evidence_ref_id": _evidence_ref_id(source_package),
        "evidence_class": metadata["evidence_class"],
        "source_family": source_identity["source_family"],
        "source_identity": source_identity["source_name"],
        "provenance_refs": [source_package["provenance"]["source_snapshot_id"]],
        "fingerprints": {
            "source_payload": source_package["fingerprints"]["source_payload"],
            "source_package_manifest": source_package["fingerprints"]["package_manifest"],
        },
        "classification": metadata["classification"],
        "reproducibility": {
            "state": source_package["reproducibility"]["state"],
            "handle": source_package["reproducibility"]["handle"],
            "nondeterminism": source_package["reproducibility"]["nondeterminism"],
        },
    }


def construct_evidence_evaluation(source_package: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    payload = source_package["evidence_payload"]
    evidence_ref_id = evidence["evidence_ref_id"]
    return {
        "stage": "evidence_evaluation",
        "evaluation_id": "eval-" + source_package["source_evidence_package_id"],
        "evidence_ref_id": evidence_ref_id,
        "evaluation_type": "source_fixture_contract_evaluation",
        "evaluation_statement": "The immutable source evidence package supports a factual coverage statement within the fixture scope.",
        "dimensions": {
            "validity": "valid for fixture contract",
            "freshness": source_package["provenance"]["source_snapshot_date"],
            "source_family": source_package["source_identity"]["source_family"],
            "data_lineage": "source snapshot retained",
            "reproducibility": source_package["reproducibility"]["state"],
            "contradiction_handling": "none recorded in fixture",
            "uncertainty": "limited to fixture scope",
            "missingness": "none declared for fixture scope",
            "auditability": "canonical fingerprints available",
        },
        "uncertainty": {"scope": "fixture-only", "limitations": ["single immutable package"]},
        "contradictions": [
            {
                "contradiction_id": "none-recorded",
                "contradiction_type": "none",
                "disposition": "not_applicable",
            }
        ],
        "evidence_references": [evidence_ref_id],
        "provenance": {
            "source_package_id": source_package["source_evidence_package_id"],
            "source_payload_fingerprint": source_package["fingerprints"]["source_payload"],
        },
        "fingerprints": {
            "evaluation_input": sha256_fingerprint({"evidence": evidence, "payload": payload}),
            "evaluation_statement": sha256_fingerprint("The immutable source evidence package supports a factual coverage statement within the fixture scope."),
        },
        "reproducibility": {
            "state": "reproducible",
            "handle": source_package["reproducibility"]["handle"],
        },
    }


def _evidence_reference_for_package(source_package: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_ref_id": evidence["evidence_ref_id"],
        "evidence_class": evidence["evidence_class"],
        "source_family": evidence["source_family"],
        "source_identity": evidence["source_identity"],
        "source_owner": "source package fixture",
        "source_version": source_package["package_version"],
        "accessed_at": DATE,
        "snapshot_fingerprint": source_package["fingerprints"]["package_manifest"],
        "reproducibility_handle": source_package["reproducibility"]["handle"],
        "evaluation_status": "evaluated",
    }


def _base_package(source_package: dict[str, Any], evidence: dict[str, Any], evaluation: dict[str, Any], kind: str, package_id: str, status: str) -> dict[str, Any]:
    payload = source_package["evidence_payload"]
    statement = {
        "statement_id": "stmt-" + source_package["source_evidence_package_id"],
        "statement_type": payload["knowledge_category"],
        "text": payload["factual_statement"],
        "applicability": payload["scope"],
        "dependencies": [evidence["evidence_ref_id"], evaluation["evaluation_id"]],
        "evidence_refs": [evidence["evidence_ref_id"]],
        "origin": "constructed_from_source_evidence_package",
    }
    evidence_refs = [_evidence_reference_for_package(source_package, evidence)]
    computation_method = {
        "name": "source_evidence_package_to_knowledge_package_v1",
        "version": "1.0",
        "recipe": "deterministically preserve constitutionally permitted factual statement and provenance",
        "parameters": {},
        "query_definitions": [],
        "nondeterminism": "none",
        "rerun": "python3 tools/construct_knowledge_package_v1.py tests/fixtures/package_construction_v1/valid_source_evidence_package.json",
    }
    provenance = {
        "package_identity": package_id,
        "creator": "construct_knowledge_package_v1",
        "generation_date": DATE,
        "source_systems": ["immutable SourceEvidencePackage fixture"],
        "evidence_refs": [evidence["evidence_ref_id"]],
        "evaluation_refs": [evaluation["evaluation_id"]],
        "computation_recipe": "source_evidence_package_to_knowledge_package_v1@1.0",
        "validation_tool": "validate_knowledge_pipeline_v1",
        "reproducibility_state": "reproducible",
    }
    common_without_fingerprints = {
        "package_id": package_id,
        "package_kind": kind,
        "package_version": "1.0",
        "created_at": DATE,
        "created_by": "construct_knowledge_package_v1",
        "status": status,
        "scope": {
            "domain": payload["scope"].get("domain"),
            "source_scope": payload["scope"],
            "evidence_family": source_package["source_identity"]["source_family"],
            "method_scope": "deterministic construction validation",
            "intended_use": "pre-production validation only",
        },
        "input_references": [source_package["source_evidence_package_id"]],
        "evidence_references": evidence_refs,
        "computation_method": computation_method,
        "generated_statements": [statement],
        "confidence_quality": {
            "confidence_label": "fixture-supported",
            "uncertainty_dimensions": ["fixture_scope"],
            "missingness_summary": "none declared for fixture scope",
            "evidence_sufficiency": "sufficient for deterministic construction validation",
            "reproducibility_state": "reproducible",
            "validation_state": "pass" if kind == "KnowledgeObjectPackage" else "validated",
            "governance_review_state": "pre-production validation",
            "lifecycle_state": "accepted" if kind == "KnowledgeObjectPackage" else "candidate",
        },
        "contradiction_records": [
            {
                "contradiction_id": "none-recorded",
                "target_statement": statement["statement_id"],
                "contradiction_type": "none",
                "contradicting_evidence": None,
                "disposition": "not_applicable",
            }
        ],
        "provenance_envelope": provenance,
        "validation_state": {
            "validation_result": "pass" if kind == "KnowledgeObjectPackage" else "pending",
            "validator_version": "v1",
            "blockers": [],
            "warnings": [],
            "human_review_required": kind != "KnowledgeObjectPackage",
        },
        "evolution_metadata": {
            "previous_revision": None,
            "change_reason": "initial deterministic construction validation",
            "changed_inputs_methods_templates_models_validators": [],
            "dependent_object_review_posture": "not_applicable",
        },
    }
    fingerprints = {
        "input_set": sha256_fingerprint(common_without_fingerprints["input_references"]),
        "evidence_references": sha256_fingerprint(evidence_refs),
        "query_definitions": sha256_fingerprint(computation_method["query_definitions"]),
        "computation_recipe": sha256_fingerprint(computation_method),
        "generated_statements": sha256_fingerprint([statement]),
        "package_manifest": sha256_fingerprint(common_without_fingerprints),
    }
    package = copy.deepcopy(common_without_fingerprints)
    package["fingerprints"] = fingerprints
    return package


def construct_candidate(source_package: dict[str, Any], evidence: dict[str, Any], evaluation: dict[str, Any]) -> dict[str, Any]:
    return _base_package(
        source_package,
        evidence,
        evaluation,
        "KnowledgeCandidatePackage",
        "pkg-candidate-" + source_package["source_evidence_package_id"],
        "validated",
    )


def construct_object(source_package: dict[str, Any], evidence: dict[str, Any], evaluation: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    obj = _base_package(
        source_package,
        evidence,
        evaluation,
        "KnowledgeObjectPackage",
        "pkg-object-" + source_package["source_evidence_package_id"],
        "accepted-for-controlled-production-readiness",
    )
    obj["promotion"] = {
        "from_candidate_package_id": candidate["package_id"],
        "promotion_justification": "Candidate passed deterministic construction validation for pre-production readiness.",
        "validation_history": [candidate["validation_state"], obj["validation_state"]],
        "maturity_state": "M4 controlled-readiness validated fixture",
    }
    obj["evidence_integrity"] = {
        "evidence_refs_verified": True,
        "fingerprints_verified": True,
        "source_package_fingerprint": source_package["fingerprints"]["package_manifest"],
    }
    obj["lineage"] = {
        "previous_package_id": candidate["package_id"],
        "version_lineage": [candidate["package_id"], obj["package_id"]],
        "lineage_fingerprint": sha256_fingerprint({"candidate": candidate["fingerprints"], "object": obj["fingerprints"]}),
    }
    # Recompute manifest after promotion/evidence_integrity/lineage additions.
    obj["fingerprints"]["package_manifest"] = sha256_fingerprint({k: v for k, v in obj.items() if k != "fingerprints"})
    return obj


def verify_knowledge_boundary(package: dict[str, Any]) -> dict[str, Any]:
    blockers: list[dict[str, Any]] = []
    if contains_forbidden_boundary_language(package):
        blockers.append(finding("constitutional_boundary", "knowledge package contains forbidden interpretation or action language", "package"))
    for idx, statement in enumerate(package.get("generated_statements", [])):
        statement_type = statement.get("statement_type")
        if statement_type not in SUPPORTED_KNOWLEDGE_CATEGORIES:
            blockers.append(finding("constitutional_boundary", f"unsupported statement_type: {statement_type}", f"generated_statements[{idx}].statement_type"))
    return report("knowledge_boundary", blockers)


def construct_pipeline(source_package: dict[str, Any]) -> dict[str, Any]:
    source_validation = validate_source_evidence_package(source_package)
    if not source_validation["ok"]:
        return {"source_validation": source_validation}
    evidence = construct_evidence(source_package)
    evaluation = construct_evidence_evaluation(source_package, evidence)
    candidate = construct_candidate(source_package, evidence, evaluation)
    obj = construct_object(source_package, evidence, evaluation, candidate)
    boundary = verify_knowledge_boundary(obj)
    pipeline_payload = {
        "source": source_package,
        "evidence": evidence,
        "evidence_evaluation": evaluation,
        "knowledge_candidate_package": candidate,
        "knowledge_object_package": obj,
        "knowledge_boundary": boundary,
    }
    pipeline_fingerprint = sha256_fingerprint(pipeline_payload)
    return {
        "source_validation": source_validation,
        "evidence": evidence,
        "evidence_evaluation": evaluation,
        "knowledge_candidate_package": candidate,
        "knowledge_object_package": obj,
        "knowledge_boundary": boundary,
        "determinism": {
            "pipeline_fingerprint": pipeline_fingerprint,
            "identical_replay": True,
            "nondeterminism": "none",
        },
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Construct KnowledgeForge packages from an immutable Source Evidence Package fixture")
    parser.add_argument("path")
    args = parser.parse_args()
    with open(args.path, encoding="utf-8") as fh:
        source_package = json.load(fh)
    print(json.dumps(construct_pipeline(source_package), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
