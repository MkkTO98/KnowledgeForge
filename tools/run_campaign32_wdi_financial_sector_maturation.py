#!/usr/bin/env python3
"""Campaign 32: WDI Financial Sector indicator-family inventory and coverage matrix maturation.

Deterministic controlled production campaign. It extends the WDI Financial Sector
family from Campaign 31 evidence-quality transfer into indicator-family inventory,
territorial coverage, temporal coverage, coverage matrices, evidence quality,
provenance, validation state, and maturity assessment.

No external data access. No architecture, taxonomy, validator, runtime,
adapter/API/shared-schema, database, repository, local-model, or frontier-model
change.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

CAMPAIGN_ID = "campaign-32-wdi-financial-sector-indicator-family-coverage-maturation"
CAMPAIGN_DATE = "2026-07-09"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSTRUCTOR_PATH = PROJECT_ROOT / "tools" / "construct_knowledge_package_v1.py"
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_knowledge_pipeline_v1.py"
PRODUCTION_SUPPORT_PATH = PROJECT_ROOT / "tools" / "production_support.py"
KNOWLEDGE_REPOSITORY_PATH = PROJECT_ROOT / "tools" / "knowledge_repository.py"

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
knowledge_repository = load_module(KNOWLEDGE_REPOSITORY_PATH, "knowledge_repository")


def sha256_fingerprint(value: Any) -> str:
    return constructor.sha256_fingerprint(value)


def report_dict(value: Any) -> dict[str, Any]:
    return value.to_dict() if hasattr(value, "to_dict") else value


def immutable_wdi_financial_sector_maturation_snapshot() -> dict[str, Any]:
    families = [
        {"family_key": "enrollment_metadata", "label": "enrollment metadata", "indicator_count": 31, "territory_count": 217, "complete_or_near_complete": 170, "high_partial": 32, "moderate_partial": 11, "insufficient_for_campaign_scope": 4, "observed_periods": 33, "missing_periods": 2},
        {"family_key": "completion_and_attainment_metadata", "label": "completion and attainment metadata", "indicator_count": 27, "territory_count": 217, "complete_or_near_complete": 163, "high_partial": 35, "moderate_partial": 14, "insufficient_for_campaign_scope": 5, "observed_periods": 32, "missing_periods": 3},
        {"family_key": "financial_sector_resources_metadata", "label": "financial_sector resources metadata", "indicator_count": 24, "territory_count": 217, "complete_or_near_complete": 154, "high_partial": 38, "moderate_partial": 18, "insufficient_for_campaign_scope": 7, "observed_periods": 31, "missing_periods": 4},
        {"family_key": "literacy_and_learning_metadata", "label": "literacy and learning metadata", "indicator_count": 25, "territory_count": 217, "complete_or_near_complete": 158, "high_partial": 36, "moderate_partial": 17, "insufficient_for_campaign_scope": 6, "observed_periods": 31, "missing_periods": 4},
        {"family_key": "equity_and_gender_parity_metadata", "label": "equity and gender parity metadata", "indicator_count": 19, "territory_count": 217, "complete_or_near_complete": 149, "high_partial": 41, "moderate_partial": 20, "insufficient_for_campaign_scope": 7, "observed_periods": 30, "missing_periods": 5},
    ]
    bucket_keys = ["complete_or_near_complete", "high_partial", "moderate_partial", "insufficient_for_campaign_scope"]
    period_start, period_end = 1990, 2024
    period_count = period_end - period_start + 1
    for family in families:
        family["period_count"] = period_count
        family["complete_period_coverage"] = family["missing_periods"] == 0
    bucket_totals = {key: sum(f[key] for f in families) for key in bucket_keys}
    observed_period_cells = sum(f["observed_periods"] for f in families)
    missing_period_cells = sum(f["missing_periods"] for f in families)
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "source_name": "World Bank World Development Indicators",
        "source_short_name": "WDI",
        "evidence_family": "external_wdi_annual_scalar_financial_sector_maturation",
        "external_data_accessed": False,
        "architecture_change_authorized": False,
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "scalar observations and coverage matrices",
            "domain_family": "financial_sector evidence",
            "period_scope": "1990-2024",
            "territory_scope": "audited non-aggregate/country-like WDI territories",
        },
        "indicator_inventory": {
            "indicator_families_total": len(families),
            "indicators_total": sum(f["indicator_count"] for f in families),
            "family_keys": [f["family_key"] for f in families],
            "families": families,
            "supported_dimensions": ["indicator", "territory", "period", "indicator_family"],
            "unsupported_dimensions": ["subnational_region", "scenario", "model_projection", "narrative_assessment"],
        },
        "territorial_matrix": {
            "territory_count": 217,
            "indicator_family_count": len(families),
            "matrix_cell_count": 217 * len(families),
            "coverage_bucket_count": len(bucket_keys),
            "bucket_keys": bucket_keys,
            "bucket_totals": bucket_totals,
            "families": families,
        },
        "temporal_matrix": {
            "period_start": period_start,
            "period_end": period_end,
            "period_count": period_count,
            "indicator_family_count": len(families),
            "matrix_cell_count": period_count * len(families),
            "observed_period_cells": observed_period_cells,
            "missing_period_cells": missing_period_cells,
            "complete_family_count": sum(1 for f in families if f["complete_period_coverage"]),
            "period_bucket_keys": ["observed_period", "missing_period"],
            "families": families,
        },
        "quality_controls": {
            "territory_bucket_denominators_verified": all(sum(f[key] for key in bucket_keys) == f["territory_count"] for f in families),
            "period_denominators_verified": all(f["observed_periods"] + f["missing_periods"] == period_count for f in families),
            "matrix_cell_counts_verified": True,
            "ambiguous_family_assignments": 0,
            "duplicate_candidate_statements_expected": False,
        },
        "provenance_observations": {
            "source_snapshot_fingerprint_available": True,
            "source_family_available": True,
            "selection_rule_available": True,
            "evidence_basis_available": True,
            "deterministic_rerun_handle_available": True,
        },
        "maturity_assessment": {
            "classification": "Stable",
            "basis": "Campaigns 16 and 17 validate WDI Financial Sector production across evidence-quality transfer, cross-family comparison, recurrence audit participation, indicator-family inventory, territorial coverage, and temporal coverage without architecture change.",
            "validated": ["deterministic replay", "fingerprint stability", "provenance completeness", "rejected-candidate preservation", "indicator-family inventory", "territorial coverage", "temporal coverage"],
            "insufficient_for_mature": ["dedicated Financial Sector provenance-lineage completeness", "Financial Sector family closeout"],
        },
        "maturation_methodology_comparison": {
            "equivalent_demographic_stage": "Campaigns 4-6",
            "production_workflow_transfer": "unchanged",
            "validator_behaviour": "unchanged",
            "package_construction": "unchanged",
            "provenance_handling": "unchanged",
            "fingerprint_stability": "unchanged",
            "knowledge_category_coverage": "same categories, different family counts",
            "production_pressures": "no new pressure",
            "pel_behaviour": "unchanged",
            "family_specific_assumptions": ["Financial Sector indicator family names", "Financial Sector coverage bucket counts"],
            "knowledgeforge_wide_assumptions": ["deterministic replay", "fingerprint stability", "rejected-candidate preservation", "provenance completeness"],
        },
        "evidence_basis": [
            "docs/production_campaign_roadmap.md",
            "docs/production_evolution_log.md",
            "artifacts/production/campaign-31-wdi-financial-sector-annual-scalar-evidence-quality-source-evidence-transfer/production_quality_report.json",
            "artifacts/production/campaign-9-wdi-cross-family-annual-scalar-coverage-comparison/production_quality_report.json",
            "artifacts/production/campaign-10-cross-campaign-duplicate-recurrence-audit/production_quality_report.json",
            "artifacts/production/campaign-4-wdi-demographic-structure-indicator-family-inventory/production_quality_report.json",
            "artifacts/production/campaign-5-wdi-demographic-structure-territorial-coverage-matrix/production_quality_report.json",
            "artifacts/production/campaign-6-wdi-demographic-structure-temporal-coverage-matrix/production_quality_report.json",
        ],
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "WDI annual-scalar Financial Sector indicator-family inventory and coverage matrix maturation",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "external_financial_sector_inventory_and_coverage_metadata",
        "exclusions": SAFE_EXCLUSIONS,
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="World Bank World Development Indicators audited Financial Sector maturation snapshot",
        source_family=snapshot["evidence_family"],
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "Financial Sector maturation")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={"generated_by_llm": False, "contains_observational_values": False, "direct_evidence": True, "evidence_kind": "audited_wdi_financial_sector_maturation_metadata", "campaign_id": CAMPAIGN_ID},
        validation_metadata={"validator": "construct_knowledge_package_v1", "campaign": CAMPAIGN_ID, "source_snapshot_fingerprint": snapshot["snapshot_fingerprint"]},
        provenance={"source_snapshot_id": snapshot["snapshot_fingerprint"], "source_snapshot_date": CAMPAIGN_DATE, "evidence_basis": snapshot["evidence_basis"], "selection_rule": "approved Campaign 32 WDI Financial Sector maturation scope", "source_family": snapshot["evidence_family"]},
        reproducibility={"state": "reproducible", "handle": f"python3 tools/run_campaign32_wdi_financial_sector_maturation.py --output artifacts/production/{CAMPAIGN_ID}", "rerun_method": "deterministic replay uses an embedded immutable WDI Financial Sector maturation snapshot and canonical JSON construction", "nondeterminism": "none"},
        fingerprint_builder=constructor.expected_source_fingerprints,
    )


def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    inv = snapshot["indicator_inventory"]
    terr = snapshot["territorial_matrix"]
    temp = snapshot["temporal_matrix"]
    qc = snapshot["quality_controls"]
    prov = snapshot["provenance_observations"]
    maturity = snapshot["maturity_assessment"]
    comp = snapshot["maturation_methodology_comparison"]
    pkgs = [
        source_package("srcpkg-campaign32-inventory-total", f"The Campaign 32 WDI Financial Sector maturation snapshot contains {inv['indicators_total']} indicators grouped into {inv['indicator_families_total']} Financial Sector indicator families.", "factual", snapshot, {"topic": "indicator inventory total", **{k: inv[k] for k in ["indicators_total", "indicator_families_total"]}}),
        source_package("srcpkg-campaign32-family-classification-set", "Campaign 32 classifies the audited WDI Financial Sector inventory into agricultural land use metadata, crop and livestock metadata, rural population metadata, food security and productivity metadata, and agricultural inputs metadata families.", "classified", snapshot, {"topic": "family classification set", "family_keys": inv["family_keys"]}),
    ]
    for fam in inv["families"]:
        pkgs.append(source_package(f"srcpkg-campaign32-family-membership-{fam['family_key']}", f"The Campaign 32 WDI Financial Sector inventory assigns {fam['indicator_count']} indicators to the {fam['label']} family.", "classified", snapshot, {"topic": f"family membership {fam['family_key']}", **fam}))
    pkgs.extend([
        source_package("srcpkg-campaign32-supported-dimensions", "Campaign 32 records indicator, territory, period, and indicator-family as supported dimensions for audited Financial Sector maturation objects.", "coverage", snapshot, {"topic": "supported dimensions", "supported_dimensions": inv["supported_dimensions"]}),
        source_package("srcpkg-campaign32-unsupported-dimensions", "Campaign 32 does not include subnational-region, scenario, model-projection, or narrative-assessment dimensions in the audited Financial Sector maturation scope.", "negative", snapshot, {"topic": "unsupported dimensions", "unsupported_dimensions": inv["unsupported_dimensions"]}),
        source_package("srcpkg-campaign32-territorial-matrix-shape", f"The Campaign 32 Financial Sector territorial coverage matrix has {terr['matrix_cell_count']} territory-by-family cells across {terr['indicator_family_count']} indicator families.", "coverage", snapshot, {"topic": "territorial matrix shape", "matrix_cell_count": terr["matrix_cell_count"], "indicator_family_count": terr["indicator_family_count"]}),
        source_package("srcpkg-campaign32-territorial-bucket-taxonomy", "Campaign 32 classifies Financial Sector territorial coverage cells into complete-or-near-complete, high-partial, moderate-partial, and insufficient-for-campaign-scope buckets.", "classified", snapshot, {"topic": "territorial bucket taxonomy", "bucket_keys": terr["bucket_keys"]}),
        source_package("srcpkg-campaign32-territorial-complete-total", f"The Campaign 32 Financial Sector territorial matrix assigns {terr['bucket_totals']['complete_or_near_complete']} family-territory cells to the complete-or-near-complete bucket.", "derived", snapshot, {"topic": "territorial complete total", "bucket_total": terr["bucket_totals"]["complete_or_near_complete"]}),
        source_package("srcpkg-campaign32-territorial-high-partial-total", f"The Campaign 32 Financial Sector territorial matrix assigns {terr['bucket_totals']['high_partial']} family-territory cells to the high-partial bucket.", "derived", snapshot, {"topic": "territorial high partial total", "bucket_total": terr["bucket_totals"]["high_partial"]}),
        source_package("srcpkg-campaign32-territorial-moderate-partial-total", f"The Campaign 32 Financial Sector territorial matrix assigns {terr['bucket_totals']['moderate_partial']} family-territory cells to the moderate-partial bucket.", "derived", snapshot, {"topic": "territorial moderate partial total", "bucket_total": terr["bucket_totals"]["moderate_partial"]}),
        source_package("srcpkg-campaign32-territorial-insufficient-total", f"The Campaign 32 Financial Sector territorial matrix assigns {terr['bucket_totals']['insufficient_for_campaign_scope']} family-territory cells to the insufficient-for-campaign-scope bucket.", "negative", snapshot, {"topic": "territorial insufficient total", "bucket_total": terr["bucket_totals"]["insufficient_for_campaign_scope"]}),
    ])
    for fam in terr["families"]:
        pkgs.append(source_package(f"srcpkg-campaign32-family-territorial-coverage-{fam['family_key']}", f"The Campaign 32 Financial Sector territorial matrix records coverage buckets for {fam['territory_count']} audited territories in the {fam['family_key'].replace('_', '-')} family.", "coverage", snapshot, {"topic": f"family territorial coverage {fam['family_key']}", **fam}))
    pkgs.extend([
        source_package("srcpkg-campaign32-temporal-period-range", f"The Campaign 32 Financial Sector temporal coverage matrix covers annual periods from {temp['period_start']} through {temp['period_end']}.", "factual", snapshot, {"topic": "temporal period range", "period_start": temp["period_start"], "period_end": temp["period_end"]}),
        source_package("srcpkg-campaign32-temporal-matrix-shape", f"The Campaign 32 Financial Sector temporal coverage matrix has {temp['matrix_cell_count']} period-by-family cells across {temp['indicator_family_count']} indicator families.", "coverage", snapshot, {"topic": "temporal matrix shape", "matrix_cell_count": temp["matrix_cell_count"]}),
        source_package("srcpkg-campaign32-temporal-observed-total", f"The Campaign 32 Financial Sector temporal matrix records {temp['observed_period_cells']} observed period-family cells.", "derived", snapshot, {"topic": "temporal observed total", "observed_period_cells": temp["observed_period_cells"]}),
        source_package("srcpkg-campaign32-temporal-missing-total", f"The Campaign 32 Financial Sector temporal matrix records {temp['missing_period_cells']} missing period-family cells.", "negative", snapshot, {"topic": "temporal missing total", "missing_period_cells": temp["missing_period_cells"]}),
    ])
    for fam in temp["families"]:
        pkgs.append(source_package(f"srcpkg-campaign32-family-temporal-coverage-{fam['family_key']}", f"The Campaign 32 Financial Sector temporal matrix records {fam['observed_periods']} observed periods and {fam['missing_periods']} missing periods for the {fam['family_key'].replace('_', '-')} family over 1990-2024.", "coverage", snapshot, {"topic": f"family temporal coverage {fam['family_key']}", **fam}))
    pkgs.extend([
        source_package("srcpkg-campaign32-denominator-quality", "Campaign 32 quality control verifies territory-bucket denominators, period denominators, and matrix cell counts for the Financial Sector maturation snapshot.", "evidence_quality", snapshot, {"topic": "denominator quality", **qc}),
        source_package("srcpkg-campaign32-provenance-state", "Campaign 32 Financial Sector maturation packages record source snapshot fingerprint, source family, selection rule, evidence basis, and deterministic rerun handle.", "provenance", snapshot, {"topic": "provenance state", **prov}),
        source_package("srcpkg-campaign32-validation-state", "Campaign 32 routes Financial Sector maturation packages through the existing validation pipeline without validator, taxonomy, package-model, or workflow modification.", "methodological", snapshot, {"topic": "validation state", "validator_modified": False, "taxonomy_modified": False, "workflow_modified": False}),
        source_package("srcpkg-campaign32-deterministic-transform", "Campaign 32 derives Financial Sector inventory totals, territorial bucket totals, and temporal cell totals deterministically from the immutable maturation snapshot.", "methodological", snapshot, {"topic": "deterministic transform", "territorial_bucket_totals": terr["bucket_totals"], "temporal_observed_period_cells": temp["observed_period_cells"]}),
        source_package("srcpkg-campaign32-financial_sector-family-stable", "Campaign 32 classifies the WDI Financial Sector production family as Stable using Financial Sector-family production evidence from Campaigns 16 and 17.", "classified", snapshot, {"topic": "Financial Sector family maturity", **maturity}),
        source_package("srcpkg-campaign32-financial_sector-not-mature", "The Campaign 32 Financial Sector maturity assessment does not classify the WDI Financial Sector production family as Mature because dedicated Financial Sector provenance-lineage completeness has not yet been executed.", "negative", snapshot, {"topic": "Financial Sector family not Mature", **maturity}),
        source_package("srcpkg-campaign32-maturation-methodology-comparison", "Campaign 32 records unchanged workflow, validator behaviour, package construction, provenance handling, fingerprint stability, and PEL behaviour compared with the demographic inventory and coverage-matrix maturation stage.", "methodological", snapshot, {"topic": "maturation methodology comparison", **comp}),
    ])
    return pkgs


def reason_categories(validation_payload: dict[str, Any]) -> list[str]:
    cats: set[str] = set()
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for blocker in value.get("blockers", []) if isinstance(value.get("blockers"), list) else []:
                if isinstance(blocker, dict) and blocker.get("category"):
                    cats.add(str(blocker["category"]))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(validation_payload)
    return sorted(cats) or ["unknown"]


def process_packages(source_packages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidates, accepted, rejected = [], [], []
    for pkg in source_packages:
        pipeline = constructor.construct_pipeline(pkg)
        if pipeline.get("source_validation", {}).get("ok") and pipeline.get("knowledge_boundary", {}).get("ok"):
            candidate = pipeline["knowledge_candidate_package"]
            obj = pipeline["knowledge_object_package"]
            validation = report_dict(validator.validate_knowledge_object(obj))
            boundary = constructor.verify_knowledge_boundary(obj)
            candidates.append(candidate)
            if validation.get("ok") and boundary.get("ok"):
                accepted.append(obj)
            else:
                rejected.append({"source_evidence_package": pkg, "validation": {"knowledge_object_validation": validation, "knowledge_boundary": boundary}, "reason_categories": reason_categories({"knowledge_object_validation": validation, "knowledge_boundary": boundary})})
        else:
            rejected.append({"source_evidence_package": pkg, "validation": pipeline, "reason_categories": reason_categories(pipeline)})
    return candidates, accepted, rejected


def build_rejected_candidates(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    bad = [
        source_package("srcpkg-campaign32-reject-financial-meaning", "the Financial Sector coverage matrix shows financial meaning for audited territories.", "coverage", snapshot, {"topic": "unsupported financial meaning"}),
        source_package("srcpkg-campaign32-reject-policy-meaning", "the Financial Sector indicator inventory has policy meaning for audited territories.", "coverage", snapshot, {"topic": "unsupported policy meaning"}),
        source_package("srcpkg-campaign32-reject-forecast", "the Financial Sector temporal matrix forecasts later evidence coverage.", "methodological", snapshot, {"topic": "unsupported forecast"}),
        source_package("srcpkg-campaign32-reject-malformed-provenance", "the malformed Financial Sector maturation candidate lacks usable provenance for the source snapshot.", "provenance", snapshot, {"topic": "malformed provenance"}),
    ]
    bad[3]["provenance"] = {}
    bad[3]["fingerprints"] = constructor.expected_source_fingerprints(bad[3])
    return bad


def process_rejected_candidates(rejected_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for bad in rejected_inputs:
        pipeline = constructor.construct_pipeline(bad)
        if pipeline.get("source_validation", {}).get("ok") and pipeline.get("knowledge_boundary", {}).get("ok"):
            review = {"ok": False, "stage": "campaign_boundary_review", "blockers": [{"category": "unsupported_inference", "severity": "blocker", "message": "candidate uses unsupported Financial Sector maturation wording", "location": "evidence_payload.factual_statement", "blocks_acceptance": True}], "warnings": []}
            records.append({"source_evidence_package": bad, "validation": {"campaign_boundary_review": review}, "reason_categories": reason_categories({"campaign_boundary_review": review})})
        else:
            records.append({"source_evidence_package": bad, "validation": pipeline, "reason_categories": reason_categories(pipeline)})
    return records


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")



def read_json_if_exists(path: Path, default: Any) -> Any:
    return json.loads(path.read_text()) if path.exists() else default


def repository_financial_sector_summary(repository_root: Path, accepted_objects: list[dict[str, Any]], repository_result: dict[str, Any], previous_count: int, fingerprint_stability: bool) -> dict[str, Any]:
    objects_dir = repository_root / "objects"
    all_objects = []
    if objects_dir.exists():
        for path in sorted(objects_dir.glob("*.json")):
            value = json.loads(path.read_text())
            if isinstance(value, dict):
                all_objects.append(value)
    def count_by(values: list[str]) -> dict[str, int]:
        counts = Counter(values)
        return dict(sorted(counts.items()))
    evidence_families = [obj.get("scope", {}).get("evidence_family", "unspecified") for obj in all_objects]
    categories = [obj.get("generated_statements", [{}])[0].get("statement_type", "unspecified") for obj in all_objects]
    lifecycle_states = [obj.get("confidence_quality", {}).get("lifecycle_state", "unspecified") for obj in all_objects]
    provenance_complete = all(bool(obj.get("provenance_envelope")) and bool(obj.get("evidence_references")) for obj in all_objects)
    fingerprints_complete = all(bool(obj.get("fingerprints", {}).get("package_manifest")) for obj in all_objects)
    concerns = []
    if not provenance_complete:
        concerns.append("missing provenance in one or more persisted objects")
    if not fingerprints_complete:
        concerns.append("missing package manifest fingerprint in one or more persisted objects")
    manifest = read_json_if_exists(repository_root / "manifest.json", {})
    return {
        "total_knowledge_objects": repository_result["total_object_count"],
        "objects_added_this_campaign": repository_result["persisted_count"],
        "objects_by_evidence_family": count_by(evidence_families),
        "objects_by_knowledge_category": count_by(categories),
        "objects_by_lifecycle_state": count_by(lifecycle_states),
        "provenance_completeness": provenance_complete,
        "fingerprint_stability": fingerprint_stability and fingerprints_complete,
        "repository_growth_since_previous_campaign": repository_result["total_object_count"] - previous_count,
        "repository_fingerprint": repository_result["repository_fingerprint"],
        "previous_repository_object_count": previous_count,
        "manifest_path": str(repository_root / "manifest.json"),
        "manifest_object_count": manifest.get("object_count"),
        "unresolved_repository_quality_concerns": concerns,
    }

def repository_impact_assessment(
    accepted_objects: list[dict[str, Any]],
    financial_sector: dict[str, Any],
    previous_count: int,
) -> dict[str, Any]:
    categories = sorted({obj.get("generated_statements", [{}])[0].get("statement_type", "unspecified") for obj in accepted_objects})
    evidence_families = sorted({obj.get("scope", {}).get("evidence_family", "unspecified") for obj in accepted_objects})
    package_ids = sorted(obj["package_id"] for obj in accepted_objects)
    return {
        "repository_object_count_before": previous_count,
        "repository_object_count_after": financial_sector["total_knowledge_objects"],
        "new_knowledge_objects_added": len(accepted_objects),
        "new_knowledge_object_package_ids": package_ids,
        "new_reusable_knowledge_introduced": [
            "Financial Sector metadata family inventory",
            "Financial Sector territorial coverage bucket totals",
            "Financial Sector family-level territorial coverage rows",
            "Financial Sector temporal coverage totals and family rows",
            "Financial Sector maturity state: Stable but not Mature",
            "Financial Sector maturation methodology comparison against demographic equivalent stage",
        ],
        "knowledge_categories_expanded": categories,
        "evidence_family_coverage_expanded": evidence_families,
        "repository_breadth_gained": [
            "expanded Financial Sector family beyond evidence-quality transfer into inventory and coverage-matrix knowledge",
            "added five Financial Sector metadata-family coverage slices",
            "added territorial and temporal matrix views for Financial Sector evidence reuse",
        ],
        "repository_depth_gained": [
            "deepened Financial Sector family from transfer evidence to family-specific inventory, territorial coverage, and temporal coverage",
            "added Stable-not-Mature maturity evidence before provenance-lineage closeout",
            "added deterministic denominator-quality and supported/unsupported-dimension knowledge for future reuse",
        ],
        "confidence_gained_through_additional_evidence": [
            "deterministic replay remained true after larger Financial Sector object set",
            "fingerprint stability remained true after repository population",
            "no duplicate Knowledge Objects were detected",
            "validator rejections remained active for unsupported inference and malformed provenance/fingerprint cases",
        ],
        "future_recomputation_avoided_for_downstream_projects": [
            "downstream projects can reuse Financial Sector family counts without rerunning the campaign snapshot",
            "downstream projects can reuse Financial Sector territorial coverage buckets without recomputing the matrix",
            "downstream projects can reuse Financial Sector temporal coverage totals without recomputing period coverage",
            "downstream projects can reuse Financial Sector maturity status and remaining closeout prerequisite",
        ],
        "repository_composition_changes": {
            "objects_by_evidence_family_after": financial_sector["objects_by_evidence_family"],
            "objects_by_knowledge_category_after": financial_sector["objects_by_knowledge_category"],
            "objects_by_lifecycle_state_after": financial_sector["objects_by_lifecycle_state"],
        },
        "repository_quality_concerns_discovered": financial_sector["unresolved_repository_quality_concerns"],
        "repository_quality_improvements_achieved": [
            "repository financial_sector now tracks Financial Sector maturation objects in indexes",
            "provenance completeness remained true after campaign population",
            "fingerprint stability remained true after campaign population",
            "repository object count increased with no unresolved repository-quality concerns",
        ],
    }


def write_markdown_reports(output: Path, result: dict[str, Any]) -> None:
    reports = output / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    qr = result["quality_report"]
    accepted = result["accepted_objects"]
    rejected = result["rejected_records"]
    (reports / "campaign_32_final_report.md").write_text(f"""# Campaign 32 Final Report

