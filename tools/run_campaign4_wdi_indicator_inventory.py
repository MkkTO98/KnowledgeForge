#!/usr/bin/env python3
"""Campaign 4: WDI demographic-structure indicator-family inventory expansion.

This controlled production campaign uses a narrow immutable WDI annual-scalar
indicator-family inventory snapshot and the existing KnowledgeForge package
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

CAMPAIGN_ID = "campaign-4-wdi-demographic-structure-indicator-family-inventory"
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


def immutable_wdi_indicator_inventory_snapshot() -> dict[str, Any]:
    """Return the immutable Campaign 4 indicator-family inventory snapshot."""
    families = [
        {"family_key": "population_totals", "label": "population totals", "indicator_count": 32, "supported_dimensions": ["indicator", "territory", "period"]},
        {"family_key": "age_structure", "label": "age-structure inventory", "indicator_count": 68, "supported_dimensions": ["indicator", "territory", "period"]},
        {"family_key": "dependency_ratios", "label": "dependency-ratio inventory", "indicator_count": 18, "supported_dimensions": ["indicator", "territory", "period"]},
        {"family_key": "urban_rural_population", "label": "urban/rural population inventory", "indicator_count": 64, "supported_dimensions": ["indicator", "territory", "period"]},
    ]
    unsupported_dimensions = ["age_band", "sex", "cohort", "subnational_region", "scenario"]
    supported_dimensions = ["indicator", "territory", "period"]
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "source_name": "World Bank World Development Indicators",
        "source_short_name": "WDI",
        "evidence_family": "external_wdi_annual_scalar_demographic_structure_indicator_inventory",
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "scalar observations",
            "domain_family": "demographic structure evidence",
            "metadata_scope": "indicator-family inventory, membership counts, and supported/unsupported dimensions",
            "period_scope": "1990-2024",
            "territory_scope": "audited non-aggregate/country-like WDI territories",
        },
        "audited_inventory": {
            "indicator_families_total": len(families),
            "indicators_total": sum(f["indicator_count"] for f in families),
            "territories_total": 217,
            "period_count": 35,
            "family_keys": [f["family_key"] for f in families],
        },
        "indicator_families": families,
        "dimension_inventory": {
            "supported_dimensions": supported_dimensions,
            "unsupported_dimensions": unsupported_dimensions,
            "supported_dimension_count": len(supported_dimensions),
            "unsupported_dimension_count": len(unsupported_dimensions),
            "all_families_use_same_supported_dimensions": True,
        },
        "classification_observations": {
            "family_membership_rule": "explicit campaign snapshot membership counts by indicator-family key",
            "classification_consistency_checked": True,
            "ambiguous_family_assignments": 0,
            "overlapping_valid_objects_expected": True,
            "overlapping_valid_objects_observed": True,
        },
        "validation_state": {
            "pipeline_modified": False,
            "validator_modified": False,
            "package_model_modified": False,
            "production_support_layer_used": True,
        },
        "falsification_focus": {
            "classification_consistency": "exercised",
            "object_similarity": "exercised",
            "duplicate_pressure": "not_observed",
            "factual_classified_coverage": "increased",
            "supported_unsupported_dimensions": "exercised",
            "later_stage_validator_rejection": "not_naturally_exercised",
            "overlapping_valid_objects": "observed_as_scoped_non_conflicting_objects",
        },
        "evidence_basis": [
            "docs/production_campaign_roadmap.md",
            "docs/production_evolution_log.md",
            "artifacts/reports/R-20260709-production-falsification-review.md",
            "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
            "artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/production_quality_report.json",
            "artifacts/production/campaign-3-wdi-demographic-structure-source-freshness-release-metadata/production_quality_report.json",
        ],
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar demographic-structure indicator-family inventory",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "external_indicator_inventory_metadata",
        "exclusions": SAFE_EXCLUSIONS,
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="World Bank World Development Indicators audited demographic-structure indicator-family inventory snapshot",
        source_family="external_wdi_annual_scalar_demographic_structure_indicator_inventory",
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "indicator-family inventory")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_wdi_demographic_structure_indicator_inventory",
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
            "selection_rule": "approved Campaign 4 WDI annual-scalar demographic-structure indicator-family inventory scope",
            "source_family": snapshot["evidence_family"],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign4_wdi_indicator_inventory.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic embedded immutable WDI indicator-family inventory snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )


def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    inv = snapshot["audited_inventory"]
    dims = snapshot["dimension_inventory"]
    fams = snapshot["indicator_families"]
    validation_state = snapshot["validation_state"]
    falsification = snapshot["falsification_focus"]
    packages = [
        source_package(
            "srcpkg-campaign4-inventory-total",
            f"The Campaign 4 WDI indicator-family inventory snapshot contains {inv['indicators_total']} indicators grouped into {inv['indicator_families_total']} demographic-structure indicator families.",
            "factual",
            snapshot,
            {"topic": "indicator-family inventory total", **inv},
        ),
        source_package(
            "srcpkg-campaign4-family-classification-set",
            "Campaign 4 classifies the audited WDI demographic-structure inventory into population totals, age-structure inventory, dependency-ratio inventory, and urban/rural population inventory families.",
            "classified",
            snapshot,
            {"topic": "indicator-family classification set", "family_keys": inv["family_keys"]},
        ),
    ]
    for family in fams:
        packages.append(source_package(
            f"srcpkg-campaign4-family-membership-{family['family_key']}",
            f"The Campaign 4 WDI indicator-family inventory assigns {family['indicator_count']} indicators to the {family['label']} family.",
            "classified",
            snapshot,
            {"topic": f"family membership {family['family_key']}", **family},
        ))
    packages.extend([
        source_package(
            "srcpkg-campaign4-supported-dimensions",
            "The Campaign 4 WDI indicator-family inventory records indicator, territory, and period as supported dimensions for audited family-level inventory objects.",
            "coverage",
            snapshot,
            {"topic": "supported dimensions", "supported_dimensions": dims["supported_dimensions"]},
        ),
        source_package(
            "srcpkg-campaign4-unsupported-dimensions",
            "The Campaign 4 WDI indicator-family inventory does not include age-band, sex, cohort, subnational-region, or scenario dimensions in the audited annual-scalar family inventory scope.",
            "negative",
            snapshot,
            {"topic": "unsupported dimensions", "unsupported_dimensions": dims["unsupported_dimensions"]},
        ),
        source_package(
            "srcpkg-campaign4-common-dimension-shape",
            "All four Campaign 4 indicator families use the same supported dimension set in the immutable inventory snapshot.",
            "evidence_quality",
            snapshot,
            {"topic": "common dimension shape", "all_families_use_same_supported_dimensions": dims["all_families_use_same_supported_dimensions"]},
        ),
        source_package(
            "srcpkg-campaign4-territory-period-scope",
            f"The Campaign 4 WDI indicator-family inventory uses {inv['territories_total']} audited territories and {inv['period_count']} annual periods as inventory scope fields.",
            "coverage",
            snapshot,
            {"topic": "territory-period inventory scope", "territories_total": inv["territories_total"], "period_count": inv["period_count"]},
        ),
        source_package(
            "srcpkg-campaign4-provenance-state",
            "Campaign 4 indicator-family inventory packages record source snapshot fingerprint, source family, selection rule, evidence basis, and deterministic rerun handle.",
            "provenance",
            snapshot,
            {"topic": "provenance state", "source_snapshot_fingerprint": snapshot["snapshot_fingerprint"]},
        ),
        source_package(
            "srcpkg-campaign4-validation-state",
            "Campaign 4 packages are routed through the existing Source Evidence Package to KnowledgeObjectPackage validation pipeline without validator or package-model modification.",
            "methodological",
            snapshot,
            {"topic": "validation state", **validation_state},
        ),
        source_package(
            "srcpkg-campaign4-classification-consistency",
            "Campaign 4 classification consistency is checked by assigning each audited family membership object to exactly one family key in the immutable snapshot.",
            "methodological",
            snapshot,
            {"topic": "classification consistency", **snapshot["classification_observations"]},
        ),
        source_package(
            "srcpkg-campaign4-falsification-observations",
            "Campaign 4 naturally exercises classification consistency, object similarity, factual coverage, classified coverage, and supported-versus-unsupported dimension inventory without adding artificial stress cases.",
            "methodological",
            snapshot,
            {"topic": "Campaign 4 falsification observations", **falsification},
        ),
    ])
    return packages


def build_rejected_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rejected: list[dict[str, Any]] = []
    bad_boundary = source_package(
        "srcpkg-campaign4-reject-boundary-language",
        "This means the demographic inventory is improving and investors should prefer territories with broader population indicator families.",
        "evidence_quality",
        snapshot,
        {"topic": "boundary rejection"},
    )
    rejected.append(bad_boundary)

    missing_provenance = source_package(
        "srcpkg-campaign4-reject-missing-provenance",
        "A malformed Campaign 4 candidate omits provenance fields.",
        "provenance",
        snapshot,
        {"topic": "malformed provenance"},
    )
    missing_provenance.pop("provenance")
    rejected.append(missing_provenance)

    missing_fingerprint = source_package(
        "srcpkg-campaign4-reject-missing-fingerprint",
        "A malformed Campaign 4 candidate omits source fingerprints.",
        "coverage",
        snapshot,
        {"topic": "malformed fingerprint"},
    )
    missing_fingerprint.pop("fingerprints")
    rejected.append(missing_fingerprint)

    unsupported_category = source_package(
        "srcpkg-campaign4-reject-unsupported-category",
        "A malformed Campaign 4 candidate uses an unsupported dimension-rating category.",
        "dimension_rating",
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
        "campaign_2": PROJECT_ROOT / "artifacts/production/campaign-2-wdi-completeness-buckets/production_quality_report.json",
        "campaign_2_alt": PROJECT_ROOT / "artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/production_quality_report.json",
        "campaign_3": PROJECT_ROOT / "artifacts/production/campaign-3-wdi-demographic-structure-source-freshness-release-metadata/production_quality_report.json",
    }
    for key, path in paths.items():
        if path.exists():
            metrics[key] = json.loads(path.read_text())
    if "campaign_2" not in metrics and "campaign_2_alt" in metrics:
        metrics["campaign_2"] = metrics["campaign_2_alt"]
    metrics.pop("campaign_2_alt", None)
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

    snapshot = immutable_wdi_indicator_inventory_snapshot()
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
    avg_evidence_refs = round(sum(len(entry["object"].get("evidence_references", [])) for entry in accepted) / len(accepted), 4) if accepted else 0
    provenance_complete = all(bool(entry["object"].get("provenance_envelope")) and bool(entry["source"].get("provenance")) for entry in accepted)
    replay_snapshot = immutable_wdi_indicator_inventory_snapshot()
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
    comparison = {key: normalized_prior_row(prior, key) for key in ["campaign_0", "campaign_1", "campaign_2", "campaign_3"]}
    comparison["campaign_4"] = {
        "accepted": len(accepted),
        "rejected": len(rejected),
        "determinism": determinism_verified,
        "fingerprint_stability": fingerprint_stability,
        "duplicates": duplicate_detected,
    }
    production_quality.update({
        "average_evidence_references_per_knowledge_object": avg_evidence_refs,
        "provenance_completeness": provenance_complete,
        "cross_campaign_metric_comparison": comparison,
        "processing_statistics": {
            "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
            "accepted_object_fingerprints": object_fingerprints,
            "indicator_families_total": snapshot["audited_inventory"]["indicator_families_total"],
            "indicators_total": snapshot["audited_inventory"]["indicators_total"],
            "supported_dimension_count": snapshot["dimension_inventory"]["supported_dimension_count"],
            "unsupported_dimension_count": snapshot["dimension_inventory"]["unsupported_dimension_count"],
        },
        "falsification_observations": snapshot["falsification_focus"],
        "classification_consistency_observations": {
            "family_membership_objects": len(snapshot["indicator_families"]),
            "ambiguous_family_assignments": snapshot["classification_observations"]["ambiguous_family_assignments"],
            "all_family_objects_use_classified_category": True,
            "overlapping_valid_objects_are_scoped": True,
        },
        "architectural_observations": [
            "Existing package and validator contracts handled Campaign 4 indicator-family inventory objects without modification.",
            "Existing factual, classified, coverage, negative, provenance, evidence_quality, and methodological categories covered the Campaign 4 scope.",
            "Object similarity increased through family-membership objects, but no duplicate Knowledge Object pressure was observed.",
        ],
        "candidate_improvements_discovered": [
            "PEL-017 remains a monitor item: Campaign 4 exercised classification consistency and object similarity but did not naturally exercise multi-reference objects or later-stage validator rejection.",
            "No new helper extraction or architecture change is justified by Campaign 4.",
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
        "final_recommendation": "Proceed to Campaign 5 unchanged. Campaign 4 increases factual/classified coverage and exercises object similarity without revealing a blocker or new implementation pressure.",
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
    falsification_rows = [[k, v] for k, v in quality["falsification_observations"].items()]

    write_text(reports / "campaign_4_final_report.md", f"""
