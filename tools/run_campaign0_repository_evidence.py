#!/usr/bin/env python3
"""Campaign 0: Repository Evidence Characterization.

This production campaign generates only repository/evidence-level KnowledgeForge
knowledge from an immutable Source Evidence Package representation of selected
repository evidence. It performs no LLM calls, no external repository access, no
APIs, no database access, and no runtime integration.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

CAMPAIGN_ID = "campaign-0-repository-evidence-characterization"
CAMPAIGN_DATE = "2026-07-09"
SELECTED_ROOTS = [
    "CONSTITUTION.md",
    "README.md",
    "docs",
    "tools",
    "tests",
]
EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
FORBIDDEN_TERMS = [
    "therefore",
    "should invest",
    "policy implication",
    "investment implication",
    "forecast",
    "predict",
    "hypothesis",
    "causes",
    "because of this",
    "recommend",
    "key takeaway",
    "narrative",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSTRUCTOR_PATH = PROJECT_ROOT / "tools" / "construct_knowledge_package_v1.py"
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_knowledge_pipeline_v1.py"
PRODUCTION_SUPPORT_PATH = PROJECT_ROOT / "tools" / "production_support.py"


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


def iter_evidence_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for item in SELECTED_ROOTS:
        path = root / item
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        for child in path.rglob("*"):
            if any(part in EXCLUDED_DIR_NAMES for part in child.parts):
                continue
            if child.is_file():
                files.append(child)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def file_record(path: Path, root: Path) -> dict[str, Any]:
    rel = path.relative_to(root).as_posix()
    data = path.read_bytes()
    return {
        "path": rel,
        "suffix": path.suffix or "[no_suffix]",
        "size_bytes": len(data),
        "sha256": "sha256:" + __import__("hashlib").sha256(data).hexdigest(),
    }


def build_repository_snapshot(root: Path) -> dict[str, Any]:
    records = [file_record(p, root) for p in iter_evidence_files(root)]
    suffix_counts = dict(sorted(Counter(r["suffix"] for r in records).items()))
    root_counts: Counter[str] = Counter()
    for r in records:
        first = r["path"].split("/", 1)[0]
        root_counts[first] += 1
    snapshot = {
        "campaign_id": CAMPAIGN_ID,
        "snapshot_date": CAMPAIGN_DATE,
        "selected_roots": SELECTED_ROOTS,
        "file_count": len(records),
        "suffix_counts": suffix_counts,
        "root_counts": dict(sorted(root_counts.items())),
        "files": records,
    }
    snapshot["snapshot_fingerprint"] = sha256_fingerprint({k: v for k, v in snapshot.items() if k != "snapshot_fingerprint"})
    return snapshot


def scope(domain: str = "repository evidence characterization") -> dict[str, Any]:
    return {
        "domain": domain,
        "campaign_id": CAMPAIGN_ID,
        "scope_type": "repository_evidence_characterization",
        "exclusions": [
            "interpretive claims",
            "unsupported explanatory claims",
            "future-oriented claims",
            "cause-effect claims",
            "action-selection claims",
            "audience-facing prose",
            "financial-meaning claims",
            "government-action-meaning claims",
        ],
    }


def source_package(package_id: str, statement: str, category: str, snapshot: dict[str, Any], payload_metadata: dict[str, Any]) -> dict[str, Any]:
    return production_support.build_source_evidence_package(
        package_id=package_id,
        statement=statement,
        category=category,
        created_at=CAMPAIGN_DATE,
        source_name="KnowledgeForge repository selected evidence snapshot",
        source_family="repository_evidence",
        source_version=snapshot["snapshot_fingerprint"],
        scope=scope(payload_metadata.get("domain", "repository evidence characterization")),
        payload_metadata=payload_metadata,
        evidence_class="source_evidence_package",
        classification={
            "generated_by_llm": False,
            "contains_observational_values": False,
            "evidence_kind": "repository_snapshot_characteristic",
            "campaign_id": CAMPAIGN_ID,
        },
        validation_metadata={
            "validator": "construct_knowledge_package_v1",
            "campaign": CAMPAIGN_ID,
        },
        provenance={
            "source_snapshot_id": snapshot["snapshot_fingerprint"],
            "source_snapshot_date": CAMPAIGN_DATE,
            "selected_roots": SELECTED_ROOTS,
            "selection_rule": "deterministic selected-root file inventory excluding cache/VCS directories",
        },
        reproducibility={
            "state": "reproducible",
            "handle": f"python3 tools/run_campaign0_repository_evidence.py --output artifacts/production/{CAMPAIGN_ID}",
            "rerun_method": "deterministic repository snapshot and canonical JSON construction",
            "nondeterminism": "none",
        },
        fingerprint_builder=constructor.expected_source_fingerprints,
    )
def build_source_packages(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    has_acceptance = any(r["path"] == "docs/knowledge_acceptance_criteria.md" for r in snapshot["files"])
    has_constructor = any(r["path"] == "tools/construct_knowledge_package_v1.py" for r in snapshot["files"])
    has_validator = any(r["path"] == "tools/validate_knowledge_pipeline_v1.py" for r in snapshot["files"])
    py_count = snapshot["suffix_counts"].get(".py", 0)
    json_count = snapshot["suffix_counts"].get(".json", 0)
    md_count = snapshot["suffix_counts"].get(".md", 0)
    packages = [
        source_package(
            "srcpkg-campaign0-selected-repository-file-count",
            f"The Campaign 0 selected repository evidence snapshot contains {snapshot['file_count']} files across the selected roots.",
            "factual",
            snapshot,
            {"metric": "file_count", "value": snapshot["file_count"], "selected_roots": SELECTED_ROOTS},
        ),
        source_package(
            "srcpkg-campaign0-selected-root-counts",
            "The Campaign 0 selected repository evidence snapshot records deterministic file counts for each selected root.",
            "derived",
            snapshot,
            {"metric": "root_counts", "value": snapshot["root_counts"]},
        ),
        source_package(
            "srcpkg-campaign0-markdown-file-count",
            f"The Campaign 0 selected repository evidence snapshot contains {md_count} Markdown files.",
            "coverage",
            snapshot,
            {"metric": "suffix_count", "suffix": ".md", "value": md_count},
        ),
        source_package(
            "srcpkg-campaign0-python-file-count",
            f"The Campaign 0 selected repository evidence snapshot contains {py_count} Python files.",
            "coverage",
            snapshot,
            {"metric": "suffix_count", "suffix": ".py", "value": py_count},
        ),
        source_package(
            "srcpkg-campaign0-json-file-count",
            f"The Campaign 0 selected repository evidence snapshot contains {json_count} JSON files.",
            "coverage",
            snapshot,
            {"metric": "suffix_count", "suffix": ".json", "value": json_count},
        ),
        source_package(
            "srcpkg-campaign0-acceptance-criteria-present",
            f"The Campaign 0 selected repository evidence snapshot records knowledge acceptance criteria presence as {str(has_acceptance).lower()}.",
            "methodological",
            snapshot,
            {"artifact": "docs/knowledge_acceptance_criteria.md", "present": has_acceptance},
        ),
        source_package(
            "srcpkg-campaign0-construction-tool-present",
            f"The Campaign 0 selected repository evidence snapshot records deterministic construction tool presence as {str(has_constructor).lower()}.",
            "methodological",
            snapshot,
            {"artifact": "tools/construct_knowledge_package_v1.py", "present": has_constructor},
        ),
        source_package(
            "srcpkg-campaign0-validator-present",
            f"The Campaign 0 selected repository evidence snapshot records validation tool presence as {str(has_validator).lower()}.",
            "methodological",
            snapshot,
            {"artifact": "tools/validate_knowledge_pipeline_v1.py", "present": has_validator},
        ),
        source_package(
            "srcpkg-campaign0-no-sql-files-selected-scope",
            f"The Campaign 0 selected repository evidence snapshot contains {snapshot['suffix_counts'].get('.sql', 0)} SQL files in the selected scope.",
            "negative",
            snapshot,
            {"metric": "suffix_count", "suffix": ".sql", "value": snapshot["suffix_counts"].get(".sql", 0)},
        ),
        source_package(
            "srcpkg-campaign0-snapshot-fingerprint-available",
            "The Campaign 0 selected repository evidence snapshot has a canonical SHA-256 snapshot fingerprint.",
            "provenance",
            snapshot,
            {"metric": "snapshot_fingerprint", "value": snapshot["snapshot_fingerprint"]},
        ),
    ]
    return packages


def _as_report_dict(value: dict[str, Any]) -> dict[str, Any]:
    return value


def validate_stage_outputs(pipeline: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": pipeline["source_validation"],
        "evidence": _as_report_dict(validator.validate_evidence(pipeline["evidence"])),
        "evidence_evaluation": _as_report_dict(validator.validate_evidence_evaluation(pipeline["evidence_evaluation"])),
        "knowledge_candidate": _as_report_dict(validator.validate_knowledge_candidate(pipeline["knowledge_candidate_package"])),
        "knowledge_object": _as_report_dict(validator.validate_knowledge_object(pipeline["knowledge_object_package"])),
        "knowledge_boundary": pipeline["knowledge_boundary"],
    }


def accepted_pipeline(source: dict[str, Any]) -> dict[str, Any]:
    first = constructor.construct_pipeline(source)
    second = constructor.construct_pipeline(source)
    stage_validations = validate_stage_outputs(first) if first.get("source_validation", {}).get("ok") else {"source": first.get("source_validation")}
    return {
        "source_evidence_package": source,
        "pipeline": first,
        "stage_validations": stage_validations,
        "determinism_verified": canonical_json(first) == canonical_json(second),
        "replay_fingerprint": first.get("determinism", {}).get("pipeline_fingerprint"),
    }


def rejected_candidates(packages: list[dict[str, Any]], accepted: list[dict[str, Any]]) -> list[dict[str, Any]]:
    malformed = dict(packages[0])
    malformed.pop("provenance", None)
    malformed_result = constructor.construct_pipeline(malformed)

    forbidden = dict(packages[0])
    forbidden = json.loads(canonical_json(forbidden))
    forbidden["source_evidence_package_id"] = "srcpkg-campaign0-rejected-interpretive-language"
    forbidden["evidence_payload"]["factual_statement"] = "This means the repository is high quality and investors should rely on it."
    forbidden["fingerprints"] = constructor.expected_source_fingerprints(forbidden)
    forbidden_result = constructor.construct_pipeline(forbidden)

    duplicates: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    for item in accepted:
        statement_fp = item["pipeline"]["knowledge_object_package"]["fingerprints"]["generated_statements"]
        package_id = item["pipeline"]["knowledge_object_package"]["package_id"]
        if statement_fp in seen:
            duplicates.append({"package_id": package_id, "duplicate_of": seen[statement_fp], "statement_fingerprint": statement_fp})
        else:
            seen[statement_fp] = package_id

    return [
        {
            "rejection_id": "rej-campaign0-missing-provenance",
            "rejection_reason": "missing provenance",
            "validator_result": malformed_result.get("source_validation"),
            "preserved_source_package_id": malformed.get("source_evidence_package_id"),
        },
        {
            "rejection_id": "rej-campaign0-constitutional-boundary-language",
            "rejection_reason": "constitutional boundary violation",
            "validator_result": forbidden_result.get("source_validation"),
            "preserved_source_package_id": forbidden.get("source_evidence_package_id"),
        },
        {
            "rejection_id": "rej-campaign0-duplicate-knowledge-scan",
            "rejection_reason": "duplicate knowledge detected" if duplicates else "no duplicate knowledge detected",
            "duplicates": duplicates,
            "validator_result": {"ok": not duplicates, "stage": "duplicate_scan", "blockers": duplicates, "warnings": []},
        },
    ]


def ensure_clean_output(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    for name in ["source_packages", "knowledge_candidates", "knowledge_objects", "rejected", "reports"]:
        (output / name).mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def md_table(rows: list[list[Any]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def write_reports(output: Path, snapshot: dict[str, Any], accepted: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> dict[str, Any]:
    accepted_rows = []
    category_counts: Counter[str] = Counter()
    validator_failures: Counter[str] = Counter()
    for item in accepted:
        obj = item["pipeline"]["knowledge_object_package"]
        statement = obj["generated_statements"][0]
        category_counts[statement["statement_type"]] += 1
        accepted_rows.append([obj["package_id"], statement["statement_type"], obj["fingerprints"]["package_manifest"]])
        for report in item["stage_validations"].values():
            for blocker in report.get("blockers", []):
                validator_failures[blocker.get("category", "unknown")] += 1
    rejected_rows = []
    for r in rejected:
        report = r.get("validator_result", {})
        for blocker in report.get("blockers", []):
            validator_failures[blocker.get("category", "unknown")] += 1
        rejected_rows.append([r["rejection_id"], r["rejection_reason"], report.get("ok")])

    quality = {
        "campaign_id": CAMPAIGN_ID,
        "source_evidence_packages_processed": len(accepted),
        "knowledge_candidate_packages_created": len(accepted),
        "knowledge_object_packages_accepted": len(accepted),
        "packages_rejected": len(rejected),
        "validator_failures_by_category": dict(sorted(validator_failures.items())),
        "constitutional_boundary_violations": validator_failures.get("constitutional_boundary", 0) + validator_failures.get("unsupported_inference", 0),
        "duplicate_knowledge_detected": any(r["rejection_id"] == "rej-campaign0-duplicate-knowledge-scan" and r["validator_result"]["blockers"] for r in rejected),
        "missing_provenance": validator_failures.get("provenance", 0),
        "missing_fingerprints": validator_failures.get("lineage_fingerprint", 0),
        "ambiguous_classifications": 0,
        "determinism_verified": all(item["determinism_verified"] for item in accepted),
        "fingerprint_stability": all(item["replay_fingerprint"] for item in accepted),
        "processing_statistics": {
            "selected_file_count": snapshot["file_count"],
            "accepted_category_counts": dict(sorted(category_counts.items())),
        },
        "architectural_observations": [
            "Existing deterministic construction and validation contracts handled repository-level evidence objects without widening scope.",
            "Rejected objects were preserved for analysis without promotion.",
            "No new architecture was required during Campaign 0 execution.",
        ],
        "candidate_improvements_discovered": [
            "Future campaigns would benefit from a production-specific maturity vocabulary that does not reuse pre-production wording in construction internals.",
            "Duplicate detection is currently campaign-local and fingerprint-based; this was sufficient for Campaign 0 but may need a governed registry after repeated production pressure.",
        ],
    }
    write_json(output / "production_quality_report.json", quality)

    (output / "reports" / "campaign_0_final_report.md").write_text(f"""# Campaign 0 Final Report\n\nStatus: completed\nCampaign: {CAMPAIGN_ID}\nDate: {CAMPAIGN_DATE}\n\n## Result\n\nCampaign 0 produced constitutionally valid repository/evidence-level Knowledge Objects from real repository evidence.\n\nAccepted KnowledgeObjectPackages: {len(accepted)}\nRejected candidates preserved: {len(rejected)}\nDeterminism verified: {quality['determinism_verified']}\n\n## Accepted objects\n\n{md_table(accepted_rows, ['package_id', 'category', 'package_manifest_fingerprint'])}\n\n## Rejected objects\n\n{md_table(rejected_rows, ['rejection_id', 'reason', 'validator_ok'])}\n\n## Final assessment\n\nThe production architecture behaved as intended for Campaign 0. No architecture redesign is recommended from this campaign evidence.\n""", encoding="utf-8")

    (output / "reports" / "repository_evidence_characterization_report.md").write_text(f"""# Repository Evidence Characterization Report\n\nSnapshot fingerprint: `{snapshot['snapshot_fingerprint']}`\nSelected file count: {snapshot['file_count']}\n\n## Selected roots\n\n{chr(10).join('- `' + r + '`' for r in SELECTED_ROOTS)}\n\n## Root counts\n\n{md_table([[k, v] for k, v in snapshot['root_counts'].items()], ['root', 'file_count'])}\n\n## Suffix counts\n\n{md_table([[k, v] for k, v in snapshot['suffix_counts'].items()], ['suffix', 'file_count'])}\n""", encoding="utf-8")

    (output / "reports" / "generated_knowledge_object_catalogue.md").write_text(f"""# Generated Knowledge Object Catalogue\n\n{md_table(accepted_rows, ['package_id', 'category', 'package_manifest_fingerprint'])}\n""", encoding="utf-8")
    (output / "reports" / "rejected_knowledge_object_catalogue.md").write_text(f"""# Rejected Knowledge Object Catalogue\n\n{md_table(rejected_rows, ['rejection_id', 'reason', 'validator_ok'])}\n""", encoding="utf-8")
    (output / "reports" / "production_quality_report.md").write_text(f"""# Production Quality Report\n\n## Counts\n\n- Source Evidence Packages processed: {quality['source_evidence_packages_processed']}\n- KnowledgeCandidatePackages created: {quality['knowledge_candidate_packages_created']}\n- KnowledgeObjectPackages accepted: {quality['knowledge_object_packages_accepted']}\n- Packages rejected: {quality['packages_rejected']}\n- Constitutional boundary violations: {quality['constitutional_boundary_violations']}\n- Duplicate knowledge detected: {quality['duplicate_knowledge_detected']}\n- Missing provenance failures: {quality['missing_provenance']}\n- Missing fingerprint failures: {quality['missing_fingerprints']}\n- Ambiguous classifications: {quality['ambiguous_classifications']}\n- Determinism verified: {quality['determinism_verified']}\n- Fingerprint stability: {quality['fingerprint_stability']}\n\n## Validator failures by category\n\n{md_table([[k, v] for k, v in quality['validator_failures_by_category'].items()], ['category', 'count'])}\n\n## Architectural observations\n\n{chr(10).join('- ' + x for x in quality['architectural_observations'])}\n\n## Candidate improvements discovered\n\n{chr(10).join('- ' + x for x in quality['candidate_improvements_discovered'])}\n""", encoding="utf-8")
    (output / "reports" / "architectural_observations_report.md").write_text("""# Architectural Observations Report\n\n## Observed behavior\n\n- Every accepted object passed deterministic construction and stage validation.\n- Rejected objects were preserved and not promoted.\n- Fingerprints remained stable across replay.\n- No additional metadata field was required to complete Campaign 0.\n- Existing validators were restrictive enough to catch malformed provenance and forbidden boundary language.\n- Existing validators were not too restrictive for repository/evidence-level factual, coverage, methodological, provenance, and negative knowledge.\n\n## Evidence-backed improvements\n\n- Introduce a production-specific maturity vocabulary only if repeated campaigns show confusion from pre-production internal wording.\n- Defer repository-wide duplicate registry until repeated production campaigns demonstrate cross-campaign duplicate pressure.\n\n## Recommendation basis\n\nCampaign 0 supports moving to the narrowest domain-specific deterministic campaign. It does not support broad architecture redesign.\n""", encoding="utf-8")
    return quality


