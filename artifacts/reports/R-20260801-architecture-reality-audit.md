# Architecture-to-Reality Audit

Date: 2026-08-01T00:30:00+00:00
Project: /tmp/knowledgeforge-eppilot-sweden-infrastructure-v1-20260731/workspace
Mode: generated
Latest previous audit: artifacts/reports/R-20260731-architecture-reality-audit.md
Completed tasks since latest audit: 0

## Scope

This audit checks documented architecture, governance rules, operating procedures, state artifacts, templates, automation, logging/context systems, and available implementation for drift.

## Candidate attestation

This report attests the frozen audit subject identified below; it does not recursively hash itself or predict a final commit.

- Parent repository HEAD: `f96497c58903ba715908b33bfad87e5e72aa4995`
- Subject-manifest fingerprint: `sha256:d729a7cdb3f478b0e6b1d95ee8a9c48830f41ad07d7878d2b3d3dbf9706a8eb1`
- Subject path count: 57
- Canonical repository fingerprint: `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`
- Audit tool fingerprint: `sha256:3b704ac07262415f5e2eb21dd953898d151fb8129629d3377f31ad6731326192`
- Audit result: `generated`
- Workspace location (informational): `/tmp/knowledgeforge-eppilot-sweden-infrastructure-v1-20260731/workspace`
- Exact exclusions:
  - `artifacts/reports/R-20260801-architecture-reality-audit.md` — audit output depends on audit generation
  - `artifacts/reports/_SUMMARY.md` — mixed generated reports summary is represented separately and must list audit output
- Machine-readable attestation: `{"audit_result":"generated","audit_tool_fingerprint":"sha256:3b704ac07262415f5e2eb21dd953898d151fb8129629d3377f31ad6731326192","contract":"knowledgeforge.architecture_reality.candidate_attestation.v1@1.0","exclusions":[{"path":"artifacts/reports/R-20260801-architecture-reality-audit.md","reason":"audit output depends on audit generation"},{"path":"artifacts/reports/_SUMMARY.md","reason":"mixed generated reports summary is represented separately and must list audit output"}],"parent_repository_head":"f96497c58903ba715908b33bfad87e5e72aa4995","repository_fingerprint":"sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67","subject_manifest_fingerprint":"sha256:d729a7cdb3f478b0e6b1d95ee8a9c48830f41ad07d7878d2b3d3dbf9706a8eb1","subject_path_count":57,"workspace_location_informational":"/tmp/knowledgeforge-eppilot-sweden-infrastructure-v1-20260731/workspace"}`

## Categories

- architecture_vs_implementation
- state_files_vs_reality
- agent_instructions_vs_behavior
- logging_systems
- context_management_systems
- governance_processes
- automation_workflows
- templates_vs_generated_projects

## Drift types

- drift
- obsolete_documentation
- duplicated_systems
- unused_systems
- missing_implementation
- implementation_without_documentation
- documentation_without_implementation

## Blocks

None.

## Warnings

None.

## Remediation workflow

1. Fix blocks before major architecture/governance work continues.
2. Convert durable policy or architecture changes into decision artifacts.
3. Update implementation, templates, docs, and state together so future projects inherit the correction.
4. Refresh affected folder summaries and latest handoff.
5. Rerun `tools/architecture_reality_audit.py`, `tools/check_coherence.py`, and relevant tests.