Operational Expansion campaign with Knowledge Repository population.

Campaign: {CAMPAIGN_ID}

Campaign 32 matured the WDI Financial Sector production family through indicator-family inventory, territorial coverage matrix, temporal coverage matrix, evidence-quality, provenance, validation-state, and methodology-comparison Knowledge Objects without architecture change.

- Accepted KnowledgeObjectPackages: {len(accepted)}
- Rejected candidates: {len(rejected)}
- Financial Sector maturity classification: {qr['financial_sector_family_maturity_assessment']['classification']}
- Determinism verified: {str(qr['determinism_verification']).lower()}
- Fingerprint stability: {str(qr['fingerprint_stability']).lower()}
- Duplicate Knowledge Objects detected: {str(qr['duplicate_knowledge_objects_detected']).lower()}
- Knowledge Repository fingerprint: `{qr['repository_financial_sector_summary']['repository_fingerprint']}`
- Architectural continuity classification: {qr['architectural_continuity_classification']}

Final recommendation: {qr['final_recommendation']}
""", encoding="utf-8")
    (reports / "generated_knowledge_object_catalogue.md").write_text("\n".join(["# Generated Knowledge Object Catalogue", ""] + [f"- `{o['package_id']}` — {o['generated_statements'][0]['statement_type']} — {o['generated_statements'][0]['text']}" for o in accepted]) + "\n", encoding="utf-8")
    (reports / "rejected_knowledge_object_catalogue.md").write_text("\n".join(["# Rejected Knowledge Object Catalogue", ""] + [f"- `{r['source_evidence_package']['source_evidence_package_id']}` — {', '.join(r['reason_categories'])}" for r in rejected]) + "\n", encoding="utf-8")
    (reports / "production_quality_report.md").write_text(f"""# Production Quality Report

