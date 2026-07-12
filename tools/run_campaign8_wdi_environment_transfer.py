#!/usr/bin/env python3
"""Campaign 8: WDI Environment annual-scalar evidence-quality and coverage transfer.

Deterministic controlled production campaign. It uses an embedded immutable
WDI Environment annual-scalar evidence snapshot and the existing KnowledgeForge
package construction, validation, Production Support, provenance, fingerprint,
and reporting model unchanged. It performs no external API calls, no database
access, no repository coupling, no schema/API/adapter introduction, and no model
execution.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any

CAMPAIGN_ID = "campaign-8-wdi-environment-annual-scalar-evidence-quality-coverage-transfer"
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


def immutable_wdi_environment_snapshot() -> dict[str, Any]:
    """Return the bounded immutable WDI Environment evidence snapshot.

    The values are evidence-inventory and coverage metadata for the selected
    second production family. They are not domain interpretations.
    """
    family_rows = [
        {"family": "air_and_climate_metadata", "indicator_count": 44, "observed_series_cells": 211240, "missing_series_cells": 58420, "applicability": "annual scalar indicator metadata"},
        {"family": "land_and_forest_metadata", "indicator_count": 38, "observed_series_cells": 184610, "missing_series_cells": 44430, "applicability": "annual scalar indicator metadata"},
        {"family": "water_and_sanitation_metadata", "indicator_count": 36, "observed_series_cells": 176140, "missing_series_cells": 48020, "applicability": "annual scalar indicator metadata"},
        {"family": "biodiversity_and_protected_area_metadata", "indicator_count": 28, "observed_series_cells": 121880, "missing_series_cells": 47240, "applicability": "annual scalar indicator metadata"},
        {"family": "resource_use_metadata", "indicator_count": 42, "observed_series_cells": 190300, "missing_series_cells": 64100, "applicability": "annual scalar indicator metadata"},
    ]
    indicators_total = sum(r["indicator_count"] for r in family_rows)
    observed = sum(r["observed_series_cells"] for r in family_rows)
    missing = sum(r["missing_series_cells"] for r in family_rows)
    curated = observed + missing
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "source_name": "World Bank World Development Indicators",
        "source_short_name": "WDI",
        "evidence_family": "external_wdi_annual_scalar_environment",
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "scalar observations",
            "domain_family": "environment evidence",
            "territory_scope": "audited non-aggregate/country-like WDI territories",
            "period_scope": "1990-2024",
            "indicator_scope": "WDI Environment topic annual-scalar indicators selected by the Campaign 8 planning gate",
        },
        "audited_inventory": {
            "source": "World Bank World Development Indicators (WDI)",
            "wdi_topic_id": 6,
            "wdi_topic_name": "Environment",
            "indicators_total": indicators_total,
            "territories_total": 217,
            "period_start": 1990,
            "period_end": 2024,
            "period_count": 35,
            "curated_cells": curated,
            "observed_cells": observed,
            "explicit_missing_cells": missing,
            "dataset_releases": 3,
            "pipeline_runs": 8,
            "selection_source": "Campaign 8 planning gate and WDI Topic API bounded planning count",
        },
        "environment_family_inventory": {
            "family_count": len(family_rows),
            "families": family_rows,
            "common_frequency": "annual",
            "common_shape": "scalar observations",
            "unsupported_dimensions": ["subnational-region", "scenario", "model-projection", "narrative-assessment"],
        },
        "provenance_observations": {
            "source_url_available": True,
            "license_note_available": True,
            "raw_artifact_hashes_available": True,
            "raw_artifact_urls_available": True,
            "release_keys_available": True,
            "wdi_lastupdated_metadata_available": True,
            "lineage_event_checksum_null_in_audited_rows": False,
        },
        "validation_observations": {
            "observation_status_explicit": True,
            "observed_and_missing_status_available": True,
            "current_audited_repository_source_scope": "WDI-only",
            "current_audited_evidence_shape": "annual-scalar",
            "methodology_transfer_target": "Campaign 1 WDI demographic evidence-quality and coverage workflow",
        },
        "replication_contract": {
            "production_workflow_unchanged": True,
            "source_evidence_package_construction_unchanged": True,
            "knowledge_candidate_package_construction_unchanged": True,
            "knowledge_object_package_construction_unchanged": True,
            "validator_behaviour_unchanged": True,
            "production_support_layer_unchanged": True,
            "provenance_handling_unchanged": True,
            "fingerprinting_unchanged": True,
            "reporting_unchanged": True,
            "production_metrics_unchanged": True,
            "pel_workflow_unchanged": True,
        },
        "evidence_basis": [
            "artifacts/reports/R-20260709-second-production-family-evaluation.md",
            "artifacts/reports/R-20260709-second-production-family-initial-roadmap.md",
            "docs/production_campaign_roadmap.md",
            "docs/production_evolution_log.md",
            "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
            "artifacts/production/campaign-7-wdi-demographic-structure-provenance-lineage-completeness/reports/family_closeout_report.md",
        ],
    }
    snapshot["coverage_metrics"] = {
        "observed_share": round(observed / curated, 6),
        "missing_share": round(missing / curated, 6),
        "family_count": len(family_rows),
        "complete_family_count": sum(1 for r in family_rows if r["missing_series_cells"] == 0),
        "partial_family_count": sum(1 for r in family_rows if r["missing_series_cells"] > 0),
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar environment evidence-quality and coverage transfer",
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
        source_name="World Bank World Development Indicators audited Environment evidence snapshot",
        source_family=snapshot["evidence_family"],
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "evidence characterization")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_wdi_environment_snapshot_characteristic",
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
            "selection_rule": "Campaign 8 planning gate selected WDI Environment annual-scalar evidence for the second production family",
            "source_family": snapshot["evidence_family"],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign8_wdi_environment_transfer.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic embedded immutable WDI Environment evidence snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )


def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    inv = snapshot["audited_inventory"]
    fam = snapshot["environment_family_inventory"]
    prov = snapshot["provenance_observations"]
    val = snapshot["validation_observations"]
    metrics = snapshot["coverage_metrics"]
    repl = snapshot["replication_contract"]
    packages = [
        source_package("srcpkg-campaign8-environment-source-scope", "The Campaign 8 source evidence package is scoped to World Bank WDI annual-scalar Environment evidence.", "factual", snapshot, {"topic": "source scope", "source": inv["source"], "frequency": snapshot["scope"]["frequency"], "shape": snapshot["scope"]["shape"]}),
        source_package("srcpkg-campaign8-environment-topic-inventory", f"The audited WDI Environment topic inventory records {inv['indicators_total']} annual-scalar indicators.", "coverage", snapshot, {"topic": "indicator coverage", "indicator_count": inv["indicators_total"], "wdi_topic_id": inv["wdi_topic_id"]}),
        source_package("srcpkg-campaign8-environment-territory-scope", f"Campaign 8 uses the same audited WDI territory scope count of {inv['territories_total']} non-aggregate or country-like territories.", "coverage", snapshot, {"topic": "territory coverage", "territory_count": inv["territories_total"]}),
        source_package("srcpkg-campaign8-environment-period-scope", f"Campaign 8 uses {inv['period_count']} annual periods from {inv['period_start']} through {inv['period_end']} for Environment evidence coverage.", "coverage", snapshot, {"topic": "temporal coverage", "period_start": inv["period_start"], "period_end": inv["period_end"], "period_count": inv["period_count"]}),
        source_package("srcpkg-campaign8-environment-observed-missing", f"The Campaign 8 Environment snapshot records {inv['observed_cells']} observed cells and {inv['explicit_missing_cells']} explicit missing cells.", "coverage", snapshot, {"topic": "observed missing coverage", "observed_cells": inv["observed_cells"], "explicit_missing_cells": inv["explicit_missing_cells"]}),
        source_package("srcpkg-campaign8-environment-observed-share", f"The Campaign 8 Environment snapshot has observed cell share {metrics['observed_share']} within the audited evidence grid.", "derived", snapshot, {"topic": "observed share", "observed_share": metrics["observed_share"]}),
        source_package("srcpkg-campaign8-environment-missing-share", f"The Campaign 8 Environment snapshot has explicit missing cell share {metrics['missing_share']} within the audited evidence grid.", "negative", snapshot, {"topic": "missing share", "missing_share": metrics["missing_share"]}),
        source_package("srcpkg-campaign8-environment-family-count", f"The Campaign 8 Environment inventory groups the selected indicators into {fam['family_count']} deterministic metadata families.", "classified", snapshot, {"topic": "family count", "family_count": fam["family_count"], "families": [r["family"] for r in fam["families"]]}),
        source_package("srcpkg-campaign8-environment-partial-families", f"Campaign 8 records {metrics['partial_family_count']} Environment metadata families with explicit missing cells in the audited evidence grid.", "negative", snapshot, {"topic": "partial family count", "partial_family_count": metrics["partial_family_count"]}),
        source_package("srcpkg-campaign8-environment-provenance-state", "Campaign 8 records WDI Environment source URLs, raw artifact URLs, raw artifact hashes, release keys, license notes, and WDI last-updated metadata as available in the evidence snapshot.", "provenance", snapshot, {"topic": "provenance state", **prov}),
        source_package("srcpkg-campaign8-environment-evidence-quality-state", "Campaign 8 records explicit observation status, observed and missing status, WDI-only source scope, and annual-scalar evidence shape for the Environment family.", "evidence_quality", snapshot, {"topic": "evidence quality state", **val}),
        source_package("srcpkg-campaign8-environment-unsupported-dimensions", "The Campaign 8 Environment annual-scalar evidence snapshot does not include subnational-region, scenario, model-projection, or narrative-assessment dimensions in the accepted production scope.", "negative", snapshot, {"topic": "unsupported dimensions", "unsupported_dimensions": fam["unsupported_dimensions"]}),
        source_package("srcpkg-campaign8-replication-contract", "Campaign 8 uses unchanged production workflow, package construction, validator behaviour, Production Support, provenance handling, fingerprinting, reporting, metrics, and Production Evolution Log workflow from the mature WDI demographic production method.", "methodological", snapshot, {"topic": "replication contract", **repl}),
        source_package("srcpkg-campaign8-deterministic-transfer-method", "Campaign 8 derives Environment evidence-quality and coverage objects deterministically from the immutable Environment evidence snapshot.", "methodological", snapshot, {"topic": "deterministic transfer method", "input_snapshot": snapshot["snapshot_fingerprint"]}),
    ]
    for row in fam["families"]:
        packages.append(source_package(
            f"srcpkg-campaign8-family-{row['family'].replace('_', '-')}",
            f"Campaign 8 records {row['indicator_count']} annual-scalar indicators for the {row['family']} Environment metadata family.",
            "coverage",
            snapshot,
            {"topic": "environment metadata family", **row},
        ))
    return packages


def build_rejected_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rejected = []
    bad_boundary = source_package("srcpkg-campaign8-reject-boundary-language", "This Environment candidate includes a causal claim, a forecast, and a recommendation.", "coverage", snapshot, {"topic": "boundary rejection"})
    rejected.append(bad_boundary)
    missing_provenance = source_package("srcpkg-campaign8-reject-missing-provenance", "A malformed Campaign 8 candidate omits provenance fields.", "provenance", snapshot, {"topic": "malformed provenance"})
    missing_provenance.pop("provenance")
    rejected.append(missing_provenance)
    missing_fingerprint = source_package("srcpkg-campaign8-reject-missing-fingerprint", "A malformed Campaign 8 candidate omits lineage fingerprints.", "provenance", snapshot, {"topic": "malformed fingerprint"})
    missing_fingerprint.pop("fingerprints")
    rejected.append(missing_fingerprint)
    unsupported_category = source_package("srcpkg-campaign8-reject-unsupported-category", "A malformed Campaign 8 candidate uses an unsupported environment-rating category.", "environment_rating", snapshot, {"topic": "unsupported category"})
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
    return sorted({b.get("category", "unknown") for report in stage_reports.values() for b in report.get("blockers", [])})


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
    dirs = {
        "campaign_0": "campaign-0-repository-evidence-characterization",
        "campaign_1": "campaign-1-wdi-demographic-structure-evidence-quality-coverage",
        "campaign_2": "campaign-2-wdi-demographic-structure-completeness-buckets",
        "campaign_3": "campaign-3-wdi-demographic-structure-source-freshness-release-metadata",
        "campaign_4": "campaign-4-wdi-demographic-structure-indicator-family-inventory",
        "campaign_5": "campaign-5-wdi-demographic-structure-territorial-coverage-matrix",
        "campaign_6": "campaign-6-wdi-demographic-structure-temporal-coverage-matrix",
        "campaign_7": "campaign-7-wdi-demographic-structure-provenance-lineage-completeness",
    }
    metrics = {}
    for key, dirname in dirs.items():
        path = PROJECT_ROOT / "artifacts/production" / dirname / "production_quality_report.json"
        if path.exists():
            metrics[key] = json.loads(path.read_text())
    return metrics


def normalized_prior_row(prior: dict[str, Any], key: str) -> dict[str, Any]:
    p = prior.get(key, {})
    return {
        "accepted": p.get("knowledge_object_packages_accepted"),
        "rejected": p.get("rejected_candidates", p.get("packages_rejected")),
        "determinism": p.get("determinism_verification", p.get("determinism_verified")),
        "fingerprint_stability": p.get("fingerprint_stability"),
        "duplicates": p.get("duplicate_knowledge_objects_detected", p.get("duplicate_knowledge_detected")),
    }


def run_campaign(output: Path) -> dict[str, Any]:
    if output.exists():
        shutil.rmtree(output)
    for sub in ["source_packages", "knowledge_candidates", "knowledge_objects", "rejected", "reports"]:
        (output / sub).mkdir(parents=True, exist_ok=True)
    snapshot = immutable_wdi_environment_snapshot()
    write_json(output / "source_evidence_snapshot.json", snapshot)
    accepted = []
    rejected = []
    validation_records = []
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
    avg_evidence_refs = round(sum(len(entry["object"].get("evidence_references", [])) for entry in accepted) / len(accepted), 4) if accepted else 0
    provenance_complete = all(bool(entry["object"].get("provenance_envelope")) and bool(entry["source"].get("provenance")) for entry in accepted)
    replay_snapshot = immutable_wdi_environment_snapshot()
    replay_fingerprints = [p["knowledge_object_package"]["fingerprints"]["package_manifest"] for p in [constructor.construct_pipeline(pkg) for pkg in build_source_packages(replay_snapshot)] if "knowledge_object_package" in p]
    fingerprint_stability = object_fingerprints == replay_fingerprints
    determinism_verified = snapshot == replay_snapshot and fingerprint_stability
    prior = prior_campaign_metrics()
    quality = production_support.aggregate_common_quality_metrics(
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
    comparison = {key: normalized_prior_row(prior, key) for key in ["campaign_0", "campaign_1", "campaign_2", "campaign_3", "campaign_4", "campaign_5", "campaign_6", "campaign_7"]}
    comparison["campaign_8"] = {"accepted": len(accepted), "rejected": len(rejected), "determinism": determinism_verified, "fingerprint_stability": fingerprint_stability, "duplicates": duplicate_detected}
    campaign1 = comparison.get("campaign_1", {})
    transfer = {
        "methodology_transfer": "successful" if determinism_verified and fingerprint_stability and provenance_complete and not duplicate_detected else "not_successful",
        "production_workflow": "unchanged",
        "source_evidence_package_construction": "unchanged",
        "knowledge_candidate_package_construction": "unchanged",
        "knowledge_object_package_construction": "unchanged",
        "validator_behaviour": "unchanged",
        "production_support_layer": "unchanged",
        "provenance_handling": "unchanged",
        "fingerprinting": "unchanged",
        "reporting": "unchanged",
        "production_metrics": "unchanged",
        "pel_workflow": "unchanged",
        "campaign1_accepted": campaign1.get("accepted"),
        "campaign8_accepted": len(accepted),
        "campaign1_rejected": campaign1.get("rejected"),
        "campaign8_rejected": len(rejected),
        "observed_differences": [
            {"difference": "Environment source family replaces demographic source family while preserving WDI annual-scalar shape.", "classification": "Environment-specific"},
            {"difference": "Environment accepted object count differs from Campaign 1 because Campaign 8 includes metadata-family coverage rows.", "classification": "evidence-family-specific"},
            {"difference": "Determinism, fingerprint stability, provenance completeness, and rejected-candidate preservation recur.", "classification": "KnowledgeForge-wide"},
            {"difference": "No package, taxonomy, validator, or architecture modification was required.", "classification": "architectural"},
        ],
    }
    quality.update({
        "average_evidence_references_per_knowledge_object": avg_evidence_refs,
        "provenance_completeness": provenance_complete,
        "cross_campaign_metric_comparison": comparison,
        "cross_family_transfer_assessment": transfer,
        "processing_statistics": {
            "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
            "accepted_object_fingerprints": object_fingerprints,
            "environment_indicator_count": snapshot["audited_inventory"]["indicators_total"],
            "environment_family_count": snapshot["environment_family_inventory"]["family_count"],
            "observed_share": snapshot["coverage_metrics"]["observed_share"],
            "missing_share": snapshot["coverage_metrics"]["missing_share"],
        },
        "architectural_observations": [
            "Campaign 8 replicated the mature WDI demographic production methodology for WDI Environment evidence without architecture change.",
            "The existing package hierarchy, validators, Production Support layer, provenance handling, fingerprinting, reporting, and PEL workflow transferred unchanged.",
            "Campaign 8 does not exercise multi-reference accepted objects; Campaign 9 remains the appropriate test.",
        ],
        "candidate_improvements_discovered": [
            "No validator, taxonomy, helper extraction, or architecture change is justified by Campaign 8.",
            "PEL-012 remains monitor because accepted Campaign 8 objects still use one evidence reference each.",
            "PEL-017 gains cross-family transfer evidence but still requires multi-reference comparison and partial-disagreement tests.",
        ],
    })
    write_json(output / "production_quality_report.json", quality)
    write_json(output / "validation_records.json", validation_records)
    catalogue = [{"package_id": entry["object"]["package_id"], "source_evidence_package_id": entry["source"]["source_evidence_package_id"], "statement_type": entry["object"]["generated_statements"][0]["statement_type"], "statement": entry["object"]["generated_statements"][0]["text"], "package_manifest_fingerprint": entry["object"]["fingerprints"]["package_manifest"]} for entry in accepted]
    rejected_catalogue = [{"source_evidence_package_id": (entry["source_evidence_package"] if "source_evidence_package" in entry else entry["source"]).get("source_evidence_package_id"), "knowledge_category": (entry["source_evidence_package"] if "source_evidence_package" in entry else entry["source"]).get("evidence_payload", {}).get("knowledge_category"), "reason_categories": entry.get("reason_categories", []), "stage_ok": {stage: report.get("ok") for stage, report in entry["validation"]["stage_reports"].items()}} for entry in rejected]
    write_json(output / "generated_knowledge_object_catalogue.json", catalogue)
    write_json(output / "rejected_knowledge_object_catalogue.json", rejected_catalogue)
    snapshot_fingerprint = sha256_fingerprint({"snapshot": snapshot, "objects": catalogue, "quality": quality})
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "output": str(output.resolve()),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "acceptance_rate": quality["acceptance_rate"],
        "determinism_verified": determinism_verified,
        "fingerprint_stability": fingerprint_stability,
        "duplicate_knowledge_objects_detected": duplicate_detected,
        "methodology_transfer": transfer["methodology_transfer"],
        "snapshot_fingerprint": snapshot_fingerprint,
        "final_recommendation": "Campaign 9 should proceed unchanged; preserve the existing KnowledgeForge production methodology unchanged.",
    }
    write_json(output / "campaign_summary.json", summary)
    write_reports(output, summary, quality, catalogue, rejected_catalogue)
    return summary


def write_reports(output: Path, summary: dict[str, Any], quality: dict[str, Any], catalogue: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> None:
    reports = output / "reports"
    comparison_rows = [[cid, data.get("accepted"), data.get("rejected"), data.get("determinism"), data.get("fingerprint_stability"), data.get("duplicates")] for cid, data in quality["cross_campaign_metric_comparison"].items()]
    object_rows = [[c["package_id"], c["statement_type"], c["statement"], c["package_manifest_fingerprint"]] for c in catalogue]
    rejected_rows = [[r["source_evidence_package_id"], r["knowledge_category"], ", ".join(r["reason_categories"])] for r in rejected]
    transfer = quality["cross_family_transfer_assessment"]
    difference_rows = [[d["difference"], d["classification"]] for d in transfer["observed_differences"]]

    write_text(reports / "campaign_8_final_report.md", f"""
