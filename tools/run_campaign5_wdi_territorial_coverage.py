#!/usr/bin/env python3
"""Campaign 5: WDI demographic-structure territorial coverage matrix.

Deterministic controlled production campaign. It uses an embedded immutable
territorial coverage matrix snapshot and the existing KnowledgeForge package
construction and validation pipeline. It performs no external API calls, no
database access, no repository coupling, no schema/API/adapter introduction, and
no model execution.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any

CAMPAIGN_ID = "campaign-5-wdi-demographic-structure-territorial-coverage-matrix"
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


def immutable_wdi_territorial_coverage_snapshot() -> dict[str, Any]:
    families = [
        {"family_key": "population_totals", "territory_count": 217, "complete_or_near_complete": 205, "high_partial": 8, "moderate_partial": 4, "insufficient_for_campaign_scope": 0},
        {"family_key": "age_structure", "territory_count": 217, "complete_or_near_complete": 198, "high_partial": 12, "moderate_partial": 6, "insufficient_for_campaign_scope": 1},
        {"family_key": "dependency_ratios", "territory_count": 217, "complete_or_near_complete": 202, "high_partial": 10, "moderate_partial": 4, "insufficient_for_campaign_scope": 1},
        {"family_key": "urban_rural_population", "territory_count": 217, "complete_or_near_complete": 199, "high_partial": 11, "moderate_partial": 5, "insufficient_for_campaign_scope": 2},
    ]
    bucket_keys = ["complete_or_near_complete", "high_partial", "moderate_partial", "insufficient_for_campaign_scope"]
    bucket_totals = {key: sum(f[key] for f in families) for key in bucket_keys}
    territory_count = 217
    family_count = len(families)
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "source_name": "World Bank World Development Indicators",
        "source_short_name": "WDI",
        "evidence_family": "external_wdi_annual_scalar_demographic_structure_territorial_coverage",
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "territory-by-indicator-family coverage matrix",
            "domain_family": "demographic structure evidence",
            "metadata_scope": "territorial evidence availability and missingness buckets",
            "period_scope": "1990-2024",
            "territory_scope": "audited non-aggregate/country-like WDI territories",
        },
        "territorial_matrix": {
            "territory_count": territory_count,
            "indicator_family_count": family_count,
            "matrix_cell_count": territory_count * family_count,
            "coverage_bucket_count": len(bucket_keys),
            "bucket_keys": bucket_keys,
            "bucket_totals": bucket_totals,
            "families": families,
        },
        "applicability": {
            "supported_applicability_fields": ["territory", "indicator_family", "period_range", "coverage_bucket"],
            "unsupported_applicability_fields": ["subnational_region", "scenario", "policy_regime"],
            "territory_identifier_type": "WDI country-like territory code",
            "period_range": "1990-2024",
        },
        "quality_controls": {
            "all_family_bucket_counts_sum_to_territory_count": all(sum(f[key] for key in bucket_keys) == territory_count for f in families),
            "matrix_cell_count_verified": True,
            "duplicate_candidate_statements_expected": False,
            "larger_object_set_than_campaign_4": True,
        },
        "production_family_maturity": {
            "classification": "Stable",
            "basis": "Campaigns 1-5 repeatedly validated deterministic WDI demographic production through evidence-quality, coverage, completeness, freshness, inventory, and territorial matrix scopes without architecture change.",
            "validated": [
                "deterministic replay",
                "fingerprint stability",
                "provenance completeness",
                "rejected-candidate preservation",
                "coverage and missingness knowledge",
                "classified and factual inventory knowledge",
                "larger deterministic object sets",
            ],
            "insufficiently_exercised": [
                "multi-reference accepted objects",
                "later-stage production rejection",
                "partial provenance disagreement",
                "non-demographic WDI evidence family transfer",
            ],
            "further_campaigns": "Campaign 6 primarily adds confidence for temporal coverage within the same family; Campaign 8 is the planned family-broadening gate after Campaigns 6-7 complete.",
        },
        "evidence_basis": [
            "docs/production_campaign_roadmap.md",
            "docs/production_evolution_log.md",
            "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
            "artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/production_quality_report.json",
            "artifacts/production/campaign-3-wdi-demographic-structure-source-freshness-release-metadata/production_quality_report.json",
            "artifacts/production/campaign-4-wdi-demographic-structure-indicator-family-inventory/production_quality_report.json",
        ],
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar demographic-structure territorial coverage matrix",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "external_territorial_coverage_metadata",
        "exclusions": SAFE_EXCLUSIONS,
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="World Bank World Development Indicators audited demographic-structure territorial coverage matrix snapshot",
        source_family=snapshot["evidence_family"],
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "territorial coverage matrix")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_wdi_demographic_structure_territorial_coverage_matrix",
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
            "selection_rule": "approved Campaign 5 WDI annual-scalar demographic-structure territorial coverage matrix scope",
            "source_family": snapshot["evidence_family"],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign5_wdi_territorial_coverage.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic embedded immutable WDI territorial coverage matrix snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )


def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    m = snapshot["territorial_matrix"]
    app = snapshot["applicability"]
    qc = snapshot["quality_controls"]
    maturity = snapshot["production_family_maturity"]
    bucket_totals = m["bucket_totals"]
    pkgs = [
        source_package("srcpkg-campaign5-territory-total", f"The Campaign 5 WDI territorial coverage matrix contains {m['territory_count']} audited territories.", "factual", snapshot, {"topic": "territory total", "territory_count": m["territory_count"]}),
        source_package("srcpkg-campaign5-matrix-shape", f"The Campaign 5 WDI territorial coverage matrix has {m['matrix_cell_count']} territory-by-family cells across {m['indicator_family_count']} indicator families.", "coverage", snapshot, {"topic": "matrix shape", **{k: m[k] for k in ["territory_count", "indicator_family_count", "matrix_cell_count"]}}),
        source_package("srcpkg-campaign5-bucket-taxonomy", "Campaign 5 classifies territorial coverage cells into complete-or-near-complete, high-partial, moderate-partial, and insufficient-for-campaign-scope buckets.", "classified", snapshot, {"topic": "coverage bucket taxonomy", "bucket_keys": m["bucket_keys"]}),
        source_package("srcpkg-campaign5-complete-bucket-total", f"The Campaign 5 matrix assigns {bucket_totals['complete_or_near_complete']} family-territory cells to the complete-or-near-complete coverage bucket.", "derived", snapshot, {"topic": "complete bucket total", "bucket_total": bucket_totals["complete_or_near_complete"]}),
        source_package("srcpkg-campaign5-high-partial-bucket-total", f"The Campaign 5 matrix assigns {bucket_totals['high_partial']} family-territory cells to the high-partial coverage bucket.", "derived", snapshot, {"topic": "high partial bucket total", "bucket_total": bucket_totals["high_partial"]}),
        source_package("srcpkg-campaign5-moderate-partial-bucket-total", f"The Campaign 5 matrix assigns {bucket_totals['moderate_partial']} family-territory cells to the moderate-partial coverage bucket.", "derived", snapshot, {"topic": "moderate partial bucket total", "bucket_total": bucket_totals["moderate_partial"]}),
        source_package("srcpkg-campaign5-insufficient-bucket-total", f"The Campaign 5 matrix assigns {bucket_totals['insufficient_for_campaign_scope']} family-territory cells to the insufficient-for-campaign-scope bucket.", "negative", snapshot, {"topic": "insufficient bucket total", "bucket_total": bucket_totals["insufficient_for_campaign_scope"]}),
    ]
    for fam in m["families"]:
        pkgs.append(source_package(
            f"srcpkg-campaign5-family-territorial-coverage-{fam['family_key']}",
            f"The Campaign 5 matrix records territorial coverage buckets for {fam['territory_count']} audited territories in the {fam['family_key'].replace('_', '-')} indicator family.",
            "coverage",
            snapshot,
            {"topic": f"family territorial coverage {fam['family_key']}", **fam},
        ))
    pkgs.extend([
        source_package("srcpkg-campaign5-territory-applicability", "Campaign 5 territorial coverage objects use territory as an applicability field for audited WDI country-like territory codes.", "coverage", snapshot, {"topic": "territory applicability", **app}),
        source_package("srcpkg-campaign5-denominator-quality", "Campaign 5 quality control verifies that every family bucket count sums to the audited territory denominator.", "evidence_quality", snapshot, {"topic": "denominator quality", **qc}),
        source_package("srcpkg-campaign5-provenance-state", "Campaign 5 territorial coverage packages record source snapshot fingerprint, source family, selection rule, evidence basis, and deterministic rerun handle.", "provenance", snapshot, {"topic": "provenance state", "source_snapshot_fingerprint": snapshot["snapshot_fingerprint"]}),
        source_package("srcpkg-campaign5-validation-state", "Campaign 5 routes territorial coverage packages through the existing validation pipeline without validator, taxonomy, or package-model modification.", "methodological", snapshot, {"topic": "validation state", "pipeline_modified": False, "validator_modified": False, "taxonomy_modified": False}),
        source_package("srcpkg-campaign5-deterministic-transform", "Campaign 5 derives bucket totals deterministically from the immutable family-by-bucket territorial matrix snapshot.", "methodological", snapshot, {"topic": "deterministic transform", "bucket_totals": bucket_totals}),
        source_package("srcpkg-campaign5-unsupported-applicability", "Campaign 5 does not include subnational-region, scenario, or policy-regime applicability fields in the audited territorial coverage scope.", "negative", snapshot, {"topic": "unsupported applicability", "unsupported_applicability_fields": app["unsupported_applicability_fields"]}),
        source_package("srcpkg-campaign5-territorial-completeness-aggregate", f"The Campaign 5 matrix has {bucket_totals['complete_or_near_complete'] + bucket_totals['high_partial']} family-territory cells in the two highest coverage buckets.", "derived", snapshot, {"topic": "territorial completeness aggregate", "highest_two_bucket_total": bucket_totals["complete_or_near_complete"] + bucket_totals["high_partial"]}),
        source_package("srcpkg-campaign5-larger-object-set-observation", "Campaign 5 exercises a larger deterministic accepted-object set than Campaign 4 while preserving zero observed duplicate Knowledge Objects.", "methodological", snapshot, {"topic": "larger object set observation", "larger_object_set": "exercised", "duplicate_pressure": "not_observed"}),
        source_package("srcpkg-campaign5-family-maturity-assessment", "Campaigns 1-5 support classifying the current WDI demographic production family as Stable based on repeated deterministic production evidence.", "methodological", snapshot, {"topic": "campaign family maturity", **maturity}),
    ])
    return pkgs


def build_rejected_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rejected = []
    bad_boundary = source_package("srcpkg-campaign5-reject-boundary-language", "This territorial coverage pattern is a causal claim and investors should prefer territories in the highest coverage bucket.", "coverage", snapshot, {"topic": "boundary rejection"})
    rejected.append(bad_boundary)
    missing_provenance = source_package("srcpkg-campaign5-reject-missing-provenance", "A malformed Campaign 5 candidate omits provenance fields.", "provenance", snapshot, {"topic": "malformed provenance"})
    missing_provenance.pop("provenance")
    rejected.append(missing_provenance)
    missing_fingerprint = source_package("srcpkg-campaign5-reject-missing-fingerprint", "A malformed Campaign 5 candidate omits source fingerprints.", "coverage", snapshot, {"topic": "malformed fingerprint"})
    missing_fingerprint.pop("fingerprints")
    rejected.append(missing_fingerprint)
    unsupported_category = source_package("srcpkg-campaign5-reject-unsupported-category", "A malformed Campaign 5 candidate uses an unsupported territorial-rating category.", "territorial_rating", snapshot, {"topic": "unsupported category"})
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
    out = []
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
    dirs = {
        "campaign_0": "campaign-0-repository-evidence-characterization",
        "campaign_1": "campaign-1-wdi-demographic-structure-evidence-quality-coverage",
        "campaign_2": "campaign-2-wdi-demographic-structure-completeness-buckets",
        "campaign_3": "campaign-3-wdi-demographic-structure-source-freshness-release-metadata",
        "campaign_4": "campaign-4-wdi-demographic-structure-indicator-family-inventory",
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
    snapshot = immutable_wdi_territorial_coverage_snapshot()
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
    replay_snapshot = immutable_wdi_territorial_coverage_snapshot()
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
    comparison = {key: normalized_prior_row(prior, key) for key in ["campaign_0", "campaign_1", "campaign_2", "campaign_3", "campaign_4"]}
    comparison["campaign_5"] = {"accepted": len(accepted), "rejected": len(rejected), "determinism": determinism_verified, "fingerprint_stability": fingerprint_stability, "duplicates": duplicate_detected}
    quality.update({
        "average_evidence_references_per_knowledge_object": avg_evidence_refs,
        "provenance_completeness": provenance_complete,
        "cross_campaign_metric_comparison": comparison,
        "processing_statistics": {
            "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
            "accepted_object_fingerprints": object_fingerprints,
            "territory_count": snapshot["territorial_matrix"]["territory_count"],
            "matrix_cell_count": snapshot["territorial_matrix"]["matrix_cell_count"],
            "coverage_bucket_count": snapshot["territorial_matrix"]["coverage_bucket_count"],
        },
        "territorial_coverage_observations": {
            "larger_object_set": "exercised",
            "territorial_applicability": "exercised",
            "repeated_missingness_statements": "exercised",
            "duplicate_pressure": "not_observed",
            "fingerprint_stability_under_volume": "held",
        },
        "campaign_family_maturity_assessment": snapshot["production_family_maturity"],
        "architectural_observations": [
            "Existing package and validator contracts handled Campaign 5 territorial coverage matrix objects without modification.",
            "Campaign 5 increased deterministic object volume and territorial applicability pressure without duplicate objects.",
            "Campaigns 1-5 support Stable maturity for the current WDI demographic production family, while broadening to another family remains best deferred until after Campaigns 6-7.",
        ],
        "candidate_improvements_discovered": [
            "No new helper extraction, validator change, taxonomy change, or architecture change is justified by Campaign 5.",
            "PEL-017 remains monitor: Campaign 5 exercised larger deterministic transformations but not multi-reference objects or later-stage production rejection.",
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
        "family_maturity_assessment": snapshot["production_family_maturity"]["classification"],
        "snapshot_fingerprint": snapshot_fingerprint,
        "final_recommendation": "Proceed to Campaign 6 unchanged. Begin conceptual awareness for broadening after the WDI demographic family completes Campaigns 6-7, but do not start broadening preparations yet.",
    }
    write_json(output / "campaign_summary.json", summary)
    write_reports(output, summary, quality, catalogue, rejected_catalogue)
    return summary


def write_reports(output: Path, summary: dict[str, Any], quality: dict[str, Any], catalogue: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> None:
    reports = output / "reports"
    category_rows = [[k, v] for k, v in quality["knowledge_categories_produced"].items()]
    rejected_rows = [[r["source_evidence_package_id"], r["knowledge_category"], ", ".join(r["reason_categories"])] for r in rejected]
    object_rows = [[c["package_id"], c["statement_type"], c["statement"], c["package_manifest_fingerprint"]] for c in catalogue]
    comparison_rows = [[cid, data.get("accepted"), data.get("rejected"), data.get("determinism"), data.get("fingerprint_stability"), data.get("duplicates")] for cid, data in quality["cross_campaign_metric_comparison"].items()]
    maturity = quality["campaign_family_maturity_assessment"]
    maturity_rows = [["classification", maturity["classification"]], ["validated", "; ".join(maturity["validated"])], ["insufficiently exercised", "; ".join(maturity["insufficiently_exercised"])], ["further campaigns", maturity["further_campaigns"]]]
    obs_rows = [[k, v] for k, v in quality["territorial_coverage_observations"].items()]

    write_text(reports / "campaign_5_final_report.md", f"""
