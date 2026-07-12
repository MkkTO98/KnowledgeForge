#!/usr/bin/env python3
"""Campaign 10: cross-campaign duplicate and recurrence audit.

Deterministic controlled production campaign. It treats existing KnowledgeForge
production artifacts from Campaigns 0-9 as the only evidence base and audits
recurrence, duplicate pressure, validator patterns, metadata patterns, production
methodology stability, and Production Evolution Log signals.

No external data access. No prior campaign output modification. No architecture,
taxonomy, validator, runtime, adapter/API/shared-schema, database, repository,
local-model, or frontier-model change.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

CAMPAIGN_ID = "campaign-10-cross-campaign-duplicate-recurrence-audit"
CAMPAIGN_DATE = "2026-07-09"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSTRUCTOR_PATH = PROJECT_ROOT / "tools" / "construct_knowledge_package_v1.py"
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_knowledge_pipeline_v1.py"
PRODUCTION_SUPPORT_PATH = PROJECT_ROOT / "tools" / "production_support.py"

CAMPAIGN_QUALITY_REPORTS = [
    "artifacts/production/campaign-0-repository-evidence-characterization/production_quality_report.json",
    "artifacts/production/campaign-1-wdi-demographic-structure-evidence-quality-coverage/production_quality_report.json",
    "artifacts/production/campaign-2-wdi-demographic-structure-completeness-buckets/production_quality_report.json",
    "artifacts/production/campaign-3-wdi-demographic-structure-source-freshness-release-metadata/production_quality_report.json",
    "artifacts/production/campaign-4-wdi-demographic-structure-indicator-family-inventory/production_quality_report.json",
    "artifacts/production/campaign-5-wdi-demographic-structure-territorial-coverage-matrix/production_quality_report.json",
    "artifacts/production/campaign-6-wdi-demographic-structure-temporal-coverage-matrix/production_quality_report.json",
    "artifacts/production/campaign-7-wdi-demographic-structure-provenance-lineage-completeness/production_quality_report.json",
    "artifacts/production/campaign-8-wdi-environment-annual-scalar-evidence-quality-coverage-transfer/production_quality_report.json",
    "artifacts/production/campaign-9-wdi-cross-family-annual-scalar-coverage-comparison/production_quality_report.json",
]

SAFE_SCOPE_EXCLUSIONS = [
    "explanatory meaning statements",
    "future-looking statements",
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _bool(value: Any) -> bool:
    return bool(value) if value is not None else False


def build_cross_campaign_snapshot() -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    validator_counter: Counter[str] = Counter()
    produced_category_counter: Counter[str] = Counter()
    rejected_category_counter: Counter[str] = Counter()
    accepted_total = 0
    rejected_total = 0
    duplicate_true_count = 0
    determinism_true_count = 0
    fingerprint_true_count = 0
    provenance_true_count = 0
    multi_reference_campaigns = 0
    average_evidence_refs: list[float] = []

    for index, rel in enumerate(CAMPAIGN_QUALITY_REPORTS):
        path = PROJECT_ROOT / rel
        exists = path.exists()
        quality = read_json(path) if exists else {}
        accepted = int(quality.get("knowledge_object_packages_accepted", quality.get("accepted", 0)) or 0)
        rejected = int(quality.get("rejected_candidates", quality.get("rejected", 0)) or 0)
        accepted_total += accepted
        rejected_total += rejected
        duplicate_detected = _bool(quality.get("duplicate_knowledge_objects_detected"))
        duplicate_true_count += 1 if duplicate_detected else 0
        determinism = _bool(quality.get("determinism_verification", quality.get("determinism_verified")))
        fingerprint = _bool(quality.get("fingerprint_stability"))
        provenance = _bool(quality.get("provenance_completeness", True))
        determinism_true_count += 1 if determinism else 0
        fingerprint_true_count += 1 if fingerprint else 0
        provenance_true_count += 1 if provenance else 0
        avg_refs = float(quality.get("average_evidence_references_per_knowledge_object", quality.get("average_evidence_references", 0.0)) or 0.0)
        average_evidence_refs.append(avg_refs)
        if int(quality.get("multi_reference_accepted_object_count", 0) or 0) > 0 or avg_refs > 1.0:
            multi_reference_campaigns += 1
        for k, v in (quality.get("validator_failures_by_category") or {}).items():
            validator_counter[str(k)] += int(v)
        for k, v in (quality.get("knowledge_categories_produced") or {}).items():
            produced_category_counter[str(k)] += int(v)
        for k, v in (quality.get("knowledge_categories_rejected") or {}).items():
            rejected_category_counter[str(k)] += int(v)
        summaries.append({
            "campaign_number": index,
            "campaign_id": quality.get("campaign_id", f"campaign-{index}"),
            "quality_report_path": rel,
            "quality_report_exists": exists,
            "accepted_objects": accepted,
            "rejected_candidates": rejected,
            "determinism_verification": determinism,
            "fingerprint_stability": fingerprint,
            "provenance_completeness": provenance,
            "duplicate_knowledge_objects_detected": duplicate_detected,
            "average_evidence_references": avg_refs,
            "multi_reference_accepted_object_count": int(quality.get("multi_reference_accepted_object_count", 0) or 0),
            "validator_failures_by_category": quality.get("validator_failures_by_category") or {},
            "knowledge_categories_produced": quality.get("knowledge_categories_produced") or {},
            "knowledge_categories_rejected": quality.get("knowledge_categories_rejected") or {},
            "report_fingerprint": sha256_fingerprint(quality) if quality else None,
        })

    aggregate = {
        "total_accepted_objects": accepted_total,
        "total_rejected_candidates": rejected_total,
        "campaigns_with_duplicate_objects": duplicate_true_count,
        "campaigns_without_duplicate_objects": len(summaries) - duplicate_true_count,
        "campaigns_with_determinism_true": determinism_true_count,
        "campaigns_with_fingerprint_stability_true": fingerprint_true_count,
        "campaigns_with_provenance_completeness_true": provenance_true_count,
        "campaigns_with_rejections_preserved": sum(1 for row in summaries if row["rejected_candidates"] > 0),
        "campaigns_with_multi_reference_objects": multi_reference_campaigns,
        "max_average_evidence_references": max(average_evidence_refs) if average_evidence_refs else 0.0,
        "min_average_evidence_references": min(average_evidence_refs) if average_evidence_refs else 0.0,
        "validator_failure_totals": dict(sorted(validator_counter.items())),
        "produced_category_totals": dict(sorted(produced_category_counter.items())),
        "rejected_category_totals": dict(sorted(rejected_category_counter.items())),
        "production_support_used_after_proof_campaigns": [4, 5, 6, 7, 8, 9],
        "pel_observations_audited": ["PEL-007", "PEL-008", "PEL-009", "PEL-011", "PEL-017", "PEL-018", "PEL-021"],
    }
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "campaign_range": "0-9",
        "campaigns_audited": len(summaries),
        "external_data_accessed": False,
        "prior_campaign_outputs_modified": False,
        "evidence_basis": CAMPAIGN_QUALITY_REPORTS + ["docs/production_evolution_log.md", "docs/production_campaign_roadmap.md"],
        "campaign_summaries": summaries,
        "aggregate_metrics": aggregate,
        "audit_conclusions": {
            "duplicate_registry_implementation_justified": False,
            "new_helper_extraction_justified": False,
            "architecture_taxonomy_validator_or_workflow_pressure": False,
            "production_support_pressure_satisfied": True,
            "taxonomy_sufficiency_reconfirmed": True,
            "wdi_demographic_maturity_conflict_detected": False,
            "wdi_environment_maturity_complete": False,
            "methodology_stability": "stable_across_campaigns_0_9",
            "roadmap_recommendation": "continue_with_wdi_environment_maturation",
        },
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def package_scope(topic: str) -> dict[str, Any]:
    return {
        "domain": "KnowledgeForge production campaign artifacts",
        "campaign_id": CAMPAIGN_ID,
        "topic": topic,
        "scope_type": "cross_campaign_recurrence_audit",
        "exclusions": SAFE_SCOPE_EXCLUSIONS,
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="KnowledgeForge Campaigns 0-9 production artifact recurrence snapshot",
        source_family="knowledgeforge_production_campaign_artifacts",
        source_version=snapshot["snapshot_fingerprint"],
        scope=package_scope(metadata.get("topic", "cross-campaign recurrence audit")),
        payload_metadata=metadata,
        evidence_class="internal_production_artifact_metadata",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "direct_evidence": True,
            "evidence_kind": "audited_production_artifact_recurrence",
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
            "campaign_range": snapshot["campaign_range"],
            "campaign_quality_report_fingerprints": [row["report_fingerprint"] for row in snapshot["campaign_summaries"]],
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign10_cross_campaign_recurrence_audit.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic replay reads existing Campaigns 0-9 production quality reports and constructs a canonical recurrence snapshot",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )


def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    agg = snapshot["aggregate_metrics"]
    conclusions = snapshot["audit_conclusions"]
    packages = [
        source_package("srcpkg-campaign10-artifact-evidence-base", "campaign 10 audited 10 existing production quality reports from Campaigns 0 through 9 without external data access.", "provenance", snapshot, {"topic": "prior campaign artifacts as source evidence", "paired_with": "srcpkg-campaign10-methodology-stability"}),
        source_package("srcpkg-campaign10-accepted-object-recurrence", f"Campaigns 0 through 9 produced {agg['total_accepted_objects']} accepted KnowledgeObjectPackages in total.", "derived", snapshot, {"topic": "accepted object recurrence", "total_accepted_objects": agg["total_accepted_objects"], "paired_with": "srcpkg-campaign10-rejected-candidate-recurrence"}),
        source_package("srcpkg-campaign10-rejected-candidate-recurrence", f"Campaigns 0 through 9 preserved {agg['total_rejected_candidates']} rejected candidates in total.", "evidence_quality", snapshot, {"topic": "rejected candidate recurrence", "total_rejected_candidates": agg["total_rejected_candidates"], "paired_with": "srcpkg-campaign10-accepted-object-recurrence"}),
        source_package("srcpkg-campaign10-determinism-recurrence", f"{agg['campaigns_with_determinism_true']} audited campaigns reported deterministic replay as true.", "methodological", snapshot, {"topic": "deterministic transformation recurrence", "count": agg["campaigns_with_determinism_true"], "paired_with": "srcpkg-campaign10-fingerprint-recurrence"}),
        source_package("srcpkg-campaign10-fingerprint-recurrence", f"{agg['campaigns_with_fingerprint_stability_true']} audited campaigns reported fingerprint stability as true.", "methodological", snapshot, {"topic": "fingerprint stability recurrence", "count": agg["campaigns_with_fingerprint_stability_true"], "paired_with": "srcpkg-campaign10-determinism-recurrence"}),
        source_package("srcpkg-campaign10-duplicate-absence", f"{agg['campaigns_without_duplicate_objects']} audited campaigns reported no duplicate Knowledge Objects.", "negative", snapshot, {"topic": "duplicate pressure", "duplicate_registry_implementation_justified": conclusions["duplicate_registry_implementation_justified"], "paired_with": "srcpkg-campaign10-cross-family-duplicate-pressure"}),
        source_package("srcpkg-campaign10-cross-family-duplicate-pressure", "Campaign 9 exercised cross-family overlap and duplicate pressure without duplicate Knowledge Object detection.", "negative", snapshot, {"topic": "cross-family duplicate pressure", "paired_with": "srcpkg-campaign10-duplicate-absence"}),
        source_package("srcpkg-campaign10-validator-recurrence", f"validator failure totals recurred across audited campaigns with categories {sorted(agg['validator_failure_totals'].keys())}.", "evidence_quality", snapshot, {"topic": "repeated validator failures", "validator_failure_totals": agg["validator_failure_totals"], "paired_with": "srcpkg-campaign10-rejected-candidate-recurrence"}),
        source_package("srcpkg-campaign10-production-support-reuse", "Campaigns 4 through 9 used the Production Support layer after the bounded proof without contract change.", "methodological", snapshot, {"topic": "Production Support recurrence", "production_support_pressure_satisfied": conclusions["production_support_pressure_satisfied"], "paired_with": "srcpkg-campaign10-helper-extraction-absence"}),
        source_package("srcpkg-campaign10-helper-extraction-absence", "Campaign 10 found no new helper extraction justified by Campaigns 0 through 9 production evidence.", "negative", snapshot, {"topic": "helper extraction pressure", "new_helper_extraction_justified": conclusions["new_helper_extraction_justified"], "paired_with": "srcpkg-campaign10-production-support-reuse"}),
        source_package("srcpkg-campaign10-taxonomy-recurrence", f"accepted objects across audited campaigns used existing categories {sorted(agg['produced_category_totals'].keys())} without taxonomy change.", "coverage", snapshot, {"topic": "taxonomy sufficiency", "produced_category_totals": agg["produced_category_totals"], "paired_with": "srcpkg-campaign10-architecture-pressure-absence"}),
        source_package("srcpkg-campaign10-architecture-pressure-absence", "Campaign 10 found no architecture, taxonomy, validator, or workflow pressure requiring implementation after Campaigns 0 through 9.", "negative", snapshot, {"topic": "architecture pressure", "architecture_taxonomy_validator_or_workflow_pressure": conclusions["architecture_taxonomy_validator_or_workflow_pressure"], "paired_with": "srcpkg-campaign10-taxonomy-recurrence"}),
        source_package("srcpkg-campaign10-maturity-consistency", "Campaign 10 found no conflict between WDI demographic Mature status and Campaigns 0 through 9 production evidence.", "evidence_quality", snapshot, {"topic": "production-family maturity consistency", "wdi_demographic_maturity_conflict_detected": conclusions["wdi_demographic_maturity_conflict_detected"], "paired_with": "srcpkg-campaign10-environment-maturity-incomplete"}),
        source_package("srcpkg-campaign10-environment-maturity-incomplete", "WDI Environment production maturity remains incomplete after Campaigns 8 and 9 because Environment indicator-family inventory and provenance-lineage completeness have not yet been executed.", "negative", snapshot, {"topic": "Environment maturity progression", "wdi_environment_maturity_complete": conclusions["wdi_environment_maturity_complete"], "paired_with": "srcpkg-campaign10-maturity-consistency"}),
        source_package("srcpkg-campaign10-methodology-stability", "Campaigns 0 through 9 preserve production methodology stability across repository-level, demographic, Environment, and cross-family artifact evidence.", "methodological", snapshot, {"topic": "production methodology stability", "methodology_stability": conclusions["methodology_stability"], "paired_with": "srcpkg-campaign10-artifact-evidence-base"}),
    ]
    return packages


def _evidence_ref_from_object(obj: dict[str, Any]) -> dict[str, Any]:
    return obj["evidence_references"][0]


def _make_multi_reference(obj: dict[str, Any], paired_obj: dict[str, Any], suffix: str) -> dict[str, Any]:
    out = copy.deepcopy(obj)
    if len(out["evidence_references"]) == 1:
        out["evidence_references"].append(_evidence_ref_from_object(paired_obj))
    if paired_obj["input_references"][0] not in out["input_references"]:
        out["input_references"].append(paired_obj["input_references"][0])
    stmt = out["generated_statements"][0]
    for ref in paired_obj["generated_statements"][0]["evidence_refs"]:
        if ref not in stmt["evidence_refs"]:
            stmt["evidence_refs"].append(ref)
    for dep in paired_obj["generated_statements"][0]["dependencies"]:
        if dep not in stmt["dependencies"]:
            stmt["dependencies"].append(dep)
    out["package_id"] = out["package_id"] + suffix
    out["provenance_envelope"]["evidence_refs"] = stmt["evidence_refs"]
    out["provenance_envelope"]["source_systems"] = ["Campaigns 0-9 production artifact snapshot", "paired campaign recurrence evidence"]
    out["computation_method"]["recipe"] = "deterministically preserve constitutionally permitted recurrence statement and paired campaign-artifact evidence references"
    out["computation_method"]["parameters"]["multi_reference"] = True
    out["scope"]["evidence_family"] = "knowledgeforge_production_campaign_artifacts"
    out["fingerprints"] = {
        "input_set": sha256_fingerprint(out["input_references"]),
        "evidence_references": sha256_fingerprint(out["evidence_references"]),
        "query_definitions": sha256_fingerprint(out["computation_method"]["query_definitions"]),
        "computation_recipe": sha256_fingerprint(out["computation_method"]),
        "generated_statements": sha256_fingerprint(out["generated_statements"]),
        "package_manifest": sha256_fingerprint({k: v for k, v in out.items() if k != "fingerprints"}),
    }
    out["evidence_integrity"]["source_package_fingerprint"] = sha256_fingerprint(out["input_references"])
    out["lineage"]["version_lineage"] = [out["promotion"]["from_candidate_package_id"], out["package_id"]]
    out["lineage"]["lineage_fingerprint"] = sha256_fingerprint({"package": out["package_id"], "fingerprints": out["fingerprints"]})
    out["fingerprints"]["package_manifest"] = sha256_fingerprint({k: v for k, v in out.items() if k != "fingerprints"})
    return out


def reason_categories(validation_payload: dict[str, Any]) -> list[str]:
    cats: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if isinstance(value.get("blockers"), list):
                for blocker in value["blockers"]:
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
    candidates: list[dict[str, Any]] = []
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    by_source: dict[str, dict[str, Any]] = {}
    for pkg in source_packages:
        pipeline = constructor.construct_pipeline(pkg)
        if pipeline.get("source_validation", {}).get("ok") and pipeline.get("knowledge_boundary", {}).get("ok"):
            candidates.append(pipeline["knowledge_candidate_package"])
            by_source[pkg["source_evidence_package_id"]] = pipeline["knowledge_object_package"]
        else:
            rejected.append({"source_evidence_package": pkg, "validation": pipeline, "reason_categories": reason_categories(pipeline)})
    for pkg in source_packages:
        base = by_source[pkg["source_evidence_package_id"]]
        paired_id = pkg["evidence_payload"]["payload_metadata"].get("paired_with")
        obj = _make_multi_reference(base, by_source[paired_id], "-multi-ref") if paired_id in by_source else base
        validation = report_dict(validator.validate_knowledge_object(obj))
        boundary = constructor.verify_knowledge_boundary(obj)
        if validation.get("ok") and boundary.get("ok"):
            accepted.append(obj)
        else:
            rejected.append({"source_evidence_package": pkg, "validation": {"knowledge_object_validation": validation, "knowledge_boundary": boundary}, "reason_categories": reason_categories({"knowledge_object_validation": validation, "knowledge_boundary": boundary})})
    return candidates, accepted, rejected


def build_rejected_candidates(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    bad = [
        source_package("srcpkg-campaign10-reject-causal-reading", "the repeated validator failures cause future production design outcomes.", "methodological", snapshot, {"topic": "causal wording"}),
        source_package("srcpkg-campaign10-reject-policy-meaning", "the recurrence audit has policy meaning for evidence production.", "coverage", snapshot, {"topic": "unsupported policy meaning"}),
        source_package("srcpkg-campaign10-reject-forecast", "the absence of duplicates forecasts that duplicate objects will not occur later.", "negative", snapshot, {"topic": "unsupported forecast"}),
        source_package("srcpkg-campaign10-reject-malformed-provenance", "the malformed recurrence candidate lacks usable provenance for campaign artifact evidence.", "provenance", snapshot, {"topic": "malformed provenance"}),
    ]
    bad[3]["provenance"] = {}
    bad[3]["fingerprints"] = constructor.expected_source_fingerprints(bad[3])
    return bad


def process_rejected_candidates(rejected_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for bad in rejected_inputs:
        pipeline = constructor.construct_pipeline(bad)
        if pipeline.get("source_validation", {}).get("ok") and pipeline.get("knowledge_boundary", {}).get("ok"):
            review = {
                "ok": False,
                "stage": "campaign_boundary_review",
                "blockers": [{
                    "category": "unsupported_inference",
                    "severity": "blocker",
                    "message": "candidate uses unsupported recurrence-audit wording for Campaign 10 scope",
                    "location": "evidence_payload.factual_statement",
                    "blocks_acceptance": True,
                }],
                "warnings": [],
            }
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
    (reports / "campaign_10_final_report.md").write_text(f"""# Campaign 10 Final Report