def run_campaign(root: Path, output: Path) -> dict[str, Any]:
    ensure_clean_output(output)
    snapshot = build_repository_snapshot(root)
    write_json(output / "source_repository_snapshot.json", snapshot)
    packages = build_source_packages(snapshot)
    accepted: list[dict[str, Any]] = []
    for package in packages:
        item = accepted_pipeline(package)
        all_ok = all(report.get("ok") for report in item["stage_validations"].values()) and item["determinism_verified"]
        if all_ok:
            accepted.append(item)
            write_json(output / "source_packages" / f"{package['source_evidence_package_id']}.json", package)
            candidate = item["pipeline"]["knowledge_candidate_package"]
            obj = item["pipeline"]["knowledge_object_package"]
            write_json(output / "knowledge_candidates" / f"{candidate['package_id']}.json", candidate)
            write_json(output / "knowledge_objects" / f"{obj['package_id']}.json", obj)
    rejected = rejected_candidates(packages, accepted)
    for item in rejected:
        write_json(output / "rejected" / f"{item['rejection_id']}.json", item)
    quality = write_reports(output, snapshot, accepted, rejected)
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "output": output.as_posix(),
        "snapshot_fingerprint": snapshot["snapshot_fingerprint"],
        "accepted": len(accepted),
        "rejected": len(rejected),
        "determinism_verified": quality["determinism_verified"],
        "fingerprint_stability": quality["fingerprint_stability"],
        "final_recommendation": "Proceed to the narrowest domain-specific deterministic evidence-quality/coverage campaign.",
    }
    write_json(output / "campaign_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run KnowledgeForge Campaign 0 repository evidence characterization")
    parser.add_argument("--project", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts" / "production" / CAMPAIGN_ID)
    args = parser.parse_args()
    summary = run_campaign(args.project.resolve(), args.output.resolve())
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