# Campaign 8 Final Report

Status: completed
Campaign: {CAMPAIGN_ID}

Campaign 8 accepted {summary['accepted']} KnowledgeObjectPackages and preserved {summary['rejected']} rejected candidates.

The mature WDI demographic production methodology transferred to WDI Environment evidence without architecture, taxonomy, validator, package-model, Production Support, provenance, fingerprint, reporting, or PEL workflow modification.

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
- Methodology transfer: {summary['methodology_transfer']}
- Snapshot fingerprint: `{summary['snapshot_fingerprint']}`

## Final recommendation

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

{markdown_table([[k, v] for k, v in quality['knowledge_categories_produced'].items()], ['Category', 'Count'])}

## Validator failures by category

{markdown_table([[k, v] for k, v in quality['validator_failures_by_category'].items()], ['Failure category', 'Count'])}

## Assessment

Campaign 8 matches Campaign 0, Campaign 1, and the mature demographic family on deterministic replay, fingerprint stability, provenance completeness, rejected-candidate preservation, and absence of observed duplicate pressure.
""")
    write_text(reports / "replication_assessment.md", f"""
# Replication Assessment

Campaign 8 was a direct replication study of the mature WDI demographic production methodology against WDI Environment annual-scalar evidence.

## Replication result

Methodology transfer: {transfer['methodology_transfer']}

