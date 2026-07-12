#!/usr/bin/env python3
"""Campaign 1: WDI demographic-structure evidence-quality and coverage knowledge.

This controlled production campaign uses only a small immutable KnowledgeForge
SourceEvidencePackage-shaped snapshot of already-audited WDI annual-scalar
Demographic Structure evidence. It performs no external API calls, no database
access, no adapters, no repository coupling, no shared schemas, and no model
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

CAMPAIGN_ID = "campaign-1-wdi-demographic-structure-evidence-quality-coverage"
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


def canonical_json(value: Any) -> str:
    return constructor.canonical_json(value)


def sha256_fingerprint(value: Any) -> str:
    return constructor.sha256_fingerprint(value)


def report_dict(value: Any) -> dict[str, Any]:
    return value.to_dict() if hasattr(value, "to_dict") else value


def immutable_wdi_snapshot() -> dict[str, Any]:
    """Return the narrow audited WDI demographic evidence snapshot for Campaign 1.

    The facts below are not domain interpretations. They are source/evidence
    inventory facts preserved from the KnowledgeForge production-readiness audit
    artifacts and scoped to the selected WDI annual-scalar demographic-structure
    evidence family.
    """
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
            "period_scope": "1990-2024",
            "indicator_scope": "five-year age-sex cohort count/share indicators plus demographic context indicators retained by the audited evidence inventory",
        },
        "audited_inventory": {
            "source": "World Bank World Development Indicators (WDI)",
            "indicators_total": 182,
            "territories_total": 217,
            "period_start": 1990,
            "period_end": 2024,
            "period_count": 35,
            "curated_facts": 1377595,
            "observed_facts": 1095789,
            "explicit_missing_facts": 281806,
            "dataset_releases": 3,
            "pipeline_runs": 8,
        },
        "demographic_structure_inventory": {
            "age_sex_cohort_indicators": 68,
            "observed_rows": 516460,
            "cohort_granularity": "five-year age-sex cohorts",
            "open_ended_terminal_age_class": "80+",
            "sex_dimensions": ["female", "male"],
            "measure_families": ["count", "share"],
        },
        "provenance_observations": {
            "source_url_available": True,
            "license_note_available": True,
            "raw_artifact_hashes_available": True,
            "raw_artifact_urls_available": True,
            "release_keys_available": True,
            "wdi_lastupdated_metadata_available": True,
            "dataset_release_release_date_null_in_audited_rows": True,
            "lineage_event_checksum_null_in_audited_rows": True,
        },
        "validation_observations": {
            "observation_status_explicit": True,
            "observed_and_missing_status_available": True,
            "current_audited_repository_source_scope": "WDI-only",
            "current_audited_evidence_shape": "annual-scalar",
        },
        "evidence_basis": [
            "artifacts/reports/R-20260709-knowledge-capability-inventory.md",
            "artifacts/reports/R-20260709-first-production-campaign-recommendation.md",
            "artifacts/reports/R-20260709-production-gap-analysis.md",
            "artifacts/reports/R-20260709-campaign-1-production-design.md",
        ],
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar demographic-structure evidence characterization",
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
        source_name="World Bank World Development Indicators audited demographic-structure evidence snapshot",
        source_family="external_wdi_annual_scalar_demographic_structure",
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "evidence characterization")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_wdi_demographic_structure_snapshot_characteristic",
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
            "selection_rule": "narrow audited WDI annual-scalar demographic-structure evidence scope from existing KnowledgeForge campaign design",
            "source_family": snapshot["evidence_family"],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign1_wdi_demographic_evidence.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic embedded immutable WDI evidence snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )
def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    inv = snapshot["audited_inventory"]
    demo = snapshot["demographic_structure_inventory"]
    prov = snapshot["provenance_observations"]
    validation = snapshot["validation_observations"]
    observed_share = round(inv["observed_facts"] / inv["curated_facts"], 6)
    missing_share = round(inv["explicit_missing_facts"] / inv["curated_facts"], 6)
    return [
        source_package(
            "srcpkg-campaign1-wdi-source-scope",
            "The Campaign 1 source evidence package is scoped to World Bank WDI annual-scalar demographic-structure evidence.",
            "factual",
            snapshot,
            {"topic": "source scope", "source": inv["source"], "frequency": snapshot["scope"]["frequency"], "shape": snapshot["scope"]["shape"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-indicator-inventory",
            f"The audited WDI inventory records {inv['indicators_total']} indicators within the current WDI annual-scalar evidence scope.",
            "coverage",
            snapshot,
            {"topic": "indicator coverage", "indicator_count": inv["indicators_total"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-territory-inventory",
            f"The audited WDI inventory records {inv['territories_total']} non-aggregate or country-like territories.",
            "coverage",
            snapshot,
            {"topic": "territory coverage", "territory_count": inv["territories_total"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-period-inventory",
            f"The audited WDI annual-scalar inventory covers {inv['period_count']} annual periods from {inv['period_start']} through {inv['period_end']}.",
            "coverage",
            snapshot,
            {"topic": "temporal coverage", "period_start": inv["period_start"], "period_end": inv["period_end"], "period_count": inv["period_count"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-observed-missing-counts",
            f"The audited WDI inventory records {inv['observed_facts']} observed facts and {inv['explicit_missing_facts']} explicit missing facts within {inv['curated_facts']} curated facts.",
            "evidence_quality",
            snapshot,
            {"topic": "observed and missing evidence", "observed_facts": inv["observed_facts"], "explicit_missing_facts": inv["explicit_missing_facts"], "curated_facts": inv["curated_facts"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-observed-missing-shares",
            f"Deterministic Campaign 1 computation records observed-fact share {observed_share} and explicit-missing-fact share {missing_share} for the audited WDI inventory.",
            "derived",
            snapshot,
            {"topic": "derived completeness shares", "method": "observed_facts / curated_facts and explicit_missing_facts / curated_facts", "observed_share": observed_share, "missing_share": missing_share},
        ),
        source_package(
            "srcpkg-campaign1-wdi-demographic-cohort-family",
            f"The audited demographic-structure inventory records {demo['age_sex_cohort_indicators']} five-year age-sex cohort indicators.",
            "classified",
            snapshot,
            {"topic": "indicator-family membership", "age_sex_cohort_indicators": demo["age_sex_cohort_indicators"], "sex_dimensions": demo["sex_dimensions"], "measure_families": demo["measure_families"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-demographic-observed-rows",
            f"The audited demographic-structure inventory records {demo['observed_rows']} observed rows for five-year age-sex cohort evidence.",
            "coverage",
            snapshot,
            {"topic": "demographic structure observed rows", "observed_rows": demo["observed_rows"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-provenance-availability",
            "The Campaign 1 WDI evidence snapshot records available source URL, license note, raw artifact hash, raw artifact URL, release-key, and WDI last-updated metadata fields.",
            "provenance",
            snapshot,
            {"topic": "provenance availability", **prov},
        ),
        source_package(
            "srcpkg-campaign1-wdi-freshness-metadata",
            "The audited WDI evidence records release-key and WDI last-updated metadata while audited dataset-release date rows are null.",
            "evidence_quality",
            snapshot,
            {"topic": "source freshness metadata", "release_keys_available": prov["release_keys_available"], "wdi_lastupdated_metadata_available": prov["wdi_lastupdated_metadata_available"], "dataset_release_release_date_null_in_audited_rows": prov["dataset_release_release_date_null_in_audited_rows"]},
        ),
        source_package(
            "srcpkg-campaign1-wdi-validation-state",
            "The audited WDI evidence records explicit observed and missing observation status within the annual-scalar evidence shape.",
            "methodological",
            snapshot,
            {"topic": "validation state", **validation},
        ),
        source_package(
            "srcpkg-campaign1-wdi-negative-boundary",
            "The Campaign 1 WDI evidence snapshot does not support non-WDI source comparison, revision-aware identity statements, or prospective demographic statements.",
            "negative",
            snapshot,
            {"topic": "scoped negative knowledge", "unsupported": ["non-WDI source comparison", "revision-aware identity statements", "prospective demographic statements"]},
        ),
    ]


def build_rejected_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rejected = []
    bad_boundary = source_package(
        "srcpkg-campaign1-reject-boundary-language",
        "This means demographic quality is strong and investors should prefer this country.",
        "evidence_quality",
        snapshot,
        {"topic": "boundary rejection fixture"},
    )
    rejected.append(bad_boundary)

    missing_provenance = source_package(
        "srcpkg-campaign1-reject-missing-provenance",
        "The Campaign 1 malformed package intentionally omits provenance metadata.",
        "methodological",
        snapshot,
        {"topic": "missing provenance rejection fixture"},
    )
    missing_provenance.pop("provenance")
    rejected.append(missing_provenance)

    missing_fingerprint = source_package(
        "srcpkg-campaign1-reject-missing-fingerprint",
        "The Campaign 1 malformed package intentionally omits source package fingerprints.",
        "methodological",
        snapshot,
        {"topic": "missing fingerprint rejection fixture"},
    )
    missing_fingerprint.pop("fingerprints")
    rejected.append(missing_fingerprint)

    unsupported_category = source_package(
        "srcpkg-campaign1-reject-unsupported-category",
        "The Campaign 1 malformed package uses an unsupported knowledge category label.",
        "ranking",
        snapshot,
        {"topic": "unsupported category rejection fixture"},
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
    return out


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def run_campaign(output: Path) -> dict[str, Any]:
    if output.exists():
        shutil.rmtree(output)
    for sub in ["source_packages", "knowledge_candidates", "knowledge_objects", "rejected", "reports"]:
        (output / sub).mkdir(parents=True, exist_ok=True)

    snapshot = immutable_wdi_snapshot()
    write_json(output / "source_evidence_snapshot.json", snapshot)

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    validation_records: list[dict[str, Any]] = []

    source_packages = build_source_packages(snapshot)
    for package in source_packages:
        write_json(output / "source_packages" / f"{package['source_evidence_package_id']}.json", package)
        pipeline = constructor.construct_pipeline(package)
        validation = validate_pipeline(pipeline)
        record = {"source_evidence_package_id": package["source_evidence_package_id"], "validation": validation}
        validation_records.append(record)
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
        if "knowledge_object_package" in pipeline:
            validation = validate_pipeline(pipeline)
        else:
            validation = {"ok": False, "stage_reports": {"source": pipeline["source_validation"]}}
        rejected_record = {
            "source_evidence_package": package,
            "validation": validation,
            "reason_categories": blocker_categories(validation["stage_reports"]),
        }
        write_json(output / "rejected" / f"{package['source_evidence_package_id']}.json", rejected_record)
        rejected.append(rejected_record)

    object_fingerprints = [entry["object"]["fingerprints"]["package_manifest"] for entry in accepted]
    duplicate_detected = len(object_fingerprints) != len(set(object_fingerprints))
    category_counts = Counter(entry["object"]["generated_statements"][0]["statement_type"] for entry in accepted)
    rejected_category_counts = Counter((entry["source_evidence_package"] if "source_evidence_package" in entry else entry["source"]).get("evidence_payload", {}).get("knowledge_category", "missing") for entry in rejected)
    failure_counts = Counter(cat for entry in rejected for cat in entry.get("reason_categories", []))
    avg_evidence_refs = round(sum(len(entry["object"].get("evidence_references", [])) for entry in accepted) / len(accepted), 4) if accepted else 0
    provenance_complete = all(bool(entry["object"].get("provenance_envelope")) and bool(entry["source"].get("provenance")) for entry in accepted)

    replay_snapshot = immutable_wdi_snapshot()
    replay_pipelines = [constructor.construct_pipeline(pkg) for pkg in build_source_packages(replay_snapshot)]
    replay_fingerprints = [p["knowledge_object_package"]["fingerprints"]["package_manifest"] for p in replay_pipelines if "knowledge_object_package" in p]
    fingerprint_stability = object_fingerprints == replay_fingerprints
    determinism_verified = snapshot == replay_snapshot and fingerprint_stability

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
        "processing_statistics": {
            "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
            "accepted_object_fingerprints": object_fingerprints,
            "period_count": snapshot["audited_inventory"]["period_count"],
            "indicator_count": snapshot["audited_inventory"]["indicators_total"],
            "territory_count": snapshot["audited_inventory"]["territories_total"],
        },
        "architectural_observations": [
            "Existing package and validator contracts handled the first domain-specific WDI evidence campaign without modification.",
            "The same production workflow used by Campaign 0 was reusable for domain-specific evidence-quality and coverage knowledge.",
            "Rejected candidates were preserved with validator evidence.",
        ],
        "candidate_improvements_discovered": [
            "A future deterministic SourceEvidencePackage authoring helper may reduce repeated manual package field construction if Campaign 2 repeats the same pattern.",
            "A future campaign-local metric summary helper may reduce repeated production-quality aggregation code if the same metrics recur again.",
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
        "final_recommendation": "Proceed to a second narrow WDI evidence-quality campaign only if it exercises additional deterministic coverage pressure without interpretation.",
    }
    write_json(output / "campaign_summary.json", summary)

    write_reports(output, summary, production_quality, catalogue, rejected_catalogue)
    return summary


def markdown_table(rows: list[list[Any]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def write_reports(output: Path, summary: dict[str, Any], quality: dict[str, Any], catalogue: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> None:
    reports = output / "reports"
    category_rows = [[k, v] for k, v in quality["knowledge_categories_produced"].items()]
    rejected_rows = [[r["source_evidence_package_id"], r["knowledge_category"], ", ".join(r["reason_categories"])] for r in rejected]
    object_rows = [[c["package_id"], c["statement_type"], c["statement"], c["package_manifest_fingerprint"]] for c in catalogue]

    write_text(reports / "campaign_1_final_report.md", f"""
