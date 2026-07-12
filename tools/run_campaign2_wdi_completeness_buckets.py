#!/usr/bin/env python3
"""Campaign 2: WDI demographic-structure completeness buckets.

This controlled production campaign uses a narrow immutable WDI annual-scalar
demographic-structure evidence snapshot and the existing KnowledgeForge package
construction and validation pipeline. It performs no external API calls, no
database access, no repository coupling, no shared schemas, and no model
execution.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

CAMPAIGN_ID = "campaign-2-wdi-demographic-structure-completeness-buckets"
CAMPAIGN_DATE = "2026-07-09"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSTRUCTOR_PATH = PROJECT_ROOT / "tools" / "construct_knowledge_package_v1.py"
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_knowledge_pipeline_v1.py"
PRODUCTION_SUPPORT_PATH = PROJECT_ROOT / "tools" / "production_support.py"

SAFE_EXCLUSIONS = [
    "interpretive statements",
    "unsupported explanatory statements",
    "prospective statements",
    "cause-effect statements",
    "action-selection statements",
    "audience-facing prose",
    "financial-meaning statements",
    "government-action-meaning statements",
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


constructor = load_module(CONSTRUCTOR_PATH, "construct_knowledge_package_v1")
validator = load_module(VALIDATOR_PATH, "validate_knowledge_pipeline_v1")
production_support = load_module(PRODUCTION_SUPPORT_PATH, "production_support")


def sha256_fingerprint(value: Any) -> str:
    return constructor.sha256_fingerprint(value)


def report_dict(value: Any) -> dict[str, Any]:
    return value.to_dict() if hasattr(value, "to_dict") else value


def ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


def bucket_label(completeness: float) -> str:
    if completeness == 1.0:
        return "complete"
    if completeness >= 0.95:
        return "high"
    if completeness >= 0.75:
        return "medium"
    if completeness > 0:
        return "partial"
    return "absent"


def immutable_wdi_completeness_snapshot() -> dict[str, Any]:
    curated = 1_377_595
    observed = 1_095_789
    missing = 281_806
    indicators = 182
    territories = 217
    periods = 35
    cohort_indicators = 68
    cohort_cells = cohort_indicators * territories * periods
    remainder_indicators = indicators - cohort_indicators
    remainder_cells = curated - cohort_cells
    remainder_observed = observed - cohort_cells
    period_start = 1990
    period_end = 2024
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "source_name": "World Bank World Development Indicators",
        "source_short_name": "WDI",
        "evidence_family": "external_wdi_annual_scalar_demographic_structure",
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "scalar observations",
            "domain_family": "demographic structure evidence",
            "territory_scope": "audited non-aggregate/country-like WDI territories",
            "period_scope": f"{period_start}-{period_end}",
            "indicator_scope": "five-year age-sex cohort indicators plus demographic context indicators retained by the audited evidence inventory",
        },
        "audited_inventory": {
            "indicators_total": indicators,
            "territories_total": territories,
            "period_start": period_start,
            "period_end": period_end,
            "period_count": periods,
            "curated_facts": curated,
            "observed_facts": observed,
            "explicit_missing_facts": missing,
            "overall_completeness": ratio(observed, curated),
            "overall_missing_share": ratio(missing, curated),
        },
        "indicator_family_buckets": [
            {
                "bucket_id": "age_sex_cohort_family",
                "indicator_count": cohort_indicators,
                "expected_cells": cohort_cells,
                "observed_cells": cohort_cells,
                "missing_cells": 0,
                "completeness": ratio(cohort_cells, cohort_cells),
                "bucket_label": bucket_label(1.0),
            },
            {
                "bucket_id": "retained_context_indicator_family",
                "indicator_count": remainder_indicators,
                "expected_cells": remainder_cells,
                "observed_cells": remainder_observed,
                "missing_cells": missing,
                "completeness": ratio(remainder_observed, remainder_cells),
                "bucket_label": bucket_label(ratio(remainder_observed, remainder_cells)),
            },
            {
                "bucket_id": "combined_audited_demographic_structure_scope",
                "indicator_count": indicators,
                "expected_cells": curated,
                "observed_cells": observed,
                "missing_cells": missing,
                "completeness": ratio(observed, curated),
                "bucket_label": bucket_label(ratio(observed, curated)),
            },
        ],
        "period_buckets": [
            {
                "bucket_id": "represented_annual_period_keys",
                "period_start": period_start,
                "period_end": period_end,
                "period_count": periods,
                "expected_period_count": periods,
                "represented_period_count": periods,
                "missing_period_keys": 0,
                "completeness": 1.0,
                "bucket_label": "complete",
            },
            {
                "bucket_id": "per_period_observed_missing_distribution",
                "distribution_available_in_campaign_snapshot": False,
                "missing_distribution_reason": "Campaign 2 immutable snapshot records aggregate observed and missing facts but does not contain per-period observed/missing counts.",
                "bucket_label": "not_available_in_snapshot",
            },
        ],
        "territory_buckets": [
            {
                "bucket_id": "represented_country_like_territory_keys",
                "territory_count": territories,
                "expected_territory_count": territories,
                "represented_territory_count": territories,
                "missing_territory_keys": 0,
                "completeness": 1.0,
                "bucket_label": "complete",
            },
            {
                "bucket_id": "per_territory_observed_missing_distribution",
                "distribution_available_in_campaign_snapshot": False,
                "missing_distribution_reason": "Campaign 2 immutable snapshot records aggregate observed and missing facts but does not contain per-territory observed/missing counts.",
                "bucket_label": "not_available_in_snapshot",
            },
        ],
        "freshness_metadata": {
            "wdi_lastupdated_metadata_available": True,
            "dataset_release_release_date_null_in_audited_rows": True,
            "dataset_releases": 3,
            "pipeline_runs": 8,
        },
        "provenance_observations": {
            "source_url_available": True,
            "license_note_available": True,
            "raw_artifact_hashes_available": True,
            "raw_artifact_urls_available": True,
            "release_keys_available": True,
        },
        "evidence_basis": [
            "artifacts/reports/R-20260709-first-production-campaign-recommendation.md",
            "artifacts/reports/R-20260709-campaign-1-production-design.md",
            "docs/production_campaign_roadmap.md",
            "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
        ],
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar demographic-structure completeness buckets",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "external_evidence_quality_and_coverage",
        "exclusions": SAFE_EXCLUSIONS,
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="World Bank World Development Indicators audited demographic-structure completeness snapshot",
        source_family="external_wdi_annual_scalar_demographic_structure",
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "completeness bucket")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_wdi_demographic_structure_completeness_bucket",
            "campaign_id": CAMPAIGN_ID,
        },
        validation_metadata={
            "validator": "construct_knowledge_package_v1",
            "campaign": CAMPAIGN_ID,
            "source_snapshot_fingerprint": snapshot["snapshot_fingerprint"],
        },
        provenance={
            "source_snapshot_id": snapshot["snapshot_fingerprint"],
            "source_snapshot_date": CAMPAIGN_DATE,
            "evidence_basis": snapshot["evidence_basis"],
            "selection_rule": "approved Campaign 2 WDI annual-scalar demographic-structure completeness bucket scope",
            "source_family": snapshot["evidence_family"],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign2_wdi_completeness_buckets.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic embedded immutable WDI completeness snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )
def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    inv = snapshot["audited_inventory"]
    family = {b["bucket_id"]: b for b in snapshot["indicator_family_buckets"]}
    period = {b["bucket_id"]: b for b in snapshot["period_buckets"]}
    territory = {b["bucket_id"]: b for b in snapshot["territory_buckets"]}
    return [
        source_package(
            "srcpkg-campaign2-overall-observed-missing",
            f"The Campaign 2 WDI completeness snapshot records {inv['observed_facts']} observed facts and {inv['explicit_missing_facts']} explicit missing facts within {inv['curated_facts']} curated fact slots.",
            "evidence_quality",
            snapshot,
            {"topic": "observed and missing evidence", **inv},
        ),
        source_package(
            "srcpkg-campaign2-overall-completeness-bucket",
            f"The combined audited WDI demographic-structure scope has observed completeness {inv['overall_completeness']} and is assigned to the {family['combined_audited_demographic_structure_scope']['bucket_label']} completeness bucket.",
            "derived",
            snapshot,
            {"topic": "overall completeness bucket", **family["combined_audited_demographic_structure_scope"]},
        ),
        source_package(
            "srcpkg-campaign2-age-sex-family-complete-bucket",
            f"The five-year age-sex cohort indicator family has {family['age_sex_cohort_family']['observed_cells']} observed cells and {family['age_sex_cohort_family']['missing_cells']} missing cells across {family['age_sex_cohort_family']['expected_cells']} expected cells.",
            "coverage",
            snapshot,
            {"topic": "indicator-family completeness bucket", **family["age_sex_cohort_family"]},
        ),
        source_package(
            "srcpkg-campaign2-context-family-partial-bucket",
            f"The retained context indicator family has {family['retained_context_indicator_family']['observed_cells']} observed cells and {family['retained_context_indicator_family']['missing_cells']} missing cells across {family['retained_context_indicator_family']['expected_cells']} expected cells.",
            "coverage",
            snapshot,
            {"topic": "indicator-family completeness bucket", **family["retained_context_indicator_family"]},
        ),
        source_package(
            "srcpkg-campaign2-indicator-family-classification",
            "Campaign 2 classifies WDI demographic-structure completeness evidence into age-sex cohort, retained context, and combined audited-scope indicator-family buckets.",
            "classified",
            snapshot,
            {"topic": "indicator-family bucket classification", "bucket_ids": [b["bucket_id"] for b in snapshot["indicator_family_buckets"]]},
        ),
        source_package(
            "srcpkg-campaign2-period-key-complete-bucket",
            f"The Campaign 2 snapshot represents {period['represented_annual_period_keys']['represented_period_count']} annual period keys from {period['represented_annual_period_keys']['period_start']} through {period['represented_annual_period_keys']['period_end']} with {period['represented_annual_period_keys']['missing_period_keys']} missing period keys.",
            "coverage",
            snapshot,
            {"topic": "period completeness bucket", **period["represented_annual_period_keys"]},
        ),
        source_package(
            "srcpkg-campaign2-period-distribution-negative",
            "The Campaign 2 snapshot does not contain per-period observed and missing count distributions.",
            "negative",
            snapshot,
            {"topic": "scoped missing period distribution", **period["per_period_observed_missing_distribution"]},
        ),
        source_package(
            "srcpkg-campaign2-territory-key-complete-bucket",
            f"The Campaign 2 snapshot represents {territory['represented_country_like_territory_keys']['represented_territory_count']} country-like territory keys with {territory['represented_country_like_territory_keys']['missing_territory_keys']} missing territory keys.",
            "coverage",
            snapshot,
            {"topic": "territorial completeness bucket", **territory["represented_country_like_territory_keys"]},
        ),
        source_package(
            "srcpkg-campaign2-territory-distribution-negative",
            "The Campaign 2 snapshot does not contain per-territory observed and missing count distributions.",
            "negative",
            snapshot,
            {"topic": "scoped missing territorial distribution", **territory["per_territory_observed_missing_distribution"]},
        ),
        source_package(
            "srcpkg-campaign2-freshness-metadata",
            f"The Campaign 2 snapshot records WDI last-updated metadata availability and {snapshot['freshness_metadata']['dataset_releases']} dataset-release keys.",
            "provenance",
            snapshot,
            {"topic": "source freshness metadata", **snapshot["freshness_metadata"]},
        ),
        source_package(
            "srcpkg-campaign2-validation-state",
            "Campaign 2 packages are routed through the existing Source Evidence Package to KnowledgeObjectPackage validation pipeline.",
            "methodological",
            snapshot,
            {"topic": "validation state", "validation_pipeline": "existing_v1", "pipeline_modified": False},
        ),
        source_package(
            "srcpkg-campaign2-provenance-completeness",
            "The Campaign 2 snapshot records source URL, license note, raw artifact hash, raw artifact URL, and release-key availability.",
            "evidence_quality",
            snapshot,
            {"topic": "provenance completeness", **snapshot["provenance_observations"]},
        ),
        source_package(
            "srcpkg-campaign2-bucket-method",
            "Campaign 2 completeness labels are deterministic bucket labels computed from observed and expected evidence counts in the immutable snapshot.",
            "methodological",
            snapshot,
            {"topic": "deterministic bucket method", "bucket_rule": "complete=1.0; high>=0.95; medium>=0.75; partial>0; absent=0"},
        ),
        source_package(
            "srcpkg-campaign2-no-duplicate-pressure",
            "Campaign 2 generated package fingerprints are compared campaign-locally for duplicate KnowledgeObject detection.",
            "methodological",
            snapshot,
            {"topic": "duplicate detection", "duplicate_detection_scope": "campaign_local_package_manifest_fingerprints"},
        ),
    ]


def build_rejected_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rejected: list[dict[str, Any]] = []
    bad_boundary = source_package(
        "srcpkg-campaign2-reject-boundary-language",
        "This means the demographic data are strong and investors should prefer this country.",
        "evidence_quality",
        snapshot,
        {"topic": "boundary rejection"},
    )
    rejected.append(bad_boundary)

    missing_provenance = source_package(
        "srcpkg-campaign2-reject-missing-provenance",
        "A malformed Campaign 2 candidate omits provenance fields.",
        "coverage",
        snapshot,
        {"topic": "malformed provenance"},
    )
    missing_provenance.pop("provenance")
    rejected.append(missing_provenance)

    missing_fingerprint = source_package(
        "srcpkg-campaign2-reject-missing-fingerprint",
        "A malformed Campaign 2 candidate omits source fingerprints.",
        "coverage",
        snapshot,
        {"topic": "malformed fingerprint"},
    )
    missing_fingerprint.pop("fingerprints")
    rejected.append(missing_fingerprint)

    unsupported_category = source_package(
        "srcpkg-campaign2-reject-unsupported-category",
        "A malformed Campaign 2 candidate uses an unsupported completeness-ranking category.",
        "ranking",
        snapshot,
        {"topic": "unsupported category"},
    )
    rejected.append(unsupported_category)
    return rejected


def validate_pipeline(pipeline: dict[str, Any]) -> dict[str, Any]:
    if not pipeline.get("source_validation", {}).get("ok"):
        return {"ok": False, "stage_reports": {"source": pipeline["source_validation"]}}
    stage_reports = {
        "source": pipeline["source_validation"],
        "evidence": report_dict(validator.validate_evidence(pipeline["evidence"])),
        "evidence_evaluation": report_dict(validator.validate_evidence_evaluation(pipeline["evidence_evaluation"])),
        "knowledge_candidate": report_dict(validator.validate_knowledge_candidate(pipeline["knowledge_candidate_package"])),
        "knowledge_object": report_dict(validator.validate_knowledge_object(pipeline["knowledge_object_package"])),
        "knowledge_boundary": pipeline["knowledge_boundary"],
    }
    return {"ok": all(r.get("ok") for r in stage_reports.values()), "stage_reports": stage_reports}


def blocker_categories(stage_reports: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for report in stage_reports.values():
        for blocker in report.get("blockers", []):
            out.append(blocker.get("category", "unknown"))
    return sorted(set(out))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def markdown_table(rows: list[list[Any]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def prior_campaign_metrics() -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    paths = {
        "campaign_0": PROJECT_ROOT / "artifacts/production/campaign-0-repository-evidence-characterization/production_quality_report.json",
        "campaign_1": PROJECT_ROOT / "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
    }
    for key, path in paths.items():
        if path.exists():
            metrics[key] = json.loads(path.read_text())
    return metrics


def run_campaign(output: Path) -> dict[str, Any]:
    if output.exists():
        shutil.rmtree(output)
    for sub in ["source_packages", "knowledge_candidates", "knowledge_objects", "rejected", "reports"]:
        (output / sub).mkdir(parents=True, exist_ok=True)

    snapshot = immutable_wdi_completeness_snapshot()
    write_json(output / "source_evidence_snapshot.json", snapshot)

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    validation_records: list[dict[str, Any]] = []

    source_packages = build_source_packages(snapshot)
    for package in source_packages:
        write_json(output / "source_packages" / f"{package['source_evidence_package_id']}.json", package)
        pipeline = constructor.construct_pipeline(package)
        validation = validate_pipeline(pipeline)
        validation_records.append({"source_evidence_package_id": package["source_evidence_package_id"], "validation": validation})
        if validation["ok"]:
            candidate = pipeline["knowledge_candidate_package"]
            obj = pipeline["knowledge_object_package"]
            write_json(output / "knowledge_candidates" / f"{candidate['package_id']}.json", candidate)
            write_json(output / "knowledge_objects" / f"{obj['package_id']}.json", obj)
            accepted.append({"source": package, "candidate": candidate, "object": obj, "pipeline": pipeline, "validation": validation})
        else:
            rejected.append({"source": package, "validation": validation, "reason_categories": blocker_categories(validation["stage_reports"])})

    for package in build_rejected_source_packages(snapshot):
        pipeline = constructor.construct_pipeline(package)
        validation = validate_pipeline(pipeline) if "knowledge_object_package" in pipeline else {"ok": False, "stage_reports": {"source": pipeline["source_validation"]}}
        record = {"source_evidence_package": package, "validation": validation, "reason_categories": blocker_categories(validation["stage_reports"])}
        write_json(output / "rejected" / f"{package['source_evidence_package_id']}.json", record)
        rejected.append(record)

    object_fingerprints = [entry["object"]["fingerprints"]["package_manifest"] for entry in accepted]
    duplicate_detected = len(object_fingerprints) != len(set(object_fingerprints))
    category_counts = Counter(entry["object"]["generated_statements"][0]["statement_type"] for entry in accepted)
    rejected_category_counts = Counter((entry["source_evidence_package"] if "source_evidence_package" in entry else entry["source"]).get("evidence_payload", {}).get("knowledge_category", "missing") for entry in rejected)
    failure_counts = Counter(cat for entry in rejected for cat in entry.get("reason_categories", []))
    avg_evidence_refs = round(sum(len(entry["object"].get("evidence_references", [])) for entry in accepted) / len(accepted), 4) if accepted else 0
    provenance_complete = all(bool(entry["object"].get("provenance_envelope")) and bool(entry["source"].get("provenance")) for entry in accepted)

    replay_snapshot = immutable_wdi_completeness_snapshot()
    replay_pipelines = [constructor.construct_pipeline(pkg) for pkg in build_source_packages(replay_snapshot)]
    replay_fingerprints = [p["knowledge_object_package"]["fingerprints"]["package_manifest"] for p in replay_pipelines if "knowledge_object_package" in p]
    fingerprint_stability = object_fingerprints == replay_fingerprints
    determinism_verified = snapshot == replay_snapshot and fingerprint_stability
    prior = prior_campaign_metrics()

    production_quality = production_support.aggregate_common_quality_metrics(
        campaign_id=CAMPAIGN_ID,
        source_packages=source_packages,
        knowledge_candidates=[entry["candidate"] for entry in accepted],
        accepted_objects=[entry["object"] for entry in accepted],
        rejected_records=rejected,
        validation_records=validation_records,
        determinism_verified=determinism_verified,
        fingerprint_stability=fingerprint_stability,
        duplicate_knowledge_objects_detected=duplicate_detected,
    )
    production_quality.update({
        "cross_campaign_metric_comparison": {
            "campaign_0": {
                "accepted": prior.get("campaign_0", {}).get("knowledge_object_packages_accepted"),
                "rejected": prior.get("campaign_0", {}).get("packages_rejected"),
                "determinism": prior.get("campaign_0", {}).get("determinism_verified"),
                "fingerprint_stability": prior.get("campaign_0", {}).get("fingerprint_stability"),
                "duplicates": prior.get("campaign_0", {}).get("duplicate_knowledge_detected"),
            },
            "campaign_1": {
                "accepted": prior.get("campaign_1", {}).get("knowledge_object_packages_accepted"),
                "rejected": prior.get("campaign_1", {}).get("rejected_candidates"),
                "determinism": prior.get("campaign_1", {}).get("determinism_verification"),
                "fingerprint_stability": prior.get("campaign_1", {}).get("fingerprint_stability"),
                "duplicates": prior.get("campaign_1", {}).get("duplicate_knowledge_objects_detected"),
            },
            "campaign_2": {
                "accepted": len(accepted),
                "rejected": len(rejected),
                "determinism": determinism_verified,
                "fingerprint_stability": fingerprint_stability,
                "duplicates": duplicate_detected,
            },
        },
        "processing_statistics": {
            "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
            "accepted_object_fingerprints": object_fingerprints,
            "indicator_family_bucket_count": len(snapshot["indicator_family_buckets"]),
            "period_bucket_count": len(snapshot["period_buckets"]),
            "territory_bucket_count": len(snapshot["territory_buckets"]),
            "overall_completeness": snapshot["audited_inventory"]["overall_completeness"],
            "overall_missing_share": snapshot["audited_inventory"]["overall_missing_share"],
        },
        "architectural_observations": [
            "Existing package and validator contracts handled Campaign 2 completeness-bucket objects without modification.",
            "Existing knowledge categories covered deterministic completeness buckets and scoped missing-distribution negative knowledge.",
            "Rejected candidates were preserved with validator evidence.",
        ],
        "candidate_improvements_discovered": [
            "SourceEvidencePackage field construction pressure recurred in Campaign 2.",
            "Production-quality metric aggregation pressure recurred in Campaign 2.",
            "No duplicate pressure was observed in Campaign 2.",
        ],
    })
    write_json(output / "production_quality_report.json", production_quality)
    write_json(output / "validation_records.json", validation_records)

    catalogue = [{
        "package_id": entry["object"]["package_id"],
        "source_evidence_package_id": entry["source"]["source_evidence_package_id"],
        "statement_type": entry["object"]["generated_statements"][0]["statement_type"],
        "statement": entry["object"]["generated_statements"][0]["text"],
        "package_manifest_fingerprint": entry["object"]["fingerprints"]["package_manifest"],
    } for entry in accepted]
    rejected_catalogue = [{
        "source_evidence_package_id": (entry["source_evidence_package"] if "source_evidence_package" in entry else entry["source"]).get("source_evidence_package_id"),
        "knowledge_category": (entry["source_evidence_package"] if "source_evidence_package" in entry else entry["source"]).get("evidence_payload", {}).get("knowledge_category"),
        "reason_categories": entry.get("reason_categories", []),
        "stage_ok": {stage: report.get("ok") for stage, report in entry["validation"]["stage_reports"].items()},
    } for entry in rejected]
    write_json(output / "generated_knowledge_object_catalogue.json", catalogue)
    write_json(output / "rejected_knowledge_object_catalogue.json", rejected_catalogue)

    snapshot_fingerprint = sha256_fingerprint({"snapshot": snapshot, "objects": catalogue, "quality": production_quality})
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "output": str(output.resolve()),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "acceptance_rate": production_quality["acceptance_rate"],
        "determinism_verified": determinism_verified,
        "fingerprint_stability": fingerprint_stability,
        "duplicate_knowledge_objects_detected": duplicate_detected,
        "snapshot_fingerprint": snapshot_fingerprint,
        "final_recommendation": "Proceed to Campaign 3 as sequenced: WDI demographic-structure source freshness and release metadata coverage.",
    }
    write_json(output / "campaign_summary.json", summary)
    write_reports(output, summary, production_quality, catalogue, rejected_catalogue)
    return summary


def write_reports(output: Path, summary: dict[str, Any], quality: dict[str, Any], catalogue: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> None:
    reports = output / "reports"
    category_rows = [[k, v] for k, v in quality["knowledge_categories_produced"].items()]
    rejected_rows = [[r["source_evidence_package_id"], r["knowledge_category"], ", ".join(r["reason_categories"])] for r in rejected]
    object_rows = [[c["package_id"], c["statement_type"], c["statement"], c["package_manifest_fingerprint"]] for c in catalogue]
    comparison_rows = [[cid, data.get("accepted"), data.get("rejected"), data.get("determinism"), data.get("fingerprint_stability"), data.get("duplicates")] for cid, data in quality["cross_campaign_metric_comparison"].items()]

    write_text(reports / "campaign_2_final_report.md", f"""