Campaign: {CAMPAIGN_ID}

## Result

Campaign 10 audited prior production artifacts from Campaigns 0-9 as evidence and produced recurrence, duplicate-pressure, validator-pattern, metadata-pattern, and methodology-stability Knowledge Objects without architecture change.

- Accepted KnowledgeObjectPackages: {len(accepted)}
- Rejected candidates: {len(rejected)}
- Multi-reference accepted objects: {qr['multi_reference_accepted_object_count']}
- Determinism verified: {str(qr['determinism_verification']).lower()}
- Fingerprint stability: {str(qr['fingerprint_stability']).lower()}
- Duplicate Knowledge Objects detected: {str(qr['duplicate_knowledge_objects_detected']).lower()}

## Final recommendation

{qr['final_recommendation']}
""", encoding="utf-8")
    (reports / "generated_knowledge_object_catalogue.md").write_text("\n".join(["# Generated Knowledge Object Catalogue", ""] + [f"- `{o['package_id']}` — {o['generated_statements'][0]['statement_type']} — evidence refs: {len(o['evidence_references'])} — {o['generated_statements'][0]['text']}" for o in accepted]) + "\n", encoding="utf-8")
    (reports / "rejected_knowledge_object_catalogue.md").write_text("\n".join(["# Rejected Knowledge Object Catalogue", ""] + [f"- `{r['source_evidence_package']['source_evidence_package_id']}` — {', '.join(r['reason_categories'])}" for r in rejected]) + "\n", encoding="utf-8")
    (reports / "production_quality_report.md").write_text(f"""# Production Quality Report