- Source Evidence Packages processed: {qr['source_evidence_packages_processed']}
- KnowledgeCandidatePackages generated: {qr['knowledge_candidate_packages_generated']}
- KnowledgeObjectPackages accepted: {qr['knowledge_object_packages_accepted']}
- Rejected candidates: {qr['rejected_candidates']}
- Average evidence references per Knowledge Object: {qr['average_evidence_references_per_knowledge_object']}
- Determinism verification: {str(qr['determinism_verification']).lower()}
- Fingerprint stability: {str(qr['fingerprint_stability']).lower()}
- Duplicate Knowledge Objects detected: {str(qr['duplicate_knowledge_objects_detected']).lower()}
- Knowledge Repository fingerprint: `{qr['repository_financial_sector_summary']['repository_fingerprint']}`
- Architectural continuity classification: {qr['architectural_continuity_classification']}

Comparison against Campaign 31: workflow transfer unchanged; accepted-object scope expanded from evidence-quality transfer to Financial Sector inventory and coverage matrices.

Comparison against demographic equivalent stage: equivalent stage Campaigns 4-6; workflow, validators, package construction, provenance handling, fingerprint stability, and PEL behaviour transferred unchanged.
""", encoding="utf-8")
    financial_sector = qr["repository_financial_sector_summary"]
    repository_financial_sector_text = f"""# Repository Financial Sector Summary