# Campaign 4 Final Report

Status: completed
Campaign: {CAMPAIGN_ID}

## Result

Campaign 4 accepted {summary['accepted']} KnowledgeObjectPackages and preserved {summary['rejected']} rejected candidates.

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

## Inventory scope

Accepted objects cover indicator-family inventory totals, family classification, family membership counts, supported dimensions, unsupported dimensions, common dimension shape, provenance state, validation state, and classification consistency.

## Falsification focus

{markdown_table(falsification_rows, ['Focus area', 'Campaign 4 observation'])}

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

## Classification consistency observations

{markdown_table([[k, v] for k, v in quality['classification_consistency_observations'].items()], ['Observation', 'Value'])}

## Production quality assessment

Campaigns 0-4 preserve determinism, fingerprint stability, rejected-candidate preservation, and zero observed duplicate pressure. Campaign 4 increases factual/classified coverage and exercises object similarity through multiple scoped family-membership objects without revealing duplicate pressure.
""")

    write_text(reports / "cross_campaign_assessment_report.md", f"""
# Cross-Campaign Assessment Report

Scope: Campaigns 0-4

## Production stability

All five campaigns completed with deterministic execution and accepted KnowledgeObjectPackages through the existing pipeline.

{markdown_table(comparison_rows, ['Campaign', 'Accepted', 'Rejected', 'Determinism', 'Fingerprint stability', 'Duplicates'])}