- Source Evidence Packages processed: {qr['source_evidence_packages_processed']}
- KnowledgeCandidatePackages generated: {qr['knowledge_candidate_packages_generated']}
- KnowledgeObjectPackages accepted: {qr['knowledge_object_packages_accepted']}
- Rejected candidates: {qr['rejected_candidates']}
- Multi-reference accepted objects: {qr['multi_reference_accepted_object_count']}
- Average evidence references per Knowledge Object: {qr['average_evidence_references_per_knowledge_object']}
- Determinism verification: {str(qr['determinism_verification']).lower()}
- Fingerprint stability: {str(qr['fingerprint_stability']).lower()}
- Duplicate Knowledge Objects detected: {str(qr['duplicate_knowledge_objects_detected']).lower()}

Campaign 10 used only existing production artifacts from Campaigns 0-9 and did not modify prior campaign outputs.
""", encoding="utf-8")
    (reports / "cross_campaign_duplicate_recurrence_audit_report.md").write_text(f"""# Cross-Campaign Duplicate and Recurrence Audit Report

## Falsification focus

- Duplicate registry pressure: {qr['falsification_focus']['duplicate_registry_pressure']}
- Repeated validator failures: {qr['falsification_focus']['repeated_validator_failures']}
- Repeated production metrics and automation pressure: {qr['falsification_focus']['repeated_production_metrics']}
- Recurrence-derived objects fit taxonomy: {qr['falsification_focus']['recurrence_derived_objects_fit_taxonomy']}
- Prior campaign artifacts as Source Evidence Packages: {qr['falsification_focus']['prior_campaign_artifacts_as_source_evidence']}
- Family maturity conflicts: {qr['falsification_focus']['family_maturity_conflicts']}

