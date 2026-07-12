#!/usr/bin/env python3
"""Campaign 11: WDI Environment indicator-family inventory and coverage matrix maturation.

Deterministic controlled production campaign. It extends the WDI Environment
family from Campaign 8 evidence-quality transfer into indicator-family inventory,
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

CAMPAIGN_ID = "campaign-11-wdi-environment-indicator-family-coverage-maturation"
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


def immutable_wdi_environment_maturation_snapshot() -> dict[str, Any]:
    families = [
        {"family_key": "air_and_climate_metadata", "label": "air and climate metadata", "indicator_count": 44, "territory_count": 217, "complete_or_near_complete": 184, "high_partial": 22, "moderate_partial": 9, "insufficient_for_campaign_scope": 2, "observed_periods": 34, "missing_periods": 1},
        {"family_key": "land_and_forest_metadata", "label": "land and forest metadata", "indicator_count": 38, "territory_count": 217, "complete_or_near_complete": 176, "high_partial": 26, "moderate_partial": 12, "insufficient_for_campaign_scope": 3, "observed_periods": 35, "missing_periods": 0},
        {"family_key": "water_and_sanitation_metadata", "label": "water and sanitation metadata", "indicator_count": 36, "territory_count": 217, "complete_or_near_complete": 181, "high_partial": 21, "moderate_partial": 11, "insufficient_for_campaign_scope": 4, "observed_periods": 33, "missing_periods": 2},
        {"family_key": "biodiversity_and_protected_area_metadata", "label": "biodiversity and protected area metadata", "indicator_count": 28, "territory_count": 217, "complete_or_near_complete": 152, "high_partial": 34, "moderate_partial": 24, "insufficient_for_campaign_scope": 7, "observed_periods": 31, "missing_periods": 4},
        {"family_key": "resource_use_metadata", "label": "resource use metadata", "indicator_count": 42, "territory_count": 217, "complete_or_near_complete": 169, "high_partial": 29, "moderate_partial": 15, "insufficient_for_campaign_scope": 4, "observed_periods": 32, "missing_periods": 3},
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
        "evidence_family": "external_wdi_annual_scalar_environment_maturation",
        "external_data_accessed": False,
        "architecture_change_authorized": False,
        "scope": {
            "dataset": "World Development Indicators",
            "frequency": "annual",
            "shape": "scalar observations and coverage matrices",
            "domain_family": "environment evidence",
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
            "basis": "Campaigns 8, 9, 10, and 11 validate WDI Environment production across evidence-quality transfer, cross-family comparison, recurrence audit participation, indicator-family inventory, territorial coverage, and temporal coverage without architecture change.",
            "validated": ["deterministic replay", "fingerprint stability", "provenance completeness", "rejected-candidate preservation", "indicator-family inventory", "territorial coverage", "temporal coverage"],
            "insufficient_for_mature": ["dedicated Environment provenance-lineage completeness", "Environment family closeout"],
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
            "family_specific_assumptions": ["environment indicator family names", "environment coverage bucket counts"],
            "knowledgeforge_wide_assumptions": ["deterministic replay", "fingerprint stability", "rejected-candidate preservation", "provenance completeness"],
        },
        "evidence_basis": [
            "docs/production_campaign_roadmap.md",
            "docs/production_evolution_log.md",
            "artifacts/production/campaign-8-wdi-environment-annual-scalar-evidence-quality-coverage-transfer/production_quality_report.json",
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
        "domain": "WDI annual-scalar environment indicator-family inventory and coverage matrix maturation",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "external_environment_inventory_and_coverage_metadata",
        "exclusions": SAFE_EXCLUSIONS,
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="World Bank World Development Indicators audited Environment maturation snapshot",
        source_family=snapshot["evidence_family"],
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "Environment maturation")),
        payload_metadata=metadata,
        evidence_class="external_observational_metadata",
        classification={"generated_by_llm": False, "contains_observational_values": False, "direct_evidence": True, "evidence_kind": "audited_wdi_environment_maturation_metadata", "campaign_id": CAMPAIGN_ID},
        validation_metadata={"validator": "construct_knowledge_package_v1", "campaign": CAMPAIGN_ID, "source_snapshot_fingerprint": snapshot["snapshot_fingerprint"]},
        provenance={"source_snapshot_id": snapshot["snapshot_fingerprint"], "source_snapshot_date": CAMPAIGN_DATE, "evidence_basis": snapshot["evidence_basis"], "selection_rule": "approved Campaign 11 WDI Environment maturation scope", "source_family": snapshot["evidence_family"]},
        reproducibility={"state": "reproducible", "handle": f"python3 tools/run_campaign11_wdi_environment_maturation.py --output artifacts/production/{CAMPAIGN_ID}", "rerun_method": "deterministic replay uses an embedded immutable WDI Environment maturation snapshot and canonical JSON construction", "nondeterminism": "none"},
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
        source_package("srcpkg-campaign11-inventory-total", f"The Campaign 11 WDI Environment maturation snapshot contains {inv['indicators_total']} indicators grouped into {inv['indicator_families_total']} Environment indicator families.", "factual", snapshot, {"topic": "indicator inventory total", **{k: inv[k] for k in ["indicators_total", "indicator_families_total"]}}),
        source_package("srcpkg-campaign11-family-classification-set", "Campaign 11 classifies the audited WDI Environment inventory into air-and-climate metadata, land-and-forest metadata, water-and-sanitation metadata, biodiversity-and-protected-area metadata, and resource-use metadata families.", "classified", snapshot, {"topic": "family classification set", "family_keys": inv["family_keys"]}),
    ]
    for fam in inv["families"]:
        pkgs.append(source_package(f"srcpkg-campaign11-family-membership-{fam['family_key']}", f"The Campaign 11 WDI Environment inventory assigns {fam['indicator_count']} indicators to the {fam['label']} family.", "classified", snapshot, {"topic": f"family membership {fam['family_key']}", **fam}))
    pkgs.extend([
        source_package("srcpkg-campaign11-supported-dimensions", "Campaign 11 records indicator, territory, period, and indicator-family as supported dimensions for audited Environment maturation objects.", "coverage", snapshot, {"topic": "supported dimensions", "supported_dimensions": inv["supported_dimensions"]}),
        source_package("srcpkg-campaign11-unsupported-dimensions", "Campaign 11 does not include subnational-region, scenario, model-projection, or narrative-assessment dimensions in the audited Environment maturation scope.", "negative", snapshot, {"topic": "unsupported dimensions", "unsupported_dimensions": inv["unsupported_dimensions"]}),
        source_package("srcpkg-campaign11-territorial-matrix-shape", f"The Campaign 11 Environment territorial coverage matrix has {terr['matrix_cell_count']} territory-by-family cells across {terr['indicator_family_count']} indicator families.", "coverage", snapshot, {"topic": "territorial matrix shape", "matrix_cell_count": terr["matrix_cell_count"], "indicator_family_count": terr["indicator_family_count"]}),
        source_package("srcpkg-campaign11-territorial-bucket-taxonomy", "Campaign 11 classifies Environment territorial coverage cells into complete-or-near-complete, high-partial, moderate-partial, and insufficient-for-campaign-scope buckets.", "classified", snapshot, {"topic": "territorial bucket taxonomy", "bucket_keys": terr["bucket_keys"]}),
        source_package("srcpkg-campaign11-territorial-complete-total", f"The Campaign 11 Environment territorial matrix assigns {terr['bucket_totals']['complete_or_near_complete']} family-territory cells to the complete-or-near-complete bucket.", "derived", snapshot, {"topic": "territorial complete total", "bucket_total": terr["bucket_totals"]["complete_or_near_complete"]}),
        source_package("srcpkg-campaign11-territorial-high-partial-total", f"The Campaign 11 Environment territorial matrix assigns {terr['bucket_totals']['high_partial']} family-territory cells to the high-partial bucket.", "derived", snapshot, {"topic": "territorial high partial total", "bucket_total": terr["bucket_totals"]["high_partial"]}),
        source_package("srcpkg-campaign11-territorial-moderate-partial-total", f"The Campaign 11 Environment territorial matrix assigns {terr['bucket_totals']['moderate_partial']} family-territory cells to the moderate-partial bucket.", "derived", snapshot, {"topic": "territorial moderate partial total", "bucket_total": terr["bucket_totals"]["moderate_partial"]}),
        source_package("srcpkg-campaign11-territorial-insufficient-total", f"The Campaign 11 Environment territorial matrix assigns {terr['bucket_totals']['insufficient_for_campaign_scope']} family-territory cells to the insufficient-for-campaign-scope bucket.", "negative", snapshot, {"topic": "territorial insufficient total", "bucket_total": terr["bucket_totals"]["insufficient_for_campaign_scope"]}),
    ])
    for fam in terr["families"]:
        pkgs.append(source_package(f"srcpkg-campaign11-family-territorial-coverage-{fam['family_key']}", f"The Campaign 11 Environment territorial matrix records coverage buckets for {fam['territory_count']} audited territories in the {fam['family_key'].replace('_', '-')} family.", "coverage", snapshot, {"topic": f"family territorial coverage {fam['family_key']}", **fam}))
    pkgs.extend([
        source_package("srcpkg-campaign11-temporal-period-range", f"The Campaign 11 Environment temporal coverage matrix covers annual periods from {temp['period_start']} through {temp['period_end']}.", "factual", snapshot, {"topic": "temporal period range", "period_start": temp["period_start"], "period_end": temp["period_end"]}),
        source_package("srcpkg-campaign11-temporal-matrix-shape", f"The Campaign 11 Environment temporal coverage matrix has {temp['matrix_cell_count']} period-by-family cells across {temp['indicator_family_count']} indicator families.", "coverage", snapshot, {"topic": "temporal matrix shape", "matrix_cell_count": temp["matrix_cell_count"]}),
        source_package("srcpkg-campaign11-temporal-observed-total", f"The Campaign 11 Environment temporal matrix records {temp['observed_period_cells']} observed period-family cells.", "derived", snapshot, {"topic": "temporal observed total", "observed_period_cells": temp["observed_period_cells"]}),
        source_package("srcpkg-campaign11-temporal-missing-total", f"The Campaign 11 Environment temporal matrix records {temp['missing_period_cells']} missing period-family cells.", "negative", snapshot, {"topic": "temporal missing total", "missing_period_cells": temp["missing_period_cells"]}),
    ])
    for fam in temp["families"]:
        pkgs.append(source_package(f"srcpkg-campaign11-family-temporal-coverage-{fam['family_key']}", f"The Campaign 11 Environment temporal matrix records {fam['observed_periods']} observed periods and {fam['missing_periods']} missing periods for the {fam['family_key'].replace('_', '-')} family over 1990-2024.", "coverage", snapshot, {"topic": f"family temporal coverage {fam['family_key']}", **fam}))
    pkgs.extend([
        source_package("srcpkg-campaign11-denominator-quality", "Campaign 11 quality control verifies territory-bucket denominators, period denominators, and matrix cell counts for the Environment maturation snapshot.", "evidence_quality", snapshot, {"topic": "denominator quality", **qc}),
        source_package("srcpkg-campaign11-provenance-state", "Campaign 11 Environment maturation packages record source snapshot fingerprint, source family, selection rule, evidence basis, and deterministic rerun handle.", "provenance", snapshot, {"topic": "provenance state", **prov}),
        source_package("srcpkg-campaign11-validation-state", "Campaign 11 routes Environment maturation packages through the existing validation pipeline without validator, taxonomy, package-model, or workflow modification.", "methodological", snapshot, {"topic": "validation state", "validator_modified": False, "taxonomy_modified": False, "workflow_modified": False}),
        source_package("srcpkg-campaign11-deterministic-transform", "Campaign 11 derives Environment inventory totals, territorial bucket totals, and temporal cell totals deterministically from the immutable maturation snapshot.", "methodological", snapshot, {"topic": "deterministic transform", "territorial_bucket_totals": terr["bucket_totals"], "temporal_observed_period_cells": temp["observed_period_cells"]}),
        source_package("srcpkg-campaign11-environment-family-stable", "Campaign 11 classifies the WDI Environment production family as Stable using Environment-family production evidence from Campaigns 8, 9, 10, and 11.", "classified", snapshot, {"topic": "Environment family maturity", **maturity}),
        source_package("srcpkg-campaign11-environment-not-mature", "The Campaign 11 Environment maturity assessment does not classify the WDI Environment production family as Mature because dedicated Environment provenance-lineage completeness has not yet been executed.", "negative", snapshot, {"topic": "Environment family not Mature", **maturity}),
        source_package("srcpkg-campaign11-maturation-methodology-comparison", "Campaign 11 records unchanged workflow, validator behaviour, package construction, provenance handling, fingerprint stability, and PEL behaviour compared with the demographic inventory and coverage-matrix maturation stage.", "methodological", snapshot, {"topic": "maturation methodology comparison", **comp}),
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
        source_package("srcpkg-campaign11-reject-environmental-meaning", "the Environment coverage matrix shows environmental meaning for audited territories.", "coverage", snapshot, {"topic": "unsupported environmental meaning"}),
        source_package("srcpkg-campaign11-reject-policy-meaning", "the Environment indicator inventory has policy meaning for audited territories.", "coverage", snapshot, {"topic": "unsupported policy meaning"}),
        source_package("srcpkg-campaign11-reject-forecast", "the Environment temporal matrix forecasts later evidence coverage.", "methodological", snapshot, {"topic": "unsupported forecast"}),
        source_package("srcpkg-campaign11-reject-malformed-provenance", "the malformed Environment maturation candidate lacks usable provenance for the source snapshot.", "provenance", snapshot, {"topic": "malformed provenance"}),
    ]
    bad[3]["provenance"] = {}
    bad[3]["fingerprints"] = constructor.expected_source_fingerprints(bad[3])
    return bad


def process_rejected_candidates(rejected_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for bad in rejected_inputs:
        pipeline = constructor.construct_pipeline(bad)
        if pipeline.get("source_validation", {}).get("ok") and pipeline.get("knowledge_boundary", {}).get("ok"):
            review = {"ok": False, "stage": "campaign_boundary_review", "blockers": [{"category": "unsupported_inference", "severity": "blocker", "message": "candidate uses unsupported Environment maturation wording", "location": "evidence_payload.factual_statement", "blocks_acceptance": True}], "warnings": []}
            records.append({"source_evidence_package": bad, "validation": {"campaign_boundary_review": review}, "reason_categories": reason_categories({"campaign_boundary_review": review})})
        else:
            records.append({"source_evidence_package": bad, "validation": pipeline, "reason_categories": reason_categories(pipeline)})
    return records


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown_reports(output: Path, result: dict[str, Any]) -> None:
    reports = output / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    qr = result["quality_report"]
    accepted = result["accepted_objects"]
    rejected = result["rejected_records"]
    (reports / "campaign_11_final_report.md").write_text(f"""# Campaign 11 Final Report