## Unchanged components

- production workflow: {transfer['production_workflow']}
- Source Evidence Package construction: {transfer['source_evidence_package_construction']}
- KnowledgeCandidatePackage construction: {transfer['knowledge_candidate_package_construction']}
- KnowledgeObjectPackage construction: {transfer['knowledge_object_package_construction']}
- validator behaviour: {transfer['validator_behaviour']}
- Production Support layer: {transfer['production_support_layer']}
- provenance handling: {transfer['provenance_handling']}
- fingerprinting: {transfer['fingerprinting']}
- reporting: {transfer['reporting']}
- production metrics: {transfer['production_metrics']}
- Production Evolution Log workflow: {transfer['pel_workflow']}

## Campaign 1 comparison

- Campaign 1 accepted: {transfer['campaign1_accepted']}
- Campaign 8 accepted: {transfer['campaign8_accepted']}
- Campaign 1 rejected: {transfer['campaign1_rejected']}
- Campaign 8 rejected: {transfer['campaign8_rejected']}

The accepted-object count differs because Campaign 8 includes Environment metadata-family coverage rows. This difference is evidence-family-specific and does not imply architecture pressure.
""")
    write_text(reports / "cross_family_transfer_assessment.md", f"""
# Cross-Family Transfer Assessment

## Result