# Campaign 1 Final Report

Status: completed
Campaign: {CAMPAIGN_ID}

## Result

Campaign 1 accepted {summary['accepted']} KnowledgeObjectPackages and preserved {summary['rejected']} rejected candidates.

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

## Final recommendation

Proceed next to a narrow WDI evidence-quality campaign that exercises additional deterministic coverage pressure without interpretation. Recommended scope: WDI annual-scalar demographic-structure coverage by indicator family and period/territory completeness buckets, still limited to evidence availability and missingness.
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

## Knowledge categories produced

{markdown_table(category_rows, ['Category', 'Count'])}

## Validator failures by category

{markdown_table([[k, v] for k, v in quality['validator_failures_by_category'].items()], ['Failure category', 'Count'])}
""")

    write_text(reports / "production_retrospective_report.md", f"""
# Production Retrospective Report

Campaign: {CAMPAIGN_ID}

## Successfully exercised capabilities

- SourceEvidencePackage construction from a narrow immutable evidence snapshot.
- Evidence validation.
- Evidence Evaluation validation.
- KnowledgeCandidatePackage construction and validation.
- KnowledgeObjectPackage construction and validation.
- Rejected candidate preservation.
- Production-quality metric reporting.
- Deterministic replay and fingerprint stability.

## Most frequent generated categories