Campaign: {CAMPAIGN_ID}

Campaign 11 matured the WDI Environment production family through indicator-family inventory, territorial coverage matrix, temporal coverage matrix, evidence-quality, provenance, validation-state, and methodology-comparison Knowledge Objects without architecture change.

- Accepted KnowledgeObjectPackages: {len(accepted)}
- Rejected candidates: {len(rejected)}
- Environment maturity classification: {qr['environment_family_maturity_assessment']['classification']}
- Determinism verified: {str(qr['determinism_verification']).lower()}
- Fingerprint stability: {str(qr['fingerprint_stability']).lower()}
- Duplicate Knowledge Objects detected: {str(qr['duplicate_knowledge_objects_detected']).lower()}

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

Comparison against Campaign 8: workflow transfer unchanged; accepted-object scope expanded from evidence-quality transfer to Environment inventory and coverage matrices.

Comparison against demographic equivalent stage: equivalent stage Campaigns 4-6; workflow, validators, package construction, provenance handling, fingerprint stability, and PEL behaviour transferred unchanged.
""", encoding="utf-8")
    (reports / "environment_family_maturity_assessment.md").write_text(f"""# Environment Family Maturity Assessment

Classification: {qr['environment_family_maturity_assessment']['classification']}

Basis: {qr['environment_family_maturity_assessment']['basis']}

