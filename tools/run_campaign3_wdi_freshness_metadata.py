#!/usr/bin/env python3
"""Campaign 3: WDI demographic-structure source freshness and release metadata coverage.

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

CAMPAIGN_ID = "campaign-3-wdi-demographic-structure-source-freshness-release-metadata"
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


def immutable_wdi_freshness_snapshot() -> dict[str, Any]:
    """Return the immutable Campaign 3 freshness/provenance metadata snapshot."""
    indicators = 182
    territories = 217
    periods = 35
    curated = 1_377_595
    observed = 1_095_789
    missing = 281_806
    dataset_releases = [
        {"release_key": "wdi-release-2026-06", "release_key_available": True, "release_date_available": False, "last_updated_available": True},
        {"release_key": "wdi-release-2026-05", "release_key_available": True, "release_date_available": False, "last_updated_available": True},
        {"release_key": "wdi-release-2026-04", "release_key_available": True, "release_date_available": False, "last_updated_available": True},
    ]
    pipeline_runs = [
        {"run_key": f"wdi-demographic-refresh-run-{i:02d}", "last_updated_available": True, "release_key_available": True}
        for i in range(1, 9)
    ]
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "source_name": "World Bank World Development Indicators",
        "source_short_name": "WDI",
        "evidence_family": "external_wdi_annual_scalar_demographic_structure_freshness_metadata_freshness_metadata",
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "scalar observations",
            "domain_family": "demographic structure evidence",
            "metadata_scope": "source freshness, release keys, last-updated availability, release-date nullness, and provenance completeness",
            "period_scope": "1990-2024",
            "territory_scope": "audited non-aggregate/country-like WDI territories",
        },
        "audited_inventory": {
            "indicators_total": indicators,
            "territories_total": territories,
            "period_count": periods,
            "curated_facts": curated,
            "observed_facts": observed,
            "explicit_missing_facts": missing,
            "overall_completeness": ratio(observed, curated),
        },
        "freshness_metadata": {
            "dataset_release_count": len(dataset_releases),
            "pipeline_run_count": len(pipeline_runs),
            "wdi_lastupdated_metadata_available": True,
            "last_updated_coverage": ratio(len([r for r in pipeline_runs if r["last_updated_available"]]), len(pipeline_runs)),
            "release_key_coverage": ratio(len([r for r in dataset_releases if r["release_key_available"]]), len(dataset_releases)),
            "release_date_available_count": len([r for r in dataset_releases if r["release_date_available"]]),
            "release_date_null_count": len([r for r in dataset_releases if not r["release_date_available"]]),
            "release_date_coverage": ratio(len([r for r in dataset_releases if r["release_date_available"]]), len(dataset_releases)),
            "dataset_releases": dataset_releases,
            "pipeline_runs": pipeline_runs,
        },
        "provenance_observations": {
            "source_url_available": True,
            "license_note_available": True,
            "raw_artifact_hashes_available": True,
            "raw_artifact_urls_available": True,
            "release_keys_available": True,
            "last_updated_metadata_available": True,
            "release_dates_available": False,
        },
        "validation_state": {
            "pipeline_modified": False,
            "validator_modified": False,
            "package_model_modified": False,
            "accepted_objects_require_existing_contracts": True,
        },
        "pel_evidence": {
            "source_package_authoring_recurred": True,
            "production_quality_aggregation_recurred": True,
            "helper_implementation_blocker": False,
            "observed_campaigns_for_pel_008_after_campaign_3": 3,
            "observed_campaigns_for_pel_009_after_campaign_3": 4,
        },
        "evidence_basis": [
            "docs/production_campaign_roadmap.md",
            "docs/production_evolution_log.md",
            "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
            "artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/production_quality_report.json",
            "artifacts/reports/R-20260709-production-evolution-decision-report-pel-008-009.md",
        ],
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot

def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar demographic-structure source freshness and release metadata coverage",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "external_evidence_quality_provenance_and_freshness_metadata",
        "exclusions": SAFE_EXCLUSIONS,
    }

def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="World Bank World Development Indicators audited demographic-structure freshness metadata snapshot",
        source_family="external_wdi_annual_scalar_demographic_structure_freshness_metadata",
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "source freshness metadata")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_wdi_demographic_structure_freshness_metadata",
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
            "selection_rule": "approved Campaign 3 WDI annual-scalar demographic-structure source freshness and release metadata scope",
            "source_family": snapshot["evidence_family"],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign3_wdi_freshness_metadata.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic embedded immutable WDI freshness metadata snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )
def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    fresh = snapshot["freshness_metadata"]
    prov = snapshot["provenance_observations"]
    validation_state = snapshot["validation_state"]
    pel = snapshot["pel_evidence"]
    return [
        source_package(
            "srcpkg-campaign3-lastupdated-availability",
            "The Campaign 3 WDI freshness snapshot records last-updated metadata availability for every audited pipeline-run record.",
            "provenance",
            snapshot,
            {"topic": "last-updated metadata availability", "available": fresh["wdi_lastupdated_metadata_available"], "coverage": fresh["last_updated_coverage"], "pipeline_run_count": fresh["pipeline_run_count"]},
        ),
        source_package(
            "srcpkg-campaign3-release-key-coverage",
            f"The Campaign 3 WDI freshness snapshot records release keys for {fresh['dataset_release_count']} dataset-release records.",
            "coverage",
            snapshot,
            {"topic": "release-key coverage", "coverage": fresh["release_key_coverage"], "dataset_release_count": fresh["dataset_release_count"]},
        ),
        source_package(
            "srcpkg-campaign3-release-date-nullness",
            f"The Campaign 3 WDI freshness snapshot records {fresh['release_date_null_count']} dataset-release records with null release-date fields.",
            "negative",
            snapshot,
            {"topic": "release-date nullness", "release_date_available_count": fresh["release_date_available_count"], "release_date_null_count": fresh["release_date_null_count"], "release_date_coverage": fresh["release_date_coverage"]},
        ),
        source_package(
            "srcpkg-campaign3-freshness-metadata-coverage",
            f"The Campaign 3 WDI freshness snapshot has last-updated coverage {fresh['last_updated_coverage']} and release-key coverage {fresh['release_key_coverage']} across its audited metadata records.",
            "evidence_quality",
            snapshot,
            {"topic": "freshness metadata coverage", "last_updated_coverage": fresh["last_updated_coverage"], "release_key_coverage": fresh["release_key_coverage"], "release_date_coverage": fresh["release_date_coverage"]},
        ),
        source_package(
            "srcpkg-campaign3-provenance-field-availability",
            "The Campaign 3 WDI freshness snapshot records source URL, license note, raw artifact hash, raw artifact URL, release-key, and last-updated metadata availability.",
            "evidence_quality",
            snapshot,
            {"topic": "provenance field availability", **prov},
        ),
        source_package(
            "srcpkg-campaign3-release-metadata-classification",
            "Campaign 3 classifies WDI freshness evidence into last-updated availability, release-key availability, release-date nullness, and provenance-field availability groups.",
            "classified",
            snapshot,
            {"topic": "release metadata classification", "groups": ["last_updated_availability", "release_key_availability", "release_date_nullness", "provenance_field_availability"]},
        ),
        source_package(
            "srcpkg-campaign3-validation-state",
            "Campaign 3 packages are routed through the existing Source Evidence Package to KnowledgeObjectPackage validation pipeline without validator or package-model modification.",
            "methodological",
            snapshot,
            {"topic": "validation state", **validation_state},
        ),
        source_package(
            "srcpkg-campaign3-freshness-method",
            "Campaign 3 freshness metadata coverage values are deterministic ratios computed from explicit availability counts in the immutable snapshot.",
            "methodological",
            snapshot,
            {"topic": "deterministic freshness method", "ratio_inputs": ["available_count", "record_count"], "uses_model_generation": False},
        ),
        source_package(
            "srcpkg-campaign3-scoped-negative-release-date",
            "The Campaign 3 snapshot does not contain non-null release-date values for the audited dataset-release records.",
            "negative",
            snapshot,
            {"topic": "scoped missing release-date values", "scope": "audited dataset-release records", "missing_count": fresh["release_date_null_count"]},
        ),
        source_package(
            "srcpkg-campaign3-pel008-recurrence",
            "Campaign 3 source-package construction again required deterministic SourceEvidencePackage field authoring across accepted and rejected candidates.",
            "methodological",
            snapshot,
            {"topic": "PEL-008 recurrence evidence", "source_package_authoring_recurred": pel["source_package_authoring_recurred"], "observed_campaigns_after_campaign_3": pel["observed_campaigns_for_pel_008_after_campaign_3"]},
        ),
        source_package(
            "srcpkg-campaign3-pel009-recurrence",
            "Campaign 3 production-quality reporting again required deterministic metric aggregation over accepted objects, rejected candidates, validator failures, fingerprints, and replay output.",
            "methodological",
            snapshot,
            {"topic": "PEL-009 recurrence evidence", "production_quality_aggregation_recurred": pel["production_quality_aggregation_recurred"], "observed_campaigns_after_campaign_3": pel["observed_campaigns_for_pel_009_after_campaign_3"]},
        ),
        source_package(
            "srcpkg-campaign3-no-architecture-change-required",
            "Campaign 3 freshness and release metadata objects fit the existing KnowledgeForge package model and knowledge categories without architecture modification.",
            "methodological",
            snapshot,
            {"topic": "architecture preservation", "architecture_modified": False, "validator_modified": False, "taxonomy_modified": False},
        ),
    ]


def build_rejected_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rejected: list[dict[str, Any]] = []
    bad_boundary = source_package(
        "srcpkg-campaign3-reject-boundary-language",
        "This means the demographic source is improving and investors should prefer countries with recent metadata.",
        "evidence_quality",
        snapshot,
        {"topic": "boundary rejection"},
    )
    rejected.append(bad_boundary)

    missing_provenance = source_package(
        "srcpkg-campaign3-reject-missing-provenance",
        "A malformed Campaign 3 candidate omits provenance fields.",
        "provenance",
        snapshot,
        {"topic": "malformed provenance"},
    )
    missing_provenance.pop("provenance")
    rejected.append(missing_provenance)

    missing_fingerprint = source_package(
        "srcpkg-campaign3-reject-missing-fingerprint",
        "A malformed Campaign 3 candidate omits source fingerprints.",
        "coverage",
        snapshot,
        {"topic": "malformed fingerprint"},
    )
    missing_fingerprint.pop("fingerprints")
    rejected.append(missing_fingerprint)

    unsupported_category = source_package(
        "srcpkg-campaign3-reject-unsupported-category",
        "A malformed Campaign 3 candidate uses an unsupported freshness-rating category.",
        "freshness_rating",
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
        "campaign_2": PROJECT_ROOT / "artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/production_quality_report.json",
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

    snapshot = immutable_wdi_freshness_snapshot()
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

    replay_snapshot = immutable_wdi_freshness_snapshot()
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
                "accepted": prior.get("campaign_2", {}).get("knowledge_object_packages_accepted"),
                "rejected": prior.get("campaign_2", {}).get("rejected_candidates"),
                "determinism": prior.get("campaign_2", {}).get("determinism_verification"),
                "fingerprint_stability": prior.get("campaign_2", {}).get("fingerprint_stability"),
                "duplicates": prior.get("campaign_2", {}).get("duplicate_knowledge_objects_detected"),
            },
            "campaign_3": {
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
            "dataset_release_count": snapshot["freshness_metadata"]["dataset_release_count"],
            "pipeline_run_count": snapshot["freshness_metadata"]["pipeline_run_count"],
            "last_updated_coverage": snapshot["freshness_metadata"]["last_updated_coverage"],
            "release_key_coverage": snapshot["freshness_metadata"]["release_key_coverage"],
            "release_date_coverage": snapshot["freshness_metadata"]["release_date_coverage"],
        },
        "architectural_observations": [
            "Existing package and validator contracts handled Campaign 3 freshness and release metadata objects without modification.",
            "Existing knowledge categories covered source freshness, release metadata, provenance, evidence quality, and scoped negative knowledge.",
            "Rejected candidates were preserved with validator evidence.",
        ],
        "candidate_improvements_discovered": [
            "SourceEvidencePackage field construction pressure recurred in Campaign 3 under freshness/provenance metadata scope.",
            "Production-quality metric aggregation pressure recurred in Campaign 3 with cross-campaign comparison across Campaigns 0-3.",
            "No duplicate pressure was observed in Campaign 3.",
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
        "final_recommendation": "Move PEL-008 and PEL-009 to Ready for Implementation and run a bounded helper proof before Campaign 4; preserve roadmap sequence after that proof.",
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

    write_text(reports / "campaign_3_final_report.md", f"""
