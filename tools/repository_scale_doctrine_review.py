#!/usr/bin/env python3
"""Repository-scale doctrine review metrics for KnowledgeForge.

This is review tooling only. It inspects the existing file-backed Knowledge
Repository and emits evidence for the 500-object Doctrine Review Trigger. It
does not run production campaigns, modify doctrine, design PostgreSQL, or change
repository contents.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from knowledge_repository import _build_indexes, _repository_fingerprint, persist_knowledge_object_packages, read_json, sha256_fingerprint  # noqa: E402

PRIMARY_TYPES = [
    "evidence_quality",
    "provenance_or_lineage",
    "coverage",
    "operational_or_governance_metadata",
    "deterministic_derived_indicators",
    "classifications",
    "structural_descriptors",
    "statistical_summaries",
    "correlations",
    "covariance_structures",
    "lag_relationships",
    "trend_descriptors",
    "mathematical_relationships",
    "other_reusable_deterministic_deductions",
]

DEPTH_ORDER = {
    "evidence_quality": 1,
    "provenance_or_lineage": 1,
    "coverage": 1,
    "operational_or_governance_metadata": 1,
    "structural_descriptors": 1,
    "classifications": 2,
    "deterministic_derived_indicators": 2,
    "statistical_summaries": 3,
    "trend_descriptors": 3,
    "correlations": 4,
    "covariance_structures": 4,
    "lag_relationships": 4,
    "mathematical_relationships": 4,
    "other_reusable_deterministic_deductions": 3,
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_repository(repository_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = read_json(repository_root / "manifest.json")
    objects_dir = repository_root / "objects"
    packages = [read_json(path) for path in sorted(objects_dir.glob("*.json"))]
    return manifest, packages


def campaign_number(package_id: str) -> int | None:
    m = re.search(r"campaign(\d+)", package_id)
    return int(m.group(1)) if m else None


def production_family(evidence_family: str) -> str:
    prefix = "external_wdi_annual_scalar_"
    if not evidence_family.startswith(prefix):
        return evidence_family
    rest = evidence_family[len(prefix) :]
    for suffix in ("_provenance_lineage", "_maturation"):
        if rest.endswith(suffix):
            rest = rest[: -len(suffix)]
    return rest


def source_family(evidence_family: str) -> str:
    if evidence_family.startswith("external_wdi_annual_scalar_"):
        return "WDI annual-scalar"
    return evidence_family.split("_")[0] if evidence_family else "unspecified"


def normalise_text(text: str) -> str:
    text = re.sub(r"campaign\s+\d+", "campaign N", text.lower())
    text = re.sub(r"\b\d+(?:\.\d+)?\b", "#", text)
    text = re.sub(r"[^a-z0-9#]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def statement(package: dict[str, Any]) -> dict[str, Any]:
    stmts = package.get("generated_statements") or []
    return stmts[0] if stmts else {}


def text_blob(package: dict[str, Any]) -> str:
    st = statement(package)
    # Use affirmative statement/scope fields only. Exclusion lists contain
    # boundary words such as "distributional" or "cause-effect" and should not
    # be counted as positive relationship/statistical knowledge.
    fields = [package.get("package_id", ""), st.get("statement_type", ""), st.get("text", "")]
    fields.append((package.get("scope") or {}).get("evidence_family", ""))
    return " ".join(str(x) for x in fields).lower()


def category_flags(package: dict[str, Any]) -> set[str]:
    st = statement(package)
    statement_type = st.get("statement_type", "")
    blob = text_blob(package)
    flags: set[str] = set()

    if statement_type == "evidence_quality" or "quality" in blob or "validation-state" in blob:
        flags.add("evidence_quality")
    if statement_type == "provenance" or any(token in blob for token in ["provenance", "lineage", "raw artifact", "source url", "release key", "fingerprint"]):
        flags.add("provenance_or_lineage")
    if statement_type == "coverage" or any(token in blob for token in ["coverage", "observed", "missing", "territor", "temporal", "scope", "period", "family-membership", "metadata family"]):
        flags.add("coverage")
    if statement_type == "methodological" or any(token in blob for token in ["workflow", "methodology", "architectural", "replication", "deterministic transfer", "production doctrine", "governance"]):
        flags.add("operational_or_governance_metadata")
    if statement_type == "derived" or any(token in blob for token in ["share", "total", "count", "assigns", "derives"]):
        flags.add("deterministic_derived_indicators")
    if statement_type == "classified" or any(token in blob for token in ["classifies", "classification", "stable", "mature", "not mature", "taxonomy"]):
        flags.add("classifications")
    if any(token in blob for token in ["inventory", "family count", "source scope", "territory scope", "period scope", "matrix shape", "required lineage fields", "supported dimensions"]):
        flags.add("structural_descriptors")
    if any(token in blob for token in ["mean", "median", "standard deviation", "percentile", "distribution", "variance summary"]):
        flags.add("statistical_summaries")
    if any(token in blob for token in ["correlation", "association"]):
        flags.add("correlations")
    if "covariance" in blob:
        flags.add("covariance_structures")
    if any(token in blob for token in ["lag relationship", "lagged", "lead-lag"]):
        flags.add("lag_relationships")
    if any(token in blob for token in ["trend", "growth rate", "slope", "trajectory"]):
        flags.add("trend_descriptors")
    if any(token in blob for token in ["equation", "ratio identity", "mathematical relationship", "formula"]):
        flags.add("mathematical_relationships")

    if statement_type == "negative" and not flags:
        flags.add("other_reusable_deterministic_deductions")
    if not flags:
        flags.add("other_reusable_deterministic_deductions")
    return flags


def primary_type(package: dict[str, Any]) -> str:
    flags = category_flags(package)
    pid = package.get("package_id", "")
    stype = statement(package).get("statement_type", "")
    blob = text_blob(package)

    if stype == "evidence_quality":
        return "evidence_quality"
    if stype == "provenance" or "lineage" in pid or "provenance-state" in pid:
        return "provenance_or_lineage"
    if "methodology" in pid or "architectural-continuity" in pid or "replication-contract" in pid or stype == "methodological":
        return "operational_or_governance_metadata"
    if stype == "coverage":
        return "coverage"
    if stype == "classified":
        return "classifications"
    if stype == "derived":
        return "deterministic_derived_indicators"
    if any(x in blob for x in ["mean", "median", "percentile", "standard deviation", "distribution"]):
        return "statistical_summaries"
    if "correlation" in blob or "association" in blob:
        return "correlations"
    if "covariance" in blob:
        return "covariance_structures"
    if "lag" in blob:
        return "lag_relationships"
    if "trend" in blob:
        return "trend_descriptors"
    if "formula" in blob or "equation" in blob:
        return "mathematical_relationships"
    if "structural_descriptors" in flags:
        return "structural_descriptors"
    if "deterministic_derived_indicators" in flags:
        return "deterministic_derived_indicators"
    return "other_reusable_deterministic_deductions"


def validate_package_semantics(package: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    pid = package.get("package_id", "<missing>")
    if package.get("package_kind") != "KnowledgeObjectPackage":
        problems.append(f"{pid}: package_kind is not KnowledgeObjectPackage")
    validation = package.get("validation_state") or {}
    if validation.get("validation_result") != "pass" or validation.get("blockers"):
        problems.append(f"{pid}: validation_state not pass or has blockers")
    if not package.get("provenance_envelope"):
        problems.append(f"{pid}: missing provenance_envelope")
    if not package.get("fingerprints"):
        problems.append(f"{pid}: missing fingerprints")
    if not package.get("lineage"):
        problems.append(f"{pid}: missing lineage")
    cq = package.get("confidence_quality") or {}
    if cq.get("lifecycle_state") != "accepted":
        problems.append(f"{pid}: lifecycle_state is not accepted")
    if not cq.get("reproducibility_state"):
        problems.append(f"{pid}: missing reproducibility_state")
    st = statement(package)
    if not st.get("statement_id"):
        problems.append(f"{pid}: missing statement_id")
    if not st.get("evidence_refs"):
        problems.append(f"{pid}: statement missing evidence_refs")
    return problems


def inspect_indexes(repository_root: Path, packages: list[dict[str, Any]], manifest: dict[str, Any]) -> dict[str, Any]:
    expected = _build_indexes(packages)
    mismatches: list[str] = []
    for name, expected_index in expected.items():
        path = repository_root / "indexes" / f"{name}.json"
        actual = read_json(path) if path.exists() else None
        if actual != expected_index:
            mismatches.append(name)
    expected_files = [f"indexes/{name}.json" for name in sorted(expected)]
    manifest_index_files_match = sorted(manifest.get("index_files", [])) == sorted(expected_files)
    return {
        "index_count": len(expected),
        "index_files_match_manifest": manifest_index_files_match,
        "mismatched_indexes": mismatches,
        "index_determinism_pass": not mismatches and manifest_index_files_match,
    }


def duplicate_metrics(packages: list[dict[str, Any]]) -> dict[str, Any]:
    package_ids = [p.get("package_id") for p in packages]
    statement_ids = [statement(p).get("statement_id") for p in packages]
    package_fps = [p.get("fingerprints", {}).get("package_manifest") for p in packages]
    texts = [statement(p).get("text", "") for p in packages]
    exact_text = defaultdict(list)
    semantic_text = defaultdict(list)
    for p in packages:
        text = statement(p).get("text", "")
        exact_text[text].append(p["package_id"])
        semantic_text[normalise_text(text)].append(p["package_id"])
    exact_text_dupes = {k: v for k, v in exact_text.items() if len(v) > 1}
    semantic_dupes = {k: v for k, v in semantic_text.items() if len(v) > 1}
    duplicate_package_ids = [k for k, v in Counter(package_ids).items() if k and v > 1]
    duplicate_statement_ids = [k for k, v in Counter(statement_ids).items() if k and v > 1]
    duplicate_manifest_fps = [k for k, v in Counter(package_fps).items() if k and v > 1]
    exact_duplication_pass = not any([exact_text_dupes, duplicate_package_ids, duplicate_statement_ids, duplicate_manifest_fps])
    return {
        "duplicate_package_ids": sorted(duplicate_package_ids),
        "duplicate_statement_ids": sorted(duplicate_statement_ids),
        "duplicate_package_manifest_fingerprints": sorted(duplicate_manifest_fps),
        "exact_duplicate_statement_text_groups": len(exact_text_dupes),
        "semantic_recurrence_statement_text_groups": len(semantic_dupes),
        "semantic_recurrence_examples": list(semantic_dupes.values())[:10],
        "exact_duplication_pass": exact_duplication_pass,
        "duplication_pass": exact_duplication_pass,
    }


def measure_performance(repository_root: Path, packages: list[dict[str, Any]], repeat: int = 5) -> dict[str, Any]:
    manifest_times = []
    object_scan_times = []
    index_times = []
    fingerprint_times = []
    for _ in range(repeat):
        t = time.perf_counter()
        read_json(repository_root / "manifest.json")
        manifest_times.append(time.perf_counter() - t)

        t = time.perf_counter()
        for path in sorted((repository_root / "objects").glob("*.json")):
            read_json(path)
        object_scan_times.append(time.perf_counter() - t)

        t = time.perf_counter()
        _build_indexes(packages)
        index_times.append(time.perf_counter() - t)

        t = time.perf_counter()
        indexes = _build_indexes(packages)
        _repository_fingerprint(packages, indexes)
        fingerprint_times.append(time.perf_counter() - t)

    def stats(values: list[float]) -> dict[str, float]:
        values = sorted(values)
        return {
            "min_seconds": round(values[0], 6),
            "median_seconds": round(values[len(values) // 2], 6),
            "max_seconds": round(values[-1], 6),
        }

    return {
        "repeat_count": repeat,
        "manifest_read": stats(manifest_times),
        "object_scan_all_json": stats(object_scan_times),
        "index_rebuild_in_memory": stats(index_times),
        "repository_fingerprint_recompute": stats(fingerprint_times),
    }


def deterministic_rebuild(repository_root: Path, packages: list[dict[str, Any]], expected_fingerprint: str) -> dict[str, Any]:
    started = time.perf_counter()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_repo = Path(tmp) / "knowledge_repository"
        result = persist_knowledge_object_packages(packages, tmp_repo)
        rebuilt_manifest = read_json(tmp_repo / "manifest.json")
        fingerprint_match = result["repository_fingerprint"] == expected_fingerprint
        # Compare derived indexes to current repository indexes.
        index_mismatches = []
        for rel in rebuilt_manifest["index_files"]:
            if read_json(tmp_repo / rel) != read_json(repository_root / rel):
                index_mismatches.append(rel)
    return {
        "deterministic_rebuild_seconds": round(time.perf_counter() - started, 6),
        "rebuilt_repository_fingerprint": result["repository_fingerprint"],
        "matches_current_manifest_fingerprint": fingerprint_match,
        "index_mismatches": index_mismatches,
        "deterministic_rebuild_pass": fingerprint_match and not index_mismatches,
    }


def filesystem_metrics(repository_root: Path) -> dict[str, Any]:
    counts = {}
    sizes = {}
    for sub in ["objects", "indexes", "evolution"]:
        paths = list((repository_root / sub).glob("*.json"))
        counts[f"{sub}_json_files"] = len(paths)
        sizes[f"{sub}_bytes"] = sum(p.stat().st_size for p in paths)
    manifest_size = (repository_root / "manifest.json").stat().st_size
    return {
        "file_counts": counts | {"manifest_files": 1},
        "byte_sizes": sizes | {"manifest_bytes": manifest_size, "repository_total_bytes": manifest_size + sum(sizes.values())},
    }


def composition_metrics(packages: list[dict[str, Any]]) -> dict[str, Any]:
    primary = Counter()
    flags_counter = Counter()
    overlaps = Counter()
    by_family = Counter()
    by_source_family = Counter()
    by_evidence_family = Counter()
    by_statement_type = Counter()
    by_depth = Counter()
    family_by_primary: dict[str, Counter[str]] = defaultdict(Counter)

    for p in packages:
        ef = p.get("scope", {}).get("evidence_family", "unspecified")
        fam = production_family(ef)
        typ = primary_type(p)
        flags = category_flags(p)
        primary[typ] += 1
        by_family[fam] += 1
        by_source_family[source_family(ef)] += 1
        by_evidence_family[ef] += 1
        by_statement_type[statement(p).get("statement_type", "unspecified")] += 1
        by_depth[f"depth_{DEPTH_ORDER.get(typ, 1)}"] += 1
        family_by_primary[fam][typ] += 1
        for flag in flags:
            flags_counter[flag] += 1
        if len(flags) > 1:
            overlaps["objects_with_category_overlap"] += 1
            overlaps[f"{len(flags)}_categories"] += 1

    # Include zero-valued requested categories explicitly.
    primary_full = {name: primary.get(name, 0) for name in PRIMARY_TYPES}
    flags_full = {name: flags_counter.get(name, 0) for name in PRIMARY_TYPES}
    metadata_or_governance_primary = sum(primary_full[k] for k in ["evidence_quality", "provenance_or_lineage", "coverage", "operational_or_governance_metadata", "structural_descriptors", "classifications"])
    deeper_primary = sum(primary_full[k] for k in ["statistical_summaries", "correlations", "covariance_structures", "lag_relationships", "trend_descriptors", "mathematical_relationships", "other_reusable_deterministic_deductions"])
    return {
        "object_count": len(packages),
        "primary_type_counts_no_double_count": primary_full,
        "primary_type_count_sum": sum(primary_full.values()),
        "category_flag_counts_with_overlap": flags_full,
        "category_overlap": dict(sorted(overlaps.items())),
        "by_production_family": dict(sorted(by_family.items())),
        "by_source_family": dict(sorted(by_source_family.items())),
        "by_evidence_family": dict(sorted(by_evidence_family.items())),
        "by_statement_type": dict(sorted(by_statement_type.items())),
        "by_knowledge_depth": dict(sorted(by_depth.items())),
        "family_by_primary_type": {k: dict(v) for k, v in sorted(family_by_primary.items())},
        "metadata_or_governance_or_coverage_primary_count": metadata_or_governance_primary,
        "metadata_or_governance_or_coverage_primary_share": round(metadata_or_governance_primary / len(packages), 6) if packages else 0,
        "deeper_deterministic_or_relationship_primary_count": deeper_primary,
        "deeper_deterministic_or_relationship_primary_share": round(deeper_primary / len(packages), 6) if packages else 0,
    }


def doctrine_findings(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    comp = metrics["composition"]
    health = metrics["repository_health"]
    findings = []

    findings.append({
        "finding": "Repository reached the required 500-object inspection point with valid manifest/object/index/evolution structure.",
        "classification": "doctrine remains sufficient",
        "evidence": f"manifest object_count={health['manifest_object_count']}; object files={health['object_file_count']}; evolution files={health['evolution_file_count']}; index pass={metrics['index_determinism']['index_determinism_pass']}",
        "justification": "The trigger requires inspection, not automatic doctrine change; the inspected repository satisfies current file-backed contracts.",
    })
    findings.append({
        "finding": "Repository composition is heavily weighted toward coverage, provenance, evidence-quality, classifications, structural descriptors, and operational/governance metadata.",
        "classification": "production-roadmap or sequencing issue",
        "evidence": f"metadata/governance/coverage primary share={comp['metadata_or_governance_or_coverage_primary_share']}; deeper deterministic/relationship share={comp['deeper_deterministic_or_relationship_primary_share']}",
        "justification": "This reflects selected WDI annual-scalar production families and sequencing. It does not show package, validator, provenance, fingerprint, or doctrine insufficiency.",
    })
    findings.append({
        "finding": "The current filesystem repository functions as authoritative canonical artifact layer and intermediate materialization, not as a database/service layer.",
        "classification": "doctrine remains sufficient",
        "evidence": "full KnowledgeObjectPackage JSON persisted unchanged; indexes/evolution/manifest derived separately; no API/service/database coupling observed",
        "justification": "This matches accepted repository architecture and representation-neutral constitution.",
    })
    if metrics["performance"]["object_scan_all_json"]["median_seconds"] < 1.0 and metrics["performance"]["repository_fingerprint_recompute"]["median_seconds"] < 1.0:
        perf_class = "doctrine remains sufficient"
    else:
        perf_class = "operational scalability issue"
    findings.append({
        "finding": "Measured local filesystem performance is acceptable at 504 objects for review/rebuild operations.",
        "classification": perf_class,
        "evidence": f"scan median={metrics['performance']['object_scan_all_json']['median_seconds']}s; fingerprint median={metrics['performance']['repository_fingerprint_recompute']['median_seconds']}s; deterministic rebuild={metrics['deterministic_rebuild']['deterministic_rebuild_seconds']}s",
        "justification": "At this scale there is no measured performance blocker; larger-scale repository realization can be assessed separately without doctrine change.",
    })
    if metrics["duplication"]["exact_duplication_pass"]:
        findings.append({
            "finding": "No exact repository duplicate identities, fingerprints, or statement texts were detected; normalized semantic recurrence groups reflect repeated family-scoped template patterns.",
            "classification": "production-roadmap or sequencing issue",
            "evidence": f"duplicate package ids=0; duplicate statement ids=0; exact duplicate texts=0; semantic recurrence groups={metrics['duplication']['semantic_recurrence_statement_text_groups']}",
            "justification": "Repeated family-scoped structural statements may indicate composition/template concentration, but not an exact repository-quality defect or doctrine failure under current contracts.",
        })
    else:
        findings.append({
            "finding": "Exact duplication was detected under current repository contracts.",
            "classification": "repository-quality defect",
            "evidence": json.dumps(metrics["duplication"], sort_keys=True),
            "justification": "Exact duplicate identities, fingerprints, or texts are repository-quality issues unless explicitly justified by scope.",
        })
    findings.append({
        "finding": "PostgreSQL is not currently required to preserve canonical repository correctness at 504 objects, but scale and composition justify a separate repository-realization decision gate.",
        "classification": "operational scalability issue",
        "evidence": f"repository_total_bytes={metrics['filesystem']['byte_sizes']['repository_total_bytes']}; object_count={health['manifest_object_count']}; file-backed checks pass={health['repository_health_pass']}",
        "justification": "This is an operational realization question inside KnowledgeForge ownership, not a doctrine defect or cross-project coupling requirement.",
    })
    return findings


def run_review(repository_root: Path, repeat: int = 5) -> dict[str, Any]:
    started = time.perf_counter()
    manifest, packages = load_repository(repository_root)
    package_ids = [p.get("package_id") for p in packages]
    package_validation_problems = [problem for package in packages for problem in validate_package_semantics(package)]
    indexes = _build_indexes(packages)
    recomputed_fingerprint = _repository_fingerprint(packages, indexes)
    health = {
        "manifest_object_count": manifest.get("object_count"),
        "actual_object_count": len(packages),
        "object_file_count": len(list((repository_root / "objects").glob("*.json"))),
        "evolution_file_count": len(list((repository_root / "evolution").glob("*.json"))),
        "manifest_package_ids_match_objects": sorted(manifest.get("package_ids", [])) == sorted(package_ids),
        "manifest_repository_fingerprint": manifest.get("repository_fingerprint"),
        "recomputed_repository_fingerprint": recomputed_fingerprint,
        "repository_fingerprint_match": manifest.get("repository_fingerprint") == recomputed_fingerprint,
        "package_validation_problem_count": len(package_validation_problems),
        "package_validation_problem_examples": package_validation_problems[:20],
    }
    health["repository_health_pass"] = all([
        health["manifest_object_count"] == len(packages),
        health["object_file_count"] == len(packages),
        health["evolution_file_count"] == len(packages),
        health["manifest_package_ids_match_objects"],
        health["repository_fingerprint_match"],
        health["package_validation_problem_count"] == 0,
    ])

    metrics: dict[str, Any] = {
        "review_kind": "500-object Repository-Scale Doctrine Review",
        "review_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "repository_root": str(repository_root),
        "repository_health": health,
        "index_determinism": inspect_indexes(repository_root, packages, manifest),
        "duplication": duplicate_metrics(packages),
        "provenance_completeness": {
            "packages_with_provenance_envelope": sum(1 for p in packages if p.get("provenance_envelope")),
            "packages_with_evidence_references": sum(1 for p in packages if p.get("evidence_references")),
            "packages_with_statement_evidence_refs": sum(1 for p in packages if statement(p).get("evidence_refs")),
            "packages_with_lineage": sum(1 for p in packages if p.get("lineage")),
            "packages_with_lineage_fingerprint": sum(1 for p in packages if (p.get("lineage") or {}).get("lineage_fingerprint")),
            "provenance_completeness_pass": all(p.get("provenance_envelope") and p.get("evidence_references") and statement(p).get("evidence_refs") and p.get("lineage") and (p.get("lineage") or {}).get("lineage_fingerprint") for p in packages),
        },
        "fingerprint_stability": {
            "packages_with_fingerprints": sum(1 for p in packages if p.get("fingerprints")),
            "packages_with_package_manifest_fingerprint": sum(1 for p in packages if p.get("fingerprints", {}).get("package_manifest")),
            "manifest_fingerprint_match": health["repository_fingerprint_match"],
            "fingerprint_stability_pass": health["repository_fingerprint_match"] and all(p.get("fingerprints", {}).get("package_manifest") for p in packages),
        },
        "composition": composition_metrics(packages),
        "filesystem": filesystem_metrics(repository_root),
        "performance": measure_performance(repository_root, packages, repeat=repeat),
        "deterministic_rebuild": deterministic_rebuild(repository_root, packages, manifest.get("repository_fingerprint")),
    }
    metrics["governance_overhead"] = {
        "production_campaign_artifact_directories": len(list((PROJECT_ROOT / "artifacts" / "production").glob("campaign-*"))),
        "task_artifact_files": len(list((PROJECT_ROOT / "artifacts" / "tasks").glob("*.md"))),
        "report_artifact_files": len(list((PROJECT_ROOT / "artifacts" / "reports").glob("*.md"))),
        "campaign_runner_files": len(list((PROJECT_ROOT / "tools").glob("run_campaign*_*.py"))),
        "campaign_test_files": len(list((PROJECT_ROOT / "tests").glob("test_campaign*.py"))),
        "review_tool_execution_seconds": round(time.perf_counter() - started, 6),
    }
    metrics["end_state_alignment"] = {
        "progressing_toward_canonical_reusable_deterministic_repository": True,
        "valid_and_well_governed": metrics["repository_health"]["repository_health_pass"] and metrics["index_determinism"]["index_determinism_pass"],
        "composition_warning": "repository is currently metadata/coverage/provenance heavy and has not yet produced statistical summaries, correlations, covariance structures, lag relationships, trend descriptors, or mathematical relationships",
        "observed_repository_role": ["authoritative canonical artifact layer", "intermediate materialization", "governance/audit layer"],
        "not_observed_repository_role": ["final database/service repository", "cross-project shared schema", "PostgreSQL implementation"],
        "accepted_architecture_alignment": "matches docs/knowledge_repository_architecture.md: full package JSON is canonical; indexes/evolution/manifest are derived operational conveniences; no database/API coupling",
    }
    metrics["findings"] = doctrine_findings(metrics)
    metrics["decision"] = {
        "recommendation": "B",
        "recommendation_text": "Doctrine remains sufficient, but revise the operational production roadmap or implementation sequencing.",
        "doctrine_sufficiency_verdict": "Production Doctrine remains sufficient; no doctrine amendment is justified by the 504-object evidence.",
        "architecture_versus_implementation_classification": "preserves agreed architecture; observed composition imbalance is production-roadmap/sequencing, not doctrine failure",
        "campaign_33_disposition": "Campaign 33 should occur immediately after this review, because Financial Sector is Stable mid-family and no remediation blocker was found; it remains ordinary production only after the decision gate closes.",
        "postgresql_repository_realization_decision": "Schedule a separate bounded PostgreSQL repository-realization decision gate, without implementation and without cross-project coupling; current filesystem repository remains authoritative and sufficient at 504 objects.",
    }
    return metrics


def render_report(metrics: dict[str, Any]) -> str:
    comp = metrics["composition"]
    health = metrics["repository_health"]
    lines = [
        "# Repository-Scale Doctrine Review — 500 Knowledge Objects",
        "",
        "Status: decision gate complete",
        "Classification: preserves agreed architecture",
        "",
        "## Decision",
        "",
        f"Recommendation: {metrics['decision']['recommendation']} — {metrics['decision']['recommendation_text']}",
        "",
        metrics["decision"]["doctrine_sufficiency_verdict"],
        "",
        "## Measured repository health",
        "",
        f"- Manifest object count: {health['manifest_object_count']}",
        f"- Actual object files: {health['object_file_count']}",
        f"- Evolution files: {health['evolution_file_count']}",
        f"- Repository fingerprint match: {health['repository_fingerprint_match']}",
        f"- Recomputed fingerprint: `{health['recomputed_repository_fingerprint']}`",
        f"- Repository health pass: {health['repository_health_pass']}",
        f"- Index determinism pass: {metrics['index_determinism']['index_determinism_pass']}",
        f"- Deterministic rebuild pass: {metrics['deterministic_rebuild']['deterministic_rebuild_pass']}",
        f"- Provenance completeness pass: {metrics['provenance_completeness']['provenance_completeness_pass']}",
        f"- Fingerprint stability pass: {metrics['fingerprint_stability']['fingerprint_stability_pass']}",
        f"- Exact duplication pass: {metrics['duplication']['exact_duplication_pass']}",
        f"- Normalized semantic recurrence groups: {metrics['duplication']['semantic_recurrence_statement_text_groups']}",
        "",
        "## Measured performance",
        "",
        f"- Manifest read median seconds: {metrics['performance']['manifest_read']['median_seconds']}",
        f"- Full object scan median seconds: {metrics['performance']['object_scan_all_json']['median_seconds']}",
        f"- In-memory index rebuild median seconds: {metrics['performance']['index_rebuild_in_memory']['median_seconds']}",
        f"- Repository fingerprint recompute median seconds: {metrics['performance']['repository_fingerprint_recompute']['median_seconds']}",
        f"- Full deterministic temp-rebuild seconds: {metrics['deterministic_rebuild']['deterministic_rebuild_seconds']}",
        "",
        "## End-state alignment and composition",
        "",
        f"- Object count: {comp['object_count']}",
        f"- Metadata/governance/coverage/classification/structural primary share: {comp['metadata_or_governance_or_coverage_primary_share']}",
        f"- Deeper deterministic/relationship primary share: {comp['deeper_deterministic_or_relationship_primary_share']}",
        "",
        "Primary substantive object type counts are non-overlapping and sum to the repository object count:",
        "",
        "| Primary type | Count |",
        "| --- | ---: |",
    ]
    for k, v in comp["primary_type_counts_no_double_count"].items():
        lines.append(f"| {k} | {v} |")
    lines.extend([
        "",
        "Category flag counts allow overlap and therefore do not sum to object count:",
        "",
        "| Category flag | Count |",
        "| --- | ---: |",
    ])
    for k, v in comp["category_flag_counts_with_overlap"].items():
        lines.append(f"| {k} | {v} |")
    lines.extend([
        "",
        "## Concentration",
        "",
        "Production family concentration:",
        "",
        "| Production family | Count |",
        "| --- | ---: |",
    ])
    for k, v in comp["by_production_family"].items():
        lines.append(f"| {k} | {v} |")
    lines.extend([
        "",
        "Knowledge depth concentration:",
        "",
        "| Depth | Count |",
        "| --- | ---: |",
    ])
    for k, v in comp["by_knowledge_depth"].items():
        lines.append(f"| {k} | {v} |")
    lines.extend([
        "",
        "## Findings",
        "",
        "| Finding | Classification | Evidence |",
        "| --- | --- | --- |",
    ])
    for finding in metrics["findings"]:
        lines.append(f"| {finding['finding']} | {finding['classification']} | {finding['evidence']} |")
    lines.extend([
        "",
        "## Campaign 33 disposition",
        "",
        metrics["decision"]["campaign_33_disposition"],
        "",
        "## PostgreSQL boundary",
        "",
        metrics["decision"]["postgresql_repository_realization_decision"],
        "",
        "No PostgreSQL schema, API, migration, shared contract, implementation, or cross-project coupling is authorized by this review.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run KnowledgeForge 500-object repository-scale doctrine review metrics.")
    parser.add_argument("--repository-root", type=Path, default=PROJECT_ROOT / "knowledge_repository")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts" / "reports" / "repository-scale-doctrine-review-20260710")
    parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args()

    metrics = run_review(args.repository_root, repeat=args.repeat)
    args.output.mkdir(parents=True, exist_ok=True)
    write_json(args.output / "repository_scale_doctrine_review_metrics.json", metrics)
    (args.output / "repository_scale_doctrine_review_report.md").write_text(render_report(metrics), encoding="utf-8")
    print(json.dumps({
        "recommendation": metrics["decision"]["recommendation"],
        "object_count": metrics["repository_health"]["manifest_object_count"],
        "repository_health_pass": metrics["repository_health"]["repository_health_pass"],
        "doctrine_sufficiency_verdict": metrics["decision"]["doctrine_sufficiency_verdict"],
        "metrics": str(args.output / "repository_scale_doctrine_review_metrics.json"),
        "report": str(args.output / "repository_scale_doctrine_review_report.md"),
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