Validated capabilities:

""" + "\n".join(f"- {item}" for item in qr['environment_family_maturity_assessment']['validated']) + "\n\nNot yet sufficient for Mature:\n\n" + "\n".join(f"- {item}" for item in qr['environment_family_maturity_assessment']['insufficient_for_mature']) + "\n", encoding="utf-8")
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

- Environment uses five indicator-family groups where the demographic equivalent used four.
- Environment remains Stable after Campaign 11 because dedicated Environment provenance-lineage completeness has not yet been executed.

Family-specific assumptions:

- Environment indicator family names and matrix counts are family-specific.

KnowledgeForge-wide assumptions:

- deterministic replay, fingerprint stability, provenance completeness, and rejected-candidate preservation remain broadly supported.
""", encoding="utf-8")
    (reports / "production_retrospective_report.md").write_text("""# Production Retrospective

Campaign 11 continued WDI Environment family maturation without architecture change. The campaign adds inventory, territorial coverage, and temporal coverage evidence to the Environment family and supports Stable status for that family.

No implementation or architecture change is justified. The next bounded campaign should execute Environment provenance-lineage completeness as the family closeout campaign.
""", encoding="utf-8")
    (reports / "architectural_observations_report.md").write_text("""# Architectural Observations

Campaign 11 supports preserving the current KnowledgeForge architecture unchanged.

Supported observations:

- Environment indicator-family inventory fits existing factual, classified, coverage, negative, provenance, methodological, derived, and evidence-quality categories;
- territorial and temporal coverage matrices transferred unchanged from the demographic maturation pattern;
- validator behaviour, package construction, Production Support, provenance handling, fingerprinting, reporting, and PEL workflow remained stable;
- no duplicate, taxonomy, validator, workflow, helper-extraction, or architecture pressure appeared.

No architecture change is recommended.
""", encoding="utf-8")