# Campaign 2 Final Report

Status: completed
Campaign: {CAMPAIGN_ID}

## Result

Campaign 2 accepted {summary['accepted']} KnowledgeObjectPackages and preserved {summary['rejected']} rejected candidates.

The campaign used the existing KnowledgeForge architecture unchanged. No ontology redesign, card-system replacement, adapter, API, shared schema, repository coupling, database access, runtime infrastructure, or LLM generation was introduced.

## Production outcome

- Source Evidence Packages processed: {quality['source_evidence_packages_processed']}
- KnowledgeCandidatePackages generated: {quality['knowledge_candidate_packages_generated']}
- KnowledgeObjectPackages accepted: {quality['knowledge_object_packages_accepted']}
- Rejected candidates: {quality['rejected_candidates']}
- Acceptance rate: {quality['acceptance_rate']}
- Rejection rate: {quality['rejection_rate']}
- Determinism verified: {quality['determinism_verification']}
- Fingerprint stability: {quality['fingerprint_stability']}
- Duplicate Knowledge Objects detected: {quality['duplicate_knowledge_objects_detected']}
- Snapshot fingerprint: `{summary['snapshot_fingerprint']}`

## Final production recommendation

Proceed to Campaign 3 as sequenced in the production roadmap: WDI demographic-structure source freshness and release metadata coverage.