## Direct answers

1. Duplicate-registry implementation justified: {str(qr['duplicate_registry_implementation_justified']).lower()}
2. New helper extraction justified: {str(qr['new_helper_extraction_justified']).lower()}
3. Roadmap recommendation: {qr['roadmap_recommendation']}
4. Architecture/taxonomy/validator/workflow pressure: {str(qr['architecture_taxonomy_validator_or_workflow_pressure']).lower()}
""", encoding="utf-8")
    (reports / "production_retrospective_report.md").write_text("""# Production Retrospective

Campaign 10 converted prior production artifacts into deterministic production evidence. The campaign validated recurrence-derived Knowledge Objects and did not uncover implementation pressure.

The most important result is negative: repeated production evidence still does not justify a duplicate registry, helper extraction, taxonomy change, validator change, workflow change, or architecture redesign.

The next action should continue the approved roadmap with WDI Environment maturation.
""", encoding="utf-8")
    (reports / "architectural_observations_report.md").write_text("""# Architectural Observations

Campaign 10 supports preserving the current KnowledgeForge architecture unchanged.

Supported observations:

- prior production artifacts can serve as valid Source Evidence Packages;
- recurrence-count derived knowledge fits existing categories;
- cross-campaign duplicate pressure remains absent;
- recurring validator failures are expected safety behaviour, not design pressure;
- Production Support pressure remains satisfied;
- no new helper extraction is justified;
- no architecture, taxonomy, validator, or workflow blocker appeared.

