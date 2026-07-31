#!/usr/bin/env python3
"""Architecture-to-Reality Audit for ProjectForge projects.

This is a lightweight automated drift detector. It does not replace human or
cloud-governance review; it creates an evidence-backed checklist and catches the
mechanical cases that routinely cause architecture/governance drift.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

AUDIT_CATEGORIES = [
    "architecture_vs_implementation",
    "state_files_vs_reality",
    "agent_instructions_vs_behavior",
    "logging_systems",
    "context_management_systems",
    "governance_processes",
    "automation_workflows",
    "templates_vs_generated_projects",
]

DRIFT_TYPES = [
    "drift",
    "obsolete_documentation",
    "duplicated_systems",
    "unused_systems",
    "missing_implementation",
    "implementation_without_documentation",
    "documentation_without_implementation",
]

REQUIRED_PROCESS_PHRASES = [
    "Architecture-to-Reality Audit",
    "every 5-10 completed tasks",
    "before major architecture changes",
    "before major governance reviews",
]

ROOT_TOOL_REQUIRED = [
    "tools/check_coherence.py",
    "tools/context_health.py",
    "tools/build_context.py",
    "tools/architecture_reality_audit.py",
]

GENERATED_TOOL_REQUIRED = [
    "tools/check_coherence.py",
    "tools/context_health.py",
    "tools/build_context.py",
    "tools/architecture_reality_audit.py",
]

POLICY_FILES = [
    "CONSTITUTION.md",
    "AGENTS.md",
    "context/context_policy.yaml",
    "docs/OPERATOR_MANUAL.md",
    "automation/orchestration_schedule.yaml",
]

TEMPLATE_POLICY_FILES = [
    "templates/_shared_project/AGENTS.md",
    "templates/_shared_project/context/context_policy.yaml",
    "templates/_shared_project/instructions/GENERAL_INSTRUCTIONS.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def byte_fingerprint(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def value_fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _contained_regular_file(project: Path, relative_path: str) -> Path:
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"audit subject path is not repository-relative: {relative_path}")
    root = project.resolve(strict=True)
    try:
        resolved = (root / relative).resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ValueError(f"audit subject path escapes or is missing: {relative_path}") from exc
    if not resolved.is_file():
        raise ValueError(f"audit subject path is not a regular file: {relative_path}")
    return resolved


def _git_mode(path: Path) -> str:
    return "100755" if path.stat().st_mode & 0o111 else "100644"


def audit_subject_fingerprint(manifest: dict[str, Any]) -> str:
    return value_fingerprint({key: value for key, value in manifest.items() if key != "subject_manifest_fingerprint"})


def _validate_exclusions(exclusions: list[dict[str, str]]) -> None:
    if not isinstance(exclusions, list) or len(exclusions) != 2:
        raise ValueError("audit subject must declare exactly audit-output and reports-summary exclusions")
    paths = sorted(row.get("path") for row in exclusions if isinstance(row, dict))
    audit_paths = [path for path in paths if isinstance(path, str) and re.fullmatch(r"artifacts/reports/R-\d{8}-architecture-reality-audit\.md", path)]
    if len(audit_paths) != 1 or "artifacts/reports/_SUMMARY.md" not in paths:
        raise ValueError("audit subject exclusion set must contain only its audit output and reports summary")
    if any(not isinstance(row.get("reason"), str) or not row["reason"].strip() for row in exclusions):
        raise ValueError("every audit subject exclusion requires a reason")


def build_audit_subject_manifest(
    project: Path, paths: list[str], *, parent_head: str, repository_fingerprint: str,
    exclusions: list[dict[str, str]],
) -> dict[str, Any]:
    _validate_exclusions(exclusions)
    excluded_paths = {row["path"] for row in exclusions}
    normalized = sorted(set(paths))
    if len(normalized) != len(paths):
        raise ValueError("audit subject paths must be unique")
    if excluded_paths.intersection(normalized):
        raise ValueError("excluded paths must not appear in audit subject")
    subject_paths = []
    for relative in normalized:
        path = _contained_regular_file(project, relative)
        subject_paths.append({"path": relative, "mode": _git_mode(path), "blob_sha256": byte_fingerprint(path)})
    manifest = {
        "schema_name": "knowledgeforge.architecture_reality.audit_subject_manifest.v1",
        "schema_version": "1.0", "parent_repository_head": parent_head,
        "repository_fingerprint": repository_fingerprint, "subject_paths": subject_paths,
        "subject_path_count": len(subject_paths),
        "exclusions": sorted(exclusions, key=lambda row: row["path"]),
    }
    manifest["subject_manifest_fingerprint"] = audit_subject_fingerprint(manifest)
    return manifest


def verify_audit_subject_manifest(project: Path, manifest: Any) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise ValueError("audit subject manifest must be a JSON object")
    if manifest.get("schema_name") != "knowledgeforge.architecture_reality.audit_subject_manifest.v1" or manifest.get("schema_version") != "1.0":
        raise ValueError("audit subject schema or version mismatch")
    _validate_exclusions(manifest.get("exclusions"))
    rows = manifest.get("subject_paths")
    if not isinstance(rows, list) or manifest.get("subject_path_count") != len(rows):
        raise ValueError("audit subject path count mismatch")
    if [row.get("path") for row in rows] != sorted(row.get("path") for row in rows):
        raise ValueError("audit subject paths must be sorted")
    excluded = {row["path"] for row in manifest["exclusions"]}
    if excluded.intersection(row.get("path") for row in rows):
        raise ValueError("excluded path appears in audit subject")
    for row in rows:
        path = _contained_regular_file(project, row.get("path"))
        if row.get("mode") != _git_mode(path) or row.get("blob_sha256") != byte_fingerprint(path):
            raise ValueError(f"audit subject blob or mode mismatch: {row.get('path')}")
    if manifest.get("subject_manifest_fingerprint") != audit_subject_fingerprint(manifest):
        raise ValueError("audit subject manifest fingerprint mismatch")
    return {"valid": True, "subject_path_count": len(rows), "subject_manifest_fingerprint": manifest["subject_manifest_fingerprint"]}


def audit_attestation(subject_manifest: dict[str, Any], tool_fingerprint: str, workspace: str | None = None) -> dict[str, Any]:
    return {
        "contract": "knowledgeforge.architecture_reality.candidate_attestation.v1@1.0",
        "parent_repository_head": subject_manifest["parent_repository_head"],
        "subject_manifest_fingerprint": subject_manifest["subject_manifest_fingerprint"],
        "subject_path_count": subject_manifest["subject_path_count"],
        "exclusions": copy_exclusions(subject_manifest["exclusions"]),
        "repository_fingerprint": subject_manifest["repository_fingerprint"],
        "audit_tool_fingerprint": tool_fingerprint, "audit_result": "generated",
        "workspace_location_informational": workspace,
    }


def copy_exclusions(value: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{"path": row["path"], "reason": row["reason"]} for row in value]


def verify_audit_report_binding(project: Path, audit_report_path: str, subject_manifest: dict[str, Any]) -> dict[str, Any]:
    text = read(_contained_regular_file(project, audit_report_path))
    match = re.search(r"Machine-readable attestation: `([^\n]+)`", text)
    if not match:
        raise ValueError("architecture audit lacks machine-readable candidate attestation")
    try:
        attestation = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError("architecture audit candidate attestation is malformed") from exc
    tool_rows = [row for row in subject_manifest["subject_paths"] if row.get("path") == "tools/architecture_reality_audit.py"]
    if len(tool_rows) != 1:
        raise ValueError("frozen audit subject must contain exactly one architecture audit tool")
    expected_tool_fingerprint = tool_rows[0].get("blob_sha256")
    expected = audit_attestation(subject_manifest, expected_tool_fingerprint, attestation.get("workspace_location_informational"))
    if attestation != expected:
        raise ValueError("architecture audit tool identity or frozen-subject attestation mismatch")
    return {"valid": True, "subject_manifest_fingerprint": subject_manifest["subject_manifest_fingerprint"]}


def final_manifest_fingerprint(manifest: dict[str, Any]) -> str:
    return value_fingerprint({key: value for key, value in manifest.items() if key != "final_manifest_fingerprint"})


def build_final_candidate_manifest(
    project: Path, paths: list[str], subject_manifest: dict[str, Any], audit_report_path: str,
    reports_summary_path: str,
) -> dict[str, Any]:
    verify_audit_subject_manifest(project, subject_manifest)
    verify_audit_report_binding(project, audit_report_path, subject_manifest)
    required = {row["path"] for row in subject_manifest["subject_paths"]} | {audit_report_path, reports_summary_path}
    if set(paths) != required or len(paths) != len(required):
        raise ValueError("final candidate paths must exactly equal the audited subject plus audit and reports summary")
    rows = []
    for relative in sorted(set(paths)):
        path = _contained_regular_file(project, relative)
        rows.append({"path": relative, "mode": _git_mode(path), "blob_sha256": byte_fingerprint(path)})
    if Path(audit_report_path).name not in read(project / reports_summary_path):
        raise ValueError("reports summary does not list architecture audit")
    manifest = {
        "schema_name": "knowledgeforge.prospective_publication_manifest.v3", "schema_version": "1.0",
        "subject_manifest_fingerprint": subject_manifest["subject_manifest_fingerprint"],
        "audit_report_path": audit_report_path, "reports_summary_path": reports_summary_path,
        "path_count": len(rows), "paths": rows,
    }
    manifest["final_manifest_fingerprint"] = final_manifest_fingerprint(manifest)
    return manifest


def verify_final_candidate_manifest(
    project: Path, manifest: Any, subject_manifest: dict[str, Any], audit_report_path: str,
    reports_summary_path: str,
) -> dict[str, Any]:
    if not isinstance(manifest, dict) or manifest.get("schema_name") != "knowledgeforge.prospective_publication_manifest.v3" or manifest.get("schema_version") != "1.0":
        raise ValueError("final candidate manifest schema or version mismatch")
    verify_audit_subject_manifest(project, subject_manifest)
    verify_audit_report_binding(project, audit_report_path, subject_manifest)
    if manifest.get("subject_manifest_fingerprint") != subject_manifest["subject_manifest_fingerprint"]:
        raise ValueError("final candidate audit-subject binding mismatch")
    if manifest.get("audit_report_path") != audit_report_path or manifest.get("reports_summary_path") != reports_summary_path:
        raise ValueError("final candidate audit or summary binding mismatch")
    rows = manifest.get("paths")
    if not isinstance(rows, list) or manifest.get("path_count") != len(rows):
        raise ValueError("final candidate path count mismatch")
    required = {row["path"] for row in subject_manifest["subject_paths"]} | {audit_report_path, reports_summary_path}
    row_paths = [row.get("path") for row in rows if isinstance(row, dict)]
    if len(row_paths) != len(rows) or row_paths != sorted(required) or len(row_paths) != len(set(row_paths)):
        raise ValueError("final candidate paths must be the exact canonical sorted unique set")
    for row in rows:
        if set(row) != {"path", "mode", "blob_sha256"}:
            raise ValueError("final candidate path row schema is not exact")
        path = _contained_regular_file(project, row.get("path"))
        if row.get("mode") != _git_mode(path) or row.get("blob_sha256") != byte_fingerprint(path):
            raise ValueError(f"final candidate blob or mode mismatch: {row.get('path')}")
    if Path(audit_report_path).name not in read(project / reports_summary_path):
        raise ValueError("reports summary does not list architecture audit")
    if manifest.get("final_manifest_fingerprint") != final_manifest_fingerprint(manifest):
        raise ValueError("final candidate manifest fingerprint mismatch")
    return {"valid": True, "path_count": len(rows), "final_manifest_fingerprint": manifest["final_manifest_fingerprint"]}


def has(path: Path, text: str) -> bool:
    return text.lower() in read(path).lower()


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


def add(items: list[dict[str, str]], severity: str, category: str, drift_type: str, message: str, remediation: str) -> None:
    items.append({
        "severity": severity,
        "category": category,
        "drift_type": drift_type,
        "message": message,
        "remediation": remediation,
    })


def latest_architecture_audit(project: Path, exclude: Path | None = None) -> Path | None:
    excluded = exclude.resolve() if exclude is not None else None
    reports = sorted(path for path in (project / "artifacts" / "reports").glob("R-*-architecture-reality-audit.md") if excluded is None or path.resolve() != excluded)
    return reports[-1] if reports else None


def completed_tasks_since(project: Path, since: Path | None) -> int:
    since_time = since.stat().st_mtime if since and since.exists() else 0.0
    count = 0
    for task in (project / "artifacts" / "tasks").glob("*.md"):
        if task.name == "_SUMMARY.md":
            continue
        text = read(task).lower()
        if ("status: completed" in text or "status: done" in text or "completed:" in text) and task.stat().st_mtime >= since_time:
            count += 1
    return count


def detect_mode(project: Path) -> str:
    return "root" if (project / "projectforge.yaml").exists() else "generated"


def check_process_documented(project: Path, mode: str, findings: list[dict[str, str]]) -> None:
    files = POLICY_FILES if mode == "root" else ["AGENTS.md", "context/context_policy.yaml", "instructions/GENERAL_INSTRUCTIONS.md"]
    combined = "\n".join(read(project / rel) for rel in files)
    for phrase in REQUIRED_PROCESS_PHRASES:
        if phrase.lower() not in combined.lower():
            add(
                findings,
                "block" if phrase == "Architecture-to-Reality Audit" else "warn",
                "governance_processes",
                "documentation_without_implementation",
                f"Architecture audit process phrase missing from policy/instructions: {phrase}",
                "Document the Architecture-to-Reality Audit cadence, triggers, recording location, and remediation workflow in AGENTS/context policy/operator instructions.",
            )


def check_tools_and_automation(project: Path, mode: str, findings: list[dict[str, str]]) -> None:
    required = ROOT_TOOL_REQUIRED if mode == "root" else GENERATED_TOOL_REQUIRED
    for rel in required:
        if not (project / rel).exists():
            add(findings, "block", "automation_workflows", "missing_implementation", f"Required audit/coherence tool missing: {rel}", "Copy the current ProjectForge tool from templates or restore it before relying on automated governance checks.")

    if mode == "root":
        schedule = project / "automation" / "orchestration_schedule.yaml"
        if not has(schedule, "architecture_reality_audit"):
            add(findings, "block", "automation_workflows", "missing_implementation", "orchestration schedule does not run architecture_reality_audit", "Add Architecture-to-Reality Audit to periodic and pre-major-governance automation.")
        hygiene = project / "tools" / "orchestrator_hygiene.py"
        if not has(hygiene, "architecture_reality_audit.py"):
            add(findings, "warn", "automation_workflows", "implementation_without_documentation", "orchestrator_hygiene.py does not invoke architecture_reality_audit.py", "Add the audit command to periodic/all hygiene phases so routine automation can execute it.")


def check_context_and_state(project: Path, findings: list[dict[str, str]]) -> None:
    state_files = ["state/active_goal.md", "state/project_state.md", "state/architecture.md"]
    for rel in state_files:
        p = project / rel
        if not p.exists():
            add(findings, "block", "state_files_vs_reality", "missing_implementation", f"Missing primary state file: {rel}", "Restore the primary state artifact or regenerate the project scaffold.")
            continue
        text = read(p)
        if estimate_tokens(text) > 3500:
            add(findings, "warn", "state_files_vs_reality", "drift", f"{rel} is large for a current-state artifact (~{estimate_tokens(text)} tokens)", "Summarize current truth in state and move history/evidence to task artifacts, reports, handoffs, or derived logs.")
        historical_markers = len(re.findall(r"\b(completed|implemented|verification|changed files|diff|commit|log)\b", text, flags=re.I))
        if historical_markers > 20:
            add(findings, "warn", "state_files_vs_reality", "obsolete_documentation", f"{rel} appears to accumulate implementation history", "Keep only active/current pointers in state; move historical details to reports or task artifacts.")

    if not has(project / "context" / "context_policy.yaml", "context_loading_hierarchy"):
        add(findings, "block", "context_management_systems", "documentation_without_implementation", "context policy lacks explicit context_loading_hierarchy", "Upgrade context/context_policy.yaml from current ProjectForge templates.")
    if not has(project / "context" / "context_policy.yaml", "architecture_reality_audit"):
        add(findings, "warn", "governance_processes", "documentation_without_implementation", "context policy lacks Architecture-to-Reality Audit governance settings", "Add architecture_reality_audit policy with cadence, categories, and report location.")


def check_agent_instruction_alignment(project: Path, mode: str, findings: list[dict[str, str]]) -> None:
    agent_files = list((project / "agents").glob("*.md")) if (project / "agents").exists() else []
    if not agent_files:
        add(findings, "warn", "agent_instructions_vs_behavior", "missing_implementation", "No role agent instruction files found under agents/", "Generated projects should inherit role prompts or document why this project uses only AGENTS.md.")
        return
    for p in agent_files:
        if p.name.startswith("_"):
            continue
        txt = read(p).lower()
        if "context used" not in txt:
            add(findings, "warn", "agent_instructions_vs_behavior", "drift", f"{p.relative_to(project)} does not require Context used reporting", "Update role prompt from ProjectForge templates or add explicit Context used reporting.")
        if "architecture-to-reality" not in txt and p.name in {"auditor.md", "reviewer.md", "planner.md"}:
            add(findings, "warn", "agent_instructions_vs_behavior", "documentation_without_implementation", f"{p.relative_to(project)} does not mention Architecture-to-Reality Audit triggers", "Add audit-trigger guidance to governance/review/planning roles.")


def check_logging_and_metrics(project: Path, findings: list[dict[str, str]]) -> None:
    if not has(project / "logs" / "logging_policy.yaml", "raw"):
        add(findings, "warn", "logging_systems", "obsolete_documentation", "logging policy does not clearly define raw operational logs", "Clarify logs/raw vs logs/derived separation in logs/logging_policy.yaml.")
    if not has(project / "metrics" / "metrics_policy.yaml", "derived"):
        add(findings, "warn", "logging_systems", "obsolete_documentation", "metrics policy does not clearly define metrics as derived evidence", "Clarify metrics as derived evidence, not raw logs.")


def check_templates(project: Path, mode: str, findings: list[dict[str, str]]) -> None:
    if mode != "root":
        return
    for rel in TEMPLATE_POLICY_FILES:
        if not (project / rel).exists():
            add(findings, "block", "templates_vs_generated_projects", "missing_implementation", f"Template policy file missing: {rel}", "Restore shared generated-project template file.")
            continue
        if not has(project / rel, "Architecture-to-Reality Audit"):
            add(findings, "block", "templates_vs_generated_projects", "documentation_without_implementation", f"Template does not inherit Architecture-to-Reality Audit guidance: {rel}", "Patch shared template so future generated projects inherit the audit process.")
    for rel in ["templates/_shared_project/tools/architecture_reality_audit.py", "templates/_shared_project/tools/check_coherence.py"]:
        if not (project / rel).exists():
            add(findings, "block", "templates_vs_generated_projects", "missing_implementation", f"Generated-project template missing tool: {rel}", "Copy root tool into templates/_shared_project/tools/.")


def check_architecture_docs(project: Path, findings: list[dict[str, str]]) -> None:
    arch = project / "state" / "architecture.md"
    if not arch.exists():
        return
    arch_text = read(arch).lower()
    implementation_markers = ["tools/", "context/", "agents/", "templates/", "logs/", "metrics/"]
    missing = [m for m in implementation_markers if m.rstrip("/") in arch_text and not (project / m).exists()]
    for marker in missing:
        add(findings, "warn", "architecture_vs_implementation", "documentation_without_implementation", f"architecture.md references {marker} but path is missing", "Either restore the implementation path or update architecture.md to reflect current reality.")
    if "architecture-to-reality" in "\n".join(read(project / rel) for rel in POLICY_FILES if (project / rel).exists()).lower() and not (project / "tools" / "architecture_reality_audit.py").exists():
        add(findings, "block", "architecture_vs_implementation", "documentation_without_implementation", "Architecture-to-Reality Audit is documented but the tool is missing", "Restore tools/architecture_reality_audit.py.")


def check(project: Path, *, exclude_audit: Path | None = None, timestamp: str | None = None) -> dict[str, Any]:
    project = project.resolve()
    mode = detect_mode(project)
    findings: list[dict[str, str]] = []
    latest = latest_architecture_audit(project, exclude=exclude_audit)
    completed = completed_tasks_since(project, latest)

    check_process_documented(project, mode, findings)
    check_tools_and_automation(project, mode, findings)
    check_context_and_state(project, findings)
    check_agent_instruction_alignment(project, mode, findings)
    check_logging_and_metrics(project, findings)
    check_templates(project, mode, findings)
    check_architecture_docs(project, findings)

    if completed >= 10:
        add(findings, "block", "governance_processes", "drift", f"{completed} completed task(s) since last Architecture-to-Reality Audit", "Run and record an Architecture-to-Reality Audit before continuing major work.")
    elif completed >= 5:
        add(findings, "warn", "governance_processes", "drift", f"{completed} completed task(s) since last Architecture-to-Reality Audit", "Schedule an Architecture-to-Reality Audit soon; cadence is every 5-10 completed tasks.")

    blocks = [f for f in findings if f["severity"] == "block"]
    warnings = [f for f in findings if f["severity"] == "warn"]
    return {
        "project": str(project),
        "mode": mode,
        "timestamp": timestamp or dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "audit_categories": AUDIT_CATEGORIES,
        "drift_types": DRIFT_TYPES,
        "latest_architecture_reality_audit": str(latest.relative_to(project)) if latest else None,
        "completed_tasks_since_latest_audit": completed,
        "blocks": blocks,
        "warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Architecture-to-Reality Audit",
        "",
        f"Date: {report['timestamp']}",
        f"Project: {report['project']}",
        f"Mode: {report['mode']}",
        f"Latest previous audit: {report['latest_architecture_reality_audit'] or 'none'}",
        f"Completed tasks since latest audit: {report['completed_tasks_since_latest_audit']}",
        "",
        "## Scope",
        "",
        "This audit checks documented architecture, governance rules, operating procedures, state artifacts, templates, automation, logging/context systems, and available implementation for drift.",
    ]
    if "attestation" in report:
        attestation = report["attestation"]
        lines.extend([
            "", "## Candidate attestation", "",
            "This report attests the frozen audit subject identified below; it does not recursively hash itself or predict a final commit.",
            "",
            f"- Parent repository HEAD: `{attestation['parent_repository_head']}`",
            f"- Subject-manifest fingerprint: `{attestation['subject_manifest_fingerprint']}`",
            f"- Subject path count: {attestation['subject_path_count']}",
            f"- Canonical repository fingerprint: `{attestation['repository_fingerprint']}`",
            f"- Audit tool fingerprint: `{attestation['audit_tool_fingerprint']}`",
            f"- Audit result: `{attestation['audit_result']}`",
            f"- Workspace location (informational): `{attestation.get('workspace_location_informational') or 'not-recorded'}`",
            "- Exact exclusions:",
        ])
        lines.extend(f"  - `{row['path']}` — {row['reason']}" for row in attestation["exclusions"])
        lines.append(f"- Machine-readable attestation: `{canonical_json(attestation)}`")
    lines.extend(["", "## Categories", ""])
    lines.extend(f"- {cat}" for cat in report["audit_categories"])
    lines.extend(["", "## Drift types", ""])
    lines.extend(f"- {kind}" for kind in report["drift_types"])
    for title, key in [("Blocks", "blocks"), ("Warnings", "warnings")]:
        lines.extend(["", f"## {title}", ""])
        if not report[key]:
            lines.append("None.")
        for item in report[key]:
            lines.extend([
                f"- Category: {item['category']}",
                f"  Drift type: {item['drift_type']}",
                f"  Finding: {item['message']}",
                f"  Remediation: {item['remediation']}",
            ])
    lines.extend([
        "",
        "## Remediation workflow",
        "",
        "1. Fix blocks before major architecture/governance work continues.",
        "2. Convert durable policy or architecture changes into decision artifacts.",
        "3. Update implementation, templates, docs, and state together so future projects inherit the correction.",
        "4. Refresh affected folder summaries and latest handoff.",
        "5. Rerun `tools/architecture_reality_audit.py`, `tools/check_coherence.py`, and relevant tests.",
    ])
    return "\n".join(lines) + "\n"


def write_report(project: Path, report: dict[str, Any], output_path: Path | None = None) -> Path:
    today = report["timestamp"][:10].replace("-", "")
    out = output_path or project / "artifacts" / "reports" / f"R-{today}-architecture-reality-audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(report), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Run ProjectForge Architecture-to-Reality Audit.")
    ap.add_argument("--project", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-report", action="store_true", help="Write artifacts/reports/R-YYYYMMDD-architecture-reality-audit.md")
    ap.add_argument("--output-path", help="Explicit report output path; must remain under the project")
    ap.add_argument("--subject-manifest", help="Frozen Audit Subject Manifest JSON")
    ap.add_argument("--timestamp", help="Explicit ISO timestamp for deterministic regeneration")
    ns = ap.parse_args()

    project = Path(ns.project).resolve()
    output_path = Path(ns.output_path).resolve() if ns.output_path else None
    if ns.write_report and output_path is None:
        date_text = (ns.timestamp[:10] if ns.timestamp else dt.date.today().isoformat()).replace("-", "")
        output_path = project / "artifacts" / "reports" / f"R-{date_text}-architecture-reality-audit.md"
    if output_path is not None:
        try:
            output_path.relative_to(project)
        except ValueError as exc:
            raise ValueError("audit output path must remain under project root") from exc
    report = check(project, exclude_audit=output_path, timestamp=ns.timestamp)
    if ns.subject_manifest:
        subject = json.loads(Path(ns.subject_manifest).read_text())
        verify_audit_subject_manifest(project, subject)
        report["attestation"] = audit_attestation(subject, byte_fingerprint(Path(__file__).resolve()), str(project))
    report_path = None
    if ns.write_report:
        report_path = write_report(project, report, output_path=output_path)
        report["report_path"] = str(report_path)

    if ns.json:
        print(json.dumps(report, indent=2))
    else:
        if report_path:
            print(f"Report: {report_path}")
        for item in report["blocks"]:
            print(f"BLOCK: {item['message']}", file=sys.stderr)
        for item in report["warnings"]:
            print(f"WARN: {item['message']}")
        print(f"architecture-reality-audit: {len(report['blocks'])} block(s), {len(report['warnings'])} warning(s)")
    return 2 if report["blocks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