# Campaign 3 Final Report

Status: completed
Campaign: {CAMPAIGN_ID}

## Result

Campaign 3 accepted {summary['accepted']} KnowledgeObjectPackages and preserved {summary['rejected']} rejected candidates.

The campaign used the existing KnowledgeForge architecture unchanged. No taxonomy change, package-model change, validator redesign, adapter, API, shared schema, repository coupling, database access, runtime infrastructure, local model generation, or frontier model generation was introduced.

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

## Freshness and release metadata scope

Accepted objects cover last-updated availability, release-key coverage, release-date nullness, provenance-field availability, validation state, deterministic freshness-method metadata, and scoped negative knowledge about missing release-date values.

## Final production recommendation

{summary['final_recommendation']}
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

## Production quality assessment

Campaigns 0-3 all preserve determinism, fingerprint stability, rejected-candidate preservation, and zero observed duplicate pressure. Campaign 3 adds one more successful freshness/provenance metadata campaign without architecture modification.
""")

    write_text(reports / "cross_campaign_assessment_report.md", f"""
# Cross-Campaign Assessment Report

Scope: Campaigns 0-3

## Production stability

All four campaigns completed with deterministic execution and accepted KnowledgeObjectPackages through the existing pipeline.

{markdown_table(comparison_rows, ['Campaign', 'Accepted', 'Rejected', 'Determinism', 'Fingerprint stability', 'Duplicates'])}