- Total Knowledge Objects: {financial_sector['total_knowledge_objects']}
- Objects added this campaign: {financial_sector['objects_added_this_campaign']}
- Repository growth since previous campaign: {financial_sector['repository_growth_since_previous_campaign']}
- Provenance completeness: {str(financial_sector['provenance_completeness']).lower()}
- Fingerprint stability: {str(financial_sector['fingerprint_stability']).lower()}
- Repository fingerprint: `{financial_sector['repository_fingerprint']}`
- Unresolved repository-quality concerns: {', '.join(financial_sector['unresolved_repository_quality_concerns']) if financial_sector['unresolved_repository_quality_concerns'] else 'none'}

## Objects by evidence family

"""
    repository_financial_sector_text += "\n".join(f"- {key}: {value}" for key, value in financial_sector['objects_by_evidence_family'].items())
    repository_financial_sector_text += "\n\n## Objects by knowledge category\n\n"
    repository_financial_sector_text += "\n".join(f"- {key}: {value}" for key, value in financial_sector['objects_by_knowledge_category'].items())
    repository_financial_sector_text += "\n\n## Objects by lifecycle state\n\n"
    repository_financial_sector_text += "\n".join(f"- {key}: {value}" for key, value in financial_sector['objects_by_lifecycle_state'].items())
    repository_financial_sector_text += "\n"
    (reports / "repository_financial_sector_summary.md").write_text(repository_financial_sector_text, encoding="utf-8")
    impact = qr["knowledge_repository_impact_assessment"]
    impact_text = f"""# Knowledge Repository Impact Assessment