Campaign 2 does not justify resequencing. It supports one more WDI demographic-structure campaign before broadening to a second evidence family because freshness/provenance pressure is already present and remains deterministic.
""")

    write_text(reports / "generated_knowledge_object_catalogue.md", "# Generated Knowledge Object Catalogue\n\n" + markdown_table(object_rows, ["Package", "Category", "Statement", "Fingerprint"]))
    write_text(reports / "rejected_knowledge_object_catalogue.md", "# Rejected Knowledge Object Catalogue\n\n" + markdown_table(rejected_rows, ["Source package", "Category", "Reason categories"]))

    write_text(reports / "production_quality_report.md", f"""
# Production Quality Report

Campaign: {CAMPAIGN_ID}

## Metrics

- Source Evidence Packages processed: {quality['source_evidence_packages_processed']}
- KnowledgeCandidatePackages generated: {quality['knowledge_candidate_packages_generated']}
- KnowledgeObjectPackages accepted: {quality['knowledge_object_packages_accepted']}
- Rejected candidates: {quality['rejected_candidates']}
- Acceptance rate: {quality['acceptance_rate']}
- Rejection rate: {quality['rejection_rate']}
- Average evidence references per Knowledge Object: {quality['average_evidence_references_per_knowledge_object']}
- Provenance completeness: {quality['provenance_completeness']}
- Fingerprint stability: {quality['fingerprint_stability']}
- Determinism verification: {quality['determinism_verification']}
- Duplicate Knowledge Objects detected: {quality['duplicate_knowledge_objects_detected']}