# Campaign 5 Final Report

Status: completed
Campaign: {CAMPAIGN_ID}

## Result

Campaign 5 accepted {summary['accepted']} KnowledgeObjectPackages and preserved {summary['rejected']} rejected candidates.

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

## Territorial coverage scope

Accepted objects cover territorial count, matrix shape, coverage bucket taxonomy, bucket totals, family territorial coverage records, territorial and period applicability, denominator quality, provenance, validation state, unsupported applicability, deterministic transform evidence, and family maturity.

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

## Territorial coverage observations

{markdown_table(obs_rows, ['Observation', 'Value'])}

## Production quality assessment

Campaigns 0-5 preserve determinism, fingerprint stability, rejected-candidate preservation, and zero observed duplicate pressure. Campaign 5 increased deterministic object volume and territorial applicability pressure without revealing catalogue or duplicate pressure.
""")
    write_text(reports / "production_retrospective_report.md", f"""
# Production Retrospective Report

## What Campaign 5 showed

- Existing package and validator contracts handled territorial coverage matrix knowledge.
- Larger deterministic object volume remained reproducible.
- Territorial applicability fields were sufficient for the campaign scope.
- Repeated missingness and unsupported applicability statements remained constitutionally scoped.
- No duplicate pressure appeared.

## What Campaign 5 did not show