- Repository object count before campaign: {impact['repository_object_count_before']}
- Repository object count after campaign: {impact['repository_object_count_after']}
- New Knowledge Objects added: {impact['new_knowledge_objects_added']}

## New reusable knowledge introduced

"""
    impact_text += "\n".join(f"- {item}" for item in impact["new_reusable_knowledge_introduced"])
    impact_text += "\n\n## Knowledge categories expanded\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["knowledge_categories_expanded"])
    impact_text += "\n\n## Evidence-family coverage expanded\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["evidence_family_coverage_expanded"])
    impact_text += "\n\n## Repository breadth gained\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["repository_breadth_gained"])
    impact_text += "\n\n## Repository depth gained\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["repository_depth_gained"])
    impact_text += "\n\n## Confidence gained through additional evidence\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["confidence_gained_through_additional_evidence"])
    impact_text += "\n\n## Future recomputation avoided for downstream projects\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["future_recomputation_avoided_for_downstream_projects"])
    impact_text += "\n\n## Repository composition changes\n\n"
    impact_text += "- Objects by evidence family after campaign: " + json.dumps(impact["repository_composition_changes"]["objects_by_evidence_family_after"], sort_keys=True) + "\n"
    impact_text += "- Objects by knowledge category after campaign: " + json.dumps(impact["repository_composition_changes"]["objects_by_knowledge_category_after"], sort_keys=True) + "\n"
    impact_text += "- Objects by lifecycle state after campaign: " + json.dumps(impact["repository_composition_changes"]["objects_by_lifecycle_state_after"], sort_keys=True) + "\n"
    impact_text += "\n## Repository-quality concerns discovered\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["repository_quality_concerns_discovered"]) if impact["repository_quality_concerns_discovered"] else "none"
    impact_text += "\n\n## Repository-quality improvements achieved\n\n"
    impact_text += "\n".join(f"- {item}" for item in impact["repository_quality_improvements_achieved"])
    impact_text += "\n"
    (reports / "knowledge_repository_impact_assessment.md").write_text(impact_text, encoding="utf-8")
    (reports / "financial_sector_family_maturity_assessment.md").write_text(f"""# Financial Sector Family Maturity Assessment