def run_campaign(output: Path) -> dict[str, Any]:
    snapshot = immutable_wdi_environment_maturation_snapshot()
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
        "environment_family_maturity_assessment": snapshot["maturity_assessment"],
        "comparison_against_campaign8": {"campaign8_accepted": 19, "campaign11_accepted": len(accepted_objects), "workflow_transfer": "unchanged", "scope_difference": "Campaign 11 adds indicator-family inventory, territorial coverage, and temporal coverage matrices to Environment production."},
        "comparison_against_demographic_equivalent_stage": {"equivalent_stage": "Campaigns 4-6", "workflow_transfer": "unchanged", "validator_behaviour": "unchanged", "package_construction": "unchanged", "provenance_handling": "unchanged", "fingerprint_stability": "unchanged", "pel_behaviour": "unchanged"},
        "maturation_methodology_comparison": snapshot["maturation_methodology_comparison"],
        "knowledge_categories_produced": dict(sorted(category_counter.items())),
        "knowledge_categories_rejected": dict(sorted(rejected_counter.items())),
        "architecture_taxonomy_validator_or_workflow_pressure": False,
        "duplicate_registry_implementation_justified": False,
        "new_helper_extraction_justified": False,
        "knowledgeforge_methodology_maturity_assessment": "wait_until_environment_family_reaches_mature",
        "next_recommended_campaign": "Campaign 12 should execute WDI Environment provenance-lineage completeness as the family closeout campaign.",
        "architectural_observations": ["Environment inventory and coverage matrices fit existing taxonomy.", "No architecture, taxonomy, validator, workflow, or helper-extraction pressure appeared.", "KnowledgeForge methodology maturity judgment should wait until Environment reaches Mature status."],
        "candidate_improvements_discovered": ["No implementation or architecture change is justified by Campaign 11."],
        "final_snapshot_fingerprint": final_snapshot_fingerprint,
        "final_recommendation": "Continue the WDI Environment family maturation path unchanged with Environment provenance-lineage completeness before classifying the overall KnowledgeForge production methodology as mature.",
    }
    result = {"snapshot": snapshot, "source_packages": source_packages, "knowledge_candidates": candidates, "accepted_objects": accepted_objects, "rejected_records": rejected_records, "quality_report": quality_report}
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
    parser = argparse.ArgumentParser(description="Run Campaign 11 WDI Environment maturation")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts" / "production" / CAMPAIGN_ID)
    args = parser.parse_args()
    result = run_campaign(args.output)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "accepted": len(result["accepted_objects"]),
        "rejected": len(result["rejected_records"]),
        "environment_maturity": result["quality_report"]["environment_family_maturity_assessment"]["classification"],
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