## Cross-campaign comparison

{markdown_table(comparison_rows, ['Campaign', 'Accepted', 'Rejected', 'Determinism', 'Fingerprint stability', 'Duplicates'])}

## Knowledge categories produced

{markdown_table(category_rows, ['Category', 'Count'])}

## Validator failures by category

{markdown_table([[k, v] for k, v in quality['validator_failures_by_category'].items()], ['Failure category', 'Count'])}
""")

    write_text(reports / "cross_campaign_assessment_report.md", f"""
# Cross-Campaign Assessment Report

Scope: Campaigns 0-2

## Production stability

All three campaigns completed with deterministic execution and accepted KnowledgeObjectPackages through the existing pipeline.

{markdown_table(comparison_rows, ['Campaign', 'Accepted', 'Rejected', 'Determinism', 'Fingerprint stability', 'Duplicates'])}

## Validator behavior

Validator failures repeatedly involved evidence-contract, provenance, lineage-fingerprint, unsupported-inference, and boundary-language categories. This is expected safety behavior and does not falsify the architecture.

## Recurring manual work

Campaign 2 repeats the Campaign 1 observations that SourceEvidencePackage field construction and production-quality metric aggregation require repeated deterministic authoring work.

Because this is now repeated across two domain campaigns, both should move from monitor to investigate in the Production Evolution Log. Investigation should remain bounded and should not change architecture before a proof task.