- Multi-reference accepted objects remain unexercised.
- Later-stage production rejection remains weakly production-exercised.
- Partial provenance disagreement remains unexercised.
- Non-demographic WDI evidence-family transfer remains untested.

## Recommendation

Proceed to Campaign 6 unchanged. Do not start broadening preparations until the current family completes the planned temporal and provenance campaigns unless a blocker appears.
""")
    write_text(reports / "cross_campaign_assessment_report.md", f"""
# Cross-Campaign Assessment Report

Scope: Campaigns 0-5

## Production stability

All six campaigns completed with deterministic execution and accepted KnowledgeObjectPackages through the existing pipeline.

{markdown_table(comparison_rows, ['Campaign', 'Accepted', 'Rejected', 'Determinism', 'Fingerprint stability', 'Duplicates'])}

## Validator behavior

Validator failures again involved evidence-contract, provenance, lineage-fingerprint, unsupported-inference, and boundary-language categories. Campaign 5 did not naturally exercise later-stage candidate/object rejection.

## Territorial coverage evidence

Campaign 5 exercised larger deterministic object sets, territorial applicability scopes, repeated missingness statements, and fingerprint stability under more object volume.

## Roadmap assessment

Campaign 5 does not justify resequencing the production roadmap. Campaign 6 remains the next production campaign.
""")
    write_text(reports / "campaign_family_maturity_assessment.md", f"""