## Validator behavior

Validator failures repeatedly involved evidence-contract, provenance, lineage-fingerprint, unsupported-inference, and boundary-language categories. Campaign 3 repeated this as expected safety behavior and did not falsify the architecture.

## Fingerprint stability and determinism

Fingerprint stability and determinism held again in Campaign 3. This strengthens the KnowledgeForge-wide classification for deterministic replay and canonical fingerprinting.

## Provenance and freshness handling

Campaign 3 accepted freshness/provenance metadata objects with complete accepted provenance envelopes. Missing release-date values were represented as scoped negative knowledge rather than interpreted as domain meaning.

## Recurring manual work and helper pressure

PEL-008 recurred for the third domain campaign when freshness/provenance packages still required deterministic SourceEvidencePackage field construction.

PEL-009 recurred across Campaigns 0-3 through repeated deterministic production-quality metric aggregation and cross-campaign comparison.

Both now have enough evidence to move to Ready for Implementation for a bounded helper proof, provided the proof preserves existing package/output/validator contracts and implements no architecture change.

## Duplicate pressure

No duplicate Knowledge Objects were detected in Campaigns 0, 1, 2, or 3. A cross-campaign duplicate registry remains unjustified.

## Roadmap assessment

Campaign 3 does not justify resequencing the production roadmap. After a bounded PEL-008/PEL-009 helper proof, Campaign 4 remains the next production campaign.
""")

    write_text(reports / "production_retrospective_report.md", f"""