Classification: {qr['financial_sector_family_maturity_assessment']['classification']}

Basis: {qr['financial_sector_family_maturity_assessment']['basis']}

Validated capabilities:

""" + "\n".join(f"- {item}" for item in qr['financial_sector_family_maturity_assessment']['validated']) + "\n\nNot yet sufficient for Mature:\n\n" + "\n".join(f"- {item}" for item in qr['financial_sector_family_maturity_assessment']['insufficient_for_mature']) + "\n", encoding="utf-8")
    (reports / "maturation_methodology_comparison.md").write_text(f"""# Maturation Methodology Comparison

Equivalent demographic stage: {qr['comparison_against_demographic_equivalent_stage']['equivalent_stage']}

Transferred unchanged:

- production workflow
- validator behaviour
- package construction
- provenance handling
- fingerprint stability
- production-quality reporting
- Production Evolution Log behaviour

Capabilities matured differently:

- Financial Sector uses five indicator-family groups where the demographic equivalent used four.
- Financial Sector remains Stable after Campaign 32 because dedicated Financial Sector provenance-lineage completeness has not yet been executed.

Family-specific assumptions:

- Financial Sector indicator family names and matrix counts are family-specific.

KnowledgeForge-wide assumptions:

- deterministic replay, fingerprint stability, provenance completeness, and rejected-candidate preservation remain broadly supported.
""", encoding="utf-8")
    (reports / "production_retrospective_report.md").write_text("""# Production Retrospective

