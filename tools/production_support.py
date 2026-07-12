#!/usr/bin/env python3
"""Small deterministic production support helpers for KnowledgeForge campaigns.

This module is deliberately narrow. It consolidates only the repeated mechanics
proven by PEL-008 and PEL-009:

- construction of existing SourceEvidencePackage dictionaries;
- aggregation of common production-quality metrics.

It does not define a new package model, validator, workflow, persistence layer,
registry, schema, adapter, or framework.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Callable


def ratio(numerator: int | float, denominator: int | float) -> float:
    return 0.0 if denominator == 0 else round(numerator / denominator, 6)


def report_dict(value: Any) -> dict[str, Any]:
    return value.to_dict() if hasattr(value, "to_dict") else value


def build_source_evidence_package(
    *,
    package_id: str,
    statement: str,
    category: str,
    created_at: str,
    source_name: str,
    source_family: str,
    source_version: str,
    scope: dict[str, Any],
    payload_metadata: dict[str, Any],
    evidence_class: str,
    classification: dict[str, Any],
    validation_metadata: dict[str, Any],
    provenance: dict[str, Any],
    reproducibility: dict[str, Any],
    fingerprint_builder: Callable[[dict[str, Any]], dict[str, str]],
) -> dict[str, Any]:
    """Build the existing SourceEvidencePackage shape and attach fingerprints.

    All campaign-specific meaning remains explicit at the call site. The helper
    only assembles the already-established package dictionary and applies the
    existing fingerprint builder.
    """
    package = {
        "source_evidence_package_id": package_id,
        "package_kind": "SourceEvidencePackage",
        "package_version": "1.0",
        "created_at": created_at,
        "immutability": {"state": "immutable_fixture", "mutation_policy": "read_only"},
        "source_identity": {
            "source_name": source_name,
            "source_family": source_family,
            "source_version": source_version,
        },
        "evidence_payload": {
            "knowledge_category": category,
            "factual_statement": statement,
            "scope": scope,
            "payload_metadata": payload_metadata,
        },
        "evidence_metadata": {
            "evidence_class": evidence_class,
            "classification": classification,
            "validation_metadata": validation_metadata,
        },
        "provenance": provenance,
        "reproducibility": reproducibility,
    }
    package["fingerprints"] = fingerprint_builder(package)
    return package


def aggregate_common_quality_metrics(
    *,
    campaign_id: str,
    source_packages: list[dict[str, Any]],
    knowledge_candidates: list[dict[str, Any]],
    accepted_objects: list[dict[str, Any]],
    rejected_records: list[dict[str, Any]],
    validation_records: list[dict[str, Any]],
    determinism_verified: bool,
    fingerprint_stability: bool,
    duplicate_knowledge_objects_detected: bool,
) -> dict[str, Any]:
    """Aggregate the common production-quality metrics used by campaigns 1-3."""
    accepted_count = len(accepted_objects)
    rejected_count = len(rejected_records)
    total_candidates = accepted_count + rejected_count
    category_counts = dict(sorted(Counter(
        obj["generated_statements"][0]["statement_type"] for obj in accepted_objects
    ).items()))
    rejected_category_counts = dict(sorted(Counter(
        (
            r.get("source_evidence_package")
            or r.get("source")
            or {"evidence_payload": {}}
        ).get("evidence_payload", {}).get("knowledge_category", "missing")
        for r in rejected_records
    ).items()))
    failure_counts = dict(sorted(Counter(
        category
        for record in rejected_records
        for category in record.get("reason_categories", [])
    ).items()))
    avg_evidence_refs = ratio(
        sum(len(obj.get("evidence_references", [])) for obj in accepted_objects),
        accepted_count,
    )
    provenance_complete = all(
        bool(obj.get("provenance_envelope"))
        for obj in accepted_objects
    )
    return {
        "campaign_id": campaign_id,
        "source_evidence_packages_processed": len(source_packages),
        "knowledge_candidate_packages_generated": len(knowledge_candidates),
        "knowledge_object_packages_accepted": accepted_count,
        "rejected_candidates": rejected_count,
        "acceptance_rate": ratio(accepted_count, total_candidates),
        "rejection_rate": ratio(rejected_count, total_candidates),
        "knowledge_categories_produced": category_counts,
        "knowledge_categories_rejected": rejected_category_counts,
        "average_evidence_references_per_knowledge_object": avg_evidence_refs,
        "validator_failures_by_category": failure_counts,
        "provenance_completeness": provenance_complete,
        "fingerprint_stability": fingerprint_stability,
        "determinism_verification": determinism_verified,
        "duplicate_knowledge_objects_detected": duplicate_knowledge_objects_detected,
    }