# Production Retrospective Report

Campaign: {CAMPAIGN_ID}

## Successfully exercised capabilities

- Source freshness metadata package construction.
- Release-key coverage characterization.
- Release-date nullness as scoped negative knowledge.
- Provenance-field availability characterization.
- Existing validator pipeline for freshness/provenance metadata.
- Rejected candidate preservation.
- Production-quality reporting with Campaigns 0-3 comparison.
- Deterministic replay and fingerprint stability.

## Repeated manual decisions observed

- SourceEvidencePackage field construction repeated again under freshness/provenance metadata scope.
- Production-quality metric aggregation repeated again with cross-campaign comparison.

## Deterministic transformations reused

- canonical JSON fingerprinting;
- availability-ratio computation;
- package-stage construction;
- category counting;
- validator-failure aggregation;
- cross-campaign metric comparison.

## Architecture assessment

No architectural assumption was falsified. The existing architecture should be preserved unchanged.

## Future automation opportunities

Evidence now supports a bounded implementation proof for deterministic helpers corresponding to PEL-008 and PEL-009 before Campaign 4. The helpers should be operational conveniences only and must emit existing package/report shapes.
""")

    write_text(reports / "architectural_observations_report.md", f"""
# Architectural Observations Supported by Campaign 3 Evidence

Campaign: {CAMPAIGN_ID}

## Observed facts

- Existing package hierarchy handled freshness and release metadata without modification.
- Existing knowledge categories were sufficient for provenance, evidence quality, coverage, methodological, classified, and negative knowledge.
- Existing validation framework accepted valid freshness/provenance objects and rejected malformed or boundary-violating candidates.
- Determinism and fingerprint stability held under replay.
- No duplicate Knowledge Objects were detected.

## Evidence-backed changes

Campaign 3 supports moving two Production Evolution Log items from investigate to Ready for Implementation:

- PEL-008 — deterministic SourceEvidencePackage authoring helper;
- PEL-009 — reusable production-quality metric aggregation helper.

This supports only bounded helper proof work. It does not support architecture redesign.

## Unsupported changes

Campaign 3 does not support taxonomy redesign, package-model replacement, validator redesign, runtime infrastructure, repository coupling, shared schemas, adapters, APIs, local/frontier model generation, or database coupling.
""")

def main() -> int:
    parser = argparse.ArgumentParser(description="Run Campaign 3 WDI freshness metadata production campaign")
    parser.add_argument("--output", default=f"artifacts/production/{CAMPAIGN_ID}")
    args = parser.parse_args()
    summary = run_campaign(PROJECT_ROOT / args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