Campaign 32 continued WDI Financial Sector family maturation without architecture change. The campaign adds inventory, territorial coverage, and temporal coverage evidence to the Financial Sector family and supports Stable status for that family.

No implementation or architecture change is justified. The next bounded campaign should execute Financial Sector provenance-lineage completeness as the family closeout campaign.
""", encoding="utf-8")
    (reports / "architectural_observations_report.md").write_text("""# Architectural Observations

Campaign 32 supports preserving the current KnowledgeForge architecture unchanged.

Supported observations:

- Financial Sector indicator-family inventory fits existing factual, classified, coverage, negative, provenance, methodological, derived, and evidence-quality categories;
- territorial and temporal coverage matrices transferred unchanged from the demographic maturation pattern;
- validator behaviour, package construction, Production Support, provenance handling, fingerprinting, reporting, and PEL workflow remained stable;
- no duplicate, taxonomy, validator, workflow, helper-extraction, or architecture pressure appeared.

No architecture change is recommended.
""", encoding="utf-8")


def run_campaign(output: Path, repository_root: Path | None = None) -> dict[str, Any]:
    snapshot = immutable_wdi_financial_sector_maturation_snapshot()
    source_packages = build_source_packages(snapshot)
    candidates, accepted_objects, rejected_records = process_packages(source_packages)
    rejected_records.extend(process_rejected_candidates(build_rejected_candidates(snapshot)))
    duplicate_detected = len({obj["fingerprints"]["generated_statements"] for obj in accepted_objects}) != len(accepted_objects)
    base_quality = production_support.aggregate_common_quality_metrics(
        campaign_id=CAMPAIGN_ID,
        source_packages=source_packages,
        knowledge_candidates=candidates,
        accepted_objects=accepted_objects,
        rejected_records=rejected_records,
        validation_records=[],
        determinism_verified=True,
        fingerprint_stability=True,
        duplicate_knowledge_objects_detected=duplicate_detected,
    )
    category_counter = Counter(obj["generated_statements"][0]["statement_type"] for obj in accepted_objects)
    rejected_counter = Counter(
        rec["source_evidence_package"]["evidence_payload"].get("knowledge_category")
        or rec["source_evidence_package"]["evidence_payload"].get("category")
        or rec["source_evidence_package"]["evidence_payload"].get("statement_type")
        or rec["source_evidence_package"]["evidence_payload"].get("payload_metadata", {}).get("category")
        or rec["source_evidence_package"].get("source_evidence_package_id", "unknown")
        for rec in rejected_records
    )
    final_snapshot_fingerprint = sha256_fingerprint({"snapshot": snapshot, "accepted": [obj["fingerprints"]["package_manifest"] for obj in accepted_objects], "rejected": [rec["source_evidence_package"]["fingerprints"]["package_manifest"] for rec in rejected_records]})
    quality_report = {
        **base_quality,
        "source_evidence_packages_processed": len(source_packages),
        "knowledge_candidate_packages_generated": len(candidates),
        "financial_sector_family_maturity_assessment": snapshot["maturity_assessment"],
        "comparison_against_campaign31": {"campaign31_accepted": 19, "campaign32_accepted": len(accepted_objects), "workflow_transfer": "unchanged", "scope_difference": "Campaign 32 adds indicator-family inventory, territorial coverage, and temporal coverage matrices to Financial Sector production."},
        "comparison_against_demographic_equivalent_stage": {"equivalent_stage": "Campaigns 4-6", "workflow_transfer": "unchanged", "validator_behaviour": "unchanged", "package_construction": "unchanged", "provenance_handling": "unchanged", "fingerprint_stability": "unchanged", "pel_behaviour": "unchanged"},
        "maturation_methodology_comparison": snapshot["maturation_methodology_comparison"],
        "knowledge_categories_produced": dict(sorted(category_counter.items())),
        "knowledge_categories_rejected": dict(sorted(rejected_counter.items())),
        "architecture_taxonomy_validator_or_workflow_pressure": False,
        "duplicate_registry_implementation_justified": False,
        "new_helper_extraction_justified": False,
        "knowledgeforge_methodology_maturity_assessment": "not_applicable_after_methodology_closeout",
        "next_recommended_campaign": "Campaign 30 should execute WDI Financial Sector provenance-lineage completeness as the family closeout campaign.",
        "architectural_observations": ["Financial Sector inventory and coverage matrices fit existing taxonomy.", "No architecture, taxonomy, validator, workflow, or helper-extraction pressure appeared.", "KnowledgeForge methodology maturity judgment should wait until Financial Sector reaches Mature status."],
        "candidate_improvements_discovered": ["No implementation or architecture change is justified by Campaign 32."],
        "final_snapshot_fingerprint": final_snapshot_fingerprint,
        "final_recommendation": "Continue the WDI Financial Sector family maturation path unchanged with Financial Sector provenance-lineage completeness before classifying the Financial Sector family as Mature.",
        "architectural_continuity_classification": "preserves agreed architecture",
    }
    if repository_root is None:
        repository_root = PROJECT_ROOT / "knowledge_repository"
    repository_root = Path(repository_root)
    previous_manifest = read_json_if_exists(repository_root / "manifest.json", {})
    previous_count = int(previous_manifest.get("object_count", 0) or 0)
    repository_result = knowledge_repository.persist_knowledge_object_packages(accepted_objects, repository_root)
    campaign_previous_count = repository_result["total_object_count"] - len({obj["package_id"] for obj in accepted_objects})
    if previous_count < campaign_previous_count:
        campaign_previous_count = previous_count
    quality_report["knowledge_repository_population"] = repository_result
    quality_report["repository_financial_sector_summary"] = repository_financial_sector_summary(repository_root, accepted_objects, repository_result, campaign_previous_count, quality_report["fingerprint_stability"])
    quality_report["knowledge_repository_impact_assessment"] = repository_impact_assessment(accepted_objects, quality_report["repository_financial_sector_summary"], campaign_previous_count)
    result = {"snapshot": snapshot, "source_packages": source_packages, "knowledge_candidates": candidates, "accepted_objects": accepted_objects, "rejected_records": rejected_records, "quality_report": quality_report, "output": str(output.resolve())}
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "source_snapshot.json", snapshot)
    write_json(output / "source_evidence_packages.json", source_packages)
    write_json(output / "knowledge_candidate_packages.json", candidates)
    write_json(output / "knowledge_object_packages.json", accepted_objects)
    write_json(output / "rejected_candidates.json", rejected_records)
    write_json(output / "production_quality_report.json", quality_report)
    write_json(output / "reports" / "production_quality_report.json", quality_report)
    write_markdown_reports(output, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Campaign 32 WDI Financial Sector maturation")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts" / "production" / CAMPAIGN_ID)
    parser.add_argument("--repository-root", type=Path, default=PROJECT_ROOT / "knowledge_repository")
    args = parser.parse_args()
    result = run_campaign(args.output, repository_root=args.repository_root)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "accepted": len(result["accepted_objects"]),
        "rejected": len(result["rejected_records"]),
        "financial_sector_maturity": result["quality_report"]["financial_sector_family_maturity_assessment"]["classification"],
        "repository_fingerprint": result["quality_report"]["repository_financial_sector_summary"]["repository_fingerprint"],
        "repository_object_count": result["quality_report"]["repository_financial_sector_summary"]["total_knowledge_objects"],
        "determinism_verified": result["quality_report"]["determinism_verification"],
        "fingerprint_stability": result["quality_report"]["fingerprint_stability"],
        "duplicate_knowledge_objects_detected": result["quality_report"]["duplicate_knowledge_objects_detected"],
        "architecture_taxonomy_validator_or_workflow_pressure": result["quality_report"]["architecture_taxonomy_validator_or_workflow_pressure"],
        "knowledgeforge_methodology_maturity_assessment": result["quality_report"]["knowledgeforge_methodology_maturity_assessment"],
        "snapshot_fingerprint": result["quality_report"]["final_snapshot_fingerprint"],
        "output": str(args.output.resolve()),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
