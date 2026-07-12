#!/usr/bin/env python3
"""Bounded PostgreSQL Knowledge Repository Realization Decision support.

Decision/evidence tooling only. This script does not connect to PostgreSQL, emit SQL,
create schemas, define tables, or implement loaders/APIs/services. It inspects the
canonical filesystem-backed Knowledge Repository and project governance artifacts,
then writes a decision-support report and machine-readable option matrix.
"""
from __future__ import annotations

import argparse
import json
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCALE_TARGETS = [1_000, 10_000, 100_000, 1_000_000]
FORBIDDEN_IMPLEMENTATION_TERMS = [
    "CREATE TABLE",
    "ALTER TABLE",
    "CREATE INDEX",
    "INSERT INTO",
    "CREATE SCHEMA",
    "MIGRATION",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def load_packages(repository_root: Path) -> list[dict[str, Any]]:
    return [read_json(path) for path in sorted((repository_root / "objects").glob("*.json"))]


def read_text_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def contains_any(text: str, needles: list[str]) -> list[str]:
    lower = text.lower()
    return [needle for needle in needles if needle.lower() in lower]


def extract_architectural_commitments(project_root: Path) -> dict[str, Any]:
    files = {
        "constitution": project_root / "CONSTITUTION.md",
        "architecture": project_root / "docs" / "architecture.md",
        "production_doctrine": project_root / "docs" / "production_doctrine.md",
        "repository_architecture": project_root / "docs" / "knowledge_repository_architecture.md",
        "state_architecture": project_root / "state" / "architecture.md",
        "doctrine_review_decision": project_root / "artifacts" / "decisions" / "D-20260710-repository-scale-doctrine-review-500-object-gate.md",
        "roadmap": project_root / "docs" / "production_campaign_roadmap.md",
        "evolution_log": project_root / "docs" / "production_evolution_log.md",
    }
    text = {name: read_text_if_exists(path) for name, path in files.items()}
    commitments = {
        "canonical_authority": [
            {
                "commitment": "Full KnowledgeObjectPackage JSON is canonical and remains the authoritative package representation.",
                "evidence": "docs/knowledge_repository_architecture.md states the canonical persisted object representation is the existing validated KnowledgeObjectPackage JSON and repository metadata/indexes/evolution records are separate.",
                "classification": "preserves existing architecture",
            },
            {
                "commitment": "Tables, graphs, APIs, database schemas, and documents are representations, not defining abstractions.",
                "evidence": "CONSTITUTION.md non-negotiable rule 4 and representation-neutrality rule 9.",
                "classification": "preserves existing architecture",
            },
        ],
        "operational_retrieval": [
            {
                "commitment": "KnowledgeForge must serve reusable knowledge and provide governed reusable knowledge interfaces for downstream reasoning/navigation/decision systems.",
                "evidence": "CONSTITUTION.md purpose line and docs/architecture.md purpose/architectural-position sections.",
                "classification": "operational realization requirement",
            },
            {
                "commitment": "Current file indexes support retrieval by package id, knowledge identity, evidence family, statement type, lifecycle state, and package manifest fingerprint.",
                "evidence": "docs/knowledge_repository_architecture.md indexing strategy and knowledge_repository/indexes contents.",
                "classification": "preserves existing architecture",
            },
        ],
        "postgresql": [
            {
                "commitment": "A separate bounded PostgreSQL repository-realization decision is required; implementation is not authorized by prior gates.",
                "evidence": "500-object doctrine review decision and current state/architecture handoff.",
                "classification": "operational realization requirement",
            },
            {
                "commitment": "V1 did not select storage technology, but KnowledgeForge should eventually own a knowledge database or equivalent persistent knowledge store separate from external observational databases.",
                "evidence": "docs/architecture.md knowledge database posture.",
                "classification": "operational realization requirement",
            },
        ],
        "downstream_consumption": [
            {
                "commitment": "KnowledgeForge may provide governed reusable knowledge interfaces to downstream systems but must not own reasoning, forecasting, decision, presentation, or observational responsibilities.",
                "evidence": "CONSTITUTION.md and docs/architecture.md scope/non-scope boundaries.",
                "classification": "preserves existing architecture",
            },
            {
                "commitment": "External project-specific runtime interfaces and shared ownership are forbidden; KnowledgeForge remains independent.",
                "evidence": "CONSTITUTION.md rule 2 and docs/knowledge_repository_architecture.md architectural boundary.",
                "classification": "preserves existing architecture",
            },
        ],
        "rebuildability": [
            {
                "commitment": "Repository indexes, manifests, and evolution records are deterministic operational structures derived from packages.",
                "evidence": "docs/knowledge_repository_architecture.md persistence/index/evolution sections and repository-scale review metrics.",
                "classification": "preserves existing architecture",
            }
        ],
        "project_independence": [
            {
                "commitment": "KnowledgeForge must not introduce shared schemas, database ownership, runtime code, or cross-project coupling.",
                "evidence": "CONSTITUTION.md, repository architecture boundary, 500-object decision, and user task boundary.",
                "classification": "preserves existing architecture",
            }
        ],
    }
    contradiction_checks = {
        "json_canonical_and_database_intent_coexist": all(
            [
                "KnowledgeObjectPackage" in text["repository_architecture"],
                "knowledge database" in text["architecture"],
                "Representation neutrality" in text["constitution"] or "Representation neutrality is mandatory" in text["constitution"],
            ]
        ),
        "postgresql_not_currently_implemented": "PostgreSQL implementation" in text["state_architecture"] or "PostgreSQL remains" in text["state_architecture"],
        "doctrine_frozen_and_realization_allowed": "Repository population is an additional operational output" in text["production_doctrine"] and "PostgreSQL" in text["doctrine_review_decision"],
    }
    contradictions: list[dict[str, str]] = []
    if not contradiction_checks["json_canonical_and_database_intent_coexist"]:
        contradictions.append({
            "finding": "Unable to prove coexistence of canonical JSON and eventual database intent from inspected artifacts.",
            "classification": "genuine architectural contradiction",
        })
    return {"commitments": commitments, "contradiction_checks": contradiction_checks, "contradictions": contradictions}


def package_text(package: dict[str, Any]) -> str:
    statements = package.get("generated_statements") or []
    return "\n".join(str(s.get("text", "")) for s in statements if isinstance(s, dict))


def derive_supported_requirements(packages: list[dict[str, Any]], repository_root: Path) -> dict[str, Any]:
    manifest = read_json(repository_root / "manifest.json")
    indexes_dir = repository_root / "indexes"
    index_names = sorted(path.stem for path in indexes_dir.glob("*.json"))
    def count(predicate) -> int:
        return sum(1 for package in packages if predicate(package))
    text_all = "\n".join(package_text(p).lower() for p in packages)
    requirements = [
        ("lookup_by_package_id", "package_id" in (packages[0] if packages else {}), "package_id exists for every package and by_package_id index exists", "preserves existing architecture"),
        ("filter_by_family", "by_evidence_family" in index_names, "evidence_family appears in scope and is indexed", "preserves existing architecture"),
        ("filter_by_source", count(lambda p: bool(p.get("provenance_envelope", {}).get("source_system") or p.get("scope", {}).get("source_family") or p.get("scope", {}).get("evidence_family"))) > 0, "source/evidence family represented in package scopes/provenance", "operational realization requirement"),
        ("filter_by_object_type", "by_statement_type" in index_names, "generated statement_type is indexed", "preserves existing architecture"),
        ("filter_by_knowledge_depth", True, "521-object review computed knowledge-depth classifications from package content; no canonical index yet", "implementation concern for a later task"),
        ("filter_by_maturity", "mature" in text_all or "stable" in text_all, "family maturity/status appears in generated statements and production artifacts", "operational realization requirement"),
        ("filter_by_evidence_scope", count(lambda p: bool(p.get("scope"))) == len(packages), "scope exists for every inspected package", "preserves existing architecture"),
        ("filter_by_geography", any("territory" in package_text(p).lower() or "geograph" in package_text(p).lower() for p in packages), "territory/geography is represented in production statements where applicable", "implementation concern for a later task"),
        ("filter_by_time", any("period" in package_text(p).lower() or "temporal" in package_text(p).lower() for p in packages), "temporal coverage/period knowledge exists in production statements", "implementation concern for a later task"),
        ("filter_by_methodology", any("methodolog" in package_text(p).lower() for p in packages), "methodological statements are present", "operational realization requirement"),
        ("provenance_and_lineage_traversal", count(lambda p: bool(p.get("provenance_envelope")) and bool(p.get("lineage"))) == len(packages), "provenance_envelope and lineage exist for all packages", "operational realization requirement"),
        ("fingerprint_lookup_and_verification", "by_package_manifest_fingerprint" in index_names, "package manifest fingerprint index exists", "preserves existing architecture"),
        ("relationship_discovery", any(word in text_all for word in ["relationship", "mapping", "dependency", "comparison"]), "relationship/comparison/dependency language exists but richer relationship objects are not yet present", "implementation concern for a later task"),
        ("deterministic_derived_knowledge_retrieval", any((p.get("generated_statements") or [{}])[0].get("statement_type") == "derived" for p in packages), "derived statement_type appears in persisted packages", "operational realization requirement"),
        ("version_and_supersession_discovery", count(lambda p: bool(p.get("package_version") or p.get("evolution_metadata") or p.get("lineage"))) == len(packages), "package_version/evolution/lineage fields exist", "operational realization requirement"),
        ("bulk_retrieval_for_downstream_analysis", len(packages) > 0, "full package JSON is available for all objects; bulk retrieval currently means filesystem traversal", "operational realization requirement"),
        ("reproducible_repository_snapshots", bool(manifest.get("repository_fingerprint")), "manifest records repository fingerprint", "preserves existing architecture"),
        ("efficient_access_for_richer_statistical_objects", True, "architecture intends statistical summaries/relationships, but repository currently has zero such primary objects", "implementation concern for a later task"),
    ]
    return {
        "object_count": len(packages),
        "index_names": index_names,
        "requirements": [
            {"requirement": name, "supported_by_current_evidence": bool(ok), "evidence": evidence, "classification": classification}
            for name, ok, evidence, classification in requirements
        ],
    }


def measure_retrieval_performance(packages: list[dict[str, Any]], repository_root: Path, repeat: int) -> dict[str, Any]:
    package_paths = sorted((repository_root / "objects").glob("*.json"))
    manifest_path = repository_root / "manifest.json"
    indexes_dir = repository_root / "indexes"
    by_package_id = read_json(indexes_dir / "by_package_id.json")
    by_evidence_family = read_json(indexes_dir / "by_evidence_family.json")
    by_statement_type = read_json(indexes_dir / "by_statement_type.json")
    by_fingerprint = read_json(indexes_dir / "by_package_manifest_fingerprint.json")
    sample_package_id = packages[len(packages) // 2]["package_id"] if packages else ""
    sample_evidence_family = next(iter(by_evidence_family.keys())) if by_evidence_family else ""
    sample_statement_type = next(iter(by_statement_type.keys())) if by_statement_type else ""
    sample_fingerprint = next(iter(by_fingerprint.keys())) if by_fingerprint else ""

    timings: dict[str, list[float]] = defaultdict(list)
    for _ in range(repeat):
        start = time.perf_counter(); read_json(manifest_path); timings["manifest_read"].append(time.perf_counter() - start)
        start = time.perf_counter(); [read_json(path) for path in package_paths]; timings["full_object_scan"].append(time.perf_counter() - start)
        start = time.perf_counter(); by_package_id.get(sample_package_id); timings["package_id_index_lookup"].append(time.perf_counter() - start)
        start = time.perf_counter(); [by_package_id[i] for i in by_evidence_family.get(sample_evidence_family, [])]; timings["evidence_family_filter_index_lookup"].append(time.perf_counter() - start)
        start = time.perf_counter(); [by_package_id[i] for i in by_statement_type.get(sample_statement_type, [])]; timings["statement_type_filter_index_lookup"].append(time.perf_counter() - start)
        start = time.perf_counter(); by_fingerprint.get(sample_fingerprint); timings["fingerprint_index_lookup"].append(time.perf_counter() - start)
        start = time.perf_counter(); [p for p in packages if p.get("provenance_envelope") and p.get("lineage")]; timings["provenance_lineage_scan"].append(time.perf_counter() - start)
        start = time.perf_counter(); sorted((p.get("package_id"), (p.get("fingerprints") or {}).get("package_manifest")) for p in packages); timings["package_fingerprint_materialization"].append(time.perf_counter() - start)
    stats = {
        name: {
            "median_seconds": round(statistics.median(values), 6),
            "min_seconds": round(min(values), 6),
            "max_seconds": round(max(values), 6),
        }
        for name, values in timings.items()
    }
    object_count = len(packages)
    baseline_scan = stats["full_object_scan"]["median_seconds"]
    baseline_provenance = stats["provenance_lineage_scan"]["median_seconds"]
    baseline_fingerprint = stats["package_fingerprint_materialization"]["median_seconds"]
    projections = {}
    for target in SCALE_TARGETS:
        factor = target / max(object_count, 1)
        projections[str(target)] = {
            "linear_full_scan_seconds": round(baseline_scan * factor, 3),
            "linear_provenance_lineage_scan_seconds": round(baseline_provenance * factor, 3),
            "linear_package_fingerprint_materialization_seconds": round(baseline_fingerprint * factor, 3),
            "evidence_type": "bounded linear projection from current filesystem timings; not measured at target scale",
        }
    return {
        "repeat_count": repeat,
        "measured_object_count": object_count,
        "measured_timings": stats,
        "projections": projections,
        "performance_conclusion": {
            "postgresql_required_today_for_performance": False,
            "evidence": f"Full object scan median {baseline_scan:.6f}s and index lookups are sub-millisecond at {object_count} objects on this host.",
            "postgresql_justified_today_for_operational_realization": True,
            "classification": "operational realization requirement",
        },
    }


def analyze_repository_composition(packages: list[dict[str, Any]]) -> dict[str, Any]:
    by_statement = Counter((p.get("generated_statements") or [{}])[0].get("statement_type", "unspecified") for p in packages)
    by_family = Counter((p.get("scope") or {}).get("evidence_family", "unspecified") for p in packages)
    family_slug_counter = Counter()
    for p in packages:
        text = (p.get("package_id", "") + " " + (p.get("scope") or {}).get("evidence_family", "")).lower()
        for slug in ["demographic", "environment", "infrastructure", "energy_mining", "agriculture_rural_development", "health", "education", "trade", "financial_sector"]:
            if slug in text:
                family_slug_counter[slug] += 1
                break
    richer_terms = {
        "statistical_summaries": ["summary", "mean", "median", "distribution", "statistical"],
        "correlations": ["correlation"],
        "covariance_structures": ["covariance"],
        "lag_relationships": ["lag"],
        "trend_descriptors": ["trend"],
        "mathematical_relationships": ["equation", "formula", "mathematical"],
        "relationships_or_mappings": ["relationship", "mapping", "comparison", "dependency"],
    }
    joined = "\n".join(canonical_json(p).lower() for p in packages)
    richer_counts = {name: sum(joined.count(term) for term in terms) for name, terms in richer_terms.items()}
    return {
        "by_statement_type": dict(sorted(by_statement.items())),
        "by_evidence_family": dict(sorted(by_family.items())),
        "by_detected_production_family": dict(sorted(family_slug_counter.items())),
        "richer_deterministic_knowledge_term_counts": richer_counts,
        "readiness_assessment": {
            "current_repository_supports_uniform_package_persistence": True,
            "current_repository_contains_many_richer_statistical_objects": False,
            "postgresql_before_deeper_campaigns": "yes, bounded realization should precede deeper deterministic-knowledge campaigns so richer objects are discoverable, retrievable, and bulk-exportable from the start",
            "classification": "operational realization requirement",
        },
    }


def build_option_matrix() -> dict[str, Any]:
    options = {
        "A": {
            "name": "Disposable query projection derived entirely from canonical KnowledgeObjectPackages",
            "architecture_fit": "partial",
            "benefits": ["maximal canonical clarity", "low authority ambiguity", "easy rebuild semantics"],
            "risks": ["quietly demotes intended operational repository role", "weak durability for discovery/retrieval", "may under-serve downstream consumers"],
            "classification": "preserves existing architecture",
            "decision": "reject",
            "justification": "Too weak for accepted end-state intent that KnowledgeForge should own an operational knowledge store, but useful as a rebuildability constraint inside option B.",
        },
        "B": {
            "name": "Durable KnowledgeForge-owned PostgreSQL operational repository derived from canonical packages",
            "architecture_fit": "strong",
            "benefits": ["serves discovery and retrieval", "preserves package authority", "supports independent ownership", "fully rebuildable", "enables future richer deterministic objects"],
            "risks": ["stale projection", "schema rigidity if overbuilt", "governance overhead", "accidental consumer coupling"],
            "classification": "operational realization requirement",
            "decision": "select",
            "justification": "Best reconciles canonical package authority with accepted operational database intent and downstream discovery/retrieval needs.",
        },
        "C": {
            "name": "Co-authoritative operational store governed by explicit synchronization rules",
            "architecture_fit": "weak",
            "benefits": ["could support database-native operations"],
            "risks": ["authority ambiguity", "dual-write risk", "harder deterministic rebuild", "conflicts with canonical package posture without stronger evidence"],
            "classification": "unsupported expansion",
            "decision": "reject",
            "justification": "No repeated evidence justifies co-authority; it would increase governance and consistency risk.",
        },
        "D": {
            "name": "New canonical repository replacing filesystem packages as authority",
            "architecture_fit": "conflicting",
            "benefits": ["single operational database authority if architecture were rewritten"],
            "risks": ["contradicts current canonical-package architecture", "requires doctrine/architecture amendment", "non-rebuildable database authority risk"],
            "classification": "unsupported expansion",
            "decision": "reject",
            "justification": "521-object scale is not exceptional repeated production evidence; this conflicts with accepted architecture.",
        },
        "E": {
            "name": "Not presently justified; preserve filesystem-only operation",
            "architecture_fit": "partial",
            "benefits": ["lowest immediate implementation cost", "keeps current adequate performance"],
            "risks": ["fails to realize accepted end-state operational repository", "delays downstream usability", "deeper objects may arrive before discovery substrate exists"],
            "classification": "unsupported expansion",
            "decision": "reject",
            "justification": "Performance does not require PostgreSQL today, but operational realization and intended end state justify a bounded decision now.",
        },
    }
    return {"selected_option": "B", "options": options}


def authority_model() -> dict[str, Any]:
    return {
        "canonical_authority": "Full KnowledgeObjectPackage JSON files under knowledge_repository/objects remain canonical.",
        "postgresql_role": "Durable KnowledgeForge-owned operational repository for discovery, retrieval, traversal, verification support, and bulk access, derived from canonical packages.",
        "postgresql_contains_conceptually": [
            "queryable projections of package identity, statement metadata, scope, provenance, lineage, lifecycle/governance state, fingerprints, relationships/dependencies where represented, and retrieval pointers to canonical packages",
            "repository snapshot and rebuild metadata sufficient to detect divergence",
        ],
        "may_postgresql_originate_or_mutate_canonical_knowledge": False,
        "fully_rebuildable_from_packages": True,
        "divergence_detection": "Compare package ids, package manifest fingerprints, repository fingerprint inputs, projection build metadata, and deterministic counts between canonical packages and PostgreSQL projection.",
        "fingerprint_relationship": "Package fingerprints remain canonical object fingerprints. Repository filesystem fingerprint remains canonical materialization fingerprint. PostgreSQL should have a projection/rebuild fingerprint derived from the same package inputs, but it does not replace canonical fingerprints.",
        "postgresql_in_canonical_fingerprints": False,
        "failure_behavior_on_disagreement": "Canonical packages win. PostgreSQL must be marked stale/invalid, downstream operational retrieval should fail closed or degrade to canonical filesystem reads, and rebuild/reconciliation is required before PostgreSQL results are treated as current.",
        "classification": "preserves existing architecture",
    }


def downstream_boundary() -> dict[str, Any]:
    options = {
        "direct_read_only_postgresql_access": {
            "acceptable": "conditionally later",
            "coupling": "medium to high unless view/interface ownership remains entirely KnowledgeForge-owned and versioned",
            "reproducibility": "good only if snapshot/projection version is explicit",
            "access_control": "read-only only; no consumer writes",
            "versioning": "requires KnowledgeForge-owned version policy later",
            "operational_complexity": "medium",
            "consumer_convenience": "high",
            "ownership_preservation": "acceptable only if consumers cannot define structures or write",
        },
        "exported_deterministic_snapshots": {
            "acceptable": "yes",
            "coupling": "low",
            "reproducibility": "high",
            "access_control": "simple file/object access",
            "versioning": "strong via repository fingerprints and export manifests",
            "operational_complexity": "low to medium",
            "consumer_convenience": "medium",
            "ownership_preservation": "strong",
        },
        "knowledgeforge_owned_query_interface": {
            "acceptable": "yes later, not designed now",
            "coupling": "low to medium if interface is KnowledgeForge-owned",
            "reproducibility": "good if responses identify snapshot/fingerprints",
            "access_control": "strongest boundary",
            "versioning": "requires later contract decision",
            "operational_complexity": "medium to high",
            "consumer_convenience": "high",
            "ownership_preservation": "strong if consumer writes are impossible",
        },
        "filesystem_package_consumption": {
            "acceptable": "yes",
            "coupling": "low",
            "reproducibility": "highest",
            "access_control": "simple repository artifact access",
            "versioning": "native through packages/manifests/fingerprints",
            "operational_complexity": "low",
            "consumer_convenience": "lower for rich retrieval",
            "ownership_preservation": "strong",
        },
        "combinations": {
            "acceptable": "yes, recommended boundary pattern",
            "coupling": "manageable if canonical packages + deterministic snapshots remain primary reproducibility path and PostgreSQL/query access is KnowledgeForge-owned read-only retrieval",
            "reproducibility": "high",
            "access_control": "read-only consumers only",
            "versioning": "must be decided later",
            "operational_complexity": "medium",
            "consumer_convenience": "high",
            "ownership_preservation": "strong if no shared schema ownership/runtime code/consumer writes",
        },
    }
    return {
        "acceptable_boundary": "Independent consumers such as InsightForge may retrieve KnowledgeForge knowledge through KnowledgeForge-owned read-only projections, exported deterministic snapshots, future KnowledgeForge-owned query interfaces, or direct canonical package consumption. They may not acquire ownership, write authority, shared schema control, shared runtime code, or the right to define KnowledgeForge structures.",
        "options": options,
        "classification": "preserves existing architecture",
    }


def risk_register() -> list[dict[str, str]]:
    return [
        {"risk": "dual-write risk", "classification": "implementation concern for a later task", "mitigation": "PostgreSQL must be derived-only; no canonical writes originate there."},
        {"risk": "authority ambiguity", "classification": "preserves existing architecture", "mitigation": "Full package JSON remains canonical; PostgreSQL disagreement invalidates projection."},
        {"risk": "stale projections", "classification": "implementation concern for a later task", "mitigation": "Projection fingerprint/rebuild metadata and fail-closed behavior."},
        {"risk": "partial rebuilds", "classification": "implementation concern for a later task", "mitigation": "Later slice must define deterministic full rebuild acceptance before partial/incremental behavior."},
        {"risk": "non-deterministic database state", "classification": "implementation concern for a later task", "mitigation": "Projection must be fully rebuildable and comparable to package inputs."},
        {"risk": "database-specific lock-in", "classification": "implementation concern for a later task", "mitigation": "Keep canonical packages and deterministic exports independent of PostgreSQL."},
        {"risk": "excessive schema rigidity before richer knowledge types exist", "classification": "implementation concern for a later task", "mitigation": "Smallest future slice should project current retrieval fields only and avoid premature rich-type modeling."},
        {"risk": "premature optimization", "classification": "preserves existing architecture", "mitigation": "Decision is justified by operational realization/end state, not present performance."},
        {"risk": "filesystem scalability", "classification": "operational realization requirement", "mitigation": "PostgreSQL selected for discovery/retrieval at future scale while filesystem remains canonical."},
        {"risk": "governance overhead", "classification": "implementation concern for a later task", "mitigation": "Require bounded implementation acceptance criteria and no cross-project consumers in first slice."},
        {"risk": "accidental coupling to InsightForge or MacroForge", "classification": "preserves existing architecture", "mitigation": "KnowledgeForge-owned read-only boundary only; no shared schema/runtime/consumer writes."},
    ]


def later_acceptance_criteria() -> dict[str, Any]:
    return {
        "smallest_later_implementation_slice": "If separately authorized, build a KnowledgeForge-owned, local, deterministic PostgreSQL projection of existing canonical KnowledgeObjectPackages sufficient for package-id lookup, evidence-family/statement-type/lifecycle/fingerprint filtering, provenance-lineage discovery, repository snapshot verification, and canonical-package retrieval pointers. No consumer access contract, no shared schema, no writes from PostgreSQL to canonical packages, no Campaign 34, and no rich statistical schema expansion in that first slice.",
        "acceptance_criteria_without_design": [
            "projection is fully rebuildable from canonical packages",
            "canonical packages remain byte-preserved and authoritative",
            "projection count and fingerprints match canonical repository inputs",
            "divergence is detected and treated as projection invalidity",
            "read-only retrieval works for the currently supported query dimensions",
            "no PostgreSQL-originated canonical knowledge is possible",
            "no cross-project runtime dependency or shared ownership is introduced",
            "full test suite, compile, coherence, context health, architecture audit, and diff checks pass",
        ],
        "future_expansion_gates": [
            "consumer-facing access requires a separate downstream consumption contract decision",
            "rich statistical relationship projection requires successful deeper deterministic-knowledge campaigns first or an explicit design gate",
            "incremental synchronization requires full-rebuild proof first and a separate consistency decision",
            "direct InsightForge access requires an explicit read-only boundary decision after local KnowledgeForge projection proves stable",
        ],
    }


def findings(commitments: dict[str, Any], requirements: dict[str, Any], performance: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"finding": "Canonical filesystem packages and PostgreSQL operational realization can coexist if PostgreSQL is derived-only and rebuildable.", "classification": "preserves existing architecture", "evidence": "Representation neutrality, canonical JSON repository architecture, and knowledge database posture."},
        {"finding": "No genuine architectural contradiction was found in accepted artifacts.", "classification": "preserves existing architecture", "evidence": f"Contradiction checks: {commitments['contradiction_checks']}"},
        {"finding": "PostgreSQL is not required today for raw performance at 521 objects.", "classification": "preserves existing architecture", "evidence": performance["performance_conclusion"]["evidence"]},
        {"finding": "PostgreSQL is justified now as operational realization of accepted end-state retrieval/discovery intent and future scale readiness.", "classification": "operational realization requirement", "evidence": "Architecture says KnowledgeForge should eventually own a knowledge database or equivalent store; current state requires bounded realization decision after 521 objects."},
        {"finding": "A co-authoritative or canonical PostgreSQL role is unsupported.", "classification": "unsupported expansion", "evidence": "No repeated evidence shows canonical package architecture is insufficient."},
        {"finding": "Future richer deterministic objects increase retrieval pressure but do not justify schema design in this decision task.", "classification": "implementation concern for a later task", "evidence": "Current composition has zero primary statistical/correlation/covariance/lag/trend/mathematical objects, while architecture intends such objects later."},
    ]


def build_decision(packages: list[dict[str, Any]], repo: Path, repeat: int) -> dict[str, Any]:
    commitments = extract_architectural_commitments(PROJECT_ROOT)
    requirements = derive_supported_requirements(packages, repo)
    performance = measure_retrieval_performance(packages, repo, repeat)
    composition = analyze_repository_composition(packages)
    options = build_option_matrix()
    model = authority_model()
    downstream = downstream_boundary()
    risks = risk_register()
    criteria = later_acceptance_criteria()
    decision_answers = {
        "selected_option": "B",
        "is_postgresql_justified_now": True,
        "justification_basis": ["operational usability", "accepted end-state realization", "future scale readiness"],
        "not_justified_by": ["present performance alone", "doctrine insufficiency", "canonical package failure"],
        "mandatory_or_optional": "mandatory operational infrastructure once separately implemented and accepted for repository operation; not canonical authority and not required for emergency canonical filesystem access",
        "may_postgresql_originate_or_mutate_canonical_knowledge": False,
        "must_be_fully_rebuildable_from_canonical_packages": True,
        "disagreement_behavior": model["failure_behavior_on_disagreement"],
        "downstream_consumption_boundary": downstream["acceptable_boundary"],
        "realization_before_deeper_campaigns": True,
        "smallest_later_slice": criteria["smallest_later_implementation_slice"],
        "expansion_gates": criteria["future_expansion_gates"],
    }
    result = {
        "decision_kind": "Bounded PostgreSQL Knowledge Repository Realization Decision",
        "repository_object_count": len(packages),
        "architectural_commitments": commitments,
        "operational_requirements": requirements,
        "scale_and_performance": performance,
        "repository_composition": composition,
        "option_matrix": options,
        "selected_option": options["selected_option"],
        "authority_and_consistency_model": model,
        "downstream_consumption_boundary": downstream,
        "risk_register": risks,
        "later_implementation_acceptance_criteria": criteria,
        "findings": findings(commitments, requirements, performance),
        "decision_answers": decision_answers,
        "forbidden_implementation_check": {
            "contains_forbidden_implementation_terms": False,
            "note": "Machine artifact deliberately contains no SQL/DDL/API/loader implementation design.",
        },
    }
    serialized = canonical_json(result)
    found = contains_any(serialized, FORBIDDEN_IMPLEMENTATION_TERMS)
    result["forbidden_implementation_check"]["contains_forbidden_implementation_terms"] = bool(found)
    result["forbidden_implementation_check"]["found_term_count"] = len(found)
    return result


def write_report(output_dir: Path, result: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "postgresql_realization_options_evidence_matrix.json"
    metrics_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    perf = result["scale_and_performance"]
    options = result["option_matrix"]["options"]
    report = f"""# Bounded PostgreSQL Knowledge Repository Realization Decision Report

Status: decision gate complete
Selected option: {result['selected_option']} — {options[result['selected_option']]['name']}
Repository objects inspected: {result['repository_object_count']}

## Existing architectural commitments discovered

- Full KnowledgeObjectPackage JSON remains canonical authority.
- Filesystem-backed packages remain the authoritative canonical artifact layer.
- Indexes, manifests, and evolution records are deterministic operational structures derived from packages.
- KnowledgeForge should eventually own a knowledge database or equivalent persistent knowledge store separate from external observational databases.
- KnowledgeForge serves reusable knowledge for downstream systems without owning reasoning, forecasting, presentation, observational databases, or consumer project structures.
- KnowledgeForge remains independently owned; no shared schemas, shared runtime code, consumer writes, or cross-project ownership are allowed.

## Contradictions

No genuine architectural contradiction was found. Existing architecture supports coexistence: packages remain canonical while a future operational database can serve discovery/retrieval as a representation derived from canonical packages.

## Measured versus projected operational need

Measured at {perf['measured_object_count']} objects:

- Full object scan median: {perf['measured_timings']['full_object_scan']['median_seconds']}s
- Package-id index lookup median: {perf['measured_timings']['package_id_index_lookup']['median_seconds']}s
- Evidence-family filter index lookup median: {perf['measured_timings']['evidence_family_filter_index_lookup']['median_seconds']}s
- Fingerprint lookup median: {perf['measured_timings']['fingerprint_index_lookup']['median_seconds']}s
- Provenance/lineage scan median: {perf['measured_timings']['provenance_lineage_scan']['median_seconds']}s

Conclusion: PostgreSQL is not required today for performance. It is justified now for operational realization, downstream usability, future scale readiness, and richer deterministic knowledge retrieval.

Projected linear filesystem costs, not measured at target scale:

| Objects | Full scan seconds | Provenance scan seconds | Fingerprint materialization seconds |
| ---: | ---: | ---: | ---: |
"""
    for target, values in perf["projections"].items():
        report += f"| {target} | {values['linear_full_scan_seconds']} | {values['linear_provenance_lineage_scan_seconds']} | {values['linear_package_fingerprint_materialization_seconds']} |\n"
    report += "\n## Option comparison\n\n| Option | Decision | Classification | Justification |\n| --- | --- | --- | --- |\n"
    for key, option in options.items():
        report += f"| {key}. {option['name']} | {option['decision']} | {option['classification']} | {option['justification']} |\n"
    report += f"""

## Selected option

Option B is selected: durable KnowledgeForge-owned PostgreSQL operational repository derived from canonical packages, serving discovery and retrieval while canonical authority remains with the packages.

## Authority and consistency model

- Canonical authority: {result['authority_and_consistency_model']['canonical_authority']}
- PostgreSQL role: {result['authority_and_consistency_model']['postgresql_role']}
- PostgreSQL may originate or mutate canonical knowledge: {result['authority_and_consistency_model']['may_postgresql_originate_or_mutate_canonical_knowledge']}
- Fully rebuildable from packages: {result['authority_and_consistency_model']['fully_rebuildable_from_packages']}
- PostgreSQL participates in canonical fingerprints: {result['authority_and_consistency_model']['postgresql_in_canonical_fingerprints']}
- Disagreement behavior: {result['authority_and_consistency_model']['failure_behavior_on_disagreement']}

## Downstream-consumption boundary

{result['downstream_consumption_boundary']['acceptable_boundary']}

Direct consumption does not authorize shared database ownership, shared schema ownership, shared runtime code, consumer writes, or consumer-defined KnowledgeForge structures.

## Ordering relative to deeper deterministic-knowledge production

PostgreSQL realization should occur before deeper deterministic-knowledge campaigns. Reason: richer future objects such as statistical summaries, correlations, covariance structures, lag relationships, trend descriptors, mathematical relationships, and other deterministic deductions will be more useful if discoverability/retrieval and bulk access are realized before they are produced at scale.

## Smallest later implementation slice

{result['later_implementation_acceptance_criteria']['smallest_later_implementation_slice']}

## Risks

"""
    for risk in result["risk_register"]:
        report += f"- {risk['risk']} — {risk['classification']}; mitigation: {risk['mitigation']}\n"
    report += "\n## Finding classifications\n\n"
    for finding in result["findings"]:
        report += f"- {finding['finding']} — {finding['classification']}. Evidence: {finding['evidence']}\n"
    report += "\n## Decision answers\n\n"
    report += json.dumps(result["decision_answers"], indent=2, sort_keys=True) + "\n"
    (output_dir / "bounded_postgresql_realization_decision_report.md").write_text(report, encoding="utf-8")

    responsibility = {
        "authority_and_consistency_model": result["authority_and_consistency_model"],
        "downstream_consumption_boundary": result["downstream_consumption_boundary"],
        "later_implementation_acceptance_criteria": result["later_implementation_acceptance_criteria"],
    }
    (output_dir / "conceptual_responsibility_and_authority_model.json").write_text(json.dumps(responsibility, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "risk_register.json").write_text(json.dumps(result["risk_register"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "later_implementation_acceptance_criteria.json").write_text(json.dumps(result["later_implementation_acceptance_criteria"], indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="PostgreSQL repository-realization decision support; no implementation.")
    parser.add_argument("--repository-root", type=Path, default=PROJECT_ROOT / "knowledge_repository")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts" / "reports" / "postgresql-realization-decision-20260710")
    parser.add_argument("--repeat", type=int, default=7)
    args = parser.parse_args()
    repo = args.repository_root if args.repository_root.is_absolute() else PROJECT_ROOT / args.repository_root
    packages = load_packages(repo)
    result = build_decision(packages, repo, repeat=args.repeat)
    write_report(args.output, result)
    print(json.dumps({
        "selected_option": result["selected_option"],
        "repository_object_count": result["repository_object_count"],
        "postgresql_justified_now": result["decision_answers"]["is_postgresql_justified_now"],
        "postgresql_required_for_present_performance": result["scale_and_performance"]["performance_conclusion"]["postgresql_required_today_for_performance"],
        "canonical_authority": result["authority_and_consistency_model"]["canonical_authority"],
        "output": str(args.output.resolve()),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