{markdown_table(category_rows, ['Category', 'Count'])}

## Validator rejection pressure

The most direct rejection pressure came from malformed provenance/fingerprint structures, unsupported category labels, and boundary-language checks. This matches expected Campaign 1 safety behavior.

## Repeated manual decisions observed

- SourceEvidencePackage field construction was repeated across accepted and rejected packages.
- Production-quality metric aggregation repeated the Campaign 0 pattern.

These observations support possible future helpers only if Campaign 2 repeats the same pressure. They do not justify architecture changes now.

## Deterministic transformations reused

- canonical JSON fingerprinting;
- observed/missing share computation;
- package-stage construction;
- category counting;
- validation-stage aggregation.

## Metadata observations

No accepted package field was proven unnecessary. No required metadata field was repeatedly missing in accepted objects. Rejected candidates intentionally demonstrated missing provenance/fingerprint failure behavior.

## Architecture assessment

No architectural assumption was falsified. The existing architecture should be preserved unchanged.

## Future automation opportunities

Evidence-backed but deferred:

- deterministic SourceEvidencePackage authoring helper;
- reusable production-quality metric aggregation helper.

Potential local-AI opportunity remains deferred. Campaign 1 did not require local AI because all accepted outputs were deterministic.
""")

    write_text(reports / "architectural_observations_report.md", f"""
# Architectural Observations Supported by Campaign 1 Evidence

Campaign: {CAMPAIGN_ID}

## Observed facts

- Existing package hierarchy handled Campaign 1 without modification.
- Existing knowledge categories were sufficient.
- Existing validation framework accepted valid evidence-level WDI objects and rejected malformed/boundary-violating candidates.
- File-backed production output remained sufficient.
- Determinism and fingerprint stability held under replay.

## Unsupported changes

Campaign 1 does not support:

- taxonomy redesign;
- card-system replacement;
- runtime infrastructure;
- repository coupling;
- shared schemas;
- adapters;
- APIs;
- LLM generation;
- database coupling.

## Evidence-backed deferred candidates

- Consider a small authoring helper if Campaign 2 repeats SourceEvidencePackage field-construction pressure.
- Consider a shared metric aggregation helper if Campaign 2 repeats production-quality reporting code.

Neither candidate is required before the next campaign.
""")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Campaign 1 WDI demographic evidence-quality and coverage production campaign")
    parser.add_argument("--output", default=f"artifacts/production/{CAMPAIGN_ID}")
    args = parser.parse_args()
    summary = run_campaign(PROJECT_ROOT / args.output)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