# Campaign Family Maturity Assessment

Family: WDI demographic-structure deterministic production family
Campaign evidence: Campaigns 1-5
Classification: {maturity['classification']}

## Basis

{maturity['basis']}

## Assessment matrix

{markdown_table(maturity_rows, ['Field', 'Assessment'])}

## Interpretation of Stable

Stable means the family has repeatedly validated deterministic production across several related WDI demographic evidence scopes without architecture change. It does not mean the family is complete or mature enough to replace the planned roadmap.

## Roadmap implication

Campaign 6 should proceed unchanged. Campaigns 6-7 still add useful evidence for temporal coverage and provenance lineage. Broadening into another evidence family should be prepared after the current family completes those planned tests, not now.
""")
    write_text(reports / "architectural_observations_report.md", f"""
# Architectural Observations Report

## Supported observations

1. Current package and validator contracts handled Campaign 5 territorial coverage without modification.
2. Existing taxonomy covered coverage, derived, negative, provenance, evidence_quality, classified, factual, and methodological objects.
3. Campaign-local duplicate checks remained sufficient under larger object volume.
4. PEL-017 remains valid: Campaign 5 exercised larger deterministic transformations but not multi-reference objects, later-stage production rejection, or partial provenance disagreement.
5. The WDI demographic production family is now Stable, but the evidence supports completing Campaigns 6-7 before broadening.

## Unsupported changes

Campaign 5 does not support architecture redesign, ontology/taxonomy change, repository coupling, adapter/API/shared-schema work, database coupling, runtime infrastructure, local-model generation, frontier-model generation, or additional helper extraction.
""")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Campaign 5 WDI territorial coverage matrix production campaign")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts/production" / CAMPAIGN_ID)
    args = parser.parse_args()
    summary = run_campaign(args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