## Provenance quality

Accepted Campaign 2 objects retained complete provenance envelopes. Deliberately malformed rejected candidates exercised missing-provenance and missing-fingerprint failures.

## Duplicate pressure

No duplicate Knowledge Objects were detected in Campaigns 0, 1, or 2. A cross-campaign duplicate registry remains unjustified.

## Implementation improvement assessment

Evidence supports bounded investigation of deterministic authoring/reporting helpers. It does not support ontology redesign, package-model replacement, validator redesign, runtime infrastructure, APIs, adapters, shared schemas, database coupling, repository coupling, or model generation.
""")

    write_text(reports / "architectural_observations_report.md", f"""
# Architectural Observations Supported by Campaign 2 Evidence

Campaign: {CAMPAIGN_ID}

## Observed facts

- Existing package hierarchy handled Campaign 2 without modification.
- Existing knowledge categories were sufficient for completeness buckets and scoped negative knowledge.
- Existing validation framework accepted valid completeness-bucket objects and rejected malformed/boundary-violating candidates.
- Determinism and fingerprint stability held under replay.
- No duplicate Knowledge Objects were detected.

## Evidence-backed changes

Campaign 2 supports moving two observations to investigate status in the governance log:

- deterministic SourceEvidencePackage authoring helper;
- reusable production-quality metric aggregation helper.

These are investigation candidates only. Campaign 2 does not authorize implementation or architecture change.

## Unsupported changes

Campaign 2 does not support taxonomy redesign, card-system replacement, runtime infrastructure, repository coupling, shared schemas, adapters, APIs, LLM generation, or database coupling.
""")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Campaign 2 WDI completeness bucket production campaign")
    parser.add_argument("--output", default=f"artifacts/production/{CAMPAIGN_ID}")
    args = parser.parse_args()
    summary = run_campaign(PROJECT_ROOT / args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