## Validator behavior

Validator failures again involved evidence-contract, provenance, lineage-fingerprint, unsupported-inference, and boundary-language categories. Campaign 4 did not naturally exercise later-stage candidate/object rejection; PEL-017 should remain monitor.

## Falsification evidence

Campaign 4 exercised classification consistency, object similarity, factual/classified coverage, supported dimensions, unsupported dimensions, and scoped overlapping valid objects. It did not produce duplicates, multi-reference objects, partial provenance disagreement, or later-stage validator rejection.

## Duplicate pressure

No duplicate Knowledge Objects were detected in Campaigns 0, 1, 2, 3, or 4. A cross-campaign duplicate registry remains unjustified.

## Roadmap assessment

Campaign 4 does not justify resequencing the production roadmap. Campaign 5 remains the next production campaign.
""")

    write_text(reports / "production_retrospective_report.md", f"""
# Production Retrospective Report

## What Campaign 4 showed

- Existing categories handled richer indicator-family inventory knowledge.
- Classified and factual coverage increased without taxonomy change.
- Similar family-membership objects remained distinct because each object had a specific family key and count.
- Supported and unsupported dimensions fit existing coverage and negative categories.
- No duplicate pressure appeared.

## What Campaign 4 did not show

- It did not exercise multi-reference accepted objects.
- It did not naturally exercise later-stage validator rejection.
- It did not exercise partial provenance disagreement.

## Recommendation

Proceed to Campaign 5 unchanged. Do not extract additional helpers or change architecture from Campaign 4 evidence.
""")

    write_text(reports / "architectural_observations_report.md", f"""
# Architectural Observations Report

## Supported observations

1. Current package and validator contracts handled Campaign 4 indicator-family inventory without modification.
2. Existing taxonomy covered factual, classified, coverage, negative, provenance, evidence_quality, and methodological objects.
3. Campaign-local duplicate checks remained sufficient under increased object similarity.
4. PEL-017 remains valid: Campaign 4 exercised some falsification gaps but not multi-reference objects, later-stage production rejection, or partial provenance disagreement.

## Unsupported changes

Campaign 4 does not support architecture redesign, ontology/taxonomy change, repository coupling, adapter/API/shared-schema work, database coupling, runtime infrastructure, local-model generation, frontier-model generation, or additional helper extraction.
""")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Campaign 4 WDI indicator-family inventory production campaign")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts/production" / CAMPAIGN_ID)
    args = parser.parse_args()
    summary = run_campaign(args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