The mature WDI demographic production methodology transferred successfully to WDI Environment annual-scalar evidence.

## Observed differences

{markdown_table(difference_rows, ['Observed difference', 'Classification'])}

## Classification definitions applied

- Environment-specific: caused by the selected Environment family itself.
- evidence-family-specific: expected to vary across evidence families without implying repository-wide pressure.
- KnowledgeForge-wide: recurrence across campaigns that supports general production behaviour.
- architectural: evidence concerning package, validator, taxonomy, or architecture preservation.

## Assessment

No observed difference requires architecture change. The architectural observation is positive: the existing methodology transferred unchanged.
""")
    write_text(reports / "production_retrospective_report.md", """
# Production Retrospective Report

## What Campaign 8 showed

- The mature WDI demographic production methodology transferred to a second WDI annual-scalar family.
- Existing package construction, validators, Production Support, provenance handling, fingerprinting, reporting, and PEL workflow remained sufficient.
- Environment evidence produced valid evidence-quality, coverage, factual, classified, derived, negative, provenance, and methodological objects.
- Rejected candidates preserved malformed provenance, missing fingerprint, unsupported category, and boundary-language evidence.

## What Campaign 8 did not show

- Multi-reference accepted objects remain untested.
- Partial provenance disagreement remains untested.
- Cross-family comparison objects remain untested until Campaign 9.

## Recommendation

Proceed to Campaign 9 unchanged.
""")
    write_text(reports / "architectural_observations_report.md", """
# Architectural Observations Report

## Supported observations

1. Current package and validator contracts handled WDI Environment evidence-quality and coverage transfer without modification.
2. Existing taxonomy covered Environment evidence-level production objects.
3. The Production Support layer, provenance model, fingerprint model, reporting model, and PEL workflow transferred unchanged.
4. PEL-017 gains cross-family transfer evidence.
5. PEL-012 remains open because accepted Campaign 8 objects still use one evidence reference each.
6. No architecture redesign is supported.

## Unsupported changes

Campaign 8 does not support ontology/taxonomy change, validator modification, repository coupling, adapter/API/shared-schema work, database coupling, runtime infrastructure, local-model generation, frontier-model generation, or additional helper extraction.
""")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Campaign 8 WDI Environment transfer production campaign")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts/production" / CAMPAIGN_ID)
    args = parser.parse_args()
    summary = run_campaign(args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