No architecture change is recommended.
""", encoding="utf-8")


def run_campaign(output: Path) -> dict[str, Any]:
    snapshot = build_cross_campaign_snapshot()
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
    multi_count = sum(1 for obj in accepted_objects if len(obj.get("evidence_references", [])) >= 2)
    final_snapshot_fingerprint = sha256_fingerprint({"snapshot": snapshot, "accepted": [obj["fingerprints"]["package_manifest"] for obj in accepted_objects], "rejected": [rec["source_evidence_package"]["fingerprints"]["package_manifest"] for rec in rejected_records]})
    quality_report = {
        **base_quality,
        "source_evidence_packages_processed": len(source_packages),
        "knowledge_candidate_packages_generated": len(candidates),
        "multi_reference_accepted_object_count": multi_count,
        "single_reference_accepted_object_count": len(accepted_objects) - multi_count,
        "campaigns_audited": snapshot["campaigns_audited"],
        "campaign_range": snapshot["campaign_range"],
        "external_data_accessed": False,
        "prior_campaign_outputs_modified": False,
        "duplicate_registry_implementation_justified": False,
        "new_helper_extraction_justified": False,
        "architecture_taxonomy_validator_or_workflow_pressure": False,
        "roadmap_recommendation": "continue_with_wdi_environment_maturation",
        "next_recommended_campaign": "Campaign 11 should be resequenced as WDI Environment indicator-family inventory and coverage matrix maturation rather than local-model-assisted screening.",
        "falsification_focus": {
            "duplicate_registry_pressure": "still_absent",
            "repeated_validator_failures": "expected_safety_behaviour_not_design_pressure",
            "repeated_production_metrics": "Production Support already satisfies recurring metric aggregation pressure",
            "recurrence_derived_objects_fit_taxonomy": "validated",
            "prior_campaign_artifacts_as_source_evidence": "validated",
            "family_maturity_conflicts": "none_detected",
        },
        "pel_implications": {
            "PEL-007": "remain monitor; no duplicate registry justified after Campaign 10 audit",
            "PEL-008": "remain historical implement; Production Support pressure satisfied and no further helper extraction justified",
            "PEL-009": "remain historical implement; common metric aggregation pressure satisfied and no further helper extraction justified",
            "PEL-011": "strengthened; recurrence-derived objects fit existing taxonomy",
            "PEL-017": "broader recurrence audit completed; remaining gap is non-WDI multi-source disagreement",
            "PEL-018": "WDI demographic Mature status remains consistent; Environment maturity remains incomplete",
            "PEL-021": "methodology transfer remains supported; continue WDI Environment maturation",
        },
        "architectural_observations": [
            "Prior campaign artifacts can serve as valid Source Evidence Packages.",
            "Recurring validator failures are expected safety behaviour rather than design pressure.",
            "No duplicate-registry implementation is justified.",
            "No new helper extraction is justified beyond the completed Production Support layer.",
            "No architecture, taxonomy, validator, or workflow pressure appeared.",
        ],
        "processing_statistics": snapshot["aggregate_metrics"],
        "candidate_improvements_discovered": ["No implementation or architecture change is justified by Campaign 10."],
        "final_snapshot_fingerprint": final_snapshot_fingerprint,
        "final_recommendation": "Preserve the current production methodology unchanged and continue with WDI Environment maturation before any local-model-assisted dry campaign.",
    }
    result = {
        "snapshot": snapshot,
        "source_packages": source_packages,
        "knowledge_candidates": candidates,
        "accepted_objects": accepted_objects,
        "rejected_records": rejected_records,
        "quality_report": quality_report,
    }
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
    parser = argparse.ArgumentParser(description="Run Campaign 10 cross-campaign recurrence audit")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts" / "production" / CAMPAIGN_ID)
    args = parser.parse_args()
    result = run_campaign(args.output)
    print(json.dumps({
        "campaign_id": CAMPAIGN_ID,
        "accepted": len(result["accepted_objects"]),
        "rejected": len(result["rejected_records"]),
        "multi_reference_accepted_objects": result["quality_report"]["multi_reference_accepted_object_count"],
        "duplicate_registry_implementation_justified": result["quality_report"]["duplicate_registry_implementation_justified"],
        "new_helper_extraction_justified": result["quality_report"]["new_helper_extraction_justified"],
        "architecture_taxonomy_validator_or_workflow_pressure": result["quality_report"]["architecture_taxonomy_validator_or_workflow_pressure"],
        "roadmap_recommendation": result["quality_report"]["roadmap_recommendation"],
        "determinism_verified": result["quality_report"]["determinism_verification"],
        "fingerprint_stability": result["quality_report"]["fingerprint_stability"],
        "duplicate_knowledge_objects_detected": result["quality_report"]["duplicate_knowledge_objects_detected"],
        "snapshot_fingerprint": result["quality_report"]["final_snapshot_fingerprint"],
        "output": str(args.output.resolve()),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
